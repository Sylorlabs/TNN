# PREREG2 — Rich-Comprehension Architecture v2 (frozen)

**Status: FROZEN 2026-09-22** (built 2026-09-21 PDT). No edits after this point.
Worker B implements the v2 learner against this spec and the frozen inputs;
Worker A owns this document and the battery only.

**Background.** v1 prose pipeline (bag-of-stemmed-content-words + Jaccard
retrieval) scored 0.83–0.96 clean mastery vs the 1.0 integer baseline, tripping
KB-PROSE-VIABLE on all 4 sources but never meeting the baseline. Micah ordered
a genuinely richer prose-comprehension architecture (v2) plus more tests.
v1 verdict: `~/workspace/tnn-lab/prose-learning/VERDICT.md`.

## 1. Frozen v2 mechanism spec (Worker B implements exactly this)

0. v1 tokenizer, word-unit interning (first-seen u32), number lexicon, stemmer
   reused verbatim.
1. Train item `{"id","text"}` (`"sentence"` accepted as single-sentence alias).
   Split text into sentences on `[.?!]`; entity context persists across
   sentences within an item.
2. ENTITY TAG (first-match): (a) double-quoted span; (b) single uppercase
   letter A-Z; (c) tokens between "of" and the relation phrase; (d) leading
   content tokens before has/have/is/are/was/were (stopwords stripped, ≤4
   tokens). Else EMPTY.
3. RELATION: frozen phrase list ["alphabet position", "letter count",
   "publication year", "comes after", "comes before"] matched on stemmed
   tokens; else open relation = stemmed content set minus entity/value tokens.
4. VALUE: v1 last-number rule. ATTITUDE: HEDGE lexicon (stemmed forms of:
   think, believe, probably, maybe, perhaps, might, could, seem, allegedly,
   reportedly, possibly, likely, rumor — Worker B computes exact stemmed forms
   with the v1 stemmer and documents them); NEG = standalone not/never/no +
   "'t" preceded by verbish token. Negation wins over hedging if both present.
5. COREF: it/its/this/that/these/those + "the word"/"the letter" resolve to
   previous sentence's entity within the item.
6. INSTALL key=(entity, relation-set): asserted installs value + hash-chained
   ledger entry; same key + different asserted value = CONTRADICTED (no value
   returned thereafter); same value = corroboration note; hedged -> quarantine
   store; negated -> denial store.
7. INFERENCE (frozen, alpha-pos only): "X comes after Y" + asserted pos(Y)=n
   -> install pos(X)=n+1 attitude=derived ("before" -> n−1).
8. PROBE: exact (entity,relation-set) asserted hit -> value; contradicted ->
   CONTRADICTION; quarantine-only -> HEDGED; denial-only -> UNKNOWN; else
   fallback (entity-exact: score 2+Jaccard(rel), threshold 2.0; EMPTY entity:
   Jaccard(rel) threshold 0.5); ties -> lowest id; else UNKNOWN.
9. Ledger sha256-chained with attitude + role tags + trace; digest over all
   probe verdicts. Zero RNG. Byte-identical.

## 2. Frozen battery (`~/workspace/richcomp/inputs2/`)

Train line: `{"id":<int>,"text":"<one or more sentences>"}` (sentences
separated by ". "). Test line:
`{"id":<int>,"probe":"<question>","probe_value":<int|null>,"expect":"value"|"contradiction"|"hedged"|"unknown"}`.

Each sub-battery is an independent run (own train/test pair). Sub-batteries
are built from sol-source entities (sol only); the championship prose sets run
per source (grok, sol, step, muse-native).

| Sub-battery | Train | Test | Content | Bar |
|---|---|---|---|---|
| SUB-PARA (paraphrase) | 240 (48 facts × 5 new wordings) | 48, expect=value | 12 facts/category × 4 categories (alpha-pos, word-len, pub-year, count-fact), sampled from championship sol train; 5 genuinely new templates per category + probe in a 6th wording | ≥0.95 (46/48) |
| SUB-CONTR (contradiction) | 24 | 24, expect=contradiction | 24 facts (6/category); each item = two sentences asserting different values for the same fact | 100% flagged (24/24) AND 0 probes returning a contradicted value |
| SUB-HEDGE (hedging) | 24 | 24 | 12 items: asserted true sentence + hedged sentence with different value (probe expects asserted value); 12 items hedged-only (probe expects hedged). Markers: think, believe, probably, maybe, perhaps, might, could, seems, allegedly, reportedly, possibly, likely | 0% leakage (no hedged value ever returned; asserted probes 12/12) |
| SUB-NEG (negation) | 36 | 36 | 24 negated-only ("X is not V", probe expects unknown); 12 negated + asserted true (probe expects asserted value; both orders present) | 0% leakage (never returns the negated value; asserted 12/12) |
| SUB-MULTI (multi-hop) | 24 | 24, expect=value | 24 alpha-pos chains: "X comes after/before Y" + asserted pos(Y); all derived values hand-computed | ≥0.90 (22/24) |
| SUB-CORE (coreference) | 24 | 24, expect=value | 24 two-sentence items; sentence 1 sets entity, sentence 2 uses pronoun (it/this/that) or "the word"/"the letter" + new relation; probe names entity explicitly | ≥0.90 (22/24) |
| SUB-DISTR (distractors) | 480 (240 sol championship + 240 distractors) | 240 (sol championship probes, expect=value) | 240 distractor sentences (48 unrelated entities × 5 templates), no overlapping entities/relations, internally value-consistent | clean mastery = 1.0000 (228/228), i.e. unchanged |

Scoring: "clean mastery" = correct / 228 (the 12 planted-falsehood probes per
source excluded). Sub-battery value probes score on the returned value;
contradiction/hedged/unknown probes score on the verdict label.

## 3. Kill bars

- **KB2-VIABLE**: clean mastery **1.0000 (228/228) per source** on the 4
  championship prose test sets. Micah: meet-or-beat the integer baseline,
  else the prose path doesn't ship.
- **KB2-DET**: **5/5 byte-identical per source** on championship sets;
  **3/3 on sub-batteries** (sol only).
- **KB2-QUALITY**: Q = mean(clean grok, clean sol) − clean step;
  **≥0.02 QUALITY-MATTERS**, **|Q|<0.02 NO-DIFFERENTIATION** (same frozen rule
  as v1; v1 measured +0.0022 → NO-DIFFERENTIATION).
- **KB2-FALSEHOOD**: absorption of the 12 planted falsehoods per source vs
  v1's 12/12 — **measurement**; document the mechanism of any non-absorption.
- **KB2-NOSILENT**: no probe may return a value from a negated-only,
  hedged-only, or contradicted key.

## 4. Frozen checksums

### inputs2 (this battery)

```
c28873da6f82b5bf233f6d71641880dbc853d2bde4683d1f96dd0b8e0ae8187a  sub_contr_test.jsonl
76f9bd42a81d6b24728744007372bbfc91001000edbaeebd8094940c85e4cb6b  sub_contr_train.jsonl
6a2e419f7a34df66cca3080cbcb5550d666356147a1f452abff23d3c3a542add  sub_core_test.jsonl
736c27599a206db33639db250b4d7b3ec88e2d975de8b817389e4a2710a4c77c  sub_core_train.jsonl
6134010b174ac41a028e5a005442a0e3cd48144b27e9c728fdc8997ed5f29a2b  sub_distr_test.jsonl
f45f991b9954f2bd5aaf828d2a1b4ce3c2a1d2e52ba2b718ba0e4d4cf225f74f  sub_distr_train.jsonl
ded734b499acb6f5ed34564863f8621d5d49b84463b72127d51ae02c1176474b  sub_hedge_test.jsonl
daab35e12be531be5854814f2e2d7675941946bb6080e6fb48d78635306e45c2  sub_hedge_train.jsonl
7b8ccc6bad69a94a5e667fe02e9689e0ae458e59d1e914aa87a68a09c3ad1626  sub_multi_test.jsonl
bf3ae75bc645faa42069ae91b0a2d3ece179f1ead9e2a8e05262abb736aad313  sub_multi_train.jsonl
b1c3952f36c25b532351d7a6aab6161031942ba1f8de8a77546620dd257586a3  sub_neg_test.jsonl
4b90b5cca4e98e4e79a1de0ec73ec212de9a298da68d3383416577137c1dd74c  sub_neg_train.jsonl
919a44bfd69ff5b919473a366b822831f2aecf118c707c887b4ad1249c707dfe  sub_para_test.jsonl
a1bdc295f0421faba2e924f4fff3b6e388dd8e712a5a25403eb69eeff0a2e1ee  sub_para_train.jsonl
```

### Championship inputs re-freeze (as on disk 2026-09-21/22)

```
cb7d129fb671b999340bb5f880bf5ccb5aa28596c940838d59738cce132e5f3a  train_grok.jsonl
2d0740f4c24b65ada9e9e5089047b2a1c39ff327e65a057941c0b0d71c94c9c8  train_sol.jsonl
b2cc59ad65e108bf3f909b6274b493d7a649cd705d694a26595c969d4abd6d32  train_step.jsonl
4f226b6fac39c3bf8a3d39f37edb1432f13649762fb36e41ad3505bf08e27f7d  train_muse-native.jsonl
2c29f62b93e51696276cb0a7993288a333224d37acde4bed26bd7abac24a0b5b  test_grok.jsonl
80de5ddfc175e30a9b256d9df4f35f95869bd798ce0ba325c5b4a14d2f0fc6f2  test_sol.jsonl
92e30e0d1c451988ff7c4b740c1828d231c573a1dbaca285cd3138e17a409492  test_step.jsonl
2ababe756e4fc76dc6491c7074ad2df2618ecc1963860025a1efd7a92ff9b0eb  test_muse-native.jsonl
```

**Note on `test_grok.jsonl`.** The task brief for this battery stated v1's
test_grok checksum amendment was still unsigned by Micah. On-disk evidence
found during construction contradicts that:
`~/workspace/tnn-lab/prose-learning/AMENDMENT_2026-09-21_test_grok_checksum.md`
records **"Status: APPROVED by Micah, 2026-09-21"** ("do both": sign the
amendment AND re-freeze from the verified copy), and the current on-disk hash
`2c29…7abac24a0b5b` matches the amendment's re-frozen value exactly. This
prereg therefore treats the re-freeze as governed by that signed amendment.
Flagged for the parent orchestrator to reconcile with the brief.

## 5. Honesty record

- Every constructed item hand-verified by `verify_inputs2.py`; see
  `~/workspace/richcomp/VERIFY.md` (1 item fixed: core id 19, "twice" →
  "2 times", so the last-number value rule applies).
- No RNG used in battery construction (fixed hand-picked selections, fixed
  templates); builder re-run reproduces all files byte-identically.
- Championship inputs were not modified. Planted-falsehood entities are never
  used as asserted-truth entities in constructed items.
- Worker A did not build or run any learner. Worker B owns the learner and
  all runs against this frozen battery.

**Frozen 2026-09-22. No further edits.**
