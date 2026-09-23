"""Test-only rendezvous inside a real interactive Git ref transaction.

Replace only the selected update-ref subprocess in a disposable fixture. Git
acknowledges prepare (lock held) or commit (ref accepted), then waits on stdin.
The production runner retains ownership of its pipes, deadline and cleanup.
"""
import json
import os
import signal
import subprocess
import sys

from cgc import inspection as ins
from cgc import publication as pub
from cgc.handoff import HandoffStore
from cgc.signals import mutation_signals

args = json.loads(sys.argv[1])
stage, mode = sys.argv[2:4]
real_popen, real_read = subprocess.Popen, os.read
transaction = None
announced = False
if mode == 'timeout':
    ins.COMMAND_SECONDS = 2


def popen(command, **kwargs):
    global transaction
    if 'update-ref' not in command or 'refs/heads/main' not in command:
        return real_popen(command, **kwargs)
    index = command.index('update-ref')
    ref, new, old = command[index + 2:]
    kwargs['stdin'] = subprocess.PIPE
    transaction = real_popen(command[:index] + ['update-ref', '--no-deref', '--stdin'], **kwargs)
    script = f'start\nupdate {ref} {new} {old}\nprepare\n'
    if stage == 'committed':
        script += 'commit\n'
    transaction.stdin.write(script.encode())
    transaction.stdin.flush()
    return transaction


def read(fd, size):
    global announced
    data = real_read(fd, size)
    marker = b'commit: ok' if stage == 'committed' else b'prepare: ok'
    if transaction is not None and fd == transaction.stdout.fileno() and not announced:
        # Pipe reads may split acknowledgements; retain only these tiny fixture bytes.
        read.buffer += data
        if marker in read.buffer:
            announced = True
            print(json.dumps({'ready': stage, 'pid': transaction.pid}), flush=True)
    return data


read.buffer = b''
subprocess.Popen = popen
os.read = read
real_failure = HandoffStore.record_failure


def failure(store, *values, **kwargs):
    if mode == 'repeat':
        print('CLEANUP', flush=True)
        if sys.stdin.readline() != 'continue\n':
            raise RuntimeError('FIXTURE_CONTROL_CLOSED')
    return real_failure(store, *values, **kwargs)


HandoffStore.record_failure = failure
before = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
try:
    with mutation_signals():
        result = pub.publish(**args)
finally:
    if transaction is not None:
        transaction.stdin.close()
        if transaction.poll() is None:
            transaction.kill()
            transaction.wait(timeout=5)
result['handlers_restored'] = all(signal.getsignal(s) == h for s, h in before.items())
result['child_reaped'] = transaction.returncode is not None
print(json.dumps(result), flush=True)
