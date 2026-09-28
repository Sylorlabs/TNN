# FROZEN PREREG — VFB-1: video fault battery

**Status:** FROZEN PREREG, signature-pending. PROPOSAL ONLY — not run.
Freezing requires Micah's sign-off (see Signature block below). No battery,
fixture, or probe may be built or run under this prereg before that
signature is recorded. Running without signature violates program law.

**Decision anchor:** Micah APPROVED option B (2026-09-24): the T1–T3
three-gate test as universal law — output feedback earns authority only if
(T1) faults are detectable against plan-derived expectation, (T2) the
correction map is plan-pure (constant in measured output, Lipschitz-0,
idempotent), (T3) the output is epistemically safe to re-ingest. Video
PASSES with a per-path instantiation: plan-absolute rendering (piece 1) +
exception detect-and-reassert per frame (piece 2); no output-conditioned
scene events (piece 3 denied). Source:
`bytegen/authority_question/DECISION_BRIEF.md` (frozen pin §0).

**Scope guard:** this battery tests the *instantiation*, not the universal
principle. The T1–T3 principle is law by Micah's decision; this battery
settles whether video's two-piece instantiation holds and whether the
wrong-rule alternatives (continuous servo, self-referential events) fail as
predicted. Nothing in this prereg authorizes changing the principle, the
production emitters, or the rendering plan.

## 0. Frozen pins

| # | Pinned item | Pin |
|---|---|---|
| P1 | Repo + branch | `sylorlabs/TNN`, branch `tnn-native-lab`, HEAD `fce3cf19f3af9ed825df7db1419c24f20b4a67f8` (VERIFIED: branch resolves via GitHub API) |
| P2 | Source draft | `docs/lab/bytegen/authority_question/teams/video/BATTERY_PREREG_DRAFT.md` at P1, blob SHA `9604e390cd3a6f4212636c2d5a3caed5c420ba22` (VERIFIED) |
| P3 | Video fault analysis | `docs/lab/bytegen/authority_question/teams/video/FAULT_ANALYSIS.md` at P1, blob SHA `54b99194fabf9e63fb6b7d1073737724171eebd7` (VERIFIED) |
| P4 | Video wrong-rule cost | `docs/lab/bytegen/authority_question/teams/video/WRONG_RULE_COST.md` at P1, blob SHA `b60b46e4a3c35db671649c85dd2ecebb097416fc` (VERIFIED) |
| P5 | Video authority recommendation | `docs/lab/bytegen/authority_question/teams/video/AUTHORITY_RECOMMENDATION.md` at P1, blob SHA `d31ab3ff28b3438b8bc2b978faee47584033347d` (VERIFIED) |
| P6 | Decision brief | `docs/lab/bytegen/authority_question/DECISION_BRIEF.md` at P1, blob SHA `49d7efe186aefd9ae67e24708495bef1392f2f8f` (VERIFIED) |
| P7 | Toolchain | `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` — filename pin as cited in the draft; exact binary SHA-256 recorded in the run log at freeze (build with `--no-zagd --no-analyze --no-foreground-cache`) |
| P8 | V-DET manifest (determinism precedent) | cited in draft §0 as manifest `400ae5c6…938b26ac` (truncated prefix as cited; full 64-hex digest recorded in the run log at freeze) |
| P9 | Fixture sources (existence/provenance pins; fixture SHAs recorded at freeze per §2) | `tnn-lab/imagination_discovery/vid/ocean.zag` at P1, blob SHA `c7728042f88bcca010aa3660f5e11b337d16b79c` (VERIFIED); `tnn-lab/imagination/src/field.zag` at P1, blob SHA `89b96789c9b92bcf041d941b716c75fbc1411d8b` (VERIFIED) |

All pins resolved against true lineage at P1. If any pin fails to resolve,
it is written "UNRESOLVED — needs re-pin" and the battery may not start.

## 1. Question under test

The AUTHORITY_RECOMMENDATION.md two-piece rule — plan-absolute rendering
(piece 1) + exception detect-and-reassert per frame (piece 2), no
output-conditioned scene events (piece 3 denied). The battery must prove:
(a) piece 2 heals artifact faults exactly; (b) false positives are
no-ops; (c) any continuous-feedback candidate degrades what is natively
1.0; (d) a self-referential event prototype cascades, justifying the
piece-3 denial; (e) sub-floor faults are honestly invisible.
(Transcribed verbatim from the frozen draft.)

## 2. Frozen fixtures

| Fixture | Source | Frames | Rationale |
|---|---|---|---|
| `ocean_f23` | `imagination_discovery/vid/ocean.zag`, frame 23, `dbg 0` | 1 (3,145,782 B) | Mid-sequence, all mechanisms active (vortex, spires, foam) |
| `ocean_f00`, `ocean_f47` | same | 2 | Sequence endpoints (V-SHARP bars measured here) |
| `r4_Mg_f23` | `imagination_discovery/vid/r4/src/ocean_r4.zag` frame 23 | 1 | Newest mechanism variant (Mg cross-step shading) |
| `field_g_v1` | `imagination/src/field.zag` `f3_emit_avi_g`, v=1, 36 frames | 36 (480×480) | Keyframe-interpolated path, second native architecture |

At freeze: record SHA-256 of every fixture frame from a clean build with
the pinned toolchain. These SHAs are the "clean" reference for all
heal/no-op comparisons. Determinism gate: two clean builds on the same VM
must reproduce all SHAs byte-identically.

Fault-injector choice (pure-Zag injector or byte-exact Python script) is
frozen at freeze time; either way deterministic, no RNG, fixed offsets
recorded in the prereg appendix.

## 3. Fault injection models (frozen; all deterministic, seeded integer offsets — zero RNG)

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

Fault classes VF-1..VF-6 per FAULT_ANALYSIS.md (P3): bit-flips (VF-1),
zeroed regions (VF-2), full frame dropout (VF-3), wrong frame in slot
(VF-4), sub-floor tampering (VF-5, honest floor — disclosed invisible),
plan corruption (VF-6 — not an output fault; the C4 boundary).

## 4. Detection predicates (plan-derived, frozen at freeze time)

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

## 5. Batteries

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

### B-TAX — does a continuous-feedback candidate degrade native 1.0? (WRONG-RULE ARM)

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

*Predicted-failure framing (program law for wrong-rule arms): if this arm
PASSES (the servo does not degrade), the rule's C1 claim is wrong — the
anti-servo clause weakens to "unnecessary" rather than "corrupting," and
the rule must be revisited per §7.*

### B-CASCADE — does a self-referential event prototype cascade? (WRONG-RULE ARM)

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

*Predicted-failure framing: if this arm FAILS to cascade (the latch
self-heals — tail returns to plan within ≤2 frames), the non-coexistence
claim falls and the piece-3 denial must be re-opened per §7.*

### B-PLAN — the control

Build with F-PLAN (wrong vortex constant). Run predicates + pipeline.

**Kill criterion:** predicates pass (bytes match the wrong plan), pipeline
changes 0 bytes, healed output still differs from the *true* clean fixture.
Pass = the battery correctly identifies this as outside the exception
path's authority (proves the C4 boundary: artifact faults healed, plan
faults untouched).

## 6. Determinism and purity requirements (applies to all batteries)

- Pure Zag for generator, injector, predicates, and pipeline; pinned
  toolchain P7.
- Zero RNG anywhere: fault offsets/patterns are fixed integers in the
  prereg appendix; noise is the existing deterministic hash functions.
- Byte-identical reruns: every battery run twice; all SHAs must match
  across reruns. Any nondeterminism fails the battery (not the rule).
- No battery step may modify the frozen fixtures; work on copies in a
  scratch dir (NOT /tmp — 512 MB shared tmpfs; use `~/workspace` scratch
  per standing house rule).
- The servo (B-TAX) and latch (B-CASCADE) candidates are throwaway
  experimental binaries — never committed as product code, clearly labeled.

## 7. What would change the recommendation

- B-TAX failing to show degradation (servo harmless) → re-open C1; the
  anti-servo clause weakens to "unnecessary" rather than "corrupting."
- B-CASCADE showing the latch self-heals (tail returns to plan within ≤2
  frames) → re-open the piece-3 denial; the non-coexistence claim falls.
- A demonstrated scene need (battery-grade, preregistered) that plan-pure
  rendering cannot author but a latch can → piece-3 gates
  (AUTHORITY_RECOMMENDATION.md) get their first real applicant.
- B-DETECT below 95% on above-floor faults → predicates, not the rule, need
  work; the rule stands but the detection floor disclosure must widen.

## 8. Out of scope (documented, not tested)

- Encoder/transmission faults beyond the file level (the battery faults the
  BMP/AVI bytes; codec-level error concealment is downstream).
- Adversarial faults crafted with knowledge of the predicates (white-box
  evasion) — a red-team round, not this battery.
- Performance: detection + re-render cost is recorded but has no kill bar
  (correctness first; ~2.5 s/frame re-render is already known).

## 9. Verdict rule

- **PASS:** all kill criteria in §§5–6 hold, including both wrong-rule arms
  failing as predicted (B-TAX shows degradation, B-CASCADE cascades).
- **FAIL:** any kill criterion in B-DETECT/B-HEAL/B-NOOP/B-PLAN missed, or
  either wrong-rule arm contradicts its predicted failure without the
  §7 re-opening path.
- No victory declared on partial batteries: all fixtures × all fault
  models, or it didn't happen. The V-DET manifest (P8) determinism gate
  must hold before any fault leg runs.

## 10. Amendments clause

Frozen on Micah's signature. Any change to rules, schedule, fixtures,
fault models, predicates, batteries, metrics, or kill criteria after
signature requires his re-approval before running. Bent rules during
execution are documented and flagged for revert. The T1–T3 principle
itself is not amendable by this battery — it is law by his 2026-09-24
decision; this prereg settles only the video instantiation.

## 11. Signature

**Decision (tick one):**

- [ ] **APPROVED** — the battery may be run exactly as written. No amendments.
- [ ] **APPROVED WITH AMENDMENTS** — amendments listed below; prereg re-frozen after edits, re-signed before any run.
- [ ] **REJECTED**

Amendments (if any): ___________________________________________________

_________________________________________________________________________

Signed: ____________________________ (Micah)

Date: ____________________________

**Battery-run authorization:** no battery, fixture, probe, or harness may be
built or run under this prereg before this signature is recorded. Running
without signature violates program law. The four production emitters
(`f3_emit_wav`, `f3_emit_wav_hifi`, `f3_emit_avi`, `f3_emit_avi_g`) are not
touched by this prereg — their repair is a separate crew's work.
