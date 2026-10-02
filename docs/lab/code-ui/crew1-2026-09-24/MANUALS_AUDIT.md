# Coding-manuals-law compliance audit (T1 cards)

Date: 2026-09-24. Law (coding workstream proposal, active 2026-09-24):
manuals are on-demand reference; compiler errors/warnings are evidence
for deliberate revision; never memorize the manual — reference stays
reference, never installed knowledge.

## What is installed (cards/U1-U8.card)

Audited all 8 cards. Contents are exclusively:

1. `## TPL` sections (32 total): parameterized code templates with
   `{slot}` placeholders. These are GENERATIVE procedural schemas —
   they produce code only when slots are filled from a task. They
   contain no explanatory prose, no handbook sentences, no "about"
   text. Example: `const {var} = document.getElementById("{id}"){nonnull};`
2. `## LEARNRULES` / `## MISTAKES` sections: diagnostic-code →
   correction mappings (e.g. `TS18047 nonnull=!`). These are repair
   rules derived from compiler evidence, not manual content.
3. `## LEARNED` sections: corrections installed from deliberate
   revision during teaching (`fieldbang=!`, `nonnull=!`), each traceable
   to a specific tsc diagnostic on a practice task.

## What is NOT installed

- The corpus excerpts (`corpus/units/U*.txt`): consulted exactly once
  per unit during teaching (logged in `runlog/teach/consult.log` with
  byte counts and FNV digests), never copied into any card.
- No handbook prose, definitions, or explanations appear in any card.
- The B1 battery ran manual-free: zero corpus consultations during
  testing (driver has no consult path in the b1 phase).

## Verdict: COMPLIANT

The "distilled procedural schemas, not installed handbook prose"
interpretation holds. The reference was consulted, distilled into
generative templates and repair rules, and put away. The two learned
entries came from compiler evidence (deliberate revision), not from
re-reading the manual.

One residual note: the site scaffold (`sitecom/ts.card`, `frag.card`)
is crew-authored, not learned knowledge — documented as such in
PURITY.md and SITES_REPORT.md. It is not claimed as installed TNN
knowledge.
