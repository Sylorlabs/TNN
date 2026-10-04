# PREREG: H2-L2 Integration (value composition over adapted procedures)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
The prereg commit is committed ALONE before any implementation source.
No kill bar below may be weakened or reinterpreted after results are seen.

## Hypothesis

H2 composes ordered MAP pairs by black-box value passing; the winning
pair is discovered by search. L2 adapts a procedure via EXTEND/TRUNCATE
operators that create derived MAPs in learner state. The integration
hypothesis: when no unadapted pair reaches the goal, the learner adapts
a candidate procedure (TRUNCATE a list output to scalar, or EXTEND a
scalar output to a list), and H2's pair search over the augmented library
then discovers and executes the adapted pair by plain value passing.
The tested claim is adaptation-then-search integration, not behavior
induction: base MAP behaviors are researcher-supplied (same status as
hl.zag), while shapes are learned from teaching observations, derived
MAPs are created by generic operators, and the winning pair is found by
search with no per-problem operator choice.

## World (exact, frozen)

Facts, relation 81 (chain): (31,81,32), (32,81,33), (33,81,34),
(41,81,42), (42,81,43).
Facts, relation 82 (countable): (34,82,101), (34,82,102), (43,82,103),
(43,82,104), (43,82,105).

Learned procedures (behavior induction assumed as prior learning; the
tested claim is adaptation plus pair search, not behavior induction).
Shapes are LEARNED from teaching observations: shape_in is 2 iff taught
inputs were lists (2/3 majority rule), else 1; shape_out is 2 iff taught
outputs were multi-element lists, else 1. Zero per-MAP shape literals in
source: shapes are written only by the generic finalize step.

- m0 X, behav 0, chain-follow on r=81 collecting all successors as a
  list. Teach: X(31)->[32,33,34], X(41)->[42,43]. Learned shape 1->2.
- m1 W, behav 6, plus5: out = v+5 (computed, no facts).
  Teach: W(3)->8, W(4)->9. Learned shape 1->1.
- m2 Y, behav 4, double: out = 2*v (computed, no facts).
  Teach: Y(34)->68, Y(43)->86. Learned shape 1->1.
- m3 L, behav 7, list length: out = element count of input list.
  Teach with list inputs: L([7,8])->2, L([1,2,3])->3. Learned shape 2->1.
- m4 C, behav 1, count r=82 outgoing. Teach: C(34)->2, C(43)->3.
  Learned shape 1->1. Distractor.
- m5 P, behav 8, plus100: out = v+100 (computed, no facts).
  Teach: P(3)->103, P(4)->104. Learned shape 1->1. Distractor.

Generic adaptation operators (domain-neutral arity adapters, not
per-problem semantic cases):

- TRUNC(src): derived MAP, behav 9. Runs src on a scalar input, takes
  the LAST element of its list output as a scalar; -1 on an empty list.
  Derived shape: sig_in(src)->1. Provenance (op=TRUNC, src).
- EXTEND(src): derived MAP, behav 10. Runs src on a scalar input, wraps
  its scalar output as a 1-element list. Derived shape: sig_in(src)->2.
  Provenance (op=EXTEND, src).

Derived MAPs are created in learner state (persistent map table growth)
and reused if the same (src, op) is adapted again. Composite MAPs
(behav 11) apply A then B by value passing; composite shape is the
generic in(A)->out(B).

## Solver order (frozen design)

Per goal (goal input scalar, goal target scalar; goal-in-kind=1,
goal-out-kind=1):

1. Singles: every used MAP with sig_in==1 and sig_out==1, in id order.
   (Includes promoted composites, which enables reuse as a single.)
2. Pairs (H2): every ordered pair (A,B) of non-composite MAPs with
   sig_in(A)==1 and sig_out(B)==1, in id order. Seam match
   sig_out(A)==sig_in(B) -> execute B(A(s)) by value passing, emit
   TRY2 with the piped intermediate value. Seam mismatch -> emit
   SEAM-MISMATCH (considered, not executed).
3. Adaptation phase (only if the build-time constant adapt_on()==1):
   every needed pair (A,B) (non-composite, sig_in(A)==1,
   sig_out(B)==1) with seam mismatch, in id order. The mismatch TYPE
   selects the operator on A:
   - (have=2, need=1) -> A2 = TRUNC(A); try pair (A2,B).
   - (have=1, need=2) -> A2 = EXTEND(A); try pair (A2,B).
   Emit MISMATCH, ADAPT-TRUNC / ADAPT-EXTEND / ADAPT-REUSE, TRY2 with
   piped intermediate. First winning pair promotes composite Z with
   provenance (adapt op, src) inherited from the derived A2, and emits
   Z-COMP2 plus PROV.

If adapt_on()==0 the adaptation phase is replaced by one ADAPT-DISABLED
line and the solve fails. No other behavioral difference between the two
builds (verified by diff: exactly one line).

## Battery (exact, frozen)

- TREAT-T (TRUNC): teach all six; solve (31 -> 68). No unadapted pair
  reaches 68 (verified by enumeration in design). Needed pair (X,Y) has
  seam mismatch (2,1): TRUNC(X)=m6, X'(31)=34, Y(34)=68. Expect ans=68,
  Z-COMP2 z=7 a=6 b=2 adapt=TRUNC src=0, composite shape 1->1.
- TREAT-E (EXTEND): teach all six; solve (3 -> 1). No unadapted pair
  reaches 1 (verified by enumeration in design). TRUNC(X) attempts fail
  on value (X(3) is empty, -1 piped through). Needed pair (W,L) has seam
  mismatch (1,2): EXTEND(W)=m7, W'(3)=[8], L([8])=1. Expect ans=1,
  Z-COMP2 z=8 a=7 b=3 adapt=EXTEND src=1, composite shape 1->1.
- ABL-T: ablation build (adapt_on 0); teach all; solve (31 -> 68).
  Expect Z-FAIL, ans=-2, zero ADAPT lines, SEAM-MISMATCH a=0 b=2 present.
- ABL-E: ablation build; teach all; solve (3 -> 1). Expect Z-FAIL,
  ans=-2, zero ADAPT lines, SEAM-MISMATCH a=1 b=3 present.
- FRESH: facts only, no teaching; solve (31 -> 68). Expect Z-FAIL,
  ans=-2, zero tries.
- REUSE-T: teach all; solve (31 -> 68) twice in the same workspace. Both
  ans=68; the second solve must succeed via the promoted composite as a
  single (Z-SINGLE m=7).

Design-derived trace predictions (not kill bars): TREAT-T emits
MISMATCH a=0 b=1 have=2 need=1, ADAPT-TRUNC src=0 new=6,
TRY2 a=6 b=1 mid=34 r=39, then MISMATCH a=0 b=2, ADAPT-REUSE src=0 m=6,
TRY2 a=6 b=2 mid=34 r=68, Z-COMP2 z=7 a=6 b=2 adapt=TRUNC src=0.
TREAT-E emits ADAPT-TRUNC src=0 new=6 with failing TRY2 lines
(mid=-1), then MISMATCH a=1 b=3 have=1 need=2,
ADAPT-EXTEND src=1 new=7, TRY2 a=7 b=3 mid=[8] r=1,
Z-COMP2 z=8 a=7 b=3 adapt=EXTEND src=1.

## Frozen kill bars

- K-VL-1: a composition requiring adaptation where H2's pair-search
  finds the adapted pair. PASS iff TREAT-T shows ADAPT-TRUNC src=0
  followed by TRY2 a=6 b=2 r=68 with ans=68, AND TREAT-E shows
  ADAPT-EXTEND src=1 followed by TRY2 a=7 b=3 r=1 with ans=1.
- K-VL-2: the adapted procedure executes correctly via value passing.
  PASS iff the winning TRY2 lines expose the piped intermediate value
  produced by the adapted procedure: TREAT-T mid=34 r=68 (X'(31)=34
  passed into Y) AND TREAT-E mid=[8] r=1 (W'(3)=[8] passed into L),
  with ans equal to the goal target in both.
- K-VL-3: ablation: without adaptation, H2's search fails. PASS iff the
  adapt_on=0 build gives ans=-2 for both ABL-T and ABL-E, zero ADAPT
  lines appear in either ablation trace (grep count), and the traces
  show SEAM-MISMATCH a=0 b=2 (ABL-T) and SEAM-MISMATCH a=1 b=3 (ABL-E).
- K-VL-4: provenance shows the adapted pair was used. PASS iff the
  TREAT-T Z-COMP2 line reads z=7 a=6 b=2 adapt=TRUNC src=0 with a
  matching PROV line, AND the TREAT-E Z-COMP2 line reads z=8 a=7 b=3
  adapt=EXTEND src=1 with a matching PROV line.
- K-VL-5: 3/3 runs byte-identical per binary; sha256 digests recorded in
  REPORT.md.

## Implementation notes (frozen design)

- Single-file `vl.zag`. Value representation: (kind, count, up to 4
  elems); apply writes to an explicit output slot, so composite and
  derived application need no recursion.
- Shapes learned from observations by the generic finalize rule; the
  goal form (scalar in, scalar out) is given.
- Output uses the single-preallocated-buffer emit pattern (e1str/e1i64)
  with one raw write syscall at end of main, per the pinned-znc print
  miscompile workaround. u8-backed workspace with ig/put32 helpers; no
  `as *i32` slice construction inside functions. Stdout bytes verified
  before trusting.
- Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- 0 modes, 0 bridges, 0 handlers, 0 new hardcoded semantic cases. The
  adapt_on toggle is a build-time constant, not a cognitive mode; the
  driver runs the treat/fresh/reuse arms in the adapt_on=1 build and the
  ablation arms in the adapt_on=0 build.
- Deliverables carry zero em/en dash bytes (byte scan at the end).
