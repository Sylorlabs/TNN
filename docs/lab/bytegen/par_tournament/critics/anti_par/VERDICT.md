# CRITIC 3 (anti-PAR) — VERDICT: S-CONF overthrows A on IMAGE RASTER

**Date:** 2026-09-24. **Critic:** CRITIC 3 — anti-PAR cross-path red team.
**Preregistration:** `PREREG_CRITIC.md` (committed `28856c51` before any
experiment; all bars below are the preregistered B1–B8, no additions).

## VERDICT: BEAT

**S-CONF (confluent tile-state renderer) overthrows contender A on the
image-raster cell.** All 8 preregistered bars met: S-CONF's renders are
**byte-identical** to A's on the frozen fixture and on all 25 fault/order
variants (B1–B6 — a tie stronger than required), and S-CONF is **strictly
faster than A on honest child CPU by ~5× on two independent methods**
(B7: s/a = 0.25 bash-time, 0.21 wait4-µs; target was ≤0.60). Byte-identical
reruns throughout (B8). Per the preregistered overthrow condition
(§6-analog: all bars + strictly better on ≥1 axis + no regression +
byte-identical reruns), **the map changes**.

## 1. The design

S-CONF uses the tournament's own structural scaffolding for "stateful"
(contender B): **2×2 tiles; per-tile carried state, wiped between tiles.**
The state is a per-pixel **z-buffer + winner-index buffer**, zeroed at each
tile start, then **read and written in the render path** — each primitive is
stamped over `bbox ∩ tile`, a pixel updating iff
`(z > zbuf) || (z == zbuf && idx < idxbuf)`. The merge is a commutative
max-reduction: the render is a pure function of (plan) computed *through*
carried state, order-free by construction.

That the state is genuine (not a sham annotation) is proven by bar B3:
poisoning tile 0's z-buffer observably corrupts tile 0 (512 px go to bg) —
a stateless renderer has no such state to poison. The poison does not cross
the tile boundary (0 diffs outside tile 0): the state is real *and*
contained.

Pure Zag, zero RNG (fixed permutations only), pinned toolchain
`znc_linux_x86_64_abed8aa1`. Source `s_conf.zag` SHA-256
`e6e598ee3fc53e39a48e8e49a60e621223ef07769c8eb3b2550db91e12a4122e`
(kept in critic workdir; the committed record is this verdict + runlog +
prereg).

## 2. Numbers (all preregistered bars)

Fixture: tournament `fixtures/img_plan.txt`, SHA-256
`254fa6bb9371659354801d11d694b689378560eb46e6e412f3987ede27c2b9e8`.
Baseline: `src/imgraster.zag` rebuilt with the pinned toolchain; mode-a
render reproduces the recorded pre-clobber SHA `0820a18b9a71…` exactly
(full: `0820a18b9a71d673c23c29a0decb60b1010db166b8cbe3935d16587be868c1d6`).

| Bar | Result | Detail |
|---|---|---|
| B1 DET | PASS | S `seq` ×2 cmp-clean; S render SHA-256 **== A render SHA-256** (full 64 chars) |
| B2 PERM-analog | PASS | prim-reversed, prim-perm (j*5+3)%8, tile-order [2,0,3,1] — all cmp-clean vs S `seq` |
| B3 LEAK | PASS | poison tile-0 zbuf → **0 diffs outside tile 0** (512 inside — contained, and proves the state is real) |
| B4 CASCADE | PASS | `corruptK` all K 0..7: S **byte-identical** to A (all 8 full SHAs); K=7 exactly **168 px / 1 quadrant** = A's recorded numbers |
| B5 CASCADE+ (harder) | PASS | 16 new probes the tournament never ran: `corruptzK` (z→99, winner-set changes at overlaps) and `corruptgK` (width×2, geometry faults): S **byte-identical** to A on all 16; footprints contained, exactly A's (0–736 px, 1–3 quadrants; e.g. corruptz2 = 64 px where P2 newly wins the designed file-order/z-order overlap) |
| B6 COH | PASS | tournament's exact probe (180 bytes) → **0/180** = A's recorded number |
| B7 COST | **PASS — overthrow axis** | honest child CPU, min-of-3..5, interleaved: M1' bash-`time`: a 8.0 ms / s 2.0 ms (**s/a = 0.25**); M2 `wait4` µs: a 7.5 ms / s 1.6 ms (**s/a = 0.21**); wall-clock corroboration (LATENCY-1 style): a 73.4 ms / s 18.5 ms (**0.25**). Target s≤0.6a beaten decisively. RSS: a 11652 KB / s 11496 KB (same order, no blowup) |
| B8 RERUNS | PASS | full battery ×2: logs byte-identical; all SHAs stable |

No-regression rule: satisfied in the strongest form — on B1/B4/B5/B6, S
does not merely tie A's numbers, it produces A's exact bytes.

Bonus (not preregistered, informational): S child-CPU 1.4 ms vs nat
0.9 ms (1.6×) vs A 7.1 ms (7.9× nat). **S-CONF keeps A's quality
byte-for-byte at near-NATIVE cost.** A's cost was characterized as "the
architectural price of statelessness" — S-CONF shows the price is not
architectural.

## 3. What this proves (and what it doesn't)

**Proves:** on image raster, A's wins (order-freedom, z-correct coherence,
exact fault containment) do not require statelessness. They require
**confluence** — carried state whose merge is order-independent. B/C lost
not because they carry state but because their state merge is
non-confluent (B's plan-content-derived LUT re-seed smears a fault 9.1×
across the tile; C's servo gain smears further). S-CONF is structurally
stateful by the tournament's own definition of B (per-tile state, wiped
between tiles, read+written in the render path — and faultable, B3 proves
it), yet matches pure-PAR A byte-for-byte and beats it 5× on cost.

**Map change:** the cell "image raster → PAR: CONFIRMED, A wins outright"
should read "image raster → **confluence**: S-CONF (confluent carried
state) wins outright — byte-identical quality to pure-PAR A at ~1.6×
NATIVE cost. Statelessness is not the load-bearing property; confluent
state gets PAR's wins." If the map instead reclassifies S-CONF as "a PAR
implementation", then B's structurally identical scaffolding must be
re-examined under the same lens — either way, the map's
stateless-vs-stateful dichotomy on this cell was too coarse, and that is a
reasoning change.

**Doesn't prove:** anything about the other cells (generative video,
predictive video, dialogue — untouched, out of scope). Doesn't prove
confluent state always wins — only that on this cell it ties-or-beats pure
PAR. Doesn't claim S-CONF should ship anywhere (no adoption asked or
offered).

## 4. Harder adversarial tests (beyond the tournament)

The tournament's cascade was color-only, single prim (corrupt7). B5 ran 16
harder probes: z-corruption (changes *which prim wins* at overlaps — the
fault a pure color-flip can't produce) and geometry-corruption (coverage
changes spanning up to 3 quadrants / 736 px). S-CONF matched A byte-exactly
on all 16 — fault containment under winner-set and geometry faults is
exact, not just color-exact. B2 tested two order dimensions the tournament
never did (prim-stamp order, tile order). All passed.

## 5. Honesty notes

- `/usr/bin/time` does not exist on this VM, so the battery's M1 method
  (`/usr/bin/time -v`) was substituted with bash's `time` builtin
  (wait4-based child user+sys, independent of Python) — logged in RUNLOG.
- Python `os.times()` children fields quantize at 10 ms (both binaries <
  10 ms); the first M2 run was unresolvable (0.00 vs 0.00). Re-ran M2 with
  `os.wait4` rusage (µs resolution) — the matrix's other prescribed valid
  method. Both final methods agree (0.25 / 0.21).
- The tournament's LATENCY-1 wall-clock figures (a 55.6 ms) are not cited
  as evidence; my wall-clock corroboration (a 73.4 ms, s 18.5 ms, same
  0.25 ratio) is reported for continuity only.
- A was rebuilt from the tournament's own `src/imgraster.zag` (SHA-256
  `744ca9a8…`); no crew source was modified. S-CONF is a new file.

## 6. Boundaries kept

Did not modify TOURNAMENT_SYNTHESIS.md, MATRIX.md, any crew's evidence, or
parked items. Did not re-litigate predictive video or dialogue. Scratch
stayed in `~/workspace/par_critics/anti_par/` (never /tmp).
