# PREREG: Cross-Domain Grammar to Construction with L2 Adaptation and Learner-Created Intermediate (XDOMAIN-GRAMMAR-L2M)

Status: PREREG-FROZEN 2026-10-02, before implementation. Any change
requires a new prereg; this document is never edited after freezing.
Commit-order self-check: this prereg is committed BEFORE any
implementation file exists.

Worker: Cross-Domain Grammar-Construction Worker (subagent, 2026-10-02).

## 1. Question under test

Micah directive 2026-10-02 #4: cross-domain composition moves from
exact black-box reuse toward adaptive heterogeneous composition, with
grammar to program called out as requiring a NEW INTERMEDIATE.

Prior state:
- L1 grammar to construction (prereg b6993f039, results 141db015a):
  H1/H2 solved with unmodified mechanism logic, X(rule)=divisor
  consumed DIRECTLY by Y(divisor)=first valid word. Exact reuse only.
- xdomain_l2 (prereg 418db9bd4, results 2108d5d45): H1/H2 with the
  generic REBIND operator solved arithmetic to planning under relation
  shift, 7/7 each. L2 form tested: RELATION REBINDING.
- composition_l3 FORAGE (915c03b2b) plus adversarial RELAY
  (89fa2a665): a learner-constructed reduction program from a generic
  op basis served as a novel intermediate, persisted, reused, revised.

This experiment combines all three on a NEW pair shape: grammar to
construction where (a) X must be L2-rebound to a new grammar relation
in the sealed world, and (b) Y CANNOT construct from X's output as
taught: Y was taught only as a MEMORIZED lookup (divisor to example
word) plus no generative method. A GENERATOR INTERMEDIATE M must exist
for construction to work. The critical test: does the LEARNER create M
from generic machinery and experience (L3 evidence), or must the
RESEARCHER supply M (L2, not L3)?

## 2. World design (frozen)

Training facts (fact store only):
- Grammar divisor facts: (1,71,16), (2,71,8). Rule r licenses divisor D.
- Range-hi distractor facts: (1,72,7), (2,72,5).

Y memorized construction table (NOT facts; separate driver table, so
fact subjects stay {1,2,3,4,5} and the kind probe is uncorrupted):
- (16,17), (8,9). Y as taught returns the memorized word or -1.

Sealed facts:
- (3,74,5): distractor relation, inserted FIRST (candidate scan meets
  the distractor before the genuine relation; discrimination, not luck).
- (3,73,24): genuine: rule 3 licenses divisor 24.
- (3,72,9): hi fact for rule 3 (D1 distractor reads 9 here).
- Z2: (4,73,32): rule 4 licenses divisor 32.
- Z3: (5,73,40): rule 5 licenses divisor 40.

Validity rules (WORLD/DRIVER ONLY; the learner constructor never sees
them; the driver self-checks every label triple against them at
startup and aborts on LABEL-MISMATCH):
- G1: word v valid under divisor D iff exists q,r in [1,7] with
  v = D*q + r.
- G2 (revision regime): v valid under D iff exists q,r in [2,8] with
  v = D*q + r.

Labeled word-validity experience (driver-generated literals, the only
thing the constructor may read):
- G1 labels, D in {16,8}: valid {D+1, D+2, D+7, 2D+1, 2D+7};
  invalid {D, D+8, D-1, 2D+8, 1, 0}. 22 triples.
- G2 labels, D in {16,8}: valid {2D+2, 2D+8, 3D+2, 3D+8};
  invalid {D+1, D+2, D+8, 2D+1, D}. 18 triples.

Sealed goals (expected-answer verification, same honest boundary as all
H1/H2 waves):
- Z: (3,93) -> 25. Needs X rebound to 73 (X=24), then M(24)=25.
- Z2: (4,93) -> 33. M(32)=33 via persisted composite/M.
- Z3: (5,93) -> 82. After G2 revision, M(40)=82.

## 3. Learned structures (prior learning, behavior induction not under test)

H1 MAPs (48-byte entries, as in xdomain_l2):
- X (behav 0): X(rule) = find_obj(rule, param). param bindable,
  training-bound to 71 via generic bind_param (first relation seen for
  the training subject). Learned sig NODE->NUM.
- Y (behav 1): Y(D) = M(D) if the generator intermediate M is installed
  in learner state, else Y-lookup(D) = memorized word or -1. Learned sig
  NUM->NUM from lookup teaching (16->17, 8->9).
- D1 (behav 2): find_obj(rule, 72); fixed relation (param negative =
  not rebindable). Learned sig NODE->NUM. Distractor: type-compatible,
  wrong value (D1(3)=9, M(9)=10).
- D2 (behav 3): identity. Learned sig NODE->NODE. Distractor.
- Composite behav 4: (comp_a, comp_b), generic contract composition.

H2 modes (capability-gated executors, as in gc_h2.zag):
- 1=GRAMMAR: divisor via bound relation gram_rel (rebindable).
- 2=CONSTRUCT: Y as above (M if installed, else lookup).
- 3=HIRANGE: distractor via fixed relation 72.

## 4. The intermediate M (frozen generic machinery, disclosed)

M is a generator program over a frozen generic op basis, stored in a
dedicated learner-state slot (M base; Mprev holds revision history):
- Registers R0..R3 (i32). R0 preloaded with D. Output is R0.
- Ops: 0=CPY (Rd=Rs), 1=ADD (Rd+=Rs), 2=MUL (Rd*=Rs), 3=SET1 (Rd=1),
  4=INC (Rd+=1). Instruction = (op,d,s), 3 bytes, max 6 instructions.
- m_construct: greedy search from a given init program (empty for fresh
  construction, current M for revision). Each round evaluates every
  (op,d,s) append (5*4*4=80 candidates); score = number of training
  divisors whose emitted word carries label 1 in the label table
  (table miss counts 0); applies the single append with the largest
  strictly positive gain; ties broken by candidate order
  (op 0..4, d 0..3, s 0..3, first-max). Stops at perfect score or no
  positive gain or 6 instructions. Trace lines C-ROUND are printed.
- m_adapt (revision policy, no threshold here): score current M on new
  labels; if perfect keep (code 0); else extend from current M; if the
  extension reaches perfect, retire old M to Mprev (superseded=1) and
  adopt (code 2); else HONESTFAIL (code 3).
- The op basis and greedy search are researcher-authored GENERIC
  machinery (same footprint class as FORAGE). The L3 question is
  whether the intermediate's final program form is constructed by the
  learner from experience rather than supplied by the researcher.

Frozen hand-derived expectations (the implementation must reproduce
them; deviation is a falsifier, not a tuning opportunity):
- G1 fresh construction from empty: baseline score 0 (w=D, label 0).
  Round 1: all 64 op-0..3 candidates score 0; (4,0,0)=INC R0 is the
  first positive-gain candidate with gain 2 (w=D+1: labels 1,1).
  M = [INC R0], program bytes (4,0,0), score 2/2, stop.
- G2 adapt from [INC R0]: base score 0 (w=D+1 labeled 0,0 under G2).
  Extension round: (1,0,0)=ADD R0,R0 is the first positive-gain
  candidate with gain 2 (w=2D+2: labels 1,1). M' = [INC R0, ADD R0,R0],
  program bytes (4,0,0,1,0,0), score 2/2, adapt code 2, Mprev holds
  [INC R0] with superseded=1.

## 5. L2 solver (generic, not domain-specific)

REBIND operator (as in xdomain_l2): copy a MAP with non-negative param,
set param to the candidate relation, inherit the learned signature,
record rebound_of provenance. Candidate relations: distinct r with a
fact (s,r,*) for the query subject s, first-seen order; generic scan.

Two-phase solver per goal:
- Phase 1: exact L1 reuse (typed singles then pairs for H1; ordered
  mode pairs for H2). MUST FAIL (proves adaptation necessary).
- Phase 2 (l2_on=1): (a) if M absent and the arm allows building,
  run m_construct on the G1 labels; (b) scan candidate relations;
  (c) rebind each rebindable MAP to each candidate; (d) retry typed
  composition (H1) / ordered mode pairs (H2) with rebound structures.
  First verifying composition is promoted with full provenance.

H1 predicted TREAT Z trace: Phase 1: 2 singles tried (X r=-1; D1 r=9)
+ 4 pairs tried ((X,Y): -1->-1; (D1,Y): 9->10; (D2,X): 3->-1;
(D2,D1): 3->9); L1-FAIL. Phase 2: M constructed [INC R0];
candidates {74,73,72}; X rebound to 74: (X74,Y): 5->6 rejected;
X rebound to 73: (X73,Y): 24->25 PROMOTED. Total tries 10.
H2 predicted TREAT Z trace: L1: all 9 ordered pairs fail. L2: M built;
rel=74: (1,2): 5->6 rejected, (3,2): 9->10 rejected; rel=73:
(1,2): 24->25 VC-COMPOSE ok m1=1 m2=2 rel=73.

## 6. Frozen arms (per mechanism)

- TREAT-L2: teach; sealed facts; l2_on=1, allow_build=1. Solve Z, then
  Z2 in the SAME workspace (M must persist; build_count must stay 1).
  Expect Z PASS with rebound provenance and M created; Z2 PASS via the
  persisted composite.
- L1-ONLY: l2_on=0. Expect FAIL (Z unsolved).
- ABL-X: delete X (H1) / behav 0 (H2); l2_on=1. Expect FAIL.
- ABL-Y: delete Y (H1) / behav 1 (H2); l2_on=1. Expect FAIL.
- FRESH: facts only, no teaching; l2_on=1. Expect FAIL.
- NO-M: teach; l2_on=1, allow_build=0 (M stays absent; Y falls back to
  memorized lookup). Expect FAIL. This is the causal-necessity arm for
  the intermediate: Y as taught cannot construct for a new divisor.
- SUPPLIED: teach; l2_on=1; driver installs M=[INC R0] as
  researcher-supplied (supplied=1, NO construction trace). Expect PASS.
  Diagnostic only: if TREAT fails but SUPPLIED passes, the blocker is
  the creation step (L2 verdict), not task solvability.
- REVISE: teach; build M on G1; sanity-solve Z; G2 labels arrive;
  m_adapt; solve Z3. Expect adapt code 2, Mprev=[INC R0] superseded=1,
  Z3 PASS.

## 7. Kill bars (all must hold for the L3 verdict)

- K1 H1-SOLVE: TREAT Z ARM-RESULT PASS; composite comp_a has
  rebound_of=X and param=73; m_created=1; program bytes printed are
  (4,0,0).
- K2 H2-SOLVE: TREAT Z VC-COMPOSE ok m1=1 m2=2 rel=73; m_created=1.
- K3 L1-NECESSARY: L1-ONLY fails for both H1 and H2.
- K4 CAUSAL: ABL-X, ABL-Y, FRESH fail for both (with l2_on=1).
- K5 M-NECESSARY: NO-M fails for both.
- K6 M-CREATED: (a) the run trace shows at least one C-ROUND with
  gain>0, final program non-empty, score 2/2 on the G1 labels;
  (b) frozen grep audit on glm_learner.zag returns zero matches for
  every pattern in section 8; (c) the TREAT run output contains no
  SUPPLIED-INSTALL line (the supplied installer is never invoked on
  the TREAT path).
- K7 REUSE: Z2 PASS for both; m_build_count==1 after Z and Z2
  (M persisted, not rebuilt).
- K8 REVISE: adapt returns code 2 for both; Mprev holds program
  (4,0,0) with superseded=1; current M program is (4,0,0,1,0,0);
  Z3 PASS for both.
- K9 REBIND-DISCOVERED: grep audit: every source line containing 73
  or 74 also contains add_fact (world setup only); the scan, rebind,
  composer, and constructor logic contain no 73/74 literals.
- K10 DETERMINISM: 3/3 runs byte-identical per binary (sha256 recorded).
- K11 NO-TEMPLATE: grep finds no GRAMMAR_TO_CONSTRUCTION, no
  CHAIN_COUNT, and no per-MAP signature literals in composer code.
- K12 TOOLCHAIN: safebin active, `which python3 python` empty, pure
  Zag, no forbidden executable invoked.

## 8. Frozen K6/K9 grep audit spec

On glm_learner.zag, each pattern must return zero matches (grep -c 0):
1. `(^|[^0-9])(71|72|73|74|81)([^0-9]|$)` (no fact-relation or table
   literals in the generic machinery)
2. `SUPPLIED` (the supplied installer lives in driver files only)
3. `q *\* *r|r *\* *q` (no validity-rule shape in the machinery)

K9: `grep -n "73" *.zag | grep -v "add_fact"` empty; same for "74".
Comments are kept free of 73/74 outside add_fact lines.

## 9. Verdict rule

- K1-K12 all PASS: XDOMAIN-GRAMMAR-L2M-COMPLETE with L3 classification:
  the learner created the intermediate M from generic machinery and
  labeled experience (creation trace, persistence, reuse, revision,
  adversarial-origin audit clean).
- K1 or K2 FAIL but SUPPLIED PASS: XDOMAIN-GRAMMAR-L2M-COMPLETE with
  L2 classification: the intermediate must be researcher-supplied;
  the learner does not create it. This is the critical negative.
- Any other bar failure: verdict FAIL, failing bar named.

## 10. Honest boundaries (declared in advance)

- Behavior implementations (grammar extract, memorized lookup, hi
  extract, identity) are researcher-authored prior learned structures.
  Under test is composition plus intermediate origin, not induction.
- The REBIND operator and the m_construct/m_adapt machinery are
  generic researcher-authored machinery. The binding decisions (which
  MAP, which relation) and the intermediate's program form are
  learner-determined from the sealed world and labeled experience.
- Expected answers used for verification (same as all H1/H2 waves).
- Binary NODE/NUM kinds from the syntactic probe (same as H1).
- One L2 form (relation rebinding) composed with one intermediate
  form (generator program). Extension, truncation, specialization are
  separate future experiments.
- The hidden validity rules are builder-designed, not adversary
  designed (adversarial-world generality is open future work, as with
  FORAGE before RELAY).
- This build targets the bars above; it does not claim Micah's full
  12-criterion L3 bar.

## 11. Build and determinism spec

Pure Zag. u8-backed workspace, little-endian cell helpers. Output via
one preallocated buffer and a single _zag_raw_syscall write per arm
sequence (no _zag_print for dynamic content). No RNG. Fixed orders
everywhere. 3/3 byte-identical required. 0 modes/bridges/handlers.
No em/en dashes in loop documentation. Paper untouched. Nothing
pushed. Commits local on tnn-native-lab with EXPLICIT pathspecs.
