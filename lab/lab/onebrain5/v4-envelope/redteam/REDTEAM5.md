# REDTEAM5 — independent attacks on the V4 envelope (2026-09-27)

**Method:** Predictions in `predictions_rt.md` written before running. 7 fresh items (rt.tsv). onebrain + nov4, 2 reruns, byte-identical.

## R1: V4-help in a FORGET item — PARTIAL (1/3 help, 2/3 ANNIHILATION)

Items: forget+correction (`forget X; no, i meant Y`, expected=16). Prediction: 3/3 onebrain=16 > nov4=15.

| item | onebrain | nov4 | result |
|---|---|---|---|
| R1a | NO_VERDICT (−1) | 15 (wrong) | ANNIHILATION |
| R1b | NO_VERDICT (−1) | 15 (wrong) | ANNIHILATION |
| R1c | 16 (right) | 15 (wrong) | HELP ✓ |

**R1c confirms:** V4 2a denied the forget fact → bid15 cleaned → 16 won. V4 HELPS in a forget+correction item. The help envelope extends beyond correction+challenge.

**R1a/R1b — NEW HARM MODE (annihilation):** Trace shows 2a denied the forget fact (cleaning bid15), then 2b denied the correction fact (cleaning bids 16,22) → zero bids → NO_VERDICT. The `skipped_annihilate` guard did NOT trigger on the 2b step (flag=0) even though it removed the last bids. R1c survived only because a distractor fact (fid11) gave 2b a harmless first target, after which the guard correctly abstained (flag=1). **Finding:** when 2a and 2b both fire in the same round and their denials together cover all facts, V4 can annihilate all bids. The per-step guard is insufficient across steps.

## R2: Outcome-irrelevant V4 — CONFIRMED (2/2)

Items: correction+challenge with inter(correction) > inter(challenge). Prediction: V4 fires but onebrain == nov4.

| item | onebrain | nov4 | V4 fired? | result |
|---|---|---|---|---|
| R2a | 16 | 16 | YES (denied hid=11) | INERT ✓ |
| R2b | 16 | 16 | YES (denied hid=11) | INERT ✓ |

**Mechanism (R2a):** the duel killed reading 2 (challenge) before V4; V4's denial of the challenge fact was moot. V4 firing ≠ V4 mattering. Bounds the envelope: trace activity does not imply causal effect.

## R3: Duel-preemption break — ATTACK FAILED (0/2)

Prediction: 1/2 items (the 3-reading R3a) would show onebrain ≠ nov4 via 2b.

| item | onebrain | nov4 | result |
|---|---|---|---|
| R3a (3-reading) | 16 | 16 | INERT (attack failed) |
| R3b (control) | 19 | 19 | INERT ✓ |

**Mechanism (R3a):** the duel killed BOTH reading 6 (forget, corr=0) and reading 2 (challenge). V4 2b fired (denied two facts) but the duel had already decided. Duel pre-emption is robust: even with 3 readings, if the duel removes the contested bids, V4 cannot change the outcome.

## Summary

| attack | predicted | actual | verdict |
|---|---|---|---|
| R1 (forget help) | 3/3 help | 1/3 help, 2/3 annihilation | PARTIAL + new harm mode |
| R2 (irrelevant V4) | 2/2 inert | 2/2 inert | CONFIRMED |
| R3 (break preempt) | 1/2 break | 0/2 break | ATTACK FAILED |

**Net:** The envelope survives. One new harm mode (cross-step annihilation → NO_VERDICT). One expanded help region (forget+correction).
