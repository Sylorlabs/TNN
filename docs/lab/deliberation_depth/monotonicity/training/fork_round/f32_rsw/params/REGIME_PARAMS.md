# F32 RSW — Regime-Switch Calibrator: rule parameters + inits

Recorded BEFORE the first training run (2026-09-24). Frozen authority:
`PREREG_FORKROUND.md` §3 (F32) + `ideas/grok_forks.md` Fork 1 (authoritative
on mechanism detail; wins on discrepancies).

## Key

- `m = min(4, f1/200)` — 5 margin bins (0..4).
- Marginal yield (thousandths, clamped [0,1000]):
  - at depth 1: `my = f5`
  - later: `my = min(1000, max(0, f5 − f5_prev)·1000 / max(Δf2, 1))`,
    `Δf2 = (d − d_prev)·1000/64` (integer division, truncating toward 0)
- `yld = min(2, my/400)` — 3 bins (0..2).
- Key `r = m·3 + yld` ∈ {0..14}. 15 keys × 7 depths (d ∈ {1,2,4,8,16,32,64},
  `d_idx = log2(d)` ∈ {0..6}) → 105 cells. **f7 is NOT a key** (FM2).

## Interior-ratio invariant

`ρ(k,n) = (k+1)·1000/(n+2)` (integer division, truncating). Cold start
`ρ(0,0) = 500`. Codomain [1,998]: 0 and 1000 unreachable by construction
(FM1: no clamp attractors).

## Regime bit

- `z_r ∈ {LATCH, TRACK}` per key, **init LATCH** (0).
- Evaluated after each training-row update once the key's pooled released
  count `n_r = Σ_j n_{r,j}` ≥ **32**.
- `γ_r = ρ_deep − ρ_shallow`, pooled: deep = `d_idx ≥ 4` (d ∈ {16,32,64}),
  shallow = `d_idx ≤ 1` (d ∈ {1,2}); `ρ_deep = ρ(Σ_{j≥4} k_{r,j}, Σ_{j≥4} n_{r,j})`,
  likewise shallow. Integer thousandths.
- `LATCH→TRACK` iff `γ_r ≥ 100` **AND** the three most recent pooled
  γ evaluations are each ≥ 0 (hysteresis; history init to −1 = "not
  nonnegative", so three real evaluations are required before any switch).
- `TRACK→LATCH` iff `γ_r ≤ 60` (single evaluation; hysteresis gap 60..100).
- Switch events counted per key (hysteresis-failure report: keys switching
  more than once).

## Depth-1 commitment

`C* = ρ(k_{r,0}, n_{r,0})` computed from pre-update cell state at the item's
depth-1 row, stored on the item. Never raised by later feature movement
inside LATCH.

## Closed-form shift (selection identity)

Per key `r`, arrival depth `j ≥ 1` (previous items only):
- `E_j(r) = trunc(ΣC^stay/n^stay) − trunc(ΣC^all/n^all)`
- `ΔA_j(r) = trunc(k^stay·1000/n^stay) − trunc(k^all·1000/n^all)`
- `δ_j(r) = ΔA_j(r) − E_j(r) − β_r`
- Transition sums per (key, arrival depth j), all from released-at-`d_prev`
  rows: `n^all`/`ΣC^all`/`k^all` updated on every row whose item was
  released at `d_prev` (stay or drop); `n^stay`/`ΣC^stay`/`k^stay` only when
  the item is also released at `d` (nested release sets make stay =
  released-at-`d`). `ΣC` uses the item's EMITTED C at `d_prev`.
- **β_r = 2** in LATCH, **β_r = 4** in TRACK (buffer; dominated by measured
  E,ΔA once n is large).
- Empty denominator (n^stay=0 or n^all=0) → the depth is skipped:
  `δ_j = 0` (contributes nothing to S).
- Cumulative `S_j = Σ_{t=1..j} g(δ_t(r))`, `g = min(·,0)` in LATCH
  (only nonpositive shifts admitted; S nonincreasing ≤ 0),
  `g = identity` in TRACK.

## Emit

- LATCH: `C = clamp(C* + S_j, 1, 999)`.
- TRACK: `C = clamp(ρ(k_{r,j}, n_{r,j}) + min(S_j, 0), 1, 999)`
  (unrestricted δ summed, then only the nonpositive cumulative part admitted).
- At depth 1 (`j=0`, `S_0=0`): both regimes emit `C = C*`.
- Flip/trauma (depths > 1 only): on `f3 > 0` (leader-change latch) OR
  `f8 > f8_prev` (trauma increase this step): `C ← min(C, C_prev − 1)`,
  where `C_prev` is the item's own final emitted C at the previous depth.

## Update order (per training row, frozen file order)

emit C (pre-update state) → observe release+label → increment cell
(released rows only) and stay/drop transition sums → recompute γ and
possibly flip z_r. Byte-identical given the same trace order.

## Training discipline

- Frozen `training/features/features.tsv`
  (SHA256 `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`,
  verified on disk), 5240 rows.
- Heldout rows (`heldout=1`, 420 rows) SKIPPED — never trained, never
  update state. 4820 rows trained.
- Rows processed in frozen file order (grouped by item, depths ascending).
  Per-item cross-depth state (f5_prev, d_prev, f8_prev, C_prev, C*,
  rel_prev, correct_prev) reset on item-id change.
- M4 release rule untouched (rel4 from the TSV at train; `L_t == L_1`
  from the frozen harness at eval).
- Single online pass. Training run twice → byte-identical params.
- All integer fixed-point; zero RNG; pure Zag.

## Inits summary

cells n=k=0; transition sums 0; z_r=LATCH; γ-history {−1,−1,−1};
switch counts 0; per-item state cleared on item change.
