# PREREG: A1 Frontier Adversary vs H-CAUSALEXP-CONSTRUCT

Date: 2026-09-30.
Status: FROZEN. Committed before any attack implementation, build, or run.
Adversary: A1 (Frontier Architecture Adversary).
Target: H-CAUSALEXP-CONSTRUCT, BUILD-PASS 7/7, result commit 48f2adc15.
Target prereg: 46bdd01c5.

## 1. Mission

Assume the "experiment construction" is actually researcher-authored
machinery with learner-filled parameters until proven otherwise.
Apply the Program 3 kill condition: if the supposedly invented
experiment maps directly to one entry in a finite
researcher-enumerated candidate list, DOWNGRADE to L2.

The builder honestly scopes the mechanism as bounded L2, not L3.
These attacks do not seek to overturn BUILD-PASS (the 7 kill bars are
about construction correctness, determinism, and purity, which are not
disputed). They seek to (a) formally apply the enumerated-list kill
condition, (b) test whether the "unbounded in length" defense holds,
and (c) determine whether the disagreement criterion guides
construction or merely filters enumeration. A successful attack
confirms bounded L2 with precision about what semantic authority
remains with the researcher, and kills any future L3 claim on this
construction mechanism.

## 2. Builder claims under attack (from prereg 46bdd01c5, section 8)

C1: "not selection from an authored candidate list (sequences are
    composed, unbounded in length)."
C2: The "BECAUSE" criterion (K-CX4): "the executed sequence is the
    unique output of a deterministic procedure whose selection rule is
    predicted disagreement. A random-search learner would execute
    sequences without predicted disagreement; this learner cannot, by
    construction."

## 3. Attack AX-CX1: Finite researcher-enumerated family

### 3.1 Architectural fact to be established

From committed source cxconstruct.zag:
- Line 202: `while(d<=5)` hardcodes MAXD=5 (researcher-set depth bound).
- Line 206: `total=4^d` per depth; lines 207-222 generate every
  sequence by base-4 counting in fixed lexicographic order
  (S=0 < W=1 < OY=2 < OZ=3; most-significant digit first).
- Line 223: only sequences with >=1 observe action are simulated.
- Lines 227-228: the FIRST sequence with disagreeing predictions
  (`q0!=q1`) is recorded; search stops.

The searchable space is exactly sum_{d=1..5} 4^d = 4+16+64+256+1024
= 1364 sequences, of which 2+12+56+240+992 = 1302 contain an observe
action. The enumeration order, the primitive set {S,W,OY,OZ}, and the
depth bound are all researcher-defined. The selection rule is
deterministic lexicographic-first-discriminating.

### 3.2 Kill/downgrade criterion (frozen)

ATTACK-SUCCEEDS iff ALL of the following hold:
(a) Source contains a hardcoded finite depth bound (line 202:
    `while(d<=5)`), falsifying "unbounded in length".
(b) The enumeration order is fixed and researcher-defined
    (base-4 counting, lexicographic S<W<OY<OZ), independent of
    hypothesis content.
(c) The empirical checked counts in CXCONSTRUCT_RAW.txt match the
    lexicographic-first-discriminating prediction exactly:
    World A depth 3 checked=3 ([S,S,OY], [S,S,OZ], [S,W,OY]);
    World B depth 4 checked=15 ([S,W,W,OY] is the 15th with-observe
    sequence lexicographically).
If ATTACK-SUCCEEDS: the "constructed" intervention maps directly to
one entry (the first-discriminating entry) in a finite
researcher-enumerated candidate list of 1364 sequences. Per Program 3,
DOWNGRADE to L2 is confirmed (already conceded) and any L3
construction claim on this mechanism is KILLED. The "composed, not
listed" defense is void: lazy generation by counting IS enumeration
over a finite researcher-defined family.

ATTACK-FAILS iff any of (a)-(c) fails.

### 3.3 Method

Static source citation (lines 202, 206, 223, 227-228) plus arithmetic
verification of the checked counts against the raw output. No new
simulation needed; the raw output already contains the evidence.
A short pure-Zag program will independently recompute the expected
checked counts from pure enumeration (no hypothesis simulation) and
assert equality with the raw output values (3 and 15).

## 4. Attack AX-CX2: Depth bound is load-bearing (sealed World C)

### 4.1 Architectural fact to be tested

If "unbounded in length" were true, the depth bound would not be
load-bearing. I design sealed World C AFTER the target froze:
- H5 = [(X,Z,5),(Z,Y,0)]: X causes Z after delay 5; Z causes Y
  immediately.
- H6 = [(X,Y,4)]: X causes Y directly after delay 4.

Hand proof (frozen): At observation time t (after S at t_X=0):
H5 predicts Y=1 iff t>=5; H6 predicts Y=1 iff t>=4. They disagree
iff t=4. A sequence observing at t=4 needs S + 4xW + OY = 6 actions.
At depth <=5, max t at last observe is 3 (S+3xW+OY); H5 and H6 both
predict Y=0 for t<=3. Therefore no sequence of length <=5
discriminates, and S,W,W,W,W,OY (length 6) is the minimal
discriminating sequence.

### 4.2 Kill/downgrade criterion (frozen)

ATTACK-SUCCEEDS iff: a pure-Zag program implementing the EXACT
iterative-deepening loop from committed source (verbatim, with
MAXD=5) plus the generic simulator plus World C hypotheses emits
NO-DISCRIMINATING-SEQUENCE, while the same program with MAXD raised
to 6 emits SELECT seq=[S,W,W,W,W,OY].
If ATTACK-SUCCEEDS: the depth bound is load-bearing; "unbounded in
length" is FALSE; the enumeration family is finite and researcher-
bounded. This strengthens the AX-CX1 downgrade with a constructive
demonstration.

ATTACK-FAILS iff the MAXD=5 learner finds a discriminating sequence
in World C (which would contradict the hand proof and indicate a
simulator misunderstanding).

### 4.3 Method

Pure-Zag program `axcx2.zag`: generic simulator (copied semantics
from committed source), World C rule data, verbatim search loop
with parameterized MAXD. Run with MAXD=5 and MAXD=6. Check outputs.
3/3 byte-identical runs required.

## 5. Attack AX-CX3: Disagreement filters, never guides

### 5.1 Architectural fact to be established

In the committed learner, hypothesis content plays NO role in
GENERATION. The enumeration order and the set of simulated sequences
are fixed before any hypothesis is consulted. The disagreement
predicate (`q0!=q1`, line 227) only FILTERS the pre-enumerated
stream. A genuine construction would use the disagreement to GUIDE
generation (e.g., work backward from what must differ). Here,
generation is hypothesis-blind.

### 5.2 Kill/downgrade criterion (frozen)

ATTACK-SUCCEEDS iff: a pure-Zag program that performs PURE
ENUMERATION (lexicographic base-4 counting over {S,W,OY,OZ}, no
hypothesis simulation, no simulator at all) computes that [S,W,OY]
is the 3rd with-observe sequence at depth 3 and [S,W,W,OY] is the
15th with-observe sequence at depth 4, matching the raw output
checked counts (3 and 15) exactly.
If ATTACK-SUCCEEDS: the checked counts are pure enumeration
artifacts, proving generation is hypothesis-blind. The "BECAUSE"
criterion (K-CX4) rules out random real-world trial-and-error but
does NOT distinguish construction from exhaustive enumeration +
filtering. The learner's "construction" is empirically
indistinguishable from a zero-understanding enumerator. Semantic
authority remaining with researcher: enumeration order, depth
bound, primitive set. Learner supplies only the disagreement
filter. Any L3 "construction" claim is KILLED; the mechanism is
selection (filtering) over an enumerated family.

ATTACK-FAILS iff the pure-enumeration counts do not match the raw
output (indicating hypothesis-guided generation).

### 5.3 Method

Pure-Zag program `axcx3.zag`: no simulator, just enumeration and
counting. Assert counts equal 3 and 15. 3/3 byte-identical.

## 6. Verdict aggregation

- If AX-CX1 SUCCEEDS: enumerated-list kill condition applies.
  Mechanism confirmed as selection over finite researcher-enumerated
  family. L3 construction claim KILLED.
- If AX-CX2 SUCCEEDS: "unbounded" defense FALSE. Depth bound
  load-bearing.
- If AX-CX3 SUCCEEDS: generation is hypothesis-blind; disagreement
  only filters. "Construction" is enumeration + filtering.

All three succeeding gives the complete architectural diagnosis:
the learner does not construct experiments; it enumerates a
researcher-bounded finite family in researcher-defined order and
applies a disagreement filter. This is precisely "selection from an
authored candidate list" where the list is generated lazily by
counting.

## 7. Scope limits (frozen)

- These attacks do not dispute K-CX1 through K-CX7 (the BUILD-PASS
  bars). Correctness, determinism, and purity are not attacked.
- The builder's honest bounded-L2 scope is not disputed; the attacks
  make the L2 classification precise and kill any L3 reading.
- No Python. No em dashes. Commits local, owned path only
  (docs/lab/research-lead/overnight-20260928/adv_frontier/).

## 8. Amendments

None.
