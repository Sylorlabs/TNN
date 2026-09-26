# Closed-loop website run — plain-English report

**Date:** 2026-09-26. **Order:** Micah, 2026-09-25 ~21:15 PDT.
**Question under test:** when a builder generates a website, does it ever LOOK
at its own render and consciously decide "this looks good" — or does it
generate once and stop? (Prior rounds were one-shot: generate, then a
separate judge scored it after the fact.)
**Second question (added ~21:14 PDT):** can the builder do debuild-style
follow-ups — "add padding here" style refinements, conversationally?

## Phase 1 — the closed loop

One builder agent. It generated the "dawn" landing page fresh from the
brief (a distraction-free deep-work timer page: light, airy, restrained),
then every round it: rendered its page through the frozen pipeline, LOOKED
at the render with its own eyes, read the frozen judge's score of its own
work, read a second-opinion pixel measurement, named its own defects,
repaired the page, and re-rendered. It stopped only when IT declared DONE —
no iteration cap. It took 8 rounds.

### What it saw and fixed, round by round

| Round | Judge score | What happened |
|---|---|---|
| 1 | 55 BAD | First attempt. Judge flagged messy typography, irregular spacing, weak alignment. Builder saw a wrapped nav bar and fixed it. |
| 2 | 55 BAD | Nav pill corrected — score didn't move. Builder noted the fix was cosmetic, not structural. |
| 3 | 365 BAD | Switched body text to system sans. Spacing complaint cleared. Big jump. |
| 4 | 0 BAD | Builder's favorite round — an all-sans hero it thought looked best. The judge collapsed: 4 defects including poor contrast. The builder recorded this as a useful disagreement: its taste and the instrument diverged, and it trusted the instrument enough to keep going instead of quitting. |
| 5 | 249 BAD | Proved a serif display treatment helped the judge. Recovering. |
| 6 | (2 defects) | Redesign: minimal timer card, centered column. |
| 7 | (1 defect) | Naked timer digits; fixed body contrast. Last defect was a 4px/1px fragment artifact from headline letterforms. |
| 8 | **876 GOOD, zero defects** | All-caps letterspaced headline killed the fragments. Both judge representations agree. |

The builder's DONE rule, stated before it stopped: judge says GOOD with
zero defects on both representations AND my own eyes find nothing left to
fix. Met at round 8. It stopped at convergence, not from running out of
ideas — scores were still moving when it finished.

### Did "done" mean anything?

Yes. Three independent checks agree the final page is genuinely good:
the frozen judge (GOOD 876, zero defects), the blind pixel harness
(structurally cleaner than round 1 on every measure), and the builder's
own eyes on real-Chrome screenshots ("I'd ship it"). It did not stop
early (it kept going through a round-4 collapse) and it did not
over-iterate (it refused to chase the last 124 points, correctly judging
them instrument noise — chasing them would mean designing around the
pipeline, not improving the page).

### Honest findings from the loop

- **The judge scores the pipeline, not just the page.** The builder caught
  the frozen WeasyPrint renderer drawing its timer digits at ~55% of true
  size — a fourth "type class" that exists only in the instrument. A human
  sees three. It noted this and didn't chase it.
- **Taste vs instrument.** Round 4 is the important one: the page the
  builder liked best scored worst. It kept iterating anyway. Its
  self-judgment was honest — it never declared "looks good" while the
  proxy disagreed.
- **Real browser added mid-run.** Rounds 1–6 were judged on WeasyPrint
  renders; from round 7 the builder also viewed real headless-Chrome
  screenshots (what a human actually sees).

### Control: one-shot vs deliberate iteration

The prior one-shot dawn v1 (built without looking, judged after the fact):
**573 BAD**. The closed-loop final: **876 GOOD, zero defects**. Deliberate
iteration beats one-shot generation by 303 points on the same instrument.

## Phase 2 — follow-up refinement (debuild-style)

Starting from the finished page, four natural-language follow-ups were
given one at a time, each applied to the current version:

| # | Follow-up | Landed? | Judge before → after | Broke anything? | Scope clean? |
|---|---|---|---|---|---|
| 1 | "add more padding to the hero" | yes | 876 → 876 | no | yes — 1 CSS line |
| 2 | "make the headline bigger" | yes | 876 → 896 | no | yes — 1 CSS line |
| 3 | "change the primary button color to green" | yes | 896 → 896 | no | yes — 2 CSS lines |
| 4 | "add a footer with a copyright line" | yes | 896 → 896 | no | yes — footer markup + 1 CSS rule |

**4/4 landed.** Quality across the chain: 876 → 876 → 896 → 896 → 896 —
improved, then held. No new defects at any step. The final page shows all
four changes at once, verified by the builder's own eyes on real-Chrome
screenshots; everything else on the page is pixel-identical.

Notable: follow-up 3 was ambiguous ("the primary button" — the hero's dark
CTA vs the two orange accent buttons). The builder chose the hero CTA and
deliberately did NOT recolor the shared accent variable, which would have
dragged the eyebrow, step numbers, card icons, and brand mark along with
it. Restraint held across all four edits — diffs show only the targeted
lines changed.

### Instrument limitation found

The frozen render pipeline only captures the above-fold region: the
footer added in follow-up 4 is invisible to the judge and the pixel
harness (its render file is byte-identical to follow-up 3's). The builder
caught this and verified the footer via full-page Chrome screenshots
instead. For below-the-fold follow-ups, the judge leg is not a valid
verifier — eyes are required.

## Bottom line

- The builder looked at its own work every round, named real defects,
  repaired them, and its "done" correlated with actual quality on three
  independent checks. Micah's question is answered: yes, it consciously
  decided "this looks good" — after 8 rounds of looking.
- Conversational follow-up refinement works as the debuild demo
  advertised: 4/4 follow-ups landed, correctly scoped, no accumulated
  drift, end state matches the requested end state.
- Deliberate iteration (876 GOOD) decisively beats one-shot generation
  (573 BAD) on the same page, same judge.

## Evidence

`code-ui/closedloop/dawn/`: `iter01/`–`iter08/` (site files, frozen
renders ×2 with matching SHA-256, eye-view PNGs, real-Chrome screenshots,
judge TSVs, proxy measurements, per-round NOTEs), `DONE.md`,
`followups/base/` + `fu01/`–`fu04/` (same artifact set per follow-up).
Zero RNG throughout. Frozen scripts and judge binary untouched.
