# Unified Composition Red-Team Report

**Target:** `composition_unified/un_patch.zag` (420 lines; prereg `06ea103bd`, results `83f8853b2`).
**Verdict:** COMPOSITION-UNIFIED-REDTEAM-COMPLETE
**Recommendation:** DO NOT ADOPT AS CANONICAL. 3 KILLs, 4 BOUNDs, 3 SURVIVEs.

## Toolchain guard (Step 0)

safebin PATH built from `which` for: git znc sh bash ls cp mv rm mkdir cat grep
sed awk wc cmp sha256sum git-receive-pack git-upload-pack. `which python3 python`
returns nothing. All research logic in pure Zag; shell only for znc/git/file ops.
No forbidden executable invoked. Pinned znc: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

**Target copy:** `rt_patch.zag` sha256
`3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2`
(verified byte-identical to `un_patch.zag` via cmp).

## Battery

10 attacks (R1-R8 + R4 split into a/b/c). Built `rt_full.zag` (base + target +
driver), `rt_full_i.zag` (instrumented: fallback-fire counter header 60,
co-use-hit counter header 52, FB-FIRE emit), `rt_full_c.zag` (C-original control).
3/3 byte-identical runs for the fast battery (sha256 below). Blowup probes timed
separately.

## R1: C Z-prime reuse (regression) -- SURVIVE

Reproduced C's Z' scenario: X(1)/Y(2) segments, Z=composed, Z' reuses MAP_Z as a
single segment. Result: Z ans=37 via [27,45], Z' ans=47 via [196], ZMAP id 196
identical to C's original run. No regression. The unified mechanism preserves
C's revision/reuse of composites.

## R2: B W-reuse via episodes (regression) -- SURVIVE

Reproduced B's W scenario with ev_cq chained episodes: Z ans=37, then W reuses
the composed Z MAP as one segment (ans=67 via [398]). Co-use accumulation from
episodes and composition both function. No regression.

## R3: A Suite-A necessity (regression) -- SURVIVE

A's original Suite-A case (the one case C could not do): ZA ans=306 via
[71,13]. The A plen-contract fallback carries it. No regression; the fallback
is live and functional on A's home turf.

## R4a: segment depth 6/7/8/9 -- SURVIVE (with decline-cost note)

1-link segments, k-link Z chain on rels 1..k. k=6,7,8: PASS with honest
k-segment decompositions (e.g. k=8: [15,23,31,39,47,55,63,71]), zero fallback
fires (pure C constraint walks). The 8-segment bound works as advertised.
k=9: declines (-2) as required by the L+1>=8 gate (9 segments impossible by
construction); the decline search itself takes minutes (permutation
explosion, see R4b). Bound correct, decline expensive.

Method note: an early 2-link-segment variant produced a parity artifact (odd k
fails) that was a test-design flaw, not a mechanism bug; the probe also
revealed the fallback silently misattributes segment provenance during training
(see R7).

## R4b: decline blowup, 3-wide depth-8 layered graph -- KILL

63 single-link MAPs, unreachable goal. **The unified mechanism did not
terminate in 15+ minutes (killed).** Root cause, measured:

* At one node, 12 MAPs admitted: 2 via C's relseq walk, **10 via A's
  plen-contract fallback** (plen-2 matches any 2-path; probe `rt_bin_s`).
  The fallback is relation-agnostic, so nearly every MAP is "applicable"
  nearly everywhere.
* Decline wall time, 2-wide worlds, unreachable goal:
  C-original: depth 2: 0.20s, depth 3: 0.18s (flat).
  Unified: depth 2: 0.81s, depth 3: **37.1s (46x per added depth)**.
* Extrapolated: the R4b world (branching ~32/node after the 32-candidate cap,
  depth 8) explores ~32^8 paths. Practically non-terminating.

C's 3-segment cap bounded this; the unified 8-segment bound multiplies an
already-inflated branching factor. The builder's T4/T5 decline bars used tiny
worlds and never probed decline at scale.

## R4c: success blowup, correct path last -- KILL

Same layered graph with a reachable goal at depth 8, correct-path MAPs trained
last (highest ids) so DFS explores wrong branches first. **Did not terminate
in 15+ minutes (killed).** Same root cause as R4b: fallback-inflated branching
before the deep success is found. A mechanism whose worst-case success time is
unbounded on 63 MAPs cannot be canonical.

## R5: segment plen coverage ceiling -- BOUND

Trial learns at most 4-link chains (verified L=1..6: L=4 ok, L=5,6 fail,
no MAP promoted). Therefore C's relseq cap (7 links) and A's p<=8 **never
bind**; the production ceiling is the trial's 4-link reach. R5a: 4-link M4 +
1-link Y compose to Z correctly (PASS). R5b: 5-link chain unlearnable, Z
declines cleanly (PASS-CEILING). The unified patch's raised bounds are inert
for honest MAPs; the only live wire is the fallback's relation-agnostic
matching (see R7).

## R6a: history poisoning, selection steering -- BOUND

A1 [1], B1 [2], B2 [2] (equal plen, so co-use ordering is decisive). Z needs
[A1, B1-or-B2]. Control selects [15,23] = [A1,B1] (id order). With one injected
false type-15 edge (B2->A1), selection flips to [15,31] = [A1,B2] (cohit=1).
Answer unchanged (103; verification gate holds), but **a single false history
edge deterministically steers which MAP is chosen**, and the choice is then
written back as new "history" (duplicate type-15 edges accumulate; link_edge
has no dedup). Selection integrity is not protected; only the final answer is.

## R6b: history poisoning, search cost -- BOUND

5 decoy MAPs with dead-end facts, poisoned with co-use edges to outrank the
honest MAP. Selection unchanged ([A1,B1]; DFS completeness + verification),
but fallback fires triple (sat 15 -> 45, cohit=5): 5 dead subtrees explored
first. Poison degrades efficiency ~3x here; scales with decoy count.

## R7: predicate conflict (C says NO, A says YES) -- KILL

M [1,1], N [7,7], P [8,8] (plen 3 each). Z: r7,r7 then r8,r8 path. C's relseq
correctly rejects M (no r1 fact from 101). A's plen-contract admits M (a real
3-path exists). Permissive OR admits M; DFS picks [M,N] (M lowest id, N via
relseq). **C-alone control picks [N,P] (correct).** Unified ans=105 is
numerically right, but the decomposition is misattributed and it writes
**false persistent state**: LINK14 MAP_Z -> M and type-15 N -> M ("N used
after M"), which never happened. The fallback conflates "relseq extraction
failed" with "walk failed": it should only engage when extraction fails
(dead licensing fact), not when the walk fails on live facts. Fix: gate the
fallback on cc_relseq == -1, not on cc_satisfy == 0.

This also fires during ordinary training (R4a probe): single-link training
queries compose 1-segment fallback composites, so every MAP carries false
LINK14 provenance to the earliest MAP.

## R8: bridge audit -- SURVIVE

`compose_try`: 1 definition, 1 call site (ev_query). 0 COMPOSE_MODE, 0 new edge
types (uses 6/8/14/15, all pre-existing), 0 new node tags, 0 task-specific
relation literals, 0 new modes/bridges/handlers. `un_satisfy` = fixed-priority
(C then A) pure predicate; `un_candidates` orders by (co-use, length, id);
`un_dfs` branches only on search state. The predicate interface is not a
router. The 0-bridge claim holds.

## Determinism

Fast battery 3/3 byte-identical: rt_run1/2/3.txt sha256
`3c193aa72d22587e79fe1ea66b9298e69fcf19946f566b4396f635e8d7418e8e`.
Instrumented run: rt_run_i1.txt. C-control: rt_runc1.txt.

## Files

* `rt_patch.zag` -- byte-identical target copy
* `rt_patch_instr.zag` -- instrumented variant (probes only)
* `rt_driver.zag`, `rt_driver_main.zag`, `rt_driver_i.zag`, `rt_driver_c.zag`,
  `rt_driver_b.zag`, `rt_driver_9.zag`, `rt_driver_s.zag`, `rt_driver_t.zag`,
  `rt_driver_p.zag`, `rt_driver_q.zag`, `rt_driver_v.zag` -- drivers/probes
* `rt_full*.zag`, `rt_bin*` -- builds and binaries
* `rt_run1/2/3.txt`, `rt_run_i1.txt`, `rt_runc1.txt`, `rt_run_b1.txt`,
  `rt_run_9.txt`, `rt_run_tc33.txt` -- outputs
* `NAMECHECK.md` -- guard + battery prereg

## Bottom line

The unified mechanism is a genuine compression (420 vs 789 lines, 0 bridges)
and preserves A/B/C regression behavior (R1/R2/R3). But the A fallback's
permissive OR is unsound as integrated: it misattributes decompositions and
writes false history (R7 KILL), inflates branching to non-termination on
modest worlds (R4b/R4c KILL), and its history channel is steerable by a single
false edge (R6a BOUND). The 8-segment bound and p<=8 caps are inert (R5 BOUND:
trial caps at 4 links). Adopt only after: (1) fallback gated on extraction
failure, not walk failure; (2) branching bounded (candidate cap that considers
relation relevance, or fallback plen match restricted to relseq-compatible
paths); (3) decline-at-scale kill bars.
