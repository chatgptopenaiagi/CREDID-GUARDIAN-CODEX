"""CGC disposable M4 mechanical validation, NOT production or an R6 launcher.

Default: offline models, JSON evidence to stdout. --kernel: nonroot Linux only,
compile/run owned freestanding fixtures inside one TemporaryDirectory. No bus
connection, manager call, cgroup write, credential transition or privileged read.
Input vectors are the immutable adjacent documentation, not RPC/user commands.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

VERSION = 'CGC-M4-MECHANICAL-2'
ALLOW, DENY, KILL = 0x7fff0000, 0x50001, 0x80000000
ARCH = 0xc000003e
MAX64 = (1 << 64) - 1


def eq(i, v):
    return (i, v, v)


def le(i, v):
    return (i, 0, v)


def rule(nr, *predicates):
    return (nr, tuple(sorted(predicates)))


def union(*tables):
    # Explicit set union; canonical ordering never depends on dictionary order.
    return tuple(sorted(set(x for t in tables for x in t)))


def tables():
    final = (rule(60, le(0, 255)), rule(231, le(0, 255)), rule(228, eq(0, 1)))
    data = union(final, (rule(0, eq(0, 0), le(2, 1024)),
                        rule(1, eq(0, 1), le(2, 65536)),
                        rule(1, eq(0, 2), le(2, 65536))))
    c = union(data, tuple(rule(3, eq(0, fd)) for fd in range(4)),
              (rule(7, le(1, 4), le(2, 1000)),
               rule(46, eq(0, 3), eq(2, 16384)),
               rule(47, eq(0, 3), eq(2, 1073741824))))
    w = union(data, tuple(rule(3, eq(0, fd)) for fd in range(3)),
              (rule(39), rule(57), rule(61, eq(0, MAX64), eq(2, 0)),
               rule(61, eq(0, MAX64), eq(2, 1))))
    pbase = union(data, (rule(3, le(0, 5)), rule(39)))
    # Dummy bound C PID; replace only from retained launch identity in a future image.
    cp = 4242
    open_peer = tuple(rule(257, eq(0, MAX64 - 99), eq(2, flags), eq(3, 0))
                      for flags in (0xa0000, 0xa0001))
    direct = union(pbase, open_peer,
                   (rule(1, eq(0, 3), le(2, 32)), rule(5, eq(0, 3))))
    bus = union(pbase, (rule(41, eq(0, 1), eq(1, 0x80001), eq(2, 0)),
                        rule(42, eq(0, 3), le(2, 110)),
                        rule(0, eq(0, 3), le(2, 65536)),
                        rule(1, eq(0, 3), le(2, 65536))))
    p = {'P_T3': direct, 'P_T6': direct,
         'P_T4': union(direct, (rule(101, eq(0, 16), eq(1, cp), eq(2, 0), eq(3, 0)),
                                rule(101, eq(0, 17), eq(1, cp), eq(2, 0), eq(3, 0)),
                                rule(61, eq(0, cp), eq(2, 1)),
                                rule(267, eq(0, MAX64 - 99), le(3, 256)))),
         'P_T7': bus, 'P_T8': bus,
         'P_T9': union(pbase, (rule(46, eq(0, 3), eq(2, 16384)),)),
         'P_T14': union(pbase, (rule(46, eq(0, 3), eq(2, 16384)),))}
    # All operations are scalar constrained. Pointer contents are NOT cBPF checks.
    bread = tuple(rule(0, eq(0, fd), le(2, 65536))
                  for fd in (0, 19, 20, 21, 22, 23, 32, 33, 34, 35, 60, 61, 62, 63))
    bwrite = tuple(rule(1, eq(0, fd), le(2, 65536)) for fd in (1, 2, 16, 17, 18, 20))
    observation = union(final, bread, bwrite,
        (rule(3, le(0, 63)), rule(5, le(0, 63)),
         rule(7, le(1, 64), le(2, 1000)), rule(46, eq(0, 7), eq(2, 16384)),
         rule(47, eq(0, 7), eq(2, 1073741824)),
         rule(434, le(0, 0x7fffffff), eq(1, 0)),
         rule(247, eq(0, 3), (1, 8, 59), eq(3, 0x1000005), eq(4, 0)),
         rule(61, eq(0, MAX64), eq(2, 1)),
         rule(292, le(0, 63), (1, 44, 63), eq(2, 0x80000)),
         rule(217, eq(0, 21), le(2, 65536))),
        tuple(rule(17, eq(0, fd), le(2, 65536)) for fd in (19, 22, 23, 60, 61, 62, 63)),
        tuple(rule(257, eq(0, fd), eq(2, flag), eq(3, 0))
              for fd in (3, 4, 5, 6, 21) for flag in (0xa0000, 0xb0000)),
        tuple(rule(262, eq(0, fd), eq(3, 0x100)) for fd in (3, 4, 5, 6, 21)),
        tuple(rule(267, eq(0, fd), le(3, 256)) for fd in (3, 4, 5, 6, 21)),
        (rule(263, eq(0, 3), eq(2, 0x200)),))
    # Known runtime scalar values are deliberately not invented before launch.
    # These broad scalar predicates are explicit unresolved specialization gates.
    setup = union((rule(57), rule(39), rule(116, eq(0, 0)),
                   rule(117, le(0, 0xffffffff), le(1, 0xffffffff), le(2, 0xffffffff)),
                   rule(119, le(0, 0xffffffff), le(1, 0xffffffff), le(2, 0xffffffff)),
                   rule(118), rule(120), rule(115, le(0, 64)), rule(125), rule(126),
                   rule(317, eq(0, 1), eq(1, 0)), rule(318, le(1, 256), eq(2, 0)),
                   rule(302, eq(0, 0), eq(1, 7)),
                   rule(293, eq(1, 0x80800)),
                   rule(53, eq(0, 1), eq(1, 0x80005), eq(2, 0)),
                   rule(292, le(0, 63), le(1, 63), eq(2, 0x80000)),
                   rule(3, le(0, 63)), rule(5, le(0, 63))),
        tuple(rule(72, le(0, 63), eq(1, cmd), eq(2, 1 if cmd == 2 else 0)) for cmd in (1, 2, 3)),
        tuple(rule(157, eq(0, cmd), eq(1, val), eq(2, 0), eq(3, 0), eq(4, 0))
              for cmd, val in ((4, 0), (3, 0), (36, 1), (38, 1), (39, 0))),
        tuple(rule(157, eq(0, 24), eq(1, cap), eq(2, 0), eq(3, 0), eq(4, 0)) for cap in (6, 7, 8, 19)),
        (rule(157, eq(0, 47), eq(1, 4), eq(2, 0), eq(3, 0), eq(4, 0)),))
    gates = tuple(rule(0, eq(0, fd), le(2, 1024)) for fd in (3, 4))
    cb, wb = union(c, setup, gates), union(w, setup, gates)
    pb = union(setup, gates, *p.values())
    common = union(observation, cb, wb, pb)
    all_tables = dict(p, C_READY=c, W_RELEASED=w, C_BOOTSTRAP=cb,
                      W_BOOTSTRAP=wb, P_BOOTSTRAP=pb, B_SEALED=observation,
                      B_BOOT=common, B_CHILD_SETUP=common,
                      COMMON_BOOTSTRAP_FILTER=common)
    edges = [('COMMON_BOOTSTRAP_FILTER', 'B_BOOT'), ('B_BOOT', 'B_CHILD_SETUP'),
             ('B_CHILD_SETUP', 'B_SEALED'), ('B_CHILD_SETUP', 'C_BOOTSTRAP'),
             ('B_CHILD_SETUP', 'W_BOOTSTRAP'), ('B_CHILD_SETUP', 'P_BOOTSTRAP'),
             ('C_BOOTSTRAP', 'C_READY'), ('W_BOOTSTRAP', 'W_RELEASED')]
    edges += [('P_BOOTSTRAP', n) for n in sorted(p)]
    return all_tables, edges


def canonical(rules):
    if len(rules) != len(set(rules)):
        raise ValueError('duplicate clause')
    out = []
    for nr in sorted({x[0] for x in rules}):
        alternatives = sorted(x[1] for x in rules if x[0] == nr)
        for preds in alternatives:
            if len({x[0] for x in preds}) != len(preds):
                raise ValueError('duplicate/contradictory argument')
            for i, low, high in preds:
                if not (0 <= i < 6 and 0 <= low <= high <= MAX64):
                    raise ValueError('predicate')
                if low != high and high > 0xffffffff:
                    raise ValueError('range width')
        out.append((nr, alternatives))
    return out


def generate(rules):
    code = []
    def emit(op, jt=0, jf=0, k=0):
        code.append([op, jt, jf, k])
    emit(0x20, k=4); emit(0x15, jt=1, k=ARCH); emit(6, k=KILL)
    emit(0x20, k=0); emit(0x45, jf=1, k=0xc0000000); emit(6, k=KILL)
    for nr, alternatives in canonical(rules):
        for preds in alternatives:
            failures = []
            def fail():
                failures.append(len(code)); emit(5)
            emit(0x20, k=0); emit(0x15, jt=1, k=nr); fail()
            for i, low, high in preds:
                emit(0x20, k=20 + 8*i); emit(0x15, jt=1, k=high >> 32); fail()
                emit(0x20, k=16 + 8*i)
                if low == high:
                    emit(0x15, jt=1, k=low & 0xffffffff); fail()
                else:
                    if low:
                        emit(0x35, jt=1, k=low); fail()
                    emit(0x25, jf=1, k=high); fail()
            emit(6, k=ALLOW)
            for at in failures:
                code[at][3] = len(code) - at - 1
    emit(6, k=DENY)
    return code


def interpret(code, nr, args=(), arch=ARCH):
    raw = struct.pack('<IIQ6Q', nr & 0xffffffff, arch, 0, *(tuple(args)+(0,)*(6-len(args))))
    pc, acc = 0, 0
    for _ in range(len(code)+1):
        op, jt, jf, k = code[pc]; pc += 1
        if op == 0x20: acc = struct.unpack_from('<I', raw, k)[0]
        elif op == 5: pc += k
        elif op == 6: return k
        else:
            yes = {0x15: acc == k, 0x25: acc > k, 0x35: acc >= k, 0x45: bool(acc & k)}[op]
            pc += jt if yes else jf
    raise ValueError('no termination')


def subset(child, parent):
    def contains(p, c):
        cm = {i: (l, h) for i, l, h in c}
        return all(i in cm and l <= cm[i][0] <= cm[i][1] <= h for i, l, h in p)
    return all(any(n == pn and contains(pp, cp) for pn, pp in parent) for n, cp in child)


def filter_tests():
    policies, edges = tables(); result = {}
    for name, rules in sorted(policies.items()):
        code = generate(rules)
        assert code == generate(tuple(reversed(rules)))
        assert 0 < len(code) <= 4096, (name, len(code))
        for pos, (op, jt, jf, k) in enumerate(code):
            assert op in (0x20, 0x15, 0x25, 0x35, 0x45, 5, 6)
            if op == 5: assert pos < pos+1+k < len(code)
            if op in (0x15, 0x25, 0x35, 0x45): assert pos+1+max(jt, jf) < len(code)
        assert code[-1] == [6, 0, 0, DENY]
        for nr in (59, 322, 435, 272, 308, 110): assert interpret(code, nr) == DENY
        assert interpret(code, 1, arch=0x40000003) == KILL
        assert interpret(code, 0x40000001) == KILL
        assert interpret(code, 228, (1, 0)) == ALLOW
        # Test every clause witness plus each constrained interval boundary.
        witnesses = 0
        for nr, preds in rules:
            args = [0]*6
            for i, lo, hi in preds: args[i] = lo
            assert interpret(code, nr, args) == ALLOW, (name, nr, args)
            witnesses += 1
            for i, lo, hi in preds:
                for value in sorted({lo, hi, max(0,lo-1), min(MAX64,hi+1)}):
                    probe=list(args);probe[i]=value
                    accepted=any(n==nr and all(l<=probe[j]<=h for j,l,h in ps) for n,ps in rules)
                    assert interpret(code,nr,probe)==(ALLOW if accepted else DENY),(name,nr,probe)
                    witnesses += 1
        raw = b''.join(struct.pack('<HBBI', *x) for x in code)
        result[name] = dict(architecture=ARCH, count=len(code), instructions=code,
                            bytes=raw.hex(), sha256=hashlib.sha256(raw).hexdigest(),
                            rules=canonical(rules), witnesses=witnesses)
    for parent, child in edges: assert subset(policies[child], policies[parent]), (parent, child)
    aliases=[{'COMMON_BOOTSTRAP_FILTER','B_BOOT','B_CHILD_SETUP'}, {'P_T3','P_T6'},
             {'P_T7','P_T8'}, {'P_T9','P_T14'}]
    for a in result:
        for b in result:
            if a!=b and result[a]['sha256']==result[b]['sha256']:
                assert any({a,b}<=group for group in aliases),(a,b)
    for bad in ((rule(0), rule(0)), (rule(0, eq(0, 1), eq(0, 2)),)):
        try: canonical(bad)
        except ValueError: pass
        else: raise AssertionError('invalid rules accepted')
    return result, edges


class Reject(ValueError):
    pass


ARRAY = {'as': 's', 'ay': 'y', 'au': 'u', 'a(sv)': '(sv)',
         'a(sasb)': '(sasb)', 'a(sa(sv))': '(sa(sv))'}
RECORD = {'(sv)': ('s', 'v'), '(sasb)': ('s', 'as', 'b'), '(sa(sv))': ('s', 'a(sv)')}
ALIGN = {'s': 4, 'o': 4, 'g': 1, 'y': 1, 'u': 4, 'b': 4, 't': 8, 'v': 1}
SIGNATURES = {'': (), 's': ('s',), 'o': ('o',), 'ss': ('s', 's'),
              'u': ('u',), 't': ('t',), 'b': ('b',), 'v': ('v',),
              'sss': ('s', 's', 's'), 'sau': ('s', 'au'), 'ssau': ('s', 's', 'au'),
              'sba(sv)': ('s', 'b', 'a(sv)'),
              'ssa(sv)a(sa(sv))': ('s', 's', 'a(sv)', 'a(sa(sv))')}
VARIANTS = {'s', 'u', 't', 'b', 'as', 'ay', 'a(sasb)'}


def alignment(t):
    return 4 if t in ARRAY else 8 if t in RECORD else ALIGN[t]


class Cursor:
    def __init__(self, data, pos=0, end=None):
        self.data, self.pos, self.end = data, pos, len(data) if end is None else end

    def take(self, n):
        if n < 0 or n > self.end-self.pos: raise Reject('truncation')
        out = self.data[self.pos:self.pos+n]; self.pos += n
        return out

    def pad(self, n):
        if any(self.take((-self.pos) % n)): raise Reject('padding')

    def value(self, t, depth=0):
        if depth > 6: raise Reject('depth')
        if t not in ALIGN and t not in ARRAY and t not in RECORD: raise Reject('type')
        self.pad(alignment(t))
        if t in ('y', 'u', 'b', 't'):
            v = struct.unpack({'y': '<B', 'u': '<I', 'b': '<I', 't': '<Q'}[t],
                              self.take(1 if t == 'y' else 8 if t == 't' else 4))[0]
            if t == 'b' and v not in (0, 1): raise Reject('boolean')
            return v
        if t in ('s', 'o', 'g'):
            n = struct.unpack('<B' if t == 'g' else '<I', self.take(1 if t == 'g' else 4))[0]
            if n > 4096: raise Reject('string bound')
            raw = self.take(n)
            if self.take(1) != b'\0' or b'\0' in raw: raise Reject('terminator')
            try: s = raw.decode('ascii')
            except UnicodeError: raise Reject('ascii') from None
            if t == 'o' and not re.fullmatch(r'/(?:[A-Za-z0-9_]+(?:/[A-Za-z0-9_]+)*)?', s):
                raise Reject('path')
            return s
        if t == 'v':
            sig = self.value('g', depth)
            if sig not in VARIANTS: raise Reject('variant')
            return [sig, self.value(sig, depth+1)]
        if t in RECORD: return [self.value(k, depth+1) for k in RECORD[t]]
        n = struct.unpack('<I', self.take(4))[0]
        if n > 65536: raise Reject('array bound')
        self.pad(alignment(ARRAY[t]))
        if n > self.end-self.pos: raise Reject('array truncation')
        end, previous = self.pos+n, self.end
        self.end = end; result = []
        while self.pos < end:
            if len(result) >= 32: raise Reject('elements')
            result.append(self.value(ARRAY[t], depth+1))
        self.end = previous
        if t == 'a(sv)' and len({x[0] for x in result}) != len(result): raise Reject('duplicate property')
        return result


class Writer:
    def __init__(self): self.data = bytearray()
    def pad(self, n): self.data.extend(b'\0' * ((-len(self.data)) % n))
    def value(self, t, v):
        self.pad(alignment(t))
        if t in ('y', 'u', 'b', 't'):
            self.data.extend(struct.pack({'y': '<B', 'u': '<I', 'b': '<I', 't': '<Q'}[t], v))
        elif t in ('s', 'o', 'g'):
            b = v.encode('ascii')
            self.data.extend(struct.pack('<B' if t == 'g' else '<I', len(b))+b+b'\0')
        elif t == 'v': self.value('g', v[0]); self.value(v[0], v[1])
        elif t in RECORD:
            for k, x in zip(RECORD[t], v, strict=True): self.value(k, x)
        else:
            at = len(self.data); self.data.extend(b'\0'*4); self.pad(alignment(ARRAY[t]))
            start = len(self.data)
            for x in v: self.value(ARRAY[t], x)
            self.data[at:at+4] = struct.pack('<I', len(self.data)-start)


def frame(kind, serial, fields, sig, values, flags=0):
    b = Writer()
    for t, v in zip(SIGNATURES[sig], values, strict=True): b.value(t, v)
    h = Writer(); h.data.extend(b'\0'*16)
    for code, t, value in fields:
        h.pad(8); h.value('y', code); h.value('g', t); h.value(t, value)
    length = len(h.data)-16; h.pad(8)
    h.data[:16] = struct.pack('<BBBBIII', 108, kind, flags, 1, len(b.data), serial, length)
    return bytes(h.data+b.data)


def decode(data, expected=None, incoming=False):
    if len(data) < 16: raise Reject('fixed header')
    endian, kind, flags, version, blen, serial, hlen = struct.unpack_from('<BBBBIII', data)
    if endian != 108: raise Reject('endian')
    if version != 1: raise Reject('version')
    if kind not in ((2, 3, 4) if incoming else (1, 2, 3, 4)): raise Reject('message type')
    if flags & ~3 or not serial: raise Reject('flags/serial')
    if len(data) > 65536 or blen > 65536 or hlen > 4096: raise Reject('length bound')
    # bounded Python integers model required overflow-safe native subtract-before-add checks.
    head_end = 16+hlen; body_start = (head_end+7) & ~7
    if body_start > len(data) or blen != len(data)-body_start: raise Reject('frame length')
    cur = Cursor(data, 16, head_end); fields = {}
    field_types = {1:'o', 2:'s', 3:'s', 4:'s', 5:'u', 6:'s', 7:'s', 8:'g'}
    while cur.pos < cur.end:
        cur.pad(8); key = cur.value('y')
        if key == 9: raise Reject('UNIX_FDS')
        if key not in field_types: raise Reject('header field')
        if key in fields: raise Reject('duplicate header')
        t = cur.value('g')
        if t != field_types[key]: raise Reject('header variant')
        fields[key] = cur.value(t)
    if any(data[head_end:body_start]): raise Reject('padding')
    sig = fields.get(8, '')
    if sig not in SIGNATURES: raise Reject('signature')
    if kind==1:
        if expected is None:raise Reject('closed request selector')
        if sig!=expected['signature']:raise Reject('signature')
        if any(fields.get(k)!=expected[n] for k,n in ((1,'path'),(2,'interface'),(3,'member'),(6,'destination'))):
            raise Reject('closed request route')
    if incoming:
        if expected is None: raise Reject('missing context')
        if fields.get(7) != expected['sender']: raise Reject('sender')
        if kind in (2, 3) and fields.get(5) != expected['reply_serial']: raise Reject('reply serial')
        if kind == 4:
            actual = (fields.get(1), fields.get(2), fields.get(3))
            allowed = (('/org/freedesktop/DBus','org.freedesktop.DBus','NameOwnerChanged'),
                       ('/org/freedesktop/systemd1','org.freedesktop.systemd1.Manager','Reloading'))
            if actual not in allowed: raise Reject('signal route')
        elif kind == 2 and sig != expected['signature']: raise Reject('signature')
        elif kind == 3 and (not fields.get(4) or sig != 's'): raise Reject('error grammar')
    cur = Cursor(data, body_start)
    body = [cur.value(t) for t in SIGNATURES[sig]]
    if cur.pos != len(data): raise Reject('trailing body')
    if incoming and kind == 2 and sig == 'v':
        prop = expected.get('property')
        allowed = {'ControlGroup':'s', 'InvocationID':'ay', 'MainPID':'u', 'Version':'s', 'Features':'s'}
        if prop not in allowed or body[0][0] != allowed[prop]: raise Reject('property variant')
        if prop == 'InvocationID' and len(body[0][1]) != 16: raise Reject('invocation identity')
    if kind == 1:
        if expected is None: raise Reject('closed request selector')
        actual = dict(path=fields.get(1), interface=fields.get(2), member=fields.get(3),
                      destination=fields.get(6), signature=sig, body=body)
        if actual != expected: raise Reject('closed request structure')
        return actual
    if kind == 3:
        denial = fields[4] in ('org.freedesktop.DBus.Error.AccessDenied',
                               'org.freedesktop.DBus.Error.InteractiveAuthorizationRequired')
        if not denial or expected.get('test') not in ('T7', 'T8'): raise Reject('error not denial')
        return {'outcome': 'DENIED', 'error': fields[4]}  # Deliberately omit remote text.
    if kind == 4:
        if fields[3] == 'NameOwnerChanged':
            if sig != 'sss' or body[0] != 'org.freedesktop.systemd1': raise Reject('signal body')
            if body[1] != body[2]: raise Reject('owner generation changed')
        else:
            if sig != 'b': raise Reject('signal signature')
            raise Reject('manager continuity')
    return {'signature': sig, 'body': body}


def load_vectors(path):
    text = path.read_text(encoding='utf-8')
    records = {}
    for block in re.split(r'(?=### V-D\d+ )', text)[1:]:
        key = block.split()[1]
        logical = json.loads(re.search(r'~~~json\n(.*?)\n~~~', block, re.S)[1])
        h = bytes.fromhex(re.search(r'HEADER_HEX:\n~~~text\n([0-9a-f]+)', block)[1])
        b = re.search(r'BODY_HEX:\n~~~text\n([^\n]+)', block)[1]
        records[key] = (logical, h + (b'' if b == '(empty)' else bytes.fromhex(b)))
    return records, text


def rebuild(logical, serial):
    fields = [(1, 'o', logical['path']), (2, 's', logical['interface']),
              (3, 's', logical['member']), (6, 's', logical['destination'])]
    if logical['signature']: fields.append((8, 'g', logical['signature']))
    return frame(1, serial, fields, logical['signature'], logical['body'], 2)


def codec_tests(path):
    records, text = load_vectors(path); negatives = []; positives = []
    for key, (logical, raw) in sorted(records.items()):
        assert decode(raw, logical) == logical
        assert rebuild(logical, int(key[-2:])) == raw
        positives.append(key)
    def bad(key, base, raw, expected=None, incoming=False):
        try: decode(raw, expected if incoming else records[base][0], incoming)
        except Reject as err:
            negatives.append(dict(id=key, base=base, bytes=raw.hex(), rejection=str(err), outcome='INVALIDATED'))
        else: raise AssertionError(('negative accepted', key))
    def patch(base, offset, replacement):
        raw = records[base][1]; return raw[:offset]+replacement+raw[offset+len(replacement):]
    bad('V-D20','V-D01',patch('V-D01',0,b'B'))
    bad('V-D21','V-D01',patch('V-D01',3,b'\2'))
    # Duplicate first header using the entire canonical first field, then rebuild lengths.
    raw = records['V-D01'][1]; hlen = struct.unpack_from('<I', raw, 12)[0]
    h = raw[16:16+hlen]; duplicate = h+b'\0'*((-len(h))%8)+raw[16:46]
    f = bytearray(raw[:16]+duplicate); struct.pack_into('<I', f,12,len(duplicate)); f.extend(b'\0'*((-len(f))%8))
    bad('V-D22','V-D01',bytes(f))
    for key, field, value in [('V-D23','signature','sau'), ('V-D24','member','Reload'),
                              ('V-D25','interface','org.freedesktop.systemd1.Unknown'),
                              ('V-D28','path','/org//freedesktop/systemd1')]:
        obj = json.loads(json.dumps(records['V-D06'][0])); obj[field] = value
        if field == 'signature':
            original=records['V-D06'][0]
            fields=[(1,'o',original['path']),(2,'s',original['interface']),
                    (3,'s',original['member']),(6,'s',original['destination']),(8,'g','sau')]
            mutated=frame(1,6,fields,'ssau',original['body'],2)
        else: mutated = rebuild(obj,6)
        bad(key,'V-D06',mutated)
    raw = records['V-D06'][1]
    bad('V-D26','V-D06',raw[:-8]+struct.pack('<I',65537)+raw[-4:])
    bad('V-D27','V-D01',patch('V-D01',46,b'\1'))
    extra = [(1,'o','/org/freedesktop/DBus'),(2,'s','org.freedesktop.DBus'),
             (3,'s','Hello'),(6,'s','org.freedesktop.DBus'),(9,'u',0)]
    bad('V-D29','V-D01',frame(1,1,extra,'',[],2))
    context = {'sender':':1.42','reply_serial':1,'signature':'','test':'T7'}
    bad('V-D30','incoming',frame(2,1,[(5,'u',2),(7,'s',':1.42')],'',[]),context,True)
    bad('V-D31','incoming',frame(2,1,[(5,'u',1),(7,'s',':1.43')],'',[]),context,True)
    fields = [(1,'o','/org/freedesktop/DBus'),(2,'s','org.freedesktop.DBus'),
              (3,'s','NameOwnerChanged'),(7,'s','org.freedesktop.DBus'),(8,'g','sss')]
    bad('V-D32','incoming',frame(4,1,fields,'sss',['org.freedesktop.systemd1',':1.42',':1.43']),
        dict(context,sender='org.freedesktop.DBus'),True)
    obj=json.loads(json.dumps(records['V-D07'][0]));obj['body'][2][0][1]=['t',0]
    bad('V-D33','V-D07',rebuild(obj,7))
    bad('V-D34','V-D06',raw[:-1])
    error_fields=[(4,'s','org.freedesktop.DBus.Error.Failed'),(5,'u',1),(7,'s',':1.42'),(8,'g','s')]
    bad('V-D35','incoming',frame(3,1,error_fields,'s',['']),context,True)
    bad('V-D36','V-D01',patch('V-D01',4,b'\xff'*4))
    bad('V-D37','V-D01',patch('V-D01',12,b'\xff'*4))
    bad('V-D38','V-D01',records['V-D01'][1]+b'\0')
    obj=json.loads(json.dumps(records['V-D07'][0]));obj['body'][2] *= 2
    bad('V-D39','V-D07',rebuild(obj,7))
    # Unknown recursive signature: no generic variant descent is attempted.
    obj=json.loads(json.dumps(records['V-D07'][0]))
    obj['body'][2][0][1]=['v',['v',['s','x']]]
    bad('V-D40','V-D07',rebuild(obj,7))
    # Positive finite incoming replies/errors, no connection and no authority exercised.
    incoming=0
    for sig, body in [('',[]),('s',[':1.42']),('o',['/org/freedesktop/systemd1']),
                      ('v',[['ay',list(range(16))]])]:
        fields=[(5,'u',1),(7,'s',':1.42')]+([(8,'g',sig)] if sig else [])
        got=decode(frame(2,1,fields,sig,body),dict(context,signature=sig,property='InvocationID'),True)
        assert got == {'signature':sig,'body':body}; incoming += 1
    error_fields[0]=(4,'s','org.freedesktop.DBus.Error.AccessDenied')
    assert decode(frame(3,1,error_fields,'s',['unpublished']),context,True)['outcome']=='DENIED'
    incoming += 1
    mutations=0
    for key,(logical,raw) in sorted(records.items()):
        # Fixed header mutations and bounded truncation at every eighth byte.
        cases=[raw[:end] for end in range(0,len(raw),8)]
        cases += [raw[:off]+bytes([raw[off]^mask])+raw[off+1:]
                  for off in (0,1,3,4,7,12,15) for mask in (1,128)]
        for candidate in cases:
            mutations += 1
            try: actual=decode(candidate,logical)
            except Reject: continue
            # A syntactically valid changed serial is not in this mutation family.
            assert candidate in {v[1] for v in records.values()}, (key,actual)
    assert mutations <= 2000
    reasons=['endian','version','duplicate header','signature','closed request route','closed request route',
             'array bound','padding','path','UNIX_FDS','reply serial','sender','owner generation changed',
             'closed request structure','frame length','error not denial','length bound','length bound',
             'frame length','duplicate property','variant']
    for case in negatives:
        expected_reason=reasons[int(case['id'][-2:])-20]
        assert case['rejection']==expected_reason,(case['id'],case['rejection'],expected_reason)
        case['expected_rejection']=expected_reason
    return dict(positive=positives,incoming_positive=incoming,negative=negatives,mutations=mutations),text


def auth_tests():
    # Offline server-line parser. It cannot connect or negotiate another mechanism.
    def receive_ok(raw):
        if len(raw)>64 or not re.fullmatch(rb'OK [0-9a-fA-F]{32}\r\n',raw):
            raise Reject('auth response')
        return raw[3:-2].decode('ascii')
    positive=b'OK '+b'1'*32+b'\r\n'
    assert receive_ok(positive)=='1'*32
    for raw in (b'REJECTED EXTERNAL\r\n',b'DATA\r\n',b'AGREE_UNIX_FD\r\n',
                b'ERROR\r\n',positive+b'X',positive[:-1],b'OK '+b'g'*32+b'\r\n',b'X'*65):
        try:receive_ok(raw)
        except Reject:pass
        else:raise AssertionError('auth widening')
    return {'positive':1,'negative':8,'client_prefix_hex':(b'\0AUTH EXTERNAL '+b'1000'.hex().encode()+b'\r\n').hex(),
            'begin_hex':b'BEGIN\r\n'.hex(),'connection_executed':False}


def protocol_tests(text):
    # No JSON parser on the acceptance path: exact grammar then current tuple comparison.
    hex32 = rb'[0-9a-f]{32}'
    ready = rb'\{"NONCE":"'+hex32+rb'","TYPE":"READY","VERSION":1\}'
    request = (rb'\{"BROKER_GENERATION":"'+hex32+rb'","CONTROLLER_GENERATION":"'+hex32+
               rb'","DOMAIN_ID":"'+hex32+rb'","LAB_ID":"cgcq-'+hex32+
               rb'","OP":"(?:CREATE_OWN_DOMAIN|ATTACH_OWN_GATED_CHILD|SEAL|QUERY|REMOVE_OWN_EMPTY_DOMAIN)",'
               rb'"REQUEST_SEQUENCE":([1-9][0-9]{0,19}),"SEAL_EPOCH":"(?:0|'+hex32+rb')"\}')
    blocks=re.split(r'(?=### V-P\d+ )',text)[1:]; results=[]
    canonical={}
    for block in blocks[:6]:
        raw=re.search(r'~~~text\n(.*?)\n~~~',block,re.S)[1].encode()
        canonical[block.split()[1]]=raw
    def accept(raw, expected, ancillary):
        if len(raw)>1024 or ancillary!='one ucred(pid=4242,uid=62001,gid=62001)':return False
        match=re.fullmatch(request,raw)
        grammar=bool(re.fullmatch(ready,raw)) or bool(match and int(match[1]) <= MAX64)
        return grammar and raw==expected
    for block in blocks:
        key=block.split()[1];raw=re.search(r'~~~text\n(.*?)\n~~~',block,re.S)[1].encode()
        ancillary=re.search(r'Ancillary: (.*?)\. Expected:',block)[1]
        good='**ACCEPT_CANONICAL_ONLY**' in block
        expected=canonical.get(key,canonical['V-P01'] if key=='V-P20' else canonical['V-P04'])
        if key=='V-P23':expected=expected.replace(b'"SEAL_EPOCH":"0"',b'"SEAL_EPOCH":"'+b'5'*32+b'"')
        assert accept(raw,expected,ancillary)==good,key
        results.append(key)
    base=canonical['V-P04']; ancillary='one ucred(pid=4242,uid=62001,gid=62001)'
    for number in (b'0',b'03',b'-1',b'3.0',b'3e0',b'18446744073709551616'):
        assert not accept(base.replace(b'"REQUEST_SEQUENCE":3',b'"REQUEST_SEQUENCE":'+number),base,ancillary)
    return {'existing_cases':len(results),'additional_sequence_cases':6}


NATIVE = r'''
typedef unsigned long U;
typedef long L;
struct ins { unsigned short code; unsigned char jt,jf; unsigned int k; };
struct prog { unsigned short len; struct ins *filter; };
__attribute__((noinline,noclone)) static L call(U n,U a,U b,U c,U d,U e,U f) {
 register U r10 __asm__("r10")=d, r8 __asm__("r8")=e, r9 __asm__("r9")=f;
 L out;
 __asm__ volatile("syscall":"=a"(out):"a"(n),"D"(a),"S"(b),"d"(c),"r"(r10),"r"(r8),"r"(r9):"rcx","r11","memory");
 return out;
}
#define S(n,a,b,c,d,e,f) call(n,(U)(a),(U)(b),(U)(c),(U)(d),(U)(e),(U)(f))
#include "filters.h"
static int checks(void) {
 L t[2];
 if(S(228,1,t,0,0,0,0)!=0)return 11;
 if(S(110,0,0,0,0,0,0)!=-1)return 12;
 if(S(435,0,0,0,0,0,0)!=-1)return 13;
 if(S(59,0,0,0,0,0,0)!=-1)return 14;
 if(S(272,0,0,0,0,0,0)!=-1)return 15;
 if(S(101,0,0,0,0,0,0)!=-1)return 16;
 return 0;
}
static int run(unsigned int stage) {
 if(S(157,38,1,0,0,0,0)!=0)return 1;
 if(S(317,1,0,&programs[stage],0,0,0)!=0)return 2;
 int result=checks(); if(result)return result;
 if(stage==W_INDEX) {
  if(S(41,1,0x80001,0,0,0,0)!=-1)return 17;
  struct ins allow={6,0,0,0x7fff0000}; struct prog broad={1,&allow};
  if(S(317,1,0,&broad,0,0,0)!=-1)return 18;
  L child=S(57,0,0,0,0,0,0);
  if(child<0)return 19;
  if(child==0) {
   int child_result=checks();
   if(S(317,1,0,&broad,0,0,0)!=-1)child_result=21;
   S(60,child_result,0,0,0,0,0); __builtin_unreachable();
  }
  int status=0; if(S(61,-1,&status,0,0,0,0)!=child || status!=0)return 20;
 }
 return 0;
}
void entry(U *stack) {
 if(stack[0]!=2){S(60,99,0,0,0,0,0);__builtin_unreachable();}
 char *s=(char*)stack[2];unsigned int stage=0;
 for(unsigned int i=0;s[i];i++){if(i>1||s[i]<'0'||s[i]>'9'){S(60,98,0,0,0,0,0);__builtin_unreachable();}stage=stage*10+(unsigned int)(s[i]-'0');}
 if(stage>=STAGES){S(60,97,0,0,0,0,0);__builtin_unreachable();}
 S(60,run(stage),0,0,0,0,0);__builtin_unreachable();
}
__asm__(".global _start\n_start:\nmov %rsp,%rdi\nand $-16,%rsp\ncall entry\nud2\n");
'''


def fd_tests():
    import fcntl
    import socket
    import stat
    def observe(fd):
        st=os.fstat(fd)
        mode=fcntl.fcntl(fd,fcntl.F_GETFL) & os.O_ACCMODE
        link=os.readlink('/proc/self/fd/'+str(fd))
        info=Path('/proc/self/fdinfo/'+str(fd)).read_text()
        if len(info)>4096: raise Reject('fdinfo bound')
        kind=('pidfd' if link=='anon_inode:[pidfd]' else 'namespace' if link.startswith(('user:[','pid:['))
              else 'socket' if stat.S_ISSOCK(st.st_mode) else 'pipe' if stat.S_ISFIFO(st.st_mode)
              else 'regular' if stat.S_ISREG(st.st_mode) else 'character')
        return (kind,mode,st.st_dev,st.st_ino)
    def validate(actual,expected):
        if actual != expected: raise Reject('FD inventory')
    def snapshot():
        names=os.listdir('/proc/self/fd')
        if len(names)>64:raise Reject('FD count')
        result={}
        for name in names:
            fd=int(name)
            try:result[fd]=observe(fd)
            except OSError as err:
                # listdir's own already-closed directory FD is the sole permitted race.
                if err.errno!=9:raise
        return result
    with tempfile.TemporaryFile() as file:
        left,right=socket.socketpair();read,write=os.pipe()
        try:
            descriptors=(file.fileno(),left.fileno(),right.fileno(),read,write)
            inventory={fd:observe(fd) for fd in descriptors}
            baseline=snapshot();validate(snapshot(),baseline)
            extra=os.dup(file.fileno())
            try:
                try:validate(snapshot(),baseline)
                except Reject:pass
                else:raise AssertionError('live extra FD accepted')
            finally:os.close(extra)
            # State labels do not pretend these inert objects are real cgroup/pidfd roles.
            states=('B_READY','B_SEALED','C_GATED','C_READY','W_GATED','W_RELEASED','P_GATED','P_READY','TEARDOWN')
            checks=0
            for state in states:
                validate(inventory,dict(inventory));checks+=1
                variants=[dict(inventory,**{})]
                variants[0][63]=('unknown',0,0,0)
                for kind in ('namespace','cgroup','pidfd','socket','wrong-type'):
                    x=dict(inventory);fd=descriptors[0];v=x[fd];x[fd]=(kind,*v[1:]);variants.append(x)
                for index in (1,2,3):
                    x=dict(inventory);fd=descriptors[0];v=list(x[fd]);v[index]^=1;x[fd]=tuple(v);variants.append(x)
                for variant in variants:
                    try:validate(variant,inventory)
                    except Reject:checks+=1
                    else:raise AssertionError(state)
        finally:left.close();right.close();os.close(read);os.close(write)
    return {'checks':checks,'live_extra_fd_refused':True,
            'scope':'bounded own /proc FD snapshot plus model state inventories; not root/cgroup identities'}


def kernel_tests(filters):
    if sys.platform!='linux' or os.getuid()==0 or os.uname().machine!='x86_64':
        raise SystemExit('requires nonroot native x86-64 Linux')
    result={}
    with tempfile.TemporaryDirectory(prefix='cgc-m4-',dir='/tmp') as temp:
        d=Path(temp);names=sorted(filters);header=[]
        for i,name in enumerate(names):
            listing=filters[name]['instructions']
            header.append('static struct ins f%d[]={%s};'%(i,','.join('{%d,%d,%d,%d}'%tuple(x) for x in listing)))
        header.append('static struct prog programs[]={'+','.join('{%d,f%d}'%(filters[n]['count'],i) for i,n in enumerate(names))+'};')
        header.append('#define STAGES '+str(len(names)))
        header.append('#define W_INDEX '+str(names.index('W_RELEASED')))
        (d/'filters.h').write_text('\n'.join(header));(d/'fixture.c').write_text(NATIVE)
        argv=['/usr/sbin/gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-ffreestanding',
              '-fno-builtin','-fno-stack-protector','-fno-pie','-mno-red-zone','-nostdlib',
              '-static','-no-pie','-Wl,--build-id=none','-Wl,-z,noexecstack','fixture.c','-o','fixture']
        subprocess.run(argv,cwd=d,check=True,capture_output=True,timeout=20)
        elf=subprocess.check_output(['/usr/sbin/readelf','-hldWs',str(d/'fixture')],timeout=5).decode()
        dis=subprocess.check_output(['/usr/sbin/objdump','-d',str(d/'fixture')],timeout=5).decode()
        assert 'Advanced Micro Devices X86-64' in elf and 'INTERP' not in elf and '(NEEDED)' not in elf
        assert not re.search(r'\bUND[ \t]+\S',elf)
        assert len(re.findall(r'\bsyscall\b',dis))==1
        for i,name in enumerate(names):
            run=subprocess.run([str(d/'fixture'),str(i)],stdin=subprocess.DEVNULL,
                               capture_output=True,timeout=5)
            result[name]=run.returncode
            assert run.returncode==0,(name,run.returncode,run.stderr)
        result['image_sha256']=hashlib.sha256((d/'fixture').read_bytes()).hexdigest()
        result['source_sha256']=hashlib.sha256(NATIVE.encode()).hexdigest()
        result['compiler']=subprocess.check_output(['/usr/sbin/gcc','--version'],timeout=5).decode().splitlines()[0]
        result['compile_argv']=argv
        result['disassembly_sha256']=hashlib.sha256(dis.encode()).hexdigest()
        result['syscall_sites']=1;result['fd_validator']=fd_tests()
        result['directory']=temp
    result['cleanup']=not Path(temp).exists()
    return result


def main():
    if sys.argv[1:] not in ([],['--kernel']): raise SystemExit('only fixed --kernel selector is supported')
    path=Path(__file__).resolve().parents[1]/'V3_QUIESCENCE_LAB_VECTORS.md'
    filters,edges=filter_tests();codecs,text=codec_tests(path)
    result={'version':VERSION,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'filters':filters,'transitions':edges,'dbus':codecs,'auth':auth_tests(),'protocol':protocol_tests(text),
            'production_accepted':False}
    if sys.argv[1:]:result['kernel']=kernel_tests(filters)
    print(json.dumps(result,sort_keys=True,separators=(',',':')))


if __name__=='__main__':main()
