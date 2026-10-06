# PREREG -- P5-meta3: does prior experience change how future LEARNING occurs?

Branch `ownership`. Frozen before code. Successor to
`p5meta/lifetime_metalearn` (B5d FAIL), diagnosed below.

## DIAGNOSIS OF THE INHERITED FAILURE

`lifetime_metalearn` scored B5A/B5b/B5c/B5e/B5f PASS and **B5d FAIL**:
`err_T(E03) - err_T(E12) = 17 - 24 = -7 < 8`.

The criterion compared error on episode 3 (parity) with error on episode 12
(sum3). **Those are different tasks.** The bar therefore measured *task
difficulty*, not learning-to-learn. A learner could pass or fail it by
accident of which family was scheduled where. That is a criterion defect,
not only a mechanism defect.

Their own note records that the bar survived a bug fix and still failed,
which is evidence the criterion itself is the problem.

## THE FIX: WITHIN-FAMILY ACQUISITION CURVES

Meta-learning must be measured as a **change in the learning curve**, on
the **same family**, between a learner WITH relevant prior experience and
one WITHOUT. Task difficulty is then held constant by construction.

For each family F, run the SAME task twice:

* **acquisition**: trials 1..K needed to reach criterion.
* If relevant prior experience exists, K must be SMALLER for the continuing
  learner than for a fresh learner on the identical task.

This cannot be gamed by scheduling, because both arms run the same family
in the same episode slot with the same budget.

## ARMS

| arm | state entering the measured family |
|---|---|
| `FRESH` | none (learner reset before the family) |
| `RELEVANT` | prior episodes on the SAME family |
| `IRRELEVANT` | prior episodes on a DIFFERENT family |
| `MISLEADING` | prior episodes on a family with the same surface form but conflicting answers |
| `META_ABLATED` | prior present, but the meta-structure that selects/creates learning machinery is removed |
| `ORACLE_META` | researcher-written meta rule (upper bound, not a claim) |

The decisive comparison is `RELEVANT` vs the other four **on acquisition
cost for the same family**.

## BARS

* **M1**: `RELEVANT` acquisition < `FRESH` acquisition (strictly, every family)
* **M2**: `IRRELEVANT` acquisition ~= `FRESH` (neutral: |diff| <= 1 trial)
* **M3**: `MISLEADING` acquisition >= `FRESH` (harmful or rejected), OR it is
  detected and revised within the family (measured: post-detection trials
  to criterion <= FRESH)
* **M4**: `META_ABLATED` loses the M1 advantage while retaining raw prior
  state -- this is what separates "learning-to-learn" from "already knows it"
* **M5**: `ORACLE_META` <= `RELEVANT` acquisition (sanity: the bound is not
  beaten by the learner)
* **M6**: NOT a strategy menu. The learner must have no finite set of
  named strategies to select from; verified by source enumeration.

## M4 IS THE CRITICAL BAR

M1 alone could be satisfied by an ordinary cache: keep the answers, skip
the learning. M4 removes exactly that. If `META_ABLATED` retains the prior
*facts* but loses the *speedup*, then the speedup came from learned
learning machinery, not from retained task state.

`META_ABLATED` is implemented by zeroing the structural state that encodes
*how* the family is learned while leaving the *what* (facts) intact.

## FALSIFIABILITY

If M1 holds but M4 fails, the result is **retained task state**, not
meta-learning, and must be reported as such.

If all of M1-M4 hold, this is genuine learning-to-learn, and must STILL be
classified bounded L2 unless the learned machinery transfers to a family
whose surface form was never seen.

## LIMITS DECLARED NOW

Single author; no independent adversary; synthetic associative substrate;
one seed; does not measure TNN. Prior lane found that this substrate cannot
gate structure, so "learning machinery" here means acquisition dynamics, not
representational invention.
