# ARCHITECTURE ACCOUNTING: the three killed TNN-2 mechanisms

Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
(commit f4de7ff46, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd, 1591 lines).
Question per mechanism: what did the researcher write vs what did
experience create? The capability-source delta question: why did the
frozen core fail to learn what the sealed worlds demanded?

## M1: runtime executable-graph construction (`t2_trial` family)

### Researcher-written structure

- The schema menu and its fixed search order (`t2_trial`, ~80
  lines): k-hop chains for k=2..4, then subset sums, then counts,
  then single-hop fallback. Order, depth cap (4), and family
  membership are researcher constants.
- The four assemblers (`t2_asm_chain`, `t2_asm_count`,
  `t2_asm_sum`, single-hop inline, ~75 lines): each maps a value
  path to a fixed guard-then-set cell pattern over the 4-op ISA.
  The mapping from data shape to graph shape is researcher code.
- Path enumeration (`t2_gather` BFS depth 1..4, `t2_chain`,
  `t2_rels`, `t2_gather_sum`, ~90 lines): what counts as a
  candidate is defined here.
- Verification and promotion (`t2_try_verify`, `t2_exec`,
  `promote_graph`, `t2_sig`, ~60 lines): the execute-against-
  expected oracle protocol, the MAP node layout (field4=relation,
  field8=subject, field20=graph root, field28=answer), DEP-edge
  licensing, and the taught answer fact.
- Fallback bootstrap (`bootstrap_miss`, k=3 invariant relation):
  researcher-defined.
- The 4-op ISA and `execute` (protected-core-class machinery):
  legitimately frozen, not at issue.

### Learner-owned structure (created by experience)

- MAP nodes keyed to (subject, relation); executable graph cells
  with stamped literal guards and sets; DEP edges from each cell
  to its licensing fact; taught answer facts; trial statistics
  (tried/rejected) packed into header field 16; P-INV bootstrap
  MAPs.
- In the sealed battery the learner created exactly the
  structures the schemas stamp: forward chains on demonstrated
  subjects (M1-W2 engagement: MAPs with LITS 41012/41013/41014),
  per-instance single hops (M3-W1 promotion: 4 MAPs), and 8
  UNCERT nodes for the unanswerable M1-W1 probes.

### What experience could never create

A fifth schema. A composition of two schemas. An inverted schema.
A step object shared between two graphs. A procedure object
addressable by anything other than (subject, relation). Every one
of these lives on the researcher side of the line, and the freeze
put the line out of reach.

### Capability-source delta

The delta is total for the sealed demands: meeting M1-W1/W2/W3
would have required new researcher-authored schemas (a compose
assembler, an invert assembler, a step-interning assembler).
Experience can fill guards and literals; it cannot add a schema.
The learner's "construction" is selection among researcher
options, which is why the battery's white-box finding is always
the same: the structure the world demanded is absent, and the
structure present is a stamped path.

## M2: learner-originated uncertainty guiding action (`miss_inquire` + `ev_act`)

### Researcher-written structure

- `miss_inquire` (~18 lines): on a true miss, allocates an
  UNCERTAINTY node (tag 30, fields subject/relation), a
  POLICY_ROOT node (tag 2) if absent, and a guide node (tag 1)
  with `write_node(W,g,30,-999,0,0)`: action field20=30 is a
  literal constant in researcher code; relation field24=-999.
  Edges: guide-DEP->UNCERT, POLICY_ROOT-type10->guide.
- `ev_act` (~40 lines): scans POLICY_ROOT-linked candidates,
  keeps those whose subject is in the 4-deep context ring and not
  superseded, picks max `bid()`, returns the winner's field20.
  The action alphabet, the context-membership gate, and the
  selection rule are researcher code.
- `bid()` (~12 lines): edge-type counts (DEP+SUP+USE+CFM-CON).
  A fixed bookkeeping formula, not an information measure; it
  cannot represent informativeness because no term in it does.
- `ctx_push`/`ctx_get`, `pol_get`/`pol_set`: researcher-defined
  state plumbing.
- Absent by construction: any code that supersedes a guide, any
  code that writes action content from uncertainty content, any
  resolution transition. `is_superseded` exists and `ev_act`
  honors it, but no cognition path ever marks a guide superseded.

### Learner-owned structure (created by experience)

- UNCERTAINTY nodes, guide nodes, the POLICY_ROOT node and its
  type-10 links, context-ring contents (which subjects were
  recently seen). In the battery: one guide per hidden key
  (M2-W1), one guide for 44101 that outlived its resolution
  (M2-W2), three guides whose actions were all 30 (M2-W3).

### What experience could never create

A second action value with meaning. A guide retirement. A mapping
from what-is-unknown to what-to-do. The UNCERT node records
(subject, relation) but no reader converts that record into
behavior; the guide's action field is written once, by the
researcher, as 30.

### Capability-source delta

The delta is total for the sealed demands: informant selection
needs a discriminating action alphabet driven by uncertainty
content; resolution needs a guide lifecycle; content
discrimination needs content-to-action encoding. All three are
control-plane properties. Experience creates guide nodes the way
a printer creates pages: the content was fixed before printing
began.

## M3: counterexample-driven revision (`revise_on_contradict` / `t2_revise_graph`)

### Researcher-written structure

- `revise_on_contradict` (~20 lines): on contradiction, scans
  all MAPs for a DEP edge to the contradicted fact node and
  invokes the single revision schema.
- `t2_revise_graph` (~46 lines): the one and only revision
  operation. Find the stale SETREG (tag 101) reachable via the
  DEP edge; tombstone it; insert a corrected SETREG holding the
  new literal; rewire SEQ edges; re-execute; on failure revert
  everything; on success mark the old taught fact superseded
  (CON self-edge) and teach the corrected answer.
- `t2_kill_edge`, the `ev_observe` contradiction path (mark old
  fact superseded, write history node, teach new fact node).
- Dormant infrastructure, present but never called from the
  cognition path: `contradict_map` (marks a MAP superseded),
  `map_standing` (SUP/CON edge balance), `evcount`, and the
  `log_ev` event log (records teach/query/act events no decision
  ever reads). These are called only from the test battery
  functions. The file contains the parts of an evidence model
  that the mechanism does not use.

### Learner-owned structure (created by experience)

- Patched SETREG literals (42110/42107/42108/42109 in M3-W1;
  43109 in M3-W2); tombstoned cells; rewired SEQ edges; CON
  self-edges on superseded facts; history nodes; corrected taught
  facts; updated MAP answer fields. The white-box record shows
  exactly these and nothing else.

### What experience could never create

A revision threshold (the trigger fires on any contradiction and
consults no count). A law representation above instances (the
schema edits one literal in one graph). A second revision on one
link (provenance anchors to the superseded fact node, so the
lookup misses). A recovery from a failed revision (revert plus
the stale taught fact, which `ev_query`'s exact-hit check reads
before the trial loop ever runs).

### Capability-source delta

The delta is total for the sealed demands: weighing evidence
needs the trigger to read support; generalization needs a law
object; repeated revision needs live provenance; recovery needs
unpromote-and-rederive. The schema's trigger, unit of change,
provenance discipline, and failure mode are all researcher-fixed.
Experience can pull the trigger; it cannot aim, reload, or clear
a jam. The dormant evidence machinery (`map_standing`,
`contradict_map`, `log_ev`) is the sharpest accounting detail:
the researcher wrote the instruments of an evidence model and
never connected them to the operator.

## Cross-mechanism headline

In all three mechanisms the line between researcher and learner
falls in the same place: the learner may create nodes and edges;
the researcher decides what creation means. Schemas, the action
alphabet, the revision operation, the trigger conditions, and the
selection rules are researcher code. Experience fills templates.
The sealed battery placed every demand on the far side of that
line: new schemas (M1), new action meanings and lifecycles (M2),
new revision policies (M3). A frozen core whose learning surface
is template-filling cannot meet demands that live in the control
plane, regardless of how much experience it receives. Retention at
12/12 confirms the corollary: the persistence side of the line
works fine. What is missing is not memory but generativity:
structures whose meaning the learner itself can extend.

Consequence for TNN-3, per the no-patch-treadmill rule: the fix
cannot be three more researcher schemas (a compose handler, an
informant policy, a counting trigger), because that moves the
line without erasing it. The fix must move capability across the
line: generic substrate affordances (abstraction objects,
lifecycle transitions, evidence-weighted control) that
experience, not the researcher, then uses to build the missing
behaviors. The hypotheses document proposes eleven such
substrate changes.
