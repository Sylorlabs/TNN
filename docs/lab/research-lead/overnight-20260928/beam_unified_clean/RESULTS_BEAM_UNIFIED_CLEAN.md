# Unified Beam Clean Rebuild: Results

Date: 2026-09-30
Prereg: commit d074eda3d (frozen before implementation)
Verdict: BEAM-UNIFIED-FAIL

## Falsifiers fired

- F-FIT: 0 of 5 R1 seeds reach EVFIT=32/32. Best EVFIT is 31/32
  (seeds 81113, 82090, 83067, 84044); seed 85021 reaches 29/32.
  Frozen R1 bar requires 4 of 5 at 32/32.
- F-DIVERSE-FAIL: R3 Arm 2 A2-PASS=0 (requires 64/64 true accuracy
  AND reuse_iv*2 <= scratch_iv AND HAS_D=1). Observed: REUSE_IV 24,
  true=52/64, HAS_D=1; SCRATCH_IV 24, true=45/64.
- F-NODOM: NODOMV > 0 in driver invocations across all three
  batteries. R1U: 636, 700, 565, 688, 1550 per seed. R3U: 0
  (A1-REUSE), 1088 (A1-SCRATCH), 833 (A2-REUSE), 841 (A2-SCRATCH).
  FRECU: 354 to 1322 per instance (all 15 > 0). The violations arise
  in exploration rounds (0-15) where the U5 ordering ignores opc for
  ranking but F-NODOM counts equal-accuracy lower-opc prunings as
  violations per the frozen definition.
- F-BLOAT: R1 seed 85021 MAXSIMS=1328 exceeds CEIL=1219
  ((1109*110)/100). FREC instance P1-I1-S44 MAXSIMS=1273 exceeds
  CEIL=1243 ((1130*110)/100). R3 max MAXSIMS=1246 is under
  CEIL=1263; no R3 bloat.

## Falsifiers not fired

- F-TIE-HONEST: no TIE=DEFECT appears. All five R1 seeds emit
  TIECHECK=OK. Four seeds report TIE=UNDERDETERMINED with N and
  OPCRANGE; one seed (84044) reports TIE=UNIQUE.
- F-REGRESS: R3 Arm 1 A1-PASS=1, unchanged from frozen. REUSE_IV 0,
  true=64/64; SCRATCH_IV 24, true=54/64.
- F-CASE: audit of new machinery (u_depth_fill, u_hist, u_popcnt,
  u_better, beam_extend_u, select_iv_u, tie_report) finds no
  reference to fam, sealed, dlo, dhi, lib, or has_d. All species and
  ranking logic is generic.

## Determinism (K3)

- r1u: 3/3 byte-identical, md5 89cb21e6359bafaf3d02d34575d3bd0a,
  zero stderr bytes.
- r3u: 3/3 byte-identical, md5 6a8568a7232de691606e09712df0f17d,
  zero stderr bytes.
- frecu: 3/3 byte-identical, md5 95b87706c9763e22e075a5b11fc79f38,
  zero stderr bytes.
- Zero Python invoked at any stage. Shell tools only for
  verification (md5sum, grep, wc, git, diff).

## Measurements

R1U per seed (EVFIT/32, TACC/64, OPC, tie, MAXSIMS, NODOMV):
- 81113: 31, 56, 3, UNDERDETERMINED N=8 OPCRANGE=3-1133, 1215, 636
- 82090: 31, 60, 7, UNDERDETERMINED N=4 OPCRANGE=7-175, 1045, 700
- 83067: 31, 55, 198, UNDERDETERMINED N=2 OPCRANGE=198-202, 1143, 565
- 84044: 31, 60, 20, UNIQUE, 1140, 688
- 85021: 29, 49, 87, UNDERDETERMINED N=4 OPCRANGE=87-1664, 1328, 1550

R3U per tag (hit_iv, final_true/64, MAXSIMS, NODOMV):
- A1-REUSE: 0, 64, 79, 0
- A1-SCRATCH: 24, 54, 1246, 1088
- A2-REUSE: 24, 52, 1079, 833
- A2-SCRATCH: 24, 45, 1099, 841

FRECU per tag (MAXSIMS, NODOMV), all 15 instances ran:
- P1-I1: (1162,830) (1179,793) (1152,632) (1273,852) (1040,719)
- P1-I2: (1128,665) (1188,354) (1100,624) (1197,889) (1151,1063)
- P1-I3: (1163,1322) (1165,889) (1103,898) (1130,794) (1208,921)

## Implementation notes

- beam_extend_u replaces beam_extend in all three files. Candidate
  generation (beam members, NOTs, pairwise AND/OR/XOR, sigtab dedup)
  is verbatim of the frozen code; only retention changes.
- U1/U2: species = (tree depth, operator histogram). Depth via
  single increasing node-id pass. Histogram via iterative DFS with
  visit tokens. Max 8 species; merge two smallest by (count asc,
  best accuracy asc) until 8 remain.
- U3: round numbering as preregistered. Exploration 0-15 ranks by
  accuracy only; consolidation 16-24 adds opc ascending.
- U4: select_iv_u takes first beam member per distinct species
  (up to 8); disagreement d = H - abs(2*c1 - H); lowest x wins ties.
  r1u keeps select_iv_rand per frozen policy.
- U5: tie order accuracy desc, opc asc (consolidation only),
  disagreement desc, novelty desc, node id desc.
- U6: 4 slots reserved for structural novelty (accuracy at least
  50%); integer novelty comparison; fallback to U5 ordering if
  fewer than 4 qualify.
- U7: tie_report replaces taxoff_unique. Emits TIE=UNIQUE,
  TIE=UNDERDETERMINED N=<N> OPCRANGE=<min>-<max>, or TIE=DEFECT
  (duplicate-node canary only). Independent recount emits
  TIECHECK=OK or TIECHECK=FAIL.

## Scope

Honest scope per prereg: a PASS would have been bounded-L2 search
robustness for compositional reuse and evidence fitting. Not L3,
not Criterion 0, not a Q4 revival. This build FAILS on F-FIT,
F-DIVERSE-FAIL, F-NODOM, and F-BLOAT.
