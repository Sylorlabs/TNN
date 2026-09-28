# PREREG — Upscale Repair Round 3: Three Broad Mechanisms, Head-to-Head

Written 2026-09-27 BEFORE any round-3 implementation or run. Frozen. This is a
FRESH prereg; rounds 1 and 2 stay frozen with their killed arms. Tests decide;
nothing here may be tuned after seeing scores. Post-result tuning of any kind
→ the round is void.

## Problem (inherited white-box, all recorded)

- Baseline generation-from-learned-atoms (pristine `azgen.zag` + 4-image vocab):
  bridge 18.47 dB, sky 22.75 dB; 9 diverse sealed photos all lose to bicubic.
- Round 1 (3 veto arms): all killed by their own bars. Finding: rejection
  after the fact cannot fix key ambiguity (~10% SSE net vs ~37% needed).
- Round 2 (match-time energy score + diverse vocab): KILLED. The score was
  sound but tiny (+0.059 dB, oracle ceiling +0.025 dB on old vocab — selection
  is near-optimal); the diverse vocab diluted useful atoms (bridge −0.47 dB,
  people −0.62 dB).
- Cross-round diagnosis: (a) the low-res key is ambiguous — many high-res
  patches downscale to the same key; (b) vocabulary coverage is the binding
  constraint, but "more diverse via farthest-point" is the wrong objective;
  (c) where atoms self-match (fit RMSE ≈ 0) construction BEATS bicubic
  (+2.2 dB tiles); where a bad atom is stamped, losses are catastrophic
  (−14/−17.5 dB tiles). The failure tail is overconfident construction under
  ambiguity, not average-case matching.
- Decoration-audit finding: the blend, the Bresenham chords, and the
  feathering were all crew-designed — TNN's deliberation never chose a
  construction operator. The fixed SHAPES→stamp cascade is crew architecture.

## Mandate for round 3

A genuinely NEW broad mechanism per candidate — new construction operators or
new structural approaches. Parameter tweaks, threshold tuning, re-vetoes, and
vocabulary swaps are VOID by this prereg. At least one candidate must have
TNN's deliberation CHOOSING the construction operator (the native question);
if none can, that is reported as a finding, not hidden.

## Candidates (one mechanism each; clean attribution; no combinations)

### C1 — Fit-licensed construction (match-time license gate)

At every SHAPES take decision, all scales, compute for the winner:
- fit ratio f = keySSD(winner) / e_NULL, e_NULL = ||B_dev||² (NULL-atom energy)
- ambiguity margin m = keySSD(runner-up) / keySSD(winner)

The take is LICENSED iff f ≤ 1/4 (the winner explains ≥4× the energy that
mean-fill leaves) AND m ≥ 2 (the runner-up is at least 2× worse — the winner
is unambiguous). Unlicensed → the baseline NO-FIT path (measured block means,
label 6), exactly as today. Finer-split recursion, the ≥9/value gain bar,
commit logic, construction, and the LINES path are otherwise byte-identical
to baseline.

Why broad: applies to every take at every scale on every image; it targets
the diagnosed catastrophic-loss tail (overconfident stamps under ambiguity)
while preserving licensed stamps. Why not threshold tuning: the ratios are
structural design choices recorded here (4× = "clearly better than nothing",
2× = "clearly the best fit") — no parameter is fit to scores, no training
data is consulted, and the gate is evaluated at match time (it changes what
gets constructed, not a post-hoc veto).

### C2 — Lineage-vouched cascade (parent-constrained child matching)

Top scale (S=64) matching is unchanged (full vocabulary). At every finer
scale, a block's candidate atoms are restricted to atoms whose recorded
source-image index equals the parent block's winning atom's source-image
index. If the parent took NO-FIT, or the restricted set is empty, the child
uses the full vocabulary. Gain bar, split logic, construction, and LINES are
otherwise byte-identical to baseline.

Provenance check (before scoring): atoms in vocab.bin must record a source
image index (per HONEST_RESULT.md they do). If the field is absent or
unreadable, C2 is VOID — reported, not worked around.

Why broad: a structural change to the matching discipline at every
parent→child transition on every image. Hypothesis: texture identity is
coherent across scales, and the coarse decision (more spatial context per
decision) vouches the fine detail — cutting ambiguity exactly where it
worsens (denser candidate fields). Why not threshold tuning: the mechanism
has no numeric parameters at all.

### C3 — TNN-deliberated operator choice (the native candidate)

At each SHAPES take point, the fixed "take → stamp atom" cascade is replaced
by TNN's deliberation choosing one construction operator per region from:
- ATOM-STAMP: measured block mean + winner atom's full-res deviations
  (the baseline construction)
- PLANE-FIT (new operator): least-squares plane fit to the block's s×s
  observed pixels, evaluated at 2× (S×S). Pure measured — no atoms.
- MEAN-FILL: measured block mean (NULL; label 6)

Measured evidence per region: e (block deviation energy), fit f and margin m
(as in C1), Sobel edge density. Deliberation rule (frozen here, choice and
reasons recorded per region in the trace):
- f ≤ 1/4 AND m ≥ 2 → ATOM-STAMP (one atom clearly explains the block)
- else if least-squares plane residual ≤ e/2 → PLANE-FIT (smooth-gradient
  region; the plane is the honest model)
- else → MEAN-FILL (no model vouched; do not invent)

Recursion, split logic, gain bar, and LINES are otherwise unchanged. The
trace records per region: evidence values, chosen operator, reason.

Why broad: moves the construction-operator choice from crew-hardcoded
(SHAPES always stamps) into TNN's per-region deliberation — the architectural
change the decoration audit demanded. Every region on every image goes
through it. The operators are deliberately minimal (measured-only fallback
ladder); the NEW mechanism is the deliberated choice, not the operators.

## Battery (frozen) and baseline

11 images. Baseline = pristine `azgen.zag` + `generation/teach_out/vocab.bin`
(SHA cbead2f7…), generation PSNR (dB):

| Image | Category | Baseline |
|---|---|---|
| bridge (512×184) | original | 18.47 |
| sky (768×512) | original | 22.75 |
| fabric | texture | 21.47 |
| woodgrain | texture | 18.37 |
| treebark | texture | 18.94 |
| calmwaters | smooth | 19.46 |
| portrait | people | 21.19 |
| car | object | 22.92 |
| building | object | 14.96 |
| cat | animal | 16.60 |
| market | mixed | 18.36 |

Protocol: diverse 9 via `diverse_set/eval_all.py --binary <bin>
--vocab ../generation/teach_out/vocab.bin` (frozen harness, frozen
`metrics.py`); bridge/sky via indir = `generation/run_bridge_1`
(`run_sky_1`) + vocab.bin copied in, `<bin> <indir> <outdir>`, score
`upscale_gen.bmp` vs `gt.bmp` with `generation/src/metrics.py`. Vocab reused
as-is — no reteaching. Test images never enter training.

## Bars

- BAR 0 (reference validity): pristine `azgen.zag` recompiled reproduces the
  committed baseline output SHAs (bridge gen 2028ba1d…,
  sky gen 84255819…) and all 11 baseline PSNRs within ±0.02 dB. If not, the
  build pipeline is broken — stop, score nothing.
- BAR 1 (broad win — the mandate): candidate mean ΔdB over the 11 images
  ≥ +0.50 dB AND wins ≥ 8/11 AND no single image < −0.15 dB vs baseline AND
  every category-group mean ΔdB ≥ 0. No trading portrait for bridge.
- BAR 2 (originals): bridge and sky each ≥ baseline − 0.10 dB.
- BAR 3 (native choice — C3 only): across the battery, ≥2 operators each
  chosen on ≥5% of constructed regions; the trace shows per-region
  evidence + choice + reason. If TNN effectively always picks one operator,
  C3 fails BAR 3 (decorative choice) even if its dB passes BAR 1.
- KILL (program): no candidate passes BAR 1 → round 3 is killed; honest
  loss with mechanism analysis. Post-result tuning → void.

## Method notes

- Pure Zag, zero RNG. Pinned toolchain
  ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
- Byte-identical reruns: every binary runs every image twice (fresh outdirs);
  upscale_gen.bmp SHAs compared.
- No commits by implementers (coordinator commits). No binaries, .zagd,
  caches, or rendered images in repo dirs. Build in scratch; delete binaries
  after scoring. Disk is at 99% — keep workdirs lean.
- znc gotchas (recorded): no `};` after a closing brace; never name an
  identifier `try`; `@import` resolves relative to cwd; `nio_alloc` takes
  BYTES; use the `i64s()` print helper pattern for i64 output.
