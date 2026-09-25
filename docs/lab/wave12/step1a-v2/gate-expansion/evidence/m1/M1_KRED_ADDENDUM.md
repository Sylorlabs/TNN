# M1 K-RED Addendum — Blind Red-Team Round

**Date:** 2026-09-25 (~14:16 PDT)
**Method crew:** M1 method crew (method-blind to the plants until freeze)
**Red-team manifest:** `redteam/MANIFEST.md` (12 blind plants, frozen)
**Frozen launcher:** `targets/m1_sandbox.bin` — SHA-256 `fbc5f338627f63ac26cedae31acca7e003626ae0e146d06fb566b9cc0771ced5` (verified before running; launcher, filter, and verdict criteria NOT modified)
**Pinned toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Source SHA check:** all 12 `.zag` source SHAs match the manifest table exactly.
**Run protocol:** each compiled plant run 3× under the frozen launcher, ≥60 ms wall-clock sleep OUTSIDE the sandbox between runs (per the granularity caveat). Raw per-run logs: `redteam/kred_logs/`.
**Frozen miss definition:** exit 0 AND stdout varies across the 3 sandboxed runs. SIGSYS/SIGSEGV = CAUGHT. Exit 0 with identical stdout ×3 = not a miss (NEUTRALIZED if it varied unsandboxed).

## Per-plant results

| # | Plant | rc ×3 | Signal ×3 | stdout SHA-256 (run1 / run2 / run3) | stdout varied? | K-RED verdict |
|---|-------|-------|-----------|--------------------------------------|----------------|---------------|
| 1 | a1_times | 0,0,0 | — | 4d8b3668…96d / d88247e0…ca935 / a9c3d975…4bcde | YES | **MISS** |
| 2 | a2_itimer | 0,0,0 | — | f7ec7f5d…7ea84a / 50eaddd5…ba1e3d2 / 80fd5116…7892aa8 | YES | **MISS** |
| 3 | a3_adjtimex | 0,0,0 | — | a0ce8e7f…448e358 / bac8e523…51e30fb0e / 964cecf4…6dbe93d76 | YES | **MISS** |
| 4 | b1_vvar_churn | 0,0,0 | — | d0ae1c31…5b1deb9e / 7cd340b9…983b8f74 / c8d0101d…318b7f57 | YES | **MISS** |
| 5 | b2_stack_auxv | 0,0,0 | — | 9a204ef1…480db61 / 801bb28b…809aa97e / 117b52fa…f51b80ad | YES | **MISS** |
| 6 | b3_vvar_tsc | 0,0,0 | — | aa563586…d9cb58 / c303521b…a85e94a6d8 / 1c2373c7…ad2505 | YES | **MISS** |
| 7 | c1_uuid | 0,0,0 | — | 75189187…dda97ab3 / 90fb5a4c…b8e5e3c / 9863a249…a063b5 | YES | **MISS** |
| 8 | c2_auxv_random | 0,0,0 | — | c7341fe0…f262c0fb / 132a3ec6…d5cc07 / 2e8dc7a4…09c3ca53 | YES | **MISS** |
| 9 | c3_getpid | 0,0,0 | — | b1f383a2…b11642a / 6b6a49eb…2e9514005 / bc636239…9c7389b | YES | **MISS** |
| 10 | d1_times_xorshift | 0,0,0 | — | f626aad5…9d65b0989 / 430473dc…fd / 329b0467…62c31ff8f | YES | **MISS** |
| 11 | d2_uuid_checksum | 0,0,0 | — | f55f1031…05242d / 42f451d0…5df46260e / 8d62e4ae…b10ff0f2 | YES | **MISS** |
| 12 | d3_pid_word | 0,0,0 | — | 41ee6fa3…fd7 / d28cb7ec…959b8cd3c / 41ee6fa3…fd7 | YES (alpha/echo/alpha) | **MISS** |

Full stdout SHA-256 values and per-run outputs: `redteam/kred_logs/SUMMARY.txt` and `redteam/kred_logs/<plant>_run<N>.out`.
Compiled binary SHAs: logged in `redteam/kred_logs/SUMMARY.txt` (bin_sha per plant).

Sample outputs (run 1): a1 `tick=430323964 spin_iters=11574` · a2 `remain=9.999945,9.999869,9.999819,9.999731` · a3 `time=1790370915.68544` · b1 `changed=0:4307051464>4307051552,…` · b2 `rand=-4489933852600401354:-8704195433478803801` · b3 `cycles=12843762437846>12843763935594` · c1 `uuid=df637f93-9e29-4578-8478-8c20e93b6f64` · c2 `rand=-1292817918350298192:-7278383508452273285` · c3 `pid=38922` · d1 `out=7426852062368631723,4612190363583300767,6027314157532376888` · d2 `h=6874962241318230428` · d3 `word=alpha`.

## Miss rate and final K-RED verdict

- **K-RED: 12/12 misses** — every blind plant exited 0 with varying stdout under the frozen sandbox; zero were killed (no SIGSYS, no SIGSEGV), zero neutralized.
- **K-RED fires (miss rate > 0).** This M1 version is **DEAD** — it does not survive the blind red-team round.

## What the misses prove about the mechanism

The M1 filter blocks exactly three x86-64 syscalls: 318/getrandom, 228/clock_gettime, 96/gettimeofday. The red team systematically walked around that narrow deny-list, and every route survived:

- **(a) syscall disguise:** times(100) is a 100 Hz wall clock, setitimer(38)/getitimer(36) give µs remaining-time precision, adjtimex(159) returns kernel tv_sec/tv_usec — all unfiltered and all carry usable entropy.
- **(b) memory nondeterminism:** the kernel-updated vvar page (vvar churn, vvar `cycle_last` as "rdtsc without the rdtsc instruction") and the 16 AT_RANDOM bytes sitting on the stack are plain memory reads — zero syscalls, nothing for a syscall filter to catch, and PR_SET_TSC-style instruction traps never fire on memory loads.
- **(c) environment dependence:** `/proc/sys/kernel/random/uuid` is a fresh kernel-generated UUID per read through allowed open/read; AT_RANDOM is readable from `/proc/self/auxv`; getpid(39) is unfiltered per-run-unique state.
- **(d) consumption laundering:** all of the above feed control flow or PRNGs whose outputs vary without ever printing raw entropy — d1 seeds xorshift from times(100), d2 folds uuid bytes into a checksum loop count, d3 indexes a word table by pid%8.

Pattern: a seccomp-BPF deny-list of 3 literal syscalls cannot cover the kernel's redundant entropy surfaces. The known battery (K-CATCH 8/8) only tested the literal, documented routes; K-RED shows the gate is porous along every axis the red team probed.

## Method notes

- No launcher/filter/source changes during the round (verified launcher SHA before and at run time).
- Plants compiled as shipped; no repairs or retries (no mid-round method repair).
- The red team's own abandoned approaches (RDRAND via RWX thunk, forged `__vdso_clock_gettime` call) and the known vDSO bypass limitation are consistent with the observed misses: the filter's coverage ends at its 3 listed syscalls.
- Evidence uncommitted; working tree only, per instructions.
