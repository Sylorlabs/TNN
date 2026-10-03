# SEALED_C.md: Fresh sealed Family C (post-freeze adversarial)

Worker: DEVANG3, wave-20261001-2321pdt. Designed from PREREG_DEVANG3.md
section 5 only. Fresh vocabulary and fresh episode selections; the 2021pdt
sealed set is not reused. Sealed package lives in DEVANG3/sealed/. The
sealed file contents were not inspected between generation and the sealed
run; the generator was written from the class spec.

## Files and pre-run sha256 (recorded BEFORE any sealed run)

- `sealed/sealed_c.txt` (header `60 20`, 60 train + 20 test episodes):
  `9f2f944e979fa72efd4c93b0b40b3019730b59a1e852474aa97e1e3f56fff3b8`
- `sealed/genC.zag` (deterministic generator, pure Zag):
  `18abcc422c9dfbcf4ad0d1809e1a5e079a3cbbea6f67960525f6042549e8b78c`
- `sealed/genC` (compiled generator binary; build artifact, not sealed data)

Episode line format (as the sealed interface requires):
`<c0> <s0> <z0> <c1> <s1> <z1> <c2> <s2> <z2> <tgt> <utterance>`,
features in 0..2, tgt in 0..2, utterance [a-z] 1..24 chars.

## Requirement compliance

- 20 novel test episodes (all test utterance forms have 0 occurrences in
  the 60 training episodes; by construction of the episode selections).
- New surface vocabulary, no Family A word forms. Family C words: zom,
  lak, mak, nak, tel, tem, ten, bos, gos, zeva, haro. Intersection with
  {tak,not,red,blu,grn,bal,sph,cub,tri,big,biger,smal} is empty.
- Word lengths 3 to 4: 3-char content words (lak, mak, nak, tel, tem, ten,
  bos, gos, zom), 4-char negator/comparative in fixed positions (zeva,
  haro). The 3-char cold-start bootstrap reliably learns 3-char words;
  2-char words are a documented limitation (prereg section 9) and 5+ char
  words in variable positions are fragile under this segmenter, so the
  family stays within the learnable range while keeping new vocabulary
  and new combinations.
- Prefix pairs sharing >= 2 (3): (tel,tem), (tel,ten), (tem,ten).
- Suffix pairs sharing >= 2 (3): (lak,mak), (lak,nak), (mak,nak).
- Boundary statistics materially different from Family A (attested below).
- Not a trivial Family A variant: new vocabulary, new boundary positions,
  new template selections.

## Semantics (mirrors Family A; adversariality is at the segmentation
level, which is what DEVANG3 claims)

- Objects: color 0/1/2, shape 0/1/2, size 0/1/2. Roles: zom = action
  marker (interpret skips segment 0); lak/mak/nak = colors 0/1/2;
  tel/tem/ten = shapes 0/1/2; bos/gos = sizes 0/1; zeva = negator;
  haro = comparative.
- Templates: DIRECT "zom C S" (target has color C, shape S); NEG
  "zom zeva C S" (target has shape S, not color C); REL "zom haro S"
  (target is the biggest shape-S object); SIZE "zom Z S" (target has
  size Z, shape S).
- Scenes are constructed so the template's scoring gives the target a
  unique maximum. Target index rotates 0,1,2 across repeats.
- Train (60): DIRECT-A 14, DIRECT-B 10, NEG 12, REL 12, SIZE 12.
  Word occurrences in training: zom 60, lak 17, mak 9, nak 10, tel 28,
  tem 22, ten 10, bos 6, gos 6, zeva 12, haro 12. All test words occur
  >= 6 times in training (colors/shapes >= 9).
- Test (20): DIRECT-T 8 on novel combos (2,1) and (1,2); NEG-T 4 on
  novel combos (1,2) and (2,1); REL-T 4 on shape 2 (not in REL training,
  learned via DIRECT); SIZE-T 4 on novel combos (1,2) and (0,2).

## Boundary statistics: Family A vs Family C (attestation)

Family A: 10 of 12 words have length 3 (83%); mean length 3.17.
Utterance boundaries at 3,6,7,8,9 (DIRECT 3,6; NEG 3,6,9; REL 3,8;
SIZE 3,7).

Family C: 9 of 11 words have length 3 (82%), 2 have length 4 (18%);
mean length 3.18. Utterance boundaries at 3,6,7,10 (DIRECT 3,6;
NEG 3,7,10; REL 3,7; SIZE 3,6). The position 10 never occurs in
Family A; positions 8 and 9 never occur in Family C. The boundary
position distribution differs: Family C has 4-word NEG utterances
with boundaries at 3,7,10 (vs Family A NEG at 3,6,9), and no
utterance longer than 13 chars (vs Family A up to 16).

## Evaluation

`./devang3 sealc-fresh sealed/sealed_c.txt [variant]` prints per-test
`T 1/0` lines and a final `SEALC <correct>/20`. K_SEAL needs learner
>= 12/20. Variants learner/c0/c2/c1/c3 are reported for comparison.
Determinism: 3/3 byte-identical runs per variant.
