# FIX.md — the WE-09 repair (two parts)

## Part 1 — irregular-form normalization (`irregular_norm`)

**Where:** new `fn irregular_norm` in `dialogue.zag`, called in `proc_token`
immediately after the frozen `stem_inplace`:
```zag
let sl:i32=stem_inplace(tmp,tlen);
sl=irregular_norm(tmp,sl);
```
`stem_inplace` itself is untouched. Because KB-install and query processing
both flow through `proc_token`, the mapping is symmetric by construction
(single code path — KB-M5).

**What:** 16 irregular inflections → lemma (inflectional only):

| Lemma | Forms bridged |
|---|---|
| bear | birth, born, borne |
| teach | taught, teaching |
| run | ran, running |
| speak | spoke, spoken, speaking |
| think | thought, thinking |
| build | built, building |
| win | won, winning |

All mappings verified: every form reaches its lemma, every lemma is a
fixed point, and suffix-stripped plurals (`births`→`birth`→`bear`) compose
correctly (see MORPH_BATTERY.md §table-check).

**Deliberately removed — the write family.** Bridging `wrote/written/
writing`→`write` collapsed the KB's load-bearing active/passive
distinction (`X wrote the novel Y.` vs `Y was written by X.` are separate
facts whose expected answers depend on question phrasing). Result: **37
regressions** on the frozen battery (FU/RE/CO/CP turns flipping to the
passive fact, which is shorter and wins the Jaccard tie). Removed;
documented as characterization probe C04. Lesson: a morphology bridge is
only safe where the merged forms never distinguish expected answers.

## Part 2 — "birth year of \<person-desc\>" composition branch

**Where:** appended at the END of `do_compose` (never steals the `was the
author of` branch, the born-assertions, or any other turn — `birth year`
occurs exactly once in the frozen battery).

**Why Part 1 is not enough:** proven in REPRO.md — even with the bridge,
Jaccard scores the WROTE fact 2/12 over the BORN fact's 1/12.

**How:** on substring `birth year` in the query:
1. `gaz_scan` for a named person (class 0) → use them.
2. Else resolve the relative clause: find ` wrote `, `gaz_scan` the region
   after it for a work entity (class 1), `person = author_of(work)` —
   reusing the proven relation primitive from the `was the author of`
   branch.
3. `fid = born_fact_of(person)` (new helper mirroring `year_of`, returns
   the fid of the lowest-fid fact naming the person containing ` born `);
   `emit_fact` the fact verbatim → exact expected string, proper
   capitalization included.
4. Anything unresolvable → `return 0`, falls through to the default path
   (current behavior preserved).

`do_compose` gained one parameter (`ftx`, threaded from the existing
`do_turn` call site) so the branch can emit the original-case fact text.

**Generality probed:** `birth year of the woman who wrote pride and
prejudice` → Jane Austen → 1775 (S07); `what is the birth year of jane
austen?` → named-person path (S06); trigger works mid-sentence (S08).
`written by` relative clauses are a known unhandled shape (boundary).

## Files changed

- `~/workspace/tnn-lab/dialogue/dialogue.zag` — the only source change
  (+75 lines: `irregular_norm`, `born_fact_of`, compose branch, `ftx`
  threading, one call-site line).
- This directory — prereg, reproduction, battery, verdict, logs.
