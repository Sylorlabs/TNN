# VERDICT — upscale concept probe → teach → re-probe

**Date:** 2026-09-26. **Gate: PASS — concept HELD.**

## Result

TNN holds the behavioral upscale concept C1–C4. Teach committed 4/4 features
unanimously from measured pairs; on 4 held-out cases (incl. a real GT crop)
the taught knowmap ACCEPTed every correct upscale and REJECTed all 16
violators, each by its target feature:

| Feature | Concept | Held-out result |
|---------|---------|-----------------|
| F1 (C1) | 2× dims = 4× pixels | correct ACCEPT 4/4; v_dims REJECT 4/4 — HELD |
| F2 (C2) | same content, same alignment | v_shift REJECT 4/4 (shifts identified exactly); correct peak (0,0) unique 4/4 — HELD |
| F3 (C2/C3) | no new objects | v_object REJECT 4/4 (resid 5126–11250 ≫ 2000) — HELD |
| F4 (C3/C4) | detail only from knowledge | v_invent REJECT 4/4 (q up to 10696 ≫ bar 1432) — HELD |

**Generation-path work is UNBLOCKED** on the concept gate — with the recorded
scope below.

## What TNN chose vs what the crew fixed

- **TNN chose:** the commit/revert of all 4 features (computed unanimity over
  measured affinities) and the F4 bar **1432 = 2 × 716** (derived from the
  worst true-detail pair, not a crew constant).
- **Crew fixed (labeled, not passed off):** the measurement code (M1–M3),
  the unanimity rule, F3's 2000 predicate (frozen prereg), fixture synthesis.
- **Trace honesty:** `[MEASURED]` = computed; `[RULE]` = predicate-guarded
  wording; `[DELIB]` = the *selections* are computed, sentence templates fixed.
  No crew-authored prose is presented as TNN reasoning.

## Scope and limitations (not hidden)

1. C4's full pixel-value line test applies to TNN's own future constructions;
   the probe verifies its detectable consequences (M2b+M3).
2. F4 (global HF ratio) is the weakest discriminator: on textured images the
   ±30-stripe violator needed amplitude 50–60 to separate cleanly. The taught
   bar (1432) held on all held-out cases, but a subtler fabrication on a
   noisier image could pass — future generation work should strengthen the
   detail-coherence check (e.g. local/smooth-region-gated).
3. Fixtures are synthetic + one real crop; the concept is behavioral, not a
   claim about natural-image statistics at large.

## Determinism

Every stage ran twice; all outputs byte-identical (`diff -r` + sha256).
Pure Zag, zero RNG.
