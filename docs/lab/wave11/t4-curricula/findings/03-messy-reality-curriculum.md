# MESSY-REALITY CURRICULUM (t4-curricula / slice 03)

## 1. Slice

Design the curriculum that teaches TNN to act correctly on contradictory, noisy,
incomplete, adversarial, and distribution-shifted inputs — staged difficulty,
correct behaviors, and mastery bars, built on wave9 trust tiers + eliminative
logic + deliberate revision machinery.

## 2. Falsifiable claim

A TNN trained on the Messy-Reality Curriculum (MRC) revises ≥95% of corrupted
beliefs and holds contradictions unresolved-to-adjudication ≥95% of the time,
at 1x/10x legs with byte-identical reruns and zero RNG — whereas the same TNN
*without* the MRC stages but with identical machinery revises ≤60% and
adjudicates ≤60%. If the un-curriculumed control is within 15 points, the
curriculum teaches nothing and is dead.

## 3. Design

**MRC structure: five mess classes, each a three-stage ladder
(clean → single-class messy → cross-class compound mess).** The world presents
`mess_profile` per episode; the harness emits labeled ground-truth mess for
grading only (TNN never sees labels).

1. **CONTRADICTION** (staged: T1-vs-T1 trainer disagreement → T0 sensor vs T1
   trainer → two trusted peers disagreeing with NO higher tier available).
   Correct behavior: enter the wave9 H1 *suspensive contradiction hold* —
   freeze the belief, route to three preregistered paths (T0-confirm release,
   distrust-break, timeout-escalate). Never resolve by majority vote; resolve by
   eliminative evidence only. Mastery: ≥95% of contradictions held until a
   resolution path fires; 0% resolved by vote/counting.
2. **NOISE** (staged: Gaussian-ish bit corruption with closed-form deterministic
   schedule → correlated corruption on one channel → corruption mimicking real
   pattern). Correct behavior: keep the observation but tag provenance and
   *channel health*; distrust the channel (TT_CH_DIST after TT_M=5 consecutive
   disagrees, per wave9), not the memory. Do not strengthen memory from
   uncorroborated noisy observations. Mastery: channel-distrust triggered on
   ≥95% of corrupted-channel runs; zero memory-strengthens from noise-only
   corroboration.
3. **INCOMPLETENESS** (staged: missing fields → missing provenance → entire
   episodes absent). Correct behavior: mark absent as absent — write
   explicit UNKNOWN slots with provenance `TT_OP_ORIGIN` tagged as learner-marked
   incomplete; never fill by extrapolation. Recall surfaces the gap honestly.
   Mastery: ≥95% of missing-field episodes carry explicit UNKNOWN marks; zero
   fabricated completions in audit.
4. **ADVERSARIAL MESS** (staged: single lying reporter → colluding reporter pair
   → fabrication consistent with all other observations). Correct behavior:
   contradiction hold + per-source citation rings; trigger collusion-suspect
   (TT_OP_COLLUSION_SUSPECT) only on pattern evidence, never single-source
   accusation; escalate fabrication-consistent-with-observations to trainer
   (honest limit: no mechanism spots a perfect lie without records).
   Mastery: ≥95% of lies eventually distrusted via citation pattern; 0 false
   collusion accusations on clean runs.
5. **DISTRIBUTIONAL SHIFT** (staged: gradual drift → regime break → shift that
   invalidates pinned CORE-adjacent belief). Correct behavior: hypotheses that
   *fail eliminatively* under the new regime are deliberately revised/demoted —
   this is where the debate result is taught: revision fires on eliminative
   defeat, not on repetition of defeat. Pinned items shift to trainer review,
   never silent demotion. Mastery: ≥95% of defeated beliefs revised within the
   prereg window; 0 silent demotions of pinned items.

**How revision is TAUGHT (the 180/180 question):** the debate trial showed TNN
*can* revise when world records exist. The MRC teaches the *trigger
discipline*: stage 1 drills single-defeat revision (one eliminative refutation
→ one deliberate REVISE op, audited); stage 2 drills defeat-under-noise
(do not revise on corrupted evidence — hold until clean corroboration of the
defeat); stage 3 drills compound cases. The revision op itself is machinery;
the curriculum teaches *when not to fire it*. Kill criteria on premature
revision are graded per trial, not averaged away.

Zag-flavored: `mrc_present(leg, class, stage) -> world_cfg`; `grade_mess(ep) -> {revised, held, distrusted, fabricated}`; all grading deterministic from
audit ledger ops (TT_OP_CITE 51..71 family), no RNG anywhere.

## 4. Kill bar

The MRC dies if ANY of: (a) the curriculum-trained arm fails to beat the
machinery-only control by >15 points on revision rate or hold rate at either
leg; (b) premature-revision rate (revision later rolled back by post-change
verification) exceeds 5% at 10x — the curriculum must not teach trigger-happy
revision; (c) any clean-run corruption: curriculum-trained TNN revises a true
belief or distrusts a clean channel in ≥2% of clean baseline episodes. Byte-
identical rerun required for every leg, per program law 2.

## 5. Honesty notes

Weakest point: **adversarial class 3** (fabrication consistent with all other
observations) — per the accepted wave8 limit, no architecture spots a perfect
lie without authoritative records; the curriculum can only teach honest
escalation, not detection. Second: the control arm may already do well on
noise/incompleteness because wave9 tiers encode sane defaults — the falsifiable
gap lives mostly in contradiction and adversarial classes. Third: we grade from
the audit ledger, which *proves* operations but cannot see whether the defeat
evidence itself was genuine (the trust-tier qualifier) — the grade is only as
honest as the world harness. Not claiming: that MRC-trained TNN is safe against
sustained observation spoofing (the known accepted hole); that revision trigger
discipline transfers across memory substrates without re-training.

## 6. Next build step

Build the MRC harness stage-1 (clean → single-class) for CONTRADICTION and
NOISE only, against the existing wave9 `trust_tiers.zag` substrate reused
verbatim: 1x + 10x legs, curriculum-trained vs machinery-only control, graded
from audit ops. If the >15-point gap fails here, kill the whole MRC before
building classes 3–5.
