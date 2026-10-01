# WHITEBOX INVENTORY: What TNN-2 Actually Built

**Verdict:** WHITEBOX-INVENTORY-COMPLETE
**Method:** Pure-Zag read-only inspector (`inspect_state.zag`) reading the frozen
TNN-2 workspace layout (110656 bytes) from evaluator-saved state bins.
No sealed world definitions opened. No modifications. Frozen `tnn2.zag`
(hash `a29972ca8183b285`) untouched; layout constants extracted by reading only.

**States inspected:**
- `fw_run1/fw1_state.bin`: learner state after FW1 only (clock 66)
- `fw_run1/fw2` through `fw8_state.bin`: per-world progression
- `fw_run1/state.bin`: cumulative post-FW9 state (clock 469)
- `w_run1/state.bin`: cumulative post-W9 state (clock 372)

---

## 1. FW cumulative state (post-FW9): the headline numbers

```
HEADER clock=469 live_nodes=1022 live_edges=596 log_count=128 (full)
NODECENSUS FACT=87 MAP=22 UNCERT=30 OP101=203 OP102=191 OP103=37 OP104=0
  CELL902=451 K903=1 GROUP=0 HIST=0 REGRET=0 COEFF=0 TAG0=0 DEAD=0
FACTCENSUS shadow=12 guides=9 superseded=2 taught_other=64
EDGECENSUS DEP=234 SUP=42 CON=2 USE=77 CFM=3 SUR=31 PRO=7 MEM=5 SEQ=171 COR=22
LOGCENSUS query=34 observe=94 (last 128 events; teaches aged out)
CELL902 referenced_literals=382 unreferenced_frames_or_garbage=69
```

The node budget (1024) is essentially exhausted: 1022 live, 0 dead.
The event log is saturated at 128 entries.

## 2. What the 22 MAPs are

**7 bootstrap MAPs** (root=0, s=0, r=0, ans=0, no provenance): memoized
invariants from the P-INV fallback path. They encode no procedure; they are
promoted constants with a MAP wrapper.

**15 trial-promoted MAPs**, by procedure shape:
- 11 chain graphs (guard/set links; 4 to 10 steps)
- 3 count graphs (guard/set/inc triples plus MOVE epilogue; 4 to 13 steps)
- 1 sum graph (pure INC run)
- 0 DEC-containing graphs (OP104=0 everywhere; the DEC opcode was never
  assembled into any promoted procedure)

**Most complex intact structure:** MAP 358, a 4-link count graph, 13 steps
(4 BEQ guards, 4 INC, 5 MOVE), 4 provenance DEP facts. It walks a 4-element
chain while counting, then moves the count to the output slot.

**Provenance:** every trial MAP carries DEP (type 1) edges to the licensing
facts (1 to 4 facts each), plus COR/SUP/USE self-edges from promotion.
Provenance is structurally present and intact even where graphs are not.

## 3. The corruption finding: FW1's procedures did not survive FW9

MAP 45 (FW1 3-link chain, 6 steps) and MAP 82 (FW1 3-link chain) were
verified intact in the fw1 through fw8 snapshots. In the cumulative post-FW9
state:

- MAP 45's root (node 34) is now a TAG902 literal cell. Its entire graph
  (nodes 34, 35, 38, 39, 42, 43) was evicted and the slots reused.
  The MAP node survives as a fossil claiming (s, r, ans) with 2 DEP facts
  but no executable structure. Executing it would fail at the first step.
- MAP 82's root (node 71) is now a MOVE cell inside MAP 74's count graph.
  Its root pointer was hijacked by slot reuse.

Timeline: intact through fw8 (DEAD=69 free slots, GROUP=1 policy root alive,
HIST=31 eviction records). During FW9 the budget filled completely
(DEAD=0), eviction churn destroyed the early graphs, and even the HIST
records themselves were evicted (HIST=0).

**In W cumulative:** 9 of 44 graph-MAPs (20 percent) have roots pointing at
TAG902 literal cells. Same mechanism, same outcome.

This is the white-box mechanism behind the transfer analysis: graph cells
carry no protection edges, so under memory pressure the procedures learned
early are destroyed while their MAP headers survive as dangling fossils.

## 4. Which MAPs were ever executed, which are fossils

Frozen TNN-2 has no query path that executes a stored MAP (activate matches
FACT nodes only; the shadow fact always wins). Execution events per MAP:

- **At promotion:** all 15 trial MAPs were executed once by t2_try_verify
  before promotion. The 7 bootstrap MAPs were never executed (no graph).
- **At revision:** MAPs 121 and 691 show revision markers (superseded DEP
  facts with CON self-edges); their graphs were re-executed during
  t2_revise_graph. No other MAP shows revision debris.
- **At query:** zero. Every MAP is query-inert in the frozen code.

Fossil classes in the cumulative state:
1. Dangling-root fossils (MAP 45, MAP 82, 9 W MAPs): graph destroyed,
   root points at unrelated live cells.
2. Intact-but-inert fossils (remaining 13 FW MAPs): graphs decodable and
   well-formed, but no code path will ever execute them at query time.
3. Bootstrap fossils (7 FW, 8 W): never had graphs at all.

## 5. Uncertainty and policy state

- **30 UNCERT nodes** persist, each marking a (subject, relation) miss that
  reached the inquiry path. They are disconnected: no edges link them to
  any policy or guide-selection logic beyond their creation.
- **9 guide facts** (field24=-999) exist, but the **POLICY_ROOT is gone**
  (GROUP=0). Its 5 MEM edges now emanate from node 338, a BEQ guard cell
  inside MAP 358's graph, a live but semantically unrelated node whose slot
  was reused after the policy root's eviction.
- **Result:** the inquiry subsystem's learned state (uncertainties plus
  guides plus policy root) did not survive the FW battery as a connected
  structure. The uncertainties are orphans; the guides are orphans; the
  policy root is dead.

For comparison, at fw7 the policy root was still alive (GROUP=1). It died
in the FW9 eviction churn with everything else.

## 6. The 69 unreferenced 902 cells

382 literal cells are referenced by guard/set cells. 69 are unreferenced:
trial frames allocated by t2_exec (one per candidate execution) that were
never freed, plus literals of rejected candidates. This is the unreclaimed
trial garbage predicted by the transfer analysis, now counted: 69 cells,
about 7 percent of the node budget, permanently occupied by debris.

## 7. Most surprising, most useless

**Most surprising:** the policy root's MEM edges surviving with a guard cell
as their source. The edge structure outlived the node it was meant to
describe, and now asserts a policy relationship between a BEQ opcode and
five guide facts. A white-box viewer trusting edge types alone would
misread this as intentional.

**Most useless:** the 7 bootstrap MAPs. They wrap a constant (ans=0) in the
full MAP ceremony (COR/SUP/USE self-edges, promo index) while encoding no
procedure, answering no question (s=0, r=0), and carrying no provenance.
They are pure promotion-path exhaust.

**Most complex:** MAP 358 (13-step count graph), described above. It is
intact, well-formed, and never executed at query time.

## 8. W cumulative state (post-W9) in brief

```
HEADER clock=372 live_nodes=1022 live_edges=695
NODECENSUS FACT=108 MAP=52 UNCERT=30 OP101=193 OP102=174 OP103=39
FACTCENSUS shadow=29 guides=8 superseded=0 taught_other=71
```

52 MAPs (8 bootstrap, 44 with roots; 9 dangling). Same structural story:
more MAPs promoted, same eviction destruction, same dead policy root
(MEM edges from node 293, a guard cell), 30 orphaned uncertainties,
zero superseded facts (no revision survived to the end).

## 9. Standing architectural metric for this report

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (read-only inspection)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (nothing built by this worker)
- SOURCE-ENUMERABLE FORMS: N/A
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0 observed in cumulative states (no MAP executed at query)
- REVISION EVENTS: 2 (MAPs 121, 691 show revision markers)
- COGNITION LINES: 0 (inspector is tooling, not cognition)
- MODES / BRIDGES / HANDLERS / SEMANTIC CASES: 0 / 0 / 0 / 0

## 10. What the learner actually built, in one paragraph

Across the FW battery TNN-2 built 22 MAPs (15 real procedures: 11 chains,
3 counters, 1 summer; 7 empty bootstrap wrappers), 87 facts, 30 uncertainty
markers, 9 inquiry guides, and 1 policy root. By the end of FW9, memory
pressure had destroyed the graphs of its 2 earliest procedures, evicted the
policy root, orphaned all 30 uncertainties and 9 guides, and left 69 cells
of unreclaimed trial garbage. What survives intact is provenance (DEP edges
from MAPs to licensing facts) and the shadow facts that answer queries.
The learner built real executable structures, then the architecture let
them rot: no protection, no reuse path, no survival.

No em dashes were used in this document.
