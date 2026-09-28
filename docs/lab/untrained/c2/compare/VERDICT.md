# VERDICT — Workstream B confirmatory run (c2), 2026-09-26

## Bar

A binding confirmatory run must show: human seal -> TNN output -> claim-level
comparison, all hallucinations, the honest boundary, origin-verified commit,
and a self-contained gallery. The bar FAILS on any hallucination (false
positives are worse than withholding).

## Protocol integrity

- c2 analyzer frozen BEFORE any fresh input was acquired.
  Source SHA-256: `826ff00344c8d83df1d327c6474190df62eb50a4c6d8986adcf8914b371310b5`
  (frozen copy byte-identical). Binary SHA-256:
  `d4ed41c4fba7336f8474a8ee4f31d9bf4e11e9e52e145177b47437baeeba8420`.
- Human descriptions sealed 2026-09-26 18:29:57 UTC (`human/SEAL.log`),
  BEFORE the first analyzer run on confirmatory inputs.
- Six fresh inputs (different tracks/images/video from the exploratory set).
  Novelty: each original's Git blob ID (`git hash-object`) checked against
  the repo object store — all six 404 (novel). `SOURCES.md` carries the full
  provenance.
- Every input run TWICE with the frozen binary: all six byte-identical.
- Pure Zag, zero RNG, deterministic. No analytical bridge.

## Result

**23 MATCH / 8 MISS / 4 WEAK MISS / 3 PARTIAL / 6 HALLUCINATION.**
**The bar FAILS: 6 hallucinations.**

## The six hallucinations

| # | Input | False claim | Mechanism |
|---|-------|-------------|-----------|
| 1 | B1 surf | "RHYTHM 0.100 s cycle" (true: ~5 s swells) | Envelope-autocorr lag-2 artifact (same as exploratory H1/H2) |
| 2 | B1 surf | "LAYERS transients over noise-like bed" (true: single AM process) | Phantom transient layer (same as exploratory H3) |
| 3 | B2 hoot owl | "RHYTHM 0.100 s cycle" (true: irregular phrases) | Lag-2 artifact again |
| 4 | B2 hoot owl | "LAYERS transients over noise-like bed" (true: single tonal process, quiet gaps) | "Noise-like bed" false; hoots mischaracterized |
| 5 | B3 helicopter | "ONSETS 15 distinct transient events" (true: no discrete events) | Continuous AM shredded into transients |
| 6 | B4 forest | "TEXTURE mostly smooth, little fine detail" (true: bark/grass detail) | 80x45-downscale averaging (same as exploratory H4/H5) |

## What this means

The hallucinations are SYSTEMATIC and REPRODUCIBLE, not one-off noise.
Three false-positive mechanisms survived from the exploratory run onto
completely fresh inputs:

1. **The 0.1 s rhythm artifact** (H1, H3): the envelope autocorrelator's
   lag-2 peak fires on any sustained amplitude-modulated signal. It claimed
   0.100 s on surf (true ~5 s) and on owl hoots (true: irregular phrases).
   It did NOT fire on the helicopter (which reported 0.140 s, plausibly the
   real blade-pass AM) — so the artifact is input-dependent, not constant.

2. **Phantom transient layers** (H2, H4, H5): slow AM (surf swells, owl
   phrase envelopes) and continuous AM (helicopter chop) get shredded by the
   onset detector into "distinct transient events," which the sentence
   emitter then promotes to a separate layer "over a noise-like bed."
   The human ground truth in all three cases is ONE process with amplitude
   modulation, not two layers.

3. **False "smooth" texture** (H6): judging texture at 80x45 averages fine
   detail away. It fired on the misty forest (which has real bark/grass
   detail) but correctly WITHHELD on the dunes (texture_frac 0.433) — so
   the gate exists but its threshold still admits false smooths.

## Honest boundary (what the analyzer genuinely cannot do)

- Pitch above 4 kHz is invisible (B3's 5 kHz turbine whine missed; documented
  in `tests/boundary_report.txt`).
- Fine texture below the 80x45 judgment scale is unreliable (B4).
- Slow rhythms (>0.5 s period) are never reported; the rhythm detector only
  covers 0.1-0.5 s, so true ~5 s wave swells (B1) cannot be captured — and
  the lag-2 artifact fills the gap with a fabricated 0.1 s.
- Onset counts shred slow AM into spurious transients (B1: 57, B2: 64,
  B3: 15 where the human counts 12-15 swells / 5 phrases / 0 events).
- Diagonal dominance is missed when axis-aligned edges win the vote
  (B5's S-ridge reported "horizontal").
- Tonality can be missed even when strong (B2's owl harmonics: the analyzer
  withheld pitch and called it "noise-like").

## What matched (genuine capability)

Duration (6/6), dynamics/large-swings (3/3 audio), broadband-vs-tonal
spectrum shape (B1, B2-partial, B3-low), vertical edges (B4), vivid-vs-muted
color (B4, B5), top/bottom layout split (B4, B5), no-cuts (B6), static camera
(B6-partial). The analyzer reliably reports gross duration, gross dynamics,
gross spectral tilt, dominant axis-aligned edge orientation, saturation, and
coarse layout. It does not reliably report rhythm, layering, texture, or
tonality.

## Verdict

**FAIL.** Six hallucinations on fresh inputs, from three reproducible
false-positive mechanisms. The exploratory run's verdict is confirmed in
kind (hallucinations are real and systematic) but the exploratory evidence
itself remains invalid for the bar. The c2 evidence is the binding record.

The analyzer is a useful gross-structure instrument with known, characterized
false-positive modes. It is not yet a trustworthy fine-structure reporter.
The three mechanisms above are the repair targets for the next iteration.
