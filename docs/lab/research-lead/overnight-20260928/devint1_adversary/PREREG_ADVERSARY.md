# DEVINT1 Independent Adversary Preregistration

Worker: independent reproduction + adversary subagent.
Date: 2026-09-30.
Target: DEVINT1, builder commit `476c24b3d`, prereg `4b50ff7d4`
(BUILD-PASS 4/4, independently reproduced by this worker: 3/3 byte-identical,
md5 `612205f6e8a36f7f6e04134f3ef8014e`, prereg strict ancestor, zero Python).

Standing assumption (held throughout): the reported developmental trajectory
and synergy numbers are artifacts of researcher-supplied design choices until
proven otherwise. The BUILD-PASS as an engineering result (4/4 bars, one
process, 11 stages) is NOT contested. What is contested: whether the results
survive removal of future-data leakage, accidental control encoding, and
whether synergy is causal rather than correlational.

Method: pure Zag only. Attack programs derived from the committed builder
source (`devint1.zag` at `476c24b3d`, extracted via `git show`, no retyping
of learner machinery) plus new attack mains. Built with frozen toolchain
`znc 2026.07.0-dev`. Analysis via bash, git, znc, grep, cmp, md5sum only.
No Python anywhere. No em dashes in documentation (byte-verified pre-commit).

## Attack A1: future-data leakage (online variant)

Hypothesis: the reported trajectory depends on the lexicon being built from
all 12 S1 observations before any segmentation/concept use. A true online
learner cannot use observation t to build state consumed before t.

Construction: `adv_online.zag` = builder machinery verbatim, except the S1
feed schedule is changed to strictly incremental: episode t is segmented
using ONLY the lexicon accumulated from episodes 0..t-1 (empty lexicon for
t=0, single-char fallback). Concepts/rules update after each episode as in
the builder. All downstream stages (S2..S11) run on the resulting state.
No other changes.

Kill/downgrade criteria (frozen):
- KILL the "no leakage" reading if any of: S2 correct segmentations < 4/6,
  or concept inventory at S3 has < 3 of the 4 true morphemes, or the
  trajectory aborts/diverges (STATE-CONT counts collapse).
- DOWNGRADE (not kill) if: S2 = 4-5/6 correct, or concept counts are
  correct but segment/rule numbers degrade > 30% vs builder baseline.
- ATTACK-FAILS if: S2 = 6/6, 4 concepts recovered, and all B2 stage numbers
  within 10% of builder values (trajectory survives true online feeding).

## Attack A2: segmentation control weakness

Hypothesis: the S4 neutral result (treat-k=5 = ctrl-k=5) is an artifact of
the control's fixed-width-3 accidentally matching the true morpheme width 3.
The builder's own disclosure admits this.

Construction: `adv_segctrl.zag` = builder S1-S4 machinery verbatim, with
three additional controls replacing fixed-width-3: fixed-width-2,
fixed-width-4, and random-width (seeded LCG, widths 1..5 per position).
Measure full-coverage k and spurious count for each control on the same S1
corpus, plus the treat (SEG-core) numbers.

Kill/downgrade criteria (frozen):
- ATTACK-SUCCEEDS (control artifact confirmed) if: treat reaches full
  coverage at k <= 5 with 0 spurious while ALL of fw2/fw4/randwidth need
  k > 8 or produce >= 3 spurious. This shows the builder's chosen control
  was the uniquely flattering one.
- ATTACK-SUCCEEDS partially if: treat beats at least two of the three new
  controls on (k, spurious) jointly; then the S4 synergy claim is revived
  as positive rather than neutral.
- ATTACK-FAILS if: treat does not beat the new controls (e.g. fw2 also
  reaches k=5 clean, or treat itself needs k > 8). Then segmentation adds
  nothing measurable on this corpus.

## Attack A3: synergy reproduction (independent code)

Hypothesis: the three synergy numbers are implementation artifacts.

Construction: `adv_synergy.zag` = INDEPENDENT reimplementation (not the
builder's code) of the three synergy measurements on the same frozen
episode corpora (extracted from the builder raw output / source constants):
(a) procedure examples-to-criterion treat vs ctrl; (b) post-eviction probe
accuracy treat (importance) vs ctrl (LRU) on the 10 held-out episodes;
(c) refinement count treat (split) vs ctrl (delete-only).
Independent segmentation, concept, and rule code written fresh from the
prereg's functional descriptions.

Criteria (frozen):
- Each sub-claim REPRODUCED if the sign matches (treat<ctrl for a,
  treat>ctrl for b, treat>ctrl for c) with non-degenerate denominators.
- ATTACK-SUCCEEDS on a sub-claim if sign flips or denominator degenerates
  in the independent implementation.
- Overall ATTACK-FAILS only if all three sub-claims reproduce with the
  same signs.

## Attack A4: causal attribution (ablation of upstream structures)

Hypothesis: downstream improvements are correlational; no single upstream
learned structure is causally responsible.

Construction: three variants of the builder program, each removing ONE
upstream structure while keeping everything else identical:
- `adv_noSeg.zag`: segmentation replaced by fixed-width-3 chunking
  everywhere (concepts/rules/procedures learn from chunks).
- `adv_noConcepts.zag`: concept IDs disabled; all downstream learning uses
  raw segmented strings.
- `adv_noRules.zag`: rule store disabled; prediction/inquiry use raw
  bigram counts without ACTIVE/rollback machinery.
Measure: S6 procedure examples-to-criterion, S10 probe accuracy,
S11 reuse numbers, for each variant vs the intact baseline.

Criteria (frozen):
- ATTACK-SUCCEEDS (causal) for a (structure, downstream) pair if removing
  the structure degrades the downstream metric by >= 50% of the
  treat-minus-ctrl gap reported by the builder (or flips the sign).
- ATTACK-SUCCEEDS overall if at least two of the three ablations show
  causal degradation on their primary downstream metric
  (noSeg->S6, noConcepts->S6/S11, noRules->S10/S11).
- ATTACK-FAILS if no ablation degrades its primary metric (synergy is
  correlational or carried by unablated machinery).

## Attack A5: delayed transfer (heavy interference)

Hypothesis: reuse survives only because the interference is mild (20
distractor episodes + flood). Real delayed transfer needs heavier
interference.

Construction: `adv_delay.zag` = builder S1..S9 intact; then 240 unrelated
episodes (12x the builder's 20) drawn from a disjoint morpheme inventory
(novel 3-char morphemes, no overlap with bik/gup/zol/tav/bi/k), then the
S11 reuse battery (recognition + procedure reuse). Same eviction policies.

Criteria (frozen):
- ATTACK-SUCCEEDS if recognition < 12/17 or procedure reuse < 2/3
  (substantial degradation vs builder 17/17 and 3/3).
- ATTACK-FAILS if recognition >= 15/17 AND procedure reuse = 3/3
  (reuse survives 12x interference).

## Attack A6: restart (state persistence across process death)

Hypothesis: the "persistent learner" never actually persists; all gains
live in volatile process memory.

Construction: `adv_restart.zag` = builder program split into two phases
sharing a serialized state file:
- Phase 1 runs S1..S9, then serializes the full W buffer (concepts, rules,
  lexicon, pairings, tick) to `STATE.BIN` and exits (exit 0).
- Phase 2 starts a NEW process, deserializes `STATE.BIN`, verifies a
  checksum, then runs S10..S11.
Compare S10/S11 numbers against the single-process baseline. Any divergence
beyond byte-identity of the state checksum indicates the gains were not
actually in the serialized state.

Criteria (frozen):
- ATTACK-SUCCEEDS if: state file cannot capture the full learner state
  (checksum mismatch on reload), or S10/S11 numbers diverge from baseline,
  or the serialization requires researcher-visible restructuring of the
  learner (i.e. persistence was never a real property).
- ATTACK-FAILS if: reload checksum matches, S10 eviction/probe numbers
  identical to baseline, S11 reuse identical (persistence is real).

## Verdict aggregation

- Each attack reports ATTACK-SUCCEEDS / ATTACK-FAILS / PARTIAL per its
  frozen criteria. No retroactive criterion changes.
- The DEVINT1 BUILD-PASS (engineering) stands regardless. Attacks target
  the developmental-trajectory and synergy interpretations.
- Do NOT call DEVINT1 SURVIVES before all six attacks complete.
