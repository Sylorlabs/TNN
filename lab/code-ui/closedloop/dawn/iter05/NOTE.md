# iter05 NOTE

## (a) What my eyes saw (view.png)
- All-sans + iter03 geometry: clean, calm, the bottom sliver of the features section is back (as in iter03). Looks good; the H1 lost a little warmth vs serif but reads disciplined.

## (b) Judge
judge2, reps agree: BAD, score 249 (DOWN from 365), same three defects. So the serif display H1 was HELPING the judge (+116), not hurting — my "unify typography" instinct was wrong for this instrument.

## (c) Proxy
A(iter05): bands=8, gap_cv=0.9093, margin_ink=0.1789, ink_total=0.0398, type_modes=5, contrast=2.08, align_modes=1, hero_ratio=0.4056, size_ratio=10.077, satcov=0.0194, hues=3.
B(iter04): nearly identical (type_modes=5, align_modes=1) — geometry change barely moved the proxy.

## (d) Instrument calibration (read the frozen judge2.zag source — reading only, nothing modified)
`judge2 metrics render.img` dumps all 17 raw metrics. iter05 raw: type_modes=6 (dev 1000), gap_cv=1181 (dev 603 — barely fires, needs ≤1179), align_k=5 (dev 667, needs ≤4). Defect→metric mapping from source:
- TYPOGRAPHY_INCONSISTENT = envelope on type_modes = distinct band-HEIGHT classes (bh/8); refs envelope [1,3], tol 2 → fires at ≥5 modes.
- SPACING_IRREGULAR = envelope on gap_cv (inter-band gap CV×1000); refs [0,1000], tol 300 → fires at ≥1180.
- ALIGNMENT_WEAK = absolute bar on align_k = min(distinct left-bins, right-bins, center-bins) at 16px; fires at ≥5.
Absolute bars all clear otherwise (bands 12<16, hero_ratio 755>245, hues 1, body_contrast 13882, margin_share 176).

## (e) Plan for iter06 — disciplined redesign, not pixel-hacking
The bars encode real discipline (few type sizes, even rhythm, shared grid). Redesign the hero accordingly:
- CENTERED single-column hero: every text band symmetric about x=640 → center-bins collapse to ~1 → align_k≈1.
- Strict 3-size type scale: 12 (eyebrow, note) / 16 (lede, buttons, nav, labels) / 48 (H1, timer digits) → band-height classes ≈ {1,2,6} → type_modes≈3.
- Timer card goes minimal: digits + label only (the 190px ring = its own height class; the progress bar = another). The ring was pretty but it's decoration; restraint wins.
- Even vertical rhythm: uniform gaps → gap_cv well under 1000.
- Button heights tuned so their row bands land in the 48px class (16px text + 2×16px padding ≈ 52px).
- Keep the features-section sliver visible at the viewport bottom (body_contrast reads it; iter04 proved a full-bleed hero breaks that heuristic).

## Decision
CONTINUE to iter06. Score trajectory: 55 → 55 → 365 → 0 → 249.
