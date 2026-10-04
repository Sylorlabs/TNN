# C0 Integration Design: OP-RECRUIT v2 + Q4 Discovery

Date: 2026-09-30. Worker: C0 Integration Designer.
Status: DESIGN ONLY. No implementation. No Python used at any stage.
Zero em/en-dash bytes in this file (shell byte-verified before commit).

## 1. Mission and grounding

The C0 status matrix (`5891940d6`) finds the Q4 explanatory-variable
line closest to full Criterion 0 (C0-C PASS, C0-D PASS on F-PARCOND;
C0-A/C0-B PARTIAL) and identifies the blockers in order:

1. C0-A: the beam-search discovery driver is researcher-authored.
2. C0-B: the operator alphabet is closed (31 ops in implementation;
   {AND, OR, NOT, XOR} in the frozen design plus terminals).
3. C0-C: single adversary data point.
4. Promotion pipeline incomplete.

The matrix's second-closest finding: OP-RECRUIT v1 proved the C0-A
substrate on the GENEXEC2 VM (recruited opcode semantics in
learner-created bytes, one generic dispatch case, `efa618c3a`), and
OP-RECRUIT v2 (`c6ef7ffcf`) specifies learner-driven recruitment
(DETECT -> PROPOSE -> VALIDATE -> RECRUIT -> RETIRE) as a learner
cognitive action. The recommended combination: "v2-recruited operators
+ Q4 discovery" is the strongest candidate architecture for a full-C0
attempt.

This document designs that integration: the Q4 discovery beam composes
v2-recruited operators, not only the fixed alphabet; the learner
recruits operators from its own promoted explanatory variables, then
discovers new structure using the grown menu.

Q4 evidence referenced (all commits verified present via git log):

- `b719bb54b` Q4 reuse redesign (BUILD-PASS, C0-D reuse ratio 0.0)
- `ad4284269` adversary-test prereg, `5f56cc491` F-PARCOND result
  (BUILD-PASS; 7 ops, 64/64 true accuracy, margin 0.375, 3860 growth
  events)
- `121b6d5aa` reproduction (REPRODUCED, promotion step 4)
- `757442c40` baseline comparison (BASELINE-COMPARED, step 5; reuse
  beats memorization 64/64 vs 56/64)
- `98ece92e4` baseline prereg

v2 evidence referenced:

- `c6ef7ffcf` OP-RECRUIT v2 design (DETECT/PROPOSE/VALIDATE/RECRUIT/
  RETIRE, one generic dispatch case for opcodes 32..63, six falsifiers,
  test battery R-V1/T-NOFIRE/T-SELF/T-ARITY2/T-RETIRE/T-ADV)
- `efa618c3a` v1 (C0-A substrate proof, SANITY 17/17)

## 2. What each side contributes

Q4 contributes the adversary-tested discovery loop: sealed worlds,
passive confounded samples plus adaptive interventions, beam growth
with complexity penalty (lambda 0.02 per operator node), keep margin
+0.15, simplicity epsilon 0.02, persistent kept variables, a
construction trace (one event per operator addition), and Phase 2
reuse where the kept variable becomes an atomic terminal. Its proven
strengths are C0-C (first adversary data point) and C0-D (reuse ratio
0.0, beats memorization on composition-generality).

v2 contributes the recruitment loop: persistent tables
(nrec, rec_idx, rec_arity, rec_len, rec_buf, rec_buf_top, rec_use,
rec_idle, staging buffers), one generic interpreter case for opcodes
32..63, and the learner-executed pipeline: DETECT (subsequence
frequency plus MDL-style compression gain), PROPOSE (arity by generic
simulation), VALIDATE (behavioral equivalence on learner-generated
test inputs from its experience buffer), RECRUIT (install, rewrite the
program store, log RECRUITED), RETIRE (usage-decay removal with
byte-exact re-expansion). Its proven substrate claim is C0-A: opcode
meaning as learner-created data, never a source case.

The integration point is the Q4 beam's expansion menu. Today the beam
expands candidates with base operators only. In the integrated system
the menu is the union of the base alphabet and every opcode the
learner has recruited, and the menu grows at runtime as the learner
recruits. The beam remains the construction driver; what it composes
is increasingly learner-authored.

## 3. Integration architecture

### 3.1 Shared persistent state

Q4's kept explanatory variables (D1, D2, ...) already live in
persistent learner state with their expression trees, growth traces,
and evidence. v2's recruitment tables are added to the same persistent
state. One state, two cooperating loops, one save/load image. The
recruited-opcode tables must survive save/load byte-identically, as
v2 specifies.

### 3.2 Beam menu extension

The beam's candidate-expansion step gains one new expansion class:

- Base expansion: apply a base operator to beam candidates (unchanged).
- Recruited expansion: for each recruited opcode ri (0 <= ri < nrec),
  create a node with rec_arity[ri] children drawn from the beam's
  current candidate pool (terminals and subexpressions), exactly as a
  base N-ary operator would compose.

Evaluation of a recruited-opcode node routes through v2's generic
pop/bind/push wrapper: bind the child values as in0..in(a-1), execute
the body bytes from rec_buf on a fresh stack, take the result. The Q4
tree evaluator gets one generic dispatch point for opcodes 32..63,
mirroring v2's single interpreter case. No per-meaning source case is
added to the evaluator. This is the mechanical heart of the
integration: the beam can compose meanings the source never names.

Scoring treats a recruited-opcode node as 1 operator node for the
complexity penalty and the 7-node keep bound. That is the entire
point of recruitment: a 5-op fragment becomes a 1-node choice.

### 3.3 DETECT over tree fragments (adaptation of v2 section 3.1)

v2's DETECT counts instruction subsequences in promoted programs.
Q4's promoted objects are expression trees, so DETECT is adapted to
subtree frequency: for each kept variable's tree and each growth-trace
fragment, count distinct subtree shapes (up to variable renaming of
terminals), 2..6 nodes. gain(S) = (nodes(S) - 1) * freq[S] -
COST_INSTALL, candidates require freq >= K_FREQ and gain > 0. The
MDL-style compression logic is unchanged; only the fragment unit
moves from instruction subsequence to tree fragment. Staging,
PROPOSE (arity = number of distinct free terminals in the fragment,
capped at 4), and VALIDATE proceed as v2 specifies.

### 3.4 Ordering: the three phases

- Phase 1 (discover, base menu): Q4 as today on family X. Keeps D1.
  The menu is the base alphabet only; no recruitment has fired yet.
- Consolidation (recruit): the learner's consolidation routine runs
  v2's DETECT/PROPOSE/VALIDATE/RECRUIT over the kept-variable store
  (trees plus growth-trace fragments). RECRUITED events are logged;
  the program store is rewritten (F-BREAK gate: re-execute every
  rewritten kept variable on its validation inputs, require exact
  match). The beam menu now includes the recruited opcodes.
- Phase 2 (reuse, unchanged): kept D1 becomes an atomic terminal for
  the reuse pairing, as in `b719bb54b`.
- Phase 3 (discover, grown menu): Q4 on a new family Y whose true
  cause is expressible with recruited fragments. The beam expands
  with the grown menu. Measurement: interventions to criterion and
  candidate evaluations versus the frozen no-recruitment control
  (same family Y, base menu only).

Recruitment may also fire between Phase 3 tasks, so the menu can
grow across families. Retirement (v2 section 3.5) applies across the
same store: an opcode unused for W_IDLE episodes is re-expanded
byte-exactly and removed.

### 3.5 Information barrier (hard requirement)

v2's VALIDATE generates test inputs from the learner's experience
buffer. In the Q4 context the experience buffer contains only
learner-observed (input, outcome) pairs: the 8 passive samples and
the outcomes of the learner's own interventions. It must never
contain the harness's exhaustive truth table. The implementer must
demonstrate the barrier: validation inputs are drawn from observed
samples only; the sealed function is queried by the harness for
scoring, never by the learner outside its intervention budget. A
violation of this barrier invalidates any C0 claim from the
integrated system, because the recruited operator would be fit to
unearned data.

## 4. Worked example

Phase 1 on the majority family: the beam keeps D1 =
(X1 AND X2) OR (X2 AND X3) OR (X1 AND X3), 5 operator nodes, the real
kept variable from `b719bb54b`. Its growth trace contains the three
pairwise-AND fragments repeatedly.

Consolidation: DETECT counts the 5-node majority shape at freq high
enough that gain > 0 (the exact numbers depend on how many kept
variables share it; the design requires the frozen K_FREQ and
COST_INSTALL to be met, not hand-waved). PROPOSE simulates the body:
3 distinct free terminals, arity 3. VALIDATE draws N_VAL inputs from
the observed samples; inline vs wrapped agree exactly. The learner
executes RECRUIT: opcode 32 installed, store rewritten, RECRUITED(32,
3, 5, gain) logged. The beam menu now contains MAJ3 as a 1-node
choice.

Phase 3 on a new family whose true cause is
D2 = MAJ3(Xa, Xb, Xc) XOR Xd: the beam discovers it as
XOR(op32(Xa, Xb, Xc), Xd), 2 operator nodes, from passive evidence
alone. The no-recruitment control must assemble the 5-node majority
inline (6 nodes total) and is predicted to need more interventions.
This single run would demonstrate, in one trace: the menu grew at
runtime (C0-B direction), the grown entry was learner-recruited
(C0-A direction), and the later discovery was cheaper because of it
(C0-D direction).

## 5. C0-A audit criteria (K2)

The integrated system strengthens C0-A relative to current Q4 iff
all of the following hold; any failure keeps C0-A at PARTIAL:

- A1 (no dedicated cases): source grep shows opcode literals 32..63
  only in the one generic dispatch case of the tree evaluator and
  the one generic interpreter case. No branch names a recruited
  meaning. (F-SOURCE kills on violation.)
- A2 (learner-triggered): every recruited opcode appearing in any
  kept variable traces to a RECRUITED event logged by the learner's
  consolidation routine. No RECRUITED event may be emitted by
  driver code. Runs with zero RECRUITED events are valid outcomes
  (T-NOFIRE control); the claim is falsifiable. (F-DRIVER kills on
  violation.)
- A3 (sound rewrite): after every RECRUIT and every RETIRE, all
  kept variables produce byte-identical outputs on their validation
  inputs. (F-BREAK kills on violation.)
- A4 (disclosed residue): the beam scoring rule, keep margin,
  complexity penalty, intervention-selection policy, detection
  criterion family, and all numeric constants remain
  researcher-authored and are listed verbatim in the result file.
  The C0-A claim covers operator semantics only, never the driver.

Passing A1-A4 moves the line from "beam researcher-authored,
content in learner state" to "beam researcher-authored, content and
operator meanings in learner state". The driver is still authored;
that is disclosed, not hidden.

## 6. C0-B audit criteria (K2)

The integrated system strengthens C0-B relative to current Q4 iff
all of the following hold:

- B1 (grown menu): the beam's expansion menu at Phase 3 includes at
  least one recruited opcode that is absent from the researcher's
  base alphabet, and the growth trace of a kept variable contains
  expansion events using that opcode.
- B2 (not enumerable from source): the final operator inventory
  (base plus recruited) cannot be listed from the source alone; the
  recruited entries exist only in learner state. An auditor given
  only the source cannot predict which opcodes the beam will have.
- B3 (incremental): recruitment events are spread across episodes
  (not one bulk install); nrec grows 0 -> k over the run; each
  RECRUITED event cites the experience (which kept variables, which
  fragment frequencies) that triggered it.
- B4 (disclosed residue): the base alphabet {AND, OR, NOT, XOR} and
  terminals remain researcher-authored. The claim is "open, growing
  menu", not "invented primitives". The primitive alphabet is still
  supplied.

Passing B1-B4 converts the C0-B verdict from "growth is open-ended,
the menu is not" to "growth is open-ended and the menu grows at
runtime from learner experience". The base menu stays closed; that is
the disclosed boundary.

## 7. Test battery (frozen design; implementer preregisters before build)

- I1 (substrate regression): v2's R-V1 scenario plus Q4's F-PARCOND
  regression, run through the integrated binary. Bars: RECRUITED
  fires on R-V1 with a behaviorally ABS-equivalent op; F-PARCOND
  still reaches 64/64 true accuracy with margin >= 0.15. Guards
  against integration breakage of either side.
- I2 (menu growth): Phase 1 on the majority family, consolidation,
  Phase 3 on the MAJ3-XOR family (section 4). Bars: (a) at least
  one RECRUITED event in consolidation; (b) the Phase 3 kept
  variable's growth trace contains a recruited-opcode expansion;
  (c) Phase 3 node count < control node count on the same family.
- I3 (no-fire control): v2's T-NOFIRE through the integrated
  binary. Bar: zero RECRUITED events; Phase 1 discovery unaffected
  (accuracy within the frozen tolerance of the unintegrated Q4
  result).
- I4 (reuse gain): Phase 3 interventions-to-criterion and candidate
  evaluations versus the frozen no-recruitment control on identical
  families. Bar: strictly fewer on at least one metric with the
  frozen margin; the control is the same binary with recruitment
  disabled, not a weaker learner.
- I5 (adversary): post-freeze independent adversary designs a
  family requiring a materially different recruited form (different
  arity or different composition shape than the worked example).
  Bar: RECRUITED fires and C0-D reuse is demonstrated, or the
  trace diagnoses the failure (which regularity was detected, why
  none qualified). This is the second C0-C data point for the Q4
  line and the first for the integrated architecture.

Falsifiers (any one kills the corresponding claim; none may be
weakened after the implementer's prereg):

- F-SOURCE: dedicated semantic case for a recruited meaning in
  source. Kills the C0-A strengthening.
- F-DRIVER: RECRUITED fires only in driver-prompted runs, never in
  autonomous runs. Kills the learner-authored claim.
- F-BREAK: any kept-variable output changes after rewrite or
  retirement. Kills mechanism soundness.
- F-MENU: the beam never expands a recruited opcode in any Phase 3
  run (menu grew but discovery ignores it). Kills the C0-B
  strengthening.
- F-NOGAIN: recruited ops never reduce node count, interventions,
  or candidate evaluations versus control. Kills the C0-D
  strengthening.
- F-LEAK: validation or recruitment touches the harness truth table
  outside the learner's intervention budget. Kills every claim from
  the run; the run is VOID, not merely failed.

Global controls: pure Zag (znc plus shell and git only), zero
Python at any stage including scratch, zero em/en-dash bytes,
3/3 byte-identical runs, exit 0, implementer prereg strictly before
implementation (verified by merge-base), pathspec commits on owned
paths only, nothing pushed.

## 8. Honest scope and ceiling

Even with I1-I5 all passing and no falsifier firing, the integrated
system is stronger bounded L2 structural, not L3:

- The detection criterion family (subtree frequency plus
  compression gain) is researcher-designed; the learner computes it
  but did not invent it.
- The beam driver (scoring, keep/discard, intervention selection)
  is researcher-authored.
- The base operator alphabet and terminals are researcher-supplied.
- Thresholds (K_FREQ, COST_INSTALL, N_VAL, W_IDLE, lambda, margins,
  beam width, node bound) are frozen researcher constants.
- C0-C would have two data points (F-PARCOND plus I5), still short
  of "multiple unforeseen forms" as a habit, and the promotion
  pipeline (alternative-explanation attack, OOD, ablation,
  transfer, red team, governance audit) must run on the integrated
  result before any SURVIVES discussion.

What the integration genuinely buys: the two hardest blockers move
together. v2 alone has learner-authored semantics but no
adversary-tested discovery; Q4 alone has adversary-tested discovery
but authored semantics and a closed menu. Combined, one run can
show recruited meaning (C0-A direction), a grown menu (C0-B
direction), an adversary family (C0-C direction), and cheaper later
discovery (C0-D direction). No other current line can put all four
directions in one trace.

The L3 direction this enables but does not reach: a learner that
invents its own recruitment criteria (not just computes a supplied
one) and its own primitives (not just composes supplied ones).

## 9. Feasibility assessment (K3)

Feasible, with three bounded risks:

1. Substrate compatibility (low risk): v1 already demonstrated the
   recruited-opcode execution substrate on the GENEXEC2 VM family.
   The Q4 tree evaluator needs the one generic dispatch point; the
   pop/bind/push wrapper is meaning-agnostic and arity-generic
   (1..4). This is bounded engineering, not research.
2. DETECT adaptation (medium risk): v2's DETECT counts instruction
   subsequences; Q4 needs subtree-frequency counting with terminal
   renaming. The compression-gain arithmetic is identical, but the
   fragment enumeration over trees with a 7-node bound must be
   implemented and tested before any C0 claim. Prototype risk is
   over-counting (overlapping subtrees inflating freq); the design
   requires counting once per distinct kept variable, mirroring
   v2's once-per-program rule.
3. Validation barrier (medium risk): the experience-buffer-only
   rule (section 3.5) must be enforced in code and audited. The
   failure mode is subtle: any path by which the sealed function
   leaks into validation (for example, reusing harness-side
   scoring helpers inside the learner) voids the run under F-LEAK.
   The implementer should add a compile-time separation (learner
   code links only the observed-sample buffer, never the sealed
   function) rather than relying on discipline.

Dependencies: v2 must be built first (it is design-only at
`c6ef7ffcf`; an implementer is already assigned). The Q4-side
adapter (tree-fragment DETECT, menu extension, barrier) is
estimated as the smaller half of the work because Q4's beam,
scoring, and Phase 2 reuse are already built and tested.

Recommended build order:

1. v2 implementation through its own battery (R-V1, T-NOFIRE,
   T-SELF first; T-ARITY2, T-RETIRE, T-ADV after).
2. Integration Phase A: menu extension plus dispatch point; I1
   regression and I3 no-fire control. F-BREAK and F-LEAK as hard
   gates before any gain is measured.
3. Integration Phase B: consolidation plus Phase 3; I2 and I4.
4. I5 adversary world, then the full promotion pipeline on the
   integrated result (alternative-explanation attack, OOD,
   ablation, transfer, independent red team, governance audit)
   before any SURVIVES discussion.

Estimated ceiling if everything passes: the closest any TNN line
has come to a four-cell C0 claim, with C0-A and C0-B strengthened
from PARTIAL toward PASS under the audit criteria of sections 5
and 6, C0-C at two data points, C0-D demonstrated through
recruitment-mediated reuse. Still bounded L2 by the honest-scope
section; the L3 bar (learner-invented criteria and primitives)
remains unreached.

## 10. Kill-bar self-check

- K1 (integration specified): sections 3.1-3.4 specify shared
  state, menu extension, tree-fragment DETECT adaptation,
  three-phase ordering, and retirement interaction at buildable
  precision; section 4 gives the worked MAJ3 example with
  predicted node counts.
- K2 (C0-A/B audit criteria defined): section 5 defines A1-A4
  (source grep, learner-triggered trace, sound rewrite, disclosed
  residue); section 6 defines B1-B4 (grown menu, non-enumerability,
  incrementality, disclosed residue). Both name the exact checks
  and the falsifiers that kill on violation.
- K3 (feasibility assessed): section 9 rates three bounded risks,
  states dependencies (v2 built first), gives the build order,
  and names the honest ceiling.

## Verdict: DESIGN-COMPLETE
