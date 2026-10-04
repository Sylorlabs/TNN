# PREREG: Schema Persistence (Program 6 follow-up)

Date: 2026-09-30. Worker: Schema Persistence Worker.
Status: FROZEN. This prereg is committed before any implementation.
No implementation file exists at prereg time.

## 1. Question

Invention Economics (commit 9ac23932b) found: persisting a bare solution
instance (macro M=[S,W,OZ]) was ECON-NEGATIVE (net -2084 checks), while
persisting a schema (offset-form state) was ECON-POSITIVE (net +12 examples,
break-even at 0% same-form probability). Principle: "Schemas amortize;
instances do not."

This experiment tests that principle in a NEW domain: threshold
classification. Not causal experiments. Not offset learning.

## 2. Domain

Input x is an integer in 1..100. Each task has a hidden rule.
Same-family tasks: label(x) = 1 iff x >= t (single threshold t).
Different-family task: label(x) = x mod 2 (parity).

## 3. Tasks (all fixed, deterministic, no RNG)

Acquisition task T1: t1 = 30. Train set S1 = {8,25,42,58,75,92} (6 examples).
Labels under t1: 0,0,1,1,1,1.

Transfer tasks (same family, new thresholds, new train sets):
- T2: t = 73. S2 = {12,29,46,63,80,97}. Labels: 0,0,0,0,1,1.
- T3: t = 20. S3 = {5,22,39,56,73,90}. Labels: 0,1,1,1,1,1.
- T4: t = 55. S4 = {10,27,44,61,78,95}. Labels: 0,0,0,1,1,1.

Different-family task:
- T5: parity. S5 = {8,25,42,58,75,92}. Labels = x mod 2: 0,1,0,0,1,0.

Test set for every task: all x in 1..100. Metric: accuracy (correct / 100).

## 4. Conditions

(a) Fresh-NN (competent relearning control): nearest-neighbor over the
current task train set only. predict(x) = label of argmin |x - sx| over
stored points; ties broken toward smaller sx. No retained state.

(b) Schema-persist: on T1 the learner runs FORM DISCOVERY: sort S1 by x,
check labels are monotone non-decreasing. If yes, persist form_known = 1
(one integer). On each transfer task: validate (re-run the monotone check
on the current train set). If valid, fit bracket lo = max{x:(x,0)}+1
(default 1), hi = min{x:(x,1)} (default 101), cutoff c = (lo+hi)/2
(integer division), predict(x) = 1 iff x >= c. If invalid (T5), fall back
to exact-match memorizer (seen -> stored label, unseen -> 0).

(c) Instance-persist: fit cutoff c1 on T1 by the same bracket rule and
persist it VERBATIM (one integer), applied to every transfer task with no
refit: predict(x) = 1 iff x >= c1.

(d) Ablated (within-architecture control): form_known forced 0 on transfer
tasks, i.e. exact-match memorizer on current train set only.

Discovery validity: the check must return 1 on S1 threshold labels and 0
on S1 parity labels. Both asserted in the program.

## 5. Accounting

- Creation cost: the discovery check on T1 is one O(6) pass, zero extra
  training examples. Reported as create_extra examples (expected 0).
- Storage: schema = 1 int (form_known). Instance = 1 int (c1). Reported.
  Storage parity is deliberate: the economics must differ despite equal
  storage.
- Net values (accuracy points, vs Fresh-NN, summed over T2..T5):
  net_schema = sum(acc_schema - acc_fresh)
  net_instance = sum(acc_instance - acc_fresh)

## 6. Kill bars

- K1: Instance persistence measured. net_instance calculated and reported.
  PASS iff a numeric net is reported from executed runs.
- K2: Schema persistence measured. net_schema calculated and reported.
  PASS iff a numeric net is reported from executed runs.
- K3: Schema beats instance. PASS iff net_schema > net_instance.
  If not, the result is TIE or INSTANCE-WINS with documented cause.
- K4: Pure Zag, no Python at any stage, zero em-dash bytes in committed
  files. PASS iff verified by inspection.

## 7. Validity bars

- V1: 3/3 byte-identical runs, exit 0, zero stderr.
- V2: discovery returns 1 on threshold labels, 0 on parity labels.
- V3: prereg commit strictly precedes implementation (verified via
  git merge-base --is-ancestor).

## 8. Qualitative expectations (not kill bars)

- Instance is brittle: verbatim c1 should underperform Fresh-NN when the
  new threshold is far from c1 (T2), roughly match when close (T3).
  Expected net_instance < 0.
- Schema should match Fresh-NN on same-family tasks (both are competent)
  at zero retention cost, and degrade gracefully on T5 via the validation
  gate (fallback), while the instance applies blindly.
  Expected net_schema >= 0.
- The principle under test: equal storage (1 int each), different transfer
  economics. Schemas amortize because the form is re-fittable; instances do
  not because the frozen solution decays with task distance.

## 9. Governance

Pure Zag only. No Python at any stage including analysis. No em dashes.
Commits local, owned path only:
docs/lab/research-lead/overnight-20260928/schema_persist/.
Report one of SCHEMA-WINS, INSTANCE-WINS, TIE with exact numbers.
