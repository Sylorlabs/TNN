# Conditional-First Program Search: Design

Date: 2026-09-30. Worker: Conditional-First Designer.
Status: DESIGN ONLY. No implementation. No code written or modified.
No runs executed. Zero Python at every stage.

## 0. Standing-rules name-check

1. Pure Zag only. This design is prose; no Python at any stage.
2. Byte checks via worker_snippets/check_no_dash.sh (shell only).
3. No em dashes in loop documentation. This document was written
   with hyphens only and shell-checked before commit.

## 1. Provenance and scope

This design is the primary recommendation of the beam architecture
review (BEAM-REVIEW-COMPLETE, commit 2135396ce): after three failed
beam generations (Design 1, unified U1-U7, G2) on the R3 Arm 2
compositional target, the review concludes the search representation
itself is wrong at levels 2 and 3, and opens a new design lane for
conditional-first program search with a fresh preregistration.

What this design is: a bounded-L2 search-architecture experiment
specification. A future builder preregisters from this document,
implements it in pure Zag, and runs the frozen R3 battery.

What this design is not: it is not a claim that the learner invents
conditionals (COND is researcher-supplied, exactly like AND and OR);
it is not an L3 claim; it attaches no Criterion 0 claim. It addresses
one measured bottleneck: the search representation has no gradient
toward compositional targets whose intermediates are unrewarded.

Base machinery: the frozen R3 baseline (commit 023b4f84a lineage,
file q4_r3/q4_r3.zag). NOT the failed Design 1, unified, or G2
variants. Everything not named in sections 4 and 5 stays frozen:
24 rounds, beam size 32, top-32 selection by (score desc, opc asc,
node asc), tax 200 per opc, IV selection, retention, phase1/phase2
structure, determinism requirements, pure-Zag red line.

## 2. Problem restatement

Target E (R3 Arm 2, fam 8, frozen): E = (D AND Y4) OR ((NOT D) AND Y5).
D is the phase-1 F-PARCOND target: D = IF X1 THEN (X2 XOR X3) ELSE
(X2 AND X3), available in phase 2 as a library term. Y4 = bit 3,
Y5 = bit 4, Y6 = bit 5 is the decoy. Evidence is the full 64-row
truth table. Frozen bar A2-PASS: A2-REUSE reaches 64/64 with HAS_D=1.

Review findings this design addresses:

- L2 (search representation): the pairwise combination generator
  plus evidence-fit scoring plus opc tax has no representation of
  partial compositional progress. E needs AND(D,Y4) and AND(NOT(D),Y5)
  both present in some round, then OR-combined later. Each
  intermediate alone has poor evidence accuracy, so the scorer gives
  it no value and retention drops it. No gradient points toward E.
  G0 measured exactly this: 4 Q-signature candidates in 25 rounds,
  accuracies 1, 1, 1, 9 of 64.

- L3 (conditional-structure hypothesis): semantically E is a
  conditional: if D then Y4 else Y5. The tree-of-Boolean-ops prior
  makes this a 4-op coordinated discovery with unrewarded
  intermediates. A representation with conditionals as first-class
  primitives makes it a one-step composition.

- Tax interplay (post-mortem Cause 4, review Finding 5): under the
  frozen tax, a 3-op overfitter at full fit outscores the true 4-op
  tree (opc 4, tax 800). The tax is not wrong; the representation
  makes the truth expensive.

## 3. Design overview

Two changes, nothing else:

- Change A: a COND primitive (op 4) in the operator alphabet. The
  3-input multiplexer: COND(c, a, b) = (c AND a) OR ((NOT c) AND b).
  Generic, arity 3, applicable to any three nodes.

- Change B: a Branch-Accuracy Profile (BAP) per beam member plus a
  conditional combiner move. The BAP is the missing representation
  of partial compositional progress: it records how well each
  candidate explains each branch (slice) of the evidence. The
  combiner proposes COND(c, A, B) exactly when A explains the c=1
  branch and B explains the c=0 branch.

## 4. Change A: the COND primitive

Semantics: COND(c, a, b) evaluates to a where c is 1 and b where c
is 0. Truth table from child tables: lo = (loc AND loa) OR
((NOT loc) AND lob), hi likewise, masked to 64 bits. This is the
standard multiplexer, not a target-shaped case: it is defined for
all triples of nodes and knows nothing about D, Y4, or Y5.

Canonicalization: signatures are 64-bit behavior tables, so
COND(NOT D, Y5, Y4) and COND(D, Y4, Y5) dedupe automatically via the
existing sig_lookup. No new canonicalization machinery.

Node layout: nodes grow from 28 to 32 bytes. Offsets 0..24 are
unchanged (type, op, c0, c1, lo, hi, opc). Third child c2 is stored
at offset 28. The trace record grows from 20 to 24 bytes to carry
c2. All existing code paths that touch only offsets 0..24
(sig_lookup, sig_hash, node_pred, score_node, beam selection) are
byte-untouched. node_new_term and node_new_libterm keep opc 0 and
c2 = -1.

opc accounting: COND opc = 1 + opc(c) + opc(a) + opc(b), the uniform
rule (1 plus the sum of child opcs), identical in form to the binary
ops. Terminals and library terms have opc 0, so
COND(D-lib, Y4, Y5) has opc 1. The frozen tax (200 per opc) applies
unchanged, with no COND-specific discount. The honest tax argument:
COND(D,Y4,Y5) at tax 200 outscores both the 4-op tree expansion
(opc 4, tax 800) and any 3-op full-fit overfitter (tax 600), because
the conditional form is genuinely the most compact correct
hypothesis once the alphabet contains it. No bar was moved; the
frozen tax now rewards the truth.

has_d_subexpr extension: the frozen HAS_D check walks c0 (offset 8)
and c1 (offset 12). It must additionally walk c2 (offset 28) with
the same c2 >= 0 guard. COND(D, Y4, Y5) references the D library
node directly, so HAS_D=1 holds.

Node cap: the frozen 8192-node cap is unchanged.

## 5. Change B: Branch-Accuracy Profile and conditional combiner

### 5.1 Branch-Accuracy Profile

For each beam member node n and each condition node c in the
condition set, define over the 64 evidence rows:

- rows(c, b): number of rows x with pred(c, x) = b, for b in {0, 1}.
- agree(n, c, b): number of rows x with pred(c, x) = b AND
  pred(n, x) = ev_y(x).
- slice_acc(n, c, b) = agree(n, c, b) / rows(c, b), defined only
  when rows(c, b) > 0.

The condition set is every current beam member node (terminals,
library terms, round-built nodes), enumerated in beam order. No
terminal gating, no identity filter: the enumeration is generic,
which the F-CASE audit (section 7) checks.

The BAP is recomputed each round from the 64-row evidence. Cost is
bounded: at most 32 beam members times 32 conditions times 64 rows,
about 65k predicate evaluations per round, all deterministic.

The BAP is the representation of partial compositional progress the
review found missing. Example on the frozen target: slice_acc(Y4,
D, 1) = 1.0, because on rows where D=1, E = Y4. slice_acc(Y5, D,
0) = 1.0. The decoy is discriminated: slice_acc(Y6, D, 1) = 0.5,
so no proposal fires for it at tau = 1.0.

### 5.2 Conditional combiner

After the frozen pair-combination phase inside beam_extend, run one
conditional-combiner phase:

```
for c in beam members (beam order):
  for A in beam members (beam order):
    for B in beam members (beam order):
      if rows(c,1) > 0 and rows(c,0) > 0
         and slice_acc(A,c,1) >= TAU
         and slice_acc(B,c,0) >= TAU:
        propose COND(c, A, B)   // via node_new_op, op=4
```

- TAU is a frozen design parameter. For deterministic truth-table
  evidence the design freezes TAU = 1.0. A lower TAU for noisy
  settings requires its own preregistered justification; it is not
  part of this design.
- Determinism: fixed enumeration orders, no RNG. Proposals are
  deduplicated by sig_lookup automatically.
- CAP_COND = 256: at most 256 COND proposals per round, taken in
  enumeration order, then the combiner stops. This bounds the move
  count deterministically. The existing binary pair loop is
  unchanged and runs first.
- No blind ternary enumeration. Only BAP-licensed proposals are
  made. If the BAP is the wrong progress signal, the mechanism
  fails, which is the informative outcome.

### 5.3 What does not change

Scoring (evidence-fit), selection (top 32 by score desc, opc asc,
node asc), tax, rounds, IV machinery, phase1/phase2 split, the
binary combination moves, and all falsifier definitions stay
frozen. The combiner is an additional proposal move, not a
selection change.

## 6. Worked prediction on the frozen target

Phase 2, round 0: the beam holds terminals Y1..Y6 and the D library
term. BAP: slice_acc(Y4, D, 1) = 1.0, slice_acc(Y5, D, 0) = 1.0.
The combiner proposes COND(D, Y4, Y5) in the first combiner round.
Its truth table equals E on all 64 rows; opc 1; it outscores every
rival under the frozen tax and enters the beam. A2-REUSE reaches
64/64 with HAS_D=1.

Phase 1 side effect (predicted, measurable): D itself is a
conditional, D = COND(X1, XOR(X2,X3), AND(X2,X3)). BAP:
slice_acc(XOR(X2,X3), X1, 1) = 1.0 on the X1=1 slice,
slice_acc(AND(X2,X3), X1, 0) = 1.0 on the X1=0 slice, so the
combiner proposes D directly. The builder's prereg should measure
rounds-to-D against the frozen baseline as a secondary bar. This
also gives the mechanism a second compositional target, blunting
the one-target-trick objection.

Falsifiable predictions for the future prereg:

- P1: COND(D, Y4, Y5) is proposed within at most 2 combiner rounds
  of D entering the phase-2 beam.
- P2: A2-REUSE reaches 64/64 with HAS_D=1 (the frozen A2-PASS bar).
- P3: phase-1 rounds-to-D improves on the frozen baseline (bar to
  be frozen by the builder against a measured baseline number).
- P4: no regression on the frozen controls: A1-PASS stays 1, and
  the R1 and FREC batteries reproduce their frozen outcomes.

## 7. F-CASE and anti-spoof provisions

F-CASE is the hard kill from the review: any target-shaped move
kills the mechanism on the spot, regardless of scores. For the
future prereg, F-CASE fires if any of the following holds:

1. String audit: the new mechanism sources contain any of the
   literals Y4, Y5, y4, y5, 710202, fam8, F-PARCOND, or the strings
   "710101" through "710299", in code or comments. (Citations of
   frozen commits by hash are allowed; citations by target name are
   not.)

2. Gate audit: any proposal, scoring, or selection rule branches on
   a terminal index constant (in particular 3, 4, 5) or on node
   identity. Terminal indices may appear only inside generic loops
   over 0..5 or over the beam.

3. Enumeration audit: the COND proposal loop iterates the condition
   set and the A/B sets over all beam members in beam order, with
   no skip and no identity filter. The TAU threshold applies
   uniformly.

4. Semantics audit: the COND evaluator implements the generic
   multiplexer (c AND a) OR ((NOT c) AND b) from child truth
   tables, with no branch on child identity.

5. Tax audit: the tax constant is unchanged at 200 per opc, and
   COND opc follows the uniform rule (1 plus child opcs). No
   COND-specific discount, surcharge, or exemption.

6. Generality requirement: the builder's prereg must include, in
   addition to the frozen R3 battery, at least one further
   compositional target: either the frozen F-PARCOND phase-1
   measurement (P3) or a new sealed conditional family designed by
   an independent adversary after the mechanism freeze. A mechanism
   that passes R3 Arm 2 but fails every other compositional target
   is recorded as a one-target trick, not a search-architecture
   result.

## 8. Honest scope

- Bounded-L2 search-architecture experiment only. No L3 claim, no
  Criterion 0 claim.
- COND is researcher-supplied, exactly like AND, OR, XOR, NOT. The
  novelty claim is limited to: a conditional-first search
  representation (BAP plus combiner) repairs the measured
  compositional-generation bottleneck on R3 Arm 2.
- The mechanism does not invent conditionals, does not choose its
  own representation, and does not revise its alphabet. Any future
  claim beyond bounded L2 must go through the full eleven-step
  pipeline, including an independent red team.
- Residual risk, disclosed: if a D-free 3-op tree fits all 64 rows
  of some future target, the frozen tax still prefers it and
  A2-PASS stays 0. The design bets, measurably, that the BAP biases
  generation toward D-involving conditionals before the tax
  decides. P2 is the falsifier.

## 9. Open questions

- None blocking. The G3 secondary option from the review (splice as
  a single terminal search-level experiment) is the parent's call
  and is untouched by this lane.
- The builder may freeze CAP_COND at a different value only with a
  preregistered determinism and cost argument; 256 is the design
  default.
- The builder may freeze TAU below 1.0 only for a noisy-evidence
  battery with a preregistered justification; for the frozen R3
  battery TAU = 1.0 is frozen by this design.

## 10. Kill bars

- K1 (design complete): PASS. This document specifies the operator,
  the node-layout change, the BAP, the combiner, the frozen
  parameters, the worked prediction, the F-CASE provisions, and the
  honest scope.
- K2 (addresses L2/L3 findings): PASS. Section 5 is the L2
  representation of partial compositional progress; sections 4 and
  6 are the L3 conditional-first composition; section 7 guards
  against target-shaped spoofing.
- K3 (no implementation): PASS. Prose only. No .zag written or
  modified, no binaries built, no runs executed.

CONDITIONAL-DESIGN-COMPLETE.
