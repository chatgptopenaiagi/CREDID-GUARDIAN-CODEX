"""CREDID GUARDIAN CODEX (CGC) cache status and explicitly bounded observation."""
import argparse
import json
from pathlib import Path
import signal
import threading

from .cache import Cache
from .daemon import run
from .engine import StateError, status, utcnow, PolicyConfig, DEFAULT_POLICY, MAX_AGE, SCHEMA_VERSION, validate_max_age


class Parser(argparse.ArgumentParser):
    def error(self, message):
        # Do not echo untrusted arguments/paths.
        self.exit(2, 'CGC: INVALID_ARGUMENTS (see --help)\n')


def unavailable_status(code, *, error=False):
    return {'schema_version': SCHEMA_VERSION, 'validity': 'UNKNOWN',
            'freshness': 'ERROR' if error else 'UNKNOWN', 'data_disposition': 'UNAVAILABLE',
            'policy_state': None, 'policy_available': False, 'live_policy_available': False,
            'error_code': code}


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
            p.add_argument('--max-age', type=int, default=MAX_AGE)
            p.add_argument('--timeout', type=int, default=20)
            for field, default in DEFAULT_POLICY.to_dict().items():
                p.add_argument('--' + field.replace('_', '-'), type=float, default=default,
                               help='inclusive remaining-percent upper boundary')
            p.add_argument('--live', action='store_true', required=True,
                           help='explicitly initiate live quota reads (no AI turns)')
    args = parser.parse_args(argv)
    try:
        config = (PolicyConfig(args.amber_at, args.red_at, args.emergency_at)
                  if args.command == 'daemon' else None)
        if args.command == 'daemon':
            validate_max_age(args.max_age)
        # Status must not create a cache directory when none exists.
        if args.command == 'status' and not args.cache_dir.exists():
            # A dangling symlink is unsafe rather than an absent cache.
            if args.cache_dir.is_symlink():
                raise StateError('UNSAFE_CACHE')
            output = unavailable_status('CACHE_MISSING')
        else:
            with Cache(args.cache_dir, create=args.command == 'daemon') as cache:
                if args.command == 'daemon':
                    stop = threading.Event()
                    old = {s: signal.signal(s, lambda *_: stop.set()) for s in (signal.SIGINT, signal.SIGTERM)}
                    try:
                        attempts = run(cache, buckets=args.bucket, max_reads=args.max_reads,
                                       interval=args.interval, max_age=args.max_age,
                                       timeout=args.timeout, stop=stop, config=config)
                    finally:
                        for s, handler in old.items():
                            signal.signal(s, handler)
                    print(json.dumps({'attempts': attempts, 'stopped': stop.is_set()}))
                    final_state = cache.read()
                    return 0 if final_state and final_state['last_refresh_status'] == 'OK' else 1
                state = cache.read()
                output = status(state, now=utcnow()) if state else unavailable_status('CACHE_MISSING')
        if args.json:
            print(json.dumps(output, sort_keys=True, allow_nan=False))
        else:
            print('CREDID GUARDIAN CODEX (CGC)')
            print(f"Freshness: {output['freshness']}; Data: {output['data_disposition']}")
            print(f"Validity: {output['validity']}; policy: {output['policy_state'] or 'UNKNOWN'}")
            print(f"Mode: {output.get('mode') or 'UNKNOWN'}; coverage: {output.get('coverage', 'UNKNOWN')}; global all-clear: false")
            print(f"Age seconds: {output.get('age_seconds')}; refresh: {output.get('last_refresh_status', 'NEVER')}")
            thresholds = output.get('historical_policy', {}).get('thresholds')
            if thresholds:
                print(f"Thresholds: AMBER <= {thresholds['amber_at']:g}%; RED <= {thresholds['red_at']:g}%; EMERGENCY <= {thresholds['emergency_at']:g}%")
            observation = output.get('observation')
            if observation:
                print(f"Source: {observation['source']}; observed: {observation['observed_at']}")
            origins = {w['window_id']: w for w in output.get('provenance', {}).get('latest', {}).get('windows', [])}
            diagnostics = {w['window_id']: w for w in output.get('evaluated_policy', {}).get('window_diagnostics', [])}
            for window in (output.get('observation') or {}).get('windows', []):
                print(f"{window['window_id']}: remaining={window['remaining_percent']}% ({origins[window['window_id']]['remaining_percent']}), validity={window['validity']}, reset={window['reset_at']}")
                diagnostic = diagnostics.get(window['window_id'])
                if diagnostic:
                    print(f"  applicability={diagnostic['applicability']}; evidence={diagnostic['evidence_basis']}; selected={diagnostic['selected']}; exclusions={','.join(diagnostic['exclusion_reasons']) or 'NONE'}")
            print('Most constrained applicable: ' + (', '.join(output.get('limiting_window_ids', [])) or 'UNKNOWN'))
            if output.get('reason'):
                print('Reason: ' + output['reason'])
            retained = output.get('last_valid_observation')
            if retained and (not output.get('policy_available') or retained != observation or output['historical_policy'] != output.get('evaluated_policy')):
                historical = output['historical_policy']
                print(f"Last known good (HISTORICAL, {output['last_known_good_freshness']['state']}): {retained['observed_at']}; policy={historical['policy_state']}; limiting={','.join(historical['limiting_window_ids'])}")
            if output.get('error_code'):
                print('Error: ' + output['error_code'])
            if output.get('directive'):
                print(output['directive'])
        return 0 if output.get('live_policy_available') and output.get('last_refresh_status') == 'OK' else 1
    except (StateError, OSError, ValueError):
        # Fixed diagnostics: never print exception text or user/source paths.
        print(json.dumps(unavailable_status('CGC_OPERATION_FAILED', error=True)))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
