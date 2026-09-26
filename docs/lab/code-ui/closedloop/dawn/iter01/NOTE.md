# iter01 NOTE

## Real-browser leg
SKIPPED — no chromium/chromium-browser binary on this VM (`which` returned nothing). Frozen WeasyPrint pipeline only.

## (a) What my eyes saw (view.png, hero viewport only)
- Overall impression: light, airy, restrained serif design — matches the dawn brief. Warm paper background, soft peach accents, single hero with timer card. Directionally good.
- Nav: brand "Dawn" + sun dot reads well. DEFECT: "How it works" nav link wraps to two lines. DEFECT: the "Start focusing" pill button text wraps to two lines ("Start / focusing") and the pill renders as a tall blobby ellipse — ugly.
- Hero: eyebrow letterspaced caps fine; H1 "Start your morning. / Keep your focus." good size and weight; lede readable, restrained. Hero actions: orange pill fine, but the "See how it works" link sits tight against the pill (18px gap) and its underline looks cheap next to the pill.
- Timer card: ring arc, 25:00 numerals, label, progress bar — all clean, good shadow.
- What I could NOT see: everything below the hero fold (features cards, steps, CTA, footer) — the PNG only captured the top viewport.

## (b) Judge
judge2, reps a/b agree: BAD, score 55, defects TYPOGRAPHY_INCONSISTENT, SPACING_IRREGULAR, ALIGNMENT_WEAK (best_ref=vercel1, conf 1000).

## (c) Proxy (blind harness, A=B=iter01)
bands=10, gap_cv=1.039, margin_ink=0.1912, ink_total=0.0311, type_modes=6, contrast=1.923, align_modes=2, hero_ratio=0.3159, size_ratio=2.519, satcov=0.0179, hues=3.

## (d) Defects I name myself
1. Nav link wrapping ("How it works" two lines) — aligns with judge's ALIGNMENT_WEAK.
2. Nav CTA pill text wrapping ("Start focusing" two lines) — worst visual defect I saw; makes the button look broken.
3. Hero secondary link too tight to the primary pill + underlined styling clashes with the restrained look.
4. Cannot judge below-fold sections by eye; will rely on judge + (next iter) a full-page look if I can get one.

## (e) Changes planned for iter02
- `white-space: nowrap` on .nav-links a and .btn; widen .btn-small padding so "Start focusing" fits on one line.
- Hero link gap 18px → 28px; drop the underline, use plain quiet link (consistent with nav links).
- DONE criteria (stated now, per protocol): I declare DONE when judge2 returns GOOD with zero defects on both reps AND my own eyes find nothing left worth fixing in anything I can see. Stall rule: if score does not move for 3 straight iterations, I stop and report it as a finding.

## Decision
CONTINUE to iter02.
