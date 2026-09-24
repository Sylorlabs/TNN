# CRITIC 3 (anti-PAR) — PREREGISTRATION

**Critic:** CRITIC 3 — anti-PAR cross-path red team.
**Date:** 2026-09-24. **Cell under attack:** IMAGE RASTER (confirmed-PAR cell).
**Status:** PREREGISTERED — committed before any experiment. No binary built,
no render produced, no measurement taken before this commit.

## 1. The claim being attacked

Tournament synthesis §4: "Image raster → PAR: CONFIRMED. A wins outright
(order-free, z-correct coherence 0/180 vs nat 72/180; cascade exact 168 px
footprint, 1 quadrant). B/C lose (region state amplifies faults 9.1× inside
the tile, 1536 px; destroys repeated-primitive coherence 180/180)."

A's recorded numbers on this cell (MATRIX.md / TOURNAMENT_SYNTHESIS.md §4):
- IMG-PERM: 0 diffs (order-free)
- IMG-COH: 0/180 vs nat 72/180 (z-correct)
- IMG-CASCADE (corrupt7): exact 168 px footprint, 1 quadrant
- IMG-COST: LATENCY-1 wall clock a = 55.6 ms/render vs nat = 17.2 ms/render
  (3.2× slower than NATIVE — disclosed, never folded into the cell verdict)

## 2. The anti-PAR hypothesis

B/C did not lose because they carry state. They lost because their state
merge is **non-confluent**: B's per-tile LUT is re-derived from plan content
at the tile boundary, so a plan fault re-seeds the LUT and the blend
`(plan+lut)/2` smears it across the whole 1536-px tile (9.1× amplification);
C's servo gain smears it further. **Confluent carried state — state whose
merge is order-independent — should keep every one of A's wins.**

Contender **S-CONF** (stateful, confluent tile renderer):
- Same scaffolding as B (the tournament's own structural definition of
  "stateful"): 2×2 tiles; per-tile carried state, wiped between tiles.
- The state is a per-pixel **z-buffer + winner-index buffer**, zeroed at
  each tile start, then **read and written in the render path**: each
  primitive is stamped over its bbox ∩ tile; a pixel updates iff
  `(z > zbuf) || (z == zbuf && idx < idxbuf)`.
- The merge is a commutative max-reduction → the render is a pure function
  of (plan) computed through carried state. Order-free by construction.
- If S-CONF matches A's bytes exactly on every probe and beats A's cost,
  the map's "statelessness" requirement is refuted on this cell: the
  load-bearing property is **confluence, not statelessness**. Either the
  cell winner changes to S-CONF, or the map must explain why B's
  structurally identical scaffolding counts as "stateful" and S-CONF's
  does not (special pleading — itself a map-reasoning change).

S-CONF is pure Zag, zero RNG, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, fixed
permutations only.

## 3. Fixtures and baseline

- Fixture: the tournament's `fixtures/img_plan.txt` (frozen, reconstructed;
  SHA-256 recorded in RUNLOG before first build).
- Baseline: rebuild `src/imgraster.zag` with the pinned toolchain; verify
  mode-a render reproduces the recorded pre-clobber SHA prefix `0820a18b9a71`
  (fixture header). All S-vs-A comparisons are against this rebuilt binary
  on this fixture — no other crew's binary or evidence is modified.

## 4. Kill bars (all must be met; measurements, not arguments)

Let A = rebuilt tournament `imgraster` binary, S = S-CONF binary.

- **B1 DET:** S `seq` ×2 renders cmp-clean (byte-identical reruns); S `seq`
  render SHA-256 == A `seq` render SHA-256 (full 64 chars, not prefix).
- **B2 PERM-analog:** S renders with (i) prim-stamp order reversed,
  (ii) prim-stamp order fixed permutation [3,7,1,5,0,6,2,4],
  (iii) tile processing order [2,0,3,1] — all three cmp-clean vs S `seq`.
  (The battery's pixel-order PERM has no meaning for a stamp renderer;
  prim/tile order are the orders S could depend on. Preregistered analog.)
- **B3 LEAK:** S `leak` variant (poison tile-0 z-buffer to +inf before
  stamping tile 0) → 0 differing pixels OUTSIDE tile 0 vs S `seq`
  (tournament's LEAK methodology, applied to S's region state).
- **B4 CASCADE:** for every K in 0..7: S `corruptK` render byte-identical
  to A `corruptK` render (all 8, full SHA-256). K=7 must reproduce A's
  recorded numbers exactly: 168 px, 1 quadrant.
- **B5 CASCADE+ (harder than the tournament ran — color-only, single prim):**
  corrupted plan files (Python-generated from the frozen fixture, never
  hand-edited): `corruptzK` (prim K z → 99, changes the WINNER SET at
  overlaps) and `corruptgK` (prim K width ×2, geometry fault), K in 0..7.
  S render byte-identical to A render on each corrupted plan (16 files);
  footprint reported in px + quadrants; no amplification vs A on any.
- **B6 COH:** tournament's exact probe (block (10,8,10,6) vs (70,40,10,6),
  180 bytes) on the S render → 0/180, matching A's recorded 0/180.
- **B7 COST (the overthrow axis):** honest child CPU, two independent
  methods, min-of-3, interleaved (a,s,a,s,a,s) on this VM, fresh output
  path per run:
  - M1: `/usr/bin/time -v` → User+System seconds per child (the battery's
    own IMG-COST method; valid per the cost-honesty note).
  - M2: Python `os.times()` → `children_user + children_system` delta
    around `subprocess.run` (the matrix's prescribed valid method).
  - Bar: `s_min < a_min` strictly, on BOTH methods. Target effect size:
    `s ≤ 0.6 × a` (decisive, not noise). Reference (not cited as evidence):
    LATENCY-1 wall clock a = 55.6 ms, nat = 17.2 ms.
  - Per-child max RSS recorded for both (informational; bar: no S blowup
    vs A, i.e. same order of magnitude).
- **B8 RERUNS:** every artifact SHA-256 logged; every bar re-run ×2,
  cmp-clean. Zero RNG anywhere (fixed permutations, deterministic plans).

**No-regression rule:** on B1–B6, S must at least tie A's recorded numbers;
  B1/B4/B5 require the stronger condition (byte-identity with A), which
  entails the tie. B7 is the strictly-better axis. Any bar failure, or
  `s ≥ a` on COST under either method, = overthrow FAILED.

## 5. Verdict conditions

- **BEAT:** all of B1–B8 met → "S-CONF overthrows A on image raster:
  confluent carried state matches pure-PAR byte-for-byte on
  DET/PERM/LEAK/CASCADE/COH (B1–B6) and strictly beats it on honest COST
  (B7). The map cell changes: the load-bearing property is confluence,
  not statelessness; A's statelessness is not required for its wins."
- **FAILED-genuine:** any bar fails after genuine attempts (including a
  second implementation attempt if the first has a remediable defect) →
  document everything tried; confidence in the PAR map rises. Also a win.
- **PARTIAL:** bars split (e.g. COST wins but a quality bar misses) →
  reported with specifics; no map change claimed.

## 6. Map-reasoning note (argument, not evidence; recorded for the parent)

The matrix's own §6-analog verdict rule requires "no regression elsewhere"
for a WIN, yet A's image-raster WIN was granted despite a measured 3.2×
COST regression vs NATIVE (LATENCY-1: 55.6 ms vs 17.2 ms, wall clock).
Either COST is not an applicable axis for the image cell (then B7's
overthrow axis needs re-grounding — noted, not assumed), or the WIN label
violates the matrix's own rule. This preregistration takes the rule at its
word: COST is applicable (the battery defines IMG-COST), and beating A on
it with no quality regression overthrows A on the cell.

## 7. Boundaries

- Will not modify TOURNAMENT_SYNTHESIS.md, MATRIX.md, any crew's evidence,
  or parked items awaiting Micah's word.
- Will not re-litigate predictive-video or dialogue (map says STATE wins;
  out of scope for this critic).
- Scratch: `~/workspace/par_critics/anti_par/` (never /tmp).
- Deliverables: this prereg (now), then VERDICT.md + RUNLOG.md in
  `docs/lab/bytegen/par_tournament/critics/anti_par/`, committed to
  tnn-native-lab.
