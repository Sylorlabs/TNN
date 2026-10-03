# DECLINE SIGNAL ANALYSIS

**Status:** ANALYSIS ONLY. No implementation. No source modifications.
**Date:** 2026-10-01
**Input:** Frozen TNN-2 source `tnn2_build/tnn2.zag` (1591 lines, read-only).
**Verdict:** DECLINE-SIGNAL-COMPLETE

## 1. Current Behavior: The Four-Stage Query Pipeline

`ev_query` (tnn2.zag:813) implements a fixed four-stage fallback chain. On a
query (s, r), the stages execute in researcher-fixed order:

**Stage 1: activate (line 815).** Scans all live tag-1 FACT nodes for (s, r)
match. Selects by maximum `bid` (edge-count support score). Returns the
winning fact's value unconditionally. There is no minimum bid threshold; a
fact with bid 1 wins if it is the only candidate, and its value is returned
with exactly the same confidence as a fact with bid 100.

**Stage 2: trial (line 827).** `mp_run` calls `t2_trial` directly (theater
audit T1: the MISS_POLICY node is never read). The trial assembles candidate
graphs in fixed phase order and verifies each via `t2_try_verify` (line 497):
- Unmasked mode: accept iff executed value equals harness-supplied `expected`.
- Masked mode: accept iff executed value is not -2 and not -999999
  (execution failure sentinels). Any other value is accepted.

**Stage 3: bootstrap (line 830).** `bootstrap_miss` collects up to 6 recent
facts with the same relation r. If at least 2 exist, all agree on one value,
and the count meets k (from `k_get`, default 3, theater audit T2: never
rewritten by experience), it teaches and returns that value.

**Stage 4: miss (lines 832-834).** Logs the miss, calls `miss_inquire`
(creates a tag-30 UNCERTAINTY node and a guide node), and returns -2.

The only decline-shaped output in the entire system is the integer -2,
returned exclusively at Stage 4.

## 2. What -2 Means (and Does Not Mean)

The sentinel -2 is returned in five distinct situations (tnn2.zag:498, 507,
771, 787, 834):

1. `t2_try_verify`: trial root invalid, or candidate failed verification.
2. `bootstrap_miss`: fewer than 2 same-relation facts, or values disagree,
   or count below k.
3. `ev_query` Stage 4: all prior stages exhausted.

The sentinel is therefore overloaded. It conflates "no candidate existed,"
"candidates existed but failed an external check," "insufficient evidence,"
and "declined to answer." No caller distinguishes these cases. In the test
harness, -2 is treated uniformly as "don't know."

Critically, -2 at Stage 4 is **pipeline exhaust, not a cognitive choice**.
There is no point in the pipeline where the system evaluates its own
epistemic state and elects to withhold. The -2 falls out when nothing else
fires. A system that declined by choice would need a decision point; TNN-2
has none.

## 3. Confident Answer vs Guess: No Distinction Exists

The return type of `ev_query` is a bare i32. Nothing in the output
distinguishes:

- A value from a high-bid, multiply-supported fact (Stage 1).
- A value from a masked trial that accepted the first executable candidate
  (Stage 2, masked mode accepts anything that runs).
- A value from bootstrap inference over 2-3 agreeing facts (Stage 3).

All three return identically. The `log_ev` call records a success flag (1 for
any returned value, 0 for -2), but the event log is write-only (theater
audit T4: no production reader). No downstream consumer can tell a confident
answer from a guess.

The H2 void (`72173fe11`) demonstrated the consequence: all probes returned
direct FACT values that were wrong (the worlds' lying-oracle facts), with
zero behavioral or white-box distinction from correct answers. TNN-2 returned
confidently wrong values because Stage 1 has no mechanism to doubt what it
finds.

## 4. The Decline Capability: Definition

A decline capability, as distinct from pipeline exhaust, requires all three
of the following. TNN-2 has zero.

**(a) A decision point.** Some location in the query path where the system,
having a candidate answer (or candidates), evaluates whether to return it.
Currently every stage returns its first success unconditionally. There is no
"should I answer?" gate anywhere.

**(b) A learner-internal criterion.** The decision at (a) must be governed by
a value in learner state that (i) has a production read path on the decision
path, (ii) has an exercised production write path, and (iii) changes in
response to prediction error. This is the K-H2-3 six-element audit standard
applied to withholding. The criterion mechanism analysis (`8a2ff4b77`)
records zero pure learner-owned accept/reject decisions; withholding is one
third of H2's key question ("accept/reject/withhold"), and the withhold
third is entirely absent.

**(c) A distinct white-box trace.** A declined query must leave a trace
distinguishable from both "answered" and "missed by exhaust." Currently:
- Answered (right or wrong): value returned, USE edge added, `ref_prot`
  called, log success=1. Right and wrong answers are indistinguishable.
- Missed: -2 returned, UNCERTAINTY node created (never read, theater T5),
  guide created, log success=0.

A true decline would need a WITHHOLD-class record naming the withheld
candidate, the criterion value that triggered withholding, and the evidence
consulted. Nothing of this kind exists.

## 5. Gap Analysis

**G1: No confidence threshold on activate.** `bid` is used only for
max-selection, never for gating. The minimal change class would be a
threshold below which Stage 1 declines rather than returns. Currently no
threshold exists, and any threshold would need to satisfy the learner-internal
criterion standard (G2) to count as a cognitive choice rather than a new
researcher-fixed constant.

**G2: No learner-internal criterion anywhere on the accept/reject/withhold
path.** All seven decision points inventoried in `8a2ff4b77` are
researcher-owned or mixed-with-source-literals. Withholding cannot be a
cognitive choice until some criterion in the causal chain is learner-owned.
This is the same gap as K-H2-3, applied to the withhold decision.

**G3: UNCERTAINTY nodes are write-only (theater T5).** `miss_inquire` creates
tag-30 nodes on every miss, but `ev_act` keys off guide edges and context
matching, never reading UNCERTAINTY fields. The inquiry machinery therefore
cannot consult the system's own recorded ignorance. The ignorance-dedup
analysis (duplicate UNCERTAINTY nodes for already-known keys) is a symptom:
the system writes "I don't know" and never reads it back.

**G4: Masked trial is anti-decline.** In masked mode, `t2_try_verify` accepts
the first candidate that executes without failure. This is guessing, not
withholding. A system with a decline capability would need the masked path to
withhold when no candidate meets an internal standard, rather than returning
the first executable value.

**G5: Sentinel overloading.** The -2 conflates at least five distinct
epistemic situations (Section 2). A decline signal must be distinguishable
from "nothing fired." Currently the output vocabulary has exactly two words:
a value, or -2.

**G6: No withhold-vs-wrong-answer distinction.** Because Stage 1 returns any
activated fact unconditionally, and because right and wrong answers share
identical white-box traces, the system cannot currently prefer "decline" over
"confidently wrong." The H2 void is the empirical demonstration: wrong
answers were returned with the full behavioral signature of correct ones.

## 6. Relation to K-H2-2 (Lie Resistance)

K-H2-2 (frozen prereg `c15a47d63`, Section 5) permits three acceptable
responses when the oracle contradicts retained facts:

1. Raise an explicit uncertainty signal.
2. Raise a contradiction signal.
3. Refuse promotion.

Declining is directly relevant via paths 1 and 3.

**Path 1 (uncertainty signal):** The UNCERTAINTY node type exists but has no
production read path (G3). Creating a node no consumer reads cannot satisfy
"raises an explicit signal." The signal must be raised to something that
acts on it.

**Path 2 (contradiction signal):** `ev_observe` detects contradiction only
when an observation arrives for an already-activated fact (tnn2.zag:838-858).
On the query path, there is no comparison of the activated fact against
other retained facts. If a lying-oracle fact is activated at Stage 1, no
query-path mechanism checks it against the rest of the knowledge base. The
lie is returned, not flagged.

**Path 3 (refuse promotion):** Promotion (`promote_graph`, line 533) is
unconditional after verification (criterion analysis D2: researcher-owned).
There is no promotion gate at which refusal could occur. Moreover, in the H2B
scenario as constructed, the lie arrives as a direct fact, so the trial and
promotion never run; the relevant refusal point would be at query time
(decline to return the suspicious fact), which does not exist (G1, G2).

**Assessment:** Declining is not merely related to lie resistance; on the
query path, declining is the only available form of resistance, because the
query path has no contradiction-detection machinery. A learner that cannot
withhold cannot resist a lie it has already stored. K-H2-2 path 1
(uncertainty signal) presupposes exactly the decline capability analyzed
here, plus a consumer for the signal.

## 7. What Would Have to Change (Descriptive, Not Prescriptive)

For the record, the minimal class of change that would constitute a genuine
decline capability (not a design proposal; no implementation undertaken):

1. A gate in the query path, positioned no later than Stage 1 return, that
   evaluates a learner-state criterion before returning any value.
2. The criterion satisfying the six-element learner-internal standard
   (read path, exercised write path, prediction-error update, ablation
   flips the decision).
3. A distinct withhold trace, separable in white-box state from both
   "answered" and "missed by exhaust."
4. The UNCERTAINTY write path connected to a production read path, so that
   recorded ignorance informs future withhold decisions (closing the
   ignorance-dedup loop).

Items 1-4 are jointly necessary. Any subset is theater by the K-H3 audit
standard: a gate with a source-fixed threshold is a researcher decision; a
criterion with no exercised write path is decoration; a withhold trace no
consumer reads is logging.

## 8. Standing Architectural Metric (Current State, Decline Subsystem)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 4 (stage order, max-bid selection,
  trial accept rule, bootstrap k). The decline path has zero decisions; it
  is the absence of a stage firing.
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SOURCE-ENUMERABLE FORMS: all (the -2 sentinel; the UNCERTAINTY node layout).
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0.
- WITHHOLD EVENTS: 0 (no withhold decision exists; -2 returns are exhaust,
  not choice).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
- COGNITION LINES ADDED BY THIS ANALYSIS: 0.

## 9. Explicit Non-Claims

- This analysis does not establish that a decline capability is achievable
  within the current architecture; it characterizes the absence.
- It does not propose an implementation. Section 7 describes the change
  class for completeness of the gap analysis, not as a work order.
- It does not predict H2 outcomes. The H2 evaluation is VOID (`72173fe11`);
  no K-H2-2 verdict exists.
- It does not claim that declining alone would satisfy K-H2-2; path 1
  additionally requires a signal consumer, and the bar requires F=1.0 with
  zero false promotions.
- The masked-trial guessing behavior (G4) is reported as observed; no claim
  is made about whether it is ever the correct policy.

## 10. Relation to Sibling Analyses

- Criterion mechanism (`8a2ff4b77`): this analysis applies its D1-D7
  inventory to the withhold third of H2's key question. Consistent: zero
  pure learner-owned decisions.
- Theater audit (`e0423538a`): T5 (UNCERTAINTY write-only) is load-bearing
  for G3. T1 (MISS_POLICY dead) confirms the trial has no policy gate at
  which a withhold criterion could attach.
- H2 void (`72173fe11`): Finding 2 (trial never runs; direct facts returned)
  is the empirical instance of G6. The decline capability would have been
  the only query-path mechanism capable of refusing the lying-oracle facts.
- Plan constructor (`61402fd25`): G5 (no learner-internal verification
  criterion) and the decline gap are the same absence viewed from
  construction vs query. A constructor that cannot verify internally also
  cannot decline internally.
- Verification criterion (sibling worker, in flight at time of writing):
  expected to cover what replaces harness-supplied `expected`; this
  analysis covers what happens when the answer should be withheld rather
  than verified.
