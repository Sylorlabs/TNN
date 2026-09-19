# R33-N01 independent native-only engineering review

Review date: 2026-09-05 (America/Los_Angeles).

Scope: bounded read-only semantic/API/arithmetic/syscall/side-effect/assertion review of the native-only N01 engineering host-adapter candidate. No Python was executed or edited. No native case, generator, fixture, learner, training, scientific evaluator, registry mutation, parent mutation, or accepted-state mutation was performed by this review. This is not a repeat or validation of any failed historical review.

## Source identity reviewed

- `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` — SHA-256 `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e`
- `Research/R33_NATIVE_IO_V1.zag` — SHA-256 `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e`
- `Research/R33_NATIVE_PROCESS_V1.zag` — SHA-256 `547c86f7d6f7dd17b748286625c13e361f1f730a6fd32b1315ad7031f872cb80`
- `Research/R33_NATIVE_N01_DRIVER.zag` — SHA-256 `a403b5d22ac6e70469232b94144a7d6c1ca48167b368783a8ce93e85d2301cab`
- `Research/R33_NATIVE_N01_PREREGISTRATION.md` — SHA-256 `5340fa1ce641834930e546062c33166a0c26f73f31802a633d2c241c4522671c`

Installed macOS SDK references inspected read-only:

- `sys/syscall.h` — SHA-256 `8b759020ebc7f377b0cc96a09fff8f7fe7991e625f971d0fab54dfb54b08f324`
- `sys/stat.h` — SHA-256 `31c8f252b05785343ca577c007657c0fbab45a182b60fc5b73994c621dc318d4`
- `sys/resource.h` — SHA-256 `7d16930e6b75f11ba203238faa5580d31d48fcd4230f2b3f604aaa5fd7e86b58`
- `sys/fcntl.h` — SHA-256 `805fd8c695f8e5e1c327b6852382cc5533738bbfd8f18bc11f850531166e4fe8`
- `sys/errno.h` — SHA-256 `109ace10e79b9467dee3b8c7890f1d5bea1102d982c521922e9d372ab9863c97`
- `sys/signal.h` — SHA-256 `319fbc4555c1d39c95d8a5e3034956bfe8e0e1bd9142df95ab71ad3ac8bb1f54`

The SDK confirms the reviewed Darwin constants used for `open`, `close`, `wait4`, `execve`, `setitimer`, `dup2`, `fsync`, `flock`, `mkdir`, `setrlimit`, `lseek`, `openat`, `linkat`, signals and expected errno values. `nio_regular` uses syscall 339, which is `SYS_fstat64`; its read of mode bytes 4-5 is consistent with the SDK `stat64` layout. That path is therefore not a review finding.

## Strongest criticism

The preregistration overstates the supervisor's timeout guarantee. `supervise` installs a 30-second `ITIMER_REAL` on the parent, then `nr_run` performs a blocking `wait4`. If a child stalls before it installs its own `nio_guard`/timer (for example during the fork-to-exec-to-main interval or another early native failure), expiration of the parent's default `SIGALRM` terminates the **parent**, not the child. There is no parent-side timeout state machine, `WNOHANG` polling, kill of the child/process group, or guaranteed final reap.

Darwin `wait4` documentation explicitly notes that if a parent terminates without waiting for children, remaining children are reparented. Therefore the current source does not justify the claim that the native Zag parent itself enforces a bounded child wall deadline. At most, reviewed source establishes: the parent has its own 30-second lifetime bound, and each successfully entered child mode attempts to install its own shorter timer.

This matters because N01 is intended to qualify supervision primitives. A supervisor that can die while leaving an unbounded child is not yet a complete supervision boundary.

## Concrete bugs / semantic defects

### N01-R1 — missing native primary admission/create primitive

`supervise` immediately calls:

`nio_open_root("Research/R33_NATIVE_N01_RUN_PRIMARY_V1")`

`nio_open_root` only opens an existing directory. It neither atomically creates a new primary root nor refuses-and-creates it. Yet the preregistration says an existing primary directory is refused at admission and the parent shell only invokes the binary/preserves metadata.

As reviewed, a successful run therefore has an unresolved integration precondition: some external actor must create the primary directory before the native supervisor can open it, or the source must gain an explicit native admission/create step. The current code alone cannot both reject an existing primary and start from a nonexistent primary.

Precise consequence: do not claim the reviewed N01 source implements native one-shot primary admission.

### N01-R2 — preregistered write scope contradicts actual supervisor writes

The preregistration states that the only write target is `Research/R33_NATIVE_N01_RUN_PRIMARY_V1/fs`. However `nr_run` creates, with `O_CREAT|O_EXCL`, at least:

- `check.stdout`
- `check.stderr`
- `deadline.stdout`
- `deadline.stderr`
- `cpu.stdout`
- `cpu.stderr`

directly under `Research/R33_NATIVE_N01_RUN_PRIMARY_V1`.

Those are real filesystem writes outside the stated `/fs` write target. This is a documentation/source contract mismatch even if the writes are intended and safe. The write envelope must include the supervisor artifacts/root itself, or the implementation must relocate them under the declared subtree.

### N01-R3 — parent deadline is not child termination enforcement

`nio_guard(30)` sets a process-local real timer on the supervisor. `nr_run` then blocks in `wait4` and has no timeout/kill/reap branch. If the parent alarm fires, the parent can terminate while a child remains alive. The child normally installs its own guard only after `execve` reaches `main`; that is not equivalent to parent-enforced supervision.

Required architecture change for an actual supervisor claim: parent-owned elapsed-time enforcement that can identify the child PID, terminate it when the deadline expires, and reap it before returning/terminating. A process-group policy may be required if future cases can create descendants.

### N01-R4 — `nr_run` has side effects before its fallible allocation preflight completes

`nr_run` creates the child stdout/stderr files **before** allocating/validating the C strings, argv, env, status and rusage buffers. If any of those later allocations fail, the function returns immediately without closing both descriptors, freeing any successful intermediate allocations, or removing the newly created files.

This is a concrete fail-before-side-effect violation for the supervisor API. In a one-primary-attempt protocol it is especially consequential because `O_EXCL` artifacts can be consumed even though no child was started.

The narrow N01 driver may be unlikely to hit allocator failure, but a qualification of the API should not infer transactional admission from the current ordering.

### N01-R5 — `nio_guard` can partially and irreversibly mutate process limits before reporting failure

`nio_guard` lowers hard and soft resource limits sequentially:

1. CPU
2. file size
3. core
4. open files
5. wall timer

If a later `setrlimit` or `setitimer` fails, it returns `-7401` after earlier hard limits may already have been lowered. Hard-limit lowering is not generally reversible by the same unprivileged process.

For the current driver this likely causes immediate exit, which limits damage, but the API does not provide atomic "guard installed or state unchanged" semantics. Claims should say fail-explicit installation, not transactional guard installation.

### N01-R6 — generic side-effect API is not capability-confined to the preregistered path

`nio_mkdir(path)` and `nio_open_root(path)` accept arbitrary caller-provided paths (subject to string/NUL/length rules). `nio_write_all(fd, ...)` accepts any nonnegative descriptor. The **driver** uses fixed in-scope paths and descriptors, but the adapter source itself does not encode the N01 write root as a capability.

Therefore a passing N01 fixture could establish correct behavior for the fixed driver path, not that the exported native adapter is intrinsically restricted to that path. That distinction is important before these primitives become protected substrate facilities.

### N01-R7 — regular-file enforcement is caller-dependent, not guaranteed by `nio_open_child`

The source comment says the regular-file check is mandatory, but `nio_open_child` returns a descriptor without performing `nio_regular`. The driver explicitly checks the newly created `staged.bin`, and `nio_read_exact` rechecks regularity before reads, but the API permits callers to use an unverified descriptor with other operations such as `nio_lock` or `nio_write_all`.

This is acceptable for a tightly frozen trusted fixture, but it is not an API-level invariant. A stronger adapter should return a regular-file capability only after `openat` + `fstat64` succeeds, closing the fd on type-check failure.

### N01-R8 — label validation and generated filename validation have inconsistent bounds

`nr_run` accepts any `label` up to 64 characters via `nio_name_valid(label)`, then appends `.stdout` / `.stderr`. `nio_open_child` re-applies `nio_name_valid` to those generated names, also capped at 64 characters.

Therefore labels longer than 57 characters are accepted by the first validation but necessarily fail when opening `<label>.stdout`; labels longer than 57/58 depending on suffix length cannot start. This is a real API boundary inconsistency, though the frozen N01 labels (`check`, `deadline`, `cpu`) are unaffected.

### N01-R9 — wait failure/interruption has no recovery or child cleanup path

`nr_run` calls `wait4` exactly once. If it returns anything other than the child PID, the result remains started with exit `-1`; no retry for `EINTR`, no `kill`, and no second reap occurs. Darwin documents `EINTR` as a possible wait failure when interrupted by a caught non-restarting signal.

The current source installs no caught signal handler, so the common N01 path may not encounter this. Still, this is another reason to constrain the claim to the observed frozen fixture rather than a robust general supervisor.

## Assertion / test-design mistakes and missing falsifiers

### 1. No assertion proves native primary admission semantics

There is no native check for:

- primary root absent -> atomically created and admitted;
- primary root already present -> refused before any new primary artifact is written;
- symlinked primary path -> refused;
- partial previous primary artifacts -> preserved/refused without reuse.

These are prerequisites for the one-primary protocol described in the preregistration.

### 2. No falsifier for supervisor-owned child timeout/cleanup

The `deadline` case proves a **child-installed** one-second `ITIMER_REAL` can terminate that child with `SIGALRM` if execution reaches the case body. It does not prove that the parent can bound a child that never installs its timer.

A future engineering falsifier should include a child mode that deliberately does not install a child deadline and verify that the parent terminates and reaps it under a parent-owned deadline mechanism. Do not implement that as a scientific experiment; it is a host-supervision engineering control.

### 3. No falsifier for allocation failure after stdout/stderr creation

The side-effect ordering in `nr_run` is untested. A future component-level test should force or inject a post-file-creation allocation failure and verify either zero pre-start file creation or explicit preserved partial-admission status with all descriptors closed. The current source would not satisfy a no-side-effect expectation.

### 4. No boundary test for generated label filenames

Test at least label lengths 57, 58 and 64 so the API's documented/actual maximum is explicit.

### 5. No test separates fixed-driver confinement from adapter confinement

The existing `parent_path_refused` assertion tests `nio_open_child(root,"../outside",1)`. That is useful child-name traversal rejection, but it does **not** prove `nio_mkdir` or `nio_open_root` cannot target an arbitrary outside absolute/relative path. The driver is fixed-scope; the adapter is not capability-scoped.

Do not reinterpret one traversal assertion as an adapter-wide filesystem sandbox.

### 6. No file-type negative control at open/write boundary

The fixture positively checks that its created file is regular, but it does not test rejection of a FIFO/device/socket at the API boundary. `O_NONBLOCK` prevents one class of FIFO hang, while `nio_read_exact` rejects nonregular reads, but `nio_open_child` itself does not guarantee type. A future bounded engineering test should make the intended layer of enforcement explicit.

### 7. No explicit supervisor artifact capacity/readback assertion

The child stdout/stderr files are created and used for supervision but the parent does not reopen, bound-read, or assert their size/content. For N01's current negative children this may be intentional, and the parent process record is the main result. Still, claims about preserved child output should be deferred to a later native collector/journal test.

### 8. RSS assertion is measurement-only

The preregistration correctly states peak RSS is measured, not hard-contained. The source checks `0 < ru_maxrss <= 256 MiB` after child exit, but there is no hard RSS limit. This is an acceptance filter on observed usage, not memory containment. Preserve that wording exactly.

## Arithmetic / ABI observations that are acceptable by inspection

- `width`/payload-style integer arithmetic is not present in this N01 adapter, so there is no analogous unchecked image-shape multiplication here.
- `nio_read_exact` bounds `max_bytes` to 33,554,431 before casting `size+1` to i32 allocation length; the reviewed size arithmetic is bounded for admitted inputs.
- `nio_write_all` caps one write payload at 1 MiB and bounds syscall count to 4096.
- `fstat64` syscall 339 and `stat64.st_mode` byte offset 4 are consistent with the installed SDK.
- `LOCK_EX|LOCK_NB` is 6; `EWOULDBLOCK/EAGAIN` is 35; `SIGALRM`, `SIGXCPU`, and `SIGKILL` are 14, 24, and 9 in the inspected SDK.
- `rusage` begins with two `timeval` values followed by `ru_maxrss` on the inspected 64-bit Darwin layout, consistent with `usage[0..4]` interpretation used by `nr_run`.

These are source/SDK observations only; compilation or future execution remains the evidence for the pinned binary/OS combination.

## Precise claim boundary

If the exact reviewed sources are later frozen, compiled, and the sole preregistered N01 primary executes with all 27 `CHECK` assertions matching, `FAILURES,0`, the three child outcomes matching, measured RSS within the stated ceiling, empty required stderr, and all frozen identities verified, the defensible claim is limited to:

> Under the exact pinned macOS/arm64 Zag/compiler/SDK/source/run configuration, the fixed N01 non-learning engineering fixture observed the specified Darwin file-I/O, exclusive creation, no-follow child-name handling, regular-file test, exact bounded read/write, fsync, hardlink no-replace publication, advisory lock contention, process fork/exec/wait outcome collection, child-installed wall/CPU termination controls, and post-run RSS measurement for the exercised cases.

Even after such a pass, do **not** claim:

- a general native supervisor with parent-enforced child termination/reaping;
- native one-shot primary admission unless that missing boundary is implemented and tested;
- that filesystem writes are intrinsically confined by the adapter to `/fs`;
- hostile-process, same-user race, symlink-race beyond the exact exercised no-follow paths, network, sandbox, or capability-security isolation;
- power-loss durability, crash-consistent journal recovery, cryptographic integrity, authenticated authority, rollback, or complete telemetry;
- hard RSS containment;
- sensory S0/S1/S2, raw natural ingress, learner perception, learning, training, competency, cognition, scientific qualification, parent migration, promotion, milestone/grant change, or R33 completion;
- that old Python-dependent evidence qualified these native replacements;
- that any failed historical review became successful.

The current preregistration should also avoid saying the parent "enforces" the child wall deadline until a parent-owned kill/reap mechanism exists. The source presently supports only a parent self-deadline plus child self-installed deadline cases.

## Verdict

**REVIEW VERDICT: NOT READY FOR A BROAD NATIVE-SUPERVISION CLAIM.** The fixed N01 I/O assertions are coherent enough to remain useful engineering qualification candidates, and most inspected Darwin constants/layout assumptions are source-consistent. Before freezing a claim that includes native supervision/admission, the main agent should disposition R1-R4 at minimum: native primary admission, truthful write-scope declaration, parent-owned child timeout/kill/reap, and pre-side-effect supervisor allocation validation/cleanup.

No native case was executed to reach this verdict.
