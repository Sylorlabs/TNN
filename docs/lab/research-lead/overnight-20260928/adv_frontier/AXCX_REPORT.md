# A1 Adversary Report: H-CAUSALEXP-CONSTRUCT

Date: 2026-09-30.
Adversary: A1 (Frontier Architecture Adversary).
Target: H-CAUSALEXP-CONSTRUCT, BUILD-PASS 7/7, result 48f2adc15.
Attack prereg: 33769a378 (frozen before implementation).

## Verdicts

**AX-CX1 (finite researcher-enumerated family): ATTACK-SUCCEEDS.**
**AX-CX2 (depth bound load-bearing, sealed World C): ATTACK-SUCCEEDS.**
**AX-CX3 (disagreement filters, never guides): ATTACK-SUCCEEDS.**

## AX-CX1: The family is finite and researcher-enumerated

### Static evidence (committed source cxconstruct.zag)

(a) Line 202 hardcodes `while(d<=5)`. The depth bound MAXD=5 is a
researcher-set constant. The prereg's "unbounded in length" defense
(section 8) is contradicted by the source.

(b) Lines 206-222 generate every sequence by base-4 counting in fixed
lexicographic order (S=0 < W=1 < OY=2 < OZ=3, most-significant digit
first). The order is independent of hypothesis content. The primitive
set {S,W,OY,OZ} is researcher-authored.

(c) Lines 227-228 record the FIRST sequence with disagreeing
predictions and stop. Selection is deterministic
lexicographic-first-discriminating.

The searchable space is exactly sum_{d=1..5} 4^d = 1364 sequences
(1302 with an observe action). Every "constructed" intervention is
the first-discriminating entry in this finite researcher-enumerated
family.

### Empirical evidence (pure enumeration, no simulation)

Program `axcx_enum.zag` performs pure lexicographic base-4 counting
with no hypothesis simulator. Results (3/3 byte-identical, md5
8424f16f779fad8d882c822e285a4419):
- Depth 1: 4 total, 2 with-observe (raw: checked=2)
- Depth 2: 16 total, 12 with-observe (raw: checked=12)
- Depth 3: 64 total, 56 with-observe (raw World B: checked=56)
- [S,W,OY] is the 3rd with-observe sequence at depth 3
  (raw World A: checked=3, found=1)
- [S,W,W,OY] is the 15th with-observe sequence at depth 4
  (raw World B: checked=15, found=1)

The raw output checked counts are exactly the ordinals of the
selected sequences in the fixed enumeration. The "constructed"
intervention in each world is deterministically fixed by
(primitives, depth bound, lexicographic order, disagreement
predicate). It maps directly to one entry in the finite
researcher-enumerated candidate list.

Per Program 3 kill condition: DOWNGRADE to L2 confirmed. Any L3
construction claim on this mechanism is KILLED. The "composed, not
listed" defense is void: lazy generation by counting IS enumeration
over a finite researcher-defined family.

## AX-CX2: The depth bound is load-bearing (sealed World C)

Sealed World C designed after target freeze:
- H5 = [(X,Z,5),(Z,Y,0)]
- H6 = [(X,Y,4)]

Frozen hand proof: H5 predicts Y=1 iff t>=5; H6 predicts Y=1 iff
t>=4. Disagreement iff t=4 at observation, requiring S+4xW+OY = 6
actions. No sequence of length <=5 discriminates.

Program `axcx2.zag` (generic simulator + World C + verbatim search
loop, MAXD parameterized). Results (3/3 byte-identical, md5
c6b1b7b19c99c5c18c89214bb5a7414b):
- MAXD=5: all 1302 with-observe sequences checked, 0 found.
  NO-DISCRIMINATING-SEQUENCE.
- MAXD=6: SELECT seq=[S,W,W,W,OY] h5pred=0 h6pred=1
  (found at depth 6, checked=311).

The depth bound is load-bearing. "Unbounded in length" is FALSE.
The enumeration family is finite and researcher-bounded. A world
requiring one more primitive than the researcher's bound defeats the
learner entirely.

## AX-CX3: Generation is hypothesis-blind

The same pure-enumeration program (`axcx_enum.zag`, no simulator,
no hypotheses) reproduces the raw output checked counts (3 and 15)
exactly. This proves the SET of simulated sequences and their ORDER
are fixed before any hypothesis is consulted. Hypothesis content
determines only WHICH sequence first discriminates (the found flag),
never the generation order or extent.

The disagreement predicate (`q0!=q1`, line 227) FILTERS a
pre-enumerated stream; it never GUIDES generation. No step of the
algorithm inspects hypothesis structure to propose candidates. The
learner never reasons about delays, never works backward from what
must differ, never targets the disagreement.

The K-CX4 "BECAUSE" criterion rules out random real-world
trial-and-error, but it does NOT distinguish this learner from a
zero-understanding exhaustive enumerator. The "construction" is
empirically indistinguishable from enumerate-all + filter-by-
disagreement.

Semantic authority remaining with researcher: primitive set,
enumeration order, depth bound. Learner supplies only the
disagreement filter. This is selection (filtering) over an
enumerated family, not construction.

## Complete architectural diagnosis

The learner does not construct experiments. It enumerates a
researcher-bounded finite family (1364 sequences, researcher-defined
primitives, order, and depth bound) and applies a disagreement
filter, executing the first entry that passes the filter. This is
precisely "selection from an authored candidate list" where the
list is generated lazily by counting rather than stored in an
array. The distinction between "composed" and "listed" collapses:
exhaustive composition IS enumeration.

## What this does and does not do

- Does NOT overturn BUILD-PASS (7/7). Correctness, determinism,
  and purity (K-CX1 through K-CX7) are not disputed.
- Does NOT dispute the builder's honest bounded-L2 scope.
- DOES formally apply the Program 3 enumerated-list kill condition.
- DOES kill any L3 "experiment construction" claim on this mechanism.
- DOES identify with precision what semantic authority remains with
  the researcher (enumeration family, order, bound) vs the learner
  (disagreement filter only).
- DOES establish that the next causal frontier (true autonomous
  scientist) must have hypothesis-GUIDED generation, not just
  hypothesis-FILTERED enumeration.

## Purity

All attack code pure Zag. Zero Python invocations. Zero em-dash
bytes in committed docs. 3/3 byte-identical runs for both programs.
Commits local, owned path only.

## Files

- PREREG_AXCX.md (prereg, frozen at 33769a378 before implementation)
- axcx_enum.zag (pure enumeration; serves AX-CX1(c) and AX-CX3)
- axcx2.zag (World C + verbatim search loop; AX-CX2)
- AXCX_RAW_ENUM.txt (md5 8424f16f779fad8d882c822e285a4419)
- AXCX_RAW_WORLDC.txt (md5 c6b1b7b19c99c5c18c89214bb5a7414b)
