# Fork W Falsifier Report — 2026-09-24

## Paraphrase inversion

**Method**: For each PARA SAME pair (kind=1), verify that both mates produce identical verdict strings (M3). For FLIP pairs (kind=2/3), verify verdicts differ (M2).

**Result**:
- M2 (flip divergence): 21/23 PASS (91% ≥ 90% bar)
- M3 (same stability): 3/15 FAIL (20% < 95% bar)

**Interpretation**: The witness correctly distinguishes meaning-flips (different verdicts) but fails to stabilize paraphrases (same meaning → different verdicts). The canonicalizer does not normalize "feline fragment" vs "cat" to identical forms in all cases. This is a genuine mechanism limitation, not a test artifact.

## Dead testimony

**Method**: Ledger replay (`lg_verify`) checks that all 167 entries form an intact hash chain (prev pointers link correctly).

**Result**: `LEDGER entries=167 verify=1` — PASS.

**Interpretation**: The testimony ledger is intact; no entries were dropped, reordered, or tampered with between the fixture loop and scoring. Dead testimony (replay of a dead ledger) would fail the prev-linkage check.

## Fabrication blindness (W2)

**Method**: All 10 HALPTR fixtures (fabricated pointers) must produce `S_HALLUC` status.

**Result**: 4/10 FAIL under frozen rules.

**Interpretation**: Under the frozen prereg rule ("coverage failure → every atom V_UNGROUNDED"), 6 HALPTR fixtures fail coverage (their drafts are full sentences not covered by steps) and become V_UNGROUNDED instead of V_HALLUC. The witness is "blind" to the fabrication because the coverage rule overrides the hallucination finding.

With the proposed (unapproved) Amendment A1, W2 achieves 10/10. The 4/10 result is the honest frozen-rule outcome and reveals a spec-level tension: the coverage rule and the fabrication-detection requirement conflict for sentence-length drafts.

## Summary

| Falsifier | Result | Verdict |
|-----------|--------|---------|
| Paraphrase inversion (M2/M3) | M2 PASS, M3 FAIL | Mechanism partially vulnerable |
| Dead testimony (ledger replay) | PASS | Ledger intact |
| Fabrication blindness (W2) | 4/10 FAIL | Spec tension, not mechanism bug |
