# REDTEAM5 predictions — written before running (2026-09-27)

**Attacks on the V4 envelope** (PREREG5 §2 mechanism rules M1–M7 as the defender):

## R1: V4-help in a FORGET item (3 items)
**Attack:** Construct forget+correction items (`forget X; no, i meant Y`, expected=16) where V4's forget-denial (2a) removes the wrong forget bid, producing onebrain > nov4.
**Defender (M2/M3):** In forget+correction, bid22 shields reading 0 (correction, lowest-hid) → correction fact dep=2, forget fact dep=1. V4 2a considers only forget-topic-overlapping facts → denies the FORGET fact (dep 1). This removes bid15 (wrong) → onebrain should pick 16. nov4 (no V4): reint on inter tie (2 vs 2) → branch agreement decides; if branches pick 15, nov4=15 wrong.
**Prediction:** 3/3 items will show onebrain=16 > nov4=15 (V4 HELPS in a forget item). This EXPANDS the help envelope beyond correction+challenge: V4 helps whenever it denies the fact supporting the human-wrong bid, regardless of reading type.

## R2: Outcome-irrelevant V4 (2 items)
**Attack:** Construct items where V4 fires (denies a fact) but the winner doesn't change (onebrain == nov4 despite V4 activity in trace).
**Defender (M2/M5):** If the denied fact's bids weren't contenders — e.g. correction+challenge where inter(correction) > inter(challenge) so reint picks 16 with or without V4 — then V4's denial is outcome-irrelevant.
**Prediction:** 2/2 items will show V4 AUDIT_DENY_DELIB in trace AND onebrain == nov4. This bounds the envelope: V4 firing ≠ V4 mattering.

## R3: Duel-preemption break (2 items)
**Attack:** Construct items where the duel kills reading 6 in round 1 BUT V4 still changes the outcome (onebrain ≠ nov4).
**Defender (M6):** The duel kill suppresses 2a via the shared ledger. But if reading 0 (correction) ALSO fires, 2b is a separate V4 step that the duel doesn't suppress — V4 could still act through 2b.
**Prediction:** 1/2 items will show onebrain ≠ nov4 (the 3-reading item where 2b fires); 1/2 will show inert (pure 2-reading duel-preempt). If both are inert, M6 is stronger than stated.

## Scoring
Each attack item: run onebrain + nov4 (2 reruns, byte-identical required). Compare to prediction. An attack SUCCEEDS if the outcome contradicts the defender prediction.
