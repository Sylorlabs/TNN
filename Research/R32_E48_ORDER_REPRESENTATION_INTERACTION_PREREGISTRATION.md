# R32 E48 — Terminal Order × Representation Interaction Preregistration

Date frozen: 2026-08-23

Status: `WITHDRAWN_BEFORE_SOURCE_OR_EXECUTION`

Withdrawal note: an independent post-E47 audit showed that this selected-suffix
design would primarily remeasure the already-established E46 order effect. It
also produced an exploratory order-independent fit showing that order removal
and the two features can be separated more directly. No E48 source, compiler
build, fresh seed allocation, validation case, or confirmation case was consumed
under this preregistration. The active E48 preregistration is the matched online
versus batch 2×2 discriminator.

Promotion eligibility: none. This is a terminal-controller discriminator, not a
full R32 native qualification. R27 remains canonical regardless of this result.

## Question

E46 found a large presentation-order abstention/known-resolution tradeoff but no
tested order rescue. E47 found that two continuous causal co-presence statistics
varied structurally but did not rescue the original blocked online linear head.
E48 tests the unobserved interaction: can the joint E47 representation make one
of two preselected E46 interleavings satisfy the already-frozen safety and known
noninferiority gates when neither corresponding main effect does?

This test does not give UNKNOWN a learned target. UNKNOWN remains grounded value
zero and wins only when every commit head is negative. Any positive result is
therefore narrowly an order-conditioned fixed-zero-abstention result.

## Frozen six-model factorial

All six terminal heads start from exact zero, use learning rate 34, receive each
of the same 55,080 canonical records exactly once, and differ only by replay order
and whether feature slots 3 and 5 contain the E47 statistics.

| Model | Replay order | Representation |
|---:|---|---|
| M0 | blocked control | slots 3 and 5 zero |
| M1 | blocked control | joint E47 slots 3 and 5 |
| M2 | E46 strongest-safety, final-mode 0 | slots 3 and 5 zero |
| M3 | E46 strongest-safety, final-mode 0 | joint E47 slots 3 and 5 |
| M4 | E46 strongest-known, final-mode 6 | slots 3 and 5 zero |
| M5 | E46 strongest-known, final-mode 6 | joint E47 slots 3 and 5 |

Blocked order is `epoch → base → mode → resource → episode`.

The final-mode-0 interleave is E46 treatment index 3: for each epoch, base,
round 0..59, and mode slot 0..8, use
`rotation=(3+3*epoch+2*base) mod 9`,
`mode=(mode_slot+rotation) mod 9`, `resource=round/12`, and
`episode=round mod 12`.

The final-mode-6 interleave is E46 treatment index 0, with the same construction
except `rotation=(3*epoch+2*base) mod 9`.

The joint representation is exactly:

- slot 3: `clamp(min(epoch_evidence_A, epoch_evidence_B)/4, 0, 1000)`;
- slot 5: `clamp(min(option_support, option_contradiction)/4, 0, 1000)`.

The representation helper may not receive evaluator mode, truth, seed, time,
count, targets, or resource labels.

## Matched construction and integrity gates

1. Reconstruct and reserve every effective E45, E46, and E47 seed tuple before
   assigning fresh E48 stages 8–11.
2. Allocate nominal E48 IDs 48001–48003 for auxiliary training, 48101–48103 for
   terminal records, 48201–48206 for validation, and sealed 48301–48306 for
   confirmation. Confirmation records are allocated but not executed.
3. Train one common auxiliary snapshot and freeze it before terminal work.
4. Generate all 55,080 width-38 canonical terminal records once, without any
   terminal-model update. Each record stores the 32 baseline features, both E47
   representation values, and four action targets.
5. Replay only those stored records. Do not regenerate simulator worlds during
   reordered training.
6. Prove exact-once canonical-episode visitation for each of the three orders;
   require paired order hashes M0=M1, M2=M3, M4=M5, and all three pair hashes
   distinct.
7. Require identical canonical contents and targets across models, exact feature
   projection identity within each representation condition, 55,080 samples and
   220,320 updates per model, zero feature-lattice mismatches, frozen auxiliary
   parameters, and exact-zero initialization.
8. Validate all models lockstep on the same fresh seed × mode × resource × time
   grid with exactly 20 observations per cell. Retain the E47 pooled, key-mode,
   terminal-time, per-cell, and per-seed gate arithmetic.

Any integrity failure terminates interpretation.

## Frozen outcome gates and labels

No-unique safety is absolute for each model: in every one of 1,020 no-unique
cells, UNKNOWN must be at least 700 per mille and wrong commitment at most 300 per
mille. Known-truth noninferiority is evaluated against M0 and requires exact
success nondecrease and wrong nonincrease in pooled known cases, each key mode,
terminal time, each terminal key mode, and at least four joint passing seeds.

- `BASELINE_SPLIT_AMBIGUOUS`: M0 unexpectedly passes safety; do not interpret
  treatment causally.
- `MAIN_EFFECT_RESCUE_ON_FRESH_SPLIT`: M1, M2, or M4 passes its complete gate.
  Do not label a combination an interaction in this case.
- `ORDER_REPRESENTATION_INTERACTION_RESCUE`: M3 passes while M1 and M2 both fail,
  or M5 passes while M1 and M4 both fail.
- `ABSTENTION_TRADEOFF`: no complete model passes, but M3 or M5 passes absolute
  no-unique safety while failing known noninferiority.
- `NO_TESTED_ORDER_REPRESENTATION_INTERACTION_RESCUE`: integrity passes, M0 is
  unsafe, no main effect or combination passes, and neither combination reaches
  the tradeoff label.

The E48 discriminator gate is PASS only for the preregistered interaction-rescue
label. A main-effect rescue remains important evidence but is not an interaction
gate pass and would require separate confirmation/qualification.

## Bounded interpretation

A negative E48 result rejects only these two preselected orders crossed with this
joint two-feature representation under the current online linear value heads. It
does not reject all curricula, all grounded representations, nonlinear value
geometry, or an explicitly grounded nonzero UNKNOWN value. A positive result is
not R32 qualification and does not promote the architecture.
