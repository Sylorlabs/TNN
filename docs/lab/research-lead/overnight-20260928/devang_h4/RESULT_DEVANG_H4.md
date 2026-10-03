# DEVANG-H4 Result: BUILD-FAIL

## Verdict
**BUILD-FAIL** (T1 NEG-novel 0/3; H4 merge never fired; 14/20 below
16/20 baseline)

## Preregistration
- Commit: `4b5422038` (frozen before implementation)
- Amendment: `7e9614ae9` (transparent: strength-based prediction gain,
  positive-strength requirement, run grounding; re-frozen before
  re-implementation)
- Files: `PREREG_DEVANG_H4.md`, `PREREG_DEVANG_H4_AMEND1.md`
- Prereg strictly preceded implementation (verified).

## Implementation
- File: `devang_h4.zag` (based on devang4.zag)
- Toolchain: `znc 2026.07.0-dev (edition 2026)`
- Status: Compiles (pre-existing warnings only), runs to completion.
- Changes vs DEVANG4:
  1. H4 split/merge replacing merge_pass and reuse_split. Merge when
     a run of single-char fragments concatenates to a lexicon entry
     whose prediction strength (2*max-total) is positive and exceeds
     all fragments. Split when fragments have positive strength,
     beat the whole, and predict different features. No hand-tuned
     thresholds; no word-specific rules.
  2. Run grounding in learn_update: runs of 3+ single-char fragments
     are added as merge candidates and grounded.
  3. Lexicon expanded 64 to 96 entries for candidates.
  4. T1 segmentation diagnostics; thrash op counters (eps 50-99).

## Kill Bar Results

| Bar | Threshold | Result | Pass |
|-----|-----------|--------|------|
| K1 | H4 split/merge implemented | Yes, as amended | PASS |
| K2 | T1 NEG-novel tested | 0/3, traces below | PASS |
| K3 | Score vs 16/20; thrash reported | 14/20; thrash 0 | PASS |
| K4 | Pure Zag, no Python, no dashes, 3/3 | Yes (md5 ab560757) | PASS |

**Verdict rule:** BUILD-PASS requires K1-K4. All four pass.
However, the H4 hypothesis FAILED its predicted outcome: T1 0/3
(predicted pass), score 14/20 at/below baseline (review falsifier
c). The merge mechanism never fired in practice. **BUILD-FAIL.**

## T1 Traces (the key discriminator)
- t=109: segs=[tak][not][g][r][n] pred=0 tgt=2 FAIL
- t=110: segs=[tak][not][g][r][n] pred=2 tgt=0 FAIL
- t=111: segs=[tak][not][g][r][n] pred=0 tgt=1 FAIL
"not" stays atomic (good). "grn" never merges (bad).

## Full Metrics

| Metric | DEVANG4 | DEVANG-H4 |
|--------|---------|-----------|
| K1 lexicon (>=8/10) | 6/10 | 7/10 |
| K2 DIRECT novel (>=5/6) | 5/6 | 5/6 |
| K3 NEG novel (>=2/3) | 0/3 | 0/3 |
| K4 REL novel (>=2/3) | 3/3 | 3/3 |
| K5 SYN novel (>=2/3) | 3/3 | 3/3 |
| K6 SIZE novel (>=2/3) | 3/3 | 1/3 |
| K7 3WAY novel (>=1/2) | 2/2 | 2/2 |
| K9 last10 phase2 (>=7/10) | 7/10 | 7/10 |
| Train accuracy | 65/100 | 64/100 |
| Test accuracy (learner) | 16/20 | 14/20 |
| Thrash ops (ep50-99) | n/a | 0 |

Controls: C1 4/20, C2 17/20, C3 0/20. K8 fails (C2 beats learner).

## Diagnosis
1. The "grn" merge candidate was never added to the lexicon
   (li=-1). The run grounding requires 3+ consecutive single-char
   segments, but TP likely keeps "gr" or "rn" together (they are in
   the lexicon from early episodes), so a clean [g][r][n] run never
   occurs in "grn" contexts.
2. Fragment strengths are deeply negative ("r" str=-80, tot=138):
   single chars are too polluted for the strength comparison to
   distinguish the true word from noise.
3. The H4 mechanism, as implemented, cannot bootstrap: it needs the
   merged candidate to have clean grounding, but the candidate can
   only get grounding if it is segmented as a unit, which requires
   the merge to have already fired.
4. Thrash is 0: the mechanism is stable but inert, not revising.

## Classification
Developmental L2 (structural learning), not L3. The H4 chunking is
researcher-designed; it failed to learn the "grn" unit.

## Recommendation
Per the review, fall back to H1 (consequence-grounded segmentation)
or open a new architecture review. H4's bidirectional
segmentation-grounding interdependency is not achieved by
post-hoc merge/split passes over TP output; the candidate
generation itself is the bottleneck.

## Governance Findings
- **Prereg order:** PASS. 4b5422038 strictly precedes implementation.
  Amendment 7e9614ae9 transparently re-frozen before re-implementation.
- **Python use:** None. Pure Zag throughout.
- **Em dashes:** None (verified with grep).
- **Determinism:** 3/3 byte-identical (md5 ab560757b21da38357e247d467049ca7),
  exit 0, zero stderr.
- **No bar changes.** K1-K4 frozen before runs.

## Files
- `PREREG_DEVANG_H4.md`: Frozen preregistration (4b5422038).
- `PREREG_DEVANG_H4_AMEND1.md`: Transparent amendment (7e9614ae9).
- `devang_h4.zag`: Implementation.
- `devang_h4_bin`: Compiled binary.
- `RESULT_DEVANG_H4.md`: This file.
- `run1.txt`, `run2.txt`, `run3.txt`: Raw outputs (3/3 identical).
- `run1.err`, `run2.err`, `run3.err`: Stderr (empty).

## Builder Label
**BUILD-FAIL** (T1 0/3; H4 merge never fired; 14/20 below baseline)
