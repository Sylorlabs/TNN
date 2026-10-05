# REPORT -- PHASE 16: DOES COUNTING'S DOMINANCE SURVIVE AT LARGE N?

Prereg `count16/PREREG.md` (written before code). 3/3 sha256
`f537e1b4a3511da8dd66fd3223aa9e29f93bd058644b80a498e6d27c648d1c8f`
loop lint CLEAN. bars lint: 1 hit, the known `ok` false positive (see
`INDEPENDENCE_AUDIT.md` IA-5) -- `ok` is set at line 163 under a real
comparison.

## THE QUESTION

`RED_TEAM.md` A1: four mechanisms tied or lost to `argmax frequency`,
but **every one of those tests used at most 5 candidate structures**.
With n<=5, `argmax frequency` is close to optimal by construction, so
"counting wins" may be an artifact of substrate size rather than a fact
about learning. C1634.

This phase runs the same question with **36 structures and 144
queries**, and separates two explanations that make opposite
predictions:

* **small-N artifact** -- a bigger candidate set should let a learner
  overtake counting.
* **feedback granularity** -- under BINARY (0/1) outcomes, counting is
  not merely hard to beat but *sufficient*, at any N, because any
  selection rule over binary outcomes is a function of the counts.

## SUBSTRATE

36 affine structures `f(s)=a*s+b`, `a` in {1,2,3,4}, `b` in {0..8}.
Each query is two constraints `(x1,y1),(x2,y2)` with `x1!=x2`, so
exactly one structure is consistent -- correctness is unambiguous and
every query is solvable by construction.

* targets `qk(t)=t%36` -- all 36 structures are targets, 4x each
* routing feature `qfeat(t)=(t%36)/3` -- 12 buckets of 3 structures
* 108 training, 36 held-out, disjoint `x` ranges

**The feature is coarse on purpose.** Each bucket contains 3 candidate
targets, so the bucket *cannot* determine the answer. The ceiling for
any bucket-conditional learner is 1/3 = **12 of 36**. This is the
number that decides the phase.

## RESULTS

```
A1 ORACLE positive control (heldout solved)=36 of 36

A2 ARM SCORES on 36 heldout queries
   regime      COUNT FIXED AFFIN SIG_B SIG_G  best_learner
   R1        1     1     1   12     12    12
   R2        1     1     1   12     12    12
   R3        1     1     1   12     12    12

A3 VALIDITY GATES (all derived)
  V1 all 36 structures promoted in train AND heldout =1  (36/36/36)
  V2 ORACLE solves every heldout query          =1
  V3 train/heldout x ranges disjoint            =1
  V4 COUNT below ORACLE in R1                   =1  (1 vs 36)
  V5 world non-degenerate (COUNT>0)             =1
  V6 (same as V3)                                =1
  all gates pass                                =1
```

## FINDINGS

### 1. C1634 is answered: the small-N artifact was REAL. A learner beat counting 12-to-1 at N=36.

`SIG_B` (query-conditional routing on a coarse learned feature) scores
**12 of 36**. `COUNT` scores **1 of 36**. That is not a tie and not a
narrow win -- it is the exact 1/3 ceiling the feature permits, versus
1/36 for a query-blind rule.

**The red team's objection was correct.** The five small-N tests could
not have distinguished "counting is hard to beat" from "counting is
near-optimal at n<=5". At n=36 the query-conditional arm wins by 12x.

### 2. The win is bounded by feature quality, and degrades gracefully when the feature degrades.

12/36 = 1/3 is the ceiling for a 3-way-ambiguous bucket. The margin over
counting is therefore set by *how much the query partitions the
candidates*, not by any property of the mechanism. A better feature
would raise it; a worse one would erase it. See mutation M2 below.

### 3. Frequency regimes made no difference. R1=R2=R3 identically.

All three arms scored the same in all three regimes. The regime
manipulation (uniform / diluted / misleading counts) had **no effect
whatsoever**. So the earlier "counting ties the learner" results were
not caused by misleading frequencies -- the learners simply were not
using the query.

### 4. Graded vs binary feedback: no difference here either. `SIG_G`=12, identical to `SIG_B`.

This **falsifies prereg P16-D.** Prereg predicted graded residual error
would let `RESID_CREDIT` overtake counting. It did not, and the reason
is that `SIG_G` had already reached the feature's ceiling -- there was
no headroom left for a tie-breaker to exploit. **P16-C survives in
modified form**: under BINARY, nothing beat COUNT among the
query-blind arms (`COUNT`=`FIXED`=`AFFIN`=1). But P16-C's strong form
("nothing beats counting") is **false**: `SIG_B` beats it 12-to-1.

**Honest note:** P16-D was untestable as designed, because the coarse
feature capped every bucket-conditional arm at the same value. I should
have preregistered a regime where the feature is *nearly* sufficient,
so headroom exists for feedback granularity to matter. That is a design
error in the prereg, not a finding.

### 5. BINARY arms all tie at 1. `COUNT`, `FIXED_FIRST`, `AFFINITY` are indistinguishable.

All three score 1 of 36. Any query-blind rule that always names one
structure scores exactly the queries targeting that structure. Counting
is not a strong baseline here at all -- it is the *ceiling* for
query-blind selection, and it is 1/36.

## MUTATION TESTING (does the bar actually track the mechanism?)

| mutant | change | SIG_B | SIG_G | gates pass |
|---|---|---|---|---|
| none | -- | **12** | **12** | 1 |
| M1 | routing feature -> constant | **1** | **1** | 1 |
| M2 | feature -> parity (18 targets/bucket) | **2** | **2** | 1 |
| M3 | all targets -> structure 0 | 36 | 36 | **0** |

* **M1** destroys query-conditioning. The arms fall to COUNT's level
  (1). So the win is caused by the conditioning, not by the routing
  code being accidentally well-tuned.
* **M2** coarsens the feature. Score falls to 2, tracking the new
  1/18 ceiling. The bar tracks feature quality continuously.
* **M3** collapses the world. Every arm hits 36 and **the gate
  correctly refuses to certify it** (`all gates pass=0`, V1 fails).
  The harness detects its own degeneracy rather than reporting a
  perfect score.

## DEVIATIONS FROM PREREG (disclosed)

1. **`RESID_CREDIT` was made query-conditional.** As literally
   preregistered it is a per-structure global statistic, hence
   query-blind, hence *structurally unable* to beat a query-blind
   `COUNT` -- it would have degenerated for reasons of construction.
   The prereg version would have produced a vacuous tie. Made
   bucket-conditional, where the BINARY case still falls back to the
   count statistic exactly.
2. **`AFFINITY` is reported but is not a meaningful test at this N.**
   It is `COUNT` plus a generic co-occurrence bonus and ties `COUNT`.
3. **The feature was redesigned three times during development.** First
   attempt set `qfeat(t)=t%36`, which made the feature *identical to the
   target* -- `SIG_B` scored 36/36, a perfect lookup on the answer. I
   caught this because 36/36 is implausible, checked the feature against
   the target map, and rejected the world. Second attempt used 6 buckets
   which could only reach 12 of 36 structures (V1 failed). The committed
   version is the third. **All three attempts and their defects are
   recorded here because the first one would have been a spectacular
   false positive.**

## ANSWER TO C1634

> Is counting's dominance in Phases 6-9 an artifact of small N?
>
> **Partly, and less than the lane concluded.** At N=36 a
> query-conditional mechanism beats counting 12-to-1, so the small-N
> tests were indeed underpowered. But the beating arm needed a feature
> that partitions the candidate set. Where the feature is coarse, every
> arm ties at the feature's ceiling. **Counting is not a strong
> baseline that was outsmarted -- it is the ceiling of all query-blind
> selection.** The five earlier ties are therefore explained without
> any appeal to mechanism quality: those mechanisms were query-blind.

## WHAT THIS DOES NOT SHOW

* **Nothing here measures TNN.** Per `INDEPENDENCE_AUDIT.md`, still
  true of every phase. This is a declared minimal reproduction.
* **Selection only.** Candidate generation is not tested.
* **Structures are affine maps, not programs.**
* **`SIG_B` is a lookup over a learned per-bucket count.** It is not
  claimed to be a mechanism TNN could implement; it establishes only
  that the *ceiling* moves once the learner conditions on the query.
* The arm labels `FIXED`/`AFFIN`/`SIG` are researcher-authored scorers.
  Per the prereg's falsifiability note, the surprise here is the
  **positive** direction, so it is reported as the headline rather than
  reclassified as a harness artifact.

## STATUS

C1634: **RESOLVED** (with the scope limits above).
C1632: unchanged.
L3 = 0. No architecture changed. No bridges added or removed.