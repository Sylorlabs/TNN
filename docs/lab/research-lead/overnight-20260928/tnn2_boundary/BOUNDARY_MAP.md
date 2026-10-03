# TNN-2 Capability Boundary Map

Target: frozen `tnn2_bin` (commit `f4de7ff46`, source SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
1591 lines). Probed 2026-10-01 via compiled Zag probes against a
byte-identical copy of the frozen source. All probe outputs are
byte-identical across 3 runs (SHA-256 recorded in `probes/`).

Method: `probes/base.zag` is a byte-identical copy of the frozen source
(SHA-256 verified equal). Each `pN.zag` differs from base by ONLY the
`main` line, mechanically replaced (`probes/mkprobe.sh`). The frozen
`tnn2_build/` directory was never written. Fidelity probe p0 reproduces
the frozen 46-test suite exactly (`TOTAL 46/46`).

No em dashes are used in this document, per the loop style rule.

## Probe results

### p0 fidelity: PASS
`p0_bin` reproduces the frozen suite: `TOTAL 46/46`, exit 0.
The probe harness is faithful; all below results are the frozen
system's own behavior.

### pA depth ceiling: chains work to exactly 4 hops, then miss
Setup: linear fact chains of 2 to 6 hops on relation 11 from subject 11,
`ev_query(W,11,40,11+hops,0)`. Trial stats from header field 16.

| hops | ans | tried | rejected |
| 2 | 3 | 1 | 0 |
| 3 | 4 | 2 | 1 |
| 4 | 5 | 3 | 2 |
| 5 | -2 | 5 | 5 |
| 6 | -2 | 5 | 5 |

Reading: the trial tries every candidate path (shorter chains first,
then count, then single hop) and rejects each against the expected
value. At 5+ hops the BFS gather (depth cap 4, i.e. 5 nodes) cannot see
the full path, every candidate is rejected, and the query becomes a
miss (-2) which triggers the inquiry path. The depth ceiling is sharp:
4 hops is the maximum composable chain length. This is a hardcoded
constant in `t2_gather`/`t2_trial` (k=2..4), not a learned limit.

### pB sums: only with researcher-placed comb node, totals 1..900
Setup: subject 110, values taught on relations 31/32/33.

| input | comb node | ans |
| 10+20=30 | present (type 8) | 30 |
| 10+20=30 | absent | -2 |
| 400+400=800 | present | 800 |
| 500+450=950 | present | -2 |

Reading: the sum path (`t2_asm_sum`, unrolled INC cells) fires only when
a type-8 node exists in the world (`comb_present`). That node is placed
by test scaffolding (frozen source line 1106, `t_p2`), never by any
learner mechanism in the frozen binary. Without it the sum capability
is unreachable: the exact same facts and query return -2. Totals above
900 are declined (`t2_asm_sum` returns -1). So "TNN-2 can add" is true
only inside a researcher-scaffolded regime: comb marker present AND
total in 1..900 AND the expected value supplied post hoc for
verification. There is no subtraction (DEC cells are never emitted by
any assembler; pG G2 confirms ans=-2).

### pC masked first-guess: masked trial commits to the first path tried
Setup: diamond facts (1,11,2),(1,11,3),(2,11,10),(3,11,20).

| condition | expected | ans |
| masked=1, diamond | 99 | 10 |
| masked=0, diamond | 99 | -2 |
| masked=1, branch pick | 20 | 20 |

Reading: with masking on and an expected value that matches nothing
(99), the trial promotes the FIRST path tried (1->2->10), because the
mask is applied inside verification and the first candidate passes the
masked check before the expected comparison can reject it. Without
masking, expected=99 rejects both paths and the query misses (-2).
With expected=20 the 1->3->20 path verifies and promotes. The trial
order (longer chains first, gather order within a length) therefore
decides ties, and masking changes which candidates survive. There is no
genuine ambiguity resolution: the system cannot represent "two live
hypotheses" and never reports uncertainty between the branches.

### pD inquiry: guides accumulate without dedup and are never retracted
Setup: two misses on (9002,77), one miss on (9003,77).

- miss1=-2, miss2=-2, uncert(9002)=2, guides(9002)=2: the second miss on
  the same (s,r) creates a SECOND uncertainty node and a SECOND guide.
  No dedup.
- miss on (9003,77): guides(9003)=1.
- `ev_act` with ctx=9003 returns 30 (the guide's constant action).
- After `ev_teach(9002,77,42)`: query(9002,77) now returns 42 (the taught
  fact answers directly), but `ev_act` with ctx=9002 STILL returns 30,
  and guides(9002)=2, uncert(9002)=2 are unchanged.

Reading: the inquiry machinery (miss -> UNCERTAINTY node -> guide ->
POLICY_ROOT -> ev_act constant 30) fires correctly, but it has no
resolution path. Teaching the missing fact does not retract the
uncertainty nodes or the guides; the guide keeps firing 30 forever.
Inquiry is write-only: it records ignorance and acts on it, but never
notices when the ignorance is cured. The constant action 30 is
hardcoded, not learned.

### pE revision: one-shot terminal patch works; interior revision corrupts
Setup E1-E3: facts (101,11,102),(102,12,201); promote (102,40)->555 via
1-hop terminal chain; then contradict the terminal fact.

| step | observe | exec | query |
| E1 observe(102,12,999) | 0 | 999 | 999 |
| E2 observe(102,12,555) | 0 | 999 | 999 |
| E3 observe(102,12,201) | 0 | 999 | 999 |

Reading: E1 works as designed. The terminal SETREG is patched
(literal 555->999), the graph re-executes to 999, the old promoted
fact is contradicted, the new answer is taught. But E2 and E3 do
NOTHING to the graph (exec stays 999). Cause: E1's `ev_observe` taught
a NEW fact (102,12,999); the original fact keeps the graph provenance.
E2/E3's `activate` selects the newest non-superseded fact, which has no
provenance edges from any map, so `revise_on_contradict` finds no map
to revise. Revision follows the ORIGINAL fact's provenance exactly
once; after the first revision forks the fact lineage, later
contradictions on the same (s,r) never reach the graph. The graph is
frozen at the first revision. There is no revert, no second revision,
no convergence.

Setup E4-E5: fresh world, facts (101,11,102),(102,12,201); promote
2-hop chain (101,40)->201; then contradict the INTERIOR fact.

| step | observe | exec | query |
| E4 observe(101,11,777) | 0 | -999999 | 201 |
| E5 observe(101,40,777) | 0 | (n/a) | 777 |

Reading E4: the interior contradiction triggers `t2_revise_graph`,
which patches the interior SETREG, re-executes, and (correctly) gets
-999999 because the patched chain is broken (777 has no outgoing
relation-11 fact). It then runs the REVERT path. But the revert is
corrupt (see Surprise 1 below): the re-execution's frame allocator
(`t2_exec` -> `alloc_node`) reused the just-tombstoned stale node as
the execution frame, and `fr_set` overwrote its fields. The revert
restores only type and live-flag, leaving field 4 = 0, field 8 = 0,
field 20 = 777. The graph is permanently broken: `t2_exec` now
returns -999999 forever (the SETREG's slot field 0 < 1000 fails the
execute guard). Yet `ev_query` still returns the stale 201, because
queries hit the promoted FACT directly via `activate` and never
re-execute the graph. The system answers 201 with a broken
justification it cannot detect.

Reading E5: observing a contradiction on the PROMOTED fact itself
(101,40,201 -> 777) does not revise any graph (the map's provenance
points to the interior facts, not to the promoted fact). It teaches a
new fact (101,40,777) which wins `activate` by recency/higher bid, so
the query flips to 777. The old promoted fact is shadowed, not
retracted. The map still claims ans=201.

Standing (map_standing) is 1 before and after E1: the revision does
surgical graph patching and never touches standing. Standing only
tracks the DEP/CON edge balance, not correctness.

### pF composition: promotions compose via reified facts, no CALL
Setup: teach (1,11,2),(2,11,3); promote (1,40)->3 (MAP1). Then teach
(3,11,4),(4,11,5); promote (1,41)->5 (MAP2). MAP2's chain runs through
the promoted fact (1,40,3).

- MAP1: q=3, root=6, 4 cells (2x101 SETREG, 2x102 guard, 0x103, 0x104).
- MAP2: q=5, root=50, 6 cells (3x101, 3x102, 0x103, 0x104).
- roots distinct (6 vs 50). MAP2 has a type-1 provenance edge to the
  promoted fact (1,40,3): confirmed = 1.
- MAP1 re-executes to 3 after MAP2 exists: no interference.

Reading: composition works, but only by fact reification. MAP2's chain
treats the promoted fact (1,40,3) as an ordinary fact and builds a
fresh chain through it. There is no subroutine call, no graph-to-graph
edge, no shared substructure: the two graphs are disjoint (roots 6 and
50) and MAP2 redundantly re-derives what MAP1 already computed. The
only executed operation tags in any promoted graph are 101 (SETREG)
and 102 (guard/BRANCHEQ). Tags 103 (INC) and 104 (DEC) appear only in
sum graphs (103) or never (104). Composition depth is bounded by the
4-hop trial ceiling applied per promotion.

### pG novelty: no new schemas; count vs chain shadow each other
Setup: four generalization probes.

- G1 diamond-sum (1->2,3; 2->10; 3->20; expected 30): ans=-2. The sum
  path gathers values per subject but does not compose across the
  diamond branches; no diamond-sum schema exists.
- G2 subtraction (facts (7,11,3) i.e. 7-3=4 with comb node,
  expected 4): ans=-2. No DEC emission, no subtraction schema.
- G3 count (chain 1->10->20->30 on relation 11, expected 3): ans=3.
  The count path (unrolled graph with INC cells + MOVE epilogue) works.
- G4 same facts, expected 20: ans=20. The 2-hop chain 1->10->20
  verifies first (chains are tried before counts) and shadows the
  count reading.

Reading: the construction vocabulary is exactly three schemas from the
frozen source: linear guard/set chains (t2_asm_chain), unrolled-INC
sums (t2_asm_sum), link-counting graphs (t2_asm_count). No probe
elicited a fourth schema, a negated guard, a conditional branch on a
computed value, or any composition of schemas (e.g. sum-of-counts).
Which schema wins is decided by trial order, not by fit: G4 shows a
chain shadowing a count when both verify. The system does not invent
representations; it selects among three hardcoded assemblers.

### pH memory pressure: graceful miss at exhaustion, no crash
Setup: 1015 junk facts fill the 1022 usable node slots, then teach a
2-hop chain and try to promote it.

- live-after-fill=1015. Chain facts allocate at nodes 1017,1018.
- construction-under-pressure ans=-2: the promotion fails because the
  chain assembler cannot allocate its 8 cells + map node from the 5
  remaining slots. The trial skips the unbuildable candidate and the
  query misses cleanly.
- live-after=1022: partial allocations from the failed trial leak into
  the table, but nothing crashes and no existing fact is corrupted
  (the run completes and exits 0).

Reading: exhaustion degrades to miss (-2), the same signal as
"unknown". The system cannot distinguish "I have no knowledge" from
"I have no room to think". Allocation failure is silent: there is no
eviction pressure signal to the trial, no priority for the new
construction, no error. Note the node table is 1024 slots with no
growth; `evict_node` exists but the trial path does not invoke it.

### pI guide selection: bid-ordered, stable, reinforced
Setup: two guides (9002, 9003) both in context.

- Both guides start at bid 0. `ev_act` with both in context selects
  9002 (first found wins ties), returns 30.
- Acting again selects 9002 again: stable.
- After acting once with only 9003 in context, 9003's bid rises to 1
  (acting boosts the selected guide: directional bid).
- `ev_act` with both in context now selects 9003: higher bid wins.

Reading: guide selection is deterministic and bid-driven, with a
reinforcement loop (selected guides gain bid). But the action itself
(30) is constant and the bid only tracks selection history, not
outcome: there is no success/failure signal anywhere in the loop.
A guide that always fires 30 gains bid by being selected, which makes
it more likely to be selected. This is a rich-get-richer selection
over constant actions, not learning.

### pJ no-feedback: the trial is inert without post-hoc expected
Setup: 3-hop chain facts, query with expected=-2 (the MISS sentinel,
i.e. no feedback) vs expected=4 (control).

- expected=-2: ans=-2, maps=0, uncert=1. The trial ran (an uncertainty
  node was recorded) but promoted nothing.
- expected=4 (control): ans=4, maps=1.

Reading: `expected` is the only verification signal and it is
post-hoc: the researcher (or environment) supplies the right answer
after the trial, and the trial keeps the first candidate that matches.
With expected=-2 the trial cannot promote anything, by construction
(`t2_try_verify` compares against expected; -2 never matches a real
execution). The frozen TNN-2 has no intrinsic verification, no
self-consistency check, no way to prefer one candidate over another
except an externally supplied answer. This is the E-ruling made
behavioral: without feedback the miss policy only inquires.

## The competence edge, stated precisely

Inside the edge (reliably works):
1. Single-hop and multi-hop (2..4) chain lookup with post-hoc expected
   feedback, promoting a guard/SETREG executable graph and a reified
   answer fact.
2. One-shot terminal revision: contradicting the fact behind a
   promoted chain's FINAL step patches that step, re-executes, and
   teaches the corrected answer. Exactly once per fact lineage.
3. Composition by reification: a later promotion can chain through an
   earlier promotion's taught fact (provenance edge recorded).
4. Count queries over per-relation link chains (expected = link count).
5. Sums of gathered values when a researcher-placed type-8 comb node
   exists and the total is in 1..900.
6. Miss -> uncertainty -> guide -> constant-action (30) inquiry, with
   bid-ordered guide selection and selection reinforcement.
7. Graceful degradation: depth overflow, sum overflow, allocation
   failure, and no-feedback all produce miss (-2), never a crash.

On the edge (works once, then freezes or breaks):
8. Revision is one-shot per fact lineage. The second contradiction on
   the same (s,r) hits the newly taught fact, which has no graph
   provenance, so the graph is never revised again. No convergence,
   no revert-to-original, no multi-step correction.
9. Contradicting a promoted fact teaches a shadowing fact; the old
   answer is not retracted, the map keeps its stale claim.

Outside the edge (does not work):
10. Chains longer than 4 hops (hardcoded BFS/trial caps).
11. Any schema outside the three assemblers: no subtraction, no
    diamond-sum, no conditionals on computed values, no schema
    composition, no negated guards.
12. Sums without the researcher-placed comb node; sums over 900.
13. Any learning without post-hoc expected feedback (trial inert).
14. Inquiry resolution: guides and uncertainty nodes are never
    retracted when the missing fact is taught.
15. Branching ambiguity: masked trial commits to the first path tried;
    the system cannot hold two live hypotheses.
16. Genuine subroutine reuse: composition duplicates rather than calls.

## Surprises

Surprise 1 (pE E4): FAILED INTERIOR REVISION PERMANENTLY CORRUPTS THE
GRAPH. When `t2_revise_graph` patches an interior SETREG and
re-execution fails, the revert path is broken by a frame-allocation
alias: `t2_exec` allocates its execution frame via `alloc_node`, which
returns the just-tombstoned stale node (bid flag 0 = free), and
`fr_set` overwrites the stale node's fields (f4=0, f8=0, f20=frame
garbage). The revert restores only type and live-flag. The graph then
fails every future execution (-999999) while the promoted fact keeps
answering the stale value. White-box state and query answers diverge
silently. This is a bug in the frozen binary, verified by direct field
dumps before/after (`probes/pY`, `pZ` diagnostics).

Surprise 2 (pE E2/E3): revision does not converge and does not revert.
A second contradiction on the same (s,r) is a no-op on the graph
because fact lineage forked. The system cannot be talked back to the
original answer through the revision path; it can only be shadowed by
teaching (E5).

Surprise 3 (pD): inquiry has no resolution. Uncertainty nodes and
guides accumulate (no dedup: two misses = two guides) and persist
after the fact is taught. `ev_act` keeps firing the stale guide.

Surprise 4 (pB): the sum capability is scaffold-gated. Without the
researcher-placed type-8 node the identical facts/query return -2.
This is not a learner-discovered operation.

Surprise 5 (pI): guide "learning" is rich-get-richer selection over a
constant action. Bid tracks selection history with no outcome signal.

## What was not probed

- Interference between many promoted maps sharing facts (only 2-map
  composition tested).
- Whether `evict_node` ever triggers in the trial path under deeper
  pressure (pH stopped at 1022/1024 with no eviction observed).
- The ACT policy beyond constant-30 guides (no learned policies exist
  in the frozen binary to probe).
- Timing/performance boundaries (not a capability question).
- Sealed FW1-FW9 worlds (forbidden by task constraints; untouched).

## Verdict

BOUNDARY-MAP-COMPLETE. The frozen TNN-2 is a competent
feedback-gated chain/count/sum assembler with one-shot terminal
revision and write-only inquiry, bounded sharply by: 4-hop depth cap,
three hardcoded schemas, post-hoc expected feedback as the sole
verification signal, researcher-scaffolded sums, non-convergent and
non-atomic revision (failed interior revision corrupts the graph
while answers keep flowing from the stale fact), and inquiry
machinery that records ignorance permanently. Nothing in the probe
battery elicited a fourth schema, a learned action, a retracted
belief, or a second successful revision of one graph.
