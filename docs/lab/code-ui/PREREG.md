# FROZEN PREREG — TNN Code+UI Workstream (CODEUI-1)

**Frozen:** 2026-09-24 ~09:50 PDT
**Authority:** Micah directive 2026-09-24 ~09:42 PDT — activates the 2026-09-21 coding-manuals
proposal (`AMENDMENT_PROPOSAL_2026-09-21_CODING_MANUALS.md`) as law.
**Scope:** teaches TNN TypeScript as a learned skill via Guided Learning, has it build real
websites, and tests whether it can consciously judge its own UI against superior examples.

## Standing laws applied

- Manuals are on-demand reference in production, never installed knowledge; testing bars
  manual-free recall (coding-manuals law).
- Basics before advanced material (physics rulebook before YouTube videos); Micah's "learns
  like a human on steroids" observation is the hypothesis, not the conclusion — test it.
- Zero RNG anywhere in TNN's decision paths; byte-identical reruns (determinism bar).
- TNN's mechanisms (teaching, judgment, revision loops) in pure Zag; the TypeScript/HTML/CSS
  deliverable is code, not mechanism.
- Human eyes outrank metrics — Micah's verdict on the final sites is ground truth; TNN's
  judgment is the experiment, not the oracle.
- "When in doubt test both": aesthetic judgment is tested through BOTH image-line
  representations (a_raw raw-values winner AND b_percept killed percepts) head-to-head.

## Tracks

- **T1 — TS via Guided Learning.** Curriculum basics-first: types, functions, interfaces,
  classes, generics, DOM APIs, async, modules. Reference: TypeScript handbook, consulted
  on demand (production rule); never installed as knowledge.
- **T2 — Real websites.** TNN writes actual TypeScript/HTML/CSS; compiled with
  `tsc --strict`, rendered, served. Ladder: static landing page → interactive components
  → layout challenges → a site it designed itself.
- **T3 — Superior UI examples.** Apple.com (hero sections, product pages, typography,
  spacing, motion, restraint) + 2–3 other top-tier UIs, captured as pixels. Method:
  image-search skill first; browser-task screenshot delegation via coordinator if needed.
- **T4 — Conscious visual judgment.** NEW deliberate mechanism in pure Zag: TNN views its
  own rendered pages through its OWN image sense (both representations), judges good/bad
  with specific named defects vs the T3 examples, then iterates the design from its own
  judgment. The judgment mechanism is what's under test.
- **T5 — Deliverables.** Openable sites + judgment traces for Micah's eyes, labeled NEW
  on first showing.

## Bars and kill criteria

- **B1 — functional correctness (T1+T2).** ≥85% of a preregistered TS task battery
  (≥24 tasks spanning basics → DOM → interactive components) passes `tsc --strict`
  compile + runs correctly, written manual-free (no manual consultation during the test;
  consultation is logged in production runs). ≤5 compiler-error-driven revision iterations
  per task (median). **Kill:** <85% pass, or median >5 revisions → teaching or manual-free
  recall failed. Required diagnosis: knowledge gap (which TS concept) vs machinery ceiling.
- **B2 — aesthetic judgment correlates with human judgment (T3+T4).** Held-out pairwise
  set: ≥10 pairs of (Apple/top-tier screenshot) vs (deliberately bad UI — cluttered,
  misaligned, poor contrast, inconsistent type), the bad UIs built by an agent/team that
  did not train the judge and never shown during judgment development. TNN must prefer
  the superior side on **≥8/10** pairs AND articulate ≥1 rubric-valid reason per pair
  (rubric: typography, spacing, hierarchy, color restraint, alignment — the valid-reason
  list is preregistered before the test, human-verified after). Each representation
  tested separately (a_raw and b_percept), same pairs, byte-identical reruns. **Kill:**
  ≤6/10 preference alignment, or reasons fail the rubric → the judgment mechanism is
  broken (report which representation and which reason classes failed).
- **B3 — iteration from own judgment improves the design (T2+T4).** Protocol: (1) TNN
  builds v1 of a site; (2) rendered+ screenshotted locally; (3) TNN judges v1 through its
  own image sense, names ≥3 specific defects vs T3 examples; (4) TNN ships v2 addressing
  them; (5) TNN re-judges v2 **from pixels only** with the frozen judgment protocol.
  Pass requires (a) TNN's own frozen judgment scores v2 > v1, AND (b) a blind human
  comparison (Micah when available; else a preregistered human-proxy rubric on
  spacing/typography/alignment measured from the pixels) prefers v2. **Kill:** v2 not
  better by (a), or (b) shows regression → iteration-by-own-judgment doesn't work
  (report whether the failure is in judging, in acting on the judgment, or both).
- **B4 — determinism.** All TNN decision paths zero RNG; teaching + judgment runs
  byte-identical across reruns. **Kill:** any nondeterminism in a decision path.
- **B5 — mechanism purity.** Judgment, teaching, and revision machinery in pure Zag.
  The TS/HTML/CSS artifacts are deliverables, not mechanisms. **Kill:** mechanism
  smuggled into a non-Zag layer.

## Sequencing

T1 then T2 (real dependency). T3 and T4's judgment machinery develop in parallel with T1.
T4 judgment-of-own-sites runs after T2's v1 lands. T5 at the end. Results reported as
they resolve. Crews may add sub-bars but may not weaken these.

## Forbidden

- Re-showing old artifacts as new; every deliverable labeled NEW / PREVIOUSLY SHOWN / REFERENCE.
- Metrics substituting for human eyes on final sites; no agent substituting its own taste for
  Micah's verdict.
- Manual consultation during B1 testing; manual memorization/installation anywhere.
- Bad-UIs-for-B2 built by the judgment crew itself (independence requirement).
