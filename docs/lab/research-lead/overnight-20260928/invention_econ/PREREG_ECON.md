# PREREG: Invention Economics (Program 6)

Committed before any implementation. Frozen kill bars below.

## Objective

Measure whether learner-created persistent cognitive structures pay for
themselves: creation cost + storage cost vs future savings. Two structures
from completed work, both genuinely resident in learner state (not
researcher-authored procedures):

- **S1: persisted selected intervention (macro).** From H-CAUSALEXP-CONSTRUCT.
  The specific selected sequence (e.g. [S,OY]) is learner-derived data.
  Policy under test: persist the selected sequence verbatim as a new
  primitive for all later worlds.
- **S2: retained offset-form state.** From I2 learning-to-learn
  (offset_hyp, trusted, form_known). Genuinely learner-retained across
  families.

Out of scope: the disagreement filter procedure itself (researcher-authored
mechanism, sunk cost, not a learner invention). Its value (17x-85x fewer
real actions) was measured by the baseline worker and is cited, not re-run.

## Experiment E1: macro economics

Worlds W_k for k in {1,2,3,4,5}: H0=[(X,Z,k),(Z,Y,0)], H1=[(X,Y,k-1)].
Minimal discriminating sequence is [S, W^(k-1), OY], length k+1
(verified empirically in code: selected sequence must satisfy q0 != q1).

Contestants, run over the world sequence in order:
- SCRATCH: per world, iterative-deepening base-4 enumeration
  (slots 1..6), first sequence with simulated disagreement wins,
  exactly 1 real execution.
- MACRO: world 1 identical to SCRATCH; the selected sequence M is then
  persisted as a 5th primitive (verbatim, warts and all). Worlds 2..5 use
  base-5 enumeration over {S,W,OY,OZ,M} with M expanded in simulation.

Currencies:
- checks(w): number of with-observe sequences simulated (both hypotheses)
  before selection, per world.
- real(w): real-world executions, must equal 1 for every world/contestant.
- storage: bytes of M (2 action bytes + 1 length byte = 3), reported.

Accounting (world-1 checks cancel: both contestants pay them):
- net_checks = sum_{w=2..5} (checks_scratch(w) - checks_macro(w))
- Verdict on sign of net_checks; storage reported as negligible-scale
  context (single-digit bytes vs hundreds of checks).

## Experiment E2: offset-form economics, extended

Reimplementation of the I2 learner (compact, from the frozen I2 prereg
spec). Families, criterion 8 consecutive correct:
- A: x 1..20, y = x+3
- B: x 21..40, y = x+7
- C: x 41..60, y = x+12
- D: x 61..80, y = x+1
- E: x 81..100, y = x+20
- F: x 101..108 cycled twice (16 examples), y = 3x (non-offset,
  memorization-only; both learners must fall back to memory)

Contestants:
- RETAIN: carries (offset_hyp, trusted, form_known) across families.
- FRESH: resets all state per family.

Metrics:
- saving_fam = fresh_fam - retain_fam for B..E (examples).
- misfit_F = retain_F - fresh_F (examples; expected small: the
  trust/distrust check fires on the first misprediction).
- storage = 12 bytes (three i32).
- creation cost of the meta-state: incremental examples on A beyond what
  FRESH pays on A (expected 0: the flags ride free on A's learning).
- break-even: p_star = misfit_F / (avg_saving + misfit_F), the
  same-form probability above which persistence has positive expected net.

## Kill bars

- K1 (E1 correctness): SCRATCH and MACRO each select a sequence with
  simulated q0 != q1 on all 5 worlds. Else FAIL.
- K2 (E1 measurement): exact checks(w) and real(w) reported per
  world/contestant; real(w) == 1 everywhere. Else FAIL.
- K3 (E1 verdict): ECON-POSITIVE if net_checks > 0, ECON-NEGATIVE if
  net_checks < 0, ECON-MIXED if per-world (checks_scratch - checks_macro)
  takes both signs. Storage bytes reported.
- K4 (E2 reproduction): A=13, B_retain=10, B_fresh=13 (must match I2
  exactly). Else investigate and report; do not proceed silently.
- K5 (E2 extension): retain vs fresh examples reported for C, D, E;
  cumulative savings reported.
- K6 (E2 misfit): retain_F and fresh_F reported; misfit_F computed.
- K7 (E2 break-even): p_star reported per formula above.
- K8 (determinism): 3/3 byte-identical raw output, exit 0, zero stderr
  (toolchain warnings on stderr are permitted only if identical across
  runs and documented).
- K9 (governance): pure Zag, zero Python at any stage including scratch;
  zero em-dash bytes in committed files; prereg strictly before
  implementation (this file).

## Overall verdict mapping

- ECON-POSITIVE: both structures show positive net.
- ECON-NEGATIVE: both show negative net.
- ECON-MIXED: signs differ (report per structure).

## Key question to answer

When should a learner bother to invent/persist a structure vs relearning
from scratch? Answer from measured numbers, not intuition.
