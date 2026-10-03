# Beam Post-Mortem: Why A+B+D Failed

Date: 2026-09-30. Worker: Beam Post-Mortem Analyzer.
Verdict: BEAM-POSTMORTEM-COMPLETE.
Status: ANALYSIS ONLY. No implementation. No code written or modified.

## 1. What was built and what happened

Design 1 (`beam_redesign/BEAM_REDESIGN.md`, commit `27a8fd108`): A
(niching) + B (tax annealing) + D (diverse IV hypothesis set via beam
layout); C (explicit compositional operators) rejected as primary fix.

The Beam Builder implemented Design 1 faithfully (diff-reviewed: only
the specified changes; prereg `2677d90fc` strictly before
implementation). Control reproduced R3-FAIL exactly on the frozen
`q4_r3.zag` (`023b4f84a`, md5 `7ed09fda269b59cdbbf75e0df720661c`,
3/3 identical). New beam ran 3/3 byte-identical (md5
`983d2b3e5a3efe2983f85734007a043b`), zero stderr.

Result (`beam_impl/BEAM_RESULT.md`): BEAM-FAIL. F-DIVERSE-FAIL fired.
Arm 2 reuse reaches 50/64 (control: 53/64), 24 IVs, never 64/64.
HAS_D=1, so this is not re-derivation. Arm 1 does not regress (reuse
64/64 at 0 IVs). F-REGRESS, F-BLOAT, F-CASE: not fired.

K4 note: the builder invoked a no-op `python3 -c "pass"` during
post-run diagnostic preparation, after all scored runs completed. Per
the literal pure-Zag rule this is a K4 incident; purity certification
for the BEAM-FAIL wave is revoked. The scored measurements (complete
before the incident, 3/3 byte-identical) stand as deterministic
negative evidence, flagged with this incident. They are not K4-clean.

## 2. The design's theory vs the observed failure

The design diagnosed a two-fold trap:

- Fold 1 (tax ceiling): at equal evidence fit, the 3-op overfitter
  (9400 at tax 200) permanently outscores the true 4-op E (9200).
  Escape requires refuting evidence.
- Fold 2 (monoculture): the global top-32 beam collapses to
  overfitter variants, so the disagreement-driven IV selector sees no
  disagreement, selects no informative IV, and no refuting evidence
  arrives.

The predicted fix chain: niching keeps compositional building blocks
alive in their own species; diverse parents let the generator produce
E; E and the overfitter both enter the per-species IV set;
disagreement IVs target distinguishing combos; refuting evidence
drops the overfitter below full fit; under the late full tax, E wins.

Observed: niching was active throughout (72 of 76 extends held 8
species, at the merge cap; 4 held 5). The compositional form E was
still never discovered within 24 IVs. The champion-disagreement IVs
did not produce refuting evidence against the overfitter within the
IV budget. Arm 2 scored slightly worse than control (50 vs 53).

## 3. Root cause analysis

Cause 1 (primary): the generation gap. The design's fix chain
assumed E "can be generated" once beam parents are diverse. That
assumption was never validated and is false on the evidence. Niching
is retention machinery: it only protects candidates the generator
proposes. The diverse IV set is selection machinery: it only
exploits hypotheses already in the beam. Neither creates E. The
design fixed everything downstream of the bottleneck and nothing at
the bottleneck.

Cause 2 (mechanism hypothesis, testable): the species-merge rule
kills novelty. With 72/76 extends at the 8-species cap, the merge
rule ("merge the two smallest species by member count") ran
constantly. A nascent E appears as a singleton species (one member,
just generated); the merge rule preferentially destroys exactly the
novel structural forms niching was meant to protect, before they can
establish a foothold. This is consistent with "niching active, E
never discovered." It is a hypothesis, not a proven cause; see G0.

Cause 3: the IV policy cannot target what is not in its input set.
Disagreement among species champions is only informative if some
champion disagrees with the overfitter on the critical combos. With
E absent from the beam, no hypothesis does. Disagreement among wrong
hypotheses does not concentrate on the overfitter's failure modes,
so Fold 2 was not actually fixed either. The policy is only as good
as its hypothesis set.

Cause 4: the tax ceiling held by design. At the final tax (192, from
the annealing schedule), the overfitter at full fit still outscores
E at full fit (9424 vs 9232). This was the design's honest property:
escape requires refuting evidence. Per Cause 3, none arrived.

Net: the binding constraint was generation, not retention or
selection. Fixing downstream of the bottleneck cannot move the
outcome, which is why a faithful build with active niching still
failed, slightly worse than control.

## 4. What this means for U1-U7 (in flight)

The Unified Beam Builder is implementing the reconciled U1-U7 design
(prereg frozen, `beam_unified/PREREG_BEAM_UNIFIED.md`) across R1, R3,
and F-RECFOLD. The reconciler's complementarity argument (Pareto
protects the accuracy path during exploration; niching protects the
compositional form at full overfitter fit) is logically sound, but
the BEAM-FAIL evidence weakens its key premise:

- U1 (Pareto retention within species): protects high-accuracy
  candidates from being pruned by lower-accuracy ones. E was never
  generated, so there was nothing to protect. Does not address
  Cause 1.
- U4 (diverse IV hypothesis set): the same mechanism as Design 1's
  D. Subject to the same Cause 3 limitation.
- U6 (diversity floor, 4 of 32 slots): protects early rounds from
  collapse to 1-2 species. Does not address the steady-state merge
  problem (Cause 2).
- U5 (principled tie-breaking), U3 (two-phase tax), U7 (honest tie
  reporting): address R1 evidence-fit and tie symptoms, not the R3
  generation gap.

Prediction, stated before the unified result lands: U1-U7 is likely
to fail F-DIVERSE-FAIL for the same generation-gap reason. The
unified build should still run to completion. It is preregistered,
and a FAIL on U1-U7 is the honest kill of the niching-plus-Pareto
direction. Do not redirect the in-flight builder; its result is the
governing data point.

## 5. Recommended next direction (after U1-U7 reports)

G0 (diagnostic first, highest information): instrument the frozen
beam to answer one question: are E-shaped candidates (a) never
proposed by the generator, (b) proposed and then merged away by the
species-merge rule, or (c) proposed and then lost within their
species to higher-scoring mates? One instrumented run settles which
of the fixes below is load-bearing. Do not build fixes before G0
data exists.

G1 (targets Cause 2): fix the merge rule. Candidate generic fixes:
never merge a species younger than N rounds; merge by lowest
best-accuracy instead of fewest members; exempt just-generated
singleton species from merging for one round. Minimal, generic, no
target knowledge.

G2 (targets Causes 3 and 4): refutation-seeking IV policy. Instead
of (or in addition to) inter-hypothesis disagreement, target the
current global best's weak points: prefer unused x where the
champion's evidence neighborhood is sparsest, or where the
fraction of the beam agreeing with the champion is lowest. Generic;
keys on the learner's own uncertainty, not on target identity.

G3 (the honest C fallback; targets Cause 1): compositional
generation moves, as generic operators only. Now permitted because
A+B+D honestly failed, per the design's own fallback clause.
Candidates: a generic crossover/splice move combining subexpressions
of two beam members; embedding any kept-library terminal as a
subexpression of a new candidate. Never target-shaped templates;
any move shaped to the R3 target kills the design on the spot.

What not to do: do not build a third retention/selection variant
without G0 data. Beam v1 (frozen) to Design 1 (failed) to U1-U7 (in
flight) is already two repair generations on the same beam lineage.
A third adjacent tweak without new diagnostic information should
trigger the architecture-review question ("is the representation
itself wrong?") rather than another beam adjustment. Note: the
frozen architecture-review trigger covers the B/C2/D valley lane,
not the Q4 beam lane; the parent decides whether the spirit of the
three-generation rule applies here.

## 6. Governance notes

- BEAM-FAIL measurements are flagged deterministic negative
  evidence, not K4-clean (Section 1). The unified builder's prereg
  discloses its own pre-prereg `python3 -c "pass"` probe; the parent
  judges whether that voids its K3.
- Bounded L2 negative result. No L3 claim, no Criterion 0 claim, no
  Q4 revival (the revival conjunction remains dead per `563a1b354`).
- The contaminated research paper was not touched. No other
  worker's files were touched. This commit contains only the
  post-mortem document.

## Kill bars

- K1 (post-mortem complete): PASS. This document.
- K2 (failure cause identified): PASS. Causes 1-4 in Section 3.
- K3 (next direction recommended): PASS. G0-G3 in Section 5.

BEAM-POSTMORTEM-COMPLETE.
