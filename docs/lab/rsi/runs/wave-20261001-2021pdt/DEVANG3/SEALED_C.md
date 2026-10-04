# SEALED_C.md: Sealed Family C (post-freeze adversarial)

Adversary: DEVANG3-ADVERSARY, wave-20261001-2021pdt. Designed post-freeze
from PREREG_DEVANG3.md section 5 requirements only. The builder's dev files
were not inspected. Sealed package lives in DEVANG3/sealed/; the builder
never reads it.

## Files and pre-run sha256 (recorded BEFORE any sealed run)

- `sealed/sealed_c.txt` (header `60 20`, 60 train + 20 test episodes):
  `c514baf77bc7cfe86c51bb6570b291e5b5c7b57c92ffdd02583b450637c72aac`
- `sealed/sealed_c_key.txt` (20 test tgts):
  `248542f1ca74c1aa4eff88c918f2abbe8fcd4f6802c10990d812817b7c231c79`
- `sealed/genC.zag` (deterministic generator, pure Zag):
  `95f90b1fa96800107070946f49ace75d97f1fe7c5a3424361714d39ee1b5fbbc`
- `sealed/genC` (compiled generator binary; build artifact, not sealed data)

Episode line format (as the sealed interface requires):
`<c0> <s0> <z0> <c1> <s1> <z1> <c2> <s2> <z2> <tgt> <utterance>`,
features in 0..2, tgt in 0..2, utterance [a-z] 1..24 chars.

## Requirement compliance

- 20 novel test episodes (all 7 test utterance forms have 0 occurrences
  in the 60 training episodes; verified by count).
- New surface vocabulary, no Family A word forms. Family C words:
  zo, kan, kana, kalo, tel, telan, temo, bo, bona, nu, maro.
  Intersection with {tak,not,red,blu,grn,bal,sph,cub,tri,big,biger,smal}
  is empty.
- Word lengths 2 to 6 (range): 2 (zo,nu,bo), 3 (kan,tel), 4
  (kana,kalo,temo,bona,maro), 5 (telan).
- Prefix pairs sharing >= 2 (7): (kan,kana), (kan,kalo), (kana,kalo),
  (tel,telan), (tel,temo), (telan,temo), (bo,bona).
- Suffix pairs sharing >= 2 (3): (kana,telan), (kana,bona), (telan,bona),
  all sharing "na".
- Boundary statistics materially different from Family A (attested
  below).
- Raw-byte trap included (described below).
- Not a trivial Family A variant: new vocabulary, new length
  distribution, new boundary positions, systematic prefix/suffix
  ambiguity Family A lacks.

## Semantics (mirrors Family A exactly; adversariality is at the
segmentation level, which is what DEVANG3 claims)

- Objects: color 0/1/2, shape 0/1/2, size 0/1/2. Roles: zo = action
  marker (interpret skips segment 0); kan/kana/kalo = colors 0/1/2;
  tel/telan/temo = shapes 0/1/2; bona/bo = sizes 0/1; nu = negator;
  maro = comparative.
- Templates: DIRECT "zo C S" (target has color C, shape S); NEG
  "zo nu C S" (target has shape S, not color C); REL "zo maro S"
  (target is the biggest shape-S object); SIZE "zo Z S" (target has
  size Z, shape S).
- Scenes are constructed so the template's scoring gives the target a
  unique maximum (DIRECT/SIZE 2 vs 0/0; NEG 3 vs 1/-1; REL 3 vs 0/0).
  Target index rotates 0,1,2 across repeats.
- Train: DIRECT-A 16, DIRECT-B 8, NEG 12, REL 12, SIZE 12 (60).
  Every word occurs >= 6 times in training (zo 60, kan 16, kana 14,
  kalo 6, tel 26, telan 26, temo 6, bo 6, bona 6, nu 12, maro 12),
  so lexicon counts reach the primary threshold (>= 2) and the
  negator/comparative statistical tests reach their minimum totals
  (>= 3).
- Test (20): DIRECT-T 8 on novel combos (2,1) "zokalotelan" x4 and
  (1,2) "zokanatemo" x4; NEG-T 4 on (2,1)/(1,2); REL-T 4 on shape 2
  "zomarotemo" (shape 2 never in REL training); SIZE-T 4 on
  (1,2)/(0,2) "zobotemo"/"zobonatemo".

## Boundary statistics: Family A vs Family C (attestation)

Family A: 10 of 12 words have length 3 (83%); mean length 3.17.
Utterance boundaries cluster at multiples of 3 (DIRECT 3,6; NEG
3,6,9; REL 3,8; SIZE 3,7; 3WAY 3,6,9). Only one prefix-ambiguous
pair (big/biger); no suffix-ambiguous pairs.

Family C: length distribution 2:27%, 3:18%, 4:45%, 5:9%; mean 3.45.
Utterance boundaries fall at 2,4,5,6,7 (DIRECT "zokantel" 2,5;
"zokanatelan" 2,6; NEG "zonukanatel" 2,4,7; REL "zomaratelan" 2,6;
SIZE "zobonatelan" 2,6). The position 3, Family A's dominant
boundary, never occurs as a boundary in Family C. Systematic
prefix ambiguity (7 pairs) and suffix ambiguity (3 pairs) that
Family A lacks.

## Raw-byte trap (adversarial element)

In C-train, "kan" (16x) and "kana" (14x) are always followed by
t-initial shape words, so the boundary bigrams "nt" (~16x) and "at"
(~14x) become more frequent than true intra-word bigrams "em"/"mo"
("temo", 6x) and "lo" ("kalo", 6x). A raw bigram table cannot
distinguish a frequent boundary juncture from a cohesive intra-word
juncture. The 4 DIRECT-T (1,2) test episodes "zokanatemo" place the
true boundary at the frequent "a|t" juncture: a cohesion-maximizing
raw-bigram DP is lured into merging "kana"+"temo" (the merged
segment's average internal bigram score exceeds the split's), while
the learner's lexicon-frequency DP cuts at the true word boundary
because both "kana" and "temo" are in its lexicon. The 2 NEG-T
(1,2) episodes "zonukanatemo" reinforce the trap. This directly
tests the DEVANG3 design requirement: statistics from segmenter
output vs statistics from raw bytes.

## Evaluation

`./devang3 sealc-fresh sealed/sealed_c.txt [variant]` prints per-test
`T 1/0` lines and `SEALC <correct>/20`. K_SEAL needs learner >= 12/20.
Variants learner/c0/c2/c1/c3 are reported for comparison. Determinism:
3/3 byte-identical runs per variant.
