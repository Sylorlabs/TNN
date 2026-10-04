# REPORT: Grammar Encoding-Detection Worker

## Verdict: GRAMMAR-ENCODE-COMPLETE (with fail-closed proof)

## Claim tested

The third-system report (commit ee621a50d) proved the induction
machinery goes SILENTLY WRONG when the pair encoding breaks: on EXL3
(world P(a,b) = a*8+b vs the machinery's assumed a*16+b) it induced a
confident wrong grammar (a=[0,3], b=[0,15]) and reported 4/4 valid, with
no alarm anywhere. This worker implements the diagnosed repair: a
decode-consistency guard that makes induction fail closed on encoding
mismatch instead of writing a wrong grammar.

## Guard design (implemented, unfrozen)

`gi_codec_check`, called inside `gi_induce` after part-2 range induction
and before the type-70 grammar node is written. It performs a semantic
round-trip of the assumed codec against the observed fact structure:
for every taught eval fact (r in {41,42}, the eval ops the verification
lookup assumes: SUB=41, DIV=42), the subject is a pair P and the object
is the taught value t; decode P under the assumed codec to (a,b) and
require the op the relation names to reproduce t (41: a-b==t; 42: b>0,
a-(a/b)*b==0, a/b==t). A violation refuses induction with diagnostic
code -3 and writes nothing.

The check is general: it names no divisor except the machinery's own
assumed codec, and the discriminator comes from the fact stream, not
from a hardcoded list of broken encodings. The DIV facts with b=1 pin
the decoded components to the true ones on the observed support, so a
wrong codec cannot pass it.

A pure pair-set round-trip (re-encode the induced rectangle, require
every grid point to be observed) was tried during implementation and
REJECTED: it false-refused the EXL2 control, because real worlds teach
only constraint-satisfying pairs (EXL2 never teaches pair (1,2): SUB
1-2<0, DIV 1/2 inexact, so grid point 18 is legitimately absent). The
rectangle is the wrong unit; the op semantics are the load-bearing
cross-check. This rejection was recorded transparently as Amendment A1
to the prereg and re-frozen before the verdict runs; the -2 diagnostic
was retired with it.

## Machinery identity

- e4_base.zag SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
  identical to grammar_third/g3_base.zag (2 files share the digest).
- e4_patch.zag: stripping the added gi_codec_check function leaves a
  file whose diff against grammar_third/g3_patch.zag is exactly two
  hunks: the gi_induce doc comment (new return codes) and the 4-line
  guard call. All five /16 decode sites (g3 lines 53, 89, 174, 210,
  250) are byte-identical in e4_patch.zag. Zero logic changes outside
  the guard.
- Driver: teaching sections for EXL2 (literals 0..9, P=a*16+b, from
  gt_driver) and EXL3 (literals 0..7, P=a*8+b, from g3_driver) are
  renames of the frozen teachers; EXL4 (literals 0..3, P=a*32+b) is new.
  Arm functions follow the frozen pattern.

## Results (3/3 byte-identical, SHA-256 8aa84d50...)

```
GI-WORLD EXL2
GI-INDUCED 1
GI-EXPECT 1
GI-MATCH 1
GI-GRAMMAR nbuild=4 nlic=2 lic=44,43 a=[0,9] b=[0,9] maxlinks=1
GI-I-VALID 6/6
GI-WORLD EXL3
GI-INDUCED -3
GI-EXPECT -3
GI-MATCH 1
GI-GRAMMAR none
GI-I-NOGRAMMAR
GI-WORLD EXL4
GI-INDUCED -3
GI-EXPECT -3
GI-MATCH 1
GI-GRAMMAR none
GI-I-NOGRAMMAR
GI-VERDICT 3/3
```

Against the re-frozen prereg (Amendment A1):

1. EXL2 (correct encoding): GI-INDUCED 1, correct ranges a=[0,9]
   b=[0,9], battery 6/6 valid. No false refusal. PASS.
2. EXL3 (broken /8 encoding): GI-INDUCED -3 (codec op-consistency
   diagnostic). No type-70 node written (GI-GRAMMAR none). The induce
   arm prints GI-I-NOGRAMMAR and builds nothing: fail-closed, where the
   unguarded machinery previously induced the confident wrong grammar.
   PASS.
3. EXL4 (new broken encoding, sparse stride P=a*32+b on 0..3):
   GI-INDUCED -3. No grammar node, no construction. The same general
   check catches a second, structurally different encoding break with
   no encoding-specific logic. PASS.
4. Determinism: 3/3 runs byte-identical. PASS.

## Why the refusal is correct (hand verification)

- EXL3: the first eval fact contradicting the /16 codec is (8,41,1)
  (world pair (1,0), SUB value 1). Decoded under /16: (0,8);
  0-8 = -8 != 1. The codec contradicts the world's own taught
  semantics, so the induced ranges a=[0,3], b=[0,15] are refused before
  they can enter learner state.
- EXL4: the first contradicting fact is (32,41,1) (world pair (1,0),
  SUB value 1). Decoded under /16: (2,0); 2-0 = 2 != 1. Refused.
- EXL2: every eval fact decodes to its true components (the codec is
  correct), so all op checks pass and induction proceeds exactly as in
  the frozen transfer run.

## What changed vs the silent-wrong outcome

Before: gi_induce returned 1 on EXL3 and wrote a=[0,3], b=[0,15] with
full confidence; the battery's 4/4 masked the breakage end to end.
After: gi_induce returns -3 on EXL3 and EXL4, writes nothing, and the
refusal is observable in the output (GI-INDUCED -3, GI-GRAMMAR none,
GI-I-NOGRAMMAR). The wrong grammar can no longer enter learner state
silently. The vacuous part-1 sanity check is untouched (still
tautological); the guard is the real check, placed where the
third-system report said fail-closed had to happen: between range
induction and the grammar write.

## Metrics

- Cognition lines added: guard function (49 lines with comments) plus
  4-line call site in the unfrozen patch; 0 to base (byte copy).
- Modes/bridges/handlers: 0. New semantic cases: 0. The guard is a
  plain function, not a mode. Base modifications: 0.
- Frozen dirs untouched (grammar_third, grammar_transfer read-only).
- Determinism: 3/3 byte-identical runs
  (SHA-256 8aa84d504dc5639f78f5557f8a787c34a90eaa6853c78bfeead0982c47df0004
  recorded in full in the run files).
- Toolchain: safebin active, `which python3 python` empty, pure Zag;
  no forbidden executable invoked.

## Follow-ups (not started)

1. The guard currently refuses; a further step would be codec
   induction (per the third-system report's minimal-change diagnosis),
   promoting the codec to induced grammar state. Refusal is the honest
   behavior until that exists.
2. Remaining untested assumption breaks from the third-system report
   are still open: 3 genuine licensors vs nlic<=2, literals beyond 0..9
   vs the rubric range, ternary operators.
3. Audit other sanity checks for the tautology pattern (a guard that
   cannot fire is a comment, not a guard).
