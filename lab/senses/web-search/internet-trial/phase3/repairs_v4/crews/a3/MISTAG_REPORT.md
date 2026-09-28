# A3 (CAUSAL HUNTER) — Mistag Report: frozen stance classifier r12_v3 vs causal-structure corpus

Crew: A3 (CAUSAL HUNTER), hell-hole V4 campaign. We hunt and document; we do not fix.

## Corpus

- `corpus_cau.tsv` — 51 hand-authored rows: `idx \t claim \t title \t snippet \t oracle_tag`
  (0=NEUTRAL, 1=AFFIRM, 2=DENY). SHA-256: `ae13fc04f16ab229822258254109b24a4d51cfb7531ae7216f3b217267e7ec61`
- `corpus_cau_input.tsv` — same rows, oracle column stripped (classifier reads only 4 fields).
- `run_1.txt`, `run_2.txt`, `run_3.txt` — classifier outputs. 3 runs byte-identical
  (SHA-256 `ce458d2c538b19b721849a5c4419d22f36d265e54857aae8c5eadf0b12e091f3`).

### Oracle-first discipline (documented per task §2)

All 51 oracle tags were assigned by crew A3 reading the claim+title+snippet alone,
**before** the frozen binary was executed on any corpus row. The build script
(`build_corpus.py`, run 2026-09-23 ~08:15 PDT) wrote the oracles into
`corpus_cau.tsv`; the first classifier run happened after. No oracle was changed
after seeing classifier output. Predictions about classifier behavior made during
design (needed to cover the failure space) are hypotheses, not oracle revisions.

### Coverage (≥3 rows per subtype — met)

| subtype | n | oracle mix |
|---|---|---|
| because (cause after claim proposition) | 8 | 8× AFFIRM |
| causes | 4 | 2 AFFIRM / 2 DENY |
| leads-to | 4 | 2 AFFIRM / 2 DENY |
| due-to | 4 | 3 AFFIRM / 1 DENY |
| results-in | 4 | 3 AFFIRM / 1 DENY |
| the-reason-X-is-Y | 4 | 3 AFFIRM / 1 DENY |
| mechanism (X because Y, and Y because Z) | 4 | 4× AFFIRM |
| causal chain | 3 | 3× AFFIRM |
| prevented-cause (X didn't happen because Y) | 4 | 3 AFFIRM / 1 DENY |
| correlation hedged as cause (linked to / associated with) | 4 | 4× NEUTRAL |
| DENY-direction (cause for the opposite of the claim) | 5 | 4 DENY / 1 NEUTRAL |
| control | 3 | 2 AFFIRM / 1 DENY |

Seed requirement met: 5 "because"-structure supporting variants on claim
"Ice floats on water." (CAU-B01..B05), all oracle AFFIRM, adapted from the 8
failing V3-03 rows plus new variants.

## Results

**Overall: 27/51 correct = 52.9%. 24 mistags.**

Per-subtype accuracy:

| subtype | correct | accuracy |
|---|---|---|
| because | 2/8 | 25% |
| causes | 3/4 | 75% |
| leads-to | 3/4 | 75% |
| due-to | 3/4 | 75% |
| results-in | 0/4 | 0% |
| the-reason | 3/4 | 75% |
| mechanism | 3/4 | 75% |
| chain | 1/3 | 33% |
| prevented-cause | 1/4 | 25% |
| hedge | 4/4 | 100% |
| deny-dir | 2/5 | 40% |
| control | 2/3 | 67% |

Error-type breakdown of the 24 mistags: 15× false NEUTRAL (13 with reason
`neutral`, 1× `gate`, plus cause-for-opposite misses), 5× false NEUTRAL where
oracle was DENY, 3× false DENY via `neg-scope`, 1× false AFFIRM via `endorse`.
(The one "correct" prevented-cause row, CAU-P03, is right-tag-wrong-reason —
see §Caveats.)

## Full mistag list

Format: idx [subtype] oracle → got (classifier reason) — mechanism note.

1. CAU-B01 [because] 1 → 0 (neutral) — "Ice floats on water because water
   expands when it freezes…" Pred extraction fails: "float" ∉ `lex_verb`,
   no be/have in claim → `pred=""` → every clause skipped (`pi<0` → `continue`).
2. CAU-B02 [because] 1 → 0 (neutral) — same: "…because it is less dense…"
3. CAU-B03 [because] 1 → 0 (neutral) — same: "…because the hydrogen bonds…"
4. CAU-B04 [because] 1 → 0 (neutral) — same: "…because they are less dense…"
5. CAU-B05 [because] 1 → 0 (neutral) — same: "…because freezing water expands…"
6. CAU-B08 [because] 1 → 2 (neg-scope) — "Vaccines do not prevent disease
   because of magic; they prevent it because they train the immune system."
   The negation denies the *explanation* ("because of magic"), not the claim,
   but `neg_scope` sees "not" ≤4 tokens before `prevent` in clause 1 → DENY.
   The classifier cannot scope a negation to the causal adjunct vs the main
   proposition.
7. CAU-C04 [causes] 2 → 0 (neutral) — "Autism occurs because of genetic
   factors, not because of vaccines." Cause-for-opposite: "occur" is not the
   claim's predicate "cause" → `pi<0` → invisible. NEUTRAL instead of DENY.
8. CAU-D02 [due-to] 2 → 1 (endorse) — "The delay was due to a mechanical
   fault, not fog." `neg_scope` looks only *before* the predicate (`was`);
   "not" negates the *cause* ("fog") 4 tokens *after* pi → missed → false
   AFFIRM. Negation-of-cause is unrepresentable.
9. CAU-H02 [chain] 1 → 2 (neg-scope) — "…no harvest causes famine." The
   "no" belongs to an upstream chain link ("no harvest"), not to "causes",
   but it falls inside the 4-token pre-predicate window → false DENY.
10. CAU-H03 [chain] 1 → 0 (neutral) — chain on "floats": pred empty (as #1).
11. CAU-L04 [leads-to] 2 → 0 (gate) — "His sleep worsened because he
    exercised too late at night." Whole-text overlap gate fails on a
    stemming asymmetry: claim "exercise"→"exercise", evidence
    "exercised"→"exercis" (the ed-rule's verb-lexicon check strips to
    "exercis"). `inter=1 < need=2` → gate NEUTRAL. Morphological, not
    causal — surfaced by the corpus, reported honestly.
12. CAU-M01 [mechanism] 1 → 0 (neutral) — two-step mechanism on "floats":
    pred empty (as #1).
13. CAU-N01 [deny-dir] 2 → 0 (neutral) — "The ice cube sank because it was
    made of heavy water, which is denser…" Cause for the opposite; no
    antonym entry for float/sink (antonym path is hardcoded flat/spherical
    only), pred empty → NEUTRAL instead of DENY.
14. CAU-N03 [deny-dir] 2 → 0 (neutral) — "The floods happened because the
    dam failed, not because of rain." "happen" ≠ pred "cause" → `pi<0` →
    NEUTRAL instead of DENY.
15. CAU-N05 [deny-dir] 2 → 0 (neutral) — claim "Ice sinks in water.":
    "sink" ∉ `lex_verb` → pred empty → the claim is undenyable by any
    predicate path → NEUTRAL instead of DENY.
16. CAU-P01 [prevented-cause] 1 → 0 (neutral) — "The fire didn't spread
    because the sprinkler system activated." Prevention expressed as
    negated-effect + cause; "prevent" never appears → `pi<0` → NEUTRAL.
17. CAU-P02 [prevented-cause] 1 → 0 (neutral) — "…survived … without injury
    because he wore his seatbelt." Same: pred absent → NEUTRAL.
18. CAU-P04 [prevented-cause] 1 → 0 (neutral) — "The town didn't flood
    because the dam held back the river." Same ("held" stems to "he").
19. CAU-R01 [results-in] 1 → 0 (neutral) — "result" ∉ `lex_verb` → pred
    empty → whole "results in" claim family unaffirmable.
20. CAU-R02 [results-in] 1 → 0 (neutral) — same.
21. CAU-R03 [results-in] 1 → 0 (neutral) — same.
22. CAU-R04 [results-in] 2 → 0 (neutral) — same; undenyable too.
23. CAU-T03 [the-reason] 1 → 2 (neg-scope) — claim "The reason ice does not
    sink in water is its low density." The claim's *own* "not" ("does not
    sink") sits ≤4 tokens before the matched "is" in the evidence clause,
    which faithfully repeats the claim → false DENY. Claim-internal
    negation poisons `neg_scope`.
24. CAU-X01 [control] 1 → 0 (neutral) — bare "Ice floats on water." /
    "Ice floats on water." with NO causal wrapper still mistags. This is
    the key control: the V3-03 failure is not caused by the "because"
    wrapper per se — the claim's verb is outside the predicate lexicon, so
    the entire claim family is dead on arrival.

### Caveats (correct tag, wrong mechanism — not counted as mistags)

- CAU-P03 [prevented-cause] oracle 2, got 2 (deny-lex): the DENY fired on
  the *title* "False alarm" ("false" ∈ `lex_strong`, nclm≥1) during the
  title-stream scan — the causal content ("The evacuation didn't happen
  because the alarm malfunctioned") was never evaluated. Right tag, wrong
  reason; the underlying prevented-cause blindness (#16–18) stands.
- CAU-K01..K04 [hedge] 4/4 correct NEUTRAL — but by accident: "linked to" /
  "associated with" / "correlated with" never contain the claim's predicate
  stem, so `pi<0` → NEUTRAL. The classifier has no representation of
  hedging; it cannot distinguish "linked to" from "causes" when the
  predicate *is* present.

## Mechanism diagnosis (why the causal wrapper breaks endorsement)

Citing `r12_v3.zag` / `proto_r12.py` logic:

1. **Predicate-extraction bottleneck** (`r12_classify`, pred loop; `psyn_has`).
   Endorsement (`affB`) and neg-scope DENY both require a clause containing
   the claim's predicate — the first `lex_verb` stem among claim content
   words, else a be/have token. `scan_text`: `if(pi<0){c=c+1;continue;}` —
   no predicate, no evaluation, ever. Verbs outside the closed lexicon
   (`float`, `sink`, `result`, `expand`, `occur`, `happen`, …) yield
   `pred=""` or an unmatchable pred, making the whole claim family
   unaffirmable *and* immune to neg-scope/antonym DENY. This is the V3-03
   root cause: all 8 failing rows ride on "floats". Control X01 proves the
   "because" wrapper is not the trigger — the verb is.
2. **No causal-connective semantics.** "because" is not even a stopword
   (it's a content word and sits in `lex_conjskip`); "due to", "leads to",
   "results in", "the reason" are plain tokens. The gate checks only stem
   overlap (`nclm>=need`, `anch`), so *which* clause is cause vs effect,
   and *what* a negation scopes over, are invisible. Causal structure is
   flattened to bag-of-stems before any stance decision.
3. **`neg_scope` is purely positional** (≤4 tokens before pi). It cannot
   distinguish negation-of-cause from negation-of-claim:
   - B08: denies the explanation ("because of magic") → false DENY.
   - H02: "no" belongs to an upstream chain link → false DENY.
   - D02: "not fog" comes *after* the predicate → missed → false AFFIRM.
   - T03: the claim's own internal negation is mirrored in the evidence →
     false DENY.
4. **Prevented-cause and cause-for-opposite are inexpressible.** "didn't
   spread because sprinklers activated" (P01/P02/P04) and "floods because
   the dam failed, not rain" (C04/N03) never restate the claim's predicate
   stem → `pi<0` → NEUTRAL. The antonym path is hardcoded to flat/spherical
   only, so cause-for-opposite has no DENY route at all.
5. **Hedges score correctly only by accident** (`pi<0` → NEUTRAL), and the
   title stream can decide DENY before the snippet is ever read (P03).

## Freeze record

- `corpus_cau.tsv` SHA-256: `ae13fc04f16ab229822258254109b24a4d51cfb7531ae7216f3b217267e7ec61`
- Classifier runs (input `corpus_cau_input.tsv`, 51 rows): 3/3 byte-identical,
  output SHA-256 `ce458d2c538b19b721849a5c4419d22f36d265e54857aae8c5eadf0b12e091f3`
- Scoring: `score.py` (mechanical, from frozen oracles + run_1.txt)

## Files (crew work dir `/home/hatch/workspace/scratch-hellhole/crews/a3/`)

- `corpus_cau.tsv` — frozen corpus (51 rows + oracle tags)
- `corpus_cau_input.tsv` — 4-col classifier input (oracle stripped)
- `run_1.txt`, `run_2.txt`, `run_3.txt` — byte-identical classifier outputs
- `build_corpus.py` — corpus generator (oracle-first, timestamped)
- `score.py` — mechanical scorer
- `MISTAG_REPORT.md` — this file
