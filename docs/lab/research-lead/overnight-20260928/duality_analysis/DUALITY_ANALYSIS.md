# FACT/MAP Duality Analysis

**Status:** ANALYSIS ONLY. No source edits, no implementation.
**Source:** frozen `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag` (1591 lines, read-only).
**Date:** 2026-10-01.

## 1. Precise characterization of the duality

### 1.1 What a FACT is (structurally)

Tag `T_FACT = 1` (source line 79). Node layout:

| Field | Content |
|---|---|
| 0 | tag = 1 |
| 20 | s (subject) |
| 24 | r (relation) |
| 28 | o (observed answer value) |
| 32 | creation clock |

Written by `write_node(W,n,s,r,o,hg(W,0))` in both teach paths. A FACT is a stored (s, r) -> o triple. It carries no executable content. Its answer is inert data.

### 1.2 What a MAP is (structurally)

Tag `T_MAP = 20` (source line 83). Node layout (from `promote_graph`, lines 533-545):

| Field | Content |
|---|---|
| 0 | tag = 20 |
| 4 | r (relation) |
| 8 | s (subject) |
| 12 | -1 (unused) |
| 16 | -1 (unused) |
| 20 | graph root (node id of executable 4-op ISA graph; 0 if none) |
| 24 | promo index (header clock at promotion) |
| 28 | answer (cached execution result) |
| 32 | 0 |

Note the field transposition: FACT stores s at field 20 and r at field 24; MAP stores r at field 4 and s at field 8. The two types do not even agree on where (s, r) live. Any unified lookup must handle both layouts or migrate one.

A MAP is a promoted executable graph plus a cached answer. It carries executable content (the graph cells, tags 101-104, linked via ET_SEQ) and provenance.

### 1.3 Creation path divergence

| | FACT | MAP |
|---|---|---|
| External observation | `ev_teach` (line 297): clock tick, decay, ctx_push, alloc, ET_PRO self-edge, ET_REF chain to previous FACT, event log | never |
| Internal teach | `ev_teach_in` (line 310): alloc, ET_PRO self-edge only; no decay, no context, no chain, no log | n/a |
| Trial success | via `ev_teach_in` shadow (see 1.5) | `promote_graph` (line 533): alloc, write layout, ET_COR self-edge (clocked), ET_SUP self-edge, ET_USE self-edge, ET_DEP edges to licensing facts |
| Statistical shortcut | via `ev_teach_in` shadow | `bootstrap_miss` (line 763): alloc, ET_COR self-edge, ET_SUP self-edges, ET_USE self-edge; root = 0 (no graph); then `ev_teach_in` shadow |

Two facts matter. First, every MAP creation is accompanied by a FACT creation (the shadow teach), but no FACT creation is accompanied by a MAP. The coupling is one-directional. Second, `bootstrap_miss` creates MAPs with root 0: a MAP that is structurally a FACT with extra self-edges and no executable. The degenerate unified case already exists inside the codebase, unnamed.

### 1.4 Query path divergence

This is the sharpest form of the duality.

- FACT query path: `activate` (line 140). Scans all live nodes for `ng(W,n,0)==1` (hardcoded type check), matches (s, r) on fields 20/24, excludes superseded, returns max-bid. First stage of `ev_query` (line 813). This is the only exact-recall path in frozen TNN-2.
- MAP query path: none exists in frozen TNN-2. No function scans for tag 20 to answer a query. MAPs are written by promotion, revised by contradiction, executed by the test harness (line 1281-1289 does an explicit tag-20 scan), and executed by `t2_try_verify`/`t2_revise_graph` during construction and repair. They are never read to answer a question.

The reuse experiment (`ea8fc0ac1`) added a MAP-first scan to `ev_query` on an unfrozen variant: exact (s, r) match on MAP fields 8/4, execute root, return answer. That is a second lookup path, not a unified one. The audit correctly notes the duality persists.

Consequence: in frozen TNN-2, derived executable knowledge is write-only with respect to questioning. The system can construct a procedure, promote it, revise it, and never once consult it when asked. The shadow FACT (section 1.5) is what actually answers.

### 1.5 The shadow problem, stated precisely

`promote_graph` line 543: `ev_teach_in(W,s,r,ans)` executes immediately after the MAP node is created. This inserts a FACT with the same (s, r) and the promoted answer.

On the next query for (s, r), `ev_query` calls `activate`, which finds the shadow FACT (it is the most recent, carries an ET_PRO protection edge, and bid favors evidence-rich nodes). The MAP is never consulted. The procedure the learner just built is dead on arrival as a cognitive resource; only its output survives, as a memorized triple.

The shadow is load-bearing in one respect: it is what makes promoted knowledge retrievable at all in frozen TNN-2. Deleting it without adding a MAP read path (as the reuse variant did both together) would make promotion write-only in the strong sense: knowledge that can never be recalled.

### 1.6 Invariants unique to each type

FACT-only invariants:
- Bid-ranked recall. `bid` counts ET_DEP (1), ET_SUP (2), ET_USE (6), ET_CFM (7) evidence minus ET_CON (3) contradictions, plus guide-propagated evidence via ET_MEM (10) edges. MAP self-edges (ET_SUP, ET_USE) would inflate this count if MAPs entered the same scan; the type check in `activate` currently prevents that.
- Decay protection. ET_PRO (9) self-edges with clocks, decremented by `decay` on every external teach/query/observe/act. FACTs from `ev_teach_in` get protection but no decay trigger on their own creation.
- ET_REF (4) chaining. `ev_teach` links each new FACT to the previous FACT, forming a temporal chain. `ev_teach_in` facts (including shadows) are not chained.
- Supersession. ET_CON (3) self-edges mark superseded facts; `activate` excludes them; `is_superseded` scans for them.

MAP-only invariants:
- Executable root. Field 20 points to a graph of 101-104 cells. `t2_exec` interprets it. No FACT has this.
- Provenance. ET_DEP (1) edges from MAP to each licensing FACT. `revise_on_contradict` uses these to find MAPs affected by a contradicted fact. This is the revision substrate's addressing scheme.
- Standing. `map_standing` computes ET_SUP minus ET_CON over post-promotion edges. Currently computed but never read (dead signal, per audit).
- In-place answer rewrite. `t2_revise_graph` writes the corrected answer to field 28 and contradicts the old shadow FACT. The MAP's answer field is mutable; a FACT's answer field is never rewritten (contradiction creates a new FACT and supersedes the old).

Shared substrate (not duality): both are nodes in the same 1024-node store, subject to the same allocator, the same eviction economy (`evict_node` scans all live nodes regardless of type), and the same edge types.

## 2. The unified node

### 2.1 Functional definition

One knowledge node type holding (s, r, answer) plus an optional executable root. Concretely: the FACT layout (fields 20/24/28 for s/r/o) extended with an executable-root field (currently MAP field 20) and a provenance marker. A node with no root is today's FACT. A node with a root is today's MAP. The `bootstrap_miss` root-0 MAP is already this form.

Query becomes one lookup: exact (s, r) match over knowledge nodes, then execute the attached graph if present, else return the stored answer. The shadow disappears because there is no separate FACT to shadow the MAP: the promoted answer and the procedure are fields of one node.

### 2.2 What happens to the shadow problem

It dissolves structurally. The shadow existed because promotion created two nodes where one would do: the procedure (MAP) and its memoized output (FACT). Under unification, `promote_graph` creates one node: answer cached in field 28, graph in the root field. A re-query finds the node, sees a root, and executes it. There is no race between a FACT lookup and a MAP lookup because there is one lookup.

The behavioral question the shadow currently answers silently, "return the cached answer or re-execute the graph," becomes explicit. Under unification this must be decided: always re-execute (costly, but exercises the procedure and detects staleness), return cached unless contradicted (cheap, but the graph is decorative), or re-execute on a schedule or on evidence change. This is a semantic decision, not a structural one. The current architecture never makes it because the shadow always wins.

### 2.3 What breaks, by subsystem

**Lookup and ranking (`activate`, `bid`).** The hardcoded `ng(W,n,0)==1` check widens trivially. The non-trivial part is `bid`: MAP self-edges (ET_SUP, ET_USE, ET_COR) were never meant as recall evidence, but under one scan they enter the evidence count. A unified node with provenance edges would outrank plain facts systematically, or the bid formula needs edge-type semantics that distinguish "this node has a procedure" from "this node has evidence." Either the formula changes (behavioral) or ranking distorts (behavioral). There is no behavior-preserving option; the current ranking never saw these edges.

**Teaching (`ev_teach`, `ev_teach_in`).** The two teach paths differ in bookkeeping (decay, context, ET_REF chain, log). Under unification, promotion must pick one lifecycle. If promoted nodes get the full `ev_teach` bookkeeping, every promotion triggers decay and context push, changing the retention economy. If they get the minimal path, promoted knowledge never enters the ET_REF temporal chain, preserving a subtle second-class status. The duality currently hides this choice inside the shadow: the MAP gets minimal treatment, the shadow FACT gets minimal treatment too (via `ev_teach_in`), and only external observations get full treatment.

**Construction (`t2_gather`, `inc_fill`, `t2_gather_sum`, `t2_rels`, `t2_chain`).** All gather helpers hardcode the type-1 check. If unified knowledge nodes (including ones with executables) become visible to gather, construction can see prior procedures. That is barrier 1 of the transfer analysis, and breaking it here is a behavioral change with the honesty properties the barrier-break design analyzed: visibility without usability until retrieval and rebinding exist. If gather keeps a "facts only" filter, the duality persists under a new name (a flag instead of a type). The filter has to live somewhere; moving it from a type check to a field check is not unification.

**Revision (`revise_on_contradict`, `t2_revise_graph`).** Revision addresses MAPs by scanning for tag 20 plus ET_DEP provenance links to the contradicted fact. Under unification, the scan becomes "knowledge nodes with a non-null root and ET_DEP links to the fact." The provenance edges are the real discriminator, not the tag. This is arguably cleaner, but `t2_revise_graph` also reads the MAP field layout (root at 20, s at 8, r at 4, answer at 28) which differs from the FACT layout (s at 20, r at 24, o at 28). Field migration is required: one layout must win. The FACT layout (s/20, r/24, o/28) is read by more call sites (`activate`, `ev_observe`, gather helpers, `ev_teach`); the MAP layout would need to move.

**Eviction (`evict_node`, `rec_evict`).** Eviction is type-agnostic (scans all live nodes), so it does not break mechanically. But protection patterns differ: MAPs carry clocked ET_COR self-edges and ET_USE self-edges that `is_prot` does not count (it counts ET_PRO only). Under unification, the protection story for procedure-bearing nodes needs a decision: does holding a procedure protect a node, and for how long? Currently the shadow FACT's ET_PRO edge is what protects promoted knowledge from eviction; the MAP itself is protected only incidentally.

**Execution entry points (`t2_try_verify`, `t2_exec`, test harness).** `t2_try_verify` executes candidate roots during the trial; it does not care about node types. The test harness (lines 1281-1289) does an explicit tag-20 scan to find a MAP for execution tests; it would need updating. This is test code, not cognition, but it is frozen-test code, so the change has protocol implications.

**Standing (`map_standing`).** Dead signal today (no reader). Under unification, if standing is ever given a reader (H3-lite Node 3 is a candidate), its ET_SUP/ET_CON counting must be re-examined: those edge types would now be shared with the general evidence economy instead of living in a MAP-private namespace.

## 3. Compression or redesign: honest assessment

The mechanical changes (one tag, one layout, one lookup scan, provenance-as-discriminator) are compression: same capabilities, less machinery, roughly the audit's estimate for Rank 2.

The semantic changes are redesign, and they are the larger part:

1. Execute-vs-cache policy (section 2.2). Frozen TNN-2 never decides; the shadow decides by existing. Unification forces the decision.
2. Bid semantics for procedure-bearing nodes (section 2.3, lookup). The evidence economy was calibrated, implicitly, on facts. Adding a new edge-bearing population changes ranking behavior with no neutral default.
3. Lifecycle choice for promoted nodes (section 2.3, teaching). Full vs minimal bookkeeping changes the retention economy either way.
4. Gather visibility (section 2.3, construction). This is a transfer-architecture decision smuggled inside a compression change.

A unification that tried to be pure compression, preserving every behavior bit-for-bit, would need to replicate the shadow's effects (cached answer wins, MAP never consulted) inside one node, which is the duality reimplemented as a flag. That is not unification; it is renaming.

Honest verdict: unification is a redesign with a compression-shaped core. The structural merge is the easy part. The behavior that the duality currently determines by accident (shadow wins, MAPs invisible to recall, procedures never re-executed) must be re-determined by choice. Those choices are where the cognitive architecture actually lives, and they are currently made by nobody.

## 4. Relation to C0-D (cognitive reuse)

C0-D requires: the invented structure must improve transfer, prediction, procedure learning, causal inference, memory, planning, or sample efficiency. Existence alone is insufficient.

Unification resolves the shadow problem structurally: promoted procedures become first-class recallable knowledge instead of write-only artifacts with memoized outputs. This removes a structural blocker on reuse. A procedure that can never be found can never be reused; unification makes it findable by construction.

But unification does not satisfy C0-D, for two reasons.

First, findability is not reusability. The transfer experiment's barriers 3 (exact (s, r) lookup) and 4 (literals baked in, no rebinding) persist unchanged under unification. A unified node retrieved by exact (s, r) with baked-in literals is exactly as non-transferable as today's MAP. Unification changes who can see the procedure; it does not change what can be done with it once seen.

Second, C0-D demands demonstrated improvement on a cognitive dimension. Unification is an architectural enabler. The reuse experiment's MAP-first variant already demonstrated mechanical reuse (same-(s, r) re-execution, no shadow FACT) without unification. What unification adds over that variant is principled defaultness: reuse becomes what the architecture does rather than what a researcher-added scan does. That is a genuine advance in learner-authority terms (the learner's structures are first-class citizens of the query path), but the reuse events themselves still require the retrieval and rebinding machinery that barriers 3 and 4 name.

Precise relation: unification is necessary for C0-D's "procedures as reusable knowledge" reading, and orthogonal to C0-D's "demonstrated cognitive improvement" reading. It moves the blocker from structural (invisible procedures) to functional (visible but unusable procedures), which is progress of exactly the kind the barrier-break design targeted: making the binding constraint empirically accessible.

## 5. Standing architectural metric (this analysis)

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 0 (analysis; the duality itself is researcher-owned) |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 |
| SOURCE-ENUMERABLE FORMS | 3 assemblers (unchanged) |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 |
| REUSE EVENTS | 0 |
| REVISION EVENTS | 0 (analysis) |
| COGNITION LINES | 0 added, 0 modified (read-only) |
| MODES | 0 |
| BRIDGES | 1 (ev_query router, unchanged) |
| HANDLERS | 0 |
| SEMANTIC CASES | 0 |

## 6. Explicit non-claims

- This analysis does not establish that unification is correct, only what it would require and where the non-mechanical decisions lie.
- Unification does not establish SUF, L3, C0-D, or any frozen-battery gain. No behavior was changed and none was measured.
- The field-transposition finding (FACT s/20 r/24 vs MAP r/4 s/8) is reported as found in source; it constrains any migration but does not by itself recommend which layout wins.
- The `bootstrap_miss` root-0 MAP is noted as the existing degenerate unified case; this is an observation about the code, not a claim that bootstrap was designed as unification.
- No implementation is proposed. Section 2 is a functional characterization for gap analysis, not a work plan.
