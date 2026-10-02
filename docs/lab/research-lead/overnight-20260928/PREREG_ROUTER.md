# PREREG: Learned (Structure-Inferred) Task Routing

**Date:** 2026-09-29
**Agent:** Learned Routing Researcher
**Status:** FROZEN (committed before implementation)

## Hypothesis H-ROUTER

A continuing learner can infer task type (procedure-learning vs
causal-learning vs procedure-query vs causal-query) from input structure
alone, with no type label supplied. Each routing decision is computed
per-item at runtime from structural predicates, emitted as a white-box
trace, and ambiguous inputs are withheld rather than misrouted.

## Scope Honesty (read first)

The routing predicates are **authored** (like the procedure enumeration
is authored). What is *inferred* is the per-item decision: no token in
the input names the task type or the target store. This is
**structure-inferred routing**, not meta-learned routing. A router whose
rules are themselves learned from experience is future work and is NOT
claimed here.

Procedure-query slot selection is also out of scope: when several
procedures are stored, the router applies all of them and reports each
(slot, output) pair. Choosing which procedure the user *intended* is a
separate retrieval problem. The router's contract is type-routing only.

## Input Language

Lines of text. Format markers (not type labels): `>` separates
left/right within a segment, `;` separates segments, `,` separates ints
inside a tuple. A field is an int-tuple iff it matches digits and
commas only; otherwise it is a string.

Router rules (evaluated in order):

1. Split line into `;`-segments. Empty line or any empty segment ->
   WITHHOLD ("empty").
2. If every segment has the shape `str>str` (comma-free strings) and
   there are >= 2 segments -> PROC_LEARN.
3. If every segment has the shape `i,i,i>i,i` (3 ints > 2 ints) and
   there are >= 2 segments -> CAUS_LEARN.
4. If exactly 1 segment, no `>`, no commas -> PROC_QUERY.
5. If exactly 1 segment, no `>`, exactly 3 ints -> CAUS_QUERY.
6. Otherwise -> WITHHOLD with a reason (single pair, single episode,
   mixed shapes, malformed).

The >= 2 threshold for learning items is an authored disambiguation
rule: a single pair (or single episode) is structurally identical to a
malformed query, so the honest answer is WITHHOLD. Documented as a
limitation, not a cheat.

Routing is purely structural (shape-based). Whether the routed
mechanism then succeeds or fails is the mechanism's honest outcome, not
the router's claim.

## Frozen Item Stream

Learning items (unlabeled):

- L1: `abc>cba;xy>yx` -> expect PROC_LEARN, discovers n-1-k at slot 0
- L2: `0,0,0>0,1;0,0,0>0,1;1,0,0>1,0;1,0,0>1,0` -> expect CAUS_LEARN,
  induces hot->stays-low and cold->rises rules
- L3: `abc>ccc;xy>yy` -> expect PROC_LEARN, discovers n-1 at slot 1,
  slot 0 undisturbed

Query items (unlabeled):

- Q1: `hello` -> expect PROC_QUERY; slot 0 yields `olleh`,
  slot 1 yields `ooooo` (both reported)
- Q2: `1,0,0` -> expect CAUS_QUERY; predicts pressure stays low
- Q3: `0,0,0` -> expect CAUS_QUERY; predicts pressure rises

Ambiguity probes (unlabeled):

- A1: `ab>ba` (single pair) -> WITHHOLD
- A2: `0,0,0>0,1` (single episode) -> WITHHOLD
- A3: `hello;world` (two bare strings) -> WITHHOLD
- A4: `` (empty) -> WITHHOLD

Exploratory (non-kill):

- E1: `ab>xy;cd>zw` (pairs without rearrangement) -> expect route
  PROC_LEARN (structural), then honest LEARN FAIL from pextract.
  Documents router/mechanism separation.

## Kill Bars (frozen)

**K-R1 (procedure learning routes + works):** L1 and L3 trace
PROC_LEARN with reasons; slot 0 applies `hello`->`olleh`;
slot 1 applies `hello`->`ooooo`. If any route is wrong or any
application fails: H-ROUTER KILLED.

**K-R2 (causal learning routes + works):** L2 traces CAUS_LEARN;
`cpredict(1,0,0)` yields low pressure; `cpredict(0,0,0)` yields high
pressure. If route wrong or predictions wrong: H-ROUTER KILLED.

**K-R3 (queries route + work):** Q1 traces PROC_QUERY with both slot
outputs correct; Q2/Q3 trace CAUS_QUERY with correct predictions.
If any route or output wrong: H-ROUTER KILLED.

**K-R4 (ambiguity withholds):** A1..A4 all trace WITHHOLD with reasons;
zero misroutes. If any ambiguity probe is routed to a mechanism:
H-ROUTER KILLED.

**K-R5 (no regression):** The committed `integ_learn.zag` (explicit
prefix v1), recompiled from source, still passes its 5/5. The new
router is additive. If the original fails: H-ROUTER KILLED.

## What Success Looks Like

All 5 kill bars PASS. Type-level routing is computed from structure,
every decision carries an inspectable trace, ambiguity withholds, and
the original capability is intact.

## What Failure Looks Like

Any kill bar FAIL -> H-ROUTER KILLED, with the failing bar and the
misroute or misprediction documented.

## Predicted Outcome

**Prediction:** K-R1..K-R5 PASS. The structural shapes of the four
item kinds are disjoint by construction, so the main risk is parser
bugs, not architectural ambiguity.

**Falsification:** A misroute on a frozen item, or a wrong
mechanism outcome after a correct route, kills the hypothesis.
