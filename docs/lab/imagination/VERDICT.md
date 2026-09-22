# IMAGINATION-DESIGN trial — VERDICT

Date: 2026-09-22. Frozen prereg: `PREREG.md`
(commit `6603e8dd6a025d722c8ede5e607acad6f26f72a3`).
Mechanism: `src/imagine.zag` (pure Zag, zero RNG, explicit
little-endian byte arena, ≤32 scene elements), built with the pinned
znc toolchain. Audit, sources, run log: `AUDIT-Q0.md`, `Q3-SOURCES.md`,
`RUN-LOG.md`.

## Q1 — Can TNN hold an internal scene and answer questions about it?

| Bar | Frozen rule | Machine | Human | Verdict |
|---|---|---:|---:|---|
| IMAG-1 | ≥26/36 correct | 36/36 | 36/36 | **PASS / PASS** |

Control: text-only/partitional lookup gets 2/36 per mode (<12/36
guard) — the answers come from the scene, not the question text.
Determinism: 5 reps byte-identical per mode.

## Q2 — Can TNN generate designs to briefs, in two representations?

| Bar | Frozen rule | Result | Verdict |
|---|---|---:|---|
| GEN-1 | ≥10/12 brief-compliant | 12/12 | **PASS** |
| GEN-2 | 12/12 mode-faithful | 12/12 | **PASS** |
| GEN-3 | ≥20/24 partition queries agree with emitted specs | 24/24 | **PASS** |

Every generated design satisfied every brief constraint, stayed in its
mode's vocabulary (machine: coordinates/measurements/frequencies;
human: warm red / balanced / airy / tense …), and every partition
query about a generated design agreed with its emitted spec.
Determinism: 5 reps byte-identical per mode.

## Q3 — Does TNN's taste agree with documented human taste?

8 pairs, encodings rebuilt 2026-09-22 from sourced facts
(`Q3-SOURCES.md`; 5 STRONG, 3 MODERATE evidence). Zero ties.

| Bar | Frozen rule | Machine | Human | Verdict |
|---|---|---:|---:|---|
| AGREE-1 | 7/8 works · 6/8 marginal · ≤5/8 fail | 6/8 | 4/8 | **best mode 6/8 → MARGINAL** |
| AGREE-2 | lead ≥3/8 to name a mode winner | \|6−4\|=2 | | **NO-DIFFERENTIATION** |

Machine hits: Gap, Tropicana, New Coke, UC, Mastercard, Apple.
Human hits: Gap, Tropicana, New Coke, UC. Both modes miss
Cracker Barrel (both prefer the simpler 2025 wordmark — a simplicity
bias against documented human rejection) and human misses the three
MODERATE pairs. Determinism: 5 reps byte-identical per mode.

## Q4 — Blind human rating of the 12 Q2 designs

Packet `Q4-PACKET.md` is complete (12 designs blinded A–L, fixed-seed
presentation order, rating sheet). **PENDING: rater (Micah) has not
rated.** Do not claim Q4 until ratings are recorded.

## Bottom line

TNN can internally imagine: it constructs, retains, edits, and queries
scenes in visual, audio, and structural domains, in machine and human
representations, with byte-identical determinism and no external
rendering. It generates brief-compliant designs whose internal
partitions stay consistent. Its design sense is MARGINAL: it agrees
with documented human preference on the five strongly-evidenced logo
rejections but diverges on the three moderately-evidenced cases, and
no representation mode wins.

## Open items (need Micah)

1. Q4 ratings — the blind packet is ready whenever he is.
2. `PROPOSED-amendment-video-2026-09-22.md` — add an explicit
   video/temporal battery (currently no video test despite his order).
3. Pitch-handle wording gap (`AUDIT-Q0.md` Appendix B): prereg says
   human audio pitch handles are 4000–4047; the code stores the
   ordered bin index 0–47 (disjoint from machine Hz, pitch-ordered).
   Behavior is correct; the wording needs a dated amendment.
