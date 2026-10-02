# PREREG: L3C v2 Independent Adversary Attack (pipeline step 10)

Date: 2026-09-30. Status: FROZEN. Committed alone before any attack
implementation exists. The families below are designed AFTER this prereg's
freeze in the sense required by the attack protocol: no family vector,
prediction, or bar in sections 4-6 may be altered after results are observed.
Any slip found after the run is disclosed, never edited into a pass.

## 0. Step-0 name check (LOOP_STATE.md standing rules)

The four sections at the top of LOOP_STATE.md that apply to this work are:
(1) Standing owner rules: PURE ZAG ONLY, no Python anywhere in loop work
including implementation, harnesses, analysis, verification, and byte checks;
(2) Standing owner rule: fork testing (not directly applicable; single-branch
mechanism work, no forks created);
(3) Standing ruling: pure-Zag red line scope (fixture provisioning counts as
loop work; I provision no fixtures);
(4) Standing rule: shell-only byte checks (use worker_snippets/check_no_dash.sh,
never python3).
I honor them by writing the attack harness, analysis, and audit in pure Zag
plus shell tools only; running the shell dash check on every committed
document; committing with explicit owned pathspecs after inspecting
git status; freezing this prereg alone first with merge-base verification of
strict precedence; attacking only copies of the committed mechanism (the
committed l3c_v2.zag is never modified); and never touching the prohibited
contaminated paper
(docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md).

## 1. Lineage: what v2 is, what the builder showed, what it did not test

L3C-V2-PARTIAL (prereg 9e595301a, implementation in 20705ab5a): recursive
build_chain, compositional disc2 over full history, deferred construction
(EVID_MIN=2), ambiguity representation, principled observation memory.
Families A (2-conjunction, depth-2 chain), B (deferral + inequality), C (one
nested refine, edge re-pointing), E (full-history conjunction) passed; v1
regression passed; Family D was a prereg arithmetic slip (k=3 predicted,
k=2 provably correct under the frozen spec), not a mechanism failure.
Honest ceiling: bounded L2 at most; no L3 claim; no Criterion-0 claim.

What the builder did NOT test (this attack's targets):
- (i) a SECOND successive refine: refine of a refined edge (graph depth 3).
  The builder demonstrated exactly one refine (Family C). The "recursive"
  in recursive form construction is untested beyond depth 2.
- (ii) the disc2 NONE path (HONEST_FAIL): no frozen family ever produced
  disc2 == 0. The declare-and-withhold behavior on a structural blind spot
  of the predicate vocabulary is untested.
- (iii) refine on a DEFAULT edge: every builder refine targeted a labeled
  edge. The default-edge re-pointing path is untested.

## 2. Static audit findings (analyzed and closed; not empirical families)

Before designing families I read the committed implementation in full.
Three candidate holes were analyzed and CLOSED by the code; they are recorded
here so the empirical families are not wasted on them:

- (S1) Stale nested-clash records: try_refine does not re-walk clash records
  against the current graph. CLOSED: ncl records are only ever created for
  edges returned by trace_last_edge, which always targets a TERM node
  (leaf edges). Interior DISP->DISP edges can never receive records, so a
  re-point (which only ever targets leaf edges) can never alter the walk of
  a vector recorded at a different edge without consuming that record.
  Refines strictly extend the graph at leaves; no record can go stale.
- (S2) Silent misresolution: every interp miss is counted as an event and,
  in the nested case, stashed with its contradiction edge (the e<0 path is
  unreachable: build_chain always emits a default edge). The v1 silent-drop
  is eliminated by construction.
- (S3) disc2 fiat: FOUND requires exactly one separator in the full searched
  vocabulary (levels exhaustive; level-3 bound canonical tightest); the
  scan order cannot matter when nsep==1. AMBIGUOUS counting is exact.
  Minor wart noted (not a break): AMBIGUOUS_MIXED hardcodes ambig=2 rather
  than a real competitor count; trace-only, no behavioral effect.

The empirical families therefore target the untested paths in section 1.

## 3. Attack method

Copy the committed l3c_v2.zag mechanism functions VERBATIM (all functions
before the main-section marker at line 701), append an attack main with
three new families (sigs 701-703) plus structure checks in the builder's
style. The committed mechanism file is never modified; the attack compiles
its own copy. Pure Zag, pinned znc, mode 1, 3 runs byte-identical.

## 4. Frozen families

Notation: observe(W,sig,out,f0,f1,f2,f3,mode). All vectors exact.

### Family F1 (sig 701): depth-3 via successive refinement

Purpose: does the recursion compose, or does it top out at depth 2?

Vectors (mode 1):
- Root: (3,0,0,7)->2 twice; (3,1,0,7)->0 twice.
  disc2: unique (f1==1). Builds D1: default(e_D)->TERM(2),
  labeled(e_L1, f1==1)->TERM(0).
- Refine 1 at e_L1: (3,1,0,9)->7, (3,1,5,9)->7.
  Sub-train: (3,1,0,7)->0 twice (walk e_L1, correctly served).
  disc2: unique (f3==9). Builds D2: default->TERM(0),
  labeled(e_L2, f3==9)->TERM(7). e_L1 re-pointed at D2.
- Refine 2 at e_L2: (3,1,2,9)->3 twice.
  Sub-train: (3,1,0,9)->7, (3,1,5,9)->7 (walk e_L2, correctly served).
  disc2: unique (f2==2). Builds D3: default->TERM(7),
  labeled(e_L3, f2==2)->TERM(3). e_L2 re-pointed at D3.

Frozen predictions:
- REFINE fires twice (two REFINE trace lines, built delta 2 for sig 701).
- Eval 4/4: (3,0,0,7)->2, (3,1,0,7)->0, (3,1,0,9)->7, (3,1,2,9)->3.
- Structure: D1's labeled edge target is D2 (kind 2); D2's labeled edge
  target is D3 (kind 2): graph depth 3, recursion composed.

Honest bar: match -> the recursion claim survives this axis (a pass here
strengthens it; the path was untested). Any failed second refine, silent
misresolution, or non-recursive resolution -> L3C-V2-ADV-BREAK.

### Family F2 (sig 702): disjunction blind spot -> declare and withhold

Purpose: the disc2 vocabulary cannot express OR. Does v2 declare and
withhold, or build something wrong?

Truth: (f1==1 OR f2==9) -> 0, default 2. Vectors (mode 1):
- (3,0,0,7)->2 twice; (3,1,0,7)->0; (3,0,9,7)->0;
  then (3,1,0,7)->0; (3,0,9,7)->0 again.
- disc2 derivation (frozen, checked by hand): level 1: no single equality
  separates (f0==3 in train; f1 splits 1/0 across clash; f2 splits 0/9;
  f3==7 in train). Level 2: the only clash-common equalities are f0==3 and
  f3==7; every 2-conjunction either misses a clash vector or matches the
  train vector (3,0,0,7). Level 3: GE/LE bounds all fail strict separation
  (l=0 vs tmax=0; u=1 vs tmin=0; l=0 vs tmax=0; u=9 vs tmin=0; f3 ties).
  disc2 == 0 -> NONE.

Frozen predictions:
- HONEST_FAIL emitted (at clash_n = 2, 3, 4); built delta 0 for sig 702;
  rule(702) still points at TERM(2) (kind 1).
- Eval at base rate 2/4: (3,1,9,7)->0 predicted 2 (wrong), (3,0,0,7)->2
  (right), (3,5,5,7)->2 (right), (3,1,0,7)->0 predicted 2 (wrong).
- No dispatch built for 702 anywhere in the dump.

Honest bar: withhold as predicted -> acceptable bounded limitation; the
declare-and-withhold design holds on the blind spot. ANY build for 702,
any silent misresolution, or any trace other than HONEST_FAIL/
AMBIGUOUS -> L3C-V2-ADV-BREAK.

### Family F3 (sig 703): refine on a DEFAULT edge

Purpose: the default-edge re-pointing path is untested.

Vectors (mode 1):
- Root: (3,0,0,7)->2 twice; (3,1,0,7)->0 twice.
  disc2: unique (f1==1). Builds D1: default(e_D)->TERM(2),
  labeled(e_L, f1==1)->TERM(0).
- Default-edge nested contradictions: (3,0,0,9)->0, (3,0,5,9)->0.
  Both walk e_D -> TERM(2), contradict. ncl at e_D reaches 2 ->
  try_refine(e_D).
  Sub-train: (3,0,0,7)->2 twice (walk e_D, correctly served).
  disc2: unique (f3==9). Builds D2: default->TERM(2) (e_D's old target),
  labeled (f3==9)->TERM(0). e_D re-pointed at D2.

Frozen predictions:
- REFINE fires once on a default edge (REFINE trace line names the edge;
  the dump shows that edge's lk==0).
- Eval 5/5: (3,0,0,7)->2, (3,1,0,7)->0, (3,0,0,9)->0, (3,0,5,9)->0,
  (3,5,0,7)->2.
- Structure: D1's default edge target has kind==2 (DISP).

Honest bar: match -> the untested path works as designed. Failed refine,
wrong re-pointing, or silent misresolution -> L3C-V2-ADV-BREAK.

## 5. Kill bars

- K1: this prereg is committed ALONE before any attack file exists;
  precedence verified with git merge-base --is-ancestor before the result
  commit. No frozen bar in section 4 may be weakened after results.
- K2: Families F1-F3 run against the frozen predictions of section 4 with
  the committed mechanism unmodified (verbatim copy); all runs 3/3
  byte-identical. Verdict mapping: all three families match frozen
  predictions with no break bar tripped -> L3C-V2-ADV-SURVIVES-THIS-ROUND;
  any break bar tripped (build on blind spot, silent misresolution, failed
  recursion, wrong re-pointing) -> L3C-V2-ADV-BREAK, reported with the
  exact family and mechanism.
- K3: pure Zag at every step (attack copy, build, runs, analysis, byte
  checks); zero Python; no em dashes or en dashes (shell-only
  check_no_dash.sh on every committed document); the committed
  l3c_v2.zag unmodified (verified by diff of the copied prefix);
  the prohibited paper untouched (verified empty diff).

## 6. Anti-widening note

This is an attack, not a builder: no mechanism change is proposed or made.
If a family breaks, the recommendation will be a redesign direction or
retirement, never a per-family patch. The v1 emergence claim stays retired
regardless of outcome; no L3 or Criterion-0 claim is in scope.
