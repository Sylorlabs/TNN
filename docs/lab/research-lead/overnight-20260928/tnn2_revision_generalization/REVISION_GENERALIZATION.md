# TNN-2 Revision Generalization Analysis

Date: 2026-09-30. Status: ANALYSIS ONLY. This document is not a patch,
not a design commit, and not TNN-3. It informs TNN-3 root-cause clustering.

## Framing

The revision red team (commit `687ba0219`, REVISION-ATTACK-SUCCESS) found
that TNN-2's `t2_revise_graph` is a single-schema literal-patch: tombstone
a BRANCHEQ-guarded SETREG, insert a new SETREG holding the observed
literal. The learner chose operands (which cell, which value); the
researcher chose the topology. `t2_trial`, TNN-2's genuine construction
search, is never invoked by the revision path. C0-A/B/C fail; C0-D is
unestablished.

This analysis asks what genuine multi-topology revision would require
architecturally. Evidence basis: `tnn2.zag` at `f4de7ff46` (frozen,
read-only), prereg `7c1e30522`, red team `687ba0219`. Line numbers below
refer to `tnn2.zag`.

---

## 1. Could the existing `t2_trial` machinery be wired into the revision path without new opcodes, modes, bridges, or handlers?

Short answer: the execution and verification halves can be; the proposal
half cannot, because `t2_trial` has no repair-proposal generator. Wiring
it in requires adding one, which is new generic machinery but not a new
opcode, mode, bridge, or handler.

### What revision already has at the trigger point

`ev_observe` (line 836) detects a contradiction on fact node `n` and calls
`revise_on_contradict(W, n, o)` (line 847) with:
- the fact node `n` carrying fields 20=s (subject), 24=r (relation),
  28=old output;
- `o`, the newly observed output, i.e. post-hoc feedback (the E-ruling
  already legitimizes `expected` as post-hoc feedback in `t2_trial`).

`revise_on_contradict` (line 685) locates MAP nodes (tag 20) with an
ET_DEP edge to the contradicted fact. The MAP node carries:
- field 20: graph root, field 8: s, field 4: r, field 28: promoted answer;
- ET_DEP edges to every licensing fact (set in `promote_graph`, line 543);
- each SETREG step carries an ET_DEP edge to its licensing fact
  (`t2_asm_chain` line 373, `t2_asm_count` line 390).

### The pieces of `t2_trial` that are reusable as-is

- `t2_exec(W, root, s0)` (line 412): runs any candidate graph on a fresh
  frame; returns -999999 on failure. Already graph-agnostic.
- `t2_try_verify(W, root, s0, expected, masked, st)` (line 497): verifies
  any candidate graph against an expected value and records tried/rejected
  stats in header field 16. The contradiction event supplies a legitimate
  `expected` (the observed `o`).
- The cell assemblers `t2_lit`, `t2_set`, `t2_guard`, `t2_mov`, `t2_inc`
  (lines 338-361), `seq_link` (line 318), `t2_kill_edge` (line 679):
  all the primitive edits needed to build repaired graphs already exist.
- The revert discipline in `t2_revise_graph` (lines 732-744): re-execute,
  revert everything on failure, return 0. A search loop would keep this
  per-candidate and promote only the verified winner.

### The missing piece: a repair-proposal generator

`t2_trial` proposes by assembling fresh graphs from gathered value paths
(`t2_gather`, `t2_asm_chain`, `t2_asm_sum`, `t2_asm_count`). It never takes
an existing graph as input. Revision needs the dual operation: given the
stale graph and the contradiction, enumerate candidate *edits* to that
graph. Concretely, the architecture would be:

1. Blame localization: from the contradicted fact, walk provenance edges
   to the step(s) implicated, as today, but over all step types.
2. Edit enumeration: for each candidate blame site, apply edit operators
   drawn from a repair family (see section 2) using the existing cell
   assemblers, producing candidate repaired graphs as fresh cell sets that
   share the unedited remainder of the original graph (tombstoning only
   after a winner verifies, preserving the current revert discipline).
3. Verification: run each candidate through `t2_try_verify` against the
   triggering observation `o`, and additionally against the other
   licensing facts reachable from the MAP's ET_DEP edges (section 3).
4. Promotion: keep the first verified repair under a minimality ordering;
   on total failure return 0 exactly as today.

None of this needs a new ISA opcode: every edit is node allocation, field
write, edge link/kill, and EXECUTE over the frozen 4-op ISA, all of which
`revise_on_contradict` already performs. No new mode is needed: the
contradiction handler remains the single entry point, and the search runs
inside it. No new bridge or handler is needed: the trigger (`ev_observe`
-> `revise_on_contradict`) and the executor (`execute`) are unchanged.

The honest boundary: the repair-proposal generator is *new generic
machinery*. It is not a mode, bridge, or handler, but it is researcher
code the prereg did not specify. Under the One-System Rule it reads as
acceptable (generic machinery operating on the single executable-graph
type, no task-specific dispatch), provided its repair family is a genuine
space and not a second single-schema procedure wearing a loop.

### One asymmetry to preserve

`t2_trial` searches to *find any graph that works*. Revision searches to
*find a graph that still works on everything the old graph got right*.
The verification set for a repair is therefore larger than the triggering
observation: the MAP's ET_DEP edges to licensing facts give a retained
test set for free. The current literal-patch re-verifies only against the
triggering observation (line 732) and then teaches the new answer (line
760). A search-based revision that did not check the retained licensing
facts would risk fixing one case while breaking previously correct ones.
That retained set exists in learner state today and is unused by revision.

---

## 2. A multi-member repair space: five structurally different repair topologies

Each of these is a repair the current operator cannot express (it always
produces guard -> new-SETREG(literal) -> succ with the old SETREG
tombstoned).

### Repair 1: Guard-predicate edit

Change the BRANCHEQ cell's comparison literal (field 8) or tested slot
(field 4) instead of touching the guarded step. Applicable when the
counterexample means "this branch should fire on a different value" or
"this branch tests the wrong register". Example: a chain graph whose
guard tests slot0 == 102 when the relation now keys on 103. The
researcher-authored constant is the predicate, not the payload.

### Repair 2: Branch rerouting to an existing step

Repoint a guard's true-target (field 12) or a SEQ edge to an already
present step rather than inserting a new cell. Applicable when the graph
already computes the right value somewhere else and the fault is purely
routing. This is the reuse-over-insertion repair; the current operator
always allocates fresh cells and can never discover that the answer was
already in the graph.

### Repair 3: Multi-step coordinated repair

Revise two or more stale steps in a single contradiction event. Chain
graphs have plen-1 SETREG steps; a systematic value shift (every link's
target changes) breaks all of them. The current operator fixes one step
per call (`stale` is a single variable, line 709) and requires a second
contradiction event against the already-revised graph, which may no
longer be in revisable shape (the red team notes this at probe 7).

### Repair 4: Step-count / step-type conversion in unrolled sequences

Applicable to sum graphs (unrolled INC chains) and count graphs:
- adjust the unroll length (correct total is 7, graph has 5 INC cells:
  insert 2; correct total is 3: delete 2);
- convert INC to DEC (sign repair) when the counterexample shows the
  accumulation runs the wrong direction;
- convert a SETREG constant into a MOVE (the red team notes the current
  operator can silently turn a register copy into a constant when the
  stale cell happens to be a MOVE, probe 5).

### Repair 5: Step deletion without insertion

Tombstone a spurious step and rewire around it: guard/SETREG pair that
now misfires, a stray MOVE, a duplicated link step. The current operator
always inserts (lines 725-726); there is no code path that tombstones
without inserting. Deletion is also the repair that a "revert to an
earlier regime" scenario needs: when new evidence shows an added step
was the mistake, the fix is removal, not another insertion.

(Adjacent members worth naming for the record: literal re-derivation
where the replacement value is computed or selected among alternatives
rather than copied from the observation; guard insertion splitting one
branch into two; sub-graph replacement reusing a promoted MAP from a
different relation, i.e. cross-MAP repair.)

---

## 3. What information the learner needs per repair, and whether TNN-2 has it

### Information need A: blame localization (which step is at fault)

Available in learner state only for SETREG steps. SETREG cells carry
ET_DEP edges to their licensing fact (lines 373, 390), which is how the
current operator finds `stale` (lines 711-717). But:
- Guard cells (102) carry NO provenance edge to any fact. A
  guard-predicate fault (Repair 1) cannot be localized through current
  state; the operator does not even look at guards except as rewire
  anchors (lines 719-724).
- INC cells in count graphs carry no DEP edge (only the paired SETREG
  does, line 390). INC cells in sum graphs carry no fact links at all
  (`t2_asm_sum`, lines 398-410, links nothing).
- DEC cells (104) are never constructed by any assembler, so no
  provenance convention exists for them.

A search-based revision needs blame hypotheses over all step types, which
requires provenance edges on guards and arithmetic cells, or a
counterfactual method (re-execute with each step perturbed and observe
which perturbation restores the expected output; `t2_exec` already makes
this possible, but nothing calls it that way).

### Information need B: the verification set

Partially available, mostly unused. The triggering observation `o` is
available at the call site. The MAP's ET_DEP edges to all licensing
facts (line 543) give a retained set of (s, r, old-o) cases that the
repaired graph should still satisfy; revision never consults them. Note
one subtlety: after `ev_observe` teaches the new fact (line 853) and
contradicts the old node (line 846), the retained set must be read as
"all licensing facts except the contradicted one, plus the new
observation". That bookkeeping is implementable from current state.

### Information need C: disambiguation among repairs that all fit the observation

Not available. A single observation underdetermines the repair: a
guard-predicate edit and a literal swap can both explain one
counterexample. Selecting between them requires either (a) retained
discriminating cases from history (the licensing facts help only if they
discriminate, which is not guaranteed), (b) a record of previously
tried and rejected repairs (no such record exists; tombstoned cells are
deactivated and their history is lost), or (c) active inquiry: generate a
discriminating query and observe the answer, which would integrate
Change 2's miss-to-guide machinery into the revision loop. None of (a)
through (c) exists in current learner state.

### Information need D: a repair ranking criterion

Not available in learner state. With several verified repairs, the
learner needs a preference: fewest edited cells, fewest new allocations,
preservation of the most licensing facts, or simplest resulting
topology. Today there is no choice to rank, so no criterion exists
anywhere. If a researcher hardcodes "fewest edits wins", that is a
researcher-authored search bias. That bias is in the same class as
`t2_trial`'s existing composition-preserving search order (longer chains
before sums before counts, lines 592-598): an ordering heuristic over a
genuine space, not a single-schema procedure. It does not by itself kill
a generality claim, but the learner-authored version (the learner
promoting its own minimality preference from revision experience) is the
L3-grade step and is entirely absent.

### Information need E: repair history (what was tried before)

Not available. `t2_trial` packs tried/rejected counts into header field
16 for construction; revision keeps no analogous record. Successive
revisions, including reverting to an earlier regime, need the learner to
remember which repairs were attempted on which graph and why they were
abandoned. Tombstoning deactivates cells without preserving that
rationale.

### Summary table

| Need | Repair types | Available today |
|---|---|---|
| Blame over SETREG steps | literal-patch only | Yes (DEP edges) |
| Blame over guards / INC / DEC | Repairs 1, 4, 5 | No (no provenance edges; no counterfactual use of t2_exec) |
| Triggering observation | all | Yes (call-site `o`) |
| Retained licensing cases | all (regression check) | In state, unused (MAP ET_DEP edges) |
| Disambiguation of ambiguous repairs | Repairs 1 vs literal, 2 vs insert | No (no rejected-repair record; no inquiry integration) |
| Ranking criterion | any multi-candidate search | No (researcher would hardcode it) |
| Repair history | successive / revert repairs | No |

---

## 4. Minimal architectural change for genuine search over repairs

### (a) Changes within the frozen ISA

All of the following use only existing operations (node allocation, field
write, edge link/kill, the four cell tags, EXECUTE) and the existing
contradiction entry point:

1. Extend the provenance convention so every cell type carries an ET_DEP
   edge to its licensing fact at assembly time (guards in `t2_asm_chain`
   / `t2_asm_count`, INC cells in both, and any DEC cells a future
   assembler creates). This is a graph-edge convention, not an ISA
   change.
2. Replace the single-schema body of the revision operator with an
   edit-enumeration loop: for each blame-site hypothesis from provenance,
   generate candidate repaired graphs by applying edit operators (the
   section-2 family) with the existing assemblers, leaving the original
   graph intact until a winner verifies.
3. Verify each candidate with `t2_try_verify` against the triggering
   observation plus the MAP's retained licensing facts (minus the
   contradicted one).
4. Promote the first verified candidate under a fixed minimality
   ordering (fewest edited cells, then fewest new allocations); keep the
   existing revert-on-total-failure discipline and return 0 when nothing
   verifies.
5. Record tried/rejected repair counts in learner state, mirroring
   header field 16's construction stats, so revision leaves a trace.

This stays inside the ISA freeze, adds no mode/bridge/handler, and keeps
`revise_on_contradict` as the single entry point. It converts
single-schema patch into search over a researcher-enumerated repair
family. That is a genuine generality upgrade (L2-grade structural search,
comparable to what `t2_trial` does for construction) and it is still not
L3; see the ceiling note below.

### (b) Changes requiring new machinery (judgment calls)

1. A learner-owned repair grammar. As long as the edit operators are a
   fixed researcher-written set, the finite-menu problem the red team
   identified for construction applies one level up: the learner searches
   a researcher-enumerated family. Genuine C0-B needs the learner to be
   able to extend the repair family itself, e.g. promoting "INC-to-DEC
   swap" to a reusable edit operator after it succeeds twice. That is new
   machinery: edit operators as learner-created persistent structures,
   not source functions.
2. Ambiguity-driven inquiry. Disambiguating repairs that all fit current
   evidence needs the learner to generate a discriminating query and
   route the answer back into revision. That integrates the Change 2
   inquiry loop (uncertainty -> guide -> POLICY_ROOT -> ACT) with the
   revision loop. It is integration of existing mechanisms, but the
   coupling (a revision that suspends itself pending an inquiry result)
   is new control machinery and needs careful design to avoid becoming a
   new mode.
3. Cross-MAP repair reuse (Repair 2 generalized: borrow a verified
   sub-graph from a different MAP). This needs a sub-graph addressing
   scheme the current MAP layout does not provide; MAPs are atomic
   promotion units.

The line between (a) and (b): (a) widens the search inside researcher-set
bounds; (b) moves the bounds themselves into learner state. Micah's
Criterion 0 draws the L3 line at (b).

### Ceiling note, stated plainly

Even a perfect implementation of (a) yields search over a
researcher-enumerated repair family. If the construction red team finds
that `t2_trial`'s candidate grammar (chain/count/sum assemblers, depth
<= 4, sums as unrolled INC <= 900) is itself a finite researcher-authored
menu, then wiring revision into the same proposal machinery inherits the
same bound. The honest claim for (a) is "generic structural search over a
fixed repair family", which is L2, not L3. L3 requires (b): the repair
topology space itself must be learner-extensible, with at least one
demonstrated case of the learner employing a repair shape no researcher
enumerated.

---

## 5. Why the builder implemented literal-patch instead of search-based revision

Three contributing causes, in descending order of explanatory weight.
This is a causal attribution, not an excuse; all three were avoidable.

### Cause 1: the kill bar admitted it (strongest cause)

The prereg's prose for Change 3 was genuinely ambitious: "retarget a
branch, adjust a loop bound, insert or remove a step" (`7c1e30522`,
section 2). But K-T2-6, the bar that actually governed acceptance, read:
"A promoted executable graph is restructured (topology change, not
standing change) after a counterexample in at least one test."
The implemented operator satisfies this bar's letter exactly once: one
topology change, in one test (T2-REVISE), with standing untouched. The
bar measured the existence of a topology edit, not search over repairs,
not multi-schema coverage, not learner choice of topology. A
single-schema operator is the minimal-cost satisfier of an
existence-only bar. The prereg constrained the words; the kill bar
constrained the code; the code followed the bar.

### Cause 2: complexity tradeoff under a missing design (real, secondary)

`t2_trial` builds graphs from value paths; it has no notion of editing an
existing graph. Wiring it into revision is not a one-line call; it
requires designing blame localization, an edit-operator family, and a
verification set, none of which the prereg specified. The builder faced a
genuine design gap and chose the shortest path to K-T2-6 rather than
filling it. Note this was a choice, not a necessity: section 4(a) shows
the gap is fillable within the frozen ISA. The prereg's silence on the
proposal mechanism is itself a prereg weakness; "generic revision
operator" named a property of the output, not a mechanism.

### Cause 3: a conceptual gap in the prereg framing (real, tertiary)

The prereg framed revision as "the operator restructures the graph": an
operator-centric framing that invites a procedure. The red team's
corrective reframe is revision-as-search: "the revision path invokes the
trial/search machinery over a space of repair candidates with more than
one member." Nothing in the prereg required the search framing, and the
T2-REVISE test the builder wrote could only discriminate the
literal-patch schema (it asserts the re-executed graph yields the
observed literal, which is exactly what a memorizer does). The test
suite could not have caught the generality failure because it was shaped
like the implementation.

### What this implies for the kill-bar process

K-T2-6 is the instance of a general failure mode: a bar that says "in at
least one test" for a generality property will be satisfied by the
minimal schema that passes that test. Future revision bars should require
at least two structurally different repairs (from the section-2 family)
on sealed graphs, with the corrected content derived rather than copied
from the observation, and with the retained licensing facts checked. That
recommendation is process advice for TNN-3 preregistration, not a code
change.

---

## Implications for TNN-3 root-cause clustering

1. The revision failure clusters with the construction bound: both are
   "researcher-enumerated family searched by learner-executed loop"
   (L2), not learner-defined spaces (L3). If the construction red team
   confirms a finite menu in `t2_trial`, revision and construction share
   one architectural cause: proposal spaces live in source, not in
   learner state.
2. The provenance gap (guards and arithmetic cells lack DEP edges) is a
   concrete, small, within-ISA defect that blocks even L2-grade revision
   of Repairs 1, 4, and 5. It belongs in the cluster, not as a
   per-world patch.
3. The kill-bar formulation weakness ("in at least one test") is a
   process cause, not an architecture cause, but it explains why the
   architecture cause survived review. Record both; fix the bar before
   TNN-3.
4. Do not answer this analysis with a better literal-patch. The
   red-team's section 7 stands: the next revision mechanism must invoke
   search over a multi-member repair space, verify against retained
   licensing facts, and leave a tried/rejected trace. Anything less is
   the treadmill.

## Verdict

REVISION-GENERALIZATION-ANALYSIS-COMPLETE
