# PREREG: Continuing Learner Architecture (CLA-1)

Date: 2026-09-30. Worker: Continuing Learner Architect.
Status: PREREG-FROZEN (architecture design only; no implementation in this commit).
Lane: continuing learner is HIGH PRIORITY (standing ruling 2026-09-30).

## Step 0 Name-Check

The standing rules from the top of repo-root LOOP_STATE.md that apply:
(1) PURE ZAG ONLY, the literal red line. This task is architecture
design, pure markdown; no code is written, no tooling is invoked, and
no Python is used for any purpose. (2) Shell-only byte checks: the
dash check for the documents below runs via the shell-only
check_no_dash.sh snippet, never python3. (3) Fork testing and the
image-judge rule are not applicable to architecture design.
(4) Commits stay local, owned paths only
(docs/lab/research-lead/overnight-20260928/continuing_learner/),
explicit pathspecs, git status inspected before committing, the
contaminated paper untouched. This paragraph was written before any
design work began.

## The standing question

> Why can the existing general architecture not learn this behavior?

The frozen substrate owns three independent fixed-format stores
(44-byte fact slots, 1152-byte DDES hypothesis entries, rule-store
keys) with researcher-defined semantics, plus frozen researcher code
for eviction (evict_c with the C75 lowest-index tie-break pathology).
There is no generic structural substrate in which the learner can
define new node types and topologies: W9 fails because hierarchy
cannot be expressed in flat triples, not because the learner saw too
few examples. The eviction policy reads researcher-defined importance
and a hardcoded tie-break, so the learner cannot develop its own
preservation policy from experience: W4/W5/W6/W8/W9 fail because
sequential teaches collide on one slot, not because the content was
unlearnable. The missing piece is not nine capabilities; it is one
general substrate in which structures and their preservation policy
are both learner-owned.

## Failure clustering (Core Freeze Challenge 1/9)

The nine worlds cluster into three shared architectural causes, not
nine separate capability gaps:

- Cluster M (memory pathology): W4, W5, W6-treatment, W8-recall, W9.
  Shared cause: the C75 eviction tie-breaker destroys sequentially
  taught facts. The substrate cannot accumulate experience.
- Cluster C (no construction machinery): W2, W3, W9-clean. Shared
  cause: the core stores triples and retrieves by exact key; it has
  no operation that constructs a new structural form (procedure,
  causal hypothesis, hierarchy) from experience.
- Cluster A (no uncertainty/action coupling): W6, W7. Shared cause:
  the only learner-to-world action channel is the constant CHOICE 0;
  no action can be contingent on epistemic state.

W1 passes on exact-key memory. The design below addresses each
cluster with one general substrate change. Per the research
director's ruling, a repair that fixes only one world is rejected
unless it reveals a general mechanism.

## Design CLA-1

### (a) The protected core (frozen)

A minimal generic substrate. Frozen once; never edited per task.

- Persistent byte-addressable state with save/load, deterministic
  execution, and hash verification (same discipline as the freeze
  challenge: binary hash verified before every world).
- Primitive operations only: ALLOC (node), WRITE (payload), LINK
  (typed edge), READ, ACTIVATE (spreading retrieval), DECAY.
- No semantic cases for procedure, cause, language, or plan. No
  modes (no CAUSAL_MODE, no MEMORY_MODE, none). No bridges.
- The world interface is one generic event stream: TEACH, QUERY,
  ACT, OBSERVE. Events carry (tick, kind, refs, payload). The
  driver strips world and task identity: cognition never receives
  a task label.
- Default eviction exists in the core, but it reads ONLY
  learner-owned state (section d). The core never decides what is
  worth keeping; it only enforces capacity.

Projected core size is small by construction: storage, six
primitives, the event loop, serialization. The exact line count is
measured at implementation; the design target is net-negative
against the summed sources of the surviving mechanisms.

### (b) The learner-owned structural workspace (one format)

One node store, one edge discipline, learner-defined types.

- Nodes are fixed-size records: (type_tag, ref[4], payload[4]).
  The learner assigns type_tag values through use; first use
  defines the type. The core never interprets tags.
- Edges are typed links with a small generic vocabulary:
  DEPENDS-ON, SUPPORTS, CONTRADICTS, REFINES, INSTANCE-OF.
  The vocabulary is fixed and generic; what it connects is learned.
- Structure families live in the same store as node-type
  conventions, not as separate subsystems:
  - fact clusters (W1-style associations),
  - hypothesis graphs (atoms and edges in the L3C v3 style),
  - executable programs (built incrementally; see gap G1),
  - episode chains (6-i32 records, proven by C74),
  - operator models (OpScope output, already compressed to
    ledger entries by C74),
  - the protection set and utility ledger (section d).
- No per-mechanism state formats. The C74 compression (which
  eliminated the 8,400-byte OpScope slice into DDES ledger
  entries) is the precedent: every surviving mechanism is
  re-expressed as workspace content.

### (c) Integration of the surviving mechanisms

Each surviving mechanism contributes its GENERAL operation as a
workspace process. The task-specific shell is rejected in each case.

- L3C v3 (cover-set composition, bounded L2): integrate the
  general operation "compose a covering dispatch from corroborated
  atoms" as a graph operation over hypothesis nodes. The
  DISP/TERM rule format becomes one node-type convention among
  others, not a separate rule store. The EMPTY interpreter diff
  is preserved as a design constraint: composition uses existing
  primitives only.
- L3B (procedure invention, bounded L2+): DO NOT integrate the
  menu. The lane ruling stands: finite menu confirmed by the
  adversary, redesign toward incrementally constructed executable
  state, never menu expansion. The workspace supports executable
  node structures; the construction algorithm is named gap G1.
  Broadcast-last remains research evidence only.
- HypD v3 (selection schedule, bounded L2): integrate the general
  operation "maintain candidate structures under selection with
  carry-over" as a learner-owned process over workspace nodes:
  the population is nodes tagged CANDIDATE, selection is by
  held-out utility, carry-over is via the protection set. No
  separate MAP-Elites subsystem; no SEL_MODE/CARRY_MODE flags in
  the core.
- OpScope (behavioral, gate lineage CLOSED): already compressed by
  C74 into ledger entries. Integrate "episode to operator model"
  as workspace derivation. No new admission gates, ever.
- C1 (lifetime learning, bounded L2): the teach/query/revise loop
  IS the continuing learner's event loop (section f). The
  smallest-consistent-k tie-break (C76) is the bootstrap
  disambiguation policy. Revision stays evidence-style
  (relearn from fresh demos); no REVISION_MODE is canonized.
- SEM (bounded L2+): retained as baseline and control reference
  per the standing decision; not integrated into the workspace.

### (d) The eviction pathology (C75): the general answer

The research director's question: "What general learner-owned
memory representation/policy would let one frozen learner preserve
newly useful knowledge, dependencies, hypotheses and structures
without task-specific storage logic?"

The answer is a three-part learner-owned preservation system.
The core eviction routine reads ONLY these structures; it contains
no researcher policy beyond capacity enforcement.

1. Utility ledger. Every node carries learner-updated utility:
   use count, success contribution, surprise. Updated by generic
   rules on QUERY/TEACH outcomes (a hit raises the utility of the
   nodes that participated; a miss raises the utility of nodes
   on the retrieval path, marking them as load-bearing
   uncertainty). No task code participates.
2. Dependency graph. Structures link to their supports with
   DEPENDS-ON edges. Eviction of a node requires consulting its
   dependents: a node with live dependents is preserved by graph
   position, not by a researcher-maintained list. Hypotheses,
   procedures, and operator models thereby protect the facts
   they stand on, automatically.
3. Protection set. The learner pins nodes by creating protection
   structures from experience (for example: "this hypothesis
   survived three contradictions" becomes a pin with its own
   provenance). Pins are workspace content, not source constants.
   The tie-break cursor is learner-owned state: monotonic and
   non-colliding, so sequential writes spread instead of
   colliding (the direct repair of the C75 mechanism).

Bootstrap: the lowest-index tie-break is fixed with a one-line
change (same class as the C76 repair). After the bootstrap, all
policy change comes from learner experience, never from source
edits. This is not a cache-policy treadmill: the policy substrate
(utility, dependencies, protection) is fixed and general, while
the policy content is learned. A future "version" of the policy
is a new workspace structure, not a new source file.

### (e) The persistent experience format

- One append-only experience log. Entries are
  (tick, kind, refs[2], payload[4]). Kinds are learner-extensible:
  the learner registers a new kind by using it; the core stores
  bytes.
- Episode records follow the C74 6-i32 convention (proven to
  carry operator-discovery episodes with zero bespoke state).
- No task labels at any layer: the driver strips world/task
  identity before the event reaches cognition. The learner sees
  one continuous stream.
- Total state = workspace + log, both byte-serializable. Save
  and load across process invocations. The learner cannot
  distinguish "restart with loaded state" from "uninterrupted
  continuation": there is no process-reset semantic, only
  persistence.

### (f) The event loop (one loop, all capabilities)

TEACH: encode the event into workspace nodes; link to related
structures; update utility and dependencies.
QUERY: retrieve by activation spread over the workspace; answer
from the highest-utility coherent structure; record which nodes
participated.
ACT: emit through the generic action channel (gap G2 covers
epistemic contingency).
OBSERVE: compare outcome to expectation; update utility ledger,
protection set, and structures; on contradiction, create
CONTRADICTS edges and relearn from fresh evidence (C1-style);
never a REVISION_MODE.

One loop serves concepts, procedures, causal hypotheses,
contradictions, inquiry, planning, language, and representational
structure. Capabilities differ in the workspace structures they
build, not in the code path that builds them.

## One-System Rule accounting (prereg; measured at implementation)

- Cognition source lines added: projected net-negative versus the
  summed sources of the surviving mechanisms (L3B v2, L3C v3,
  HypD v3, OpScope-compressed, C1 contestant). Exact count is an
  implementation measurement; the prereg binds the direction.
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- Learner-state structures created: node store, edge discipline,
  utility ledger, dependency graph, protection set, experience
  log (6; all learner-owned, all generic, all in one workspace).

## Falsifiable predictions

P1 (eviction ceiling broken): the frozen CLA-1 implementation
stably holds 36 sequential new facts with zero eviction source
edits after the bootstrap one-liner. The C75 signature
(OBSERVED immediately followed by EVICT of the same key) does
not occur.

P2 (multi-capability accumulation): one frozen learner, no task
labels, accumulates usable structures across at least three
capability families (for example: concept associations,
causal-hypothesis graphs, episode chains) in the single
workspace, and later queries draw on structures built by
earlier, unrelated episodes.

P3 (protection ablation): deleting the protection set (and only
that) restores the eviction pathology: sequential-teach survival
falls back toward the C75 ceiling. This tests that preservation
is caused by the learner-owned structure, not by core code.

P4 (open structural form): the workspace comes to hold at least
one node-type topology not enumerated in this prereg (C0-B).
If every structure the learner builds was named here, the
workspace is a menu, not a substrate.

P5 (architectural compression): total cognition source for the
CLA-1 continuing learner is fewer lines than the sum of the
integrated mechanisms' sources. If integration costs lines,
the design failed its own rule.

P6 (no-reset indistinguishability): on a fixed event script, the
learner's state trajectory after a process restart with loaded
state is byte-identical to uninterrupted continuation. If the
learner can tell it was restarted, persistence is broken.

P7 (no task-label leakage): a probe that varies only the hidden
task identity while holding the event stream fixed produces
byte-identical learner behavior. If behavior branches on task,
the driver leaked and the test is void.

## Named gaps (not solved here; the substrate makes them learnable)

G1 (incremental executable construction): the L3B redesign target.
The workspace supports executable node structures; the algorithm
that builds them incrementally from experience is future work
under a fresh prereg.

G2 (uncertainty-contingent action): W6/W7. The generic ACT channel
exists in the event loop; the mapping from epistemic state to
action selection is future work. No constant-CHOICE plumbing is
counted as inquiry.

G3 (hierarchical/graph-native representation): W9. Nodes plus
typed links express hierarchy natively; traversal and
compositional query machinery is future work.

These gaps are named so the implementation cannot silently claim
them. A capability is claimed only when a frozen bar measures it.

## What this prereg does NOT authorize

- No implementation in this commit. The implementation worker
  builds only after this prereg is reviewed.
- No new Zag subsystems, modes, bridges, or task-specific
  handlers may be introduced by the implementation. Any such
  addition fails K2 at review.
- The surviving mechanisms are not copied as subsystems; they
  are re-expressed as workspace content per section (c).
- The eviction work is bounded: the bootstrap one-liner plus the
  three learner-owned structures. Any second round of
  cache-policy source edits is a treadmill signal and must be
  rejected at review.

## Kill bars for the implementation (frozen here)

K1: this prereg (frozen alone, before any implementation commit)
completely specifies the architecture: core, workspace,
integration per mechanism, eviction design, experience format,
event loop, accounting, predictions P1-P7, gaps G1-G3.

K2: the implementation contains zero task-specific handlers,
zero new hardcoded semantic cases, zero modes, zero bridges.
Verified by source inspection at review: grep for handler-like
dispatch on task/world identity must return nothing.

K3: pure Zag plus shell; zero Python at every step; all
documents dash-clean via the shell-only check_no_dash.sh; the
contaminated paper untouched; commits local with explicit
pathspecs under continuing_learner/ only.
