# WHY SARCASM? — Wave Report (RDTDT: Review → Debate → Test → Debate → Test)

**Date:** 2026-09-22
**Question (Micah):** "why does TNN struggle with sarcasm more?"
**Prereg:** PREREG_SARCASM.md (kill bars frozen before testing)
**Engine:** delib_sarc.zag → delib_sarc_bin (pure Zag, zero RNG)
**Evidence:** scored_evidence/sarc_*_rep{1,2,3}.txt + .sha256 (16 cells × 3 reps,
all byte-identical). `base` mode reproduces the PoC's arm-2 verdicts on c70.txt
exactly (diff of 70 verdicts: empty).

---

## 1. Test results

Correct = sarcastic → WITHHOLD, genuine → ENDORSE, attitude sarcastic → NEG.

| # | Cell | Score | Detail |
|---|---|---|---|
| 2 | base × s_bare | 3/10 | S001–S003 withheld (reason S); rest endorsed |
| 3 | notruth × s_bare | 3/10 | item-for-item identical to base |
| 4 | base × s_litfalse | 10/10 | ALL reason **F** — truth machinery decided every one |
| 5 | layered × s_bare | 3/10 | identical verdicts to base (reasons S→L) |
| 6 | layered × s_genuine | 5/10 | same 5 false positives as base |
| 7 | base × s_genuine | 5/10 | G001,G002,G003,G009,G010 false-withheld (reason S) |
| 8 | marked × s_marked | **10/10** | all reason M |
| 9 | base × s_marked | 0/10 | explicit-marker items invisible without the markers |
| 10 | marked × s_genuine | 5/10 | same 5 false positives — markers don't fix discrimination |
| 11 | speaker × s_spk | **10/10** | 5 K-withholds (ALIX) + 5 endorses (BRAM) |
| 12 | base × s_spk_utt | 5/10 | 3 false withholds + 2 missed sarcasms |
| 13 | ctx × s_ctx | **10/10** | all reason X, attitude NEG |
| 14 | base × s_ctx_utt | 3/10 | same utterances without context |
| 15 | inv × s_marked | 10/10 verdict, 10/10 NEG | attitude recovery works when detection works |
| 16 | inv × s_genuine | 5/10 verdict, 3/10 POS | attitude wrong wherever detection is wrong |

Volume data (VOLUME_CURVE.md, incorporated): sarcasm peaks at 2 examples
(6/10), then the learned profile DISSOLVES — 0/10 by 16 examples. It
saturates LOWER, not slower. Counterfactual stays at ceiling once reached;
hypothetical saturates at 1 example.

---

## 2. Kill-bar adjudication (first debate → verdicts)

| Hypothesis | Kill bar | Result | Verdict |
|---|---|---|---|
| H1 layering | layered beats base by ≥3 on s_bare | 3/10 vs 3/10, Δ=0 | **KILLED** |
| H2 truth-machinery conflict ("blocks") | notruth changes s_bare by ≥2 | Δ=0, identical | "blocks" **KILLED** |
| H2 mechanism ("wrong-reason work") | ≥50% of s_litfalse withholds reason F | 10/10 reason F | **CONFIRMED** (refined) |
| H3 missing cues (markers) | marked ≥8/10 on s_marked | 10/10 (base: 0/10) | **SURVIVES** |
| H3 missing cues (context) | ctx improves ≥3 over base | 10/10 vs 3/10, Δ=7 | **SURVIVES** |
| H4 no speaker model | speaker beats base by ≥3 | 10/10 vs 5/10, Δ=5 | **SURVIVES** |
| H5 inversion opacity | some marker set ≥8/10 on BOTH sarcastic and genuine | best: 10/10 + 5/10 (never both) | **SURVIVES** |

---

## 3. Second debate (RDTDT: the results talk back)

**H1 is dead and stays dead.** Explicit three-layer deliberation changed
reason codes (S→L) and nothing else. The layers were never interfering; the
single-status architecture was never the problem. Anyone proposing
"multi-reading deliberation" as the sarcasm fix is answered by cells 2 vs 5.

**H2 is refined, not just killed.** The "fires first and blocks" version is
dead (notruth changes nothing). But cell 4 is a real finding with teeth: when
a sarcastic utterance ALSO has a false literal, the truth machinery withholds
it 10/10 for the WRONG reason (F, never S). Two consequences: (a) sarcasm
benchmarks built on false-literal items OVERESTIMATE sarcasm understanding —
the system looks like it "gets" sarcasm while never engaging it; (b) the
12/12 falsehood strength does not transfer — it is a different skill that
masks the missing one.

**H3 vs H5 — not the same problem, and the split matters.** H3 won the
detection battle: give sarcasm dedicated lexical frames ("yeah right", "as
if") and it goes 0/10 → 10/10, exactly like hypothetical's "what if" and
counterfactual's "if I had". Give it situational context and it goes
3/10 → 10/10. But H5 won the DISCRIMINATION battle: the most common
real-world sarcasm form — positive words about a bad situation, no "yeah
right" — shares its surface EXACTLY with genuine speech ("Fantastic, the
delayed flight gave us three extra hours together" is genuine; "Fantastic,
my flight is delayed three hours" is sarcastic). No marker set in any mode
separated them above 5/10. This is also what the volume collapse IS:
sarcastic and genuine utterances share features, so more examples dilute
distinctiveness until the profile dissolves (r16: 0/10). Counterfactuals
have dedicated frames and never dissolve. H3 = "the cues are weak"
(fixable with better cues). H5 = "the utterance's surface is inherently
ambiguous" (not fixable from the utterance at all).

**H4 and H5 are complements, not competitors.** H5 says the disambiguating
information is not in the utterance's surface. H4 says where it actually
lives: the speaker. Cell 11 is the only cell in the wave that cracked the
sarcastic/genuine ambiguity (10/10) — by gating the sarcasm inference on a
speaker-attitude model. "Wonderful, my flight is delayed" is sarcastic from
ALIX (who hates delays) and genuine from BRAM (who finds silver linings);
the utterance alone cannot decide, and no amount of utterance examples will
change that.

---

## 4. Ranking (by survival)

1. **H3 — missing cues (SURVIVES, strongest).** Sarcasm has no dedicated
   lexical frame; its markers are weak and pragmatic. Dedicated markers:
   0/10 → 10/10. Situational context: 3/10 → 10/10. This is also why
   hypothetical (formulaic frames) saturates at 1 example and counterfactual
   never dissolves.
2. **H4 — no speaker model (SURVIVES).** The only fix for the genuine-vs-
   sarcastic ambiguity: 5/10 → 10/10. The missing information is the
   speaker's attitude — theory of mind as learned knowledge.
3. **H5 — inversion opacity (SURVIVES, refined).** The meaning is not-X, and
   no surface-feature set separates sarcastic from genuine utterances
   (5/10 ceiling in every mode). Predicts and explains the volume collapse.
4. **H2 — truth-machinery conflict (REFINED).** Not blocking — but the
   machinery does sarcasm's work for the wrong reason whenever the literal
   is false, masking the gap and inflating benchmarks.
5. **H1 — layering (KILLED).** Δ=0. Not the architecture.

---

## 5. The concrete answer

**Why is sarcasm harder than the other speech acts?** Three compounding
reasons, in order:

1. **No dedicated frame.** Hypothetical has "what if"/"suppose",
   counterfactual has "if I had"/"would have" — dedicated lexical machinery
   that survives any amount of data. Sarcasm's markers ("great" + bad news)
   are ordinary words doing double duty. Weak cues, pragmatically carried.
2. **Inherent surface ambiguity.** The common sarcasm form is
   feature-identical to genuine speech. No utterance-level learner can
   separate them — more examples make it WORSE (the profile dissolves),
   which is why sarcasm saturates lower (6/10) and then collapses while
   counterfactual holds its ceiling.
3. **The answer is in the speaker, not the sentence.** Resolving the
   ambiguity requires the speaker's attitude — which TNN doesn't model.
   The falsehood machinery covers up the gap by withholding false-literal
   sarcasm for the wrong reason.

**What would fix it:** NOT more utterance examples (proven to hurt past
~2), NOT architectural layering (proven Δ=0). What works: (a) speaker
modeling — attitudes as learned knowledge that gate speech-act inference
(the only 10/10 on the ambiguity set); (b) situational context as
deliberation input (3/10 → 10/10); (c) benchmark hygiene — stop counting
false-literal sarcasm items as sarcasm understanding (cell 4). In Micah's
terms: TNN can't understand sarcasm until it has learned more of the
SPEAKER — not more of the sentence.

---

## 6. Method notes

- One engine bug found and fixed mid-wave: speaker_mismatch split the
  speaker blob on ';' while speakers.txt used '|' (speakers never matched;
  cell rerun 10/10 after fix). All evidence below is post-fix.
- `base` mode reproduces PoC arm-2 on c70.txt exactly (70/70 verdicts).
- All 16 cells × 3 reps byte-identical (SHA256 per rep in scored_evidence).
- Answer-key-free: context/speaker fields are deliberation INPUTS, never
  labels — same bootstrap logic as the parent experiment.
- Honest limit: the "speaker model" here is 2 speakers × dislike lists,
  learned-state simulated. A real implementation learns speaker attitudes
  from interaction history. The structural point — gate speech-act
  inference on speaker knowledge — is what was tested.
