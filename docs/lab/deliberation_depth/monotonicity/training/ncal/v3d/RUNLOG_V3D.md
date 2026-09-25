# RUNLOG — NEC v3d: m20 vs Design S HEAD-TO-HEAD (SPEED / COST / CATCHES)

- **Date:** 2026-09-25 (PDT). **Authority:**
  `PREREG_NCAL_V3D_H2H_FROZEN.md` (frozen & committed `695997f5`
  BEFORE any measurement; local SHA-256
  `55cbc037c31a3ed706367b828912e5c062ba1fbe36ffb9b8b9afdce470b42c1f`).
- **Parents:** `PREREG_NCAL_V3B_FROZEN.md`, `PREREG_NCAL_V3C_B13FIX_FROZEN.md`,
  `job3/VERDICT_V3C.md`, `job1/VERDICT_JOB1.md`, `job2/VERDICT_V3B_JOB2.md`.

## 0. Pins

| item | value |
|---|---|
| comparison prereg | committed `695997f5e3df5979a10a0aa8137a1428483828e8` (parent `84ed45077a55`) |
| comparison binary | built from frozen `job3/src/` (nec_v3c.zag `c3fed78f…`, schema_kc.zag `b6aa3327…`), SHA-256 `7f6e0ceab59ad8a65d7a3a1500021b52934f3f41f81d34588284307e5745071f` (213,837 B) |
| pinned znc | SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` (matches record) |
| m20 contender | variant 20 of the comparison binary (adopted state, no FIX1) |
| S contender | variant 26 of the comparison binary (crew-adopted state, no FIX1) |
| machine | 2 cores, AMD EPYC 9D64 88-Core, 7 GB RAM — **SHARED lab VM** (see §1 caveat) |

**Correction to the task brief (recorded in prereg §0):**
`~/workspace/scratch_bt/m20.zag` is a DLB scratch stub, not the NEC m20
mechanism. The real m20 is driver variant 20 (v2d/v3c), pipeline-verified
below.

## 1. §0 gate — variant 20 reproduces adopted m20 legs (PASS)

| scale | adopted m20 SHA (job2 RUNLOG) | comparison-binary v20 | match |
|---|---|---|---|
| s1 | `84ffaf89…a36b81` | `84ffaf89…a36b81` | YES |
| s10 | `20ff1d10…926a` | `20ff1d10…926a` | YES |
| s100 | `f6a38269…680ff1` | `f6a38269…680ff1` | YES |

All A/B/C byte-identical. The head-to-head runs in ONE binary: identical
harness, identical I/O paths — the ONLY code-path difference between the
contenders is the tp=0 branch (constant `d1prior` vs `kc_lookup` + same latch).

**Shared-machine caveat (material to §2):** this VM is shared with other lab
crews. Load averaged 5–14 on 2 cores during measurement (other crews'
`python3` workers and a `./build/w13c_lease` binary). Wall-clock numbers are
therefore reported as full triplicates + medians, with an interleaved
validation leg; the deterministic S2 bound carries the mechanistic weight.

## 2. SPEED

### S1 — wall-clock per item (ns), 3 timed A/B/C runs per leg, sequential

(TABLE FILLED IN §2.4 BELOW — see summary.)

### S2 — deliberation steps per item (deterministic)

- v20: **1 step** — the tp=0 new-item branch executes `cl_mil=d1prior`
  (`nec_v3c.zag:117` declares `d1prior=950000`; `:265`/`:337` assign it).
  No lookup, no walk, no branch on content.
- v26: backoff levels consulted at tp=0, from the scored-run trace
  (`s2_v26_s1_trace.tsv`, output byte-identical to the scored s1 leg):
  **L1: 1000/1000 items (100%), L2/L3/L4: 0** on the s1 matrix. Observed max
  on unseen points: L3 (trap_t3, `L0 T3C0-000 75 875 1 3 1000 802000`).
  Theoretical max: 4 levels (L4 global fallback). Each level is one
  compiled if-chain walk (L1 ≤312 branches, L2 ≤246, L3 =7, L4 constant).

### S3 — tail

The planned chunked per-item tail experiment was ABANDONED for cause:
process-startup overhead (median 401 ms, range 171–682 ms over 10
empty-input runs) swamped per-chunk compute (25–200 ms for 105-row
chunks), producing negative per-item times after subtraction — the
instrument, not the mechanism, dominated. Reported instead:
(a) the deterministic worst-case bound from S2 (≤4 lookup levels ≈
hundreds of integer comparisons ≈ single-digit µs — no pathological tail
by construction); (b) run-level triplicate spread in S1 (machine noise,
shared VM). Both contenders' tails are machine-noise-dominated; neither
shows a mechanism tail.

### S1 results — sequential triplicates (median of 3)

| leg | v20 samples (s) | v20 median/item (µs) | v26 samples (s) | v26 median/item (µs) | median ratio v26/v20 |
|---|---|---|---|---|---|
| s1 | 0.34, 0.22, 0.18 | 219.6 | 0.25, 0.21, 0.31 | 245.7 | 1.119 |
| s10 | 1.60, 1.54, 1.61 | 159.6 | 1.91, 2.12, 1.51 | 190.6 | 1.194 |
| s100 | 16.51, 19.48, 81.54 | 194.8 | 80.49, 80.65, 96.32 | 806.5 | 4.140 |

Raw samples: `work/speed/*_ns.txt`. All six legs byte-identical A/B/C;
v20 legs reproduce the adopted m20 SHAs (§0 gate).

### S1 validation — interleaved alternating pairs (drift-cancelling), s10

| pair | v20 (s) | v26 (s) |
|---|---|---|
| 1 | 12.61 | 10.53 |
| 2 | 10.21 | 9.66 |
| 3 | 11.21 | 8.59 |
| 4 | 12.63 | 14.31 |
| 5 | 14.54 | 8.61 |
| median | 12.61 | 9.66 | **median ratio v26/v20 = 0.766** |

Interleave outputs byte-identical to the scored s10 legs.

### S1 reading (honest)

The sequential medians say v26 is 12–19% slower at s1/s10; the
drift-cancelling interleaved medians say v26 is 23% FASTER. Both
measurements are on the same shared 2-core VM (load 5–14) and they
contradict each other — **the differences are machine noise, not
mechanism**. The s100 sequential set is unusable for comparison (v20's own
third sample spiked 4.2× to 81.5 s; all three v26 samples sat on a
contention plateau). Mechanistic bound (S2): v26's extra work vs v20 is
≤312 integer comparisons on the FIRST observation of an item only, against
a ~30 µs/row baseline — under 1%, unresolvable. **SPEED: TIE within
measurement noise; no evidence of a speed cost for the schema.**

### S3 repair note

Chunked per-item tail measurement was ABANDONED: startup overhead
(median 401 ms, spread 171–682 ms) dominated chunk compute, yielding
negative per-item times. Replaced by the deterministic worst-case bound
(≤4 backoff levels ≈ hundreds of integer comparisons ≈ single-digit µs).
No mechanism tail exists for either contender; observed tail is machine
noise on both sides.

## 3. COST

### C1 — ledger bytes per item: 88 B/item, BOTH variants (white-box)

`nec_v3c.zag:153-160`: `slots` 64 + `confs` 8 + `pcp` 8 + `ptp` 8 = **88
B/item**. Same arrays, same code path for variants 20/26 — the schema is
shared (not per-item). Shared extras: `htab` = htsize×8
(htsize = next pow2 ≥ 2×max_items), class ledger 560 B (allocated, never
touched at nopool=1).

### C2 — schema memory footprint

- m20: **0 B** — no schema; d1prior is a compiled constant.
- S: frozen K-C schema — `schema_kc.zag` 38,271 B source; 312 L1 + 246 L2
  + 7 L3 branch-cells + L4 global; data-table equivalent **20,520 B**
  (312×40 + 246×32 + 7×24). Embedded as compiled if-chain code, not a
  data table.
- Runtime residency (RSS max, `resource.ru_maxrss`, 2× per leg, KB):

| scale | v20 | v26 | Δ (v26−v20) |
|---|---|---|---|
| s1 | 11536 / 11400 | 11664 / 11524 | **+126 KB** |
| s10 | 17740 / 17672 | 17716 / 17732 | +18 KB |
| s100 | 73972 / 73916 | 73804 / 73920 | −82 KB (noise) |

The schema's marginal resident cost is ~+126 KB at s1 (faulted-in
lookup code pages — v20 never calls them), washing out at scale against
the input buffer. Static data-equivalent: 20,520 B.

### C3 — output/audit bytes per item (measured on scored outputs)

| scale | v20 bytes | v26 bytes | v20 B/row | v26 B/row |
|---|---|---|---|---|
| s1 | 172,991 | 176,600 | 33.01 | 33.70 |
| s10 | 2,096,710 | 2,132,800 | 40.01 | 40.70 |
| s100 | 22,015,100 | 22,376,000 | 42.01 | 42.70 |

v26 output is +1.6–2.0% larger: its confs print as 7-char `1000000`
vs m20's 6-char `950000` (audit formatting, not mechanism). Per-item
deltas: +0.69 B/row (s1), +0.69 B/row (s10), +0.69 B/row (s100) —
constant, as expected from the format difference.

### C4 — deliberation depth distribution (input property, s1)

depths 1/2/4/8/16: 1000 items each; 32/64: 120 items each. Mechanism
per-observation op count is depth-invariant by source inspection (depth is
a lookup key, not a loop bound) — no per-depth timing leg was run, per
prereg §3/C4.

### C5 — projection to 1M items × 100 observations (100M rows)

From s10 sequential medians (cleanest leg: s1 has startup-share, s100v26
is contention-polluted):

| | v20 | v26 |
|---|---|---|
| wall | 3,046 s = **0.85 h** | 3,637 s = **1.01 h** |
| ledger | **0.088 GB** (1M × 88 B) | **0.088 GB** |
| output | **4.00 GB** (40.01 B/row) | **4.07 GB** (40.70 B/row) |

**Reading:** the +19% wall gap is INSIDE the noise band — the
drift-cancelling interleaved medians give v26/v20 = 0.77 (v26 faster).
The two methods bracket 1.0: **no measurable wall difference**; the
projection walls are effectively equal within noise. Ledger identical.
Output +1.7% for v26 (conf formatting). Schema is a FIXED cost
(20,520 B data-equiv, ~126 KB resident), not per-item — it does not grow
with scale.

Assumptions: linear extrapolation from s10 medians; arena allocator
constant; single-threaded; no page-cache/GC effects.

## 4. CATCHES

46 battery-legs × A/B/C = 138 runs, all byte-identical
(`work/catches/sha_catches.txt`, 159 entries incl. traces/analyses).
v20: 23 legs (RT-A, RT-B, RT-C base/v1–v6, RT-D s1/s10/s100, RT-E ×4,
RT-F, T1, T3). v26: 23 legs (same). Traces: v26 RT-B, RT-F, T3, s1-matrix.

### 4.1 Matrix bars (frozen `bars_full.py`, s1/s10/s100)

| variant | B1 | B2 | B3 | B4 | B4b | B5 | B13 |
|---|---|---|---|---|---|---|---|
| v20 (all scales) | 0 ✓ | 0/0 ✓ | **2** | 0.9500 ✓ | 0.9500 ✓ | 0.5429 ✓ | **0** ✓ |
| v26 (all scales) | 0 ✓ | 0/0 ✓ | **0** | 1.0000 ✓ | 1.0000 ✓ | 1.0000 ✓ | **0** ✓ |

B3/B13 at floor for both (Micah's ~11:20 ruling: bars no longer
discriminate). v26 additionally clears the G and calibration bars the
v20 constant cannot (B4/B4b 1.0 vs 0.95, B5 1.0 vs 0.543) — but these are
reported, not deciding.

### 4.2 Red-team asymmetry (|err| ≤ 0.100, per (id,depth) row)

| battery | n | v20 catch/miss | v26 catch/miss | only20 | only26 | v20 mean|err| | v26 mean|err| |
|---|---|---|---|---|---|---|---|
| RT-A | 300 | 165/135 | 165/135 | 0 | 0 | 0.3080 | **0.2930** |
| RT-B | 100 | 35/65 | 35/65 | 0 | 0 | 0.5175 | **0.5125** |
| RT-C base | 120 | 108/12 | 108/12 | 0 | 0 | 0.1200 | **0.1000** |
| RT-C v1 | 120 | 107/13 | 107/13 | 0 | 0 | 0.1279 | **0.1083** |
| RT-C v2 | 120 | 107/13 | 107/13 | 0 | 0 | 0.1279 | **0.1083** |
| RT-C v3 | 120 | 105/15 | 105/15 | 0 | 0 | 0.1438 | **0.1250** |
| RT-C v4 | 120 | 108/12 | 108/12 | 0 | 0 | 0.1200 | **0.1000** |
| RT-C v5 | 120 | 107/13 | 107/13 | 0 | 0 | 0.1279 | **0.1083** |
| RT-C v6 | 120 | 96/24 | 96/24 | 0 | 0 | 0.2150 | **0.2000** |
| RT-D s1 | 200 | 138/62 | 138/62 | 0 | 0 | 0.2328 | **0.2158** |
| RT-D s10 | 3200 | 2140/1060 | 2140/1060 | 0 | 0 | 0.2453 | **0.2297** |
| RT-D s100 | 44000 | 29000/15000 | 29000/15000 | 0 | 0 | 0.2510 | **0.2360** |
| RT-E learn | 150 | 100/50 | 100/50 | 0 | 0 | 0.3433 | **0.3333** |
| RT-E fatigue | 150 | 120/30 | 120/30 | 0 | 0 | 0.2033 | **0.1833** |
| RT-E solo_learn | 5 | 1/4 | 1/4 | 0 | 0 | 0.7900 | 0.8000 |
| RT-E solo_fatigue | 5 | 3/2 | 3/2 | 0 | 0 | 0.3700 | **0.3500** |
| RT-F collide | 100 | 70/30 | 70/30 | 0 | 0 | 0.3100 | **0.3000** |

**Reading:** binary catches are IDENTICAL on all 17 batteries (zero
asymmetric rows — neither variant catches anything the other misses).
v26's mean|err| is lower on 16/17 (the one exception: RT-E solo_learn,
n=5, noise). The schema buys better calibration, not new catches, on the
red-team batteries. RT-F: both miss the same 30 rows (the known 63-byte
ID-cap defect, pre-FIX1; Amendment A1: FIX1 flips both to catch, tie
preserved).

### 4.3 T1 — latch dynamics (M1/M2/M3, NOT the catch rule)

| variant | crater(C−T@d2) | C@d2 | T@d2 | M1 | M2 exact | max sparing | M3 B13 |
|---|---|---|---|---|---|---|---|
| v20 | +0.950 | 0.950 | 0.000 | ✓ | 150/150 | +0 | 4 |
| v26 | +0.802 | 0.802 | 0.000 | ✓ | 150/150 | +0 | 4 |

TIE. Both follow their stated rules exactly; both crater honestly after a
wrong observation (T1T: first obs wrong → latch 0 → all later confs 0);
zero withholding; identical B13 cost. (An earlier asymmetry-table T1 row
showing v20=66 vs v26=6 was a scoring artifact — T1 is not a
|err|≤0.100 battery — and is struck.)

### 4.4 T3 — unseen classes (frozen §4 rule: overall <0.470 AND bias ≥ −0.05)

| variant | C0 | C1 | C2 | C3 | C4 | overall |err|/bias | rule |
|---|---|---|---|---|---|---|---|
| v20 | 0.0500/−0.0500 | 0.2000/+0.2000 | 0.4500/+0.4500 | 0.7000/+0.7000 | 0.9500/+0.9500 | 0.4700/+0.4500 | FAIL |
| v26 | 0.1980/−0.1980 | 0.0520/+0.0520 | 0.3020/+0.3020 | 0.5520/+0.5520 | 0.8020/+0.8020 | **0.3812**/+0.3020 | PASS |

v26 wins T3 (0.3812 < 0.470, bias +0.3020 ≥ −0.05). Trace-verified honest
mechanism: every T3C item → L3 backoff, rate 802000
(`L0 T3C0-000 75 875 1 3 1000 802000`, all classes). v20 emits its 0.95
constant regardless of unseen-ness (bias +0.45). This is the single
biggest catches-margin in the round (19% lower mean|err|), and it is
mechanism-explained, not noise.

### 4.5 White-box traces (exact excerpts)

- **S2:** s1 matrix, v26: 1000/1000 items resolve at L1 (level histogram:
  `1000 × level 1`); v20: constant assignment, no lookup.
- **RT-B wrong-first** (`rtb-wf-00` [W,W,C,C,C]): v26
  `L0 rtb-wf-00 931 1000 1 1 8 1000000` then
  `L1 rtb-wf-00 2 1000000 0 0` — first-obs wrong → latch 0 → conf 0
  thereafter. v20: `d1→950, d2→0, d4→0` (same latch, seed 0.95).
- **RT-B correct-first** (`rtb-cf-00` [C,C,C,C,C]): v26
  `L1 rtb-cf-00 2 1000000 1000000 1000000` — stays at seed. No inversion.
- **RT-F long id** (72 chars, pre-FIX1): 5 L0 lookups, all
  `level=1 rate=1000000`; the 63-byte `nec_cmp_id` cap is the shared
  defect (both variants; FIX1 dispatched per Amendment A1).
- **T3:** `L0 T3C0-000 75 875 1 3 1000 802000` — L3 honest backoff,
  all classes.

### 4.6 Catches reading

No blowout (nothing ≥10×, no binary catch/miss asymmetry — the closest is
T3 at 19%). The catches dimension favors v26 throughout: identical binary
catches on red-team batteries with uniformly better calibration
(16/17), T1 tie, T3 win by mechanism (honest backoff vs constant).

## 5. SHA logs

- `work/speed/sha_speed.txt` — 6 matrix legs × A/B/C + interleaved pairs
  + S2 trace (all byte-identical; v20 reproduces adopted m20 SHAs).
- `work/cost/sha_cost.txt` — RSS-run outputs (v20 s1 == scored s1 output,
  v26 s100 == scored s100 output verified by cmp).
- `work/catches/sha_catches.txt` — 46 legs × A/B/C (138 runs) + 3 trace
  files + t1_h2h/t3_h2h/asymmetry/traces analyses (159 entries).
- Binary: `7f6e0ceab59ad8a65d7a3a1500021b52934f3f41f81d34588284307e5745071f`.
- Prereg: `55cbc037c31a3ed706367b828912e5c062ba1fbe36ffb9b8b9afdce470b42c1f`.

## 6. Adversity log (honest record of what went wrong)

1. **Shared-VM contention** polluted wall-clock timings (load 5–14 on 2
   cores). Mitigated by triplicates + interleaved drift-cancelling
   validation + the mechanistic S2 bound. s100 sequential v26 set
   discarded for comparison; conclusion rests on the bound + interleaving.
2. **S3 chunked-tail design failed:** startup overhead (median 401 ms,
   spread 171–682 ms) dominated chunk compute → negative per-item times.
   Abandoned; replaced by the deterministic worst-case bound.
3. **Cost crew RSS:** `/usr/bin/time` absent on this VM → repaired with a
   Python `resource.ru_maxrss` harness (`analysis/rss_one.py`).
4. **Catches crew died twice:** (a) first run killed after v20 RT-D s10
   (pipe masked the exit); (b) resume hit rc=107 — RT-D s100's 8800 items
   exceed max_items(s1)=1200; fixed by passing matching scales (s1-vs-s10
   outputs proven byte-identical, so completed s1-scale legs stand).
   A daemon restart then wiped the second resume mid-run; the idempotent
   resume script (`mkrun` skips byte-identical legs) completed on attempt 3.
5. **asymmetry.py conf-scale bug:** divided output conf by 1e6 instead of
   1e3 (output is conf_thousandths) → v20≡v26 artifact. Fixed, reran.
6. **T1 mis-scored by the catch rule:** |err|≤0.100 on T1 rewarded m20's
   constant over S's honest backoff (66 vs 6 artifact). Struck; T1 scored
   by its frozen M1/M2/M3 framework (`analysis/t1_h2h.py`) → tie.
7. **C5 projection script bug:** `v=="20"` filter vs `"v20"` values →
   empty median crash (masked by `| tee` without pipefail). Fixed, reran.
8. **Amendment A1** (committed `4df783f9`): Micah's ~11:50 UTC ruling —
   FIX1 + FIX-A apply now; recorded as orthogonal to the frozen
   contenders (shared code path, RT-F stays a tie either way).
