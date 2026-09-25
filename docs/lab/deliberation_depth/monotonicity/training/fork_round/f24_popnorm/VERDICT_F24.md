# VERDICT — F24 POPNORM (Population-Normalized Confidence), mech 24

- **Date:** 2026-09-25
- **Fork:** F24 POPNORM, `PREREG_FORKROUND.md` §3 + `ideas/native2_forks.md` FORK 1
- **Frozen authority:** PREREG_FORKROUND.md **FROZEN v2** (commit `3a2eef44`);
  §5b Repaired TRAIN-COORD v2. (v1: `0566cc81`.)
- **Verdict: VOID (§5)** — dead at the training checkpoint under v2 §5b:
  the final fitted head violates veto V1 (theater). Reported with evidence,
  not killed. **No eval spend** (same discipline as F25's v1 VOID and the
  F26/F27 stillborn gates: §5 VOID arms are reported, not burned on the
  37-leg battery).

## 1. v1-lock observation (no v1 training run completed)

F24 completed **no** literal-v1 training run: the v1-mode binary panicked on
a TSV parser bug before any training (no v1 params or logs exist). Per the
v2 tasking, F24 went straight to v2; the v1-lock observation is analytical:

- F25's lock proof (committed `f25_dismin/VERDICT_F25.md`, v1 VOID stands)
  applies **identically** to F24's 9 params: same shared TRAIN-COORD, same
  zero init, same |features|≤1000 bound → any single ±50 first-step candidate
  has |C|≤50 → training meanConfCorrect ≤0.05 <0.55 → the V2 veto rejects
  every first-step candidate, data-independently. F24's pre-training record
  (`TRAINING_SPEC.md` §5) contains the same proof derived independently
  before the v2 update.
- v2 §11(b) also confirms the §2 features.tsv hash typo (`…e65e897d` →
  `…e65a897d`); the file itself was verified correct (byte-identical to the
  frozen commit blob; SHA `4682190c…e65a897d`).

## 2. v2 training outcome

**Implementation** (`src/train_f24.zag`, pure Zag, zero RNG, pinned
toolchain `znc_linux_x86_64_abed8aa1` only; frozen harness modules copied
byte-identical, SHA-verified in `logs/SRC_SHA256SUM.txt`):

- TRAIN-COORD v2 exactly per §5b: strict-L acceptance only (no per-candidate
  vetoes); probe order per param **+50,−50,+8,−8,+1,−1** (first strict
  improvement accepted); fixed param order w1..w8,b; 8 sweeps max with
  early stop on a no-move sweep; init 0; boxes w_i∈[−1000,1000],
  b∈[−100000,100000]. (Scoping decision recorded in `TRAINING_SPEC.md` §13:
  the "±50, then ±8, then ±1 refine" schedule is the per-param probe order
  within each of the 8 sweeps — the only reading that keeps exactly
  "8 sweeps" with no invented per-phase budget.)
- Objective: Σ(C−1000y)² over depth-1, heldout=0, rel4=1 cells (940 cells).
- f9 = 1000·(N−R_d)/N (integer division) per (family,heldout,depth); f9=0 at
  depth 1 by construction. (Computed but unused — stage 2 never ran.)
- Final-answer vetoes V1–V3 evaluated once on the fitted head; any violation
  → VOID (stage-2 w9 grid gated on vetoes passing).

**Determinism record (§8 gates):**

| Check | Result |
|---|---|
| Trainer build ×2 (pinned znc) | byte-identical, SHA `641d0fa4a5a8fdf1a44736a8f962a94d673839d2968102458bf49d55aca4bf8b` |
| Train ×2 | params byte-identical, logs byte-identical |
| §5 liveness (weights ≠ init) | PASS — 6 of 9 params moved |

**Stage-1' sweep log** (`logs/train_v2_a.tsv` = run B byte-identical):

| sweep | objective | moved | weights (w1..w8,b) |
|---|---|---|---|
| 0 | 558,397,805 | 6 | 50,50,0,0,50,50,50,0 / 50 |
| 1 | 381,406,968 | 6 | 100,100,0,0,100,100,100,0 / 100 |
| 2 | 247,238,009 | 6 | 150,150,0,0,150,150,150,0 / 150 |
| 3 | 155,790,214 | 6 | 200,200,0,0,200,200,200,0 / 200 |
| 4 | 107,308,328 | 6 | 250,250,0,0,250,250,250,0 / 250 |
| 5 | 96,652,189 | 6 | 300,300,0,0,300,300,300,0 / 242 |
| 6 | 90,987,738 | 6 | 350,250,0,0,250,292,350,0 / 241 |
| 7 | 86,633,343 | 5 | **400,300,0,0,200,284,350,0 / 242** |

Init objective: 777,000,000. The optimizer converged to a genuine calibrated
head (depth-1 mcc = 0.866). The 8-sweep cap was reached (sweep 7 still
improving) — the head is the specified "final fitted head".

**Final-answer veto evidence** (Zag trainer; independently cross-validated
cell-for-cell in Python — exact agreement):

| Veto | Result | Evidence |
|---|---|---|
| V1 (theater = 0) | **FAIL** | 175 events (0 V1-type, 175 V2-type: 0→0 with strictly rising conf) over 3,282 training adjacent-depth pairs |
| V2 (mcc ≥ 0.55) | pass | 672,620/777 = 0.866 |
| V3 (G ≥ −0.080, n_rel ≥ 8) | **FAIL** | 18 (family,depth) slots below floor (admit, revoke, logic, cost, O) |

→ **VOID** per v2 §5b ("a final fitted head violating any veto is VOID").
Stage-2 w9 grid did not run (correctly gated); no policy binary was built;
no eval legs were spent.

## 3. Structural finding (for the round, not just F24)

v2 repaired the *optimization* (L now minimizable from zero init), but the
**final-answer veto set is unsatisfiable for any non-degenerate head** on
these features:

- A coarse independent search (166 candidate heads, all three vetoes
  evaluated exactly): **4/166 pass, and all four are ≈constant-1000 clamp
  attractors** (e.g. W=[800,0,0,0,0,0,0,0],b=900; constant b=1000) with
  L≈157–163M — nearly 2× the fitted head's 86.6M. The v2 optimizer would
  never select them.
- Mechanism: any head that actually fits calibration leans on f1/f2/f5, and
  those features *rise with depth on wrong→wrong pairs* (f1: 125/179,
  f2: 177/179, f5: 177/179) — so calibration-fitting implies theater, which
  V1 forbids. V3's per-group floor (G≥−0.080) additionally punishes the
  pooled-fit compromise. The vetoes' evident intent (§5b: "reject degenerate
  solutions — theater, clamp attractors, blanket underconfidence") is
  self-defeating as a set: the only heads satisfying all three vetoes ARE
  the clamp attractor (constant conf≈1000: theater-free, mcc≈1, never
  underconfident).
- The POPNORM mechanism itself (stage-2 f9 debias) was never tested — the
  fork died at the trainer gate, like F25's v1 VOID. This is a property of
  the round's veto design, not evidence about population normalization.

**Proposed §7 taxonomy entry (9): final-veto unsatisfiability** — the
V1+V2+V3 final-answer vetoes jointly admit only degenerate clamp-attractors
while rejecting every calibration-fitting head (theater is inherent to
fitting on features that rise with depth on wrong items).

## 4. Kill bars / §10 adjudication

| Bar | Result |
|---|---|
| B1–B9, B13 (37-leg eval) | **not run** — VOID at §5 checkpoint; no eval spend per §5 |
| Kill (a)/(b)/(c) | not applicable (no base/F24 eval pair) |
| **§10 verdict** | **VOID (§5)** |
| Failure-mode number | **(9)** proposed: final-veto unsatisfiability (nearest carried: (2) crutch collapse — the fitted head leans on the f1/f2/f5 crutch, hence the theater) |

## 5. Files & provenance

- Workdir: `deliberation_depth/monotonicity/training/fork_round/f24_popnorm/`
- `TRAINING_SPEC.md` — full pre-training record + v2 amendment (§13)
- `src/train_f24.zag` — v2 trainer; `src/*.zag` — frozen harness copies
  (SHA-verified, `logs/SRC_SHA256SUM.txt`)
- `logs/train_v2_{a,b}.tsv` — byte-identical training logs (sweeps + veto evidence)
- `params/f24_v2_{a,b}.zag` — byte-identical fitted params (evidence)
- Binaries and `.zagd` caches: NOT committed (build/ only).
- Frozen inputs: features.tsv SHA `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
  (v2 §2 typo fixed); prereg v2 commit `3a2eef44`.

**Bottom line:** F24 trained cleanly under repaired TRAIN-COORD v2
(deterministic, byte-identical, weights moved, L 777M→86.6M, mcc 0.866) and
was VOIDed by the §5b final-answer vetoes: 175 theater events (V1) and 18
V3 floor violations. The veto set, not the POPNORM mechanism, is what failed
— it admits only clamp-attractor degenerates. No eval was spent.
