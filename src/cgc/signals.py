"""Explicit caller-owned cancellation for synchronous manual mutation adapters."""
from contextlib import contextmanager
import signal
import threading


@contextmanager
def mutation_signals():
    """Translate the first SIGINT/SIGTERM to KeyboardInterrupt; protect cleanup.

    Use on the main thread around one checkpoint/publish call. The adapters turn
    interruption into a fixed CANCELLED result after Git cleanup and best-effort
    failure persistence. Further signals in this scope do not interrupt that
    cleanup. Exit promptly: prior handlers are restored, including on exceptions.
    This opt-in scope grants no mutation authority and cannot handle SIGKILL.
    """
    if threading.current_thread() is not threading.main_thread():
        raise ValueError('SIGNAL_SCOPE_REQUIRES_MAIN_THREAD')
    cancelled = False
    previous = {}

    def cancel(signum, frame):
        nonlocal cancelled
        if not cancelled:
            cancelled = True
            raise KeyboardInterrupt

    try:
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous[signum] = signal.getsignal(signum)
            signal.signal(signum, cancel)
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)
