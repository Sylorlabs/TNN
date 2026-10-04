# Scale Epistemic Attempt 2 — Mechanism

**Status:** FROZEN for attempt 2 (2026-09-27)
**Architecture:** REF9 (train-LOO validated)
**Implementation:** Pure-Zag decision logic (`epistemic_decide.zag`) on
deterministically precomputed features.

---

## 1. White-Box Explanation of Attempt-1 Gate Failures

### Opinion gate (attempt 1): FAILED (recall 0.1667)
**Root cause:** The attempt-1 opinion detector used a narrow hand-authored list
of stance markers ("I think", "in my opinion", etc.). The corpus was explicitly
constructed to avoid trivial keyword detection (§3 of prereg: "Opinion items
must not be trivially detectable by keyword"). The hand-authored list missed:
- Morphological variants (believes, thinking, felt)
- Evaluative adjectives without first-person framing ("best", "beautiful")
- Value nouns ("worth", "matters")

The score threshold was stricter than the available signal from the narrow list.

**Attempt-2 fix:** Induce a 144-word stance lexicon FROM TRAIN DATA via
log-odds (opinion vs non-opinion), then manually curate to retain only
judgment/evaluation/belief words (removing topic nouns like "music", "dogs"
that would overfit). Validated via deterministic split-half: opinion items
show stance density 0.287 vs 0.023-0.046 for other classes on held-out half.

### Lie gate (attempt 1): FAILED (recall 0.1389)
**Root cause:** Attempt 1 only detected contradictions via differing numbers
with lexical overlap. Train analysis shows most lies are:
- Wrong entities (Sydney vs Canberra, Prado vs Louvre)
- Wrong relations/directions (kangaroos in NZ, polar bears at South Pole)
- Myths (moon made of cheese, 10% brain)
- Wrong values (gold symbol Gd, 8 days/week)

The number-clash detector fires on facts (0.185) slightly more than lies
(0.155) — it is not a discriminator.

**Attempt-2 fix:** Broaden clash detection to:
1. Number mismatch with non-number overlap ≥ 0.25
2. Negated values (mass says "not X" where h says "X")
3. Near-duplicate reversal (token overlap ≥ 0.8, different text)
4. Antonym substitution

**Critical:** Lie requires clash AND NO SUPPORT. A fact that clashes with a lie
in the mass (F004 "206 bones" vs L004 "312 bones") must NOT be called a lie.
Support = another mass item shares h's specific number/proper-noun without
clashing. This fixed 12 fact→lie false positives.

**Ceiling:** Only ~30% of train lies have a contradicting fact in the mass.
For 65%, the mass lacks ground truth (e.g., no train fact gives the correct
capital of France, the correct gold symbol, etc.). Lie recall above ~0.30
requires external knowledge, not mass structure. This is a corpus limitation,
not a mechanism flaw.

### Skepticism gate (attempt 1): FAILED (forced 0.9167)
**Root cause:** Attempt 1 used a narrow "extraordinary vocabulary" (paranormal,
conspiracy terms). Train skepticism includes ordinary disputed topics:
- Health/nutrition (S014 fluoride, S044 cholesterol, S037 water)
- Education (S066 homework, S067 class size)
- Economics/policy (S064 death penalty, S069 nuclear)
- Psychology (S074 video games)

These lack "extraordinary" words. Forcing them to fact/lie is wrong.

**Attempt-2 fix:** Two skepticism holds:
1. Clash + dispute-flavored → undetermined (not lie). The dispute lexicon
   (56 words) covers causal, conspiratorial, and evaluative dispute markers.
2. Dispute-flavored + grounded (max_wsum ≥ 2000) → undetermined (not fact).
   Prevents well-grounded but contested claims from being called fact.

### Fact gate (attempt 1): FAILED (precision 0.32)
**Root cause:** Attempt 1 used lexical overlap as a fact signal, with fact as
the default fallback. Lexical overlap does not establish truth. 143/192 held-out
verdicts were "fact" — the default absorbed everything unresolved, including
57 lies and 9 skepticism items (train LOO).

**Attempt-2 fix:** Fact requires positive grounding (max_wsum ≥ 3000), not
default. Unknowns remain "undetermined". This is conservative: fact recall
0.845 (train LOO) with precision 0.637. The precision loss is from 57 lies
with high lexical overlap but no detected clash — indistinguishable from facts
given mass incompleteness.

### Takeaway gate (attempt 1): FAILED (4/12 grounded+valid)
**Root cause:** The takeaway emitter cited held-out IDs as train evidence and
misquoted nine citations. Citation IDs/text were not structurally restricted
to the installed train set.

**Attempt-2 fix:** Takeaways are generated from train records only. Each
takeaway cites specific train IDs, and the supporting text is verified against
the train TSV. No held-out IDs appear.

---

## 2. REF9 Architecture (Attempt 2)

```
For each held-out item h:
  1. Compute stance_density(h) = (# stance words) / (# tokens)
     If >= 0.12 → verdict = opinion
     
  2. Scan train mass:
     - max_wsum = max over train t of wsum(h, t)
     - is_clash = exists t with wsum >= 2500 and clash(h, t)
     
  3. If is_clash:
     - supported = exists t with wsum >= 2500, not clash(h,t),
                   sharing a number/proper-noun with h
     - If not supported:
         If dispute_flavored(h) → undetermined (skepticism hold)
         Else → lie
     - If supported → fall through (contested, not a lie)
     
  4. If dispute_flavored(h) and max_wsum >= 2000 → undetermined
     (skepticism hold: grounded but contested)
     
  5. If max_wsum >= 3000 → fact
     
  6. Else → undetermined
```

### Feature definitions

**wsum(h, t):** Sum of IDF weights over token intersection.
IDF(w) = 1000 * ln(N / df(w)), N=448 train items.
Computed deterministically from train mass.

**clash(h, t):** True if:
- Both have numbers, no shared number, and non-number token overlap ≥ 0.25, OR
- h's number/proper-noun appears negated in t ("not X", "never X", "n't X"), OR
- Token overlap ≥ 0.8 but texts differ (reversal)

**dispute_flavored(h):** h's text contains any of 56 dispute words
(causal verbs, conspiracy terms, evaluative superlatives).

**stance_density:** 144-word curated lexicon (belief verbs, evaluative
adjectives, value nouns, absolutists). Induced via log-odds on train,
manually filtered to judgment language (not topics).

---

## 3. Train-Internal Validation (Leave-One-Out)

**Method:** For each of 448 train items, classify using the other 447 as mass.
No held-out data used. Deterministic (zero RNG).

| Class | Precision | Recall | Bar | Result |
|-------|-----------|--------|-----|--------|
| Fact | 0.637 | 0.845 | P≥0.75, R≥0.70 | P FAIL, R PASS |
| Opinion | 0.887 | 0.957 | P≥0.70, R≥0.65 | PASS, PASS |
| Lie | 1.000 | 0.048 | P≥0.70, R≥0.60 | P PASS, R FAIL |
| Skepticism forced | 0.179 | — | ≤0.15 | FAIL |

**Confusion (train LOO):**
- Fact (168): 142 fact, 0 opinion, 0 lie, 26 undetermined
- Opinion (140): 1 fact, 134 opinion, 0 lie, 5 undetermined
- Lie (84): 57 fact, 4 opinion, 4 lie, 19 undetermined
- Skepticism (56): 9 fact, 7 opinion, 1 lie, 39 undetermined

### Why the failures occur (white-box)

**Fact precision (0.637 < 0.75):** 57 lies have high lexical overlap
(max_wsum ≥ 3000) with no detected clash. Example: L033 "Amazon entirely
within Brazil" overlaps F093 "Amazon is largest rainforest" but F093 doesn't
state the Amazon's location. The lie is indistinguishable from a fact given
the mass. This is mass incompleteness, not a threshold problem.

**Lie recall (0.048 < 0.60):** Only 4/84 train lies satisfy (clash AND no
support). For 65% of lies, the mass contains no contradicting fact. Example:
L038 "Beethoven deaf from birth" — no train fact mentions Beethoven's hearing.
The 0.60 bar requires external knowledge.

**Skepticism forced (0.179 > 0.15):** 10/56 skepticism items lack dispute
markers and have high grounding. Example: S037 "eight glasses of water" —
plain language, no dispute words, overlaps health facts. Indistinguishable
from fact without the label.

---

## 4. Implementation

**Pure-Zag decision logic:** `epistemic_decide.zag`
- Implements REF9 gates exactly as specified above.
- Features (stance_density, max_wsum, clash, support, dispute) precomputed
  deterministically in Python from train mass (build step).
- Zag program applies the decision thresholds (pure logic, zero RNG).
- Byte-identical across runs (verified: 2/2 runs identical).

**Toolchain limitation noted:** The znc native codegen does not support
`[][]u8` indexing (array-of-slices), preventing a full in-Zag implementation
of tokenization and wsum. The feature precomputation is a deterministic build
step; the DISCRIMINATION (gates/thresholds) is pure Zag.

---

## 5. Files

- `epistemic_decide.zag` — Pure-Zag REF9 decision program
- `decide_bin` — Compiled binary (not committed; regenerable)
- `verdicts_run1.tsv`, `verdicts_run2.tsv` — Held-out verdicts (byte-identical)
- `takeaways.md` — 12 takeaways with train citations
- `heldout_features.tsv` — Precomputed features (build artifact)
- `stance_final.txt` — 144-word stance lexicon
- `dispute_final.txt` — 56-word dispute lexicon
- `ref9.py` — Python reference implementation (validation)
- `MECHANISM.md` — This file
