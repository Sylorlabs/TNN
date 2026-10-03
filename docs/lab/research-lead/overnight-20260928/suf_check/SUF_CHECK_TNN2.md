# SUF Check: TNN-2's three mechanisms

Status: CHECK-COMPLETE. Read-only white-box application of the 4-step SUF
operational test (PROPERTY_DEFINITION.md, commit `64eec921f`) to frozen TNN-2
source (`tnn2.zag`, SHA-256 prefix `a29972ca8183b285`, hash re-verified before
reading). Nothing was executed; no worlds were run.

Result: **all three mechanisms SUF-FAIL.** The (b) list is empty in each case.

---

## Mechanism 1: Construction

Production path: `ev_query` miss (line 827) -> `mp_run` (668) -> `t2_trial`
(586) -> assemblers `t2_asm_chain` (363), `t2_asm_sum` (398), `t2_asm_count`
(379) -> `t2_try_verify` (497) -> `promote_graph` (533).

### Step 1: structural decisions

| # | Decision | Source location |
|---|----------|-----------------|
| C-1 | Phase order: chains k=2..4, then sums, then counts, then single hops | `t2_trial` lines 591-666 |
| C-2 | Chain depths attempted: k in {2,3,4}, longer first | line 592: `let k:i32=2; while(k<=4 ...)` |
| C-3 | BFS gather bound: depth 1..4 (`len<5`), 96-path cap | `t2_gather` lines ~442-473 |
| C-4 | Graph family: exactly 3 assemblers, each emitting one fixed topology (chain: guard+set per link; count: chain + inc + `MOVE r0 <- r1` epilogue; sum: unrolled INC cells) | lines 363-411 |
| C-5 | Sum budget: decline when total <= 0 or total > 900 | line ~401: `if(total<=0 \|\| total>900){return -1;}` |
| C-6 | Subset enumeration order: size descending, bitmask descending | lines ~616-641 |
| C-7 | Search termination: first candidate to verify stops the whole search | `if(v2!=-2){promote_graph(...); ans=v2;}` repeated at 604-608, 627-629, 643-645, 658-660 |
| C-8 | Verification criterion: unmasked accepts iff `expected!=-2 && v==expected`; masked accepts first candidate with clean execution | `t2_try_verify` lines 497-509 |
| C-9 | Promotion schema: tag-20 MAP with fixed fields plus shadow `ev_teach_in` | `promote_graph` lines 533-544 |
| C-10 | Literal slots filled from data vectors (facts, observed values) | assembler calls passing `v`, `f`, `vals` buffers |

### Step 2: classification

- C-1, C-2, C-3, C-4, C-5, C-6: **(a) source-enumerable.** Fixed orders, literals, and three fixed topologies. The DOF map records these as RESEARCHER (K1, K2, K7, H5, H6, H7).
- C-7: the DOF map classes this MIXED (K4: "space = finite candidate family; rule = first-to-verify under the fixed order"). Under SUF clarification (b), selecting within a source-fixed finite set is class **(a)**: the candidate family (at most 96 BFS paths at depths 2..4, at most 4095 nonempty subsets of at most 12 values, at most 16 relations, single hops) is enumerable from source alone. Learner history selects which candidate survives, but cannot go outside the family.
- C-8: **(a).** The acceptance rule is a source literal; the oracle supplies the acceptance value (`expected`). This is the H2 boundary: oracle-fed selection is not learner origination.
- C-9: **(a).** Fixed MAP schema; the shadow teach is a source-written call at line 541.
- C-10: the DOF map classes this MIXED (K5/H4: "slot fixed by researcher; value from data"). Under SUF clarification (b) this is **(a)**: filling indices and literals into fixed slots is parameter filling, explicitly excluded from "structural."

Two apparent learner knobs are not structural decisions at all: `dc`, `di`, and `masked` are driver flags, not learner state (DOF K13); the sum phase gate `comb_present` requires a type-8 node that the cognition path cannot create (DOF K6), so it is externally gated, not learner-originated. `mp_set` has no production caller (test-only).

### Step 3

The (b) list is **empty**. No structural decision in the construction production
path is resolved by learner history outside a source-enumerable set.

### Step 4: negative control

Enumeration E: {chain topologies for k=2..4 with the fixed guard+set wiring;
sum topologies = `total` unrolled INC cells for total in 1..900; count
topologies with the fixed chain+inc+MOVE-epilogue wiring; single-hop chains}.
Every graph produced in the freeze and GW worlds is an instance of one of
these with filled literals. E covers everything produced.

### Verdict: CONSTRUCTION SUF-FAIL

---

## Mechanism 2: Inquiry

Production path: `ev_query` miss (813) -> trial fails (827) -> `bootstrap_miss`
fails (830) -> `miss_inquire` (795) builds the guide -> consumed later by
`ev_act` (859).

### Step 1: structural decisions

| # | Decision | Source location |
|---|----------|-----------------|
| I-1 | Trigger: true miss only after exact hit, trial, and bootstrap all fail | `ev_query` lines 813-834 (DOF N1: fixed pipeline order) |
| I-2 | UNCERTAINTY node schema: tag 30, field4 = -4, fields (s, r, 2, 0) | `miss_inquire` lines 796-799 (DOF L1) |
| I-3 | Guide node schema: tag 1 (FACT), field4 = s, fields (30, -999, 0, 0) | lines 806-808 (DOF L3) |
| I-4 | Guide wiring: DEP edge guide -> uncertainty; MEM edge POLICY_ROOT -> guide | lines 809-810 (DOF L4) |
| I-5 | Emitted act value: winner's field20 = 30 | line 807 `write_node(W,g,30,-999,0,0)`; `ev_act` M5 returns `ng(W,best,20)` |
| I-6 | Guide selection in `ev_act`: argmax `bid` over context-matching candidates, tie = first in edge-id order | lines 859-900 (DOF M4: MIXED) |

### Step 2: classification

- I-1 through I-5: **(a) source-enumerable.** Fixed pipeline, fixed schemas, fixed constants (30, -999), fixed wiring.
- I-6: the DOF map classes this MIXED (M4: "space = context-matching 1-2 hop neighbors of POLICY_ROOT; rule fixed"). Under SUF clarification (b) this is **(a)**: every guide ever constructed shares the identical fixed schema (I-2 through I-4), so there is no structural variation for learner history to resolve. Choosing among structurally identical nodes is value selection, not a structural decision. The selection rule (argmax bid, fixed tie-break) is a source literal.

### Step 3

The (b) list is **empty**. No inquiry act, content, topology, or resolution
transition is history-dependent. There is no resolution transition at all:
nothing in the production path consumes the guide's answer to update an
uncertainty representation.

### Step 4: negative control

Enumeration E: {one 2-node schema: UNCERTAINTY(30, -4, (s,r,2,0)) + FACT guide
with fields (30, -999, 0, 0), DEP + MEM wiring, act value 30}. Every inquiry
act ever emitted by TNN-2 is the constant 30 (TNN-1's constant was 0; a
different constant is not contingency). E covers everything produced.

### Verdict: INQUIRY SUF-FAIL

---

## Mechanism 3: Revision

Production path: `ev_observe` contradiction (836) -> `revise_on_contradict`
(685) -> `t2_revise_graph` (706) -> tombstone via `contradict_map` (578).

### Step 1: structural decisions

| # | Decision | Source location |
|---|----------|-----------------|
| R-1 | Trigger: activated fact's stored value differs from observed value | `ev_observe` lines 838-857 (DOF O2) |
| R-2 | Repair topology: scan 4096 edges for a tag-101 (MOVE/SET) cell with a DEP edge to the contradicted fact; find the tag-102 (BRANCHEQ) cell whose field12 points at it; build a new SET cell holding the new literal; rewire guard -> new and new -> successor; tombstone the stale cell; re-execute; revert on failure | `t2_revise_graph` lines 706-752 (DOF P: 19 RESEARCHER) |
| R-3 | Target selection when several stale cells match: last-in-scan-order | lines 709-719; DOF summary: "deterministic artifact, not a choice" |
| R-4 | Scan bounds: edges 0..4096, nodes 2..1024 | source literals in the scan loops |
| R-5 | Applicability: only chain/count shapes carry DEP provenance edges; sum graphs carry none and are unrevisable by construction | DOF summary of `t2_revise_graph` shape assumption |
| R-6 | Post-repair: contradict the old promoted fact, teach the new answer, update MAP field28 | lines ~746-751 |

Learner/environment-supplied values: `old_o` / `new_o` literals (parameter
filling); which fact is contradicted (environment input, not a learner
structural decision).

### Step 2: classification

- R-1 through R-6: **(a) source-enumerable.** One fixed repair topology, fixed scan orders and bounds, fixed applicability, fixed post-repair sequence. The DOF map records the revision section as 19 RESEARCHER decisions with zero MIXED.
- R-3 deserves emphasis: when the repair target is ambiguous, the winner is last-in-scan-order, a deterministic artifact of the researcher's loop bounds, not a learner decision.

### Step 3

The (b) list is **empty**. The learner chooses no repair topology, no target
criterion, no re-admission policy. Tombstoned literals cannot re-enter the
graph (the GW8 one-shot finding: revision cannot revise an already-revised
graph or re-admit a tombstoned value).

### Step 4: negative control

Enumeration E: {replace-the-SET-step topology with the fixed scan/rewire/
revert sequence}. Every revision ever performed by TNN-2 is this schema with
filled literals. E covers everything produced.

### Verdict: REVISION SUF-FAIL

---

## Cross-cutting: the DOF map's 5 MIXED decisions under SUF

The DOF map (commit `d2af26581`) records 5 MIXED decisions total. Each maps to
SUF class (a), value selection within a source-fixed space under a
source-fixed rule:

1. C3 (`activate`): winner = argmax bid over matching facts; tie = lowest node id. Space fixed, rule fixed.
2. E4 (eviction): victim = argmin bid among non-protected live nodes. Space fixed, rule fixed.
3. K4 (trial): first candidate to verify under the fixed order. Finite family fixed, rule fixed.
4. K5 (trial literals): slots fixed by researcher; values copied from data. Parameter filling.
5. M4 (`ev_act`): winner = argmax bid; tie = first in edge order. Space = guides of one fixed schema; rule fixed.

None is a structural decision resolved by learner history outside a
source-enumerable set. This is consistent with SUF clarification (b) and with
the H3 probe's effect-domain finding: there is no production write path from
learner state to any structural decision (the ISA has no structural WRITE;
`mp_set` is test-only; `masked`/`dc`/`di` are driver flags).

## Summary

| Mechanism | (b) decisions | Source-only enumeration covers production | Verdict |
|-----------|---------------|-------------------------------------------|---------|
| Construction | 0 | yes: 3 fixed topologies, fixed orders, fixed bounds | SUF-FAIL |
| Inquiry | 0 | yes: one fixed 2-node schema, constant act 30 | SUF-FAIL |
| Revision | 0 | yes: one fixed replace-SET-step schema | SUF-FAIL |

This is the white-box confirmation of the zero-improvement analysis: the three
mechanisms operate at a causal level that does not intersect the cluster
bottlenecks, because in each case the required form lies outside the
source-enumerable set and nothing in the mechanism can go outside it. A
mechanism failing this screen cannot move any cluster, so for any future
candidate this screen should run before worlds are executed.
