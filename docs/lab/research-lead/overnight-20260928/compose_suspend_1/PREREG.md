# PREREG.md -- COMPOSE-SUSPEND-1: preregistered implementation of Hypothesis B (SUSPEND)

Date: 2026-10-03. Worker: COMPOSE-SUSPEND-1. Lane:
`docs/lab/research-lead/overnight-20260928/compose_suspend_1/`.
Task type: NON-LEDGER (claim minting paused).

Parent design: COMPOSE-GENERAL-1, REPORT.md Section 5 (Hypothesis B:
SUSPEND, two-phase lazy dataflow: ASSEMBLE then EVALUATE). This
preregistration freezes the mechanism, the worlds, the kill bars
(F-B1/F-B2/F-B3/F-B4), and the verdict rule BEFORE any implementation
file exists. Status of everything below: FROZEN. Any deviation
requires a prereg amendment committed before the deviating run.

## 1. Frozen mechanism: SUSPEND-B

### 1.1 State (persistent learner state across goals in one process)

- Thunk table: tid -> (map-id | -1 for const, in1-tid, in2-tid,
  const-value, kind-mask, size, memo, onstack). Bounded: MAXT=256.
- Intern table: hash-cons on (map-id, in1, in2); const thunks keyed
  by value. Syntactically identical applications are the same thunk
  (identity = tid equality after interning).
- Composite store: (kin, kout, contract-sketch) -> root tid, where
  sketch = sum over the goal inventory of a per-map code from
  (arity, inmask/inmask1, inmask2, outmask) only.
- Per-map execution counters exec[m]; per-thunk execution counters.
- Phase flag: 0 = ASSEMBLE, 1 = EVALUATE. Any MAP execution while
  phase == 0 increments viol_asm (phase-separation violation counter).
- Counters: asm_steps (app-thunks newly interned while phase == 0),
  search_runs (ASSEMBLE enumerations executed), widen (0/1).

Frozen safety caps: SMAX=6 (max candidate DAG depth; non-binding in
the frozen tests), MAXT=256 (assembly fails cleanly if exceeded;
predicted never hit). Sentinels: MISS=-2 (missing fact / failed
application, PAIR6 convention), NOVAL=-999999 (uncomputed memo).

### 1.2 ASSEMBLE (purely symbolic; zero execution by construction)

Regressive need solving over learned kind-set contracts, with needs
as kind-masks (the goal input s is fixed per goal; every derivation
leaf is the const thunk C(s)):

- producers(K): maps in the goal inventory in id order with
  khas(outmask(m), K).
- For 1-input m: alternatives = [C] if khas(inmask(m), kin), then
  the alternative list of need inmask(m).
- For 2-input m: leg1 alternatives = ([C] if khas(inmask1(m), kin))
  then need inmask1(m); leg2 likewise; pairs in (t1, t2) order,
  t1 outer, t2 inner.
- Loop guard (general termination rule, no shape knowledge): a
  (need-kind, producer-id) pair already on the open need stack fails
  that producer choice immediately. Depth bound SMAX as backup.
- Candidate roots: app-thunks with khas(outmask(m), kout), in the
  enumeration order above (need-major, producer id order,
  direct-close before sub-need alternatives).
- Assembly builds the ordered candidate list EAGERLY and
  symbolically (interning only). No MAP executes during assembly;
  viol_asm must stay 0 (F-B4).

Domain-blindness note: every decision above consults only opaque
map ids, arities, kind bitmasks, and tid equality. Relation
numbers, node ids, and kind labels never enter a decision except
as integers compared for equality or bitmask intersection. There
is no diamond handler, no shape template, no mode, and no branch
on domain identity anywhere in this spec.

### 1.3 EVALUATE (demand-driven, identity memoization)

- demand(t): if memo(t) != NOVAL return it; if onstack(t) fail the
  candidate (loop guard; cycles are BOUND, see 7); else evaluate
  input thunks in input order, apply the MAP once
  (exec[m]++, per-thunk counter++), memoize, return.
- Candidates evaluated in assembly order; FIRST candidate with
  value == expected wins (end-to-end verification, as in U/GEN).
- On success the root tid is stored in the composite store and the
  evaluated applications are observe-recorded (mask-OR into
  contracts; idempotent on taught contracts; no prediction depends
  on it).

### 1.4 WIDEN (generalized, exactly once)

If the kind-compatible pass exhausts without success: widen=1, one
admission-relaxed pass: enumerate applications of every inventory
map over thunks with observed non-negative memo values (observed-kind
admission; kind compatibility ignored), 1-input then 2-input, in
(map id, t1, t2) order; first end-to-end success wins. On continued
failure report ANS=-2.

### 1.5 REBIND (persistence: zero-assembly reuse)

On a goal whose (kin, kout, sketch) matches a stored composite:
structural copy of the stored DAG over a fresh const(new_s) via
intern (NOT counted in asm_steps/search_runs), all fresh memos,
then demand. No ASSEMBLE enumeration runs.

### 1.6 REVISE (surgical sub-thunk revision)

Triggered by an inventory-change notification carrying the changed
map-id set M (general rule; the dispatch REBIND-vs-REVISE-vs-fresh-
ASSEMBLE is harness-driven in this build and makes no prediction):

1. Invalidate memos of thunks whose map-id is in M, plus fixpoint
   ancestors (any thunk with an invalidated input). Nothing else.
2. demand the stored root; if == expected, done (no revision).
3. Else find the faulty thunk: among app-thunks reachable from the
   root, the -2-valued thunk of maximum size whose input thunks all
   have values != -2 (the origin of the failure, not its
   consequences); tie: lowest tid. Locate its position (parent tid,
   input slot) by DFS from the root, lowest tid first. Required
   kind K = the parent's slot inmask (inmask/inmask1/inmask2), or
   kout if the faulty thunk is the root.
4. Alternatives: producers q in id order, q != failing map,
   arity(q) == arity(failing map), khas(outmask(q), K), applied
   to the IDENTICAL input sub-thunks: alt = intern(q, inputs).
   For each in order: newRoot = substitute(root, position, alt);
   demand(newRoot); first with value == expected wins and is
   stored as the revised composite.
5. On alternative exhaustion, try the next-deepest -2 position;
   on total exhaustion, fall back to full ASSEMBLE (counted in
   search_runs; predicted never taken in the frozen tests).

## 2. Frozen worlds

Kinds are opaque bit positions: 1 and 2. MAP classes: 0=WALK
(fact lookup), 1=COUNT (fact lookup), 4=ADD2 (s1+s2; -2 if either
input is -2). Missing fact -> -2.

Q1 (diamond, PAIR6 reference world). Inventory base 0, nm=4:
m0 class0 rel91 in{1} out{1}; m1 class1 rel92 in{1} out{2};
m2 class1 rel94 in{1} out{2}; m3 class4 in1{2} in2{2} out{2}.
Facts: (202,91,211), (211,92,3), (211,94,2).
Goal: s=202, kin=1, kout=2, expected=5. True derivation:
X(202)=211, Y(211)=3, W(211)=2, G(3,2)=5.

Q1b (re-query, new input). Same inventory as Q1. Added facts:
(204,91,212), (212,92,2), (212,94,1).
Goal: s=204, kin=1, kout=2, expected=3. Solved via REBIND of the
Q1 composite. True derivation: X(204)=212, Y(212)=2, W(212)=1,
G(2,1)=3.

Q1rev (broken leg). After Q1: retract fact (211,94,2); add map
m4 (id 4) class1 rel95 in{1} out{2} with fact (211,95,2).
Changed set M={2,4}. Goal: s=202, kin=1, kout=2, expected=5.
Solved via REVISE of the Q1 composite. True revised derivation:
G(Y(X(202)), V(X(202))) = G(3,2) = 5.

CHAIN3 (3-link chain). Inventory base 5, nm=3: c0 id5 class0
rel81 in{1} out{1}; c1 id6 class0 rel82 in{1} out{1}; c2 id7
class1 rel83 in{1} out{2}. Facts: (301,81,302), (302,82,303),
(303,83,7). Goal: s=301, kin=1, kout=2, expected=7.

FANIN (fan-in, not a diamond: two independent legs, no shared
intermediate). Inventory base 8, nm=3: f1 id8 class1 rel71
in{1} out{2} fact (401,71,4); f2 id9 class1 rel72 in{1} out{2}
fact (401,72,5); g id10 class4 in1{2} in2{2} out{2}.
Goal: s=401, kin=1, kout=2, expected=9.

PARTIAL (sub-thunk reuse across goals). Same inventory as Q1
(base 0, nm=4). Fresh ASSEMBLE. Goal: s=202, kin=1, kout=2,
expected=3. True root: the Y-leg sub-thunk of Q1's DAG.

Q2 (misleading teaching, PAIR6 analog). Inventory base 11, nm=4:
m0p id11 class0 rel91 in{1} out{1}; m1p id12 class1 rel92
in{1} out{2}; m2p id13 class1 rel94 in{1} out{2};
m3p id14 class4 in1{1} in2{1} out{2} (misleading: taught on
(211,212)->423, so the contract claims NODE inputs).
Facts: (202,91,211), (211,92,3), (211,94,2). ADD2 still
computes addition. Goal: s=202, kin=1, kout=2, expected=5.
Predicted: compatible pass exhausts, widen=1, relaxed pass
finds G(Y(X(C)), W(X(C))) = 5.

Problem order in the main binary (one process; thunk table,
memos, composite store persist): Q1, Q1b, Q1rev, CHAIN3,
FANIN, PARTIAL, Q2.

## 3. Frozen kill bars

Discriminators (the sharpest architectural tests; all must pass):

- F-B4 (phase-separation integrity), on Q1: viol_asm == 0, i.e.
  zero MAP executions occur while phase == 0 (before and during
  candidate-list assembly). Discriminates vs BACKCHAIN, which
  interleaves execution with search.
- F-B3 (single evaluation), on Q1: exec[m0] == 1 over the entire
  run, AND the sum of per-thunk execution counters over the
  winning DAG's thunk set == 4 (X, Y, W, G once each).
  Discriminates vs GEN, whose eager rounds execute X twice on Q1
  (round 1 on 202, round 2 on 211).
- F-B1 (zero-assembly reuse), on Q1b: delta(search_runs) == 0,
  delta(asm_steps) == 0, delta(total MAP executions) == 4,
  ANS == 3. Discriminates vs BACKCHAIN and GEN, which predict a
  full re-search on Q1b (tries comparable to Q1).
- F-B2 (surgical revision), on Q1rev, deltas measured from the
  post-Q1b snapshot: delta(exec[m0]) == 0 AND delta(exec[m1])
  == 0 (X and Y execute 0 additional times), delta(search_runs)
  == 0 (no root re-assembly), the invalidated set contains no
  thunk with map-id 0 or 1, ANS == 5. Discriminates vs GEN and
  BACKCHAIN, which predict from-scratch re-solve (X/Y re-execute,
  tries comparable to Q1).

Regression ground (all must pass):

- R-Q1: ANS == 5.
- R-Q2: ANS == 5 AND widen == 1.
- R-CHAIN3: ANS == 7 (chains are DAGs; the loop guard must not
  block the c1(c0(C)) nesting: the guard is on (need, producer)
  pairs, not need kinds).
- R-FANIN: ANS == 9 (fan-in with no shared intermediate).
- R-PARTIAL: ANS == 3, winning root tid == Q1's Y-leg sub-thunk
  tid (sub-composite reused across goals without the parent),
  delta(exec[m0]) == 0 across PARTIAL.
- R-BLIND: five Q1 variants run as separate fresh processes,
  each printing only the blind summary lines
  PROB / ANS / ASMSTEPS / WIDEN / VERDICT:
  V0 baseline; V1 relation numbers permuted
  (m0->rel94, m1->rel91, m2->rel92, facts rewritten);
  V2 node ids permuted (202->707, 211->708, facts and s
  rewritten); V3 kind polarity swapped (1<->2 everywhere in
  contracts, kin, kout); V4 V1+V2+V3 jointly.
  The five summaries must be byte-identical.

Determinism: the main binary and each blind binary produce
byte-identical stdout across 3 runs (3/3).

## 4. Verdict rule

BUILD-PASS iff every bar in Section 3 passes on 3/3
byte-identical runs. Otherwise BUILD-FAIL, naming the killing
bar and the observed vs predicted values. VOID (terminal) if:
a forbidden interpreter is invoked (automatic PROCESS-FAIL per
the toolchain guard); the prereg is amended after any
implementation commit; a kill bar is altered to force a pass.

## 5. Honest bounds (declared, not tested here)

- Cycles: BOUND. The on-stack evaluation guard and the
  (need, producer) assembly guard fail cyclic candidates; no
  iterate-with-halt construct is built in this lane. GEN's
  five-family cycle envelope (COMPOSE-GENERAL-1 T5) stands
  unmatched.
- Purity: all MAPs in the frozen worlds are pure (T10). Identity
  memoization is unsound for effectful MAPs; SUSPEND is undefined
  for them in this build.
- The WIDEN pass enumerates over observed-good thunks only; a
  world whose solution needs an unobserved intermediate in the
  relaxed pass is out of scope.
- REBIND-vs-REVISE-vs-fresh-ASSEMBLE dispatch is harness-driven
  in this build; the tested claims are the phase behaviors
  (F-B1/F-B2), not autonomous dispatch.
- Contract growth (observe mask-OR) is implemented but no
  prediction depends on it; contracts are pre-taught.

## 6. Commit-order self-check

This PREREG.md and NAMECHECK.md are committed alone, with an
explicit pathspec, before any implementation file exists. The
prereg's first commit strictly precedes the implementation's
first commit. The prereg is adopted as frozen without
modification.
