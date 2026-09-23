# SENSES REBUILD — Verdict 2026-09-21

Crew lead adjudication against the frozen prereg
(`PREREG.md`, kill bars KB1–KB5). All numbers below were recomputed by the
crew lead from `harness/results/metrics.json` — they match the harness
assembly exactly.

## Headline

**Approach A (LLM-style raw values) wins the head-to-head. Approach B
(human-style qualitative percepts) is KILLED as a viable sense per KB1.
BUT Approach A is not cleared for memory integration: both approaches
catastrophically fail KB4.** The most important finding of this trial is
not who won — it is that the shared deliberate-memory install rule cannot
stop confident wrong percepts.

## Per-bar verdicts

| Bar | A (raw values) | B (percepts) | Verdict |
|---|---|---|---|
| KB1 viability (mean ≥ 60%) | **72.6% PASS** | **54.0% FAIL** | **B KILLED** |
| KB2 head-to-head | winner (\|Δ\|=18.6pp, ops 2.42×) | loses | **A WINS**, no tie |
| KB3 fragility (adv drop > 25pp) | 20.9pp drop — not fragile | 8.3pp drop — not fragile | clean victory claim allowed |
| KB4 memory integration (adv false-install ≤ 10%) | **59.0% (79/134) FAIL** | **55.0% (72/131) FAIL** | **both FAIL** |
| KB5 determinism | 60/60 byte-identical PASS | 60/60 byte-identical PASS | both PASS |

## Per-task accuracy (primary fixtures)

| Task | A | B | Δ (A−B) |
|---|---|---|---|
| colordisc | 48.3% | 40.0% | +8.3 |
| colorconst | 87.5% | 62.5% | +25.0 |
| shapetrans | 100% | 40.0% | +60.0 |
| pitchdisc | 83.3% | 78.3% | +5.0 |
| timbredisc | 75.0% | 75.0% | 0.0 (tie) |
| motiondir | 41.7% | 28.3% | +13.3 |
| **mean** | **72.6%** | **54.0%** | **+18.6** |

A beats B on 5 of 6 tasks; B's only non-loss is the timbre tie.
B is 2.42× cheaper in ops (428M vs 1.03B, dominated by A's audio
sample-visits) — cost does not overcome KB1.

## Kill decisions (frozen bars applied mechanically)

1. **APPROACH B — KILLED as a viable sense (KB1).** 54.0% < 60%. The
   percept-vocabulary design as built does not clear the viability bar.
   Recorded bright spots: timbre tie at 75/75, 2.42× lower ops, smallest
   adversarial degradation (8.3pp). A future B2 with redesigned
   vocabularies may be re-tested; this build is dead.
2. **APPROACH A — WINS the head-to-head (KB2), not fragile (KB3), but
   FAILS the memory-integration bar (KB4).** A may proceed as the sense
   architecture ONLY behind a stronger install gate than the one tested.
   It is not cleared for direct wiring into deliberate memory.

## The KB4 finding (both approaches fail)

The shared rule — install iff no contradictory installed belief with
confidence ≥ exists, else withhold+audit — withholds a lot (A 560, B 440
withholds) but cannot stop HIGH-CONFIDENCE wrong judgments: A installed
79 false beliefs out of 134 adversarial installs (59%), B 72/131 (55%).
Both senses emit overconfident wrong judgments on adversarial fixtures
(trick lighting, distractor harmonics, camouflaged motion), and the rule
has no defense against confident error.

This is direct experimental evidence for the program's standing
"truthful but sensor-deceivable" qualifier, and a design consequence for
the web-search sense now being built: untrusted observations need
confidence calibration and/or corroboration requirements before install,
not just contradiction checks. Recommended follow-up (not decided here):
test a corroboration-gated install rule head-to-head against this one.

## Honest caveats

- **colordisc is near/below chance for both** (A 48.3%, B 40.0% on a
  binary task). The ΔE2000 2.3-JND truth boundary is genuinely at the
  limit of fine discrimination — but neither sense resolves fine color
  differences, and the bar is absolute, applied equally.
- **A's shapetrans collapses on adversarial fixtures** (100% → 31.8%);
  A's pitchdisc likewise (83.3% → 33.3%). A's victory rests on primary
  fixtures; its adversarial accuracy (51.7%) is only 6pp above B's.
- **One runner error**: A's binary exited 1 (`task_failed`) on
  `t3_shapetrans/adversarial/p042.img` (valid fixture, truth=TRIANGLE);
  recorded, A's shape-adv n=44.
- **motiondir is weak for both** (A 41.7%, B 28.3% on a 9-way task where
  chance is 11%) — neither approach sees motion well yet.
- **B's timbre thresholds** were calibrated on four canonical 440 Hz
  syntheses (documented in B's BUILD_LOG); different harmonic recipes may
  shift margins.
- Fixture-pair conventions (halves of image/PCM; border=inset for
  colorconst) were assumed by B, not fully pinned in INTERFACE.md —
  documented in B's PERCEPT_DESIGN.md. A re-run with fully pinned
  conventions could move B's numbers slightly; it cannot move them 6pp
  to the KB1 bar without a redesign, so the kill stands.
- Fixtures are not stored in this commit (1850 files, 42MB); they are
  byte-regenerable from `harness/gen.py` (fixed master seed 20260921)
  plus the photo URLs in `harness/FIXTURE_SOURCES.md`.
  `harness/fixtures/MANIFEST.sha256` records every fixture hash so
  regeneration can be verified. End-to-end regeneration was not
  re-verified in this run.

## Evidence

- `PREREG.md`, `INTERFACE.md` (frozen before building)
- `a_raw/sense.zag`, `a_raw/BUILD_LOG.md` (A: 19/19 smoke, 6/6 determinism)
- `b_percept/transducer.zag`, `b_percept/percept.zag`, `b_percept/sense.zag`,
  `b_percept/PERCEPT_DESIGN.md`, `b_percept/BUILD_LOG.md` (B: percept.zag
  compiles standalone with zero imports — boundary verified; 18/18 smoke)
- `harness/gen.py`, `run.py`, `score.py`, `assemble.py`,
  `harness/FIXTURE_SOURCES.md`, `harness/RESULTS.md`,
  `harness/results/raw_results.json`, `harness/results/metrics.json`
- 925 fixtures + 925 truth files generated (170 real photographs;
  remainder physically-realistic procedural); deterministic splitmix64
  noise, master seed 20260921; ground truth independently re-verified
  per batch (two generator bugs caught and fixed by verification)
- Binaries excluded from the commit per lab convention (reproducible
  from sources with the pinned znc)
