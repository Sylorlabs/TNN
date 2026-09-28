# R32 E49 — Grounded Quadratic Commit-Value Discriminator Preregistration

Date frozen: 2026-08-28

Status: `EXECUTED_VALID_NATIVE_NEGATIVE — 2026-08-28`

Execution: source SHA256 `62326d5874ae77aa4ceb542807cedfed7e91d72ab158aa453ea1db6aa92214c7`,
double-identical official x86 binary SHA256
`09bf24bc8e181da7096985a26daf14381f62196c0b7a57621f31651ffa2a6869`,
and raw ledger SHA256
`fdc5c08d5637975a673c75610cc25cd63f243a91bb8b8d358a537aed02730d38`.
All integrity checks passed and confirmation remained sealed. The outcome was
`NO_TESTED_GROUNDED_QUADRATIC_RESCUE`: although the quadratic feature was
interior on 36,594 of 55,080 canonical records, it reduced no-unique UNKNOWN by
600 and added 600 wrong commitments relative to the matched joint batch control.
See `R32_E49_GROUNDED_QUADRATIC_COMMIT_VALUE_NEGATIVE_62326D58_NO_TESTED_QUADRATIC_RESCUE_EVIDENCE.json`.

Promotion eligibility: none. E49 is a terminal-controller discriminator; even a
positive result cannot promote R32 without a full native causal qualification.
R27 remains canonical until then.

## Question

E48 established that replacing blocked online updates with a specified complete-
dataset batch fit moves the controller toward abstention but fails the absolute
every-cell no-unique safety gate. E47's two grounded co-presence statistics were
linear inputs. E49 asks one narrower question: can one explicitly grounded,
nonlinear conjunction of those statistics repair the remaining abstention versus
known-resolution tradeoff under the same batch fitting discipline?

This is not a new ambiguity label, a confidence threshold, a probe quota, or a
general neural architecture search.

## Frozen two-model contrast

Construct one fresh E49 set of 55,080 canonical records exactly as E48 did,
after reserving all effective E45–E48 tuples and assigning new E49 nominal seed
ranges. Freeze one auxiliary snapshot before record construction. Validate both
models lockstep on the same fresh seed × mode × resource × time grid, with the
same 20 observations per cell and with confirmation allocated but sealed.

| Model | Representation | Fit |
|---:|---|---|
| M0 | E47 joint representation: slot 3 co-viability and slot 5 support/contradiction co-mass | E48 specified order-invariant batch fit |
| M1 | M0 plus one grounded quadratic feature `q = trunc(slot3 × slot5 / 1000)` placed in otherwise masked terminal slot 13 | the same fit, using that existing zero coordinate |

The quadratic feature is bounded to `[0,1000]`. It is computed exclusively from
the two existing endogenous, causal co-presence statistics. Its helper has no
mode, truth, seed, count, target, resource, or time input. It represents the
conjunction “multiple live hypotheses and simultaneous support/contradiction,”
rather than a supplied ambiguity category.

## Frozen value mechanism

The M0 predictor is exactly the E48 joint fixed-point predictor. M1 differs only
by placing `q` in terminal feature slot 13, which is masked to zero in the E48
terminal projection. The existing learned coefficient for that slot therefore
becomes the quadratic commit-value coefficient. The 33-column batch design is
unchanged: the constant plus 32 terminal features, with slots 3 and 5 projected
from E47 and slot 13 projected from `q` for M1 only. There is no hidden layer,
activation threshold, token classifier, or evaluator-visible feature.

Targets, score clamp, residual clamp, parameter bounds, signed arithmetic,
coordinate order, strict accepted-loss rule, 1,024-sweep integrity ceiling, and
forward/reverse record-order audit are unchanged from E48. All target values for
UNKNOWN remain zero. The UNKNOWN bias, linear weights, and quadratic weight must
remain exactly zero; abstention is still selected only when every commit score is
negative.

## Integrity and gates

Before interpreting validation, require:

- exact fresh-manifest separation from E45–E48 and nonexecution of confirmation;
- identical frozen auxiliary parameters, target hash, and record count for M0/M1;
- complete width-38 canonical records with bounded inputs and exactly zero
  UNKNOWN targets;
- structural variation of `q` (at least one interior record), no helper leakage,
  and zero feature-lattice mismatches;
- forward/reverse equality of sufficient statistics, final parameters, accepted
  sweep count, stop reason, and loss-trace hash for each model;
- full validation grid and exact partitions.

No-unique safety remains at least 700 UNKNOWN per mille and at most 300 wrong
commitments per mille in **every** one of 1,020 no-unique cells. Known
noninferiority remains exact success nondecrease and wrong nonincrease relative
to M0 for the pooled known set, each key mode, terminal time, every terminal key
mode, and at least four joint-passing seeds.

## Frozen outcomes

- `QUADRATIC_COMMIT_VALUE_RESCUE`: integrity passes, M0 is unsafe, and M1
  satisfies all safety and known-performance gates.
- `QUADRATIC_SAFETY_KNOWN_TRADEOFF`: M1 satisfies no-unique safety but fails only
  a known-performance gate.
- `QUADRATIC_SAFETY_GATE_MISS`: M1 improves but does not satisfy every no-unique
  cell.
- `NO_TESTED_GROUNDED_QUADRATIC_RESCUE`: M1 does not satisfy no-unique safety.

Any integrity failure terminates interpretation. A negative bounds precisely this
one grounded quadratic conjunction under the E48 batch arithmetic. It does not
reject richer endogenous representations, other justified nonlinear mechanisms,
or a separately grounded nonzero UNKNOWN value.
