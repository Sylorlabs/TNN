# SI-A1 resolution run — fresh-battery epistemic replication (2026-09-22)

Addendum SI-A1 (commit `96d2a3c358d15c3da56cea9b212df839cf4d8aa2`,
frozen before any resolution run). Frozen prereg `43eceed21` §3e
unchanged — no bar, clause, or verdict rule touched.

## Resolution verdict: PLATEAU-CONFIRMED

The epistemic plateau replicates on the fresh, disjoint 94-item battery:
29/94 → 59/94 → 59/94 → 59/94 — identical to the frozen battery's curve.
- gain(1x→2x) = 31.9pp > 10pp ✓
- gain(2x→4x) = 0pp ≤ 1pp ✓
- gain(4x→8x) = 0pp ≤ 1pp ✓

Per the preregistered reporting rule: **epistemic plateau replicates;
knee at 2x confirmed; Arm 1 verdict remains PARTIAL per frozen §3e
strict clause (a). Relaxing the strict clause needs Micah-signed
amendment.** Flagged to Micah as an amendment candidate (his call) —
the rule was NOT rewritten here.

## Fresh battery

`work_a1r/epi/`: `b12_false.txt` (12), `b12_true.txt` (12), `c70.txt` (70),
plus `battery_a1r_items.json` (item list with intended fires/correct
verdicts) and the construction script `gen_battery_a1r.py` (committed).

- 94 new IDs, 0 overlap with the frozen 94 (asserted programmatically):
  F901–F912, BC13–BC24, W141–W210 (joke 141–150, sarcasm 151–160,
  hypothetical 161–170, analogy 171–180, poetry 181–190,
  counterfactual 191–200, implicature 201–210).
- Same construction procedure: 12 falsehoods (false world claims the
  delib can verify), 12 true controls (true, no predicate fires),
  7 families × 10 weird-English with the same balanced design
  (per-family matcher-fire balance mirrors the frozen battery:
  joke 5, sarcasm 3, hypothetical 5, analogy 3, counterfactual 9,
  poetry 5, implicature 5 of 10 fire).
- Construction audit (Python mirror of delib_si.zag trigger lists, run
  before the sweep): all 94 items fire exactly their intended
  predicates; 35/70 W items fire a nonfactual predicate.
- Documented constraint: delib_si.zag is UNCHANGED, so its knowledge
  triggers (is_known_false/is_absurd phrases, matcher phrases) are fixed;
  fresh items reuse those trigger phrases in new sentences. Freshness is
  at the item level (new IDs, new sentences), not at the trigger level.

## Run

- `delib_si.zag` byte-identical to `work_a1/delib_si.zag`
  (sha256 `5da5885bc5a9df5bac668bfb8c29d15934032e4526ef6535610a92fd43749c41`),
  rebuilt with the pinned toolchain
  `toolchain/bin/znc_linux_x86_64_abed8aa1` in `work_a1r/`.
- Same 4 budget rungs, 3 reruns each, zero RNG. Raw outputs saved as
  `epi/out_b{B}_{false,true,c70}.txt`.

| budget | total /94 | pp | false /12 | true /12 | mean preds/item | recon | vflips | canonical digest | determinism |
|---|---|---|---|---|---|---|---|---|---|
| 1x | 29/94 | 30.9 | 12/12 | 12/12 | 3.000 | 0 | 0 | a83b37785fd62059… | IDENTICAL ×3 |
| 2x | 59/94 | 62.8 | 12/12 | 12/12 | 9.000 | 0 | 0 | 57cefaa42100f695… | IDENTICAL ×3 |
| 4x | 59/94 | 62.8 | 12/12 | 12/12 | 9.330 | 1 | 0 | 57cefaa42100f695… | IDENTICAL ×3 |
| 8x | 59/94 | 62.8 | 12/12 | 12/12 | 10.330 | 1 | 0 | 57cefaa42100f695… | IDENTICAL ×3 |

Per-family at 2x/4x/8x (identical): joke 5, sarcasm 3, hypothetical 5,
analogy 3, counterfactual 9, poetry 5, implicature 5 (35/70). At 1x:
joke 5, all other families 0 (5/70). 2x/4x/8x verdicts are
byte-identical (same canonical digest) — the extra deliberation changed
zero verdicts.

## New data point vs the frozen battery

The 4x reconsideration **fired once** (1/94), on W152
("Wonderful, the alarm is set for 6 AM on a Saturday."): sarcasm matcher
fired (pro=1) AND assertion-form counter-marker fired (" is " + digit "6",
con=1) → pro=con tie → kept the 2x verdict (WITHHOLD). The 8x
verification re-derived the same verdict (0 flips). So the 4x mechanism
is reachable on fresh items but outcome-inert by its own majority-tie
rule — the plateau is mechanism-level, not a battery artifact.

## Gate battery: 6/6 (re-confirmed on the untouched learner)

R1–R4 refused (G1/G2/G4/G5), A5/A6 allowed — identical to the frozen
Arm 1 gate result. Learner binary untouched.

## Honest limits

1. The strict clause (a) technicality stands: 0 < 0 is still false.
   The knee is at 2x (one rung early), confirmed on fresh items.
2. Fresh-item trigger phrases necessarily overlap the delib's fixed
   knowledge (see construction constraint above). The disjointness
   guarantee is at the item level.
3. Cost per quality point rises monotonically past 2x
   (9.14 → 13.48 → 13.97 → 15.47 preds/pp on the fresh battery):
   deliberation past 2x buys zero quality at positive cost.
4. No bar, clause, or verdict rule was changed. The strictness point is
   flagged to Micah as an amendment candidate — his call.
