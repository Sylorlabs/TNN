# F37 IFP — Pre-run record (FROZEN before first build/run)

Date: 2026-09-25 (corrected from 2026-09-24 — clerical date fix applied
2026-09-25 before any build or training run; the record was authored
2026-09-25 and predates all F37 builds/runs). Authority: PREREG_FORKROUND.md §3 (F37) +
`ideas/grok_forks.md` Fork 6 (authoritative on mechanism detail).

## Mechanism (verbatim from ideas file, with disambiguations recorded)

**Features** (excluding f2, f7): f1, f5, f6, max(f4,0), my — each in
thousandths. Integer weights w1..w5, bias b, **init 0**.
Linear score **s = b + ⌊Σ w_i·f_i / 1000⌋** (⌊·⌋ = mathematical floor;
explicit floor-division helper, independent of codegen div semantics).

**Marginal yield my** (RSW/MEY definition): at depth value 1, my = f5;
at later depths, my = min(1000, max(0, f5−f5_prev)·1000 / max(Δf2,1)),
Δf2 = (d − d_prev)·1000/64 with d, d_prev the depth VALUES
(1,2,4,8,16,32,64). f5_prev = same item's f5 at previous ladder depth.

**Pseudocounts (schedule):**
- Global (A,B) = (1,2); per-depth-stratum (A_d,B_d) = (1,2) for
  d_idx = log2(d) ∈ {0..6}. Invariant 1 ≤ A ≤ B−1 maintained.
- Per released training cell at stratum d: B_d ← B_d+1; if y=1 then
  A_d ← A_d+1. Global (A,B) updated identically (B++; A++ iff y=1) but
  is NOT used in emit (emit uses per-depth). No other schedule.
- Emit: **C = (A_d + max(s,0))·1000 / (B_d + |s| + max(−s,0) + 1)**,
  integer division. Note (recorded, not repaired): for extreme negative
  s this can reach 0 and for extreme positive s up to 999; the
  [1,998] claim in the ideas file is approximate. The falsifier's edge
  bands [1,20]∪[980,999] are the honest check.

**Update (released items only, file order, deterministic):**
1. Counts as above.
2. Weight step with MANDATORY decay, rate 1/(1000+t), t = # released
   updates so far (0-based; first update uses divisor 1000):
   w_i ← w_i − ⌊w_i/(1000+t)⌋ + ⌊(1000y − C)·f_i / (1000·(1000+t))⌋,
   b same with f=1000. Decay runs EVERY released update, including when
   the error term is 0. All ⌊·⌋ are mathematical floor (explicit helper).
3. Outward-clamp freeze: if (C ≥ 980 and y=1) or (C ≤ 20 and y=0),
   skip the error term (decay only). C = emitted (post-flip) confidence.
4. Monotone depth coupling: μ_d = A_d·1000/B_d (integer). If d_idx > 0
   and μ_d > μ_{d−1} + 20 and NOT (n_my[d]>0 and n_my[d−1]>0 and
   mean_my_d > mean_my_{d−1}), then while μ_d > μ_{d−1}+20: B_d ← B_d+1
   (structural drag, one unit per iteration). mean_my includes the
   current cell; my sums updated on released cells alongside counts.

**Theater flip rule** (same as MEY): let (f3p, f8p, Cp) be the previous
ladder depth's f3, f8, emitted C for the same item. If
(f3 == 1000 and f3p == 0) [f3 latched this step] or (f8 > f8p)
[trauma increase], then C ← min(C, Cp−1). Applied in train AND eval
emits (it is part of emit; the training error term uses post-flip C).
No general ratchet.

**Training stream:** `training/features/features.tsv`
(SHA256 4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d,
verified before run), file order, 3 full passes. Cells used: rel4=1
(released) AND heldout=0 only → 4222 cells/pass → 3×4222 = **12666
released updates** (≥ 10^4 as the falsifier requires). Per-item prev
state (f5/f8/f3/C/d) reset on item-id change; file verified grouped
(1000 items, depths strictly ascending, 0 violations).

**Falsifier (fixed-point, per prereg §3):**
- (i) max_i|w_i| growing linearly with t after 10^4 updates → KILL
  (decay failed to contract).
- (ii) > 5% of training emits (post-flip C) in [1,20]∪[980,999] → KILL
  (interior guarantee leaks).
- A pure bar failure with weights converged and edge-mass ≈ 0 does NOT
  kill (control semantics: expected B2/B3 fail via margin-driven
  G-rises; report as control outcome).

**Eval:** params frozen (w1..w5, b, A_d/B_d ×7). Policy binary
`<polbin> <items> <depth> <gate=0> <out.tsv>`; per item runs the FROZEN
harness at ladder depths 1,2,4,…,d, computes the C sequence with the
flip rule, emits the depth-d row. M4 release skeleton (release iff
L_t == L_1) — head never touches release. A/B byte-identical
builds+runs. mech=37.

## Analytical notes (recorded, not acted on)

- The error term ⌊(1000y−C)·f_i/(1000·(1000+t))⌋ is ∈ {+1,0} for y=1
  (only +1 at t=0) and ∈ {−1,0} for y=0 whenever C·f_i>0, for ALL t≥0
  (floor of a negative fraction in (−1,0) is −1). Decay cancels the −1
  for w_i ≤ −1, so weights equilibrate in {−1,0,+1}; s ∈ [−6,6]; the
  head is essentially the per-depth released base rate μ_d with tiny
  score perturbations. This is the literal spec; the falsifier judges
  whether the dynamics contract (they should: weights bounded).
- Consequence: B5 (separation ≥ 0.20) is expected to FAIL since C ≈ μ_d
  is near-constant within a stratum; B2 expected FAIL via margin-driven
  V2 (grok's prediction); B3 expected 4–8 violations (not better than
  NEC). These are the control's PREDICTED outcomes, not surprises.
