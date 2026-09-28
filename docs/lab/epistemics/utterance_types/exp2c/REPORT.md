# H7 exp2c — Final Report: sincere-hypotheticals calibration experiment

Date: 2026-09-27. All runs: pure Zag, zero RNG in decision paths, 3 byte-identical
reps per cell, SHA-256 per rep. Learner mechanism frozen; only additive
experimental delivery in `h7_exp2c.zag` (never `h7_main.zag`).

## 1. Headline verdicts

| Question | Verdict |
|---|---|
| Does 2c move `sinc_lk_3` (frozen 3/10, bar ≥9/10)? | **YES — 9/10 (A+B, both designs, both orders); 10/10 (A+B+C under β; 48+48 volume under α and β)** |
| Projected 6–9/10 range? | **CONFIRMED, then exceeded** — A+B legs hit 9/10 (top of range); β+C and vol2 legs hit 10/10 |
| Price of the fix? | **Zero** on every other bar in the passing legs (TR/PA/NO, SINC-DP, all 5 types' LK, leakage, suppression, NEST, FHYP, determinism all hold) |
| Broader fix (all types' SINC)? | **YES under design β** — abc-b/vol-b: every type DP≥9, LK≥9 (type-2 LK 10/10); vol2-b: LK 10/10 on types 2,3,4 |
| Design α vs β? | **β's endorse-pool append is load-bearing for family C** — α+family-C (abc-a, vol-a) catastrophically installs promiscuous joke CTX markers; β revokes them in the final calibrate |
| Dose (volume)? | Prereg's churn prediction **confirmed**: 96-item vol2 legs add 3 specific n-gram probe collisions (DP 9→8 on types 3, 5). Prereg's ceiling prediction ("no better than L1–L4") **falsified positively**: vol2-b hits 10/10 |
| Novel families (D `what if`, E `where do`)? | Clean generalization, zero collateral damage — but the frozen SINC-LK probe set contains only A/B-family lookalikes, so `sinc_lk_3` stays 3/10 (probe-blind, not mechanism failure) |

## 2. Full bar table (post-2c `2C_CURVE`; bar = DP≥9 and LK≥9)

Types: 1 sarcasm, 2 joke, 3 hypothetical, 4 quotation, 5 metaphor.

| leg | design | corpus | t1 DP/LK | t2 DP/LK | t3 DP/LK | t4 DP/LK | t5 DP/LK | 2c check failures |
|---|---|---|---|---|---|---|---|---|
| base (control) | — | — | 9/9 | 10/10 | 9/**3** | 10/10 | 9/9 | `2c_sinc_lk_3` |
| ab-a | α | A+B 32, E→W | 9/9 | 10/10 | 9/9 | 10/10 | 9/9 | none |
| ab-b | β | A+B 32, E→W | 9/9 | 10/10 | 9/9 | 10/10 | 9/9 | none |
| ab-a-rev | α | A+B 32, W→E | 9/9 | 10/10 | 9/9 | 10/10 | 10/9 | none |
| abc-a | α | A+B+C 48, E→W | **4**/9 | **5**/**0** | **5**/**0** | **5**/**0** | **5**/**0** | 9 (dp₁,₂,₃,₄,₅; lk₂,₃,₄) |
| abc-b | β | A+B+C 48, E→W | 9/9 | 10/10 | 9/10 | 10/10 | 9/9 | none |
| vol-a* | α | 96 novel, E→W | **5**/9 | **5**/**0** | **5**/**0** | **5**/**0** | **5**/**0** | 9 (dp₁,₂,₃,₄,₅; lk₂,₃,₄) |
| vol-b* | β | 96 novel, E→W | 10/9 | 10/10 | 9/10 | 10/10 | 10/9 | none |
| vol2-a | α | 48+48, E→W | 10/9 | 10/10 | **8**/10 | 9/10 | **8**/9 | `2c_sinc_dp_3`, `2c_sinc_dp_5` |
| vol2-b | β | 48+48, E→W | 10/9 | 10/10 | **8**/10 | 9/10 | **8**/9 | `2c_sinc_dp_3`, `2c_sinc_dp_5` |
| de-a | α | D+E 32, E→W | 9/9 | 10/10 | 9/**3** | 10/10 | 10/9 | `2c_sinc_lk_3` (pre-existing) |
| de-b | β | D+E 32, E→W | 9/9 | 10/10 | 9/**3** | 10/10 | 10/9 | `2c_sinc_lk_3` (pre-existing) |

\* vol-a/vol-b used a deviant 96-all-novel composition (see §6); vol2-a/vol2-b
are the prereg-§6.2-compliant 48-original + 48-new legs.

TR/PA/NO are 20/20 on every type in every leg (type-2 NO is 16/20 everywhere,
including base — pre-existing, unchanged). Every leg's frozen (pre-2c) checks
show exactly one failure: the pre-existing `sinc_lk_3`. Leakage negative
controls (`leak_substring` 0/0, `leak_paraphrase` 0/0), suppression
(`supp_bogus` 5/5, `supp_count` 5/5), NEST (20/20) and FHYP (20/20) pass in all
12 legs. The only frozen-check delta is `nofilter_guards` 1201/1201 → 1217/1217
in 2c legs: 16 new typed W records expand `tn`; actual equals the dynamically
expected value — expected scaling, not a failure.

## 3. Mechanism: why it works, why α+family-C explodes

The 2c mechanism is purely eliminative + the frozen learner's own correction:

- **E-items (sincere "if the"/"do we" lookalikes)** predict WITHHOLD (promiscuous
  hypothetical markers fire on the bare bigram) → `learn_sincere` revokes the
  firing markers. This removes exactly the markers that were withholding on
  sincere SINC-LK probes → `sinc_lk_3` 3/10 → 9/10.
- **W-items** on correct WITHHOLD change nothing; on miss they install
  provisional markers, later pruned by the final `calibrate`.

**The abc-a/vol-a catastrophe (white-box, MDUMP-diff proven):** family-C W-items
are joke absurdities taught toward JOKE. Their misses install promiscuous JOKE
markers — `says evenly`, `evenly`, `is a`, `it is a` (CTX + generic UTT n-grams
from the absurd utterances). The family-C E-items run BEFORE the W-items, so
their eliminative revocation cannot remove them; design α's final calibrate
(original 40-item pool) doesn't match them either. They survive and fire on
every SINC probe with a sincere context → mass WITHHOLD (SINC-LK 0/10 on types
2,3,4,5; SINC-DP 4–5/10 across all types). **Design β appends the 24 E-items to
the endorse pool, so the final calibrate revokes exactly those markers**
(vol-b: all four `says evenly`/`says plainly`/`evenly`/`plainly` joke CTX markers
status 3; 2CCALIB revoked 11 vs 6 in α) → abc-b/vol-b pristine.

**The vol2 surprise (interleaving self-corrects):** vol2-a (α, 48+48) does NOT
reproduce the abc-a catastrophe — its curves are IDENTICAL to vol2-b. The
second block's sincere E-items eliminatively revoke the first block's
promiscuous W-installs (all four joke CTX markers status 3 under α too).
Interleaved E→W→E→W delivery makes α self-correcting; the pool-append only
matters for single-block delivery.

**Volume churn (prereg §6.2 confirmed):** the 96-item legs add three specific
novel n-gram collisions, each white-box identified: hypothetical `the clock`
(from new A_W "If the clock ran backward…") withholds si3_03; hypothetical
`is out` (cc26 "Imagine the causeway is out…") withholds si5_01; joke
`at night` (new C_W "…chairs gossip at night") withholds si5_09. DP 9→8 on
types 3 and 5. More W-installed markers → more probe surface, exactly as
predicted. TR/PA/NO untouched.

**Novel families (D/E):** de-a/de-b process the items (MDUMP shows revocations
+ reinstalls; 2CCALIB revoked 4) with zero collateral damage — but the frozen
sinc3.txt SINC-LK probes are 9× bare-`if`, 1× `do we`, 1× `it is`: they contain
no `what if`/`where do` lookalikes, so D/E calibration cannot move the probe.
`2c_sinc_lk_3` = 3/10 is probe-blindness, not mechanism failure.

## 4. Determinism & SHAs (rep1; all legs 3/3 byte-identical)

| leg | SHA-256 |
|---|---|
| empty (Stage-0 gate) | `71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407` (= frozen) |
| base | `9cc056bd09f20168a1074d0068a84626d810c72c66a85f326ab2383e4763be1b` |
| ab-a | `626d209f4a6a10dd6bcd768a7c68efc14409284bea7b9e4ecd48811976fa9c06` |
| ab-b | `204fbf91dcb0849d84fe043c27536375fc06d6607d34b7045f54dc1ad042020f` |
| ab-a-rev | `771d38a78f838d0cda98399068348f0a336884289543efc3cdb1c8bf43e97cd5` |
| abc-a | `8cf3b789088babe5c316dd92a780375236492ee8156b6b84110443344a48f6ba` |
| abc-b | `932145c5dff8fb8d1118414726f61474141db26b6a9df1ac30ecf2f2c57d6909` |
| vol-a | `4e212c9c3931f52fd9ad429cce1b3916bc5e6f8e8f0fbbe9029ec26a84a5da4b` |
| vol-b | `013e4ae367f6b643a3117731ee3e62f7ef1727050d4c5d93da03ccdc86c54320` |
| vol2-a | `4c68084509ea705aeeffe7aba792db110c9096bb6dfba8fab0c503f72a313471` |
| vol2-b | `a625336d4d342fa99b0e237931344faac17515b8b7806ef430e3acacb669beba` |
| de-a | `a4fc2751dc518a78f62f603da5b8fbdb9217819c059df422df2c392acfed4c82` |
| de-b | `b92d829b4bf2986c45bd1c105fa56165be30307960bdb0915d7c4a467a2b3980` |

Binary provenance: v3 (`h7_exp2c_bin_v3`) — empty mode 3× = frozen SHA
(Stage-0 gate SATISFIED); v3 ab-a and base outputs byte-identical to v2 (all
pre-v3 run data stands). Pristine frozen `h7_main.zag` rebuild independently
reproduces the frozen SHA (mechanism untouched, proven separately).

## 5. Prediction scorecard

| Prediction | Source | Outcome |
|---|---|---|
| vol-a catastrophe (DP≤5, LK≤5) | PREDICTIONS_LOCKED.md | **CONFIRMED** (DP 5/10 all types, LK 0/10 t2–5) |
| vol-b all pass, lk_3≥9 | PREDICTIONS_LOCKED.md | **CONFIRMED** (0 failures, lk_3 10/10) |
| vol-a mechanism: live joke `says evenly` | PREDICTIONS_LOCKED.md | **CONFIRMED** (status 1); vol-b status 3 |
| de-a/de-b all pass, lk_3≥9 | PREDICTIONS_LOCKED.md | **FALSIFIED on lk_3** (3/10 — probe-blind); confirmed on zero-damage |
| vol2-a catastrophe | Addendum | **FALSIFIED** — interleaving self-corrects under α (curves = vol2-b) |
| vol2-b all pass, lk_3≥9 | Addendum | **PARTIAL** — lk_3 10/10, but dp_3/dp_5 8/10 (novel n-gram churn) |
| Prereg §6.2 ceiling ("no better than L1–L4") | EXP_PREREG.md | **FALSIFIED positively** — vol2-b lk_3 = 10/10 > 9/10 |
| Prereg §6.2 churn ("more W-markers → more surface") | EXP_PREREG.md | **CONFIRMED** — 3 identified collisions |

## 6. Protocol deviations (all disclosed)

1. **Stage-1 2c runs preceded the prediction lock and source commit.** The
   prereg required predictions + commit before any 2c run. Stage-1 legs
   (ab/abc) are therefore pilot-grade for prediction purposes; their
   measurements stand as observed data. Stage-2 predictions were genuinely
   locked (and source/items committed) before any Stage-2 run.
2. **Volume-leg composition.** The first vol-a/vol-b ran 96 ALL-NEW items;
   prereg §6.2 specifies 48 original + 48 new. Corrected legs vol2-a/vol2-b
   (prereg-compliant) were built, predicted, committed, and run; the deviant
   legs are retained as supplementary "96-novel" measurements.
3. **Stage-0 gate.** The first experimental binary had no exact-base mode
   (additive lines always emitted). Fixed in v3: empty/missing mode executes
   the exact frozen path — 3× runs equal the frozen SHA byte-identically.
4. **Baseline-reproduction timing.** The pristine frozen rebuild ran before the
   prereg commit; it reproduces only public frozen evidence.
5. **Post-state vs inline curves.** The 2c scoring re-scores at post-2c state,
   not at the historical inline points; raw numbers differ slightly from frozen
   inline curves (e.g. type-1 DP/LK 9/9 post-state vs 10/10 inline) while all
   threshold bars agree. Adjudicated: the 2c bars are the preregistered
   post-state bars; the comparison baseline is the 2c-control leg, not the
   frozen inline curves.

## 7. HARD0 audit

KB-H7-HARD0 re-run on `h7_exp2c.zag`: the 5 frozen `KEYWORD_LIST_SHAPE` hits
(`fname("tr"/"pa"/"no"/"sinc",…)` file-loading, adjudicated false positives)
are inherited unchanged; the new 2c code (learn_sincere/run_2c/dispatch/scoring/
MDUMP) contains **zero** type-name strings, zero type constants in control flow
— `ti` arrives as an opaque concept index from the item files. No new hits.

## 8. Recommendation

Adopt design β (endorse-pool append) as the delivery protocol for any
sincere-calibration teaching: it is the only design that survives joke
re-keying (family C) in single-block delivery, costs nothing on any other bar,
and reaches 10/10 hypothetical SINC-LK. For multi-block curricula, interleaved
E→W→E→W ordering self-corrects even under α (vol2-a = vol2-b). Cap W-item
volume per block: each novel W-item is new probe-collision surface (≈3
collisions per 96 items here, all white-box identified, none load-bearing).
Extend the SINC-LK probe set with `what if`/`where do` lookalikes before
claiming anything about novel-family discrimination — the current probes
cannot see it.
