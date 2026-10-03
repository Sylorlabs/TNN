# Experiment 2 — Measurement report (coordinator-run)

Date: 2026-09-27. Binary: `~/workspace/onebrain/impl/onebrain` (built 2026-09-27 06:20 UTC,
source `onebrain.zag` 1,358 lines). Problem set: `~/workspace/onebrain/v4/v4.tsv`,
frozen v4.1 SHA-256 `e74bfa51d3a4697eb885c0b45f63a13e4b4f0b2023bc5cb8623451460f18dde6`
(2026-09-27 06:26:07 UTC, frozen before any scoring run on that version).
Raw outputs: `single_r{1,2,3}.txt`, `onebrain_r{1,2,3}.txt`, `ablate_r{1,2,3}.txt`,
`min_r{1,2,3}.txt`, `poison_r{1,2,3}.txt` (28 VERDICT lines each).

## Accuracy (winner bid vs expected_bid)

| mode     | correct | accuracy |
|----------|---------|----------|
| single   | 14/28   | 50.0%    |
| onebrain | 14/28   | 50.0%    |
| ablate   | 14/28   | 50.0%    |
| min      | 14/28   | 50.0%    |
| poison   | 8/28    | 28.6%    |

Per-problem (exp | single | onebrain | ablate | min | poison | fork):

| id | exp | sing | ob | abl | min | poi | fork |
|----|-----|------|----|-----|-----|-----|------|
| p01 | 13 | 13 | 13 | 13 | 13 | 13 | 0 |
| p02 | 15 | 13 | -1 | 13 | -1 | -1 | 1 |
| p03 | 13 | 13 | 13 | 13 | 13 | -1 | 1 |
| p04 | 22 | 13 | 13 | 13 | 13 | -1 | 1 |
| p05 | 22 | 13 | 16 | 13 | 16 | -1 | 1 |
| p06 | 14 | 14 | 14 | 14 | 14 | 14 | 0 |
| p07 | 15 | 14 | 14 | 14 | 14 | -1 | 1 |
| p08 | 14 | 13 | 13 | 13 | 13 | 14 | 1 |
| p09 | 16 | 16 | 16 | 16 | 16 | 16 | 0 |
| p10 | 16 | 16 | 16 | 16 | 16 | -1 | 1 |
| p11 | 18 | 16 | -1 | 16 | -1 | -1 | 1 |
| p12 | 18 | 16 | 16 | 16 | 16 | -1 | 1 |
| p13 | 18 | 17 | 17 | 17 | 17 | -1 | 1 |
| p14 | 17 | 13 | 13 | 13 | 13 | -1 | 1 |
| p15 | 18 | 18 | 18 | 18 | 18 | 18 | 1 |
| p16 | 19 | 19 | 19 | 19 | 19 | -1 | 1 |
| p17 | 19 | 19 | 19 | 19 | 19 | -1 | 1 |
| p18 | 20 | 19 | 19 | 19 | 19 | -1 | 1 |
| p19 | 20 | 20 | 20 | 20 | 20 | 20 | 0 |
| p20 | 24 | 24 | 24 | 24 | 24 | 24 | 0 |
| p21 | 24 | 24 | 24 | 24 | 24 | 24 | 0 |
| p22 | 24 | 24 | 24 | 24 | 24 | 24 | 0 |
| p23 | 23 | 24 | 24 | 24 | 24 | 24 | 0 |
| p24 | 23 | 24 | 24 | 24 | 24 | 24 | 0 |
| p25 | 23 | 24 | 24 | 24 | 24 | 24 | 0 |
| p26 | 21 | 21 | 21 | 21 | 21 | -1 | 1 |
| p27 | 21 | 21 | 21 | 21 | 21 | -1 | 1 |
| p28 | 22 | 18 | 18 | 18 | 18 | 18 | 1 |

(-1 = NO_VERDICT: ARGMAX found no live bid.)

## Kill-bar assessment (frozen PREREG §kill-bars)

- **K1 — FIRES → KILL.** onebrain (50.0%) does not beat single (50.0%), and the
  shared-writes-off ablation matches onebrain exactly (50.0%; 25/28 identical
  verdicts). Both conjuncts hold. Of the 11 fork-items single got wrong,
  onebrain fixed 0. The 3 verdicts the fork moved (p02 13→-1, p05 13→16,
  p11 16→-1) were all wrong→wrong.
- **K2 — passes.** Poisoning the leading bid's supporting fact between rounds
  changed the verdict on 15/18 fork items (p02/p11 were already NO_VERDICT,
  p28 unpoisonable — red-team correction of the 17/18 first reported).
  Changed items mostly collapse to NO_VERDICT; p08 flipped 13→14
  (accidentally correct). Non-fork items unaffected (10/10), as expected —
  no branches, nothing to propagate to. Cross-talk is causal but purely
  destructive — which is why K1 kills.
- **K3 — passes.** `min` (bare loop, no crew fan-out logic) ≡ `onebrain`
  byte-identical on all 28 verdicts AND all 28 fork flags. Fork fired on
  18/28 in min mode — the ledger-driven machinery chose to fork by itself.
- **K4 — passes (weakly).** onebrain vs ablate differ on 3/28 verdicts
  (p02, p05, p11): deleting shared writes changes behavior, so shared state
  is not purely decorative. No accuracy effect either way.
- **K5 — passes.** All 5 modes byte-identical across 3 reruns
  (single a9b9999345c8, onebrain b5c20e213b0d, ablate 1a3797e96774,
  min 1b26c18caa27, poison d4b4ea91d60f — first 12 hex of SHA-256).
- **K6 — passes.** Independent grep: only matches are "zero RNG" comments;
  no RNG in decision paths.

## Mechanism notes

- Fork rate: 18/28 (64%). Fork rule (≥2 surviving ev=1 readings, top-two
  fired-bid margin ≤12) behaved as specified.
- Overhead: 28 problems in 35–66 ms per mode; onebrain not slower than
  single. Ledger geometry unchanged (25×552).
- **Destructive cross-talk (p02, p11):** shared-ledger audit can annihilate
  all candidates. p02 trace: live bids 13/15/22 all depended on fact 10
  (joke fact); branch subpass ran `AUDIT_DENY fact=10 by=6` (the forget
  reading denied the joke fact); all three bids died; ARGMAX → -1.
  The forget bid (expected winner, 15) was killed by the very denial its
  own reading triggered — friendly fire through the shared ledger.
  Ablate (scratch copies, deny discarded) kept winner 13. Genuine
  shared-state causality, but destructive rather than constructive.
- **Poison mostly collapses to NO_VERDICT** rather than flipping winners
  (14/15 changed items → -1). The shared invalidation propagates, but the
  machinery has no recovery path — it cannot re-deliberate around a denied
  fact. Cross-talk confirmed; robustness absent.
- **Unreachable bids:** withhold(23) never fires when any fact gates
  (p23–p25: expected 23, all modes 24, fork=0). These 3 items cannot
  discriminate fan-out designs — dead weight in the set, reported openly.
- v3 problem set (reading-selection space) archived as integration misfire:
  `~/workspace/onebrain/problems/` — machinery outputs action bids, v3
  expected reading-A/B answers; unscoreable. Superseded by v4.

## Red-team amendments (2026-09-27, independent — report upheld the kill)

- Scoring independently re-derived 28/28 × 5 modes: exact match. K1 math confirmed.
- **Set power is weak, not invalid:** only 11/28 items are K1-informative
  (10 fork=0 ⇒ onebrain≡single by construction; 7 fork=1 single-correct can
  only lose). p19–p22 violate the prereg's "≥2 readings" spec (1 reading
  each); removing them changes nothing (10/24 = 10/24).
- **Reachability: 0/14 single-wrong items have reachable correct states** on
  the actual machinery. On 20/28 problems every fired bid shares the single
  supporting fact, so fact-denial can only annihilate bids, never
  discriminate between them; the duel channel (the only discriminating
  audit) fired on 2/28 problems.
- **FRAGILITY (matters more than the kill):** the kill turns on one
  unprincipled tie-break — DENY by=0's strict `imin<imax` fire condition
  plus first-minimal tie-break. A minimal (~3-line), principled, fully
  general variant V4 (correction denies the least-relevant alive fact;
  relevance ties broken by fewest dependent bids — least-disruptive
  invalidation, no problem-specific logic) hand-simulates to flip exactly
  p08 → onebrain 15/28 > single 14/28 with ablate at 14/28, un-firing both
  K1 conjuncts. Hand-simulated only (not built/run — out of scope under the
  frozen prereg). The verdict kills THIS implementation, not the fan-out
  concept. Recommended follow-up: preregistered re-test of V4-class
  (least-disruptive invalidation) variants.

## Provisional verdict (pending red team)

**H1 is KILLED by K1.** The ledger-driven fork is genuine machinery (K3),
the ledger is genuinely shared and causal (K2, K4), everything is
deterministic (K5) and RNG-free (K6) — but the fan-out confers no accuracy
benefit over single deliberation on 28 hard ambiguous problems, and the
ablation matches it. The observed cross-talk is as often destructive
(mutual annihilation → NO_VERDICT) as constructive.
