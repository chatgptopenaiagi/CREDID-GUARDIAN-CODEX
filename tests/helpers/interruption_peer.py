"""Synthetic child harness; not a CGC command or a live source."""
import contextlib
import io
import json
import os
from pathlib import Path
import signal
import selectors
import subprocess
import sys
import threading
from unittest.mock import patch

# Explicit repo/test imports; never rely on an installed CGC package.
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'tests')]
from cgc import __main__ as cli
from cgc.cache import Cache
from cgc.daemon import refresh_once
from cgc.engine import refresh
from cgc.quota import read_quota
from synthetic_support import fixture_evidence
from test_engine import observation, STAMP

path, mode, stage = sys.argv[1:]
controller_stdout = sys.stdout


def checkpoint():
    print('READY', file=controller_stdout, flush=True)
    if sys.stdin.buffer.read(1) != b'x':
        raise RuntimeError('test controller disconnected')


def forbidden(*args, **kwargs):
    raise AssertionError('live source forbidden')


if mode == 'crash':
    original_read, original_open, original_replace = Cache.read, os.fdopen, os.replace

    def cache_read(cache):
        if stage == 'before_read' and cache.lock_fd is not None:
            checkpoint()
        return original_read(cache)

    def reader(**kwargs):
        if stage == 'during_read':
            checkpoint()
        return observation(95)

    def evaluate(*args, **kwargs):
        state = refresh(*args, **kwargs)
        if stage == 'after_observation':
            checkpoint()
        return state

    class PartialWriter:
        def __init__(self, stream):
            self.stream = stream
        def __enter__(self):
            self.stream.__enter__()
            return self
        def __exit__(self, *args):
            return self.stream.__exit__(*args)
        def write(self, data):
            self.stream.write(data[:len(data) // 2])
            self.stream.flush()
            checkpoint()
            raise AssertionError('crash checkpoint unexpectedly resumed')

    def fdopen(fd, mode, *args, **kwargs):
        stream = original_open(fd, mode, *args, **kwargs)
        return PartialWriter(stream) if stage == 'partial_write' and mode == 'wb' else stream

    def replace(*args, **kwargs):
        if stage == 'before_replace':
            checkpoint()
        original_replace(*args, **kwargs)
        if stage == 'after_replace':
            checkpoint()

    with patch('cgc.quota.app_server_read', forbidden), patch.object(Cache, 'read', cache_read), \
         patch('cgc.daemon.refresh', evaluate), patch('cgc.cache.os.fdopen', fdopen), \
         patch('cgc.cache.os.replace', replace), Cache(path, create=True) as cache:
        refresh_once(cache, buckets=['codex'], reader=reader, clock=lambda: STAMP,
                     evidence_provider=fixture_evidence)
    raise AssertionError('checkpoint not reached')

else:
    # Exercise real CLI signal handlers; output remains isolated from test rendezvous.
    processes = []
    original_popen = subprocess.Popen
    original_exchange = __import__('cgc.quota', fromlist=['_exchange'])._exchange
    class Event(threading.Event):
        def wait(self, timeout=None):
            if stage == 'wait':
                print('READY', file=controller_stdout, flush=True)
            return super().wait(timeout)

    def reader(**kwargs):
        if stage == 'read_success':
            checkpoint()
            return observation(95)
        if stage == 'timeout':
            return read_quota(**kwargs)
        return observation(95)

    def exchange(*args):
        checkpoint()  # Transport exists; signal arrives while the read is in flight.
        return original_exchange(*args)

    def spawn(argv, **kwargs):
        assert argv[0] == 'codex'
        # Ignore TERM to verify bounded KILL escalation and reaping. No real Codex.
        script = ('import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); '
                  "print('PEER_READY',flush=True); time.sleep(30)")
        proc = original_popen([sys.executable, '-I', '-B', '-c', script], **kwargs)
        processes.append(proc)
        with selectors.DefaultSelector() as selector:
            selector.register(proc.stdout, selectors.EVENT_READ)
            assert selector.select(8), 'transport startup timed out'
            assert proc.stdout.readline() == b'PEER_READY\n'
        return proc

    original_run, original_once = cli.run, cli.refresh_once
    def run(cache, **kwargs):
        return original_run(cache, **kwargs, reader=reader, clock=lambda: STAMP,
                            evidence_provider=fixture_evidence)
    def once(cache, **kwargs):
        return original_once(cache, **kwargs, reader=reader, clock=lambda: STAMP,
                             evidence_provider=fixture_evidence)
    output = io.StringIO()
    args = [mode, '--live', '--bucket', 'codex', '--cache-dir', path, '--timeout', '1']
    args += ['--max-reads', '3', '--interval', '60'] if mode == 'daemon' else ['--json']
    with patch.object(cli, 'run', run), patch.object(cli, 'refresh_once', once), \
         patch.object(cli, 'utcnow', lambda: STAMP), patch('cgc.quota.subprocess.Popen', spawn), \
         patch('cgc.quota._exchange', exchange), patch('cgc.__main__.threading.Event', Event), \
         contextlib.redirect_stdout(output):
        code = cli.main(args)
    assert all(proc.poll() == -signal.SIGKILL for proc in processes), 'transport not killed/reaped'
    print(json.dumps({'exit': code, 'output': json.loads(output.getvalue()),
                      'children_reaped': len(processes)}), flush=True)
