# Cross-reference verdict table — Wave 2 (Tier 2 families)

Frozen: 2026-09-23. 28/28 families resolved: 26 REPRODUCED, 2 PARTIAL.
Full reports: `runs/wave2/crews/<FAMILY>/{VERDICT.md,RUNLOG.md}`; full tally: `runs/wave2/VERDICTS.md`.

| Family | Verdict | Headline |
|---|---|---|
| T2-WEBV2 |  | REPRODUCED |
| T2-RAWVSHUMAN |  | REPRODUCED |
| T2-RSI1 |  | REPRODUCED |
| T2-BUGREAD |  | REPRODUCED |
| T2-JOKE |  | REPRODUCED (frozen PARTIAL stands) |
| T2-PROSE |  | REPRODUCED |
| T2-TRACKR0 |  | REPRODUCED |
| T2-DUEL |  | REPRODUCED (SCENARIO-FIT, no champion) |
| T2-HELLHOLE |  | REPRODUCED |
| T2-DIALOGUE |  | REPRODUCED |
| T2-SELFTEST |  | REPRODUCED |
| T2-INFORICH |  | REPRODUCED |
| T2-SCALEDOWN |  | REPRODUCED |
| T2-TQ |  | REPRODUCED |
| T2-IMAG |  | REPRODUCED |
| T2-TRACKB |  | PARTIAL (16th verdict; first non-REPRODUCED in Wave 2) |
| T2-PARAMS |  | REPRODUCED (17th verdict) |
| T2-AUDIOCONT |  | REPRODUCED (18th verdict) |
| T2-CERT |  | REPRODUCED (19th verdict) |
| T2-SENSESINT |  | PROVISIONAL PARTIAL (stood-down crew's finding; crew of record 247aa7b5 still adjudicating) |
| T2-HTD1 |  | REPRODUCED (20th verdict) |
| T2-CLASS3DEC |  | REPRODUCED (22nd verdict) |
| T2-GOALB |  | REPRODUCED (23rd verdict) |
| T2-TRACKA |  | REPRODUCED (24th verdict) |
| T2-SPEEDINTEL |  | REPRODUCED (25th verdict) |
| T2-CHAMP |  | REPRODUCED (26th verdict) |
| T2-PROSEV3 |  | REPRODUCED (27th verdict) |
| T2-SENSESH2H |  | REPRODUCED (28th verdict — WAVE 2 COMPLETE) |

## Notes
- T2-TRACKB: PARTIAL solely from the frozen rule's named condition (arm-3 identity ambiguity across three PASS variants); parked as governance call #1 for Micah. Nothing failed.
- T2-SENSESINT: PARTIAL — real evidence gap: 10/140 manifest evidence paths absent from the frozen commit (incl. the 3 P0 GK trial sources gk1/gk2/gk3_trial.zag), 2 manifest size mismatches.
- T2-JOKE: REPRODUCED with the frozen PARTIAL standing (arm-specific K1 kill-bar trip).
- T2-DUEL: REPRODUCED as SCENARIO-FIT, no overall champion.
- This table covers Wave 2 only. Earlier waves (R1–R5) are recorded in the scratch-crossref workspace; later waves append here.

## Wave 2 — heavy families (dispatched after the main batch)

| Family | Verdict | Headline |
|---|---|---|
| T2-SCALE | REPRODUCED | Scale-up anchor (N=240) + mid-scale (N=240,000) exact: mastery 1.0000, 96/96 flaw battery, 4.000 ops / 92 B per fact, 3/3 byte-identical reruns; mid-scale log byte-identical to committed s3_r0.log (sha256 17d5ee80…0fdb656). 6.58M ceiling sweep NOT re-run (Type B honest limit). |
| T2-THROUGHPUT | PARTIAL | Contention-robust anchors held: install 5.93–6.41 µs/fact (±10% of 6.2), 4 ops / 92 B exact, determinism byte-identical ×3. Wall-clock anchors (recall, deliberation, emission) fell outside bands under VM load 18–35 vs original crew's 8–13; O(1) ordering holds. Named gap: quiet-VM rerun of wall-clock anchors at original-comparable load — pending. |
| T2-SPEECHACT | REPRODUCED | PoC 7.1%→50.0% exact; volume ladder peak-and-decline reproduced (76% peak @2) and count-rule flip to monotone corrected curve 5→8→21→24→30→32→38; transfer degeneracy confirmed; implicature fixes killed as before; WHY_SARCASM H3/H4/H5 survive, H1/H2 killed. 180/180 + 330/330 cells byte-identical to committed; ≥3 identical reps per cell. |
| T2-LHADV | REPRODUCED | Full 54-stage battery: 3/3 byte-identical runs, ledger byte-identical to committed; 52/54 accepted with the same 2 honest halts (D9 UNRECOVERABLE, F1 KB-MISS); ADV-DS 47/47, ADV-REC 6/6+5/5, ADV-HH 54/54, ADV-CRIT 51/51, ADV-DIAG correct, 0 fabrication; ADV-RET 10/10, ADV-DET 5/5×5. |
| T2-REMATCH | REPRODUCED | All four budgets (T1–T4) rerun, caches byte-identical: B never crosses A (−20.0 to −27.8pp), B never reaches 60% (max 56.6%), KB6 confirmed=false ("B STAYS DEAD"), KB5 determinism digest 100b19f4… matches on 3 fresh reruns; compare_results ALL MATCH T0–T4. Survived 6 VM reboots via resumable pipeline. |
