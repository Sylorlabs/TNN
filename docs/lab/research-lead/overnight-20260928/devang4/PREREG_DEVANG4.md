# PREREG DEVANG4: Fix NEG Regression

## Mission
Fix the NEG novel regression in DEVANG3 (0/3 vs 1/3 in DEVANG2, vs 17/20 baseline).
Target: >= 17/20 test accuracy (BUILD-PASS).

## Diagnosis (from instrumented DEVANG3 run, /tmp/diag_devang3_bin)

### Observed facts
1. NEG novel test utterance "taknotgrn" segments as 5 segments:
   ["tak"(li=19), "not"(li=28), "g"(li=31), "r"(li=3), "n"(li=25)].
   "grn" never formed as a lexicon entry; TP splits it into single chars.
2. Lexicon entry "not" (lex[28]): cnt=14, neg_tot=13, neg_viol=4,
   is_negator=0. Violation rate 4/13 = 31%, below the 70% threshold
   (viol*10 >= tot*7).
3. The pair ("not","g") at test time WOULD work: "g" (lex[31]) has
   prim=2 (color 2), and NEG targets lack color 2. But the interpret
   negator branch is never taken because is_negator("not")=0.

### Root cause
In learn_update section 3 (negator stats), every adjacent pair
(segs[i], segs[i+1]) is counted when segs[i+1] has a grounded primary
(primary_of >= 0), across ALL episodes. DEVANG3's TP segmentation
splits color words inconsistently ("red" -> "r"+"ed", "grn" -> "g"+"r"+"n"
in some contexts). Single-char fragments like "r" (lex[3], prim=7),
"g" (lex[31], prim=2), "n" (lex[25], prim=2) have grounded primaries
(from their host-word contexts) but the WRONG semantics for negator
evaluation. When "not" is followed by a fragment, the viol check
(obj_has(ep,tgt,fv)==0) tests the wrong feature, usually failing to
increment viol. This pollutes neg_tot with non-violations, driving
viol/tot below threshold.

DEVANG2's bigram DP had different (also imperfect) segmentation that
happened to keep "not" paired with whole color words more often,
giving 1/3.

### How splits differ (DEVANG2 vs DEVANG3)
- DEVANG2 seg_dp: scores segments by average internal bigram log-count
  minus boundary cost. Tends to keep frequent 3-char words whole once
  bigram counts grow, but suffers cold-start whole-utterance poisoning.
- DEVANG3 seg_tp3: boundary iff forward TP
  s(p) = (ilog(c_ab+1) - ilog(c_a+4))*10 < -15. Correctly splits
  "tak|not|grn" at test time, but "grn" fragments persist from training
  because the word never consolidated in the lexicon (low frequency in
  NEG contexts + TP splits it early, preventing lexicon formation).

## Fix (K2)

In learn_update section 3 (negator stats), require the following
segment xi to be an ESTABLISHED WORD (lex_cnt(W,xi) >= 3) in addition
to primary_of(W,xi) >= 0 before incrementing tot/viol for mi.

Rationale: Negator semantics ("X does not have feature F") require X
to be a content word, not a character fragment. Fragments carry
accidental primaries from their host contexts. Filtering to
established words (count >= 3, same bar as primary_of's count >= 2
plus margin) gives "not" clean (tot,viol) from true ("not", color-word)
pairs in NEG episodes, restoring viol/tot to ~1.0.

This is a generic mechanism (applies to all candidate negators, not
"not"-specific), not a word-specific hack. No word knowledge is added.

## Kill bars

- K1: NEG diagnosis documented (above). PASS (preregistered).
- K2: Established-word filter implemented in negator stats. Must be
  the ONLY change vs DEVANG3 (plus label updates).
- K3: Test accuracy >= 17/20 (tie/beat fixed-width baseline), 3/3
  byte-identical runs, exit 0, zero stderr.

## Method
1. Copy devang3.zag to devang4.zag (owned path).
2. Modify learn_update section 3: add lex_cnt(W,xi) >= 3 condition.
3. Compile with znc, run 3 times, verify md5 identical.
4. Report BUILD-PASS if K3 met, else BUILD-FAIL with analysis.

## Governance
- Pure Zag only. No Python at any stage.
- No em dashes in source or docs (byte-check with grep).
- Prereg committed alone before implementation.
- Owned path only: docs/lab/research-lead/overnight-20260928/devang4/.
- Do not modify devang3/ or any other worker's files.
- No bar weakening. K3 is 17/20 before and after.
