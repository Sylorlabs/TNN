# TNN-2 Developmental Transfer Analysis

Date: 2026-10-01. Analyst: TNN-2 Developmental Transfer Analyst (subagent).
Frozen subject: TNN-2, commit `f4de7ff46`
(source `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
binary `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`).
Probe build: `tnn2_transfer/tnn2_transfer_bin` (frozen source with test main
replaced by probe main; TNN-2 functions byte-identical). All probes pure Zag.
Three deterministic runs; stdout byte-identical across runs.

Verdict: **TRANSFER-ANALYSIS-COMPLETE**. Findings are mixed, reported honestly
below. Headline: learned executable graphs persist in learner state and are
reused by the revision operator in place, but no promoted graph is ever
invoked for a new task; cross-task "transfer" is re-derivation by the trial
loop, and the durable cross-task memory is the promoted fact, not the graph.

## 1. Where constructed graphs persist (Q1)

All learner state is the caller-supplied workspace buffer `W` (110656 bytes).
On a verified trial, `promote_graph` (tnn2.zag:533) allocates:

- a MAP node (type 20): field4 = relation r, field8 = subject s,
  field20 = graph root cell, field24 = promotion index, field28 = answer;
- ET_DEP provenance edges from the MAP to each licensing fact;
- a type-1 FACT node `(s, r, answer)` via `ev_teach_in`.

The graph cells themselves (MOVE/BRANCHEQ/INC/DEC tags 101-104, literals
tag 902) persist as ordinary nodes in `W`. Nothing is task-local: the MAP,
its cells, and its provenance all survive subsequent unrelated teaches and
queries within the same workspace lifetime (P1: MAP node 45 identical before
and after 40 unrelated events; re-execution of its root still returns 5).

Source-level audit of every reader of type-20 MAP nodes in learner cognition:

- `t2_trial` (4 call sites): WRITES new MAPs via `promote_graph`.
- `revise_on_contradict` (line 690): READS MAPs to find those licensed by a
  contradicted fact, then rewrites them in place.
- No other cognition function scans type-20 nodes. `ev_query`,
  `activate`, `t2_gather`, `t2_gather_sum`, `t2_rels`, `t2_chain` read only
  type-1 FACT nodes. `execute`/`t2_exec` are called only from the trial
  verifier, the revision re-verifier, and tests.

Consequence: a promoted graph is never executed for any later query, for
the same subject or a new one. The artifact that serves future identical
queries is the promoted FACT (exact `(s,r)` hit in `activate`), not the
graph. The graph's only later cognitive use is as the operand of revision.

## 2. Cross-task reuse: rebuild, not invocation (Q2)

P2 (single shared workspace): chain `(1,11,2..5)` promoted as MAP for
`(1,40)`; then an isomorphic chain taught for subject 7 and queried:

- `P2 oldroot_on_7 = -999999`: executing subject-1's graph with subject 7 in
  the frame fails closed (the BRANCHEQ guard on literal 1 has no fallthrough;
  `execute` returns -999999). Graphs are subject-bound by construction:
  literals bake in the originating subject's values, so direct reuse is
  architecturally impossible, not merely untested.
- `P2 maps_before = 1`, `P2 maps_after = 2`: the trial loop assembled a
  FRESH graph and promoted a second MAP (node 91), rather than invoking the
  first.
- `P2 sig1 = P2 sig2 = 8` cells with identical tag sequences: the new graph
  is an isomorphic rebuild (same procedure shape, different literals).
- `P2 first_requery = 5`: the first structure still answers its own subject.

So what "transfers" across tasks is the trial loop's procedure for
re-deriving structure from the new subject's facts, plus the persisted facts
themselves. There is no mechanism by which a learner-built executable
structure is CALLED for a new task: the frozen 4-op ISA has no CALL/JUMP
opcode, the assemblers (`t2_asm_chain`, `t2_asm_count`, `t2_asm_sum`) never
reference existing MAPs, and no cognition path passes a stored root to
`execute` except the trial that built it and the revision verifier.

## 3. Revision output is reused in place (Q3)

P3: 2-hop chain `(101,40)` promoted (answer 201); `ev_observe(102,12,999)`
contradicts a licensing fact:

- `P3 observe_ret = 0` (contradiction registered),
  `P3 same_map_node = 0` (identical MAP node id before/after),
  `P3 map_ans_field = 999`, `P3 reexec_after_rev = 999`,
  `P3 requery = 999`.

Revision is in-place mutation of the same MAP node (stale SETREG cell
tombstoned, corrected cell inserted, guard rewired, MAP answer field
updated), re-verified by re-execution, and the revised graph persists as the
MAP's content. It is not rebuilt from scratch: the trial loop is not
re-invoked on contradiction of a licensing fact.

A second, structurally different repair (3-hop chain, stale link at a
different position, answer 304 -> 777) succeeded through the same machinery
(`P3 requery2 = 777`, `P3 map2_ans_field = 777`), and the first revision was
undisturbed (`P3 first_still = 999`). So the revision operator generalizes
across at least two repair positions and chain lengths, and its output is
the reused, persisting form of the structure.

Caveat for the revision red team (not re-litigated here): the repair
procedure itself (find stale SETREG via provenance, tombstone, insert,
rewire) is researcher-authored; what the learner contributes is the
provenance graph the repair indexes into. Whether that counts as
learner-chosen repair topology is their question.

## 4. Interference profile (Q4)

Design: build the `(1,40)` chain MAP, then apply heavy teach pressure and
re-check MAP survival, cell survival, re-executability, and re-query.

Eviction mechanics (source): 1024-node budget; `alloc_node` evicts the
lowest-bid unprotected node, scanning upward from a cursor (ties broken
oldest-first). Bids: facts carry a self PRO edge (type 9, clock 12, decayed
once per event, refreshed on hits via `ref_prot`); MAP nodes carry self SUP
(type 2) + USE (type 6) edges for a standing bid of 2 but NO protection
edge; graph cells (101-104) and literals (902) have bid 0 and no protection.

P4 result (1050 teaches past the eviction threshold, 3x byte-identical):

- `P4 live_nodes = 1022` (at cap), `P4 map_alive = 1`,
  `P4 facts_alive = 1021`, `P4 opcells_alive = 0`,
  `P4 reexec = -999999`, `P4 requery = -2`, `P4 maps_total = 1`.

Reading, in eviction order:

1. The executable structure dies first. All 101-104 cells (the winning
   8-cell graph AND the 10 rejected-trial garbage cells, which are never
   deallocated) were evicted: bid 0, unprotected. The graph is the most
   fragile thing in the workspace.
2. The MAP outlives its graph and becomes a fossil. Node 45 still has
   tag 20 (bid 2 beats the zero-bid sweep), but its root cells are gone
   (`reexec = -999999`), its licensing facts were evicted (DEP provenance
   edges removed with them), so it can never be revised or executed again.
   It is inert, unrevisable, unreclaimable-until-last.
3. The promoted fact (the actual durable answer memory) was also evicted,
   along with the four licensing chain facts: their PRO clocks expired
   after 12 events and the cursor sweep kills oldest zero-bid nodes first.
   Hence `P4 requery = -2`: the learned answer is catastrophically
   forgotten, and it cannot be rebuilt because the licensing facts are
   gone too.
4. Degradation is graceful at the interface level: the forgotten query
   falls through trial (no facts) and P-INV bootstrap (no same-relation
   facts) into `miss_inquire`, re-creating UNCERTAINTY + guide. The system
   reverts to inquiry rather than confabulating.

Interference profile summary: coexistence holds while under budget (P1:
40 unrelated events, zero disturbance; P2/P3: parallel structures and
revisions do not interfere). Past budget, forgetting is catastrophic for
the specific learned answer and destructive for the executable structure,
while the MAP record lingers as a fossil. There is no protection for
"important" old structures beyond the MAP's bid of 2, and no
consolidation mechanism that converts a fragile graph + facts into a more
durable form. This is a genuine architectural weakness for a continuing
learner: the better the trial loop gets at building structures, the faster
it fills the workspace with unreclaimable trial garbage and fossil MAPs.

## 5. Comparison against TNN-1 (Q5)

TNN-1 (`tnn1_act.zag`): the miss path built one of three FIXED plan
templates (`plan_c2`/`plan_g`/etc.), executed it with the SEPARATE
`exec_plan` interpreter (a 6-kind plan-step vocabulary, not the 4-op ISA),
and promoted the template instance via `promote_map`. TNN-1 therefore had:

- construction: NO (selection among researcher-authored templates);
- cross-task graph invocation: NO (same fact-cache mechanism as TNN-2);
- graph revision: NO (contradiction caused standing demotion only).

TNN-2 improves on TNN-1 by exactly the three frozen changes: runtime
assembly of graphs from primitive cells through the single frozen executor
(Q1/Q2: the structure is genuinely built at runtime, even though it is
rebuilt per subject rather than reused); the miss-to-guide-to-act path
(P5: guide persists across 40 unrelated events, `ev_act` returns 30 before
and after); and in-place topology revision (Q3). What did NOT change:
the promoted FACT remains the durable cross-task memory in both
generations, and neither generation invokes a stored executable structure
for a new task.

## 6. C0-D assessment (cognitive reuse)

Micah's C0-D requires the invented structure to improve transfer,
prediction, procedure learning, causal inference, memory, planning, or
sample efficiency; existence alone is insufficient.

Honest scorecard for TNN-2's three mechanisms:

- Runtime construction: the built graph demonstrably produces the answer on
  the trial that built it, and its provenance enables revision. But no
  second task has yet been shown to go faster, succeed where it otherwise
  would fail, or reuse the built structure rather than rebuild it. The
  P2 isomorphic rebuild is re-derivation, not reuse. C0-D NOT demonstrated
  for construction.
- Inquiry (uncertainty -> guide -> act): the guide persists and continues
  to drive `ev_act` (P5: 30 before and after unrelated work), which is
  persistence, not yet reuse-for-improved-capability. Whether later
  evidence updates later behavior through the guide is untested here.
  C0-D NOT demonstrated for inquiry.
- Revision: the revised graph is reused (it IS the persisting MAP content
  and answers later queries), and the same operator repaired two
  structurally different cases. This is the closest to genuine reuse, but
  the "reuse" is of the researcher's repair procedure applied to
  learner-built content, and no experiment shows revision making a
  subsequent NEW task easier. C0-D WEAK/PARTIAL for revision.

Overall: TNN-2 satisfies persistence (structures outlive their creating
task in learner state) but has not demonstrated cognitive reuse in the
C0-D sense. The architecture as frozen lacks any invocation path from a
new task to a stored executable structure (no CALL, no MAP lookup in the
trial path, subject-bound literals). A future generation that wants C0-D
must add a principled reuse path (e.g., parameterized graphs callable with
a fresh frame, or trial seeding from existing MAPs), which is itself an
architectural decision to bank, not a patch.

## 7. Architectural facts relevant to compression (for the compression lane)

- Rejected trial candidates are never deallocated: every failed assembly
  leaves its cells allocated in `W`. Under sustained trial activity this
  garbage is the dominant node consumer and the first eviction victim.
  A generational or explicit free for trial scratch would shrink working
  memory without touching capability.
- The MAP node duplicates what the promoted FACT already provides for
  same-`(s,r)` queries; the MAP's unique cognitive role is (a) provenance
  for revision and (b) the re-executable graph. If revision indexed
  provenance another way, the MAP/FACT duplication is compressible.
- `bootstrap_miss` (P-INV) promotes degenerate MAPs (root field 0) that no
  revision or execution path can use; they are pure provenance records.

## 8. Probe log

- `transfer_driver.zag`: 5 probe sets (P1 persistence, P2 cross-subject,
  P3 revision reuse, P4 interference, P5 guide persistence), 177 lines,
  appended to frozen source with test main removed.
- `tnn2_transfer_bin`: built with pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1` (analyzer warnings only,
  same class as frozen build).
- `probes_run1.txt`, `probes_run2.txt`, `probes_run3.txt`: stdout, 3x runs,
  byte-identical (`cmp` clean).
- Determinism: all five probe sets byte-identical across runs, including
  the 1050-teach P4 pressure run.
