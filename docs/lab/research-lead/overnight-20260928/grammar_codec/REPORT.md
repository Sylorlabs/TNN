# REPORT: Grammar Codec Induction Worker

## Verdict: GRAMMAR-CODEC-COMPLETE (with per-system divisor table)

## Claim tested

The third-system report (commit ee621a50d) diagnosed the minimal repair
for the silent-wrong bug: promote the pair codec from hardcoded
constant to induced grammar state (new type-70 field), induce the
divisor in gi_induce, thread it through all five decode sites, and
replace the tautological check with a real cross-fact consistency
check. The encoding-detection worker (commit df668fa20,
GRAMMAR-ENCODE-COMPLETE) built the honest interim guard (refuse -3 on
op-semantic mismatch under the assumed /16 codec) and left codec
induction as the deeper fix. This worker implements the induction: from
the taught fact stream, induce the divisor D such that P(a,b) = a*D+b,
store it in the type-70 grammar node, thread it through every decode
site, and refuse fail-closed when D is contradicted or genuinely
ambiguous.

## Induction design (implemented, unfrozen)

`gi_codec_induce`, called inside `gi_induce` after licensor discovery
and before range induction. The discriminator is literal co-occurrence
structure, never re-encoding:

- SUB eval fact (P,41,t): P+t = a*(D+1).
- DSUB decomp fact (t,43,P): P+t = a*(D+1).
- DIV eval fact (P,42,1): P = b*(D+1) (unit quotient).
- DDIV decomp fact (1,44,P): P = b*(D+1).

Let g = gcd of the positive members of this set. The true D+1 divides
g, so the candidates d = v-1 for v|g, v>=2 are derived from the observed
g by exact integer arithmetic. No divisor candidate is hardcoded or
selected from a fixed list. Each candidate is tested by the
op-consistency check (decode under d, require the named op to reproduce
t on every eval fact). Exactly one consistent divisor is induced;
zero consistent means contradicted (-3); two or more means genuinely
ambiguous (-4). On any non-1 return nothing is written.

The type-70 node gains the codec as induced grammar state. Nodes are
40 bytes with no free slot (frozen base untouched), so field 4 packs
nlic and D as field4 = nlic + 4*D (nlic<4 always by the nlic<=2 guard;
the stride 4 is 2^2 bits, not a codec divisor). `gi_grammar_read`
exposes D at buf[32]; the GI-GRAMMAR line prints it.

The five decode sites: (1) the part-1 decode + sanity check is DELETED
as diagnosed vacuous (a*D+b==P is a tautology under any fixed divisor);
its replacement is `gi_codec_induce` itself, the real cross-fact check.
(2) part-2 range induction decodes under D. (3) `gi_trial_build2`
decodes under D from the grammar buffer. (4) `gi_hardcode_build` takes
D as a parameter (hardcoding /16 there would re-test the diagnosed
broken assumption). (5) `gi_classify` takes D as a parameter.

## Machinery identity

- c_base.zag SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
  identical to grammar_encode/e4_base.zag (byte copy, never edited).
- c_patch.zag: the old `gi_codec_check` guard is removed, subsumed by
  the per-candidate op check. `grep "/16\|\*16"` on the patch returns
  only two comment lines; no codec divisor literal appears in machinery
  logic (remaining 8/16/32 matches are node field offsets, buffer
  sizes, and the pre-existing nlic<16 capacity bound).
- Drivers: EXL2/EXL3/EXL4 teachers are renames of the e4 teachers;
  NEG-AMB (diagonal-only D=8 world) and NEG-SHIFT (codec shift at a=5)
  teachers are new.

## Results (3/3 byte-identical, SHA-256 173a69f1...)

```
GI-WORLD EXL2
GI-INDUCED 1
GI-GRAMMAR nbuild=4 nlic=2 lic=44,43 D=16 a=[0,9] b=[0,9] maxlinks=1
GI-I-VALID 6/6
GI-B-VALID 0/6
GI-H-VALID 6/6
GI-WORLD EXL3
GI-INDUCED 1
GI-GRAMMAR nbuild=4 nlic=2 lic=44,43 D=8 a=[0,7] b=[0,7] maxlinks=1
GI-I-VALID 4/4
GI-B-VALID 0/4
GI-H-VALID 4/4
GI-WORLD EXL4
GI-INDUCED 1
GI-GRAMMAR nbuild=2 nlic=2 lic=44,43 D=32 a=[0,3] b=[0,3] maxlinks=1
GI-I-VALID 2/2
GI-B-VALID 0/2
GI-H-VALID 2/2
GI-WORLD NEG-AMB
GI-INDUCED -4
GI-GRAMMAR none
GI-I-NOGRAMMAR
GI-WORLD NEG-SHIFT
GI-INDUCED -3
GI-GRAMMAR none
GI-I-NOGRAMMAR
GI-VERDICT 5/5
```

Per-system divisor table: EXL2:16, EXL3:8, EXL4:32, NEG-AMB:refused
(ambiguous), NEG-SHIFT:refused (contradicted).

## Why each outcome is correct (hand verification)

- EXL2: S multiples of 17 (SUB (1,0): P+t=17); g=17 prime, sole
  candidate d=16, op check passes. D=16, ranges [0,9]/[0,9]. Battery
  6/6 class 1; every answer hand-checked under a*16+b (e.g. t=9,
  ans=144: (9,0), 9-0=9).
- EXL3: S multiples of 9; g=9; candidates {2,8}; d=2 killed by
  (8,41,1) decoding to (4,0), 4!=1; d=8 consistent. D=8, true ranges
  a=[0,7] b=[0,7]. This is the world that went silently wrong under
  hardcoded /16 (induced a=[0,3], b=[0,15]); the machinery now induces
  the true codec and true ranges, and the battery's 4/4 answers match
  the third-system report's hand-verified table (t=0 ans=9 (1,1),
  t=2 ans=16 (2,0), t=4 ans=32 (4,0), t=6 ans=48 (6,0)).
- EXL4: S multiples of 33 (SUB (1,0): P+t=33; DIV (1,1): P=33);
  g=33; candidates {2,10,32}; d=2 killed by (32,41,1)->(16,0);
  d=10 killed by DIV (65,42,2)->(6,5), 6/5 inexact; d=32 consistent.
  D=32, ranges [0,3]/[0,3]. Battery 2/2 (t=0 ans=33 (1,1), t=2
  ans=64 (2,0)).
- NEG-AMB: S={18,36,54}, g=18; candidates {1,2,5,8,17}; d=1,2,5
  killed by the op check; d=8 consistent (components {2,4,6}) AND
  d=17 consistent (components {1,2,3}: (18,41,0)->(1,1),
  (36,41,0)->(2,2), (54,41,0)->(3,3), DIV facts exact). Two consistent
  divisors: genuinely unidentifiable, refused -4 with nothing written.
  Picking either would be silent-wrong in a new form.
- NEG-SHIFT: S contains 17 (a=1 SUB) and 45 (a=5 SUB), g=1: no valid
  divisor exists. Refused -3, nothing written.

Ablate arms (0/6, 0/4, 0/2, class 2 throughout): the induced grammar,
including its divisor field, is load-bearing for construction; the
failure mode matches the prior controls. Hardcode arms match the
induce arms exactly (6/6, 4/4, 2/2), now with the induced codec instead
of the fragile hardcoded /16.

## Kill-bar audit

- K1: 3/3 byte-identical (173a69f1...). PASS.
- K2: GI-MATCH 1 on all five worlds; divisors exactly 16/8/32; ranges
  exactly [0,9]/[0,7]/[0,3] for a and b. PASS.
- K3: no hardcoded divisor candidate in the machinery (grep evidence
  above; candidates derive only from divisors of the observed gcd).
  PASS.
- K4: NEG-AMB -4 and NEG-SHIFT -3, GI-GRAMMAR none in both (observable
  refusal, nothing enters learner state). PASS.
- K5: ablate arms 0 valid on all three main worlds. PASS.
- K6: safebin active, `which python3 python` empty, pure Zag, no
  forbidden executable invoked. PASS.

## Metrics

- Cognition lines added: new patch functions (gi_gcd,
  gi_codec_op_ok, gi_codec_induce) plus gi_induce rewrite and D
  threading; 0 to base (byte copy).
- Modes/bridges/handlers: 0. New semantic cases: 0. Codec induction is
  plain functions, not a mode. Base modifications: 0.
- Determinism: 3/3 byte-identical runs
  (SHA-256 173a69f1fa4e060c94b100d221717f0efc4fdf74b56ab2e20f8a9d16edad42c4).
- Frozen dirs untouched (grammar_third, grammar_transfer read-only).

## What this does not claim

- D is induced within the P(a,b)=a*D+b family; the family itself stays
  a researcher-owned world assumption, as in all prior grammar work.
  The uniqueness argument assumes taught pairs satisfy b<D (codec
  injectivity on the taught support); violations surface as op-check
  contradictions (refusal), not silent acceptance.
- No broad generality claim: this is the targeted repair of the
  diagnosed silent-wrong bug, tested on three codecs plus two refusal
  probes.
- The remaining open probes from grammar_third (3 licensors vs
  nlic<=2, literals beyond 0..9, ternary operators) are untouched.

## Follow-ups (not started)

1. The diagonal-only ambiguity (NEG-AMB) is inherent to the fact
   stream, not to the procedure: richer teaching (any off-diagonal
   taught pair) breaks the tie toward the true codec. A follow-up
   could test whether active inquiry (the learner requesting a
   discriminating pair) resolves such ambiguities instead of refusing.
2. Non-injective codecs (taught b>=D) are outside the induced family;
   refusal is the current behavior, characterized but not stressed
   beyond NEG-SHIFT.
3. The packing of D into type-70 field 4 is a physical compromise from
   the frozen 40-byte node layout; any future node-layout change
   should give the codec its own field.
