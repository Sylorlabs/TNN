# RUNLOG — Experiment (c): honest (g)-predicate calibration (R0 vs R1)

**Prereg:** `PREREG_CEILING_TEST.md` §4 (commit `98080233c11a492916c4c54530c24b5fc66a9c4d`).
**Date:** 2026-09-23. **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Derivation (glue): augmented case file
`gen_ext.py` (Python, glue only): `case_r24_rk3_ext.txt` = frozen
`case_r24_rk3.txt` rows + `|t1|agree|strong` per seq from frozen `sweep.jsonl`
(`4163fffa…`). 11,840 rows.
**SHA-256:** `65deca5c13159a3aaeea584c0bba4068bb49ce8eef0764225000957cb34bb42b`.

## Instrument (pure Zag, additive)
`grevise.zag` (this dir): reads the augmented file; argv[1] selects R0
(identity) or R1 (revised prog=PASS iff `t1==1 && agree==1`; pred=1 iff
revised prog==PASS); replays the H2 gate with the verbatim `gate_step` logic
of frozen `diagnose.zag`; emits `GREV` metric lines. Zero RNG.
Build: `znc grevise.zag` → `grevise` (70,154 bytes). Analyzer warnings only.

## Runs (3× per candidate)
`./grevise case_r24_rk3_ext.txt R0 > r0_N.txt`; `./grevise case_r24_rk3_ext.txt R1 > r1_N.txt`.

| Candidate | Runs | Exit | stdout SHA-256 (×3 identical) |
|-----------|------|------|-------------------------------|
| R0 | 3 | 0 | `4a5d32ce5d4e8b6eccbefca792260389ca00b050d7574cc77229a6fc47e07934` |
| R1 | 3 | 0 | `cd972af6ae38c456554a85f528d844094e6375a3f895e68d95d8e41aca4a2905` |

**Byte-identical ×3 per candidate: YES.**

## R0 control (must reproduce frozen headlines)
```
GREV,REPLAY_MM,0        (0/11,840 disposition mismatches — gate fidelity)
GREV,CHC,1102
GREV,RK3,104
GREV,CEIL,824
GREV,RK1_PERM_FALSE,0
GREV,RK2_WRONGHC_PERM,0
GREV,RK5,1102,1109      (99.37%)
```
**Control: PASS** (reproduces 104 / 824 / 278 / 0 / 99.37% exactly).

## R1 (drop `strong`)
```
GREV,REPLAY_MM,0
GREV,CHC,1102
GREV,RK3,106            (+2 vs R0)
GREV,RECOVERED,2        (seq 2366, 2372 — both disp=0 PROVISIONAL_INSTALL)
GREV,CEIL,954           (revised (g)-PASS among chc: 824+128+2)
GREV,RK1_PERM_FALSE,0
GREV,RK2_WRONGHC_PERM,0
GREV,RK5,1102,1109      (99.37%, unchanged — 0 wrong-HC flipped)
```

## Interpretation
- The 128 marginal-agree (1,1,0) correct-HC trials flip to (g)-PASS under R1
  but **0 install**: 68 hit CONFLICT_WITHHELD, 60 hit SUPPRESSED (downstream
  gate state). Verified by disposition audit.
- The 2 "recovered" (seq 2366/2372) are the deliberation-downgraded trials:
  R1 restores their (g)-PASS because the replay holds deliberation at frozen
  outcomes (prereg §4 limitation). They are NOT genuine (g)-predicate
  recoveries; a live pipeline would re-deliberate them (they originally
  triggered E2/BLOCK).
- Safety holds: RK-1 0, RK-2 0, RK-5 99.37% (the 260 flipped wrong trials are
  all low-confidence; none reach permanent install).
- **Recovered: 2 << 113 required.** The (g) path CANNOT reach 85%.
- Note: the revised *gate-side* ceiling is 954/1,102 = 86.6% (above 85%),
  but actual installs stall at 106 — the binding constraint is the H2 gate's
  conflict/suppression rules, not the (g) predicates.
