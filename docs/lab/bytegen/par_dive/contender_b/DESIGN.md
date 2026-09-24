# Contender B: PAR Render with Plan-Seeded Carried State

## Design

**Core idea:** Partition the 30s plan into fixed 3-second regions (132,300 samples @ 44.1kHz).
At each region boundary, WIPE all carried state, then reseed deterministically from
immutable plan data. Inside a region, native-style phase/filter carry is allowed.

**What is carried (within a region):**
- Voice phase (Q32) and vibrato phase (Q32) — advance per-sample, never reset mid-region.
- Legato chains: events separated by <80ms form a chain. Phase/vibrato continue across
  the chain; pitch portamento (60ms linear glide) connects the notes. Amplitude envelope
  remains PAR's per-note attack/release (NOT smoothed — smoothing failed G-PER).

**What is NOT carried:**
- Amplitude state (each note gets fresh PAR attack/release).
- Anything across region boundaries (wiped, reseeded from plan).
- Prior rendered samples (synthesis never reads the output mix for state).

**Region seeding (deterministic from plan):**
- For each bus event active at R0, find its legato chain head. If the chain started
  before R0, simulate (prefix) from the chain head to R0 to establish phase/vibrato.
  The prefix is deterministic (same plan → same prefix).
- Bed phase seeded closed-form: `phase = (freq * t / SR) * 2^16` at span start.

**RESPOND (RT-LONG):**
- Plan-derived octave latch (NOT audio sensing). Finds the single planned cue voice
  overlapping the source window. Computes `k = round(log2(fcue/fnom))`. If |k|>=1
  (octave or more), sets f0 = nom * 2^k. Otherwise nominal stands.
- Abstains (nominal stands) on polyphonic/ambiguous windows.
- Honest limitation: does NOT measure pitch from audio. The cue pitch comes from
  the plan. Octave detection is plan-ratio, not pitch metering.

**Key design decision (from fork testing):**
- Chain-level amplitude smoothing (flat sustain, soft swells, release-tail continuation)
  all FAILED G-PER (0.36-0.51). Only per-note PAR attack/release with phase/pitch
  continuity PASSED (G-PER 0.336). B carries pitch/phase, NOT amplitude.

## Regions
- Fixed 3.0s plan-time segments: RSAMP=132300 @ 44.1kHz.
- Fixture: 10 regions [0-3s), [3-6s), ..., [27-30s).
- Region order independence: seq/rev/stride all byte-identical.
