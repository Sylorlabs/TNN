# TNN-3 Substrate Design: Trial-Reclamation Integration

Lane TNN3, wave-20261002-1121pdt, queue item 14.
Status: DESIGN ONLY. No substrate code changed this wave. This document is
the architecture-accounted design the task requires, plus the frozen
proposal for the first experimental test and a self red-team.

Provenance: grounded in `tnn2.zag` (tnn2_build, 1591 lines, the frozen
TNN-2 integration), the eviction-corruption root-cause analysis
(`986c52fdc`, eviction_corruption/EVICTION_CORRUPTION.md), the utility
builder's structure-atomic reclaim (`c912b9b19`, utility_build/BUILD.md),
the H-BASECERT-1 eviction latency cliff finding, and the mini-lifetime
infeasibility note (100x cost growth from full-table scans plus
destructive eviction under saturation).

## 1. Problem: trial garbage and the global-scan eviction path

A trial is any speculative executable structure the learner assembles,
executes, and then keeps or discards: `t2_trial` miss-policy candidates
(`t2_asm_chain`, `t2_asm_sum`, `t2_asm_count`), revision drafts in
`t2_revise_graph`, composition adaptation candidates. The verified
winner is promoted (`promote_graph`); every rejected candidate's cells
stay allocated. Nothing frees them. Current code confirms this: on
`t2_try_verify` rejection, `t2_trial` frees zero cells and zero edges.

Trial garbage volume per miss (from `tnn2.zag`):

- chain candidate: 4 cells per link (2 literal + 1 guard + 1 set), so a
  4-chain leaves 16 cells; `t2_gather` caps at 96 paths, tried k=2..4.
- sum candidate: up to 900 INC cells per candidate (`t2_asm_sum` skips
  totals above 900, so the worst live case is near 900).
- count candidate: 5 cells per link plus epilogue.
- every candidate: 1 frame node from `t2_exec`, plus DEP edges from
  trial cells to licensing facts (`link_edge(W,st,1,factn,0)`).

The only reclaim path is `evict_node`: at capacity, `alloc_node` falls
through to a global scan. Per eviction: 1024 candidates, each paying
`is_prot` (4096-edge scan) plus `bid` (five `evcount` 4096-scans, one
more 4096-scan, plus per-MEM-edge fanout), then a 4096-edge cleanup
sweep. That is on the order of 30M primitive ops per at-capacity
allocation (H-BASECERT-1 measured ~0.8s CPU), and every subsequent
allocation re-triggers it. The capacity plan
(`problems x 40 + teaching < 1024`) is explicitly gated on "until the
reclamation frontier lands." This design is that frontier.

Two properties make trials the right first reclamation target:

1. The learner knows exactly which cells are dead. A rejected trial's
   cells are known by construction: the assembler created them during
   the trial window and no other structure references them. No scan is
   needed to discover deadness; discovery is the current design's
   entire cost.
2. Trial garbage is the dominant dead-cell source under miss-heavy and
   bulk-teaching workloads (bulk MAP teaching via direct `t2_trial`
   calls is the redteam2 scaling path; each miss leaves its rejected
   candidates behind).

## 2. Design

### 2.1 The ownership invariant (what makes scan-free teardown sound)

Trial teardown is sound without reference scanning because of a
by-construction invariant:

**A cell allocated by a speculative assembler during trial T has no
incoming references from outside T.**

Proof sketch from the existing code: assemblers (`t2_lit`,
`t2_guard`, `t2_set`, `t2_inc`, `t2_mov`, `t2_cell`) allocate fresh
cells via `alloc_node` and link only (a) within the current trial's
fresh cells via SEQ/BEQ edges, and (b) outward to pre-existing
licensing facts via DEP edges. No pre-existing structure can reference
a cell that did not exist when it was built, and no assembler ever
looks up or links into another trial's cells. The only outward edges
are trial-cell to fact; freeing those edge slots touches no live
structure. This is strictly stronger than what `evict_node` can assume,
and it is exactly the gap the eviction-corruption analysis identified:
the retention system cannot see field-based references, so it cannot
safely reclaim by scanning. Trial teardown does not scan for
references at all; it frees exactly the cells and edges the trial
created, which the trial recorded.

Fail-safe: teardown aborts (leaving the trial for the ordinary
eviction path) if any trial cell carries a type-9 PRO edge or is named
by a live MAP root field. The invariant is asserted, not assumed.

### 2.2 Trial ledger: learner-owned state

New learner-state structure 1: the **trial ledger**, a chain of
fixed-size chunk nodes built from the existing tag-2 GROUP node type
(no new node kind). `trial_begin` allocates a ledger head for the new
trial and records it in a new header field (56: current trial id).
Every speculative allocation site (the `t2_*` cell constructors and
`link_edge` calls inside assemblers) appends the allocated cell id and
edge id to the current trial's ledger when header 56 is nonzero.
`link_edge` already returns the edge id, so recording is O(1) per
edge; no scan.

Ledger record per trial: trial id, status
(ASSEMBLING / REJECTED / PROMOTED / SWEPT), root cell, tick opened,
tick closed, chunk chain of (cell id, edge id) pairs. Ledger chunks are
allocated inside the trial's own budget, so sweeping a trial frees its
ledger too. The ledger is white-box learner state: the learner can
read its own trial history, which is also the substrate the
reclaim-regret policy (2.6) reasons over.

Boundedness: the ledger keeps at most G generation records (G is
learner-policy state, initialized to a neutral small value and adapted
by regret, never a researcher constant in the promoted design);
superseded generation records are compacted. The registry cannot leak:
every record's chunks die with its trial, and PROMOTED records are
owned by their MAP and die with the MAP's atomic reclaim.

### 2.3 Teardown: O(cells + edges), zero scans

`trial_end(REJECTED)`: walk the trial's chunk chain; for each recorded
cell id, zero the slot (`ns` field 36 to 0, fields cleared as
`alloc_node` does) and push it onto the free list (2.4); for each
recorded edge id, set edge source to -1 and decrement the edge count.
Cost is linear in the trial's own cells plus edges. No 1024-node scan,
no 4096-edge scan. The 40-op-per-element constant in the kill bars
covers the handful of `ns`/`es` writes per element.

`trial_end(PROMOTED, m)`: ownership transfer. The trial's cells become
MAP m's executable structure; the ledger record is marked PROMOTED and
linked from the MAP. They are no longer sweepable as trial garbage.
MAP-level retention (fossil detection, structure-atomic reclaim from
the utility builder) handles them later, and that path is extended to
return cells to the same free list.

Revision drafts (`t2_revise_graph`) route through the same
`trial_begin`/`trial_end`: the corrected-step draft is a trial; on
verification failure the draft is swept instead of leaving tombstoned
cells and dead DEP edges as it does today.

### 2.4 Free list: O(1) allocation before any scan

New learner-state structure 2: the **free list**. Freed cell slots
chain through field 20 (dead cells have all fields zeroed by the
reclaim path, so field 20 is scratch); the head lives in new header
field 52. `alloc_node` order becomes:

1. pop free-list head (O(1));
2. else linear scan for field-36 == 0 (unchanged);
3. else trial-sweep: reclaim REJECTED trials, oldest first, per the
   learner's sweep policy (2.6), then retry the free list;
4. else `evict_node`, unchanged, as the last resort.

Edge slots get the same treatment via the existing free-slot
convention (`eg(W,e,0) == -1`); teardown writes freed edge ids to a
small edge free stack or simply relies on the linear first-free scan,
which is O(1) amortized when teardown just freed a run of slots. The
design leaves the edge-scan as is and measures it; if it shows up in
profiles, the edge free stack is the follow-up, not this design.

### 2.5 Composition with the existing eviction hook

"The eviction hook" here means the at-capacity path as built:
`alloc_node` fallthrough to `evict_node`, victim selection by rotating
cursor plus `bid`, `is_prot` guard, `rec_evict` history record, and the
4096-edge cleanup. Trial reclamation composes with it as a pre-pass,
not a replacement:

- Ordering: trial-sweep runs before `evict_node` and only reclaims
  provably dead trial cells. `evict_node` semantics for live
  structures are untouched: same cursor, same `bid`, same `is_prot`,
  same edge cleanup. Any retention battery that passes today must pass
  byte-identically with reclamation enabled (kill bar K8).
- History: sweeps write a T_HIST record in the `rec_evict` style
  (cells freed, edges freed, trial id, tick), so the learner's
  retention policy observes reclamation events exactly as it observes
  evictions today. This is the evidence channel the reclaim-regret
  policy learns from.
- Promotion and fossil paths converge: promoted trials are owned by
  MAPs; fossil MAP atomic reclaim (`reclaim_map_atomic`) is extended
  to push its cells to the free list instead of merely zeroing field
  36. One free list, three suppliers (trial sweep, revision-draft
  sweep, fossil atomic reclaim), one consumer (`alloc_node`).
- The corruption class stays closed: teardown's fail-safe abort on
  PRO edges or live MAP-root references means the sweep can never
  create the zombie-MAP failure mode of `986c52fdc`.

### 2.6 The reclamation policy is learner-owned

New learner-state structure 3: the **reclaim-policy node** (tag 2),
referenced from new header field 60, carrying: sweep mode
(eager on rejection vs lazy on pressure), keep-generations K, and the
regret accumulator. Update rule, consequence-driven:

- Regret signal: the ledger records swept trials' graph signatures
  (`t2_sig` exists for this). If a later miss re-derives a trial with
  a matching signature that had been swept within the regret window,
  that is one unit of reclaim-regret: the sweep destroyed reusable
  structure.
- Update direction: regret increases K / shifts toward lazy; a
  pressure episode with zero regret decreases K / shifts toward eager.
  Magnitudes are learner state, initialized neutral, adapted from
  experience. No researcher-fixed threshold sits in the decision path
  of the promoted design.

For the FIRST experiment only (T-RECLAIM-1, section 4), a fixed
eager-sweep policy is used as a labeled test fixture to isolate the
mechanism (correctness, cost, no-regression) from policy learning.
The fixture is never promoted as a learner capability; the adaptive
policy is the defined follow-up experiment.

## 3. Architecture accounting

Counts are design estimates for the implementing wave to verify
exactly; the cap is part of the frozen proposal (K9).

- New cognition lines (researcher-authored mechanism code):
  `trial_begin` ~15, `trial_end` dispatch plus sweep ~60, free-list
  push/pop plus `alloc_node` integration ~15, ledger chunk
  append/walk/compact ~40, history record plus fail-safe asserts ~20.
  Total approximately 150 lines, cap 200. All of it is
  domain-neutral memory management (allocation provenance, free
  lists, teardown walks). Zero lines encode domain regularities,
  benchmarks, or task predicates.
- New hardcoded semantic cases: 0 (mandatory; verified by inspection
  of the implementing diff).
- New modes: 0. New bridges: 0. New handlers: 0. New task-specific
  gates: 0. (Mandatory; `trial_begin`/`trial_end` are substrate
  primitives in the class of `alloc_node`, not modes.)
- New edge types: 0. New node kinds: 0 (ledger and policy records
  reuse tag-2 GROUP nodes with field-packed layouts).
- New learner-state structures: 3. (1) trial ledger chain,
  (2) free-list head, (3) reclaim-policy node. New header fields: 52
  (free-list head), 56 (current trial id), 60 (reclaim-policy ref).
  Header slots 52/56/60 are currently unused (used: 0,4,8,12,16,20,
  24,28,32,36,40,44,48).
- Protected-core boundary: unchanged. DEALLOC-with-provenance is
  machinery in the allowed ISA class (ALLOC, READ, WRITE, LINK, COPY,
  generic state ops), the dual of the already-present ALLOC. It
  encodes no target-domain regularity detector and is not grown one
  benchmark at a time: it serves every speculative assembler.

## 4. One-system-rule argument

### Why the existing architecture cannot learn reclamation itself

The standing question is "why can the existing general architecture
not learn this behavior?" The answer is that learning is impossible
where the substrate withholds both the information and the primitive:

1. The information is absent. No cell records which trial assembled
   it, and no structure records a trial's cell set. A learner cannot
   learn a policy over the predicate "cells of trial T" when that
   predicate is not representable in state. Experience cannot create
   information the substrate never records.
2. The primitive is absent. The only deallocation path is the global
   `evict_node` scan; there is no O(1) cell-return for the learner to
   invoke, and no per-edge removal without a 4096-scan. A learner
   cannot learn to use a tool outside its ISA.
3. The teardown the substrate would need (per-trial edge removal by
   endpoint) is denied by the flat edge table: without recorded edge
   ids, each removal costs a full scan. The mechanism does not exist
   to be discovered.
4. The corruption analysis proves scanning is the wrong basis
   anyway: retention reasons over nodes and edges while references
   include fields, so any learned scan-based reclaimer reintroduces
   the zombie class. Only the assembler's by-construction provenance
   is complete, and only the substrate can provide it.

This is the permitted direction of the one-system rule: the
substrate supplies domain-neutral machinery (provenance recording,
O(1) return, teardown walk); the intelligence (when to sweep, what
to keep, learned from reclaim-regret) lives in learner-owned state
built from experience. No new subsystem, no mode, no bridge: one
workspace, one free list, one ledger the learner itself can read.

### Why this is an addition, not a repair

- It is domain-neutral. The mechanism serves every speculative
  assembler through one path (`trial_begin`/`trial_end`): miss-policy
  candidates, revision drafts, composition adaptation candidates,
  uncertainty guides. Nothing in the design names chains, sums,
  composition, FW worlds, or any benchmark.
- It composes with the existing eviction hook as a pre-pass and
  leaves `evict_node` semantics for live structures untouched.
- It addresses one shared architectural cause behind at least four
  distinct findings: the H-BASECERT-1 eviction latency cliff (~30M
  ops per at-capacity alloc), the mini-lifetime 100x cost growth
  under saturation, the zombie-MAP corruption class, and the blocked
  capacity plan ("until the reclamation frontier lands"). One
  mechanism, multiple worlds: the opposite of the patch treadmill.
- The kill bars (section 5) are structured so that a
  benchmark-specific repair cannot pass them: K7 requires two
  independent speculative assemblers through the same path, K8
  requires retention outcomes unchanged, K9 caps mechanism code.

## 5. Frozen proposal: experiment T-RECLAIM-1 (for a future wave)

Scope: implement sections 2.1-2.5 with the fixed eager-sweep fixture
policy (labeled fixture, not a learner capability). No adaptive
policy; that is the defined follow-up. Pure Zag, safebin toolchain,
zero randomness in decision paths, byte-identical reruns (3/3).

Harness: minimal `ev_query` over a ma_base-style substrate (ma_base
is not self-contained; the harness supplies the query path), plus a
white-box inventory verifier and a primitive-op counter.

Battery: (i) bulk teaching via direct `t2_trial` calls, 19 MAPs (the
redteam2 scaling path); (ii) contradiction-driven revision drafts;
(iii) the frozen regression battery.

Kill bars (frozen before implementation; never moved after):

- K1 (sweep exactness): the set of cells and edges freed by each
  teardown equals exactly the set allocated during that trial's
  assembly window. Verified by white-box inventory, 3/3
  byte-identical runs. Zero promoted-MAP, fact, policy, or ledger
  cells touched. Fail: any mismatch.
- K2 (no dangling references): post-sweep full-arena verifier finds
  no live node field and no live edge referencing a freed slot.
  (The verifier may scan; the mechanism must not.) Fail: any
  dangling reference.
- K3 (fail-safe): a trial whose cell is PROTECTED mid-trial (type-9
  PRO edge) aborts its sweep and falls through to the ordinary
  eviction path; a use-after-free probe (adversarial query
  referencing a swept trial's root) fails clean with no crash and
  no zombie read. Fail: sweep proceeds or probe crashes.
- K4 (cost bound): teardown primitive ops <= 40 x (trial cells +
  trial edges); `evict_node` global scans during the 19-MAP bulk
  teach drop by >= 10x versus the no-reclamation baseline. Fail:
  either bound missed.
- K5 (functional equivalence): frozen battery answers
  byte-identical with reclamation on vs off. Fail: any divergence.
- K6 (capacity): the 19-MAP bulk teach completes with arena
  occupancy < 1024 and bounded `evict_node` scans, where the
  baseline saturates the arena. Fail: saturation or scan count
  above the preregistered bound.
- K7 (generality, anti-treadmill): at least two independent
  speculative assemblers (`t2_trial` candidates AND revision
  drafts) reclaim through the same `trial_begin`/`trial_end`
  path; ledger writes are not per-mechanism code. Fail: second
  assembler cannot use the path unchanged.
- K8 (no intelligence trade): retention outcomes under pressure
  (which MAPs survive, in which order) are identical on vs off;
  the sweep never changes a live structure's fate. Fail: any
  divergence.
- K9 (accounting cap): implementing diff <= 200 new mechanism
  lines, 0 semantic cases, 0 modes/bridges/handlers, 0 new node
  kinds, 0 new edge types; header fields used are exactly
  52/56/60. Fail: any overrun.
- K10 (prereg order): prereg commit strictly precedes
  implementation commits (standard self-check). Fail:
  UNVERIFIABLE ORDERING, cannot be adopted.

Verdict rule: adopt the mechanism only on clean PASS of K1-K10 with
zero regressions; any FAIL is a kill or a transparent amend-and-
refreeze, never a moved bar. Independent red team required before
any SURVIVES claim; FW1-FW9 may be used as regression only.

## 6. Self red-team: how this could be a patch-treadmill item in disguise

1. Single-assembler coverage. If the ledger is written only by
   `t2_trial`'s assemblers, this is a `t2_trial` patch wearing
   substrate clothes. K7 exists to kill that version: revision
   drafts must ride the same path with no per-mechanism code.
2. Fixture creep. If the fixed eager-sweep fixture is later cited
   as "the learner's reclamation policy," a researcher constant has
   been laundered into a capability claim. The design labels the
   fixture as fixture; the adaptive policy is a separate
   preregistered experiment with its own kill bars.
3. Protection bypass. If teardown ever skips the PRO / live-root
   fail-safe for speed, the eviction-corruption class reopens in a
   new form. K3 probes exactly this, adversarially.
4. Registry leak. If generation records are never compacted, the
   leak moves from trial cells to ledger chunks. The design bounds
   the ledger (G generations, chunks die with trials); K9's
   inspection plus a soak run must confirm bounded ledger size.
5. Retention drift. If free-list-first allocation changes which
   live structures survive pressure (e.g., by deferring eviction
   past the point where `bid` would have chosen differently), that
   is an intelligence trade disguised as efficiency. K8 requires
   retention outcomes identical; any drift is a kill, not a tuning
   exercise.
6. Benchmark-shaped success. If the only workload that benefits is
   the composition miss path, the generality claim is hollow. The
   battery includes revision drafts and bulk teaching, and section
   4 requires the shared-cause argument across four independent
   findings.
7. The "learner could learn it" objection. If a future wave shows
   the learner achieving equivalent reclamation with existing
   primitives, this substrate addition was unnecessary and should
   be removed in favor of the learned solution. The design's
   section 4 argument is falsifiable and should be re-tested, not
   enshrined.

## 7. Open questions for the implementing wave

- Edge free-stack vs first-free scan: measure before adding.
- Optimal ledger chunk size (8 ids assumed; profile at 19-MAP scale).
- Whether `t2_exec` frames should be ledger-stamped or explicitly
  recorded (frames use fields 20/24/28/32 as registers, so stamping
  must avoid those fields; explicit recording is simpler).
- The adaptive reclaim-policy experiment (T-RECLAIM-2) prereg:
  regret-window definition, K adaptation rule, and its own kill
  bars, including a control where the fixture policy runs alongside.
- Interaction with the 5000-MAP scaling line: ledger and free-list
  overhead at 7000x scale must be measured, not assumed.

---
Design wave: wave-20261002-1121pdt, lane TNN3. No code changes.
Next: a future wave may preregister T-RECLAIM-1 per section 5.
