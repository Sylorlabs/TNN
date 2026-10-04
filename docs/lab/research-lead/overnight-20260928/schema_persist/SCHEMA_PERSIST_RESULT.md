# RESULT: Schema Persistence (Program 6 follow-up)

Prereg: 4b1d709c0 (frozen before implementation; verified below).
Implementation: schema_persist.zag (this directory).
Raw: SP_RAW_1.txt (md5 f9d801a75de68a25cef8b12cf58b93ca).
Determinism: 3/3 byte-identical, exit 0, zero stderr on all runs.
Governance: pure Zag, zero Python at any stage; zero em-dash bytes;
prereg commit 4b1d709c0 strictly precedes implementation (implementation
file untracked at prereg time; verified via git log).

## Design recap

Domain: threshold classification, x in 1..100. Same-family tasks have
label(x) = 1 iff x >= t. T5 is parity (label = x mod 2).
- Fresh-NN: nearest-neighbor on current task only (competent relearning).
- Schema-persist: threshold form discovered on T1 via monotone check
  (persisted: 1 int flag); per-task validation; bracket refit; midpoint
  cutoff; memorizer fallback when validation fails (T5).
- Instance-persist: bracket-fitted cutoff from T1 (c1 = 34) persisted
  VERBATIM (1 int), applied with no refit.
- Ablated: form forced 0, exact-match memorizer (within-architecture
  no-generalization control).

## Numbers (from executed runs, deterministic)

Discovery: DISCV_THR = 1 (threshold accepted), DISCV_PAR = 0 (parity
correctly rejected). The form check is real, not assumed.
C1_FITTED = 34 (the learner's own fitted estimate from T1, frozen as the
instance; the true t1 = 30 is never given to the learner).

| task | fresh NN | schema | instance (cutoff 34) | ablated |
|------|----------|--------|----------------------|---------|
| T2 (t=73) | 99 | 99 | 61 | 74 |
| T3 (t=20) | 94 | 94 | 86 | 24 |
| T4 (t=55) | 98 | 98 | 79 | 57 |
| T5 (parity) | 52 | 52 | 49 | 52 |

Net values vs Fresh-NN (accuracy points, summed T2..T5):
- NET_SCHEMA = (99-99)+(94-94)+(98-98)+(52-52) = 0
- NET_INSTANCE = (61-99)+(86-94)+(79-98)+(49-52) = -68

Storage: schema 1 int, instance 1 int (deliberate parity).
Creation: 0 extra examples for both (discovery is one O(6) pass on T1).

## Kill bars

- K1 (instance net measured): PASS. net_instance = -68.
- K2 (schema net measured): PASS. net_schema = 0.
- K3 (schema beats instance): PASS. 0 > -68. VERDICT: SCHEMA-WINS.
- K4 (pure Zag, no Python, no em dashes): PASS by inspection.

## Validity bars

- V1: 3/3 byte-identical, exit 0, zero stderr. PASS.
- V2: discovery 1 on threshold, 0 on parity. PASS.
- V3: prereg precedes implementation. PASS.

## Interpretation

1. The instance is brittle: -68 net vs competent relearning. Verbatim
   cutoff 34 scores 61 vs 99 on T2 (distant threshold) and 79 vs 98 on
   T4; it only approaches competence when the new task is near the old
   one (T3: 86 vs 94). A frozen solution decays with task distance.

2. The schema is a free, safe asset: 0 net vs competent relearning at
   1 int retention and 0 creation cost. It never hurts. On the
   different-family task its validation gate correctly rejects the form
   and falls back gracefully (52, tied best); the instance applies
   blindly (49, worst of all conditions).

3. Honest note: schema == fresh-NN exactly on every task. Given the same
   train data, bracket-midpoint and nearest-neighbor coincide here (the
   operative NN boundary is the midpoint of the extreme inner points, the
   schema cutoff is the midpoint of the bracket; they differ by at most a
   tie-break). The schema's value is therefore NOT a better predictor. It
   is: (a) free retention of a validated form, (b) a validation gate that
   bounds misfit on out-of-family data, (c) +136 over the amnesiac
   memorizer: (99-74)+(94-24)+(98-57) = 25+70+41 = +136 on same-family
   tasks (T5 excluded, all conditions tie at 52 there): the value of
   having any generalizing form at all.

4. Instance vs amnesia: +68 ((61-74)+(86-24)+(79-57)+(49-52) =
   -13+62+22-3). The instance beats total amnesia but loses to
   relearning. Better than nothing, worse than learning. That is exactly
   "instances do not amortize": retention without re-fittability is a
   liability the moment the task moves.

## Relation to Invention Economics

E1 (macro): -2084 checks. This experiment's instance: -68 accuracy
points. Same pattern: frozen solutions are anti-economical across task
change. E2 (offset schema): +12 examples with misfit bounded at 0. This
experiment's schema: 0 net vs competence, misfit bounded by the
validation gate (T5: 52 vs instance 49). Same pattern: re-fittable forms
are safe assets. The principle replicates in a new domain with equal
storage (1 int each), isolating transfer economics from storage cost.

## Files

- PREREG_SCHEMA_PERSIST.md (frozen)
- schema_persist.zag (implementation)
- SP_RAW_1/2/3.txt (raw outputs, byte-identical)
- build.err, run1/2/3.err (empty: zero stderr)
