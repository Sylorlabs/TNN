# CMP-ENGINE — frozen prototype design (2026-09-23)

Dedicated comparison engine in pure Zag, replacing the keyword-scan
`do_compare`. FROZEN at commit; the held-out battery is generated after
this freeze.

## Source

- `engine/cmp_engine.zag` — the engine (new `do_compare` + helpers).
- `engine/splice.py` — builds `engine/dialogue.zag` by replacing the old
  `do_compare` span in the integrated source with `cmp_engine.zag`.
  All other code byte-identical to the integrated baseline.
- `engine/dialogue.zag` — the frozen prototype source (splice output).

Build: pinned `znc_linux_x86_64_abed8aa1`, `--no-analyze`
(analyzer warnings are inherited from the integrated source).

## Design

Typed attribute model: entity → dimension → i32 value.
- dim 1 = HEIGHT_M via `year_of(..., "tall")`
- dim 2 = YEAR via `time_marker_idx` + `time_val`

Pipeline per question:
1. **Hop substitution** (`ce_hop_subst`): rewrite each "author of \<work\>"
   span to the author's name (via `author_of`), so multi-hop questions
   reduce to direct comparisons. One- and two-hop both work because
   substitution applies to every occurrence before mention scanning.
2. **Operator detection** (ordered): "before or after" (disjunction) →
   "more/less/fewer than N" (threshold) → "before/after N" (threshold) →
   "same"/"different" (equality, dimension from year/height words) →
   comparative word → (op, dim, word-class). Comparative + "than N"
   (digits) reinterprets as a threshold ("taller than 331 meters").
3. **Negation scope**: "not"/"n't" before the operator flips the outcome
   (or the min/max direction for which-questions).
4. **Mentions**: `cmp_scan` on the substituted text, position-ordered;
   "those two"/"these two"/"the two"/"either" falls back to the pv 40/44
   pair stored by the previous comparison turn.
5. **Values**: `ce_attr` per mention; missing attribute on a known
   dimension → "I don't know." (handled by the engine, never fell through
   to retrieval).
6. **Answer**:
   - before-or-after → "before." / "after."
   - threshold (needs 1 mention) → "yes." / "no."
   - same/different → "yes." / "no." (non-yes/no forms fall through)
   - max/min, yes/no → "yes." / "no."
   - max/min, which → n-way argmax/argmin over ALL mentions
     (order-invariant), rendered with the fired word class
     ("is taller.", "is shortest.", "was \<marker\> first.", …).
   - Compared pair stored at pv 40/44 for anaphora.

## Response vocabulary (exact strings)

"yes." "no." "before." "after." "I don't know." + "\<name\> is taller."
"\<name\> is shorter." "\<name\> is tallest." "\<name\> is shortest."
"\<name\> is higher." "\<name\> is lower."
"\<name\> was \<born|built|published|completed|dedicated|opened\> first."
"... last."

## Known limitations (not implemented)

- Bare "tall" as a comparative ("how tall is X?" is not comparison).
- "greater"/"lesser"/"as tall as" synonyms.
- Three-or-more-hop author chains (only "author of" substitution; chains
  compose textually so "author of the author of" is not handled).
- Non-yes/no same/different ("are X and Y the same?" falls through).
- Thresholds on the year dimension via "more than N years" (only
  before/after N and comparative+than N are implemented).

## Verification status at freeze

- 1×: 96/96, every family 1.000, digest 8fd13d42…
- 10×: 960/960, every family 1.000
- 100×: 9600/9600, every family 1.000
- All reruns byte-identical (per-chunk digests match run1/run2).

Bugs found and fixed during development (before freeze):
- `find_sub` needle length 16 on the 15-char "before or after" literal
  → slice OOB panic (literals are exact-length slices).
- `ce_num_after` did not skip the space after "than".
- Threshold questions mention one entity; the ne≥2 gate fell through.
- Negative literals ("-7") not parsed; added leading-minus support.
- "I don't know." written with length 12, dropping the period (now 13).
- "taller/shorter than N meters" added as comparative-threshold.
