# Phase B Prime Pilot Preregistration: Stability Characterization

Date: 2026-09-30. Worker: Phase B Prime Pilot Builder.
Status: PREREGISTRATION. Frozen before any pilot implementation.
Design: `9f1864f9` (PHASEB_PRIME_DESIGN.md).
Zero Python at every stage. This file is byte-verified free of em/en dashes.

## 1. Mission

Characterize fragment stability across five candidate Phase-1 families
using the frozen Phase B beam. The pilot selects a family for the main
Phase B prime wave via a frozen selection rule, or halts honestly.

## 2. Candidate Grid (frozen verbatim from design section 5)

Each family: three episodes with fixed terminal bindings. The beam is
free to keep any form.

### G1 (mixed AND/OR, disjoint bindings)
- E1: AND(OR(X1,X2),AND(X3,X4))
- E2: AND(OR(X5,X6),AND(X1,X3))
- E3: AND(OR(X2,X4),AND(X5,X6))
- Intended fragment: AND(OR(P0,P1),AND(P2,P3)), 3 ops, arity 4.

### G2 (NOT-mixed asymmetric)
- E1: OR(AND(X1,NOT(X2)),AND(X3,X4))
- E2: OR(AND(X5,NOT(X6)),AND(X1,X3))
- E3: OR(AND(X2,NOT(X4)),AND(X5,X6))
- Intended fragment: OR(AND(P0,NOT(P1)),AND(P2,P3)), 4 ops, arity 4.

### G3 (calibration: original Phase B X1/X2/X3 verbatim)
- E1: OR(AND(X1,X2),AND(X1,X3))
- E2: OR(AND(X4,X5),AND(X4,X6))
- E3: OR(AND(X2,X4),AND(X2,X6))
- Expected: low stability. If G3 reaches 0.8: CALIB-VIOLATION, halt.
- G3 is never selectable for the main wave.

### G4 (nested)
- E1: AND(X1,OR(X2,AND(X3,X4)))
- E2: AND(X5,OR(X6,AND(X1,X3)))
- E3: AND(X2,OR(X4,AND(X5,X6)))
- Intended fragment: AND(P0,OR(P1,AND(P2,P3))), 3 ops, arity 4.

### G5 (factored OR, disjoint bindings)
- E1: OR(AND(X1,X2),AND(X3,X4))
- E2: OR(AND(X5,X6),AND(X1,X3))
- E3: OR(AND(X2,X4),AND(X5,X6))
- Intended fragment: OR(AND(P0,P1),AND(P2,P3)), 3 ops, arity 4.

## 3. Measurement Protocol (frozen from design section 6)

Per candidate family (G1, G2, G3, G4, G5):

- 5 pilot triples. Each triple: the family's three episodes in order
  (E1, E2, E3), each with fresh persistent state, the frozen Phase B
  beam (all section 2 constants from the design), 8 passive samples
  plus up to 24 adaptive interventions, keep margin 0.15, node bound 7.
- Per triple, run the in-run consolidation exactly as the main wave
  would: DETECT over the three kept trees; record nshapes, the
  most-frequent canonical shape and its freq, and whether RECRUITED
  fired (freq >= K_FREQ=3, gain > 0, F-BREAK pass).

### Constants (carried forward from Phase B design, unchanged)
- K_FREQ=3, COST_INSTALL=3, N_VAL=16, W_IDLE=3
- MIN_FRAG_OPS=2, MAX_FRAG_OPS=6, MAX_ARITY=4, MAX_REC=32
- Beam width 32, node bound 7, complexity penalty 200 per operator node
- Keep margin 0.15, simplicity epsilon 0.02
- Base ops {AND, OR, NOT, XOR} with hand-written truth tables
- Budgets: 8 passive samples plus up to 24 adaptive interventions

## 4. Stability Score and Selection Rule (frozen from design section 6)

- Stability score p(family) = (triples with RECRUITED firing) / 5.
- Selection rule: select the family with max p; require p >= 0.8.
- Tie-break: higher mean top-fragment freq across the 5 triples, then
  lower family index.
- G3 is excluded from selection.
- If no family reaches 0.8: STAB-NONE, PILOT-FAIL, halt.
- If G3 reaches 0.8: CALIB-VIOLATION, PILOT-FAIL, halt.

### F* (intended fragment for probe construction)
F* = the most-frequent recruited canonical shape across the 5 triples
of the selected family, computed from the committed pilot log. The
computation is exhibited; no kept tree is inspected to choose it.

## 5. F-STAB (frozen from design section 7)

- p_pilot: the selected family's stability score from the committed
  pilot result.
- p_main: the fraction of the 5 main-wave seeds on which a qualifying
  fragment recruited (RECRUITED, gain > 0, F-BREAK pass). I2a
  NO-RECRUIT seeds count in the denominator.
- F-STAB fires iff p_main < p_pilot - 0.4.
- The 0.4 margin is adopted as designed (no amendment).

## 6. Y-Probe Construction Rule (frozen from design section 8)

Let F* be the selected family's intended fragment with arity k
(k in 1..4 by frozen MAX_ARITY).

- Y-prime-std: D-prime = XOR(F*(fresh terminals), Xd), where F* is
  instantiated on k fresh terminals disjoint from all Phase-1 bindings,
  and Xd is one additional fresh terminal. The intended base-menu
  solution needs >= 4 base ops (room for compression).
- Y-prime-hard: D-double-prime = AND(F*(fresh binding A), F*(fresh
  binding B)) with two disjoint fresh k-terminal bindings. The intended
  base-menu solution needs >= 6 base ops.

### Convergence Validation (frozen from design section 8)
- The control arm (recruitment disabled, same binary) runs each probe
  candidate on 5 stage-2 pilot seeds, 8 passive plus up to 24 adaptive
  interventions, keep margin 0.15.
- Freeze a probe family only if the control reaches 64/64 true accuracy
  within budget on >= 4/5 seeds.
- Both probes must pass; otherwise PROBE-NONE, PILOT-FAIL, halt.

## 7. Pilot Seed Lists with Disjointness Proof

### Stage-1 seeds (25 total, 5 per family)
- G1: 100011, 100012, 100013, 100014, 100015
- G2: 100016, 100017, 100018, 100019, 100020
- G3: 100021, 100022, 100023, 100024, 100025
- G4: 100026, 100027, 100028, 100029, 100030
- G5: 100031, 100032, 100033, 100034, 100035

### Stage-2 seeds (10 total)
- Y-prime-std: 100101, 100102, 100103, 100104, 100105
- Y-prime-hard: 100106, 100107, 100108, 100109, 100110

### Disjointness proof
All 35 seeds are in the range [100011, 100110]. The committed tainted
sets are:
- {11, 22, 33, 44, 55}
- {123456789, 555555555, 770404483}
- R4's 12 seeds (documented in the Phase B prereg)
- R1's {81113, 82090, 83067, 84044, 85021}
- Phase B's {90011, 90988, 91965, 92942, 93919}

No seed in [100011, 100110] appears in any committed set. The stage-1
and stage-2 lists are disjoint from each other. The stage-1 seeds are
disjoint across families. Freshness is established by construction.

## 8. Candidate-Evaluation Counter Definition

The candidate-evaluation counter is bound to the beam's per-episode
node-expansion counter, emitted as EVALS in the per-episode log line.
It counts the number of candidate tree evaluations (score computations)
during the episode's beam search, including both passive-sample and
intervention-driven evaluations. The counter is reset to zero at the
start of each episode and is never carried across episodes.

## 9. Kill Bars (this pilot wave)

- K1: Prereg frozen before implementation. This file is committed alone
  before any pilot .zag exists.
- K2: All families measured. 5 triples per family for G1, G2, G3, G4,
  G5 (25 triples total), plus stage-2 convergence validation for both
  probes on 5 seeds each (10 runs).
- K3: Pure Zag, 3/3 byte-identical runs. Zero Python at every stage,
  including verification and byte checks. Zero em/en dash bytes.

## 10. Terminal Outcomes

- STAB-NONE: no candidate family reaches p >= 0.8. PILOT-FAIL, halt.
- CALIB-VIOLATION: G3 reaches p >= 0.8. PILOT-FAIL, halt.
- PROBE-NONE: a probe family fails the 4/5 convergence rule.
  PILOT-FAIL, halt.
- PILOT-PASS: a family is selected per the frozen rule, F* is computed,
  and both probes pass convergence validation.

## 11. Governance

- Pure Zag (znc plus shell and git only). Zero Python at every stage.
- Zero em/en dash bytes in loop documentation. Verified with the
  shell-only `check_no_dash.sh` snippet.
- Pathspec commits on owned paths only
  (`docs/lab/research-lead/overnight-20260928/phaseb_pilot/`).
- Nothing pushed. Commits stay local.
- 3/3 byte-identical runs for every scored measurement.

## Verdict: PREREG-FROZEN
