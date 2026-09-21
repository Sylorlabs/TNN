# Q1N Noisy-Teacher (10% noise) — Verdict

**Date:** 2026-09-21 (PDT) · **Crew:** TQ-NOISY10 · **Track:** Q1 teacher quality
**Source dir:** `~/workspace/tnn-lab/q1n-noisy-teacher/` · **Evidence:** `evidence/`

## The question

The prereg asks for a 10%-noise teacher leg and a verdict on whether the
§L learner's judgment *filters* the teacher's false claims or *absorbs*
them. The naïve implementation — corrupt the learned teacher's claims and
teach from the world — produces a degenerate leg: the frozen Q1 wire is
span-referential (proposals carry spans, not claim values), the teaching
stimulus is rebuilt from `t5_truth`, and the corruption never touches the
learner. So Q1N runs **three legs**, not two:

| Leg | Teacher | Teaching stimulus | What it measures |
|---|---|---|---|
| `clean` | learned teacher, all-true claims | world (strict Q1 pattern) | Control: current-tree rerun of Q1B |
| `noisy` | same learned teacher + 23 false claims | world (strict Q1 pattern) | Degeneracy calibration: claim noise with no wire access |
| `taught` | same noisy teacher | **teacher's held claims** (same slot layout, same frozen §B.7 flaw schedule; only values differ) | The real question: does judgment filter or absorb? |

The taught leg is the verdict-bearing leg. The learner has no truth oracle
in it — "world truth" is only used by the harness to *count*, never to teach.

## Noise injection (frozen, deterministic, audited in-binary)

- 23 of 228 held claims flipped = **10.09%** (id % 10 == 0 on held claims).
  Selected held IDs: 20,150,40,170,60,190,210,100,230,120,10,140,30,160,50,
  180,70,200,90,220,110,0,130.
- False values use the `t5_plant_claim` construction
  (`base + ((truth - base + 1) % category_range)`): in-category, always
  different from truth (in-binary check `q1n_implausible_false_claims` = 0
  — no false value leaked out of its category range).
- 19 false claims on the 192-fact teaching path; 4 untaught (scaffold
  fact 220 + extra-tape facts 110, 0, 130).
- Post-injection audit identity: n=228, learn-gate open, 0 plants, 228
  deliberate adds, 1 disconnect — the teacher is a real learned teacher
  with noisy held claims, not a plant.

## Results

N=5 fresh runs, byte-identical:
`e0bbbbd21ce4928e9c424017d591969cb55dcef28ed77fbfa29a782b39c4661f`
All 274 CL_CHECKs green. No stderr. No RNG (static scan of Q1N-specific
source: clean).

### Leg 0 — clean control

- §B.7: **12/12 on all 8 slices** (96/96). Reproduces Q1B exactly on the
  current tree — no tree-drift confound (pins deletion, force-pin wiring).
- Learner digest = Q1B canonical
  `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`;
  teacher digest = Q1B canonical
  `6f387ee3e6fddc7692d5138fd4c1106bd745f2ec0a837956196b07c3dee756b5`.
- World-true mastery 192/192. False claims in learner: 0.

### Leg 1 — noisy teacher, strict pattern (degeneracy calibration)

- §B.7: **12/12 on all 8 slices** — same as clean, as it must be: the false
  claims never reach the wire.
- Q1N_ACCOUNT: absorbed=0, filtered=19, untaught=4 (the 19 on-path false
  claims are "filtered" only in the degenerate sense that they were never
  offered).
- Learner digest **byte-identical to the clean leg** (`6317c2dc...`) —
  the noise is provably causally inert here. This leg documents the
  degeneracy, not the judgment's filter.

### Leg 2 — noisy teacher, teacher-claim stimulus (the verdict leg)

- §B.7: **12/12 on all 8 slices** — the battery is form-blind: it measures
  proposal form (flaw identification, span validity, grounding), not
  semantic truth, so a mirror-learner scores the same.
- World-true mastery: **173/192** (= 192 − 19: exactly the 19 taught false
  claims displaced true values; everything else is true).
- False claims in learner: **19** — and the per-slice counts are
  false=absorbed in every slice (2/2, 3/3, 1/1, 3/3, 3/3, 2/2, 2/2, 3/3).
- Q1N_ACCOUNT: **absorbed=19, filtered=0, untaught=4** (structural sum
  check 19+0+4=23 passes).
- Learner digest `168c36d6...` differs from the clean leg — the false
  claims are in the end state.

## Verdict

**At 10% teacher noise, the §L learner's judgment absorbs every false claim
it is taught: 19 taught → 19 absorbed, 0 filtered.** §B.7 stays 12/12
because the battery does not see semantic truth. World-true mastery drops
exactly to 173/192 — the mirror is surgical: false claims go in, true
claims stay everywhere else.

Combined with the sibling 50%-noise result (99/99 taught false claims
absorbed, §B.7 still 12/12), the evidence says the §L learner has **no
falsehood filter at any tested noise level** — the absorption curve is
linear through the origin (0% → 0, 10% → 19, 50% → 99). The learner's
judgment is a verbatim mirror of what it was taught: truth in → truth out,
falsehood in → falsehood out, with §B.7's 12/12 reflecting judgment-form
rather than judgment-truth. A "does it believe true things" instrument does
not exist in this battery.

**DECIDED, per standing rule:** the 12/12 battery score is NOT evidence of
truth-preservation under a noisy teacher. Any claim that the learner "did
fine" under teacher noise must cite the taught-leg absorption count
(19/19), not the battery score.
