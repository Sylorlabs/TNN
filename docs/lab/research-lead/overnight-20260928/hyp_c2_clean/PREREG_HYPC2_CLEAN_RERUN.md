# PREREG: Hypothesis C2 Battery v2 Clean Rerun (K4-clean reproduction of the C2-F5 falsification)

Date: 2026-09-30.
Status: FROZEN PREREGISTRATION. No rerun build or run has been performed yet.
Authority: This document alone, committed before any rerun artifact exists.

## 1. Reason

The C2 Battery v2 wave (result commit f313372d7, HYP_C2_RESULT_V2.md) falsified
C2 as a bounded discovery mechanism (C2-F5 FIRES: T1/T3/T4/T5 exceed the 1M
evaluation budget). The wave was flagged K4-VIOLATION by transparent amendment
286c8e681 after the implementer self-disclosed a single no-op
`python3 -c "pass"` invocation during byte checking. The measurements stand as
flagged evidence; the purity certification is revoked.

This rerun reproduces the exact v2 protocol with strictly zero Python at every
stage, so that a canonical K4-clean measurement chain exists for the C2
falsification. No mechanism change. No new hypothesis. The falsification
verdict is the expected reproduction; this wave tests governance purity and
reproducibility, not a new claim.

## 2. Frozen inputs (read-only, copied or referenced but never modified)

- Mechanism source: `docs/lab/research-lead/overnight-20260928/hyp_c2_impl/hyp_c2.zag`
  (sha256 3f734a4c1b11986766154de3bb3d6f8e2a8f897ee886939f2f8c2dfa06952392,
  904 lines). This is the exact source that produced f313372d7.
- v2 prereg: 9bc64e4cf. Original v1 prereg: 01336fe83. Battery v2 prereg: d2a69d512.
- Expected v2 output digest: md5 d6fc84c095c251afd87e79eee7491f54
  (run_v2_1/2/3.txt at f313372d7, 3/3 byte-identical).
- Compiler: the repo Zag toolchain (znc 2026.07.0-dev).

## 3. Rerun protocol

1. Copy hyp_c2.zag byte-for-byte into the owned directory
   `docs/lab/research-lead/overnight-20260928/hyp_c2_clean/` and verify sha256
   matches the frozen value before compiling.
2. Compile with znc to a clean binary in the owned directory. No source edits.
3. Run the binary three times, capturing stdout to RUN_CLEAN_1/2/3.txt and
   stderr to matching .err files. No arguments; the program runs all six v2
   tasks (T0 full, T1 P-VM, T2 full, T3 full, T4 P-VM, T5 P-VM) in one pass.
4. Verify: all three stdout files byte-identical (cmp); stderr empty; md5 of
   each stdout compared against the frozen expected digest d6fc84c0....
   Divergence is reported as a REPRODUCTION-DIVERGENCE finding, not hidden.
5. Byte-check every new file for em/en-dash bytes using the shell-only
   snippet `worker_snippets/check_no_dash.sh` (never Python).
6. Commit rerun artifacts with explicit pathspec to the owned directory only.

## 4. Frozen verdict rule

- C2-CLEAN-PASS: K1, K2, K3 all hold AND all three clean runs are
  byte-identical to each other AND byte-identical to the frozen v2 output
  (md5 d6fc84c0...). The C2-F5 falsification is then reproduced under a
  K4-clean chain.
- C2-CLEAN-FAIL: any kill bar fails. If K1/K2/K3 hold but clean output
  diverges from the frozen v2 output, report REPRODUCTION-DIVERGENCE with
  both digests; verdict remains C2-CLEAN-FAIL.
- Verdict concerns the rerun's governance cleanliness and reproducibility
  only. It does not alter the C2-F5 falsification itself.

## 5. Kill bars

- K1: This prereg is committed alone (owned directory contains only this
  file at prereg time) and strictly precedes the first copy/build/run.
  Verified by `git merge-base --is-ancestor`.
- K2: Zero Python at every stage of this wave: authoring, byte checking,
  building, running, verification, committing, and this report's
  preparation. Shell tools only (sh, cp, sha256sum, md5sum, cmp, diff,
  grep with byte patterns, git). A single Python invocation of any kind,
  including no-ops, voids the wave.
- K3: Three clean runs complete, 3/3 byte-identical, zero stderr bytes.

## 6. Determinism

Frozen seed 0xC2C2C2 (unchanged from the original wave). All ordering is
deterministic by construction of the frozen mechanism.

## 7. Governance

Pure Zag only, per K2. No em/en-dash bytes in committed files (verified
with the shell-only byte-check snippet before commit). Commits local,
owned path `docs/lab/research-lead/overnight-20260928/hyp_c2_clean/`
only. Explicit pathspec commits. Nothing is pushed.
