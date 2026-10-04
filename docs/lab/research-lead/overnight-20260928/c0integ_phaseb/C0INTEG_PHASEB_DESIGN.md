# C0INTEG Phase B Design: Grown-Menu Reuse Benefit

Date: 2026-09-30. Worker: C0INTEG Phase B Designer.
Status: DESIGN ONLY. No implementation. No prereg frozen by this document.
Zero Python used at any stage. This file is byte-verified free of em/en dashes.

## 1. Mission and grounding

Phase A (`c3d8aaf90`, PHASEA-PASS) integrated OP-RECRUIT v2 with Q4
discovery into one continuing learner: one generic dispatch for
recruited opcodes 32..63, tree-fragment bodies with placeholders,
DETECT/PROPOSE/VALIDATE/RECRUIT/RETIRE as the learner's consolidation
routine, and a beam menu that grows at runtime. T-RV1 recruited
op 32 with body OR(AND(P0,P1),AND(P0,P2)), arity 3, 7 body nodes,
gain 5, freq 4. T-MENU verified 512/512 recruited expansions against
body semantics. The honest ceiling is bounded L2 infrastructure:
Phase A demonstrates the substrate, not the benefit.

Phase B measures the benefit. Criterion 0-D requires that the
invented structure improve later cognition (transfer, prediction,
procedure learning, sample efficiency); existence alone is
insufficient. The integration design (`9aa1fb0b5`, sections 3.4 and
7) freezes Phase B as tests I2 (menu growth), I4 (reuse gain), and
I5 (independent adversary), with falsifiers F-MENU and F-NOGAIN
frozen in the Phase A prereg (`c4a7e325f`, section 5) and evaluated
here. This document designs I2, I4, and I5 at buildable precision.
The Phase B implementer preregisters before building; nothing here
is frozen until that prereg is committed.

Researcher-authored residue carried forward unchanged from Phase A:
base ops {AND, OR, NOT, XOR} with hand-written truth tables,
K_FREQ=3, COST_INSTALL=3, N_VAL=16, W_IDLE=3, MIN_FRAG_OPS=2,
MAX_FRAG_OPS=6, MAX_ARITY=4, MAX_REC=32, beam width 32, node bound 7,
complexity penalty 200 per operator node, keep margin 0.15,
simplicity epsilon 0.02. The beam driver, scoring, and
intervention-selection policy remain researcher-authored. The claim
is bounded-L2 reuse, never L3.

## 2. Worked example

Phase 1 (base menu only) runs discovery on three episodes of family
X, one kept variable per episode:

- X1: D = OR(AND(X1,X2),AND(X1,X3))
- X2: D = OR(AND(X4,X5),AND(X4,X6))
- X3: D = OR(AND(X2,X4),AND(X2,X6))

Each is a 3-operator factored OR under distinct terminal bindings.
Discovery uses the Q4 standard budget: 8 passive samples plus up to
24 adaptive interventions per episode, keep margin 0.15, node
bound 7.

Consolidation runs DETECT over the three kept trees. The fragment
OR(AND(P0,P1),AND(P0,P2)) canonicalizes identically in all three
trees and is counted once per kept tree (the Phase A over-counting
guard), so freq = 3, ops = 3, gain = (3-1)*3 - 3 = 3 > 0.
PROPOSE: arity 3. VALIDATE: INLINE == WRAPPED on all N_VAL = 16
observed tuples. RECRUIT installs op 32; the kept trees are
rewritten to op32(Xa,Xb,Xc) (1 operator node each); F-BREAK
requires byte-identical outputs on validation inputs.

Phase 3 (grown menu) runs discovery on family Y, fresh episodes:

- Y-std: D' = XOR(OR(AND(Xa,Xb),AND(Xa,Xc)),Xd), with
  (Xa,Xb,Xc,Xd) a fresh variable binding disjoint from the X
  triples, e.g. (X3,X5,X6,X1).
- Y-hard: D'' = AND(OR(AND(X1,X2),AND(X1,X3)),
  OR(AND(X4,X5),AND(X4,X6))), the fragment used twice.

Predicted kept forms:

- Y-std grown: XOR(op32(Xa,Xb,Xc),Xd) = 2 operator nodes.
  Y-std control (recruitment disabled): 4 operator nodes.
  Predicted node-count gain: 2.
- Y-hard grown: AND(op32(X1,X2,X3),op32(X4,X5,X6)) = 3 nodes.
  Y-hard control: 7 nodes (at the bound). Predicted capability
  gap: the control may fail the keep margin or the budget.

These are predictions, not results. If the beam never expands
op 32, F-MENU fires and the honest verdict is recorded.

## 3. Protocol

### 3.1 Arms

- A-GROWN: Phase 1 (3 episodes of family X, base menu) then
  consolidate (in-run; fresh persistent state per seed) then
  Phase 3 (1 episode of Y-std and 1 episode of Y-hard, grown
  menu). The only cross-phase state is the recruited-opcode
  table; Phase 3 starts with an empty beam.
- A-CTRL: Phase 3 only (1 episode of Y-std and 1 of Y-hard),
  same binary with recruitment disabled (nrec forced 0, no
  consolidate), same seeds, same episodes as A-GROWN. This is
  the identical learner minus the grown menu, not a weaker
  learner.
- A-ABLATE (M5, 2 seeds only): Phase 1 then consolidate then
  force-retire op 32 (idle counter forced past W_IDLE, F-BREAK
  gate on retire) then Phase 3 Y-std. Isolates the gain to the
  recruited opcode rather than consolidation side effects.

Phase 2 kept-variable-as-terminal reuse is orthogonal
infrastructure, already proven on the Q4 line, and is not
re-tested here.

### 3.2 Seeds and determinism

Five fresh seeds S1..S5, suggested S_i = 90011 + (i-1)*977
(90011, 90988, 91965, 92942, 93919). The Phase B prereg must
prove them disjoint from all previously committed seed sets:
tainted {11,22,33,44,55}, {123456789, 555555555, 770404483},
R4's 12 seeds, R1's {81113, 82090, 83067, 84044, 85021}.
Each seed starts from fresh persistent state. Three runs per
seed per arm, byte-identical stdout required (3/3).

### 3.3 Budgets

Per episode: 8 passive samples plus up to 24 adaptive
interventions (Q4 standard). Node bound 7, beam width 32,
penalty 200 per operator node, keep margin 0.15. Coverage
logging is informational per the F-RECFOLD precedent: the
harness logs distinct input combos observed in the 32
Phase-3 observations.

### 3.4 Measurement definitions (prereg binds these to code)

- Interventions-to-criterion: harness-side log of per-round
  beam-top true accuracy (never visible to the learner); first
  round with 64/64, capped at 25 if never reached.
- Candidate evaluations: count of candidate expression
  evaluations performed by beam_extend during the Phase 3
  episode. The prereg must name the exact counter.
- Kept opc: operator nodes in the kept tree, recruited-op
  node counting as 1 (Phase A section 3.3).
- Tax-off diagnostic: per the Q4 R1 precedent, log
  TAXOFF_UNIQ per episode (informational; ties flag
  harness/beam defects but do not change verdicts).

## 4. Metrics

- M1 node count (Y-std): grown kept opc <= control kept opc - 1.
  Bar met on a seed iff the inequality holds and both arms
  reach 64/64 true accuracy.
- M2 interventions (Y-std): grown interventions-to-criterion
  <= control - 2.
- M3 evaluations (Y-std): grown candidate evaluations
  <= 0.8 * control evaluations.
- M4 structural audit: on every seed counted toward M1/M2/M3,
  the grown kept tree contains at least one node with opcode
  >= 32, and that opcode was recruited during this seed's
  consolidation (opcode index < nrec at Phase 3 start and a
  RECRUITED event for it exists in this seed's log). A seed
  meeting a metric bar without in-run recruited-op usage does
  not count toward that bar and is flagged.
- M5 ablation (2 seeds, Y-std): A-ABLATE interventions within
  +-1 of A-CTRL and A-ABLATE opc equal to A-CTRL opc.
- M6 capability (Y-hard): grown reaches true 64/64 within the
  24-intervention budget. Bar: grown succeeds on >= 4/5 seeds.
  Control success rate is reported alongside. A capability
  EXPANSION claim additionally requires grown minus control
  >= 2 seeds; otherwise capability is reported as "not
  demonstrated", which does not fail Phase B.

Metric bars M1/M2/M3 are evaluated per seed; each bar is met
iff it holds on >= 4/5 seeds.

## 5. Tests

### I2 (menu growth)

- (a) Consolidation emits at least one RECRUITED event with
  gain > 0 and F-BREAK passing, on >= 4/5 seeds. Seeds with
  no qualifying fragment are valid NO-RECRUIT outcomes
  (T-NOFIRE precedent): they are excluded from I4 metrics
  and counted against this bar.
- (b) F-MENU does not fire: at least one Phase 3 kept tree
  across all seeds contains a recruited opcode from its
  seed's consolidation.
- (c) M1 bar met.
- (d) M4 audit passes on all counted seeds.

I2-PASS iff (a), (b), (c), (d) all hold.

### I4 (reuse gain)

F-NOGAIN does not fire: at least one of the M1, M2, M3 bars
is met. M5 and M6 are reported; M6's expansion claim follows
its own bar. I4-PASS iff F-NOGAIN does not fire and hard
gates are clean.

### I5 (independent adversary)

Second C0-C data point for the integrated architecture
(F-PARCOND was the first, on the Q4 line).

1. After the I2/I4 result commit (recruited fragment F_I2 on
   record), an independent agent is assigned. Independence
   means: did not build the integration, no shared working
   state with the builder.
2. The adversary draws family Z (training, 3 episodes sharing
   a fragment F_Z) and family W (test, true cause embedding
   F_Z in novel configuration). Constraint: arity(F_Z) !=
   arity(F_I2), or canonical-shape(F_Z) !=
   canonical-shape(F_I2) under DETECT's canonicalization
   (alpha-equivalence check). The adversary exhibits an
   intended base-menu solution for W needing >= 4 base ops,
   so compression has room to show.
3. The adversary commits a draw transcript before the learner
   runs: parameters, intended fragments, the constraint
   check, sealed RNG via /dev/urandom with SHA recorded
   (F-RECFOLD precedent). If the constraint check fails, the
   draw is VOID and redrawn; silent redraw is forbidden.
4. The learner runs I5: Phase 1 (3 episodes of Z) then
   consolidate then Phase 3 (W, grown) vs control (W,
   recruitment disabled), same 5-seed discipline.
5. Bar: RECRUITED fires for a qualifying fragment on >= 4/5
   seeds and at least one of the M1/M2/M3 bars (measured on
   W) is met; OR the honest-diagnosis clause: the committed
   detection log shows which regularities were counted and
   why none qualified with gain > 0. The diagnosis must cite
   log lines, not assertions.

I5-PASS iff the bar or the honest-diagnosis clause holds with
hard gates clean.

## 6. Falsifiers

Frozen from the Phase A prereg, evaluated in Phase B:

- F-MENU: the beam never expands a recruited opcode in any
  Phase 3 run (I2 or I5). Kills the C0-B strengthening.
- F-NOGAIN: recruited ops never reduce node count,
  interventions, or candidate evaluations versus control
  (M1, M2, M3 all fail their bars). Kills the C0-D
  strengthening.

Hard gates (kill the run or the claim as specified):

- F-SOURCE: any dedicated semantic case for a recruited
  meaning in source (branch naming what op 32+ means beyond
  the generic dispatch). Kills the C0-A strengthening;
  checked by source grep.
- F-DRIVER: any RECRUITED event emitted outside
  consolidate(). Kills the learner-authored claim.
- F-BREAK: any kept-variable output change on validation
  inputs after rewrite or retirement. Kills mechanism
  soundness.
- F-LEAK: validation or recruitment touches the harness
  truth table outside the learner's intervention budget, or
  reads a truth table not derived from observed samples.
  The run is VOID, not merely failed.

Phase B specific:

- F-CTRLGAP: control arm is not the same binary, or not the
  same episodes/seeds, as the grown arm. Voids the
  comparison.
- F-SEEDTAINT: any Phase 3 seed collides with a previously
  committed seed set. Voids the affected seed; if all five
  are affected, voids the wave.
- F-STALEOP: a counted Phase 3 kept tree's recruited opcode
  was not recruited in its seed's consolidation (stale
  persistent state). The seed does not count; if all seeds
  are affected, the wave is VOID.

## 7. Verdict logic

- I2-PASS: section 5 I2 (a)-(d).
- I4-PASS: F-NOGAIN not fired; hard gates clean.
- I5-PASS: section 5 I5 bar or honest-diagnosis clause;
  hard gates clean.
- PHASEB-PASS: I2-PASS and I4-PASS and I5-PASS, K4 pure Zag
  at every stage, 3/3 byte-identical runs, exit 0.
- Otherwise PHASEB-FAIL, naming the fired falsifier or the
  missed bar.

The implementer reports PHASEB-PASS or PHASEB-FAIL only
(promotion-pipeline builders report BUILD-PASS/BUILD-FAIL).
No SURVIVES claim follows Phase B: independent reproduction,
alternative-explanation attack, OOD, ablation, transfer,
red team, and governance audit remain (pipeline steps 4-11).

## 8. Honest scope and ceiling

Even with I2, I4, I5 all passing and no falsifier firing,
Phase B is stronger bounded L2, not L3:

- The recruitment candidate space is researcher-enumerated
  (subtree shapes 2..6 ops, arity 1..4); the learner selects
  from it, it does not design the space.
- The detection criterion family (subtree frequency plus
  compression gain), the beam driver, the base alphabet, and
  every numeric constant remain researcher-authored.
- C0-D is evidenced at L2: a recruited structure improves
  later discovery efficiency within the supplied framework.
  This does not show the learner inventing its own
  recruitment criteria or its own primitives.
- No new C0-A or C0-B claims are made in Phase B; A1-A4 and
  B1-B4 from the design are regression gates here, not new
  strengthenings.
- C0-C reaches two data points for the integrated
  architecture (F-PARCOND on the Q4 line, I5 here), still
  short of "multiple unforeseen forms" as a habit.

What Phase B genuinely buys: the first measurement of
whether a runtime-grown menu does cognitive work. If
F-NOGAIN fires, the integration is honest infrastructure
with no demonstrated reuse benefit, and the C0-D direction
for this architecture is closed pending redesign. If
PHASEB-PASS, the line holds the only TNN result putting
recruited meaning (C0-A direction), a grown menu (C0-B
direction), an adversary family (C0-C direction), and
cheaper later discovery (C0-D direction) in one trace.

## 9. Risks

1. Phase 1 may not keep the factored form (the beam may keep
   an equivalent but differently-factored tree, or a
   larger form). Mitigation: the I2a validity gate; seeds
   without qualifying recruitment are honest NO-RECRUIT
   outcomes, not silent exclusions. The prereg may not
   hand-tune episodes after seeing kept trees.
2. The beam may recruit yet never expand op 32 in Phase 3
   (F-MENU fires). This is a real discovery limitation,
   not a harness defect; the verdict records it.
3. The 200/opc simplicity tax may distort selection (the Q4
   R3 failure showed the tax blocking true compositional
   forms). Mitigation: TAXOFF_UNIQ diagnostics are logged
   per episode; tax-off ties are reported but do not change
   verdicts.
4. Toolchain: the H-NEW-3 pilot reported []i32 slices from
   _zag_malloc as unreliable on this znc build (heap
   corruption under allocation pressure). The implementer
   must use the []u8 plus get32/set32 pattern and pressure-
   test any array-heavy path before freezing.

## 10. Prereg requirements (binding on the Phase B prereg)

The Phase B prereg must freeze, before any implementation:

1. Exact family X episodes (variable triples), family Y-std
   and Y-hard episodes or the seeded generator, and the
   5-seed list with the disjointness proof.
2. The candidate-evaluation counter definition bound to a
   code location.
3. The metric margins exactly as specified in section 4
   (M1: -1 node; M2: -2 interventions; M3: 0.8x; M4/M5/M6
   as specified). Margins may not be weakened after the
   prereg.
4. The I5 ordering (I2/I4 result before adversary draw),
   the adversary independence criterion, and the draw
   transcript format.
5. The A-CTRL disablement mechanism (how recruitment is
   disabled in the same binary).
6. The per-seed fresh-state procedure.

The prereg is committed alone; implementation follows only
after the freeze commit. Standard governance applies: pure
Zag (znc plus shell and git only), zero Python at every
stage including verification and byte checks, zero em/en
dash bytes, pathspec commits on owned paths only, nothing
pushed.

## 11. Kill-bar self-check

- K1 (design complete): sections 2-7 specify the worked
  example with predicted node counts, the three arms, seed
  discipline, budgets, measurement definitions, metrics
  M1-M6, tests I2/I4/I5 with bars, all falsifiers, the I5
  adversary protocol, verdict logic, honest scope, risks,
  and binding prereg requirements. Complete.
- K2 (metrics specified): M1 node count, M2 interventions,
  M3 evaluations, M4 structural audit, M5 ablation, M6
  capability, each with a frozen bar and a per-seed
  evaluation rule (>= 4/5 seeds). Specified.
- K3 (no implementation): this document contains no Zag
  source, no binaries, no runs, no measurements. The
  owned directory contains only this file.

## Verdict: DESIGN-COMPLETE
