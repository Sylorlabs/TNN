# Bid Semantics for Procedure-Bearing Nodes

**Status:** ANALYSIS ONLY. DRAFT-NOT-FROZEN.
**Scope:** Semantic decision 2 of 4 from duality analysis `6fa7dd2ec`.
**Verdict:** BID-SEMANTICS-COMPLETE.

## 1. Current bid mechanics (frozen TNN-2, read-only)

### 1.1 The formula

`bid` (tnn2.zag:237):
```
bid(n) = evcount(n,1) + evcount(n,2) + evcount(n,6) + evcount(n,7) - evcount(n,3)
       + sum over g with type-10 edge to n of [same sum for g]
```

Edge types (tnn2.zag:59-72): 1=DEP, 2=SUP, 3=CON, 4=REF, 5=INS, 6=USE, 7=CFM, 8=SUR, 9=PRO, 10=MEM, 11=REG, 12=SEQ, 13=COR.

`evcount` counts incoming edges only (target field = n). Prior ACT bid analysis confirms the semantic: **the bid measures evidence FOR the node**. Each counted edge type is a vote: DEP/SUP/USE/CFM are +1 (supporting evidence), CON is -1 (contradicting evidence). The type-10 (MEM) inheritance lets a guide propagate its evidence weight to a linked fact.

### 1.2 Where bid is used (three sites)

1. **`activate`** (line 145): retrieval ranking. Among FACTs matching (s,r), returns max-bid. Hardcoded type check `ng(W,n,0)==1` excludes MAPs.
2. **`evict_node`** (line 259): victim selection. Scans all live unprotected nodes, evicts min-bid. Ties broken oldest-first (strict `<`). MAPs are included here.
3. **`ev_act`** (lines 872, 884): guide selection. Max-bid among context-matching guides (type-2 nodes) and their neighbors.

### 1.3 What a high bid means for a FACT

For a FACT, the bid is a **dynamic evidence meter**. The fact lifecycle (forgetting analysis `2726baf74`):

- Created via `ev_teach_in`: self USE edge (type 6). Birth bid = 1.
- Query hit (`ev_query` → `activate` finds it): another self USE edge. +1 per hit.
- Observe match (`ev_observe`, stored == observed): self CFM edge (type 7). +1.
- Observe contradiction: self CON edge (type 3). -1, plus revision triggered.
- Guide DEP link: +1 per dependent.

A high-bid FACT is one that has been frequently retrieved, confirmed by observation, depended upon by other structures, and rarely contradicted. The bid is a proxy for "this fact is useful and true," and it **changes with experience**. This is the bid working as designed.

## 2. What bid means for a MAP: a birth certificate, not a utility meter

### 2.1 MAP bid at creation

`promote_graph` (line 533-541) gives a fresh MAP:
- type-13 (COR) self-edge: not counted.
- type-2 (SUP) self-edge: +1.
- type-6 (USE) self-edge: +1.
- type-1 (DEP) edges to each of the nf source facts: these point FROM the MAP TO the facts (target = fact), so they count toward the FACTS' bids, not the MAP's.

**Fresh MAP bid = 2.** The forgetting analysis called this a "constant bid of 2" and was correct for the self-edge component.

Bootstrap MAPs (line 780-782): `cnt` SUP self-edges + 1 USE self-edge. **Bid = cnt + 1**, where cnt is the number of unanimous observations. This bid reflects the evidence count at birth, but it is still frozen thereafter.

### 2.2 MAP bid after creation: frozen

Verified by exhaustive `link_edge` scan: **no production code adds a bid-relevant edge (type 1, 2, 6, 7) targeting a MAP after promotion.** The complete inventory:

- Query hits add USE to the node `activate` returns. `activate` only returns FACTs. The shadow FACT (created by `ev_teach_in` inside `promote_graph`) absorbs every query hit. The MAP gets nothing.
- `ev_observe` matches add CFM to the activated FACT, not the MAP.
- `contradict_map` (line 579) adds a type-3 self-edge to the MAP: -1 per contradiction. This is the ONLY post-creation bid change a MAP can receive.
- MAP executions (trial verification, harness) add no edges.
- No guide ever links type-10 to a MAP in the frozen code.

**MAP bid = 2 - (contradictions).** It is a birth certificate recording "I was promoted" minus "I have been contradicted." It does not change when the MAP is executed, when the MAP succeeds, when the MAP is ignored, or when the MAP's answer is consumed via the shadow FACT.

### 2.3 The semantic mismatch

The bid was designed as "evidence FOR the node." For a FACT, the node IS a truth claim, so evidence-for maps cleanly onto usefulness and truth. For a MAP, the node is a **procedure plus a truth claim** (the answer field), and the bid conflates them:

- The SUP self-edge (+1) records a historical event (promotion happened), not ongoing evidence.
- The USE self-edge (+1) is added at creation, not on each use. Its name is a lie: it does not mean the procedure was used.
- The DEP edges (to source facts) represent construction provenance, not evidence for the MAP.

A MAP that has been successfully "used" 100 times (via its shadow FACT) has the same bid as one never touched. A MAP whose procedure is subtly wrong but never contradicted keeps bid 2 forever. **The bid measures nothing about procedural quality, procedural utility, or procedural freshness.**

## 3. The procedure problem

### 3.1 Should a MAP's bid reflect procedural utility or node connectivity?

It currently reflects neither. It reflects a constant plus contradiction count. If it must reflect one:

- **Node connectivity** is what the formula computes, but for MAPs the connectivity is degenerate (two self-edges). Connectivity-based bid for a procedure is meaningless because the procedure's value is in its execution behavior, not its graph position.
- **Procedural utility** is what the bid SHOULD reflect if it is to serve eviction and (under unification) retrieval. But procedural utility requires execution feedback, which does not exist: MAPs are never executed at query time (execute-vs-cache analysis `7186294cd`: "MAPs are closed replays"), and trial/harness executions write no edges.

The honest answer: with the current architecture, a MAP's bid **cannot** reflect procedural utility because no information about procedural utility is ever recorded. Any formula change that claims to measure utility would be theater (a number that moves without a causal basis).

### 3.2 Do MAP self-edges inflate bid meaninglessly?

Yes, in two senses:

1. **Absolute inflation:** A newborn MAP (bid 2) outranks a newborn FACT (bid 1) in any hypothetical unified scan, for no reason other than the promotion ceremony adding two self-edges. The duality analysis flagged exactly this: "MAP self-edges (ET_SUP, ET_USE) would inflate this count if MAPs entered the same scan."

2. **Semantic inflation:** The self-edges borrow the names and weights of evidence types (SUP = "supported," USE = "used") while carrying none of their semantics. A reader of the bid sees "this node has support and use" when the truth is "this node was created once." This is the same class of problem as the theater audit's findings: a signal that looks informative but isn't.

The bootstrap MAP is the sharper case: its `cnt` SUP self-edges DO encode real evidence (unanimous observations), so its bid of cnt+1 is semantically honest at birth. But it freezes, so a bootstrap MAP with 6 unanimous observations from 200 events ago outranks a fact confirmed yesterday. Frozen evidence is stale evidence.

### 3.3 If a MAP is never executed at query time, what does its bid actually measure?

It measures **retention priority under the current eviction policy**, nothing more. In `evict_node`, bid 2 means "evict me after the bid-0 graph cells and literals, before the bid-1+ facts." The MAP's bid is a position in the eviction queue, assigned at birth and adjusted only by contradiction.

This is why the white-box inventory found fossil MAPs: bid 2 is high enough to survive the zero-bid sweep that kills the MAP's own graph cells (bid 0), producing a zombie (header survives, body evicted). The bid system is working exactly as specified; the specification is what creates fossils. The eviction-corruption analysis (`986c52fdc`) classified this as a design flaw, and the bid semantics are part of that flaw: **a retention priority that cannot see structural membership will always fossilize composite structures.**

## 4. The unified bid problem

If FACT and MAP merge into one knowledge node (fact + optional procedure), the bid must serve both populations. Three options, none neutral:

### Option A: Keep the formula, widen the scan

Remove the `ng(W,n,0)==1` check in `activate`. Unified nodes compete on the existing formula.

- Consequence: every unified node with a procedure gets +2 (SUP + USE self-edges) over a plain fact with the same evidence. Procedure-bearing nodes systematically outrank plain facts in retrieval, regardless of whether the procedure is any good.
- The ranking distortion is behavioral (different answers returned), not just cosmetic.
- Verdict: rejected. The duality analysis reached the same conclusion: "there is no behavior-preserving option."

### Option B: Two-component bid

`bid(n) = evidence_bid(n) + procedure_bid(n)`, where evidence_bid uses the current formula and procedure_bid uses a new execution-feedback signal.

- Requires: an execution feedback loop (currently nonexistent), a definition of procedural success (currently only "ran without error," which the V2-hole analysis showed is vacuous), and a weighting between the components (researcher judgment, treadmill risk).
- Verdict: the honest long-term direction, but every prerequisite is missing. Building it now would be decision-before-evidence (the T1/T2 theater pattern).

### Option C: Redefine bid as retention-only, separate retrieval ranking

Admit that one number cannot serve both eviction and retrieval for heterogeneous nodes. Keep bid for eviction (with structure-aware semantics per the eviction-corruption fix options), and define a separate retrieval score.

- This is the deepest change: it admits the current architecture conflates two functions in one number.
- Verdict: correct but large. It interacts with the protected-core ISA question (what computes the retrieval score?) and is TNN-3 scope.

### What the unified bid would need (information requirements)

Regardless of option, a bid that reflects cognitive utility for procedure-bearing nodes needs:

1. **Execution feedback:** MAP executions must be observable and must write edges (or equivalent). Currently zero executions write anything.
2. **Success signal:** "The procedure computed the right answer" must be distinguishable from "the procedure ran." Currently only the latter exists, and the V2-hole analysis showed even the repair path doesn't check correctness.
3. **Freshness:** Evidence must decay or be timestamped. Currently USE edges are permanent; a USE from event 10 counts the same as one from event 400.
4. **Component separation:** "This is true" evidence and "this is useful" evidence must be distinguishable in the edge types, or the formula must take node kind into account.

None of these exist. The unified bid is blocked on the same missing machinery as learner-internal verification, execute-vs-cache policy, and procedural utility measurement. They are one problem, not four.

## 5. Gap analysis: what is missing for bids to reflect cognitive utility?

Ranked by dependency:

1. **Execution writes evidence.** The single highest-leverage change. If MAP executions (trial, query-time, revision) wrote USE/CFM edges to the MAP, the bid would become dynamic for procedures. Blocked on: the execute-vs-cache accident (MAPs never execute at query time) and the closed-replay finding (execution cannot detect staleness).

2. **Correctness signal distinct from execution signal.** A procedure that runs and a procedure that is right must write different edges. Blocked on: learner-internal verification (no correctness substitute exists).

3. **Evidence freshness.** Permanent USE edges mean ancient history outvotes recent experience. The `decay` function exists but only touches PRO edges (type 9), not the bid-counted types. Extending decay to bid edges is a small change with large behavioral consequences (and would need a prereg).

4. **Learner-owned bid weights.** Currently every edge type counts 1 (CON counts -1). The forgetting analysis identified this as researcher-fixed criterion #3. A learner that cannot change what counts as evidence cannot learn what matters.

5. **Structure-aware bid.** The bid is per-node; utility is per-structure. The eviction-corruption analysis showed the fix direction: bid inheriting structural membership. Until then, any per-node bid will fossilize composites.

## 6. Standing architectural metric (this analysis)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (analysis only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: all (no new forms proposed)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 added
- MODES / BRIDGES / HANDLERS / SEMANTIC CASES: 0 / 0 / 0 / 0

## 7. Relation to the other three semantic decisions

The duality analysis named four semantic decisions for unification. This analysis (decision 2) is downstream of decision 1 (execute-vs-cache):

- If execution never reads state (closed replay), execution feedback cannot carry freshness or correctness information, so the unified bid cannot be built on execution. Decision 2 is blocked on decision 1's resolution.
- Decision 3 (lifecycle bookkeeping: full vs minimal teach) determines what edges a unified node is born with, hence its birth bid. A unified node born with full bookkeeping starts with a different bid than one born minimal, for the same knowledge.
- Decision 4 (gather visibility) determines whether procedure-bearing nodes participate in construction, which determines whether they accumulate DEP edges, which feeds the bid.

The four decisions are not independent. They are facets of one question: **what is a unit of knowledge in TNN, and how does the system know it is valuable?** The current answer is "a node, and by counting its edges." That answer was designed for facts. It does not survive contact with procedures.
