# Red-team report — design track, 2026-09-22

Red team run through gpt-5.6-sol (short prompts; Grok 4.7 quota-blocked,
see FALLBACK_LOG.md). Two probes: V1 machine aesthetic, V2 human-taste theme.

## V1 critique (fair hits)

1. **Monochrome flattens hierarchy.** Everything white-on-black competes
   equally; needs 3 luminance levels. PARTIALLY TRUE: we have muted
   (150,152,160) for secondary text, but titles/metadata/controls are all
   full white. Accepted as V1's honest look — not "fixed", because V1 must
   remain the scorer's unedited winner.
2. **No borders/grouping.** Sections risk collapsing into one column.
   TRUE of the library rows (borderless). This is what the scorer selected
   (border penalty); documented, not patched.
3. **5x7 font too crude for small text.** TRUE and inherent: from-scratch
   bitmap font caps legibility. Timestamps/tab labels at scale 1 are
   chunky. Accepted as the pixel-engine aesthetic; glyphs verified correct.
4. **Zero radius can read as unfinished.** Stylist's opinion; the machine
   chose it. Kept.

## V2 critique (fair hits)

1. **16px radius everywhere = generic SaaS.** Sol-the-red-teamer now says
   8-10px, contradicting Sol-the-designer who specified 16px. NOTED AS
   CONTRADICTION; V2 stays frozen per prereg (it is Sol's stated human
   prediction, not a moving target).
2. **Shadows muddy on dark backgrounds; prefer 1px borders.** Reasonable,
   but V2 is the frozen prediction. Noted.
3. **Coral must be functional, not decorative.** VERIFIED TRUE of our V2:
   coral carries play state, active tab, playing row, toggles-on, slider
   fills — all functional, never decorative.
4. **The coral-removal test.** "If hierarchy collapses without coral, it's
   pandering." ASSESSED: hierarchy carriers are size/position (title scale 3
   vs body 2 vs caption 1, tabbar dot position, EQ bars presence, slider
   fill fraction) — all survive accent removal. V2 passes; not pandering
   by this test.

## Rejected / out of scope

- "Use familiar icon glyphs instead of text" — we already use drawn
  transport icons, not text labels.
- "Touch targets below comfortable size" — 64px rows, 60px play button;
  fine at 360px width.
- Requests to modify the app's files — red-team is critique-only.

## Verdict

No design changes made. V1 stays the scorer's verbatim winner; V2 stays
Sol's frozen prediction. Critiques are recorded as known limitations,
not patched, to keep the experiment honest.
