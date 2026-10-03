# TNN-2 Independent Reproduction Report

Worker: TNN-2 Independent Reproducer
Date: 2026-10-01 UTC
Build under test: commit `f4de7ff46` (TNN2-BUILD-PASS)
Head during reproduction: `f4de7ff46` (build under test is HEAD)
Compiler: pinned `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev (edition 2026)`,
   SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`)
Safebin toolchain guard: PASS (Step 0 of NAMECHECK.md; no forbidden executable)

## 1. Source hash verification

| Artifact | Expected SHA-256 | Observed SHA-256 | Result |
|---|---|---|---|
| `tnn2_build/tnn2.zag` | `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd` | `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd` | PASS |
| `git show f4de7ff46:...tnn2.zag` | same | same | PASS |

Committed working-tree source and the committed-at-`f4de7ff46` source both
match the expected hash.

## 2. From-scratch recompilation

- Source copied (not the binary) to a clean directory `/tmp/tnn2_repro_clean`.
- Command: `znc tnn2.zag -o tnn2_bin_repro` using the pinned znc via safebin.
- Compile exit code 0. Analyzer emitted 142 A0102/B-lint warnings only
  (ignored return values, dead code notes); none are errors under default flags.
- Fresh binary `tnn2_bin_repro`, 218789 bytes.
- `cmp tnn2_bin_repro <committed tnn2_build/tnn2_bin>`: byte-identical.

| Artifact | Expected SHA-256 | Observed SHA-256 | Result |
|---|---|---|---|
| committed `tnn2_build/tnn2_bin` | `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b` | `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b` | PASS |
| fresh `tnn2_bin_repro` | (byte-identical required) | `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b` | PASS |

## 3. Test suite: 3 runs, determinism and transcript identity

Each run: `./tnn2_bin_repro > runN_new.txt`.

| Run | Exit | Score | FAIL lines |
|---|---|---|---|
| run 1 | 0 | 46/46 | 0 |
| run 2 | 0 | 46/46 | 0 |
| run 3 | 0 | 46/46 | 0 |

SHA-256 of all six files (three fresh runs, three committed transcripts):

```
37c7b552fe56c9b03b93aadb8108dfbd1d8031c056dd0e2cdcb6a1fb88cd3911  run1_new.txt
37c7b552fe56c9b03b93aadb8108dfbd1d8031c056dd0e2cdcb6a1fb88cd3911  run2_new.txt
37c7b552fe56c9b03b93aadb8108dfbd1d8031c056dd0e2cdcb6a1fb88cd3911  run3_new.txt
37c7b552fe56c9b03b93aadb8108dfbd1d8031c056dd0e2cdcb6a1fb88cd3911  tnn2_build/run1.txt
37c7b552fe56c9b03b93aadb8108dfbd1d8031c056dd0e2cdcb6a1fb88cd3911  tnn2_build/run2.txt
37c7b552fe56c9b03b93aadb8108dfbd1d8031c056dd0e2cdcb6a1fb88cd3911  tnn2_build/run3.txt
```

The three fresh runs are byte-identical to each other AND to all three
committed transcripts. All 46 checks pass on every run, including the new
TNN-2 checks: `T2-CHAIN4`, `T2-REJECT`, `T2-INQUIRE`, `T2-ACTLIVE`, `T2-REVISE`.

## 4. Spot checks of the three changes (on the compiled source)

(a) No `exec_plan` in code: the identifier appears only in two comment lines
    (lines 6 and 324); zero code references. PASS.

(b) `t2_trial` trial loop present: `fn t2_trial(W:[]u8,s:i32,r:i32,expected:i32,masked:i32,dc:i32,di:i32)i32`
    at line 586, called from `mp_run` (line 670); implements gather/trial/
    verify over runtime-built path graphs. PASS.

(c) `miss_inquire` creating UNCERTAINTY nodes: `fn miss_inquire` at line 795;
    allocates a node and sets tag slot 0 to 30, which is `T_UNCERT()` in
    tnn2.zag (line 85); wires it into a guide node and the policy root
    (`POLICY_ROOT`). Note: the tag differs from the standalone inquiry build
    (tag 24 there) because TNN-2 reuses tag 30 for UNCERTAINTY; the source is
    internally consistent. PASS.

(d) `revise_on_contradict` topological restructure: `fn revise_on_contradict`
    at line 685; on contradiction it locates the stale SETREG step (tag 101)
    via provenance edges and calls `t2_revise_graph`, which tombstones the
    stale step, inserts a corrected literal step, rewires the sequence, and
    re-executes, reverting on verification failure. PASS.

## Verdict

**TNN2-REPRO-PASS**

- Committed source hash verified.
- Fresh binary from pinned znc is byte-identical to the committed binary.
- 46/46 on three runs, all six transcripts byte-identical.
- All three change spot checks confirmed in the compiled source.

Scope note: this is an independent-reproduction verdict (pipeline step 4).
It does not promote TNN-2 to SURVIVES; the remaining pipeline steps (simple
baseline, alternative-explanation attack, OOD, ablation, transfer/reuse,
independent red team, governance audit) are still open.
