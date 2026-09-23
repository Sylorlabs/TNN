# PROSE-LEARNING — grok-4.7 addendum (2026-09-22)

**What this is:** the one significant grok-4.6 run that had never been mirrored
with grok-4.7. The prose-learning verdict (`VERDICT.md`, prereg `PREREG.md`,
frozen 2026-09-21) compared four teacher sources — grok-4.6, gpt-5.6-sol,
step-3.7-flash, muse-native — on the frozen prose-consuming battery. The
teacher-showdown Leg C (2026-09-22, committed) ran grok-4.7 through the **same
frozen battery** using the captured 4.7 corpus
(`GROK47_OVERNIGHT/teacher/evidence/grok47_corpus/corpus.json`,
sha256 `111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a`;
no new grok-4.7 API calls — the delisting blocks nothing). The learner binary
was rebuilt with the pinned znc and proven byte-faithful first (one run on the
frozen grok-4.6 inputs reproduces `runs/grok_rep1.log` byte-for-byte), 5/5 runs
byte-identical, independent Python oracle 0-diff. This addendum applies the
frozen `PREREG.md` bars, unchanged, to the 4.7 row. Bars are identical to the
4.6 runs — apples-to-apples.

## The 4.7 row (verified from `runs/grok47_rep1.log`)

| Source | Extraction | Clean mastery | Full mastery | Absorption | 5/5 identical |
|---|---|---|---|---|---|
| grok-4.6 (frozen) | 240/240 (1.0000) | 189/228 (0.8289) | 197/240 (0.8208) | 12/12 | yes |
| **grok-4.7** | 240/240 (1.0000) | **213/228 (0.9342)** | **223/240 (0.9292)** | 12/12 | yes |
| gpt-5.6-sol (frozen) | 240/240 (1.0000) | 220/228 (0.9649) | 231/240 (0.9625) | 12/12 | yes |
| step-3.7-flash (frozen) | 240/240 (1.0000) | 204/228 (0.8947) | 214/240 (0.8917) | 12/12 | yes |
| muse-native (frozen) | 240/240 (1.0000) | 200/228 (0.8772) | 211/240 (0.8792) | 12/12 | yes |

Δ (4.7 − 4.6): clean **+24 (+10.5pp)**, full **+26 (+10.8pp)**; per-probe diff
**26 gained, 0 lost** (Leg C verdict).

## Bars applied mechanically (frozen PREREG.md, unchanged)

| Bar | Rule | grok-4.6 outcome (frozen) | grok-4.7 outcome |
|---|---|---|---|
| KB-EXTRACT (≥0.99) | value-scan on 960 train sentences | PASS 1.0000 | **PASS** 1.0000 |
| KB-PROSE-VIABLE (≥0.98 clean) | prose ≥ integer baseline −2pp | TRIPS 0.8289 (−15pp) | **TRIPS 0.9342 (−4.6pp)** — still below bar, gap shrinks by ~10pp |
| KB-DETERMINISM | 5/5 byte-identical | PASS | **PASS** |
| KB-QUALITY | Q = mean(grok,sol) − step; ±0.05 three-bin (doc-sweep correction, proposed C3): Q≥+0.05 QUALITY-MATTERS, \|Q\|<0.05 NO-DIFFERENTIATION, Q≤−0.05 INVERSE | +0.0022 → NO-DIFFERENTIATION | **+0.0548 → QUALITY-MATTERS** |
| KB-FALSEHOOD | absorption vs integer-leg 49/49 | 12/12 | **12/12** — identical |

Q arithmetic (clean mastery): mean(213/228, 220/228) − 204/228
= mean(0.93421, 0.96491) − 0.89474 = 0.94956 − 0.89474 = **+0.0548** ≥ +0.05.

## What flips and what doesn't

1. **KB-QUALITY flips.** The prose verdict's mandated answer #1 — "does model
   quality differentiate when the TNN reads words? No (|Q| = 0.0022 < 0.05)…
   the quality hypothesis is refuted in the prose channel too" — was computed
   with grok-4.6. Substituting grok-4.7's numbers, the identical bar returns
   QUALITY-MATTERS. **With 4.7, model quality differentiates in the prose
   channel.** The mechanism is identified, not hand-waved (Leg C verdict):
   4.7 writes entity-named declarative sentences ("The publication year of
   Candide is 1759.") where 4.6 wrote bare fragments ("The publication year is
   1759."), collapsing retrieval ties (multi-way → unique). Wording specificity
   is a genuine quality-driven teaching effect under this pipeline.
2. **Boundary honesty.** Q_47 = +0.0548 sits just above the +0.05 band edge;
   SE(Q) ≈ 0.024 → z ≈ 2.3 from zero. Under the mechanical rule the flip is
   real, but it is a boundary result, not a blowout. The stronger evidence is
   the direct head-to-head: Δ_clean = +0.1053, z ≈ 3.5, 26 gained / 0 lost.
3. **KB-PROSE-VIABLE still trips.** 4.7 is the best prose teacher measured
   (0.9342 vs sol 0.9649, step 0.8947, muse-native 0.8772, 4.6 0.8289), on a
   prose channel that still underperforms the integer-leg baseline. Best on a
   path that isn't viable at the bar — the showdown's standing record
   (4.7 champion teacher) is strengthened; the prose-path viability verdict is
   unchanged.
4. **KB-FALSEHOOD unchanged.** 12/12 absorption for both groks; the 2
   false-id "gains" (117, 139) are planted falsehoods 4.7 installs *and* makes
   retrievable. Better teaching cuts both ways.

## Lineage

- 4.7 inputs: `prose-learning/inputs/{train,test}_grok47.{jsonl,txt}`,
  `false_ids_grok47.{json,txt}`; builder `prose-learning/src/build_grok47_inputs.py`
  (Leg C, committed).
- Learner: `prose-learning/src/prose_learn.zag`, frozen mechanism, rebuilt
  2026-09-22 with pinned znc (byte-faithful proven).
- Runs: `prose-learning/runs/grok47_rep{1..5}.log` (5/5 byte-identical;
  SUMMARY line verified: `extract=240/240 full=223/240 clean=213/228
  absorb=12/12`).
- This addendum performs no new runs and amends nothing frozen; it applies
  the frozen bars to the committed 4.7 results.
