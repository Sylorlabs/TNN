# PREREG — Upscale Round 4: Isolate the Ingredient, Test the Vocabulary, Invert the Architecture

Written 2026-09-27 BEFORE any round-4 implementation or run. Frozen.
Tests decide; nothing here may be tuned after seeing scores.
Post-result tuning of any kind → the round is void.

## Problem (inherited, all recorded)

- Round 3 ended in an HONEST ALL-ARM KILL (`generation_fix_round3/VERDICT_R3.md`).
- C3 measured +0.955 dB, 11/11 wins — but the win was never attributed:
  PLANE-FIT rendered 85.7% of regions, ATOM-STAMP 3.7% (functionally
  decorative: neutering ATOM→MEAN moved output ≤0.03 dB). The deliberated
  chooser is very plausibly a safety gate with a plane fallback, not a
  connoisseur. z.ai approach-skeptic: "trust the number, distrust the
  claim."
- The line's own red team killed C3 structurally: category-shift traps
  (diagonal step −5.46 dB, circle −6.54 dB, gradient+step −7.04 dB vs
  bicubic) — the plane gate licenses a plane when it explains ≥50% of
  block variance, then renders false ramps across sharp edges while its
  own trace records 28.9% strong-edge pixels; ±1–2 LSB perturbations flip
  operators in 8/12 close-call regions with 50–95× output amplification;
  no margin is recorded.
- C1 (+1.11 dB mean, 10/11) died on a −0.15 dB single-image floor after a
  −0.36 dB building regression. The floor was set at noise magnitude
  (ordinary per-image jitter is ±0.3 dB) — a miscalibrated tail guard.
- C2 (lineage-vouched cascade) was VOID: per-atom source-image provenance
  exists only in the human-readable TEACH_TRACE.txt, never in the VOC2
  binary the matcher reads (3-way byte-exact audit: zero room).
- The deepest cross-round signal: the biggest gains came from NOT stamping
  learned atoms (C1 reverting to lines+means, C3's pure-measured plane).
  The learned vocabulary may be the binding problem.

## Mandate for round 4

Four preregistered arms, each testing one causal question. No combinations,
no threshold tuning, no vocabulary swaps, no post-result mechanism changes.

## Arm P1 — PLANE-only (active-ingredient isolation)

**Question:** is the deliberated operator choice decorative?

**Mechanism:** take the committed round-3 C3 source and pin the chooser to
PLANE-FIT for every region that reaches operator choice (regions C3 would
MEAN-fill also get PLANE — "fit planes everywhere"). Everything else —
matching, recursion, split logic, gain bar, LINES — byte-identical to C3.

**Why this is the decisive experiment** (z.ai's kill experiment): with
ATOM at 3.7% of area its aggregate contribution is capped ≈0.1–0.15 dB
no matter how good the stamps are, so ≥85% of C3's +0.955 dB is already
"PLANE/MEAN instead of baseline stamping". Forcing PLANE everywhere
isolates the active ingredient and measures the ceiling of the entire
research line.

**Preregistered readings:**
- P1 mean Δ within ±0.10 dB of C3's +0.955 → the deliberation is
  decorative or harmful; the C3 authorship claim dies; the mechanism is
  "fit planes".
- P1 < C3 by >0.10 dB, concentrated on ATOM-heavy textured images →
  the deliberation premium is real and finally quantified; the claim
  survives in stronger form.
- P1 vs bicubic (column below) = the ceiling this research line can
  ever reach with this operator family.

P1 is diagnostic: it cannot "win" BAR 1 as a shippable mechanism (it is a
degenerate policy), but its numbers adjudicate C3's claim.

## Arm P2 — lineage-vouched cascade, for real (VOC3)

**Question:** does restricting fine-scale matching to the parent winner's
source image cut key ambiguity? And: does the learned vocabulary earn its
keep at all?

**Feasibility dry-run FIRST (preregistered gate):** the implementer must
demonstrate, before any battery run, that a VOC3 binary vocab format can
carry a per-atom source-image index that `g_vocab_load` reads — i.e.
parse VOC2 byte-exactly, emit VOC3 = VOC2 + per-atom source index sourced
from TEACH_TRACE.txt, reload it, and byte-verify atom payloads unchanged.
If the dry-run fails, P2 is VOID (reported, not worked around) — VOID may
not quietly drop the most informative arm a second time without a finding.

**Mechanism** (if dry-run passes): top scale (S=64) matching unchanged
(full vocabulary). At every finer scale, a block's candidate atoms are
restricted to atoms whose VOC3 source-image index equals the parent
block's winning atom's source-image index. Parent NO-FIT or empty
restricted set → full vocabulary. Gain bar, split logic, construction,
LINES otherwise byte-identical to baseline. Atoms render via the baseline
ATOM-STAMP construction.

**Preregistered vocab-abandonment bar:** after scoring, run the P2 binary
a second time with atom-takes rendered as PLANE-FIT instead of ATOM-STAMP
(same take geometry, forced render — a deterministic analysis mode, not a
new mechanism). If mean Δ(P2 − P2-with-plane-on-atom-tiles) ≤ 0 over the
battery, the learned vocabulary's marginal contribution in the winning
configuration is non-positive → **the vocabulary is retired** and the
line pivots to measured-only construction. This bar is binding on the
program, not advisory.

## Arm P3 — inverted architecture (measured base, atoms as licensed residuals)

**Question:** is atoms-as-base the wrong polarity? (z.ai's honest pivot.)

**Mechanism (frozen):** base construction is the measured ladder — per
region, PLANE-FIT if the least-squares plane residual ≤ e/2, else
MEAN-FILL (the same honest rule as C3's non-atom path, unchanged).
Then, atoms as licensed residuals: for regions where the structural
license holds (f ≤ 1/4 AND m ≥ 2 — the C1/C3 bars, recorded here, not
fit), AND the winner atom's full-res deviations over the measured base
reduce the measured residual energy on the block's observed pixels
(honest improvement, measured on real pixels, never imagined), stamp the
atom's deviations ONTO the plane/mean base. The atom never replaces the
base; it only refines it. Regions failing either condition keep the
measured base.

**Why broad:** inverts the construction polarity at every region on every
image — measured-first instead of atoms-first. Directly tests whether the
vocabulary's only honest role is residual refinement.

## Arm P4 — C1′: license gate with PLANE fallback

**Question:** did C1 die of the floor or of its fallback?

**Mechanism:** C1's match-time license gate unchanged (f ≤ 1/4 AND m ≥ 2
→ ATOM-STAMP, byte-identical to committed azgen_c1.zag). Unlicensed takes
fall back to PLANE-FIT (not the baseline NO-FIT mean+lines path). This is
the round-4 answer to the confounded C1-vs-C3 comparison (different
fallback sets): it separates "licensing as an idea" from "mean-fill as
a fallback". Record explicitly: preferring any arm over C1′ is a
worst-case-vs-mean risk-posture choice, not a finding that C1′ is the
better mechanism, unless the sealed battery says otherwise.

## Floor calibration (protocol change, preregistered)

The round-3 −0.15 dB single-image floor is replaced by a **−0.50 dB**
floor. Rationale, stated before any run: ordinary per-image jitter of any
mechanism is ±0.3 dB; a floor at noise magnitude randomly kills decent
mechanisms. −0.50 dB is real-harm magnitude — the disease is −14 dB
tiles, not −0.36 dB images. Risk posture (explicit): we ship mechanisms
with no real harm; a −0.5 dB single-image regression is signal, not
noise. Note for the record: under this floor, C1's building −0.36 dB
would NOT have killed it — the round-3 kill stands on round-3's terms,
but the floor is recalibrated for cause, not to resurrect C1.

## Batteries (frozen)

- **DEV battery (11 images):** the round-3 battery (bridge, sky, fabric,
  woodgrain, treebark, calmwaters, portrait, car, building, cat, market)
  with the committed baseline PSNRs. This battery adjudicated 3 rounds
  and fed the white-box diagnosis that shaped every mechanism — it is a
  DEV SET now. It runs for continuity/comparison only; no generalization
  claim may be made from it.
- **SEALED battery (new):** fresh real photos, never used in rounds 1–3,
  never in vocab teaching, sealed from implementers (implementers get
  dimensions only). Target ~8–10 images across texture / smooth / people
  / object / animal / mixed. Sealed SHAs recorded in the manifest before
  any arm runs. ALL generalization bars are scored on the sealed battery.
- **Bicubic column:** every image on both batteries is also scored with a
  frozen bicubic 2× upsample of the box-downscaled LR input (deterministic
  reference implementation, documented). This is the comparator round 3
  never reported. Per-image tables publish baseline / arm / bicubic.

## Bars

- **BAR 0 (validity):** pristine `azgen.zag` recompiled reproduces the
  committed baseline output SHAs (bridge gen 2028ba1d…, sky gen
  84255819…) and all 11 dev PSNRs within ±0.02 dB. If not, the build
  pipeline is broken — stop, score nothing.
- **BAR 1 (broad win — the mandate, sealed battery only):** candidate
  mean ΔdB over sealed images ≥ +0.50 dB AND wins ≥ 80% of sealed images
  AND no single sealed image < −0.50 dB vs baseline AND every
  category-group mean ΔdB ≥ 0. No trading portrait for bridge.
- **BAR 2 (originals, dev battery):** bridge and sky each ≥ baseline −
  0.10 dB.
- **BAR 3 (vocabulary, binding):** the P2 abandonment analysis fires or
  it doesn't, per the rule above. If it fires, the line pivots to
  measured-only construction regardless of which arm wins BAR 1.
- **Red-team gate (independent, after scoring):** category-shift traps
  (the round-3 killers: diagonal step, circle, gradient+step), close-call
  ±1–2 LSB perturbation amplification, operator neutering, hardcode
  audit, sealed-image leakage audit. Any arm that wins BAR 1 but fails
  the red team is KILLED, not shipped.
- **Eyes gate:** before any victory is declared, a self-contained
  data-URI gallery of side-by-side crops (candidate vs bicubic vs
  baseline) on texture images. Micah's eyes outrank the metrics; MSE
  rewards smear.
- **KILL (program):** no arm passes BAR 1 on the sealed battery → round 4
  is killed; honest loss with mechanism analysis. Post-result tuning →
  void.

## Method notes

- Pure Zag, zero RNG. Pinned toolchain
  ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
- Byte-identical reruns: every binary runs every image twice (fresh
  outdirs) plus allocator-perturbation runs (env -i, padded env,
  different cwd); upscale_gen.bmp SHAs compared.
- Deterministic reference only: the bicubic column may be computed in
  Python (PIL, deterministic) — it is a comparator, not a candidate.
- No commits by implementers (coordinator commits). No binaries, .zagd,
  caches, or rendered images in repo dirs. Build in scratch; delete
  binaries after scoring. Disk is at ~98% (2.8G free) — keep workdirs
  lean, clean staging after each phase, check `df -h ~` before heavy
  runs.
- Sealed-battery discipline: implementers never see sealed pixels.
  Battery runner applies frozen binaries to sealed images and publishes
  per-image tables. Any sealed-image SHA found in any prior artifact →
  the seal is broken; report and resample.
- znc gotchas (recorded): no `};` after a closing brace; never name an
  identifier `try`; `@import` resolves relative to the importing file;
  `nio_alloc` takes BYTES; `as []i32` consecutive same-size casts ALIAS
  (use []u8 arenas + LE accessors); define callees before callers
  (forward refs compile to corrupt binaries); `.*` on non-pointers
  segfaults; audit every large allocation against the 2^25-byte slice
  ceiling.
