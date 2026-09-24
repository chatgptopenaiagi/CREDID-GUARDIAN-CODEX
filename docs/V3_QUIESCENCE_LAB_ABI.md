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
