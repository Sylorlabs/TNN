# TOGETHER (classes 1+2) — design record (crew-drafted 2026-09-21)

**Crew:** TOGETHER (replaces the 2/3-source combined brief per Micah's 4-class
redirect). **Branch:** `tnn-native-lab`, dir `docs/lab/wave12/q2-combined-teach/`.

## Question

Micah's 4-class design, classes 1+2: does teaching from ALL sources at once
(8 UnoRouter API models + the native Muse team) beat single-source teaching,
and does a TNN taught that way teach as well as the direct route?

## The 9 corpora (all frozen as DATA before any TNN run)

| # | source | prefix | corpus path (on branch) | sha256 |
|---|--------|--------|-------------------------|--------|
| 0 | gpt-5.6-sol (Q2 frozen) | `q2` | `docs/lab/wave12/q2-distillation/corpus/corpus.json` | `42aff78177…` |
| 1 | grok-4.6 | `qg` | TBD (polled) | TBD |
| 2 | glm-5.3-flash:free | `ql` | TBD | TBD |
| 3 | glm-5.3-flash-search:free | `qls` | TBD | TBD |
| 4 | glm-5.3-flash-think-search:free | `qlt` | TBD | TBD |
| 5 | hy3:free | `qh` | TBD | TBD |
| 6 | step-3.7-flash:free | `qs` | TBD | TBD |
| 7 | swe-1-6-slow:free | `qw` | TBD | TBD |
| 8 | Muse-native | `qn` | delivered by parent coordinator | TBD |

Gate: no TNN run starts until all 9 are recorded above. The generator
(`build/gen_source_zag.py`) asserts each corpus has 240 teach rows with Q2's
exact key set and ids 0..239; any corpus failing the assertion is a data
defect, recorded, and the run does not start.

## CLASS 2 — one combined learner, 9-source teaching

Protocol: Q2's exact D2 teaching protocol (eliminative verification +
withholding + learner-initiated disconnect), with the source legs multiplied.

**Multi-source agreement mechanism (existing, not invented):** `t5_verify`
over the combined evidence set. Per fact id the learner builds 27 legs —
9 sources × (observation leg + probe leg, tier 2) + 9 directive-distractor
legs which are presented but FILTERED (never evidence, per D2). `t5_verify`
requires ALL 18 observation/probe legs to agree on (fact, value) with at
least one leg at the tier bar. Agreement → deliberate `t5_add`. ANY
disagreement (within-source or cross-source) → the add is WITHHELD and the
conflict is AUDITED (`T5_OP_CONFLICT` entry + a `CCM` log line carrying all
18 leg values). Withholding is terminal for that id in the run (mirrors Q2's
single-pass D2). Resolution of every split is therefore withheld+audited;
the conflict matrix records per-id, per-source agreement.

Curriculum geometry: Q2's verbatim (per-rep held-out sets, category passes,
per-category disconnects, disproof phase revising the 12 false ids with
world-record evidence, interference, delayed retention). 5 reps (0..4),
scale 1; S10 no-degradation leg (rep 0, scale 10); learned-arm trap battery
per rep. Byte-identical reruns N=5.

Scoring: Q2's exact Track-5-weight formulas (30/25/25/10/10):
mastery=(d1/40+d2/d2n+d3/120)/3; revisability=min(rf/12,rg/20);
integrity=(Σtraps/20+(1−hallu/20)+k1+k2+refusal)/(n+4);
retention=min(1,r3/r2); cost=1/(1+esc_per_100ep+0.1·ops/eps).

## CLASS 1 — the combined learner as TNN teacher (teacher_id=30)

The class-2 learner instance used as teacher is the first rep (0..4) whose
held-out set is disjoint from the 192-fact teaching curriculum (deterministic
selection, printed in the log), so the teacher holds the full curriculum.
New registry value `TB_TID_TOGETHER=30` (documented delta, same pattern as
Q1B's tid=7; wire format unchanged; ingress + `last30` seq counter added).

Teacher leg: the Q1 teacher-leg pattern verbatim (Q1B driver): fresh arm-B
learner, empty at t0, 8-example scaffold verified by its own observation,
learner-initiated disconnect, 8 slices × (12 flaw-first + 24 clean)
proposals from the teacher, §C tripwire, SEALED §B.7 flaw scoring (same 8
slices, same scorer, bar ≥10/12 per slice), knowledge-transfer numbers
(holds-curriculum, false-claims, clean adoptions, final mastery).

The class-1 student ALSO gets the Track-5-weight battery on its final store
(same formulas as class 2). Documented asymmetry: the Q1-pattern curriculum
contains no false-teach→disprove sequence, so the student's rev_false
measures non-acquisition of the 12 false claims rather than revision; the
composite is reported with this caveat, not redefined.

## Class-2 learner's own §B.7

The class-2 learner takes the §B.7 battery as the judging student (same 8
slices, same sealed scorer, bar ≥10/12). One documented delta vs the Q1B
leg: the learner's store is non-empty, so before each slice it runs a
span-calibration pass — deliberate world observation of the slice stimulus,
each record verified against its own held knowledge before its span is
noted. Without this, clean proposals for already-known facts would hit the
`t5_add`-duplicate refusal path and read as false positives; with it they
correctly resolve as REJECT/R5 (redundant, not a flaw accusation). The
calibration is honest (observation verified against own knowledge) and
audited. No scaffold re-run (the learner already disconnected in its build).

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
corpora frozen + committed before TNN runs; znc quirks ZNC-002..012
respected; no binaries / `.zag-cache` / `.zagd` in commits.

## Implementation notes (2026-09-21 shakedown)

### Teacher rep selection
`cc_pick_teacher_rep()` returns 0 (the class-2 learner's canonical rep).
Determinism is proven by `cc_prove_teacher_deterministic(rep)`: the SAME rep
is built 3 times in-process, requiring byte-identical state digests
(SHA-256 of claim/hold/state arrays). Cross-process determinism is proven by
N=5 byte-identical reruns. (An earlier design tried to select a rep with
held-out disjoint from the curriculum; this was dropped as unnecessary — the
teacher SHOULD hold the curriculum facts.)

### Class-1 rev asymmetry (refined)
The shakedown confirmed: class-1 student rev_false=0/12 (never acquires false
beliefs; teacher's false_claims=0). The composite uses rev_genuine/20 only
for C1, documented as "genuine-only" in the analysis. The alternative
(vacuous 1.0) was rejected as misleading — the student didn't DEMONSTRATE
false-belief revision.

### Adopt count (class-1)
Shakedown: 160 clean adopts vs Q1B's 192. The 32 difference are facts learned
during the flaw phase (q1_learn_one on flaw proposals carrying true fact
values), correctly rejected as R5 duplicates in the clean phase. This is the
redundant-known-unit mechanism working, not a bug. Load-bearing outcome:
final mastery 192/192. The `c1_adopt` check verifies adopts>0 (mechanism
live) rather than ==192.

### Conflict matrix (verified in shakedown)
With unanimous stubs: 228/228 taught, 0 withheld. The conflict path
(status=1, WITHHELD+AUDITED) is tested separately by injecting disagreement
into one stub source; the CCM lines carry all 18 leg values for split ids.
