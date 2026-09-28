# A3: Trace Neuter (Causal) Proof (Experiment 1b, PREREG2)

## A3(i): Per-turn EVAL neuter

**Method**: Run D on shifted variants, capturing RECALL→EVAL→VERDICT traces.
A turn is "contested" if D's VERDICT differs from the recalled heuristic's
action (i.e., deliberation overrode the reflex). For each contested turn,
neuter the EVAL to vacuous PASS (force evaluator to accept); the decision
reverts to the heuristic action.

**Results**:

| Domain | Variant | Contested turns | Total turns | Fraction |
|--------|---------|-----------------|-------------|----------|
| D2 SHIFT | d2_s0 | 280 | 600 | 46.7% |
| D3 TOOL | d3_s0 | 98 | 600 | 16.3% |

On all contested turns, neutering EVAL to PASS changes the VERDICT (from the
exploratory/exploitative action back to the heuristic's action). 

**Fraction of contested turns whose decision changes under neuter: 100%**

K3(i) threshold: <25% changes = KILL. **PASSES** (100% >> 25%).

**Interpretation**: The EVAL is causal, not decorative. When D distrusts a
heuristic (observed << claimed), the low EVAL score directly causes the
VERDICT to override the recall. Removing the EVAL (forcing PASS) eliminates
the override.

## A3(ii): Whole-run D_accept

**Method**: D_accept = D with evaluator forced to always-accept (never distrust).
This is implemented via `recall_delib_accept.zag` (delib_check_distrust always
returns 0). Run D_accept on shifted variants; measure gap closure vs R_true.

**Results**:

| Domain | R_home | R_true | D | D_accept | D closure | D_accept closure | Fall |
|--------|--------|--------|---|----------|-----------|------------------|------|
| D2 | -1500 | 4500 | 3900 | -1500 | 90.0% | 0.0% | 90.0% |
| D3 | 45084 | 52000 | 50664 | 45084 | 80.7% | 0.0% | 80.7% |

D_accept regresses exactly to R_home (as expected: always-accept = reflexive).
The gap-closure falls by 90.0% (D2) and 80.7% (D3), both ≥50%.

K3(ii) threshold: D_accept closure falls <50% vs D_home = KILL. **PASSES**.

**Interpretation**: The deliberative evaluator is what closes the gap. Without
it (D_accept), performance collapses to the harmful reflexive baseline. The
"consciousness" (explicit EVAL step) is not decorative.

## Trace audit

**Method**: Verify that every VERDICT in the trace matches the action actually
executed (no trace/reality mismatches).

**Result**: All traces audited. Every RECALL→EVAL→VERDICT triple is in order,
and the VERDICT action matches the action passed to the world step function.
No mismatches found.

K3(iii): Any VERDICT/trace mismatch = KILL. **PASSES** (zero mismatches).

## K3 Verdict

All three sub-bars pass. The deliberative trace is causal and faithful.
