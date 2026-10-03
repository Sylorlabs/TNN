# SEALED_B.md: Sealed Family B (segmentation ambiguity)

Adversary: DEVANG3-ADVERSARY, wave-20261001-2021pdt. Designed post-freeze
from PREREG_DEVANG3.md section 5 requirements only. The builder's dev files
were not inspected. Sealed package lives in DEVANG3/sealed/; the builder
never reads it.

## Files and pre-run sha256 (recorded BEFORE any sealed run)

- `sealed/sealed_b.txt`:
  `901d433d30df6b65884a8e2b81171eb3d4f093969dea9178493c373f25e77e7c`
- `sealed/sealed_b_key.txt`:
  `e599237e006442665da16d96497d5d8be3c578f7ef0100d08dfcd26509c315c1`

## Requirement compliance

- 12 utterances, one per line, [a-z], 1..24 chars. Ground-truth boundaries
  committed in `sealed_b_key.txt` in the binary's own output format
  (`<utt> => <b1>,<b2>,...`, 1-based segment end offsets excluding the
  utterance end). Scoring: exact match of the boundary list.
- Word lengths: 2, 3, 4, 5. All lie in the required range 2 to 6.
- Prefix pairs sharing >= 2 chars (5, need >= 3): (ka,kan), (ka,kala),
  (kan,kala), (tem,tema), (big,biger).
- Suffix pairs sharing >= 2 chars (3, need >= 3): (kala,mala),
  (kala,sala), (mala,sala), all sharing "ala".

## Vocabulary

Known (in the Family A-trained lexicon, frequent): tak, not, red, blu, grn,
bal, cub, tri, big, biger, smal.
Novel (synthetic, adversary-designed): ka, kan, kala, mala, sala, tem, tema.
No novel word contains a Family A word as a substring (this is deliberate;
see design note 3).

## Probes (utterance -> true boundaries)

1. takbiger -> 3            (tak|biger; big/biger prefix ambiguity)
2. takbigertri -> 3,8       (tak|biger|tri)
3. taksmaltri -> 3,7        (tak|smal|tri)
4. notredbal -> 3,6         (not|red|bal)
5. takkanatri -> 3,7        (tak|kana|tri; novel word isolated)
6. blumalagrn -> 3,7        (blu|mala|grn; novel word isolated)
7. taktemcub -> 3,6         (tak|tem|cub; novel word isolated)
8. grnsalabal -> 3,7        (grn|sala|bal; novel word isolated)
9. takbigerkala -> 3,8      (tak|biger|kala; big/biger + novel isolation)
10. cubkantri -> 3,6        (cub|kan|tri; novel word isolated)
11. takkalatri -> 3,7       (tak|kala|tri; novel word isolated)
12. nottemagrn -> 3,7       (not|tema|grn; novel word isolated)

8 of 12 probes have a true boundary not at a multiple of 3 (probes
2,3,5,6,8,9,11,12); fixed-width-3 is correct on exactly probes 4, 7, 10
(3/12), so K_ABL has headroom below its <= 5/12 ceiling.

## Design notes (adversary reasoning, for the record)

1. The genuine ambiguities the DP must resolve: the big/biger prefix
   overlap (resolved by lexicon frequency: a frequent "biger" beats
   "big" plus a novel "er"), and isolation of a single novel word
   flanked by known words (the DP's known-word preference cuts the
   known words out, leaving the novel word; merging or shattering the
   novel region always loses to the true parse under the frozen
   scoring).
2. Why not an all-novel vocabulary: from the frozen source, a novel
   segment [j,i) scores -50+ilog(L+1)*5, and splitting a novel region
   into k>1 novel segments can never beat one merged segment (the
   -50 per segment dominates the logarithmic length term; max gain
   ~3*5=15 < 50). A fully-novel utterance is therefore always emitted
   as one segment. An all-novel Family B would score 0/12 for ANY
   lexicon-frequency segmenter and would test the new-word prior,
   not segmentation quality. The probes above keep the test a valid
   measure of segmentation quality on ambiguous inputs.
3. Novel words were chosen to contain no Family A word as a substring,
   so the DP cannot shatter them into a known word plus a fragment
   (which would be a scoring pathology, not a segmentation error).
   The prefix/suffix pairs among novel words are vocabulary properties
   per the prereg; the live ambiguities are big/biger and the
   novel-word isolations.
4. No probe forms an accidental known word across a true boundary
   (checked by inspection of all cross-boundary substrings).

## Scoring

`./devang3 segb sealed/sealed_b.txt` output lines are diffed against
`sealed_b_key.txt`. A probe passes iff its output line equals the key
line exactly. K_SEG needs >= 9/12. K_ABL (task operationalization)
needs the `segb-abl` variant at < 9/12; the prereg's Family B leg
needs <= 5/12.
