# PREREG_ROUTER2: Learned Routing Predicates (H-ROUTER2)

**Status:** FROZEN. No edits after this commit except an explicit amendment
record. Implementation must strictly follow this document.

**Date:** 2026-09-29
**Parent result:** H-ROUTER SURVIVES (structure-inferred routing, but predicates
authored by the researcher).
**Question (NQ2):** Can the learner induce its own routing rules from
labeled-then-unlabeled experience, using the causal learner's SPLIT machinery?

## Hypothesis H-ROUTER2

A learner exposed to a MARKED curriculum (input line + task-type mark) will
induce routing predicates as entries in the causal learner's hypothesis store,
via the validated SPLIT machinery (single-variable equality splits, chained
via parent/child inheritance). In the UNMARKED phase the induced predicates
route novel inputs to PROC_LEARN / CAUS_LEARN / PROC_QUERY / CAUS_QUERY /
WITHHOLD, matching the authored H-ROUTER decisions.

## Design (frozen)

**Machinery:** The causal learner from
`docs/lab/research-lead/overnight-20260928/causal/causal_learn.zag` is copied
VERBATIM (all functions except `main()`). No modifications. One pre-seeded
unconditional entry for action ROUTE=7.

**Episode encoding (frozen):**
- State vars are input-structure FEATURES, computed without any task-type
  knowledge (authored feature extractors, disclosed below; the ROUTING RULES
  are what must be learned):
  - s0 = pair_kind: 0 = no `>` in any segment; 1 = every non-empty segment is
    str>str (exactly one `>`, both sides non-numeric); 2 = every non-empty
    segment is iii>ii (left 3 ints, right 2 ints); 3 = mixed/other.
  - s1 = nseg: segment count split on `;`, capped at 9. Empty line -> 0.
  - s2 = query_kind (only meaningful when nseg==1 and no `>`): 1 = bare
    string; 2 = 3-int tuple; 3 = other single field; 0 = nseg!=1 or has `>`.
- Action a = 7 (ROUTE), constant.
- Next state ns = (task_code, 0, 0). Task codes are DELIBERATELY offset so no
  numeric coincidence with feature values can masquerade as learning:
  WITHHOLD=10, PROC_LEARN=11, CAUS_LEARN=12, PROC_QUERY=13, CAUS_QUERY=14.
- The mark in the curriculum phase IS ns0 (the supervised outcome). In the
  test phase marks are removed and `predict()` is called on features.

**Marked curriculum (frozen, in this order):**

| # | line | features (s0,s1,s2) | mark |
|---|---|---|---|
| 1 | `abc>cba;xy>yx` | (1,2,0) | PROC_LEARN |
| 2 | `ab>ba;cd>dc;ef>fe` | (1,3,0) | PROC_LEARN |
| 3 | `a>b;c>d;e>f;g>h` | (1,4,0) | PROC_LEARN |
| 4 | `mn>nm;op>po` | (1,2,0) | PROC_LEARN |
| 5 | `0,0,0>0,1;1,0,0>1,0` | (2,2,0) | CAUS_LEARN |
| 6 | `1,1,0>1,0;0,1,1>0,0;2,0,1>2,1` | (2,3,0) | CAUS_LEARN |
| 7 | `5,5,5>5,4;6,6,6>6,5;7,7,7>7,6;8,8,8>8,7` | (2,4,0) | CAUS_LEARN |
| 8 | `hello` | (0,1,1) | PROC_QUERY |
| 9 | `world` | (0,1,1) | PROC_QUERY |
| 10 | `1,0,0` | (0,1,2) | CAUS_QUERY |
| 11 | `0,0,0` | (0,1,2) | CAUS_QUERY |
| 12 | `ab>ba` | (1,1,0) | WITHHOLD |
| 13 | `0,0,0>0,1` | (2,1,0) | WITHHOLD |
| 14 | `hello;world` | (0,2,0) | WITHHOLD |
| 15 | `` (empty) | (0,0,0) | WITHHOLD |
| 16 | `ab>ba;cd` | (3,2,0) | WITHHOLD |
| 17 | `123` | (0,1,3) | WITHHOLD |
| 18 | `1,2` | (0,1,3) | WITHHOLD |

Every (features -> mark) mapping is a function (no two items share features
with different marks); exact-state contradictions must not occur. If a
contradiction occurs during execution, the run is INVALID (curriculum bug),
not a learner failure.

**Predicted induction (recorded before running; not a kill bar):**
The unconditional entry will split on s0 (pair_kind), then the pair-kind
children will split on s1 (nseg) when the single-pair WITHHOLD items arrive.
The query branch will split on s2. Because splits are equality-only, the
learner is EXPECTED to induce per-(pair_kind, nseg) rules rather than a clean
`nseg>=2` threshold. Novel nseg values are EXPECTED to WITHHOLD (honest
degradation), not to route. This prediction is recorded to prevent
post-hoc rationalization; the kill bars below are what judge.

## Frozen kill bars

**K-R2A (inspectability):** PASS iff the `list_hypos` dump after the marked
phase shows routing rules as white-box entries with readable conditions and
SET effects mapping feature combinations to task codes (e.g. an entry with
cond including s0=1,s1=2 and fx SET 11 on var0). A black-box mapping, or
rules that cannot be read off the dump, FAILS.

**K-R2B (suite match):** PASS iff the learned router's route decisions match
the authored H-ROUTER decisions on ALL of:
(a) the 10 H-ROUTER suite items:
`abc>cba;xy>yx`->PL, `0,0,0>0,1;0,0,0>0,1;1,0,0>1,0;1,0,0>1,0`->CL,
`abc>ccc;xy>yy`->PL, `hello`->PQ, `1,0,0`->CQ, `0,0,0`->CQ,
`ab>ba`->W, `0,0,0>0,1`->W, `hello;world`->W, ``->W;
(b) 6 novel surface strings with seen feature combos:
`zz>yy;xx>ww` (1,2,0)->PL, `q>w;e>r;t>y` (1,3,0)->PL,
`3,3,3>3,2;4,4,4>4,3` (2,2,0)->CL, `goodbye` (0,1,1)->PQ,
`2,2,2` (0,1,2)->CQ, `xy>yx` (1,1,0)->W.
16/16 required. (Downstream task execution is unchanged from H-ROUTER and is
not re-tested; the bar is on the routing predicates.)

**K-R2C (withhold on novel ambiguity):** PASS iff ALL of these feature-novel
inputs WITHHOLD (predict returns WITHHOLD or task code 10), i.e. the learner
does not confidently misroute outside its experience:
`a>b;c>d;e>f;g>h;i>j` (1,5,0),
`1,1,1>1,0;2,2,2>2,1;3,3,3>3,2;4,4,4>4,3;5,5,5>5,4` (2,5,0),
`ab>12` (3,1,0),
`ab>ba;cd;ef>fe` (3,3,0).
4/4 required.

**K-R2D (determinism):** PASS iff 3 consecutive runs are byte-identical
(md5 of stdout).

**Verdict rule:** H-ROUTER2 SURVIVES iff K-R2A, K-R2B, K-R2C, K-R2D all PASS.
Any FAIL kills H-ROUTER2. A kill is informative: per the honest failure mode,
if single-variable equality vocabulary proves too narrow, the result is
documented as a boundary motivating vocabulary enrichment, not as a
near-miss.

## Scope notes (frozen)

- Feature extractors (`field_kind`, segment split) are authored and disclosed.
  What is learned is the mapping from features to task types. This matches
  NQ2's concrete approach ("SPLIT machinery on input-structure features").
- Pure Zag. No Python anywhere, including verification.
- No em dashes in loop documentation.
- Commit order: this prereg strictly before any implementation commit.
