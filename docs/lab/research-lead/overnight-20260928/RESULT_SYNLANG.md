# RESULT H-SYNLANG: Synthetic Language Test KILLED (0/3)

**Prereg:** PREREG_SYNLANG.md (commit 2d8d53dee, frozen before implementation)
**Date:** 2026-09-29
**Verdict:** H-SYNLANG KILLED. All kill bars FAIL.

## Summary

FDCR was tested on a minimal synthetic language (10 words, [size][color][shape]
grammar, compositional semantics). The test failed, but the failure is
informative: it reveals a fundamental architectural gap, not a bug in FDCR.

**Kill bar results:**
- K-S1 (compositional generalization): FAIL 0/2. sl_q1 WITHHOLDs (correctly,
  sibling disagreement on referent). sl_q2 answers obj6 via sib marker, but
  the expected value objN is undefined (no correct referent exists for novel
  combinations).
- K-S2 (few-shot novel word): FAIL 0/1. sl_q3 WITHHOLDs (sibling disagreement
  on referent between obj9, obj1, obj3).
- K-S3 (determinism): PASS. Three runs byte-identical (cmp-verified).

## What the results show

### FDCR behaves correctly

The WITHHOLDs are CORRECT behavior, not failures of the mechanism:
- sl_q1 (small+blue+block): Siblings sl_d2 (→obj2), sl_d3 (→obj3), sl_d8 (→obj8)
  disagree on sl_ref. WITHHOLD is the right answer under conflicting evidence.
- sl_q3 (big+yellow+block): Siblings sl_y1 (→obj9), sl_d1 (→obj1), sl_d3 (→obj3)
  disagree. WITHHOLD is correct.
- sl_q2 (big+green+ball): Answered obj6 via sibling inference (sib marker).
  Sibling sl_d6 (green+ball→obj6) provided the answer. This is the mechanism
  working as designed.

Step-0 miss verified: grep confirms 0 T lines teach (sl_q1|sl_q2|sl_q3, sl_ref).
The sib marker on sl_q2 proves sibling inference was used, not direct lookup.

### The design flaw: atomic referents cannot support composition

The prereg defined the task as "given a description, output the object ID."
But object IDs (obj1, obj2...) are ATOMIC. There is no compositional structure
to derive "the referent of small+blue+block" from the referents of its parts.

For compositional generalization to be testable, the semantic space must itself
be compositional. Options:
1. The "meaning" is the feature bundle (but then the task is trivial: the
   features ARE the description).
2. Objects are defined compositionally (but then novel combinations need
   novel objects, which FDCR cannot invent).

The prereg's expected value "objN" was undefined because no such object exists
in the training data. This is a design flaw, not a mechanism failure.

### The pre-segmentation gap (fundamental)

This test supplied word boundaries and slot assignments:
- "small blue block" was pre-segmented into sl_size=small, sl_color=blue,
  sl_shape=block.
- No TNN mechanism learns segmentation from raw sequences.

The procedure learner (proc_learn.zag) cannot fill this gap:
- `extract_seq` requires output characters to appear in the input string.
- For ("red block" → "obj1"), 'o' is not in "red block", so extraction
  returns VACUOUS (-1).
- Even for overlapping strings, it learns POSITIONAL mappings P(k,n),
  not semantic ones. It has no notion of word boundaries or meaning.

The causal learner cannot fill this gap:
- It operates on fixed 3-variable states, not variable-length sequences.
- There is no mechanism for segmenting "small blue block" into words.

FDCR cannot fill this gap:
- It operates on pre-segmented (subject, relation, value) triples.
- The relations sl_size, sl_color, sl_shape were supplied by the researcher.

**Conclusion:** No current TNN mechanism learns synthetic language from raw
sequential exposure. The pre-segmentation step (sequence → words → slots)
is entirely researcher-supplied. This is the primary architectural gap.

## Phase 3: Procedure learner on raw sequences (documented)

Code analysis of proc_learn.zag (frozen historical file, not modified):

`extract_seq(inp, out, seq)`:
- For each output character c at position k, finds c in inp.
- Requires EXACTLY ONE occurrence (cnt==1), else returns -1 (VACUOUS).
- For ("red block" → "obj1"): 'o' not in "red block" → VACUOUS.
- For ("abc" → "cba"): finds positions, learns P(k,n)=n-1-k.

The procedure learner is a STRING TRANSDUCER, not a semantic mapper. It
cannot learn that "red" MEANS color=red because:
1. It has no semantic representation (only character positions).
2. It requires character overlap between input and output.
3. It learns index functions, not meaning functions.

This confirms the architectural gap with evidence from the source code.

## Classification

H-SYNLANG KILLED by design flaw (atomic referents) revealing a fundamental
gap (no sequence segmentation learning). FDCR itself behaved correctly
(WITHHOLD on conflict, sib inference on consensus). This is a negative
result that maps the boundary: current mechanisms handle pre-segmented
features but cannot learn language from raw sequences.

Not L3. Not a mechanism failure. An architectural gap documentation.

## What would be needed

A synthetic language learner would require:
1. **Segmentation**: Raw sequence → word boundaries (unattempted).
2. **Slot assignment**: Words → semantic roles (unattempted).
3. **Compositional semantics**: Phrase meaning from word meanings
   (FDCR does this for pre-segmented features, but not from sequences).
4. **Novel referent handling**: What IS the meaning of a novel combination?
   (Requires a compositional semantic space, not atomic IDs).

These are open research questions, not engineering tasks.

## Commits

- Prereg: 2d8d53dee
- Fixture + result + raw output: (this commit)

## Files

- docs/lab/research-lead/overnight-20260928/PREREG_SYNLANG.md
- docs/lab/research-lead/overnight-20260928/synlang.txt
- docs/lab/research-lead/overnight-20260928/RESULT_SYNLANG.md
- docs/lab/research-lead/overnight-20260928/SYNLANG_RAW_OUTPUT.txt

## Governance

Pure Zag throughout. No Python used at any stage. Prereg 2d8d53dee strictly
precedes implementation. No em dashes in documentation.
