# INDEPENDENT BATTERY V2 — VERDICT

**Crew:** independent-battery-v2 · **Date:** 2026-09-21/22
**Parent order (Micah):** implement the GOODS of the red team, not the bars — remove
every bar the red team proved illegitimate; write v2 as the ongoing standard.
**Artifacts:** `PROTOCOL_V2.md` (the standard, PROPOSED — needs Micah's dated
signature to become law), `rescore_v2.py` + `SCORES_V2.md` (mechanical calibration),
`CALIBRATION.md` (human calibration record).

## Bars removed (with the evidence that forced each removal)

| # | Removed | Evidence |
|---|---|---|
| R1 | KB-GAP(para) vs 0.9649 | v1 VERDICT's own correction: 0.9649 was Sol's clean-mastery on canonically-worded facts, never a paraphrase measurement. A gap against a non-measurement is uninterpretable. |
| R2 | AFFIRM/REJECT-expected on wire-undecidable truth probes (v1: 138/139/142, 140/141) | Wrong-target pathology (BAR_AUDIT.md §1d): verdicts demanding unknowable knowledge measure policy-luck. V1's "generator-severity note" on probe 142 admitted the AFFIRM required identifying the planted lie — unknowable from the wire. |
| R3 | Bare round-number thresholds (KB-GAP's ungrounded 0.30) | Bar-audit bar-setting rule: thresholds grounded, never round numbers; every bar carries slack. |
| R4 | Directional-only KB-TRUTH with no margin accounting | 2-item directional hold at n=12 (~1.2 SE) can't separate robust from fragile; margins required on every bar. |

## Bars kept and hardened

| Bar | v2 form |
|---|---|
| KB-GAP | Grounded: trip iff gap > max(2×SE_binom, 2/n); coupled-comparability rule enforced (same-capability baseline or no gap bar). |
| KB-TRUTH | Margin-reported on the cleaned axis; margin < 2 items → HOLD (FRAGILE) with mandatory re-run at n≥16. |
| KB-DET / KB-NOLEAK / KB-PARSE | Kept as the validity tier — labeled anti-cheat, not capability evidence (BAR_AUDIT.md §1e). |

## Goods kept (the red-team goods, not the bars)

Process-separated authorship · sealed protocol · disjoint vocabulary AND schemas ·
undisclosed corruption rate · truth-grounded scoring with mirror baseline ·
abstention + provenance scoring · byte-identical reruns · plus v1 lessons now
structural: paraphrase as a first-class axis with SYN/SYNT split scoring (§3),
detectability classification (§1.7), wire-decidability audit (§5), granularity and
noise-floor rule (§6), unscored floor axis (§4).

## Calibration result: do the v1 scores survive cleaned scoring?

| Axis | v1 | v2 | Verdict |
|---|---|---|---|
| contra | 1.0000 | 1.0000 (surface 8/8, mediated 4/4) | SURVIVES — both strata real |
| false | 1.0000 | 1.0000 (D3 6/6, D4 6/6) | SURVIVES — both strata real |
| para | 0.0833 | 0.0833 SYN; SYNT unmeasured | NUMBER SURVIVES as inaugural absolute; "syntactic survives" sub-claim WITHDRAWN (stratum was empty) |
| truth | 0.6667 | 0.8571 (FRAGILE) | SCORE CHANGES — up in number, down in certainty; re-run at n≥16 required before "truthful" is cited robust |
| abstain / prov | 1.0000 | 1.0000 | SURVIVE unchanged |

Two findings the v1 scoring could not see:
1. **Guess-on-undecidable vice (ABS-C 0/3):** on wire-undecidable inter-claim
   conflicts the learner picks a side (reject-on-conflict) instead of abstaining.
   V1's scoring counted two of these as hits — policy-luck, not truth-tracking.
2. **Quantified floor (0/2):** both smooth lies affirmed — irreducible from the wire,
   reported as the honest boundary, deliberately unbarred.

## What this means for the program's headlines

- "Contradiction 1.0000 and falsehood 1.0000 are real capabilities" — CONFIRMED under
  cleaned scoring with strata splits. These survive the red-team goods.
- "Paraphrase 0.0833" — CONFIRMED as the inaugural absolute reading, but its scope
  narrows to synonym-swaps; syntactic paraphrase remains UNMEASURED anywhere in the
  program. The next independent run must fill the SYNT stratum.
- "Truthful (0.6667 > 0.5000 mirror)" — SUPERSEDED by "truthful on wire-decidable
  probes, 0.8571 vs 0.7143 mirror, HOLD (FRAGILE)". The qualifier survives; the
  robustness claim does not yet exist. Next run at n≥16 decides it.
- New standing vice to fix: the learner guesses sides on undecidable conflicts. A
  truth-tracking learner must abstain there. This is now a measured, bar-backed
  requirement (ABS-C stratum), not a suspicion.

## Open items requiring Micah

1. **Signature:** `PROTOCOL_V2.md` is PROPOSED. It becomes the binding "independent"
   label standard only on his dated signature (same for the bar-audit's
   `PROPOSED_BARS.md` — the two proposals are consistent: v2 implements the audit's
   bar-setting rule).
2. **Next independent run** at v2 (n≥16 truth axis, filled SYNT stratum, §1.7
   detectability classification at generation time) — needed to de-fragile the truth
   claim and to measure syntactic robustness for the first time.
3. The ABS-C vice (guess-on-undecidable) is a repair target for the mechanism crews.

## Reproduction

- `rescore_v2.py` re-derives `SCORES_V2.md` from the committed v1 data
  (`../items.jsonl`, `../expected.json`, `../runs/runN.log`); deterministic.
- V1 battery SHA: see `../SHA256SUMS`. V2 protocol SHA: see `v2/SHA256SUMS`.
