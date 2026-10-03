# XDOMAIN-L2 REPORT: Cross-Domain L2 Adaptive Reuse (arithmetic to planning)

Date: 2026-10-02. Branch: tnn-native-lab. All commits local; nothing pushed.

## Question

C262 found cross-domain composition L1 PASS but L2 FAIL: no adaptation
operator, only exact reuse of whole MAPs. C269 killed H1/H2/H3 invention on
sum-then-plan and XIO failed. The question here: given an ADAPTATION
operator (rebind a learned structure to a new interface) that the LEARNER
drives, can H1 and H2 solve a Z that exact L1 reuse cannot?

## Design (frozen in PREREG.md, commit 418db9bd4, before implementation)

World from the first (superseded) arith_plan prereg: X=SUM over (s,71,v)
with X(101)=15, X(102)=10; Y=ALLOC n/5 with Y(15)=3, Y(10)=2; D1=MAX and
D2=IDENT distractors. Sealed facts for fresh subject 103: (103,74,100)
distractor inserted FIRST, then (103,73,6), (103,73,9). Z=(103,93)->3
requires rebind X to relation 73: X'(103)=15, Y(15)=3. The distractor path
(100->Y(100)=20) must be rejected by the learner, not skipped by the
researcher.

REBIND operator (generic): copy MAP, set param to a candidate relation,
inherit the learned signature, record rebound_of provenance. Candidates
come from a generic scan of the sealed world for the query subject,
first-seen order, with no domain knowledge. Neither the operator, the
scan, nor the composer contains the target relation or the answer.

## Implementation

- l2_h1.zag: H1 typed contracts (from xdomain_typed/xt.zag) plus
  parameterized SUM/MAX, generic REBIND, two-phase solver. 10 MAP slots,
  40 fact slots, 8 candidate slots. Compiles clean with the pinned znc
  (one analyzer warning fixed; final build warning-free).
- l2_h2.zag: H2 value composition (from xdomain_causal_interv/ci_h2.zag)
  plus relation-parameterized stages, two-phase retry over candidates.
  8 MAP slots. Compiles clean.
- Both: pure Zag, 0 modes, 0 bridges, 0 handlers, 0 new semantic cases,
  single preallocated output buffer with one raw syscall write at the end.

## Results

Kill bars K1 through K7 are frozen in the prereg. All seven PASS.

- K1 H1-L2-SOLVE: PASS. TREAT-L2 trace shows Z-COMP z=6 a=5 b=1 with
  REBOUND a=5 param=73 rebound_of=0 (a rebound of X id 0, paired with Y
  id 1, rebound param differs from training param 71).
- K2 H2-L2-SOLVE: PASS. TREAT-L2 trace shows VC-COMPOSE ok m1=1 m2=2
  rel=73, with rel 73 != rel_train 71.
- K3 L1-NECESSARILY-FAILS: PASS both. L1-ONLY arm prints L1-FAIL for H1
  (6 tries: 2 singles, 4 pairs) and H2 (9 ordered pairs), then
  PASS-expected-fail.
- K4 CAUSAL: PASS both. ABL-X, ABL-Y, FRESH all print the expected fail
  with l2_on=1. H1 ABL-X even rebinds D1 (MAX) and rejects 100->20 and
  9->1, showing the distractor rebind is tried and discarded, not
  skipped. H1 ABL-Y tries only rebound singles (no Y to pair with) and
  fails. H2 ABL-X composes (ALLOC,ALLOC) and (MAX,*) under both
  candidates and fails; ABL-Y has no valid stage-2 and fails.
- K5 REBIND-DISCOVERED: PASS both. grep for 73 across each source: the
  only hits are the add_fact world-setup lines. No 73 in rebind, scan,
  or composer code or comments.
- K6 DETERMINISM: PASS both. 3/3 runs byte-identical.
  H1 sha256: 0dd8e67761a37ad08efb4eca9da318cbd826deb79b5efcc48aa505c21d2f6a7f
  H2 sha256: 2bd7afaa5541bb0418dc0fd3346548d6b2487e4e2281301c29953f83fcdcc9af
- K7 NO-TEMPLATE: PASS both. No 103/15/3 literals in composer, rebind,
  or scan logic. Every hit classified: add_fact world setup, arm harness
  query literals (the Z query itself, explicitly allowed), behavior/mode
  ids (bh==3 is the IDENT id; modes 1..3), bit-shift constants, and
  variable names. No 15 anywhere.

## Per-mechanism adaptive scores

Adaptive score = kill bars passed that govern that mechanism (K1/K2 are
mechanism-specific; K3-K7 apply to both).

- H1 (typed contracts + REBIND): 7/7. Solves Z only via Phase 2
  adaptation; exact reuse provably insufficient; binding discovered by
  the learner from the sealed world.
- H2 (value composition + L2 relation retry): 7/7. Solves Z only via
  Phase 2; all 9 L1 ordered pairs fail; the winning (SUM,ALLOC) pair is
  found under the scanned relation 73 after 74 is exhausted.

## Honest analysis

1. What is actually demonstrated: a learner-driven adaptation operator
   (REBIND) lets both H1 and H2 cross the exact-reuse gap on one
   arithmetic-to-planning world. The binding choice is made by the
   learner through type filtering plus composition validation against
   the sealed goal, with the distractor met first and rejected on
   value, not on identity. This is L2 adaptive reuse, not L1 exact
   reuse, and not L3 invention: the operator itself is researcher-built.

2. Y taught on X outputs (disclosed): Y's signature is learned from
   observations of X's training outputs as inputs. This is signature
   teaching, not paired X+Y training for Z: Y never sees (103,93) or
   the answer 3, and the L1-ONLY arm proves Y's presence alone does not
   solve Z. But it is a scaffold the prereg allowed, and a stricter
   variant would teach Y on independent numeric facts.

3. Phase-2 pair scope (disclosed): the rebound MAP is tried as a single
   and then paired with every MAP including the originals and (in H1)
   other rebounds. The winning pair is (rebound-X, Y). The search is
   type-gated, so the scope is principled, but it is broader than
   "rebound then compose with the single known partner." The provenance
   check (K1) pins the actual winning structure regardless.

4. Single sealed world: the claim is one world, one Z query. No
   transfer, no second adversary world, no scaling. This is an L2
   existence proof, not generality evidence.

5. Distractor handling: the candidate scan meets 74 first by
   construction. H1 rebinds X to 74, computes 100->20, rejects it
   because it does not equal the goal. The rejection is value-driven,
   which is the honest mechanism, but note the goal value itself
   supplies the selection pressure (as the prereg designed).

## Toolchain incident (transparency)

During this session a concurrent worker wrote l2_h1.zag/l2_h2.zag into
this directory using a syntax without statement semicolons; neither file
compiled (E0001 unexpected end of input) and the worker stalled. Those
files are preserved unmodified under sibling_draft_uncompilable/ for the
record. The implementation committed here is a complete independent
implementation written after the prereg freeze. The prereg commit
(418db9bd4) strictly precedes all implementation commits, satisfying the
prereg commit-order self-check.

## Verdict

XDOMAIN-L2-COMPLETE. H1 adaptive score 7/7, H2 adaptive score 7/7.
The L2 adaptation operator the C262 recommendation called for now exists
for both mechanisms and is learner-driven on a sealed world. Next: a
second sealed world with a different adaptation shape (truncate or
specialize rather than rebind), and the stricter Y-teaching variant.
