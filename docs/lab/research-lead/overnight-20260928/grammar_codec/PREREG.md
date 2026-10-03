# PREREG: Grammar Codec Induction (the deeper grammar fix)

## Worker

Codec Induction Worker. Unfrozen variant only. Frozen read-only:
grammar_third/ and grammar_transfer/ are never modified; their sources
are copied, never edited. This prereg is committed BEFORE any
implementation (commit-order self-check).

## Problem (from the two prior reports)

grammar_third (commit ee621a50d) proved the induction machinery goes
SILENTLY WRONG when the pair codec breaks: on EXL3 (world
P(a,b) = a*8+b vs assumed a*16+b) it induced a confident wrong grammar
(a=[0,3], b=[0,15]) with 4/4 valid and no alarm. Diagnosis: promote the
codec from hardcoded constant to induced grammar state (new type-70
field), induce the divisor in gi_induce, thread it through all five
decode sites, replace the tautological check with a real cross-fact
consistency check, and refuse (fail closed) when the codec is not
established.

grammar_encode (commit df668fa20, GRAMMAR-ENCODE-COMPLETE) built the
honest interim guard (gi_codec_check: refuse with -3 on op-semantic
mismatch under the assumed /16 codec) and noted codec induction is the
deeper fix; refusal is honest until induction exists. This worker
implements the induction.

## Codec induction design: gi_codec_induce

Model family (unchanged world assumption, now with induced parameter):
pair encoding P(a,b) = a*D+b with unknown positive divisor D. The
discriminator comes from literal co-occurrence structure, never from
re-encoding (re-encoding is vacuous under any fixed divisor, as both
prior reports show).

Key algebraic facts, all read off the taught fact stream:

- SUB eval fact (P,41,t): P = a*D+b, t = a-b, so P+t = a*(D+1).
- DSUB decomp fact (t,43,P): same, P+t = a*(D+1).
- DIV eval fact (P,42,1) (unit quotient): a=b, P = b*(D+1).
- DDIV decomp fact (1,44,P) (unit quotient): same, P = b*(D+1).

So every positive value in the set

  S = { P+t : (P,41,t) or (t,43,P) } union { P : (P,42,1) or (1,44,P) }

is a positive multiple of (D+1). Let g = gcd of the positive members
of S. Then (D+1) divides g, i.e. the true D is always among the values
d = v-1 where v divides g and v >= 2. The candidate set is derived from
the observed g by exact integer arithmetic; NO divisor candidate is
hardcoded or selected from any fixed list (in particular not from
{8,16,32}).

Each candidate d is tested by the op-consistency check (the
grammar_encode discriminator, now run per candidate instead of under an
assumed codec): for every live type-1 eval fact (r in {41,42}), decode
P under d to (aa,bb) = (P/d, P-aa*d) and require the named op to
reproduce t (41: aa-bb==t; 42: bb>0, aa-(aa/bb)*bb==0, aa/bb==t).

Decision rule (fail-closed):

- exactly ONE consistent divisor d: the codec is identified; induce D=d.
- ZERO consistent divisors (includes g<2, i.e. no positive multiple
  observed or g=1): contradicted; refuse with -3. No grammar written.
- TWO OR MORE consistent divisors: genuinely ambiguous; refuse with -4.
  No grammar written. Guessing between consistent codecs would be the
  old silent-wrong bug in a new form.

Why uniqueness is the right bar: the op check is strong (it killed the
wrong /16 codec on EXL3/EXL4 in grammar_encode and kills every wrong
divisor of g on the three main worlds, verified by hand below), but the
stream can be genuinely ambiguous (NEG-AMB below: D=8 with components
{2,4,6} vs D=17 with components {1,2,3} satisfy every taught fact). The
machinery must refuse there, not pick.

Scope note (honest limitation): the uniqueness argument assumes the
teacher's taught pairs satisfy b<D (codec injectivity on the taught
support), which holds in all worlds tested here. A teacher violating it
teaches colliding pairs; the collision surfaces in the op check as a
contradiction (refusal), because one P would have to satisfy two
incompatible op semantics. Non-injective codecs are outside the induced
family and fail closed.

## Type-70 node: the codec becomes induced grammar state

New logical field: divisor D, stored in the type-70 grammar node.
Physical constraint: nodes are exactly 40 bytes (noff(n) = 64+n*40 in
the frozen base, which is not modified), fields 0..32 hold the existing
grammar data and field 36 is the live flag, so no free 4-byte slot
exists. Field 4 (nlic, always in {1,2} by the nlic<=2 guard) packs both:
field4 = nlic + 4*D. Unpack: D = field4/4, nlic = field4 - 4*D. The
packing stride 4 is 2^2 bits for nlic (nlic<4 always); it is NOT a codec
divisor candidate and never enters any decode. gi_grammar_read exposes
D at buf[32]; the driver prints it on the GI-GRAMMAR line.

## Threading D through the decode sites

The old /16 appears at five sites in e4_patch.zag. New treatment:

1. gi_induce part 1 (old lines 53-54, decode + sanity check): DELETED
   as diagnosed vacuous (a*D+b==P is a tautology under ANY divisor; the
   check can never contradict the codec). Part 1 keeps only the
   codec-independent licensor discovery. Its replacement is
   gi_codec_induce, called after part 1 and before part 2: the real
   cross-fact consistency check the diagnosis required.
2. gi_induce part 2 (range induction): decode decomp pair objects under
   the induced D; track min/max (no codec-tied 0..15 bound).
3. gi_trial_build2: decode construction outputs under D read from the
   grammar buffer; range check against induced min/max (unchanged).
4. gi_hardcode_build: decode under D passed as a parameter (read by the
   driver from the induced grammar; the arm keeps its hardcoded 43/44
   relations and 0..9 range, but the codec is the induced one, since a
   hardcoded /16 would re-test the already-diagnosed broken assumption).
5. gi_classify: decode the MAP object pair under D passed as a
   parameter (read by the driver from the induced grammar before any
   ablation).

gi_induce return contract: 1 induced (node written WITH divisor
field); 0 legacy refusal (unchanged); -3 codec contradicted; -4 codec
ambiguous. On any non-1 code nothing is written (fail-closed). The old
-3 guard function gi_codec_check is removed, subsumed by the
per-candidate op check inside gi_codec_induce.

## Worlds (all: SUB=41, DIV=42, DSUB=43, DDIV=44, BUILD=45)

- EXL2 (control): literals 0..9, P(a,b) = a*16+b. TRAIN {1,3,5,7}
  (4 BUILD facts). TEST {0,2,4,6,8,9} (6 targets).
- EXL3: literals 0..7, P(a,b) = a*8+b. TRAIN {1,3,5,7} (4 BUILD
  facts). TEST {0,2,4,6} (4 targets).
- EXL4: literals 0..3, P(a,b) = a*32+b. TRAIN {1,3} (2 BUILD facts).
  TEST {0,2} (2 targets).
- NEG-AMB (genuinely ambiguous codec): literals {2,4,6}, P(a,b) =
  a*8+b, but SUB/DIV/DSUB/DDIV/BUILD taught ONLY on diagonal pairs
  (a,a). Every taught fact is satisfied both by D=8 (components
  {2,4,6}) and by D=17 (components {1,2,3}). The machinery must REFUSE
  with -4, not pick.
- NEG-SHIFT (no consistent codec): literals 0..9, teacher uses
  P=a*16+b for a in 0..4 and P=a*8+b for a in 5..9 (codec shift
  mid-stream). S contains 17 and 45, so g=1. The machinery must REFUSE
  with -3.

Hand-verified divisor tables (S, g, candidates d=v-1, op-check
outcome):

- EXL2: S multiples of 17 (e.g. SUB (1,0): P+t=17); g=17 (prime);
  candidates {16}; d=16 consistent (true codec). INDUCE D=16.
- EXL3: S multiples of 9 (e.g. SUB (1,0): P+t=9); g=9; candidates
  {2,8}; d=2 killed by (8,41,1): (4,0), 4!=1; d=8 consistent.
  INDUCE D=8.
- EXL4: S multiples of 33 (e.g. SUB (1,0): P+t=33; DIV (1,1): P=33);
  g=33; candidates {2,10,32}; d=2 killed by (32,41,1): (16,0),
  16!=1; d=10 killed by DIV (65,42,2): (6,5), 6/5 inexact; d=32
  consistent. INDUCE D=32.
- NEG-AMB: S = {18,36,54} (all multiples of 18); g=18; candidates
  {1,2,5,8,17}; d=1,2,5 killed (e.g. d=5 by (36,41,0): (7,1),
  7-1=6!=0); d=8 consistent; d=17 consistent ((18,41,0)->(1,1),
  (36,41,0)->(2,2), (54,41,0)->(3,3), DIV facts exact). Two
  consistent: REFUSE -4.
- NEG-SHIFT: g=1: REFUSE -3.

## Predicted outcomes (frozen bars)

- EXL2: GI-INDUCED 1, GI-GRAMMAR D=16 a=[0,9] b=[0,9] nlic=2,
  induce arm 6/6 valid (class 1), ablate arm 0/6, hardcode arm 6/6.
- EXL3: GI-INDUCED 1, GI-GRAMMAR D=8 a=[0,7] b=[0,7] nlic=2,
  induce arm 4/4 valid (class 1), ablate arm 0/4, hardcode arm 4/4.
- EXL4: GI-INDUCED 1, GI-GRAMMAR D=32 a=[0,3] b=[0,3] nlic=2,
  induce arm 2/2 valid (class 1), ablate arm 0/2, hardcode arm 2/2.
- NEG-AMB: GI-INDUCED -4, GI-GRAMMAR none, GI-I-NOGRAMMAR.
- NEG-SHIFT: GI-INDUCED -3, GI-GRAMMAR none, GI-I-NOGRAMMAR.
- Determinism: 3 runs byte-identical (SHA-256 recorded in run files).

## Kill bars (all must hold, else verdict fails)

K1: 3/3 runs byte-identical.
K2: per-world GI-MATCH 1 on all five worlds; induced divisors exactly
    16/8/32 on EXL2/EXL3/EXL4; ranges exactly a=[0,9]/[0,7]/[0,3] and
    b=[0,9]/[0,7]/[0,3].
K3: no divisor candidate hardcoded in the machinery: the patch names no
    codec divisor literal; candidates come only from divisors of the
    observed gcd. (The packing stride 4 in field 4 is documented above
    and is not a divisor.)
K4: NEG-AMB refuses -4 and NEG-SHIFT refuses -3, with no grammar node
    written in either (GI-GRAMMAR none observable).
K5: ablate arms 0 valid on EXL2/EXL3/EXL4 (the induced grammar,
    including its divisor field, is load-bearing for construction).
K6: toolchain guard: safebin active, `which python3 python` empty,
    pure Zag; no forbidden executable invoked.

## What this does NOT claim

- The divisor is induced within the P(a,b)=a*D+b family, not invented
  as a representation; the family itself remains a researcher-owned
  world assumption (as in all prior grammar work).
- 9/9-style generality is not claimed: this is the targeted repair of
  the diagnosed silent-wrong bug, tested on three codecs plus two
  refusal probes.
- The remaining open probes from grammar_third (3 licensors vs
  nlic<=2, literals beyond 0..9, ternary operators) are untouched.

## Verdict on pass

GRAMMAR-CODEC-COMPLETE, with the per-system divisor table
(EXL2:16, EXL3:8, EXL4:32, NEG-AMB:refused-ambiguous,
NEG-SHIFT:refused-contradicted).
