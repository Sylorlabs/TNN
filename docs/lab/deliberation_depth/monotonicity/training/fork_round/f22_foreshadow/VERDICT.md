# F22 FORESHADOW — Verdict

**Mechanism 22** · fork_round/f22_foreshadow · 2026-09-25
**§10 verdict: PARTIAL** (honest families clear B1–B9+B13; adversarial residual characterized; foreshadow-tuning caveat below)

## 1. Determinism / build gates (§8)

| Gate | Result |
|---|---|
| Pure Zag, zero RNG | ✓ (fixed file order, fixed inits, integer arithmetic; no RNG anywhere) |
| Pinned toolchain only (`znc_linux_x86_64_abed8aa1`) | ✓ |
| Trainer A/B byte-identical binaries | ✓ |
| Training ×2 → byte-identical params | ✓ (`cmp` clean on params + logs) |
| Policy A/B byte-identical binaries | ✓ |
| Eval legs A/B byte-identical | ✓ (37/37 PASS via run_eval.sh) |
| []u8 arenas + LE accessors; no zalloc; no slice > 2^25 | ✓ |
| No binaries / .zagd committed | ✓ (binaries local only, removed before handoff) |

**Trainer bug found and fixed pre-eval.** The first coordinate-descent
build had an acceptance bug: after accepting `+s` (`lcur=ln`), the
`if(ln>=lcur)` guard was true by equality, so the `-s` trial always ran
and clobbered the accepted `+s`; on revert, the phantom `lcur` (loss of
the untaken `+s`) decoupled from `p`. Symptom: `loss_final << loss_init`
while params sat exactly at inits. Fixed to try ±s, keep the
strictly-best, commit to `p`; `lcur` always equals `loss(p)` by
construction. The voided run's params were discarded (never committed).
The fixed run was independently cross-checked (Python recomputation of
admit-d1 loss = 0, matching the trainer).

## 2. Bar table (37-leg short battery, gate=0)

| # | Bar | Threshold | Result |
|---|---|---|---|
| B1 | 1→0 transitions | = 0 | **PASS** (0) |
| B2 | Theater V1=V2 | = 0 | **PASS** (V1=0, V2=0) |
| B3 | G-violations per family | = 0 every family | **0 on all honest families**; 2 on redteam (tiny-n, see below) |
| B4 | meanConfCorrect (aggregate) | ≥ 0.50 | **PASS** (0.9994) |
| B4b | Honest-family floor (n≥10) | ≥ 0.50 | **PASS** (all 1.0000; ceiling/P n=0 → n/a) |
| B5 | Separation | ≥ 0.20 | **PASS** (0.9885) |
| B6 | Recall vs M4 | ≥ 0.95 | **PASS** (1.00 everywhere; trap/ceiling-P 0/0 vacuous) |
| B7 | Abstention volume | ≤ 0.30 | **PASS** (0.1475) |
| B8 | G-definedness (amended §4b) | per §4b | **PASS** (genuine perfect calibration, \|G\|≤1e-6); VOID redteam/trap (kills nothing) |
| B9 | Release+correct identity vs M4 | 100% | **PASS** (5240/5240) |
| B12 | G>0 crossings | recorded | redteam: 3 depths (does not kill) |
| B13 | Underconfidence floor (n_rel≥8) | ≥ −0.100 | **PASS** (0 violations) |
| B3pi | Per-item B3 | recorded | 1/3467 violations (does not kill) |

**B3 detail.** The 2 redteam violations are at d4 (G +0.500, n_rel=2) and
d8 (G +1.000, n_rel=1) on a 3-item battery — FM7 tiny-n noise, not a
calibration failure. NEC m9 also shows redteam Gviol=2. All six honest
families (admit, revoke, logic, cost, ceiling D/O/P) have **zero**
G-violations at every depth, with G ≡ +0.000 throughout.

## 3. F22-specific falsification (§3 F22)

| # | Kill bar | Result |
|---|---|---|
| (a) | Any analyzer leg with n_rel ≥ 16 and V1+V2 > 0 | **NO TRIGGER** (V1=V2=0 on every leg) |
| (b) | α,β,γ,δ ≈ 0 (≤8) on majority (≥15/29) of direct fits | **NO TRIGGER** (0/29; all stayed at init 250) |
| (c) | B4 < 0.50 on any honest leg | **NO TRIGGER** (B4 = 0.9994) |

**Material caveat on (b).** The hazard weights did not "fit to ≈0" — they
never moved from inits at all. The greedy coordinate descent (preregistered
order w1..w8, b, w9, α, β, γ, δ) saturated the training loss with the base
weights alone (many legs hit loss 0) before ever reaching w9/α..δ, so the
foreshadow path was never tuned. At eval the foreshadow IS in the causal
path (w9=250, α=β=γ=δ=250, discount computed), but with default — not
fitted — hazard coefficients. The fork's success is driven by the per-leg
linear heads; the foreshadow mechanism's *specific* contribution is
unproven by this experiment. This does not trigger kill bar (b) as
operationalized (stayed-at-init ≠ fit-to-zero), but it is disclosed here
as the central interpretive caveat: F22-as-specified works, but we cannot
attribute the win to foreshadowing per se.

## 4. Deltas vs NEC m9 (CTL yardstick)

| Metric | NEC m9 | F22 | Δ |
|---|---|---|---|
| B2 theater (V2 total) | 132 | 0 | **−132 (eliminated)** |
| B3 G-violations (total) | 21 | 2 (redteam tiny-n) | **−19** |
| B4 meanConfCorrect | 0.6564 | 0.9994 | **+0.3430** |
| B13 violations | 16 | 0 | **−16** |

F22 strictly dominates the CTL yardstick on every measured bar.

## 5. §6 long-horizon

Not run. §6 admits only forks clearing B1–B9+B13 on the short battery;
F22's 2 redteam B3 violations (tiny-n) mean it does not clear strictly,
so it does not advance. No failure-mode number is assigned (no kill).

## 6. Authority resolutions (recorded)

- **Per-leg vs global params.** Task text says "ONE global param set";
  ideas/native1_forks.md Fork 3 (explicitly authoritative on
  discrepancies) says parameters are fit per-leg. Implemented per-leg
  (29 direct fits with ≥16 cells; pooled family/global fallbacks).
- **Feature SHA erratum.** Frozen prereg cites `...04e65e897d`; actual
  `features/features.tsv` SHA-256 is
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
  (one-character prereg typo; seven earlier frozen/build documents cite
  the on-disk SHA).

## 7. Commits (branch `tnn-native-lab`)

- `05a1d50393b45ef4b110e9b929a870bb357d5a75` — design + harness + trainer source (pre-training)
- `e7d2d019477928578bb41ab36fff47b54e73bf11` — trainer bugfix + valid deterministic params/logs
- `c6d8cb4fc23c6db969dd4ae7b75174e1f55322af` — policy source + canonical params copy

(Training/analysis/results/verdict commits follow incrementally.)

## 8. Files

- `src/f22_train.zag`, `src/f22_policy.zag`, `src/f22_params.zag` (canonical = `params/f22_params_A.zag`)
- `params/f22_params_A.zag`, `logs/train_A.tsv` (B copies byte-identical, local only)
- `results/` — 37 `_A.tsv` legs (B byte-identical per run_eval.sh)
- `analysis/analyze_f22.txt` (frozen analyzer), `analysis/bars_f22.py`, `analysis/bars_f22.txt`
- `DESIGN.md` (preregistration record), `VERDICT.md` (this file)
