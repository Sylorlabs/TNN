# RESULT: Program 7 Persistence Policy (P7)

Prereg: 436b8ac24 (frozen before implementation; committed alone;
verified strict ancestor of implementation via git log ordering).
Implementation: persist_policy.zag (this directory).
Raw: P7_RAW_1.txt (md5 bdb63d46bb2429fd3faef3d39a2274ba).
Determinism: 3/3 byte-identical, exit 0, zero stderr on all runs.
Governance: pure Zag, zero Python at any stage; zero em-dash bytes;
prereg strictly precedes implementation.

## Design recap

P7 policy: (1) DISCOVER a form via a cheap check on the first task;
(2) PERSIST only re-fittable schemas, never verbatim instances;
(3) APPLY after a per-task verification gate, refitting on reduced
examples (10 of 13); fall back to fresh learning when the gate fails;
(4) RETIRE when cumulative accuracy ledger < 0 OR consecutive
rejections >= 2; ledger and counters reset per schema incarnation;
rediscovery allowed after retirement.

Workload: 8 tasks, threshold classification x in 1..100.
T1 t=30 (discovery); T2 t=73, T3 t=20, T4 t=55 (same family);
T5 parity, T6 reversed x<40, T7 interval 25..70 (different family);
T8 t=66 (same family returns).

Conditions: P7 (the policy); E (persist everything: schema + verbatim
instance c1, reused blindly, 0 new examples); N (persist nothing:
fresh NN on 13 points, 13 examples per task).

## Numbers (from executed runs, deterministic)

DISCV=1 (form found on T1), C1=30 (fitted instance cutoff).
GATE = 1 1 1 1 0 0 0 1 (accepts T1-T4,T8; rejects T5-T7).

| task | p7 acc | every acc | none acc | p7 examples | event |
|------|--------|-----------|----------|-------------|-------|
| T2 | 100 | 57 | 100 | 10 | schema |
| T3 | 98 | 90 | 98 | 10 | schema |
| T4 | 95 | 75 | 99 | 10 | schema, RETIRE-LEDGER |
| T5 | 44 | 49 | 44 | 13 | discover, gate fails |
| T6 | 97 | 10 | 97 | 13 | discover, gate fails |
| T7 | 97 | 65 | 97 | 13 | discover, gate fails |
| T8 | 99 | 64 | 99 | 13 | discover, REDISCOVER |

Totals T2..T8:
- TOT_P7 = 630, TOT_EVERY = 410, TOT_NONE = 634.
- EX_P7 = 82, EX_NONE = 91 (9 examples saved).
- LEDGER = 0 (reset on retire; T8 incarnation net 0).
- RETIRED = 1, REDISCOVERED = 1.
- Storage: P7 4 ints, E 2 ints, N 0 ints.

## Kill bars

- K1 (policy defined and implemented as specified): PASS. Both
  retirement triggers (ledger < 0, consec >= 2) are implemented;
  ledger and counters reset per incarnation.
- K2 (tested on 8-task workload, 3 conditions, deterministic): PASS.
- K3a (TOT_P7 >= TOT_EVERY + 100): PASS. 630 >= 510, margin 220.
  The verbatim instance is anti-economical across family change
  (T6: 10 vs 97; total deficit 224 points).
- K3b (EX_P7 <= EX_NONE - 8 AND TOT_P7 >= TOT_NONE - 10): PASS.
  82 <= 83 and 630 >= 624. The policy saves 9 examples at a cost of
  4 accuracy points vs competent relearning.
- K4 (pure Zag, no Python, no em dashes, prereg first, 3/3
  identical): PASS.

VERDICT: POLICY-DESIGNED.

## Validity bars

- V1 (3/3 byte-identical, exit 0, zero stderr): PASS.
- V2 (gate 1 on T1-T4,T8; 0 on T5-T7): PASS. Observed
  1 1 1 1 0 0 0 1 exactly.
- V3 (retire then rediscover): MECHANISM VERIFIED with a deviation
  from the predicted trigger. The prereg predicted retirement after
  T6 via 2 consecutive rejections. What happened: the LEDGER trigger
  fired first, after T4 (ledger reached -4 when the reduced-example
  schema scored 95 vs NN 99 on T4). Rediscovery at T8 confirmed.
  The retirement and rediscovery machinery works; the trigger that
  fired differed from prediction.

## Interpretation

1. The policy beats persist-everything by 220 accuracy points. The
   verbatim instance (c1=30) decays catastrophically with task
   distance (T6: 10/100). This replicates the E1 macro (-2084) and
   schema_persist instance (-68) findings: frozen solutions are
   anti-economical.

2. The policy beats persist-nothing on examples (9 saved) while
   staying within 4 accuracy points. The schema compresses learning
   (10 vs 13 examples) at a small refit-noise cost. This replicates
   the E2 offset-schema (+12 examples) finding.

3. Finding on the ledger trigger: the strict ledger < 0 rule fired on
   noise (-4 from a single reduced-refit task), retiring a schema
   that was net-beneficial (9 examples saved). The trigger is
   over-sensitive as specified. A production policy should use a
   tolerance band or account example savings in the ledger, not
   accuracy alone. This is a design finding for Program 7, not a
   bar failure: the prereg rule was implemented literally and the
   kill bars still pass.

4. The consecutive-rejection trigger never fired in this workload
   (the ledger trigger fired first). Both triggers exist in the
   implementation; only the ledger path was exercised.

5. Honest scope: the workload is synthetic and small; the 9-example
   saving is real but modest; the policy's advantage scales with the
   number of same-family tasks (net(n) = 3n - small noise).

## The P7 policy (deliverable)

Persist a structure when: (a) it is a validated re-fittable schema,
not a verbatim instance; (b) a cheap per-task verification gate
bounds misfit; (c) measured saving_per_use > 0. Apply only when the
gate passes, refitting on reduced examples. Retire on sustained
rejection or negative ledger (with a tolerance band in production).
Allow rediscovery after retirement. Never persist frozen solutions.

## Files

- PREREG_PERSIST_POLICY.md (frozen prereg)
- persist_policy.zag (implementation)
- P7_RAW_1.txt, P7_RAW_2.txt, P7_RAW_3.txt (byte-identical raws)
- P7_RESULT.md (this file)
- build.err (93 bytes: znc zagd warning only), run1/2/3.err (empty),
  p7_bin (compiled binary)
