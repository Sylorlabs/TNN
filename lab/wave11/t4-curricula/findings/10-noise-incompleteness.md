# Slice 10 — Messy reality: learning under noise and incompleteness (Track 4: teaching curricula)

## 1. Slice
Track 4 / slice 10: the teaching curriculum by which TNN learns to learn under
observation noise and incomplete evidence — what corroboration thresholds and
provenance discounting it develops, and when it suspends judgment vs acts on
partial evidence.

## 2. Falsifiable claim
A staged noise/incompleteness curriculum teaches TNN to (a) calibrate its
learning rate to measured corruption via provenance discounting, and (b)
suspend judgment on partial evidence below an explicit bar — such that its
post-curriculum verdicts match the ground-truth learnability boundary in both
directions: it learns where signal remains extractable and issues explicit
evidence-holds where nothing is learnable. The curriculum succeeds only if
suspension behavior tracks the boundary; freezing on learnable data and
learning garbage from pure noise both count as failure.

## 3. Design
Corruption model: field-level noise on observations (value flips, sensor
glitches, tampered readings — input-side noise, distinct from LH-5's
reward-sign flips; see docs/lab/wave2/longhorizon/PREREG.md, LH-5 ramp).

Noise ladder (corruption rate announced per stage — known-rate regime):
- L0: 0% corruption, full observations. Baseline: what correct belief looks like.
- L1: 5% corruption. Teach 2-of-3 source agreement for belief admission.
- L2: 10% corruption. Teach per-source corruption counters; sources with
  measured corruption >2x cohort median lose weight but are not blacklisted.
- L3: 25% corruption. Teach 3-of-5 quorum; disagreement triggers
  suspensive-contradiction-hold (wave9 trust-tier amendment).
- L4: 50% corruption. Teach the hold itself: signal is unrecoverable alone;
  only multi-source agreement survives.

Blind stages: rate withheld. TNN must estimate per-source corruption from
agreement patterns and set its own gates. Known-rate stages teach the
mechanism; blind stages test generalization.

Incompleteness ladder (fields missing per observation):
- M0: 0% missing. M1: 25%. M2: 50%. M3: 75%.
- M4 (contradictory partials): two half-observations disagree; correct verdict
  is Hold, not majority vote on fragments.

Suspend-vs-act protocol (the taught content): every conclusion requires a
declared evidence-sufficiency verdict first —
SUFFICIENT (act), MARGINAL (act with uncertainty logged), INSUFFICIENT (hold,
log exactly which fields/sources would unblock). Taught by deliberate
practice: trainer presents partial-evidence cases with known ground truth;
verdicts are scored on calibration, not outcomes — acting wrongly on
insufficient evidence and holding on sufficient evidence are scored equally
bad.

Zag sketch (gate parameters are taught, then removed in blind stages):
```
struct Obs { fields: [u8; N], present: u64, /*bitmask*/ src: u32, t: u64 }
fn verdict(obss: []Obs, bar: Gate) -> Verdict {
    let w: u64 = 0; let nsrc: u64 = 0;
    for o in obss {
        if o.src == KILLED { continue; }
        w += weight(o.src) * popcount(o.present); nsrc += 1;
    }
    if nsrc < bar.min_sources { return Hold(MissingSources); }
    if w < bar.weight { return Hold(MissingWeight); }
    if corroborate(obss) < bar.quorum { return Hold(MissingQuorum); }
    return Act(corroborate(obss));
}
```

## 4. Kill bar
Either condition fires → curriculum design is dead:
(1) On a held-out blind mix (25% corruption, 50% missing fields), TNN's
verdicts disagree with the ground-truth sufficiency boundary in >15% of
cases (false acts + false holds summed — both directions fail).
(2) If TNN still extracts >80% of learnable signal at 50% corruption, the
"impossible" regime isn't impossible and the ladder teaches paranoia, not
calibration. Conversely, if verdict error exceeds 50% at or below 10%
corruption, it repeats LH-5's fragility (reward-sign corruption broke the
delayed-credit rule between 0% and 10%, regime switches 19→181) with no gain
over the naive rule — kill and report that observation noise inherits the
same knee.

## 5. Honesty notes
Weakest point: blind-stage corruption estimates are themselves learned from
agreement patterns — circular when the whole source set is corrupted together
(the known sensor-deceivable hole: sustained coordinated spoofing breaks the
hold; this curriculum teaches graceful behavior under independent noise, it
does not fix coordinated spoofing). The protocol risks teaching learned
helplessness: excessive holds are as real a failure as spurious confidence,
and the 15% bar may need per-stage recalibration. I do NOT claim noise is
unlearnable above some universal rate — the rate interacts with source count
and quorum design (more independent sources buy back higher per-source
corruption). I do NOT claim reward noise and observation noise are the same
problem: LH-5 showed reward-sign flips poison the delayed-credit rule
directly; observation noise is upstream and partly filterable, so the
observation-noise knee should sit higher — if it doesn't, that is the
interesting falsification. Verdicts must stay byte-identical given full
state; only expression may vary.

## 6. Next build step
Build the L1–L2 prototype (5% and 10% known-rate corruption, M0–M1
incompleteness) as a native Zag harness against a 2-source truth store with
seeded corruption flips: trainer sets gates explicitly, TNN learns the quorum
protocol, and verdict error is measured against ground-truth sufficiency per
stage — one binary, byte-identical reruns, zero randomness in the learner,
all corruption from logged seeded flips only.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

This document cites results that are **QUARANTINED**: the LH-5 fragility claims cited twice (reward-sign corruption breaking the delayed-credit rule between 0% and 10%, regime switches 19→181).
The cited runs trained with `explore_enabled=1`, engaging a hidden seeded LCG
(`r34v3_rng` in `r34_learner_core.zag`) in the learner's action-choice path —
a violation of the no-randomness law (r34 RNG probe, workstream 2/8, commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE).
Treat the cited numbers as recorded-but-uncertified until clean reruns exist.
The original text above is left intact for the record.
