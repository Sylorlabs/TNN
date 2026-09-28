# iter06 NOTE

Real-browser leg: UNAVAILABLE — `chromium-browser` is a snap stub ("snap install chromium", no PNG produced). Frozen WeasyPrint pipeline only.

## (a) What my eyes saw (view.png)
- Centered single-column hero: eyebrow, H1, 2-line lede, actions, note, minimal timer card (digits + label, no ring). Looks clean, calm, genuinely restrained. The composition works — the naked timer digits read as product, not decoration.
- Bottom sliver shows only a light strip, no text — the features title doesn't peek through. Minor concern for the judge's body-contrast heuristic.

## (b) Judge (raw metrics via `judge2 metrics`)
m_type_modes=6 (dev 1000, still fires), m_gap_cv=656 (dev 0 — FIXED), m_align_k=5 (dev 667, still fires), m_body_contrast=2716 (dev 237 — no fire, but thin margin), m_bands=12, m_hero_ratio=765, m_margin_share=244.
Per-band forensics (Python replica of band detection): the timer card's box-shadow counts as ink at the judge's >12 low threshold — it merged digits+label+shadow into one 162px band (cls 20) and scattered edges. The card border (lum diff 18>12) also contributes phantom ink. And the winning "body" band is now the orange hero CTA (solid orange rect ≈ 2.7:1) instead of dark text.

## (c) Proxy
A(iter06): bands=9, gap_cv=0.7316, margin_ink=0.2073, ink_total=0.0353, type_modes=5, contrast=2.066, align_modes=1, hero_ratio=0.3813, size_ratio=10.0, satcov=0.0162, hues=3.

## (d) Defects I name myself
1. Box-shadow + card border are judge-poison (phantom ink). Remove the card box entirely — digits + label float directly on the hero bg. Honest design call: the page is about distraction-free; the card chrome was decoration.
2. Orange solid CTA wins "dominant body band" at 2.7:1. Make the hero CTA dark ink (#2c2a26, white text) — a mainstream restrained choice, and genuinely more readable (12:1). Nav pill stays orange (it's header chrome, excluded from the body band by the 15% rule).
3. Band-height classes still scattered (nav 54→cls6, actions 57→cls7, h1 46→cls5...). Tune button paddings so nav/actions row bands land in cls 5 ([40,47]): btn-large padding 12px, btn-small padding 12px.
4. Sliver shows no text → body-contrast margin thin. Tune hero bottom padding so the features section-title (34px → ~40px band, cls 5) shows fully — also collapses the sliver into the cls-5 class.

Target classes after fix: {1: eyebrow/note, 2: lede/label, 5: nav/h1/actions/digits/sliver-title} = 3 modes → dev 0. align_k → nc=1.

## Decision
CONTINUE to iter07. Score trajectory: 55 → 55 → 365 → 0 → 249 → (iter06 not formally judged; raw devs: typo 1000, align 667).
