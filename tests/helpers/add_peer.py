"""Fixture-only loader injection into real git add; ordinary CGC runner/cleanup."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys


def worker(args, control, library, stage):
    from cgc import checkpoint as cp
    from cgc.signals import mutation_signals

    real_popen = subprocess.Popen
    child = None
    adds = commits = 0
    cp.ins.COMMAND_SECONDS = 4

    def popen(command, **kwargs):
        nonlocal child, adds, commits
        if 'commit' in command:
            commits += 1
        if 'add' not in command:
            return real_popen(command, **kwargs)
        adds += 1
        # Only this fixture's real add process gets the shim. No production
        # environment/configuration or command/return value is replaced.
        kwargs['env'] = dict(kwargs['env'], LD_PRELOAD=library,
                             CGC_FIXTURE_INDEX=str(Path(args['project']) / '.git/index'),
                             CGC_FIXTURE_STAGE=stage,
                             CGC_FIXTURE_READY=str(control / 'ready'),
                             CGC_FIXTURE_GATE=str(control / 'gate'))
        child = real_popen(command, **kwargs)
        print(json.dumps({'add': child.pid}), flush=True)
        return child

    subprocess.Popen = popen
    previous = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        with mutation_signals():
            result = cp.checkpoint(**args)
        result['fixture_adds'] = adds
        result['fixture_commits'] = commits
        result['fixture_child_reaped'] = child is not None and child.returncode is not None
        result['fixture_handlers_restored'] = all(signal.getsignal(s) == h for s, h in previous.items())
        print(json.dumps(result), flush=True)
    finally:
        if child is not None:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait(timeout=5)


if __name__ == '__main__':
    worker(json.loads(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4])
