# VERDICT R2-10 — Witness-emission PAM (B-HC-2)

**Verdict: DEAD — killed by B5 (KB4 false permanent installs).**
**Date:** 2026-09-23. **Analyst:** replacement checkpoint (resumed after daemon kill).

## Headline

R2-10 dies on the same bar that killed all six round-1 forks: adversarial
false installs. B5 measured **12.31% (1344/10915)** against the ≤3% bar, at the
frozen initial gate (THETA=700, VETO=0). A comprehensive feasibility analysis
proves B5 is **unreachable** for this build: no threshold/veto gate on the
available signals can reach ≤3% — the best non-degenerate gate achieves 5.05%,
and the only "passes" install nothing (bar-gaming, refused by the
constitutional veto). The false installs come from adversarial families that
confidently fool the front-ends with no available veto signal:

| Family (inferred) | False installs (conf≥700) | Veto signal? |
|---|---|---|
| pitchdisc harmonic-distractor (confident wrong f0) | 495 | none |
| motiondir spurious-correlation (opposite direction) | 458 | none |
| colorconst metamer-ish | 129 | none |
| pitchdisc glide-through-threshold | 119 | feat1=glide (exists) |
| colordisc | 97 | none |
| timbredisc | 46 | none |

Even a perfect glide veto leaves 1225 false installs (11.2%). Per the task
protocol, B5 failure marks DEAD without allowing human verdicts to rescue it —
and the feasibility proof shows human verdicts *could not* rescue it anyway
(B5 is truth-oracle; the gate discipline is human-oracle).

## Mechanical bars

| Bar | Result | Detail |
|---|---|---|
| B1 viability (370 harness) | **PASS** | 325/370 = 87.84% (≥60%) |
| B2 vs Approach A | +15.2pp | 87.84% vs 72.6% on identical 370 |
| B3 efficiency | measured | mean ops: colordisc 8704, colorconst 24576, shapetrans ~48k, pitchdisc 246600, timbredisc 102400, motiondir 22528 |
| B4 no-interference (HARD KILL) | **PASS** | 10,915 trials: percepts+dispositions byte-identical emit vs noemit (0 diffs) |
| B5 KB4 false installs (HARD) | **FAIL → DEAD** | 12.31% (1344/10915); ≤3% required; proven unreachable |
| B6 determinism (HARD KILL) | **PASS** | 3 full no-emission reruns byte-identical (10,915 trials each) |
| KB-E1 emission payload identity | **PASS** | artifact digests match; payloads byte-identical to source regions (video frames exact; image crop pixels exact) |
| KB-E2 non-empty owned selections | **PASS** | mapping_ok 10915/10915 |
| KB-E5/EC1 hash-chained ledger | **PASS** | all 6 chains independently re-verified; endpoints recorded |
| KB-E6 human agreement | NOT MEASURED | fork dead on B5 before gate discipline; no human verdicts sought |

Overall accuracy: 76.01% (8297/10915); adversarial 64.37%, normal 89.29%.

## What was inherited vs built

**Inherited** (previous crew, kept): the six front-end estimators, the
witness-emission architecture, the install-gate design, frozen train/eval
manifests (200+200, disjoint, SHA-verified), the fixture set.

**Built/repaired by this checkpoint:**
1. **Timbre front-end repaired** (genuine bug): inherited code had an i64
   overflow (`hh*1000*P/tot`) plus a systematically biased quadrant estimator.
   Ported R2-9's exact-bin f64 Goertzel estimator. timbredisc: 24.96% → 88.94%
   accuracy; B1 timbre 45/60 → 60/60.
2. **Video witness emission repaired** (genuine bug): code cited two frames
   but emitted only frame 0. Now emits frames 0+1 side-by-side.
3. **`mode_revise` repaired** (was non-functional): fixed table/arena offset
   bugs, task-name parsing, PENDING-row exclusion.
4. **Constitutional veto implemented and observed firing**: 58/76 grid
   candidates refused for degrading installs-on-witnessed-correct (including
   the bar-gaming veto-everything candidates). R2-12 white-box criterion met.
5. **B5 feasibility proof**: the current gate parameterization cannot reach
   B5; documented above.
6. **Human-package generator** (`make_human_package.py`): builds blinded
   train/eval packages (media conversion, waveform consistency gate,
   double-blind shuffle, index.html + verdict sheets). **Not run** — mechanical
   bars failed first, per protocol.

## Gate discipline status

The gate was NOT disciplined (no human verdicts; fork dead). The `revise`
machinery is repaired, tested, and ready: with truth-as-oracle on the 200
training trials, the frozen gate scores 20 false / 68 correct installs, and
no allowed candidate improves on it (best: theta=675, veto=0, identical).
The constitutional veto fired 58 times, refusing all bar-gaming candidates.

## Human package status

Generator ready (`make_human_package.py`, `make_revise_input.py`).
**Not executed** — per protocol, mechanical bars come first and B5 failed.
No artifacts were produced for human judgment; nothing was sent to Micah.

## Commit

[Pending — files to be committed via commit_racefree.py after B4 completes.]

## Why it died (for the record)

R2-10's hypothesis was that a percept is only as good as the evidence it can
point to. The emission machinery works (KB-E1/E2/E5 pass; B6 passes). What
kills it is the same memory-contract disease as round 1: the front-ends are
confidently fooled by adversarial stimuli (harmonic distractors, spurious
motion correlations), and confidence — the gate's only signal — is
anti-correlated with correctness on exactly those trials. The gate cannot
distinguish "confident and right" from "confident and fooled" because the
front-ends provide no fool-detection signal. This is an architecture
limitation, not a calibration issue: no threshold or veto on the available
signals can fix it.
