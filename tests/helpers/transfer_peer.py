"""Test-only flow control of a real local Git upload-pack stream.

No fabricated objects, packets, Git results or production transport changes.
The upload role forwards a prefix, announces the live pipeline, and waits for
the fixture gate. The worker runs the ordinary publication adapter and runner.
"""
import ctypes
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import time


def upload(control, project):
    child = subprocess.Popen(['/usr/bin/git', 'upload-pack', project],
                             stdin=sys.stdin.buffer, stdout=subprocess.PIPE,
                             stderr=sys.stderr.buffer)
    sent = 0
    try:
        while sent < 256 * 1024:
            data = os.read(child.stdout.fileno(), min(8192, 256 * 1024 - sent))
            if not data:
                raise RuntimeError('FIXTURE_STREAM_TOO_SHORT')
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
            sent += len(data)
        with open(control / 'ready', 'w') as ready:
            ready.write(json.dumps({'proxy': os.getpid(), 'upload': child.pid,
                                    'group': os.getpgrp(), 'forwarded': sent}) + '\n')
        with open(control / 'gate', 'rb') as gate:
            if gate.read(1) != b'G':
                raise RuntimeError('FIXTURE_GATE_CLOSED')
        while data := os.read(child.stdout.fileno(), 8192):
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
        return child.wait(timeout=5)
    finally:
        child.stdout.close()
        if child.poll() is None:
            child.kill()
            child.wait(timeout=5)


def worker(args, control):
    from cgc import inspection as ins
    from cgc import publication as pub
    from cgc.signals import mutation_signals

    # Test-process-only subreaper: collect orphaned fixture grandchildren after
    # the production runner kills their group. This is NOT CGC runtime behavior.
    pr_set_child_subreaper = 36
    if ctypes.CDLL(None, use_errno=True).prctl(pr_set_child_subreaper, 1, 0, 0, 0) != 0:
        raise RuntimeError('FIXTURE_SUBREAPER_FAILED')
    real_popen = subprocess.Popen
    fetch = None
    transfers = 0
    ref_updates = 0
    ins.COMMAND_SECONDS = 4

    def popen(command, **kwargs):
        nonlocal fetch, transfers, ref_updates
        if 'update-ref' in command:
            ref_updates += 1
        if 'fetch' in command and args['project'] in command:
            transfers += 1
            command = list(command)
            helper = shlex.join([sys.executable, '-B', str(Path(__file__).resolve()),
                                 'upload', str(control)])
            command.insert(command.index('--'), '--upload-pack=' + helper)
            fetch = real_popen(command, **kwargs)
            print(json.dumps({'fetch': fetch.pid}), flush=True)
            return fetch
        return real_popen(command, **kwargs)

    subprocess.Popen = popen
    try:
        with mutation_signals():
            result = pub.publish(**args)
        result['fixture_fetch_reaped'] = fetch is not None and fetch.returncode is not None
        result['fixture_transfers'] = transfers
        result['fixture_ref_updates'] = ref_updates
        # Reap only children already terminated by Git or production cleanup.
        # Do not hide a surviving descendant by killing it before reporting.
        reaped = []
        deadline = time.monotonic() + 3
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                break
            if pid:
                reaped.append(pid)
            elif time.monotonic() >= deadline:
                raise RuntimeError('FIXTURE_DESCENDANT_SURVIVED')
            else:
                time.sleep(0.01)
        result['fixture_adopted_reaped'] = reaped
        print(json.dumps(result), flush=True)
    finally:
        if fetch is not None:
            try:
                os.killpg(fetch.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            fetch.wait(timeout=5)


if __name__ == '__main__':
    if sys.argv[1] == 'upload':
        sys.exit(upload(Path(sys.argv[2]), sys.argv[3]))
    worker(json.loads(sys.argv[2]), Path(sys.argv[3]))
