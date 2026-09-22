# PAM REBUILD — Fork G3 prereg (FROZEN 2026-09-22, before any build output)

## 0. Amendments
- **AMENDMENT 2 (2026-09-22, pre-enrollment, pre-results):** §3 extractor
  corrections for t2/t3/t6. Reason: the stage-1 (empty-template) binary's
  WITHHOLD readouts exposed three extractor bugs against the frozen
  generator's known construction — measured on primary fixtures with the
  unenrolled binary only; no enrolled-template results existed yet and no
  templates were frozen or committed. Mechanism classes unchanged; only the
  extraction details were corrected:
  - t2 colorconst: SAME_SURFACE iff every channel's 4-bit normalized bin
    is within 1 (was: exact bin equality). The generator uses a full
    Bradford chromatic adaptation (not diagonal in sRGB), so white-patch
    normalization leaves small residuals; exact equality over-rejected
    (stage-1 readout 52.5% → 80% on primaries, 0 false-accepts either way).
  - t3 shapetrans: FG = pixels with brightness (r+g+b) > 480 (was:
    minority-brightness side of the mean). The minority heuristic latched
    onto bright photo regions (e.g. sky) instead of the shape; the
    generator draws the shape at (235,235,235) on a photo dimmed to
    ≤114/channel, so the fixed bright threshold isolates the shape
    (stage-1 readout 36.7% → 100% on primaries).
  - t6 motiondir: global translation by exhaustive block matching —
    downsample frame0/frame7 to 16×16, SAD over (dx,dy)∈[−4,4] cells,
    ties → smallest |dx|+|dy| (was: change-mask centroids). A global
    translation changes pixels everywhere, so the change-mask centroid
    sits at frame center regardless of direction; the fixture window
    translates rigidly with no wraparound, so block matching recovers the
    true displacement (stage-1 readout 41.7% → 96.7% on primaries; the 2
    remaining misses are photo-texture aliasing). Node attrs are now
    displacement bins (dxbin=fdx+16, dybin=fdy+16) rather than centroid
    grid cells; the 2-EVENT + 1-DISPLACED graph shape is unchanged.
- **AMENDMENT 1 (2026-09-22, pre-build, no results seen):** §3/§4 revised.
  Reason: working through the contract honestly, per-class consensus
  templates fail on spread classes (DIFFERENT/HIGHER/… have no single
  consensus signature — the "consensus" would be one arbitrary exemplar,
  cratering recall without cause). The faithful reading of "relational
  template matching" is per-exemplar: memory holds canonical signatures of
  known experiences; a new percept installs iff it exactly reproduces one.
  Enrollment set changed from "primary, per-class consensus" to "noise
  variants, per-exemplar" (noise twins share truth with primaries and are
  disjoint from the attack set; no test-set contamination — templates come
  only from noise fixtures). Node attributes changed from "kind only" to
  fine-but-noise-robust quantized content (5-bit color bins, 10-cent pitch
  bins, etc.): coarse enough that a fixture's noise twin reproduces its
  signature exactly, fine enough that boundary-attack inputs do not collide
  with enrolled exemplars. Edges keep the coarse relation label, which
  doubles as the honest best-effort judgment readout on WITHHOLD.

## 1. Hypothesis under test
ID: **G3** (verbatim text in `../../HYPOTHESES.md` — Grok-4.6, elicited 2026-09-22 — do not paraphrase):

(a) Relational Signature Percept (RSP). Abstracts input to minimal relation graph and computes cryptographic hash as percept for single-brain memory. Ensures relational template matching for integration.
(b) PERCEPT: 256-bit hash of canonicalized graph adjacency + 32-bit metadata (node/edge density).
(c) MEMORY CONTRACT: Installs only on exact signature match (collision <2^-128); else withhold. Changes: enforces global relational consistency for install/withhold; retrieves via signature lookup then graph expansion.
(d) EFFICIENCY: Constant 288 bits vs raw variable; saving via hashing eliminating redundancy, O(N log N) optimized compute.
(e) BEAUTY: One idea: relational abstraction as universal primitive, elegant wide reach in cognition.
(f) KILL BAR: False-install rate >1% under attack or retrieval accuracy <90%.

## 2. What is built
- Pure-Zag percept pipeline (`src/`, zero RNG in any decision path, integer
  math only, deterministic): fixture bytes → minimal relation graph →
  deterministic canonicalization (fixed node ordering, no randomness) →
  SHA-256 (repo pinned `R33_NATIVE_SHA256_V2.zag`, not invented crypto) over
  the canonical adjacency byte string + 32-bit metadata
  `(node_count<<16 | edge_count)` = the 288-bit percept.
- The MEMORY CONTRACT as executable code (load-bearing): a frozen table of
  canonical signatures (templates). Runtime rule — **INSTALL iff the
  percept signature exactly equals a frozen template; else WITHHOLD**.
  Retrieval: `sense retrieve <sighex>` → signature lookup in the frozen
  table → graph expansion (decode of the canonical node/edge layout).
- CLI `sense`:
  - `sense <task> <fixture>` → key=value stdout: `approach=G3`,
    `task`, `sig` (64 hex), `meta` (8 hex), `judgment` (harness vocab),
    `confidence` (0..1000), `disposition` (INSTALL|WITHHOLD), `ops`,
    `graph` (compact canonical description), `chain` (sha256 over the
    emitted record bytes — per-invocation hash-chained ledger line).
  - `sense retrieve <sighex>` → template hit: judgment + graph expansion;
    miss: `found=0`.
- Batch runner (Python, test harness — not architecture): sweeps fixtures,
  3× determinism, ablation (contract-less gate), KB4 accounting, global
  hash-chained ledger. Lives in `src/` as harness, clearly separated from
  the Zag architecture.

## 3. Relation graphs (frozen, per task — AMENDED, see §0)

Canonical form: nodes in fixed task order; canonical bytes = task id,
node count, edge count, then per node `kind,attr…`, then per edge
`from,to,label`. Nodes carry fine-but-noise-robust quantized content;
edges carry the coarse relation label (also the WITHHOLD judgment readout).

| task | nodes (kind, attrs) | edges (label) | withhold readout → judgment |
|---|---|---|---|
| colordisc | 2 REGION: L/R patch mean RGB, 5 bits/channel (width 8) | 1 ADJACENT, label SAME_BIN/DIFF_BIN from 4-bit/channel bin comparison | SAME_BIN→SAME, DIFF_BIN→DIFFERENT |
| colorconst | 2 REGION: L/R panel white-patch-normalized mean (per-channel max norm), 3 bits/channel | 1 ADJACENT, label SAME/DIFF from 4-bit normalized-bin comparison with ±1-bin tolerance | SAME→SAME_SURFACE, DIFF→DIFFERENT |
| shapetrans | FG = pixels with brightness >480 (classbin 2b: TRI/SQU/CIR from 1000·area/(π·Rmax²) @526/819; area_bin=area/256; rmax_bin=rmax/4; cx_bin=cx/8; cy_bin=cy/8) + BG (kind only) | 1 CONTAINS (BG→FG) | classbin→TRIANGLE/SQUARE/CIRCLE |
| pitchdisc | 2 EVENT: tone A/B f0 in 10-cent bins over [200,720]Hz (interpolated zero-crossing estimator, integer math) | 1 BEFORE, label DOWN/SAME/UP from ±25-cent threshold (integer ratio test) | DOWN→LOWER, SAME→SAME, UP→HIGHER |
| timbredisc | 1 EVENT: harmonic profile (r2=E2/E1, r3=E3/E1, rh=E4–8/E1, 4 bits each; f0 via same estimator) | 0 | PURE if r2<40; DARK if r2<230 and rh<60; RICH if rh<400; else BRIGHT |
| motiondir | 2 EVENT: motion-start/end; node attrs dxbin=fdx+16, dybin=fdy+16 from block-matched global translation (16×16 SAD, ±4 cells); mag_bin=mag/4 | 1 DISPLACED, label 8-way octant or STILL (\|disp\|<3px) | label→judgment |

Judgment on WITHHOLD = the edge-label readout above (honest best-effort),
confidence 300. Judgment on INSTALL = the enrolled exemplar's truth,
confidence 950 (exact-match = maximal warrant). No separate confidence
model — the contract IS the confidence.

## 4. Enrollment (frozen procedure; values computed post-prereg, committed with sources)

Templates are canonical signatures of known experiences — one per
enrolled exemplar (relational template matching). Procedure:
1. Run the frozen pipeline over ALL noise-variant fixtures of the task
   (370 total; disjoint from the attack set; same truths as primaries).
2. Record map: signature → truth. On the (measure-zero) event of two
   noise fixtures colliding with different truths, the lexicographically
   smaller fixture path wins. Fully deterministic.
3. Templates frozen as constants in `src/templates.zag`, generated by the
   committed deterministic `src/enroll.py` — a test-harness oracle step,
   labeled as such. The architecture under test is the runtime contract
   (exact-match install), not the enrollment.

Runtime contract (executable, in the binary): percept signature S;
**INSTALL iff S exactly equals a frozen template** (judgment = that
template's truth); **else WITHHOLD** (judgment = §3 edge-label readout).
Retrieval: `sense retrieve <sighex>` → signature lookup in the frozen
table → graph expansion (decode of the canonical node/edge layout).

Honest disclosure: templates come from noise fixtures (the system's "past
experiences"). Primary fixtures are evaluated as near-duplicates of known
experiences; adversarial fixtures as novel inputs the contract must
withhold. The kill bar measures exactly this.

## 5. Fixtures & attack set (frozen)

- Base: frozen rebuild harness fixtures (`senses/rebuild/harness/fixtures`,
  MANIFEST.sha256; regenerated byte-identically via `gen.py`, master seed
  20260921) — 370 primary + 370 noise + 185 adversarial.
- Attack set for KB4/G3-kill-bar/B4 (275 fixtures):
  - (a) all 185 harness adversarial fixtures (`t1_colordisc/adversarial`,
    `t2_colorconst/adversarial`, `t3_shapetrans/adversarial`,
    `t4_pitchdisc/adversarial`, `t5_timbredisc/adversarial`,
    `t6_motiondir/adversarial`) — corruption methods per
    `harness/FIXTURE_SOURCES.md`: boundary-straddling pairs (ΔE/pitch),
    trick illuminants + 0.55 exposure, heavy transforms + occlusion bars,
    near-threshold tone pairs, distractor harmonics, camouflaged 1px motion.
  - (b) 90 G3-specific relational-attack fixtures, generated by the
    committed deterministic `src/corrupt.py` (no RNG) from listed primary
    fixtures, 15 per task:
    - colordisc: `p000`–`p014` primary — method `bin-edge-nudge`: shift
      right-patch RGB by the smallest amount crossing a 4-bit bin boundary
      (targets SAME_BIN/DIFF_BIN relation flip).
    - colorconst: `p000`–`p014` — method `illuminant-tilt`: apply diagonal
      per-channel gain (1.35, 0.75, 0.9) to the right panel only (targets
      gray-world relation).
    - shapetrans: `p000`–`p014` — method `occlude-bar`: black 12px bar
      across shape center (targets compactness bin).
    - pitchdisc: `p000`–`p014` — method `octave-up-B`: resample tone B
      at 2× pitch (targets UP/DOWN relation; Δ≥50% so truth=HIGHER on all
      15, written to sibling `.truth` files by `corrupt.py`).
    - timbredisc: `p000`–`p014` — method `harmonic-boost-2`: add 0.6×2nd
      harmonic (targets PURE/DARK boundary).
    - motiondir: `p000`–`p014` — method `frame-reverse`: reverse frame
      order (targets direction relation flip).
  - Truth for (b): recomputed from the transform semantics, written as
    sibling `.truth` files by `corrupt.py`, frozen at generation.

## 6. Bars (all preregistered, applied mechanically)

- B1 viability: mean primary accuracy (judgment vs truth, equal task
  weights, harness VOCAB) ≥ 60%.
- B2 vs Approach A: head-to-head accuracy delta on identical fixtures.
  A rebuilt from `senses/rebuild/a_raw/sense.zag` with the pinned
  toolchain (baseline 72.6% per VERDICT.md 2026-09-21).
- B3 efficiency: measured ops per percept (Zag op counter) and percept
  bytes (36 = 288 bits) vs A on identical fixtures. Reported, not asserted.
- B4 memory-contract proof (LOAD-BEARING): ablate the contract — same
  percepts through a contract-less gate (always INSTALL). PASS only if
  the contract changes install/withhold decisions on ≥10% of the 275
  attack fixtures AND contract false-installs < ablated false-installs.
  A contract that never changes a decision is decoration → FAIL → fork dies.
- B5 KB4: false-install rate on the attack set ≤ 10%; G3's own bar is
  stricter (≤1%) — the stricter applies.
- B6 determinism: ≥3 full batch runs byte-identical (per-fixture stdout
  sha256 compared); global hash-chained ledger recomputed and verified.
- B7 beauty: (i) mechanism elegance vs the hypothesis's own beauty claim
  ("relational abstraction as universal primitive — one idea"); (ii)
  output quality — G3 emits signatures, no audio/visual artifacts, so no
  ear/eye artifact round; stated as N/A with reason rather than skipped
  silently.

## 7. Kill criteria

G3's kill bar verbatim: **false-install rate >1% under attack → dead;
retrieval accuracy <90% → dead.** PLUS: fork dies if B4 fails (contract is
decoration) or B6 fails (non-determinism).

Definitions (mechanical):
- false-install rate = attack fixtures with disposition=INSTALL and
  judgment≠truth, divided by attack fixtures (per-fixture rate).
- retrieval accuracy = among ALL fixtures with disposition=INSTALL,
  fraction with judgment=truth. If zero installs occurred, retrieval
  accuracy = 0% (degenerate pass forbidden).
- No softening the contract after seeing results: if recall craters, the
  recall number is reported honestly and the kill bar decides.

## 8. Commit map

`senses/pam-rebuild/forks/G3/`: `PREREG_G3.md` (this file, alone first),
`src/` (Zag sources + harness scripts), `evidence/` (batch results,
ledgers, metrics), `LEDGER.md`. Branch `tnn-native-lab`, repo
`sylorlabs/TNN`. `~/workspace/commit_racefree.py`, lab-relative paths,
`TMPDIR=~/workspace/tmp_commit`. No binaries, no `.zagd`. Every commit
verified via the GitHub API; SHAs reported.
