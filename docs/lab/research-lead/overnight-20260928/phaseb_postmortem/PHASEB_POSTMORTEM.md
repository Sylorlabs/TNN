# C0INTEG Phase B Post-Mortem: Why PHASEB-FAIL

Date: 2026-09-30. Worker: Phase B Post-Mortem Analyzer.
Result under analysis: `docs/lab/research-lead/overnight-20260928/c0integ_phaseb_impl/RESULT_PHASEB.md`
Prereg: `ba971c03d`. Design: `2571d52c1`. Phase A baseline: `c3d8aaf90`.
Verdict of this document: PHASEB-POSTMORTEM-COMPLETE.

Zero Python used at any stage. This file is byte-verified free of em/en dashes.

## 1. What Phase B tested

Phase B asked whether the Phase A OP-RECRUIT integration produces
measurable reuse benefit (C0-D at bounded L2). Protocol: three arms
(A-GROWN, A-CTRL, A-ABLATE), five fresh seeds, frozen families X1/X2/X3
(Phase 1), consolidation (DETECT/PROPOSE/VALIDATE/RECRUIT), then Phase 3
on Y-std and Y-hard with the grown menu versus a no-recruitment control.
Metrics M1 (node count), M2 (interventions), M3 (evaluations), M4
(structural audit), M5 (ablation), M6 (capability). Falsifiers F-MENU
and F-NOGAIN. I5 conditional on I2 firing.

The result is a clean FAIL: recruitment 0/5 seeds, M1/M2/M3 0/5,
F-NOGAIN fired, I5 correctly did not run per prereg section 8. The run
was governance-clean (prereg frozen first, 3/3 byte-identical stdout,
sha256 2b7a4e040e864cfe8fe2e14a955a8096c9dab6073759af7429b815f4bf6cc609,
exit 0, empty stderr, zero Python). This post-mortem treats the FAIL as
information, not a defect in the test.

## 2. Failure cause 1 (primary): the beam's simplicity objective destroys the consolidation precondition

The Phase B hypothesis was: three factored-OR episodes (X1, X2, X3)
yield kept trees sharing one canonical fragment
OR(AND(P0,P1),AND(P0,P2)), which DETECT counts at freq=3 and RECRUITs
as op 32.

What the logs show (PHASEB_RUN1.txt, all five seeds):

- Every X episode reaches 32/32 evidence fit and 64/64 true accuracy,
  so discovery works. The kept trees are 2-3 operator nodes.
- But the kept canonical shapes differ across episodes. Every
  CONSOLIDATE line reads `nshapes=2` or `nshapes=3`, `winner=-1`:
  no single canonical shape reaches the frozen K_FREQ=3.
- On seeds 91965 and 92942 the beam keeps 2-op trees for X1 and X2.
  The 2-op form is AND(b0,OR(b1,b2)): a correct, simpler equivalent
  of the intended 3-op factored OR, found by the beam's own
  simplicity tax (200/opc). The beam is not failing; it is
  succeeding at minimality and thereby producing a different
  canonical shape than the intended fragment.
- On seeds 90988, 91965, and 93919, X3 fails the keep margin
  (keep=0), so only two trees enter consolidation, and even those
  two differ in shape.

This is exactly the design's Risk 1: "the beam may keep an
equivalent but differently-factored tree." The I2a validity gate
worked as specified: seeds without qualifying fragments were honest
NO-RECRUIT outcomes, counted against the bar, and the verdict
followed.

The mechanism is sound (Phase A proved RECRUIT fires when the
fragment is present). The hypothesis that three factored-OR
episodes reliably produce a recruitable common fragment is false
under the current beam. The tension is structural: the beam
optimizes for evidence fit plus simplicity, not for structural
consistency across episodes, while consolidation requires the same
canonical shape in all kept trees. Phase 1's success at finding
compact equivalents is what kills Phase 2's detection.

## 3. Failure cause 2 (independent): Phase 3 was unmeasurable even if recruitment had fired

Every Y-std and Y-hard run, on both arms, capped M2 at 25 (never
reached 64/64 true accuracy within the 24-intervention budget).
Observed true accuracy: 48-62/64 across arms and seeds. The control
arm fails just as the grown arm does; this is a difficulty property
of the Y families under the Q4-standard budget, not a recruitment
effect.

Consequence: the M1 bar requires grown opc <= control opc - 1 with
both arms at 64/64 true accuracy. That condition was unreachable on
every seed regardless of recruitment. M2 (first 64/64 round) was
capped everywhere, so no intervention comparison could show a gain.
Even a successful consolidation could not have produced a PASS on
the frozen bars, because the Phase 3 probe family was never
pilot-validated for control-arm convergence.

This is a second, independent design defect: family selection for
the reuse probe must guarantee that the control can solve the probe
within budget, otherwise the gain metrics are undefined.

## 4. What did not fail

- The test machinery: F-NOGAIN fired exactly as designed, naming
  the missed bars. The falsifier did its job.
- Governance: prereg before implementation, pure Zag, 3/3
  byte-identical, no Python at any stage, no bar weakened after
  results. The FAIL is canonical evidence.
- The I5 conditional: skipping I5 when I2 yields no F_I2 is correct
  protocol per prereg section 8, not a gap. The I5 adversary
  protocol stands ready for a future wave where I2 fires.
- Phase A: untouched. The OP-RECRUIT mechanism still holds its
  PHASEA-PASS; the failure is in the Phase B family design, not
  the recruitment machinery.

## 5. Architectural tension to record

The fixed simplicity tax (200/opc) that Phase 1 needs to find
minimal forms (it found the minimal D on the Q4 line, and the
compact 2-op AND(b0,OR(b1,b2)) here) is the same force that
destabilizes fragment identity across episodes. This is the third
independent appearance of tax-induced structural instability in
the program: Q4 R3 (tax ceiling blocks the true 4-op form),
T-ADV5-adjacent beam work (tax blocks compositional reuse), and
now Phase B (tax destroys the consolidation precondition).

Coordination note for the beam-repair lanes: a diversity-preserving
beam (niching, Pareto frontier) keeps more forms alive inside one
episode's beam, but the kept tree is still a single beam-top, and
cross-episode shape consistency is a separate requirement from
within-episode diversity. Whoever redesigns the reuse direction
must satisfy both: search diversity within an episode and
fragment stability across episodes. They pull in opposite
directions under a fixed tax, and the resolution has to be stated
explicitly in the next design.

## 6. Recommended next direction: Phase B prime

Do not weaken any bar. K_FREQ=3, the M1/M2/M3 margins, and the
falsifiers were not the problem; the family design was. The next
hypothesis (Phase B prime) should be preregistered as a new wave
with two pilot-validated preconditions frozen before the main run:

1. Fragment-stability characterization. Before committing to
   families, run a measurement wave over a grid of episode-family
   shapes and record the kept-tree canonical-shape consistency
   (nshapes distribution, per-shape frequency) under the frozen
   beam. Select Phase 1 families by a frozen stability rule
   (for example: pilot-measured probability that three episodes
   yield a freq>=3 fragment at or above a frozen threshold).
   This is mechanism characterization, not hand-tuning: the
   selection rule is frozen before the main wave and the kept
   trees are never inspected to pick winners.
2. Phase 3 convergence validation. Pilot the probe family on the
   control arm (no recruitment) and freeze it only if the control
   reaches 64/64 true accuracy within the 24-intervention budget
   on at least 4/5 pilot seeds. A reuse gain is only measurable
   against a solvable baseline.

Additional design guidance for the Phase B prime author:

- Prefer Phase 1 families whose intended fragment is the unique
  minimal expression under the beam's objective, so the
  simplicity tax works for consolidation instead of against it.
  Asymmetric fragments with no compact factored equivalent are
  the natural candidates; the stability characterization in
  point 1 will confirm or deny this.
- Keep the three-arm structure (grown, control, ablate) and the
  per-seed fresh-state discipline; they were correct and the
  logs show they behaved as specified (A-ABLATE ran, nrec was 0
  throughout, so its comparisons were vacuous but honest).
- State the tax-consistency tension from section 5 in the design
  and name the mechanism that resolves it, or name it as an open
  risk with a dedicated falsifier.
- The I5 adversary protocol needs no changes; it triggers when
  I2 fires.

## 7. Kill bars

- K1 (post-mortem complete): PASS. Causes 1 and 2 documented
  with log citations, non-failures listed, tension recorded,
  next direction specified.
- K2 (failure cause identified): PASS. Primary cause: beam
  keeps structurally diverse minimal equivalents across
  episodes, so no fragment reaches K_FREQ=3 (design Risk 1
  confirmed; log lines cited). Independent cause: Y families
  unsolvable within budget on both arms, making M1/M2/M3
  unmeasurable regardless of recruitment.
- K3 (next direction recommended): PASS. Phase B prime with
  frozen stability characterization and convergence validation,
  bars unchanged, tension named.

## Verdict: PHASEB-POSTMORTEM-COMPLETE
