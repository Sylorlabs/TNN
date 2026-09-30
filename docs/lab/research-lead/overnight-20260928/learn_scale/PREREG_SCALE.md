# PREREG: Learning-to-Learn Scaling

Frozen before any implementation or test execution. This prereg commits
the family specs, the learner mechanism, the conditions, and the kill
bars. Any amendment must be committed transparently and re-frozen before
implementation; no bar may be altered after seeing results.

## Context

Continuing Learner Transfer (TRANSFER-TESTED, `08d7c9fd5`) showed form
transfer to novel values within one relational template
(OPS_P7=53 < OPS_FRESH=60), and the 13 to 10 example improvement is real
but small. This wave scales the result: five related schema families
with a predicted decreasing examples-to-criterion curve, one
adversarial unrelated family testing transfer rejection, and a control
condition isolating the causal learner state.

## 1. Schema forms (researcher-supplied, frozen)

Three forms, fixed before the run. The learner selects among them,
fits their parameters, and tracks a per-form transfer record. It does
not invent forms.

- F0 CONST: obj = c (one parameter).
- F1 LIN: obj = a*subj + b (two parameters).
- F2 EXC: default d, with one exception: at subj == p, obj = e
  (three parameters: d, p, e).

## 2. Family specs (frozen)

Five related families, all instances of F1 LIN with disjoint subject
ranges and distinct (a, b):

- A: a=2, b=1, subj = 10 + i
- B: a=3, b=5, subj = 1000 + i
- C: a=1, b=0, subj = 2000 + i
- D: a=5, b=3, subj = 3000 + i
- E: a=2, b=9, subj = 4000 + i

One adversarial family, an instance of F2 EXC, unrepresentable by F0 or
F1 once the exception is in evidence:

- X: default d=7, exception at subj=5001 (i=1) with obj=3,
  subj = 5000 + i.

Example i of family f is (subj, obj) with obj given by the true
function above. The example stream per family is unbounded
(subj = base + i); the learner stops consuming when it reaches
criterion.

## 3. Learner mechanism (frozen)

Persistent state across families (within a condition): live_form
(-1 none, else 0/1/2), fitted params (p0,p1,p2), uses[3] (per-form
count of families brought to criterion), strikes[3] (per-form count
of refit/verify rejections).

Phases within one family:

- DISCOVER (live_form == -1): buffer examples. When the buffer holds
  at least BMIN examples, try forms in prior order (descending
  uses[form], ties broken by lower form index) and adopt the first
  form whose fitted parameters predict ALL buffered examples
  exactly. If no form fits and the buffer reaches BMAX, declare
  UNLEARNABLE (adopted = -1, cost = BMAX).
- REFIT (live form carried into a new family): buffer exactly R
  examples, then fit the live form. If it fits, keep it with refit
  parameters and enter VERIFY. If it fails, record a strike for the
  form, set live_form = -1, KEEP the R refuting examples as the start
  of the discovery buffer (a real learner does not discard its
  counterexamples), and enter DISCOVER.
- VERIFY (live form with fitted params): predict each new example.
  Count consecutive correct (vc). Reach criterion when vc == V, where
  V = max(1, ceil(V0 / 2^uses[form])), uses taken before this family.
  If wrong predictions reach WMAX during verify, record a strike,
  abandon the form (live_form = -1), and enter DISCOVER with an empty
  buffer. On reaching criterion: adopted = form; uses[form]++ unless
  the condition freezes uses.

Frozen parameters: BMIN=6, R=4, V0=14, WMAX=3, BMAX=40.

Fitting rules (exact integer arithmetic):
- F0 fits iff all buffered objs equal.
- F1 fits iff the first two buffered points determine integer (a, b)
  with (o1-o0) divisible by (s1-s0), and all buffered points satisfy
  obj == a*subj + b.
- F2 fits iff all-but-one buffered objs are equal (that value is d)
  and the remaining one differs (at subj p with obj e).

## 4. Conditions (frozen)

- FRESH: state fully reset before each family. Six independent runs
  (A, B, C, D, E, X). Baseline cost per family.
- RETAINED: one sequential run A, B, C, D, E, X with persistent
  state. Transfer may accumulate.
- CONTROL: one sequential run A, B, C, D, E, X with persistent
  state EXCEPT uses[] frozen at 0 (no transfer record accumulates).
  Isolates uses[] as the causal state behind any decreasing curve.

Metric: examples to criterion = examples consumed in the family
(discover/refit buffer + verify predictions), counted exactly.

## 5. Model predictions (derived from the frozen mechanism)

- FRESH: every family 20 (discover 6 + verify 14; X discovers F2,
  6 + 14).
- RETAINED: A=20, B=11 (refit 4 + V=7), C=8 (4 + V=4), D=6 (4 + V=2),
  E=5 (4 + V=1); X=20 (refit 4 fails with strike, discover keeps the
  4 refuting examples, 2 more to BMIN, F2 adopted, verify 14).
- CONTROL: A=20, B=C=D=E=18 (refit 4 + V=14, uses frozen), X=20.

These are predictions, not kill bars. The kill bars below test the
qualitative pattern; exact numbers are reported and compared.

## 6. Kill bars (all must pass)

- K1 (spec): all 6 families executed with the preregistered distinct
  specs. Code check: family count == 6 and the emitted spec table
  matches section 2.
- K2a (decrease): retained costs strictly decreasing A > B > C > D > E.
- K2b (savings per family): each retained B, C, D, E cost is below
  its fresh counterpart.
- K2c (total savings): sum(retained A..E) * 10 < sum(fresh A..E) * 6
  (retained total below 60 percent of fresh total).
- K3a (rejection): in RETAINED X, strikes[F1] >= 1 and adopted form == 2.
- K3b (return to fresh): retained X cost within [fresh X cost,
  fresh X cost + 6].
- K3c (no wrong-form application): retained X adopted form != 1.
- K4 (purity and determinism): pure Zag at every stage (source, znc
  build, execution, analysis); zero Python invocations; zero em-dash
  or en-dash bytes in all wave files (byte-checked); 3/3
  byte-identical runs, exit 0, zero stderr.

Supporting check (reported, must hold for the causal claim):
- K2d: CONTROL B..E costs show no decrease (all equal), proving the
  decreasing RETAINED curve comes from the accumulating uses[]
  record and not from family order or difficulty.

Verdict SCALE-TESTED iff K1, K2a, K2b, K2c, K3a, K3b, K3c, K4 pass.

## 7. Trace plan

The program emits, per family per condition: cost, adopted form,
uses[3] before the family, V required, refit outcome (ok/fail/na),
and strikes[3]. The result document must name the exact learner
state responsible for (a) positive transfer (the uses[] counter
driving V through V = max(1, ceil(V0 / 2^uses))) and (b) transfer
rejection (the refit-fit predicate failing on X, the strike, and
the kept refuting examples seeding F2 discovery), citing the
emitted values.

## 8. Honest scope (preregistered)

Three researcher-supplied forms; the learner selects, fits, keeps,
and rejects, but does not invent forms. Bounded L1/L2, not L3.
Transfer is form reuse with shrinking verification, not cross-task
transfer. The adversarial family is learnable by a known form (F2);
true open-form rejection is out of scope.

## Commit order

This prereg is committed alone. The implementation commit must be a
strict descendant. Verified via git merge-base --is-ancestor before
the result is reported.
