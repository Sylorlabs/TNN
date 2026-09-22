# PROSE-LEARNING verdict — 2026-09-21/22

Micah's question: does model quality differentiate when the TNN actually READS the
LLM's words? The numeric channel said no (standardized class-3 Δ = 0.0000). This
experiment runs the same fact sets through a prose-consuming learner.

Prereg: `PREREG.md` (frozen before any learner run). Builder implemented the frozen
mechanism verbatim; an independent Python oracle matches the Zag binary with 0 diffs
on all 4 sources (per-probe, per-install, digest, ledger terminal hash).

## Results (4 sources × 5 reps, byte-identical full logs)

| Source | Extraction | Clean mastery | Full mastery | Absorption | 5/5 identical |
|---|---|---|---|---|---|
| grok-4.6 | 240/240 (1.0000) | 189/228 (0.8289) | 197/240 (0.8208) | 12/12 | yes |
| gpt-5.6-sol | 240/240 (1.0000) | 220/228 (0.9649) | 231/240 (0.9625) | 12/12 | yes |
| step-3.7-flash | 240/240 (1.0000) | 204/228 (0.8947) | 214/240 (0.8917) | 12/12 | yes |
| muse-native | 240/240 (1.0000) | 200/228 (0.8772) | 211/240 (0.8792) | 12/12 | yes |

Digest (truncated) / ledger terminal hash per source are in the run logs'
`DIGEST`/`LEDGER` lines (`runs/<source>_rep<1..5>.log`).

## Kill bars — applied mechanically

| Bar | Rule | Outcome |
|---|---|---|
| KB-EXTRACT (≥0.99) | value-scan success on 960 train sentences | **PASS** — 1.0000 all sources, zero failures |
| KB-PROSE-VIABLE (≥0.98 clean) | prose must reach integer baseline −2pp | **TRIPS on all four** — 0.8289 / 0.9649 / 0.8947 / 0.8772. No re-tuning was done. The prose path underperforms the integer-leg baseline by 3.5–17pp. |
| KB-DETERMINISM | 5/5 byte-identical | **PASS** — full logs byte-identical per source; binary self-verifies (ledger recompute + double digest) |
| KB-QUALITY | Q = mean(grok,sol) − step; ≥0.02 matters, \|Q\|<0.02 none | Q = 0.8969 − 0.8947 = **+0.0022** → **NO-DIFFERENTIATION**. The numeric-channel result reproduces in prose. |
| KB-FALSEHOOD | absorption vs integer-leg 49/49 | **12/12 on every source** — prose gives the learner no additional grip on smooth lies. |

## Why the prose path underperforms (frozen-spec-inherent mechanisms)

The misses are retrieval ties, not extraction failures. Dominant mechanisms:

1. **Key collapse via stopwords/number-words as entities.** Word-len facts about the
   words "an", "four", "seven", "the" lose their entity from the key (stopword or
   number-word), leaving bare keys like {letter, count, word}.
2. **Bare-key facts win ties via lowest-id.** ("The letter count of word is 4.",
   "The publication year is 1759.") — the deterministic tiebreak systematically
   favors early facts.
3. **Stemmer conflations** (`misunderstandings`→`misunderstanding`,
   `incomprehensibilities`→`incomprehensibility`) merging distinct facts.
4. **Train/test wording gaps.** sol probe 18 ("What is the alpha-pos value of S?")
   has key {alpha,pos,value}, disjoint from every train key (train says "alphabet
   position"; "s" is a stopword) → 240-way all-zero Jaccard tie → fact 0.

Tie counts: grok 106/240 probes tied (35 tied&wrong), sol 54 (9), step 43 (23),
muse-native 12 (10). Every PROBE line in the logs carries `ties=N best=<fact>`.

Notable ordering (descriptive, not a bar outcome): sol > step > muse-native > grok.
sol's terse prose ("A has the value 1.") minimizes key collisions; grok's richer
prose maximizes ties. Wording SHAPE affects this pipeline more than model "quality".

## Answers to the two mandated questions

1. **Does model quality differentiate when the TNN reads words?** No — per the
   frozen rule, |Q| = 0.0022 < 0.02. The quality hypothesis is refuted in the
   prose channel too, under this pipeline. (Scope: bag-of-stemmed-content-words
   retrieval; a richer comprehension architecture is a different experiment.)
2. **Falsehood absorption, prose vs integer legs?** Identical: 12/12 in prose,
   49/49 in integer legs. Fluent, unhedged falsehoods install smoothly in both
   channels. Prose style cues do not exist in these corpora (zero hedging
   observed), and nothing in the pipeline could use them if they did.

## Integrity note — prereg checksum amendment PROPOSED (needs Micah's signature)

`test_grok.jsonl` on disk no longer matches its frozen prereg sha256
(`2c29…409492`; current file `2c29…7a0b5b`; byte-level rewrite, size/mtime
unchanged). The current content was verified **0-diff against the authoritative
championship `corpus.json`** (whose `SHA256SUMS.txt` is intact); the original
serialization is unrecoverable. The experiment ran on semantically-verified
content. Proposed amendment: replace the frozen checksum with the verified
current file's. NOT applied unilaterally — flagged for Micah's dated approval.

## Lineage

- Inputs: `inputs/` (frozen w/ sha256; `.txt` conversions via `src/convert_inputs.py`)
- Learner: `src/prose_learn.zag` (pure Zag, zero RNG), built with
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Oracle: `src/oracle.py` (independent Python pipeline, 0-diff vs Zag)
- Runs: `runs/` — 20 logs, 4 sources × 5 reps
