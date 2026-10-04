# TOGETHER ENGLISH (classes 1+2) — prereg (crew-drafted 2026-09-21/22)

**Crew:** TOGETHER ENGLISH (championship classes 1+2 on real English).
**Branch:** `tnn-native-lab`, dir `docs/lab/wave12/championship/english/together/`.
Adapts `docs/lab/wave12/q2-combined-teach/prereg/PREREG_CC_TOGETHER.md`
(the toy shakedown prereg) to the English domain. Deltas are documented inline;
everything not mentioned is verbatim from the toy prereg.

## Amendments

**2026-09-21 (Micah's order — GLM sources FORGOTTEN):** carried over from the
toy prereg. The three Zhipu/GLM models stay HTTP 403; dropped permanently.

**2026-09-21 (hy3 OUT):** hy3:free hit 41 consecutive HTTP 503s and was blocked
at corpus-freeze time. The TOGETHER ENGLISH gate is therefore **5 corpora**,
not 6. Every "6" below (source count, 18 legs, 12 evidence legs, 6 distractors)
now reads **5 / 15 / 10 / 5**.

**2026-09-21/22 (English domain port):** the Zharovia toy geometry is replaced
by the frozen English geometry (see table). The §P wire format is byte-identical
to frozen §B.3; only the teacher-id registry gains two values.

## Question

Micah's 4-class design, classes 1+2, on real English: does teaching from ALL
five frozen English corpora at once beat single-source teaching, and does a TNN
taught that way teach as well as the direct route?

## The 5 corpora (all frozen as DATA before any TNN run)

| # | source | prefix | corpus path (on branch) | sha256 |
|---|--------|--------|-------------------------|--------|
| 0 | gpt-5.6-sol | `q2` | `docs/lab/wave12/championship/english/sol/corpus/corpus.json` | `41aa8f5b…19015d7` |
| 1 | grok-4.6 | `qg` | `docs/lab/wave12/championship/english/grok/corpus/corpus.json` | `7f3a2573…2bc2508` |
| 2 | step-3.7-flash | `qs` | `docs/lab/wave12/championship-english/step/corpus/corpus.json` | `c52e4f52…d2ea69ab` |
| 3 | swe-1-6-slow | `qw` | `docs/lab/wave12/championship/english/swe/corpus/corpus.json` | `ca1e7b85…12b92456b7f` |
| 4 | muse-native | `qn` | `docs/lab/wave12/championship/english/muse-native/corpus/corpus.json` | `1d5c2ede…1defa9c51e07` |

Gate: no TNN run starts until all 5 are recorded above AND byte-verified
against the branch. The generator (`build/gen_source_zag.py`) asserts each
corpus has 240 teach rows with the exact English Q2 teach keys and ids 0..239;
any corpus failing the assertion is a data defect, recorded, and the run does
not start. Full hashes: `evidence/DATA_MANIFEST.md`.

## English geometry (replaces the toy's 48/24/36/48/36/48)

| Category | Id range | Width | Content |
|----------|----------|-------|---------|
| 0 | 0–47 | 48 | alpha-position facts |
| 1 | 48–95 | 48 | word-length facts |
| 2 | 96–143 | 48 | publication-year facts |
| 3 | 144–239 | 96 | count facts |

Category boundaries: 48/96/144. A hard assertion (`cc_geometry_assert`,
`CC_GEOMETRY` log line, `cl_check cc_geometry_240`) proves before any teaching
that ids 0..239 appear exactly once across the four lanes; failure is terminal.
(The width-48 bug that silently untaught ids 192–239 in the first English port
is the reason this assertion exists.)

## CLASS 2 — one combined learner, 5-source English D2 teaching

Protocol: the D2 teaching protocol (eliminative verification + withholding +
learner-initiated disconnect), ported to the English domain.

**Multi-source agreement mechanism (existing, not invented):** `t5_verify`
over the combined evidence set. Per fact id the learner builds 15 legs —
5 sources × (observation leg + probe leg, tier 2) + 5 directive-distractor legs
which are presented but FILTERED (never evidence, per D2). `t5_verify` requires
ALL 10 observation/probe legs to agree on (fact, value). Agreement →
deliberate `t5_add`. ANY disagreement → the add is WITHHELD and the conflict
is AUDITED (`T5_OP_CONFLICT` entry + a `CCM` log line carrying all 10 leg
values). Withholding is terminal for that id (single pass).

**English D2 chain:** landmark = alpha-position fact id `l` (0..47);
`k = t5_truth(l)` (alpha-pos truth, 1..26); ruler = word-length fact id
`48+(k-1)`. `cc_lm_valid` enforces the chain (fact non-false, not held-out,
k in 1..26, ruler non-false and not held-out).

Curriculum: per-rep held-out sets, category passes, per-category disconnects,
disproof phase revising the 12 false ids with world-record evidence,
interference, delayed retention. 5 reps (0..4), scale 1; S10 no-degradation leg
(rep 0, scale 10); learned-arm trap battery per rep (7 families × 20).
Byte-identical reruns N=5.

Scoring: Q2's exact Track-5-weight formulas (30/25/25/10/10):
mastery=(d1/40+d2/d2n+d3/120)/3; revisability=min(rf/12,rg/20);
integrity=(Σtraps/20+(1−hallu/20)+k1+k2+refusal)/(n+4);
retention=min(1,r3/r2); cost=1/(1+esc_per_100ep+0.1·ops/eps).

## CLASS 1 — the combined learner as TNN teacher (teacher_id=60)

The class-2 learner instance used as teacher is the first rep (0..4) whose
held-out set is disjoint from the 192-fact teaching curriculum (deterministic
selection, printed in the log), so the teacher holds the full curriculum.
New registry values: `TB_TID_TOGETHER_EN=60` (the together-teacher for
class 1), `TB_TID_TOGETHER_EN_C2=61` (the class-2 learner's direct §B.7 probe
id). Documented deltas, same pattern as the class-3/4 tid=43/53 delta; wire
format unchanged; ingress + `last60`/`last61` seq counters added.

**Documented deviation:** evaluated on the frozen English geometry, no rep in
0..4 satisfies the disjoint-held-out rule (overlaps 9/11/9/9/12). The driver
scans reps 0..4, prints the scan (`TEACHER_REP_SCAN`), and falls back to rep 0
(the class-2 canonical rep), logged as `TEACHER_REP,0` after
`TEACHER_REP_FALLBACK,no_disjoint_rep_in_0_to_4`. This matches the toy
shakedown's documented resolution ("dropped as unnecessary").

Teacher leg: the Q1 teacher-leg pattern verbatim (Q1B driver): fresh arm-B
learner, empty at t0, 8-example scaffold verified by its own observation,
learner-initiated disconnect, 8 slices × (12 flaw-first + 24 clean) proposals
from the teacher (tid=60), §C tripwire, SEALED §B.7 flaw scoring (same 8
slices, same scorer, bar ≥10/12 per slice), knowledge-transfer numbers
(holds-curriculum, false-claims, clean adoptions, final mastery).

The class-1 student ALSO gets the Track-5-weight battery on its final store
(same formulas as class 2). Documented asymmetry: the Q1-pattern curriculum
contains no false-teach→disprove sequence, so the student's rev_false measures
non-acquisition of the 12 false claims rather than revision; the composite
uses rev_genuine/20 only ("genuine-only"), reported with this caveat, not
redefined.

## Class-2 learner's own §B.7 (tid=61)

The class-2 learner takes the §B.7 battery as the judging student (same 8
slices, same sealed scorer, bar ≥10/12), with the fresh direct-probe teacher
id 61. One documented delta vs the Q1B leg: the learner's store is non-empty,
so before each slice it runs a span-calibration pass — deliberate world
observation of the slice stimulus, each record verified against its own held
knowledge before its span is noted. Without this, clean proposals for
already-known facts would hit the `t5_add`-duplicate refusal path and read as
false positives; with it they correctly resolve as REJECT/R5 (redundant, not a
flaw accusation). The calibration is honest (observation verified against own
knowledge) and audited. No scaffold re-run (the learner already disconnected
in its build).

## Decision rules (evidence-decided, not asked)

- Combined-vs-single: decided by the class-2 composite vs Q2's D2 sol-only
  composite (0.9911, same formulas, same weights) + the conflict matrix.
- "Combined best?": the verdict is whatever the numbers say; per-slice §B.7
  (frozen instrument — expected 12/12 wherever the teacher genuinely holds
  the knowledge, per Q1B's caveat), knowledge-transfer numbers, and the
  coverage cost of withholding.
- Withholding cost: coverage = taught ids / 228 curriculum ids; every
  withheld id is named in the matrix.

## Standing rules

Pure Zag; no RNG in any TNN decision path; byte-identical reruns (N=5);
corpora frozen + committed before TNN runs; znc quirks ZNC-002..014 respected
(ZNC-013: `tb_sess_bump` flattened — 5-deep else-nesting miscompiles);
no binaries / `.zag-cache` / `.zagd` in commits.
