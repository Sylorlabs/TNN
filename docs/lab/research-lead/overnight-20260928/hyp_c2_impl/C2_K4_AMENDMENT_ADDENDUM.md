# C2 K4 Amendment Addendum: Purity-Repaired Evidence Chain

Date: 2026-09-30.
Amends: 286c8e681 (C2_K4_AMENDMENT.md, transparent amendment).
Clean rerun result: cdffdcca9 (C2_CLEAN_RESULT.md).
Clean rerun prereg: d01f4cb8a.

This addendum is appended, not substituted. The original amendment
(C2_K4_AMENDMENT.md) and the original result files (f313372d7) are NOT
edited. Transparent amendment remains the sole correction mechanism.

## What the clean rerun establishes

Commit cdffdcca9 is a K4-clean rerun of the C2 Battery v2 wave, executed
under a strictly zero-Python chain from task start through commit:

- Prereg d01f4cb8a frozen before any build or run; ancestry verified.
- Mechanism source hyp_c2_clean.zag copied byte-for-byte from the frozen
  hyp_c2.zag (sha256 match, zero edits).
- Three runs, 3/3 byte-identical (md5 d6fc84c095c251afd87e79eee7491f54
  each), zero stderr bytes, and cmp-identical to the frozen v2 output
  run_v2_1.txt from f313372d7.
- Kill bars K1 (prereg precedes), K2 (zero Python at every stage),
  K3 (3/3 deterministic) all PASS.

The falsification is reproduced exactly: T0 SOLVE, T2 SOLVE; T1/T3/T4/T5
BUDGET with C2-F5 firing; F-SMUG audit passes; C2-F1/F2/F3/F4, F-TRICK,
F-MEM not fired.

## Effect on the amended wave

1. The purity certification revocation in C2_K4_AMENDMENT.md stands:
   the original wave (f313372d7) remains K4-VIOLATION because the
   disclosed python3 -c "pass" invocation cannot be undone.
2. The evidence chain is now purity-repaired: cdffdcca9 provides a
   canonical K4-clean measurement of the same falsification. Readers and
   downstream gates should cite cdffdcca9, not f313372d7, for the C2
   measurements.
3. The verdict is unchanged: C2 remains falsified as a bounded discovery
   mechanism (C2-F5 FIRES). No promotion follows from the clean rerun;
   a falsification needs no rescue, only a clean evidence chain.
4. The mechanism code was never flagged: only the original wave's purity
   certification was. The valley-depth battery may freeze
   hyp_c2_clean.zag (or hyp_c2.zag, byte-identical) as mechanism files.

## Verdict mapping

- Original wave f313372d7: C2-TESTED, K4-VIOLATION (purity).
- Clean rerun cdffdcca9: C2-CLEAN-PASS (K4-clean measurement, same
  falsification verdict).
- Standing verdict: C2-F5 FIRES; C2 falsified as bounded discovery.
