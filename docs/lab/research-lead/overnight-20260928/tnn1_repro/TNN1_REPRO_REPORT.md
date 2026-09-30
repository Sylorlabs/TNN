# TNN-1 Independent Reproduction Report

## Verdict: TNN1-REPRO-PASS

Date: 2026-09-30
Worker: TNN-1 Independent Reproduction Worker

## Method

1. Extracted committed source from build commit `0323b97d5`:
   `git show 0323b97d5:docs/lab/research-lead/overnight-20260928/tnn1_build/tnn1.zag`
2. Verified committed source is byte-identical to the working-tree copy
   (`cmp` PASS, 1088 lines).
3. Built with the pinned compiler
   `src/tools/toolchain/znc_linux_x86_64_abed8aa1` via
   `znc tnn1_committed.zag -o tnn1_repro_bin`.
   Build exit 0. Warnings only (A0102 ignored-return-value analyzer
   warnings, non-blocking).
4. Ran the rebuilt binary 3 times, capturing stdout each run.

## Results

- **Binary identity:** Rebuilt `tnn1_repro_bin` is byte-identical to the
  committed `tnn1_bin` (169082 bytes, `cmp` PASS). The committed source
  reproduces the committed binary exactly.
- **Test battery:** 35 PASS, 0 FAIL on all three runs. Final line:
  `TOTAL 35/35`. Test names observed: CLA-2 P1/P2/P2b/P3a/P3b/P4/P5,
  ABL-I, ABL-C, ACT A1-A6, COMP-1, CAM-1 P6/P7, DV, XCAP.
- **Determinism:** SHA-256 of stdout on all three runs:
  `78847448a6afa384b6c9387d11d80ea849135f4c402196a3e03034b254cd8164`
  This matches the value reported by the independent red team
  (commit `cbde38737`, TNN1_REDTEAM_REPORT.md Vector 5).

## Conclusion

REPRO-PASS. The TNN-1 build is independently reproducible from committed
source: same source, same pinned compiler, byte-identical binary,
35/35 tests, 3/3 byte-identical outputs matching the reported hash.

No discrepancies found.

## Governance

- Step 0 guard recorded in NAMECHECK.md: `/usr/bin/python3` present as
  unremovable system binary, documented non-use, zero invocations.
- Target source not modified. Read-only on `tnn1_build/`.
- Build artifacts kept in `/tmp/tnn1_repro/`; not committed.
- No sealed FW1-FW9 files accessed.
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` untouched.
- No em dashes in this report (byte-checked on write).
