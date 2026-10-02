# REPORT: F2 v6 3x SEALED EVALUATION (wave-20261002-1121pdt, lane F2)

Task: queue item 10. Re-run the frozen F2 v6 sealed evaluation
(PREREG_F2V6.md, frozen 2026-10-02, wave-20261002-0521pdt) that went
PARTIAL under CPU contention. Measure K6-R4 (convergence + two
revisions + wave-3 goal achievement) under serialized, clean-as-possible
CPU conditions. Pure Zag throughout.

## Provenance (inherited, not re-authored)

- Prereg: docs/lab/rsi/runs/wave-20261002-0521pdt/F2/PREREG_F2V6.md
  (frozen commit 8f99040b3; NC5 amendment 3c69d53cb).
- Implementation: .../0521pdt/F2/f2v6_learner.zag @50693d022
  (206 changed lines vs v5 base; sha256
  e041d4f6bfcdccf851a05167ace6d492b76d7ac60f6a8f4ad0e61ee9e8404d87).
- Prior sealed record: .../0521pdt/F2/SEALED_EVAL.md (PARTIAL).
- This lane modifies NO source and NO sealed world. Rebuild only.

## Seal verification (before any run)

World hashes recomputed and matched against the prereg freeze record:

- shift2: 05e26e0854427b07fa3b0971f46d22cdec368f9d84bad1b6a057d05f730ca054 MATCH
- shift1: c0986c12fd3ad22366b37eb943927c1df7ba482557b18a75ccbae5f075dc6f5c MATCH
- osc:    2fb92115015f385649fbab78f40fcc8b815d9c3db725d2ad4b7db005f74a0470 MATCH

Seal holds. Worlds frozen (committed) before all runs below.

## Kill bars applied (frozen, unmoved)

K6-R1..R8 per PREREG_F2V6.md section 8. Negative controls NC1..NC5 per
section 9 (NC5 per the 2026-10-02 amendment). BUILD-PASS requires all
eight bars; any FAIL is BUILD-FAIL.

## Run conditions

- Toolchain: safebin znc (/home/hatch/safebin/znc); python3/python
  resolve to nothing (NAMECHECK.md Step 0).
- Sealed binary: /tmp/f2v6_shift2, sha256
  196c889361dfae6968318b132b054f481a23037ef059756578b69beca559a545
  (built from frozen sources via lane build.sh).
- Serialization: one sealed run at a time; no compiles in parallel
  with measurement; live scaling binaries (s5f_bin, s10000_bin_fixed)
  not disturbed.
- Byte-identical check: sha256sum + cmp over the binary's stdout
  (run metadata kept in separate .meta files, not in the compared log).

## SHIFT2 sealed runs (the 11-action planning gap)

(to be filled)

## K6-R4 adjudication (mechanical, from logs)

(to be filled)

## Negative controls

(to be filled)

## Regression (K6-R8)

(to be filled)

## Red team

(to be filled)

## VERDICT

(to be filled)
