# PREREG L3B: Residual-growth builder - learner-grown base-language programs

Frozen: 2026-09-30. This prereg is committed alone before any L3B
implementation, run, or result exists. Pure Zag. No Python at any stage.
Builder reports L3B-GROWTH-PASS or L3B-GROWTH-FAIL only. No promotion to
SURVIVES and no L3 claim is made here: partial Criterion 0 evidence is not
L3, and this experiment targets only the C0-A structural question plus the
four frozen behavioral bars.

## 1. Objective

Test whether a learner can grow new executable structure from prediction
failures using generic construction machinery, where the grown structure
is a program in the PRE-EXISTING base language B, executed by the
pre-existing generic base interpreter. Structural difference from
REPEXPAND-1 (downgraded to L2+ at C0-A): REPEXPAND added a new production
to the interpreter (node tag 7, researcher-written apply_rel cases). L3B
adds no production and no semantic case: the grown structure is base
language data, and the source-audit question "where are the semantics of
the grown structure implemented?" must be answerable as "in the
pre-existing base interpreter binterp_eval, which evaluates arbitrary B
programs including ones growth never produced."

## 2. Step 0 name-check (standing rules)

Four standing rules govern this lane. (1) Pure Zag only: every lane
artifact (design, implementation, harness, byte checks, analysis) is Zag
or POSIX shell; no Python is authored or executed at any step, and episode
data are frozen literals in the Zag source, never provisioned by another
language. (2) Fork testing: the frozen bar battery K-RG-1..K-RG-9 is this
lane's test battery; it runs under the pinned znc binary on branch
tnn-native-lab with 3/3 byte-identical reruns as the lane's per-fork
evidence; wave-level enumeration of every fork stays with the parent
coordinator. (3) Pure-Zag red line scope: fixture provisioning counts as
loop work, so all episode lists live as Zag literals. (4) Shell-only byte
checks: em/en dash screening uses only
worker_snippets/check_no_dash.sh, never python3. I honor all four: this
prereg is committed alone before any implementation exists, the
implementation will be pure Zag, the run harness will be POSIX shell, and
no Python check will be used for anything.

## 3. Frozen base predictor language L (provably inadequate)

L is the bounded-template predictor family, frozen as follows.

- An L-expression is one single branch (used by the learner baseline
  bestL) or, for the inadequacy check only, an ALT of 1 to 3 branches.
- A branch is a fixed triple (c0, c1, c2) with each ci in 1..8.
- Prediction semantics: given observed (spec_sym, n, head[2]): if
  spec_sym == '#' and a branch with c0 == n exists (first in canonical
  order), predict (head[0]^c1, head[1]^c2). Otherwise predict nothing
  (failure). Canonical single index: idx = (c0-1)*64 + (c1-1)*8 + (c2-1),
  range 0..511.
- bestL (the frozen simple baseline inside each learner instance): the
  highest-scoring single branch on previous LEARN-phase episodes of that
  instance (score = exact predictions; tie-break: lowest canonical idx;
  episode 1 default: branch (1,1,1)). bestL is trained on LEARN episodes
  only, never on HIDDEN, CONTRADICTION, or FOLLOWUP episodes.

## 4. Inadequacy argument (frozen before learning)

Family A target: E_n^A = (spec='#', n, head, content head[0]^n
head[1]^(2n)) for n >= 1.
Family B target: E_n^B = (spec='#', n, head, content head[0]^(n+2)
head[1]^n) for n >= 1.

Lemma A. A branch (c0,c1,c2) predicts E_n^A correctly iff c0==n, c1==n,
c2==2n. Hence it is correct on at most one E_n^A (exactly the triple
(n,n,2n), which is in range only for n in 1..4).
Proof. The branch fires iff spec_sym=='#' and c0==n. Its prediction is
head[0]^c1 head[1]^c2, which equals head[0]^n head[1]^(2n) iff c1==n and
c2==2n. Two distinct n would require c0 to equal both.

Lemma B. A branch (c0,c1,c2) predicts E_n^B correctly iff c0==n,
c1==n+2, c2==n. Hence it is correct on at most one E_n^B (the triple
(n,n+2,n), in range only for n in 1..6).

Theorem. No ALT of at most 3 branches predicts more than 3 of E_1..E_12
correctly, for either family. Hence no L-expression solves either
infinite target family.
Proof. By Lemma A (resp. B) each branch is correct on at most one of
E_1..E_12. An ALT is correct on an episode iff at least one of its at
most 3 branches is, so at most 3 of the 12.

Computational check (K-RG-1): the frozen program scores all 512
canonical singles on E_1..E_12 for each family and reports the maxima
maxA, maxB. The bar requires maxA == 1 and maxB == 1 (each single
correct on at most one E_n, and the bound is attained, e.g. (1,1,2) on
E_1^A). By the Theorem, any ALT of at most 3 then scores at most 3.

## 5. Frozen base executable language B and its interpreter

B is the arithmetic expression language over observation features.

- Node ops (frozen, the complete set): 1=CONST, 2=VAR, 3=ADD, 4=MUL,
  5=SUB.
- Node record fields: op, left child id, right child id (-1 = none),
  cval (CONST value), feat (VAR feature index).
- Features: F0 = observed spec run length n. (Only F0 is used in this
  experiment; the interpreter maps any other feat to 0.)
- binterp_eval(nid, f0), frozen semantics, standard arithmetic:
  CONST returns cval; VAR returns f0 if feat==0 else 0; ADD returns
  eval(left)+eval(right); MUL returns eval(left)*eval(right); SUB
  returns eval(left)-eval(right); invalid id returns 0.
- The interpreter is delimited in source by INTERP-BEGIN / INTERP-END
  markers. It is frozen as base machinery: the growth machinery in
  sections 6-8 may CALL it but may not add any case, tag, or branch to
  it. Its five ops are the whole of B; no grown structure ever needs a
  sixth.

## 6. Generic construction operators (frozen substrate)

One persistent node store per learner instance, capacity 256 records.

- CREATE(op, cval, feat): allocate the next record with the given op
  (op must be in 1..5), children -1. Returns the id. Allocates only;
  implements no semantics.
- CONNECT(pid, slot, cid): set child slot 0 (left) or 1 (right) of pid
  to cid. Wiring only.
- SPLIT(id): allocate a new record copying op, children, cval, feat of
  id (shallow copy). Returns the new id. Duplication only.
- MERGE(a, b): CREATE(3) then CONNECT left=a, CONNECT right=b.
  Generic combine under ADD.

Every constructor call is appended to a per-growth call log as a
symbolic record: CREATE:op[:val], CONNECT:p:slot:c, SPLIT:id,
MERGE:a:b. The audit (K-RG-9/A3) validates every record.

## 7. Failure monitor (frozen)

- Consecutive-failure counter on the primary hypothesis; threshold T=3
  (frozen).
- Ring buffer of the last 8 failures with features
  (l0, l1, l2, s1, s2, h0, h1): observed spec length, true content
  lengths, true content symbols, head symbols.
- Primary hypothesis: the newest active grown structure if one exists,
  otherwise bestL.

## 8. Residual analyzer (fixed vocabulary, frozen, applied uniformly)

Over the last F=3 failures (F frozen), for each content run j in
{1,2} with l0 the observed spec length, checked in the fixed order:

- EQ if lj == l0 on all 3 failures;
- else MUL(q) if lj == q*l0 with integer q in 1..8 constant on all 3;
- else ADD(d) if lj - l0 == d with d in 0..8 constant on all 3;
- else SUB(d) if l0 - lj == d with d in 1..8 constant on all 3;
- else NONE.

Relation codes: 1=EQ, 2=MUL, 3=ADD, 4=SUB, 0=NONE.
Symbol rule: sj == h[j-1] on all 3 failures (content symbols bound to
head positions, never to literal bytes).
Growth fires iff both runs yield a non-NONE relation and both symbol
rules hold. The vocabulary is never extended per task; family A and
family B are analyzed by the identical code path.

## 9. Growth protocol (frozen)

build_expr(rel, k) assembles a B-expression tree using ONLY the section
6 operators, on a single generic code path parameterized by the
data-determined (rel, k):

- rel=1 (EQ): v = CREATE(2,0,0); return v.                         // VAR(F0)
- rel=2 (MUL): v = CREATE(2,0,0); c = CREATE(1,k,0);
  m = CREATE(4,0,0); CONNECT(m,0,v); CONNECT(m,1,c); return m.
- rel=3 (ADD): v = CREATE(2,0,0); c = CREATE(1,k,0);
  return MERGE(v, c).
- rel=4 (SUB): v = CREATE(2,0,0); c = CREATE(1,k,0);
  m = CREATE(5,0,0); CONNECT(m,0,v); CONNECT(m,1,c); return m.

New growth: r1 = build_expr(rel1,k1), r2 = build_expr(rel2,k2). The
active growth record is {root1=r1, root2=r2, version=v, status=active}.
Emits TRACE-CREATE with instance, phase, episode index, version,
rel1, k1, rel2, k2, evidence count (must equal F=3), and the symbolic
constructor call list.

Revision (supersession): when the analyzer fires while a growth is
active, the old growth is retired with TRACE-RETIRE naming the reason
(contradiction) and the superseding version. For any run whose
(rel,k) is UNCHANGED from the retired growth, the new growth reuses
the old subtree via SPLIT(old_root) instead of rebuilding it; changed
runs are rebuilt with build_expr. The new TRACE-CREATE carries
supersedes=<old version> and names the split reuse.

Phase permissions: LEARN: creation allowed. HIDDEN, FOLLOWUP: frozen
(no creation; the monitor may count but growth is suppressed).
CONTRADICTION: creation allowed (supersession). ABLATION: separate
learner instances with growth disabled.

Prediction with an active growth: r1 = binterp_eval(root1, n),
r2 = binterp_eval(root2, n); predict (head[0]^r1, head[1]^r2). This is
a CALL into the pre-existing interpreter, not a new semantic case.

## 10. Frozen episode lists (no randomness anywhere)

Instance 1, family A, head="ab", spec='#':
- LEARN-A (creation allowed): n in [2,3,5,7,4,6], content a^n b^(2n).
  6 episodes.
- HIDDEN-A (frozen): n in [1,4,8], content a^n b^(2n). 3 episodes.
- CONTRADICTION (supersession allowed): n in [3,6,5], content a^n
  b^(n+4). 3 episodes.
- FOLLOWUP (frozen): n in [5,7], content a^n b^(n+4). 2 episodes.

Instance 2, family B, head="xy", spec='#':
- LEARN-B (creation allowed): n in [2,4,6,3,5,7], content x^(n+2)
  y^n. 6 episodes.
- HIDDEN-B (frozen): n in [1,5,8], content x^(n+2) y^n. 3 episodes.

Ablation instances A1/A2: same episode lists as instance 1
(LEARN-A + HIDDEN-A) and instance 2 (LEARN-B + HIDDEN-B), growth
disabled, bestL trained on LEARN only.

## 11. Pre-registered expected trace

- Inst1 LEARN-A: ep1 (n=2): bestL=(1,1,1), c0=1 != 2, fail. ep2 (n=3):
  bestL=(2,2,4), c0=2 != 3, fail. ep3 (n=5): bestL=(2,2,4), fail.
  Monitor reaches 3: analyzer over eps 1-3 finds run1 EQ, run2 MUL(2),
  symbols bind. TRACE-CREATE v1 (EQ, MUL k=2), evidence=3. eps 4-6
  (n=7,4,6): v1 exact (l1=n, l2=2n).
- Inst1 HIDDEN-A [1,4,8]: v1 exact 3/3.
- Inst1 CONTRADICTION [3,6,5] with law a^n b^(n+4): v1 predicts
  l2=2n: (6 vs 7), (12 vs 10), (10 vs 9): 3 consecutive fails.
  Analyzer finds run1 EQ, run2 ADD(4). TRACE-RETIRE v1
  (reason=contradiction, superseded-by=2). v2 = (SPLIT(v1.root1),
  MERGE(VAR, CONST(4))), TRACE-CREATE v2 supersedes=1.
- Inst1 FOLLOWUP [5,7]: v2 exact 2/2 (l2 = n+4: 9, 11).
- Inst2 LEARN-B: ep1 (n=2): bestL=(1,1,1) fail. ep2 (n=4):
  bestL=(2,4,2) fail. ep3 (n=6): bestL=(2,4,2) fail. Analyzer over eps
  1-3 finds run1 ADD(2), run2 EQ, symbols bind. TRACE-CREATE v1
  (ADD k=2, EQ), evidence=3, built via MERGE for the ADD tree. eps
  4-6 (n=3,5,7): v1 exact (l1=n+2, l2=n).
- Inst2 HIDDEN-B [1,5,8]: v1 exact 3/3 ((3,1), (7,5), (10,8)).
- Ablation: A1 HIDDEN-A 0/3 (bestL=(2,2,4) fires only at n=2);
  A2 HIDDEN-B 0/3 (bestL=(2,4,2) fires only at n=2). Total 0/6.
- Growth-assisted exact predictions: inst1: 3 (LEARN eps 4-6) + 3
  (HIDDEN-A) + 2 (FOLLOWUP) = 8; inst2: 3 (LEARN eps 4-6) + 3
  (HIDDEN-B) = 6. Total 14.

## 12. Kill bars (all evaluated by the frozen program and shell harness)

- K-RG-1 inadequacy: maxA == 1 and maxB == 1 over the 512 canonical
  singles on E_1..E_12 (section 4 computational check).
- K-RG-2 creation: TRACE-CREATE present for inst1 LEARN ep3 with
  (rel1=EQ, rel2=MUL, k2=2, evidence=3) and for inst2 LEARN ep3 with
  (rel1=ADD, k1=2, rel2=EQ, evidence=3); every constructor call in
  both growths validates (CREATE op in 1..5, CONNECT slot in 0..1,
  SPLIT/MERGE ids valid).
- K-RG-3 held-out: HIDDEN-A 3/3 and HIDDEN-B 3/3 (6/6).
- K-RG-4 ablation: ablation instances total <= 2/6 on the HIDDEN sets
  (expected 0/6).
- K-RG-5 reuse count: growth-assisted exact predictions >= 10
  (expected 14).
- K-RG-6 revision: TRACE-RETIRE of v1 present with
  reason=contradiction and superseded-by=2; v2 run2 relation
  (ADD,k=4) differs from v1 run2 relation (MUL,k=2); v2 run1 built by
  SPLIT reuse; FOLLOWUP 2/2.
- K-RG-7 determinism: 3/3 byte-identical raw outputs (shell cmp).
- K-RG-8 purity: pure Zag (no Python authored or executed at any
  stage); check_no_dash.sh clean on all lane files.
- K-RG-9 C0-A audit: A1-A4 all PASS (section 13).

L3B-GROWTH-PASS iff K-RG-1 through K-RG-9 all PASS. The builder
reports L3B-GROWTH-PASS or L3B-GROWTH-FAIL only.

## 13. Frozen C0-A audit procedure

- A1 (shell harness): extract the source region between INTERP-BEGIN
  and INTERP-END in l3b.zag; grep for `== 0`, `== 6`, `== 7`,
  `== 8`, `== 9`: zero matches required. The region must contain the
  five op names CONST, VAR, ADD, MUL, SUB.
- A2 (shell harness): grep the whole l3b.zag for `apply_rel`,
  `COUPLED`, `tag 7`: zero matches required. (REPEXPAND's
  dedicated-production vocabulary must be absent.)
- A3 (frozen program): validate every TRACE-CREATE constructor call:
  CREATE op in {1,2,3,4,5}; CONNECT slot in {0,1} with valid ids;
  SPLIT/MERGE reference valid ids. Emit RG-AUDIT-A3 PASS/FAIL.
- A4 (frozen program): interpreter generality on hand-written
  B-expressions never produced by growth:
  G1: ADD(MUL(VAR,CONST(3)),CONST(2)) at f0=5 -> 17;
  G2: SUB(MUL(VAR,CONST(2)),CONST(1)) at f0=6 -> 11;
  G3: MERGE-built ADD(CONST(2),CONST(3)) -> 5;
  G4: SPLIT-built copy of a MUL(VAR,CONST(3)) subtree at f0=5 -> 15.
  All four exact: emit RG-AUDIT-A4 PASS/FAIL.
- K-RG-9 PASS iff A1, A2, A3, A4 all PASS. The result document answers
  the semantics-location question: "the semantics of grown structures
  v1/v2 are implemented in binterp_eval's cases for the base ops
  {CONST,VAR,ADD,MUL,SUB}, frozen in prereg section 5 independently of
  any growth event; the growth log contains only base-language
  constructor calls."

## 14. Pre-registered defense against the "disguised menu" objection

Objection: the EQ/MUL/ADD/SUB relation templates are a
researcher-enumerated menu, so growth is L2 menu selection.

Frozen response, for the independent adversary to attack: (a) the
templates are generic arithmetic relations over observed features,
and their MEANING lives in the pre-existing interpreter, proven
generic by A4 on expressions growth never produced; (b) the growth
machinery is one generic code path (build_expr) parameterized by
data-determined (rel,k): it adds no semantic case anywhere in
source; (c) the same path yields (EQ,MUL(2)) on family-A residuals
and (ADD(2),EQ) on family-B residuals, so grown content is
data-determined; (d) the ablation (K-RG-4) shows the advantage comes
from the grown structure, and the memorization control bestL scores
0/6 on HIDDEN.

## 15. Honest limitations (frozen)

- The worlds are synthetic and small; L is the bounded-template family
  by design. The claim under test is growth of base-language programs
  via generic constructors, not task difficulty.
- The fixed relation vocabulary {EQ, MUL, ADD, SUB} is a documented
  boundary of the analyzer: a world needing another relation would not
  trigger creation. The vocabulary is applied uniformly, never
  extended per task.
- MERGE is growth-exercised only through the ADD case of build_expr;
  SPLIT is growth-exercised only through revision reuse. Both are
  additionally covered by the A4 generality checks.
- Prediction operates at the run-structure level (symbol, length)
  pairs, which exactly determine the sequences.
- Transfer across changed surface form beyond the head alphabet
  change in family B is not tested in this experiment.
