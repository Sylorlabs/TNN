# Slice 16 — State-enumeration completeness

## 1. Slice
Track 1, slice 16: the complete enumerated state-variable list for the variation
prereg, the differential-replay discovery method that proves a variable is missing,
and the dated amendment process for adding one.

## 2. Falsifiable claim
The differential-replay discovery method is sufficient: any missing state variable
whose **output-influence** p (fraction of episodes in which its value changes the
output, given byte-identical logged state and input) is at least **p = 0.01** will
be exposed with probability ≥ 0.99 within **460 differential-replay episode pairs**.
If a deliberately planted missing variable of p ≥ 0.01 survives 460 pairs
undetected, the discovery method is insufficient and this slice's claim is killed.

## 3. Design

**3a. Enumerated state list for the prereg.** Output = f(input, S), S partitioned:

- **S_mem** (deliberate memory): active partition identity; per-slot contents,
  judgment-set strengths, pin flags; tombstones (kill log); CORE contents;
  consolidation/promotion pending queues; composed symbolic recall traces.
- **S_ctrl** (control/budget): reasoning-step budget remaining; deliberation
  budget; verification-bar tightness (RC1: the bar the learner inspects);
  deliberative-standard flags; training-phase/stage indicator (destruction
  firewall stage); scaffold connected/disconnected state; gate thresholds and
  prior gate decisions; overseer force-pin table; pending self-change
  proposals and post-change verification results (RC1 rollback machinery).
- **S_clock** (time): episode index; per-deliberation round/step counters;
  memory age/staleness counters; budget refill schedule; SIGNAL_DISCONNECT
  arming counters.
- **S_hist** (history): recent refusal history (integrity + deliberative, with
  contents — drives temptation counters); last-N verdicts/outputs; suspensive
  contradiction holds (wave9 H1); sensor-spoof / corroboration counters;
  per-source trust-tier assignments (wave9).
- **S_audit**: append-only ledger length and last-entry hash (the audit state
  itself is state; replay to exact state requires it — MA1 58/58).

Every variable is logged at episode boundaries, chunked per the 2^25-byte
slice limit with byte-identical logical semantics (validated workaround).

**3b. Discovery method — differential replay.**
Log (S_logged, input, output) per episode. Alarm rule: if
S_logged¹ == S_logged² byte-identical and input¹ == input² but output¹ !=
output², then either a variable is missing from S_logged or a decision path
violated the no-RNG law. Both are alarms; both get hunted.

```
fn find_missing_var(run1, run2) // same logged state, different output
  for candidate in suspect_unlogged_set:   // S_clock extras, cache lines, env reads
    instrument candidate; rerun both episodes
    if candidate1 != candidate2: return FOUND(candidate)
  return NOT_FOUND  // → escalate: law-2 violation (nondeterminism), not a variable
```

Proactive sweep: perturb each suspect variable while holding S_logged fixed
(controlled twin runs); any output change mandates logging it. Influence
estimate: divergence rate over pairs ≈ p, which calibrates the sample bound.

**3c. Amendment process.**
Adding a variable is a prereg amendment, never silent: dated changelog entry
on the branch; reviewed by the overseer channel; re-approved by Micah
(program law 4 — rule changes need re-approval); then **retroactive
re-validation**: re-run all prior approved legs with the expanded S; old
results must reproduce byte-identically, else the amendment is rejected and
the affected results are re-flagged pending.

## 4. Kill bar
Kill condition K1 (method): a planted missing variable with measured
p ≥ 0.01 goes undetected after 460 differential-replay episode pairs —
the discovery method is dead, revert to manual audit of suspect lists.
Kill condition K2 (enumeration): after adding the discovered variable, a
fresh differential replay still shows output divergence on identical logged
state — the exhaustive-enumeration premise is false; freeze the variation
program until the residual cause (nondeterminism vs structural blind spot)
is identified. Statistical kill: if the observed divergence rate exceeds
0.01 across 460 pairs with no variable found, the scheme is unfalsifiably
leaky and stops.

## 5. Honesty notes
The bound assumes episode pairs sample the regions where the variable
matters — a variable with p ≥ 0.01 *globally* but p ≈ 1 only in a rare
regime could hide if the corpus never visits that regime; coverage is the
real weak link, and the corpus must be audited for regime coverage, not
just episode count. The 460-pair bound is a negative-binomial sampling
argument, not a proof of completeness: absence of divergence is never proof
a variable doesn't exist, only that none with p ≥ 0.01 fired in N pairs.
`NOT_FOUND` escalations will most often be instrumentation gaps in the
suspect set, not genuine nondeterminism — the suspect set itself needs the
same completeness discipline or the method begs the question. I am NOT
claiming enumeration ever terminates; I claim divergence alarms force it to
converge on the variables that matter for output identity.

## 6. Next build step
Build the differential-replay harness on the existing audit infrastructure
(append-only ledger gives (S, input, output) triples for free): implement
hash-compare pairing over logged episode states, inject one planted missing
variable of known p ≈ 0.05 (e.g. an unlogged deliberation-round counter),
and run 460 pairs to verify exposure. Single most informative result:
whether the measured pairs-to-detection matches the 1−(1−p)^N bound.
