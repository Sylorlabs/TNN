# PREREG: L3C Protocol v2 (recursive form-constructing dispatcher)

Date: 2026-09-30. Status: FROZEN. Committed alone before any implementation.

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
I honor them by writing implementation, harness, analysis, and audit in pure
Zag plus shell tools only; running the shell dash check on every committed
document; committing with explicit owned pathspecs; freezing this prereg alone
first with merge-base verification of strict precedence; and never touching
the prohibited contaminated paper
(docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md).

## 1. Lineage: what v1 was, what the adversary proved

L3C-FORM-PASS (prereg dc9a91501, result e663864f5): a learner with no
conditional form at start built dispatch structure from five generic ops on
contradiction events. Honest scope was NOT L3, NOT Criterion 0.

L3C-ADVERSARY-PROTOCOL-SMUGGLING-PROVEN (repro 7fae6a188, attack prereg
7af24029e, results c96875d36): independent reproduction passed byte-identical,
then the adversary broke the emergence claim. construct() always emits the
identical shape (one DISP node, two TERM nodes, unlabeled default edge, one
labeled (fi==fv) edge); interp() implements exactly the matching fixed
semantics. The conditional FORM is researcher-supplied; only the (feature,
value) pair is data-driven: parameter fitting of a supplied template, the
same pattern behind the H-PROCLANG1/REPEXPAND-1 downgrades. The v1
"emergence" claim is RETIRED and stays retired regardless of v2's outcome.
v1 is not promoted as a C0-A candidate.

The adversary's forcing exhibits (frozen falsifiers for v2):
- (A) Conjunction needed (sig 501): honest fail, events=2, built=0, eval 2/4.
  Forcing: conjunctive predicates or nested dispatch emission.
- (B) Threshold needed (sig 502): eager overfit then dead end. construct()
  fires on the FIRST clash observation (cc=1); disc() overfits (f1==9) from a
  single sample; the second clash vector (f1=10) dead-ends (return code 2).
  Forcing: deferred/evidence-accumulating construction plus a revision path.
- (C) Nested dispatch (sig 503): SILENT dead end. Nested contradictions
  return code 2,2: counted as events, never constructed, never flagged
  unresolved, vectors not even stashed. Forcing: stash on the DISP branch and
  recursive construction re-pointing EDGE targets (construct() currently only
  re-points the rule slot). This is the principal structural exhibit: v2
  passes only if C resolves with NO per-family source change.
- (D) Underdetermined separator (sig 504): silent misresolution. (f1==1),
  (f2==9), and (f3==9) are all consistent with every observed vector; disc()
  takes the first scan-order hit; held-out 2/4 with silent misresolutions.
  Forcing: ambiguity representation instead of first-hit fiat.
- (E) Stash-window forgetting (sig 505): silent misresolution. stash() keeps
  2 vectors per class, so disc() builds (f1==1), contradicting
  actually-observed (but unstashed) training data. Forcing: principled
  observation memory; the discriminator must reason over the full stored
  history, never a 2-vector window.

## 2. v2 design: the dispatch form itself is constructed

v2 replaces the fixed six-op construct() and first-hit disc() with generic
construction machinery. There are five uniform mechanisms, none of which is
a per-family semantic case:

### 2a. Recursive constructor with edge re-pointing

`build_chain(atoms, natoms, default_target, new_out)`: given an ordered atom
list (a discovered predicate), emits one DISP node per atom in a nested
chain: node D_i carries the default (unlabeled) edge to default_target and
the labeled edge carrying atom i to D_{i+1}; the last labeled edge points to
TERM(new_out). For natoms=1 this degenerates to the v1 shape. For natoms=2 it
emits nested dispatch. The nesting depth of the emitted form equals the arity
of the discovered predicate: the FORM is determined by the data-driven
predicate, not fixed in source.

`try_construct_root(s)`: on corroborated root contradiction (rule slot still
points at a TERM node), discriminates the full observation history and, on
success, re-points the RULE SLOT at the new chain (as v1 did).

`try_refine(s, e)`: on corroborated nested contradiction (interp misses at a
DISP node; the walk took edge e), discriminates the sub-problem (vectors that
traversed edge e and were correctly served vs the new contradicting vectors)
and, on success, re-points EDGE e's TARGET at the new chain, whose default
edge points at e's old target. This is recursive form construction: the
dispatch graph grows at the point of contradiction, to the depth the evidence
requires. interp() is generalized to recurse into DISP targets (v1 assumed
TERM targets).

### 2b. Compositional discriminator (disc2)

disc2 searches a compositional predicate space in fixed simplest-first order
over the FULL stored history (never a window):
1. Single equality atoms (fi==v): separates iff it matches every clash vector
   and no train vector.
2. Conjunctions of 2 distinct-feature equality atoms (max arity 2, frozen).
3. Inequalities: for each feature fi, GE candidate bound L = min over clash
   of fi, valid iff L > max over train of fi (tightest consistent lower
   bound, a frozen canonical tie-break, not first-hit); LE candidate bound
   U = max over clash of fi, valid iff U < min over train of fi.
At each level: exactly 1 separating predicate -> FOUND; more than 1 ->
AMBIGUOUS (count recorded); 0 -> next level; level 3 with 0 -> NONE
(honest fail).

### 2c. Deferred construction (EVID_MIN = 2, frozen)

No construction fires on a single clash observation. Root construction
requires clash_n >= 2 for the signature; nested refinement requires >= 2
contradicting vectors at the same edge. A lone surprising observation is
stored as evidence, never acted on. This directly answers Family B's eager
overfit. Consequence, disclosed: v1's original scripts used single clash
observations with eager construction; v2's regression therefore presents each
clash vector twice (as the adversary's families already do). The regression
tests the same contradiction types with corroborated evidence.

### 2d. Ambiguity representation (Family D answer)

When disc2 finds more than one separating predicate, v2 does NOT build. It
records the ambiguity count for the signature, emits an AMBIGUOUS trace line
naming the competing atoms, and leaves the TERM mapping untouched.
Underdetermination is explicitly represented; silent misresolution is
eliminated by construction. If later evidence disambiguates (new clash
vectors change the separator set), construction is retried (attempt marker
per signature).

### 2e. Principled observation memory (Family E answer)

Every observation is appended to a per-signature history log (capacity 32
vectors per signature, frozen; 16 signatures; 20 bytes per vector). disc2
reasons over the entire stored log. The capacity bound is disclosed; no
frozen family exceeds 6 vectors per signature, so the bound never binds in
this evaluation. The v1 bug (reasoning over a 2-vector window and
contradicting observed-but-unstashed data) cannot occur: any vector the
discriminator could contradict is in the log it reasons over.

### 2f. Revision path (Family B second half, generality)

On nested contradiction the protocol refines at the edge of contradiction
(2a). Additionally, root re-discrimination always uses the full history, so a
dispatch built on early evidence is rebuilt from all evidence if the root
contradiction recurs before any dispatch exists. Post-construction
contradictions at the root cannot occur (rule slot points at DISP); they
arrive as nested contradictions and are handled by try_refine.

## 3. Memory layout (65536-byte workspace, all offsets frozen here)

- 0..511: rule table, 16 slots x 32 bytes. +0 sig, +4 node, +8 hist_n,
  +12 clash_n, +16 ambig (0 or competing-separator count), +20 built_flag,
  +24 nclash_n (pending nested vectors), +28 last_attempt_n.
- 512..1023: nodes, 64 x 8 bytes. +0 kind (1=TERM, 2=DISP), +4 val.
- 1024..2559: edges, 64 x 24 bytes. +0 from, +4 to, +8 lk (0 default,
  1 labeled), +12 fi, +16 op (0=EQ, 1=GE, 2=LE), +20 fv.
- 3072..3583: report area, 16 sigs x 32 bytes: natoms + 2 atoms x (fi,op,fv).
- 4096..: counters: +0 nodes, +4 edges, +8 events, +12 built, +16 unresolved,
  +20 ambig_events.
- 8192..18431: observation history, 16 sigs x 32 vecs x 20 bytes
  (f0,f1,f2,f3,out).
- 18432..21503: pending nested-clash buffer, 16 sigs x 8 recs x 24 bytes
  (edge,f0,f1,f2,f3,out).
- 22016..22815: discriminator scratch (train 32x20, clash 8x20).

The five generic ops (op_new_node, op_mark_term, op_mark_disp, op_new_edge,
op_label_edge) remain the only mutators of node/edge state; history appends
are observation memory (the v1 stash role), generalized to the full log.

## 4. Frozen falsifiers: Families A-E (exact adversary vectors)

All vectors are the adversary's exact observation scripts from attack_main.zag
(commit 7af24029e), run with construction ENABLED (mode=1). Predictions are
frozen here before implementation.

### Family A (sig 501): conjunction required
Observations: (3,0,1,7)->2, (3,1,0,7)->2, (3,0,0,7)->0, (3,0,0,7)->0.
Frozen predictions:
- No construction after the first clash vector (deferral holds at root).
- disc2 finds no single equality; finds exactly one 2-conjunction
  (f1==0 AND f2==0); emits nested chain D_a1 -[f1==0]-> D_a2 -[f2==0]->
  TERM(0), defaults -> TERM(2). The emitted form has depth 2: form
  construction demonstrated on a non-nested input family.
- eval: 4/4 ((3,0,1,7)->2, (3,1,0,7)->2, (3,0,0,7)->0 twice).
- Structure check: rule(501) -> DISP; its labeled edge target is a DISP node
  (kind==2); chain carries atoms (1,EQ,0) then (2,EQ,0).

### Family B (sig 502): threshold required
Observations: (3,5,0,7)->2, (3,6,0,7)->2, (3,9,0,7)->0, (3,10,0,7)->0.
Frozen predictions:
- After the first clash vector (3,9,0,7): built delta for sig 502 is 0
  (deferral directly observed; the v1 eager-overfit path is closed).
- After the second clash vector: disc2 finds no equality and no conjunction;
  finds exactly one inequality (f1,GE,9) with the frozen tightest-bound rule
  (L = min clash f1 = 9 > max train f1 = 6); builds single dispatch
  default -> TERM(2), labeled (f1,GE,9) -> TERM(0).
- eval: 4/4. No dead end: both clash vectors resolve.

### Family C (sig 503): nested dispatch (principal structural exhibit)
Observations: (3,0,0,7)->2 twice, (3,1,0,7)->0 twice, (3,1,0,9)->7 twice.
Frozen predictions:
- Root: after two (3,1,0,7)->0 clashes, disc2 finds unique (f1==1); builds
  D1: default -> TERM(2), labeled (f1,EQ,1) -> TERM(0).
- Nested: the first (3,1,0,9)->7 observation contradicts at D1's labeled edge
  and is STASHED (the v1 silent drop is closed); the second triggers
  try_refine: sub-train = history vectors that traversed the labeled edge
  and were correctly served ((3,1,0,7)->0 twice); sub-clash = ((3,1,0,9)->7
  twice); disc2 finds unique (f3==9); builds D2: default -> old target
  TERM(0), labeled (f3,EQ,9) -> TERM(7); D1's labeled edge target is
  re-pointed from TERM(0) to D2.
- eval: 6/6. Structure check: D1's labeled edge target has kind==2 (DISP):
  recursive emission demonstrated. No per-family source change: the
  re-pointing path is the generic try_refine used for every nested
  contradiction.

### Family D (sig 504): underdetermined separator
Observations: (3,0,5,7)->2, (3,0,6,7)->2, (3,1,9,7)->0 twice.
Frozen predictions:
- disc2 finds three separating single equalities: (f1==1), (f2==9),
  (f3==9). Count > 1 -> AMBIGUOUS, ambig=3 recorded for sig 504, AMBIGUOUS
  trace line naming the competitors, NO dispatch built (rule(504) still
  points at TERM(2)).
- held-out eval against the untouched TERM: (3,1,5,7)->2 correct,
  (3,0,9,7)->2 wrong (true 0), (3,1,9,7)->2 wrong (true 0), (3,0,5,7)->2
  correct: 2/4. The score equals v1's, but the failure mode is converted
  from silent misresolution to explicit represented ambiguity: this is the
  pass criterion for D, not the score.
- No silent misresolution: the emitted trace contains AMBIGUOUS sig=504 and
  no dispatch is built for 504.

### Family E (sig 505): full-history conjunction
Observations: (3,0,0,7)->2, (3,0,1,7)->2, (3,1,0,7)->2, (3,1,1,7)->0 twice.
Frozen predictions:
- disc2 over the full history finds no single equality (the v1 2-window
  artifact (f1==1) is contradicted by the retained third training vector
  (3,1,0,7), which is IN the log); finds exactly one 2-conjunction
  (f1==1 AND f2==1); builds nested chain.
- observed eval: 5/5, including (3,1,0,7)->2 (the vector v1 misresolved).

## 5. Regression: v1 builder families (same vector sets, clash x2)

v1's scripts used single clash observations with eager construction. v2
requires corroborated contradiction (EVID_MIN=2, section 2c), so each clash
vector is presented twice, exactly as the adversary's families do. The vector
SETS are unchanged; the regression bar is the same eval scores.

- sig 67: train (1,1,0,7)->2 twice; clash (1,1,1,7)->0 twice. Expect dispatch
  with unique (f2==1); eval 6/6 (each vector checked twice, as v1).
- sig 131: train (0,1,0,7)->2 twice; clash (0,1,1,7)->0 twice. Expect (f2==1);
  eval 6/6.
- sig 327: train (0,3,0,7)->4 twice, (1,3,0,7)->4 twice; clash (0,3,0,9)->1
  twice, (1,3,0,9)->1 twice. Expect unique (f3==9); eval 4/4.

## 6. Kill bars

- K1: this prereg is committed ALONE before any implementation file exists;
  precedence verified with git merge-base --is-ancestor before the result
  commit. No frozen bar in sections 4-5 may be weakened after results; any
  arithmetic or predictive slip found after the run is disclosed, never
  edited into a pass.
- K2: Families A-E run against the frozen predictions of section 4 with NO
  per-family source change; family C resolves with recursive edge
  re-pointing; family D withholds with explicit ambiguity; v1 regression
  families hold 6/6, 6/6, 4/4. All runs 3/3 byte-identical. Verdict mapping:
  all five families as predicted -> L3C-V2-PASS; family C resolves but any
  other family misses its frozen prediction, or C resolves via a
  non-recursive path -> L3C-V2-PARTIAL (reported honestly with the exact
  miss); C fails to resolve, any silent misresolution occurs, or any
  per-family source change is required -> L3C-V2-FAIL.
- K3: pure Zag at every step (implementation, build, runs, audit, byte
  checks); zero Python; no em dashes or en dashes (shell-only
  check_no_dash.sh on every committed document); anti-widening audit
  (section 7) committed with its output; the prohibited paper untouched
  (verified empty diff).

## 7. Anti-widening bar and audit plan

The mechanism must be generic construction machinery. Frozen prohibitions:
- No branch on signature literals 501-505 (or 67/131/327) outside fn main.
  The observation scripts in main MUST reference sigs; the protocol
  functions (observe, disc2, try_construct_root, try_refine, build_chain,
  interp, trace_edge, history append) must not.
- No dedicated semantic case per family: the ONLY per-family-varying inputs
  to construction are the discovered predicate atoms (data-driven) and the
  contradiction edge (walk-derived). op_label_edge is called only from
  build_chain with variable atom arguments.
- audit_v2.sh (shell + grep, committed with output) checks: A1 sig literals
  501-505 appear only inside fn main; A2 op_label_edge has one definition
  and call sites only in build_chain with variable args; A3 interp has one
  edge-following path with recursive DISP targets and no domain literals;
  A4 every set32 to node/edge state sits in an op_* fn or build_chain (which
  only calls op_*); A5 no identifiers naming families (fam_a, conj_fix,
  thresh_fix, nested_fix, etc.).
- The v1 emergence claim stays retired regardless of v2's outcome; v2 makes
  no L3 claim and no Criterion-0 claim. Honest ceiling: bounded L2
  mechanism with a constructed (not supplied) dispatch form on the frozen
  families. C0-A would additionally require the discriminator's predicate
  vocabulary and the construction protocol's search order to be
  learner-authored; they are researcher-authored here and disclosed as such.

## 8. Ablation (supplementary, not a kill bar)

Mode 0 (construction disabled: observe-only, no try_construct_root /
try_refine): the clash families must fail their evals while the pre-clash
observations still match. This mirrors v1's ablation and attributes the
resolution to the construction machinery. Recorded in the result doc.
