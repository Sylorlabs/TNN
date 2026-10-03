# TNN-2 Mechanism Interaction Analysis

Date: 2026-09-30 (PDT). Target: `tnn2.zag` @ `f4de7ff46` (frozen,
read-only). Method: read-only source audit of the frozen build plus the
frozen sealed-evaluation driver `core_freeze_tnn2_shim/shim_driver2.zag`
(read-only, for `ev_act` call context). Cross-checked against the three
frozen red-team reports (construction, inquiry, revision). No source
edits. No em dashes used in this document per loop style rule.

Verdict: **INTERACTION-ANALYSIS-COMPLETE**.

## 0. Mechanism inventory and the complete cognition call graph

All line numbers refer to `tnn2.zag` @ `f4de7ff46`.

**Cognition entry points** (called by the driver, never by each other):
- `ev_query` (813): exact hit via `activate` (140) -> else trial via
  `mp_run` (668) -> `t2_trial` (586) -> else `bootstrap_miss` (763) ->
  else `miss_inquire` (795), return -2.
- `ev_observe` (836): exact hit -> match: confirm; mismatch:
  `revise_on_contradict` (685) then teach corrected fact. Miss: teach.
- `ev_act` (859): select over POLICY_ROOT-linked candidates by ctx match
  and bid. Called by no cognition function; only by the driver on world
  `act` lines and by tests.

**Construction (Change 1):** `t2_trial` assembles candidates with exactly
three assemblers (`t2_asm_chain` 363, `t2_asm_count` 379, `t2_asm_sum`
398), executes each with `t2_exec` (412) -> `execute` (192), verifies
with `t2_try_verify` (497), promotes winners with `promote_graph` (533).
`promote_graph` has exactly four call sites, all inside `t2_trial`
(605, 628, 644, 659). No other code path creates executable graphs.

**Inquiry (Change 2):** `miss_inquire` allocates a T_UNCERT node (tag 30)
recording (s, r) and a guide node (tag 1, field20=30, field24=-999,
field4=s), links guide -> uncertainty via ET_DEP and POLICY_ROOT ->
guide via ET_MEM. Sole production caller: `ev_query` (833), only after
`t2_trial` and `bootstrap_miss` both fail.

**Revision (Change 3):** `revise_on_contradict` scans all MAP nodes
(tag 20) for ET_DEP edges to the contradicted fact, then
`t2_revise_graph` (706) finds the stale SETREG cell (tag 101) via its
DEP edge to the fact, finds the guard (tag 102) whose true-target
(field12) is that cell, tombstones the stale cell, inserts a corrected
SETREG holding the observed value, rewires the guard, re-executes via
`t2_exec`, and on success contradicts the old answer fact, teaches the
new one (`ev_teach_in`, 748), and updates the MAP answer (field28).
Sole production caller chain: `ev_observe` (845).

**Key structural fact used throughout:** the cognition query path never
reads MAP nodes. `activate` (140) scans tag-1 fact nodes only.
`ev_query` never consults a promoted graph; answers come from memoized
T_FACTs. MAP nodes are read at exactly two sites: `revise_on_contradict`
(690) and the T2-REVISE test (1281). `execute` (192) is called only from
`t2_exec` (416, trial verification and revision re-verification) and
`exec_val` (217, tests only at 973 and 980).

## 1. Does construction's output feed into revision?

**Yes, through MAP nodes and DEP provenance, but only partially.**

Data flow: `t2_trial` -> `promote_graph` writes a MAP node (tag 20,
field20=graph root, field28=answer, field4=r, field8=s) plus ET_DEP edges
from the MAP to each licensing fact, and each chain/count SETREG cell
carries its own ET_DEP edge to its licensing fact (assemblers at
363-397). Later, `ev_observe` on a contradiction calls
`revise_on_contradict`, which scans every MAP for a DEP edge to the
contradicted fact (688-700) and calls `t2_revise_graph`, which locates
the stale SETREG cell through that cell's own DEP edge to the fact
(711-717) and the guard whose field12 points at it (719-724).

**Sharp limitation: sum-graph MAPs are unrevisable.** `t2_asm_sum`
(398) emits only INC cells (tag 103) and attaches no per-cell DEP edges;
`t2_revise_graph`'s stale search requires a live tag-101 cell with a
DEP edge to the fact, so it returns 0 for every sum-promoted MAP,
silently. The arithmetic construction family (the FW3-relevant path)
produces exactly the MAPs the revision mechanism cannot touch.
Chain (363), count (379), and single-hop graphs are structurally
revisable. Repeated revision of the same graph is possible: the
replacement SETREG receives a fresh DEP edge to the fact (727), so a
second contradiction re-enters `t2_revise_graph`.

## 2. Does inquiry's guide affect construction?

**No. The guide is invisible to every construction reader, and the
trigger carries no data.**

- `miss_inquire` fires only after `t2_trial` returns -2 AND
  `bootstrap_miss` returns -2 (ev_query 829-833). It is trigger-only:
  the trial statistics packed into header+16 (`hs(W,16,...)` at 662) are
  read by no cognition function (sole reader is the T2-REJECT test at
  1232). The guide records nothing about which candidates were tried or
  why they were rejected.
- The guide node (tag 1, field20=30, field24=-999) is excluded from every
  gatherer: `t2_gather` (442) and `t2_gather_sum` (474) skip
  field24==-999; `t2_rels` (485) excludes relation -999; all scan tag-1
  nodes by value, and the guide's field20 is the constant 30. T_UNCERT
  nodes (tag 30) are scanned by no gatherer at all (sole readers are
  tests at 1244-1245).
- The guide's only consumer is `ev_act`, which no cognition function
  calls. In the sealed evaluation the driver calls `ev_act` only when a
  world file contains an `act` line (shim_driver2.zag, process_line).
  `ev_act` then returns the constant 30 whenever any guide matches the
  context stack, else 0. The action does not vary with the content of the
  uncertainty: every guide ever created encodes the same action value.

Minor interference note: a guide would match `activate` only for the
degenerate query s=30, r=-999. Negligible in practice, but the channel
exists because the guide reuses the T_FACT tag.

## 3. Does revision's output feed back into construction?

**Only through the fact store, never structurally. Revision makes future
construction less likely, not better informed.**

- On success, `t2_revise_graph` calls `ev_teach_in(s,r,out)` (748),
  adding a corrected T_FACT that later `t2_gather` / `t2_chain` /
  `t2_gather_sum` calls will see, and supersedes the old answer fact via
  a CON self-edge (745-751), which `activate` then skips.
- Construction never reads MAP nodes, never re-executes a revised graph,
  and never reuses revised topology: the next trial rebuilds from facts
  from scratch. `promote_graph` is called only from `t2_trial`.
- Because the corrected fact is now an exact hit, subsequent queries on
  (s, r) take the `activate` path and never invoke the trial loop. The
  revised graph itself becomes inert: it is consulted only if another
  contradiction arrives on one of its licensing facts.

## 4. Feedback loops: are there any?

**No closed feedback loops exist between the three mechanisms.** The
verified interaction matrix (rows write, columns read):

| writer -> reader | construction | inquiry | revision | action (ev_act) |
|---|---|---|---|---|
| construction | n/a | trigger only (fires iff trial+bootstrap fail; no data passed) | YES: MAP nodes + DEP provenance (chain/count/single-hop only; sum graphs excluded) | none |
| inquiry | none (guides/UNCERT invisible to all gatherers) | n/a | none | YES but terminal: ev_act uncalled by cognition; driver-invoked only; constant 30 |
| revision | WEAK: corrected facts visible to future gatherers; no structural feedback; revised graphs never re-read | none | n/a (re-revision of same graph possible, same fixed schema) | none |

The construction -> revision -> fact store -> construction path is a
cycle through shared state, not a control loop: revision cannot alter
construction's proposal distribution, grammar, or verification
criterion, and construction never observes revised structures. Inquiry
is a dead-end pipeline in the cognition path: it writes state that only
`ev_act` reads, and `ev_act`'s output terminates at the driver. Nothing
writes back into construction's candidate grammar (the four assembler
call sites are fixed source), and nothing ever deletes or updates a
guide or uncertainty node based on later evidence; they accumulate
write-only.

## 5. Do the red-team limitations compound or stay independent?

They compound. Each limitation is independently fatal to its mechanism's
generality claim, and the interactions multiply the damage:

1. **Finite construction x literal-only revision.** Revision can only
   ever see template-shaped graphs, because only template-shaped graphs
   can be promoted. The system's reachable executable-structure space is
   the intersection: four fixed template families (construction red
   team: exactly three assemblers, DEC never emitted, no nesting, no
   reuse of MAPs as components) with literal-only patching (revision red
   team: exactly one repair schema, guard->new-SETREG->succ). The
   limitations multiply on structural novelty: neither mechanism can
   introduce a topology the other did not already fix.

2. **Inquiry fires exactly where construction is blind, and says
   nothing.** `miss_inquire` is reached only when all templates fail,
   i.e., precisely on cases outside the finite family. But the guide
   carries no information about the failure (no tried/rejected
   candidates, no expected value, not even the relation in a usable
   slot), and no mechanism reads it back into construction. The two
   mechanisms are complementary in coverage and non-communicating in
   content: the failure signal is computed and then discarded.

3. **Supervised construction vs. inert inquiry.** `t2_try_verify` (497)
   promotes only graphs whose execution equals `expected`, and in the
   sealed evaluation the driver supplies `expected` from the world file
   (`ev_query(W,subj,rel,exp,0)`, shim_driver2.zag line 91). Construction
   therefore cannot promote anything the world did not already hand it
   the answer to. Inquiry is the designated handler for the unsupervised
   case, but its action (constant 30) never produces an observation that
   feeds back into the learner: `ev_act`'s output goes to the driver,
   and nothing teaches the result. The system has no unsupervised
   learning loop at all: supervised template-matching on one side, a
   content-free miss flag on the other.

4. **Sum-graph unrevisability (Section 1).** The construction family most
   relevant to arithmetic produces MAPs the revision operator silently
   skips. Even the construction->revision link, the one genuine
   mechanism-to-mechanism data flow, is partial along exactly the axis
   the mechanisms were built to cover.

5. **Promoted graphs are never executed to answer queries.** Answers come
   from memoized facts; MAPs are derivation certificates, not reusable
   procedures. This undercuts reuse (C0-D) at the interaction level
   regardless of any single mechanism's generality: even a genuinely
   constructed procedure would never be called again by the cognition
   path.

## 6. Bottleneck identification

**The bottleneck is construction, specifically the propose/verify pair
in `t2_trial` + `t2_try_verify`, with verification as the tighter
constraint.**

Reasoning:

- Construction is the sole generator of executable structure. Revision
  is a patch operator defined over construction's output vocabulary;
  inquiry creates no executable structure at all. Generalizing revision
  first leaves the template family intact (nothing new to patch).
  Generalizing inquiry first produces richer guides that no mechanism
  reads (no read path into construction, and `ev_act` output terminates
  at the driver).
- Construction's finite grammar bounds everything downstream:
  revision's input vocabulary, the set of structures that could ever be
  revised, reused, or transferred.
- The verification criterion is the deeper constraint: promotion
  requires an externally supplied `expected` match. Even an open
  proposal grammar would still need the answer in advance. A genuinely
  general constructor needs a self-generated verification criterion
  (prediction of future observations, internal consistency, or
  executability without supervision). That single change would
  simultaneously give inquiry a real question to ask (discriminating
  evidence for self-verification) and revision a real criterion
  (predicted vs. observed). This is why construction lifts the others
  and the others cannot lift it.
- Second-order bottleneck, independent of the above: there is no reuse
  path. `ev_query` never executes a MAP. Until promoted graphs are
  executed at query time, generality of construction cannot convert
  into capability or transfer (C0-D fails structurally, not just
  empirically).

Three structurally different hypotheses for the bottleneck, per the
no-treadmill rule (for TNN-3 root-cause work, not patches):

- H1 (verification-first): the binding constraint is the
  expected-gated verifier. Replace external-answer matching with a
  learner-generated verification criterion (e.g., the graph must predict
  a held-out observation the learner then seeks). Predicts fixes to
  construction autonomy and gives inquiry a functional role.
- H2 (representation-first): the binding constraint is that procedures
  are write-only certificates. Route `ev_query` hits through MAP
  execution instead of memoized facts, so constructed structure is
  actually reused. Predicts transfer and revision pressure on real
  procedure topology rather than literals.
- H3 (grammar-first): the binding constraint is the fixed assembler
  set. Make proposal compositional over previously promoted graphs
  (graphs as components, not just facts as inputs). Predicts depth and
  cross-domain reuse, but only helps if H1 is also addressed, since an
  open grammar with expected-gating is still supervised enumeration.

Recommended order: H1 before H3; H2 is required for any of them to
matter for reuse. None of these is a per-world patch: each is a general
substrate change testable across multiple fresh worlds.

## 7. Consequences for the frozen claims

- The three mechanisms are not an integrated cognitive architecture;
  they are three pipelines sharing a workspace, one of which
  (inquiry) terminates outside cognition and one of which (revision)
  serves a subset of construction's output.
- The TNN-2 BUILD-PASS and REPRO-PASS verdicts are unaffected: this
  analysis concerns mechanism interaction and generality, not build
  integrity or determinism.
- Any future L3 claim on these mechanisms must address the interaction
  findings, not just the per-mechanism red-team findings: C0-B fails at
  the system level because the reachable structure space is the
  intersection of the three finite schemas, and C0-D fails structurally
  because promoted graphs are never re-executed.

Verdict: **INTERACTION-ANALYSIS-COMPLETE**.
