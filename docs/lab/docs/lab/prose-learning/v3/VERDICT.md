# VERDICT — Rich-Comprehension v3 (pure-Zag repair of prose learner v2)

Frozen: 2026-09-22. v2 remains frozen; this verdict covers the four preregistered ablation legs
(PREREG3.md §§1–7 normative; §8 non-normative hypotheses, added 2026-09-22 at Micah's direction).

## 1. Headline verdicts

| Bar | Criterion (PREREG3 §6) | Result |
|---|---|---|
| KB3-VIABLE | Full v3 beats v1 clean mastery on ≥3/4 sources | **FAIL — 2/4** (beats v1 on step, muse-native; loses on grok, sol) |
| KB3-RETAIN | Retains all v2 capability wins | **PASS** (CONTR 24/24, HEDGE zero leaks, NEG zero negated-value returns, MULTI 24/24, PARA 48/48, asserted 12/12 both) |
| KB3-NOSILENT | Zero VALUE verdicts from contradicted / negated-only / hedged-only keys | **PASS** on all legs (audit §5) |
| KB3-BYTEID | 5 byte-identical reps of every scored run | **PASS** (championship 5/5; sub-batteries 5/5, reps 4–5 done 2026-09-22) |
| Oracle verification | Independent oracle byte-identical to Zag on all scored runs | **PASS** — 16/16 championship, 26/28 sub-battery (2 misses = documented v2-binary id-17 deviation, §11) |

KB3-VIABLE is the primary bar and it **fails**. Per PREREG3 §6, the verdict names which change carried
the improvement and whether any subset meets a revised bar — **no post-hoc bar movement** without a dated
amendment. None is proposed here.

## 2. Championship clean mastery (228 clean probes per source; 12 false-fact probes excluded)

| Leg | Grok | Sol | Step | Muse-native | Q (meas. only) |
|---|---|---|---|---|---|
| A0 frozen v2, single exposure | 59/228 = .2588 | 65/228 = .2851 | 75/228 = .3289 | 144/228 = .6316 | −0.0570 |
| A1 dense phrasing only (C1) | 59/228 = .2588 | 77/228 = .3377 | 87/228 = .3816 | 158/228 = .6930 | −0.0833 |
| A2 dense + coref-order repair (C2) | 59/228 = .2588 | 77/228 = .3377 | 87/228 = .3816 | 158/228 = .6930 | −0.0833 |
| A3 full v3: + KEYSOFT tier-3 (C4) | 183/228 = .8026 | 204/228 = .8947 | 208/228 = .9123 | 227/228 = .9956 | −0.0636 |
| Frozen v1 (reference) | .8289 (189) | .9649 (220) | .8947 (204) | .8772 (200) | — |

A3 vs v1: grok −6, sol −16, step +4, muse-native +27. **Beats v1 on 2/4 (step, muse-native).**

### 2.1 Ablation deltas (per-source clean-mastery gain per change)

| Change | Grok | Sol | Step | Muse-native |
|---|---|---|---|---|
| C1 dense phrasing (A0→A1) | +0.0000 | +0.0526 | +0.0527 | +0.0614 |
| C2 coref order (A1→A2) | 0 | 0 | 0 | 0 |
| C4 KEYSOFT tier-3 (A2→A3) | +0.5438 | +0.5570 | +0.5307 | +0.3026 |

**C4 carried essentially all the improvement.** C1 contributed a small gain on 3 sources and **zero on grok**.
C2 moved nothing on the championship (predicted: coreference is near-absent from championship prose) but
fixed the CORE battery 11/24 → 22/24 (§4).

### 2.2 What the misses are (A3 residual)

| Source | Misses | Composition |
|---|---|---|
| Grok | 45 | 24 degenerate pubyear items (train text omits the title; unlearnable — see §7), ~19 wordlen (curly-quote entity mismatch + tier-3 near-ties), 2 tier-3 wrong-value (ids 64, 68) |
| Sol | 24 | 13 wordlen curly-quote probes (`“a”` vs `"a"` — entity tagger keeps the quotes), rest scattered |
| Step | 20 | scattered |
| Muse-native | 1 | — |

Precision cost of tier-3 (912 clean probes): wrong-value verdicts A1 = 8 → A3 = 30, while
unknown/other misses fell 523 → 60. Tier-3 converted ~463 unknowns into values at a cost of 22 additional
wrong values (≈3.6% error on tier-3-resolved probes). Two grok wordlen probes (ids 64, 68) were UNKNOWN in
A1 and became wrong values in A3 via near-tie Jaccard matches (ties=3). This is the C4 risk the prereg
flagged; it materialized in small but nonzero form.

## 3. Hypothesis scorecard (PREREG3 §8 — non-normative, registered 2026-09-22)

| Hypothesis | Prediction | Outcome |
|---|---|---|
| Sol H1: exact conjunctive keys overbind | Softening retrieval recovers most of the gap | **Supported** — C4 (+0.30–0.56) dwarfs C1 (+0.00–0.06) |
| Sol H3: poor sample efficiency; 3 phrasings should restore coverage | Dense phrasing recovers most of the v1 gap | **Weakened** — dense added ≤0.06 and 0 on grok; most recovery came from C4 |
| Grok: dense phrasing restores coverage without repairing the matcher | Dense alone closes most of the gap | **Weakened** — grok dense delta was exactly 0 |
| Sol H2: symbolic retrieval amplifies upstream parse/order errors | (oracle-vs-production parse test — not run in v3) | Untested here; registered for future work |

The experiment discriminates: the binding is in the **retriever**, not the exposure count. Three phrasings of
the same fact do not teach the learner much that one phrasing plus soft retrieval cannot already reach —
and on grok they taught it literally nothing new (59/228 → 59/228).

## 4. Sub-battery results (all legs ran the v3 rebuilt batteries, PREREG3 §5)

| Battery | A0 (v2 bin) | A1 | A2 | A3 | Frozen bar |
|---|---|---|---|---|---|
| SUB-PARA (48) | 48/48 | 48/48 | 48/48 | 48/48 | 48/48 |
| SUB-CONTR (24) | 24/24 | 24/24 | 24/24 | 24/24 | 24/24 |
| SUB-HEDGE (24) | 19/24, leaks 0, asserted 12/12 | 19/24, leaks 0 | 19/24, leaks 0 | 19/24, leaks 0, asserted 12/12 | zero hedged-value leaks; asserted 12/12 |
| SUB-NEG (36) | 34/36, asserted 12/12 | 34/36 | 34/36 | 34/36, asserted 12/12 | zero negated-value returns; asserted 12/12 |
| SUB-MULTI (24) | 24/24 | 24/24 | 24/24 | 24/24 | 24/24 |
| SUB-CORE (24) | 11/24 | 11/24 | 22/24 | 22/24 | (improvement; not a v2 win to retain) |
| SUB-DISTR (240) | 65/240 | 65/240 | 65/240 | 199/240 | (poor in v2; improvement allowed) |

Notes:

- **SUB-HEDGE 19/24**: the 5 misses (ids 12, 13, 21, 22, 23) are hedged→UNKNOWN, zero value leaks —
  identical in A0 (pure v2 binary) and A3. This is v2's behavior on this battery, retained, not a v3 regression.
- **SUB-NEG 34/36**: the 2 non-`unknown` results (ids 18, 19 → VALUE:4, VALUE:5) are **not** negated-value
  leaks. Both values are the live asserted values from the battery's asserted items 30/31
  (`The "Beatles" have 4 members.`), never the denied values (5/6). The phenomenon is identical in A0–A3,
  including the pure-v2 legs — it is v2's own entity-tier key-matching across battery items, and the same
  phenomenon v2's VERDICT documented on the defective battery. The rebuilt battery made all 36 probe
  strings textually unique, but the **semantic** overlap (asserted Beatles=4 elsewhere in the battery) is
  intrinsic to the battery's design: the store is global, so a probe about Beatles membership legitimately
  retrieves the asserted value. Documented as a remaining battery limitation, not hidden.
- **SUB-CORE 11/24 → 22/24**: the C2 fix. The 2 residual misses (ids 19, 21) return sentence-1's value
  (alphabet position) instead of sentence-2's (count). Root cause: sentence 2 contains a quoted word
  (`"letter"`, `"bookkeeping"`), and rule 2b (explicit quoted entities) still outranks coreference — the
  priority order the prereg deliberately preserved. A coref-before-2b change would need its own prereg.
- **SUB-DISTR 65/240 → 199/240**: tier-3's largest battery gain; distractor resistance was v2's weakest
  area and it improved without any new leaks.

## 5. KB3-NOSILENT audit (all legs, championship + batteries)

- **Contradicted keys**: id 3's key is dead (contradicted by id 29) in all sources. Probe id=3 verdicts:
  grok CONTRADICTION, sol UNKNOWN, step UNKNOWN, muse-native CONTRADICTION — **identical in A0–A3**.
  No leg ever returns VALUE from the dead key. The false-fact probes that return VALUE:<false value> in A3
  (e.g. sol 8/12) all come from **live** asserted keys (the absorbed lies, ABS-3) — that is absorption being
  measured, not a silent-truth violation. Tier-3 consults only live asserted rows by construction.
- **Negated-only keys**: zero negated values returned in any leg (SUB-NEG). The 2 VALUEs are from live
  asserted keys (§4).
- **Hedged-only keys**: zero hedged-value leaks in any leg (SUB-HEDGE value_leaks=0).
- **KB3-NOSILENT: PASS on all four legs.**

## 6. Absorption (ABS-3, frozen metric from GATE0)

| Source | A0 | A1 | A2 | A3 |
|---|---|---|---|---|
| Grok | 9/12 | 9/12 | 9/12 | 9/12 |
| Sol | 11/12 | 11/12 | 11/12 | 11/12 |
| Step | 11/12 | 11/12 | 11/12 | 11/12 |
| Muse-native | 11/12 | 11/12 | 11/12 | 11/12 |

Absorption is unchanged across all legs: none of C1/C2/C4 made the learner more gullible or more
resistant. The falsehood-absorption profile of v2 is preserved exactly.

## 7. Known defects and limitations (not hidden)

1. **Grok degenerate pubyear items (input defect, documented in prereg)**: 24/240 grok training facts
   (`The publication year is 1759.` with no title) cannot be learned by any key-based mechanism. Grok's
   ceiling is therefore 204/228 = 0.8947 on clean probes; v1 reached 189, A3 183.
2. **Dense-input internal summary defect**: the learner's own `clean N/M` summary line is invalid on dense
   inputs (denominator counts dense training IDs = 720 while test probes use 12 original fact IDs;
   produced impossible `205/204`). All mastery figures in this verdict come from the external scorer with
   the original-fact mapping (`dense_train_id // 3`), never the internal summary.
3. **NEG battery semantic overlap** (§4): rephrasing probes 18/19 achieved textual uniqueness but the
   battery still contains live asserted Beatles=4 / Jackson5=5 sentences, so probes 18/19 legitimately
   retrieve them. A future battery revision should isolate negated-only items from asserted same-entity items.
4. **Tier-3 near-tie precision** (§2.2): 22 additional wrong-value verdicts vs A1, concentrated in
   near-duplicate sentence families (wordlen). Jaccard ties (ties=3 observed) resolve arbitrarily.
5. **Wordlen curly quotes**: probes using `“word”` never match train's `"word"` — a tokenizer gap
   affecting 13 sol probes, untouched by C1/C2/C4.

## 8. Determinism and verification status

- Championship: 5/5 byte-identical reps for all 4 legs × 4 sources. ✓
- Sub-batteries: 5/5 byte-identical reps for all 4 legs × 7 batteries (reps 4–5
  completed 2026-09-22, 56/56 `cmp` clean). ✓ KB3-BYTEID **fully satisfied**.
- Implementation proof: m0 vs frozen v2 14/15 input classes byte-identical; the single
  deviation (sub_core id 17 sent=1) is the trigger-expansion deviation documented in
  §11 and src/PROOF.md. Zag vs independent oracle byte-identical on all 16 championship
  leg/sources and 26/28 sub-battery leg/batteries (the 2 misses are the same id-17
  v2-binary-vs-oracle deviation). ✓
- A0 mechanically replicates the frozen v2 championship scores (59/65/75/144, Q=−0.0570) — the ablation
  baseline is exact.

## 9. Decision record

- **KB3-VIABLE FAILS (2/4).** v3 does not ship as the prose path; **v1 stays pinned** (Micah's 2026-09-21
  decision stands).
- **What carried the recovery**: C4 KEYSOFT tier-3 (+0.30–0.56/source). C1 dense phrasing (+0.00–0.06, zero
  on grok). C2 coref repair (0 on championship, 11/24→22/24 on CORE).
- **No subset meets a revised bar without an amendment**: A3 alone is the only leg that beats v1 anywhere
  (2/4); A1/A2 beat v1 on 0/4. No post-hoc bar movement is proposed.
- **Hypothesis update**: Sol H1 (overbinding retriever) supported; Sol H3 and Grok's dense-phrasing
  prediction weakened by the grok C1 delta of exactly 0.
- The Sol-vs-Grok candidate-architecture head-to-head (factorized quorum semantic index vs canonical
  logical skeleton) is registered in PREREG3 §8 and needs its own preregistration before scored runs.

## 10. Outstanding work

1. ~~Sub-battery reps 4–5 for A0–A3 (KB3-BYTEID).~~ Done 2026-09-22: 56/56 byte-identical.
2. ~~Full championship oracle-vs-Zag byte comparison, all legs/sources; append dense proof to src/PROOF.md.~~
   Done 2026-09-22: 16/16 championship + 26/28 sub-battery oracle comparisons pass
   (2 misses = the documented id-17 v2-binary deviation); dense proof appended to src/PROOF.md.
3. Package under `docs/lab/prose-learning/v3/` (exclude binary, `.zagd`, caches); checksums/manifests.
4. Commit to `sylorlabs/TNN`, branch `tnn-native-lab` (use `~/workspace/commit_big_files.py` ≥96 KB).
5. Update `~/workspace/NIGHT_RUN_2026-09-21.md`.

## 11. Prereg deviation: coref trigger expansion (found 2026-09-22 during oracle verification)

PREREG3 §3 C2 says v3 "moves the **existing** train-only coreference block before rule 2d".
The implementation additionally **expanded the trigger set**: v2 fires coref on
`it/this/that`; v3 fires on `it/its/this/that/these/those` plus the `"the word"` /
`"the letter"` bigram (tokenizer precompute, `sctx[76]`). This was not preregistered.

Impact on the CORE 11/24 → 22/24 result (11 items fixed):

| Cause | Items | Count |
|---|---|---|
| Preregistered order change (narrow it/this/that trigger now beats 2d) | 2, 5, 9, 10, 13 | 5 |
| Unpreregistered trigger expansion ("the word"/"the letter" bigram) | 3, 7, 16, 17, 18, 23 | 6 |

The prereg's "any battery movement between A1 and A2 is attributed to this change" is therefore
**confounded**: roughly half the CORE gain came from the trigger expansion, not the order change.
The 2 residual CORE misses (ids 19, 21) are the predicted cost of keeping 2b above coref (§4).

The expanded trigger also leaks into m0: v3 m0 ≠ v2 binary on exactly one scored sentence
(sub_core id 17 sent=1; 14/15 input classes identical). **No scored result is affected** — A0/A1
ran the frozen v2 binary, never v3 m0 — but src/PROOF.md gate (a) overstated the claim and has
been corrected. The m1/m2 scored behavior is exactly as implemented and fully oracle-verified.
