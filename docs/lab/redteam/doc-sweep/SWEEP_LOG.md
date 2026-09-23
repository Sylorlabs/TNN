# DOC-SWEEP LOG — bar-audit tripwire remediation

**Date:** 2026-09-22 · **Coordinator:** DOC-SWEEP crew · **Bar-audit:** commit `abaa5c7b57b6`
**Order:** Micah — fix the tripwires and sweep every document making claims backed by them.
**Policy:** ANNOTATE / RESTATE / RETRACT. No measured values or evidence deleted — only claims
qualified or restated. Every correction carries a dated
`> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):**` note adjacent to the claim.
All proposed replacement bars are cited as **pending Micah's signature** — nothing treated as frozen law.

## Summary counts

| Document | Annotate | Restate | Retract | Claims touched |
|---|---|---|---|---|
| self-test/SELFTEST_VERDICT.md | 4 | 1 | 0 | 5 |
| scale/VERDICT.md | 5 | 0 | 0 | 5 |
| scale/params/PARAM_VERDICT.md | 1 | 3 | 0 | 4 |
| scale/fewshot/VERDICT.md | 0 | 1 (14 cells + header) | 0 | 1 group |
| info-source/VERDICT.md | 5 | 1 | 0 | 6 |
| principle-detection/VERDICT.md | 0 | 5 | 0 | 5 |
| q1n-noisy-teacher/Q1N_NOISY10_VERDICT.md | 0 | 1 | 0 | 1 |
| tq-noisy25/TQ_NOISY25_VERDICT.md | 1 | 4 | 0 | 5 |
| q1tq-noisy50/Q1TQ_NOISY50_VERDICT.md | 1 | 3 | 0 | 4 |
| prose-learning/v2/VERDICT.md | 3 | 2 | 1 | 6 |
| prose-learning/v3/VERDICT.md | 3 | 1 | 0 | 4 |
| prose-learning/VERDICT.md (v1) | 2 | 1 | 0 | 3 |
| coding/CODING_REPORT.md | 2 | 3 | 0 | 5 |
| dialogue/VERDICT.md | 2 | 0 | 0 | 2 |
| docs/lab/FINDINGS_2026-09-21.md (front) | 3 | 0 | 0 | 3 |
| TNN_VS_LLM_CAPABILITY_DRAFT.md (front) | 3 | 0 | 0 | 3 |
| docs/lab/redteam/battery-design/BLIND_SPOT_MAP.md (mirror) | 1 | 0 | 0 | 1 |
| **TOTAL** | **36** | **25** | **1** | **62 claim groups** |

## Headline changes (what Micah was told vs what the docs now say)

1. **H7 coding KB-C2 → FAIL under the frozen rule.** The report's T3-only "PASS (loop essential)"
   framing was a narrowing without amendment. Frozen T3+T4: A=22, B=12, 2×B=24 > 22 → FAIL.
   (Micah was already told FAIL verbally on 2026-09-21; the document now matches.)
2. **H1 principle-detection: Arch B → HONEST-FAIL.** It installed the planted lie on F45
   ("cobra produces milk"); the "design choice" framing is struck. The YES verdict is scoped to Arch A.
3. **H3 fewshot: the `96/96*` presentation is gone.** Honest distinct-id denominators throughout
   (24/24 down to `1/1 existence proof`); only N≥96 rows qualify as floor results.
4. **H2 params: reduced-capacity flaw cells marked `96/96 †DEGRADED`** — the battery samples
   ids in [0, n/4) only, blind to capacity loss beyond 4×.
5. **H4 noisy-teacher ×3: headlines now carry the mastery-collapse triple** (absorbed/filtered/
   untaught) and world-true mastery vs control (−9.9/−25.5/−51.6pp), with the retroactive N2 TRIP.
   §B.7 PASSes are scoped to proposal form and labeled proposed-never-frozen.
6. **H8 prose-v3: the "C4 carried the recovery" headline now carries the precision price**
   (tier-3 wrong-value 8→30/912, 0.9%→3.29%, unbarred).
7. **Gap-13 prose-v2: falsehood headline restated under frozen ABS-3** — v2 installs 9–11/12
   lies as asserted vs v1's 12/12 (the "far fewer (0–4/12)" probe-metric headline is corrected).
8. **Front docs:** scale-up "no degradation" rows qualified with T2/T3 infinite slack;
   "spoof resistance 6/6" scoped to the single-domain leg with the unanimous-spoof residual
   called out; params "gracefully" qualified with the H2 coverage artifact.

## Tripwire fixes applied

- **T1** (self-test overhead 157×): "lean enough to scale" / "cheap" claims annotated; proposed ≤0.10 pending.
- **T2/T3** (scale mastery-drop / forget-gap ∞): "no degradation" / "zero forgetting" claims annotated
  with the 125,137-wrong-fact / 187,700-forgotten-fact tolerances; proposed >0.25pp / >0.5pp pending.
- **T4** (info-source spoof-residual unfailable): relabeled from passed kill bar to documentation
  requirement; proposed 30-day follow-on gate pending.
- **Wrong-target §B.7** (noisy-teacher): all PASS claims scoped to proposal form; "the bar"
  corrected to "the proposed (never-frozen) bar" everywhere.

## Cross-check results

- Crews A/B/C/D each sanity-checked every other bar in their documents: **no additional >10×-slack
  tripwire** the audit missed. One audit-missed zero-margin pair documented (info-source KB-CATCH /
  KB-CONTEST — zero-margin by construction, annotated, not a tripwire).
- Crew D found one new >10×-slack-class flag the audit missed: the web-search v2 M5–M6
  unanimous-spoof residual is unfailable by construction (same pathology as T4). The v2 verdict
  already documents it as a residual (not a passed bar) and KB-MODE-RW's PASS is explicitly
  A1-scoped to exclude it — reviewed, no doc change warranted; the front-doc "spoof resistance 6/6"
  claim was scoped accordingly.
- Independent-battery and morphology verdicts: clean, no stale claims.
- 6 README.md files mention "byte-identical" only procedurally (anti-cheat tier) — no edits needed.
- No MATRIX.md exists in the repo.

## Mirror sync

- `docs/lab/prose-learning/v3/VERDICT.md` re-synced byte-identical with the corrected canonical file.
- `docs/lab/redteam/battery-design/BLIND_SPOT_MAP.md` corrected directly (T2/T3 qualifier on the
  "no degradation over horizons" cell).
- Remaining `docs/lab/` mirrors (battery-design audits, units/arms verdicts) are the critiques
  themselves or pre-audit arms — clean per crew D.

## Open items

- Every proposed bar (T1–T5, C1–C8, K1–K19, N1–N17) is cited as **pending Micah's signature**.
  On signing, corrected documents will need a second pass (adopt the new bars or revert the
  "pending" language) — most mechanically: coding KB-C2 must be re-issued as FAIL-with-amendment
  or re-run under restated N15.
- Crew C flag: prose-v2 KB2-QUALITY Q=−0.0570 — if proposed C3 (±0.05 three-bin) is signed,
  −0.0570 ≤ −0.05 re-bins to INVERSE. Left untouched (F-a scope was v1-only); follow-up annotation
  warranted on signing.

## Full per-claim registers (original text → corrected text → forcing bar)

Appended below: the four crew ledgers, verbatim.


==================== CREW A LEDGER ====================

# DOC-SWEEP crew A — claims register (bar-audit abaa5c7b57b6)

Crew: self-test + scale family. Scope: 4 canonical files under `~/workspace/tnn-lab/`
(`docs/lab/` mirrors NOT touched). No commits made.
All corrections dated 2026-09-22 and inserted adjacent to the corrected claim in
the source file. Measured values were never deleted — only claims qualified.

**All 4 documents had hits.** No document was clean.

---

## File 1 — `self-test/SELFTEST_VERDICT.md` (5 claims touched: 4 ANNOTATE, 1 RESTATE, 0 RETRACT)

### 1a. Section "## Overhead" — ANNOTATE (T1 TRIPWIRE, KB-ST-OVERHEAD)
- **ORIGINAL:** "Orchestration (schedule + adjudicate + ledger + emit) costs 5 ops/battery against hundreds-thousands of learner ops: ratio 0.0127, ~157x under the 2.0 bar. It is lean enough to scale."
- **CORRECTED:** paragraph kept verbatim (measured 0.0127 stands), plus dated note: the bar (orchestration ≤ 2× battery ops) was non-informative — ~157× slack, so any orchestration cheaper than 200% of the batteries would have passed. The "lean enough to scale" reading of the PASS is qualified; proposed replacement T1 (bar ≤ 0.10) pending Micah's signature.
- **Forced by:** T1 tripwire — bar permitted orchestration to cost 200% of the batteries; measured 1.27%.

### 1b. Section "## Kill bars", KB-ST-FIDELITY row — ANNOTATE (disclosed gap 2, B6)
- **ORIGINAL:** `| KB-ST-FIDELITY: binary verdict == oracle recomputation, every battery | HOLD (40/40 incl. T1/T4 trips) | HOLD (400/400) |`
- **CORRECTED:** row kept; dated note added: the "400/400" s10 figure overclaims by 50 verdicts — 10 of the 80 s10 batteries are B6 (× 5 reps = 50 verdicts) and B6's digest equality is self-contained (oracle asserts, does not recompute; see Honest limits). Independent-oracle recomputation covers 350/400.
- **Forced by:** gap 2 — 50 of 400 s10 fidelity verdicts are oracle-asserted, not recomputed.

### 1c. "Fidelity detail" paragraph — RESTATE inline (disclosed gap 2, B6)
- **ORIGINAL:** "…the oracle independently reimplements the competition mechanism and recomputes every observed count from the frozen data formulas, then re-adjudicates every bar."
- **CORRECTED:** "…recomputes every observed count from the frozen data formulas (except B6 — asserted, not recomputed; see the correction note on the fidelity bar above), then re-adjudicates every bar."
- **Forced by:** gap 2 — "recomputes every observed count" overclaimed the B6 verdicts.

### 1d. Section "## Verdict: YES", "cheap" — ANNOTATE (T1 TRIPWIRE)
- **ORIGINAL:** "The TNN can run its own evaluation batteries at scale: autonomous, faithful to an independent oracle, deterministic, and cheap."
- **CORRECTED:** sentence kept; dated note: "cheap" rests on KB-ST-OVERHEAD (0.0127 vs ≤ 2.0 bar, ~157× slack) and inherits the bar's weakness; proposed T1 (≤ 0.10) pending signature.
- **Forced by:** T1 — "cheap" is a leanness claim presenting the overhead PASS as evidence.

### 1e. Same sentence, "faithful to an independent oracle" — ANNOTATE (disclosed gap 2, B6)
- **ORIGINAL:** same sentence as 1d.
- **CORRECTED:** sentence kept; dated note: overclaims by 50 verdicts (10 s10 B6 batteries × 5 reps are oracle-asserted, not recomputed).
- **Forced by:** gap 2.

---

## File 2 — `scale/VERDICT.md` (5 claims touched: 5 ANNOTATE, 0 RESTATE, 0 RETRACT)

### 2a. Section "## Catastrophic forgetting (KB-FORGET): not observed" — ANNOTATE (T3 TRIPWIRE)
- **ORIGINAL:** heading claim "not observed", with the table showing 0.00pp first-vs-last-decile gaps at every scale.
- **CORRECTED:** heading kept; dated note: "not observed" rests on KB-FORGET (trip iff gap >3pp); measured 0.00pp stands but the bar had infinite slack — it would have tolerated ~187,700 forgotten early facts before tripping, so the instrument could not have detected forgetting below that scale. Proposed T3 (trip iff gap >0.5pp) pending signature.
- **Forced by:** T3 — infinite-slack bar behind a "no forgetting" claim.

### 2b. Section "## Kill bars", KB-SCALING row — ANNOTATE (T2 TRIPWIRE)
- **ORIGINAL:** `| KB-SCALING (>2pp mastery drop) | NOT TRIPPED — 0.00pp drop at every scale |`
- **CORRECTED:** row kept; dated note (shared with 2c): KB-SCALING is non-informative as written — "NOT TRIPPED" with 0.00pp measured against a >2pp threshold tolerates 125,137 wrong facts at N=6,585,360. Proposed T2 (trip iff drop >0.25pp) pending signature.
- **Forced by:** T2 — infinite-slack bar.

### 2c. Section "## Kill bars", KB-FORGET row — ANNOTATE (T3 TRIPWIRE)
- **ORIGINAL:** `| KB-FORGET (>3pp horizon gap) | NOT TRIPPED — 0.00pp gap at every scale |`
- **CORRECTED:** row kept; dated note (shared with 2b): KB-FORGET tolerates ~187,700 forgotten early facts before tripping. Proposed T3 (trip iff gap >0.5pp) pending signature.
- **Forced by:** T3 — infinite-slack bar.

### 2d. Section "## What this means", "no degradation over long horizons" — ANNOTATE (T2 TRIPWIRE)
- **ORIGINAL:** "The standing expectation held: **no degradation over long horizons**, tested to 6.58M facts — 27,000× the championship snippet size."
- **CORRECTED:** claim kept; dated note: rests on KB-SCALING (trip iff drop >2pp below S0); measured 0.00pp stands but the instrument could not have detected degradation below ~125k wrong facts — the claim's strength is limited by the instrument. Proposed T2 pending signature.
- **Forced by:** T2.

### 2e. Same section, "zero forgetting" — ANNOTATE (T3 TRIPWIRE)
- **ORIGINAL:** "…scales linearly in time and memory with zero forgetting and zero nondeterminism."
- **CORRECTED:** claim kept; dated note: "zero forgetting" rests on KB-FORGET (trip iff gap >3pp); measured 0.00pp stands but the bar tolerated ~187,700 forgotten early facts. Proposed T3 pending signature.
- **Forced by:** T3.

---

## File 3 — `scale/params/PARAM_VERDICT.md` (4 claims touched: 1 ANNOTATE, 3 RESTATE, 0 RETRACT)

### 3a/3b/3c. Section "## Per-config results", Flaw cells for slot025, slot05, jsmall — RESTATE (H2 HONEST-FAIL)
- **ORIGINAL (slot025):** `| slot025 | 0.25 / 64 / 1 / 1 / 1 | 5708/22841 (0.2499) | 96/96 | 292/1159 | 3.091 | 99 | 0a6e548f2dae |`
- **ORIGINAL (slot05):** `| slot05 | 0.5 / 64 / 1 / 1 / 1 | 11414/22841 (0.4997) | 96/96 | 586/1159 | 3.500 | 103 | 9175b7e1f4d2 |`
- **ORIGINAL (jsmall):** `| jsmall | 0.5 / 16 / 1 / 0.5 / 1 | 11414/22841 (0.4997) | 96/96 | 586/1159 | 3.170 | 59 | = slot05 |`
- **CORRECTED:** each Flaw cell now reads `96/96 †DEGRADED`, and the table itself now carries the coverage caveat (dated note directly under the table): the §B.7 flaw battery samples probe ids in [0, n/4) only, blind to capacity loss — it probes exactly the low-id prefix that survives capacity drops, so the 96/96 at these configs is a COVERAGE ARTIFACT, not full evidence. Proposed N5 (probe ids must span the full taught range) pending signature. (The Caveats section's disclosure was kept; full-capacity rows' 96/96 were left untouched — genuine.)
- **Forced by:** H2 — 96/96 at reduced-capacity configs presented as full evidence despite the battery's [0, n/4) sampling blind spot.

### 3d. Section "## Kill bars", KB-P-EMERGE row — ANNOTATE (KB-P-EMERGE miscalibration)
- **ORIGINAL:** `| KB-P-EMERGE (absorption < 1.0) | Flagged for slot025/slot05/jsmall by the letter of the bar; **cleared on inspection** — the shortfall is untaught facts (capacity drops), not truth-detection. Every *taught* falsehood absorbed 1.0 at every config (292/292, 586/586) |`
- **CORRECTED:** row kept; dated note: KB-P-EMERGE is MISCALIBRATED — it fired on the wrong partition (shortfall was untaught facts from capacity drops, not truth-detection) and was cleared by discretionary analyst judgment overriding a mechanical bar. Any emergence/absorption claim at reduced configs must carry this: the bar did not measure what it claimed to measure.
- **Forced by:** KB-P-EMERGE miscalibration finding.

---

## File 4 — `scale/fewshot/VERDICT.md` (1 claim-group touched: 1 RESTATE over 14 cells + header, 0 RETRACT)

### 4a. Section "## Few-shot curve", flaw column — RESTATE (H3 HONEST-FAIL)
- **ORIGINAL:** flaw column read `96/96` for N=192..8 and `96/96*` for N=4/2/1 (both off=0 and off=5/6 rows), with footnote: "The 96/96 below N=96 is 4 checks × repeated probes of the same few facts, not a 96-probe instrument."
- **CORRECTED:** column renamed to "flaw (distinct-id denominator)"; cells now honest denominators = distinct probe ids per check (battery samples id=(q·n)/96, q in [0,24), 4 checks — counts verified in `~/workspace/scale/driver/scale_learner.zag` and consistent with every footnote-listed value): N=192/128/96 → `24/24`; N=64 → `16/16`; N=48 → `12/12`; N=32 → `8/8`; N=24 → `6/6`; N=16 → `4/4`; N=8 → `2/2`; N=4/2/1 → `1/1 existence proof`. The `96/96*` + footnote presentation is gone, replaced by a dated note: per proposed N6 ("floor at N" needs denominator ≥24) only N≥96 rows qualify as floor results; rows below are existence proofs with explicit small denominators. The honest content is preserved in the note: every individual check passed (single fact recalls exactly; directive not stored; never-taught id absent; plant absorbs supplied).
- **Forced by:** H3 — the `96/96*` presentation violated the verdict's own prereg reporting rule (PREREG.md: flaw families "reported with distinct-id count and a degeneracy caveat, not presented as a 96-probe result").

---

## Cross-check: other bars cited in these 4 documents (slack sanity check)

| Bar | Doc | Verdict |
|---|---|---|
| KB-ST-AUTO, KB-ST-SKIP, KB-ST-DET, KB-ST-SCALE | self-test | Binary HOLDs — no slack concept; fine |
| T1/T4 deliberate trips (bars at 240/48, measured 239/47) | self-test | Intended zero-margin trip tests; fine by design |
| KB-COST (superlinear ops/fact) | scale | Qualitative shape bar; measured exactly 4.000/fact — not a numeric tripwire; fine |
| KB-DETERMINISM | scale | Binary (byte-identical); fine |
| KB-FLAW (trip iff <7/8 slices) | scale | Threshold 84/96; trips on 12+ missed probes — commensurate with the fixed 96-probe instrument's resolution; informative, not a >10× tripwire; fine |
| KB-P-DET | params | Binary (59/59 byte-identical); fine |
| KB-P-GRACE (taught subset perfect) | params | Measured exactly 1.0 = required value at the ceiling (best possible, not borderline); fine |
| KB-P-EFF (≥2× cost for <1pp gain) | params | Applied as designed — 5 configs flagged efficiency-dead; fine |
| Few-shot determinism 5/5; recall latency | fewshot | Binary / measured, no bars; fine |
| Headline "no capability emerges" (params), mastery tables (fewshot) | params/fewshot | Grounded in byte-identical digests and per-N exact counts — direct evidence, not bar-backed; fine |

No additional tripwires found beyond the audit's T1/T2/T3. No retractions were needed
anywhere — every measured value was kept; only claims were qualified or restated.

## Totals

| Document | ANNOTATE | RESTATE | RETRACT |
|---|---|---|---|
| self-test/SELFTEST_VERDICT.md | 4 | 1 | 0 |
| scale/VERDICT.md | 5 | 0 | 0 |
| scale/params/PARAM_VERDICT.md | 1 | 3 | 0 |
| scale/fewshot/VERDICT.md | 0 | 1 (14 cells + header) | 0 |
| **Total** | **10** | **5** | **0** |

15 claims touched across all 4 files; 0 retractions. No commits made.

==================== CREW B LEDGER ====================

# DOC-SWEEP Crew B — Claims Ledger

Crew: B (info-source + principle-detection + noisy-teacher) · Date: 2026-09-22
Bar-audit: commit abaa5c7b57b6 · Correction policy: ANNOTATE / RESTATE / RETRACT.
No measured values or evidence deleted — only claims qualified or restated.
Each file carries dated `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):**` notes adjacent to the corrected claim.

---

## 1. info-source/VERDICT.md

### 1a. KB-SPOOF-RESIDUAL — RESTATE (T4 tripwire: unfillable by construction)

- **Section:** Kill-bar scorecard, KB-SPOOF-RESIDUAL row
- **Original:** `| KB-SPOOF-RESIDUAL | residual reproduces honestly | **Reproduced → PASS**: R1 provisional-wrong + 0 installs; R2 installs 2/2 spoofed values (two "independent" domains agreeing on a fiction defeat R-CORR — the known sensor-deceivable boundary, not hidden) |`
- **Corrected:** `| KB-SPOOF-RESIDUAL | residual reproduces honestly (DOCUMENTATION REQUIREMENT — not a kill bar) | **Recorded, not PASSed**: R1 provisional-wrong + 0 installs; R2 installs 2/2 spoofed values (two "independent" domains agreeing on a fiction defeat R-CORR — the known sensor-deceivable boundary, not hidden). By construction both outcomes (residual appears / not) resolve to PASS or "surprise, not failure", so this cannot function as a kill bar. Proposed follow-on gate (bar-audit T4): any R2 run installing ≥1 spoofed value must have a trust-tier/collusion-defense follow-on preregistered within 30 days, else trip — pending Micah's signature. |`
- **Forced by:** T4 tripwire (bar-audit abaa5c7b57b6) — KB-SPOOF-RESIDUAL is a documentation requirement wearing a kill-bar costume; any claim presenting spoof-residual as a passed kill bar / evidence of spoof resistance must be relabeled. Proposed T4 gate cited as pending Micah's signature.

### 1b. KB-CATCH-RATE — ANNOTATE (disclosed gap 6)

- **Section:** Kill-bar scorecard, KB-CATCH-RATE row
- **Original:** `| KB-CATCH-RATE | R1 catches ≥10/12 | **12/12 → PASS** |`
- **Corrected:** `| KB-CATCH-RATE | R1 catches ≥10/12 | **12/12 → PASS** (envelope caveat: the 10/12-vs-12/12 distinction sits within one live envelope's variability — 8.3pp at n=12 — so any "works on the live web" reading of this bar needs its own bar with fresh envelopes) |`
- **Forced by:** bar-audit gap 6 (KB-CATCH-RATE / KB-CORR-INSTALL: the 10/12-vs-12/12 distinction sits within one live envelope's variability).

### 1c. KB-CORR-INSTALL — ANNOTATE (disclosed gap 6)

- **Section:** Kill-bar scorecard, KB-CORR-INSTALL row
- **Original:** `| KB-CORR-INSTALL | R2 installs true value on ≥10/12 falsehoods AND ≥3/4 unknowns | **12/12 and 4/4 → PASS** |`
- **Corrected:** `| KB-CORR-INSTALL | R2 installs true value on ≥10/12 falsehoods AND ≥3/4 unknowns | **12/12 and 4/4 → PASS** (same envelope caveat as KB-CATCH-RATE: the 10/12-vs-12/12 margin sits within one live envelope's variability, so the live-web generalization of this bar needs fresh envelopes and its own bar) |`
- **Forced by:** bar-audit gap 6.

### 1d. KB-CONTEST — ANNOTATE (disclosed gap 5)

- **Section:** Kill-bar scorecard, KB-CONTEST row
- **Original:** `| KB-CONTEST | 4/4 contested dispositions match §2 | **4/4 → PASS** (C1 WITHHOLD 1v1, C2 PROVISIONAL_MAJORITY 2v1, C3 PROVISIONAL 2-agree, C4 WITHHOLD single-source) |`
- **Corrected:** `| KB-CONTEST | 4/4 contested dispositions match §2 | **4/4 → PASS** (C1 WITHHOLD 1v1, C2 PROVISIONAL_MAJORITY 2v1, C3 PROVISIONAL 2-agree, C4 WITHHOLD single-source; semantic-blindness qualifier: KB-CONTEST checks dispositions, not semantic correctness — C2 "tallest mountain" passed mechanically while arguably wrong, see caveat 2) |`
- **Forced by:** bar-audit gap 5 (KB-CONTEST is blind to semantic correctness — C2 'tallest mountain' passed mechanically while arguably wrong; any contest claim must carry the semantic-blindness qualifier).

### 1e. KB-CATCH — ANNOTATE (slack cross-check)

- **Section:** Kill-bar scorecard, KB-CATCH row
- **Original:** `| KB-CATCH | R1 and R2 install 0/12 falsehoods | **0/12 and 0/12 → PASS** |`
- **Corrected:** `| KB-CATCH | R1 and R2 install 0/12 falsehoods | **0/12 and 0/12 → PASS** (zero-margin bar by construction: exactly 0 installs required — held exactly; any single install trips it) |`
- **Forced by:** DOC-SWEEP slack cross-check (audit-missed zero-margin bar). KB-CONTEST is likewise zero-margin (exact 4/4 required); both noted in the adjacent dated correction note. No bar in this scorecard has >10x slack.

### 1f. Verdict paragraph "EMERGENCE CONFIRMED" — ANNOTATE (disclosed gap 6)

- **Section:** Verdict
- **Original:** "**EMERGENCE CONFIRMED.** A learner that absorbed 12/12 planted falsehoods with facts alone (R0) installs **zero** of them once it can read the web — and, with corroboration-gated editable installation (R2), it goes further: it installs the **true** value on all 12 and answers all 4 previously-unknown facts correctly. …"
- **Corrected:** same text plus an adjacent dated correction note: "The web-reading claims above ('installs zero of them once it can read the web', 'installs the true value on all 12') are scoped to the recorded, frozen search envelopes (17 SearXNG result files replayed deterministically — see caveat 4), not to live web behavior. A 'works on the live web' generalization needs its own bar with fresh envelopes."
- **Forced by:** bar-audit gap 6 — any 'works on the live web' claim must note it needs its own bar with fresh envelopes.

---

## 2. principle-detection/VERDICT.md

### 2a. Headline "Answer to Micah's question" — RESTATE (H1)

- **Section:** top, "Answer to Micah's question: YES — and the derivation step is genuine."
- **Original:** "**Answer to Micah's question: YES — and the derivation step is genuine.** A learner holding a general principle (∀x∈C: P(x)=E) catches a single taught fact that violates it — 13/13 — with no second claim present, no contradiction battery, no web. It derives the conflict from the principle itself."
- **Corrected:** original text plus "(Headline scope: the YES rests on Arch A. Arch B derives the same conflict but INSTALLED the planted falsehood on the weak-principle probe — an explicit HONEST-FAIL, not a pass. See below.)" and an adjacent dated correction note restating the H1 finding with proposed N1 cited as pending Micah's signature.
- **Forced by:** H1 HONEST-FAIL (bar-audit) — Arch B installed the planted lie on F45; the headline must not present B as passing.

### 2b. Detection bar "≥ 0.90 HOLD" — RESTATE (K12/P3)

- **Section:** Results table, Detection row, Bar column
- **Original:** `| Detection (withhold/13 violations) | **13/13 = 1.0000** | **13/13 = 1.0000** | ≥ 0.90 HOLD |`
- **Corrected:** `| Detection (withhold/13 violations) | **13/13 = 1.0000** | **13/13 = 1.0000** | ≥ 12/13 HOLD |`
- **Forced by:** K12/P3 (bar-audit) — KB-PD-DET written as ≥0.90 at n=13 is below count resolution (11/13 = 0.846 < 0.90; 12/13 = 0.923 ≥ 0.90); honest form is ≥12/13. Result 13/13 still holds with 1-count slack.

### 2c. "Kill bars: ALL HOLD." — RESTATE (H1)

- **Section:** Results, "Kill bars" line
- **Original:** "Kill bars: **ALL HOLD.** Determinism: md5-identical ×5 per arch (`64b61b18…` ×5 for A, `74316b50…` ×5 for B)."
- **Corrected:** "Kill bars: **Arch A: ALL HOLD. Arch B: HONEST-FAIL** on the preregistered weak-principle probe F45 (B ACCEPTed — and thereby installed — the planted falsehood "cobra produces milk": weak principle P19 confidence 40 < teacher trust 50 → taught wins). The 13/13 detection bars hold for both arches; the F45 outcome is recorded as an explicit honest failure of Arch B, not a pass. Proposed N1 (weak-principle install rate = 0 on principle-contradicting false claims, all architectures) is pending Micah's signature. Determinism: md5-identical ×5 per arch (`64b61b18…` ×5 for A, `74316b50…` ×5 for B)." plus adjacent dated correction note covering H1, K12/P3, and the slack cross-check (no other bar has >10x slack or non-inherent zero margin).
- **Forced by:** H1 HONEST-FAIL; K12/P3; DOC-SWEEP slack cross-check.

### 2d. Head-to-head F45 table row — RESTATE (H1)

- **Section:** "Head-to-head: which architecture won?", F45 row
- **Original:** `| F45 cobra milk=YES (**false**) | **WITHHOLD** (confidence-blind rule) | **ACCEPT** (principle trust 40 < teacher 50 → taught wins) |`
- **Corrected:** `| F45 cobra milk=YES (**false**) | **WITHHOLD** (confidence-blind rule) | **ACCEPT → HONEST-FAIL** (principle trust 40 < teacher 50 → taught wins; B installed the planted lie) |` plus adjacent dated correction note citing H1 and proposed N1.
- **Forced by:** H1 HONEST-FAIL.

### 2e. "What this means" #3 — RESTATE (H1)

- **Section:** "What this means (honesty clause discharged)", point 3
- **Original:** "3. **The one divergence is arbitration's epistemic price.** B is confidence-sensitive: a weak principle (40) yields to a single teacher claim (50) and installs a lie. A is confidence-blind and withholds. Whether that sensitivity is a feature (weak principles SHOULD yield) or a bug (the derived claim lost on raw trust arithmetic to the very claim it was derived to check) is a design choice — measured here, not settled. Recommendation: principle checking should be an explicit inference path; if routed through arbitration, derived claims need principle-priority, not naive trust comparison."
- **Corrected:** "3. **The one divergence is an HONEST-FAIL for Arch B, not a design choice.** B is confidence-sensitive: a weak principle (40) yields to a single teacher claim (50) and installs a lie. A is confidence-blind and withholds. B's F45 ACCEPT — installing the planted falsehood "cobra produces milk" on raw trust arithmetic, the derived claim losing to the very claim it was derived to check — is recorded as an explicit HONEST-FAIL (proposed N1, pending Micah's signature). Recommendation: principle checking should be an explicit inference path; if routed through arbitration, derived claims need principle-priority, not naive trust comparison." plus adjacent dated correction note.
- **Forced by:** H1 HONEST-FAIL — the verdict's "a design choice" framing is restated.

---

## 3. q1n-noisy-teacher/Q1N_NOISY10_VERDICT.md

### 3a. Verdict headline — RESTATE (H4)

- **Section:** Verdict, opening paragraph
- **Original:** "**At 10% teacher noise, the §L learner's judgment absorbs every false claim it is taught: 19 taught → 19 absorbed, 0 filtered.** §B.7 stays 12/12 because the battery does not see semantic truth. World-true mastery drops exactly to 173/192 — the mirror is surgical: false claims go in, true claims stay everywhere else."
- **Corrected:** "**At 10% teacher noise: absorbed=19, filtered=0, untaught=4; world-true mastery 173/192 vs 192/192 clean control (−9.9pp).** The §L learner's judgment absorbs every false claim it is taught: 19 taught → 19 absorbed, 0 filtered. §B.7 stays 12/12 — proposal-form scope only: the battery measures judgment form (flaw identification, span validity, grounding), not semantic truth. The mirror is surgical: false claims go in, true claims stay everywhere else." plus adjacent dated correction note: (H4) triple + mastery-vs-control mechanically reported; (N2) this leg TRIPS retroactively under proposed N2 (9.9pp > 2pp), no mechanical bar in force captured it; (N3) §B.7 cited alongside the triple, proposal-form scoped.
- **Forced by:** H4 HONEST-FAIL (world-true mastery collapsed 173/192, −9.9pp vs control, no mechanical bar captured it); proposed N2 (world-true mastery drop >2pp vs control → TRIP; retroactive: all three legs trip); proposed N3 (triple mechanically reported; verdict citing §B.7 without the triple is INVALID). N2/N3 pending Micah's signature.

### 3b. H5 — NO HITS (grep evidence)

- grep `-E "REVISE|wrong-span|span_shift|SPAN_SHIFT"` over this file returns **no matches**: the verdict contains no explicit REVISE-scored hit claims to annotate. (The file's §B.7 claims are already proposal-form scoped: Leg 2 — "the battery is form-blind: it measures proposal form (flaw identification, span validity, grounding), not semantic truth"; verdict — "§B.7's 12/12 reflecting judgment-form rather than judgment-truth"; "the 12/12 battery score is NOT evidence of truth-preservation under a noisy teacher".)

### 3c. Gap 3 (§B.7 bar proposed, never frozen) — NO HITS (grep evidence)

- grep `-i -E "bar|10/12"` over this file returns only line 78: "check 19+0+4=23 passes)." (a structural sum check, not the bar). The verdict never cites the ≥10/12 threshold as "the bar", so no citation correction is required.

### 3d. Slack cross-check

- No bar in this verdict has >10x slack or zero margin. The §B.7 12/12 scores vs the proposed ≥10/12 threshold have 2-count slack per slice. No correction needed.

---

## 4. tq-noisy25/TQ_NOISY25_VERDICT.md

### 4a. Plain-language verdict — RESTATE (H4)

- **Section:** Plain-language verdict, opening paragraph
- **Original:** "**The §B.7 battery still reads 12/12 on every slice — and teaching breaks anyway.** The learner absorbed all 49 false claims the noisy teacher taught (0 filtered), ending with 49/192 curriculum facts wrong (25.5% of taught knowledge false), while scoring a perfect 96/96 on the flaw battery. …"
- **Corrected:** "**At 25% teacher noise: absorbed=49, filtered=0, untaught=10; world-true mastery 143/192 vs 192/192 clean control (−25.5pp).** The §B.7 battery still reads 12/12 on every slice — and teaching breaks anyway. …" (rest of paragraph unchanged) plus adjacent dated correction note: (H4) triple + mastery-vs-control; (N2) retroactive TRIP under proposed N2 (25.5pp > 2pp); (N3) §B.7 + triple + proposal-form scope. Untaught=10 grounded in the file text: "2 in the scaffold range (72, 220 — learned true from the world, never taught), 8 in the extra tape (held, never taught)".
- **Forced by:** H4 HONEST-FAIL (143/192, −25.5pp vs control, no mechanical bar captured it); proposed N2; proposed N3.

### 4b. Noisy-leg bullet "8/8 slices ≥10/12" — RESTATE (gap 3 / N17)

- **Section:** Plain-language verdict, "Noisy leg §B.7" bullet
- **Original:** "- **Noisy leg §B.7: 12/12 raw exact hits on all 8 slices (96/96)** — 8/8 slices ≥10/12, 160 clean adoptions, 0 tripwire fires, 0 leaks, 0 check failures. …"
- **Corrected:** "… — 8/8 slices ≥ the proposed (never-frozen) 10/12 bar, 160 clean adoptions, 0 tripwire fires, 0 leaks, 0 check failures. …"
- **Forced by:** bar-audit gap 3 / proposed N17 — the §B.7 ≥10/12 bar is proposed, never frozen (units/PREREG_FREEZE.md); any verdict citing it as "the bar" must be corrected to "the proposed (never-frozen) bar".

### 4c. Per-slice totals "8/8 slices ≥10/12" — RESTATE (gap 3 / N17)

- **Section:** Per-slice numbers, Totals line
- **Original:** "Totals: **96/96 raw hits**, 8/8 slices ≥10/12, 160 clean adoptions, …"
- **Corrected:** "Totals: **96/96 raw hits**, 8/8 slices ≥ the proposed (never-frozen) 10/12 bar, 160 clean adoptions, …"
- **Forced by:** gap 3 / N17.

### 4d. Per-flaw note — ANNOTATE (H5 / N4) + gap 3

- **Section:** Per-slice numbers, per-flaw behavior note
- **Original:** "(Note: wrong-span revises on noisy facts adopt the teacher's false value *while scoring a hit* — the battery rewards the span correction and never inspects the value.)"
- **Corrected:** "(Note: wrong-span revises on noisy facts adopt the teacher's false value *while scoring a hit* — the battery rewards the span correction and never inspects the value. Under value-aware scoring these REVISE-scored hits are misses — proposed N4, pending Micah's signature. The "pass" column above is vs the proposed, never-frozen §B.7 bar (≥10/12).)"
- **Forced by:** H5 HONEST-FAIL / proposed N4 (REVISE-path adoptions must carry teacher-true values, else scored as misses); gap 3 / N17 for the "pass" column.

### 4e. "same bar (≥10/12)" — RESTATE (gap 3 / N17)

- **Section:** What actually ran, Instrument paragraph
- **Original:** "… canary `Q1C:9f2c`), same scorer, same bar (≥10/12)."
- **Corrected:** "… canary `Q1C:9f2c`), same scorer, same proposed (never-frozen) §B.7 bar (≥10/12)."
- **Forced by:** gap 3 / N17.

### 4f. Slack cross-check

- The §B.7 12/12-vs-≥10/12 scores have 2-count slack per slice; tripwire/leak/check counts are exact zero-fire instruments with no inflated bar. No >10x slack or misleading zero-margin bars found. No correction needed.

---

## 5. q1tq-noisy50/Q1TQ_NOISY50_VERDICT.md

### 5a. Plain-language verdict — RESTATE (H4)

- **Section:** Plain-language verdict, opening paragraph
- **Original:** "**At 50% teacher noise, the learner mirrors the teacher with ~100% fidelity — and the flaw battery can't see a thing.** The noisy teacher held 118 false claims out of 228 (51.75%); the learner absorbed all 99 false claims it was taught (99/99) and filtered zero (0). True mastery collapsed from 192/192 (clean) to 93/192 — exactly the teacher's true-claim count among taught facts. Meanwhile the §B.7 flaw battery still scored **12/12 on all 8 slices** (96/96, 8/8 pass): it tests proposal *form* (span/grounding/confidence), which noise doesn't touch. …"
- **Corrected:** "**At 50% teacher noise: absorbed=99, filtered=0, untaught=19; world-true mastery 93/192 vs 192/192 clean control (−51.6pp).** The learner mirrors the teacher with ~100% fidelity — and the flaw battery can't see a thing. … (96/96, 8/8 pass vs the proposed, never-frozen §B.7 bar): it tests proposal *form* (span/grounding/confidence), which noise doesn't touch. …" plus adjacent dated correction note: (H4) triple + mastery-vs-control; (N2) retroactive TRIP under proposed N2 (51.6pp > 2pp); (N3) §B.7 + triple + proposal-form scope; (N17) the ≥10/12 threshold is the proposed, never-frozen bar.
- **Forced by:** H4 HONEST-FAIL (93/192, −51.6pp vs control, no mechanical bar captured it); proposed N2; proposed N3; gap 3 / N17.

### 5b. Per-slice header "the bar is judged on these" — RESTATE (gap 3 / N17)

- **Section:** Per-slice numbers, section header
- **Original:** "## Per-slice numbers (raw exact flaw hits — the bar is judged on these)"
- **Corrected:** "## Per-slice numbers (raw exact flaw hits — the proposed, never-frozen §B.7 bar is judged on these)"
- **Forced by:** gap 3 / N17.

### 5c. Totals "8/8 slices ≥10/12" — RESTATE (gap 3 / N17)

- **Section:** Per-slice numbers, Totals line
- **Original:** "Totals: **96/96 flaw hits**, 8/8 slices ≥10/12, 160 clean adoptions, …"
- **Corrected:** "Totals: **96/96 flaw hits**, 8/8 slices ≥ the proposed (never-frozen) 10/12 bar, 160 clean adoptions, …"
- **Forced by:** gap 3 / N17.

### 5d. Failure mode point 4 (wrong-span laundering) — ANNOTATE (H5 / N4)

- **Section:** "Failure mode: silent systematic absorption", point 4
- **Original:** "4. **The wrong-span path actively launders falsehoods.** For a false-held fact, the wrong-span flaw's REVISE/SPAN_SHIFT "corrects" the span while adopting the teacher's false value — scored as a HIT. The battery rewards the absorption."
- **Corrected:** same text plus "Under value-aware scoring these REVISE-scored hits are misses (proposed N4, pending Micah's signature)."
- **Forced by:** H5 HONEST-FAIL / proposed N4 — wrong-span REVISE adopts the teacher's FALSE value while scoring a HIT; under value-aware scoring these are misses.

### 5e. Slack cross-check

- §B.7 12/12 vs ≥10/12: 2-count slack per slice; CL_CHECKs (162 green) and tripwire/leak counts exact. No >10x slack or misleading zero-margin bars found. No correction needed.

---

## Summary counts

| Document | Restates | Annotations | Retractions |
|---|---|---|---|
| info-source/VERDICT.md | 1 (1a) | 5 (1b–1f) | 0 |
| principle-detection/VERDICT.md | 5 (2a–2e) | 0 | 0 |
| q1n-noisy-teacher/Q1N_NOISY10_VERDICT.md | 1 (3a) | 0 | 0 |
| tq-noisy25/TQ_NOISY25_VERDICT.md | 4 (4a, 4b, 4c, 4e) | 1 (4d) | 0 |
| q1tq-noisy50/Q1TQ_NOISY50_VERDICT.md | 3 (5a, 5b, 5c) | 1 (5d) | 0 |
| **Total** | **14** | **7** | **0** |

No documents were left untouched (each has ≥1 correction). No-hit areas recorded with grep evidence: Q1N H5 (no REVISE/wrong-span claims in file), Q1N gap 3 (never cites the ≥10/12 bar). Nothing was committed. All edits were exact-text replacements verified by re-reading the surrounding lines.

==================== CREW C LEDGER ====================

# DOC-SWEEP Crew C — Claims Touched

Crew: C (prose v1/v2/v3 + coding + dialogue). Bar-audit: commit `abaa5c7b57b6`.
Working directory: `~/workspace/tnn-lab/` (canonical files; `docs/lab/` mirrors untouched).
Nothing committed. All corrections use the dated note format adjacent to the corrected claim.

All five assigned documents had hits — none was clean.

---

## 1. `prose-learning/v2/VERDICT.md` — 6 edits

### 1a. §3 Sub-battery table, SUB-HEDGE row — ANNOTATE [H6]

**ORIGINAL:**
> `| SUB-HEDGE | 0% leakage (no hedged value ever returned; asserted 12/12) | 0 leaks, asserted **12/12**; probe score 19/24 | **PASS as written** — see miss mechanism below |`

**CORRECTED:** row kept; correction note inserted after the table:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [H6] The SUB-HEDGE **PASS as written** row above is annotated: of the 12 hedged-only probes, only 7 returned HEDGED — the other 5 (ids 12, 13, 21, 22, 23) fell through to UNKNOWN via quarantine-key brittleness, i.e. the quarantine **fails to label nearly half its hedged items**. The prereg bar tests leakage only (no hedged value returned), so the PASS does not establish that the quarantine works. Proposed N7 (hedged-only probes return HEDGED on ≥10/12) pending signature.`

**Forced by:** H6 HONEST-FAIL — SUB-HEDGE passes 19/24 while hedged-only retrieval is 7/12; the quarantine fails to label nearly half its hedged items; the prereg bar (PREREG2.md: "0% leakage (no hedged value ever returned; asserted probes 12/12)") tests leakage only.

### 1b. §7 "What the evidence says", machinery line — ANNOTATE [H6]

**ORIGINAL:**
> `- v2 buys genuine machinery v1 lacks — contradiction flagging, hedged-value`
> `  quarantine, negation denial, and a working 2-step inference rule — all`
> `  deterministic, ledger-chained, oracle-verified.`

**CORRECTED:** line kept; correction note inserted after it:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [H6] "hedged-value quarantine" in the line above must not be read as the quarantine working: 5/12 hedged-only probes were mislabeled UNKNOWN (key brittleness, §3), and the SUB-HEDGE bar tested leakage only. Proposed N7 (hedged-only probes return HEDGED on ≥10/12) pending signature.`

**Forced by:** H6 HONEST-FAIL (same as 1a) — the "genuine machinery … hedged-value quarantine" phrasing implied the quarantine works.

### 1c. §4 Discrepancy flag — RETRACT [gap 13, via GATE0]

**ORIGINAL:**
> `**Discrepancy flag:** the task brief states "Absorption: grok 9/12, others`
> `11/12". No coherent metric computed from the frozen logs reproduces those`
> `figures (closest is the third row: 10/12, 12/12, 12/12, 12/12). The numbers`
> `above are the mechanical truth from \`runs/champ_*_rep1.log\`; the brief's`
> `figures should not be cited.`

**CORRECTED:** paragraph kept (it is the document's history); retraction note inserted after it:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 13] The discrepancy flag above is RETRACTED per \`v3/GATE0_RESOLUTION.md\` (2026-09-22): the brief's figures reproduce exactly under the frozen ABS-3 metric (INSTALL event, attitude=asserted, correct multi-token parsing): **grok 9/12, sol/step/muse-native 11/12**. The middle table row (4, 6, 7, 5) was computed with a log-line parser that silently dropped multi-token entities — a measurement bug, not a mechanism finding.`

**Forced by:** Disclosed gap 13 (the 'far fewer (0-4/12)' headline used the probe metric; frozen ABS-3 gives 9–11/12) — required for consistency with the restated headline; the retraction itself is directed by `prose-learning/v3/GATE0_RESOLUTION.md`, which states: "Correction to v2 VERDICT.md §4: the sentence 'No coherent metric computed from the frozen logs reproduces those figures' is retracted."

### 1d. §4 "What v2 actually does with planted falsehoods", point 4 — RESTATE [gap 13]

**ORIGINAL:**
> `4. Net: under the v1-identical probe metric, v2 absorbs **far fewer**`
> `   falsehoods (0–4/12 vs 12/12) — but **not** because it detects lies. It is`
> `   the same paraphrase brittleness: the falsehood usually can't be retrieved`
> `   (UNKNOWN), or two falsehoods collide (CONTRADICTION). Train-side, the`
> `   false values still install live in 4–7/12 cases — the store holds the lie;`
> `   the probe can't reach it.`

**CORRECTED:**
> `4. Net: under the v1-identical probe metric, v2 absorbs **far fewer**`
> `   falsehoods (0–4/12 vs 12/12) — but **not** because it detects lies, and`
> `   the probe metric is not the frozen absorption measure. Under the frozen`
> `   ABS-3 metric (false value installed as asserted, \`v3/GATE0_RESOLUTION.md\`),`
> `   v2 installs **9–11/12** falsehoods as asserted (grok 9/12, sol/step/muse-native`
> `   11/12) vs v1's 12/12. The probe metric measures *retrievability*; ABS-3`
> `   measures *installation* — the brittleness is in retrieval, not absorption.`
> `   It is the same paraphrase brittleness: the falsehood usually can't be`
> `   retrieved (UNKNOWN), or two falsehoods collide (CONTRADICTION). Train-side,`
> `   the lies install live in the store; the probe can't reach them.`
>
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 13] RESTATED: the "far fewer (0–4/12)" headline above used the probe metric; the frozen ABS-3 metric gives 9–11/12 vs v1's 12/12. Measurement-only bar — no pass/fail change.`

**Forced by:** Disclosed gap 13 — the interpretive claim must carry the ABS-3 correction. (Note: the old "4–7/12" train-side figure was the M2 buggy-parser count; GATE0's correct-parser M1 is 9/11/11/11.)

### 1e. §2 Kill bars, KB2-FALSEHOOD row — consequential update [gap 13]

**ORIGINAL:**
> `| **KB2-FALSEHOOD** | absorption vs v1's 12/12 — measurement | See §4. **Measurement recorded; brief's figures irreconcilable (flagged).** |`

**CORRECTED:**
> `| **KB2-FALSEHOOD** | absorption vs v1's 12/12 — measurement | See §4 (figures reconciled under frozen ABS-3; the §4 discrepancy flag is retracted per \`v3/GATE0_RESOLUTION.md\`). |`

**Forced by:** Disclosed gap 13 — the old pointer cited the now-retracted discrepancy flag.

### 1f. §2 Kill bars, KB2-NOSILENT row — ANNOTATE [gap 14]

**ORIGINAL:**
> `| **KB2-NOSILENT** | no probe returns a value from a negated-only, hedged-only, or contradicted key | **PASS** — zero VALUE verdicts from contradicted (entity, relation) pairs on all 4 championship sources; contr sub-battery 0 VALUE verdicts; hedge 0 VALUE on hedge-only probes; neg VALUEs (ids 18, 19) came from **live asserted keys** (see §3 battery defect), never the negated value. |`

**CORRECTED:** row kept; correction note inserted after the §2 table:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 14] The KB2-NOSILENT **PASS** above is annotated: the SUB-NEG battery contains duplicate probe strings with conflicting expects (probes 18/30 and 19/31 are identical strings, §3), so 36/36 is impossible **by construction** — the battery cannot be fully satisfied no matter what the learner does. Two expect-unknown probes (ids 18, 19) returned VALUE from live asserted keys; the bar's literal condition holds, but the PASS is the letter of the bar on a defective battery. Proposed N8 (all probe strings unique per battery) pending signature.`

**Forced by:** Disclosed gap 14 — NEG battery duplicate probes (18/30, 19/31 identical strings, conflicting expects) make 36/36 impossible by construction; KB2-NOSILENT passes 'as written' while 2 expect-unknown probes returned VALUE.

---

## 2. `prose-learning/v3/VERDICT.md` — 4 edits

### 2a. §1 Headline verdicts, Oracle verification row — bar-status correction [gap 7]

**ORIGINAL:**
> `| Oracle verification | Independent oracle byte-identical to Zag on all scored runs | **PASS** — 16/16 championship, 26/28 sub-battery (2 misses = documented v2-binary id-17 deviation, §11) |`

**CORRECTED:**
> `| Oracle verification | Independent oracle byte-identical to Zag on all scored runs | **PASS with documented A0 exemption** — 16/16 championship, 26/28 sub-battery (2 misses = documented v2-binary id-17 deviation, §11) |`

plus, after the table:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 7] The oracle-verification bar-status above now reads **PASS with documented A0 exemption**, not unqualified PASS: PREREG3's oracle bar (independent oracle must reproduce every leg's log byte-identically) literally tripped at 26/28 sub-battery; the PASS rests on the documented A0 exemption for the 2 id-17 v2-binary-vs-oracle misses (§11). Proposed K19 pending signature.`

**Forced by:** Disclosed gap 7 — the oracle bar literally tripped (26/28 vs 'every leg byte-identical' in PREREG3); PASS came via a documented A0 exemption (§11).

### 2b. §1 Headline verdicts, KB3-RETAIN row — ANNOTATE [gap 9]

**ORIGINAL:**
> `| KB3-RETAIN | Retains all v2 capability wins | **PASS** (CONTR 24/24, HEDGE zero leaks, NEG zero negated-value returns, MULTI 24/24, PARA 48/48, asserted 12/12 both) |`

**CORRECTED:** row kept; correction note inserted after the §1 table (same block as 2a):
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 9] The KB3-RETAIN row above is ANNOTATED: RETAIN is **not** a prereg bar — PREREG3 §6 lists KB3-VIABLE (conjunctive: beats v1 on ≥3/4 sources **AND** retains v2 capability wins), KB3-DET, KB3-NOSILENT, KB3-FALSEHOOD (measurement), KB3-QUALITY (measurement). RETAIN is the retention conjunct reported as a measurement summary; listing it as a separate **PASS** softens the FAIL. **KB3-VIABLE as written FAILS (2/4).** Proposed K18 (forbid splitting conjunctive bars at verdict level) pending signature.`

**Forced by:** Disclosed gap 9 — RETAIN is not a prereg bar (verified: PREREG3 §6 has no KB3-RETAIN; KB3-VIABLE is conjunctive); the split softens the FAIL.

### 2c. §2.1 Ablation deltas, "C4 carried essentially all the improvement" — ANNOTATE [H8]

**ORIGINAL:**
> `**C4 carried essentially all the improvement.** C1 contributed a small gain on 3 sources and **zero on grok**.`
> `C2 moved nothing on the championship (predicted: coreference is near-absent from championship prose) but`
> `fixed the CORE battery 11/24 → 22/24 (§4).`

**CORRECTED:** lines kept; correction note inserted after them:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [H8] The "C4 carried the recovery" headline above is recall-only and ANNOTATED with its precision price: tier-3 wrong-value verdicts rose **8 → 30 per 912 clean probes (0.9% → 3.29%)**, i.e. 22 additional wrong values for ~463 converted unknowns (≈3.6% error on tier-3-resolved probes; §2.2). This precision cost is **unbarred** — no prereg bar constrains it. Proposed N9 (tier-3-introduced wrong-value rate ≤2% on the clean set) pending signature; note the current 3.29% **honest-fails** N9 at ≤2% and passes it at ≤5%.`

**Forced by:** H8 HONEST-FAIL — tier-3 wrong-value rate 8→30/912 (0.9%→3.29%) is unbarred; the 'C4 carried the recovery' headline is recall-only.

### 2d. §9 Decision record, "What carried the recovery" — ANNOTATE [H8]

**ORIGINAL:**
> `- **What carried the recovery**: C4 KEYSOFT tier-3 (+0.30–0.56/source). C1 dense phrasing (+0.00–0.06, zero`
> `  on grok). C2 coref repair (0 on championship, 11/24→22/24 on CORE).`

**CORRECTED:** bullet kept; correction note inserted after it:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [H8] Recall-only headline — annotated with the unbarred precision price in §2.1: tier-3 wrong-value verdicts 8 → 30/912 (0.9% → 3.29%); proposed N9 (≤2% on the clean set) honest-fails at ≤2%, passes at ≤5%.`

**Forced by:** H8 HONEST-FAIL (same as 2c) — the decision-record repetition of the recall-only headline.

---

## 3. `prose-learning/VERDICT.md` (v1) — 3 edits

### 3a. Kill bars, KB-QUALITY row — RESTATE band [F-a]

**ORIGINAL:**
> `| KB-QUALITY | Q = mean(grok,sol) − step; ≥0.02 matters, \|Q\|<0.02 none | Q = 0.8969 − 0.8947 = **+0.0022** → **NO-DIFFERENTIATION**. The numeric-channel result reproduces in prose. |`

**CORRECTED:**
> `| KB-QUALITY | Q = mean(grok,sol) − step; ±0.05 three-bin rule (corrected; proposed C3): Q≥+0.05 matters, \|Q\|<0.05 none, Q≤−0.05 INVERSE | Q = 0.8969 − 0.8947 = **+0.0022** → **NO-DIFFERENTIATION** (\|Q\|<0.05). The numeric-channel result reproduces in prose. |`

plus, after the table:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [F-a] The KB-QUALITY band above is corrected from the prereg's ±0.02 to the **±0.05 three-bin rule** (Q≥+0.05 QUALITY-MATTERS, |Q|<0.05 NO-DIFFERENTIATION, Q≤−0.05 INVERSE): the ±0.02 band sits **below the measurement noise floor** (binomial SE(Q)≈0.024 at n=228; band edge at ~0.8 SE; a true-zero Q escapes the NO-DIFFERENTIATION bin by noise alone ~40% of the time), so the old band could not support a no-differentiation claim. Q=+0.0022 still lands NO-DIFFERENTIATION under the corrected band — outcome unchanged, footing corrected. Proposed C3 pending signature.`

**Forced by:** Noise-floor F-a — the ±0.02 no-diff band sits below the measurement noise floor; any NO-DIFFERENTIATION headline resting on ±0.02 must be corrected to the ±0.05 three-bin rule (INVERSE at Q≤−0.05). Outcome unchanged (0.0022 < 0.05).

### 3b. "Answers to the two mandated questions", #1 — consequential update [F-a]

**ORIGINAL:**
> `1. **Does model quality differentiate when the TNN reads words?** No — per the`
> `   frozen rule, |Q| = 0.0022 < 0.02. The quality hypothesis is refuted in the`
> `   prose channel too, under this pipeline. (Scope: bag-of-stemmed-content-words`
> `   retrieval; a richer comprehension architecture is a different experiment.)`

**CORRECTED:**
> `1. **Does model quality differentiate when the TNN reads words?** No —`
> `   |Q| = 0.0022 < 0.05 under the corrected ±0.05 three-bin rule (proposed C3;`
> `   see the KB-QUALITY correction note above). The quality hypothesis is refuted in the`
> `   prose channel too, under this pipeline. (Scope: bag-of-stemmed-content-words`
> `   retrieval; a richer comprehension architecture is a different experiment.)`

**Forced by:** Noise-floor F-a (same as 3a) — the mandated answer rested on the ±0.02 band.

---

## 4. `coding/CODING_REPORT.md` — 5 edits

### 4a. Kill-Bar Outcomes table, KB-C2 row — RESTATE as FAIL under frozen rule [H7]

**ORIGINAL:**
> `| KB-C2 loop value | Final(A) < 2× Final(B) on T3+T4 → FAIL | A=22, B=12, 2×B=24; 22<24 → **FAIL** (see note) |`

(The table cell already read FAIL; the finding required the FAIL to be stated unambiguously under the frozen rule with the narrowing made explicit.)

**CORRECTED:** row kept; correction note inserted after the table:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [H7] The KB-C2 verdict above is RESTATED as **FAIL under the frozen rule**: KB-C2 (PREREG.md §5) requires final-correct(A) ≥ 2 × final-correct(B) **on T3+T4** — A = 10/10 + 12/12 = 22, B = 0/10 + 12/12 = 12, 2×B = 24 > 22 → the frozen bar FAILS. The "repair loop is essential" framing below narrows the preregistered T3+T4 rule to T3 only and was made **without a dated amendment**; it is retained as a measurement summary (T3 10/10 vs 0/10; T4 12/12 both arms), not as the bar verdict. Proposed N15 pending signature.`

**Forced by:** H7 HONEST-FAIL — the report narrowed the preregistered T3+T4 rule to T3 only; under the frozen rule (PREREG.md §5: "final-correct(A) < 2 × final-correct(B) on T3+T4 → the repair loop adds nothing → FAIL the speed claim") A=22, B=12, 2×B=24 > 22 → FAIL. The narrowing was done without amendment.

### 4b. "KB-C2 note (honesty clause)" — narrowing made explicit [H7]

**ORIGINAL:**
> `**KB-C2 note (honesty clause):** The repair loop is ESSENTIAL for T3 (10/10 vs 0/10`
> `baseline — the baseline's single repair shot cannot fix the 10 broken items), but the`
> `prereg bar measures T3+T4 combined. Since T4 needs no repair (12/12 both arms), the`
> `combined 22 vs 12 does not reach the 2× threshold (24). The loop adds decisive value`
> `for repair tasks; it adds nothing for generation tasks that already pass first-try.`

**CORRECTED:**
> `**KB-C2 note (honesty clause):** The frozen KB-C2 rule measures **T3+T4 combined** and the verdict is **FAIL** (22 < 24) — see the correction note above. What follows narrows the frozen rule to T3 only, done **without a dated amendment**, and is a measurement summary, not the bar verdict: the repair loop is ESSENTIAL for T3 (10/10 vs 0/10`
> `baseline — the baseline's single repair shot cannot fix the 10 broken items), but since T4 needs no repair (12/12 both arms), the combined 22 vs 12 does not reach the 2× threshold (24). The loop adds decisive value`
> `for repair tasks; it adds nothing for generation tasks that already pass first-try.`

**Forced by:** H7 HONEST-FAIL (same as 4a).

### 4c. Key Finding #2 — pointer [H7]

**ORIGINAL:**
> `2. **Repair loop is essential for T3**: Baseline (single repair shot) vs loop shows the`
> `   loop matters. All 10 T3 items require at least one repair; the loop achieves 10/10.`

**CORRECTED:** appended pointer: `(T3-only measurement summary — the frozen KB-C2 rule is T3+T4 and **FAILS**; see the [H7] correction note under Kill-Bar Outcomes.)`

**Forced by:** H7 HONEST-FAIL (same as 4a) — the finding is the T3-narrowed framing.

### 4d. Kill-Bar Outcomes table, KB-C5 row — ANNOTATE [F-b]

**ORIGINAL:**
> `| KB-C5 memorization | T4m < T4 − 30pp → FAIL | T4m 4/4 = 100%, T4 12/12 = 100% → PASS |`

**CORRECTED:** row kept; correction note inserted after the table (same block as 4a):
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [F-b] The KB-C5 **PASS** above is annotated with a granularity limitation: with n=4, each T4m item is **25pp**, so the 30pp band **cannot resolve a single failure** — 3/4 = 75% ≥ 70% (T4 − 30pp) still passes. The observed 4/4 = 100% passes the bar as written, but the bar is too coarse at this n to detect one memorization failure. Proposed C7 (n≥8, band 10pp) pending signature.`

**Forced by:** Noise-floor F-b — KB-C5 (T4m ≥ T4−30pp) with n=4 → 25pp/item; the 30pp band cannot resolve a single failure (75% still passes). (PREREG.md §5: "T4m correct < T4 correct − 30pp → memorization flagged"; §3: T4m n=4.)

### 4e. Key Finding #3 — pointer [F-b]

**ORIGINAL:**
> `3. **Generalization, not memorization**: T4m (mutated constants/sizes) scores 4/4,`
> `   identical to T4. The learner applies concepts parametrically.`

**CORRECTED:** appended pointer: `(Granularity caveat: at n=4 the KB-C5 30pp band cannot resolve a single failure; see the [F-b] correction note under Kill-Bar Outcomes.)`

**Forced by:** Noise-floor F-b (same as 4d).

---

## 5. `dialogue/VERDICT.md` — 2 edits

### 5a. "Understand vs Repeat" verdict — ANNOTATE [gap 10]

**ORIGINAL:**
> `**Verdict: TNN understands what's happening in the dialogue.** It does not`
> `merely repeat; it composes novel answers from multi-turn state.`

**CORRECTED:** lines kept; correction note inserted after them:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 10] The novelty claim above is ANNOTATED: COMPOSE-NOVEL is **self-attested** — the binary asserts the compose response is not a substring of any KB fact or prior turn and prints \`COMPOSE-NOVEL=1\` per its own check (PREREG.md novelty control); the independent oracle (\`verify_dialogue.py\`) consumes the binary's own novel flag and checks outputs against KB facts, it does **not** independently verify novelty. The "understands, doesn't merely repeat" headline therefore rests on a binary-asserted flag, not oracle-verified novelty. Proposed N14, and K17 (promote to kill bar ≥24/28 with independent oracle novelty verification), pending signature.`

**Forced by:** Disclosed gap 10 — COMPOSE-NOVEL is self-attested; the oracle does not independently verify novelty (verified: PREREG.md "Novelty control: the binary asserts the compose response is not a substring of any KB fact text or any prior turn text, and prints `COMPOSE-NOVEL=1` per compose turn"; `verify_dialogue.py` §5 reads the binary's `novel` flag).

### 5b. Conclusion — pointer [gap 10]

**ORIGINAL:**
> `contradictions, and — crucially — **composes novel answers from multi-turn`
> `state**. It understands what's happening; it does not merely repeat.`

**CORRECTED:** lines kept; correction note inserted after them:
> `> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 10] The "composes novel answers" claim above is binary-asserted, not oracle-verified — see the correction note under "Understand vs Repeat". Proposed N14 and K17 (kill bar ≥24/28 with independent oracle novelty verification) pending signature.`

**Forced by:** Disclosed gap 10 (same as 5a) — the Conclusion repeats the headline.

---

## Cross-check of all other bars (audit-missed slack/zero-margin sweep)

Every other bar cited in the five documents was sanity-checked against its frozen prereg. No >10x-slack or zero-margin issue the audit missed was found; no further correction was warranted:

- v1: KB-EXTRACT (≥0.99; observed 1.0000, gate by design), KB-PROSE-VIABLE (≥0.98; **trips** honestly on all four sources), KB-DETERMINISM (5/5 byte-identical; exact by nature), KB-FALSEHOOD (12/12 measurement, factual).
- v2: KB2-VIABLE (228/228; **FAILS** decisively and honestly), KB2-DET (5/5 + 3/3 byte-identical), SUB-PARA 48/48 (bar ≥46/48, margin 2), SUB-CONTR 24/24 exact, SUB-MULTI 24/24 (bar ≥22/24, margin 2), SUB-CORE 11/24 and SUB-DISTR 65/240 (**FAIL** honestly).
- v3: KB3-VIABLE (**FAIL** 2/4, honest), KB3-NOSILENT (exact-count, audit §5), KB3-BYTEID 5/5 (label differs from prereg's KB3-DET but the criterion text is identical — cosmetic, no narrowing), ABS-3 and Q (measurement-only), §2.2 precision figures (factual).
- coding: KB-C1 (12/12 vs <50% fail threshold; coarse gate by design), KB-C3 (5/5 byte-identical), KB-C4 (6/6 refused; critical bar, full set).
- dialogue: every-turn-type ≥70% (min 96.7%), weird-gap ≤30pp (3.3pp), 5/5 byte-identical.

**Flagged for the parent (out of mandate, not corrected):** v2's KB2-QUALITY (Q = −0.0570, "unbinned negative") is not a NO-DIFFERENTIATION headline so F-a did not apply to it, but if proposed C3 (±0.05 three-bin) is signed, −0.0570 ≤ −0.05 lands in the INVERSE bin — a verdict-affecting re-binning the parent may want annotated in `prose-learning/v2/VERDICT.md` §5. Left untouched per the F-a scope ("v1 — only").

---

## Counts

| Document | Edits |
|---|---|
| `prose-learning/v2/VERDICT.md` | 6 (H6×2 annotate, gap-13×2 restate+retract, gap-13 pointer update, gap-14 annotate) |
| `prose-learning/v3/VERDICT.md` | 4 (gap-7 bar-status, gap-9 annotate, H8×2 annotate) |
| `prose-learning/VERDICT.md` (v1) | 3 (F-a band restate + note + mandated-answer update) |
| `coding/CODING_REPORT.md` | 5 (H7×3 restate+explicit+pointer, F-b×2 annotate+pointer) |
| `dialogue/VERDICT.md` | 2 (gap-10 annotate + pointer) |
| **Total** | **20 edits across 5 files** |

Retractions: 1 (v2 §4 discrepancy flag, per GATE0). Restatements: 4 (v2 §4 headline, v1 KB-QUALITY band, coding KB-C2, v3 oracle bar-status). Annotations: 15. Measured values/evidence deleted: **none** — all corrections qualify claims only.

==================== CREW D LEDGER ====================

# DOC-SWEEP Crew D — Claims Report

**Crew:** D (front docs + cross-check) · **Date:** 2026-09-22 · **Bar-audit:** commit `abaa5c7b57b6` (`redteam/bar-audit/BAR_AUDIT.md`)
**Working dir:** `~/workspace/tnn-lab/` · **No commits made** (per task).

---

## 1. Front-doc claims touched

Six claims corrected across the two front docs. All corrections use the mandated format
`> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** …` and were verified by
re-reading the edited sections. No measured values were deleted — only qualified.
Corrections were placed immediately below the table/paragraph containing the claim
(tables can't hold blockquotes without breaking), each naming the row it qualifies.

### 1a. `docs/lab/FINDINGS_2026-09-21.md` — Data scale-up row (T2 + T3) — ANNOTATE

- **Section:** "Scaling: two nulls that are actually the finding", Data scale-up row
- **ORIGINAL:** "240 → 6,585,360 facts: clean mastery 1.0 at every leg; exactly 4.000 ops/fact, 92 B/fact, linear cost; zero horizon gap (first decile = last decile); no kill bar tripped. Stopped at the corpus ceiling, not a learner failure."
- **Forcing bars:** T2 KB-SCALING (threshold 2.00pp, measured 0.00pp, slack ∞ — tolerates 125,137 wrong facts at N=6,585,360); T3 KB-FORGET (threshold 3.00pp, measured 0.00pp, slack ∞ — tolerates ~187,700 forgotten early facts).
- **Corrected text (inserted below the table):** "no kill bar tripped" is qualified: the two bars behind it are tripwires with infinite slack. "Clean mastery 1.0" and "zero horizon gap" are the measured values, exact to the battery's resolution — the bars could not have failed short of six figures of wrong/forgotten facts.

### 1b. `docs/lab/FINDINGS_2026-09-21.md` — Parameter scale-up row (H2) — ANNOTATE

- **Section:** "Scaling: two nulls that are actually the finding", Parameter scale-up row
- **ORIGINAL:** "…Under-capacity degrades exactly proportionally and gracefully. No emergent capability."
- **Forcing bar:** H2 — the flaw battery at reduced configs scores 96/96 while sampling ids in [0, n/4) only; blind to capacity loss beyond 4×; audit verdict: mark reduced-config readings DEGRADED (honest-fail on table presentation).
- **Corrected text (inserted below the table):** "degrades exactly proportionally and gracefully" is qualified: the flaw battery behind reduced-config readings is a coverage artifact — "graceful" describes the probed quarter of the id range, not the full store.

### 1c. `docs/lab/FINDINGS_2026-09-21.md` — Web-search sense v2 row (T4 pattern) — ANNOTATE

- **Section:** "What *does* buy capability", Web-search sense v2 row
- **ORIGINAL:** "All legs PASS on the live web: utility 20/20, spoof resistance 6/6, teacher-check 12/12, discipline 12/12, install modes 24/24, rules 24/24, standing sense 4/4. … Residual: unanimous multi-source spoof remains sensor-deceivable."
- **Forcing bar:** T4 (info-source KB-SPOOF-RESIDUAL, unfailable by construction) — the v2 battery carries the same pathology: `senses/web-search/v2/PREREG.md` excludes the M5–M6 unanimous-spoof residual from KB-MODE-RW ("both rules may install; counted separately, not as a bar failure"); verdict records "7 INSTALL (residual) | 7 INSTALL (residual)" as the expected outcome.
- **Corrected text (inserted below the table):** "spoof resistance 6/6" covers the B-live single-domain-spoof leg only (bar 6/6, exact). The unanimous-spoof residual cannot fail — it is a documented-by-design install. "Spoof resistance" covers single-domain spoof only.

### 1d. `TNN_VS_LLM_CAPABILITY_DRAFT.md` — Data row (T2) — ANNOTATE

- **Section:** "Parameters buy nothing (2026-09-21, measured)", Data axis row
- **ORIGINAL:** "mastery 1.0 throughout; exactly 4 ops/fact, 92 B/fact, linear cost"
- **Forcing bar:** T2 KB-SCALING (threshold 2.00pp, measured 0.00pp, slack ∞ — tolerates 125,137 wrong facts at N=6,585,360).
- **Corrected text (inserted below the table):** "mastery 1.0 throughout" is the measured value; the bar behind it has infinite slack — "1.0" is exact to the battery's resolution; the bar could not have failed short of six figures of wrong facts.

### 1e. `TNN_VS_LLM_CAPABILITY_DRAFT.md` — "graceful" paragraph (H2) — ANNOTATE

- **Section:** "Parameters buy nothing (2026-09-21, measured)", paragraph after the table
- **ORIGINAL:** "Below it, degradation is exactly proportional and graceful — what fits stays perfect."
- **Forcing bar:** H2 (same as 1b: reduced-config 96/96 samples ids in [0, n/4) only; coverage artifact; mark DEGRADED).
- **Corrected text (inserted below the paragraph):** "graceful" is qualified — "what fits stays perfect" describes the probed quarter of the id range, not the full store.

### 1f. `TNN_VS_LLM_CAPABILITY_DRAFT.md` — Long-horizon stability row (T2 + T3) — ANNOTATE

- **Section:** "How to read this", capability-map table, Long-horizon stability row
- **ORIGINAL:** "Long-horizon stability: no degradation at 100x the training horizon"
- **Forcing bars:** T2 KB-SCALING (trip iff mastery drop >2pp; measured 0.00pp; tolerates 125,137 wrong facts at N=6,585,360) + T3 KB-FORGET (trip iff last−first decile gap >3pp; measured 0.00pp; tolerates ~187,700 forgotten early facts).
- **Corrected text (inserted below the table):** "no degradation" means none detectable within the battery's resolution, not absolute absence.

### Checked, no hit (front docs)

- "Pure Zag, zero randomness in decision paths, byte-identical reruns unless noted." (`FINDINGS` line 4) — standing program-law/process statement, not a claim resting on an audited kill bar. No edit.
- "Learn without forgetting … (our churn-freeze finding is the honest version of this problem, under test)" (DRAFT line 86) — strength-trial mechanism claim, already qualified "under test"; does not rest on KB-FORGET. No edit.
- Wave-5 memory numbers in the DRAFT map (58/58 deliberate memory, 100/100 recall, 64/64 corruption, 18/18 revision, 2,595 refusals, 180/180 revision, byte-identical replay) — not among the ~70 audited bars; no audit finding forces a correction. No edit.
- Prose-v1 Q=+0.0022 NO-DIFFERENTIATION + source ranking (`FINDINGS` line 30) — KB-QUALITY band ±0.02 sits below the noise floor (SE(Q)≈0.024, audit flag F-a), but measured |Q|=0.0022 ≪ the audit's corrected ±0.05 band, so the refutation verdict is robust under the corrected bar. No edit (see §3).
- "Prose v1 viability tripped on all four sources" / senses-rebuild false-install ceilings / "Honest limit: single-source smooth lies … absorbed 12/12" — already honest fail/limit statements backed by tight bars (audit §7.3: v1/v2/v3 VIABLE all tripped; bars working). No edit.
- No MATRIX.md exists anywhere in the repo (full-tree `find` returned nothing). README.md files checked: 6 of 17 mention "byte-identical" but only procedurally (rerun reproducibility, fixture regeneration — the audit's procedure tier, correctly read as anti-cheat, not capability evidence); none state claims resting on the 4 tripwires or 8 honest-fails. No edits.

---

## 2. Mirror staleness hits (read-only scope — NOT edited; for coordinator sync)

| # | File | Claim quote | Needed canonical correction |
|---|---|---|---|
| M1 | `docs/lab/prose-learning/v3/VERDICT.md:40` | "**C4 carried essentially all the improvement.** C1 contributed a small gain on 3 sources and **zero on grok**." | H8: the headline is recall-only; tier-3 introduced 22 additional wrong-value verdicts (8→30/912, 0.9%→3.29% precision price), unbarred — retroactive HONEST-FAIL at ≤2%. Mirror is currently byte-in-sync with canonical `prose-learning/v3/VERDICT.md` (diff clean), so crew C's canonical correction will land here too — flag for sync after crew C edits. (Also line 161: "**What carried the recovery**: C4 KEYSOFT tier-3 (+0.30–0.56/source)" — same headline, same fix.) |
| M2 | `docs/lab/prose-learning/v3/VERDICT.md:53,139` | "Precision cost of tier-3 (912 clean probes): wrong-value verdicts A1 = 8 → A3 = 30, while…" | Discloses the H8 numbers but without the honest-fail framing; needs the canonical H8 verdict language (retroactive HONEST-FAIL at ≤2%, passes at ≤5%). Sync with crew C. |
| M3 | `docs/lab/redteam/battery-design/BLIND_SPOT_MAP.md` (H6, CAN-see column) | "No degradation over horizons (the standing expectation, holding)" and "Storage fidelity at scale: 1.0000 from N=1 to N=6,585,360, exactly linear cost, byte-identical reruns." | Needs the T2/T3 tripwire qualifiers per canonical scale corrections: KB-SCALING tolerates 125,137 wrong facts (∞ slack), KB-FORGET tolerates ~187,700 forgotten early facts (∞ slack). "Holding" and "1.0000" are measured values exact to battery resolution, not bar-verified absolutes. |
| — | `docs/lab/redteam/battery-design/BATTERY_HEALTH_AUDIT.md` (A9), `RANKED_ATTACKS.md` (#5, #9) | — | CLEAN: these already contain the bar-audit-consistent critiques (fewshot 96/96 degeneracy: "effective resolution (24) should be stated wherever 96/96 is quoted"; §B.7 form-not-content with laundering-into-hits). They are the source of the flags, not stale mirrors. |
| — | `docs/lab/units/arms/{B-8,E,I2,K2,M,M2,P,R2,Z3}/VERDICT.md` | — | CLEAN: no hits on any claim family (grep: no degradation / no kill bar / spoof / 96/96 / self-test / KB-* / cobra / §B.7 / overhead). |
| — | `docs/lab/scale/` | — | No files present (empty mirror directory). Nothing to sync. |
| — | `redteam/independent-battery/VERDICT.md` | — | CLEAN (new): bars are tight and one actually tripped — KB-GAP(para) TRIPPED (0.8816 > 0.30), reclassifying the old 0.9649 paraphrase headline as GENERATOR-COUPLED; KB-TRUTH "truthful" qualifier is 0.6667 vs a 0.5000 mirror baseline (measured comparison, not a tripwire). No claim rests on the 4 tripwires. |
| — | `dialogue/morphology/VERDICT.md` | — | CLEAN (new): exact-equality bars throughout (370/370, 5/5 byte-identical digest `35aaae8a…`). No claim rests on the audited bars. |

---

## 3. Cross-check results (bars cited in front docs: threshold vs measured)

Slack rule: >10× = tripwire; ∞ = measured 0 against a >0 allowance.

| Bar (front-doc claim) | Threshold | Measured | Slack | Result |
|---|---|---|---|---|
| KB-SCALING (`FINDINGS` data row; DRAFT Data row) | 2.00pp | 0.00pp | **∞** (>10×) | Audit-flagged T2; corrected (§1a, §1d). Tolerates 125,137 wrong facts at N=6,585,360. |
| KB-FORGET (`FINDINGS` "zero horizon gap"; DRAFT "no degradation at 100x") | 3.00pp | 0.00pp | **∞** (>10×) | Audit-flagged T3; corrected (§1a, §1f). Tolerates ~187,700 forgotten early facts. |
| KB-SPOOF-RESIDUAL, info-source (T4) | unfailable by construction | reproduced | unfailable | Audit-flagged; not directly cited in front docs. |
| v2 M5–M6 unanimous-spoof residual (`FINDINGS` v2 row) | excluded from KB-MODE-RW by construction ("counted separately, not as a bar failure") | 7 INSTALL expected-and-installed | **unfailable** | **NEW flag (audit missed — same pathology as T4, not in audit's tables); corrected (§1c).** |
| B-live spoof leg (`FINDINGS` v2 row "spoof resistance 6/6") | 6/6 | 6/6 | 1.0× exact | OK — tight. |
| A-live utility (`FINDINGS` v2 row) | 20/20 + baseline | 20/20 | 1.0× exact | OK — tight. |
| C-live teacher-check (`FINDINGS` v2 row) | ≥9/12 | 12/12 | 1.333× | OK — tight. |
| D-live discipline (`FINDINGS` v2 row) | ≥11/12 | 12/12 | 1.09× | OK — tight. |
| M mode battery / R rule battery / S standing sense (`FINDINGS` v2 row) | 24/24 / per-matrix / 4/4 | 24/24 / 24/24 / 4/4 | 1.0× exact | OK — tight. |
| KB-P-DET (`FINDINGS` params row "16/19 byte-identical"; DRAFT params row) | 0 diffs, 19/19 | 0 | exact | OK. |
| KB-P-GRACE (DRAFT "graceful" context) | mastery 1.0 at 0.5× | 1.0 (also at 0.25×) | exact | OK — but the *interpretation* "graceful" rests on the H2 coverage artifact; corrected (§1b, §1e). |
| KB-QUALITY ±0.02 band (`FINDINGS` prose-v1 "Q=+0.0022, frozen NO-DIFFERENTIATION") | ±0.02 | +0.0022 | 9.09× headroom, but band edge at ~0.8 SE (audit F-a noise floor) | **Checked, no correction:** measured |Q|=0.0022 ≪ audit's corrected ±0.05 band — the refutation verdict is robust under the corrected bar. |
| KB-ST-OVERHEAD (T1) | ≤2.0 | 0.0127 | **157×** (>10×) | Audit-flagged, but **no front-doc claim rests on it** — neither front doc mentions self-test. No correction needed. |
| KB-PD-FA (mechanical ∞) | ≤0.05 | 0/26 | ∞ mechanical (effective slack 1.3 items) | Not in front docs. No correction needed. |
| Noisy-teacher §B.7 wrong-target pathology (H4/H5; bar PROPOSED-never-frozen) | — | — | — | **Not cited in front docs** (grep for `§B.7`/`B.7`/`noisy` returned nothing in either file). No correction needed. |

**New >10x/zero-margin flags the audit missed:** exactly one — the web-search v2 M5–M6 unanimous-spoof residual, unfailable by construction (same pathology as T4). It was corrected in §1c. All other front-doc bars are ≤1.34× slack or exact.

**Not in front docs (no sweep obligation, noted for completeness):** H1 (cobra/F45 — not in front docs), H3 (fewshot 96/96* — `FINDINGS` only says "TBD"), H4/H5 (noisy-teacher — not in front docs), H6 (prose-v2 hedged — `FINDINGS` says "running"/"TBD"), H7 (coding KB-C2 — not in front docs), H8 (prose-v3 tier-3 precision — not in front docs; mirror hit M1/M2 filed above).

---

## Counts

- Front-doc claims corrected: **6** (3 in `docs/lab/FINDINGS_2026-09-21.md`, 3 in `TNN_VS_LLM_CAPABILITY_DRAFT.md`) — all ANNOTATE (measured values kept, claims qualified).
- README.md / MATRIX.md edits: **0** (no MATRIX.md exists; 6 READMEs with byte-identical mentions are procedural only).
- Mirror staleness hits: **3 actionable** (M1/M2 prose-v3 "C4 carried the recovery" → needs crew C's H8 correction; M3 BLIND_SPOT_MAP H6 "No degradation over horizons" → needs T2/T3 qualifiers); 5 mirror files/groups clean; `docs/lab/scale/` empty.
- New verdicts verified clean: `redteam/independent-battery/VERDICT.md`, `dialogue/morphology/VERDICT.md` — no stale claims on the audited bars.
- Cross-check: **1 new flag** the audit missed (v2 M5–M6 residual unfailable-by-construction, same pathology as T4) — corrected; all other front-doc bars tight (≤1.34×) or exact.
- Commits: **0** (per task).
