# PREREG_SEGREDESIGN: Transitional-Probability Threshold Segmentation

**Status:** FROZEN. Committed before any implementation.
**Date:** 2026-09-30.
**Worker:** Segmentation Redesign Worker.
**Owned path:** `docs/lab/research-lead/overnight-20260928/seg_redesign/`

## 1. Problem analysis: why bigram DP fails

DEVANG2 (BUILD-FAIL, 153e2af8e) isolated the failure to segmentation
design, not implementation. Root cause analysis:

1. **Cold start tie.** `seg_dp` scores a segment as
   `avg_bigram_ilog * 10 - 40`. At t=0 all bigram counts are zero, so
   every segmentation scores `-40` per segment. The DP tie-break
   (strict `>`) keeps the longest segment, so nseg=1: the whole
   utterance (e.g. "takredbal") becomes one lexicon entry.

2. **Lexicon poisoning is permanent.** `lex_add` returns -1 when the
   64-entry lexicon is full. Early whole-utterance entries fill the
   finite lexicon, so true words discovered later can never be added.
   The learner never recovers. This is the "never recovers" mechanism.

3. **Raw bigram frequency cannot see function-word boundaries.** "tak"
   is always word 0, followed by varied content words. The boundary
   bigram "kr" (tak|red) occurs exactly as often as the within-word
   bigrams "re","ed" (18 times in phase 1), because "kr" appears
   whenever "red" follows "tak". Raw frequency is blind here. What
   distinguishes them is the TRANSITIONAL PROBABILITY: P(a|k)=1.0
   within "tak" (k is always followed by a), while P(r|k)=0.22 across
   the boundary (k is followed by r,b,n,s depending on the next word).
   Normalizing by the left character's total count reveals the
   boundary. The bigram DP never normalizes.

## 2. New approach: TP-THRESHOLD segmentation

Replace raw bigram counts with Laplace-smoothed forward transitional
probability as the boundary cue, with an absolute threshold.

**State added:** unigram[26] counts alongside bigram[26][26].
Updated online from each raw utterance (same as bigrams; no
segmentation dependence, so K11-style no-leakage holds).

**Boundary score** for the pair (x=utt[p], y=utt[p+1]):

    s(p) = (ilog(c_xy + 1) - ilog(c_x + 26)) * 10

where c_xy is the bigram count, c_x the unigram count of the left
character. This is 10x the integer log of the Laplace-smoothed
P(y|x) = (c_xy+1)/(c_x+26).

**Decision rule:** place a word boundary between p and p+1 iff
s(p) < THETA, with THETA = -15 (fixed constant, same status as the
old -40: a generic prior, not word-specific knowledge).

**Cold start behavior (by construction, not tie-break):** at t=0,
c_xy=0 and c_x=0, so s(p) = (ilog(1)-ilog(26))*10 = (0-4)*10 = -40
< -15 for every p. Boundaries everywhere: the first utterance
segments into single characters. The lexicon receives at most 26
single-character entries, never whole utterances. No poisoning.

**Learning dynamics:** as counts accumulate, deterministic
within-word transitions (e.g. k->a, always) rise above THETA and
merge, while variable cross-boundary transitions (k->r/b/n/s) stay
below THETA and keep boundaries. Expected steady state on phase-1
data: "tak|red|bal"-style splits for most words.

**Known limitation (disclosed):** words whose left characters are
very frequent (e.g. "bal": P(a|b) is diluted because b starts
bal/blu/big/biger) may stay over-split. This is a recall limitation
of forward TP, not a correctness bug. K3 measures net improvement
over baseline, not perfection.

**What this does NOT do:** no researcher-supplied word list, no
word-length prior, no position-0 special casing, no template
knowledge. The machinery (counts, TP, threshold) is generic.

## 3. Prototype design

Standalone pure-Zag program `segproto.zag` (no dependency on
devang2.zag; self-contained):

1. Copies the 12 word definitions and the phase-1 episode generator
   (60 episodes: 24 DIRECT, 12 NEG, 12 REL, 12 SIZE) from DEVANG2.
   Target features (color/shape/size) stored per episode.
2. Variant V0 (baseline): the exact `seg_dp` bigram DP from DEVANG2.
3. Variant V1 (new): TP-THRESHOLD as specified above.
4. Both variants run the identical online loop over episodes 0..59:
   segment episode t using counts from episodes 0..t-1 only, then
   update counts (bigram, and unigram for V1) from the raw utterance.
   Segments feed a 64-entry lexicon (get/add/bump, same semantics as
   DEVANG2 lexicon).
5. Report per variant at t=60:
   - nseg on episodes 0,1,2 (cold-start behavior check)
   - lexicon size
   - words discovered: of the 10 phase-1 true words
     (tak, not, red, blu, bal, sph, cub, big, biger, smal), how many
     appear as exact lexicon entries with count >= 2.

Determinism: seeded LCG, no wall clock. 3/3 byte-identical runs.

## 4. Kill bars

- K1 (approach defined): this prereg specifies the TP-THRESHOLD
  mechanism completely before implementation. PASS by existence.
- K2 (prototype implemented): `segproto.zag` compiles with znc and
  runs to completion in pure Zag, no Python at any stage. PASS/FAIL
  by execution.
- K3 (beats baseline): V1 discovers strictly more true words
  (count >= 2) at t=60 than V0 on the identical episode sequence.
  Baseline reference: DEVANG2 K1 = 3/10. K3 requires V1 > V0 AND
  V1 >= 5/10. PASS/FAIL by measured numbers.

**Verdict rule:** REDESIGN-PROTOTYPED requires K1, K2, K3 all PASS.
Otherwise REDESIGN-BLOCKED.

## 5. Governance

- Prereg committed ALONE before any .zag implementation.
- Pure Zag only. No Python at any stage (coding, building, running,
  analysis).
- No em dashes in documentation (verified via od before commit).
- Owned paths only (`seg_redesign/`). Local commits only.
- No change to devang2.zag or any other worker's files.
