"""CREDID GUARDIAN CODEX (CGC): synthetic normalization and protocol tests."""
import copy
import json
from pathlib import Path
import unittest

from cgc.quota import QuotaError, normalize, read_quota

FIXTURE = Path(__file__).parent / 'fixtures/quota.json'
STAMP = '2026-09-17T00:00:00Z'

class QuotaTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(FIXTURE.read_text())

    def norm(self, raw=None):
        return normalize(self.raw if raw is None else raw, observed_at=STAMP, mode='synthetic')

    def test_single_window(self):
        r=self.norm({'rateLimits':{'primary':{'usedPercent':63}}})
        self.assertEqual(len(r['windows']),1)
        self.assertEqual(r['windows'][0]['remaining_percent'],37)

    def test_multiple_windows_and_buckets(self):
        r=self.norm(); self.assertEqual(len(r['windows']),4)
        self.assertEqual(len({w['window_id'] for w in r['windows']}),4)
        self.assertNotIn('most_constrained_remaining_percent',r)

    def test_direct_remaining(self):
        w=next(w for w in self.norm()['windows'] if w['window_kind']=='individual_limit')
        self.assertEqual(w['remaining_percent'],42); self.assertEqual(w['value_origin'],'direct')
        self.assertEqual(w['used_percent'],None); self.assertIsNone(w['duration_seconds'])
        self.assertNotIn('SYNTHETIC_OMIT',json.dumps(w))

    def test_invalid_direct_value_is_not_relabelled(self):
        for value in [-1,101,True,'42']:
            with self.subTest(value=value),self.assertRaises(QuotaError):
                self.norm({'rateLimits':{'individualLimit':{'remainingPercent':value}}})

    def test_derived_remaining(self):
        w=self.norm()['windows'][0]
        self.assertEqual(w['used_percent_origin'],'direct'); self.assertEqual(w['value_origin'],'derived')
        self.assertEqual(w['derivation'],'clamp(100 - usedPercent, 0, 100)')

    def test_missing_reset(self):
        self.assertIsNone(self.norm()['windows'][1]['reset_at'])

    def test_unknown_duration(self):
        self.assertIsNone(self.norm()['windows'][2]['duration_seconds'])

    def test_unknown_percentage(self):
        r=self.norm({'rateLimits':{'primary':{'usedPercent':None}}})
        self.assertIsNone(r['windows'][0]['remaining_percent']); self.assertEqual(r['status'],'UNKNOWN')
        self.assertEqual(r['windows'][0]['value_origin'],'unknown')

    def test_malformed_input(self):
        for d in [[],None,{}, {'rateLimits':[]}, {'rateLimits':{'primary':'bad'}},
                  {'rateLimitsByLimitId':[],'rateLimits':{}}]:
            with self.subTest(d=d),self.assertRaises(QuotaError):self.norm(d) if d is not None else normalize(d,observed_at=STAMP)

    def test_invalid_percentages(self):
        for v in [True,float('nan'),float('inf'),'63',63.5]:
            with self.subTest(value=v),self.assertRaises(QuotaError):
                self.norm({'rateLimits':{'primary':{'usedPercent':v}}})

    def test_clamped_derived_value_retains_invalidity(self):
        for used,expected in [(-1,100),(101,0)]:
            r=self.norm({'rateLimits':{'primary':{'usedPercent':used}}})
            w=r['windows'][0]
            self.assertEqual(w['remaining_percent'],expected)
            self.assertTrue(w['clamped']); self.assertEqual(w['validity'],'INVALID')
            self.assertEqual(r['status'],'UNKNOWN')

    def test_unexpected_extra_fields_are_not_exported(self):
        self.raw['accountId']='private-account'; self.raw['email']='private@example.invalid'
        self.raw['rateLimitsByLimitId']['codex']['planType']='private-plan'
        self.raw['rateLimitUpsell']={'private':'do not export'}
        text=json.dumps(self.norm())
        for value in ['private-account','private@example.invalid','private-plan','do not export']:self.assertNotIn(value,text)

    def test_temporary_source_failure(self):
        def fail(timeout): raise QuotaError('SOURCE_ERROR')
        r=read_quota(transport=fail); self.assertEqual(r['status'],'ERROR')
        self.assertEqual(r['error_code'],'SOURCE_ERROR'); self.assertEqual(r['windows'],[])
        self.assertIsNone(r['observed_at'])

    def test_empty_windows_unknown(self):
        for raw in [{'rateLimits':{}},{'rateLimits':{'primary':None,'secondary':None}},
                    {'rateLimits':{},'rateLimitsByLimitId':{}}]:
            r=self.norm(raw); self.assertEqual(r['status'],'UNKNOWN'); self.assertEqual(r['windows'],[])

    def test_sensitive_field_rejection(self):
        for key in ['access_token','Authorization','cookie','apiKey','refreshToken','password','session_secret']:
            raw=copy.deepcopy(self.raw); raw[key]='synthetic-secret'
            with self.subTest(key=key),self.assertRaises(QuotaError) as cm:self.norm(raw)
            self.assertNotIn('synthetic-secret',str(cm.exception))

    def test_sensitive_values_in_identifiers_rejected(self):
        for value in ['hf_'+'x'*30,'sk-proj-'+'x'*32,'Bearer synthetic-secret','../outside','private@example.invalid']:
            raw={'rateLimits':{'limitId':value,'primary':{'usedPercent':10}}}
            with self.subTest(value=value),self.assertRaises(QuotaError):self.norm(raw)

    def test_fixture_mode_not_live(self):
        self.assertEqual(self.norm()['mode'],'synthetic')
        self.assertEqual(self.norm()['source_confidence'],'SYNTHETIC')

    def test_bounds(self):
        with self.assertRaises(QuotaError):self.norm({'rateLimits':{},'rateLimitsByLimitId':{str(i):{} for i in range(33)}})
        for timeout in [0,31,float('nan'),float('inf')]:
            called=[]
            with self.assertRaises(ValueError):read_quota(timeout=timeout,transport=lambda t:called.append(t))
            self.assertEqual(called,[])

    def test_reset_conversion_and_bad_dates(self):
        self.assertEqual(self.norm()['windows'][0]['reset_at'],'2033-05-18T03:33:20Z')
        for val in [-1,True,'tomorrow',10**30]:
            with self.assertRaises(QuotaError):self.norm({'rateLimits':{'primary':{'usedPercent':3,'resetsAt':val}}})

    def test_bucket_identity_conflict(self):
        raw={'rateLimits':{},'rateLimitsByLimitId':{'a':{'limitId':'b','primary':{'usedPercent':3}}}}
        with self.assertRaises(QuotaError):self.norm(raw)

    def test_bad_duration(self):
        for v in [-1,0,True,'300']:
            with self.assertRaises(QuotaError):self.norm({'rateLimits':{'primary':{'usedPercent':3,'windowDurationMins':v}}})

    def test_observation_time_and_unknown_server_age(self):
        r=self.norm(); self.assertEqual(r['observed_at'],STAMP)
        self.assertIsNone(r['source_observed_at']); self.assertEqual(r['coverage'],'UNKNOWN')
        self.assertTrue(r['source_supported']); self.assertEqual(r['source_maturity'],'experimental')

if __name__=='__main__':unittest.main()
