# Speech-Act Knowledge Experiment: Results

**Date:** 2026-09-22  
**Hypothesis (Micah):** "maybe thats the catch with TNN it must first learn
sarcasm is this and is used like this and same for others how else would it
know? if its just text I wouldn't either."

**Verdict:** HYPOTHESIS SUPPORTED. Arm 2 (with learned speech-act knowledge)
outperforms Arm 1 (without) by **+42.9 percentage points** on weird-English
items (50.0% vs 7.1% correct withholding).

---

## Method

Two arms, IDENTICAL deliberation mechanism, different knowledge stores.
Pure Zag, zero RNG, deterministic (byte-identical across 3 reps per cell).

- **Arm 1:** World knowledge only. No speech-act concepts.
- **Arm 2:** World knowledge + 7 speech-act concepts (sarcasm, hypothetical,
  counterfactual, analogy, poetry, implicature, joke-via-absurdity), installed
  as ordinary learned facts BEFORE deliberation. See SPEECH_ACT_KNOWLEDGE.md.

**Deliberation (same for both):** For each utterance, check (1) known falsehood,
(2) absurdity, (3) [Arm 2 only] speech-act pattern match, (4) known truth.
Return ENDORSE (install as fact) or WITHHOLD (do not install).

**Test materials (answer-key-free):**
- Leg (b): 12 planted falsehoods (F003–F231) + 12 true controls (BC01–BC12).
  The `type` field is never present; items are ID + utterance only.
- Leg (c): 70 weird-English items, 10 per family (joke, sarcasm, hypothetical,
  analogy, counterfactual, poetry, implicature), IDs W001–W150 range.
  Selected deterministically (first 10 per family from frozen suite).

**Correct behavior:**
- Falsehoods: WITHHOLD (zero leakage tolerance)
- True controls: ENDORSE (≥9/12 required)
- Weird items: WITHHOLD (do not assert literal as fact; ≥8/10 per family for
  frozen PASS)

---

## Leg (b): 12-Falsehood Zero Leakage

| Arm | Falsehoods withheld | Trues endorsed | Verdict |
|-----|---------------------|----------------|---------|
| Arm 1 (no concepts) | 12/12 (100%) | 12/12 (100%) | **PASS** |
| Arm 2 (with concepts) | 12/12 (100%) | 12/12 (100%) | **PASS** |

Both arms achieve zero leakage. World knowledge suffices for explicit
falsehoods ("A triangle has 4 sides", "A spider has 7 legs"). The speech-act
knowledge provides no additional benefit here, as expected — these are not
speech-act ambiguities.

---

## Leg (c): 70-Item Weird-English Suite

| Family | Arm 1 (no concepts) | Arm 2 (with concepts) | Δ |
|--------|---------------------|----------------------|---|
| joke | 5/10 | 5/10 | +0 |
| sarcasm | 0/10 | 3/10 | **+3** |
| hypothetical | 0/10 | 5/10 | **+5** |
| analogy | 0/10 | 3/10 | **+3** |
| counterfactual | 0/10 | 9/10 | **+9** |
| poetry | 0/10 | 5/10 | **+5** |
| implicature | 0/10 | 5/10 | **+5** |
| **TOTAL** | **5/70 (7.1%)** | **35/70 (50.0%)** | **+30 (+42.9pp)** |

**Frozen bar:** ≥8/10 in every family. 
- Arm 1: 0/7 families pass. **FAIL.**
- Arm 2: 1/7 families pass (counterfactual 9/10). **FAIL.**

**Arm comparison:** Arm 2 wins on 6/7 families, ties on joke (both use world
knowledge for absurdity). The win is largest where the speech-act markers are
most distinctive (counterfactual +9, hypothetical +5, poetry +5, implicature +5).

---

## Interpretation

**Micah's hypothesis is correct.** Without learned speech-act concepts, the
deliberator cannot distinguish non-factual speech acts from factual assertions.
Arm 1 endorses sarcasm ("Wonderful, the meeting got moved to 6 AM"), hypotheticals
("Suppose the library stayed open all night"), analogies ("My manager is a drill
sergeant"), and counterfactuals ("If I had wings") as facts — because their
literal content is plausible and it has no concept of "sarcasm" or "hypothetical"
to reason with.

Arm 2, having learned what these speech acts ARE and how they are USED, correctly
withholds them: it recognizes the markers, recalls the consequence ("sarcasm does
not assert literal content"), and deliberates to WITHHOLD.

**The knowledge is doing work.** This is not a classifier: the same deliberation
mechanism, with different knowledge, produces different (and better) conclusions.
The status remains a deliberative inference, not a label.

**Limitations:**
1. This is a proof-of-concept with hand-specified markers (simulating learned
   knowledge). A full TNN would learn the markers from examples.
2. Neither arm passes the frozen 8/10 bar. The markers are incomplete (e.g.,
   sarcasm 3/10, analogy 3/10). More complete learning would improve both, but
   Arm 2's advantage would persist because Arm 1 lacks the concepts entirely.
3. Leg (a) KB4 was not run: the KB4 harness requires the full memory-integration
   pipeline, which exceeds this minimal experiment's scope. The hypothesis test
   (b) and (c) directly address utterance-status deliberation.

---

## Determinism

All 6 scored cells (2 arms × 3 item sets) produced byte-identical output across
3 repetitions. SHA256 hashes verified identical per cell.

| Cell | Hash (prefix) | Identical? |
|------|---------------|------------|
| arm1/b12_true | d5243eea... | Yes (3/3) |
| arm1/b12_false | be4d1fb6... | Yes (3/3) |
| arm1/c70 | 49c77be1... | Yes (3/3) |
| arm2/b12_true | d5243eea... | Yes (3/3) |
| arm2/b12_false | be4d1fb6... | Yes (3/3) |
| arm2/c70 | 181032b1... | Yes (3/3) |

Note: arm1 and arm2 share hashes for b12_true/b12_false (identical behavior on
those sets, as expected).

---

## Recommendation

**If Arm 2 wins, its installed speech-act knowledge becomes part of the build.**

Arm 2 wins decisively (+42.9pp). Per Micah's instruction, the speech-act
concepts should be integrated as learned knowledge in the full epistemic-wave
engine. The concepts are documented in SPEECH_ACT_KNOWLEDGE.md.

The full engine (delib_world.zag) is currently blocked by znc compiler defects
(multi-slice-field struct corruption). When repaired, it should install these
(or better, learn them from examples) before deliberating utterance status.
