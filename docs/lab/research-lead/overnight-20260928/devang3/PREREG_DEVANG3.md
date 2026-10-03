# PREREG_DEVANG3: Developmental Semantic Language, Third Attempt

## Context
- DEVANG1: BUILD-FAIL (crash).
- DEVANG2: BUILD-FAIL (153e2af8e). Bigram DP segmentation failed:
  zero initial counts caused all segmentations to tie, defaulting to
  whole-utterance segments. Learner 13/20 vs fixed-width baseline 17/20.
- Segmentation Redesign: REDESIGN-BLOCKED (8178531c8). Frozen V1
  (TP-threshold, +26 Laplace) scored 4/10 < 5/10. Exploratory V3
  (TP-threshold, +4 Laplace, THETA=-15) scored 6/10, doubling the
  V0 baseline (3/10). Cold-start fix validated: single characters at
  t=0, no lexicon poisoning. V3 over-merges ([takb] c=15, [takred]
  c=6). Hard words (bal, biger, smal) need grounding cues.

## Design

### Pass 1: V3 TP segmentation (frozen from redesign)
For each inter-character position p in utterance of length n,
with bigram count c_ab and unigram count c_a (both from episodes
0..t-1 only, true online):
  s(p) = (ilog(c_ab + 1) - ilog(c_a + 4)) * 10
Boundary at p iff s(p) < -15.
At t=0, s(p) = (ilog(1) - ilog(4)) * 10 = (0 - 2) * 10 = -20 < -15,
so boundaries everywhere: single characters, no poisoning.
Formula copied exactly from segproto.zag seg_tp3.

### Pass 2: Lexicon-reuse over-merge repair (new)
For each pass-1 segment (st, ln) with ln > 1, try every split
point sp in 1..ln-1. Let L = lex_find(st, sp), R = lex_find(st+sp,
ln-sp). If both found and min(lex_cnt(L), lex_cnt(R)) >= 2, the
split is eligible. Choose the eligible split maximizing
min(count_left, count_right). If none eligible, keep the segment.
Recurse on each half (each split strictly reduces piece length,
so this terminates). Rationale: [takb] splits to [tak][b] once
"tak" is established, because both halves are known words; true
novel words ([red], [sph]) have no eligible split since their
proper subparts are not established lexicon entries.
This is generic machinery: no word-specific knowledge, only the
learner's own accumulated lexicon.

### Unigram tracking (new)
Separate 104-byte buffer UG (26 x i32), updated in the training
loop after segmentation/interpretation, alongside the bigram
update. Strictly online: episode t uses counts from 0..t-1.

### Everything else
Identical to DEVANG2 (153e2af8e): episode generator (seed
123456789), lexicon, grounding, negator/comparative detection,
interpret, learn_update, controls C1/C2/C3, 100 train + 20 test
episodes, 3/3 determinism. Only the segmentation function changes
(seg_dp replaced by seg_devang3). C2 control still uses
seg_fixed3 unchanged.

## Kill bars (frozen)
- K1: V3 segmentation implemented as specified: s(p) =
  (ilog(c_ab+1) - ilog(c_a+4)) * 10, boundary iff s(p) < -15,
  single characters at t=0. Verified by code inspection against
  segproto.zag seg_tp3.
- K2: Over-merging addressed via lexicon-reuse pass-2 as specified
  above. Verified by code inspection and by observing that
  spurious units ([takb], [takred]) are split when their parts
  are established.
- K3: Test accuracy (learner, 20 test episodes) >= 17/20, i.e.,
  beats or ties the DEVANG2 fixed-width baseline (17/20).
  3/3 byte-identical runs required.

## Verdict rule
BUILD-PASS requires K1, K2, K3. Otherwise BUILD-FAIL.
No bar may be altered after results are observed.

## Governance
- Pure Zag: implementation, compilation, execution, analysis.
  No Python anywhere.
- No em dashes in source or documentation.
- Prereg committed alone before any implementation.
- Commits local, owned paths only
  (docs/lab/research-lead/overnight-20260928/devang3/).
- Additional DEVANG2-protocol metrics (K1..K12 style) reported
  for comparability, but the verdict uses the three bars above.
