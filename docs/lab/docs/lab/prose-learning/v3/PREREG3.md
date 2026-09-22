# PREREG3 — prose learner v3: deliberate repair of v2 (FROZEN 2026-09-22)

Status: FROZEN. No change to mechanism, inputs, battery, or bars without a
dated Micah-approved amendment. v2 stays frozen and untouched; v3 is a
separate implementation (`v3/src/`). No scored v3 run has occurred as of
this writing.

## 1. Background

- v1 prose (pinned): clean mastery grok 0.8289, sol 0.9649, step 0.8947,
  muse-native 0.8772 — all below the frozen ≥0.98 bar; Q = +0.0022
  (NO-DIFFERENTIATION, model-quality hypothesis abandoned).
- v2 (frozen, commit 51e6d4dace27): bought real deterministic capabilities
  (CONTR 24/24, HEDGE zero leaks, NEG zero leaks, MULTI 24/24, dense
  paraphrase 48/48) but collapsed single-exposure clean mastery
  (grok 0.2588, sol 0.2851, step 0.3289, muse-native 0.6316) because exact
  `(entity, relation-set)` keys are brittle to paraphrase.
- Micah's decision 2026-09-21: v1 stays the pinned prose path; a v3 repair
  crew runs with preregistered ablations.

## 2. GATE 0 resolution (closed 2026-09-22)

The Worker-B (9,11,11,11) vs Worker-C verdict discrepancy is resolved;
see `GATE0_RESOLUTION.md`. Summary:

- Worker B's figures reproduce exactly under the metric **ABS-3**:
  INSTALL event with attitude=asserted carrying the planted false value,
  parsed with correct multi-token-entity handling.
- Worker C's (4,6,7,5) row was ABS-3 computed with a parser that dropped
  multi-token entities (measurement bug).
- Worker C's (10,12,12,12) row is ABS-3 plus one CONTRADICT old/new event
  per source (id 29's collision on id 3's key); it over-counts by crediting
  dead keys, so it is NOT the frozen metric.

**Frozen metric ABS-3.** Absorption = n/12, where n counts planted-falsehood
fact ids whose planted false value appears in an INSTALL ledger event with
attitude=asserted (value compared exactly). Secondary descriptives
reported alongside: ABS-live-at-end (key still live after training),
ABS-probe (v1-identical probe behavior).

## 3. The four changes (each specified separately, each gated)

### C1 — Dense phrasing regime (input change, no mechanism change)
Every championship fact is taught in 3 phrasings: the original plus two
deterministically generated canonical paraphrases. Builder:
`v3/build_inputs3.py`. Rules: category detection (alpha/wordlen/pubyear/
open), slot extraction, template emission, verification per wording
(value-scan == probe_value, single sentence, string-distinct from original
and from each other). Fallback (documented): items with no extractable
slots repeat the original 3× — exactly 24 facts, all grok degenerate
pubyear items whose train text names no title ("The publication year is
1759."), unlearnable without test-leak. Result: 936/960 facts × 3 distinct
wordings. Championship probes, false-fact ids, and all sub-battery inputs
are unchanged except §3.4. Falsehood facts are paraphrased with the false
value (same regime, no special-casing).

### C2 — Coreference tag order (mechanism change)
v2's train tagger order `2a → 2b → 2c → 2d → coref` starves coreference:
"the word"/"the letter" in sentence-2 position are claimed by rule 2d
before coreference sees them (CORE 11/24). v3 moves the existing
train-only coreference block before rule 2d: `2a → 2b → 2c → coref → 2d`.
Coreference keeps its `peid != EMPTY` guard and train-only restriction.
Explicit quoted entities, single uppercase letters, and relation-phrase
entities keep priority (2a/2b/2c unchanged). Any other battery movement
between A1 and A2 is attributed to this change.

### C3 — NEG battery rebuild (input fix, no mechanism change)
v2's NEG probes 18/30 and 19/31 are identical strings with conflicting
expectations (perfect 36/36 impossible). v3 rephrases probes 18 and 19
(the negated-only, expect-unknown items) to
'How many members are in the "Beatles"?' and
'How many members are in the "Jackson 5"?'.
All 36 probe strings are now unique. Train side unchanged.

### C4 — KEYSOFT tier-3 probe fallback (mechanism change, preregistered option)
Deterministic Jaccard ≥ 0.5 sentence-similarity fallback over LIVE
asserted rows only, consulted only when all v2 probe tiers miss and the
entity-exact/Jaccard fallback finds no candidate. Spec:
- At INSTALL of an asserted row, store the sentence's sorted-unique
  content-stem unit ids (cap 64; first 64 after sort if more).
- At probe: build the probe's sorted-unique content-stem list; per live
  asserted row (status==0) compute inter/union by merge-join; accept iff
  union>0 and 2*inter >= union; argmax by cross-multiplication
  (inter1*union2 vs inter2*union1, i64); ties → lowest fact id.
- Winner → VALUE:<row value>; else UNKNOWN.
- Contradicted / quarantined / denial rows never yield VALUE (KB3-NOSILENT).
Rationale: KB2's exact-key brittleness is the exact failure C1 attacks at
train time; C4 is the probe-time counterpart. Tested as a separately
preregistered option per standing "test both" law, because it softens the
exact-key guarantee and could reintroduce unreachable-lie risk.

## 4. Ablation legs (each = full championship × 4 sources + sub-batteries)

| Leg | Inputs | Mechanism | What it isolates |
|---|---|---|---|
| A0 v2 | v2 single-phrasing inputs | v2 (frozen binary) | baseline replication |
| A1 v2+dense | v3 dense inputs (§3.1) | v2 (frozen binary) | C1 alone |
| A2 v2+dense+coref | v3 dense inputs | v3 mode m1 (C2 only) | C2 on top of C1 |
| A3 v3 | v3 dense inputs | v3 mode m2 (C2+C4) | C4 on top of C2 |

Mode is `argv[2]` of `prose_learn3`: `m0` = v2-exact, `m1` = C2 only,
`m2` = C2+C4. A0 runs the frozen v2 binary, not prose_learn3 m0.

## 5. Battery and scoring

- Championship: dense train (720 lines/source), frozen 240 probes/source,
  false ids = 36 train ids/source (3 per false fact). Clean mastery =
  correct / 228 (12 planted-falsehood probes excluded), per source.
- Sub-batteries: v2's frozen inputs verbatim (PARA, CONTR, HEDGE, MULTI,
  CORE, DISTR) plus the rebuilt NEG (§3.4). Scored with v2's rules.
- Each scored run: 5 repetitions; KB3-DET requires byte-identical logs.
- Independent oracle (`oracle3.py`) must reproduce every leg's log
  byte-identically (oracle modes m0/m1/m2 match learner modes).

## 6. Kill bars

- **KB3-VIABLE**: A3 beats v1's clean mastery on ≥3/4 sources AND retains
  all v2 capability wins (CONTR 24/24, HEDGE zero leaks, NEG zero leaks on
  the rebuilt battery, MULTI 24/24, dense PARA 48/48 on v2's battery).
  (v1's bar is its recorded clean mastery per source, §1 — not 0.98,
  which v1 itself never reached.)
- **KB3-DET**: 5/5 byte-identical repetitions per scored run.
- **KB3-NOSILENT**: zero VALUE verdicts from contradicted, negated-only,
  or hedged-only keys (checked on logs, all legs).
- **KB3-FALSEHOOD** (measurement, no kill): ABS-3 per source per leg,
  with mechanism of any non-absorption documented.
- **KB3-QUALITY** (measurement): report Q per leg; no bar (Micah abandoned
  universal differentiation, but reporting continues).

If KB3-VIABLE fails, the verdict names which of C1/C2/C4 carried the
improvement (from the ablation deltas) and whether any subset meets a
revised bar — no post-hoc bar movement without a dated amendment.

## 7. Frozen input checksums (sha256, `v3/inputs3/`)

Championship dense train:
- e960894549b9250629a9e46ed279868bae9eec3691ac8aaad4ea0c57d5dcbe5a train_grok.txt
- 3412bbe9650e3735abb71d96835c8f357b03081613a50b1fbd449fc51b7a4f52 train_sol.txt
- 174771f3b8675c2546ebeefc211f32f186aa65dd8b0b2645f25b083ee93d4937 train_step.txt
- 6e4aa751a9eb3c944177bf93edf3ccf38cbf75a1c773ed70010da3173f9b0dbe train_muse-native.txt
Championship test (unchanged probes):
- 39afb1904acabb9b05179e6c7490d1045e512e45e0cc8a4d67d846b5493e681c test_grok.txt
- d1935ce986b6c32824139417ab0546f6f7f709789f82fcffe69d7c655adb6554 test_sol.txt
- 749f6b2851937deda8d1d01b53f2614416611fd871b9e34072377fdd6d1919a0 test_step.txt
- ab2029414ebe272b00daeb8bab9d5b21187c8a9a6e8535769889b0489cbf85b5 test_muse-native.txt
False ids (36/source, identical across sources):
- c6ebdf1dc514617436b97cdcfaa8f291cab8d3eda8c2f9ca3ecf46bc057acaf6 false_ids_{grok,sol,step,muse-native}.txt
Sub-batteries:
- 21b1155985b57de3d56e771a2c68a00b5aaf18881368acd3df011bc7e64542d3 sub_para_train.txt
- f570ae537d97300022bdfd60bb0cc450d9c993a090e6f5250cffe17821e128f6 sub_para_test.txt
- 300aa57765f2d31344f2c605a20af86c0735d76e3cdec1846a1aa4100d2aeab6 sub_contr_train.txt
- e5166abdb90b3243d217ec1a03caf9039043908bed159e6d8d374d80c5d8c4ff sub_contr_test.txt
- c35a10486a4781566e44643f69c67e16183a236d290b244f34171f5efd2a481b sub_hedge_train.txt
- cd958fb9972fc89ae660cd955ff7d93001a285bc821ac1cabc8b4b7e677fab3f sub_hedge_test.txt
- e7d1c37663773a2ee01ab70429427d891af9240b26b5862a07e20d642acc7b78 sub_neg_train.txt
- c160c8478204b88e934e160f1a9f8e1a6d7e8c57fcf9894f84ea6a48662e0422 sub_neg_test.txt
- 6f5755d85062af3d00a3e48b4ed270869738bc8e3c06bbfd16e6a19b4058152b sub_multi_train.txt
- 55d8773ea6426926cb51ab92f35098fd9c001dd8b47a217949d66d3ea72de4fb sub_multi_test.txt
- e22d08c1f909e5c8674b82b21a5e25ec81e8b174944cfc665f148be77c85f21c sub_core_train.txt
- bc81a0f2c3e13c3af44e31ef75731d80bfa2edde233819bebb8e7cfa6ee6294b sub_core_test.txt
- f1942e57b5f87c63c8307e492bffe5b04c419d388d95dd5446bcdfff5cb2cf35 sub_distr_train.txt
- cf930412047b7c1e863303217a0f9888f7d1e44c9cc8bd548396770459ab1590 sub_distr_test.txt

Builder: `v3/build_inputs3.py` (deterministic; re-running reproduces all
checksums). NEG source JSONs: `v3/inputs3/negfix/sub_neg_{train,test}.jsonl`.

## 8. Appendix H — external hypotheses register (non-normative)

Added 2026-09-22, after freeze, per Micah's standing order to consult Sol
and Grok on the v2-redo/v3 and fold their input into PREREG3. This appendix
records hypotheses **as hypotheses** — they are candidates to test, not
conclusions adopted. It changes nothing normative: the mechanism (§3),
inputs (§7), battery (§5), and kill bars (§6) are untouched. Each test
below requires its own preregistered bars (dataset, metric, kill
criterion) before any scored run; none are authorized by this appendix.
Per the standing "test both / test everything" law, untested hypotheses
stay on the table until an experiment kills them.

Attribution: Sol (gpt-5.6-sol via UnoRouter) and Grok (grok-4.6 via
UnoRouter); both notes received 2026-09-22 and folded in below.

### 8.1 Why-v2-got-brittle hypotheses (Sol)

**H1 — Overbinding of the retrieval key.** v2 treats (entity,
relation-set) as one conjunctive identity; a paraphrase preserving the
fact but changing one surface-derived component becomes a total miss.
v1's broad lexical overlap tolerated local variation; v2 converts a small
normalization error into zero recall. Status: UNTESTED as an isolated
claim. Relation to v3: C1 (dense phrasing) and C4 (KEYSOFT tier-3) both
target this mechanism from opposite ends; the A1/A3 ablation deltas bear
on it but do not isolate "overbinding" from other brittleness sources —
that isolation is what T1/T4 would provide.

**H2 — Upstream parse errors amplified by downstream symbolic exactness.**
Subject/object assignment, coreference, hedge/negation scope, and tag
ordering can produce the wrong graph even when most of the sentence was
understood; rule scheduling is part of the semantic result, not an
implementation detail. Exact graph lookup then hides partial
understanding. Status: UNTESTED. Relation to v3: C2 (coref tag order) is
one instance of a rule-scheduling effect; T2/T5 would generalize the
question.

**H3 — Compositional in theory but not in retrieval.** The index requires
the entire structured pattern to match an observed example; three
phrasings provide redundant surface evidence that compensates — a
sample-efficiency problem, not a fundamental representational inability.
Status: UNTESTED. Relation to v3: A1 (v2 + dense phrasing) is the direct
test of this claim's practical consequence; H3 predicts A1 recovers most
of the v1-vs-v2 gap. If A1 recovers little, H3 is weakened (the
brittleness is not just sample-efficiency).

### 8.2 Proposed tests (Sol) — each needs preregistered bars before running

**T1 — Representation ablation ladder.** Identical single-exposure corpus
through v1 BoW → v2 lexical keys only → +predicate → +roles →
+coreference → full graph. Proves WHICH added feature causes the
collapse. Not run; would require building the intermediate key variants
as separate preregistered legs.

**T2 — Oracle-parse vs production-parse.** Same probes with gold canonical
frames manually supplied vs normal parser. Large gap = parser/normalization
at fault; small gap = index/matcher is brittle. Not run; requires a
gold-frame probe set (preregister the construction protocol to avoid
bias).

**T3 — Single-factor paraphrase matrix.** Per fact, deterministic variants
changing exactly one property (synonym, active/passive, argument order,
nominalization, pronoun vs explicit, clause order, hedge wording,
negation wording), at 1 and 3 exposures. Gives a failure signature
instead of one aggregate score. Not run; partially overlaps v2's
SUB-PARA battery (5 wordings + 1 probe wording, uncontrolled factors).

**T4 — Exact vs partial-match retrieval with candidate traces.**
Instrumented comparison logging shared/mismatched fields, candidate rank,
polarity/modality of winner, proof or rejection reason. If partial
matching restores recall while polarity/modality constraints hold
precision, v2's defect is overbinding. Not run; C4 (KEYSOFT tier-3) is a
narrow instance — T4 generalizes it and adds the trace instrumentation.

**T5 — Rule-order and duplicate-control regression suite.** Dedup NEG
battery by semantic identity; run coref/tag rules under several declared
orderings; assert every rule consumes or preserves downstream-required
tags. Separates measurement defects from model defects. Partially
subsumed: C3 (NEG dedup) and C2 (one declared reordering) are in the
frozen plan; the generalized ordering sweep and the consume-or-preserve
assertion are not run.

### 8.3 Architectural idea (Sol) — proposal only, not adopted

Factorized quorum-based semantic index with proof-carrying retrieval:
index independent deterministic projections (predicate, subject, object,
typed roles, polarity, modality, temporal/evidential attributes, lexical
features); query combines via fixed quorum (e.g. predicate+polarity
exact, modality compatible, ≥2 of {subject, object, roles}); the
surviving candidate must pass symbolic unification and emit an
explanation. Paraphrase can damage one projection without destroying the
fact's identity; lexical similarity finds candidates, symbolic
verification decides entailment. Status: PROPOSAL ONLY — recorded per the
"test everything" law; not designed, not preregistered, not built. If
pursued, it needs its own prereg with kill bars before any scored run.

### 8.4 Pending

- None. Grok's note arrived 2026-09-22 and is folded in as §8.5 below.

### 8.5 Grok's input (grok-4.6 via UnoRouter, received 2026-09-22)

**Hypothesis.** Richer v2's structured keys replaced v1's tolerant
bag-of-words overlap with exact (entity, relation-set) matching.
Paraphrases deliberately alter surface forms, roles, and connective
phrasing, breaking the exact key while leaving lexical cues intact —
hence brittleness. Single-exposure storage amplified the mismatch; the
3+ phrasings fix worked because it restored coverage without changing
the matcher. Status: UNTESTED as an isolated claim. Note: this
converges with Sol's H1 (overbinding) and H3 (sample-efficiency); all
three predict that A1 (v2 + dense phrasing) recovers most of the
v1-vs-v2 gap. If A1 recovers little, all three are weakened together.

**Three proposed tests (all on held-out facts; each needs preregistered
bars before any scored run):**

1. **Paraphrase mastery delta.** 100 facts, 3 variants each (synonym swap
   + role reordering + hedging); score exact vs 3-phrasing storage;
   target ≥0.90 with 3-phrasings. Not run. Relation to v3: this is the
   A0-vs-A1 comparison with controlled single-factor variants — A1 uses
   the championship dense inputs instead; T3 (Sol) is the finer-grained
   version.
2. **Multi-hop + negation.** Chain a two-hop fact, negate one link, add a
   hedge qualifier; measure whether the canonical key survives or
   collapses. Not run. Relation to v3: composes SUB-MULTI and SUB-NEG
   conditions, which the frozen battery tests only separately.
3. **Coreference drift.** Same fact in two sentences, second using a
   pronoun or alternate name; track whether role binding survives
   paraphrase. Not run. Relation to v3: SUB-CORE tests the two-sentence
   coreference case; this adds the paraphrase dimension on top.

**Architectural idea (proposal only, not adopted).** Store each fact as a
canonical logical skeleton (roles + relations, no surface words) PLUS a
small set of attested surface paraphrases. Retrieval: exact skeleton
match OR bag-of-words cosine fallback. Deterministic, restores
paraphrase robustness without neural components. Status: PROPOSAL ONLY —
not designed, not preregistered, not built. Design note (open, not a
rejection): "cosine" must be given a deterministic fixed-point/rational
formulation to satisfy the byte-identical rerun law; that is a prereg
design requirement, not an optional detail.

**Head-to-head registration (test-both law).** Sol's factorized
quorum-based semantic index (§8.3) and Grok's skeleton+BoW-fallback are
now BOTH registered as v3 candidate architectures — two different
candidates, neither adopted, neither authorized for scored runs by this
appendix. Per the program's test-both law, if either is pursued it gets
its own prereg (mechanism spec, dataset, metrics, kill bars), and the
other gets preregistered alongside it; they are tested head-to-head
rather than picked by opinion. A single architecture may only ship after
beating the other (or the frozen v3) under preregistered bars.

Frozen 2026-09-22. Amendments require Micah's dated approval.
(Appendix §8 added post-freeze 2026-09-22 as a non-normative hypotheses
register; §§1–7 unchanged.)
