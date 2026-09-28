# GAMMA-DISEASE REPAIR — execution note

Date: 2026-09-24. Prereg: `REPAIR_PREREG.md` (committed pre-execution as
`f472ca9c53b45e6b732c5b74e6576e473bf0b337`).
Source fix: `imagination/src/field.zag` (this commit).

## What was done

Removed the output-derived peak normalizer from all four production
emitters in `imagination/src/field.zag`:

| Emitter | Removed | Replaced with |
|---|---|---|
| `f3_emit_wav` | peak scan (unsigned read) + `if (peak>28000) v=v*28000/peak` | gain 1: `v = f3_get32(mix,s2)` |
| `f3_emit_wav_hifi` | peak scan (signed read) + `v=v*24000/peak` | gain 1: `v = f3_get32s(mix,s2)` |
| legacy `f3_emit_avi` | same as `f3_emit_wav` on the AVI soundtrack | gain 1 |
| `f3_emit_avi_g` | same as `f3_emit_wav_hifi` on the AVI-G soundtrack | gain 1 |

Kept: the mix read calls as-is (legacy keeps unsigned `f3_get32` — the
rectification sign bug is NOT fixed here, out of scope), the fixed
`±32767` safety clamps (constant rails, not output-derived), all
WAV/AVI headers, the interleave plan, and every other line. Stale
"normalized to 24000/28000" comments rewritten. Test-only `f3gammaproof`
main mode added (proof scaffolding, not emitter behavior).

## Proof results (bars R1–R5, all PASS)

Battery: `f3wav` (6) + `f3hifi` (4) + `f3avi` (2) + `f3gavi` (2) +
`f3gammaproof` (4) = 18 files, pure Zag, zero RNG.

- **R1**: all 18 emits rc=0.
- **R2**: 3 full reruns, all 18 files byte-identical (SHA256) across runs.
- **R3 — the gamma proof** (field B = song field A + one appended loud
  frame; compare samples the two plans render identically):
  - hifi path, samples [0,107484): OLD binary **107,428 diffs** (the loud
    tail rescaled the entire file — the disease); NEW binary **0 diffs**.
  - 8kHz path, samples [0,20000): NEW binary **0 diffs**. (OLD legacy
    gain barely moves on this fixture because its unsigned peak scan is
    dominated by sign-wraparound; its gamma shows as every file pinned at
    max=28000 regardless of plan energy.)
  - NEW outputs are now a pure function of (plan, LUT): no rendered
    statistic feeds any scaling decision (verified by code inspection —
    no peak scan remains in any emitter).
- **R4**: all 10 WAV headers byte-identical before/after; all 4 AVIs
  byte-identical before/after with audio (`01wb`) chunks masked —
  video frames, headers, interleave untouched.
- **R5**: zero RNG — no RNG primitive in the emit path (only fixed-seed
  `f3_hash2` in field construction, deterministic) + R2 determinism.

## MATERIAL FINDING — the ticket's premise is falsified by measurement

The ticket asserted "the plan already knows the intended levels." With
plan-pure gain = 1, the current plan corpus **clips**:

| File (NEW) | samples at ±32767 rail |
|---|---|
| f3song_hifi.wav | 5.90% |
| f3mood_happy.wav | 4.06% |
| f3mood_scary.wav | **16.94%** |
| f3mood_calm.wav | 0% (peak 26056, clean) |
| legacy f3song.wav etc. | 40–46% at +32767 (see sign-bug note) |

The old code's "clipping impossible by construction" design note was
false: the plan's per-voice energies (`ew = e*28*w/1000`) were staged in
a world where the normalizer existed. The normalizer was **load-bearing
for absolute level management**, not just a gamma nicety. Deleting it
restores the plan's inter-render dynamics (the cure is real — see R3)
but the corpus is staged hot for a gain-1 world.

The calm mood (0% railed) shows the plan *can* stage safe levels; the
other three fixtures cannot — their energies assume normalization.

## Legacy sign-bug interaction (documented, not fixed)

MOOD2 B1 already documents the legacy unsigned-read rectification bug
(old stats: min=0/max=28000/zero-crossings=0). After this repair the bug
is still present but manifests differently: negative samples now hit the
+32767 clamp rail instead of being rescaled to ~28000. Fixing the read
itself (`f3_get32s`) is a separate ticket — deliberately not done here
per "do not change any other emitter behavior."

## Test dependencies on the OLD normalizer (flagged, not silently changed)

- **HIFI-PREREG H3 / MOOD2-RESULTS H3** assert "peak exactly 24000" on
  hifi renders. By design this bar can no longer pass (new peaks are
  plan-determined: 26056–32767 on the battery). Re-running those suites
  needs a Micah-signed prereg amendment.
- MOOD2 B1's legacy stats (min=0/max=28000) were a bug report, not a
  passing bar; they now read min=0/max=32767 per the sign-bug note above.

## Open decision for Micah (not decided here)

Absolute level strategy for the gain-1 world — pick one:
1. **Re-stage plan energies** for gain 1 (plan authors own levels now;
   calm-mood proves it is possible);
2. **Adopt a fixed plan-pure mastering gain** (a single constant for all
   renders — preserves dynamics, needs a loudness decision; any constant
   < 1 is a new mastering choice, not derivable from the plan);
3. **Revert** this repair and keep output-derived normalization.

Note the v2 hybrid precedent is split: its architecture deleted the
servo, but its own `wav_write` demo still peak-normalizes to 0.85 FS —
even there, final mastering stayed output-derived. Production mastering
policy is still an open question for the authority swarm.

## Before/after SHAs (after = run 1 of 3 identical runs)

Before (old normalizer):
- f3a1.wav e42df0b1cf9a2b36d03a72aff898aa85a9875b5055548c120c0254f32f8110d4
- f3song.wav 4abdb09d3b25fdad61d6c5d7e4d70c404589c71db2bd7de2c20010df5c687e7e
- f3song_hifi.wav 0af6a284942f7a0eae23321a7c8bbc8c3eba80e14217f3b873c8813cadc48a08
- f3mood_happy.wav d774f4a4b6f76def9827e876893f63eaa7e79ceab20e3d5209df74d7e71d8dba
- f3vid1.avi 744b79b0fa9b8c44f56139b18df40e4493bd66338ce5c1e8caecf7894b405acf
- f3gvid1.avi fe0d2fb38ea51bff41c61ebf0a02c9b001fbdf021c180bbb435625fc1ce8992c
After (plan-pure gain 1), run 1 = run 2 = run 3:
- f3a1.wav 20b85bbbbd7148951d7b9dcecae2a1a12145383796c26dee79526e4a631bf38a
- f3song.wav 8fd500c91acc730873e7d3623306cf84a78d532028dc32327a5eea81e9d3dae5
- f3song_hifi.wav 0742f7ec87627c281dfa9a15dffaa3cc3eba107880d77938481715fb72f2b906
- f3mood_happy.wav 4a7169faa90ce19d61515df9ddad15da2cc52f7883fe9c982b8d442b56299be1
- f3vid1.avi 8a8e2f4f0199d3b1a93fa7864608e6fe7e5ca6ba8905a055d6b7cbb9736c93c4
- f3gvid1.avi fb5dddde8c9c9afce57c9cf635148236d8b0377d233bcae36a53461bbd302c8b
(Full 18-file SHA lists in run logs; every file differs before/after —
expected, the old scaler fired on all of them.)
