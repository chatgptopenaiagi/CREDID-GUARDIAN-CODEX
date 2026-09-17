"""Offline policy and canonical state acceptance tests."""
import copy
import unittest
from cgc.quota import normalize
from cgc.engine import (StateError, classify, empty_state, refresh, status,
                        validate_observation, validate_state)

STAMP = '2026-09-17T00:00:00Z'


def observation(used=80, mode='synthetic', stamp=STAMP):
    return normalize({'rateLimits': {'limitId': 'codex', 'primary': {'usedPercent': used}}},
                     observed_at=stamp, mode=mode)


def populated(used=80, mode='synthetic'):
    return refresh(empty_state(['codex']), observation(used, mode), now=STAMP)


class EngineTests(unittest.TestCase):
    def test_exact_and_fractional_thresholds(self):
        for value, expected in [(100,'GREEN'),(21,'GREEN'),(20.001,'GREEN'),(20,'AMBER'),
                                (19.999,'AMBER'),(11,'AMBER'),(10.001,'AMBER'),(10,'RED'),
                                (9.999,'RED'),(6,'RED'),(5.001,'RED'),(5,'EMERGENCY'),(0,'EMERGENCY')]:
            self.assertEqual(classify(value), expected)
        for bad in [True,False,None,-1,101,'5',float('nan'),float('inf')]:
            with self.assertRaises(StateError): classify(bad)

    def test_empty_unknown(self):
        s = status(empty_state(['codex']), now=STAMP)
        self.assertIsNone(s['policy_state'])
        self.assertEqual(s['validity'], 'UNKNOWN')

    def test_multi_bucket_selection_and_partial(self):
        obs = normalize({'rateLimits':{}, 'rateLimitsByLimitId':{
            'codex':{'primary':{'usedPercent':65},'secondary':{'usedPercent':None},'individualLimit':{'remainingPercent':8}},
            'other':{'primary':{'usedPercent':99}}}}, observed_at=STAMP, mode='synthetic')
        state = refresh(empty_state(['codex','missing']), obs, now=STAMP)
        self.assertEqual(state['policy']['policy_state'], 'RED')
        self.assertEqual(state['policy']['missing_buckets'], ['missing'])
        self.assertEqual(state['policy']['coverage'], 'PARTIAL')
        self.assertFalse(state['policy']['global_all_clear'])

    def test_failure_retains_timestamp_and_policy(self):
        before = populated()
        after = refresh(before, {'status':'ERROR','error_code':'TIMEOUT'}, now='2026-09-17T00:01:00Z')
        self.assertEqual(before['last_valid_observation'], after['last_valid_observation'])
        self.assertEqual(before['policy'], after['policy'])
        self.assertEqual(status(after, now='2026-09-17T00:02:00Z')['age_seconds'],120)
        self.assertEqual(after['error_code'],'TIMEOUT')
        self.assertEqual(before['generation'],1)

    def test_staleness_and_clock_skew(self):
        state=populated()
        self.assertEqual(status(state,now='2026-09-17T00:15:00Z')['validity'],'VALID')
        s=status(state,now='2026-09-17T00:15:01Z')
        self.assertEqual(s['validity'],'STALE'); self.assertIsNone(s['policy_state'])
        self.assertEqual(s['historical_policy']['policy_state'],'AMBER')
        self.assertEqual(status(state,now='2026-09-16T23:59:59Z')['validity'],'CLOCK_SKEW')

    def test_invalid_and_empty_do_not_erase(self):
        before=populated()
        for obs in [observation(101), normalize({'rateLimits':{}},observed_at=STAMP), {}, {'status':'ERROR','error_code':['secret']}]:
            after=refresh(before,obs,now=STAMP)
            self.assertEqual(after['last_valid_observation'],before['last_valid_observation'])
            self.assertEqual(after['last_refresh_status'],'ERROR')

    def test_tampering_rejected_without_echo(self):
        for key,value in [('remaining_percent',99),('validity','VALID-secret'),('clamped',0),('reset_at','secret'),('token','synthetic-secret')]:
            obs=observation();obs['windows'][0][key]=value
            with self.assertRaises(StateError) as cm:validate_observation(obs)
            self.assertNotIn('secret',str(cm.exception))
        obs=observation();obs['accountId']='synthetic-private'
        with self.assertRaises(StateError):validate_observation(obs)
        state=populated();state['policy']['policy_state']='GREEN'
        with self.assertRaises(StateError):validate_state(state)

    def test_synthetic_isolation(self):
        state=populated(99)
        s=status(state,now=STAMP)
        self.assertFalse(s['live_policy_available']);self.assertIsNone(s['directive'])
        after=refresh(state,observation(99,'live'),now=STAMP)
        self.assertEqual(after['error_code'],'MODE_MISMATCH')

    def test_future_observation_rejected(self):
        s=refresh(empty_state(['codex']),observation(stamp='2026-09-18T00:00:00Z'),now=STAMP)
        self.assertIsNone(s['last_valid_observation'])

    def test_live_policy_with_uncertainty(self):
        s=status(populated(95,'live'),now=STAMP)
        self.assertTrue(s['live_policy_available'])
        self.assertEqual(s['policy_state'],'EMERGENCY')
        self.assertFalse(s['global_all_clear'])

    def test_reset_passage_never_replenishes(self):
        obs=normalize({'rateLimits':{'limitId':'codex','primary':{'usedPercent':99,'resetsAt':0}}},observed_at=STAMP)
        s=refresh(empty_state(['codex']),obs,now=STAMP)
        self.assertEqual(status(s,now=STAMP)['policy_state'],'EMERGENCY')

    def test_selection_and_config_reject_bad_values(self):
        for buckets in [[],['codex','codex'],['../x'],['secret'],[None]]:
            with self.assertRaises(StateError):empty_state(buckets)
        for age in [True,0,86401]:
            with self.assertRaises(StateError):empty_state(['codex'],age)

    def test_explicit_usage_denial_withholds_current_directive(self):
        obs=observation(0,'live');obs['ordinary_usage_allowed']=False
        state=refresh(empty_state(['codex']),obs,now=STAMP)
        result=status(state,now=STAMP)
        self.assertEqual(result['validity'],'USAGE_BLOCKED')
        self.assertIsNone(result['policy_state']);self.assertIsNone(result['directive'])
        self.assertFalse(result['live_policy_available'])

    def test_regressing_observation_cannot_replace_newer(self):
        state=populated()
        updated=refresh(state,observation(stamp='2026-09-16T23:59:00Z'),now=STAMP)
        self.assertEqual(updated['last_refresh_status'],'ERROR')
        self.assertEqual(updated['last_valid_observation'],state['last_valid_observation'])

    def test_cache_cannot_claim_empty_observation_as_success(self):
        from cgc.engine import policy
        state=populated()
        state['last_valid_observation']=normalize({'rateLimits':{}},observed_at=STAMP)
        state['policy']=policy(state['last_valid_observation'],['codex'])
        with self.assertRaises(StateError):validate_state(state)
