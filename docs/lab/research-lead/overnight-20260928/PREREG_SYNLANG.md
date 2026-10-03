# PREREG H-SYNLANG: Synthetic Language Learning Test

**Status:** FROZEN. This prereg strictly precedes implementation.
**Date:** 2026-09-29
**Author:** Synthetic Language Researcher (subagent)

## Background

No TNN mechanism has attempted language-like sequential learning. All
current mechanisms work on structured I/O pairs (procedure learner),
state/action episodes (causal learner), or pre-segmented feature triples
(FDCR). Micah's directive lists "synthetic language" as part of the
continuing learner requirements. This is a completely unattempted frontier.

The honest question: can the current mechanisms be adapted to learn a
minimal synthetic language, or is a new architecture needed? This prereg
designs the test. If the mechanisms cannot handle it, the exact failure
mode is the finding.

## Hypothesis H-SYNLANG

FDCR's concept formation and sibling inference can learn a minimal
synthetic language with compositional semantics: novel word combinations
not seen in training are correctly interpreted via sibling inference,
and a novel word introduced with minimal examples is productively used
in novel combinations.

## Synthetic language design

**Vocabulary (10 words):**
- Colors: red, blue, green
- Shapes: block, ball
- Sizes: big, small
- Novel (few-shot): yellow, cube

**Grammar:** [size] [color] [shape]
All three slots optional except shape. Examples: "block", "red block",
"big red block", "small blue ball".

**Semantics:** Each description refers to an object. The meaning is the
conjunction of slot values. "big red block" = object with
size=big AND color=red AND shape=block.

## Fixture: synlang.txt (fresh vocabulary, sl_ prefix)

No vocabulary overlaps existing fixtures. All subjects use sl_ prefix.
All relations use sl_ prefix. This prevents accidental transfer from
prior training.

### Training: 8 descriptions (cover all slots, leave gaps)

```
T sl_d1 | sl_size | big
T sl_d1 | sl_color | red
T sl_d1 | sl_shape | block
T sl_d1 | sl_ref | obj1

T sl_d2 | sl_size | small
T sl_d2 | sl_color | red
T sl_d2 | sl_shape | block
T sl_d2 | sl_ref | obj2

T sl_d3 | sl_size | big
T sl_d3 | sl_color | blue
T sl_d3 | sl_shape | block
T sl_d3 | sl_ref | obj3

T sl_d4 | sl_size | small
T sl_d4 | sl_color | blue
T sl_d4 | sl_shape | ball
T sl_d4 | sl_ref | obj4

T sl_d5 | sl_color | green
T sl_d5 | sl_shape | block
T sl_d5 | sl_ref | obj5

T sl_d6 | sl_color | green
T sl_d6 | sl_shape | ball
T sl_d6 | sl_ref | obj6

T sl_d7 | sl_size | big
T sl_d7 | sl_shape | ball
T sl_d7 | sl_ref | obj7

T sl_d8 | sl_size | small
T sl_d8 | sl_shape | block
T sl_d8 | sl_ref | obj8
PHASE
```

Training covers: each color appears, each shape appears, each size
appears. But NOT all combinations. Specifically missing:
- small + blue + block (novel combination)
- big + green + ball (novel combination)
- red + ball (novel combination)

### Test Phase 1: Compositional generalization (K-S1)

```
Q SL1 sl_q1 | sl_size | small
Q SL1 sl_q1 | sl_color | blue
Q SL1 sl_q1 | sl_shape | block
```

sl_q1 is a new description with small+blue+block. This exact combination
was never taught. The learner must compose: small (from sl_d2, sl_d4,
sl_d8), blue (from sl_d3, sl_d4), block (from sl_d1, sl_d2, sl_d3, sl_d5,
sl_d8).

Predicted: The concept system recruits a parent from shared features
and sibling inference derives the referent. The exact predicted referent
depends on the induced hierarchy; what matters is that the answer comes
via sibling inference (sib marker, ans_kind=3), not Step-0 lookup.

**Critical:** A grep check must confirm no T line teaches
(sl_q1, sl_ref, *). Step-0 provably misses.

```
Q SL1 sl_q2 | sl_size | big
Q SL1 sl_q2 | sl_color | green
Q SL1 sl_q2 | sl_shape | ball
```

sl_q2 = big+green+ball. Never taught. Same prediction.

### Test Phase 2: Few-shot novel word (K-S2)

Teach the novel word "yellow" with TWO examples (in the test phase,
before the query):

```
T sl_y1 | sl_color | yellow
T sl_y1 | sl_shape | block
T sl_y1 | sl_ref | obj9

T sl_y2 | sl_color | yellow
T sl_y2 | sl_shape | ball
T sl_y2 | sl_ref | obj10
PHASE
Q SL2 sl_q3 | sl_size | big
Q SL2 sl_q3 | sl_color | yellow
Q SL2 sl_q3 | sl_shape | block
```

sl_q3 = big+yellow+block. The word "yellow" was seen only twice, in
different shapes. The combination big+yellow+block is novel.

Predicted: sibling inference composes big (from training) with yellow
(from the two few-shot examples) to answer via sib marker.

### Test Phase 3: Raw sequence handling (documented failure expected)

This phase does NOT use FDCR. It tests whether the procedure learner
can handle raw sequential input:

Input pairs for proc_learn:
```
("red block" -> "obj_red_block")
("blue ball" -> "obj_blue_ball")
```

The procedure learner will attempt character-level index mapping.
Expected: it either finds a spurious program or returns VACUOUS/NO
PROGRAM. This documents the exact failure mode: the procedure learner
has no notion of word boundaries or semantic composition.

This phase is exploratory and does not affect the kill verdict. It is
included to document WHY a new architecture may be needed, with
evidence rather than assertion.

## Kill bars (frozen)

- K-S1 (compositional generalization, 2/2): Both SL1 probes (sl_q1,
  sl_q2) are answered AND carry the sib marker (ans_kind=3), proving
  Step-0 direct lookup did not answer them. A grep check confirms no T
  line teaches the queried (subject, sl_ref) pair.
- K-S2 (few-shot novel word, 1/1): The SL2 probe (sl_q3) is answered
  AND carries the sib marker. The novel word "yellow" appears in only
  2 T lines before the query.
- K-S3 (determinism): Three consecutive runs of synlang.txt produce
  byte-identical stdout (cmp-verified).

## What kills H-SYNLANG

- Any SL1/SL2 probe lacks the sib marker (answered by Step-0, i.e.,
  the probe is confounded): K-S1 or K-S2 FAIL, H-SYNLANG KILLED.
- Any probe answers incorrectly or WITHHOLDs: K-S1 or K-S2 FAIL,
  H-SYNLANG KILLED.
- Non-deterministic output: K-S3 FAIL, H-SYNLANG KILLED.

## Honest failure modes (documented, not hidden)

1. If FDCR cannot form the needed concepts (e.g., the hierarchy does
   not support cross-cutting compositional inference), the specific
   structural reason is documented. This motivates new concept
   formation machinery.

2. If the sib marker appears but the answer is wrong, the inference
   procedure's compositional limits are documented.

3. Phase 3 (procedure learner on raw sequences) is expected to fail.
   The exact output (spurious program, VACUOUS, or NO PROGRAM) is
   documented as evidence for why sequence handling needs a new
   mechanism.

4. The pre-segmentation gap: this test supplies word boundaries and
   slot assignments (sl_size, sl_color, sl_shape). No current mechanism
   learns segmentation from raw sequences. This is documented as the
   fundamental architectural gap, even if K-S1 and K-S2 pass.

## Scope

Bounded to FDCR's concept formation and sibling inference on
pre-segmented synthetic descriptions. Does not claim language learning
in the full sense (no segmentation learning, no word order sensitivity,
no recursion). Does not claim L3. Success shows compositional
generalization within the feature-based architecture; the
pre-segmentation gap remains the primary open problem.

## Prereg commit ordering

This file is committed before any fixture or result. The fixture
(synlang.txt) and result (RESULT_SYNLANG.md) come in later commits.
