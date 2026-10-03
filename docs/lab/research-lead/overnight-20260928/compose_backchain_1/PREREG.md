# PREREG.md -- COMPOSE-BACKCHAIN-1: preregistered implementation of Hypothesis A (BACKCHAIN)

Date: 2026-10-03. Worker: COMPOSE-BACKCHAIN-1 (retry; prior worker errored
with no scientific result). Lane:
`docs/lab/research-lead/overnight-20260928/compose_backchain_1/`.
Task type: NON-LEDGER (claim minting paused).

Parent design: COMPOSE-GENERAL-1, REPORT.md Section 4 (Hypothesis A:
BACKCHAIN, goal-directed regressive decomposition). Competitor:
COMPOSE-SUSPEND-1 (Hypothesis B, BUILD-PASS). This preregistration
freezes the mechanism, the worlds, and the kill bars (F-A1/F-A3/F-A4
plus A-vs-B discriminators) BEFORE any implementation file exists.
Status of everything below: FROZEN. Any deviation requires a prereg
amendment committed before the deviating run.

## 1. Frozen mechanism: BACKCHAIN-A

### 1.1 State (fresh per problem: the mechanism is memoryless)

- Thunk table: tid -> (map-id | -1 const, in1, in2, const-val,
  kindmask, memo, onstack). Hash-consed on (map-id, in1, in2);
  consts keyed by value. Bounded: MAXT=4096 (fail-clean if hit;
  predicted never hit).
- Occurrence frames (explicit backtracking stack): one frame per
  open need occurrence. Fields: need-kind K, next-producer cursor,
  current producer m (-1 none), stage, child occ (1-input sub-need
  or leg1), child2 occ (leg2), current leg1 solution thunk p,
  parent occ. A frame yields its next non--2 solution thunk on
  each resume; -1 when exhausted.
- Counters: tries (= total MAP executions; each candidate
  derivation executes exactly one un-memoized MAP application),
  per-map exec[40], widen (0/1), e1 (exec_total recorded right
  after the first candidate derivation is executed).
- No phase flag, no composite store, no rebind, no revise. There
  is no assembly/evaluation split: each completed candidate
  derivation is executed immediately, and end-to-end failure
  drives chronological backtracking.

### 1.2 Search (lazy chronological backtracking; the design 4.3/4.4 walkthrough)

Goal (s, kin, kout, exp). Root occurrence for need kout.
occ_next(frame):
- Pick next producer m in id order with khas_rel(outmask(m), K)
  passing the loop guard (1.3). If none: return -1.
- 1-input: direct-close app(m, C(s)) first if
  khas_rel(inmask(m), kin); then sub-need inmask(m) alternatives
  via a child occurrence, yielding app(m, t) per child solution t.
- 2-input: child occurrence for leg1 need inmask1(m); for each
  leg1 solution p (in order), a FRESH child2 occurrence for leg2
  need inmask2(m) enumerates its solutions q; yield app(m, p, q).
  (Leg occurrences include direct-close as their first
  alternative, so (C,C) pairs are covered with no special case.)
- Every yielded candidate is executed immediately via demand()
  (identity memoization: already-evaluated thunks are memo hits
  and do not re-execute). -2 outcomes are skipped, never yielded.
- Root loop: t = occ_next(root); -1 -> widen (1.4); else
  value(t)==exp -> SUCCESS; else backtrack (resume root).

Enumeration order: producer id order; direct-close before
sub-need alternatives; leg1-outer/leg2-inner. Deterministic.

### 1.3 Loop guard (AMENDED vs design 4.3; reason below)

A (need-kind, producer-id) pair already on the open-need stack
fails that producer choice ENTIRELY (no direct close, no
sub-need expansion). Backup: path depth bound DMAX=16 (frozen).

Amendment reason (recorded pre-implementation, not a post-hoc
fix): design 4.3's guard ("a sub-need identical to a need
already on the open stack fails that producer choice") provably
breaks chain nesting -- c1's sub-need {NODE} is identical to the
open need {NODE} opened by c2's choice, so c2(c1(c0(C))) is
unreachable and CHAIN3 would FAIL. The (need,producer)-pair
guard preserves the design's intent (no infinite regress) while
allowing chains; it is the SUSPEND PREREG 1.2 rule applied
correctly (guard the whole producer choice). Consequence:
design F-A2's "exactly D wasted tries, failed immediately" does
not hold under any chain-compatible guard -- the distractor's
input need is a new (need,producer) pair, so it opens a bounded
sub-search instead of failing instantly. F-A2 is restated as
DIST1 (Section 2): ANS=5, WIDEN=0, terminates. The exact-count
prediction is withdrawn as resting on the unworkable guard.

### 1.4 WIDEN (exactly once)

On observed exhaustive failure of the kind-compatible pass:
widen=1, relaxed=1 (khas_rel always true; needs keep their
kinds), fresh occurrences, thunk memos kept (still valid), one
re-run. On renewed exhaustion: ANS=-2.

### 1.5 Domain-blindness

Every decision consults only opaque map ids, arities, kind
bitmasks, and thunk identity. No diamond handler, no shape
template, no mode, no domain branch.

## 2. Frozen worlds (PAIR6 substrate; classes 0=WALK,1=COUNT,4=ADD2; kinds opaque bits 1,2)

Q1, Q1b, Q1rev, CHAIN3, FANIN, PARTIAL, Q2: identical to
COMPOSE-SUSPEND-1 PREREG Section 2 (same inventories, facts,
goals, expected values).

Q1K (F-A4, goal-kind gating): Q1 inventory; s=202, kin=1,
kout=1 (deliberately wrong), exp=5. Compatible pass must
exhaust (only X produces {NODE}; X(C)=211 != 5), then WIDEN=1
exactly once, relaxed pass finds G(Y(X(C)),W(X(C)))=5.

CHAIN10 (F-A1): base 20, nm=10: c0..c8 ids 20..28 class0
rels 61..69 in{1} out{1}; c9 id29 class1 rel70 in{1} out{2}.
Facts: (501,61,502),(502,62,503),(503,63,504),(504,64,505),
(505,65,506),(506,66,507),(507,67,508),(508,68,509),
(509,69,510); (510,70,801..804). s=501, kin=1, kout=2, exp=4.

DIST1 (F-A2 restated): Q1 inventory + distractor d id4 class0
rel96 in{2} out{1}, no facts. s=202, kin=1, kout=2, exp=5.

Problem order (one process; fresh learner state per problem):
Q1, Q1b, Q1rev, CHAIN3, FANIN, PARTIAL, Q2, Q1K, CHAIN10, DIST1.

## 3. Frozen kill bars

Hand-traced under the frozen enumeration order (Section 1.2).
tries = total MAP executions (each candidate executes exactly
one un-memoized MAP application; memo hits do not count).

- Q1: ANS=5, WIDEN=0, TRIES=7, EXEC(m0..m3)=1 2 2 2, e1=1.
  F-A3: exec(m0)==1 (need memoization; never recomputed).
  F-A-INT (interleaving; complement of B's F-B4): e1==1, i.e. a
  MAP executes during search, before the second candidate is
  even constructed. B predicts 0 executions before its assembly
  completes.
- Q1b: ANS=3, WIDEN=0, TRIES=7.
  F-A-B1 (vs B's F-B1): TRIES(Q1b)==TRIES(Q1). A is memoryless:
  it re-derives per query. B predicts 0 search/assembly steps.
- Q1rev: ANS=5, WIDEN=0, TRIES=9, EXEC(m0)=1, EXEC(m1)=2.
  F-A-B2 (vs B's F-B2): EXEC(m0)>0 AND EXEC(m1)>0 on re-solve.
  A has no surgical revision; it re-searches from scratch. B
  predicts 0 additional X/Y executions.
- CHAIN3: ANS=7, WIDEN=0, TRIES=6.
- FANIN: ANS=9, WIDEN=0, TRIES=4.
- PARTIAL: ANS=3, WIDEN=0, TRIES=3 (memoryless re-derivation;
  contrasts B's sub-thunk reuse).
- Q2: ANS=5, WIDEN=1.
- Q1K: ANS=5, WIDEN=1.
  F-A4: the goal-kind gate holds (WIDEN=0 would falsify); the
  relaxed pass still solves.
- CHAIN10: ANS=4, WIDEN=0, TRIES<=120.
  F-A1: solved with only the frozen depth bound DMAX=16. No
  round cap and no pool cap exist anywhere in the
  implementation. Discriminates vs frozen GEN (round cap 6).
- DIST1: ANS=5, WIDEN=0.
- R-BLIND: five Q1 variants as separate fresh processes (V0
  baseline; V1 relations permuted; V2 nodes permuted; V3 kind
  polarity swapped; V4 all three), each printing only
  PROB/ANS/TRIES/WIDEN/VERDICT. All five summaries
  byte-identical (ANS=5, TRIES=7, WIDEN=0).

Determinism: main binary and blind binary byte-identical
stdout across 3 runs each (3/3).

## 4. Verdict rule

BUILD-PASS iff every bar in Section 3 passes on 3/3
byte-identical runs. Otherwise BUILD-FAIL, naming the killing
bar with observed vs predicted values. VOID (terminal) if: a
forbidden interpreter is invoked; the prereg is amended after
any implementation commit; a kill bar is altered to force a
pass.

## 5. Honest bounds (declared)

- Cycles: BOUND (pair guard + onstack demand guard fail cyclic
  candidates; no iterate-with-halt construct). GEN's cycle
  envelope stands unmatched.
- Purity: all MAPs pure; identity memoization unsound for
  effectful MAPs.
- BACKCHAIN is memoryless by construction: nothing persists
  across goals. Any learning-curve claim belongs to Hypothesis
  C, not A.

## 6. Commit-order self-check

This PREREG.md and NAMECHECK.md are committed alone, with an
explicit pathspec, before any implementation file exists. The
prereg's first commit strictly precedes the implementation's
first commit.
