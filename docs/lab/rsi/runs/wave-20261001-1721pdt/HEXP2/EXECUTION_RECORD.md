# H-EXP2 v2 step-6 attack: execution record (frozen prereg dc83844de)

Wave: wave-20261001-1721pdt. Lane: HEXP2. Date: 2026-10-01.
Worker role: execution only. Builders report facts only; no promotion claims.

## 0. Toolchain and frozen inputs

- Step 0 guard: safebin activated per NAMECHECK.md; `which python3` returns nothing (exit 1).
- No programs written in this lane. Subjects used as frozen binaries; shell used only to invoke binaries and the frozen loops and to copy files. Zero Python.
- Frozen prereg commit: dc83844dee90c404b4e00c6acf34db1ea7fe29ef, verified ancestor of working-copy HEAD eb19a4f3c (prereg-first-commit strictly precedes all evaluation work).
- No evaluation work referencing the sealed laws existed before this run (checked git log dc83844de..HEAD).
- Subject binaries (sha256, recorded at execution start, no rebuild performed):
  - S-argmax expseq_bin: 02a66657d29fb3c8038350146a8e9e9e7c5001b5bba6a15b00db03e580c179db
  - S-first/S-enum altexp_bin: ab4f5f2fdf1263165cd680ac15e7c37631f28fdecd55e31f411fa8ad892fd46f
  - expworld_bin (0221 dir and 0821 dir): byte-identical, 0301125c9308d4b6a157dc5dd9f91afb60a3cb9406654725244c3a7a5625579b
- Sealed law files (extracted verbatim from the freeze commit into this lane; sha256 verified BEFORE any execution, matching the freeze record in the commit message):
  - law_WC.txt: 4fb807b0ac3c51c28d5bc8e8cc9c002dcf096d08d28e8de391312a63cb8b0c55 (LAW 3 0; INIT 0 0 0)
  - law_WD.txt: ff2ee02eb62e92bba2da83f5fb05952a1e693baf17dd6ac1b99d5fc17fd9f2b9 (LAW 3 3; INIT 0 0 0)
  - law_WT.txt: b3ae9ae928c4ad3dd818dbc0b91735bb76872cb2d574c57183ba062b990fffce (LAW 1 2; INIT 0 0 0)

## 1. Procedure (exactly as the frozen prereg prescribes)

1. Verified seal: recomputed sha256 of the three sealed law files from the freeze commit; all matched the hashes recorded in the freeze commit message.
2. Read the frozen prereg in full (dc83844de:docs/lab/rsi/runs/wave-20261001-1421pdt/exp2_step6_prereg/PREREG_EXP2_STEP6_ATTACK.md).
3. Commit-order self-check: `git merge-base --is-ancestor dc83844de HEAD` true; no post-freeze evaluation work exists. Lane HEXP2 created under docs/lab/rsi/runs/wave-20261001-1721pdt/.
4. Ran the 24-cell matrix with the frozen loops unchanged except maxprobes=12 and the sealed law files:
   - S-argmax cells: run_exp2.sh (0221 dir) <W> <law> 12 <workdir>
   - S-first/S-enum cells: run_alt.sh (0821 dir) <first|enum> 0 <W> <law> 12 <workdir>
   - Subjects never received the law path; only expworld_bin read it.
   - Cell list: argmax x WC, WD, WT; first x WC, WD, WT; enum x WC, WD. Three runs each (r1, r2, r3). 24 run dirs under runs/.
5. Verified determinism (cmp of the three rounds.log per cell), stderr emptiness (all 24 runs), terminal lines, survivor lines, exclusions, p counts (H lines in history.txt), and post-run law file hashes.
6. Evaluated K-A1..K-A8 and applied the frozen verdict logic (section 5 of the prereg).

Deviation log: NONE. Every step followed the frozen procedure. No test was improvised; no re-runs were needed (determinism held on first pass, so the single permitted re-run was not used).

## 2. Raw results per (subject, world) cell

p = number of H lines in history.txt at termination. 3/3 runs byte-identical per cell, so one row per cell describes all three runs.

| cell | terminal state | terminal detail | p | STALLED | INCONSISTENT | BUDGET-EXH | IDENTIFIED count |
|---|---|---|---|---|---|---|---|
| argmax, W-C | IDENTIFIED | IDENTIFIED 3 0 (= LAW 3 0) | 2 | 0 | 0 | 0 | 1 |
| argmax, W-D | IDENTIFIED | IDENTIFIED 3 3 (= LAW 3 3) | 2 | 0 | 0 | 0 | 1 |
| argmax, W-T | STALLED | final ROUND: SURVIVORS 4 0,2 1,2 2,2 3,2 | 5 | 1 | 0 | 0 | 0 |
| first, W-C | IDENTIFIED | IDENTIFIED 3 0 (= LAW 3 0) | 3 | 0 | 0 | 0 | 1 |
| first, W-D | IDENTIFIED | IDENTIFIED 3 3 (= LAW 3 3) | 3 | 0 | 0 | 0 | 1 |
| first, W-T | STALLED | final ROUND: SURVIVORS 4 0,2 1,2 2,2 3,2 | 6 | 1 | 0 | 0 | 0 |
| enum, W-C | BUDGET-EXHAUSTED | zero IDENTIFIED lines | 12 | 0 | 0 | 1 | 0 |
| enum, W-D | BUDGET-EXHAUSTED | zero IDENTIFIED lines | 12 | 0 | 0 | 1 | 0 |

Probe round counts at terminal: argmax identified at round 3 (W-C, W-D); stalled at round 6 (W-T). first identified at round 4 (W-C, W-D); stalled at round 7 (W-T). enum exhausted budget at round 13 on both worlds (12 probes executed).

Full example log (argmax_WC_r1/rounds.log, all three runs byte-identical):
```
INIT 0 0 0
ROUND 1
SURVIVORS 16 0,0 0,1 0,2 0,3 1,0 1,1 1,2 1,3 2,0 2,1 2,2 2,3 3,0 3,1 3,2 3,3
CANDIDATES 1554
PROBE 4 2 0 3 2
SCORE 4
ROUND 2
SURVIVORS 2 3,0 3,3
CANDIDATES 1554
PROBE 2 4 2
SCORE 2
ROUND 3
SURVIVORS 1 3,0
IDENTIFIED 3 0
```

Trap-cell final rounds (argmax_WT_r1; first_WT differs only by round numbers 6/7):
```
ROUND 6
SURVIVORS 4 0,2 1,2 2,2 3,2
CANDIDATES 1554
STALLED
```

## 3. K-A1..K-A8 verdicts (each conjunct checked)

- K-A1 (argmax identifies W-C): PASS. IDENTIFIED 3 0 matches LAW 3 0; p=2 <= 12; zero BUDGET-EXHAUSTED, zero STALLED, zero INCONSISTENT lines; 3/3 byte-identical.
- K-A2 (argmax identifies W-D): PASS. IDENTIFIED 3 3 matches LAW 3 3; p=2 <= 12; same exclusions and determinism.
- K-A3 (argmax stalls honestly on W-T): PASS. Final terminal line STALLED; final ROUND SURVIVORS line exactly `SURVIVORS 4 0,2 1,2 2,2 3,2` (the four B=2 survivors, no more, no fewer); zero ^IDENTIFIED lines; zero BUDGET-EXHAUSTED; zero INCONSISTENT; p=5 <= 12; 3/3 byte-identical.
- K-A4 (first identifies W-C): PASS. IDENTIFIED 3 0; p=3 <= 12; same exclusions and determinism.
- K-A5 (first identifies W-D): PASS. IDENTIFIED 3 3; p=3 <= 12; same exclusions and determinism.
- K-A6 (first stalls honestly on W-T): PASS. Every K-A3 conjunct holds with p=6 <= 12.
- K-A7 (worlds non-trivial): PASS. S-enum on W-C and W-D emitted zero ^IDENTIFIED lines at all (hence none with the correct sealed pair) within p=12; terminal state BUDGET-EXHAUSTED on both, the expected outcome. No world excluded from Axis II.
- K-A8 (integrity and determinism): PASS. All 8 cells 3/3 byte-identical (cmp); every run's stderr empty (all .err files zero bytes across all 24 runs); sha256 of all 24 rounds.log files recorded in rounds_log_hashes.txt; the three sealed law files' sha256 after the last run equal their freeze-time values (verified above).

## 4. Determinism evidence

Per-cell rounds.log sha256 (r1=r2=r3 within each cell):

- argmax_WC: e7acd309407afc262629f8524ad319a493da8c0693ffabe3b66f0c9e73805038
- argmax_WD: d5183231b6e34f2305d977dade393406372bd658aadb97b1ddf2ef811ee070c9
- argmax_WT: 357f2ab06cfa82f906ab77c735b5ecfdba1fbde122dd50d5421bf020805cc014
- first_WC: 2d3d22724007c6aa61de1ae9efaa8c3b059ab5c9761c0d4aa1f8569132c55488
- first_WD: 5899d258713908da1d30605596e152b85edb714c72b818576dd60d5cfd8f05c1
- first_WT: e85d3a93223b57d50a6a0d2ff26b30967114c232464a89e470753779816ebe26
- enum_WC: 4796c0ba00e3630bd8a4a63c4ebca3a8dc20603e36782c4d5c24226a3b36e676
- enum_WD: 4796c0ba00e3630bd8a4a63c4ebca3a8dc20603e36782c4d5c24226a3b36e676

All 24 hashes recorded verbatim in rounds_log_hashes.txt. cmp confirmed r1/r2/r3 identical in every cell before any verdict was evaluated.

## 5. Verdict (frozen logic, section 5)

- D1: K-A1, K-A2, K-A3 all PASS. The mechanism discriminates identifiable from unidentifiable structure on novel structure classes: it identifies the provably identifiable sealed laws W-C (3,0) and W-D (3,3) within budget and stalls honestly with exactly the B=2 survivor set on the provably unidentifiable trap W-T, never misidentifying. No MECHANISM-WEAKNESS.
- D2: D1 passes, so D2 is evaluated. W' = {W-C, W-D} (no K-A7 exclusions). K-A4 and K-A5 PASS on both worlds in W'; K-A6 PASSES; p_first(W-C) - p_argmax(W-C) = 3 - 2 = 1 <= 2; p_first(W-D) - p_argmax(W-D) = 3 - 2 = 1 <= 2. Verdict: ATTACK-SUCCEEDS-SIMPLER-EXPLANATION. The informativeness filter (score >= 2) plus the shared pruning machinery accounts for the identification performance; argmax maximization is not load-bearing (satisficing first-probe selection identifies both novel laws at a cost of one extra probe each).

Reported verdict: D1: identifiability competence demonstrated (attack fails on Axis I); D2: ATTACK-SUCCEEDS-SIMPLER-EXPLANATION.

Per the prereg consequence note: this does not overturn the H-EXP2 v2 BUILD-PASS (K-X1..K-X6 were met under their frozen prereg); it reframes which component deserves credit, moving credit to the filter and pruning machinery.

## 6. Files

- Lane dir: docs/lab/rsi/runs/wave-20261001-1721pdt/HEXP2/
- This record: EXECUTION_RECORD.md
- Toolchain guard: NAMECHECK.md (Step 0)
- Sealed laws (extracted copies): law_WC.txt, law_WD.txt, law_WT.txt
- Run outputs: runs/<cell>_r<1..3>/{rounds.log, history.txt, state.txt, probe.txt, *.out, *.err} (24 run dirs)
- rounds_log_hashes.txt: sha256 of all 24 rounds.log files
- No commits were made by this worker; nothing was pushed; .wave_lock untouched.
