"""Temporary private caches and injected sensors only; never live Codex."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from cgc.cache import Cache, CacheError, MAX_CACHE_BYTES
from synthetic_support import run
from cgc.engine import StateError
from cgc.__main__ import main
from test_engine import STAMP, populated, observation


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'cache'

    def test_atomic_roundtrip_and_modes(self):
        with Cache(self.path,create=True) as cache, cache.writer():
            self.assertIsNone(cache.read())
            cache.write(populated())
            self.assertEqual(cache.read(),populated())
            self.assertEqual((self.path/'state.json').stat().st_mode & 0o777,0o600)
        self.assertEqual(self.path.stat().st_mode & 0o777,0o700)

    def test_failure_before_replace_preserves_previous(self):
        with Cache(self.path,create=True) as cache, cache.writer():
            cache.write(populated())
            with patch('cgc.cache.os.replace',side_effect=OSError('synthetic-secret')):
                with self.assertRaises(CacheError):cache.write(populated(99))
            self.assertEqual(cache.read(),populated())
            self.assertEqual(list(self.path.glob('*.tmp')),[])

    def test_writer_exclusion_and_release(self):
        with Cache(self.path,create=True) as one, Cache(self.path) as two:
            with one.writer():
                with self.assertRaises(CacheError):
                    with two.writer():pass
            with two.writer():two.write(populated())

    def test_write_requires_lock(self):
        with Cache(self.path,create=True) as cache:
            with self.assertRaises(CacheError):cache.write(populated())

    def test_symlinks_refused(self):
        target=Path(self.temp.name)/'target';target.mkdir(mode=0o700)
        self.path.symlink_to(target)
        with self.assertRaises(CacheError):
            with Cache(self.path):pass
        self.path.unlink()
        with Cache(self.path,create=True) as cache:
            (self.path/'state.json').symlink_to(target/'outside')
            with self.assertRaises(CacheError):cache.read()
        self.assertFalse((target/'outside').exists())

    def test_hardlinks_and_public_permissions_refused(self):
        with Cache(self.path,create=True) as cache,cache.writer():
            cache.write(populated())
            os.link(self.path/'state.json',self.path/'alias')
            with self.assertRaises(CacheError):cache.read()
        (self.path/'alias').unlink()
        (self.path/'state.json').chmod(0o644)
        with Cache(self.path) as cache:
            with self.assertRaises(CacheError):cache.read()

    def test_corruption_and_size_limits(self):
        with Cache(self.path,create=True) as cache:
            for raw in ['{','{"x":1,"x":2}', 'x'*(MAX_CACHE_BYTES + 1), json.dumps({'token':'synthetic-secret'})]:
                p=self.path/'state.json';p.write_text(raw);p.chmod(0o600)
                with self.assertRaises(CacheError) as cm:cache.read()
                self.assertNotIn('synthetic-secret',str(cm.exception))

    def test_status_missing_does_not_create_or_read_source(self):
        output=io.StringIO()
        with patch('cgc.quota.app_server_read',side_effect=AssertionError('live read')),contextlib.redirect_stdout(output):
            code=main(['status','--cache-dir',str(self.path),'--json'])
        self.assertEqual(code,1);self.assertFalse(self.path.exists())
        self.assertIsNone(json.loads(output.getvalue())['policy_state'])

    def test_cli_status_matches_engine_and_hides_corruption(self):
        with Cache(self.path,create=True) as cache,cache.writer():cache.write(populated())
        output=io.StringIO()
        with patch('cgc.__main__.utcnow',return_value=STAMP),contextlib.redirect_stdout(output):
            code=main(['status','--cache-dir',str(self.path),'--json'])
        self.assertEqual(code,1)
        self.assertEqual(json.loads(output.getvalue())['policy_state'],'AMBER')
        (self.path/'state.json').write_text('{"private":"synthetic-secret"}')
        output=io.StringIO()
        with contextlib.redirect_stdout(output):code=main(['status','--cache-dir',str(self.path),'--json'])
        self.assertEqual(code,2);self.assertNotIn('synthetic-secret',output.getvalue())

    def test_daemon_bounded_backoff_and_recovery(self):
        class Stop:
            def __init__(self):self.waits=[]
            def is_set(self):return False
            def wait(self,seconds):self.waits.append(seconds);return False
        stop=Stop();results=iter([observation(),{'status':'ERROR','error_code':'TIMEOUT'},observation(95)])
        with Cache(self.path,create=True) as cache:
            n=run(cache,buckets=['codex'],max_reads=3,interval=60,reader=lambda **_:next(results),clock=lambda:STAMP,stop=stop)
            self.assertEqual(n,3);self.assertEqual(cache.read()['generation'],3)
            self.assertEqual(cache.read()['policy']['policy_state'],'EMERGENCY')
        self.assertEqual(stop.waits,[60,120])

    def test_daemon_stop_and_configuration_before_read(self):
        stop=threading.Event();stop.set()
        def forbidden(**_):raise AssertionError('unexpected source read')
        with Cache(self.path,create=True) as cache:
            self.assertEqual(run(cache,buckets=['codex'],max_reads=1,reader=forbidden,stop=stop),0)
            for count in [0,True,101]:
                with self.assertRaises(StateError):run(cache,buckets=['codex'],max_reads=count,reader=forbidden)
            with self.assertRaises(StateError):run(cache,buckets=['codex'],max_reads=1,interval=30,reader=forbidden)

    def test_config_mismatch_and_corruption_block_sensor(self):
        with Cache(self.path,create=True) as cache:
            with cache.writer():cache.write(populated())
            def forbidden(**_):raise AssertionError('unexpected source read')
            with self.assertRaises(StateError):run(cache,buckets=['other'],max_reads=1,reader=forbidden)
            (self.path/'state.json').write_text('broken')
            with self.assertRaises(CacheError):run(cache,buckets=['codex'],max_reads=1,reader=forbidden)

    def test_post_replace_sync_failure_leaves_complete_generation(self):
        with Cache(self.path,create=True) as cache,cache.writer():
            cache.write(populated())
            real_sync=os.fsync
            def fail_directory(fd):
                if fd == cache.fd:raise OSError('injected')
                return real_sync(fd)
            with patch('cgc.cache.os.fsync',side_effect=fail_directory):
                with self.assertRaises(CacheError):cache.write(populated(99))
            self.assertEqual(cache.read(),populated(99))

    def test_independent_process_writer_exclusion(self):
        import subprocess
        import sys
        script='''import sys
from cgc.cache import Cache,CacheError
try:
    with Cache(sys.argv[1]) as cache,cache.writer():
        sys.exit(7)
except CacheError:
    sys.exit(0)
'''
        with Cache(self.path,create=True) as cache,cache.writer():
            child=subprocess.run([sys.executable,'-B','-c',script,str(self.path)],capture_output=True,timeout=5)
            self.assertEqual(child.returncode,0)

    def test_sigterm_stops_wait_and_releases_lock(self):
        import subprocess
        import sys
        script='''import signal,sys,threading
from cgc.cache import Cache
from cgc.daemon import run
from cgc.quota import normalize
from cgc.engine import utcnow
stop=threading.Event()
signal.signal(signal.SIGTERM,lambda *_:stop.set())
def reader(**_):
    print('ready',flush=True)
    return normalize({'rateLimits':{'limitId':'codex','primary':{'usedPercent':20}}},observed_at=utcnow(),mode='synthetic')
with Cache(sys.argv[1],create=True) as cache:
    count=run(cache,buckets=['codex'],max_reads=2,interval=60,reader=reader,stop=stop)
    assert count==1
'''
        child=subprocess.Popen([sys.executable,'-B','-c',script,str(self.path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            import selectors
            with selectors.DefaultSelector() as sel:
                sel.register(child.stdout,selectors.EVENT_READ)
                self.assertTrue(sel.select(5))
                self.assertEqual(child.stdout.readline(),b'ready\n')
            child.terminate()
            child.communicate(timeout=5)
            self.assertEqual(child.returncode,0)
            with Cache(self.path) as cache,cache.writer():self.assertEqual(cache.read()['generation'],1)
        finally:
            if child.poll() is None:child.kill()
            child.communicate()
