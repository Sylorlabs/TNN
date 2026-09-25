# F35 CDC (Cluster-Discovered Ceilings) — Build Design Record

**Date:** 2026-09-25. Recorded BEFORE first training run / first build (per task).
Written 2026-09-24, corrected to 2026-09-25 before any build or training run;
no binary existed and no training had occurred at either date.
**Fork:** F35 CDC, mech 35.
**Frozen authority:** `PREREG_FORKROUND.md` FROZEN v2 §3 (F35) +
  `ideas/grok_forks.md` Fork 5 (CDC) — authoritative on mechanism detail;
  Fork 2 (SRS) for the residual formula; Fork 1 (RSW) for the `my` definition.
  Prereg commit: `3a2eef44` (v2). This file resolves every ambiguity found;
  the ideas file wins on all mechanism questions.

## 1. Frozen pins

- Training cells: `training/features/features.tsv`, 5240 rows, 15 cols
  (id, family, heldout, depth, t, rel4, correct4∈{1,0,A}, f1..f8).
  SHA-256 verified on disk:
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`.
- Heldout flags honored: only heldout=0 rows ever update learned state.
  Verified: heldout is constant per item (no mixed items).
- Stream order = features.tsv file order (item-major, depths ascending
  1,2,4,8,16 per item; ceiling D/O/P items 1..64). Deterministic.
- Toolchain ONLY: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Harness modules copied byte-identical into `src/` (SHAs in
  `logs/SRC_SHA256SUM.txt`): R33_NATIVE_IO_V1.zag, R33_NATIVE_SHA256_V2.zag,
  dlb_util.zag. (The batch driver reads the frozen cell list; it does not
  re-run the harness. The harness's M4 release/correctness outputs are
  already encoded as rel4/correct4 in features.tsv.)
- Eval: NEC-style BATCH driver (prereg §2, explicitly allowed): one binary,
  frozen ordered cell list (features.tsv), all 37 TSVs in one run,
  per-item cross-depth state in memory. A/B = two runs, byte-compared.
- CTL yardstick deltas vs NEC m9 (B2 pass, B3=6, B13=6).

## 2. Architecture: two phases

- **Phase 1 — train** (`f35_train.zag`): streams features.tsv in file order;
  processes heldout=0 cells with full online updates (§4–§7); writes
  `params/f35_params.txt` (prototypes, τ, ρ counts, per-cluster transition
  sums, cap flag), `params/cluster_log.tsv` (final-prototype reassignment of
  every training released cell: id, battery9, cluster), and
  `logs/train_stats.tsv` (per-256-block movement/birth/merge/τ).
  Run twice → byte-identical params (§8 gate).
- **Phase 2 — eval** (`f35_policy.zag`): streams features.tsv in file order;
  loads params (frozen); assigns clusters (nearest, NO birth/merge/update);
  emits conf per §8; maintains per-item inference state; writes the 37
  per-leg TSVs `<battery>_m35_d<depth>_<tag>.tsv` in one run. Run twice
  (tag A, tag B) → byte-identical (A/B gate).

## 3. State vector and inits (recorded BEFORE first run)

- x = (f1, f5, f6, min(f8,1000), my) ∈ Z^5, all thousandths, ≥ 0.
  f8 is already ∈ [0,1000] in the data; min() is a no-op guard.
- `my` (marginal yield, per ideas Fork 1):
  depth 1: my = f5;
  depth d>1: my = min(1000, max(0, f5 − f5_prev)·1000 / max(Δf2, 1)),
  Δf2 = (d − d_prev)·1000/64, where (f5_prev, d_prev) are from the item's
  previous RELEASED cell. All integer, non-negative → native `/` exact.
- Prototype init: EMPTY (K=0). First training released item births p_0 = x
  exactly, nproto[0]=1, and records assignment distance 0.
- τ init: UNDEFINED until the 32nd training released item is processed.
- ρ counts init: kc[c]=nc[c]=0 → ρ(0,0)=500 for a fresh cluster.
- All transition sums init 0 → δ=0 on empty denominators ("the depth is
  skipped").
- Per-item state init: empty slot table (id → last_cell, last_released).

## 4. τ rule (exact, data-determined)

- Distances recorded: nearest-prototype L1 distance of every ASSIGNED training
  released cell, in stream order. A birth cell has no nearest-prototype
  distance (there was no prototype to be near, or it was farther than τ);
  fabricating 0 would drag τ down and distort the birth threshold. Only
  assignments record. (Resolution: the spec's "nearest-prototype distances"
  and "assignment distance" refer to assignments, not births.)
- After the 32nd training released item: sort all recorded distances so far
  ascending d[0..m-1]; τ = d[(3·(m-1))/4] (75th percentile, order statistic).
  With one birth among the first 32, m=31 and τ=d[22].
- Recompute at training-released counts N ∈ {256,512,768,…}: τ = 2 × median
  of the LAST up-to-256 recorded distances; median = lower median,
  sorted[(w-1)/2] where w=min(256, recorded). With w=256, index 127.
- τ is an integer ≥ 0. Merge threshold τ/3 uses integer division.

## 5. Assignment / birth / merge (training only; exact order per cell)

For each training released cell, with x computed:
1. If K=0: birth p_0=x (see §3). Else c = argmin_j L1(x,p_j), ties → smaller
   j; dist = L1(x,p_c). Record dist.
2. If τ defined and dist > τ:
   - if K < TEST_KMAX (8): append p_K=x, nproto[K]=1, c=K, K+=1.
   - else: cap_bound=1 (birth denied by the test cap; recorded).
   Else (no birth): nproto[c]+=1 (increment FIRST); per-coordinate
   p_c[k] += tdiv(x[k] − p_c[k], nproto[c]), k=0..4.
   tdiv(a,b) = truncation toward zero (explicit; b>0).
3. If τ defined: merge pass — repeat until no pair fires: scan i<j ascending;
   if L1(p_i,p_j) < τ/3: merge j into i:
   n_i += n_j; p_i[k] = tdiv(n_i_old·p_i[k] + n_j·p_j[k], n_i_new);
   add ALL per-cluster SRS state (kc,nc; per transition nstay,sumCstay,
   nall,sumCall,kall,kstay) of j into i; compact slot K−1 into j; K−=1;
   remap the current item's c (c==j→i; c==K−1→j); restart scan.
   Merge fires at most until fixpoint; order deterministic.

**K≤8 note (Micah's no-arbitrary-limits law):** the prototype STORE is
allocated for 64 slots (expandable; memory bound only). TEST_KMAX=8 is the
preregistered TEST CONSTANT for this experiment, enforced as a parameter,
not an architectural ceiling. Growth rule beyond the test constant: birth
appends a new slot (documented here); the experiment records cap_bound.
If the cap never binds, the test constant did not constrain the result.

## 6. Per-cluster SRS state (training only)

Per cluster c, per schedule transition j ∈ {0..5} ↔
(1→2, 2→4, 4→8, 8→16, 16→32, 32→64): nstay, sumCstay, nall, sumCall, kall,
kstay (i64, []u8 arenas + LE accessors).
Per cluster: kc[c], nc[c] (depth-1 released correct/total).

Update rules (label observed AFTER emit; training cells only). Let prev =
item's previous cell (always at depth d/2 when d>1; binary asserts
d == 2·prev.depth — fail-closed):
- If prev.released (at d/2): j=trans_idx; c2=prev.cluster;
  nall_j[c2]++, sumCall_j[c2]+=prev.C, kall_j[c2]+=prev.correct.
  If current cell released: nstay_j[c2]++, sumCstay_j[c2]+=prev.C,
  kstay_j[c2]+=cur_correct.
  (Non-released training cells contribute the dropout population to nall.)
- If depth==1 and released: kc[c]+=correct; nc[c]+=1 (c = final cluster
  after §5 merges).

δ_j(c) at emit time (frozen from previous items = current cumulative sums):
- if nstay==0 or nall==0: δ=0.
- else E = sumCstay/nstay − sumCall/nall;
  ΔA = kstay·1000/nstay − kall·1000/nall;
  δ = clamp(ΔA − E − 3, −40, 40). (Operands ≥ 0; native `/` exact.)

## 7. Emit (both phases; params frozen at eval)

Per released cell (inference state: last_released per item):
- my, x as in §3. c = argmin L1 (no birth/merge at eval).
- d_idx = log2(depth) ∈ {0..6}. dsum = Σ_{j=1..d_idx} δ_j(c) (δ from §6;
  at eval, from frozen params).
- Depth 1: Cstar_item = ρ(kc[c],nc[c]) = (kc+1)·1000/(nc+2) [pre-update
  counts]; store per item. Deeper: Cstar_item from depth 1 (stored).
- flip_or_trauma = (f3>0) ∨ (f8>f8d1), f8d1 = f8 at depth 1 (stored).
  π = flip_or_trauma ? min(400, (f3>0?50:0) + (f8−f8d1)/8) : 0.
- C_emit = clamp(Cstar_item + dsum − π, 1, 999).
- Yield gate (ON CLUSTER TRANSITIONS ONLY, c ≠ c_prev): if C_emit > C_prev
  and my ≤ my_prev: C=C_prev; elif my > my_prev: C=C_emit; else C=C_emit.
  (Same cluster: C=C_emit — the SRS identity governs.)
- Flip/trauma −1 rule (after the gate; depth>1 only):
  if flip_or_trauma: C = min(C, C_prev−1).
- Final: C = clamp(C, 1, 999). Output conf=C.
- Non-released cells: conf=0 (matches training-M4 abstain rows, verified).

Per-item inference state updated after emit (both phases): last_cell and
last_released (depth, cluster, C, correct, f5, my, f8d1, Cstar_item).

## 8. B9 (release+correct identity vs M4)

The fork implements NO release logic (prereg §2 forbids changing it).
release/correct are taken verbatim from features.tsv (rel4/correct4 — the
frozen harness's M4 outputs; verified 5240/5240 consistent with the
training round's M4 TSVs in results_100x). Release label strings
(ACCEPT_INSTALL/…/ABSTAIN:leader-changed) and the frozen non-conf columns
(t, rounds, consumed, ne, leader_idx, cert) are reproduced from the frozen
training-M4 reference via a lockstep map file `params/cellmap.tsv`
(generated by script from results_100x `*_m4_d*_A.tsv`, order-verified
1:1 against features.tsv). The eval binary reads features.tsv +
cellmap.tsv in lockstep and writes only conf itself. B9 is then a real
check of (release, correct) identity against results_100x M4 copies in
the results dir.

## 9. Kill bars & falsifiers (operationalized)

Per prereg §4 + task kill list:
- (a) DISCOVERY: I(cluster; battery9) on training released cells under the
  FINAL prototypes (cluster_log.tsv). KILL if MI < 0.05 bits
  (≈5× the finite-sample noise floor ≈0.01 bits at n=4222).
- (b) CHURN: per-256-block max prototype L1 movement (running-mean only)
  + birth/merge counts in train_stats.tsv. KILL if, in the last complete
  256-block within the first 2000 training released items (items
  1536..1791), max movement > τ_block/10 OR any birth/merge fired.
- (c) EVAL: KILL if strict B3 (family G-violations, frozen analyzer) ≥ 6
  (NEC m9's 6).
- §5 go/no-go: VOID (not killed) if K<2 at checkpoint (no partition
  discovered = dead intervention). GO requires K≥2, τ defined, nc>0.

## 10. Determinism gates (§8)

Pure Zag, zero RNG, fixed stream order, integer arithmetic, explicit tdiv
where negatives occur. Pinned toolchain only. Training ×2 → byte-identical
params+logs. Eval ×2 (A/B) → byte-identical 37 TSVs. []u8 arenas + LE
accessors for all indexed tables; no `zalloc`; no slice > 2^25 (largest:
per-leg DOut 256KB; file buffers < 2MB). No binaries/.zagd committed.

## 11. Analysis plan

- `analysis/mi_churn.py`: MI(cluster;battery9) from cluster_log.tsv;
  churn table from train_stats.tsv; per-cluster residual signs (δ per
  cluster×transition from params); discovered K; cap_bound.
- Frozen `training/analyze.py` on results dir (37 m35 TSVs + m4 copies):
  B1–B9, B4b, B13, recorded B12/B3pi; deltas vs NEC m9.
- VERDICT.md per prereg §10 (SUPPORTED/PARTIAL/KILLED/DEGENERATE/VOID),
  failure-mode number from §7 taxonomy (+new entry if novel).
