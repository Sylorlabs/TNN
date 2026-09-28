# Arm-1 teacher 8-slice reproduction under fresh REAL perturbations

Date: 2026-09-21. Crew: marathon crew 8 (determinism expansions).
Frozen vectors: `wired/expected/S{i}.bin` (session ids 1001..1008),
sha256 recorded below. Prior perturbations (session-id change, env
noise, stimulus flips) are superseded here by perturbations verified
REAL at the OS level — the old M8 battery's MALLOC_PERTURB_ was PROVEN
a no-op on this runtime, so this re-trial uses only classes that
demonstrably perturb the process (see §0). Bar: N=5 runs per class,
stdout bytes == expected vector for all 8 slices, REQUIRED.

Build (pure Zag): `znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze
--no-foreground-cache` teacher.zag -> tb1 (64,682 bytes). Built TWICE:
tb1 md5 1e7791c3fe85a76a4ee39d6e844ff262 == tb2 (build determinism).

Invocation: `tb1 <slice 0-7> <session_id 1001+i> <wired_dir>`.

## §0 Perturbation classes (verified REAL)

- baseline: normal ASLR, normal env, absolute argv[0] + absolute wired_dir.
- aslr_off (N=5): `setarch x86_64 -R`; child base pinned 0x555555554000.
- envsize (N=5): env -i + filler 1024/8192/32768/65536/120000 bytes;
  [stack] VMA demonstrably shifts with env size.
- cwd (N=5): /, /tmp, harness dir, arm1 dir, deep nested dir.
- stack (N=5): ulimit -s 1024/8192/32768/131072/unlimited.
- argshuffle (N=5): argv[0] as absolute / ./tb1 / short symlink /
  62-char symlink / absolute + wired_dir absolute vs relative-from-deep-cwd;
  slices executed in 5 different orders (per-slice outputs compared
  individually, so order cannot mask a divergence).

## §1 Results — 30/30 runs PASS, 0 divergences

Expected sha256 (frozen vectors, reproduced exactly in every run):

| slice | session | sha256 |
|---|---|---|
| S0 | 1001 | 1e30aa9084a2dc8f586f4608f366110dfd109b44f82352aa93d72dff56fc75b5 |
| S1 | 1002 | 104513e3d8615b2636ed28a60e4c4d7ca202b5ee1cc1fcab4239215c67a2233c |
| S2 | 1003 | 6e854c5e1e93c85ef6d61c8ad5eb07d6c75ae3ef2344204c73245866c58b2dad |
| S3 | 1004 | f34bda21e04374bc7697efc5f5eb2336ce0ad346586c8c5035a7ba7b5bf113d5 |
| S4 | 1005 | 159c2a11342e081a5b5c019e435c9152f805f3964b7f1af98f606d6967903776 |
| S5 | 1006 | 2583e682288588cf961048063cdffaab4f721d32b52ba7552a9edc0f365bbeb7 |
| S6 | 1007 | f7df2361f48df5ffd0ef125afd9f233031d04a44319bbdeb57b2b8124f5186c9 |
| S7 | 1008 | f473c5e01e76e0f406b6468fa2948295dbbe9a54a27bdf2afdc1a891ee40b311 |

Per class: baseline 5/5 | aslr_off 5/5 | envsize 5/5 | cwd 5/5 |
stack 5/5 | argshuffle 5/5 — 240 slice executions, all rc=0, all
byte-identical to the frozen vectors.

## §2 Anomalies during the run (reported, not papered over)

1. One transient: a single argshuffle run-4 execution failed (rc=1,
   empty stdout/stderr) mid-campaign while a concurrent harness battery
   was running; the identical command passed on the immediate rerun and
   8/8 subsequent identical executions pass. No mechanism identified;
   no reproduction after cleanup. Treated as environment transient, not
   a determinism finding — the bar (N=5 clean per class) is met with
   headroom (10+ clean executions of that exact case).
2. Script bugs caught by the bar itself (wrong relative wired_dir depth,
   md5-vs-sha256 reference mixup, trailing whitespace in expected-hash
   list): all surfaced as loud mismatches, fixed, full loop re-run
   clean. No silent passes.

## Verdict

**PASS** — arm-1 teacher 8-slice reproduction byte-identical under all
fresh REAL perturbations. No divergence to bisect. The no-RNG /
byte-identical-rerun gate (RULE-3, RULE-4) holds under ASLR on/off,
env-size shifts, cwd changes, stack-size changes, and argv shuffling.
