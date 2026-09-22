# MORPH_BATTERY.md — characterization of the keyword core's morphological boundary

## What the frozen stemmer already handles (controls — all pass pre/post)

Regular suffix stripping (`stem_inplace`, first-match-wins, single pass):
plurals (`towers`→`tower`), past tense (`published`→`publish` via the
`ished` rule, `discovered`→`discover` via `ed`), 3rd-person singular
(`writes`→`write`). Probes S02, S03, S05, S09–S14.

## The boundary, mapped

| Class | Example | Status | Mechanism |
|---|---|---|---|
| Regular inflection | towers/tower, published/publish | bridged (stemmer) | suffix strip |
| Irregular inflection | birth/born, won/win, built/build, taught/teach, ran/run | **bridged post-fix** | `irregular_norm` table |
| Active/passive convention | wrote / was written by | **NOT bridged (deliberate)** | bridging caused 37 regressions; the KB keeps both forms as separate facts with phrasing-dependent expected answers (probe C04) |
| Derivational (adj↔noun) | high/tall, height/tall | **not bridged** | different lexemes; no wire information supports the mapping (probes C01, C03 — C03 passes anyway via `big ben` entity overlap) |
| Synonym | penned/wrote | **not bridged** | no synonym inventory in the core (probe C02; consistent with the independent-battery finding that single-sided synonym swaps fail 10/11) |
| Compounds | birth year | **handled compositionally** | `birth year` triggers the Part-2 compose branch, not keyword matching |
| `written by` relative clause | "birth year of the guy the martian was written by" | **unhandled** | Part 2 only resolves ` wrote ` clauses; documented gap |

## Scored probes (S02–S14): 13/13 post-fix (KB-M2)

| Probe | Query shape | Pre-fix | Post-fix | Fixed by |
|---|---|---|---|---|
| S02 | `moby dick was written by whom?` | PASS | PASS | — (control) |
| S03 | `when was the eiffel tower built?` | PASS | PASS | — (built→build symmetry) |
| S04 | `what did marie curie win?` | FAIL→`was born in 1867` | PASS | won→win |
| S05 | `who won the nobel prize?` | PASS | PASS | — (control) |
| S06 | `what is the birth year of jane austen?` | PASS | PASS | — (via Part-2 named path post-fix; Jaccard pre-fix) |
| S07 | `birth year of the woman who wrote pride and prejudice` | FAIL→wrote-fact | PASS | Part 2 (author_of generalization) |
| S08 | `tell me the birth year of the guy who wrote the martian` | FAIL→wrote-fact | PASS | Part 2 (trigger robustness) |
| S09 | `when was andy weir born?` | PASS | PASS | — (born→bear symmetry) |
| S10 | `who wrote the martian?` | PASS | PASS | — (control) |
| S11 | `charles darwin wrote what?` | PASS | PASS | — (control) |
| S12 | `how tall is the montparnasse tower?` | PASS | PASS | — (control) |
| S13 | `when was charles darwin born?` | PASS | PASS | — (control) |
| S14 | `who discovered radium?` | PASS | PASS | — (control) |

Pre-fix scored: 9/13. Post-fix: **13/13 = 100%** (bar: ≥95%).

## Characterization probes (honest fails — the boundary)

| Probe | Query | Got | Why it fails | Verdict |
|---|---|---|---|---|
| C01 | `how high is the eiffel tower?` | `The Eiffel Tower is in Paris.` | high↛tall: derivational adjective gap, no mapping on the wire | out of scope |
| C02 | `who penned the martian?` | `The Martian was published in 2011.` | penned↛wrote: no synonym inventory | out of scope |
| C03 | `what is the height of big ben?` | PASS (`Big Ben is 96 meters tall.`) | `big ben` entity overlap carries it; height/tall still unbridged | boundary noted |
| C04 | `who has written the martian?` | `The Martian was published in 2011.` | written→write bridging REMOVED: unsafe under the KB's active/passive convention (37 regressions) | deliberate |

## Table check (Python mirror of `stem_inplace` + table)

All 16 table entries reach their lemma; all 7 lemmata are fixed points;
suffix interactions compose (`births`→`bear`, `teaches`→`teach`,
`runs`→`run`, `wins`→`win`, `builds`→`build`). Full log in `table_check.log`.

## Micah's questions, answered directly

- **Why can't "birth year" and "born" separate?** They can now: both
  normalize to the `bear` lemma at index and query time. But that alone
  did not fix WE-09 — the relative clause outscored the focus word, so a
  compositional rule was also required. Two stacked causes, both fixed.
- **The one WEIRD miss** was WE-09 turn 1 (`i'm curious about the birth
  year of the guy who wrote the martian`); WEIRD is now 30/30.
