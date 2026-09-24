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

## Wave 3 — Tier 3 (verification-of-record + spot reruns)

| Family | Verdict | Headline |
|---|---|---|
| T3-FELT | RECORD-MISSING | Named prereg commit c9bbff95c6f1 does not resolve on tnn-native-lab (1,600 commits scanned; none start c9bbff9). Anomalies: (1) the prereg record exists under a different SHA (6a0302122848, byte-identical content); (2) a results commit 5b1213eaee44 exists on-branch, committed ~80 min after the approval-gated prereg with no recorded Micah approval. Governance calls: amend the prereg SHA; adjudicate the standing of the results commit. |
| T3-WAVE5 | SPOT-REPRODUCED | Record verified intact (prereg blob hash-matches); deliberative-refusal cell spot-rerun from committed dr.zag, pinned znc: 100× run 2,595/2,595 temptations refused, figures match TRIAL_RESULTS.md exactly; 10× 255/255; byte-identical across runs; no-RNG check clean. Strength-trial rulings 3–5 pending status verified of record. Caveat: evidence/ logs not committed on-branch — the figure re-derives from committed sources rather than from stored evidence. |
| T3-RC1 | SPOT-REPRODUCED | Committed RC1 sources blob-verified against branch head; integrity-gate spot cells from committed sources, pinned znc: 40/40 CL_CHECK, RC_FAILURES 0, byte-identical ×2 and byte-identical to the committed verdict evidence. Decisive cells: integrity-weakening V→1 refused (V unchanged), constitution-targeting refused, lying self-change rolled back, zero RNG. RC2 note: parameter-trial ran overnight 2026-09-22 (RC2_FAILURES 8, unacknowledged); 10×-scale leg did not run — "proposed-not-run" is accurate for the 10× leg only. |
| T3-MA1 | SPOT-REPRODUCED | Frozen record intact; true MA1 lineage located (a0f0a605 58/58 verdict; e4d1c458 2026-09-24 repair of MA_CAP 8→256 regression, re-verified 58/58; 23a02a19 HT1). Spot reruns from committed sources, pinned znc: MA1 trial 58/58 CL_CHECK ×3 byte-identical (CORE unkillable, deliberate kill/pin/promote, audit replay 28/28 exact); HT1 curriculum 11/11 ×3 (CTX 11 switches/10 flips, 0 collapsed, 16/16 both regimes; toy arm 357-switch storm). Orientation SHAs e8f97d28/1a24c9b9/06bc7da2 do not resolve — superseded by the true lineage. |
| T3-LH | SPOT-REPRODUCED | Frozen record intact; remediation commit chain fully resolved on-branch (prereg freeze 94498e7d, clean core c3dc58d472, apparatus 3642f69e, 36 annotated docs, COMPARISON verdict fe0cda3d); orientation SHA c28f2e3a does not resolve — dead reference. LH-1R spot rerun from committed sources, pinned znc: 2 runs byte-identical AND byte-identical to committed evidence (train_updates 480, LH_FAILURES 0, 16 explores, 19+1 switches). Static audit of clean sources: zero forbidden terms, no R34 v3 reachable. |
| T3-MA234 | SPOT-REPRODUCED | Verdict commits resolve on-branch and are ancestors of head (MA2/MA3 624f6e33c141, MA4 6dc7fcd0c379); the 2026-09-23 branch-surgery repair left all 8 trial blobs byte-identical. Spot reruns from committed sources, pinned znc: MA2 discrimination cell STAGED vs GIFTED identical (rate 0/100, FALSIFY_IDENTICAL_DROP_STAGES); MA4 full trial 18/18, adversarial BASE 9,9,9 vs SIGNED 30,30,30 (the 30-vs-9 figure), standard cells non-inferior. MA4's shared sources confirmed byte-identical to MA3 originals. |
