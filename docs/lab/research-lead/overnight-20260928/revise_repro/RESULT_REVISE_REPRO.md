# RESULT: F3 REVISE independent reproduction (pipeline step 4)

Verdict: REVISE-REPRO-PASS.

## Step 0 (standing-rules name-check)

Read the standing-rules block at the top of LOOP_STATE.md before any work.
Rules in force and honored: (1) PURE ZAG ONLY, literal owner red line,
covers glue, analysis, verifiers, harnesses, and fixture provisioning;
this task used shell, git, znc, and coreutils only, zero Python anywhere.
(2) Image judge: not applicable, no image work. (3) Fork testing: noted;
this task operates on committed history only. (4) Pure-Zag red line scope:
source extraction used git plumbing (git archive, git show) only.
(5) Shell-only byte checks: all comparisons via cmp, md5sum, sha256sum,
and worker_snippets/check_no_dash.sh; never python3.

## Source under test

- Builder implementation: commit 7009d711c (f3_revise_impl/).
- Sealed evaluation: commit 1df8addec (revise_sealed/).
- Builder worlds from committed history: world_adv1.zag (f2_ablation),
  world_tneg_a.zag (f3_phase3), world_tneg_renamed.zag (f3_attack).

## Independence method

1. Extracted committed sources via git archive into a fresh /tmp/revise_repro
   directory. Never used the worktree files or the committed binaries.
2. Frozen-learner integrity gate: f3_revise.zag sha256
   354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392
   and f3_revise_abl.zag sha256
   4e3bdf0680f11778d9226ac127d20588b40a42295e85af2efaf3a1b77ea786b2,
   exactly matching the sealed evaluator's frozen gate.
3. Reconstructed all 11 harnesses by my own concatenation
   (learner + world). All 11 byte-identical (cmp) to the committed
   run_*.zag files, confirming the worlds match what the builder used.
4. Rebuilt with the repo znc (znc 2026.07.0-dev), ran each harness 3x,
   compared every run byte-for-byte (cmp) against the committed raw_*.txt.

## Results (11 harnesses, 33 runs)

All harnesses: 3/3 runs byte-identical internally (DET-OK), zero stderr
bytes on all 33 runs, and 3/3 byte-identical to the committed raw logs.

| Harness | my md5 | committed md5 | match |
|---|---|---|---|
| revise_c (T-CONJ) | f37d0acfa02f4906e0885ddc0cac4c27 | f37d0acfa02f4906e0885ddc0cac4c27 | 3/3 |
| revise_n (T-NEG) | a1ad9ac2b972e4c862c45238f38daa82 | a1ad9ac2b972e4c862c45238f38daa82 | 3/3 |
| revise_rn (T-NEG renamed) | a1ad9ac2b972e4c862c45238f38daa82 | a1ad9ac2b972e4c862c45238f38daa82 | 3/3 |
| abl_c (T-CONJ ablation) | af7643b4a9d3cf11cbd7ff75219a47d2 | af7643b4a9d3cf11cbd7ff75219a47d2 | 3/3 |
| abl_n (T-NEG ablation) | 58e747bd44a1e84ffd84869b2b0e5f18 | 58e747bd44a1e84ffd84869b2b0e5f18 | 3/3 |
| sealed_c (S-CONJ2) | 84ab277e7535c740c5210c2065a8cef6 | 84ab277e7535c740c5210c2065a8cef6 | 3/3 |
| sealed_cr (S-CONJ2 renamed) | 84ab277e7535c740c5210c2065a8cef6 | 84ab277e7535c740c5210c2065a8cef6 | 3/3 |
| sealed_n (S-NEG2) | 85ebb436b4f7d6eac370466bc98a878c | 85ebb436b4f7d6eac370466bc98a878c | 3/3 |
| sealed_nr (S-NEG2 renamed) | 85ebb436b4f7d6eac370466bc98a878c | 85ebb436b4f7d6eac370466bc98a878c | 3/3 |
| sealed_abl_c (S-CONJ2 ablation) | f1f3a016a142620a98d09b9ea1c2781b | f1f3a016a142620a98d09b9ea1c2781b | 3/3 |
| sealed_abl_n (S-NEG2 ablation) | 052bb58c6a8e22066df13875d6486ab6 | 052bb58c6a8e22066df13875d6486ab6 | 3/3 |

Verdict lines in my runs: F3P3 RESULT REVISE-PASS on revise_c, revise_n,
sealed_c, sealed_n; F3P3 RESULT REVISE-FAIL on abl_c, sealed_abl_c,
exactly as the builder and sealed evaluator reported.

## Kill bars

- K1 (independent rebuild): PASS. Sources from git objects, harnesses
  reconstructed by my own concatenation, rebuilt with repo znc; committed
  binaries never executed or relied upon.
- K2 (results match): PASS. 33/33 runs byte-identical to the committed
  raw_*.txt logs from 7009d711c and 1df8addec.
- K3 (pure Zag, 3/3 identical): PASS. Shell, git, znc, coreutils only;
  zero Python invocations; my own 3 runs per harness byte-identical.

## Honest scope

Independent reproduction of committed evidence only; no new claim.
Pipeline steps 5-11 remain. Bounded L2 verdict stands; no L3, no Criterion
0. No file outside the owned path was staged or committed.
