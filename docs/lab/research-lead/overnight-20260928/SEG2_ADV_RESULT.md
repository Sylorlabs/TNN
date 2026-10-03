# SEG2-ADV RESULT: H-SEG2 Red Team — DOWNGRADED

**Prereg:** PREREG_SEG2_ADV.md (commit 26fc0ee4e, frozen before any attack
code or execution)
**Date:** 2026-09-29
**Verdict:** H-SEG2 DOWNGRADED. Three of four attacks succeed. The frozen
5/5 bars are not retroactively altered (all four frozen experiments
reproduce exactly); the source audit passes. The downgrade narrows the
generality claim and documents two demonstrated failure classes.

## Attack results

All attacks executed in pure Zag. Main binary deterministic 3/3
byte-identical (md5 721bd84a3aaeac9cc4f65da679b96b23). Long-sequence
binary crashes reproducibly 2/2 (exit 1, identical panic).

### Regression control: PASS

The attack harness is a verbatim copy of seg2_learn.zag (mechanism lines
1-283 byte-identical by diff) with only new fixture functions and a new
main(). All four frozen experiments reproduce exactly:

- REG-A: SEGMENTED small|green|ball, score 132, NOPT 1
- REG-C: SEGMENTED small|red|cube, score 100, NOPT 1
- REG-D: SEGMENTED big|b|l|u|e|cube, score -30, NOPT 1
- REG-B: AMBIGUOUS, candidates ab|cde and abc|de, score 34

The harness is faithful; what follows is the target failing, not the
harness.

### X-SG2-1 (penalty sensitivity): SUCCEEDS -> DOWNGRADE

**ADV-1** (corpus: xabcd,xabcd,yabcd,yabcd,zabcd,zabcd;
shared chunk "abcd" count 6, score 96; true words score 50):

- T1 "xabcd" (a seen training word): SEGMENTED **x|abcd**, score 76,
  NOPT 1. Contract: "xabcd". The mechanism fragments a word it saw in
  training.
- T2 "xabcdyabcd" (novel pairing of seen words, EXP-C shape):
  SEGMENTED **x|abcd|y|abcd**, score 152, NOPT 1. Contract:
  "xabcd|yabcd" (100).

**ADV-2** (corpus ADV-1 + wabcd,wabcd; "abcd" count 8, score 128):

- T2 "xabcdyabcd": SEGMENTED **x|abcd|y|abcd**, score 216, NOPT 1.
  Contract: "xabcd|yabcd" (100).

All three outputs match the frozen prereg predictions exactly
(76 / 152 / 216). Root cause: chunk scores scale as count*len^2 while
the penalty is a constant 20 per residue character. The repair only
holds while count(C)*len(C)^2 - 20*r < word_score. In ADV-1,
96 - 20 = 76 > 50; the inequality the frozen fixture satisfied
(36 - 20 = 16 < 32) reverses as soon as the shared chunk is frequent.
FBPEN=20 was tuned to the frozen fixture's frequency regime (the
prereg says so itself: "validated in H-SEG exploratory analysis");
it does not generalize.

Narrowed claim: the shared-substring limitation is closed only when
the shared chunk's count*len^2 advantage over the true word is less
than 20 per residue character. Outside that band the H-SEG failure
recurs, now worse: the mechanism fragments seen words.

### X-SG2-2 (adversarial fixture): SUCCEEDS -> DOWNGRADE

Same fixtures as X-SG2-1, reported independently per the prereg. The
corpora are natural (repeated words, same regime as the frozen corpus)
and the tests are exactly the frozen EXP-C shape (novel pairing of
seen words) plus a seen word. No exotic inputs were needed. The
failure is systematic across two frequency levels (count 6 and
count 8), not a one-off.

### X-SG2-3 (long sequences): SUCCEEDS -> robustness boundary

**ADV-3:** frozen EXP-A corpus table, 120-char digit test
("0123456789" x12; zero chunk matches, pure fallback path).
DP completes: SCORE -2400 (120 x -20), NOPT 1. Then:

```
panic: slice index out of bounds
```

Exit 1, reproducible 2/2 with byte-identical output. The 120-move
reconstruction path overflows build_best's 64-entry move stacks
(seg2_learn.zag lines 151-152; same in enum_bwd, lines 270-271).
The runtime traps it as a bounds panic; without the trap this is heap
corruption. A segmentation mechanism that crashes on a 120-character
input has a demonstrated robustness limit. Long inputs are outside the
frozen scope, so this is documented as a downgrade-relevant boundary,
not a bar failure. Repair direction: size move stacks by n, or cap
input length explicitly.

### X-SG2-4 (source audit): PASS

- (a) Fallback relax site (line 241) applies 0-FBPEN() per character.
  Confirmed.
- (b) Sentinel DPSENT()=-1000000 (line 35), table init (line 235),
  guard dpi>DPSENT() (line 240). Confirmed correct.
- (c) No expected-output literals. Corpora are disclosed fixtures
  (input data, not answers); verdict strings are generic.
- (d) Latent bounds noted informationally: mv_add 8-move cap per
  position (line 122, silently drops further tied moves, can corrupt
  nopt/AMBIGUOUS enumeration under heavy ties); 64-deep stacks
  (X-SG2-3); nopt cap 999 (line 141); 256-byte reconstruction buffer.

No spoofing. The SURVIVES verdict on the frozen bars was earned.

## Revised classification

H-SEG2 DOWNGRADED: bounded L2 segmentation repair whose fragmentation
penalty is valid only in a narrow, authored frequency band. What
stands: the four frozen experiments, determinism, ambiguity detection
on the frozen fixture, honest labeling of FBPEN as authored. What
falls: (1) the claim that the shared-substring limitation is closed in
general -- it recurs whenever a shared chunk is frequent (demonstrated
at count 6 and count 8, fragmenting even seen words); (2) robustness
on inputs longer than 64 moves (demonstrated crash at 120 chars).

Repair directions (not implemented by the red team): frequency-scaled
penalty (e.g., penalty proportional to competing chunk scores) or a
derived MDL lexicon prior instead of a constant; move stacks sized by
n; explicit statement of the validated frequency regime.

## Commits (branch tnn-native-lab, local only)

- 26fc0ee4e -- PREREG SEG2-ADV FROZEN (before any attack code)
- (this commit) -- seg2_adv.zag, seg2_advlong.zag,
  SEG2_ADV_RAW.txt, SEG2_ADV_RAW_LONG.txt, SEG2_ADV_RESULT.md

## Files

- docs/lab/research-lead/overnight-20260928/PREREG_SEG2_ADV.md
- docs/lab/research-lead/overnight-20260928/seg2_adv.zag
- docs/lab/research-lead/overnight-20260928/seg2_advlong.zag
- docs/lab/research-lead/overnight-20260928/SEG2_ADV_RAW.txt
- docs/lab/research-lead/overnight-20260928/SEG2_ADV_RAW_LONG.txt
- docs/lab/research-lead/overnight-20260928/SEG2_ADV_RESULT.md

## Governance

Pure Zag throughout; no Python at any stage. Prereg 26fc0ee4e strictly
precedes attack implementation and execution. Only adversary-owned
files staged and committed; concurrent agents' files untouched. No em
dashes in documentation. No binaries committed (/tmp binaries only).
No commit-hygiene sweep encountered on my own commits; one stale
index.lock wait was not needed (no contention observed at commit
time).
