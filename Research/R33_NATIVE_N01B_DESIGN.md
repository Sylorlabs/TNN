# R33-N01B native process-supervisor V3 design

Status: new compile-only corrective engineering identity. No N01B native case has run.
No learner, scientific data, training, accepted-parent mutation, grant, registry, handoff,
Python execution/edit, compiler recovery, or compiler rebuild is part of this package.

## Why V3 exists

Frozen N01A BUILD02 retained a sole-primary failure: its launch output records 21 failed
checks out of the 66 N01A controls. All four started children were killed/reaped with
`NRV2_CLOCK=-7510`; named i32 status/artifact constants passed as expected i64 arguments
also rendered address-like values instead of their intended numeric constants. That
failed identity is preserved and is not rerun or reinterpreted as success.

V3 does not attempt to repair the pinned compiler or depend on
`_zag_clock_monotonic_ms`. The final V3 source contains zero references to that symbol.

## Compiler-interface diagnosis behind N01B

The two N01A failure modes are distinct and are not treated as one inferred defect.

### Pinned monotonic-clock lowering defect

The pinned compiler provenance binds `znc_macos_arm64_7cacbfc0` to Zag source commit
`7cacbfc04f6cffec02ea9b1d5ff6702fe2e93f3c` from
`origin/codex/macos-arm64-v2:bootstrap/znc`. Inspection of that commit's ARM64 backend
`selfhost/native/arch/aarch64/acodegen.zag` shows the macOS lowering for
`_zag_clock_monotonic_ms()` selecting raw Darwin syscall **169**, while the adjacent
backend comments describe the call as `gettimeofday(struct timeval *, void *)`.

The installed SDK interface used by this package identifies Darwin `gettimeofday` as
syscall **116**. This is source evidence for why the frozen N01A/V2 children immediately
entered the `NRV2_CLOCK=-7510` path. N01B avoids the helper entirely: deadline enforcement
is the relative kernel EVFILT_TIMER, while optional non-monotonic measurement invokes
Darwin syscall 116 directly.

This diagnosis does not qualify or repair the pinned compiler, and the later working-copy
backend is not substituted for the pinned seed.

### Imported top-level const lowering defect

N01A's failed checks show imported named status/artifact constants arriving at the i64
`expected` assertion parameter as address-like `610473...` values, while equivalent
literal expectations arrive numerically. Source inspection explains that pattern more
specifically than a generic i32-width bug: top-level Zag `const` declarations are
represented as annotated nullary functions, and imported references require backend
recognition because they bypass the parser's ordinary implicit-call conversion.

The current ARM64 backend contains explicit `ac_is_desugared_const` handling for this
case and documents that imported refs need that special recognition. The pinned
`7cacbfc0` ARM64 backend lacks that handling. Thus a pinned imported const reference can
be materialized as a function/fat-function value rather than evaluated to its scalar
constant; casting that imported identifier to i64 is therefore not a safe correction.

This is a source-backed diagnosis consistent with the retained N01A output, **not** an
isolated runtime reproduction. No compiler probe or N01B fixture was executed here.

## Darwin kernel deadline ABI inspected

The installed macOS SDK `sys/event.h` used for this design states:

- `struct kevent` is packed to 4-byte alignment and occupies 32 bytes on arm64;
- `EVFILT_TIMER = -7`;
- `EV_ADD = 0x0001` and `EV_ONESHOT = 0x0010`;
- the default EVFILT_TIMER `data` unit is milliseconds;
- relative timers are the default; `NOTE_ABSOLUTE` is not used;
- `kevent` accepts a relative `timespec` wait timeout.

`sys/syscall.h` confirms `SYS_kqueue=362` and `SYS_kevent=363`.

V3 encodes the 32-byte kevent record explicitly in native little-endian arm64 layout:
ident at byte 0, filter at 8, flags at 10, fflags at 12, data at 16, udata at 24. The
timer is ident 1, filter -7, flags `EV_ADD|EV_ONESHOT`, fflags 0, and positive relative
deadline milliseconds in data.

SDK identities observed for the design:

- `sys/event.h`: `b09a4fdd9e88a5c1c9a29bded36a6f8b96b39a3054f0075a07c19da587f0e062`
- `sys/syscall.h`: `8b759020ebc7f377b0cc96a09fff8f7fe7991e625f971d0fab54dfb54b08f324`

These header inspections are source references, not execution evidence.

## V3 supervision contract

`nrv3_run` supervises exactly one direct child PID.

1. Validate root, binary/mode bounds, deadline, output limit, and label length <=57.
2. Allocate every C string/name/argv/env/wait/rusage/timer/poll/measurement buffer before
   filesystem output creation.
3. Create the kqueue before filesystem output admission; kqueue failure leaves no child
   output artifact.
4. Exclusively create regular empty `.stdout` and `.stderr` files. Partial admission is
   retained and reported; evidence files are never deleted by V3.
5. Register a relative one-shot EVFILT_TIMER with `kevent` **before fork**.
6. Fork. The child lowers `RLIMIT_FSIZE` to the requested output ceiling, redirects only
   stdout/stderr, closes the inherited kqueue descriptor, and execves one binary with one
   mode argument and an empty environment.
7. Parent repeatedly checks `wait4(pid,...,WNOHANG,...)`. A short relative `kevent`
   timespec wait is only the polling sleep; timeout enforcement is the registered
   EVFILT_TIMER event, not accumulated poll time and not any clock helper.
8. When the timer event arrives, V3 makes one final `wait4(WNOHANG)` check to close the
   exit-vs-timer delivery race. If the child is already reapable, its actual exit wins.
   Otherwise V3 classifies timeout, sends SIGKILL to the direct child, and requires a final
   blocking reap.
9. Any wait/kqueue supervision error also triggers direct-child kill plus final reap; an
   unreaped child changes the result to an explicit reap failure.
10. Output size is inspected after reap. SIGXFSZ 25 or observed output beyond the
    requested ceiling is classified separately as output-limit failure.

The timer protects only the direct child. V3 does not create/manage a child process group
and does not claim descendant containment. A child that independently creates descendants
is outside this supervisor guarantee.

## Time and resource accounting

Enforcement does not use wall-clock time.

The only optional elapsed-time measurement is Darwin `gettimeofday` syscall 116 before
fork and after reap. It is stored as `wall_us_nonmonotonic` with a separate validity bit.
It is explicitly a non-monotonic observational measurement and cannot establish or alter
the deadline result.

CPU microseconds and peak RSS come independently from the reaped child's Darwin `rusage`
returned by `wait4`. PROCESSV3 output reports status, start/timeout/timer/reap state,
exit/signal, output bytes, non-monotonic wall measurement + validity, CPU microseconds,
and peak RSS as distinct fields.

The N01B supervisor installs frozen IO_V1 `nio_guard(20)` fail-fatally before admission:
CPU 20 s, file size 1 MiB, core 0, descriptor limit 64, and outer wall guard 20 s. The
outer guard is a fixture fail-safe, not the V3 child-deadline mechanism. Children inherit
the 1 MiB hard file-size ceiling and may only lower it per case (for example flood=1024).

Peak RSS remains measured, not hard-contained.

## Expected-value/compiler-interface correction

N01B's assertion function takes `actual:i64` and `expected:i64`. Every expected numeric
argument is now an explicit typed literal/local scalar expression. In particular, the
driver uses **no imported `NRV3_*` top-level numeric constant as an assertion expected
value**. Status/artifact expectations are literal `i64` values such as `-7608 as i64`
and `2 as i64`, so the pinned imported-const path is not involved before conversion.
No implicit i32-to-i64 expected argument is relied on.

Three additional controls explicitly widen named/local i32 values to i64 and compare them
to typed i64 literals (`-7608`, `25`, `2`). These exercise ordinary local scalar widening;
they do not claim to repair or experimentally certify the pinned imported-const lowering.

## N01B corrective control schedule

The driver retains the prior N01A control categories:

- native exclusive one-shot run-root admission and existing-root refusal;
- fixed whole-run-directory write scope;
- regular-file/nonregular/traversal boundary;
- label 57 accepted, 58/64 rejected before artifacts/start;
- retained partial output admission when second output creation fails;
- normal child exit;
- deliberately unguarded infinite child timeout/kill/reap;
- 1024-byte flood/output-limit classification;
- missing executable -> child exit 127;
- root close and nonzero overall failure exit.

The source contains 79 assertion call sites excluding the assertion helper itself: the 66
analogous N01A assertions plus 13 new timer/resource/explicit-width controls. New checks
include named-i32 widening, timer registered/not-fired for non-timeout cases, timer
registered/fired for the unguarded timeout, and separate CPU/RSS/non-monotonic time
measurement presence.

No N01B expected result is an executed result. Main-agent preregistration must bind the
exact assertion schedule and identities before any primary execution.

## Write scope and admission

The only intended N01B fixture write tree is:

`Research/R33_NATIVE_N01B_RUN_PRIMARY_V1/`

That whole directory, not only `/fs`, is the documented write envelope because child
stdout/stderr and retained partial-admission evidence live directly beneath the run root.
The run root is absent at compile close and must be created only by `nrv3_admit_root`
during the future registered primary. Existing root returns the underlying EEXIST refusal
and is not reopened/retried as a new primary.

## Compile-only BUILD01

Compiler command:

`Research/toolchain/znc_macos_arm64_7cacbfc0 Research/R33_NATIVE_N01B_DRIVER.zag --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o Research/R33_NATIVE_N01B_BUILD_01/n01b`

Final BUILD01 compile exit was 0. Compiler stdout reported a signed native binary with
103,876 bytes text, 1,991 bytes data, and zero external build tools. Compile stderr was
empty. The binary was **not executed**.

Final compile identities:

- `R33_NATIVE_PROCESS_V3.zag`:
  `04c5bc6c3c7222786ab5c6d9af384935c9dd533a6a89046860da0c67ffcb2f89`
- `R33_NATIVE_N01B_DRIVER.zag`:
  `d186fa8b235fe15449c113d88686483eb7bd84066d606ef72fb41e6be7b325c9`
- BUILD01 `n01b`:
  `41cb3b4b34b5d659731d0d4b961f6149c0563fbd187fd0282b32d6658cfb0f21`
- BUILD01 `compile.stdout`:
  `c757c5e29167b096a9d6b02a19af2b98ddfa7692c8668174bd9320d5e968d851`
- BUILD01 empty `compile.stderr`:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- pinned compiler:
  `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`
- frozen IO_V1:
  `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e`

Frozen failed-N01A references observed and left untouched:

- `R33_NATIVE_PROCESS_V2.zag`:
  `1006fe5dad48c3399d159ab4920d3a02ca12ed0d62470e363a3ab52f78705e56`
- `R33_NATIVE_N01A_DRIVER.zag`:
  `830901590fd2cb4af38e0eafa1e50ab3700e2d380177efad338c7b61ba6dad48`
- `R33_NATIVE_N01A_DESIGN.md`:
  `b90f947306ea0c3694023174ae82fa45edb34ae893582f6435a11943e9346035`
- retained `R33_NATIVE_N01A_LAUNCH.stdout`:
  `3617d8b935b0c24f077e17931465b985c29a6f28c29a07a078464d7d78b7a96b`
- N01A BUILD02 `n01a`:
  `4a993d620519faec101d0b967a3f91759a55ed0d4c5f26094e08c401022bd580`

## Claim boundary and limitations

Compilation proves only that this exact source is accepted by the pinned compiler for the
requested target. It does not establish working kqueue behavior, timer delivery,
supervision correctness, assertion outcomes, or resource values until a separately frozen
N01B primary is executed.

Even a future clean N01B run may support only a narrow native macOS direct-child process
supervisor engineering claim for the exercised cases. It must not be described as:

- whole-runtime, hostile-code, sandbox, process-group or descendant containment;
- a network/filesystem security certificate beyond the fixed tested paths;
- hard RSS containment;
- power-loss durability, journal recovery, telemetry qualification or signed authority;
- learner cognition, learning, training, sensory S0/S1/S2, full-brain migration,
  competency, promotion, grant/milestone change, dominance or R33 completion;
- repair or success of the frozen failed N01A identity;
- compiler recovery or qualification of the unavailable monotonic helper.

N01B is an engineering corrective identity only. Main owns preregistration and execution.
