"""Fixture-only hooks rendezvous inside real Git commit, before/after acceptance."""
import ctypes
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def hook(control):
    with open(control / 'ready', 'w') as ready:
        ready.write(json.dumps({'hook': os.getpid(), 'parent': os.getppid(),
                                'group': os.getpgrp()}) + '\n')
    with open(control / 'gate', 'rb') as gate:
        if gate.read(1) != b'G':
            raise RuntimeError('FIXTURE_GATE_CLOSED')


def worker(args, control):
    from cgc import checkpoint as cp
    from cgc.signals import mutation_signals

    # Fixture hygiene only, not a runtime descendant-reaping guarantee.
    pr_set_child_subreaper = 36
    if ctypes.CDLL(None, use_errno=True).prctl(pr_set_child_subreaper, 1, 0, 0, 0) != 0:
        raise RuntimeError('FIXTURE_SUBREAPER_FAILED')
    real_popen = subprocess.Popen
    commit = None
    attempts = 0
    cp.ins.COMMAND_SECONDS = 4

    def popen(command, **kwargs):
        nonlocal commit, attempts
        if 'commit' not in command:
            return real_popen(command, **kwargs)
        attempts += 1
        # Only the fixture commit gets synchronization hooks. Source config,
        # hook files and all production preflight checks remain untouched.
        command = list(command)
        index = command.index('commit')
        command[index:index] = ['-c', 'core.hooksPath=' + str(control / 'hooks')]
        (control / 'dispatch-index').write_bytes((Path(args['project']) / '.git/index').read_bytes())
        commit = real_popen(command, **kwargs)
        print(json.dumps({'commit': commit.pid}), flush=True)
        return commit

    subprocess.Popen = popen
    previous = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        with mutation_signals():
            result = cp.checkpoint(**args)
        result['fixture_commit_reaped'] = commit is not None and commit.returncode is not None
        result['fixture_attempts'] = attempts
        result['fixture_handlers_restored'] = all(signal.getsignal(s) == h for s, h in previous.items())
        deadline = time.monotonic() + 3
        while True:
            try:
                pid, _ = os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                break
            if not pid:
                if time.monotonic() >= deadline:
                    raise RuntimeError('FIXTURE_DESCENDANT_SURVIVED')
                time.sleep(0.01)
        print(json.dumps(result), flush=True)
    finally:
        if commit is not None:
            try: os.killpg(commit.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            commit.wait(timeout=5)


if __name__ == '__main__':
    if sys.argv[1] == 'hook':
        hook(Path(sys.argv[2]))
    else:
        worker(json.loads(sys.argv[2]), Path(sys.argv[3]))
