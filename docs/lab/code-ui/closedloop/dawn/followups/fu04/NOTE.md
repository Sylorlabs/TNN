# FU04 NOTE — follow-up test

## Follow-up instruction (verbatim)
"add a footer with a copyright line"

## Change applied
- index.html lines 87-89: the footer's right side ("Made for quiet mornings.")
  was grouped into `<div class="foot-copy">` and a second line added:
  `<p>&copy; 2026 Dawn. All rights reserved.</p>`. Brand block untouched.
- style.css line 122: added `.foot-copy { text-align: right; }` (the existing
  `.foot-inner p` rule already styles both lines).
- app.js untouched.

## Verification

### (1) Change visible? YES — LANDED
- IMPORTANT CAVEAT: the frozen render pipeline renders only the above-fold
  region — fu04's render.img is BYTE-IDENTICAL to fu03's (SHA-256
  c6d09a221383d5fe9d7b4b59b19f37af0d2691e27c6c22db412eb333a2b, render.img =
  render2.img). The pipeline cannot see the footer at all.
- Verified with my own eyes on a full-page real-Chrome screenshot
  (fullpage.png, 1280x3000): the footer now shows the Dawn brand on the left
  and a right-aligned two-line block — "Made for quiet mornings." above
  "© 2026 Dawn. All rights reserved." Styled consistently (same 14px
  ink-soft type), coherent with the page, no overlap, nothing broken.

### (2) Nothing else broke? YES
- Judge2 (reps a/b agree): **GOOD 896, zero defects** — identical to fu03
  (896→896), as expected since the frozen render is unchanged. No new defects.
- Proxy blind A(fu04) vs B(fu03): all twelve measures byte-identical —
  the change is below the pipeline's field of view.
- Rest of page verified via fullpage.png: hero (bigger headline, green
  button, extra padding), cards, steps, CTA panel, and footer all intact.

### (3) Scope clean? YES
- `diff -u` fu03 vs fu04: footer markup gained the copyright line (3 added
  lines, 1 removed) + one CSS rule (`.foot-copy`). app.js byte-identical.
  No unrelated sections touched.

## Scores
- Judge: 896 → 896 (GOOD, zero defects both; render unchanged by design)
- Proxy: identical (change is outside the pipeline's viewport)

## Verdict: LANDED
