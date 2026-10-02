# PREREG: H1-L2 Integration (learned type contracts drive adaptation)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
The prereg commit is committed ALONE before any implementation source.
No kill bar below may be weakened or reinterpreted after results are seen.

## Hypothesis

H1 learns I/O signatures from observation and uses them to admit or reject
compositions. L2 adapts MAPs via operators triggered by structural
preconditions. The integration hypothesis: a learned signature MISMATCH at
a composition seam can be the TRIGGER for adaptation, and the mismatch TYPE
can SELECT the correct adaptation operator, with no researcher flag and no
per-problem operator choice.

Concretely: the composer first tries contract-admissible singles and pairs
(H1). When a needed pair (A matches the goal input kind, B matches the goal
output kind) has a seam mismatch sig_out(A) != sig_in(B), the learner does
not discard it. The mismatch triggers adaptation. The operator is selected
by the mismatch kind pair:

- OP12 for mismatch (1,2) [have NODE, need NUM]: insert a learned adapter
  P with signature 1->2 between A and B (typed EXTEND of the plan).
- OP21 for mismatch (2,1) [have NUM, need NODE]: insert a learned adapter
  P with signature 2->1 between A and B.

Adapter candidacy is decided SOLELY by the learned contract comparison
sig_in(P)==sig_out(A) and sig_out(P)==sig_in(B). The winning triple is
verified by execution against the goal value.

## World (exact, frozen)

Facts, relation 81 (chain): (31,81,32), (32,81,33), (33,81,34),
(41,81,42), (42,81,43).
Facts, relation 82 (countable): (34,82,101), (34,82,102), (43,82,103),
(43,82,104), (43,82,105).
Distinct fact subjects in first-appearance order:
31, 32, 33, 41, 42, 34, 43.

Previously-learned procedures (behavior induction assumed as prior
learning, same status as xt.zag; the tested claim is mismatch detection
plus operator selection, not behavior induction):

- m0 X, behav 0, chain-follow on r=81 to endpoint.
- m1 Y, behav 4, double: out = 2*v (computed, no facts).
- m2 E, behav 3, count r=81 outgoing (distractor adapter).
- m3 C, behav 1, count r=82 outgoing (adapter).
- m4 D, behav 5, 1-based index into the distinct-subject list above;
  -1 when out of range (adapter).
- m5 D1, behav 2, identity.

Teaching observations (kind probe: 1=NODE iff value appears as a fact
subject, else 2=NUM; signature set by majority once n>=2, same rule as H1):

- X: 31->34, 41->43. Learned sig 1->1.
- Y: 2->4, 3->6. Learned sig 2->2.
- E: 31->1, 34->0. Learned sig 1->2.
- C: 34->2, 43->3. Learned sig 1->2.
- D: 2->32, 5->34. Learned sig 2->1.
- D1: 31->31, 41->41. Learned sig 1->1.

Zero per-MAP signature literals in source: signatures are written only by
the generic finalize step from probe observations, and by generic contract
composition at promotion.

## Battery (exact, frozen)

- TREAT-Z1: teach all six; solve (31 -> 4) with contracts on. Needed pair
  (X,Y): seam mismatch (1,2). OP12 must select a 1->2 adapter: m2 tried
  (triple X;E;Y gives 0, fails), then m3 wins (triple X;C;Y:
  X(31)=34, C(34)=2, Y(2)=4). Expect ans=4, composite (0,3,1),
  composite contract 1->2.
- TREAT-Z2: teach all six; solve (43 -> 34) with contracts on. Needed pair
  (C,X): seam mismatch (2,1). OP21 must select the 2->1 adapter m4:
  triple C;D;X: C(43)=3, D(3)=33, X(33)=34. Expect ans=34, composite
  (3,4,0), composite contract 1->1.
- ABL-C: teach all, delete m3; solve (31 -> 4). The only 1->2 adapter left
  is m2 and its triple fails. Expect Z-FAIL, ans=-2.
- ABL-D: teach all, delete m4; solve (43 -> 34). No 2->1 adapter exists.
  Expect Z-FAIL, ans=-2.
- FRESH: facts only, no teaching; solve (31 -> 4). Expect Z-FAIL,
  ans=-2, zero tries.
- NOTYPE-Z1: ablation build (type_on 0); solve (31 -> 4). Contracts off:
  singles and all pairs tried blindly; the ill-typed direct pair (X,Y) is
  executed (r=68, the wrong operator for a mismatched seam); the
  mismatch-triggered adaptation is replaced by one blind default bridge
  (lowest-id third map, no signature check), which fails. Expect Z-FAIL,
  ans=-2.
- NOTYPE-Z2: ablation build; solve (43 -> 34). Expect Z-FAIL, ans=-2.
- REUSE-Z1: teach all; solve (31 -> 4) twice in the same workspace. Both
  ans=4; the second solve must succeed via the promoted composite as a
  single (Z-SINGLE).

Design-derived trace predictions (not kill bars): TREAT-Z1 emits
MISMATCH a=0 b=1 have=1 need=2, BRIDGE-SEL OP12 for p=2 then p=3, and
Z-COMP3 z=6 a=0 p=3 b=1. TREAT-Z2 emits MISMATCH a=3 b=0 have=2 need=1
(after two failing OP21 attempts on needed pairs (E,X) and (E,D1)),
BRIDGE-SEL OP21 p=4, and Z-COMP3 z=6 a=3 p=4 b=0.

## Frozen kill bars

- K-HL-1: the battery contains a composition problem where X's learned
  signature mismatches what Y needs, in both directions. PASS iff the
  TREAT-Z1 trace emits MISMATCH a=0 b=1 have=1 need=2 AND the TREAT-Z2
  trace emits MISMATCH a=3 b=0 have=2 need=1.
- K-HL-2: the learner detects the mismatch via contract comparison, not a
  researcher flag. PASS iff both MISMATCH lines are present and their
  have/need values equal the signatures printed by the TEACH lines
  (m0 1->1, m1 2->2, m3 1->2, m4 2->1); the detector reads only the
  learned sig_in/sig_out slots.
- K-HL-3: the learner selects the correct adaptation operator based on
  the mismatch type. PASS iff TREAT-Z1 shows BRIDGE-SEL OP12 selecting
  adapters with learned sig 1->2 (m2 tried and rejected on value, m3
  wins) with winning triple Z-COMP3 (0,3,1), AND TREAT-Z2 shows
  BRIDGE-SEL OP21 selecting the adapter with learned sig 2->1 (m4 wins)
  with winning triple Z-COMP3 (3,4,0).
- K-HL-4: adapted composition succeeds. PASS iff TREAT-Z1 ans=4 with
  composite comp_a=0, comp_b=3, comp_c=1 and composite contract 1->2,
  AND TREAT-Z2 ans=34 with composite comp_a=3, comp_b=4, comp_c=0 and
  composite contract 1->1.
- K-HL-5: ablation without type contracts. PASS iff NOTYPE-Z1 ans=-2 with
  trace evidence that the learner tried the wrong operator (the ill-typed
  direct pair emits TRY2 a=0 b=1 r=68) and the blind default bridge fails
  (BLIND-BRIDGE line, r != target), AND NOTYPE-Z2 ans=-2.
- K-HL-6: 3/3 runs byte-identical per binary; sha256 digests recorded in
  REPORT.md.

## Implementation notes (frozen design)

- Single-file `hl.zag`. Solver order per goal: contract-admissible singles,
  then contract-admissible pairs, then the adaptation phase. The adaptation
  phase examines needed pairs (sig_in(A)==goal-in-kind,
  sig_out(B)==goal-out-kind) with seam mismatch; operator selection is
  (have,need)=(1,2)->OP12, (2,1)->OP21; adapter candidacy is purely
  sig_in(P)==have and sig_out(P)==need; p ranges over non-composite maps
  in id order, excluding A and B.
- New map behavior 6: generic triple application (A then P then B);
  composite contract in(A)->out(B) by generic contract composition.
  Map entry grows by one i32 slot (comp_c); fact and map table bounds
  unchanged otherwise.
- Ablation build `hl_na.zag` differs from `hl.zag` by exactly one line
  (`type_on` returns 0 instead of 1), verified by diff, mirroring the L2
  lane's adapt_on methodology. With contracts off, the mismatch detector
  cannot fire; the build tries singles/pairs blindly and then exactly one
  blind default bridge (first pair (m0,m1), lowest-id third map, no
  signature check) before failing.
- Output uses the single-preallocated-buffer emit pattern (e1str/e1i64)
  with one raw write syscall at end of main, per the pinned-znc print
  miscompile workaround. Stdout bytes verified before trusting.
- Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- 0 modes, 0 bridges, 0 handlers, 0 new hardcoded semantic cases. The
  driver runs the treat arms in the type_on=1 build and the notype arms in
  the type_on=0 build; the toggle is a build-time constant, not a
  cognitive mode.
- Deliverables carry zero em/en dash bytes (byte scan at the end).
