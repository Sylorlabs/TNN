# PHASE 0 -- REAL BRIDGE AUDIT

Lane `ownership`. Corpus: all `.zag` under
`*/docs/lab/research-lead/overnight-20260928/**`, excluding
`build/` and `runs/`.

## 0. BASELINE COUNTS

```
files        105,673
LOC          80,991,292
experiments     987   (distinct overnight-20260928/<exp> dirs)
lanes           106
```

Name-based scan results:

```
named cognitive MODES in code          0
   (12 hits, ALL in comments asserting absence: "There is no COMPOSE_MODE...")

explicit _TO_ bridge identifiers        0
   (10 hits, ALL in comments asserting absence:
    GRAMMAR_TO_CONSTRUCTION x4, CAUSAL_TO_INTERVENTION x4, ARITH_TO_PLAN x2)
```

**The name scan finds nothing. That is the single most important
audit result.** TNN's cognitive bridges are not name-declared. They
are implemented as *input-format classification* and *implicit
fallback policy*, which is why a name grep reports a clean bill of
health on an architecture that is substantially bridged.

Name-based auditing is therefore insufficient by construction here.
Everything below was found by reading code.

---

## BR-1 -- SYNTACTIC DOMAIN ROUTER (canonical learner)

**Source**: `unified_learn.zag` (1892 LOC, canonical learner,
supersedes `bridge_learn.zag`).

1. path: `unified_learn.zag:734-800` (`route_line`, `route_name`,
   `field_kind`, `is_digit`, `find_ch`)
2. caller/callee: `route_line(line)` -> route code; callee is one of
   five procedure families selected by that code.
3. what crosses: the raw input line, decomposed into segments on
   `;`, with `>` and `,` positions inspected.
4. semantic translation: **YES.** Input shape is mapped to a
   cognitive role.
5. cognitive/domain knowledge: **YES.**
6. merely representation plumbing: **NO.**
7. deletion changes capability: **YES** -- no routing, no cognition.
8. subsumed by another generic mechanism: **NO** found.
9. active on witnessed paths: **YES**, reached from the main
   apply path.
10. candidate replacement by learned recruitment: **YES** -- learned
    typed contracts already validated on four domain pairs.
11. value of deleting: **HIGH.** Removes the researcher's authority
    to decide which cognition runs.

Source, verbatim:

```
// Route codes: 0=WITHHOLD, 1=PROC_LEARN, 2=CAUS_LEARN,
//              3=PROC_QUERY, 4=CAUS_QUERY
fn route_name(c:i32)[]u8 {
  if(c==1){return "PROC_LEARN";}
  if(c==2){return "CAUS_LEARN";}
  if(c==3){return "PROC_QUERY";}
  if(c==4){return "CAUS_QUERY";}
  return "WITHHOLD";
}
```

`route_line` classifies purely on syntax: counts `;` segments,
looks for `>` and `,`, counts integer fields. Two lines with
identical meaning but different formatting can receive different
cognitive routes, and two lines with identical formatting but
different meaning receive the same route.

**Classification: D -- cognitive bridge TNN should learn around.**
This is the top deletion priority.

---

## BR-2 -- FAILURE-TRIGGERED CONDITIONAL BRIDGE (canonical learner)

**Source**: `unified_learn.zag:423` (`bridge_apply`),
`:445` (`bridge_learn`).

1. path: as above
2. caller/callee: the candidate-application path at
   `unified_learn.zag:1043` calls `bridge_apply`; callee is one of
   two procedure slots, chosen by a learned `(pos, val)` condition.
3. what crosses: input line + learned `(pos, val)` selector ->
   which procedure executes.
4. semantic translation: **YES.**
5. cognitive/domain knowledge: **YES** -- and specifically the
   *policy* at line 11: "PROC_LEARN failure automatically triggers
   bridge induction."
6. merely plumbing: **NO.**
7. deletion changes capability: **YES.**
8. subsumed: **NO.**
9. active: **YES**, `unified_learn.zag:1043`.
10. replacement by learned recruitment: **PARTIAL.** The `(pos,val)`
    condition is already learned by search. The *decision to induce*
    is researcher policy.
11. value of deleting: **HIGH**, because it conceals discovery
    failure behind a working substitute.

Source, verbatim:

```
//   - Bridge: direct-first, then (pos,val) conditional induction
//     (from bridge_learn.zag)
//   - PROC_LEARN failure automatically triggers bridge induction.
...
// bridge_apply: evaluate condition, dispatch to correct procedure.
fn bridge_apply(...)
```

Note the known defect already recorded in the superseded copy:
**F-LEAK** -- "bridge store full leaves leaked subset procedures"
(`bridge_learn.zag` header). The bridge is not merely unnecessary,
it is a known leak source.

**Classification: D.**

---

## BR-3 -- CANDIDATE-KIND DISPATCH TAXONOMY

**Source**: `unified_learn.zag:1008`.

```
// kind: -1 = no candidate, -2 = ambiguous, 0 = proc, 1 = bridge.
```

A researcher-owned enumeration over *where a candidate came from*.
The dispatcher branches on origin rather than on the candidate's
learned properties.

**Classification: D.** Small but load-bearing: it makes "which
mechanism produced this" part of cognition.

---

## BR-4 -- COUNT RE-DERIVATION FOR NUMERIC MAPs

**Source**: `xio_adapters/xio_core.zag:95-99`, in `xio_stage_exec`,
`oty==1` branch. Present as `xio_core2.zag`,
`xio_idfix/xio_core_fixed.zag`, and in every
`ap_full_xio.zag` / `cd_full_xio.zag` assembly.

Source, verbatim:

```
let len:i32=t2_chain(W,x,rel,vv2,ff2);
if(len<2){return -999999;}
let root2:i32=t2_asm_count(W,vv2,len,ff2);
```

1. path: as above
2. caller/callee: `xio_stage_exec` -> `t2_chain` + `t2_asm_count`,
   then `t2_try_verify`.
3. what crosses: MAP identity `m` and input `x`; the output is a
   *re-derived count*, not the MAP's own value.
4. semantic translation: **YES.**
5. cognitive/domain knowledge: **YES** -- count semantics.
6. merely plumbing: **NO.**
7. deletion changes capability: **YES.** Documented: `sum(103)=15`
   is reported as `count(103)=2`, and every arm yields
   `adapters=0`.
8. subsumed: **NO.**
9. active: **YES**, on the oty-1 branch of every witnessed path.
10. replacement by learned recruitment: **BLOCKED BY LOSSINESS**,
    see below.
11. value of deleting: **HIGH**, and it is currently *wrong*.

**Root cause (the real finding).** Both aggregators emit the same
structure -- a chain of INC cells whose length *is* the number:

```
fn t2_asm_count(W,v,plen,f)   -> plen-1 INC cells
fn t2_asm_sum(W,vals,n)       -> total INC cells, total = sum(vals)
```

`promote_graph` (`composition_A/cx_core.zag:533`) persists
`field4=r, field8=s, field20=graph root, field24=promo index,
field28=answer` and DEP edges to licensing facts. **It does not
persist which aggregation produced the chain length.**

So a learned numeric MAP is *lossy*: it records the answer, not the
operation that generalizes to a new input. Therefore there is no
generic way to re-instantiate it, and `xio_stage_exec` substitutes
the one aggregator that is implemented -- count.

**This is why the bridge is not merely inelegant. The information a
generic executor would need is absent from learner state.**
A generic executor cannot fix BR-4; learner state must first retain
provenance.

**Classification: D, with a representation-loss root cause.**

---

## BR-5 -- L3 BRIDGE GENERIC CONSTRUCTORS (positive finding)

**Source**: `l3_bridge_impl/bridge.zag`, `bridge_fix_impl/bridge.zag`.

This is prior art in the *correct* direction. It **removed**:

* `diagnose()` signature enum and all branches
* `build_tree(st, sig, dp)` and three recipe branches
* `node_count(sig)` lookup
* sig-keyed `novelty_check()`

and **added** four generic operators: `op_const_leaf`, `op_split_lt`,
`op_split_eq`, `op_prune`. Every `setnode` call is inside one of the
four (M3 verified).

Status `BRIDGE-TESTED`, no SURVIVES claim.

**Classification: B -- generic interface mechanism.** This is what
deleting a bridge is supposed to produce. It is the template the
other four should be converted into.

---

## CLASSIFICATION SUMMARY

```
A. REQUIRED MACHINE PLUMBING         0 found
B. GENERIC INTERFACE MECHANISM       1  (BR-5)
C. RESEARCH SCAFFOLD / TEMPORARY     0 found
D. COGNITIVE BRIDGE TO LEARN AROUND  4  (BR-1, BR-2, BR-3, BR-4)
E. DEAD / REDUNDANT / SUBSUMED       0 found
```

## BRIDGE-COUNT BASELINE

```
explicit named bridges (_TO_ in code)     0
named cognitive modes in code             0
structural cognitive bridges (BR-1..4)    4
  of which in the CANONICAL learner       3   (BR-1, BR-2, BR-3)
generic interface mechanisms              1   (BR-5)
bridges inside the canonical learner, as
share of its dispatch surface             3 of 5 route codes are
                                          role-named; 1 of 2 candidate
                                          kinds is bridge-named
```

## CLUSTER ANALYSIS

Three of the four D-class items are the **same missing generic
property**, and the cluster is the actual finding:

> **BR-1, BR-2, BR-3 all exist because TNN lacks a generic way to
> decide which learned structure applies to a situation using that
> structure's own learned properties.**

BR-1 substitutes *input syntax* for applicability.
BR-2 substitutes *a hardcoded fallback policy* for applicability.
BR-3 substitutes *mechanism provenance* for applicability.

All three are researcher answers to one question the learner should
answer.

And the answer already exists and has been validated. Learned typed
contracts (signatures computed at runtime by scanning each MAP's own
graph for INC cells, with stage relations read from each MAP's own
DEP edges) have **PASSED on four structurally different domain
pairs** with mechanism logic unmodified:

```
navigation x aggregation      H1 PASS, H2 PASS
arithmetic    x planning      H1 PASS, H2 PASS   <-- DISPUTED, see below
causal model  x intervention   H1 PASS, H2 PASS
grammar       x construction   H1 PASS, H2 PASS
```

The contract mechanism prunes search (NOTYPE arm: 6 tries; TREAT: 3
tries) using only probe observations and zero literals.

**So the generic property is not missing. It is implemented,
validated, and simply not used by the canonical learner's router.**

---

## AUDIT FINDING: FALSE GENERALITY CLAIM

`xdomain_causal_interv/REPORT.md` and
`xdomain_grammar_construct/REPORT.md` both cite, as prior evidence:

> "Arithmetic to planning: H1 PASS, H2 PASS (mechanism logic
> unmodified)."

**That run does not exist.** The
`xdomain_arith_plan/NAMECHECK.md` records a transparent
preregistration supersession:

> "PREREG.md (aa708f552) registered a different experiment (novel
> typed-contract/value-composition mechanisms expecting success) than
> the assigned task (verbatim H1/H2/H3 ports + XIO control,
> expecting the chain-bound negative). It was SUPERSEDED
> transparently by PREREG2.md..."

In the superseded run, the `H1`/`H2`/`H3` labels denote **invention
mechanisms** (mutation, fragment recombination, chain invention), not
contracts and composition. All three were KILLED. The typed-contract
mechanism was never executed on sum-then-plan.

There is therefore a **name collision between two H1/H2 naming
schemes** across experiments, and a generality claim propagated
from a run that was replaced.

**Corrected generality statement: three real pairs, not four**
(navigation x aggregation, causal x intervention, grammar x
construction). The arithmetic x planning pair remains **untested for
contracts**, and is a live gap.

**Process failure recorded: PROCESS-FAIL (citation).** No data is
falsified; a claim of generality was overstated by citation across a
supersession boundary.

---

## WHAT THE AUDIT CHANGES

1. BORROW Phase 1 must target **BR-1/BR-2/BR-3 as one cluster**,
   because they are one missing property wearing three costumes.
2. The generic replacement already exists and is validated
   (learned typed contracts, 3 real pairs). The experiment is
   therefore not "can generic recruitment work" -- prior evidence
   says yes. It is **"can the canonical learner be made to use it,
   so the router and the bridge become unnecessary."**
3. BR-4 is a separate and harder problem (representation lossiness).
   It is queued for PHASE 10 subtraction, not Phase 3 recruitment.
4. Name-based bridge auditing is proven inadequate for this codebase
   and is retired as a method.