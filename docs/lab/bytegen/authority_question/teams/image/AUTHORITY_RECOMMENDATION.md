# AUTHORITY_RECOMMENDATION — image

Team Image, 2026-09-23. Recommendation first, steelman of the opposition
second (so the work is auditable), then the rule stated precisely.

## Recommendation

**Image gets an image-specific instantiation of the three-piece pattern:
Pieces 1 + 2 active, Piece 3 empty (audited, not assumed).**

> **Image authority rule.** The plan is the sole authority over all
> content. Rendered pixels earn authority only on the exception path:
> measured bytes may be READ to detect a fault, and damaged bytes may be
> REPLACED — with plan-pure re-renders only. They may never set a
> parameter, choose content, alter layer/stroke order, or move a global
> gain. The plan keeps last word by construction: correction is
> re-assertion, never arbitration.

The three pieces, instantiated for image:

- **Piece 1 — plan path (default, always).** Every pixel is a pure
  function of the plan: Path C `px = F(seed, x, y)` (disc.zag :767/:940);
  Path A `px = raster(strokes[0..n], x, y)` (field.zag :1233/:2257);
  Path B `px = replay(op_sequence)` (toolkit.zag, render.zag :34).
  Sole authority over: stroke/layer existence, order, geometry, color,
  alpha, seeds, dither, grain. `d_blend`'s pixel read-back is classified
  as a Piece-1 rendering operator (PATH_MECHANICS.md settlement), not
  feedback — no authority question attaches to it.
- **Piece 2 — exception detect-and-reassert (idle; fires only on
  fault).** Region-scoped. Detection: re-render the region to scratch
  and diff (bit-exact), or region checksum vs plan-derived expectation.
  Correction: overwrite with the plan-pure re-render — for Path B this
  means replaying ALL layers in order over the region (d_blend operands
  stay plan-determined); for Path A replay the stroke log into a fresh
  arena (never correct forward from corrupted cells). Correction map
  constant in the corruption: Lipschitz 0, idempotent, one-step
  convergence. False positive = no-op.
- **Piece 3 — discrete latch: EMPTY for image.** Audio's latch exists
  because RESPOND reacts to a measured external stimulus (the cue's
  pitch) — a discrete plan-level fact with a quantized sensor. Image
  has no external-stimulus analog: the image plan (strokes, seed, theme)
  is fully authored before rendering begins. The slot is reserved and
  documented empty; filling it would require a preregistered, Micah-signed
  finding of a genuine discrete measured-plan-fact in the image line.

---

## Steelman: the case FOR image feedback (opposition, strongest form)

1. **"d_blend is precedent."** Image already reads output bytes during
   generation; a bounded continuous controller on rendered pixels
   (contrast servo, seam smoother) is a natural extension of an existing
   read-back, not a new architectural sin.
2. **"Aesthetic self-correction."** TNN could look at its render and fix
   real defects: text illegible on its background (c_button draws text
   over accent colors), muddy contrast, banding. A plan can't foresee
   every bad interaction; eyes on the output close the loop.
3. **"The AVI normalizer is precedent."** Native code already grants
   output feedback authority (`f3_emit_wav` :1025–1039 peak→28000,
   `f3_emit_wav_hifi` :1166–1184 ×24000/peak, `f3_emit_avi_g`
   soundtrack). Feedback authority is not foreign to this codebase.
4. **"Seams need eyes."** Only by measuring the rendered image can you
   find unintended seams; the plan doesn't know they appeared.

## Rebuttal (why the steelman fails, point by point)

1. **Precedent refuted by classification.** PATH_MECHANICS.md settles it:
   d_blend is data flow with a plan-fixed operator, not control flow over
   measured output. Extending it into a controller changes the category,
   not the degree — like arguing that because a mixer *adds* signals it
   may also *judge* them. The survey's AR criterion (output bytes as
   semantic input deciding later content) is failed by d_blend and would
   be satisfied by any servo: that is precisely the line.
2. **Aesthetic self-correction = audio Attack 1 in costume.** A contrast
   servo needs a target (e.g. minimum luminance ratio). That target is a
   frozen constant measured from some tuning set — on a plan that
   *deliberately* uses low contrast (f3_gen_g4 "harbor lights": near-black
   water; g6 dark ground), the servo permanently fights the plan toward a
   constant the plan didn't author. The honest path: the plan author
   (deliberation, red team, Micah's eyes) revises the plan. Thermometer
   before thermostat: feeling/evaluation may *read* the render, but the
   renderer must not *steer* by it. Plan keeps last word; no arbitration.
3. **The AVI normalizer is a cautionary specimen, not a license.** It
   exhibits exactly the gamma.zag disease: one corrupted sample moves
   `peak`, so every sample's gain shifts; content edits break bit-identity
   globally; detection targets become output-derived and ill-defined
   (FAULT_ANALYSIS §F3). It survives as a *post-pass mastering choice*,
   not as generation authority — and the recommended rule would flag it
   for plan-derivation or removal, not extend its logic to pixels.
4. **Seams: intent is plan-side.** Unintended vs authored seams are
   indistinguishable in the measurement (FAULT_ANALYSIS §F4) — the arch's
   over/under signal IS seam shading. A seam servo erases content. And
   genuine defect seams (tears) are F1 region faults: plan-pure re-render
   heals them with no seam-specific authority.

## Steelman: the case for "no feedback, plan absolute" (strongest form)

Simpler rule, smaller attack surface, zero new machinery: rendering is
already deterministic and byte-identical; every fault the battery can
name is either prevented by construction or healed by replay; admitting
even exception-path measurement invites scope creep back toward the v1
servo. The AVI normalizer shows how easily "just a post-pass" becomes
load-bearing.

## Why plan-absolute loses

Because detection without correction is abdication. F1/F2 faults are
real (bit-rot, torn tiles, mid-render cell corruption) and plan-pure
replay heals them to 0 differing bytes at bounded, one-shot cost. A
plan-absolute rule leaves detectable, healable faults unhealed — and
worse, gives no *alarm*: the corrupted image ships to Micah's eyes
silently. The audio battery already proved exception-path re-assertion
exact and safe (64-sample bit-flip, full-block dropout, 1292-block
sustained corruption → 0 differing samples). Image's case is strictly
stronger: detection can be bit-exact (no band floor), and Path C needs
no ordering discipline at all. Refusing Piece 2 buys nothing and costs
healable failures.

## Final rule (frozen wording for the prereg)

1. Plan is sole authority over content, order, parameters, gains.
2. Exception path only: measured pixels may be read **to detect** a
   fault; damaged regions may be overwritten **with plan-pure
   re-renders only** (full layer/stroke replay from the plan, never
   forward correction from corrupted state, never neighbor-matching).
3. No output-derived global gains, ever (the four native peak
   normalizers are grandfathered post-pass mastering, flagged for
   plan-derivation review — they are not generation authority and not
   precedent).
4. No continuous servo on rendered pixels, of any target, with any
   dead zone.
5. Piece 3 slot audited empty for image; filling it requires a frozen
   prereg amendment with a demonstrated discrete measured-plan-fact.
6. d_blend (and field-level f3_blend) remain Piece-1 rendering
   operators; their read-back confers no authority and sets no
   precedent.
