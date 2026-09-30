# PREREG: Program 7 Persistence Policy (P7)

Frozen before implementation. This prereg strictly precedes any
implementation file. No implementation exists at prereg time.

## Question

Given the measured principle "schemas amortize; instances do not"
(Invention Economics 9ac23932b: persisted macro net -2084 checks,
retained offset schema net +12 examples; Schema Persistence 2e0f65a2b:
persisted instance net -68 accuracy points, persisted schema net 0),
what persistence policy should a continuing learner follow? When should
it persist, what should it persist, and when should it retire a
persisted structure?

## The policy (P7)

1. DISCOVER. On the first task (or after a retirement), run a cheap
   form check (label monotonicity over the training points, O(13)).
   If it passes, the form is a persist-candidate.

2. PERSIST-DECIDE. Persist the candidate if and only if all three hold:
   (a) it is a re-fittable schema (carries refit parameters, not a
   verbatim solution); (b) a cheap per-task verification gate exists;
   (c) the scale rule net(n) = n * saving_per_use - creation - carrying
   is positive for expected reuse n >= 1, with saving_per_use measured
   on the discovery task, not assumed. Verbatim solution instances
   (frozen cutoffs, macros) are never persisted.

3. APPLY. On each new task, run the verification gate. If it passes,
   refit the schema on REDUCED examples (10 of 13) and apply it. If it
   fails, fall back to fresh learning (full 13 examples, nearest
   neighbor) and do not apply the schema.

4. RETIRE. Maintain a ledger: cumulative accuracy net vs the fallback,
   and a consecutive-rejection counter. Retire the schema if cumulative
   net < 0 OR consecutive rejections >= 2. After retirement the next
   task is treated as a first task, so rediscovery is allowed. The
   retirement itself must be cheap (ledger counters only).

What is persisted: validated re-fittable schemas only (form flag plus
refit procedure). What is never persisted: verbatim solution instances.

## Synthetic workload

Domain: threshold classification, x in 1..100. Train points per task:
x_j = 4 + 7*j + ((11*t) mod 5), j = 0..12 (13 points, ascending).
Reduced set: 10 points, dropping full indices 4, 6, 8 (interior points;
extremes kept so the refit bracket is preserved).

Tasks:
- T1: threshold t=30 (acquisition and discovery)
- T2: threshold t=73 (same family)
- T3: threshold t=20 (same family)
- T4: threshold t=55 (same family)
- T5: parity, label = x mod 2 (different family)
- T6: reversed, label = 1 iff x < 40 (different family)
- T7: interval, label = 1 iff 25 <= x <= 70 (different family)
- T8: threshold t=66 (same family returns; exercises retire then
  rediscover: T5..T7 are three consecutive rejections)

## Conditions

- P7: the policy above. Tracks form_known, consecutive rejections,
  cumulative net ledger, examples consumed, retirement and rediscovery
  events.
- E (persist everything): persists the schema AND the fitted instance
  c1 from T1; reuses the instance verbatim (predict 1 iff x >= c1) on
  every task; consumes 0 new examples. This is the naive "reuse what
  you persisted" behavior.
- N (persist nothing): fresh nearest neighbor on all 13 points every
  task; 13 examples per task; persists nothing.

## Metrics

Per task T2..T8 and per condition: accuracy over x = 1..100, examples
consumed. Totals across T2..T8. Storage in ints. Ledger events
(validation pass or fail per task, retirement event, rediscovery event).

## Kill bars (frozen)

- K1: The policy is defined in this prereg and implemented as
  specified. PASS by construction if the implementation matches.
- K2: The policy is tested on the 8-task workload across the 3
  conditions, deterministically. PASS if all runs complete.
- K3a: total_accuracy(P7) >= total_accuracy(E) + 100 over T2..T8.
  Grounded: the persisted instance lost 68 points over 4 tasks in
  Schema Persistence; over 7 tasks including a reversed family the
  expected deficit exceeds 100.
- K3b: total_examples(P7) <= total_examples(N) - 8 AND
  total_accuracy(P7) >= total_accuracy(N) - 10. Grounded: Invention
  Economics E2 measured 3 examples saved per family with the form
  known; 3 successful schema applications give 9 saved, so 8 is a
  conservative bar. Accuracy parity is grounded in the measured
  schema == fresh-NN result.
- K4: Pure Zag, zero Python at any stage, zero em-dash bytes in loop
  documentation, prereg strictly precedes implementation, 3/3
  byte-identical runs, exit 0, zero stderr.

## Validity bars

- V1: 3/3 byte-identical runs, exit 0, zero stderr on all runs.
- V2: Gate correctness: mono_ok = 1 on T1, T2, T3, T4, T8 and 0 on
  T5, T6, T7.
- V3: Retirement triggers after T6 (2 consecutive rejections) and
  rediscovery occurs at T8 (form check passes, schema re-persisted).

## Verdict rule

POLICY-DESIGNED if K1 through K4 all pass. If K3a or K3b fails, report
honestly which clause failed with the measured numbers; the verdict
becomes POLICY-MIXED with the failing clause named. No bar is moved
after results.
