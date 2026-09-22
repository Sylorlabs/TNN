# TEACHER SHOWDOWN — LEG C (prose teaching) VERDICT

**Date:** 2026-09-22. **Status:** RUN COMPLETE. This supersedes the "LEG C — NOT RUN
(pending)" section of `SHOWDOWN_VERDICT.md` (which is left frozen as the record of
the earlier task); the Leg B verdict there is unaffected — Leg C cannot overturn it
and does not need to.

**Question (SHOWDOWN PREREG.md, Leg C):** run grok-4.7 vs grok-4.6 as prose teacher
on the frozen prose-learning battery. Registered weak prediction P-C1: 4.7 ≈ 4.6
within the battery's noise band. Decision rule: 4.7 "beats" 4.6 on a preregistered
metric with material margin — Leg C counts if the battery margin is runnable.

## Procedure (exactly the pending step from SHOWDOWN_VERDICT.md)

1. Corpus: `GROK47_OVERNIGHT/teacher/evidence/grok47_corpus/corpus.json`,
   sha256 `111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a`
   (hash re-verified before building inputs; no new grok-4.7 API calls — the
   delisting blocks nothing).
2. Inputs: `prose-learning/src/build_grok47_inputs.py` built
   `inputs/{train,test}_grok47.{jsonl,txt}` + `inputs/false_ids_grok47.{json,txt}`
   from the corpus's `dump` sentences (train), `teach` probes + `probe_value`
   (test), and `false_ids` (the same 12 planted ids). Line format byte-identical
   in structure to the frozen `convert_inputs.py` output; 240/240/12 rows, ids
   0..239 asserted, no tabs/newlines in sentences.
3. Learner: `src/prose_learn.zag` rebuilt with the pinned znc
   (`toolchain/bin/znc_linux_x86_64_abed8aa1`). The rebuild was proven faithful
   first: one run on the frozen grok-4.6 inputs reproduces `runs/grok_rep1.log`
   **byte-for-byte** (SUMMARY/DIGEST/LEDGER/VERIFY all identical).
4. Runs: `./prose_learn_bin grok47`, 5 reps, logs `runs/grok47_rep{1..5}.log`.
   Pure Zag, zero RNG in any decision path.
5. Cross-check: independent Python oracle (`src/oracle.py::run`) on the grok47
   inputs — 0 diffs vs the Zag binary (extract/full/clean/absorb, digest and
   ledger terminal hash all match).

## Results

| Source | Extract | Full mastery | Clean mastery | Absorption | 5/5 identical |
|---|---|---|---|---|---|
| grok-4.6 (frozen) | 240/240 | 197/240 (0.8208) | 189/228 (0.8289) | 12/12 | yes |
| grok-4.7 | 240/240 | **223/240 (0.9292)** | **213/228 (0.9342)** | 12/12 | yes |
| Δ (4.7 − 4.6) | 0 | **+26 (+10.8pp)** | **+24 (+10.5pp)** | 0 | — |

Δ_clean = +0.1053, SE(diff) ≈ 0.030 → z ≈ 3.5. Well outside the ±0.05 noise band
(the corrected three-bin rule from the prose doc-sweep, proposed C3).

Per-probe diff: **26 gained, 0 lost.** Clean gains (24): ids 79, 81, 83 (word-len
family), 109–116, 118, 119 (pub-year family), 132–138, 140–143 (pub-year family).
Plus 2 false-id gains (117, 139 — planted falsehoods, excluded from clean).

## Mechanism (identified, not hand-waved)

The gains are a **wording-specificity effect** in 4.7's dump sentences, and every
gained probe shows the same signature: a tie collapse (multi-way → unique) or a
wrong-unique → right-unique flip.

1. **Pub-year family (109–119, 132–143): entity-named sentences.** 4.6's dump
   sentences are bare fragments — "The publication year is 1759." — whose key
   after the frozen pipeline is the bare {publish, year}, shared across ~48 facts.
   Probes ("In what year was Candide published?") then 24-way tie and lose to the
   lowest-id fact (log: `ties=24 best=108`). 4.7's dump sentences name the entity —
   "The publication year of Candide is 1759." — giving discriminating keys and
   unique retrieval (`ties=1 best=109`). The frozen dump prompt asks for "one
   declarative sentence stating that English fact"; 4.7 states the fact as given,
   4.6 drops the claim. The complete sentence is the better teaching utterance,
   and the learner can only learn from what the sentence contains.
2. **Word-len family (79, 81, 83): probe/dump key alignment.** 4.6's probe "How many
   letters does the word sentence contain?" collides with fact 78's key ("of word")
   → 2-way tie lost to fact 78. 4.7's probe "How many letters does "sentence"
   contain?" aligns with its dump key → unique winner.
3. **NOT the Leg B faithfulness fix.** Ids 88–94 (4.6's word-length miscounts,
   corrected by 4.7) are *unchanged* in the prose scores: both runs lose those
   probes to the same fact-78 tie (`ties=2 best=78`). 4.7 installs the now-correct
   value, but the tie mechanism dominates. The prose gain and the faithfulness
   gain are independent effects.

## Kill bars (prose PREREG.md, applied mechanically)

| Bar | Rule | Outcome |
|---|---|---|
| KB-EXTRACT (≥0.99) | value-scan success on train sentences | **PASS** — 240/240 |
| KB-PROSE-VIABLE (≥0.98 clean) | prose ≥ integer baseline −2pp | **TRIPS** — 0.9342 < 0.98. The prose path still underperforms the integer-leg baseline (~6.6pp). Tripped on all four original sources too; no re-tuning done. |
| KB-DETERMINISM | 5/5 byte-identical | **PASS** — full logs byte-identical; VERIFY chain=1 dmatch=1; oracle 0-diff |
| KB-QUALITY analog (Leg C margin) | \|Δ\| ≥ 0.05 material | **4.7 WINS** — Δ=+0.1053, z≈3.5 |
| KB-FALSEHOOD | absorption vs integer-leg 49/49 | **12/12** — identical to 4.6. Prose gives the learner no additional grip on smooth lies. |

## Verdict

**grok-4.7 WINS Leg C with material margin** (+10.5pp clean mastery, +26/−0 probes,
mechanism identified). The registered weak prediction **P-C1 is REFUTED**: 4.7 is
not "≈ 4.6 within noise" in the prose channel — its self-contained, entity-named
teaching sentences are genuinely more learnable by the frozen prose pipeline.

This **strengthens the showdown's standing record** (grok-4.7 champion teacher:
Leg B faithfulness blowout + Leg C prose-teaching win; Leg A numeric tie). It does
not change the Leg B verdict and was never able to.

## Honest caveats

1. The win is **wording-specificity under this pipeline** (bag-of-stemmed-words
   Jaccard retrieval), not a general "prose comprehension" result. A richer
   comprehension architecture is a different experiment (cf. prose VERDICT.md).
2. **Better teaching cuts both ways:** the 2 false-id "gains" (117, 139) are
   planted falsehoods that 4.7 installs *and* makes retrievable. Absorption stays
   12/12; nothing in the pipeline resists fluent unhedged falsehoods.
3. **KB-PROSE-VIABLE still trips** (0.9342 < 0.98): the prose channel remains
   below the integer-leg baseline for every source tested. 4.7 is the best
   prose teacher measured, on a path that is still not viable at the bar.
4. The ±0.05 three-bin rule applied here is the doc-sweep correction (proposed C3,
   pending Micah's signature). Δ=+0.1053 clears even the prereg's original ±0.02
   band by 5x, so the outcome does not depend on which band is in force.

## Lineage

- Inputs: `prose-learning/inputs/{train,test}_grok47.{jsonl,txt}`,
  `false_ids_grok47.{json,txt}`; builder `prose-learning/src/build_grok47_inputs.py`
- Learner: `prose-learning/src/prose_learn.zag` (unchanged, frozen mechanism);
  binary built 2026-09-22 with pinned znc (build proven byte-faithful vs frozen
  grok rep1); binary NOT committed per convention
- Runs: `prose-learning/runs/grok47_rep{1..5}.log` (5/5 byte-identical)
- Oracle: `prose-learning/src/oracle.py` (0-diff cross-check)
- Corpus: `GROK47_OVERNIGHT/teacher/evidence/grok47_corpus/corpus.json`
  (sha256 `111f588f…f467a`, re-verified at build time)
