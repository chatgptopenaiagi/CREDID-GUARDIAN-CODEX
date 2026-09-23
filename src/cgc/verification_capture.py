"""Explicit I/O bridge to the existing collector; never invoked by pure verification.

The private in-memory binding is provenance within the trusted Python caller boundary,
not authentication against hostile same-user Python code and not mutation authority.
"""
from dataclasses import dataclass
from . import reconciliation as rc

_SEAL = object()


@dataclass(frozen=True)
class Capture:
    _json: str
    _seal: object

    @property
    def projection(self):
        import json
        return json.loads(self._json)


def capture(project, **kwargs):
    """Explicit bounded I/O, exactly one unchanged reconciliation invocation."""
    return Capture(rc.render_json(rc.reconcile(project, **kwargs)), _SEAL)


def matches(binding, projection):
    """Pure comparison; serialized labels cannot create a binding."""
    return (type(binding) is Capture and binding._seal is _SEAL
            and binding._json == rc.render_json(projection))
