# Reuse Path Design for TNN-3

**Status: NOT IMPLEMENTED.** This document is design only. No source was
modified, no binary was built, no experiment was run. All line numbers
refer to `tnn2.zag` at frozen `f4de7ff46`, re-verified by grep during
this task. Any TNN-3 work that follows must go through its own
preregistration with frozen kill bars. No em dashes are used in this
document per loop style rule.

Date: 2026-10-01 (UTC). Designer: Reuse Path Designer.
Verdict on completion: REUSE-PATH-DESIGN-COMPLETE.

Read-only sources: C0-D structural analysis (`tnn2_c0d/`, commit
`8bfb80fdd`); target-selection design (`tnn2_targetsel/`, commit
`01c2aacfe`); interaction analysis (`tnn2_interaction/`, commit
`9009ff259`); frozen TNN-2 source.

## 0. The problem in one paragraph

Promoted graphs are causally inert at query time. `promote_graph` (533)
writes the MAP node and then at line 541 calls `ev_teach_in(W,s,r,ans)`,
inserting an exact-match fact that shadows the graph it just promoted.
`ev_query` (813) answers via `activate` (140), whose filter at line 143
(`ng(W,n,0)==1`) admits only tag-1 facts, never tag-20 MAPs. The next
query on the same (s, r) is therefore always an exact hit and never
reaches any graph. A promoted graph executes exactly twice in its life:
verification inside `t2_trial` and re-verification inside
`t2_revise_graph`. The interaction analyst's verdict stands: "The system
has no unsupervised learning loop at all," and C0-D "fails structurally,
not just empirically." The C0-D analysis further established a second,
independent sufficient cause: the graphs are value traces (literals
embedded, relation only in provenance), and the frozen 4-op ISA has no
relational-dereference operation, so subject-general procedures are
inexpressible. Either cause alone is fatal to C0-D. Both are present.

This design addresses the first cause (query-path bypass) in full and
states exactly where it stops relative to the second (value-trace
encoding at the ISA boundary, which is a protected-core decision banked
for Micah, not taken here).

## 1. Query path: where the MAP branch goes

### 1.1 Insertion point

In `ev_query` (813), the MAP lookup is inserted as a new branch
**before** the existing `activate` call. The resulting order:

1. MAP lookup: scan live tag-20 MAPs for `field8 == s` and
   `field4 == r` and `is_superseded == 0`. On a hit, run
   `t2_exec(W, ng(W,m,20), s)` where `ng(W,m,20)` is the graph root
   stored by `promote_graph` (via `write_node(W,m,root,...)` at line
   536). If the result is not -999999, perform the same bookkeeping
   the `activate` branch performs (`link_edge` type 6, `ref_prot`,
   `log_ev` with the MAP as source) and return the result.
   On execution failure (-999999), fall through.
2. `activate` (existing fact path), unchanged.
3. Trial loop via `mp_run` (existing), unchanged.
4. `bootstrap_miss` (existing), unchanged.
5. `miss_inquire` (existing), unchanged.

### 1.2 Why MAP-first, not activate-first

Two orderings were considered. Activate-first (facts win; MAPs consulted
only on fact miss) preserves the current priority of explicitly taught
facts but makes the MAP branch nearly dead: any fact for (s, r),
including stale ones, blocks reuse, and the reuse signal the
target-selection design needs would rarely fire. MAP-first (live
executable MAP wins; facts are the fallback) makes procedures
first-class answerers, which is what the interaction report's H2
("Route ev_query hits through MAP execution instead of memoized
facts") requires and what the C0-D analysis's minimal wiring
prescribes ("live executable MAP wins over facts; on execution failure
fall back to the fact"). The risk of MAP-first, a stale MAP answering
wrong with confidence, is handled by the liveness policy in section 2,
not by demoting MAPs below facts. If the liveness policy is correct, a
live MAP is by definition the most current structured knowledge about
(s, r), and trusting it over a fact is the intended semantic.

### 1.3 Lookup key and match semantics

The lookup key is the pair (s, r), matching MAP `field8` (s) and
`field4` (r). This is the minimal key: it reuses exactly the identity
fields `promote_graph` already stores, needs no new index structure,
and matches the query contract (`ev_query` takes s and r). Structural
signature matching (same graph shape, different subject) is explicitly
out of scope for the minimal design; it belongs to the complete design
and depends on portable procedures (section 5).

### 1.4 Determinism obligation

Executing MAPs at query time allocates frames (`t2_exec` calls
`alloc_node` for the frame at line 414) on every MAP-hit query, so the
freeze's 3/3 byte-identical property must be re-verified under the new
path. This is a test obligation for the TNN-3 preregistration, not a
blocker: frame allocation is already deterministic in the frozen source
(the allocator is a bump pointer over a fixed arena), but the claim must
be measured, not assumed.

## 2. Shadow policy: deleting the self-shadowing teach

### 2.1 The deletion

`promote_graph` line 541, `ev_teach_in(W,s,r,ans);`, is deleted. The MAP
becomes the promoted artifact. The fact store keeps only observed or
explicitly taught facts (from `ev_observe`, `ev_teach`, `bootstrap_miss`);
it no longer receives derived answers as a side effect of promotion.

This deletion is load-bearing for the whole design. With MAP-first
ordering, keeping the shadow teach would merely waste a node per
promotion (the fact would never be read for (s, r) while a live MAP
exists). With activate-first ordering, keeping it would make the MAP
branch dead code, reproducing the current degeneracy. The design
therefore pairs the deletion with MAP-first ordering as a unit; either
change alone is incoherent.

### 2.2 What prevents stale MAPs from answering incorrectly

Three mechanisms, all reusing existing machinery:

**(a) Supersession.** `is_superseded` (132) already honors type-3
self-edges, and both `activate` and `ev_act` already respect it. The MAP
lookup in section 1.1 filters on `is_superseded == 0`, exactly as
`activate` does for facts. When a MAP is contradicted (section 4), it
receives a type-3 self-edge and is skipped thereafter. No new
supersession machinery is needed.

**(b) Decay and eviction.** `ev_query` already calls `decay(W)` on every
query. MAPs must participate in decay the way facts do, so that
procedures do not outlive the regime they were built for. If the frozen
`decay` implementation keys off tag-1 nodes, the minimal extension is to
include tag-20 nodes in its sweep. This is a small, localizable change,
and it is the piece that answers "what if the world changes silently
without an explicit contradiction": unused MAPs age out like unused
facts.

**(c) Execution-failure fallback.** If a live MAP executes to -999999
(structural failure, allocation failure), the query falls through to
`activate`. A MAP that cannot execute never blocks the fact path. This
bounds the damage of any liveness bug: worst case, the system behaves
as TNN-2 does today.

### 2.3 Legacy and mixed states

During any transition, and in states built by older binaries, both a
MAP and a fact may exist for the same (s, r). The rule: a live,
non-superseded MAP wins; a superseded MAP is skipped; on MAP execution
failure, fall back to the fact. This rule is total (every state maps to
an answer path) and it degrades gracefully to current behavior when no
live MAP exists.

## 3. MAP selection: which graph executes when several match

Multiple live MAPs can match (s, r): re-promotion after revision
creates a new MAP, and nothing in the frozen source deletes the old one
(the old MAP is superseded only if the contradiction path marks it;
see section 4).

**Minimal rule:** the most recently promoted live MAP wins, ordered by
MAP `field24` (the promotion index written by `promote_graph` from the
header counter `hg(W,24)`). This is a researcher-fixed tie-break, stated
as such. It is the smallest rule that is total and deterministic.

**The seam for target-selection.** The selection function is a single
call site where the target-selection policy plugs in later. The
target-selection design (`01c2aacfe`) specifies per-MAP score scalars
(MAP `field12`/`field16` are written -1 at promotion and never read,
natural slots), an update rule on verified composition vs genuine
rejection, and a provenance-overlap tie-breaker. The minimal design
leaves `field12`/`field16` untouched and documents the selection call
site as the integration point. Build order, per that design: reuse path
first (this document), then score scalars with the interim
composability signal, then reuse-based scoring once query-time
execution generates the signal. The minimal rule must therefore be
written so that replacing "max field24" with "max score, then overlap,
then field24" is a localized edit at one site.

## 4. Contradiction: retargeting at the MAP

### 4.1 Current wiring

`ev_observe` on a mismatch calls `revise_on_contradict` (845 -> 685),
which scans MAPs for DEP edges to the contradicted fact (688-700),
then `t2_revise_graph` (706) patches the stale SETREG cell, re-verifies
via `t2_exec` (732), and on success contradicts the old answer fact,
teaches the new one (`ev_teach_in`, 748), and updates the MAP answer
(`field28`).

### 4.2 Retargeted wiring

The contradicted object becomes the MAP itself:

1. `ev_observe` on a mismatch first runs the same MAP lookup as
   section 1.1 for (s, r). If a live MAP is found, it is the
   contradicted object. (If none is found, the existing fact
   contradiction path runs unchanged; this preserves behavior for
   purely observed knowledge.)
2. `revise_on_contradict`'s DEP scan (688-700) already enumerates MAPs
   by licensing fact; it is kept, but its role changes from "find MAPs
   to patch" to "find the MAP whose answer is contradicted," which in
   the common case is the same MAP found in step 1. The two lookups
   must agree; the preregistration should specify that the (s, r)
   lookup is authoritative and the DEP scan is the fallback.
3. `t2_revise_graph` runs as today (single-schema literal patch; its
   generality limits are the revision red team's finding and are out
   of scope here). On success it updates the MAP's answer field
   (`field28`) as today.
4. **No shadow fact is taught on MAP revision.** Step 4 of the current
   wiring (`ev_teach_in` at 748 plus the old-fact contradiction at
   745-751) is the MAP-level analogue of the promotion shadow teach,
   and it is deleted for the same reason: with MAP-first query
   ordering, derived answers live in MAPs. Observed answers live in
   facts. This is the clean architectural line the C0-D analysis
   called for ("no procedure standing, no procedure contradiction, no
   procedure eviction, no procedure identity across revision" was the
   diagnosis; this design supplies all four: standing via the MAP
   branch, contradiction via this section, eviction via section 2.2,
   identity via the MAP node persisting across revisions).

### 4.3 What if revision fails

If `t2_revise_graph` returns 0 (cannot patch: sum graphs have no DEP
edges per the interaction analysis section 1, or the single schema
does not apply), the MAP is marked superseded via a type-3 self-edge
and the observation is taught as a fact. The next query then takes the
`activate` path (fact hit) or the trial path (rebuild). This is the
honest failure mode: an unrevisable procedure is retired, not
silently kept.

## 5. Value traces: what reuse can and cannot do without portable procedures

The C0-D analysis proved the graphs are value traces: `t2_asm_chain`
embeds `t2_lit` literal values gathered for the original subject, the
traversed relation lives only in DEP provenance, and the frozen ISA
cannot compute "the fact (s, r)" at runtime. Executing subject 1's
graph on subject 7 returns -999999 (transfer probe P2, confirmed
behaviorally).

**Same-(s, r) reuse works with value traces.** Re-executing a MAP on
the (s, r) it was promoted for recomputes the known answer; that is
exactly what verification already does. The minimal design therefore
delivers working reuse on the promotion instance. What this buys, stated
without oversell:

- (a) The architecture becomes honest: procedures are first-class
  answerers, and the "derivation certificate" degeneracy is gone.
- (b) The reuse-history signal exists: MAPs accumulate execution
  counts, which is the prerequisite signal the target-selection design
  needs for reuse-based scoring (its section 3 dependency).
- (c) Revision pressure lands on real procedure topology:
  contradictions hit the MAP (section 4), so a future general revision
  operator would have something to work on besides literals.
- (d) Composition operands are exercised structures, which the MUL
  direction (graphs calling graphs) ultimately needs.

What it does **not** buy: transfer to new subjects, prediction gain on
unseen (s, r), or sample efficiency beyond what fact memoization
already provides. On those axes the minimal design converts C0-D from
"fails structurally" to "testable, currently failing behaviorally,"
which is exactly the staging the C0-D analysis recommended. The
behavioral failure that remains is the value-trace limitation.

**Cross-(s, r) reuse requires portable procedures,** which requires a
relational-dereference capability in the protected core (a
memory/lookup primitive over the graph store, in the ISA ruling's
allowed class of ALLOC/READ/WRITE/LINK but absent from the frozen
instance). That is the Layer 2 fix the C0-D analysis banked as Micah's
decision. This design does not take it, does not presuppose it, and is
not blocked on it: the minimal path is fully specified within the
frozen ISA, and the portable-procedure upgrade, if ever approved,
plugs into the same MAP branch (the lookup key generalizes from
(s, r) identity to structural signature; the execution call is
unchanged).

## 6. Minimal vs complete

### 6.1 Minimal: C0-D becomes testable

All within the frozen ISA, no new opcodes, no new modes, no new
bridges, no new node types (the MAP tag 20 layout is reused as-is):

1. MAP-lookup branch in `ev_query` before `activate` (section 1),
   MAP-first ordering, fallback to facts on -999999.
2. Delete the shadow teach at `promote_graph:541` (section 2.1).
3. Liveness: MAPs in the `decay` sweep; `is_superseded` filter on the
   MAP lookup; live-MAP-wins rule for mixed states (section 2.2, 2.3).
4. Contradiction retargeted at the MAP; no shadow fact on MAP
   revision; supersede-and-teach-fact on revision failure
   (section 4).
5. MAP selection: most-recent live MAP by `field24`, with the
   selection call site documented as the target-selection
   integration point (section 3).

After these five, a white-box probe can observe a MAP node being read
during a query, which is the discriminator the C0-D analysis handed to
the transfer lane: reuse is then an observable event, not an
impossibility. C0-D is testable. It will fail behaviorally on transfer
(the value-trace limitation), which is the honest next result.

### 6.2 Complete: C0-D becomes achievable

Minimal plus, in dependency order:

1. **Portable procedures** (protected-core decision, banked for
   Micah): relational dereference in the ISA so graphs are not value
   traces. This is the only item that touches the frozen
   computational basis.
2. **Target-selection policy** wired into MAP selection
   (K-TSEL-1/K-TSEL-2 from the target-selection design): per-MAP
   score scalars, update rule on verified composition vs genuine
   rejection, provenance-overlap tie-breaker. Needs the reuse path
   first (signal dependency); needs no ISA change.
3. **Composition via inlining** with executed MAPs as operands (the
   MUL comparator's freeze-compatible route): the trial loop splices
   promoted graph cells into new candidates with slot remapping,
   using the target-selection policy for operand choice. Needs 1
   and 2; needs no new opcode.
4. **General revision** beyond the single-schema literal patch (the
   revision generalization analysis enumerated five unexpressible
   repair classes): so that contradictions on reused procedures
   produce topology change, not just literal overwrite. Needs 1
   (procedures worth revising must be portable first).

Each of the four is a separate preregistration with its own kill
bars. None is a per-world patch. The order matters: 2 needs the reuse
path (this design); 3 needs 1 and 2; 4 needs 1. Doing 3 before 1
reproduces the "larger finite menu" objection the MUL comparator
sustained.

### 6.3 What the minimal design deliberately does not do

- It does not widen the construction grammar (H1 territory).
- It does not replace expected-gated verification (H2 territory).
- It does not make procedures learner-built (full H3 territory).
- It does not fix the sum-graph unrevisability (no per-cell DEP
  edges; separate repair).
- It does not claim L3, C0-D satisfaction, or any FW1-FW9 score
  improvement. The honest prediction is: scores unchanged (the
  answers are the same; only the answering mechanism changes), while
  the architecture gains the observable reuse event the program has
  been missing.

## 7. Kill bar for the reuse path (draft, DRAFT-NOT-FROZEN)

Draft language for the kill-bar lane, not a frozen bar:

> **K-REUSE-1 (query-time MAP execution).** In a sealed world, after
> the learner has promoted a MAP for (s, r), a subsequent query on
> the identical (s, r), with no intervening contradiction or
> observation touching (s, r), must produce a white-box trace in
> which a tag-20 node is read during the query and `t2_exec` is
> invoked on its stored root. **Discrimination condition:** the
> trace must show the MAP read preceding any `activate` hit for
> (s, r), and the returned answer must equal the MAP's executed
> output, not a memoized fact value read. A binary that answers
> from the fact store fails this bar even with identical answers.
> The preregistration must name the exact MAP-lookup call site and
> the liveness predicate; any query-time answer path that bypasses
> the lookup is a bar violation.
>
> **K-REUSE-2 (no shadow facts).** Across the sealed evaluation,
> no `ev_teach_in` call site reachable from `promote_graph` or
> from MAP revision may insert a fact with the same (s, r) as a
> live MAP. White-box audit of teach sites; one shadow fact is a
> bar violation. This bars the reintroduction of the degeneracy
> under a new name.

Why two bars: K-REUSE-1 proves the reuse event happens (execution,
not memoization). K-REUSE-2 proves the old degeneracy was actually
removed rather than routed around. Together they are the reuse
analogue of the synthesis's prereg checklist: "list every structural
decision the learner can make that the source cannot," applied to
the answering mechanism itself.

## 8. Risks and open questions

1. **Stale-MAP confidence.** MAP-first ordering trusts a live MAP over
   facts. If the liveness policy has a hole (a MAP that should have
   been superseded was not), the system answers wrong with full
   confidence where TNN-2 would have answered from a (possibly also
   stale) fact. Mitigation: the decay sweep and the revision-failure
   supersede rule (section 4.3) are both specified as load-bearing,
   and K-REUSE-1's sealed worlds should include a silent-regime-change
   world with no explicit contradiction, exercising the decay path.
2. **Performance.** Every query now scans up to 1022 nodes for MAPs
   before the fact scan. The frozen source already does full sweeps
   per query (`activate`, gatherers), so this is a constant-factor
   change, but the preregistration should budget it.
3. **The (s, r) key is narrow.** Reuse only fires on exact re-query.
   This is deliberate for the minimal design (no signature machinery,
   no portability presupposed), but it means the behavioral C0-D
   payoff is small until the complete design lands. The honest
   framing in section 6.3 stands.
4. **Interaction with the trial loop.** On a MAP execution failure
   (-999999) the query falls through to the trial loop, which may
   promote a *second* MAP for the same (s, r). The selection rule
   (section 3) then prefers the newer one. Over many failures this
   accumulates MAPs; the decay sweep (section 2.2) is the cleanup
   mechanism. The preregistration should cap MAPs per (s, r) or
   specify the eviction interaction explicitly.
5. **Open question for Micah (banked, not decided here):** whether the
   protected core may gain the relational-dereference primitive that
   portable procedures need. Nothing in this design presupposes an
   answer; the minimal path is complete without it.

## 9. Relation to the other lanes

- **Target-selection** (`01c2aacfe`): this design is its stated
  prerequisite ("target selection is downstream of the reuse path").
  Section 3 documents the integration seam.
- **H3-lite** (trial order, guide template, repair dispatcher policy
  nodes): the reuse path is orthogonal and composes with all three;
  none of the three needs modification for the MAP branch to work.
- **Interaction H1/H2/H3** (commit `9009ff259`): this design is H2
  (reuse-path-first), implemented at the minimal level. It does not
  address H1 (verification) or H3 (grammar); the recommended order
  (H1 before H3, H2 required for reuse) is respected.
- **C0-D analysis** (`8bfb80fdd`): implements its section 6 minimal
  wiring (the four items) plus the selection seam and the kill bars.
  Its Layer 2 (value traces, ISA boundary) is acknowledged in
  section 5 and banked, not taken.

*End of design. No source modified. No worlds designed. No scores
claimed. Paper untouched.*
