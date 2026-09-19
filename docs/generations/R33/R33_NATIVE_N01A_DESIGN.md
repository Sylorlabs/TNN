# R33-N01A native process-supervisor V2 design

Status: implementation + compile-only corrective engineering package. No N01A case has
been executed. No learner, scientific data, training, parent mutation, grant, registry,
handoff, Python execution, or Python edit is part of this package.

## Purpose and separation from frozen N01

N01A is a new disjoint engineering fixture. It does not alter or reinterpret frozen
`R33_NATIVE_IO_V1.zag`, `R33_NATIVE_PROCESS_V1.zag`, the N01 driver/preregistration,
BUILD03, or the sole N01 primary result. N01's retained status and withheld broad
supervisor claim remain historical evidence; N01A is the corrective implementation path.

`R33_NATIVE_PROCESS_V2.zag` imports frozen IO_V1 and adds process-supervision semantics.
`R33_NATIVE_N01A_DRIVER.zag` is a native corrective fixture that must not be run until the
main agent preregisters the exact source/binary identities and assertion contract.

## V2 process contract

`nrv2_run` supervises one direct child PID. It validates the root, binary/mode bounds,
deadline, output limit, and **label length <=57 before any output-file write**. The
57-character limit is deliberate: appending `.stdout` or `.stderr` yields the frozen
IO_V1 64-character child-name maximum.

All C strings, generated names, argv/env, wait/rusage storage and poll storage are
allocated before output creation. Child output files use IO_V1 exclusive create, then are
required to be regular and initially size zero. If only one output artifact has been
created and a later admission step fails, V2 closes acquired descriptors, frees owned
allocations, returns `NRV2_ARTIFACT_PARTIAL`, and **does not delete the artifact**.
Evidence-preserving partial admission is intentional.

After fork, the child installs a hard `RLIMIT_FSIZE=output_limit` using preallocated
post-fork storage, redirects stdout/stderr, and calls `execve` with exactly one argument
and an empty environment. `execve` failure exits 127. Redirection failure exits 126;
child file-limit installation failure exits 125. The parent additionally measures both
output file sizes after reap and records an explicit output-limit violation if either
exceeds the requested ceiling.

The parent does **not** rely on a child-installed wall timer. It samples
`_zag_clock_monotonic_ms()`, polls `wait4(pid,...,WNOHANG,...)`, pauses in bounded 5 ms
`select` intervals, and compares elapsed monotonic milliseconds with the requested
deadline. At timeout it sends `SIGKILL` to the direct child PID and performs a final
blocking reap (with bounded EINTR retries) before returning. Non-EINTR wait failure also
triggers direct-child kill + final reap. Timeout is separately classified as
`NRV2_TIMEOUT` with `timed_out=1`.

### Containment boundary

V2 contains **only the direct child PID**. It does not establish a new process group,
kill a descendant tree, sandbox hostile code, or prove that grandchildren cannot escape.
N01A children do not fork. A future supervisor that admits descendant-creating programs
requires a separately reviewed process-group/session/capability policy and falsifiers.

## Native one-shot admission and write scope

`nrv2_admit_root` performs native `mkdir` first. A pre-existing primary returns Darwin
`EEXIST (-17)` and is not opened/retried by that admission attempt. If creation succeeds
but the protected root open fails, the new directory is preserved and reported as a
partial admission; it is not deleted.

The fixed fixture path is:

`Research/R33_NATIVE_N01A_RUN_PRIMARY_V1`

The **whole run directory** is the documented write envelope. This includes the `fs`
subdirectory and all supervisor child `.stdout` / `.stderr` evidence files. There is no
N01-style `/fs`-only wording. The generic V2/IO_V1 functions are not themselves a
filesystem sandbox; the fixed N01A driver supplies the scoped path.

## Corrective fixture cases encoded but not executed

The driver uses exact native assertions and returns nonzero on any mismatch. It encodes:

- first primary admission succeeds; immediate second admission returns exact `-17`
  without opening/retrying that attempt;
- a child directory opened through the V2 regular-child wrapper is rejected as
  `NRV2_NONREGULAR`;
- `../outside` is rejected by the frozen IO_V1 child-name boundary;
- literal labels of length 57, 58 and 64 are measured; 57 is accepted while 58/64 are
  rejected before output admission/start;
- forced second-output `EEXIST` produces explicit partial-artifact status, no child
  start, and leaves the first output artifact readable as preserved evidence;
- the 57-character label is used by a normal child which must start, exit 0, be reaped,
  produce no stdout/stderr, and avoid timeout/output-limit classification;
- an **unguarded** infinite child deliberately installs no wall guard; V2 must classify a
  parent-owned 100 ms timeout, send direct-child `SIGKILL`, and final-reap signal 9;
- a missing executable is actually forked and reaches `execve`, producing normal child
  exit 127 rather than being misreported as a timeout;
- the admitted primary root is closed and aggregate `N01A_FAILURES` must be exactly zero
  before the success marker can print.

No symlink object is fabricated by N01A because frozen IO_V1 has no symlink-creation
primitive and the task forbids broadening into unrelated host tooling. Thus N01A tests
the frozen lexical parent-traversal refusal and V2 nonregular type rejection, while
`O_NOFOLLOW`/`O_NOFOLLOW_ANY` remain source/ABI properties inherited from IO_V1 rather
than a newly executed symlink falsifier. This limitation must remain explicit.

## Claim boundary if later preregistered and executed

Even a perfect N01A primary could support only a bounded engineering statement about the
exact pinned macOS/arm64 Zag sources: direct-child fork/exec/wait supervision, parent-
owned monotonic deadline polling, direct-child kill/final reap, exclusive regular output
artifacts, bounded output files, label/admission boundaries, selected nonregular/path
rejections, and exact fixture outcomes.

It would **not** establish descendant/process-group containment, hostile-process
isolation, a general filesystem sandbox, power-loss durability, cryptographic integrity,
native journal recovery, telemetry completeness, sensory S0/S1/S2, scientific learning,
competency, continuing-parent migration, authority/grants, promotion, or R33 completion.
It does not retroactively turn a failed historical review into a success and does not
replace the retained N01 primary result.

## Build 01

Compile command used, with no binary execution afterward:

`Research/toolchain/znc_macos_arm64_7cacbfc0 Research/R33_NATIVE_N01A_DRIVER.zag --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o Research/R33_NATIVE_N01A_BUILD_01/n01a`

Compiler stdout reported a signed native binary with 76,164 bytes text, 1,515 bytes data,
and zero external build tools. Compile stderr was empty and compile exit was 0.

Source/binary hashes below are the final BUILD01 compile snapshot and must be recomputed
after any subsequent source change before preregistration:

- `R33_NATIVE_PROCESS_V2.zag`: `0e0a951e3b2d576912d8f453ea64e3af031ebc1de0252d129d89cfbbe9935478`
- `R33_NATIVE_N01A_DRIVER.zag`: `f605018774433b353f88e34e892c7468394cabf498b77785d5eceed980ed6f66`
- BUILD01 `n01a`: `6f0b92bcc259aaeb445220fb160a2b69cd44eb018906b3767de1364e8c8ff45d`
- compiler `znc_macos_arm64_7cacbfc0`: `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`

Frozen prior references observed before N01A implementation:

- `R33_NATIVE_IO_V1.zag`: `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e`
- frozen top-level / BUILD03 `R33_NATIVE_PROCESS_V1.zag`:
  `4f35857cfc562bfc3d513caa021914dc99fe9098e8a15e9cbfc9f6cdf1af2760`
- frozen top-level / BUILD03 `R33_NATIVE_N01_DRIVER.zag`:
  `74199587fb1477a95748340ab6c453f7c9cc140d1fc77e3b40d08209ce07bb7c`
- `R33_NATIVE_N01_PREREGISTRATION.md`:
  `5340fa1ce641834930e546062c33166a0c26f73f31802a633d2c241c4522671c`
- frozen BUILD03 `n01`:
  `46463804ef73c43fb1014ab4ab5cea911f450f1ec660b7c11282cd4d0651cb5f`
- retained N01 primary `RESULT.json`:
  `a3c2617ff12bd3faee2f13221e41eb2871dce01576e8a9035bbc7bf474a0a491`

BUILD01 was recompiled after installing the hard child file-size ceiling; the hashes above
correspond to that compile. No execution is authorized by this design document.
