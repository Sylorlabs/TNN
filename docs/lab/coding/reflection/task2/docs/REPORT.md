# Task 2 — Synth Coding Probe: Final Report

**Date:** 2026-09-22
**Branch:** `tnn-native-lab` (repo `sylorlabs/TNN`)
**Paths:** `coding/reflection/task2/`

## 1. Separation statement

The audio program has **BANNED synths as TNN's imagination paradigm** (Micah,
2026-09-22 — the synthesis paradigm itself is what his ears convict, not just
the hiss). This task is **only a coding-capability probe**: whether TNN can
write a correct synthesizer program. Outputs are judged solely by byte-exact
comparison to a frozen oracle. They are never played, never scored as audio,
and never evaluated for quality. **This task changes nothing about the audio
program's direction.** No synthesizer code from this probe is used by, or
feeds into, the audio line.

## 2. Oracle: independent and frozen

`oracle/oracle.py` implements the three frozen vectors directly from the
preregistered formulas using Python `math.sin`, `math.floor`, `struct.pack`:

| Vector | Description | Bytes | SHA-256 |
|---|---|---:|---|
| V1 | 440 Hz sine, 1 s, amp 0.5 | 88,244 | `2cd26846…e39e907` |
| V2 | 880 Hz sine + ADSR, 0.5 s, amp 0.8 | 44,144 | `a77253e2…09f66` |
| V3 | 440 Hz @0.5 + 660 Hz @0.3 mix, clamped, 0.5 s | 44,144 | `7b5ee936…432a6b2` |

(Full hashes in `oracle/FREEZE.txt`.) The oracle shares no code path with the
Zag learner: it was written directly from the frozen formulas before either
arm's first generation. Standard 44-byte RIFF header, mono 16-bit PCM, 44.1 kHz.

## 3. Corpus and store controls

**Prior-art corpus** (`store/corpus/`, frozen 2026-09-22, manifest with
SHA-256 per entry): six entries of general human synthesizer knowledge —
SYN-FLOAT (exact f64 floor), SYN-OSC (sine oscillator: split-2π range
reduction + Taylor recurrence), SYN-ENV (ADSR piecewise-linear), SYN-MIX
(sample-domain clamp), SYN-STRUCT (program organization), SYN-NOTE (vector →
samples rendering). The corpus contains **no vector parameters, no sample
values, no WAV bytes, and no complete solutions** to V1/V2/V3.

**Coding baseline** (`store/installed_scratch.csv`): the 69 Phase-1 coding
entries (install digest `a92e1031d460dbd9`) plus E-WAVHDR (44-byte RIFF/WAV
header + raw-syscall file writing — file-format knowledge, not synth
knowledge). Frozen digest (SHA-256 of the installed-set CSV):

- coding-knowledge-only: `ef6d81ae72d93e8973329336201c227541f2e8755a823ab0d4a9664bc843089c`

**Teach ceremony** (`driver/setup_stores.py`): each corpus entry installed via
`learner corpus-teach <id> <digest>`, which validates the digest against the
frozen manifest hardcoded in the learner and prints an `AUDIT
op=CORPUS_INSTALL` line (installed=1 only on digest match; digest-mismatch
and unknown-id are refused). All six installed; audit lines in
`store/audit.log`. Informed installed-set digest:
`5b821fee9edd4cd53f306eb76a3eee138583c6600bfcd7007687dd03badf668e`.

**Scratch control:** the scratch store digest was re-verified after the teach
ceremony and **exactly equals the coding-knowledge-only digest** above. No
drift; the comparison is valid.

**Same for both arms:** one learner binary (`work/learner`, built from
`learner.zag` with the pinned `znc_linux_x86_64_abed8aa1`), one driver
(`driver/driver.py`), one spec, one budget (6 iterations), one oracle.

## 4. Numerical foundation (pre-trial verification)

The informed fragment's sine was verified **before the trial** by a bit-exact
Python simulation of the exact Zag operations (`oracle/analyze2.py`):

- 110,250 pre-floor samples across all three vectors: **0 floor mismatches**
  vs the oracle.
- Max |sim − oracle| = 1.64e-11; nearest non-zero oracle value to an integer
  boundary = 9.63e-11 → **6× safety margin**.
- znc f64 confirmed bit-identical to IEEE-754 doubles via a probe binary
  (`src/probe_f64.zag`): `0.1+0.2`, `1.0/3.0`, literal parsing, `as i64`
  truncation, and the sine fragment all match the Python simulation exactly.

Two znc constraints shaped the fragment (both documented): float literals
≥ 2^32 are rejected (Taylor factorials rewritten as a recurrence with small
divisors; the 2π low part written as `3.968374318722162/1000000000.0`), and
the 2π split constant must be derived from the **exact** binary value of the
high part (an early decimal-repr slip cost 1.6e-16 and was caught by the
simulation before freezing).

## 5. Per-arm results (5 reps each, budget 6)

| Arm | Rep | First-attempt pass | Iters to byte-exact | Final | Outcome |
|---|---|---|---|---|---|
| INFORMED | 1 | yes | 1 | pass | pass |
| INFORMED | 2 | yes | 1 | pass | pass |
| INFORMED | 3 | yes | 1 | pass | pass |
| INFORMED | 4 | yes | 1 | pass | pass |
| INFORMED | 5 | yes | 1 | pass | pass |
| FROM-SCRATCH | 1 | no | 7 (never) | fail | halt-sine-limit (iter 3) |
| FROM-SCRATCH | 2 | no | 7 (never) | fail | halt-sine-limit (iter 3) |
| FROM-SCRATCH | 3 | no | 7 (never) | fail | halt-sine-limit (iter 3) |
| FROM-SCRATCH | 4 | no | 7 (never) | fail | halt-sine-limit (iter 3) |
| FROM-SCRATCH | 5 | no | 7 (never) | fail | halt-sine-limit (iter 3) |

Determinism: all 5 informed reps byte-identical (canonical digest
`5d3b2f62acef1423`); all 5 scratch reps byte-identical (canonical digest
`8fb803e552850173`). Zero RNG in any decision path; byte-identical reruns
confirmed.

## 6. Vector-by-vector evidence

**INFORMED** — all three vectors byte-exact on iteration 1, every rep. Emitted
WAV SHA-256s equal the frozen oracle hashes (V1 `2cd26846…`, V2 `a77253e2…`,
V3 `7b5ee936…`).

**FROM-SCRATCH** — the learner improvises a sine (no SYN-OSC installed) and
genuinely repairs it. Sample-mismatch counts (of 44,100 / 22,050 / 22,050):

| Iteration | Sine | V1 | V2 | V3 | Learner decision |
|---|---|---|---|---|---|
| 1 | V1 naive (while-loop reduction, 10 Taylor terms) | 5 | 2 | 25 | SYNTH_SAMPLE → repair-sine-v2 |
| 2 | V2 floor-based reduction, 10 terms | 0 | 0 | 3 | SYNTH_SAMPLE → repair-sine-v3 |
| 3 | V3 floor-based reduction, 14 terms | 0 | 0 | 3 | SYNTH_SAMPLE → **halt-sine-limit** |

The ladder is real progress (25 → 3 mismatches on V3), but the last 3 V3
samples cannot be fixed without the split-2π reduction prior art: at 660 Hz
the phases reach ~2073 rad, where single-constant reduction loses the low
bits. The learner correctly concludes it cannot improve further and halts
itself rather than thrashing. Honest arm failure, within budget.

## 7. Arm gap

| Metric | INFORMED | FROM-SCRATCH |
|---|---|---|
| First-attempt pass rate | 5/5 (100%) | 0/5 (0%) |
| Iterations to byte-exact | 1 | 7 (never; self-halted at 3) |
| Final pass rate | 5/5 (100%) | 0/5 (0%) |
| Deterministic across 5 reps | yes | yes |

**Reading:** with the oscillator prior art installed, TNN writes a byte-exact
synth on the first attempt, five times out of five. Without it, TNN writes a
working synth (correct structure, ADSR, mixer, WAV container — all derived
from the spec and coding knowledge), invents and repairs a sine through two
genuine improvement steps, but cannot reach bit-exactness: the numerical
method (split range reduction) is the piece that has to be taught, not
derived, within this budget. The gap is stark and entirely attributable to
the prior art.

## 8. Driver leak audit

The driver (`driver/driver.py`) was audited for decision leakage:

- It never classifies failures (no pattern matching on bytes, no thresholds
  beyond byte equality).
- Evidence handed to the learner is facts only: vector index, file lengths,
  header match/diff, first-differing byte offset, and decoded i16 sample
  pairs around the divergence. Decoding LE bytes to i16 is presentation, not
  diagnosis — the learner decides what the numbers mean.
- No repair strategies, no sine knowledge, no constants in the driver. The
  sine ladder (V1→V2→V3→halt) lives entirely in `learner.zag`
  (`diagnose_synth`); the driver only routes the learner's revised source.
- Sentinel routing (`UNTAUGHT:`/`REFUSED:`) is protocol plumbing, identical
  to the main loop driver.
- The 6-iteration budget, stall guard, and cycle guard are enforced by the
  driver as harness rules, not coding decisions.

**Verdict: no driver decision leak.** Every coding decision (fragment recall
vs improvisation, sine repair ladder, halt) is in the Zag learner.

## 9. Known limitations and honest failures

1. **FROM-SCRATCH fails** — reported as an arm failure per the prereg
   (`halt-sine-limit`, 3 iterations, 0/5 final pass). This is the measured
   gap, not a harness defect.
2. **Diagnose scope:** the synth diagnoser only repairs the improvised sine;
   structural failures (length/header/compile) halt. This was sufficient —
   no structural failure occurred in 10 reps.
3. **Corpus size:** six entries; the differentiator is effectively SYN-OSC.
   SYN-STRUCT/SYN-NOTE document structure the composer applies in both arms.
4. **The informed sine's safety margin is 6×**, verified by simulation, not
   by proof. A future vector with samples nearer an integer boundary would
   need re-verification.
5. **No audio was produced for listening** in this probe beyond the
   byte-comparison artifacts, which were never played or scored.

## Artifacts

- `oracle/oracle.py`, `oracle/FREEZE.txt`, `oracle/oracle_v*.wav` (frozen)
- `oracle/analyze.py`, `oracle/analyze2.py` (numerical verification)
- `store/corpus/` (6 frozen entries + `MANIFEST.md`)
- `store/coding/E-WAVHDR.zag`, `store/installed_*.csv`, `store/audit.log`
- `learner.zag` → `work/learner` (the one binary used by both arms)
- `driver/driver.py`, `driver/setup_stores.py`, `driver/spec.txt`
- `src/probe_f64.zag` (f64 semantics probe)
- `work/rep{1..5}_{informed,scratch}.json` + per-rep workdirs (full traces)
- `docs/REPORT.md` (this file)
