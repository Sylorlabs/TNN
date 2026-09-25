# F21 GRAF — Frozen Hyperparameters

Frozen 2026-09-24, BEFORE the first training run. Per PREREG_FORKROUND.md §3 (F21)
+ ideas/native1_forks.md Fork 2 (authoritative on discrepancy).

- **λ = 1** (per-cell calibration weight)
- **μ = 4** (soft per-item theater penalty weight; matches v2's theater
  coefficient of 4 in its symmetric loss)

Weight init (fixed, recorded): w1=1000, w2..w8=0, b=0
(M4-harness-confidence start; identical to v2's init. Neutral: the GRAF
intervention is the objective, not the init.)

Objective (all fixed-point integer, i64):
  L = Σ_{rungs} n_r·G(r)² + λ·Σ_{cells}(c−y)² + μ·Σ_{items}Σ_{d} max(0, c_{d+1}−c_d)
  G(r) = trunc(1000·Σ_{rel@r}(c−y)/n_r), y ∈ {0,1000}
  rungs = (family × depth) over released training cells (heldout=0, rel4=1);
  μ-term adjacency = consecutive released training cells of the same item
  in ascending depth order.

Optimizer: deterministic integer coordinate descent on the 9-parameter
lattice (w1..w8, b; thousandths). Sweep order: w1,w2,...,w8,b. Per param,
try +step then −step; accept the FIRST strict L decrease; move on.
Step phases: ±8 to full-sweep convergence, then ±1 refine to full-sweep
convergence. No RNG, no restarts, single deterministic run (run twice for
byte-identical params per §8).
