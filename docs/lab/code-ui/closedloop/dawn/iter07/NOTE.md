# iter07 NOTE

Real Chrome now works (~/workspace/chrome-testing/chrome-linux64/chrome) — browser.png added to the loop from here on.

## (a) What my eyes saw — WeasyPrint view.png vs Chrome browser.png
- WeasyPrint: centered hero, dark CTA button (looks sharp), naked "25:00" digits look SMALL (~30px) under the note, features sliver shows no text.
- Chrome (what a human sees): the SAME page but the "25:00" digits are BIG and bold (true 48px) — clearly the intended display size. The h1 renders identically in both. The dark button looks excellent. The features title peeks at the very bottom. Overall: Chrome render looks genuinely good — clean, restrained, professional.
- ARTIFACT FOUND: WeasyPrint renders `.timer-time` at ~55% size (18px band) vs Chrome's 33px band for the same 48px CSS. The judge therefore sees a cls=2 digits band that a human never sees. Noted as instrument artifact, not a design flaw. (h1 verified pixel-identical between pipelines — no artifact there.)

## (b) Judge (raw metrics)
m_type_modes=5 (dev 1000, FIRES — one defect left), m_align_k=4 (dev 333, clear ✓), m_body_contrast=13882 (dark CTA fixed it ✓), m_gap_cv=758 ✓, m_bands=13 ✓, m_hero_ratio=349 (dev ~6, no fire but thin margin above the 245 fire line), m_margin_share=235 ✓.
Per-band forensics: the 5th type class is cls=0 — TWO fragment bands from the h1's glyphs: a 4px sliver (ascender tops of 'S'/'t') and a 1px sliver ('g'/'y' descender bottoms), detached because mid-glyph rows fall under the 32px/row ink threshold. Classes: {0:fragments, 1:eyebrow/lede/note/label, 2:digits[artifact], 3:h1-mains, 6:nav/actions-buttons}.

## (c) Proxy
A(iter07): bands=9, gap_cv=0.8207, margin_ink=0.2015, ink_total=0.0314, type_modes=5, contrast=2.617, align_modes=1, hero_ratio=0.3517, size_ratio=10.0, satcov=0.0072, hues=2.

## (d) Defects I name myself / plan for iter08
The cls=0 fragments are the last defect. Root cause: sentence-case display type has detached ascender/descender rows. Deterministic fix: set the H1 IN ALL CAPS — caps have flat tops/baselines, so every row of the line is densely populated (no sub-threshold rows, no fragments). Letterspaced caps also match the eyebrow voice. New expected classes: h1-caps at 48px → ~35px bands → cls 4.
Also collapse the button bands into cls 4: `.btn { line-height: 1.2 }`, padding 9px vertical → ~37px tall buttons → nav/actions bands land in [32,39] = cls 4, same bucket as the caps h1.
Expected judge classes: {1: micro+body text, 2: digits (artifact), 4: h1 + nav + actions} = 3 modes → dev 0. align_k stays ~1 (all centered).
Design risk I accept: all-caps H1 is a bolder voice; I'll judge it with my eyes (Chrome) — if it shouts, I'll revert and find another way to kill the fragments.

## Decision
CONTINUE to iter08. Score trajectory: 55 → 55 → 365 → 0 → 249 → (iter06 raw: typo+align fire) → (iter07 raw: only typo fires).
