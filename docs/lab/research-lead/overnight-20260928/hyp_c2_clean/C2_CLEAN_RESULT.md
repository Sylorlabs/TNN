# RESULT: Hypothesis C2 Battery v2 Clean Rerun (K4-clean reproduction)

Date: 2026-09-30.
Prereg: d01f4cb8a (PREREG_HYPC2_CLEAN_RERUN.md, frozen before any build or run).
Amended wave: f313372d7 (C2-F5 FIRES, falsification of C2 as bounded discovery).
K4 amendment to original wave: 286c8e681 (K4-VIOLATION, purity certification revoked).

## Verdict: C2-CLEAN-PASS

All three kill bars hold. The clean rerun is byte-identical to the frozen
v2 output. The C2-F5 falsification is reproduced under a K4-clean chain.

## What was done

1. Copied the frozen mechanism source `hyp_c2_impl/hyp_c2.zag` byte-for-byte
   into the owned directory as `hyp_c2_clean.zag`; sha256 verified against
   the frozen value 3f734a4c1b11986766154de3bb3d6f8e2a8f897ee886939f2f8c2dfa06952392
   before compiling. No source edits.
2. Compiled with the repo znc toolchain (znc 2026.07.0-dev) to
   `hyp_c2_clean_bin`. Build log: build.err (contains only a znc planning
   warning; exit 0).
3. Ran the binary three times: RUN_CLEAN_1/2/3.txt with RUN_CLEAN_1/2/3.err
   stderr captures.
4. Verified: 3/3 byte-identical (cmp); md5 of each stdout is
   d6fc84c095c251afd87e79eee7491f54, matching the frozen expected digest;
   `cmp` against the frozen v2 output `hyp_c2_impl/run_v2_1.txt` confirms
   exact identity. Stderr empty on all three runs (0 bytes).
5. Byte-checked every new file with the shell-only snippet
   `worker_snippets/check_no_dash.sh`: all clean, zero em/en-dash bytes.

## Reproduced measurements (identical to f313372d7)

- T0 (full, 2x+1): SOLVE. 9/9 train, 16/16 held-out, 5 ops, 229287 evals,
  3 repairs, 1 backtrack, 0 splits.
- T1 (P-VM, abs): BUDGET. 1000012 evals (>1M). C2-F5 fires.
- T2 (full, mod3): SOLVE. 17/17 train, 17/17 held-out, 3 ops, 105230 evals.
- T3 (full, parity): BUDGET. 1000020 evals (>1M). C2-F5 fires.
- T4 (P-VM, nested abs): BUDGET. 1000001 evals (>1M). C2-F5 fires.
- T5 (P-VM, fragment composition): BUDGET. 1000009 evals (>1M). C2-F5 fires.
- F-SMUG: audit passes on all P-VM tasks (fsmug=1). Op cap: T0 5, T2 3
  (both <= 40). C2-F1/F2/F3/F4: NOT FIRED. F-TRICK, F-MEM: NOT FIRED.

## Kill bars

- K1: PASS. Prereg d01f4cb8a is an ancestor of this result commit;
  at the prereg commit the owned directory contained only the prereg file.
- K2: PASS. Zero Python at every stage: authoring, byte checking (shell
  snippet only), building (znc), running, verification (sha256sum,
  md5sum, cmp, grep), committing (git), and this report's preparation.
  No Python invocation of any kind occurred in this wave.
- K3: PASS. Three runs complete, 3/3 byte-identical, zero stderr bytes.

## Implications

The C2 falsification (C2-F5 FIRES: T1/T3/T4/T5 exceed the 1M budget on
Battery v2) now rests on a K4-clean measurement chain. The original
wave's measurements are corroborated exactly; the amendment 286c8e681
may reference this rerun as the canonical purity chain.

No promotion follows: the verdict is a falsification. Per the amendment
conditions, the valley-depth battery may freeze the mechanism files;
the mechanism code was never flagged, only the original wave's purity
certification.

## Files (all under docs/lab/research-lead/overnight-20260928/hyp_c2_clean/)

- PREREG_HYPC2_CLEAN_RERUN.md (prereg, d01f4cb8a)
- hyp_c2_clean.zag (frozen mechanism, sha256 3f734a4c..., byte-identical
  to hyp_c2_impl/hyp_c2.zag)
- hyp_c2_clean_bin (compiled binary, build.err)
- RUN_CLEAN_1/2/3.txt (3/3 byte-identical, md5 d6fc84c0...)
- RUN_CLEAN_1/2/3.err (empty)
- C2_CLEAN_RESULT.md (this file)
