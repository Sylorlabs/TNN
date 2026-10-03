# SEALED_B.md: Fresh sealed Family B (segmentation ambiguity)

Worker: DEVANG3, wave-20261001-2321pdt. Designed from PREREG_DEVANG3.md
section 5 only. Fresh vocabulary and fresh probes; the 2021pdt sealed set
is not reused. Sealed package lives in DEVANG3/sealed/. The sealed file
contents were not inspected between generation and the sealed run; the
generator was written from the class spec, and the key below is transcribed
from the design notes in genB.zag comments.

## Files and pre-run sha256 (recorded BEFORE any sealed run)

- `sealed/sealed_b.txt` (12 utterances):
  `86925aaec703a39efddc25bf941a1dada200a01c6067e24e6fd039e609a79423`
- `sealed/sealed_b_key.txt` (ground truth, binary output format):
  `9934f8e72a8d5d505a8db30c7b85daa67a776f4ab889e73360b15eb0202ac5e6`
- `sealed/genB.zag` (deterministic generator, pure Zag):
  `fbf05dcc4873239cbb53586da217c8836a4c898b27976bb172d6cce6228efddf`
- `sealed/genB` (compiled generator binary; build artifact, not sealed data)

## Requirement compliance

- 12 utterances, one per line, [a-z], 1..24 chars. Ground-truth boundaries
  in `sealed_b_key.txt` in the binary's own output format
  (`<utt> => <b1>,<b2>,...`, 1-based segment end offsets excluding the
  utterance end). Scoring: exact match of the boundary list.
- Word lengths: 3, 4. Within the required range.
- Prefix pairs sharing >= 2 chars (4, need >= 3): (kir,kira), (tem,tema),
  (tem,temo), (tema,temo).
- Suffix pairs sharing >= 2 chars (3, need >= 3): (kira,tira),
  (kira,mira), (tira,mira), all sharing "ira".

## Vocabulary

Known (Family A anchors): tak, not, blu, grn, bal, cub, tri, big, biger.
Novel: kir, kira, tem, tema, temo, tira, mira.

## Probes (utterance -> true boundaries)

1. takkir -> 3 (tak|kir; novel isolation)
2. notkira -> 3 (not|kira; 4-char novel isolation)
3. blutemtri -> 3,6 (blu|tem|tri; novel between knowns)
4. grntirabal -> 3,7 (grn|tira|bal; 4-char novel, weak left anchor)
5. taktemobal -> 3,7 (tak|temo|bal; tem/temo prefix ambiguity)
6. notmiragrn -> 3,7 (not|mira|grn; suffix ambiguity, weak right anchor)
7. takbigerkira -> 3,8 (tak|biger|kira; big/biger + novel)
8. cubtemtri -> 3,6 (cub|tem|tri)
9. blukirabal -> 3,7 (blu|kira|bal)
10. taktemagrn -> 3,7 (tak|tema|grn; tem/tema prefix ambiguity)
11. notkirbal -> 3,6 (not|kir|bal)
12. grntemocub -> 3,7 (grn|temo|cub; weak left anchor)

8 of 12 probes have a true boundary not at a multiple of 3 (probes
2,4,5,6,7,9,10,12); fixed-width-3 is correct on exactly probes 3, 8, 11
(3/12), so K_ABL has headroom below its <= 5/12 ceiling.

## Scoring

`./devang3 segb sealed/sealed_b.txt` output lines are diffed against
`sealed_b_key.txt`. A probe passes iff its output line equals the key
line exactly. K_SEG needs >= 9/12. K_ABL needs the `segb-abl` variant at
<= 5/12 (and < 9/12).
