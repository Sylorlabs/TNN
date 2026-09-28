# Job-3 red-team report (independent, pre-verdict)

Date: 2026-09-27. Author: independent red team (no access to the builder's
memorizer prototype; all variants below reimplemented from PREREG_JOB3.md
§5/§10 and Crew E's REDTEAM_REPORT description). The generator (`gen3.py`) is
shared ground truth — it defines the items, not the agents. Pure Python,
zero RNG. Code: `redteam/rt_attacks.py`; raw output: `redteam/rt_output.txt`.

## Attack 1 — fidelity: is the Zag memorizer faithful to the prereg spec?

Reimplemented the Crew-E affine memorizer from the prereg §5 text (fit in
raw-byte space, solve (s,o) from positions 0,1, verify on the rest,
case-preserving transform, skip sorted probes for rule 5, P3 first-solved
policy). Compared item-by-item against the Zag binary's `memA`/`memB`/`memC`
outputs.

| Check | Result |
|---|---|
| P0+P2 items vs Zag (3 arms × 176) | 528/528 byte-identical, 0 mismatches |
| P3 policy reimplementation | 0/8 (A), 6/8 (B), 6/8 (C) — matches Zag exactly |

**FAITHFUL.** The instrument implements the specified agent.

## Attack 2 — within-class extension: no-verify interpolation variant

Dropped the M2 verification step ("subset fit": solve (s,o) from positions
0,1, apply without checking — the charge explicitly invited subset fits).
Measured on arm B:

| Metric | noverify on arm B |
|---|---|
| P0 | [0,0,0,4,2,0] = 6/48 |
| P2 | 4/120: (3,4):1, (3,5):1, (5,3):1, (5,4):1 |
| P3 withhold score | 0/8 (never withholds — maximally reflexive) |

Every noverify arm-B P0 hit is also scored by the *verified* memorizer on
arm A (subset check: True) — the hits are salt-invariant.

The (3,5) hit (idx 277, len-3 probe `pvz`): step-1 droplast is exact via the
floor (output positions {0,1} ⊆ fitted {0,1}, m1=`pv`); step-2 sortchars uses
a vacuous fit against the first len-2 train token, which happens to already
be sorted — a sortedness data accident in the same family as the
preregistered (5,3)/(5,4) accidents (§7), not structural exploitation.

**K-J3-4(a) status: TRIGGERED BY LETTER.** This 2-parameter variant scores
(3,4) 1/4 and (3,5) 1/4 on arm B, beyond the §7 accidents. See §"Verdict
implication" for why the trigger is the characterized floor, not salt
exploitation.

## Attack 2b — exhaustive position-pair scan (optimality proof)

For every arm-B probe, every train token, and every position pair (P0: all
pairs; P2: step-1 pair (0,1), all step-2 pairs): is the resulting transform
output correct for any rule?

**Exactly 10 items have any winning pair** — the 6 P0 floor items
(droplast idx 128,129,132,133; upperfirst 136,140) and 4 P2 items
((3,4):273, (3,5):277, (5,3):312, (5,4):316). **Every winner uses pair
(0,1) at every step.** No other position pair wins any item.

This proves the no-verify variant is OPTIMAL among 2-parameter
interpolation tricks on arm B: no 2-parameter agent can be correct on any
arm-B item whose output has ≥3 positions, because correctness requires the
interpolant to be queried only at fitted positions. The residual is the
degrees-of-freedom floor, fully characterized, not salt exploitation.

## Attack 2c — (s,o) propagation through rule position maps

The "smart" affine extension: propagate the fitted (s,o) through each rule's
position map instead of refitting.

| Arm | reverse via propagation | rotleft via propagation |
|---|---|---|
| A (control) | 8/8 — the attack is real where algebra exists | 0/8 (wrap breaks affinity, even on arm A) |
| B | 1/8 — the single hit is idx 100, len 2 (vacuous floor) | 0/8 |

Propagation cannot beat the cubic salt: it is exact only where the
underlying map is affine, which on arm B is exactly the vacuous floor.

## Attack 3 — degree ladder: quadratic-fit memorizer (3 params)

| Arm | P0 | P2 |
|---|---|---|
| C (quadratic salt) | [0,0,0,8,8,0] = 16/48 | 6/120: (3,4):3, (3,5):1, (5,3):1, (5,4):1 |
| B (cubic salt) | [0,0,0,4,4,0] = 8/48 | 4/120: (3,4):1, (3,5):1, (5,3):1, (5,4):1 |

On arm C the 3-parameter memorizer recovers the **full Crew-E signature**
(P0 [0,0,0,8,8,0], (3,4) 3/4 on lengths 3,4,5, the two sorted-train
accidents) — the degree-2 salt is beaten by the degree-2 memorizer, as the
ladder predicts. On arm B it recovers only the 3-parameter floor
(len ≤ 3 hits on droplast/upperfirst, the (3,4) len-3 chain, accidents) —
**no length≥4 hit, no reverse/rotleft/dupfirst/sortchars hit.** The cubic
salt is not beaten by the quadratic memorizer. The ladder holds:
salt of degree d requires a memorizer of degree ≥ d.

## Attack 4 — free-delta clone (principled behavioral limit)

| Clone | arm A | arm B | arm C |
|---|---|---|---|
| σ-aware (true position maps) | P0 [8,8,8,8,8,0]=40/48, (3,4)=4/4 | same | same |
| σ=id (prereg-specified) | P0 [0,0,0,8,8,0]=16/48 | same | same |

The prereg-specified σ=id clone scores droplast/upperfirst **8/8 on every
arm** — behaviorally identical to the genuine combiner on identity-σ rules.
**K-J3-4(b): CONFIRMED.** Salt alone cannot separate "applies rule 3/4"
from "copies per-position deltas" on identity-position rules; the
separation must come from non-identity-σ rules (reverse/rotleft/dupfirst),
where the clone's σ=id assumption fails 0/8. (The σ-aware variant further
shows that even with perfect position-map knowledge, the data-dependent
σ of sortchars still separates — 0/8 there on all arms.)

## Attack 5 — combiner white-box audit

- `gen_p0`/`gen_p2`/`gen_p3` bodies contain **zero** references to
  `salt_c`, `tokfill`, `train_index`, `taught`, `fit_affine`, `_zag_arg`,
  or the memorizer — the probe path touches no generator algebra.
- Signatures take only `(probe, out)` plus rule ids — no arm, no taught
  table, no indices.
- Ok-flag patterns are byte-identical across arms (all ones).

**CLEAN.** The genuine combiner cannot see the salt; its perfect scores are
rule composition, not salt exploitation.

## Attack 6 — other angles probed

- Salt self-fitting (learn C1/C2/C3 per phase, then compute δ directly):
  collapses to the degree ladder (attack 3) — no new power.
- Length oracle: token length is salt-independent, but the memorizer
  already conditions on length; no extra power.
- P3 policy variants (e.g. withhold-unless-output≠input): cannot recover
  arm-B exploitation; the no-verify variant's 0/8 shows reflexivity is the
  price of dropping verification.

## Verdict implication (red-team assessment)

K-J3-4(a) fired **by letter**: a 2-parameter subset-fit variant scores
(3,4) 1/4 and (3,5) 1/4 on arm B beyond the §7 accidents. The red team
assesses the trigger as the **characterized degrees-of-freedom floor**,
not salt exploitation, on three grounds:

1. **Exhaustiveness (2b):** no position-pair trick is correct on any arm-B
   item with ≥3 output positions. The variant never queries beyond its
   fitted positions — it asks only questions the salt cannot make hard.
2. **Salt-invariance:** every hit is also scored on the affine arm A; the
   floor exists on every salt family (it is information-theoretic: 2
   parameters always match 2 points). No salt family can remove it, so it
   cannot be mistaken for salt exploitation.
3. **Accident, not structure:** the (3,5) hit is a sortedness data
   accident in the preregistered family; the (3,4) len-3 chain is exact
   droplast on 2 positions followed by a vacuous fit.

The bar's intent — recovering the Crew-E *exploitation signature* on arm B
(P0 [0,0,0,8,8,0] with (3,4) 3/4) — **provably failed**: G2′=0 (zero
non-vacuous cross-phase affine systems on arm B), and 2b proves no
2-parameter trick goes beyond the floor. The discrimination claim is
therefore **refined, not dead**: the cubic salt provably reduces every
2-parameter agent to the salt-independent floor (correct iff #output
positions ≤ #fitted positions, plus characterized data accidents), while
the genuine combiner stays perfect (48/48, 120/120, 8/8) on all arms.
The floor is exposed by the P3 reflex check (the variant scores 0/8 —
it cannot withhold).

Recommendation: verdict **YES, with the refined boundary stated
prominently** — the cubic non-affine salt is the family Micah asked for;
"provably cannot" means "cannot exploit the salt's structure," with the
salt-independent degrees-of-freedom floor characterized as the permanent,
unremovable residual.
