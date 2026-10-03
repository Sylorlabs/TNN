# SUBSTRATE INTEGRATION RESULT

Worker: I2, Substrate Integration Worker.
Date: 2026-09-30.

## Verdict: SUBSTRATE-INTEGRATED

All 3 frozen kill bars pass.

## Commits (local, tnn-native-lab, owned path only)

- Prereg: `5420e7a7a` (committed alone before any implementation).
- Implementation + result: this commit.
- Commit order verified: prereg strictly precedes implementation
  (git merge-base --is-ancestor).

## What was tested

The shared substrate (SUBSTRATE-PROTOTYPED, 2835e5641) was tested
against the merged curriculum's experience stream:

1. S1/S2 replay: all 18 utterances from Step E's s1_ep/s2_ep
   (bikgup, gupzol, bikguptav, zolbik, tavgupbik, bikgupzol,
   guptav, bikgup, zoltav, tavbikgup, gupzoltav, bikgup,
   zolgupbik, tavzoltav, gupbikzol, biktav, zolgup, tavgupzol)
   segmented by fixed-width-3 (all true morphemes are length 3;
   all utterances are exact concatenations). 45 morphemes fed as
   substrate fact triples: (morph,"lenclass","L3") and
   (morph,"initbyte",X).
2. Concept formation implemented in Zag USING substrate facts,
   mirroring Step E's con_form: group by (lenclass, initbyte);
   per concept store (cN,"feat_len",L), (cN,"feat_init",X),
   (cN,"member",morph).
3. Causal phase: the 5 substrate-prototype episodes (SETX/WAIT)
   recorded via sub_episode and processed via sub_causal_update
   on the SAME workspace, in the SAME run, after concept
   formation.

## Kill bar verdicts

- K1 (curriculum loaded, concepts formed): PASS. 45 morphemes fed.
  concept_count == 4, verified via substrate fact queries (not
  just Zag-side state). Member sets: {bik}, {gup}, {zol}, {tav},
  matching Step E's S3-FDCR-CONCEPTS 4 exactly. Feature initbytes
  {b,g,z,t} distinct.
- K2 (causal AND concepts maintained): PASS. After 5 causal
  episodes + sub_causal_update: concept_count still 4, member
  sets identical (C2 == C1, verified via substrate queries).
  All 4 prototype causal queries correct: (110)WAIT->(111),
  (100)WAIT->(110), (000)WAIT->(000), (000)SETX->(100).
  Morpheme fact queries correct: (bik,lenclass)->"L3",
  (tav,initbyte)->"t".
- K3 (purity): PASS. Pure Zag at every stage (source, znc build,
  execution). Zero Python invocations. Zero em-dash bytes
  (byte-checked). 3/3 byte-identical runs, md5
  de77d07d6a29032bf7839f0e967e9e58, exit 0, zero stderr.

## Comparison: substrate vs original

| Aspect | Step E (merged curriculum) | Substrate |
|---|---|---|
| Concepts formed | 4 (S3-FDCR-CONCEPTS 4) | 4, identical members |
| Concept features | (lenclass, initbyte) | (lenclass, initbyte) |
| Morpheme feed | S1/S2 utterances via DEVINT1 segmentation | S1/S2 utterances, fixed-width-3 |
| Causal episodes | Not supported (DEVINT1 has no causal store) | 5 episodes, 6 entries, queries correct |
| Workspace | DEVINT1 16384B + FDCR at 14336 | One 32768B, nvar runtime |
| Fact count | N/A (FDCR store) | 143 facts |

The substrate hosts the same declarative cognitive state (4
concepts, morpheme features) AND causal learning on one
workspace. DEVINT1 cannot do the causal half; the substrate can
do both.

## Honest limitations (not hidden)

- S1/S2 segmentation used fixed-width-3, not DEVINT1's DP
  segmenter. Justified: all S1/S2 utterances are exact
  concatenations of length-3 morphemes. This tests
  representational hosting, not segmentation.
- S4-S11 declarative products (bigram rules, procedures,
  contradictions, inquiry, revision, memory pressure) were NOT
  replayed. They require mechanisms beyond the substrate's
  fact/causal representation. This is a representational
  limitation of the substrate as currently specified.
- Concept formation logic (grouping) is Zag code operating ON
  substrate facts, not derived BY the substrate. The substrate
  provides persistent state; the FORM/MERGE computation is
  still researcher-authored mechanism.
- Effect vocabulary remains UNCH/SET only (inherited from
  substrate prototype).

## Files

- PREREG_SUBSTRATE_INTEG.md (frozen prereg)
- substrate_integ.zag (implementation: substrate core verbatim +
  curriculum replay)
- integ_additions.zag (the appended curriculum-replay code)
- SI_RESULT.md (this file)
- SI_RAW_1.txt, SI_RAW_2.txt, SI_RAW_3.txt (3/3 byte-identical)

## Purity

Pure Zag at every stage. No Python invoked. Zero em-dash bytes
in all committed files. Commits local on tnn-native-lab; nothing
pushed.
