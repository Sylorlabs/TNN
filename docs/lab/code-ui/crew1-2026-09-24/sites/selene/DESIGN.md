# selene — default-design procedure record

Site: **selene** — "a night-sky field guide" (self-designed site, rung 4 of the T2 ladder).

## What was given

The spec (`sitecom/specs/selene.spec`) carried ONLY:
- `SITE=selene`
- `TITLE=Selene — a night-sky field guide`
- `TOPIC=night sky field guide`

No sections, no copy, no palette, no layout instructions. Everything below
was chosen by the default-design procedure.

## The default-design procedure (deterministic, documented before use)

Input: a single TOPIC string.

1. **Palette selection.** Scan TOPIC for keywords:
   - contains "night" / "sky" / "dark" / "space" → dark theme
     (deep-navy background, starlight text, one warm accent).
   - else → light theme.
   → "night sky field guide" → dark theme (`sitecom/css/selene.css`).

2. **Section selection (fixed default vocabulary, in fixed order).**
   The procedure knows four section kinds: hero, interactive-list,
   data-card, footer. For a guide-type topic it picks:
   hero → interactive-list → data-card → footer.
   - interactive-list → constellation filter (filter buttons + cards).
   - data-card → moon-phase card (computed from the date).

3. **Copy generation.** Topic-derived, from fixed sentence frames:
   - hero title: "Know the sky above you." (topic=night sky → sky frame)
   - hero sub: "Four constellations worth learning first, and tonight's
     moon — no telescope required."
   - list items: four real constellations, two per hemisphere, each with
     one locating tip (Ursa Major, Cassiopeia, Crux, Scorpius).
   - moon card: phase computed in TypeScript from `new Date().getDate()`.

4. **Interactive wiring.** Default interactive set for a guide:
   filter-by-attribute buttons (learned querySelectorAll idiom) +
   date-derived text (learned getElementById idiom).

## What the procedure did NOT choose

- The fragment templates themselves (`conlist`, `mooncard` in
  `sitecom/frag.card`) and the CSS were written by the crew as part of
  building the procedure's vocabulary. The procedure chose WHICH
  vocabulary items to use and what content fills them, not their shape.

## Determinism

The procedure is a fixed mapping from TOPIC → (palette, sections, copy
frames). Re-running it on "night sky field guide" yields this exact site.
A different topic would yield a different site through the same rules.
