# PREREG: F2 Retry Independent Reproduction (F2-REPRO)

Date: 2026-09-30. Status: FROZEN. This prereg is committed alone before any
reproduction work. No reproduction binaries, concatenations, or runs exist
at commit time.

## 1. Objective

Independently reproduce the F2 retry (AUTOSCI2, implementation commit
1eb66765d, reported BUILD-PASS in RESULT_AUTOSCI2.md) from committed source
only, with no assistance from the original builder. This is promotion
pipeline step 4 (independent reproduction), recommended first in information
order by the F2 promotion assessment (ffcfc50e8).

## 2. Frozen target

- Source commit: 1eb66765d (local, tnn-native-lab).
- Files: docs/lab/research-lead/overnight-20260928/autosci2/
  PREREG_AUTOSCI2.md, RESULT_AUTOSCI2.md, autosci2_learner.zag,
  world_a2.zag, world_b2.zag.
- Reported frozen results to reproduce exactly:
  - World A: 3/3 runs byte-identical, md5 156d4ea8fefa74443502d5592ac89e91
  - World B: 3/3 runs byte-identical, md5 52cd392ca369bbdfcb3f3f9c0ffd5ac7

## 3. Method (frozen)

1. Extract the three .zag files from the frozen commit 1eb66765d into a
   scratch area (read-only copy; no modification).
2. Build: concatenate autosci2_learner.zag + world_a2.zag into run_a.zag;
   concatenate autosci2_learner.zag + world_b2.zag into run_b.zag.
   (This matches the world file comments: "Concatenate AFTER
   autosci2_learner.zag".)
3. Compile each concatenated file with the repo znc toolchain and execute.
4. Run each world 3 times. Record md5 of stdout for each run.
5. Compare reproduced md5s against the frozen reported md5s above.
6. Record all reproduction artifacts under
   docs/lab/research-lead/overnight-20260928/f2_repro/ and commit.

If the source does not build or run as documented, that is a finding, not a
reason to modify source. The reproduction uses the source exactly as
committed. Build flags or concatenation order beyond section 3 step 2 are
not permitted without a prereg amendment and re-freeze.

## 4. Kill bars (frozen)

- K1 (non-author independence): the reproduction is performed by an agent
  who did not author the AUTOSCI2 implementation, working only from the
  committed files. The committed source is used verbatim; no edits to the
  three .zag files. FAIL if any source modification is required to build.
- K2 (result match): World A reproduced md5 equals
  156d4ea8fefa74443502d5592ac89e91, and World B reproduced md5 equals
  52cd392ca369bbdfcb3f3f9c0ffd5ac7, each across 3/3 byte-identical runs.
  Any mismatch: REPRODUCTION-FAILED (report which world, which run, and
  the observed md5 and a diff characterization).
- K3 (purity): pure Zag only. No Python at any stage (source, build,
  execution, analysis, editing of wave artifacts). No em dashes in wave
  documentation. Otherwise: FAIL.

## 5. Verdicts

- REPRODUCED: K1, K2, K3 all pass.
- REPRODUCTION-FAILED: any kill bar fails. The report must state exactly
  what failed and whether the failure is non-author environment,
  under-specified build, or source-level.

## 6. Governance

Commits local on tnn-native-lab, owned path only:
docs/lab/research-lead/overnight-20260928/f2_repro/.
