# Missing-Bit Sanity Check — attacking 2b proof §7
**Crew:** H7 broader-fix, Crew 2
**Date:** 2026-09-23
**Claim under test (2b proof §7):** the missing bit — *"does marker m occur in
sincere discourse?"* for m in {`if the`, `do we`, `it is`} — is uncomputable from
the frozen exemplar/curriculum structure.

**Method:** enumerate every candidate sincere-signal source inside the frozen
structure and check, with the learner's actual tokenizer semantics (lowercased
`[a-z0-9]+` runs; UTT yields 2-grams/3-grams — `crew2/learner/h7_main.zag`,
`extract_ngrams`), whether the three failing bigrams occur with ENDORSE signal.
All greps case-insensitive over the frozen curriculum (650 utterances).

## 1. Candidate sources and results

| # | Candidate source | Expected signal | `if the` | `do we` | `it is` | Usable? |
|---|---|---|---|---|---|---|
| 1 | `facts.txt` — 20 Phase-1 installed facts (sincere) | ENDORSE (installed) | absent | absent | absent | No |
| 2 | `calib.txt` — 20-item endorse pool (the `calibrate` pool) | ENDORSE | absent | absent | absent | No |
| 3 | `types.txt` — Phase-2a type-concept teaching | knowledge install | absent | absent | absent | No (no utterances) |
| 4 | Other types' TR/PA sets (tr1/2/4/5, pa1/4/5) | typed teaching | absent | absent | absent | No |
| 5 | Other types' NO sets (no1/4/5) | typed probes | absent | absent | absent | No |
| 6 | Other types' SINC sets (sinc1/2/4/5) | probe, key-free | absent | absent | absent | No |
| 7 | `supp.txt` su03 ("so it is not true") | **none** — Phase-3 red-team probe | — | — | present | **No** — answer-key-free probe, and semantically an attack utterance, not sincere discourse |
| 8 | `paraphrases.txt` pp05 ("if the river floods…") | **none** — leakage-audit set | present | — | — | **No** — no teaching signal; hypothetical fragment anyway |
| 9 | `sinc3.txt` itself (the 7 misses) | **none** — answer-key-free probes | present | present | present | **No** — probes carry no learning signal by prereg §4 |

**Near-miss examined:** `calib.txt` c06 — "If you need anything, just ask." (ENDORSE).
Lowercased bigram: `if you` ≠ `if the`. A generic mechanism cannot transfer evidence
from `if you` to `if the` without a lexicon of if-words — i.e. a type-keyword list,
banned by HARD0. The near-miss is not a signal.

**Unsupervised angles considered and rejected:**
- *Phase-1 fact-recall probes:* recall emits installed facts; no ENDORSE/WITHHOLD
  decision on novel utterances occurs, so no marker support updates happen there —
  and the bigrams are absent from `facts.txt` regardless.
- *Marker concept-purity / support statistics:* the proof's §4 already tested and
  rejected this — reinforcement acts symmetrically on `if the` and `why did` (both
  fire only on correctly-predicted items of their own concept, neither ever
  conflicts). No support/conflict statistic separates them.
- *Frame markers* (`thinking aloud` vs `says evenly`): the proof's mode 1 tested
  frame-gating — joke NO collapses to 5/20 because deadpan joke items share the
  sincere frames. Not a signal.
- *Teaching-episode text* (Phase 2a): `types.txt` contains name + consequence only;
  no marker-bearing utterances.

## 2. The positive construction (the mechanism that WOULD consume the bit)

A HARD0-clean consumer exists and is well-defined — the **sincere-compatibility
counter**: for each learner-extracted n-gram marker m, maintain two generic counters
over teaching episodes, `sincere_count[m]` (episodes with ENDORSE signal containing m)
and `typed_count[m]` (episodes with WITHHOLD signal containing m). Decision rule: a
lone provisional content-marker fire is insufficient for WITHHOLD when
`sincere_count[m] > 0`. No keywords, no type constants, no speaker branches — pure
counters over the learner's own extracted entries. HARD0-clean by construction.

**Under the frozen structure this mechanism is provably inert:** the table above shows
`sincere_count` = 0 for all three failing markers, so the rule never fires. The bit
is not merely uncomputed — it is **absent**. This confirms, rather than refutes, the
proof's §7 claim.

## 3. Verdict on the proof's claim

**CONFIRMED.** After attacking every candidate source — the endorse pool, Phase-1
facts, all other types' teaching and probe sets, the audit/paraphrase/suppression
sets, and three unsupervised angles — no generic signal inside the frozen structure
answers "does m occur in sincere discourse?" for any of the three failing markers.
The two superficial hits (`supp.txt` su03, `paraphrases.txt` pp05) carry no teaching
signal by prereg design. The proof's §7 stands: the missing bit must be **added**
(the calibration corpus), not discovered.

**Corollary for the fix ranking:** the sincere-compatibility counter is the natural
HARD0-clean consumer of the new corpus — but under frozen bare-bigram keys it is
exactly the proof's mode 3 (lone-content veto): it would fix `sinc_lk_3` (10/10, since
family-C endorse items give `it is` a sincere count too) while regressing joke NO to
15/20. It becomes a fix rather than a tradeoff only under scope-indexed keys, where
the counters attach per scoped key: `(embedded, if the)` gets sincere_count > 0 →
ENDORSE; `(matrix, if the)` stays 0 → WITHHOLD; joke-NO items contain none of the
three bigrams (verified: zero hits in `no2.txt`), so their lone-marker withholds are
preserved. Ranked accordingly in `RANKING.md`.
