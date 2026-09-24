# BATTERY_PREREG_DRAFT — video fault battery (VFB-1)

**Status:** PROPOSAL ONLY — not run, not frozen. Freezing requires Micah's
sign-off on the fixture and the kill bars (per standing governance: frozen
prereg amendments come to him).

**Question under test:** the AUTHORITY_RECOMMENDATION.md two-piece rule —
plan-absolute rendering (piece 1) + exception detect-and-reassert per frame
(piece 2), no output-conditioned scene events (piece 3 denied). The battery
must prove: (a) piece 2 heals artifact faults exactly; (b) false positives
are no-ops; (c) any continuous-feedback candidate degrades what is natively
1.0; (d) a self-referential event prototype cascades, justifying the piece-3
denial; (e) sub-floor faults are honestly invisible.

## 0. Frozen fixtures (to be blessed at freeze time)

| Fixture | Source | Frames | Rationale |
|---|---|---|---|
| `ocean_f23` | `imagination_discovery/vid/ocean.zag`, frame 23, `dbg 0` | 1 (3,145,782 B) | Mid-sequence, all mechanisms active (vortex, spires, foam) |
| `ocean_f00`, `ocean_f47` | same | 2 | Sequence endpoints (V-SHARP bars measured here) |
| `r4_Mg_f23` | `imagination_discovery/vid/r4/src/ocean_r4.zag` frame 23 | 1 | Newest mechanism variant (Mg cross-step shading) |
| `field_g_v1` | `imagination/src/field.zag` `f3_emit_avi_g`, v=1, 36 frames | 36 (480×480) | Keyframe-interpolated path, second native architecture |

At freeze: record SHA-256 of every fixture frame from a clean build with the
pinned toolchain (`tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
`--no-zagd --no-analyze --no-foreground-cache`). These SHAs are the
"clean" reference for all heal/no-op comparisons. Determinism gate: two
clean builds on the same VM must reproduce all SHAs byte-identically
(V-DET precedent: manifest `400ae5c6…938b26ac9`).

## 1. Fault injection models (all deterministic, seeded integer offsets — zero RNG)

Applied to *copies* of fixture frames (never the frozen originals):

- **F-BIT1:** single-bit flip at fixed byte offset (mid-file).
- **F-BIT64:** 64-byte burst overwrite (fixed offset, fixed pattern `0xA5`).
- **F-BIT1K:** 1024-byte burst overwrite.
- **F-ZTILE:** 16×16 pixel tile zeroed (fixed position, water region).
- **F-ZQUART:** quarter-frame zeroed (top-left 512×512).
- **F-ZFULL:** full frame zeroed (3,145,728 zero bytes + valid BMP header).
- **F-DROP:** frame file replaced by 0-byte file (VF-3).
- **F-DUP:** frame `f+1`'s slot filled with a copy of frame `f` (VF-4).
- **F-SHUF:** frames 20–27 written in reverse order (VF-4, sequence-level).
- **F-SUB1:** every pixel's R channel XOR 1 (±1 LSB global — sub-floor probe).
- **F-SUBT:** 64×64 region tinted +6 RGB (small-region, near-floor probe).
- **F-PLAN (control):** `o_scene` vortex constant altered (+50% `vrr`) at
  build time — a plan fault. The battery must show piece 2 does NOT "heal"
  this (bytes match the wrong plan; predicates pass).

Each fault is applied by a pure-Zag injector (or a byte-exact Python
script — injector choice frozen at freeze time; either way deterministic,
no RNG, fixed offsets recorded in the prereg appendix).

## 2. Detection predicates (plan-derived, frozen at freeze time)

No frozen literals. For ocean frames, per-frame expected statistics derived
from the scene model:

- **P-SIZE:** file size == 3,145,782 (exact — catches F-DROP, truncation).
- **P-TILE:** 16×16 tile mean luminance vs plan-computed tile mean
  (recompute the material model per tile from `(f, tile)` — same functions
  the renderer uses, independent code path); fault iff any tile outside
  `[0.35×, 2.5×]` of expected (band borrowed from audio HYBRID_SPEC §2;
  exact band frozen after calibration on clean fixtures, must contain all
  clean tiles with margin).
- **P-GRAD:** frame gradient energy vs plan-expected band (catches
  F-ZTILE/F-ZQUART: zeroed regions collapse gradients).
- **P-TEMP (sequence-level):** per-pair mean|Δ|/255 within the plan's motion
  band (ocean: [0.5%, 15%] per V-TEMP; field-AVI: keyframe-endpoint exactness
  + interpolation monotonicity). Catches F-DUP (|Δ|≈0) and F-SHUF.
- **P-HDR:** BMP header fields exact (catches header corruption in F-BIT*).

Calibration step (frozen procedure): build clean, compute per-tile ratios
`measured/plan-expected` over all fixture frames, set bands to contain
min..max with ≥20% margin, record. Re-calibration required on any renderer
change — the band is an implementation calibration (synth↔model bridge),
not a scene judgment (cf. audio `K_PLAN`, HYBRID_SPEC §5).

## 3. Batteries

### B-DETECT — does the predicate suite catch artifact faults?

For each fault in {F-BIT1, F-BIT64, F-BIT1K, F-ZTILE, F-ZQUART, F-ZFULL,
F-DROP, F-DUP, F-SHUF} × each fixture frame: apply fault, run predicates,
record detected/not per predicate.

**Kill criterion:** ≥95% of above-floor faults detected by ≥1 predicate;
100% of F-ZFULL/F-DROP/F-DUP/F-SHUF detected. F-SUB1/F-SUBT are
*expected* to evade some or all predicates — recorded as the disclosed
detection floor, not a failure (cf. audio §8: 64-sample zeroing ×0.97 RMS).

### B-HEAL — does re-render restore byte-identity?

For each detected fault: re-render the faulted frame plan-pure
(`o_emit_frame(f)` / `f3_vidfield(v,f)` + raster, same binary, same args),
compare SHA-256 vs frozen clean SHA.

**Kill criterion:** 0 differing bytes on every healed frame. (Expected:
passes by construction — the correction map is constant. The battery's job
is to *verify* the construction, not to assume it.)

### B-NOOP — are false positives harmless?

Run the full predicate suite + "re-render on detection" pipeline on all
clean fixture frames (no fault injected).

**Kill criterion:** 0 bytes changed across all clean frames (every
re-render, if any fire, must be byte-identical to the input). A single
changed byte fails the battery — it would mean the correction map is not
constant.

### B-TAX — does a continuous-feedback candidate degrade native 1.0?

Construct the servo candidate the recommendation rejects: per-frame mean
luminance servo — after rendering frame `f`, measure its mean luminance
`m_f`, adjust a global exposure scalar `g_{f+1} = clamp(T / m_f)` toward a
frozen target `T` (the video analog of audio v1's per-block AGC; deliberately
the naive design). Render the full 48-frame ocean sequence with the servo
engaged from frame 0.

Measure: (a) frame-level recurrence — re-render frame 23 standalone
(plan-pure, `g` reset) vs the servo's frame 23: count differing bytes
(expected: >0 — the servo's state leaked into the frame); (b) plan-fidelity
drift — per-tile deviation of servo frames from plan-expected tile means vs
clean frames' deviation (expected: servo deviation strictly larger on
≥80% of tiles — it fights the material law); (c) determinism — two full
servo runs byte-identical (expected: yes — the servo is deterministic; the
point is that determinism ≠ plan-fidelity).

**Kill criterion (for the *candidate*, i.e. pass = candidate rejected):**
(a) >0 differing bytes AND (b) drift larger on ≥80% of tiles. If the servo
somehow passes (a)/(b) — i.e., it does not degrade anything — the
recommendation's C1 claim is falsified and the rule must be revisited.
This battery is the load-bearing test of "feedback corrupts here."

### B-CASCADE — does a self-referential event prototype cascade?

Construct the denied piece-3 prototype: "spire-glint event" — frame `f+1`'s
sun elevation is raised +5% iff frame `f`'s measured mean brightness in the
sky region exceeds a threshold (a bounded, one-shot-per-frame latch,
deliberately the *safest* version of the idea). Inject F-BIT1K into frame 20
of a clean sequence; render frames 20–28 with the latch engaged; compare
each frame's bytes vs the clean plan-pure sequence.

**Kill criterion (pass = prototype rejected):** ≥1 frame beyond the faulted
frame differs from clean (expected: frames 21+ all differ — the corrupted
measurement diverted the latch, and the scene never returns to plan), AND
single-frame re-render of frame 20 alone does NOT restore frames 21+
(expected: it doesn't — proving piece 2's healing guarantee is destroyed by
piece 3, the non-coexistence claim of AUTHORITY_RECOMMENDATION §steelman-3).

### B-PLAN — the control

Build with F-PLAN (wrong vortex constant). Run predicates + pipeline.

**Kill criterion:** predicates pass (bytes match the wrong plan), pipeline
changes 0 bytes, healed output still differs from the *true* clean fixture.
Pass = the battery correctly identifies this as outside the exception
path's authority (proves the C4 boundary: artifact faults healed, plan
faults untouched).

## 4. Determinism and purity requirements (applies to all batteries)

- Pure Zag for generator, injector, predicates, and pipeline; pinned
  toolchain `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Zero RNG anywhere: fault offsets/patterns are fixed integers in the
  prereg appendix; noise is the existing deterministic hash functions.
- Byte-identical reruns: every battery run twice; all SHAs must match
  across reruns. Any nondeterminism fails the battery (not the rule).
- No battery step may modify the frozen fixtures; work on copies in a
  scratch dir (NOT /tmp — 512 MB shared tmpfs; use `~/workspace` scratch
  per standing house rule).
- The servo (B-TAX) and latch (B-CASCADE) candidates are throwaway
  experimental binaries — never committed as product code, clearly labeled.

## 5. What would change the recommendation

- B-TAX failing to show degradation (servo harmless) → re-open C1; the
  anti-servo clause weakens to "unnecessary" rather than "corrupting."
- B-CASCADE showing the latch self-heals (tail returns to plan within ≤2
  frames) → re-open the piece-3 denial; the non-coexistence claim falls.
- A demonstrated scene need (battery-grade, preregistered) that plan-pure
  rendering cannot author but a latch can → piece-3 gates
  (AUTHORITY_RECOMMENDATION.md) get their first real applicant.
- B-DETECT below 95% on above-floor faults → predicates, not the rule, need
  work; the rule stands but the detection floor disclosure must widen.

## 6. Out of scope (documented, not tested)

- Encoder/transmission faults beyond the file level (the battery faults the
  BMP/AVI bytes; codec-level error concealment is downstream).
- Adversarial faults crafted with knowledge of the predicates (white-box
  evasion) — a red-team round, not this battery.
- Performance: detection + re-render cost is recorded but has no kill bar
  (correctness first; ~2.5 s/frame re-render is already known).
