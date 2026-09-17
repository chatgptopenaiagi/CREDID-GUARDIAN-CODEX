"""CREDID GUARDIAN CODEX (CGC) cache status and explicitly bounded observation."""
import argparse
import json
from pathlib import Path
import signal
import threading

from .cache import Cache
from .daemon import run
from .engine import StateError, status, utcnow


class Parser(argparse.ArgumentParser):
    def error(self, message):
        # Do not echo untrusted arguments/paths.
        self.exit(2, 'CGC: INVALID_ARGUMENTS (see --help)\n')


def main(argv=None):
    parser = Parser(description='CREDID GUARDIAN CODEX (CGC)')
    sub = parser.add_subparsers(dest='command', required=True, parser_class=Parser)
    for name in ('status', 'daemon'):
        p = sub.add_parser(name)
        p.add_argument('--cache-dir', type=Path, default=Path.home() / '.codex' / 'cgc')
        if name == 'status':
            p.add_argument('--json', action='store_true')
        else:
            p.add_argument('--bucket', action='append', required=True)
            p.add_argument('--max-reads', type=int, required=True)
            p.add_argument('--interval', type=int, default=300)
            p.add_argument('--max-age', type=int, default=900)
            p.add_argument('--timeout', type=int, default=20)
            p.add_argument('--live', action='store_true', required=True,
                           help='explicitly initiate live quota reads (no AI turns)')
    args = parser.parse_args(argv)
    try:
        # Status must not create a cache directory when none exists.
        if args.command == 'status' and not args.cache_dir.exists():
            # A dangling symlink is unsafe rather than an absent cache.
            if args.cache_dir.is_symlink():
                raise StateError('UNSAFE_CACHE')
            output = {'validity': 'UNKNOWN', 'policy_state': None, 'error_code': 'CACHE_MISSING'}
        else:
            with Cache(args.cache_dir, create=args.command == 'daemon') as cache:
                if args.command == 'daemon':
                    stop = threading.Event()
                    old = {s: signal.signal(s, lambda *_: stop.set()) for s in (signal.SIGINT, signal.SIGTERM)}
                    try:
                        attempts = run(cache, buckets=args.bucket, max_reads=args.max_reads,
                                       interval=args.interval, max_age=args.max_age,
                                       timeout=args.timeout, stop=stop)
                    finally:
                        for s, handler in old.items():
                            signal.signal(s, handler)
                    print(json.dumps({'attempts': attempts, 'stopped': stop.is_set()}))
                    final_state = cache.read()
                    return 0 if final_state and final_state['last_refresh_status'] == 'OK' else 1
                state = cache.read()
                output = status(state, now=utcnow()) if state else {'validity': 'UNKNOWN', 'policy_state': None, 'error_code': 'CACHE_MISSING'}
        if args.json:
            print(json.dumps(output, sort_keys=True, allow_nan=False))
        else:
            print('CREDID GUARDIAN CODEX (CGC)')
            print(f"Validity: {output['validity']}; policy: {output['policy_state'] or 'UNKNOWN'}")
            print(f"Mode: {output.get('mode') or 'UNKNOWN'}; coverage: {output.get('coverage', 'UNKNOWN')}; global all-clear: false")
            print(f"Age seconds: {output.get('age_seconds')}; refresh: {output.get('last_refresh_status', 'NEVER')}")
            for window in (output.get('observation') or {}).get('windows', []):
                print(f"{window['window_id']}: remaining={window['remaining_percent']}% ({window['value_origin']}), validity={window['validity']}, reset={window['reset_at']}")
            if output.get('error_code'):
                print('Error: ' + output['error_code'])
            if output.get('directive'):
                print(output['directive'])
        return 0 if output.get('live_policy_available') and output.get('last_refresh_status') == 'OK' else 1
    except (StateError, OSError, ValueError):
        # Fixed diagnostics: never print exception text or user/source paths.
        print(json.dumps({'validity': 'UNKNOWN', 'policy_state': None, 'error_code': 'CGC_OPERATION_FAILED'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
