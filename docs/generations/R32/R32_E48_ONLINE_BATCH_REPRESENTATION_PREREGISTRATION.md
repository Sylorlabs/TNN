# R32 E48 — One-Pass Online vs Batch Fit × Representation Preregistration

Date frozen: 2026-08-23

Status: `EXECUTED_VALID_NATIVE_NEGATIVE — 2026-08-28`

Execution: source SHA256 `24e8098f805fa1f1548250ac5c7968658caeb8293534b2cb5f2ae0d06d442d0a`,
double-identical official x86 binary SHA256
`5efdab6533f66fabe9ef90c9edd6092e8c90cceeef58c8fe44e1fd4dc680a884`,
and raw ledger SHA256
`0df6a38241c63275f0fd2eea15154875dadbce46580921811ba7fcec00f5d950`.
Integrity passed; confirmation remained sealed. The preregistered outcome was
`NO_TESTED_BATCH_SAFETY_RESCUE`: batch baseline passed 346/1,020 no-unique cells
and batch joint passed 318/1,020, so neither completed the absolute safety gate.
See `R32_E48_ONLINE_BATCH_REPRESENTATION_NEGATIVE_24E8098F_NO_TESTED_BATCH_SAFETY_RESCUE_EVIDENCE.json`.

Promotion eligibility: none. This is a terminal-controller causal discriminator,
not a full R32 qualification. R27 remains canonical regardless of the result.

## Question

E46 observed that the frozen terminal head is highly presentation-order sensitive.
E47 showed that two structurally varying causal co-presence features do not rescue
the blocked one-pass online head. E48 asks whether a specified order-invariant
batch fit changes the outcome, with and without those two features. It is a fit
rule discriminator, not proof that presentation overwrite is the sole cause.

## Frozen four-model 2×2

All models use one frozen auxiliary snapshot and one fresh E48 multiset of 55,080
canonical width-38 records. Each record contains 32 baseline features, the two
E47 statistics, and four targets; it is shared across all four arms.

| Model | Fit | Representation |
|---:|---|---|
| M0 | E47 blocked one-pass online update, rate 34 | slots 3 and 5 zero |
| M1 | E47 blocked one-pass online update, rate 34 | joint E47 slots 3 and 5 |
| M2 | order-invariant batch linear fit | slots 3 and 5 zero |
| M3 | order-invariant batch linear fit | joint E47 slots 3 and 5 |

The joint statistics and helper boundary are unchanged from E47:

- slot 3: `clamp(min(epoch_evidence_A, epoch_evidence_B)/4, 0, 1000)`;
- slot 5: `clamp(min(option_support, option_contradiction)/4, 0, 1000)`;
- evaluator mode, truth, seed, time, count, targets, and resource labels are not
  inputs to the representation helper.

UNKNOWN retains grounded target zero. E48 tests whether all three commit values
can be fit below that grounded zero where commitment is unwarranted; it does not
introduce an UNKNOWN class, confidence threshold, ambiguity label, or fixed probe
count.

## Batch-fit definition frozen before validation

The batch arms use the E47 per-term fixed-point predictor: score equals the
action bias plus `trunc(weight_j × feature_j / 1000)` summed over 32 features,
then clamped to `[-4000, 4000]`. Residual is `clamp(target-score, -3000, 3000)`.
The accepted loss is the sum of squared residuals over every record and all four
actions, evaluated by that exact predictor in signed 64-bit arithmetic.

For each representation separately, construct a 33-column design where column 0
is constant 1000 and columns 1–32 are the applicable feature values. Build these
complete-dataset sufficient statistics in signed 32-bit storage using signed
truncation toward zero per term:

- `G[j,k] = sum(trunc(column_j × column_k / 1000))`;
- `C[j,a] = sum(trunc(column_j × target_a / 1000))`.

The per-term bounds are 1,000 for `G` and 2,000 for `C`, so their complete sums
are bounded by 55,080,000 and 110,160,000 respectively—inside signed 32-bit
range. Every coordinate calculation, parameter-weighted sum, loss, and comparison
uses signed 64-bit arithmetic before clamping back to an integer parameter.

Starting from exact zero, each action has a deterministic coordinate sweep in the
fixed column order 0–32. For coordinate `j`, substitute the rounded nearest
integer solution of the scaled normal equation:
`q_j = round_nearest((1000*C[j,a] - sum(k != j, G[j,k]*q_k)) / G[j,j])`.
Bias is clamped to `[-4000,4000]`; weights are clamped to `[-16000,16000]`; a
zero diagonal forces its parameter to zero. Coordinate order is fixed but record
order cannot affect the statistics or a sweep.

At the end of every complete four-action sweep, recompute the exact accepted loss
from the frozen E47 predictor. Retain a sweep only if it strictly lowers loss. If
no parameter changes, or the candidate fails strict loss decrease, restore the
last retained snapshot and stop. A 1,024-sweep ceiling is an integrity abort only;
hitting it forbids interpretation. The batch arms are independently rebuilt from
zero using forward and reverse record traversal; they must match in sufficient
statistics, final parameters, accepted-sweep count, stop reason, final loss, and
loss-trace hash.

No validation outcome may tune this arithmetic, stopping rule, features, or
targets.

## Fresh matched construction

1. Reconstruct and reserve every effective E45, E46, and E47 seed tuple before
   assigning E48 stages 8–11.
2. Allocate nominal IDs 48001–48003 for auxiliary training, 48101–48103 for
   canonical terminal records, 48201–48206 for validation, and sealed 48301–48306
   for confirmation. Confirmation is allocated but not executed.
3. Train one auxiliary snapshot, clone/freeze it, then construct canonical records
   once without terminal-model updates.
4. Train M0 and M1 in exact blocked lockstep order. Fit M2 and M3 only from the
   stored records with order-invariant complete-dataset steps.
5. Prove zero initialization, exact 55,080-record coverage, identical targets,
   correct baseline/joint projection, frozen auxiliary parameters, zero feature-
   lattice mismatch, forward/reverse batch identity, strict monotone retained
   batch loss, and nonexecution of sealed confirmation.
6. Validate all four models lockstep on the same fresh seed × mode × resource ×
   time grid, exactly 20 observations per cell, retaining E47 pooled, key-mode,
   terminal-time, per-cell, and per-seed arithmetic.

Any integrity failure terminates interpretation.

## Frozen gates and causal labels

For each model, no-unique safety requires UNKNOWN at least 700 per mille and wrong
commitment at most 300 per mille in every one of 1,020 cells. Known noninferiority
is relative to M0: exact success nondecrease and wrong nonincrease in pooled known
cases, each key mode, terminal time, every terminal key mode, and at least four
joint passing seeds.

- `BASELINE_SPLIT_AMBIGUOUS`: M0 unexpectedly passes no-unique safety.
- `ONLINE_JOINT_FEATURE_RESCUE`: M1 completes while M0 is unsafe; reported
  separately and never sufficient for the E48 batch gate.
- `BATCH_BASELINE_FEATURE_RESCUE`: M2 completes and M3 does not.
- `BATCH_JOINT_FEATURE_RESCUE`: M3 completes and M2 does not.
- `BATCH_RESCUE_BOTH_REPRESENTATIONS`: M2 and M3 both complete.
- `BATCH_ABSTENTION_TRADEOFF`: no batch arm completes, but a batch arm passes
  absolute no-unique safety and fails a pure known-performance gate.
- `INCONCLUSIVE_BATCH_GATE_MISS`: no batch arm completes, a batch arm passes
  safety, but the miss is not pure known-performance harm.
- `NO_TESTED_BATCH_SAFETY_RESCUE`: neither batch arm passes absolute safety.

The primary label is exclusive, with integrity failure and baseline ambiguity
taking priority. The E48 gate is PASS only when integrity passes, M0 is unsafe,
and M2 or M3 completes. It prints four matched contrasts—M1−M0, M2−M0, M3−M1,
and M3−M2—and the difference-of-differences as diagnostics only.

## Bounded interpretation

A negative result bounds these four specified fit/feature combinations. It does
not establish that no linear solution exists, nor reject nonlinear grounded value
heads, richer endogenous causal statistics, or an explicitly grounded nonzero
UNKNOWN value. A positive result remains diagnostic and cannot promote R32 without
full native causal qualification.
