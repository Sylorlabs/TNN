# BYTEGEN — verdict

## Question
Is byte generation for TNN better done **autoregressively** (each chunk
conditioned on previously generated output) or **in parallel** (every sample a
pure function of the plan)?

## Answer
**Hybrid, PAR-default with bounded AR feedback.** Neither fork wins outright.

## Evidence
Built true autoregressive Fork AR and true parallel Fork PAR in pure Zag
(pinned toolchain `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), rendered
the same 30 s / 44.1 kHz / mono / 16-bit plan, proved byte-identical reruns.

| dimension | PAR (parallel) | AR (autoregressive) |
|---|---|---|
| 9-bar quality gate | 9/9 PASS | 9/9 PASS |
| CHOP-1/2 | PASS / PASS | PASS / PASS |
| CHOP-3 | 14 unexplained spikes (all ≤ 0.35 s of note boundaries; transients) | 0 spikes |
| determinism | byte-identical reruns; seq/rev/stride identical | byte-identical reruns |
| motif recurrence xcorr | **1.000000** | **0.741083** |
| RT-CASCADE (fault at 3 s) | 0/1.19M post-cut samples differ — immune | 5,791 differ (~131 ms), then bit-identical recovery |
| RT-LONG (wrong nominal pitch) | renders wrong 880 Hz | infers true 440 Hz from own output |
| RT-EDGE (cut at 15 s) | 0 discontinuities | 0 discontinuities |
| cost (30 s) | ~9.7 s, 13.0 MB | ~9.4 s, 13.1 MB |

## Why hybrid, why PAR-default
- PAR's strengths are structural (reproducibility, cascade immunity, exact
  recurrence) — they hold by construction, not by tuning.
- AR's one unique capability is real and has no parallel equivalent: it can
  discover facts from its own generated output (RT-LONG). But its feedback is
  currently unbounded, and unbounded feedback measurably degrades long-range
  coherence (1.0 → 0.74) and admits cascades.
- Therefore: the plan keeps the last word by default (PAR); output-feedback
  earns its place only where the task provably needs ears on the waveform
  (response dependencies, adaptive leveling), with authority bounded to
  designated parameters/regions.

## What would change this verdict
- Micah's ears on the excerpts (`excerpts/`): his hearing outranks all metrics
  on quality. If AR's motif drift is inaudible but its smoothness is audible
  (or vice versa), the weighting shifts.
- A sustained/adversarial fault that keeps AR derailed would harden the case
  for PAR-default; a demonstration of AR recovering from one would soften it.
- ZCR pitch inference failing on realistic (non-pure-tone) cues would shrink
  AR's claimed advantage to the servo's leveling behavior alone.

## Caveats (prereg execution defects — not hidden)
1. **Fixture**: the prereg said to reuse a frozen V10-era plan fixture. No
   such fixture exists in the V10 materials (searched `aud_v10/` and
   `imagination_discovery/`). `fixture/plan_v1.txt` was created new for this
   run. Calling it "frozen" does not cure the mismatch — disposition needed.
2. **Crews**: the prereg's mandated builder/test crews were not spawned (this
   session cannot create deeper children). Both forks were built directly by
   the single executing agent instead. No independent verification.
3. **Debate**: Sol was unreachable (provider returned empty completions twice);
   grok-4.6 served as the outside 2nd opinion per the rescinded model rule.
4. **Coherence metric**: the prereg references a "frozen metric in test
   harness" — no pre-existing bytegen harness was found; zero-lag normalized
   cross-correlation was used instead, documented in `tests/coherence.txt`.
5. Two implementation bugs were found and fixed mid-run (1000× amp scaling,
   unnormalized harmonic stack); final evidence is from the fixed binaries.
6. RT-CASCADE's original 64-sample multi-bit corruption was replaced by a
   single-bit fault model plus mix-level comparison (WAV-level comparison is
   invalid under global peak normalization — standing house rule).

## Follow-ups
- Micah listens to `excerpts/` (4 clips: motif × fork, recurrence × fork).
- Adversarial sustained fault vs AR's servo; multi-trap RT-LONG on complex audio.
- Bound the AR servo's authority (parameter/region-scoped feedback) and re-run
  coherence — the hybrid's actual design.
- Decide fixture disposition (bless plan_v1.txt as the frozen fixture or
  designate a real one and rerun).
