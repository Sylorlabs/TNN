# DEVANG3 Result: BUILD-FAIL (close)

## Verdict
**BUILD-FAIL** (K3: 16/20 < 17/20; substantial progress vs DEVANG2)

## Preregistration
- Commit: `b2ceb6b38`
- File: `PREREG_DEVANG3.md`
- Prereg strictly preceded implementation (verified: b2ceb6b38 is an
  ancestor of the implementation commit).

## Implementation
- File: `devang3.zag` (copied from devang2.zag, segmentation replaced)
- Toolchain: `znc 2026.07.0-dev (edition 2026)`
- Status: Compiles (pre-existing warnings only), runs to completion.
- Changes vs DEVANG2:
  1. `seg_tp3`: V3 TP segmentation, formula copied exactly from
     segproto.zag: s(p) = (ilog(c_ab+1) - ilog(c_a+4)) * 10,
     boundary iff s(p) < -15.
  2. `reuse_split` + `seg_devang3`: lexicon-reuse pass 2. Each
     pass-1 segment longer than 1 char is split at the point
     maximizing min(count_left, count_right) over splits where both
     halves are lexicon entries with count >= 2. Recursive.
  3. `unigram_update`: 104-byte unigram buffer, updated online after
     segmentation (same point as the bigram update).
  4. `main`: the two `seg_dp` calls replaced by `seg_devang3`;
     unigram buffer allocated; output label updated.
- Everything else identical to DEVANG2: episode generator (seed
  123456789), lexicon, grounding, negator/comparative, interpret,
  controls C1/C2/C3.

## Kill Bar Results

| Bar | Threshold | Result | Pass |
|-----|-----------|--------|------|
| K1 | V3 formula as specified, single chars at t=0 | Code matches segproto exactly | PASS |
| K2 | Lexicon-reuse pass-2 implemented as specified | Implemented per prereg | PASS |
| K3 | Test accuracy >= 17/20 | 16/20 | FAIL |

3/3 byte-identical runs (md5 ee6f434a99bfca96781b2c77dbbca9c3),
exit 0, zero stderr.

**Verdict rule:** BUILD-PASS requires K1, K2, K3. K3 FAIL.
**BUILD-FAIL.**

## Full Protocol Metrics (for comparability with DEVANG2)

| Metric | DEVANG2 | DEVANG3 |
|--------|---------|---------|
| K1 lexicon (>=8/10) | 3/10 | 6/10 |
| K2 DIRECT novel (>=5/6) | 5/6 | 5/6 |
| K3 NEG novel (>=2/3) | 1/3 | 0/3 |
| K4 REL novel (>=2/3) | 3/3 | 3/3 |
| K5 SYN novel (>=2/3) | 1/3 | 3/3 |
| K6 SIZE novel (>=2/3) | 3/3 | 3/3 |
| K7 3WAY novel (>=1/2) | 0/2 | 2/2 |
| K9 last10 phase2 (>=7/10) | 6/10 | 7/10 |
| Train accuracy | 43/100 | 65/100 |
| Test accuracy (learner) | 13/20 | 16/20 |
| C1 no-seg | 4/20 | 4/20 |
| C2 fixed-width-3 | 17/20 | 17/20 |
| C3 substring | 0/20 | 0/20 |
| Sub-bars (need >=4) | 3/7 | 6/7 |

## Analysis

1. **Large improvement.** Test accuracy 13/20 -> 16/20. Sub-bars
   3/7 -> 6/7. Train accuracy 43/100 -> 65/100. Lexicon discovery
   3/10 -> 6/10. The V3 segmentation plus lexicon-reuse is a real
   architectural step, not a parameter tweak.

2. **K3 missed by one point.** 16/20 vs the 17/20 fixed-width bar.
   The bar is not weakened; the verdict stands.

3. **NEG regressed (1/3 -> 0/3).** The negator "not" is discovered
   (in the 6/10 lexicon hits) but fails on novel NEG items. Possible
   causes: the lexicon-reuse pass splits "not" contexts differently,
   or the negator grounding needs the exact bigram-DP segment
   boundaries it was tuned against. This is the specific gap for
   the next wave.

4. **K2 status.** The pass-2 mechanism is implemented as specified.
   Whether it fully eliminates [takb]/[takred] over-merging in live
   runs (vs merely being available) is not directly measured by the
   frozen bars; the 16/20 result bounds its practical effect.

## Governance Findings
- **Prereg order:** PASS. b2ceb6b38 strictly precedes implementation.
- **Python use:** None. Pure Zag (implementation, compilation,
  execution, analysis).
- **Em dashes:** None in source or documentation.
- **No bar changes.** K3 was 17/20 before the run and remains so.

## Classification
Developmental L2 (structural learning), not L3. The segmentation
cue (TP-threshold) and the repair (lexicon-reuse) are
researcher-designed generic mechanisms; the learner discovers the
words. No representational invention claimed.

## Files
- `PREREG_DEVANG3.md`: Frozen preregistration.
- `devang3.zag`: Implementation.
- `RESULT_DEVANG3.md`: This file.
- `run1.txt`, `run2.txt`, `run3.txt`: Raw outputs (3/3 identical).

## Builder Label
**BUILD-FAIL** (K3: 16/20 < 17/20)
