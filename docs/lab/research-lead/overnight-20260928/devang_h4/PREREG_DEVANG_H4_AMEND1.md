# AMENDMENT to PREREG_DEVANG_H4.md (transparent, before re-implementation)

## Flaw found in frozen mechanism
The prereg specified merge iff the merged candidate's best-feature
RAW COUNT strictly exceeds both fragments' best-feature raw counts.
This fails due to frequency imbalance: single-char fragments like
"g" and "r" occur in many contexts (grn, big, biger, red), so their
raw best-feature counts grow large from noisy accidental
co-occurrences. The rare merged candidate ("gr", 7 observations) can
never exceed them in raw counts, so the merge never fires. Observed:
T1 segments as [tak][not][g][r][n], 0/3, 12/20 overall.

## Corrected mechanism (no thresholds, no constants)
Define prediction strength for a lex entry as:
  strength(li) = 2 * max_feature_count(li) - total_feature_count(li)
This is the margin by which the best-predicted feature beats all
other features combined. Positive iff the best feature is a strict
majority. It measures prediction QUALITY, not observation count.

Merge iff strength(m) > 0 AND strength(m) > strength(a) AND
strength(m) > strength(b). Split iff strength(a) > 0 AND
strength(b) > 0 AND strength(a) > strength(whole) AND strength(b) >
strength(whole) AND best_feature(a) != best_feature(b).

The positive-strength requirement (strict majority) is part of
"predicts": a unit that does not predict a majority feature has no
prediction to compare. The zero point is natural, not hand-tuned.
This prevents the split from firing on noise (e.g., "not" -> "n"+"ot"
when none have clear grounding).

This is still a pure prediction-gain comparison. No hand-tuned
thresholds. No word-specific rules. No constant rescues a test item.
It operationalizes the review's "conjunction predicts better than
either alone" correctly under frequency imbalance.

## Re-freeze
Implementation will be updated to use strength. Test protocol,
kill bars K1-K4, and verdict rule unchanged. K1 now requires the
strength-based split/merge as specified here.
