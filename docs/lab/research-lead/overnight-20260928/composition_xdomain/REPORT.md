# REPORT.md -- Composition Cross-Domain: Navigation x Aggregation

## Verdict: COMPOSITION-XDOMAIN-COMPLETE (with domain-gap analysis)

**All three composition mechanisms (A, B, C) fail on cross-domain
composition. The failure is clean, deterministic (3/3 byte-identical per
mechanism), and diagnosed to the exact line where each mechanism's
domain assumption breaks. Cross-domain composition is a new hard problem:
every existing mechanism implements composition as navigation
concatenation; cross-domain needs function composition over typed values.**

## World design

Two structurally different domains, taught independently, never paired:

- **X (navigation)**: chain-following, r=81, plen-4 chains. Queries
  (s,91) -> endpoint. X MAPs are guard/set chains; output is a literal
  retrieved by walking facts.
- **Y (aggregation)**: count queries, r=82. Queries (s,92) -> link count.
  Y MAPs are count graphs: guard/set links PLUS INC cells (tag 103) and a
  MOV epilogue. Output is computed arithmetically (unrolled INCs), not
  retrieved. No output literal exists in the fact store.
- **Z (chain-then-count)**: facts (31,81,32),(32,81,33),(33,81,34) then
  (34,82,35),(35,82,36). Query (31,93) -> 2. Requires X-walk to 34, then
  Y-count of 34 = 2.

The handoff is value-level: X's output node (34) is Y's input subject.
Y's output (2) is a number, not a walkable node. 30-fact interference gap
between training and test. Fresh literals throughout; query rel 93 is new.

Arms per mechanism: TREAT (X+Y trained), ABL-X (r=91 MAPs deleted),
ABL-Y (r=92 MAPs deleted), FRESH (no X/Y). B TREAT additionally runs one
ev_cq co-use episode (chain query (41,91)->44, then count query (44,92)->2
on the chain's output) to give B's history mechanism its best chance.

SHA-256 (3/3 byte-identical runs each):
- A: `2c751f855e3fc2034fe1ea8991bfe62af18c147d939c3aaf878577af57356d78`
- B: `bb3a7f2b4fead621971e7c0dd927a8e92e1ad1110f429ee892ce1af7593a1c40`
- C: `0d84997ba2536d1801fc40368e0e58596417be45df994819da2f381250be7330`

## Results

### Competence (all mechanisms, TREAT): X and Y are each solidly learned

| Query | A | B | C | via |
|-------|---|---|---|-----|
| X1 (11,91)->14 | 14 | 14 | 14 | trial (2 tried, 1 rejected) |
| X2 (15,91)->18 | 18 | 18 | 18 | rebind (1 tried, 0 rejected) |
| Y1 (50,92)->3 | 3 | 3 | 3 | trial count template (3 tried, 2 rejected) |
| Y2 (60,92)->4 | 4 | 4 | 4 | trial count template (4 tried, 3 rejected) |

MAP census (identical across mechanisms, ids vary):
- 2 chain MAPs: r=91, plen/contract/relse q = 4 / 4 / [81,81,81]
- 2 count MAPs: r=92, plen = -1, contract = -1, relseq = [] (empty)

The count MAPs are real, competent, reusable-via-trial structures. Every
mechanism's admission filter renders them invisible (details below).

### Z: all mechanisms fail, all arms

| Arm | A Z | B Z | C Z |
|-----|-----|-----|-----|
| TREAT | -2 | -2 | -2 |
| ABL-X | -2 | -2 | -2 |
| ABL-Y | -2 | -2 | -2 |
| FRESH | -2 | -2 | -2 |

No Z MAP promoted in any arm (ZMAP id=-1 throughout). Trial alone cannot
solve Z in FRESH (chain gives 34, count gives 3, sum template is dead in
this base, bootstrap has no rel-93 facts), so the failure is
composition-specific, not a broken world.

## Per-mechanism diagnosis (white-box)

### A: fails at ADMISSION (cx_contract)

`cx_contract` derives plen via `rb_chain_plen`, which demands strict
guard(102)/set(101) alternation. The count graph's INC cell (tag 103)
breaks the alternation: contract = -1. The pair search requires
`p1>=2` and `p2>=2`, so Y MAPs never enter a pair. Census trace:

```
MAP id=141 r=92 s=50 ans=3 contract=-1 class=count
```

Z trace: rebind tried 2 rejected 2 (chain MAPs rebound to 34, not 2),
compose tried 0 pairs (silent), trial 3 rejected 3. Total 5/5.
Deeper: even if admitted, `cx_apply` builds candidates with
`t2_asm_chain` from a gathered fact path. A count has no fact path; A's
"contract applies to a gathered path" semantics are navigation-only.

### B: history generalizes, ASSEMBLY does not (pair filter)

This is the most informative result. The co-use HISTORY mechanism is
domain-general: the episode (chain query, then count query on its output)
wrote a genuine cross-domain type-15 edge, endpoints learner-determined:

```
EP1 ans=44 (rebind, 1 tried 0 rejected)
EP2 ans=2  (trial count, 2 tried 1 rejected)
couse15=1
  EDGE15 251 -> 228 pa=4 pb=-1
```

Edge 251 (countMAP) -> 228 (chainMAP): "used together, chain first".
But `compose_try` filters `pa>=2 && pb>=2`: pa=4, pb=-1 (count MAP has no
chain plen), pair skipped. `cb_stage` additionally requires plen 2..8.
No COMPOSE attempt; Z=-2. Deeper: even if admitted, B assembles via
`t2_asm_chain` on concatenated value chains. A count contributes no value
chain (its output 2 is not a node); chain concatenation cannot represent
"apply count graph to node 34". B localizes the domain gap exactly:
**history yes, assembly no.**

### C: fails at ADMISSION (cc_relseq), and deeper at SEARCH SEMANTICS

`cc_relseq` walks the graph demanding guard/set alternation with a
licensing DEP fact per SET cell. The INC cell returns -1: relseq = [].
`cc_candidates` requires `len>=1`, so count MAPs are never candidates.
Census trace:

```
MAP id=115 r=92 s=50 ans=3 relseq=[] class=count
```

Z trace: `COMP-FAIL` (DFS from 31: X MAP [81,81,81] walks to 34; from 34
no candidate continues; backtrack exhausts). Deeper: even a repaired
relse q would not save C. `cc_satisfy` walks relations via `t2_lu_first`
and the goal test is `nv==expected` on a walked value. A count's output
is never a walkable value. C conflates "MAP behavior" with "relation
walk"; its search semantics are navigation-only.

## The shared broken assumption

All three mechanisms define composition as **navigation concatenation**:

| Stage | A | B | C |
|-------|---|---|---|
| Admission | plen contract >= 2 | plen >= 2 both | relseq non-empty |
| Staging | gathered fact path | cb_stage (plen 2..8) | relation walk |
| Assembly | t2_asm_chain x2 + SEQ | t2_asm_chain on concat values | t2_asm_chain per segment + SEQ |

Every cell in this table assumes chain-structured fragments. The
admission filters are symptoms; the assembly (`t2_asm_chain` everywhere)
is the disease. Cross-domain composition needs:

1. **Typed I/O contracts**: node->node (navigation) vs node->number
   (aggregation). Plen/relse q describe path shape, not computation.
2. **Value-level handoff**: f(g(x)) where the intermediate is a value fed
   as input, not path concatenation. No current machinery feeds one
   graph's output as another graph's input subject.
3. **Heterogeneous execution**: verify a chain graph feeding a count
   graph, not just longer chains.

## Honest boundaries

1. Y (count) is graph-structured; audio/program domains are further out.
   But count IS structurally different: INC cells, MOV epilogue,
   arithmetically computed output, no output literal, invisible to all
   three admission filters. The navigation/aggregation divide is the
   minimal true domain gap, and all three mechanisms fail it.
2. Z's expected value (2) is the given goal constraint, same methodology
   as the A/B/C workers. The claim is about fragment selection and
   assembly, not answer discovery.
3. One cross-domain pair tested. The "new hard problem" claim rests on
   the shared architectural reason (navigation-concatenation), white-box
   evident in all three patches, not on sweeping the pair space.
4. B got a genuine co-use episode (its mechanism's best chance); A and C
   have no episode/history concept to feed, their filters are purely
   structural. Asymmetric help is disclosed, not hidden.
5. Positive within-domain composition for A/B/C is established by their
   own reports (all COMPLETE); this worker's ports use their patches
   verbatim (byte-identical inputs, assembly recipe in NAMECHECK.md).
   Training-phase signatures reproduce (X1 trial-promote, X2
   rebind-promote + LINK14), confirming port fidelity.

## Most promising substrate

B's type-15 history is the only piece that crossed the domain gap: the
edge formed correctly from a cross-domain episode with
learner-determined endpoints. A future cross-domain mechanism keeps B's
history and replaces chain-assembly with typed function composition
(value-level handoff, heterogeneous verification). A and C fail earlier,
at perception: they cannot even represent a non-chain MAP as composable.

## Standing metrics

- Cognition lines added: 0 (drivers only, ~150 lines each; patches and
  bases verbatim from prior workers).
- Modes / bridges / handlers / new semantic cases: 0 / 0 / 0 / 0.
- Researcher-owned: world design, drivers, ablation procedure, B episode
  queries, search biases inherited from A/B/C.
- Learner-owned: X/Y MAP graphs, type-15 edge endpoints, trial verifies.

## Deliverables

- `xd_driver_a.zag`, `xd_driver_b.zag`, `xd_driver_c.zag` (new)
- `xd_full_a/b/c.zag` (assembled inputs), `xd_bin_a/b/c` (pinned znc)
- `xd_run_a1/2/3.txt`, `xd_run_b1/2/3.txt`, `xd_run_c1/2/3.txt`
  (3/3 byte-identical; SHAs above)
- `xd_compile_a/b/c.txt`, `NAMECHECK.md`, `REPORT.md` (this file)

Assembly recipe (bases/patches referenced verbatim from sibling dirs):
- A: `cat ../composition_A/cx_core.zag ../composition_A/cx_patch.zag xd_driver_a.zag`
- B: `head -1567 ../knowledge_composition/kc_core.zag` + `../composition_B/cb_patch.zag` + `xd_driver_b.zag`
- C: `cat ../composition_C/cc_base.zag ../composition_C/cc_patch.zag xd_driver_c.zag`

Pure Zag. Safebin PATH. Zero em/en dashes (byte-verified). Paper
untouched. Frozen source read-only. Committed locally, nothing pushed.
