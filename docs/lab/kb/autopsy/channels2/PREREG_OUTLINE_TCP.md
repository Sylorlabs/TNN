# PREREG OUTLINE — KB4 next experiment: transform-consistency probe (C2)

Status: OUTLINE (not yet frozen). To freeze: fill the (T, L) table verbatim,
add the byte-blob manifest, commit BEFORE any test execution.

## Experiment

**Channel.** Transform-consistency probe (TCP): for each adversarial fixture,
apply a frozen deterministic task-covariant transform T to the raw stimulus
bytes (pure Zag), re-run the same frozen sense binary on T(stim), and emit
INSTALL iff J(T(stim)) == L(J(stim)) under the preregistered per-task law L;
else WITHHOLD.

**Frozen (T, L) table** (fill in byte-exact transform specs before freezing):

| task | bytes | T | L |
|---|---|---|---|
| t1 colordisc | .img | horizontal flip (row-mirror) | identity |
| t2 colorconst | .img | horizontal flip (row-mirror) | identity |
| t3 shapetrans | .img | horizontal flip (row-mirror) | identity |
| t4 pitchdisc | .pcm | time reversal (sample order) | HIGHER↔LOWER, SAME→SAME |
| t5 timbredisc | .pcm | time reversal (sample order) | identity (single 0.8 s tone) |
| t6 motiondir | .vid | frame-order reversal | N↔S, E↔W, NE↔SW, NW↔SE, STILL→STILL |

**Battery.** Frozen 93-calibration / 92-test adversarial split (same split as
the shootout). Both senses (a_raw, b_percept). Raw bytes from the frozen
`MANIFEST.sha256` (2020 entries); add a byte-blob input manifest (fixture
path → SHA256) to the frozen inputs. Zero RNG; pure Zag instrument; sense
binaries' SHAs frozen; temp fixtures preserve header format.

**Calibration validity gate (go/no-go, before test).** On the 93 calibration
PRIMARY stimuli: J(T(primary)) == L(J(primary)) on ≥ 95% of fixtures PER SENSE.
If a sense fails the gate, that sense's TCP results are VOID (transform breaks
the judge; channel invalid, not merely weak).

**Test scoring.** Run the locked instrument once on the 92 TEST adversarial
fixtures per sense. Same metric suite as the shootout: I(verdict; Y),
resolution accuracy, false-install rate, plus P(J(T(stim))==L(J(stim)) | Y=0).

## Kill bars (preregistered, decisive)

- **F1 — bits:** I(verdict; Y) ≤ 0.15 bits on TEST → KILL (adds nothing over
  the (a)+(c) champion).
- **F2 — systematic-error kill:** P(consistent | Y=0) ≥ 0.70 on TEST → KILL
  the channel AND retire the whole judgment-side family permanently: fooled
  judgments are transform-consistent, so the sense's boundary error is
  systematic, not noise-driven, and only stimulus re-measurement (C1 class)
  can repair it.
- **F3 — validity gate:** < 95% transform-consistency on calibration primaries
  for a sense → that sense's results VOID.
- **F4 — deployability:** false-install ≥ 0.15 on TEST → KILL (fails the
  ≤0.10 bar with margin).

## Branching consequences (decided in advance)

- F2 fires → abandon ALL judgment-side channels; all resources to C1-class
  (stimulus-analytic verification); record the retirement as law.
- C2 beats 0.15 bits with false-install < 0.15 → first deployable channel;
  scale the methodology to C1.
- F1 fires without F2 → transform probe adds nothing; C1 is the only
  remaining direction.
- There is no outcome in which nothing is learned.

## Discipline

Prereg frozen (outline + (T,L) table + byte-blob manifest + instrument SHA)
and committed BEFORE any test run. Calibration gate runs before test scoring.
Test truth never touched until scoring. 2× byte-identical reruns required.
Per-class rows reported alongside aggregates. If the threat model is ever
advanced to an adaptive adversary, that is a separate preregistered
red-team, not a reinterpretation of this one.
