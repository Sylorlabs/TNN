# Structural Protection Experiment

Date: 2026-10-01. Builder: Structural Protection Builder (subagent).
Variant: unfrozen TNN-2 (interference variant + learner-owned protection).
Status: COMPLETE. 3/3 runs byte-identical
(SHA-256 4821ce25af69c54ce6359625c354cd6dc8b9e715ff2ad900da3f6ae8a659497c).

## Question

The interference experiment (3708fbd15) found the "how" dies before the
"what": at V=1000 the executable graph breaks (cells 18->8) while the
answer stays intact, and refresh preserves answers but does NOT slow
procedure decay. "The learner has no mechanism to mark graph cells worth
keeping." Can a learner-owned structural protection mechanism save the
executable graph under interference, using only existing architecture?

## Mechanism

When a MAP is referenced, its graph cells are marked structurally
important via PRO edges (type 9) from the MAP node. Reuses existing
machinery: `is_prot` skips PRO-held nodes during eviction (no policy
change), `decay` expires protection after hg(W,4)=12 events without
refresh.

Reference points (all production code, learner-owned):

1. `promote_graph`: birth protection when a MAP is created.
2. `ev_query` hit branch: re-protect on query hit via `protect_map_use`.
3. `ev_observe` hit branch: re-protect on observation hit.
4. `t2_revise_graph` success: re-protect after revision.

Walk: iterative DFS from MAP root (field 20) over ET_SEQ edges,
BRANCHEQ true/false targets (fields 12/16), and operand literals
(field 8 for MOVE/BRANCHEQ cells). Protects tags 101-104 (op cells)
and 902 (literals). Per cell: refresh the live MAP->cell PRO edge if
present, else add one with clock 12.

New functions: pro_edge_live, protect_one, protect_cells,
protect_map_use (~80 lines). Modified: promote_graph, ev_query,
ev_observe, t2_revise_graph (one call each).

### Architecture accounting

- New node types: 0. New edge types: 0 (ET_PRO=9 existing).
- New fields: 0. New modes: 0. New bridges: 0.
- New task-specific handlers: 0. New semantic cases: 0.
- Researcher-set per-cell decisions: 0. Protection follows the MAP's
  actual graph topology; only the pre-existing PRO clock (12) is used.

### Learner-owned criterion

Protection edges are written by production code in response to learner
events (promotion, query hit, revision). The researcher does not choose
which cells are protected; the MAP's own graph determines the set.
Protection expires after 12 events without continued use.

## Method

Treatment: protection variant, same battery as 3708fbd15
(V in {0,1000,1050,1100}, IX-1 no refresh, IX-2 refresh every 10).
Control: published interference battery (3 byte-identical runs).

## Results

### IX-1: no refresh (treatment vs control)

| V | cells T | cells C | reexec T | reexec C | requery T | requery C |
|---|---------|---------|----------|----------|-----------|-----------|
| 0 | 18 | 18 | 5 | 5 | 5 | 5 |
| 1000 | 8 | 8 | -999999 | -999999 | 5 | 5 |
| 1050 | 0 | 0 | -999997 | -999997 | -2 | -2 |
| 1100 | 0 | 0 | -999997 | -999997 | -2 | -2 |

Treatment == control exactly. Birth protection (12-event clock) expires
long before eviction pressure; cells decay at the baseline rate.

### IX-2: refresh every 10 events (treatment vs control)

| V | cells T | cells C | reexec T | reexec C | requery T | requery C |
|---|---------|---------|----------|----------|-----------|-----------|
| 0 | 18 | 18 | 5 | 5 | 5 | 5 |
| 1000 | 8 | 8 | 5 | -999999 | 5 | 5 |
| 1050 | 8 | 0 | 5 | -999997 | 5 | 5 |
| 1100 | 8 | 0 | 5 | -999997 | 5 | 5 |

The executable "how" is saved at every interference volume under
refresh. All 8 winner cells survive; re-execution returns the correct
answer 5 through V=1100. Shadow fact and chain facts survive as in
control; map_same_id=1 throughout.

## Analysis

### 1. SAVES-HOW under use

The protection mechanism does what the fixed policy could not: it ties
structural survival to use. Each refresh query re-marks the MAP's cells
before the 12-event PRO clock expires, so the winner graph is never an
eviction candidate while the knowledge stays in use. reexec=5 at V=1100
vs -999997 in control.

### 2. Falsification check passes

IX-1 treatment is byte-for-byte the control table. Protection without
use expires and saves nothing. The mechanism's presence alone changes
no outcome; only the use history does. This is the consequence-driven
signature: same volumes, different refresh history, different cell
survival.

### 3. Selective, not blanket

cells_alive=8, not 18. The 10 rejected-trial garbage cells are
unreachable from the MAP root, never receive PRO edges, and are
evicted at the baseline rate. Protection follows the promoted
structure, not all cells. Dead structures are still reclaimed.

### 4. Counterfactual

IX-1 vs IX-2 is the counterfactual: identical interference volumes,
different use histories, different structural outcomes, mediated by
the protection edges written on query hit. Behavior differs across
histories on the same probe; learner state (PRO edges) differs; a
production write path (protect_map_use) caused the difference.

## Cost

- Nodes: 0 new nodes. Edges: 16 PRO edges per protected MAP per
  ~12-event window (refreshed in place, not accumulated).
- Compute: protect_cells runs a DFS (~16 nodes) with a 4096-edge scan
  per cell per query hit. Battery runtime ~18 min/run vs ~14 min
  control (~30% overhead, dominated by the refresh-path walks).
- Code: ~80 new lines, 4 one-line call sites.

## Interference with dead-structure reclamation

None observed. Garbage cells die on schedule. MAP fossils still form.
Protection expires without use. The eviction policy is unchanged;
protection only exempts what the learner is actively using.

## Classification

Bounded L2. The researcher authored the policy (protect on MAP
reference); the learner's use history determines which structures are
protected and the MAP's own topology determines the cell set. No new
learner-internal criterion (uses the pre-existing PRO clock, unlike
the decline gate's researcher-set N=3).

## Standing architectural metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 1 (the protect-on-reference
  policy; no per-cell researcher choices)
- LEARNER-OWNED STRUCTURAL DECISIONS: protection edges written on use;
  protected cell set derived from learner-built graph topology
- SOURCE-ENUMERABLE FORMS: all existing (PRO edges, DFS over SEQ/guard
  links)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: reexec=5 at all IX-2 volumes (vs 0 in control at
  V>=1050)
- REVISION EVENTS: 0 in battery
- COGNITION LINES: ~80 added, 4 modified (one call each)
- MODES / BRIDGES / HANDLERS / SEMANTIC CASES: 0 / 0 / 0 / 0

## Verdict

PROTECTION-COMPLETE: SAVES-HOW.

Learner-owned structural protection via MAP->cell PRO edges saves the
executable graph under interference when the knowledge stays in use
(IX-2: 8/8 winner cells alive, reexec=5 at V=1100; control: 0 cells,
reexec dead). Without use it changes nothing (IX-1 == control),
confirming the effect is consequence-driven, not a policy change.
Selective: garbage cells still evicted. Zero new types, fields, modes,
bridges, or handlers. Cost is ~16 decaying edges per live MAP and ~30%
battery slowdown.
