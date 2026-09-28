# F34 LSTWBA — Pre-Run Spec Record

**Written BEFORE any build or training run. Date: 2026-09-25.**
(Corrected 2026-09-25: original draft said 2026-09-24 in error.)
**Fork:** F34 LSTWBA (Latched State Tax, Worst-Boundary Adversary), mech 34.
**Frozen authority:** sylorlabs/TNN @ `3a2eef44` (v2),
  `docs/lab/deliberation_depth/monotonicity/training/fork_round/PREREG_FORKROUND.md`
  §3 (F34) + `ideas/grok_forks.md` FORK 3 (authoritative on mechanism detail;
  read in full before building — done).

## 1. Frozen pins

- Training cells: `training/features/features.tsv`, 5240 rows, 15 cols
  (id, family, heldout, depth, t, rel4, correct4∈{1,0,A}, f1..f8).
  SHA256 `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
  (verified before training; heldout=1 rows skipped — 4820 train rows,
  4222 released per pass).
- Toolchain ONLY: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Harness: `training/src/*.zag` copied byte-identical into `src/`
  (SHA-verified per file, recorded in logs/).
- Shared grok substrate: ρ(k,n)=(k+1)·1000/(n+2) ∈ [1,998]; d_idx=log2(d)
  for d ∈ {1,2,4,8,16,32,64} → {0..6}; updates after label observed;
  M4 release skeleton UNTOUCHED (release ⟺ L_t == L_1).
- Eval: NEC-style BATCH driver (one binary, frozen ordered cell list,
  all 37 TSVs in one run, per-item state in memory). Leg order =
  run_eval.sh order (admit/revoke/logic/trap/cost/redteam × {1,2,4,8,16},
  then ceiling × {1,2,4,8,16,32,64}). Controller state stays ONLINE
  through eval (prereg §6: online-state forks run repeated battery passes;
  NEC precedent: ledger GT-updated during eval).
- CTL yardstick: NEC m9 (B2 pass, B3=6, B13=6). Kill (c): eval strict B3 ≥ 6.

## 2. Region construction (FIXED, recorded before first run)

Per-item region r ∈ {0..14}, assigned ONCE at depth 1 from depth-1 features,
stored as per-item cross-depth state (never recomputed):

- m = min(4, f1/200), f1 = depth-1 margin (thousandths, clamped [0,1000]).
- my = f5 at depth 1 (thousandths, clamped [0,1000]); yld = min(2, my/400).
- r = m·3 + yld.

The family is DISCOVERED as the region whose G misbehaves — no family label
enters r.

## 3. Tax schedule + inits (BEFORE first run)

- T[d_idx][r], d_idx ∈ 0..6, r ∈ 0..14: init 0. Invariant after every write:
  T[d][r] ≥ T[d−1][r] for d ≥ 1.
- Per region: depth-1 released ledger (n_r, k_r) init (0,0); per (r,d_idx)
  released running sums (n, ΣC, Σy) init 0; correct-mean accumulators
  (ΣC_corr, n_corr) init 0; B4-freeze bit init 0 (unfrozen).
- Per-item state (keyed by item id): region (−1=unset), C* (latched depth-1
  ρ), C_prev, f8_d1 (latched depth-1 f8), f3_prev, f8_prev. Cleared at each
  training-pass boundary (each pass re-latches at depth 1).

## 4. Emit rule (per cell, released or not)

1. d_idx from the row/leg DEPTH (not t): 1→0, 2→1, 4→2, 8→3, 16→4, 32→5,
   64→6. Unknown depth → hard error.
2. At depth 1: assign r (§2); latch C* = ρ(k_r, n_r) = (k_r+1)·1000/(n_r+2)
   from region r's depth-1 released ledger (previous-items-only state);
   latch f8_d1 = f8.
3. π = min(400, (f3>0 ? 50 : 0) + max(0, f8 − f8_d1)/8), integer division
   truncating toward zero. (f8^(1) in the ideas file = depth-1 f8, latched
   per item — the (1) superscript denotes depth 1, distinct from the
   previous-step language used in the flip rule.)
4. C = clamp(C* − T[d_idx][r] − π, 1, 999).
5. Flip rule: if d_idx > 0 AND (f3 > f3_prev OR f8 > f8_prev):
   C ← min(C, C_prev − 1). ("f3 just latched" ⟺ f3 rose 0→1000 this step;
   f3 is the cumulative leader-change indicator, so f3>f3_prev ⟺ 0→1000.)
6. Store C_prev ← C, f3_prev ← f3, f8_prev ← f8.

## 5. Update rule (after label observed; released cells only — one tax unit
##    per released outcome, for the item's LATCHED region r)

Let sums be the region's per-depth released sums AFTER incorporating this
cell (n++, ΣC += C_emitted, Σy += y where y=1 iff correct).

1. g[d] = tdiv(ΣC[d],n[d]) − tdiv(1000·Σy[d],n[d]) if n[d] ≥ 8,
   else (d>0 ? g[d−1] : 0). tdiv = truncation toward zero.
2. d* = argmax_{d≥1} (g[d] − g[d−1]); ties → larger d_idx.
3. Correct-mean / B4-freeze (BEFORE the tax step): if y==1:
   ΣC_corr += C; n_corr++. If tdiv(ΣC_corr,n_corr) < 520
   AND not frozen: frozen_r ← 1 (LATCHING, permanent; recorded with stream
   index). (EXACT ideas-file rule — no n gate. Cold-start C*=500 may freeze
   a region on its first correct outcome; that is the specified behavior.)
4. If g[d*] − g[d*−1] > 0:
   - If frozen_r: SKIP the increment (no tax change; the honest-region
     protection holds). (Kill-bar (b) is NOT evaluated online — it is a
     post-hoc check after training settles, §6.)
   - Else: T[d*][r]++; for j=d*..6: T[j][r] = max(T[j][r], T[j−1][r])
     (monotone repair upward). Mark "tax changed".
5. Else (worst boundary ≤ 0): if ∃d: g[d] < −80:
   d_m = argmin_d g[d] over d ∈ 0..6, ties → larger d_idx.
   If T[d_m][r] ≥ 1 AND (d_m==0 OR T[d_m][r]−1 ≥ T[d_m−1][r]):
   T[d_m][r]-- ; mark "tax changed". (The only decrease allowed.)
6. Settle tracking: consecutive released items with no tax change.
   Training stops at 500 (ideas-file settle criterion) or 10^4 released
   items — see §6.

## 6. Training run

- Stream: heldout=0 rows of features.tsv in file order (item-major:
  depths 1,2,4,8,16[,32,64] per item), repeated passes in the same fixed
  order until settle (500 consecutive released items, zero tax change) or
  10^4 released items processed.
- Per-item state cleared at each pass boundary (each pass re-latches).
- Global controller state (T, ledgers, sums, freeze bits) persists across
  passes — one continuous online stream.
- Kill (a): at 10^4 released items, if the trailing 500 were NOT all
  change-free (taxes still moving) → KILL (mark verdict; still run the full
  37-leg battery for characterization). (With 4222
  released/pass, 10^4 ≈ 2.37 passes.)
- Kill (b): POST-HOC, evaluated once after training settles (or at 10^4):
  if any region has g[d]−g[d−1] > 0 on a cell with n ≥ 30 → KILL.
  A killed fork is still characterized through the FULL 37-leg eval battery
  (using terminal params) — kill marks the verdict, it does not abort
  mid-battery.
- Params artifact: deterministic LE serialization of T[7][15], per-region
  (n_r,k_r), per-(r,d) (n,ΣC,Σy), (ΣC_corr,n_corr), frozen bits.
  Training run TWICE → byte-identical params (gate).

## 7. Eval run (batch driver)

- Binary `f34_eval`: loads params, processes the frozen 37-cell list in
  run_eval.sh order; per (leg,item): fresh deliberation at the leg depth
  (frozen harness, cfg shallow=deep=depth), t=min(depth,rounds),
  release ⟺ hist_l[t]==hist_l[1] (M4), features via pl_features, F34 emit
  (§4) with per-item state keyed by id, TSV row
  (id,depth,t,rounds,consumed,ne,release,correct,conf,leader_idx,cert);
  controller update (§5) on released cells — online through eval.
- cert: "lstwba" if released else "leader-changed".
- A/B: two full runs → all 37 TSVs byte-identical. M4 reference TSVs copied
  in (B9 check). Frozen analyze.py for bars; deltas vs NEC m9.

## 8. Determinism gates (§8)

Pure Zag, zero RNG, fixed file order, integer arithmetic, truncating
division via explicit helper (codegen div semantics not trusted for
negatives). []u8 arenas + LE accessors; no fn named zalloc; no slice >
2^25 bytes; no bare {...} blocks. A/B byte-identical builds AND runs.
No binaries/.zagd committed.

## 9. Verdict mapping (§10)

- SUPPORTED: clears B1–B9+B13 short + §6 horizon.
- KILLED: (a)/(b) fire, or eval B3 ≥ 6 (kill c), or any B1–B9/B13 bar fails
  — failing bar named + failure-mode number from §7 taxonomy (new mechanism
  → new numbered entry).
- This round has no separate long-horizon gate in the task; §6 applies to
  survivors only.
