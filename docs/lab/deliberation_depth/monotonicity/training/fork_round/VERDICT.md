# H5 Fork Round — VERDICT.md

**Round:** 19 forks (F20–F37 + F25v1) · short battery (37 legs) · frozen prereg `PREREG_FORKROUND.md`
**Date:** 2026-09-25 · **Status:** SHORT BATTERY COMPLETE — all forks resolved
**Authority:** prereg v2 (`3a2eef44`) — see §7 governance notes

## 1. Final tally

| Verdict | Forks | Count |
|---|---|---|
| **PARTIAL** | F22 (oracle bound; foreshadow untested — see §3) | 1 |
| **KILLED** | F20, F21, F23, F28, F31, F32, F33, F34, F35, F36, F37 | 11 |
| **VOID** | F24, F25 v1, F25 v2, F26, F30 | 5 |
| **STILLBORN** | F27, F29 | 2 |

**No fork produced a genuine mechanism that clears the short battery.**
F22 is the sole PARTIAL, but it is an oracle-conditioning bound, not a mechanism (§3).
No fork advances to §6 long-horizon (none clears B1–B9+B13 strictly).

## 2. What the round established

### 2a. Selection (FM6) is the load-bearing failure mode
- **F37 (control):** head decayed to w=0 (pure stratum base rates, zero dynamics),
  fixed-point conditions held — B2/B3 *still* failed. FM6 is **sufficient** for
  overconfidence independent of dynamics. Fixing dynamics is necessary but not sufficient.
- **F31:** empirical ledger corrections don't transfer (training G≤0.115, deployment G~100× larger).
- **F36:** "causal" ledger reduced to miscalibrated static ρ lookup; path rule decorative.
- **F34:** zero taxes can't address selection enrichment.

### 2b. Conditioning works iff it is oracle-grade
- **F22:** 29 per-(family,depth) linear calibrators → B3=0 honest, B2=0, B13=0.
  Strictly dominates NEC. **But:** foreshadow weights never left init (hypothesis untested);
  head selection keys on dataset identity (file paths, item-id parsing) — not deployable.
- **F35:** discovered clusters *succeeded* (MI=0.906, stable by item 768) but confidence
  on them fails (B2=85, B3=8, B13=21 — strictly worse than NEC).
- **Measured gap:** oracle conditioning (F22) vs discovered conditioning (F35) is large.
  Discovery finds structure but lacks per-depth granularity and introduces non-monotonicity.

### 2c. Capacity, not mechanism (FM9 sharpened)
- **F21:** one global linear head cannot jointly calibrate all family×depth rungs (V2=181, B3=15).
- **F22:** 29 rung-specific heads can. FM9 is now a clean capacity claim: 1 fails / 29 succeed.
- **F23:** absolute f1 margin is load-bearing — self-normalization destroys it (f1'≡1000, conf≡1000).

### 2d. Trainer/veto structural incompatibility (F24/F25/F26/F30)
- Squared-error objective + final V1/V3 vetoes are **unsatisfiable** on the frozen manifold:
  unconstrained optimum has V1=175, V3=7–18 (base control fails identically).
- TRAIN-COORD v1 was analytically locked (init 0 + ±50 moves → conf≤0.05, veto rejects all).
- v2 repair works as optimizer but both heads VOID on final vetoes.
- **F30:** G-penalty collapsed predictor (P≡0) before adversarial censor saw any signal —
  the two THAC components are mutually incompatible under the frozen curriculum.

### 2e. New failure modes discovered
| # | Name | Fork | Mechanism |
|---|---|---|---|
| — | **Relief theater** | F33 | Non-monotone trauma penalty: penalty decay *raises* conf on wrongs (174/174 V2 pairs) |
| 9 | **Adversarial starvation** | F30 | G-penalty destroys the overconfidence signal the adversary needs |
| — | **FM-SELFNORM-001** | F23 | Trailing-max normalization destroys absolute margin signal |

### 2f. Dead on arrival (structural)
- **F20:** w9 gradient sub-quantal under frozen integer DIV → dead feature, clamp attractor.
- **F28:** energy budget never binds (replenishment ≫ charge, ~1000× scaling error) → conf≡1000.
- **F32:** regime-switch fires but TRACK emission doesn't suppress theater; systematic ceiling/O underconfidence.
- **F27/F29:** STILLBORN — frozen inputs lack required observables (L_k leader history; binary h_i).

## 3. F22 interpretive correction (load-bearing)

F22's PARTIAL verdict stands per §10 letter (honest families clear B1–B9+B13; redteam
tiny-n residual characterized). **But it must not be read as a foreshadow validation:**

1. The foreshadow hypothesis is **untested** — w9/α/β/γ/δ never moved from init 250.
   Greedy descent saturated loss with base weights before reaching them.
2. The bars are cleared by **29 per-(family,depth) linear calibrators** (oracle conditioning).
   Independent per-rung calibration trivially flattens G — a capacity demonstration, not a mechanism.
3. Head selection keys on **dataset identity** (file-path substrings, item-id parsing),
   unavailable at deployment. Not a unified policy.

**Scientific value:** F22 is the oracle-conditioning upper bound. It sharpens FM9 and sets the
target for discovered-conditioning approaches. F35 measured the gap: discovery alone doesn't
recover the oracle.

## 4. Baseline-constant discrepancy (must resolve before citing)

F33 independently recomputed NEC m9's strict B3 via the frozen analyzer as **21**
(per-family: 1+1+4+4+2+3+2+4+0), not the **6** recorded in prereg §3 kill bars and the NEC report.
Affected comparisons: F21 (c), F28 (a), F30, F32 (3), F33 (c), F35 (3), F36 (b), F37.
**No verdict hinges on it** (all affected forks were killed/voided absolutely on other bars),
but every "(c)-bar vs NEC=6" claim in fork verdicts must be re-verified against the frozen
analyzer before the round is cited. The "6" may count a subset (e.g. honest-only) — the
counting definition needs pinning.

## 5. Failure-mode census

| Mode | Forks |
|---|---|
| FM6 selection | F31, F34, F36, F37 (isolated) |
| FM1 clamp attractors | F20, F28 (+ F33 carried) |
| FM9 capacity | F21 (1 fails), F22 (29 succeed) |
| Trainer/veto unsatisfiability | F24, F25 v1/v2, F26 |
| Relief theater (new) | F33 |
| Adversarial starvation (new) | F30 |
| Signal destruction | F23 |
| FM5-class theater | F32 |
| Missing observables | F27, F29 (stillborn) |

## 6. What this means for the H5 question

**"What fixes overconfidence with depth under strict B3?"**

The round falsified: training alone (as specified), single-head capacity, empirical ledgers,
energy budgets, trauma penalties, regime switches, marginal-yield ledgers, discovered
clustering, adversarial censors (under frozen curriculum), self-normalization.

The round established:
1. **Selection (FM6) is the core adversary** — it survives perfect dynamics (F37).
2. **Per-rung conditioning solves it** — but only at oracle grade (F22); discovery doesn't
   recover the oracle (F35).
3. **Absolute f1 margin is load-bearing** — don't normalize it away (F23).
4. **The objective and the vetoes are jointly unsatisfiable** — a veto-aware constrained
   search needs its own preregistration; do not retrofit mid-round.

The surviving hypothesis space (for a future round, not this one):
per-depth-granular *discovered* conditioning + selection-robust confidence + veto-aware training.
F22 shows the target exists; F35 shows naive discovery doesn't reach it.

## 7. Governance notes (for Micah)

1. **B8 amendment:** prereg labels the §4b replacement "coordinator-signed." Micah did **not**
   sign the exact wording. It was used as a killing bar (F28, F34). Recommend: preserve old B8
   as frozen or downgrade amended B8 to non-killing telemetry until Micah signs.
2. **TRAIN-COORD v2:** analytical defect repair (candidate vetoes → final-head-only) was
   committed as prereg v2 without Micah's explicit sign-off on the exact amendment. Reversible;
   designed to avoid leaving forks untested. Needs his word before any further amendment.
3. **F27/F29 revival** needs a signed data-regeneration amendment (log L_k; define h_i).
4. **Baseline constants** (§4) need re-verification before citation.

## 8. Commits (branch `tnn-native-lab`)

F20: `c0ec3328`, `3b68b479` · F21: `d6dfa7fb`, `7470a6a0` · F22: `05a1d503`, `e7d2d019`, `c6d8cb4f`, `310f0ec0` ·
F23: `dd7e65a8`, `7a82818d` · F24: `88475486` · F25v1: `3287813a`, `8461c659` · F25v2: `0db96133`, `b973fe6f` ·
F26: `2a5db535`, `6e5aee44` · F27: `bc7b681a` · F28: `df144676`, `56cf5c09`, `68719a04` · F29: `a450d078` ·
F30: `636bd9c3`, `95af4956` · F31: `39b77ce2`, `b046f807`, `619966d2` · F32: `f62e89c5`, `22d8517e`, `bb4b66a1` ·
F33: `d4b07253`, `bb83349f`, `55db3cb1`, `68452bba`, `660cfd69` · F34: `25018360`, `6558ba1b` ·
F35: `1fa06e4e` · F36: `f427606c`, `9db6cc6a` · F37: `54cca405`, `5c87dae9`, `3558a1ef`, `8d269f09`

All forks: pure Zag, zero RNG, pinned toolchain `abed8aa1`, A/B byte-identical builds/runs,
B9=100% release+correct identity vs M4 (5240/5240) unless noted.
