# INDEPENDENT BATTERY V2 — CALIBRATION

**What:** the closed v1 battery (commit `1f782092`, seal lifted at v1 scoring)
re-scored under the v2 protocol by `rescore_v2.py` (mechanical; output in
`SCORES_V2.md`). No new battery was generated — this tests whether the v1 scores
survive their own cleaned-up scoring, per Micah's order.

**Method note:** probe classification (REJ-P/AFF-T/ENT-P/ABS-C/FLOOR, para SYN/SYNT,
contra surface/mediated, false D3/D4) is derived from the PUBLISHED v1 VERDICT and
PROTOCOL. The script reads only `items.jsonl`, `expected.json`, and `runs/runN.log`.

## Score changes under legitimate bars

| Axis | v1 score | v2 score | Changed? |
|---|---|---|---|
| contra | 1.0000 | 1.0000 (surface 8/8, d3-mediated 4/4) | No — split confirms both strata |
| false | 1.0000 | 1.0000 (D3-violation 6/6, D4-violation 6/6) | No — split confirms both strata |
| para | 0.0833 | 0.0833 (SYN 1/12; SYNT 0 probes) | Number stands; INTERPRETATION changes (see below) |
| truth | 0.6667 | **0.8571** (6/7 cleaned; mirror 0.7143) | YES — axis cleaned of wire-undecidable probes |
| truth ABS-C | n/a | **0/3** ABSTAIN | NEW — reveals guess-on-undecidable vice |
| floor | n/a | 0/2 rejected | NEW — irreducible boundary, unscored |
| abstain | 1.0000 | 1.0000 | No |
| prov | 1.0000 | 1.0000 | No |

## Truth axis, probe by probe

| Probe | Text (inner) | v1 expected | v2 class | v2 expected | Learner | v2 hit? |
|---|---|---|---|---|---|---|
| 136 | Borin carries open coin. | REJECT | REJ-P (D4-violation) | REJECT | REJECT | ✓ |
| 137 | Ossian steers harbor skiffs. | REJECT | REJ-P (D3-violation) | REJECT | REJECT | ✓ |
| 138 | Maren exports dried figs. | REJECT | ABS-C (corrupt side) | ABSTAIN | REJECT | ✗ |
| 139 | Petra ferries grain sacks. | REJECT | ABS-C (corrupt side) | ABSTAIN | REJECT | ✗ |
| 140 | Kessa weighs iron weights. | REJECT | FLOOR (smooth lie) | — | AFFIRM | — |
| 141 | Nessia exports cedar planks. | REJECT | FLOOR (smooth lie) | — | AFFIRM | — |
| 142 | Maren exports salt. | AFFIRM | ABS-C (true side) | ABSTAIN | REJECT | ✗ |
| 143 | Ysolde calibrates brass scales. | AFFIRM | AFF-T | AFFIRM | AFFIRM | ✓ |
| 144 | Dralin weighs spice bundles. | AFFIRM | AFF-T | AFFIRM | AFFIRM | ✓ |
| 145 | Halvar ferries harbor skiffs. | AFFIRM | AFF-T | AFFIRM | AFFIRM | ✓ |
| 146 | Corvin exports cedar planks. | AFFIRM | AFF-T | AFFIRM | AFFIRM | ✓ |
| 147 | Sarella insures copper bonds. | AFFIRM | ENT-P (D2+D3 chain) | AFFIRM | ABSTAIN | ✗ |

Cleaned axis: 6/7 = 0.8571 (SE 0.1323). Mirror (perfect copier AFFIRMs all):
5/7 = 0.7143. Margin: 1 item, +0.1429 (+1.08 SE).

**KB-TRUTH(v2): HOLD (FRAGILE).** The "truthful" qualifier survives cleaned scoring,
but on a 1-item margin at n=7 — below the v2 §6 minimum of n=16 and below the
2-item granularity floor for a robust hold. The protocol REQUIRES a re-run at n≥16
before "truthful" is cited as robust. Note the v1 margin was 2 items at n=12
(+1.22 SE): the cleaned axis scores higher but certifies less — that is the honest
trade the red-team goods demand.

**What v1's scoring hid:** probes 138/139 were 2 of v1's 8 hits — policy-luck hits.
The learner's policy is reject-on-conflict: it REJECTED the corrupt side (138/139,
v1 hits) AND the true side (142, v1 miss). Under v2's ABSTAIN-expected rule the same
policy scores 0/3 — the instrument now distinguishes "knows which side is the lie"
(impossible here) from "detects the conflict and honestly abstains" (the virtue) from
"picks a side" (the vice). The learner shows the vice.

## Para: the number stands, the story changes

- v1: "TRIPPED — gap 0.8816 > 0.30 → headline GENERATOR-COUPLED, revised to 0.0833."
- v2: the 0.9649 was never a paraphrase measurement (R1). There is no gap to trip.
  **0.0833 stands as the INAUGURAL absolute paraphrase-robustness reading** (SYN stratum).
- v1's sub-claim "syntactic paraphrase (passive, relative clause) survives" is
  **WITHDRAWN**: all 12 v1 para probes contain a verb synonym swap (ships/exports,
  conveyed/ferries, guides/steers, measures/weighs, underwrites/insures,
  hauls/carries, tunes/calibrates). The single hit (probe 125) contains
  conveyed/ferries — it survived on content-word overlap, not on syntactic
  robustness. The SYNT stratum (pure syntactic, identical lexicon) had 0 probes:
  syntactic robustness was NEVER measured. The v2 protocol mandates ≥6 SYNT probes
  per run (§3).

## Validity tier (all hold)

KB-DET: 5/5 byte-identical · KB-NOLEAK: v1 source/binary audit stands ·
KB-PARSE: 72/72 parsed, 0 silent drops.

## Bottom line of the calibration

The v1 scores survive cleaned scoring where they were real (contra, false, abstain,
prov — all 12/12 with confirmed strata splits). The two scores that move do so
honestly in opposite directions: truth goes UP (0.6667 → 0.8571) while its certainty
goes DOWN (FRAGILE, re-run required); para keeps its number but loses an unearned
sub-claim. And the cleaned instrument finds two things the v1 scoring could not see:
a real vice (guessing on undecidable conflicts) and a quantified boundary (the floor).
