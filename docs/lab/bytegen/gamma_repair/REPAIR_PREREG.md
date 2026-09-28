# GAMMA-DISEASE REPAIR — frozen prereg

Frozen: 2026-09-24 ~00:05 PDT (before any source edit).
Status: PREREG — no code changed yet.

## Finding (from the bytegen authority swarm)

Four production emitters in `imagination/src/field.zag` carry output-derived
peak normalizers — rendered-output statistics feeding scaling decisions, the
exact pattern the v2 hybrid deleted from the audio servo:

| Emitter | Lines (pre-repair) | Gamma pattern |
|---|---|---|
| `f3_emit_wav` | ~1025–1041 | scans rendered `mix` for peak (unsigned read), `if (peak > 28000) v = v*28000/peak` |
| `f3_emit_wav_hifi` | ~1166–1184 | scans rendered `mix` for peak (signed read), `v = v*24000/peak` always |
| legacy `f3_emit_avi` | ~1496–1513 | same as `f3_emit_wav`, on the AVI soundtrack |
| `f3_emit_avi_g` | ~1863–1880 | same as `f3_emit_wav_hifi`, on the AVI-G soundtrack |

## Repair spec (exact edits, nothing else)

In each emitter: DELETE the peak-scan loop. DELETE the output-derived scale
(`*28000/peak`, `*24000/peak`, and the `if (peak > 28000)` / `if (peak < 1)`
guards). Replace with plan-pure gain = 1: emit the mix sample directly.
KEEP: the mix read call as-is (`f3_get32` in legacy, `f3_get32s` in hifi —
the legacy unsigned-read sign bug is NOT fixed here, out of scope), the fixed
`±32767` safety clamps (constant rails, not output-derived), WAV/AVI headers,
interleave plan, and every other line.

Rationale: the plan already stages intended levels per voice
(`ew = e*28*w/1000`, mix = Σ voices). The normalizer destroyed inter-render
dynamics (every render peaked at 24000/28000 regardless of plan energy).
Gain = 1 restores the plan's own level design. This mirrors the v2 hybrid's
servo deletion (pure F(plan,t)).

Also added (test scaffolding only, NOT emitter behavior): a `f3gammaproof`
main mode that builds song field A, field B = A + one extra loud frame
(energy 2000 × 48 bins), emits both via `f3_emit_wav` and
`f3_emit_wav_hifi`, and prints diagnostic mix peaks. Python compares PCM
prefixes.

## Battery (fixture = the binary's own deterministic scene builders)

- `f3wav` → 6 WAVs (legacy 8 kHz)
- `f3hifi` → 4 WAVs (hifi)
- `f3avi` → 2 AVIs (legacy)
- `f3gavi` → 2 AVIs (hifi-G)
- `f3gammaproof` → 4 WAVs (A/B × legacy/hifi)
- Full battery run 3× → SHA256 of every file must match across runs.

## Acceptance bars

- R1: every emit returns rc=0; all 18 files produced.
- R2: 3 reruns byte-identical (all SHAs match).
- R3 (the gamma proof): NEW binary — PCM prefix bytes of proof-B ==
  proof-A (samples before the appended loud frame), for both wav paths.
  OLD binary — the same prefixes DIFFER (the loud tail rescales the whole
  file). This is the before/after byte-diff showing output bytes no longer
  depend on rendered statistics.
- R4 (no other behavior changed): WAV headers byte-identical before/after;
  AVI bytes byte-identical before/after with audio (`01wb`) chunks masked;
  non-emit modes untouched.
- R5: zero RNG — no RNG primitive in the emit path (static grep) + R2.

## Known test dependencies on the OLD normalizer (flagged, not silently changed)

- HIFI-PREREG H3 / MOOD2-RESULTS H3 assert "peak exactly 24000" on hifi
  renders. After repair, hifi peak = plan-rendered peak (≤24000 by
  construction per the design note, but no longer exactly 24000). Those bars
  need a Micah-signed amendment if they are to be re-run.
- MOOD2 B1 documents legacy stats (min=0/max=28000/zero-crossings=0) as the
  rectification bug report. After repair the legacy unsigned-read sign bug is
  still present but manifests differently (negative samples now hit the
  +32767 clamp rail instead of being rescaled to ~28000). The sign bug itself
  is out of scope for this ticket.

## Commit plan

1. This prereg (ordering proof).
2. `imagination/src/field.zag` fix + `bytegen/gamma_repair/REPAIR_NOTE.md`
   with before/after SHAs, proof results, and the flags above.
