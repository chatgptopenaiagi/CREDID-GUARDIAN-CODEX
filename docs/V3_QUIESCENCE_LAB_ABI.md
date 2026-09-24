# CGC V3 — disposable native lab ABI

Status: **DESIGN / PARTIAL; NOT AN IMPLEMENTATION OR EXECUTION APPROVAL**.
Companion to [quiescence section 16](V3_QUIESCENCE.md#16-m1m5-installed-evidence-and-native-contract--2026-09-24).
Scope: ROOT_OWNED_BROKER_WITH_BOUND_CONTROLLER, CGC_LAB_R1R5_1, Linux x86-64 only.
This single companion keeps mechanical ABI details out of the evidence narrative. No production
schema or src/tests change. Normative requirements below are proposed, not tested role enforcement.

## 1. Native image and build

Choose C11 plus one x86-64 assembly entry/syscall veneer. Fixed branches B, C, W, P_C and P_W
are selected internally from the root-reviewed test enum, never from user-supplied code/argv.
Source set: start.S, sys_x86_64.h, lab.c, protocol.c, policy.c, sha256.c, dbus_fixed.c.
No libc, libsystemd, dynamic loader, TLS, threads, allocator, constructors, plugins or post-start exec.
This avoids unavailable static glibc and libsystemd development metadata. It also makes the
hand-written parser/D-Bus surface a review burden, not an assumed security improvement.

Proposed compile/link vector, inputs only from an exclusively created build directory:

~~~text
/usr/sbin/gcc -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-builtin
-fno-stack-protector -fno-pie -mno-red-zone -nostdlib -static -no-pie
-Wl,--build-id=none -Wl,-z,noexecstack
start.S lab.c protocol.c policy.c sha256.c dbus_fixed.c -o cgc-lab
~~~

All lines above form one argv vector, not separate commands or shell text. Explicit -I only for reviewed source directory
and compiler/kernel headers recorded in build manifest; environment clear except LANG=C/LC_ALL=C,
SOURCE_DATE_EPOCH fixed in build record (does not prove reproducibility). Compiler observed:
GCC 16.2.1 20260819 (Red Hat 16.2.1-2), ld 2.46.1-1.fc44. Record realpath, package identity and
digest of compiler/linker/used headers, exact source bytes, flags and output SHA256. No floating
download, package install or hidden include directory. Inspect ELF class=64, machine=x86-64,
little-endian, static ET_EXEC, no INTERP/NEEDED, no undefined symbols, non-executable stack.
Build twice only in later artifact acceptance if reproducibility is claimed; none claimed here.

Privileged launcher must independently compare the approved digest before executing B.
B also checks its own opened image and manifest, device/inode/mount identity, root ownership,
0500 image/0600 manifest, no symlinks/set-ID/file capabilities and protected ancestors. Self-check
does not authenticate the executable that already ran. B binds retained handles, not path alone.

Preallocate bounded buffers before role release: per-process <=1 MiB private mutable data,
64 KiB manifest, 1024-byte lab packet, 64 KiB D-Bus frame, fixed recursion-free parsers.
No mmap/brk after entry is needed for this proposed freestanding design. Unexpected compiler
runtime calls, unresolved symbols or new syscalls block acceptance rather than extending policy.

## 2. Kernel ABI and role filters

Syscall veneer uses x86-64 syscall instruction, rax number, rdi/rsi/rdx/r10/r8/r9 arguments,
rcx/r11/memory clobbers and negative errno returns. Do not invoke glibc fork (which may use clone).
All pointers/structures use installed x86-64 UAPI layout with compile-time size/offset assertions.
No i386/x32 support despite i686 glibc being installed. Signal handlers absent; default terminating
signals invalidate. poll handles EINTR by budget check without restarting privileged operations.

Policy representation: each named set below expands to exact syscall numbers shown. Compile
classic BPF in ascending syscall-number order; same-number argument alternatives are OR branches.
Load arch at seccomp_data offset 4: unequal AUDIT_ARCH_X86_64 (0xc000003e) -> KILL_PROCESS.
Load nr at offset 0: x32 bit 0x40000000 or negative -> KILL_PROCESS.
For matching numbers compare both 32-bit halves of constrained 64-bit scalar arguments.
Unmatched call or argument -> ERRNO|EPERM (0x00050001); allowed -> ALLOW (0x7fff0000).
No TRACE, USER_NOTIF, log listener or fallback. BPF installation: seccomp(317,
SECCOMP_SET_MODE_FILTER=1, flags=0, exact sock_fprog) after no_new_privs=1.
Only one thread; no TSYNC needed. Failure terminates gated setup before release.

| Set | Exact syscall:number entries | Purpose / scalar restrictions |
|---|---|---|
| EXIT | exit:60, exit_group:231 | Fixed exit status 0..255 |
| CLOCK | clock_gettime:228 | CLOCK_MONOTONIC=1 only |
| C_IO | read:0, write:1, close:3, poll:7, sendmsg:46, recvmsg:47 | read only 0; write only 1/2; close 0..3; poll nfds<=4 timeout 0..1000; send/recv only 3, flags send=MSG_NOSIGNAL, recv=MSG_CMSG_CLOEXEC |
| W_IO | read:0, write:1, close:3, poll:7 | read 0/3; write 1/2; close 0..3; poll nfds<=4 timeout 0..1000 |
| W_CHILD | fork:57, wait4:61, getpid:39 | fork no arguments; wait4 pid=-1 or bound child PID, options=WNOHANG or 0; getpid for fixed test payload |
| B_IO | read:0, write:1, close:3, fstat:5, pread64:17, poll:7, sendmsg:46, recvmsg:47, getdents64:217, readlinkat:267, newfstatat:262, openat:257 | FDs/dirfds only B inventory; read/write lengths<=65536; poll nfds<=64 timeout 0..1000; send/recv only channel/bus slots; filenames selected by fixed B code, not packet input |
| B_CREATE | mkdirat:258, unlinkat:263, pipe2:293, socketpair:53, socket:41, connect:42, setsockopt:54, getsockopt:55, dup3:292, fcntl:72 | Setup only, own objects; pipe CLOEXEC/NONBLOCK; AF_UNIX only; dup targets 0..63 with CLOEXEC; fcntl only F_GETFD/F_GETFL/F_SETFD(FD_CLOEXEC) |
| B_CHILD | fork:57, pidfd_open:434, waitid:247, wait4:61, getpid:39 | Owned child slots only; pidfd_open flags=0; waitid P_PIDFD and WEXITED|WNOHANG|WNOWAIT; no signal syscall |
| BOOT_CRED | setgroups:116, setresgid:119, setresuid:117, getresuid:118, getresgid:120, getgroups:115, capget:125, capset:126, prctl:157, prlimit64:302, seccomp:317 | Trusted root bootstrap only; IDs from manifest; prctl only dumpability, no_new_privs, cap bounding/ambient drops and B subreaper; limits only current process |
| RANDOM | getrandom:318 | flags=0; total requested<=256 bytes per role before READY |
| P_IO | read:0, write:1, close:3, poll:7, openat:257, fstat:5, readlinkat:267, socket:41, connect:42, sendmsg:46, recvmsg:47, getpid:39, ptrace:101 | Fixed test branch only, FD 0..5, AF_UNIX, frame<=65536; T4 ptrace PTRACE_ATTACH/DETACH only against bound owned C; no unrelated target |

Argument descriptions involving pointed-to memory or dynamic child IDs are trusted-code checks,
not claims that classic BPF can inspect them. B/P exact scalar specialization is generated from
manifest-bound FDs/child slots before filters are installed. W wait4 permits -1 for its own children;
no W-supplied PID controls B. OPENAT in B/P cannot be pathname-filtered by this BPF: root B is TCB,
P has unprivileged credentials and only fixed test logic. Unknown direct syscalls default deny.

Role policies:

- B_BOOT: trusted entry, before external request acceptance. B_IO+B_CREATE+B_CHILD+BOOT_CRED+
  RANDOM+CLOCK+EXIT; bootstrap syscall inventory checked statically, filter installed after
  initial FD normalization (no claim of confinement before installation).
- B_READY: same set while owned bootstraps are gated; filter stacking must leave child credential
  operations possible until children install their narrower role filters.
- B_SEALED: B_IO+B_CHILD+CLOCK+EXIT plus unlinkat for empty-only teardown; remove fork from
  B_CHILD, disallow writes to migration/topology FD classes by closing those FDs before ACK.
  dup3 is additionally permitted only for remapping new observation handles to slots 44..63;
  source type/read-only provenance is verified by trusted B code before remapping.
  B_IO openat becomes read-only O_RDONLY|O_CLOEXEC|O_NOFOLLOW, optionally O_DIRECTORY;
  writes only data/log/channel FDs, never cgroup controls. No credential changes after final drop.
- C_READY: C_IO+CLOCK+EXIT. No fork, pathname open, new socket, exec, cap change or prctl.
- W_GATED/W_RELEASED/descendant: W_IO+W_CHILD+CLOCK+EXIT; FD 3 closed before W forks.
- P_C/P_W: P_IO+CLOCK+EXIT, plus only test-required operations in the finite table in section 5.
  Peers are outside contained domain; their lesser restrictions never count as containment proof.

Explicitly denied after bootstrap unless named above: clone:56, clone3:435, vfork:58,
execve:59, execveat:322, ppoll:271 (use poll), rt_sigaction:13, rt_sigprocmask:14,
rt_sigreturn:15 (no handlers), futex:202, set_tid_address:218, set_robust_list:273,
rseq:334, mmap:9, mprotect:10, brk:12, arch_prctl:158, close_range:436 (explicit closes),
pidfd_send_signal:424, openat2:437, statx:332, ioctl:16, memfd_create:319,
io_uring/keyrings/mount/unshare/setns/process_vm_* and all nonlisted numbers.
Any actual runtime dependency on these falsifies this proposed freestanding build contract.
C/W behavior is deterministic enough to specify filters; compiled full-role artifacts do not
exist. B/P pointer-bound checks and D-Bus parser still require implementation review, not PASS.

## 3. FD inventory by phase

All installed FDs are CLOEXEC, including remapped standard FDs; no post-start exec is supported.
B_BOOT entry has only 0=/dev/null read, 1/2=bounded output pipes write. Unexpected inherited FD
refuses before fork. Slots below are fixed logical numbers, not serialized capabilities.

| B FD | Object and mode | Lifetime / inheritance |
|---|---|---|
| 3 / 4 / 5 / 6 | Parent/control/workers/peers directories, read-only directory handles | B only; 5 absent until CREATE |
| 7 | Broker socketpair endpoint, read/write | B_READY through channel retirement |
| 8..11 | C/W/P_C/P_W launch pidfds, in that order | Optional peer slots closed if test lacks peer; B only |
| 12..15 | C/W/P_C/P_W bootstrap gate write ends | Close each after fixed release/abort; C never owns these |
| 16..18 | events.jsonl, observations.jsonl, cleanup.json, write-only | B only; close before exit |
| 19 | workers/cgroup.events read-only | CREATE through worker-domain retirement |
| 20 | B system-bus observer socket | Never inherited past child bootstrap |
| 21 / 22 / 23 | /proc directory / manifest / image read-only handles | B only; digest verification before request acceptance |
| 24 | workers/cgroup.procs writable | Only controlled attach; close before SEAL ACK |
| 25 | control/cgroup.procs writable | Setup movement; close before SEAL ACK |
| 26 | peers/cgroup.procs writable | Predeclared peers only; close before SEAL ACK |
| 27..31 | Closed | Never occupied in a stable state |
| 32..35 | C/W/P_C/P_W output read pipes | B only; each child's FD 1/2 duplicate the same write pipe |
| 36..39 | Closed | Never occupied in stable state |
| 40..43 | Temporary root-bootstrap pipe/socket ends | Closed before B_READY, except creation of next predeclared child; never stable after seal |
| 44..59 | Owned adopted-descendant pidfds in increasing admission order | At most remaining task budget; B only; exhaustion invalidates |
| 60..63 | B scratch read-only observation handles | At most one operation at a time; close before dispatch/ACK |

Kernel allocation returns lowest free descriptors; trusted bootstrap verifies against its tracked
free-slot map, dup3-remaps to specified slot and closes original. This transient allocation state
is not B_READY/SEALED and accepts no requests. No 'unknown extra FD' exception. Filter compares
actual stable FD numbers, inventory verification includes fdinfo/access mode and object identity.

C_GATED: 0/1/2 above; 3=C channel; 4=bootstrap gate read; everything else closed.
C_READY: 0/1/2/3 only, gate 4 already closed.
W_GATED: 0/1/2; 3=release gate read; no others.
W_RELEASED and descendant: only 0/1/2; close 3 before test or fork.
P_GATED: 0/1/2; 3=bootstrap gate. P_READY closes it then may use 3/4/5 for exactly its test.
T9 deliberately places duplicate C endpoint in P FD 3; this is adversarial injection, not a
normal launch inventory. T5 inserts forbidden W FD 4 and must refuse release. T14 transfers
C's data FD 1 as SCM_RIGHTS, never a real privileged control FD.
B_SEALED: 12..15,24..26,40..43 closed; live observation handles above remain.
TEARDOWN: monotonically close retained handles; no new authority handle or child. Empty worker
removal precedes C exit; occupied control child is removed by administrator only after B exit.

Two unresolved mechanical conflicts require artifact review before this table becomes executable:
a B filter inherited across fork must admit each child bootstrap until narrowing, and retained
B syscall argument specializations must not accidentally exclude child FD remapping. Generate
a distinct bootstrap filter stage rather than reusing B_SEALED. Exact generated cBPF bytes and
negative tests for these stages remain outstanding; no engineer may silently loosen the sets.

## 4. CGC_LAB_PROTO_V1

Lab protocol is independent of D-Bus. One SOCK_SEQPACKET packet, 1..1024 bytes, no length prefix,
UTF-8 restricted to ASCII bytes, no BOM/NUL/newline/whitespace/escape sequences. Fixed JSON object
with lexically ordered keys. Requests have exactly this order:
BROKER_GENERATION, CONTROLLER_GENERATION, DOMAIN_ID, LAB_ID, OP, REQUEST_SEQUENCE, SEAL_EPOCH.
All values quoted strings except sequence; generations/domain are exactly 32 lowercase hex digits,
LAB_ID is cgcq- plus 32 such digits; OP one of the five section-15 names. SEAL_EPOCH quoted "0"
pre-seal or 32 hex digits post-seal. Sequence digits 1..18446744073709551615 with no sign,
leading zero, fraction or exponent. Increment once per accepted request; wrap invalidates.
Equality is byte-exact; parser compares canonical re-encoding. No general JSON parser extensions.

READY bytes: {"NONCE":"<32 lowercase hex>","TYPE":"READY","VERSION":1}.
Reply order inserts RESULT between REQUEST_SEQUENCE and SEAL_EPOCH; value OK or INVALIDATED.
SEAL OK includes newly allocated epoch. No reply is sent on unauthenticated/malformed input;
retire channel. A trustworthy authenticated request with invalid state may receive INVALIDATED
before close. No free-text error, path, raw PID, FD or shell field.

Linux receive buffer reserves CMSG_SPACE(sizeof(struct ucred)) plus space for at most 16 received
FDs to safely dispose of malicious ancillary data; MSG_CMSG_CLOEXEC set. Exactly one SCM_CREDENTIALS,
length=CMSG_LEN(sizeof(struct ucred)), expected PID/UID/GID required. Any rights, duplicate/unknown
control, MSG_TRUNC/MSG_CTRUNC or length mismatch closes received FDs and invalidates. Kernel-closed
excess rights under truncation do not make truncation acceptable. Send no explicit spoofed credentials.
SO_PEERCRED is diagnostic only, never substitutes for current sender checks.

Decoder order: RECEIVE -> VALIDATE_LENGTH -> VALIDATE_CREDENTIAL_ANCILLARY -> REJECT_RIGHTS ->
PARSE_CANONICAL_PAYLOAD -> VERIFY_GENERATIONS -> VERIFY_SEQUENCE -> VERIFY_CALLER_INSTANCE ->
VERIFY_STATE -> DISPATCH_FIXED_OP -> GENERATE_CANONICAL_REPLY. Every failure invalidates;
no automatic reconnect or broadened retry. Correlated nonce/digest is not caller authentication.
Dispatch follows section 15, including no late attach and no queued epoch-0 request after seal.

## 5. Fixed peer and manager adapter boundary

No generic client API. P_C/P_W get one compiled test selector and immutable manifest-derived
targets; no caller-selected path, PID, interface/member or argument vector. Limits per invocation:
B+C+W+one descendant+two peers, hard task ceiling 16; 64 FDs/process; at most 8 privileged lab
requests, 8 mutation-attempt manager calls total, 32 read-only bus calls, 64 KiB/frame,
256 KiB bus traffic total, 1 MiB/log, 10-second phase and 120-second overall budget.
Timeout invalidates and retains unresolved survivors; no kill operation. Threads/fork storms
are not a supported workload. Finite fixed test logic, not timeout alone, bounds execution.

| Peer selector | Exact permitted action set |
|---|---|
| T3 | Open workers cgroup.procs then cgroup.threads, write own PID once to each |
| T4 | T3 plus at most 4 attach/proc-FD attempts against bound C in distinct bootstrap phases; allow wait4:61 only for that attached target to confirm stop before detach; successful attach falsifies, never inject code |
| T6 | Same objects through two reviewed existing aliases; absent aliases NOT_EXECUTED; no mount creation |
| T7 | Manager AttachProcessesToUnit(unit,"workers",[self]); service AttachProcesses("workers",[self]) |
| T8 | One StartTransientUnit for fixed LAB_ID-peer.service, mode fail, fixed lab image; one SetUnitProperties(lab,true,[("Description",fixed "CGC lab unauthorized probe")]) |
| T9 | One valid-looking current tuple on deliberately duplicated C endpoint; wrong PID must invalidate |
| T14 | C sends one data FD as rights; W invokes denied recvmsg; no root FD leak |

T8's subordinate unit would be unauthorized even if execution fails; an unexpectedly created
unit must be retained for scoped review, not silently stopped by this client.
Successful ptrace attachment in T4 is falsification, not accepted diagnostic inspection.

Manager adapter is confined to /run/dbus/system_bus_socket, AF_UNIX stream. Socket is created
after peer credential drop; no inherited root-authenticated connection. SASL EXTERNAL identity
is hex encoding of decimal own UID, no cookie mechanism, no interactive-authorization flag,
no activation fallback, no UNIX_FD negotiation. Only org.freedesktop.DBus Hello/GetNameOwner/
AddMatch and fixed systemd GetUnit/Properties.Get/Subscribe plus the T7/T8 methods above.
B's adapter excludes every mutation method; the external approved administrator performs launch.

D-Bus wire v1, little-endian, fixed type-specific signatures and padding per the normative
D-Bus specification. Serial starts 1, increasing, bounded; replies must match serial and bound
unique sender. Interfaces/destinations/member names are compile-time strings. Unit object path
comes only from GetUnit for the bound unit, validated against expected systemd escaping.
No arbitrary variant decoding: use finite signatures ssau, sau, ssa(sv)a(sa(sv)), sba(sv), s,
ss, and scalar properties s/u/t/ay/b required by the launch/continuity contract.
Unknown body types, oversize frames, auth challenges or unexpected FDs invalidate.

**INCOMPLETE M4:** exact D-Bus variant whitelist/launch property marshalling, bootstrap filter
specialization and syscall-to-image conformance still need a concrete artifact and decoder
vectors. The finite method set above is not a completed byte-code implementation. Do not promote
this design to READY simply because a raw-syscall smoke artifact compiled. Decision C remains
appropriate until these mechanical gaps are closed; privileged policy reads alone cannot do it.

## 6. Source semantics and limits

[Linux seccomp](https://man7.org/linux/man-pages/man2/seccomp.2.html) supports syscall filters and
fork inheritance; it does not interpret filenames or application messages.
[D-Bus specification](https://dbus.freedesktop.org/doc/dbus-specification.html) defines the separate
manager wire/authentication protocol. [Dumpability](https://man7.org/linux/man-pages/man2/PR_SET_DUMPABLE.2const.html)
and [ptrace checks](https://man7.org/linux/man-pages/man2/ptrace.2.html) inform the bootstrap model.
These are mechanism references, not proof of installed policy or accepted CGC lab behavior.
PRODUCTION QUIESCENCE PRODUCER = NOT_STARTED. R6 = NOT_EXECUTED.

## 7. Mechanical specialization review

2026-09-24; starting checkpoint ce41ad2020ddfcaa7a2a3687ade86c6eb8358ea4.
Sections 1–6 retain the previous design and its explicit gaps. This section narrows it where
stated. Status: **M4_PARTIAL_REMAINING_DESIGN_GAP**. Generated final C/W filters and fixed request
body vectors are available in [vectors](V3_QUIESCENCE_LAB_VECTORS.md); a full native image and
complete B/peer/bootstrap argument specialization are absent. Do not fill those gaps at R6 launch.

### Stage and installation order

The pre-fork policy must include the union of all intended child setup operations, including
the finite peer ptrace test. The old B_BOOT set omitted that peer operation. Adding it only in
the peer would not recover authority denied by an inherited filter. This is a concrete design
conflict, not evidence that the kernel permits filter widening.

| Stage | Policy and exact transition | Fork / credentials / signals |
|---|---|---|
| B_BOOTSTRAP | Normalize inherited FDs; validate image/manifest; set subreaper and nondumpable; set no_new_privs; install common superset before first fork | Raw fork:57 only; B credential setup; no handlers or signal-sending syscall |
| B_CHILD_SETUP | Common filter remains; create only predeclared gated C/W/peer, immediately bind pidfd in parent | Child stays root in trusted fixed code; no protocol dispatch; failed pidfd acquisition aborts release |
| C_BOOTSTRAP | Close/remap to 0..4 before drop; empty groups, drop bounding/ambient capabilities while authorized, setresgid then setresuid, restore dumpable=0, zero effective/permitted/inheritable capabilities, verify no_new_privs, read/close gate 4; install C_READY | No further fork; bootstrap prctl/credential calls must be admitted by common filter |
| C_READY | Only exact generated C_READY table; validate 0..3; send authenticated READY on 3 | No fork, credentials, prctl, seccomp, socket creation or exec |
| W_BOOTSTRAP | Same fixed credential sequence; 0..3 only; gate 3 read while gated; no payload or fork yet | Gate release does not itself authorize workload until final filter installed |
| W_RELEASED | Close gate 3, verify 0..2, install exact generated W_RELEASED; then fixed workload | Raw fork:57, no clone/clone3/vfork/threads; descendant inherits filter/FDs; no exec |
| PEER_BOOTSTRAP | Same drop/FD checks; close gate; create its own unprivileged bus connection only if selected; install selector-specific final policy | No inherited root-authenticated socket; T4 needs specialized ptrace against bound C |
| PEER_TEST | Finite selector from section 5; no new selectors, arbitrary paths, PIDs or manager methods | Generated complete per-selector policies still a gate; do not substitute P_IO union |
| B_SEALED | Close 12..15,24..26,40..43; remove setup authority/capabilities; verify inventory; stack final B policy; only then SEAL ACK | No fork, credential transition, new control socket or filter installation; observation/empty teardown only |

All children must exist and be launch-bound before B_SEALED. W can await its gate while B closes
the write end after a fixed release token. EOF without that token means refusal. C READY is not
W release. B must verify child readiness and exact epoch before committing seal; partial gate
release or missing final child acknowledgment invalidates, never reports sealed acceptance.
Every filter is stacked, never replaced. For each generated child/final policy require a
mechanical subset check against the inherited common policy, including high argument halves.
No pre-filter confinement claim. The root-to-nonroot dumpability transition remains non-atomic
and requires M3 privileged acceptance; this ordering does not prove an injection-free interval.

FD remapping uses dup3 before final specialization; child closes every inherited B handle before
credential drop. CLOEXEC does not close handles on fork. Pre-fork B cannot close handles it still
needs, so trusted child setup is part of the TCB. Verify actual FD inventory before READY/release;
an extra FD refuses, not silently closes after the fact. All stable FD numbers remain section 3.

### Generated final C/W policy and cBPF format

The vector document contains the complete scalar rules, generated instruction bytes, SHA256
and deterministic generator for C_READY/W_RELEASED. Those rules supersede the broader C_IO/W_IO
sets for final stages. C reads only FD0, <=1024 bytes; writes 1/2 <=65536; channel sendmsg/recvmsg
only FD3 with flags 16384/1073741824. W reads FD0, writes 1/2, closes only 0..2, uses raw fork:57
and wait4:61 with PID=-1/options 0 or WNOHANG. W has no poll or gate-read after release.
Both permit exit/exit_group status 0..255 and clock_gettime CLOCK_MONOTONIC only.
poll in C constrains count<=4 and timeout<=1000; cBPF cannot inspect pointed-to pollfd contents.
The native code must validate those records against its inventory; this is not an FD argument
check by the kernel. Likewise sendmsg iov/ancillary bytes remain application checks.

Each instruction is little-endian HBBI. Architecture gate loads offset4, accepts only
0xc000003e; otherwise KILL_PROCESS=0x80000000. Number gate loads offset0, rejects bits
0xc0000000 (negative numbers and x32 marker) with KILL_PROCESS. Default ERRNO|EPERM=0x50001;
success ALLOW=0x7fff0000. No TRAP, TRACE, USER_NOTIF or signal handler.
Sort clauses by number/predicates. Emit LD nr, JEQ nr skipping a JA-to-next-clause on equality;
for each scalar load high/low words at 20+8*i / 16+8*i, compare, and JA-to-next on failure.
EQ compares both halves; LE is unsigned <=32-bit and requires high=0. Return ALLOW only after
all clause predicates, otherwise continue; final return EPERM. Reject >4096 instructions.
The published generator is authoritative for jump offsets; no undocumented library output.

| Vector | Input/action | Expected kernel result / lab state | Falsifies if |
|---|---|---|---|
| V-F01 | C_READY write(1,buffer,8) | ALLOW; actual write result depends on owned pipe | Filter denies |
| V-F02 | C_READY getppid:110 | EPERM; unexpected code path invalidates | Filter allows |
| V-F03 | C_READY write(4,buffer,8) | EPERM; invalid request | Allows |
| V-F04 | C_READY recvmsg(4,msg,MSG_CMSG_CLOEXEC) | EPERM | Allows |
| V-F05 | Arch 0x40000003, or x32 number 0x40000001 | KILL_PROCESS; proof invalidated | Executes syscall |
| V-F06 | clone3:435 in either final stage | EPERM | Allows |
| V-F07 | execve:59 or execveat:322 | EPERM | Allows |
| V-F08 | unshare:272 / setns:308 | EPERM | Allows |
| V-F09 | socket:41 | EPERM | Allows |
| V-F10 | ptrace:101 | EPERM in C/W | Allows |
| V-F11 | W raw fork, child repeats V-F06..10 | Inherited EPERM; lifecycle accounting separately required | Child broadens authority |
| V-F12 | W_GATED unexpectedly has FD4 | Native inventory REFUSE BEFORE RELEASE; no workload | Releases |

OBSERVED_FACT: 20 offline instruction-interpreter checks passed, including full-width FD
rejection. No seccomp filter from these tables was installed. V-F11/F12 native cases NOT_EXECUTED.
Compiler/site conformance remains NOT_EXECUTED: there is no complete image to inspect. Future
map must record source function, disassembled instruction address, syscall number, role, stage
and reason. Only the reviewed syscall veneer may contain syscall instructions; computed numbers
must come from closed compile-time call sites. ELF/header/undefined-symbol/relocation checks and
an optional owned-process trace cannot replace complete static path review. The earlier smoke
artifact is not the image and is not rebuilt to pretend otherwise.

### D-Bus finite wire contract

New installed read-only observation: system service XML introspection returned Type:s,
ExitType:s, Restart:s, RuntimeMaxUSec:t, WatchdogUSec:t, Delegate:b, TasksMax:t,
Environment:as, SupplementaryGroups:as, UMask:u, LimitCORE/Soft:t, LimitNOFILE/Soft:t,
User/Group:s, KillMode:s and SendSIGKILL/SendSIGHUP:b. It exposes ExecStart readback as
a(sasbttttuii), **not** its setter. The [v259 setter source](https://raw.githubusercontent.com/systemd/systemd/v259/src/core/dbus-execute.c)
accepts the transient a(sasb) form. This establishes encoding semantics, not caller authorization.
Only XML signatures were read, not service environment values or command lines.

Auth states: SOCKET_CREATED -> CONNECTED -> NUL_SENT -> AUTH_EXTERNAL_SENT -> AUTH_OK_RECEIVED
-> BEGIN_SENT -> HELLO_SENT -> HELLO_REPLY_BOUND -> SYSTEMD_OWNER_BOUND -> READY.
Exactly one AF_UNIX stream connection to /run/dbus/system_bus_socket. Emit byte00 then ASCII
"AUTH EXTERNAL " + lowercase hex(ASCII decimal own UID without leading zero) + CRLF.
Accept only "OK " + 32 ASCII hex GUID + CRLF, <=64 bytes, one line; retain GUID as connection
metadata, not identity proof. Emit "BEGIN\r\n". No cookie/challenge/FD negotiation/fallback.
Any unexpected line, EOF, oversize response, failed Hello or reconnect invalidates.
Read/write fragmentation is permitted; finite buffers, no unbounded retries; phase timeout applies.

Wire: little endian only; version1; increasing nonzero u32 serial without wrap; frame<=65536,
header fields<=4096, strings<=4096, arrays<=65536 bytes and <=32 elements, nesting<=6 containers.
The deepest accepted branch is properties array -> property struct -> variant -> ExecStart array
-> command struct -> argv array. No other six-level shape is accepted.
All lengths checked before addition/alignment, before allocation and before reading a field.
Client method calls flags=2 (NO_AUTO_START), never interactive authorization. Header starts
endian/type/flags/version (one byte each), body length u32, serial u32, fields length u32.
Fields are 8-aligned (byte code, variant); body begins at next 8-aligned position. All padding
must be zero. Strings s/o: align4, u32 byte length, ASCII payload and NUL; g: align1, u8 length,
signature bytes and NUL. y aligns1, u/b align4, t aligns8; b is exactly 0 or1. Array aligns4,
u32 byte count excludes padding before first element, then element alignment. Struct aligns8.
Variant is a signature of exactly one whitelisted type then that type's aligned value.

Outbound headers: PATH1:o, INTERFACE2:s, MEMBER3:s, DESTINATION6:s, optional SIGNATURE8:g,
in numeric order; no SENDER. Incoming: allow only those plus ERROR_NAME4:s, REPLY_SERIAL5:u,
SENDER7:s. Duplicate or unknown code, UNIX_FDS9 even zero, ancillary rights, malformed object
path or signature invalidates. Header order on incoming bus messages is not required to match
outbound order. Required fields depend on type: replies require reply serial/sender; errors
also error name; signals path/interface/member/sender. Missing body means absent or empty
signature; nonempty body needs exact expected signature. Reject nonzero unknown flags.

Only fixed codecs: s, ss, u, t, b, ay, au, sau, ssau, sba(sv), ssa(sv)a(sa(sv)), plus
as and a(sasb) for the property table. Reply codecs: s/o/empty, fixed property v(s/t/u/b/ay),
NameOwnerChanged:sss and Reloading:b; no arbitrary recursive variant parser. InvocationID ay
must contain exactly16 bytes. Unique-name strings accept colon followed by decimal components
separated by dots, bounded255; object paths must have slash-separated ASCII alnum/underscore
components, no empty component except root. Unit path must equal locally escaped bound unit.

Launch properties: the complete name/type/value list is V-D05 logical input, sorted by name,
no duplicate/extra property. ExecStart exactly one (image,[image,"--manifest",manifest],false),
mode fail, empty auxiliary units. The administrator's separate launcher emits it; B cannot.
Environment property contains LANG=C and LC_ALL=C; manager-injected environment may still exist.
The static entry ignores/clears all environment before processing and uses no dynamic loader.
This is not a claim that Environment replaces every manager variable.

T7 emits only V-D06 and V-D08; PIDs derive from bound peer, never caller input. T8 emits V-D11
and V-D07. V-D11 is an unauthorized creation probe, not an alternative authorized broker launch.
Any successful creation falsifies the authorization claim even if its image refuses startup.
All other methods/paths/properties refused by closed enum dispatcher; no function accepts
destination/member/signature/argv strings from a request. The offline model used a type writer
to produce fixtures; it is not a runtime generic client and is not shipped as executable code.

Bind Hello result and GetNameOwner(systemd1) to connection generation. Subscribe to owner changes
before acquiring final owner snapshot; process queued owner-change events before accepting it.
Only a reply from the bound owner with pending serial/signature is accepted. Outstanding calls
are serialized, one at a time. Bus daemon replies require its well-known sender. NameOwnerChanged,
disconnect, Reloading or suspected reexec invalidates; never automatically rebind. Same owner
does not prove no same-PID reexec: M5 remains unresolved. Method errors may prove denial only
for exact AccessDenied or InteractiveAuthorizationRequired on the corresponding peer attempt;
other errors invalidate that test and never prove policy denial. Do not publish error body text.

### Negative decoder vector contract

These are deterministic mutations of the published bytes, not executed native decoder tests.
Offsets are zero-based. Field replacement means reconstruct that one field using the encoding
above and update header/body lengths; every other logical field is unchanged. Stateful cases
start with one pending call, bound owner :1.42 and current generation1. Security failures all
produce decoder REJECT and lab INVALIDATED, with no dispatch. No normalization into a valid call.

| ID | Exact mutation/input | First required rejection |
|---|---|---|
| V-D20 | D01 byte0=0x42 | Endian |
| V-D21 | D01 byte3=2 | Version |
| V-D22 | D01 append a second header PATH equal to first, adjust fields length/padding | Duplicate field |
| V-D23 | D06 SIGNATURE becomes "sau", unchanged body | Signature |
| V-D24 | D06 MEMBER becomes "Reload" | Closed member enum |
| V-D25 | D06 INTERFACE becomes "org.freedesktop.systemd1.Unknown" | Interface |
| V-D26 | D06 final au length word becomes 65537 | Array bound |
| V-D27 | D01 byte46=1 (padding between first and second header fields) | Nonzero padding |
| V-D28 | D03 PATH becomes "/org//freedesktop/systemd1" | Path grammar |
| V-D29 | D01 adds UNIX_FDS:u=0 | Forbidden header |
| V-D30 | Method return: reply_serial2, pending1, sender:1.42, empty body | Correlation |
| V-D31 | Same as D30 with reply_serial1, sender:1.43 | Sender |
| V-D32 | Valid NameOwnerChanged(systemd1,:1.42,:1.43) while bound :1.42 | Generation invalidation |
| V-D33 | D07 Description variant changes from s to t=0 | Property-type whitelist |
| V-D34 | Remove final byte of D06, retain lengths | Truncation |
| V-D35 | Error reply serial1, sender:1.42, error "org.freedesktop.DBus.Error.Failed", body s="" | Not proof of denial; invalidate |

The raw full-frame negative corpus and finite incoming signal/error decoder are still required.
Positive body round trips do not test these mutations. D01's first path occupies bytes24..44,
its terminator is byte45, and bytes46..47 are padding before the next header field.

### Artifact conformance and exit decision

| Artifact | Spec complete? | Deterministic / negative vectors | Implemented / compiled / executed | Privilege required? | Blocks R6? |
|---|---|---|---|---|---|
| Bootstrap filter | No: common union and runtime scalar specialization | Stage contract; full bytes absent | No / no / no | Native unprivileged validation possible | Yes |
| C filter | Final scalar table yes | Exact generated bytes / model checks | Offline generator only / no / model only | No for filter analogue | Yes: image/FD conformance |
| W filter | Final scalar table yes | Exact generated bytes / model checks | Offline generator only / no / model only | No for filter analogue | Yes: image/inheritance |
| Peer filter | No: per-selector BPF not generated | Actions fixed; no complete bytes | No / no / no | R6 later | Yes |
| B_SEALED filter | No: observation FD allocation specialization | State restrictions only | No / no / no | Root acceptance later | Yes |
| CGC_LAB_PROTO_V1 | Byte grammar specified | 6 positive / 13 negative model cases | Model only / no / offline | No for parser | Yes: native decoder |
| D-Bus auth | State machine specified | Exact auth grammar / rejection conditions | No / no / no | No for codec | Yes |
| D-Bus launch | Fixed property/body encoding specified | D05 exact / partial negative corpus | Body model / no / offline | Sending requires separate privilege approval | Yes |
| D-Bus peer | Fixed outbound messages specified | D06..11 exact / partial negatives | Body model / no / offline | Actual attacks require R6 | Yes |
| FD validator | Inventory specified | V-F12 expectation / not executed | No / no / no | No for owned analogue | Yes |
| Native image | Source architecture only | No complete source/disassembly mapping | No / no / no | Root path later | Yes |

**M4_PARTIAL_REMAINING_DESIGN_GAP.** Do not promote to specification-complete or request R6.
Remaining mechanical work is specifically complete bootstrap/B/peer scalar cBPF generation,
incoming D-Bus signal/error decoder and byte-exact negative frame corpus, then syscall-site/FD
conformance against a reviewable disposable image. RO review is independently useful but cannot
close these gaps. No generic D-Bus runtime capability exists; no native codec exists either.
