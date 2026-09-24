# VERDICT W10 — forge-PAM spoof duel (third generation)

Evidence commit: `ed9e02922f7409b7a611e8b762e2da2282a9eb31`
(prereg `wild/prereg/PREREG_W10.md`, frozen.)

## Observed numbers (instrument + exact-arithmetic mirror agree on all
## 2291x6 spoof E values, bestT, margin, verdict)

- Candidates: 2291 (C=1102, B=1109, W=12, P=18, F=50)
- K1: **0 W/P/F admits** — PASS
- D1: **573/1102 C duel-rejected = 52.00%** (bar <10%) — KILL
- D2: verdict changes mu 1000->500: **0/2291 = 0.00%** (bar >20%) — PASS
- K3: C correct admits **529/1102 = 48.00%** (bar >=66.78%) — FAIL
- D4: wrong-set items reproducible at duel-winning strength: **0**
  (bar >1) — PASS
- B diagnostic: 557/1109 admits
- K2: PASS (2x mu=1000 byte-identical). D3/K4/K5: PASS.

## Root cause (design flaw, not implementation defect)

All 573 rejected C bundles lose to **T4 (T_splice)**. The frozen spec
defines T_splice's content breakage as
`content_sig := (content_sig & ~1023) | 700` ("broken marker") while E's
intactness check is `(content_sig mod 1000) < 500`. OR-ing 700 into the
low 10 bits does NOT control mod 1000: e.g. id 4
(csig=731446304304): spliced csig mod 1000 = 444 < 500 — still "intact".
So T_splice usually keeps the +4000 content term while gaining
+(9000−mrgF)/100 on mrgF (e.g. +86 for id 4): spoof E exceeds genuine E,
margin −86 < μ=1000 → REJECT. The prereg's predicted analysis ("worst
transform is T_eps_up, margin +5500") assumed the breakage works; it does
not, for 573/1102 genuine bundles. Two independent implementations (Zag
mod-1024000 tracking + Python exact big-int) agree on every E value, and
the id-4 arithmetic was verified by hand: the flaw is in the frozen
transform definition, which operates in bit-domain while E checks in
mod-1000 domain.

## Status: KILL (D1 fired; K3 also failed)

The forger mints spoofs that beat-or-tie genuine low-mrgF candidates, and
the duel then rejects the genuine candidates (paranoia). F1's "forged
candidates lose their own duel" holds (K1: 0 wrong admits), but F2
("genuine candidates beat their spoofs by >= μ") is falsified at 52%.
Redesign direction: the breakage mechanism and the breakage check must
operate in the same domain (e.g. force the marker in mod-1000 space), or
T_splice must not be a free mrgF boost.

## Numeric-cap classification (standing law: no arbitrary hard limits)

- μ=1000 (existence): LOAD-BEARING (a duel needs a decision threshold);
  the VALUE 1000 is calibration -> FLAGGED. (D2: 0% sensitivity — the
  margin is not doing the work; the forger's brokenness dominates.)
- K=6 transforms: ARBITRARY count -> FLAGGED (library composition is the
  design; "6" is not principled).
- E weights (100, /100, 5000, 2000, ±8000, ±4000): ARBITRARY calibration
  -> FLAGGED.
- ε=25, +150, splice-floor 9000: ARBITRARY constants -> FLAGGED.
