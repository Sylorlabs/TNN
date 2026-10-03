# C0INTEG Phase B Prime Design: Reuse Benefit with Stability Characterization

Date: 2026-09-30. Worker: Phase B Redesigner.
Status: DESIGN ONLY. Not a preregistration. The builder freezes their own
preregistrations (pilot and main) before any implementation. No .zag, no
binaries, no runs.
Zero Python used at any stage. This file is byte-verified free of em/en dashes.

## 1. Mission and grounding

Phase B (`a2896f022480d0c1da972159ff600680c2c9c8d0`, PHASEB-FAIL, prereg
`ba971c03dd8d6f09214d5b41f7be65b76cf4cec5`) asked whether the Phase A
OP-RECRUIT integration (`c3d8aaf90`, PHASEA-PASS) produces measurable reuse
benefit (C0-D at bounded L2). The wave was governance-clean and the FAIL is
canonical evidence. The post-mortem (`fc613823e`, PHASEB-POSTMORTEM-COMPLETE)
found two independent causes:

- Cause 1 (primary): the beam's 200/opc simplicity tax finds different
  minimal equivalents across Phase 1 episodes (for example, the 2-op
  AND(b0,OR(b1,b2)) instead of the intended 3-op factored OR), so
  consolidation sees nshapes=2 or 3, winner=-1, and no fragment reaches
  the frozen K_FREQ=3 on 0/5 seeds.
- Cause 2 (independent): the Phase 3 probe families (Y-std, Y-hard) never
  reached 64/64 true accuracy within the 24-intervention budget on either
  arm (observed 48-62/64), so the M1/M2/M3 gain metrics were unmeasurable
  regardless of recruitment.

The post-mortem's section 6 recommends Phase B prime: keep every bar, add
two pilot-validated preconditions (fragment-stability characterization,
Phase 3 convergence validation), state the tax-consistency tension
explicitly, and name the resolving mechanism or a dedicated falsifier.
This document designs Phase B prime at buildable precision.

What Phase A and B proved and what is reused unchanged: the OP-RECRUIT
mechanism (DETECT/PROPOSE/VALIDATE/RECRUIT/RETIRE), the generic dispatch for
opcodes 32..63, the consolidation constants, the beam driver and scoring,
the three-arm structure, the seed discipline, metrics M1-M6 with frozen
bars, falsifiers F-MENU and F-NOGAIN, the hard gates, and the I5 adversary
protocol. The failure was in the Phase B family design, not the recruitment
machinery, so Phase B prime changes the families and the validation, not
the mechanism.

## 2. What stays unchanged

No bar is weakened. Carried forward verbatim from the Phase B design
(`2571d52c199704ebf1d1c4589697fb23d26e5019`, sections 1, 3, 4, 6, 7):

- Constants: K_FREQ=3, COST_INSTALL=3, N_VAL=16, W_IDLE=3, MIN_FRAG_OPS=2,
  MAX_FRAG_OPS=6, MAX_ARITY=4, MAX_REC=32, beam width 32, node bound 7,
  complexity penalty 200 per operator node, keep margin 0.15, simplicity
  epsilon 0.02, base ops {AND, OR, NOT, XOR} with hand-written truth tables.
- Arms: A-GROWN (Phase 1, consolidate, Phase 3), A-CTRL (Phase 3 only,
  recruitment disabled in the same binary), A-ABLATE (2 seeds, retire then
  Phase 3 Y-std).
- Budgets: 8 passive samples plus up to 24 adaptive interventions per
  episode (Q4 standard).
- Metrics M1-M6 with the frozen bars (M1: grown opc <= control opc - 1;
  M2: grown interventions <= control - 2; M3: grown evaluations <= 0.8x
  control; M4 structural audit; M5 ablation; M6 capability), each met iff
  it holds on >= 4/5 seeds.
- Falsifiers F-MENU and F-NOGAIN. Hard gates F-SOURCE, F-DRIVER, F-BREAK,
  F-LEAK, F-CTRLGAP, F-SEEDTAINT, F-STALEOP.
- The I2a validity gate: seeds with no qualifying fragment are honest
  NO-RECRUIT outcomes, counted against the bar, not silently excluded.
- The I5 adversary protocol, still conditional on I2 firing, with the
  honest-diagnosis clause unchanged.
- Seed discipline: fresh seeds per wave, disjointness proved against all
  previously committed sets: tainted {11,22,33,44,55},
  {123456789, 555555555, 770404483}, R4's 12 seeds, R1's
  {81113, 82090, 83067, 84044, 85021}, and Phase B's
  {90011, 90988, 91965, 92942, 93919}.
- Verdict logic: PHASEB-PASS iff I2-PASS and I4-PASS and I5-PASS with hard
  gates clean, K4 pure Zag at every stage, 3/3 byte-identical runs,
  exit 0. Otherwise PHASEB-FAIL naming the falsifier or the missed bar.

## 3. The tax-consistency tension (stated explicitly)

The beam's 200/opc simplicity objective is the selection force in Phase 1
discovery (where minimality is desired), while consolidation assumes
cross-episode canonical-shape identity. A fixed tax cannot distinguish a
simpler equivalent of the same causal form from a different form:
AND(b0,OR(b1,b2)) and OR(AND(P0,P1),AND(P0,P2)) are the same function with
different canonical shapes, and the tax prefers the former. This is the
third independent appearance of tax-induced structural instability in the
program (Q4 R3, T-ADV5-adjacent beam work, Phase B).

Resolving mechanism (named): align the consolidation target with the
beam's own minimizers, verified empirically. We do not alter the tax, the
beam, the consolidation constants, or the detection rule. We restrict what
we ask consolidation to detect to fragments that the frozen beam reliably
produces across episodes, as measured by the Stage 1 characterization
wave. The tax then works for consolidation (it produces the same shape
repeatedly) instead of against it.

Residual risk (open, with dedicated falsifier): the beam may find a novel
compact equivalent on main seeds that the pilot did not surface.
Falsifier: F-STAB (section 7).

## 4. Two-stage governance

Phase B prime runs as two governed stages. The pilot stage characterizes;
the main stage tests. Nothing about the main wave is chosen by inspecting
pilot kept trees.

Stage 1 (stability characterization):

- The pilot prereg (PREREG_PHASEB_PRIME_PILOT.md) freezes: the candidate
  grid (section 5), the measurement protocol and stability score
  (section 6), the selection rule and thresholds, the G3 calibration
  gate, the stage-1 pilot seed list with disjointness proof, and the
  Y-probe construction rule (section 8). Committed alone before any pilot
  implementation.
- Pilot implementation and run: pure Zag, 3/3 byte-identical, zero
  Python. Committed.
- Pilot result commit: stability scores per family, the selected family
  computed by the frozen rule (arithmetic shown), the measured intended
  fragment F* (the most-frequent recruited shape, computed, not
  eyeballed), and the Y-probe convergence results.

Stage 2 (probe convergence validation) is part of the same pilot wave:

- The builder's pilot run instantiates Y-probe candidates from F* per
  section 8 and validates them on the control arm with stage-2 pilot
  seeds (fresh, disjoint from stage-1 seeds and all committed sets).
- A probe family is frozen only if the control reaches 64/64 true
  accuracy within the 24-intervention budget on >= 4/5 stage-2 seeds.
  Both Y-prime-std and Y-prime-hard must pass; otherwise PROBE-NONE.

Transparent amendment:

- After the pilot result commits, the builder amends with
  PREREG_PHASEB_PRIME_MAIN.md: the family selection and the concrete Y
  episodes computed from the pilot result by the frozen rule, the main
  5-seed list with disjointness proof, and all metrics, falsifiers, and
  bars unchanged. The amendment exhibits the selection arithmetic.
  Committed alone before any main implementation.
- Main implementation and run: pure Zag, 3/3 byte-identical.

Pilot terminal outcomes: STAB-NONE (no candidate family reaches the 0.8
stability threshold), CALIB-VIOLATION (G3 reaches 0.8, so the apparatus
cannot reproduce the known failure), PROBE-NONE (a probe family fails the
4/5 convergence rule). Any of these yields PILOT-FAIL; the main wave does
not launch. These are honest outcomes, not defects.

## 5. Stage 1 candidate grid

Five candidate Phase-1 families, each three episodes with fixed terminal
bindings. Each episode's true cause is stated as the intended form; the
beam is free to keep any form. Inclusion rationale is hypothesis, not
evidence; the measurement decides.

- G1 (mixed AND/OR, disjoint bindings): E1: AND(OR(X1,X2),AND(X3,X4));
  E2: AND(OR(X5,X6),AND(X1,X3)); E3: AND(OR(X2,X4),AND(X5,X6)).
  Intended fragment: AND(OR(P0,P1),AND(P2,P3)), 3 ops, arity 4.
  Rationale: disjoint variable sets across the two subterms resist
  distributive factoring; no common factor exists.
- G2 (NOT-mixed asymmetric): E1: OR(AND(X1,NOT(X2)),AND(X3,X4));
  E2: OR(AND(X5,NOT(X6)),AND(X1,X3));
  E3: OR(AND(X2,NOT(X4)),AND(X5,X6)).
  Intended fragment: OR(AND(P0,NOT(P1)),AND(P2,P3)), 4 ops, arity 4.
  Rationale: the NOT blocks the factoring that killed the original
  family; no common factor across the disjuncts.
- G3 (calibration): the original Phase B X1/X2/X3 verbatim:
  E1: OR(AND(X1,X2),AND(X1,X3)); E2: OR(AND(X4,X5),AND(X4,X6));
  E3: OR(AND(X2,X4),AND(X2,X6)).
  Expected outcome: low stability (reproduces the known failure). If G3
  reaches the 0.8 threshold, the apparatus is suspect: halt with
  CALIB-VIOLATION. G3 is never selectable for the main wave.
- G4 (nested): E1: AND(X1,OR(X2,AND(X3,X4)));
  E2: AND(X5,OR(X6,AND(X1,X3))); E3: AND(X2,OR(X4,AND(X5,X6))).
  Intended fragment: AND(P0,OR(P1,AND(P2,P3))), 3 ops, arity 4.
  Rationale: the factored form is strictly simpler than its distributive
  expansion (4 ops); tests whether the beam stably keeps a nested
  factored form.
- G5 (factored OR, disjoint bindings): E1: OR(AND(X1,X2),AND(X3,X4));
  E2: OR(AND(X5,X6),AND(X1,X3)); E3: OR(AND(X2,X4),AND(X5,X6)).
  Intended fragment: OR(AND(P0,P1),AND(P2,P3)), 3 ops, arity 4.
  Rationale: the disjoint-variable variant of the original; tests
  whether the shared variable was the factoring culprit.

## 6. Stage 1 measurement protocol and selection rule

Per candidate family (G1, G2, G4, G5; G3 measured as calibration):

- 5 pilot triples. Each triple: the family's three episodes in order
  (E1, E2, E3), each with fresh persistent state, the frozen Phase B
  beam (all section 2 constants), 8 passive samples plus up to 24
  adaptive interventions, keep margin 0.15, node bound 7.
- Per triple, run the in-run consolidation exactly as the main wave
  would: DETECT over the three kept trees; record nshapes, the
  most-frequent canonical shape and its freq, and whether RECRUITED
  fired (freq >= K_FREQ=3, gain > 0, F-BREAK pass).
- Stability score p(family) = (triples with RECRUITED firing) / 5.
- Selection rule: select the family with max p; require p >= 0.8;
  tie-break by higher mean top-fragment freq across the 5 triples, then
  lower family index. G3 is excluded from selection.
- If no family reaches 0.8: STAB-NONE, PILOT-FAIL, halt.
- F* (the intended fragment for probe construction) = the
  most-frequent recruited canonical shape across the 5 triples of the
  selected family, computed from the committed pilot log. The builder
  exhibits the computation; no kept tree is inspected to choose it.

Pilot seed discipline: stage-1 seeds are fresh; the pilot prereg proves
the full seed list disjoint from the tainted sets (section 2) and from
the stage-2 seeds.

## 7. New falsifier: F-STAB

- p_pilot: the selected family's stability score from the committed
  pilot result.
- p_main: the fraction of the 5 main-wave seeds on which a qualifying
  fragment recruited (RECRUITED, gain > 0, F-BREAK pass). I2a
  NO-RECRUIT seeds count in the denominator.
- F-STAB fires iff p_main < p_pilot - 0.4.
- F-STAB kills the stability-characterization claim: the
  characterization did not transfer from pilot to main seeds. It is
  distinct from F-NOGAIN (reuse benefit) and from the I2(a) bar (which
  F-STAB diagnoses, not replaces). The 0.4 margin is a design parameter
  the builder's prereg adopts or transparently amends with rationale.

## 8. Stage 2: Y-probe construction and convergence validation

Let F* be the selected family's intended fragment with arity k (k in
1..4 by the frozen MAX_ARITY). Probe candidates are constructed by the
frozen rule:

- Y-prime-std: D-prime = XOR(F*(fresh terminals), Xd), where F* is
  instantiated on k fresh terminals disjoint from all Phase-1 bindings,
  and Xd is one additional fresh terminal. The intended base-menu
  solution needs >= 4 base ops (room for compression); the builder's
  amendment verifies this against the intended form.
- Y-prime-hard: D-double-prime = AND(F*(fresh binding A), F*(fresh
  binding B)) with two disjoint fresh k-terminal bindings. The intended
  base-menu solution needs >= 6 base ops.

Validation: the control arm (recruitment disabled, same binary) runs
each probe candidate on 5 stage-2 pilot seeds (fresh, disjoint from
stage-1 seeds and all committed sets), 8 passive plus up to 24 adaptive
interventions, keep margin 0.15. Freeze a probe family only if the
control reaches 64/64 true accuracy within budget on >= 4/5 seeds. Both
probes must pass; otherwise PROBE-NONE, PILOT-FAIL, halt.

The intended-room constraints (>= 4 and >= 6 base ops) keep the
M1/M2/M3 compression bars meaningful: without room, a pass would be
vacuous.

## 9. Main wave (unchanged skeleton)

With the amended prereg frozen: the three arms (A-GROWN, A-CTRL,
A-ABLATE), the selected X-prime family for Phase 1 (3 episodes per
seed), consolidation, then Phase 3 on the validated Y-prime-std and
Y-prime-hard probes, 5 fresh main seeds, 3/3 byte-identical runs per
seed per arm, metrics M1-M6 with the frozen bars, falsifiers F-MENU,
F-NOGAIN, and F-STAB, all hard gates, the I2a validity gate, and the I5
adversary protocol conditional on I2 firing. The main-wave
implementation reuses the Phase A mechanism code unchanged; only the
frozen families differ.

Verdict logic: PHASEB-PASS iff I2-PASS and I4-PASS and I5-PASS with hard
gates clean, K4 pure Zag at every stage, 3/3 byte-identical, exit 0.
Otherwise PHASEB-FAIL, naming the fired falsifier or the missed bar. No
SURVIVES claim follows: the 11-step pipeline's remaining steps are
untouched.

## 10. Prereg requirements (binding)

The pilot prereg (PREREG_PHASEB_PRIME_PILOT.md) must freeze, before any
pilot implementation:

1. The candidate grid (section 5) verbatim, the measurement protocol
   and stability score (section 6), the selection rule, the 0.8
   threshold, the tie-break order, and the G3 calibration gate.
2. The F-STAB definition and the 0.4 margin (or a transparently amended
   value with rationale).
3. The Y-probe construction rule (section 8), the intended-room
   constraints, and the 4/5 convergence rule.
4. The stage-1 and stage-2 pilot seed lists with the disjointness proof
   against all committed sets.
5. The candidate-evaluation counter definition bound to a code location.

The main prereg (PREREG_PHASEB_PRIME_MAIN.md) must freeze, before any
main implementation:

1. The family selection and concrete Y episodes computed from the pilot
   result by the frozen rule, with the arithmetic exhibited.
2. The main 5-seed list with the disjointness proof.
3. The metric margins exactly as in section 2 (unchanged).
4. The A-CTRL disablement mechanism and the per-seed fresh-state
   procedure.

Both preregs are committed alone; implementation follows only after
each freeze. Standard governance: pure Zag (znc plus shell and git
only), zero Python at every stage including verification and byte
checks, zero em/en dash bytes in loop documentation, pathspec commits
on owned paths only, nothing pushed.

## 11. Honest scope and ceiling

Phase B prime is stronger bounded L2, not L3, even if it passes: the
candidate grid is researcher-enumerated, the beam and all constants
remain researcher-authored, the detection criteria are unchanged, and
C0-D is evidenced at L2 only. The characterization wave is mechanism
measurement, not hand-tuning, for four reasons: (1) the selection rule
is frozen before any measurement; (2) selection is computed from
aggregate stability scores, never from inspecting kept trees to pick
winners; (3) the pilot result is committed before the main prereg;
(4) the G3 calibration gate checks the apparatus against the known
failure. The design does not claim the tax problem is solved in
general; it claims a measured, transfer-checked region where the tax is
consistent, with F-STAB watching the transfer.

## 12. Kill-bar self-check

- K1 (design complete): sections 1-11 specify the grounding, the
  unchanged skeleton, the tax-consistency tension with its resolving
  mechanism, the two-stage governance with terminal pilot outcomes, the
  candidate grid, the measurement protocol and selection rule, F-STAB,
  the Y-probe construction and validation, the main wave, the binding
  prereg requirements, and the honest scope. Complete.
- K2 (addresses failure cause): Cause 1 is addressed by the Stage 1
  stability characterization (frozen selection rule, tax-alignment
  strategy, G3 calibration gate) and watched by F-STAB. Cause 2 is
  addressed by the Stage 2 control-arm convergence validation with the
  4/5 rule and the intended-room constraints. Both post-mortem causes
  map to design components.
- K3 (no implementation): this document contains no Zag source, no
  binaries, no runs, no measurements. The owned directory contains only
  this file.

## Verdict: PHASEB-REDESIGN-COMPLETE
