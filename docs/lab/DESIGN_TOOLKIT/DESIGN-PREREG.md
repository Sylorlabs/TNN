# DESIGN TRACK PREREG — 2026-09-21/22 (go-time)

## Question
Can TNN implement its designs in its head? I.e., hold a full UI design as an
internal model, reason about it (answer queries) without rendering, then emit
professional-quality renders — in two aesthetic versions: its OWN taste vs its
model of HUMAN taste.

## Deliverables
1. **Toolkit** (`design/toolkit.zag`): pure-Zag UI toolkit — canvas, 5x7 bitmap
   font (integer-scaled), primitives (rect, rounded rect, circle, line, text),
   components (button, textfield, listrow, card, navbar, tabbar, dialog,
   toggle, slider, progressbar, avatar). Every pixel from Zag. Renders 24-bit BMP.
2. **Mental model**: the design spec table (component records: screen, type,
   x,y,w,h, label, style). The renderer AND the query engine both consume it
   through independent code paths. "In its head" = queries answered from the
   spec table without rasterizing.
3. **V1 design** = TNN's own aesthetic opinion: a DETERMINISTIC scoring function
   in Zag scores a grid of candidate parameter sets (corner radius, spacing,
   palette, type scale, shadow, density...); the winner is rendered. No human
   taste injected into V1's selection.
4. **V2 design** = grok-4.7's model of human taste (parameter set chosen by
   grok deliberation, documented rationale).
5. **App**: music player, 3 screens (Library, Now Playing, Settings) x 2
   versions = 6 PNGs + component sheet, in `~/workspace/your_files/imagination_design/`.
6. **Difference map**: where/why V1 and V2 differ — a finding about TNN's
   aesthetic theory of mind.

## Bars (binding)
- B-D1 determinism: two clean renders of every artifact byte-identical (16/16).
- B-D2 in-head accuracy: >=90% of preregistered queries answered consistently
  between the query engine and the rendered pixels (independent verifier).
- B-D3 purity: 100% of delivered pixels from Zag; BMP->PNG conversion is
  transport-only and verified pixel-identical.
- B-D4 quality: professional quality judged by Micah's eyes (binding,
  subjective). Not Google-Slides level: real layout grid, consistent spacing,
  type hierarchy, component consistency, contrast.
- B-D5 V1 integrity: V1's parameter set must be the argmax of the Zag scoring
  function over the preregistered candidate grid — provable from source, not
  crew taste.

## Method notes
- grok-4.7: reasoning/design/analysis (grok-first tonight). Native Muse work:
  Zag builds + verification only.
- Fallback chain: grok-4.7 -> native -> gpt-5.6-sol (unorouter). All fallbacks logged.
- Red-team: grok agents attack V1/V2 for inconsistencies and amateur tells.
