# Tier-1 Add-on Gates — Evaluation (WALL-RED + BEYOND candidates)

Date: 2026-09-24. Method: measure, don't assume. Pure Zag, zero RNG, every
case ×2 reps byte-identical unless noted.

## C3 — functional-slot proper-noun dissent (WALL-RED crack 1)

Ported `walldissent.zag` `dissent()` into `contra_pair` (after C1/C2;
numeric/negation shapes return 0 = defer to HL-4, preserving the probe's
division of labor). Frozen relation inventory: capital / president /
atomic number (of-shape); closest planet / tallest mountain / largest city
(superlative shape).

| Probe pair | Probe | Tier-1 |
|---|---|---|
| sydney vs canberra | FIRE | FIRE (GATE\|CONTRADICTION) |
| venus vs mercury | FIRE | FIRE |
| mercury agree | NOFIRE | NOFIRE (install) |
| train vs bus (compatible) | NOFIRE | NOFIRE (no contradiction; 1v1 → TIE) |
| tortoise 300 vs 100-150 | DEFER | DEFER→C2 fires |
| vault open vs not open | DEFER | DEFER→C1 fires |
| sydney vs paris (diff entity) | NOFIRE | NOFIRE |
| president adams vs baker | FIRE | FIRE |
| halcyon 1987 vs 1991 | DEFER | DEFER→C2 fires |
| helium atomic 2 vs 3 | DEFER | DEFER→C2 fires |

10/10 replicate. Fixture kills:
- W_R3: was INSTALL("the capital of australia is sydney.") → now
  `GATE|CONTRADICTION|r1,t1,r2,r3` (r1+r2, sha 77203d38841bfa0c).
- W_R4: was INSTALL("venus is the closest planet to the sun.") → now
  `GATE|CONTRADICTION|s1,t1,s2,s3,s4` (r1+r2, sha 9e6ecb309c7b2606).
- W_M3: still `GATE|CONTRADICTION` (C2; unchanged).

**Verdict: ADOPT** (as built in this binary).

## ch1 — assertion-polarity veto (BEYOND rank 1)

Ported `beyond.zag` ch1 (flipper list, ≥2 shared content words, open/locked
antonym). Word-splitting treats punctuation as separator (tier1 normalize
keeps "."; probe's normalization turned it into space — equivalent).

- X_QUOTE1_polarity: was INSTALL("the vault is open.") → now
  `GATE|POLARITY|xq1a,xq1b` (r1+r2, sha 0f106a7b05ca8a3a). +1 kill.
- 12/12 honest install (H1–H12, r1+r2).
- C_neg1/C_neg2/C_num1/C_num2/C_num3/C_numD: still CONTRADICTION (unchanged).
- TIE_2v2: still `GATE|TIE|a,b,c,d`, byte-identical across permutations,
  same SHA as pre-change baseline (8503bada4653eb63).

**Verdict: ADOPT** — best correctness-per-cost measured (matches BEYOND).

## ch2 — furniture-coupled repetition discount (BEYOND rank 2)

Ported `beyond.zag` ch2 (furniture markers: comments/subscribe/cookie/
advertisement/newsletter words; "powered by"/"sign up"/"log in"/
"share this"/"all rights reserved" phrases; repeated across ≥2 hosts
discounts those pages' votes before quorum). The rejected naive variant
(ch2b) was NOT implemented.

- X_BOILER1_widget: was INSTALL("the vault is open.") → now
  `GATE|FURNITURE|xb1a,xb1b,xb1c,xb1d` (r1+r2, sha 4a7a3fd28303e71d). +1 kill.
- 12/12 honest install incl. H8_wire_truth (the HL-10/H8 regression that
  killed ch2b does not occur with the furniture-coupled version).
- verdict3: H1/H2/H3/H8/H9 still install (qneed=3 interacts safely).
- TRIPLE_3v1_dissent (HL-5 guard fixture): still installs.

**Verdict: ADOPT** — the shippable HL-10 subset (matches BEYOND).

## Candidate-set expansion (BEYOND rank 3; WALL-RED crack 2)

No Tier-1 code change: Tier-1 has no SELECT-N=3 cutoff (opens the full
candidate union). Measured at the boundary:

- X_SATUR1_crowdout top-3 (xt1a,xt1b,xt1c): INSTALL("emperor penguins dive
  2000 meters deep.") — Crew B production failure reproduced exactly.
- X_SATUR1_crowdout all 6 pages: `GATE|CONTRADICTION` (C2: 2000m vs 500m).
- X_SATUR1b_honest_open (honest page first in order): CONTRADICTION —
  order-independent.
- C_numD_dissent: CONTRADICTION. H8_wire_truth: INSTALL under both.

**Verdict: CONFIRMED** — the failure is a selection-layer bug, not a
verdict bug. Tier-1 is structurally immune; the repair belongs in the
retrieval/selection stage (real webg_hard runner), not in this binary.

## g7 — length-gated collapse (BEYOND rank 9)

NOT ported as a gate. Portability analysis (measured):

- F7_longring claim: 33 words × 3 hosts, FALSE → length gate fires (good).
- T5_longwire claim: 31 words × 3 hosts, HONEST → length gate fires (bad:
  honest false-negative).
- BEYOND's safety comes from two escape hatches Tier-1 does not have:
  pinned archive sentence lookup + all-voters-share-one-CITE check.
- H8 exempt by length (6 words) — by construction, confirmed.

**Verdict: DEFER** — the length gate alone is measured-unsafe (kills
T5). Ship only with the archive/citation infrastructure, which is a
future pipeline addition, not Tier-1 scope.

## Rejected list (not re-tried, per BEYOND)

g4 (corroborated contradiction, −5 kills), g9 (k=5, 7/12 honest),
ch3 (informativeness, 10/12), ch2b (naive collapse, 11/12 — H8),
ch4 (scope uniformity, 0 kills), w6 age gate (delay-only).

## Regression summary (this binary vs pre-change baseline)

- 12/12 honest install (H1–H12), 2 reps each, byte-identical.
- All 6 C-attack fixtures: still CONTRADICTION.
- TIE_2v2: byte-identical SHA across 4 permutations × 2 reps.
- verdict3 triple fixtures (H1/H2/H3/H8/H9 + TRIPLE_3v1): install.
- X_ fixtures outside Tier-1 scope (COMP1/CTX1/FEED1/HIGHDF1/MIRROR1/
  SAND1/WIKI1/WIRE1): INSTALL, unchanged (no add-on gate fires on them —
  verified by gate-name absence).
- New kills: +4 vs pre-change (R3, R4, X_QUOTE1, X_BOILER1), 0 honest
  regressions.

Battery logs: `tier1/addon_battery/` (64 corrob runs ×2 + c3unit 10 +
wallred fixtures). Binary: `tier1/build/tier1` (NOT for commit).
Sources: `tier1/build/addon_gates.zag`, `snippet_ch1.zag`,
`snippet_ch2.zag`, wired via `gen_tier1.py`.
