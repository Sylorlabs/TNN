# H7 Crew 2 Final Report — PRIMARY ARM KILL (sinc_lk_3 unfixable)

**Status:** KILL — Primary arm fails frozen bar `sinc_lk_3` (hypothetical SINC lookalikes: 3/10 vs required ≥9/10). All other frozen bars pass. The failure is a fundamental limitation of the n-gram marker mechanism, not a surface bug. Repaired at the mechanism level as far as possible; the remaining gap is unfixable without violating HARD0 or the frozen curriculum.

**Date:** 2026-09-24  
**Source:** `utterance_types/crew2/learner/h7_main.zag` (pure Zag, znc `abed8aa1`)  
**Determinism:** 3× byte-identical runs, SHA256 `71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`

## Verdict Summary

| Check | Result |
|---|---|
| H7_FAILURES | 1 (`sinc_lk_3`) |
| All NEST/FHYP/leakage/suppression/recall/learning bars | PASS |
| SINC-DP (all 5 types) | PASS (9-10/10) |
| SINC-LK (sarcasm, joke, quotation, roleplay) | PASS (9-10/10) |
| SINC-LK (hypothetical) | **FAIL (3/10, need ≥9/10)** |
| HARD0 | PASS (5 scanner hits, all false positives — curriculum filename prefixes, not decision logic) |
| Zero RNG in decision paths | PASS |
| METAQ/RETRACT | NOT BUILT (gated on primary pass) |
| h7_main_stack.zag (H-A) | NOT BUILT (gated on primary pass) |

## Learning Curves (32 exemplars, TR/PA/NO out of 20; SINC out of 10)

| Type | TR | PA | NO | SINC-DP | SINC-LK |
|---|---|---|---|---|---|
| 1 sarcasm | 20 | 20 | 20 | 9 | 10 |
| 2 joke | 20 | 20 | 20 | 10 | 10 |
| 3 hypothetical | 20 | 20 | 20 | 9 | **3** |
| 4 quotation | 20 | 20 | 20 | 10 | 10 |
| 5 roleplay | 20 | 20 | 20 | 10 | 9 |

Learning is visible: at 2 exemplars TR/PA/NO are 15-18/20; by 8-16 exemplars they reach 20/20 and hold. SINC-DP is stable ≥9/10 across all exemplar counts. SINC-LK for hypothetical degrades from 8/10 (2 ex) to 3/10 (4+ ex) — more data makes it worse (the 'if' markers strengthen).

## Root Cause: The 'if' Ambiguity (mechanism-level, unfixable)

The hypothetical type is defined by suppositional constructions ("What if...", "Imagine if...", "Suppose that..."). The learner installs 2-gram markers like 'if the', 'if we', 'do we' from exemplars. The SINC lookalikes are sincere "if" statements ("Ask if the shop is open", "See if the door is locked", "Call me if you need help") that share these 2-grams.

The n-gram marker mechanism cannot distinguish:
- "What if the harvest fails?" (hypothetical supposition about non-actual state)
- "Ask if the shop is open." (sincere question about actual state)

Both contain 'if the'. The 3-grams differ ('what if the' vs 'ask if the'), but the 2-gram fires and triggers WITHHOLD.

**Why it's unfixable:**
1. The endorse pool (frozen: 20 facts + 20 calib) contains only one "if" statement (c06 "If you need anything, just ask" with 'if you', not 'if the'). The problematic 'if the'/'if we' markers never face contradiction during training, so FL2 eliminative revocation cannot remove them.
2. Making markers more specific (UTT 3-4 grams) destroys recall on probes (learn_bar_2 fails).
3. Requiring frame evidence (CTX markers) fails because CTX n-grams don't generalize across phrasings ("thinking aloud" vs "musing quietly"), and generic CTX 1-grams ('with', 'says') are revoked by calibrate.
4. Minimum-evidence thresholds (≥2 markers, weighted scores) either don't fix SINC or break probe recall.
5. The distinction requires pragmatic/semantic understanding (supposition vs question) that n-gram overlap cannot capture. Any fix targeting 'if' specifically would be a type-content hardcode, violating HARD0.

The curriculum's hypothetical lookalikes are adversarial by design ("learned-marker lookalikes"). For 4/5 types the learner handles them; for hypothetical, the 'if' construction is genuinely ambiguous at the n-gram level.

## Mechanism Fixes Applied (all generic, HARD0-clean)

1. **Case-normalization bug in calibrate()** — The endorse pool stored raw (capitalized) bytes, but markers are lowercase. `has_sub("Mara", "mara")` was false, so the precision gate never revoked speaker-name markers. Fixed by storing lowered bytes in the endorse pool. This repaired 10 failures (SINC collapses, phase3_fact_predict).
2. **field_at bounds warning** — Rewrote loop to avoid `i <= line.len` indexing.
3. **Curve-array stride** — Fixed 12-byte cell layout to match the bar reader.
4. **Explicit zfill initialization** — For cv, sdp, slk, steps, scores arrays.

## Learned vs Scaffolded (honest statement)

**Learned from data:** All 5 utterance-type concepts (marker sets) are learned from exemplars via the FL2 loop (install on miss, reinforce on correct, revoke on wrong-type or endorse-match). No type keywords, regexes, or type-name strings in decision paths. The `predict()` function scores concepts by firing markers; the winner is selected by integer `know_idx`, never by string matching.

**Scaffolded (not learned):** 
- The 5 type concepts are TAUGHT (Phase 2a `know_teach`) with human-written consequence text — the learner does not discover the types.
- N-gram sizes (UTT 2-3, CTX 1-3, SPK 1-2), support thresholds (commit at ≥2), and the endorse pool composition are designer choices.
- The field structure (utterance/context/speaker) is given, not learned.
- The FL2 control flow (calibrate after each batch, wrong-type revocation) is scaffolded.

The learner genuinely learns the marker→type associations from exemplars, but it does not learn the types themselves, the field semantics, or the learning hyperparameters.

## Generalization

- **Paraphrase (PA):** 20/20 across all types at 32 exemplars — markers generalize to reworded probes.
- **Novel (NO):** 20/20 — markers generalize to new utterances with the type's constructions.
- **NEST/FHYP:** Pass — quotation nesting and hypothetical framing are handled.
- **Leakage:** PASS — typed utterances do not leak into the factual store (NEGCTL live).
- **Suppression:** PASS — bogus type claims on true facts are rejected.

## What Was Not Built (gated on primary pass)

- **METAQ:** Installed/committed/revoked counts per concept, single-concept-tag invariant, roleplay-tag isolation. Not implemented because the primary arm did not pass.
- **RETRACT:** Conflicting sincere evidence causing self-revocation. Not implemented.
- **h7_main_stack.zag (H-A):** Shared store with modal/type stack. Not built.
- **Commit:** No GitHub commit made. Source, curriculum, evidence, and this report are staged in `utterance_types/crew2/` ready for commit, but the KILL status should be recorded.

## Recommendation

The n-gram marker mechanism is insufficient for the hypothetical 'if' ambiguity. Options:
1. **Accept KILL** for H7 Crew 2 as specified (pure n-gram markers cannot pass sinc_lk_3).
2. **Amend the prereg** to allow a pragmatic-frame mechanism (but this would be a significant design change, not a parameter tweak).
3. **Redesign the curriculum** to avoid 'if'-ambiguous lookalikes for hypothetical (but the curriculum is frozen).

I recommend option 1 (honest KILL). The work demonstrates that 4/5 utterance types are learnable with n-gram markers, and identifies a precise, mechanism-level limitation for the fifth.
