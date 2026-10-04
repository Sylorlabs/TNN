# PREREG: A2 Simpler-Explanation Attacks on Frontier Claims

Date: 2026-09-30.
Status: FROZEN. Committed before any attack implementation, build, or run.
Role: A2 (Simpler-Explanation / Authored-Intelligence Adversary).

## Mission

Attack frontier claims from the simpler-explanation angle. Assume every
"invention" is memorization, search, or researcher cuing until proven
otherwise. For each target, identify precisely what semantic authority
remains with the researcher, then design an attack that succeeds if that
authority is load-bearing.

## Target status at prereg time

- F1 genexec substrate: NO LIVE CLAIM. First wave governance-void. No
  attack possible yet. A2 stands ready for the fresh wave.
- F2 autonomous scientist (H-CAUSALEXP-CONSTRUCT, BUILD-PASS 7/7,
  result 48f2adc15): LIVE TARGET. Primary attack below.
- F3 developmental language (DEVINT1): DEVINT1 A2 already established
  the width-match artifact and revived S4 as positive. No new A2 attack
  this wave; A2 endorses the A2 findings.
- I2 learning-to-learn: NO LIVE CLAIM FOUND. No attack possible yet.

## Attack A-F2-1: Effective menu size (disguised menu)

### Researcher authority under test

The H-CAUSALEXP-CONSTRUCT learner (cxconstruct.zag, lines 202-246):
- loops depth d from 1 to 5 (hardcoded `while(d<=5)`);
- at each depth enumerates ALL 4^d sequences via base-4 counting
  (`si` from 0 to total-1, digits map to S=0,W=1,OY=2,OZ=3);
- simulates each under both hypotheses;
- selects the FIRST sequence (in enumeration order) with disagreeing
  predictions;
- executes it once.

### Attack

Count the exact effective candidate set: the number of distinct
sequences the learner can ever output, across all possible hypothesis
pairs. This is bounded by sum_{d=1..5} 4^d = 4+16+64+256+1024 = 1364.

### Kill criterion

ATTACK-SUCCEEDS if the learner's output for any hypothesis pair is
fully determined by (fixed 1364-sequence enumeration, researcher-defined
lexicographic order S<W<OY<OZ, researcher-defined first-disagreement
criterion, researcher-defined MAXD=5), with no incremental construction,
no partial-progress guidance, and no learner reasoning about sequence
structure. Specifically: if a trivial precomputation (enumerate 1364
sequences in fixed order, apply disagreement test) produces byte-identical
SELECT outputs to the learner on Worlds A and B, the "construction" is
selection from a disguised menu.

ATTACK-FAILS if the learner exhibits structure-sensitive assembly
(e.g., building on partial matches, skipping provably-useless prefixes,
or extending beyond a fixed bound based on the problem).

### Expected result

ATTACK-SUCCEEDS. The implementation is exhaustive enumeration plus
argmin. There is no incremental construction.

## Attack A-F2-2: Beyond-menu world (length-6 discrimination required)

### Researcher authority under test

MAXD=5 is hardcoded. The prereg (section 8) claims "sequences are
composed, unbounded in length." If the bound is load-bearing, a world
requiring length 6 will cause the learner to emit
NO-DISCRIMINATING-SEQUENCE and halt, proving the "unbounded" claim false
and the menu bounded by researcher choice.

### World C (frozen)

- H5: [(X,Z,5),(Z,Y,0)]. X causes Z after delay 5; Z causes Y immediately.
- H6: [(X,Y,4)]. X causes Y directly after delay 4. Z never changes.

Frozen hand proof:
- Lengths 1-4: all observing sequences have t<=3 at observation or no
  S before observation; both hypotheses predict 0. Agree.
- Length 5: S,W,W,W,OY gives t=3. H5: 3<5 so Z=0,Y=0. H6: 3<4 so Y=0.
  Agree (0/0). All other length-5 observing sequences have t<=3. Agree.
- Length 6: S,W,W,W,W,OY gives t=4. H5: 4<5 so Z=0,Y=0. H6: 4>=4 so
  Y=1. Predictions 0 vs 1. DISCRIMINATES.
- Therefore the minimal discriminating sequence has length 6.

### Attack

Implement World C in a standalone Zag program using the same generic
simulator semantics. For depths 1 through 6, count discriminating
sequences. Show:
(a) depths 1-5 yield zero discriminating sequences;
(b) depth 6 yields at least one (S,W,W,W,W,OY).

### Kill criterion

ATTACK-SUCCEEDS if (a) and (b) both hold. This proves the learner,
capped at MAXD=5, would emit NO-DISCRIMINATING-SEQUENCE on World C
(its own prereg defines this as BUILD-FAIL), while a genuine
open-ended constructor would extend to depth 6. The depth bound is
researcher-imposed and load-bearing; the "unbounded in length" claim
is false.

ATTACK-FAILS if a discriminating sequence exists at depth <=5 in
World C (my hand proof is wrong), or if the learner architecture
contains a principled (non-arbitrary) reason to stop at 5 that is
derived from the problem rather than hardcoded.

## Attack A-F2-3: Researcher-order determinism (selection, not reasoning)

### Researcher authority under test

When multiple discriminating sequences exist at the found depth, the
learner selects the lexicographically first (S=0<W=1<OY=2<OZ=3). This
order is researcher-defined. The learner does not prefer shorter,
cheaper, or more informative sequences; it prefers the one that comes
first in the researcher's counting order.

### Attack

In World A, enumerate ALL discriminating sequences at depth 3 (not just
the first). Count them. Identify which one the learner selects
(S,W,OY) and show it is the lexicographically first, not e.g. the one
with fewest waits or the most informative observation pattern.

### Kill criterion

ATTACK-SUCCEEDS if >=2 discriminating sequences exist at the found
depth and the learner's choice is fully explained by researcher-defined
lexicographic order with no problem-derived justification (cost,
informativeness, robustness) for preferring it.

ATTACK-FAILS if exactly 1 discriminating sequence exists at the found
depth in both worlds (the order is then irrelevant), or if the learner
uses a problem-derived tie-breaker.

## Scope and honesty

- These attacks target the CONSTRUCTION claim, not the discrimination
  filter (which H-CAUSALEXP1 already established as load-bearing).
- A-F2-1 and A-F2-2 succeeding does not invalidate the 7/7 BUILD-PASS;
  the bars do not test authorship. It reclassifies the mechanism as
  bounded L2 (systematic search over researcher-bounded space) and
  kills any L3 reading.
- Pure Zag for all test code. No Python. No em dashes.
- 3/3 determinism required for all attack programs.

## Amendments

None.
