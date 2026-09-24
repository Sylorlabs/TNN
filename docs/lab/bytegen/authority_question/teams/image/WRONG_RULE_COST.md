# WRONG_RULE_COST — what breaks if the rule is wrong, each direction

Team Image, 2026-09-23. Concrete failure modes, mechanistically traced,
no hypotheticals without a mechanism.

## Direction 1: feedback admitted where none belonged

### 1a. Continuous pixel servo (brightness/contrast chasing frozen targets)
**What breaks:** the servo's target is a constant measured from some
tuning render (audio Attack 1, v1's RMS-0.19/ZCR-0.016 literals). On
`f3_gen_g4` "harbor lights" (near-black water, spec'd in the plan) the
servo permanently fights the plan toward mid-gray — the render converges
to a scene the plan never authored, and the stroke log no longer
describes the output. Every dark or low-contrast scene in the G-series
(g1 ember coast night water, g6 dark ground) is distorted the same way.
**Cost:** plan authority destroyed silently; the battery's K2 (no harm
on clean output) fails by design, not by accident. This is not a tuning
problem — no target constant is correct for all plans, and a plan-derived
target is just Piece 1 with extra steps.

### 1b. Seam/artifact smoother (gradient-driven)
**What breaks:** the impossible triangle (disc.zag arch) carries its
cyclic over/under *entirely* in seam shading — highlight lip on the
winner's side, dark seam + contact AO on the loser's (:809–939 design
comments). A gradient smoother measures exactly these features as
"defects" and blurs them. The render becomes three flat beams with no
readable over/under: the one property the scene was built to demonstrate
is erased. Same for stroke occlusion edges (g2's foreground mullion over
lamp glow — depth signal gone). **Cost:** content destruction the plan
cannot veto, because the destroyer outranks the plan. Intent is plan-side
only; measurement cannot recover it.

### 1c. Output-derived global gain (the native specimen, scaled up)
**What breaks:** the four grandfathered peak normalizers (`f3_emit_wav`
:1025–1039, `f3_emit_wav_hifi` :1166–1184, `f3_emit_avi_g` soundtrack)
already show the mechanism: gain = f(rendered output). One corrupted
sample moves `peak` → every sample rescales → a single-tile fault is
amplified to a full-image fault. Extend this philosophy to pixels
(auto-contrast/auto-levels post-pass) and: (i) any content edit shifts
every byte (bit-identity across edits dead — the AGENTS.md gamma.zag
note documents this exact death); (ii) detection targets become
ill-defined, because "plan-expected output" is now a function of the
possibly-corrupted output (FAULT_ANALYSIS §F3); (iii) fault localization
becomes impossible — the fault's signature is smeared across the whole
frame. **Cost:** the exception path (Piece 2) is structurally disabled;
you cannot heal what you cannot localize.

### 1d. Forward compensation (correct the future for the past)
**What breaks:** damaged tile detected → clean neighboring tiles
brightened/sharpened to "make up for it." The damaged bytes are already
rendered; the compensation distorts clean pixels that were correct.
After the fault is repaired (or in the next render without the fault),
the compensation's rationale is gone but its effects persist if any
state carried them — and even one-shot, the shipped image contains
distortion the plan never authored. Audio Attack 6's verdict transfers
verbatim: causally wrong. **Cost:** clean output corrupted *by the
corrector*; K2 fails.

### 1e. The involution class (carried gain updated from measured output)
**What breaks:** any controller of the form `g ← f(g, measured)` with
`f(f(g)) = g` structure (audio Attack 4's `g ↦ clamp(T/(g·S))`, f′=−1 at
the fixed point) admits sustained 2-cycles and rail pins constructible
from plan text alone. In image: a per-tile auto-exposure gain updated
from measured tile means would 2-cycle on alternating tile patterns
describable in a stroke log. Magnitude clamps bound the output bytes,
not the history-dependence — the cycle lives in the controller state.
**Cost:** non-terminating, plan-independent behavior in the renderer;
determinism of *content* technically preserved (bytes are deterministic
given the cycle) but the image becomes a function of controller history,
not of the plan. Byte-identical reruns still pass while the image
drifts from the plan's intent across renders — the worst failure mode:
silent.

### 1f. Scope creep (the meta-failure)
**What breaks:** "just a post-pass" becomes load-bearing. The AVI
normalizer was presumably "just mastering"; it now determines every
output byte's value as a function of global content. Each admitted
feedback is precedent for the next; the v1 audio servo was deleted, not
bounded, for exactly this reason (HYBRID_SPEC §6). **Cost:** the
authority question re-litigated per incident instead of settled once.

## Direction 2: plan-absolute imposed where feedback was needed

(Plan-absolute = detect-only or nothing; Piece 2 refused.)

### 2a. Unhealed dropouts ship to Micah's eyes
**What breaks:** FM-2 (128×128 zeroed tile) persists in the emitted BMP.
There is no mechanism that even *notices* — detect-only without
correction is an alarm nobody answers. A torn tile in a deliverable
image is a visible defect with a known exact cure (0 differing bytes via
re-render) deliberately withheld. **Cost:** quality failures that are
both detectable and healable, left in the artifact.

### 2b. Mid-render carried-state corruption propagates
**What breaks:** FM-4 — cells corrupted after stroke 10 of 20. Every
later stroke blends against corrupted cells (`f3_blend` reads them);
the raster then bilinearly interpolates corruption across the whole
frame. Without Piece 2's replay-from-plan, the only options are
ship-it or re-render-the-world-manually. **Cost:** a fault class with
an exact, cheap, one-step cure becomes a full manual re-run or a
corrupted deliverable.

### 2c. Silent bit-rot in stored/emitted files
**What breaks:** post-render buffer damage (FM-1/FM-3/FM-5) between
render and write, or in an archived BMP, is never caught. The plan says
X; the file says Y; nothing reconciles them. **Cost:** the ledger's
"truthful, not hiding" standard (MEMORY.md wave-5 verdicts) fails at
the byte level — TNN ships bytes it believes are plan-pure and they
aren't.

### 2d. No honest floor for "small" faults
**What breaks:** under plan-absolute, sub-threshold flips (FM-5) are
*by definition* unactionable — but bit-exact detection (F1) could have
caught and healed them for free. Refusing Piece 2 doesn't buy
simplicity here; detection-via-rerender is the same code path as
correction. **Cost:** leaving exactness on the table for no gain.

## Asymmetry note

Direction 1 failures are **active corruptions**: the renderer damages
clean output, destroys authored content, or disables healing — and the
worst (1e) is silent. Direction 2 failures are **omissions**: healable
faults go unhealed. Both are real, but they are not symmetric: 1e-style
silent drift from plan intent is strictly worse than 2a-style visible
defects, because visible defects get caught by Micah's eyes (the final
oracle) while silent drift passes every metric. This asymmetry is why
the recommended rule admits feedback *only* in the Lipschitz-0,
one-step, idempotent form: the exception path is engineered so that
even its failure mode (false positive) is a no-op.
