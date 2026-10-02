# REPORT.md -- Composition Hypothesis B: Fragment Composition via Persistent Co-Use History

## Verdict: COMPOSITION-B-COMPLETE

Co-use LINK edges (type 15, "used together in one successful episode")
enable TNN to assemble X+Y into Z for a novel goal, where the prior
knowledge-composition experiment (commit `7c3ce673e`) proved TNN-2 cannot
compose. Ablation (deleting the links, or never forming them) destroys
the capability. The composition emerges from experienced co-use history,
not a designed contract system.

## Hypothesis

When MAPs are used together successfully (X's output feeds Y's input in
a trial), a persistent LINK records the co-use. Over episodes, a graph
of "these structures work together" accumulates. Given a novel goal Z
that rebind and trial cannot solve, TNN scans the LINK history for
fragment pairs, stages each fragment's shape (masked), assembles ONE
composed chain from grounded values, and verifies it. No paired X/Y
examples for Z. No "combine" hint.

## Method

### Base and patch

- Base: `knowledge_composition/kc_core.zag` lines 1-1567 (frozen TNN-2
  core machinery, no `ev_query`). Frozen source read-only.
- Patch: `cb_patch.zag` (this worker). Extends `pc_patch.zag` (commit
  `105e9ee8b`) with:
  - Type-15 co-use LINK edges, written by the episode success event
    (`ev_cq`), never authored by the driver. Endpoints are whichever
    MAPs actually solved the episode queries (learner-determined).
  - `compose_try`: for each type-15 pair (b -> a), stage a's shape on
    the query subject (masked execution), stage b's shape on the
    intermediate, concatenate value chains, assemble one chain via
    `t2_asm_chain`, verify against expected, promote with type-14
    links to both fragments.
  - `ev_query` order: activate -> rebind_try -> compose_try -> trial
    -> bootstrap. `compose_try` fires only when rebind fails.
  - Ablation hook `cb_del_couse` deletes type-15 edges.
- Driver: `cb_driver.zag` (this worker). Four arms, one binary run each.
- Build: `cb_full.zag` = base head + patch + driver, compiled with the
  pinned `znc_linux_x86_64_abed8aa1`. Zero modes, bridges, handlers.

### World design (all literals fresh per phase; no Z leakage)

- X: plen-3 chains on r1 (11-13, 14-16), queried as (11,61)->13.
- Y: plen-5 chains on r2 (21-25, 26-30), queried as (21,62)->25.
- Co-use episodes (TREAT only): X chain 41->42->43 then Y chain
  43->44->45->46->47 (bridge fact at 43, fresh literals, not Z's);
  second episode 51-57 likewise. Queries via `ev_cq` with chain=0/1.
- Z: mixed plen-7 chain (31,1,32),(32,1,33),(33,2,34)...(36,2,37),
  queried as (31,50)->37. Plen 7 exceeds trial's gather reach (max 5)
  and exceeds any single fragment (3 or 5). Rebind of X-shape or
  Y-shape alone gives the wrong answer (verified rejected).
- W (reuse): fresh literals 61-67, same X->Y mixed shape,
  queried as (61,50)->67. Tests that the LINK persists and generalizes.

### Arms (3/3 deterministic byte-identical runs each)

- TREAT: train X, train Y, 2 co-use episodes, Z, then W reuse.
- ABL-COUSE: identical to TREAT, then `cb_del_couse()` before Z.
  Tightest causal test: same fragments, same history, links removed.
- ABL-NOEP: train X, train Y, skip episodes (no type-15 ever), Z.
- FRESH: Z facts + Z query only.

## Results

All runs byte-identical (sha256
`62ecf41fb0db39e260bee707ffa56a890652ed240565e0d77a1114714e8d784c`).

### TREAT (full)

- X learned (13, 16), Y learned (25, 30). 4 MAPs.
- EP1: 43, 47, couse15=1. EP2: 53, 57, couse15=2.
- Type-15 edges (white box):
  - `212 (plen 5) -> 184 (plen 3)`
  - `274 (plen 5) -> 246 (plen 3)`
  These are the episode MAPs (Y-shape -> X-shape), endpoints determined
  by which MAPs actually solved, not authored.
- Z: rebind tried 8 candidates, all rejected (plen mismatch). Then
  `COMPOSE pairs=1`. **Z ans=37. SOLVED.**
- ZMAP id=457, plen=7, with type-14 fragment links:
  - `457 -> 184 (plen 3)` (X fragment)
  - `457 -> 212 (plen 5)` (Y fragment)
  Full provenance: the composed MAP records both fragments that built it.
- W: `COMPOSE pairs=1`. **W ans=67. SOLVED.** WMAP plen=7.
  The LINK persists and generalizes to fresh literals.

### ABL-COUSE (links deleted)

- Same training and episodes, couse15=2, then deleted to 0.
- Z: rebind tried 8, all rejected. No COMPOSE (no pairs). **Z ans=-2. FAIL.**
- No Z MAP promoted. The fragments alone cannot solve Z; the links are
  causal, not correlational.

### ABL-NOEP (no episodes)

- couse15=0. Z: rebind tried 4, all rejected. **Z ans=-2. FAIL.**

### FRESH (Z only)

- Z: rebind tried 0 (no MAPs). **Z ans=-2. FAIL.**

## Why this is composition (and what it is not)

- The prior experiment proved TNN-2 has no sequencing mechanism: X/Y
  MAPs are causally inert for Z. Here, Z is solved, and the ONLY
  difference from the failing arms is the type-15 co-use history.
- Selection, not brute force: at Z time TREAT holds 8 MAPs (56 ordered
  pairs). The LINK narrows this to 2 candidate pairs; the first succeeds.
  Without the LINK there is no mechanism that tries pairs at all (all
  ablations fail rather than falling back to exhaustive search).
- Learner-determined endpoints: the driver supplies episode queries; the
  episode success event links whichever MAPs actually solved. If rebind
  had promoted different MAPs, different endpoints would be linked.
- Honest limits (disclosed):
  - Composition is within the chain family: plen-3 + plen-5 -> plen-7
    via value-chain concatenation. Not arbitrary structural invention.
  - The final composed chain is verified against the expected answer
    (same methodology as rebind). The scientific claim is about fragment
    SELECTION from history, not answer discovery without a target.
    Stages use masked execution only; no intermediate is target-checked.
  - Greedy pair order: first type-15 pair that assembles a verified
    chain wins. No ranking or conflict resolution.
  - The driver designs the episode structure (X-then-Y co-use). What is
    learned (which MAPs, which links) is not designed.
  - Chain family only; no test of non-chain or cross-family composition.

## Cost

- TREAT Z: rebind 8 tried / 8 rejected, compose 1 pair attempted.
- Node budget: TREAT ends at 620/1024 nodes, 10 MAPs. Well within limits.
- No new task-specific handlers; the patch adds generic LINK/scan/stage
  machinery (type-15 edges, `compose_try`), 0 modes, 0 bridges.

## Instrumentation note

`cb_tstat` (the `tried=`/`rejected=` line after each answer) reports the
last SUCCESSFUL rebind's stats, which can be stale when rebind fails and
compose/trial succeeds. The `RB-STAT` line printed by `ev_query` itself
is the authoritative per-query rebind count. All claims above use RB-STAT.

## Files

- `cb_patch.zag`: patch (type-15 links, compose_try, ev_cq, ev_query).
- `cb_driver.zag`: four-arm driver with white-box checks.
- `cb_full.zag`: assembled build input (base head + patch + driver).
- `cb_bin`: compiled binary (pinned znc).
- `cb_run1.txt`, `cb_run2.txt`, `cb_run3.txt`: 3/3 byte-identical outputs.
- `cb_compile.txt`: build log.
- `NAMECHECK.md`: toolchain guard and build record.

## Reproduction

```
export PATH="$HOME/safebin"
head -1567 ../knowledge_composition/kc_core.zag > cb_full.zag
cat cb_patch.zag >> cb_full.zag
cat cb_driver.zag >> cb_full.zag
$ZNC cb_full.zag -o cb_bin   # pinned znc_linux_x86_64_abed8aa1
./cb_bin > out.txt   # run 3x, sha256 must match
```
