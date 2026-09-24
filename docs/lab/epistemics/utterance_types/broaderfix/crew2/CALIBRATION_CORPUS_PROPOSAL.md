# H7 Sincere-Discourse Calibration Corpus — Design Proposal
**Crew:** H7 broader-fix, Crew 2 (curriculum design)
**Date:** 2026-09-23
**Status:** PROPOSED — **NEEDS MICAH'S SIGNATURE** (frozen-prereg curriculum change, §3)
**Companion item file:** `calibration_corpus_items.txt` (cc01–cc48, exact text, verified)

## 1. What this fixes

The 2b impossibility proof (§7) identifies the missing bit for every `sinc_lk_3` miss:

> **Does marker m occur in sincere discourse?**

The frozen exemplars show `if the` / `do we` / `it is` only in typed (hypothetical/joke)
exemplars; the endorse pool — the only sincere sample in the frozen structure — does not
contain them (verified by case-insensitive grep over all 650 frozen utterances; see
`MISSING_BIT_CHECK.md`). `calibrate` therefore cannot revoke or adjust the provisional
content markers, and the learner withholds on lone marker fires — correctly for joke
deadpan (`learn_bar_2`), incorrectly for the 7 sincere lookalikes.

This corpus **supplies the missing bit as legitimate teaching data**: 48 FL2
deliberate-teaching episodes in which the three failing marker families occur in
sincere use with an ENDORSE signal, contrasted against genuine typed uses with a
WITHHOLD signal reusing the same surface bigrams under the opposite compositional
scope. No type keywords, no regexes, no type constants anywhere in the mechanism path —
the corpus is data, and the consumer is the learner's own generic FL2
provisional-install / eliminative-revocation machinery.

## 2. The 48 items (exact text in `calibration_corpus_items.txt`)

| Family | Failing bigram | Sincere form (ENDORSE ×8) | Typed contrast (WITHHOLD ×8) | Scope contrast |
|---|---|---|---|---|
| A | `if the` | embedded interrogatives: "Ask if the corner shop is open.", "Check if the rear entrance is bolted.", … | matrix suppositions: "Say that if the grid fails tonight, we light candles.", "Assume if the rains never come, the fields crack.", … | interrogative-governor vs supposition-governor |
| B | `do we` | matrix interrogatives: "When do we leave for the station?", "Do we have enough chairs?", … | suppose-embedded interrogatives: "Suppose the alarm rings, where do we all gather?", "Assume the coach is cancelled, how do we get home?", … | matrix vs suppose-embedded governor slot |
| C | `it is` | sincere predications: "It is raining.", "It is as if the whole town paused.", … | joke absurdities: "It is a proven fact that my goldfish pays rent.", … | complement type (sincere vs absurd predication) — **taxonomy-dependent** |

Format matches the frozen curriculum: `id|speaker|ctx|utterance|signal`
(`cc01|Mara|says evenly|Ask if the corner shop is open.|E`).

**Anti-confound controls (deliberate):**
- **Context held constant:** all 48 items use `says evenly` / `says plainly` (the sincere
  ctx pool) on BOTH polarities, so the learner cannot substitute a frame rule for the
  scope distinction. (The proof's §3 shows the critical pair already shares ctx.)
- **Speakers rotated** through the six frozen names (Mara, Dev, Priya, Theo, June, Sam)
  on both polarities — no speaker signal.
- **No type labels attached** to items (same as Phase 2b).
- **No teaching to the test:** every item verified by deterministic script against all
  650 frozen utterances (exemplars, probes, calib, facts) — zero shared ≥16-byte
  substrings; none of the 7 miss utterances appears verbatim or paraphrased within
  16 bytes. The SINC probes remain answer-key-free; the corpus is teaching content,
  never probe content.
- **Bigram presence verified** with the learner's actual tokenizer semantics
  (lowercased `[a-z0-9]+` runs): every item contains its family's target bigram.

## 3. Volume justification: why 8+8 per family (16/family, 48 total)

1. **Matches the proven stable regime.** The frozen §3 exemplar schedule is
   {2, 4, 8, 16, 32}; type profiles stabilize (not dissolve) in the 8–16 window.
   8 per polarity per family is the low end of that window — the same volume at which
   FL2's provisional-install / eliminative-revocation dynamics are already
   characterized.
2. **Symmetric polarity at installation-relevant volume.** Revocation needs the
   contradiction observed often enough to cross the eliminative threshold; 8+8 gives
   both scoped keys fresh installation (see §5: under a new scoped key space, old
   bare-bigram support does not transfer — both polarities must be installed anew).
3. **Small enough to be safe.** Calibration items are not type exemplars and do not
   count toward §3 exemplar schedules; the §5c dissolution kill (TR ≥6/10 at 16+) is
   evaluated on the type profiles, which the contrastive withhold items reinforce
   rather than dilute. The frozen hypothetical withhold side is additionally already
   represented by 32 exemplars + TR/PA/NO sets.

## 4. Supervision signal (exact)

Each corpus item is **one FL2 deliberate-teaching episode** per the frozen §3 Phase 2b
protocol (reference `training_paradigms/scaffold_release/gl_default/gl_learner.zag`):
teacher presents the utterance → learner predicts ENDORSE/WITHHOLD + type + reason →
teacher corrects with the item's listed signal (E = correct toward ENDORSE, install as
sincere; W = correct toward WITHHOLD, provisional install of the typed verdict) →
eliminative revocation on contradiction proceeds per the frozen FL2 rule. No new
episode type, no new signal vocabulary, no mechanism-code change.

## 5. Preregistered dependency (honest)

Under the **frozen bare-bigram representation**, this corpus is predicted to be
**bar-neutral at best** (grok proposal #4's analysis; 2b proof §4/§6): the missing bit
is supplied, but the frozen key space cannot hold it — sincere and matrix uses of
`if the` remain the same key, so FL2 can only revoke-or-not (the mode-3 tradeoff:
fixes `sinc_lk_3`, regresses `learn_bar_2` to 15/20). **The corpus achieves its purpose
only together with a representation in which embedded-scope and matrix-scope marker
occurrences are distinct keys** (Crew 1's scope-indexed markers — itself a proposed
amendment needing Micah's signature). Adopting the corpus without the representation
is recommended **only as an ablation** confirming the proof.

## 6. Gated delivery (family C)

Families A and B contrast on governor slots that any structural taxonomy must
distinguish (interrogative-complement governors vs supposition governors; matrix vs
embedded interrogative). Family C (`it is`) is scope-identical at the governor level
(matrix `be` in both "It is as if the whole town paused." and "It is a proven fact
that my goldfish pays rent.") — separation needs a finer taxonomy split (complement
type) that Crew 1's build may or may not provide. Teaching 8 ENDORSE + 8 WITHHOLD on
one collided key risks revocation churn on the joke `it is` key (leak-adjacent:
joke items pa2_05/ex2_02/ex2_05 carry `it is`).

**Gating rule (preregistered):** sub-phase 2c-i (families A+B, cc01–cc32) runs first,
then all §5c bars are re-scored. Sub-phase 2c-ii (family C, cc33–cc48) runs **only if**
Crew 1 demonstrates distinct scoped keys for the family-C endorse vs withhold items on
a dry run. If the keys collide, 2c-ii is replaced by the H7-A5 admissibility ruling
for si3_15 (see `AMENDMENT_TEXTS.md`) and the set is adjudicated at 9/10 with si3_15
as the single admissible miss.

## 7. Exact prereg change (frozen §3 quoted, replacement given)

**Frozen §3 text (to be amended):**

> **Phase 2b — markers learned from exemplars.**
> For each type, the teacher presents exemplar episodes (utterance, no type label attached to generalization probes): the learner predicts ENDORSE/
> WITHHOLD + type + reason; the teacher corrects via FL2 (provisional install
> of the type verdict, eliminative revocation on contradiction). Exemplar
> schedule per type: {2, 4, 8, 16, 32} exemplars; the per-type learning curve is
> scored at every step on three frozen probe sets (below). Phase 2b is complete
> for a type when its §6 learning bar is met; all five types must meet it.
>
> **Phase 3 — interference + generalization batteries (§7) + red-team
> batteries (§8).** After Phase 2b: (i) Phase-1 facts re-probed — 20/20 must
> hold (no forgetting, no suppression by type machinery); (ii) generalization
> batteries per type; (iii) the two red-team batteries.

**Amendment — insert between Phase 2b and Phase 3 (NEEDS MICAH'S SIGNATURE):**

> **Phase 2c — sincere-discourse calibration (AMENDED 2026-09-23, Micah's signature required).**
> After Phase 2b completes for all five types and before Phase 3, the teacher delivers
> 48 FL2 deliberate-teaching episodes (the sincere-discourse calibration corpus,
> `calibration_corpus_items.txt`, cc01–cc48): for each of three marker families —
> (A) `if`-constructions, (B) `do`-interrogatives, (C) `it is`-frames — 8 sincere
> ENDORSE episodes and 8 genuine WITHHOLD contrast episodes reusing the same surface
> bigrams under the opposite compositional scope. Episode protocol is identical to
> Phase 2b (learner predicts ENDORSE/WITHHOLD + type + reason; teacher corrects with
> the listed signal; provisional install and eliminative revocation proceed per the
> frozen FL2 rule; no type labels attached). Delivery is gated: sub-phase 2c-i
> (families A+B, cc01–cc32) runs first and all §5c bars are re-scored; sub-phase
> 2c-ii (family C, cc33–cc48) runs only if the learner's representation demonstrates
> distinct keys for the family-C endorse vs withhold items on a dry run, else the
> H7-A5 admissibility ruling applies to si3_15. The corpus is teaching content, not
> probes: the §4 answer-key-free rule is unchanged, corpus items are excluded from all
> Phase 3 probe sets, and no corpus item shares a ≥16-byte substring with any frozen
> probe or exemplar utterance. Calibration items are not type exemplars and do not
> count toward the §3 exemplar schedules; the §5c dissolution kill is evaluated on the
> type profiles. Bars in §5c are adjudicated on post-calibration scores. Preregistered
> prediction: under the frozen bare-bigram representation this corpus is bar-neutral
> at best (ablation only); it supplies the missing sincere-compatibility bit only in
> combination with a representation in which embedded-scope and matrix-scope marker
> occurrences are distinct keys.

**Sections affected:** §3 only (curriculum). §4 unchanged (answer-key-free preserved).
§5c unchanged in thresholds; adjudication point moves to post-calibration. §5d
(HARD0) unchanged — the corpus is data; no mechanism-code addition.

## 8. Score projection (preregistered, not a promise)

- Families A+B fix 6 of the 7 misses (si3_12, si3_13, si3_14, si3_16, si3_18, si3_20)
  via scope separation → **9/10** with si3_15 as the single miss.
- 10/10 iff family-C gating passes (distinct scoped keys) or H7-A2's Head B supplies
  a generic content cue for si3_15.
- **Live risks (not hidden):** joke NO sits exactly at 16/20 — re-keying under Crew 1
  must not lose a single currently-withheld item; hypothetical TR/PA/NO must not churn
  under revocation. The 2c-i bar re-score is the tripwire.
