# VERDICT — F25 DISMIN v2 (Disjoint-Feature Min Ensemble), mech 25

- **Date:** 2026-09-25
- **Fork:** F25 DISMIN, `PREREG_FORKROUND.md` FROZEN v2 (commit `3a2eef44`)
  §3 + **§5b repaired TRAIN-COORD v2** + `ideas/native2_forks.md` FORK 2
  (ideas file authoritative on mechanism; §5b overrides veto application).
- **Verdict: VOID** — dead at the prereg §5 training checkpoint under the
  repaired trainer. Reported with evidence, not killed; no eval spend (same
  discipline as v1's VOID and F26/F27's stillborn gates).
- v1 evidence in `f25_dismin/` (PROTOCOL.md, VERDICT_F25.md, v1 logs)
  untouched; all v2 artifacts under `f25_dismin/v2/`.

## What was built

`v2/src/train_dismin2.zag` — TRAIN-COORD v2 exactly as §5b specifies:

- All 10 params init 0; fixed sweep order [bias, w1..w4]; per param visit
  step sizes **±50, then ±8, then ±1 refine** (+s first, then −s; first
  strict L-reduction accepted, incumbent updated immediately); box
  [−1000,1000]; 8 full sweeps; objective Σ(C−1000y)² per head over the 4222
  released training cells. **No vetoes on candidates** — 198 accepted steps,
  of which 192 had v12>0 and all 198 had v3bad=1 logged-but-not-gating
  (verified in the log: acceptance is pure strict L-reduction).
- **Vetoes V1–V3 on the FINAL fitted head only** (violating head = VOID).
- Δ grid {0,50,…,500} ascending, Δ added to **both biases inside the clamp**
  (correcting v1's post-clamp addition; ideas-file-literal), maximizing
  training B4 score subject to V3 on the grid (strict-greater wins,
  ties → smaller Δ).
- Training-cells dump (id, family, depth, y, A, B, C with final heads) for
  the per-head-vs-min B8-on-training analysis.
- Pure Zag, zero RNG, pinned toolchain only
  (`toolchain/bin/znc_linux_x86_64_abed8aa1`); []u8 arenas + LE accessors;
  no `zalloc`; no slice > 2^25. Frozen harness modules copied
  byte-identical (SHA-verified) into `v2/src/`.
- Protocol + inits recorded in `v2/PROTOCOL.md` and **committed
  (`0db96133`) BEFORE the first training run**.

## Determinism record (§8 gates)

| Check | Result |
|---|---|
| Build ×2 (pinned znc) | byte-identical, SHA `69a53efa3b2e1ecfa45fa125269e70a488c9987c917285e297c681bb0a11e950` |
| Train ×2 | params byte-identical (`b931de03…41c6411e`), logs byte-identical, cells dumps byte-identical |
| Features hash | `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d` (v2 corrected hash, verified) |

## Evidence

**The trainer moves under v2** (the §5b repair works as intended):
objective 3.880e9 → 2.740e8 (A) / 2.464e8 (B) over 8 sweeps.

Fitted heads (pre-shift):
- A: a_0=472, a_1=472 (f1 margin), a_2=453 (f2 depth), a_3=0 (f3), a_4=239 (f4)
- B: b_0=404, b_1=336 (f5 consumed), b_2=205 (f6), b_3=472 (f7 sole-survivor), b_4=351 (f8)

**Final vetoes (Zag trainer; independently re-computed in Python,
`v2/analysis/veto_evidence.py`, exact match):**

| Head | V1 theater | V2 meanConfCorrect | V3 slots | Verdict |
|---|---|---|---|---|
| A | 160 (all wrong→wrong rising; 0 correct→wrong) | 0.8666 ≥ 0.55 pass | 17 slots G<−0.080 (all acc=1.000) | **VOID** |
| B | 175 (all wrong→wrong rising; 0 correct→wrong) | 0.9344 ≥ 0.55 pass | 9 slots G<−0.080 (all acc=1.000) | **VOID** |

**Δ grid:** Δ=0…300 all V3-rejected (fitted underconfidence persists);
Δ=350…500 V3-pass with strictly rising score → **Δ\*=500 (max)**,
score=3,880,000 = 3880×1000 — i.e. C≡1000 on every training cell
(the grid escapes the V3 veto by saturating to the clamp attractor).
Final shifted biases: a_0=972, b_0=904.

**Liveness:** veto_rate_training_final = **0/4222** — min(A,B) never fires
below max−50; the disjoint veto is decorative even on training.

**Checkpoint (§5):** weights≠init ✓, but headA VOID and headB VOID →
the DISMIN intervention (min of two *fitted*, veto-passing heads) cannot be
honestly instantiated. **Fork VOID. No 37-leg eval.**

## Why it died (mechanistic account)

The unconstrained squared-error optimum on this data *is* a veto-violator;
the vetoes caught exactly what they were built to catch:

1. **Theater via depth/consumed crutches.** Σ(C−Y)² rewards pushing correct
   cells to 1000. Features f2 (=t·1000/64, depth) and f5 (consumed/ne) grow
   along *every* path, correct or not. Coordinate descent leaned on them
   (a_2=453, b_1=336): on wrong→wrong chains confidence *rises* with depth —
   160/175 V2-subtype theater violations. The objective never penalizes
   this; the veto does.
2. **Underconfidence on easy slots.** The linear head compromises between
   easy and hard cells; on slots with acc=1.000 (admit/logic/revoke/cost d1,
   O family) mean conf sits 0.62–0.92 → G∈[−0.38,−0.08] → 17/9 V3
   violations. Squared error underfits the easy manifold.
3. **The Δ stage degenerates to the clamp attractor.** Gated only by V3,
   the grid maximizes the B4 score by driving Δ to the 500 cap: C≡1000
   everywhere, G=1−acc≥0, veto_rate=0. Failure mode **(1) clamp attractors**
   — produced by the repair stage itself, not the heads.

Note on falsification condition (c): A does lean hardest on f1 (472) and B
has b_1=336 on f5, but (c) requires eval-manifold f1≈f5 correlation and the
(a)/(b)/(c) conditions presuppose a live fork — they do not apply to a
checkpoint VOID (v1 precedent).

## Consequences for the round

1. **The vetoes work as final-answer gates; the objective fights them.**
   TRAIN-COORD v2 is satisfiable as an optimizer (it moves, it minimizes)
   but its unconstrained optimum violates V1+V3 on this data — for the
   disjoint two-head form. The vetoes are not decorative: they reject the
   theater/underconfidence the squared-error objective actively produces.
2. **Independent confirmation of the F26 pattern.** Per parent-orchestrator
   information (not my measurement): F26 EFFIC under v2 VOIDed identically
   — fitted head live, final answer violated V1 (theater) and V3
   (underconfidence floor) — and its base control violated identically.
   My F25 v2 run reached the same conclusion independently under the frozen
   spec: the unconstrained squared-error optimum violates the vetoes with
   or without the disjoint-head structure, with or without new features.
   The defect is in the objective↔veto pairing, not in any fork's mechanism.
3. **No kill-bar table**: nothing was evaluated (VOID short-circuits before
   eval). **No failure-mode number**: VOID ≠ KILLED (§10; v1 precedent).
   **No NEC-m9 deltas / per-head-vs-min B8**: moot without a live fork
   (NEC m9 baseline archived in `v2/analysis/nec_m9_baseline.txt` for the
   round). The fork's *mechanism* (disjoint min ensemble) remains untested —
   this verdict is about the trainer objective, not the mechanism.

## Artifacts (`f25_dismin/v2/`)

- `PROTOCOL.md` — inits + protocol (pre-training; committed `0db96133`
  before first run)
- `src/train_dismin2.zag` — v2 trainer (built ×2, byte-identical)
- `src/` — 7 frozen harness modules, SHA-verified byte-identical copies
- `params/f25_params.zag` — final shifted params (SHA `b931de03…41c6411e`;
  includes fit biases, Δ\*=500, void-count=2)
- `logs/train_dismin2_run1.tsv`, `run2.tsv` — byte-identical training logs
  (198 accepted strict-L-reduction steps; veto stats logged, not gating)
- `logs/train_cells_run1.tsv`, `run2.tsv` — byte-identical training-cells
  dumps (final heads)
- `analysis/veto_evidence.py` — independent Python re-computation of the
  final vetoes (exact match with the Zag trainer)
- `analysis/nec_m9_baseline.txt` — NEC m9 37-leg analyzer output (round CTL)
- `work/` — build binaries + run2 params (NOT committed)

## Notes

- Build warnings: 9× E0101 "adding 0 has no effect" (analyzer noise on
  index expressions) — benign, build clean otherwise (same class as v1's 6).
- `/tmp` on this VM is a shared tmpfs; all durable artifacts live in the
  fork dir. Binaries kept out of commits (per AGENTS.md).
