# Plan Constructor Analysis

**Status:** ANALYSIS-COMPLETE (read-only white-box, frozen TNN-2 build `f4de7ff46`).
**Verdict:** PLAN-CONSTRUCTOR-ANALYSIS-COMPLETE.
**Question:** Frontier backlog Q13. Micah framing: "composition as one
execution problem with the plan constructor as the missing piece."

This document inventories what TNN-2 composes today, defines the plan
constructor functionally, states the gap, and relates it to SUF. It does
not design the implementation.

---

## 1. Inventory: composition-adjacent machinery in frozen TNN-2

All line references are to `tnn2_build/tnn2.zag` (1591 lines).

### 1.1 What composes multi-step structures today

Three researcher-authored assemblers build executable graphs from
gathered materials:

- `t2_asm_chain` (line 363): chain graph. Guard each link
  (v[j] to v[j+1]), set on match. SEQ-linked guard/set pairs.
  Provenance edges (type 1) to the licensing facts.
- `t2_asm_count` (line 382): count graph. Same chain skeleton plus an
  INC cell per link, then a MOVE r0 from r1 epilogue so the count is
  the output.
- `t2_asm_sum` (line 398): sum graph. Unrolled INC cells for the subset
  total. Computed at assembly time: the total is baked in as a literal
  run of INC cells, not computed at execution time.

The trial driver `t2_trial` (line 586) is the only caller:

1. Gather materials from the fact store:
   - `t2_gather` (442): BFS paths from s, depth 1..4, cycle-free.
   - `t2_gather_sum` (474): direct fact values of s.
   - `t2_chain` (428) + `t2_rels` (485): per-relation value chains.
2. Instantiate candidates, one assembler family at a time, in a fixed
   researcher-set order: chain (k=2..4), then sum (subsets, descending
   size), then count (per relation), then chain k=1 fallback.
3. Verify each candidate by execution: `t2_try_verify` (497) runs
   `t2_exec` (412) on a fresh frame against the expected answer.
4. Promote the first verifier: `promote_graph` (533) allocates a MAP
   node (tag 20), links the graph root, and (in frozen TNN-2) also
   teaches the exact answer as a shadow FACT.

Compositional facts about this pipeline:

- The structural form of every candidate is fully determined by which
  of the 3 templates fires and which gathered materials fill its slots.
  Template choice order is researcher-fixed.
- Candidates are composed from FACTS, never from existing MAPs. No
  candidate ever embeds, calls, or chains a previously promoted MAP.
- Verification is execution against a supplied expected answer
  (`expected` parameter). In masked/sealed runs the expected value comes
  from the evaluator harness, not from the learner.

### 1.2 Where the "plan" lives before execution

There is no persistent plan object distinct from the MAP:

- Candidate graphs are built in freshly allocated cells (transient).
  They exist only during the trial loop.
- The candidate is executed on a fresh frame via `t2_exec`.
- On verification success, `promote_graph` persists the graph as a MAP
  (tag 20) with provenance edges. The plan IS the MAP after promotion.
- On verification failure, the candidate cells are abandoned (unreclaimed
  garbage under the node budget; see transfer analysis `475c57e23`).

So "plan before execution" = transient candidate cells during trial.
There is no staged, inspectable, revisable plan representation that
persists independently of the promoted MAP.

### 1.3 Adjacent machinery that is NOT a plan constructor

- `ev_act` (859): selects ONE action among candidate guides by
  directional bid. Single-step selection, not multi-step composition.
  The guides themselves are single actions (bootstrap: `miss_inquire`
  builds one guide per uncertainty).
- `miss_inquire` (795): builds a single guide node linked to
  POLICY_ROOT. No sequencing of guides.
- `execute` (192): the 4-op ISA interpreter (MOVE/BRANCHEQ/INC/DEC
  over SEQ edges). It executes plans; it does not build them.
- `t2_revise_graph` (706): surgical revision of one stale step.
  Repairs a plan; does not compose one.
- `bootstrap_miss` (763): P-INV invariance bootstrap. Memorizes a
  repeated value as a MAP. No composition.

Summary: TNN-2 has construction (trial over 3 templates), execution
(4-op ISA), revision (surgical step replacement), and single-step
action selection. It has no mechanism that takes a goal plus a set of
existing structures and returns a novel composed executable graph.

---

## 2. Functional definition of the plan constructor

### 2.1 Inputs

1. **Goal specification.** A representation of what is to be achieved,
   distinct from a (subject, relation) query key. Minimal form: a
   desired end state expressed in the same vocabulary the structures
   operate over (slots, values, relations). TNN-2 has no goal
   representation; its closest analog is the (s, r, expected) triple,
   where `expected` is supplied by the harness, not the learner.
   A genuine constructor needs the learner to originate or adopt the
   goal (cf. H2 key question: learner-internal criterion).
2. **Available structures.** The set of existing MAPs/procedures the
   constructor may compose: their input/output contracts (which slots
   they read, which they write, under what guard conditions they apply)
   and their provenance. TNN-2 MAPs carry (s, r, root, answer) but no
   machine-readable contract beyond the (s, r) key and the executable
   root.
3. **Constraints.** Resource bounds (node budget, execution step budget),
   and any ordering or safety constraints. The 1000-step execution cap
   in `execute` is a constraint of this kind, but it is global and
   researcher-fixed, not per-plan.

### 2.2 Output

One executable graph in the existing 4-op vocabulary (MOVE, BRANCHEQ,
INC, DEC over SEQ edges), rooted at a node the existing `execute` can
run. This is the One-System Rule requirement: the composed plan must be
the same executable graph type as procedures and causal rules, not a
second plan language. The output must be verifiable before execution
(see 2.4) and promotable as a MAP on success.

### 2.3 What makes it general (not task-specific)

- The constructor's search is over **structure compositions**, not over
  a researcher-enumerated template menu. Adding a fourth assembler for
  a new benchmark is the treadmill; a constructor is general only if
  new plan shapes arise from combining existing structures in ways the
  source did not enumerate.
- The composition operators (sequencing, guarding, value passing
  between sub-plans) must be domain-neutral: the same operators compose
  arithmetic plans and navigation plans.
- Goal-directedness: construction is guided by reducing the distance
  to the goal (however represented), not by exhaustively trying
  templates in a fixed order until the harness-supplied expected answer
  matches. `t2_trial`'s fixed family order with harness verification is
  the anti-pattern: it is search, but researcher-ordered search toward
  a researcher-supplied target.

### 2.4 Verification before execution

The constructor must answer, before running the plan in the world:
does this composition plausibly achieve the goal? Options in increasing
strength:

- **Type/contract check:** output slots of step N match input slots of
  step N+1 (requires the contracts in 2.1.2).
- **Dry-run on a scratch frame:** execute the composed graph against a
  simulated or remembered state without world side effects. TNN-2's
  `t2_try_verify` is a dry-run, but against a harness-supplied expected
  answer; the constructor needs a learner-internal success criterion.
- **Sub-plan provenance:** each sub-plan was itself verified when
  learned (composition inherits verified parts; only the glue is new).

On verification failure the constructor must have a defined fallback:
backtrack to the next composition, decompose the goal differently, or
decline (report inability) rather than emit a guess. `t2_trial`
declines by returning -2; the constructor needs the same honesty at the
plan level.

---

## 3. Gap analysis

### 3.1 What is missing in TNN-2

| # | Missing piece | TNN-2 status |
|---|---|---|
| G1 | Goal representation | Absent. Queries are (s, r) keys; `expected` comes from the harness. |
| G2 | Structure contracts | Absent. MAPs are keyed by (s, r) with an opaque executable root. No input/output slot contract. |
| G3 | Composition from MAPs | Absent. Assemblers compose from FACTS only. No MAP is ever embedded in a new candidate. |
| G4 | Goal-directed search | Absent. `t2_trial` tries 3 fixed families in fixed order; direction comes from harness verification. |
| G5 | Learner-internal verification criterion | Absent. `t2_try_verify` checks against harness `expected`. |
| G6 | Persistent staged plan | Absent. Candidates are transient; only promoted MAPs persist. |

### 3.2 Minimal architectural delta (requirements, not design)

Any plan constructor for TNN must add, at minimum:

1. A **goal slot** in learner state: a persistent, learner-writable
   representation of what is to be achieved, separable from the query
   key. (Relates to H2: learner-internal criterion.)
2. **Contract metadata** on MAPs: which slots a sub-plan reads and
   writes. This is bookkeeping over existing node fields, not a new
   graph type.
3. A **composition operator set** restricted to the existing 4-op ISA
   plus SEQ wiring: sequencing two graphs, guarding a sub-plan on a
   condition, passing a value between sub-plan frames. No new opcodes
   (Alternative C: structural mutation opcodes deferred).
4. A **verification gate** with a learner-internal criterion, exercised
   through a production write path (K-H3 audit standard: a criterion
   with no exercised write path is theater).
5. A **decline path**: when no composition verifies, the constructor
   reports inability instead of emitting an unverified plan.

What it must NOT add: new modes, new bridges, new task-specific
handlers, new semantic cases, a second plan language. The standing
architectural metric applies: count researcher-owned vs learner-owned
structural decisions for every piece.

### 3.3 Relation to adjacent work

- **Composition memory (fragments):** that work asks what the
  constructor draws from (the fragment store). This analysis asks what
  the constructor IS (the process). The two meet at G2: fragments need
  contracts for the constructor to use them.
- **Reuse path (`ea8fc0ac1`):** MAP-first query execution is
  prerequisite infrastructure (a composed plan that is never executed
  is theater, same as a promoted MAP shadowed by a fact). The reuse
  result showed same-(s, r) invocation works; the constructor needs
  cross-context invocation (R4 limitation: fresh subject rebuilds
  rather than invokes).
- **H3-lite:** policy nodes move decision criteria into learner state.
  A constructor's search-order and verification criteria are exactly
  the kind of decision points H3-lite is built to relocate. H3-lite is
  diagnostic for whether criteria-in-learner-state changes behavior;
  the constructor presupposes an affirmative answer.
- **TNN-1 composition prereg (COMP-1):** built on the CLA-2
  architecture with 3 frozen templates (CHAIN-2, GATHER-n,
  ITERATE-UNTIL). TNN-2's assemblers are the descendants of those
  templates. The prereg's honest limitation stands: frozen templates
  are the treadmill the constructor must get beyond.

---

## 4. Relation to SUF

**Would a plan constructor's output satisfy SUF? Under what conditions?**

SUF (Source-Underdetermined Form): at least one causal structural
decision in the production path is resolved by learner history such
that the produced form cannot be completely enumerated from source
alone. SUF check `8ef148a42`: construction, inquiry, revision all
SUF-FAIL in TNN-2.

A plan constructor does NOT satisfy SUF by itself. The conditions under
which its output could:

1. **The composition choice must be learner-history-resolved.** If the
   constructor picks sub-plan A over sub-plan B because of a
   learner-owned criterion (a policy node with an exercised write path,
   per the K-H3 audit), and a different history would pick B, then the
   choice is underdetermined by source. If it picks by a researcher-fixed
   ordering (as `t2_trial` does), the output is source-enumerable and
   SUF-FAIL, no matter how novel the composed shape looks.
2. **The composed topology must not be source-enumerable.** Composing
   two MAPs in a way the source enumerates (e.g., "try all ordered
   pairs") keeps the output enumerable even if the pair was never tried
   before. SUF needs the *form* to escape enumeration: the glue, the
   arity, or the nesting must depend on learner history in a way no
   source loop bounds.
3. **Verification must be learner-internal.** A plan verified against a
   harness-supplied expected answer inherits the harness's judgment;
   the structural decision "this plan is good" is then researcher-made
   (Micah: researcher still owns judgment criteria). SUF is about
   structural decisions; outsourcing the acceptance decision to the
   harness keeps it source-side.

Converse: SUF is necessary but not sufficient (Micah ruling).
A constructor could produce SUF-satisfying plans that are useless,
unverifiable, or never reused. The full entrance criterion stands:
SUF AND useful behavior AND learner-internal verification AND
revisability AND cognitive reuse.

**Honest current status:** TNN-2's assembly pipeline is SUF-FAIL on all
three prongs that matter here: template set enumerable (3), family order
fixed, acceptance criterion harness-supplied. A plan constructor built
on the same three prongs would also be SUF-FAIL. The SUF question for
any constructor proposal reduces to: point to the specific structural
decision the source cannot enumerate, show the learner-state fields
that resolve it, the production read path, the exercised production
write path, and the sealed behavioral variation. That is the K-H3
six-element audit applied to construction.

---

## 5. Open questions for future work

1. **Goal origination:** where does the first goal come from? Options:
   adopted from the query stream, generated from uncertainty (inquiry
   link), or proposed by a higher-level driver. Each has different
   SUF implications.
2. **Contract learning:** are MAP contracts declared at promotion time
   (researcher-shaped bookkeeping) or inferred from execution traces
   (learner-observed)? The latter is more honest but harder.
3. **Composition vs. search budget:** the node budget (1024) and
   execution cap (1000 steps) bound plan size. A constructor that
   builds plans too large to verify is worse than no constructor.
4. **Interaction with revision:** a composed plan will contain wrong
   sub-plans. Copy-and-commit revision (approved architecture
   experiment) must extend to composed plans: which sub-plan gets
   blamed, and does blame require re-verification of the whole?
5. **The decline signal:** what the learner does with "I cannot compose
   a plan for this goal" is itself a cognitive decision (cf. H2B lie
   trap: withholding is a capability). The decline path needs its own
   bar.

---

## Standing architectural metric (this analysis)

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 0 (analysis only) |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 (analysis only) |
| SOURCE-ENUMERABLE FORMS | n/a |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 |
| REUSE EVENTS | 0 |
| REVISION EVENTS | 0 |
| COGNITION LINES | 0 |
| MODES | 0 |
| BRIDGES | 0 |
| HANDLERS | 0 |
| SEMANTIC CASES | 0 |

Zero source lines added. Zero modes, bridges, handlers, semantic cases.
Paper untouched. No sealed worlds opened.
