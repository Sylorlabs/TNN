# FORK 6 (psola_voice) — KILLED (2026-09-24)

## Verdict: KILL — source not validated as laughter; pitch marks incorrect.

## Source analysis (laugh_src.bin, 17.70–19.30s)
- 70,560 samples (1.6s), max amplitude 1750 (very quiet).
- frac_static: 0.99 (extremely static).
- periodicity: 0.83 (has periodic structure).
- prosody: 0.0% (PERFECTLY static pitch — unnatural for laughter).
- HNR: 7.04 dB.

## Pitch marks (laugh_src.marks)
- 1,573 marks in 1.6s.
- Mean interval: 44.7 samples = 1.01 ms = 990 Hz.
- A child's laugh has F0 300–600 Hz (1.7–3.3ms intervals).
- 990 Hz is NOT a plausible glottal pulse rate.
- The marks are tracking a harmonic or noise, not the F0.

## Conclusion
The 17.70–19.30s interval is NOT validated as laughter. The
algorithmic selection (modulation spectrum) found a periodic
signal, but:
1. Prosody 0.0% is unnatural (real laughter has pitch variation).
2. Pitch marks at 990 Hz are incorrect.
3. No human confirmed it's laughter.

Per the task: "Validate rigorously, find a real laughing source,
or kill psola_voice honestly." The source fails validation. Without
a genuine laughing recording, PSOLA resynthesis cannot proceed.

## Per the task rules
Cannot ship a clip labeled "child laughing" without a validated
laughing source. Fork 6 is KILLED. No clip shipped.

## Artifacts (for the record)
- `laugh_src.bin`, `laugh_src.marks` (unvalidated source).
- Analysis showing why it was rejected.
