"""CREDID GUARDIAN CODEX (CGC): local synthetic peers, never real Codex."""
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

from cgc.quota import QuotaError, _decode, _exchange, app_server_read, read_quota

FIXTURE=json.loads((Path(__file__).parent/'fixtures/quota.json').read_text())

class ProtocolTests(unittest.TestCase):
    def exchange(self, messages):
        sent=[]; source=iter(messages)
        result=_exchange(sent.append,lambda:next(source))
        return result,sent

    def test_exact_handshake_and_one_read(self):
        result,sent=self.exchange([{'id':1,'result':{'codexHome':'do-not-export'}}, {'id':2,'result':FIXTURE}])
        self.assertEqual(result,FIXTURE)
        self.assertEqual([s['method'] for s in sent],['initialize','initialized','account/rateLimits/read'])
        self.assertFalse(sent[0]['params']['capabilities']['experimentalApi'])
        self.assertEqual(sent[2]['params'],{'excludeResetCreditDetails':True,'supportsLunaReserve':False})

    def test_ignores_notifications_not_credentials_requests(self):
        _,sent=self.exchange([{'method':'noise','params':{'accountId':'omit'}},{'id':1,'result':{}},{'id':2,'result':FIXTURE}])
        self.assertEqual(len(sent),3)
        with self.assertRaises(QuotaError) as cm:
            self.exchange([{'id':99,'method':'account/chatgptAuthTokens/refresh','params':{}}])
        self.assertEqual(cm.exception.code,'SERVER_REQUEST_REFUSED')

    def test_source_errors_never_echo_message(self):
        with self.assertRaises(QuotaError) as cm:
            self.exchange([{'id':1,'result':{}},{'id':2,'error':{'message':'private secret text'}}])
        self.assertEqual(str(cm.exception),'SOURCE_ERROR')

    def test_json_rejects_duplicates_and_nonfinite(self):
        for raw in [b'{"id":1,"id":2}',b'{"n":NaN}',b'[]',b'\xff',b'bad']:
            with self.subTest(raw=raw),self.assertRaises(QuotaError):_decode(raw)

    def test_message_bound(self):
        with self.assertRaises(QuotaError) as cm:self.exchange([{'method':'noise'}]*101)
        self.assertEqual(cm.exception.code,'FRAME_COUNT_LIMIT')

    def peer(self, script, timeout=1):
        real_popen=subprocess.Popen; processes=[]; calls=[]
        def spawn(argv,**kwargs):
            calls.append((argv,kwargs))
            p=real_popen([sys.executable,'-I','-B','-c',script],**kwargs)
            processes.append(p);return p
        with patch('cgc.quota.subprocess.Popen',side_effect=spawn):
            result=read_quota(timeout=timeout)
        self.assertTrue(all(p.poll() is not None for p in processes))
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0][0],['codex','app-server','--listen','stdio://','-c','analytics.enabled=false'])
        self.assertNotIn('shell',calls[0][1]); self.assertNotIn('env',calls[0][1])
        return result

    def test_synthetic_process_success_and_stderr_omission(self):
        script="""import sys,json
m=json.loads(sys.stdin.readline())
print(json.dumps({'id':m['id'],'result':{'codexHome':'private-home'}}),flush=True)
json.loads(sys.stdin.readline())
m=json.loads(sys.stdin.readline())
print('private stderr diagnostic',file=sys.stderr,flush=True)
print(json.dumps({'id':m['id'],'result':RAW}),flush=True)
sys.stdin.read()
""".replace('RAW',repr(FIXTURE))
        result=self.peer(script)
        self.assertEqual(result['status'],'OK')
        self.assertEqual(len(result['windows']),4)
        for text in ['private-home','private stderr diagnostic']:self.assertNotIn(text,json.dumps(result))

    def test_timeout_terminates_peer(self):
        start=time.monotonic();result=self.peer('import time; time.sleep(20)',timeout=0.1)
        self.assertEqual(result['error_code'],'TIMEOUT');self.assertLess(time.monotonic()-start,3)

    def test_oversized_stderr_is_bounded(self):
        r=self.peer("import sys,time;sys.stderr.write('x'*600000);sys.stderr.flush();time.sleep(5)")
        self.assertEqual(r['error_code'],'OUTPUT_LIMIT')

    def test_oversized_stdout_frame_is_bounded(self):
        r=self.peer("import sys,time;sys.stdout.write('x'*200000);sys.stdout.flush();time.sleep(5)")
        self.assertEqual(r['error_code'],'FRAME_LIMIT')

    def test_early_exit_safe_error(self):
        r=self.peer("import sys;sys.stderr.write('sensitive details');sys.exit(1)")
        self.assertEqual(r['error_code'],'SOURCE_CLOSED')
        self.assertNotIn('sensitive details',json.dumps(r))

if __name__=='__main__':unittest.main()
