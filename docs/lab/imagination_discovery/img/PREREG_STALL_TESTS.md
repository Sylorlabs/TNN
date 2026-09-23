# STALL-SWEEP PREREG — Visual line: the four required counterfactual tests
# FROZEN 2026-09-22 (before any run). Branch: tnn-native-lab.

This prereg un-stalls the four tests required by the program record for
Fork B (leader) after the T13/T13b moonfix (commit 40958e4a4):
  (1) RELIGHT TEST, (2) BACKLIT ARCH TEST, (3) ORGANISM RE-CONCEPTION,
  (4) TRACE INTEGRITY.
Proposed in FORK_OPINIONS.md §§4–5 (sol E4, Critic 2 counterfactual,
Critic 3 arch test + standing artifact-first recommendation).

Standing rules for all four: pure Zag generation path, zero RNG anywhere
in decision or depiction paths; pinned toolchain znc_linux_x86_64_abed8aa1,
--no-zagd --no-analyze; Python only for verification/measurement (never in
the generation path); D-DET (two independent clean-process renders
byte-identical, SHA-256 recorded); no binaries/.zagd committed; BMPs + PNG
previews committed; lab-relative paths via commit_racefree.py.

Trace claims are scored against the artifact, never the reverse
(Critic 3's standing rule): any quantitative trace claim (e.g. "~19% lit",
"r=80") must be verified by measurement on the render before it may be
cited as evidence.

================================================================
TEST 1 — RELIGHT (counterfactual light change)
================================================================
Frozen input: imagination_discovery/img/r8b_alien.zag as committed in
40958e4a4 (T13/T13b canonical). ONE change: the deliberated sun vector is
rotated 90° in azimuth. Sun vector change is the only permitted source
edit; every other changed constant must be mechanically sun-derived
(sky azimuth gradient terms, sun-disc screen position, shadow-march
direction) and each is listed with its derivation in the report.
Geometry, camera, moon orbit, noise seeds: byte-identical otherwise.
Output: imagination_discovery/img/r8b_relight.zag (source),
r8b_relight_1024.bmp/png.

Bars (all artifact-first):
- R1-SHADOW-FLIP: terrain shading follows the NEW sun. Measurable:
  sample ≥2000 terrain pixels classified as slope-facing-left vs
  slope-facing-right (from the SAME SDF normal field in both renders);
  the light/dark assignment must invert: the fraction of pixels whose
  luminance class flips from lit to dark / dark to lit ≥0.90, and the
  fitted illumination azimuth must be within 20° of the new sun azimuth
  and within 70–110° of the old one. FAIL otherwise.
- R1-MOON: the moon's phase recomputes to a *measurably visible*
  crescent under the new sun: ≥5% of disc pixels above sky luma on the
  lit side; disc interior mean ≥8/255 (planetshine present); the moon is
  not a black disc again. FAIL if it renders black.
- R1-FOREGROUND: the foreground does not collapse into unreadable murk:
  mean gradient in the foreground third ≥ the canonical render's
  foreground-third mean gradient × 0.8 (no collapse).
- R1-DET: two independent 1024 renders byte-identical.
Kill criterion: if R1-MOON fails (moon black again) or R1-SHADOW-FLIP
fails (shadows need hand-patching), the world model and the renderer are
coupled only by the author's hand — B's "correct by construction"
architecture claim FAILS; Fork B returns to repair. If all pass, the
mechanism — not the artifact — is demonstrated: B's light transport is
reusable under counterfactual light.

================================================================
TEST 2 — BACKLIT ARCH (Critic 3's decisive experiment)
================================================================
Identical brief to every fork: "A wind-carved arch stands ~20 m from the
camera, backlit by the low sun. The far landscape must be visible
THROUGH its opening. Render it."
Fork B build: imagination_discovery/img/r8b_arch.zag — new SDF scene in
the B idiom (true 3D distance field, raymarched, one deliberated sun,
no placed primitives): terrain + wind-carved arch (noise-eroded torus
arc, ~20 m from camera, backlit) + far landscape behind the opening.
The relight variant (Test 1's 90° sun rotation) is also rendered for
the arch scene as the joint E4/counterfactual run (r8b_arch_relight).

Bars:
- A1-OPENING: the opening is real occlusion, not paint. Measurable: a
  contiguous opening region ≥30 px² whose pixel colors match the
  far-field sightline model (the same pixels' sky/terrain blend along
  the sightline continued past the arch, or the render's own horizon
  color statistics) within ±15% luminance — i.e. far landscape is
  genuinely visible through it. FAIL if the opening is a painted patch.
- A1-EDGE: mechanical silhouette bar (Critic 3): mean gradient across the
  arch silhouette ≥2.0× the local background gradient (no mush).
  FAIL below 2.0.
- A1-SHADOW: the arch casts a sun-consistent cast shadow toward the
  camera (backlit): measured shadow azimuth within 25° of the sun
  azimuth line through the arch. FAIL if no consistent shadow.
- A1-RELIGHT: under the 90°-rotated sun the arch keeps recognizable hard
  geometry (A1-EDGE still ≥2.0) and the cast shadow moves to the new
  sun-consistent azimuth (within 25°). FAIL if the relight is a global
  color wash.
- A1-DET: byte-identical reruns.
- Human bars (pending a blind panel; reported as UNCLAIMED until run):
  ≥4/5 blind viewers trace a continuous arch outline and describe
  structured content through the opening.
Kill criterion: if A1-OPENING or A1-EDGE fails, B cannot express hard
subtractive form (occlusion through an opening) — B's "nothing placed,
everything computed" claim FAILS for composed geometry; if A1-RELIGHT
fails, the arch is a first-pass arrangement, not a reusable scene model.
Fork C runs the same brief with its own harness (staffed to the
follow-up C crew; C's bars per FORK_OPINIONS §5: arch visible as an
arch, ≥4/5 blind viewers, mechanical edge ≥2.0).

================================================================
TEST 3 — ORGANISM RE-CONCEPTION
================================================================
Re-conceive the r8b foreground as the back of a DORMANT COLOSSAL
ORGANISM (the world-model invention test). Fork B build:
imagination_discovery/img/r8b_organism.zag — the foreground rubble is
replaced by a reconceived organism back: a domed carapace with a
tessellated scute-plate structure (plates with seams, distinct albedo),
bilateral symmetry about a spinal axis, half-buried at the scarp edge —
a creature at rest, not decorated terrain. One sun, same light
transport, same camera as the canonical render.

Bars:
- O1-SYMMETRY: bilateral mirror-correlation of the foreground region
  about the spinal axis ≥0.65 (rubble baseline from the canonical render
  <0.45, measured with the same code). FAIL below 0.65.
- O1-PLATES: plate tessellation measurable — spatial autocorrelation of
  the foreground albedo/shading shows a peak at the plate spacing with
  contrast ≥1.5× the no-plate noise floor (code also run on canonical
  foreground as negative control). FAIL if no plate structure.
- O1-LIGHT: the organism obeys the same one-sun transport: normal-field
  shading model vs rendered luminance R² ≥0.85 (same test as canonical
  terrain). FAIL below — painted, not lit.
- O1-NO-STARVE: the organism fills the foreground third (occupancy ≥60%
  of the foreground band by organism-surface pixels); foreground mean
  gradient ≥ canonical foreground mean gradient × 0.8 (detail is not
  starved away). FAIL if the organism is a small patch.
- O1-DET: byte-identical reruns.
- Human bar (pending blind panel; UNCLAIMED until run): ≥4/5 blind
  viewers describe the foreground as a dormant creature's back / carapace.
Kill criterion: if O1-SYMMETRY or O1-PLATES fails, the reconception is
parameter-tuning of terrain, not reconception — Critic 2's "the mind
paints better than it invents" stands and B's invention capacity FAILS.

================================================================
TEST 4 — TRACE INTEGRITY (standing gate)
================================================================
Score artifacts first, then trace claims. For the canonical render and
every new artifact in this battery: enumerate the trace's quantitative
claims (T1..T13b in UNIFIED_TRACE.md / r8b_alien.zag), map each to a
measurable artifact property, and score PASS/FAIL by measurement.
- TI-1: every feedback episode (T10/T11/T12/T13/T13b) must have a
  measurable render delta vs its pre-feedback render; a feedback claim
  with no measurable delta FAILS (diary, not mechanism).
- TI-2: no quantitative trace claim may be falsified by pixels. The r8b
  defect pattern (trace claimed a ~14%-lit crescent while the moon
  rendered a near-black disc, interior max 16/255) is the regression
  template: any recurrence on a new artifact FAILS the gate.
- TI-3: claims that do not visibly affect the artifact are struck from
  the evidence (they may stay as prose, but cannot be cited for
  architecture claims).
Verdict: TI-PASS requires all quantitative claims measured-and-held and
all feedback episodes with measurable deltas. This gate runs on the
canonical artifact now and on each new artifact from Tests 1–3.

================================================================
SEQUENCING
================================================================
1. Commit this prereg alone (frozen before any run).
2. Test 4 on the canonical artifact (measurements on committed BMPs).
3. Test 1: build r8b_relight.zag, render ×2 at 1024, measure bars.
4. Test 2: build r8b_arch.zag (+ relight variant), render ×2, measure.
5. Test 3: build r8b_organism.zag, render ×2, measure.
6. Commit sources + BMPs + PNGs + score report per test; verify head
   SHA via gh-api.
The C-fork side of Tests 1–2 is staffed to the follow-up C crew
(C's elaboration harness, same frozen bars); it does not block the
B-side verdicts.
