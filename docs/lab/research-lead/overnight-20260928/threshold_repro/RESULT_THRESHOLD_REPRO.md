# Threshold Mechanism Independent Reproduction: Result

Date: 2026-09-30. Worker: Threshold Mechanism Independent Reproducer.
Prereg: THRESHOLD-REPRO-PREREG-FROZEN (955106ae5), committed alone before
any reproduction build or run.

## Verdict

THRESHOLD-REPRO-PASS

Every committed number from d0d296650 reproduces exactly from an
independent rebuild of committed source. Zero discrepancies.

## Rebuild provenance

- Sources extracted from d0d296650 via git show into scratch:
  r3h.zag (blob 381cb28de6c2cf1d32f3478498bfdff5e5d90bdc),
  r1h.zag (blob 88745d9c5a39140d8c8db3e5b825cdfaca9154a4),
  frch.zag (blob c9b601471b549c209fc639337a92c7e6eeb3b5c1).
  All three verified BLOB-MATCH against the committed blobs.
- Independent single-change verification: diff of each extracted file
  against its v2 base at b0d1749f2
  (conditional_tax_build/r3t.zag, r1t.zag, frct.zag) shows the ONLY
  functional change is the Tier-1 min slice:
  `let minsl1:i32=en/8; if(minsl1>4){ minsl1=4; }`
  replacing the fixed `if(r1c>=4){ if(r0c>=4){`; all other diff lines
  are comments.
- F-CASE string audit re-run on added/modified lines
  (Y4/Y5/y4/y5/710202/fam8/F-PARCOND/710101-710299): zero matches.
- Built with the pinned znc
  (/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc,
  version 2026.07.0-dev). Compiler warnings only (E0101/A0102 notes),
  no errors.
- The uncommitted /tmp debug build was not used at any stage. No file
  from /tmp entered the build or any run.

## Bar-by-bar comparison

Committed values from RESULT_CONDITIONAL_THRESHOLD.md at d0d296650;
reproduced values from this worker's independent rebuild and nine runs.

| Bar | Committed (d0d296650) | Reproduced | Match |
|---|---|---|---|
| K3 R3 md5 (3/3) | 12f93b593d65bb986e5e23ad9df33d3d | 12f93b593d65bb986e5e23ad9df33d3d | yes |
| K3 R1 md5 (3/3) | cc0300294803ee8ee8d684ced90d6aad | cc0300294803ee8ee8d684ced90d6aad | yes |
| K3 FREC md5 (3/3) | bde90e4686883846724d56b4ebd9c81f | bde90e4686883846724d56b4ebd9c81f | yes |
| K3 .err files | all nine zero bytes | all nine zero bytes | yes |
| K3 pure Zag | zero Python | zero Python (git, znc, shell only) | yes |
| P1'' CONDHIT round <= 2 | round=0 | round=0 | yes |
| P2'' A2-PASS == 1 | 1; REUSE_IV 5 true=64/64 HAS_D=1; SCRATCH_IV 24 true=52/64 | identical lines | yes |
| P3'' DROUND < 4 | 1 | 1 | yes |
| P4''(a) A1-PASS == 1 | 1 | 1 | yes |
| P4''(b) R1 PASS_SEEDS >= 0/5 | 1/5; seed 84044 64/64 | 1/5; seed 84044 64/64 | yes |
| P4''(c) FREC I1 >= 46/64 | 48/64 | 48/64 | yes |
| P4''(c) FREC I2 >= 63/64 | 63/64 | 63/64 | yes |
| P4''(c) FREC I3 >= 40/64 | 40/64 (S33) | 40/64 (S33) | yes |
| F-CASE nine audits | none fire | none fire (string audit re-run: zero matches) | yes |

Full-file cmp of each battery's run-1 output against the committed
THR_R3_1.txt / THR_R1_1.txt / THR_FRC_1.txt: BYTE-IDENTICAL.

## Kill bars

- R1 (rebuild from committed source only; no /tmp debug build, no prior
  binaries; source commits documented): PASS.
- R2 (every committed number reproduces exactly; discrepancies
  documented): PASS. Zero discrepancies.
- R3 (pure Zag, zero Python, no em dashes): PASS.
- R4 (/tmp debug build not used at any stage): PASS.

## Honest scope

Bounded-L2 independent reproduction only. No L3 claim, no Criterion 0
claim, no pipeline promotion, no SURVIVES claim. The verdict is
THRESHOLD-REPRO-PASS, a reproduction verdict only.

## Files

- REPRO_PREREG.md (frozen prereg, 955106ae5)
- REPRO_R3_1/2/3.txt, REPRO_R1_1/2/3.txt, REPRO_FRC_1/2/3.txt
  (raw outputs; byte-identical to committed THR outputs)
- REPRO_R3_1/2/3.err, REPRO_R1_1/2/3.err, REPRO_FRC_1/2/3.err
  (all zero bytes)
- RESULT_THRESHOLD_REPRO.md (this file)

THRESHOLD-REPRO-PASS.
