# EVIDENCE-CHECK: verdict evidence completeness, wave-20261001-2321pdt

Scope: the 47 verdicts listed under "Verdicts" in WAVE_RECORD.md (wave-20261001-2321pdt).
Method: for each verdict, (1) the lane directory is named from the verdict title, (2) checked that the dir exists under docs/lab/rsi/runs/wave-20261001-2321pdt/, (3) searched the dir for a JUDGE_BRIEF.md or VERDICT file (RT lanes: the RT-*_REVIEW.md review document is the verdict record).

## Result: 47/47 verdicts have evidence on disk. 0 missing lane dirs. 0 lane dirs without a judge brief or verdict record.

Notes:
- The five RT lanes (RT-EXEC, RT-INT, RT-GOV, RT-C174, RT-SENSE) do not use the name JUDGE_BRIEF.md; each has an RT-*_REVIEW.md review document that records the review verdict. Counted as verdict evidence.
- F1-REPAIR and F1-REPAIR2 also carry runs/verdict.txt files in addition to JUDGE_BRIEF.md.
- CONTLEARN, CONTLEARN-OWNED, and CONTLEARN-OWNED2 carry VERDICT_*.md files in addition to JUDGE_BRIEF.md.

## Per-verdict evidence

| # | Verdict | Lane dir | Exists | Evidence document |
|---|---------|----------|--------|-------------------|
| 1 | Fork battery: 59 refs, 0 FAIL | FORK | yes | JUDGE_BRIEF.md (3 files) |
| 2 | H-PI-REV2 narrowed single-conflict claim: BUILD-PASS | HPIREV2 | yes | JUDGE_BRIEF.md (44 files) |
| 3 | RT-EXEC: EVIDENCE-HOLDS on F1, TNN3H5R | RT-EXEC | yes | RT-EXEC_REVIEW.md (2 files) |
| 4 | TNN3-SUBSTRATE: DESIGN-COMPLETE | TNN3-SUBSTRATE | yes | JUDGE_BRIEF.md (10 files) |
| 5 | H5R2-REPRO: REPRO-PASS | H5R2-REPRO | yes | JUDGE_BRIEF.md (3 files) |
| 6 | CONSEQ: VALIDATION-PASS | CONSEQ | yes | JUDGE_BRIEF.md (4 files) |
| 7 | CONTLEARN: BUILD-PASS, LEARNOWN-DEMONSTRATED | CONTLEARN | yes | JUDGE_BRIEF.md + VERDICT_LEARNOWN.md (26 files) |
| 8 | TNN-3 H5R2: BUILD-PASS, H5R2 ADVANCES | TNN3H5R | yes | JUDGE_BRIEF.md (10 files) |
| 9 | ARENA inquiry (C8): BUILD-PASS | ARENA | yes | JUDGE_BRIEF.md (8 files) |
| 10 | F1 interleaved-error trigger: BUILD-FAIL | F1 | yes | JUDGE_BRIEF.md (8 files) |
| 11 | RT-INT: EVIDENCE-HOLDS on CONSEQ, CONTLEARN | RT-INT | yes | RT-INT_REVIEW.md (2 files) |
| 12 | RT-GOV: HOLDS on all three axes, one QUALIFY | RT-GOV | yes | RT-GOV_REVIEW.md (2 files) |
| 13 | ARENA2 transfer-by-recoding (C12): BUILD-PASS | ARENA2 | yes | JUDGE_BRIEF.md (10 files) |
| 14 | ARENA3 transfer-by-relabeling (C12): BUILD-PASS | ARENA3 | yes | JUDGE_BRIEF.md (8 files) |
| 15 | F1-FOLLOWUP: Part 1 BUILD-PASS, Part 2 NOT-FOUND | F1-FOLLOWUP | yes | JUDGE_BRIEF.md (11 files) |
| 16 | C174 shared tag-61 store: VALIDATION-PASS | C174 | yes | JUDGE_BRIEF.md (22 files) |
| 17 | BATTERY: Part 1 VALIDATED, Part 2 1/6 PASS | BATTERY | yes | JUDGE_BRIEF.md (37 files) |
| 18 | DEVANG3: BUILD-PASS | DEVANG3 | yes | JUDGE_BRIEF.md (13 files) |
| 19 | RT-C174: EVIDENCE-HOLDS, no dissent | RT-C174 | yes | RT-C174_REVIEW.md (2 files) |
| 20 | RT-HPIREV2: Part 1 QUALIFY, Part 2 bound PARTIALLY survives | RT-HPIREV2 | yes | JUDGE_BRIEF.md (46 files) |
| 21 | BATTERY-CLUSTER: COMPLETE | BATTERY-CLUSTER | yes | JUDGE_BRIEF.md (3 files) |
| 22 | H5R2-BASELINE: BASELINE-MATCHES via REVERT-TO-LATEST | H5R2-BASELINE | yes | JUDGE_BRIEF.md (12 files) |
| 23 | C9BAT: GEN-PASS | C9BAT | yes | JUDGE_BRIEF.md (13 files) |
| 24 | RT-SENSE (DEVANG3): QUALIFY | RT-SENSE | yes | RT-SENSE_REVIEW.md (2 files) |
| 25 | F1-BUFFER: BUFFER-NOT-PREDICTIVE | F1-BUFFER | yes | JUDGE_BRIEF.md (7 files) |
| 26 | ARENA4 (C15 audit + ROSTER build): BUILD-PASS | ARENA4 | yes | JUDGE_BRIEF.md (9 files) |
| 27 | BATTERY-E2: E2-CONTENT-BLIND | BATTERY-E2 | yes | JUDGE_BRIEF.md (9 files) |
| 28 | H7R: BUILD-PASS | H7R | yes | JUDGE_BRIEF.md (13 files) |
| 29 | BATTERY-E1: E1-FIRSTCLASS | BATTERY-E1 | yes | JUDGE_BRIEF.md (17 files) |
| 30 | H5R2-DECOY: DECOY-DISCRIMINATES | H5R2-DECOY | yes | JUDGE_BRIEF.md (7 files) |
| 31 | F1-REPAIR: GREEDY-CONFIRMED | F1-REPAIR | yes | JUDGE_BRIEF.md + runs4/verdict.txt (7 files) |
| 32 | BATTERY-E3: E3-ORACLE-DEPENDENT | BATTERY-E3 | yes | JUDGE_BRIEF.md (19 files) |
| 33 | F2V3 (F2 v4 depth-9): BUILD-PASS | F2V3 | yes | JUDGE_BRIEF.md (10 files) |
| 34 | BATTERY-E6: E6-CONTENT-READ, H2C-STICKY | BATTERY-E6 | yes | JUDGE_BRIEF.md (13 files) |
| 35 | H6R: BUILD-FAIL | H6R | yes | JUDGE_BRIEF.md (12 files) |
| 36 | BATTERY-E4: E4-PRECEDENCE | BATTERY-E4 | yes | JUDGE_BRIEF.md (17 files) |
| 37 | ARENA5 (DEFRECALL): BUILD-PASS | ARENA5 | yes | JUDGE_BRIEF.md (11 files) |
| 38 | F1-REPAIR2: REPAIR2-CONFIRMED | F1-REPAIR2 | yes | JUDGE_BRIEF.md + runs5/verdict.txt (7 files) |
| 39 | BATTERY-E5: E5-INSTANCE-ONLY | BATTERY-E5 | yes | JUDGE_BRIEF.md (21 files) |
| 40 | ARENA-BLIND (E3-mandated ROSTER audit): ORACLE-FREE | ARENA-BLIND | yes | JUDGE_BRIEF.md (4 files) |
| 41 | H5R2-SKEPTIC2: SKEPTIC-SURVIVES | H5R2-SKEPTIC2 | yes | JUDGE_BRIEF.md (8 files) |
| 42 | BATTERY-E8: E8-BANDWIDTH | BATTERY-E8 | yes | JUDGE_BRIEF.md (9 files) |
| 43 | RT-ARENA5: QUALIFY (BUILD-PASS stands) | RT-ARENA5 | yes | RT-ARENA5_REVIEW.md (2 files) |
| 44 | CONTLEARN-OWNED: MACHINERY-DEPENDENT | CONTLEARN-OWNED | yes | JUDGE_BRIEF.md + VERDICT_OWNED.md (30 files) |
| 45 | ARENA-GEN: NARROW | ARENA-GEN | yes | JUDGE_BRIEF.md (6 files) |
| 46 | CONTLEARN-OWNED2: MACHINERY-DEPENDENT | CONTLEARN-OWNED2 | yes | JUDGE_BRIEF.md + VERDICT_OWNED2.md (44 files) |
| 47 | H5R2-SKEPTIC3: SEPARATED | H5R2-SKEPTIC3 | yes | JUDGE_BRIEF.md (7 files) |

## Missing lane dirs

None.

## Lane dirs without judge brief or verdict record

None. (RT lanes use RT-*_REVIEW.md as the verdict record; see note above.)

No em-dashes are used in this document.
