# RECENCY VS COHERENCE — VERDICT (2026-09-22)

**Prereg:** `PREREG_R4C.md` (commit `48bde9301a6c928d0bea2a46155eeb045d3b3749`),
committed before any trial binary was built or run. Oracle:
`verify_rsi4c.py` (frozen). Battery: 24 fresh teach-conflict items
(disjoint from RSI-3 D1/D2), ground truth in `battery_r4c.csv`, never
read by the binary (KB5-SEPARATION verified: binary item fields match
the CSV exactly; no gt in the binary).

## Arm x metric (n=24, 5/5 byte-identical per mode)

| arm | accuracy | wrong installs | withhold on NEITHER | consults | cost (ops) |
|---|---|---|---|---|---|
| base (withhold-all) | 8/24 | 0/24 | 8/8 | 0 | 0 |
| recency (PREF-SEQ-GT) | 8/24 | **16/24** | 0/8 | 0 | 48 |
| coherence | 20/24 | 4/24 | 8/8 | 0 | 168 |
| ask-first | 22/24 | 2/24 | 8/8 | 16 | 424 |

All bars KB1 (battery targets), KB2 (determinism), KB5 (separation) PASS.

## Frozen-rule outcome: NO-CHAMPION — and that is a defect in my bar

KB3 as frozen requires strictly greatest accuracy AND wrong-install ≤
*every* other arm's. The withhold-everything baseline has wrong-install
0 by construction (it never decides anything), so no deciding arm can
satisfy the second clause. The rule is unsatisfiable by design against
a degenerate baseline — a drafting defect on my part, owned here, not
fudged. The prereg stays frozen; the defect is reported, not repaired
after the fact.

## Substantive outcome (the question Micah actually asked)

Among the three conflict-resolving arms, the ranking is unambiguous on
BOTH accuracy and wrong-install rate:

**ask-first (22/24, 2 wrong) > coherence (20/24, 4 wrong) > recency (8/24, 16 wrong).**

- **Micah's critique is CONFIRMED, not falsified.** Recency — newest
  teaching always wins — is the worst deciding arm: it installs the
  wrong teaching on 16 of 24 items (67%), failing exactly the way he
  predicted ("newest teaching shouldn't be the fix"). KB4-FALSIFY does
  not trigger.
- **Coherence beats recency decisively** (20 vs 8 correct, 4 vs 16
  wrong installs). The teaching that makes the most logical sense of
  the corroborating info wins over the newest one.
- **Ask-first beats coherence** (22 vs 20; 2 vs 4 wrong installs). The
  16 consults cost 256 extra ops (424 vs 168) — the accuracy is bought,
  not free. Its withhold behavior on all 8 NEITHER items is correct.

## Residual failure mode (honest)

Ask-first's 2 misses are the ADV-OLD items: recency and coherence
*wrongly agree* (both fooled by the same stale corroboration), so no
consult fires and the wrong teaching installs. Agreement of two
channels is not safety when both channels drank from the same stale
well. This is the next boundary: disagreeing channels are covered;
*correlated-wrong* channels are not.

## KB6 — scope restriction on PREF-SEQ-GT@ARBITRATE (recorded)

RSI-3's invented primitive is valid ONLY for same-key corrections with
no conflicting background knowledge (the RSI-3 battery had none — a
correction under one key, nothing else speaking to it). Teach-conflicts
against corroborating knowledge require coherence or ask-first.
Newest-wins must never be applied where older knowledge contradicts the
new teaching.

## Grade: A (trial) / B+ (prereg drafting — the KB3 defect above)

The trial answered the question it was asked, with a frozen battery,
mechanical oracle, byte-identical reruns, and an honest falsification
branch that did not trigger. The KB3 defect is the deduction: write
the champion rule to exclude degenerate baselines next time.
