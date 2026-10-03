# FU03 NOTE — follow-up test

## Follow-up instruction (verbatim)
"change the primary button color to green"

## Change applied
- style.css lines 48-49: `.btn-dark { background: var(--ink); ... }` →
  `.btn-dark { background: #2e7d32; ... }`; hover `#1a1815` → `#256428`.
- Scope decision: "the primary button" was read as the hero's main CTA
  ("Start a session"), the only `.btn-dark` on the page. The accent-orange
  buttons (nav "Start focusing", CTA "Try the live timer") were left alone —
  recoloring `--accent` would have dragged the eyebrow, step numbers, card
  icons, and brand mark along with it (scope violation).
- No other files touched.

## Verification

### (1) Change visible? YES — LANDED
- Chrome browser.png and frozen view.png both show the hero "Start a session"
  button in a clear, readable green. White text on it remains legible.
- Nav "Start focusing" and CTA "Try the live timer" buttons are still orange
  (unchanged), and all other page elements are pixel-identical vs fu02.

### (2) Nothing else broke? YES
- Deterministic render: render.img and render2.img SHA-256 identical
  (c6d09a221383d5fe9d7b4b59b19f37af0d2691e27c6c22db412eb333a2b).
- Judge2 (reps a/b agree): **GOOD 896, zero defects** — unchanged from fu02
  (896→896). No new defects.
- Proxy blind A(fu03) vs B(fu02): all structural measures identical
  (bands 9/9, type_modes 4/4, contrast 2.901/3.144, align_modes 8/8); only the
  expected color signals move: satcov 0.0056→0.0114 and judge m_hues 1→2 —
  the green itself. Exactly the intended change.

### (3) Scope clean? YES
- `diff -u` fu02 vs fu03: exactly 2 lines changed in style.css (the .btn-dark
  background and its :hover). index.html and app.js byte-identical to fu02.

## Scores
- Judge: 896 → 896 (GOOD, zero defects both)
- Proxy: neutral except expected saturation/hue delta from the new green

## Verdict: LANDED
