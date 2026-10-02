# R33 parameter and capacity scaling matrix

Status: prospective design; no scaling campaign executed. Prerequisites: relevant
sensory qualification, complete state/telemetry, source-frozen training family,
freshness checks and bounded native resource preflight. Canonical R27 unchanged.

## Historical boundary

[E51M](R32_E51M_RESULT.md) and [E51N](R32_E51N_RESULT.md) already tested scalar
calibration dose × 0/4/8/16 hinges. The fresh N grid was non-monotone with
tradeoffs. Printed dose/capacity flags describe isolated local improvements,
not a monotonic scaling law. Do not repeat it as the R33 capacity study. AJ's 130 mutable residual
coefficients are only two diagnostic heads, not the total TNN parameter count.
Inherited experts, feature construction, memory, routing and optimizer state
must be counted separately.

## First fixed-family matrix

Freeze one generic cell-bank family before varying its capacity: 64 admitted
input coordinates, H identical local cells, one cell nonlinearity, two output
residual heads, fixed optimizer/precision/learning rule. This is a proposed
experimental family, not an already adopted learner architecture. Establish
the family and its training implementation before the scale study. Use a
zero-contribution extension of the named parent wherever preservation permits.

For a dense single-layer bank with trainable input weights, cell biases,
output weights and two output biases, `P(H)=64H+H+2H+2=67H+2`.
Logical weighted connections are `66H`; bias parameters are not connections.
These are design counts, not measured performance or total brain capacity.

| Level | H | Added stored parameters | Added parameter bytes at i32 | Dense active parameters |
|---|---:|---:|---:|---:|
| Very small | 8 | 538 | 2,152 | 538 |
| Small | 32 | 2,146 | 8,584 | 2,146 |
| Medium | 128 | 8,578 | 34,312 | 8,578 |
| Large | 512 | 34,306 | 137,224 | 34,306 |
| Very large for this bounded family | 2,048 | 137,218 | 548,872 | 137,218 |

Add parent, gate, memory-policy, optimizer, indices, activations and retained
experience to obtain total resident/logical bytes. Larger than this initial
family is not forbidden; extend only after measured resource/stability curves.

Cross each level with fixed cumulative presentation checkpoints
1,080/4,320/17,280/69,120, recording unique experience and replay separately.
Use at least three paired fresh development populations as an initial
exploratory design, not high-confidence proof from three samples. Specify
population size, overlap, unseen-context probes, order and holdout rule before
allocation. A source-frozen successor preregistration must lock these details.
No stages or new scientific data have been allocated by this plan.

## Separate structural axes

After the fixed-family curve, vary one axis while holding the others fixed:
more admitted features; more cells/experts; greater within-cell capacity; more
routed regions; local interaction depth; recurrent/temporal state; sparse versus
dense connectivity; shared versus specialized parameters; memory-policy capacity;
architecture-policy capacity. Feature expansion must not silently add semantic
information, and recurrence must not add future state.

For E regions of the above bank and a dense scalar gate per region, a proposed
count is `E*(67H+2)+65E`. With K active regions, active parameters include
`K*(67H+2)+65E`; the gate is not free. Count instantiated and lazily represented
connections separately. Equal K does not mean equal compute if gating, retrieval
or cache behavior differs. Pin actual formulas to the implemented topology.

## Required curves and metrics

Stored and active parameters; total/active/effective/materialized connections;
parameter/state/memory bytes; training and inference operations/time; learning
speed; final and fresh capability; transfer; forgetting/interference; delayed
retention; stability/overflow; and capability per resource. Show every level,
seed, checkpoint and negative result, with denominators and uncertainty.

Separate comparisons at matched experience, matched active inference compute,
matched training compute and matched retained capability. These are different
estimands, not simultaneous equality by assertion. Charge teacher help, memory
retrieval, replay, optimizer sweeps and architecture search.

Questions include whether larger sparse storage helps at equal active compute,
whether specialization beats a dense bank, whether better memory beats more
weights, which component saturates, and whether capacity helps or harms
retention. Plateau diagnosis requires adequate training and usable sensory
information; it does not establish an ultimate capacity limit.

## Stop rules

Resource/integrity failure terminates the affected arm and preserves partial
evidence. A plateau is declared only under a preregistered practical improvement
margin over successive dose checkpoints and fresh evaluation; no post-hoc peak
selection. Any extension is a new registered batch. Never shrink memory or
restart the continuing brain to make a larger arm appear stable.
