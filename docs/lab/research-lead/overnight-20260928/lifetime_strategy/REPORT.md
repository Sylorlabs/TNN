# LM4 REPORT — Strategy-Level Meta-Learning

**Date:** 2026-10-03
**Verdict:** **STRATEGY-LEVEL META-LEARNING DEMONSTRATED** (all frozen bars PASS)
**Lane:** `docs/lab/research-lead/overnight-20260928/lifetime_strategy/`

## Summary

LM3 found **RETENTION WITHOUT META-LEARNING**: the associative prior helps base rates, but within-episode learning washes out cross-episode gains (B5d FAIL: err(E03)−err(E12) = −7 < 8).

LM4 operationalizes meta-learning at the **strategy level**: does the learner acquire better *contradiction-management policies* over time? **Yes.**

- **B5a (Strategy learning):** Regret vs shadow oracle 14 → 3 (first6 → last6). PASS.
- **B5b (Beats fixed):** T-POLICY total 149 vs T-FIXED 179 (30pt gap). PASS.
- **B5c (R control):** R regret flat (0 → 0). PASS.
- **B5d (Retention):** Fork probes 100%, rev mean 85.7%. PASS.
- **B5e (Apparatus):** T-FIXED forks 100%, zero evictions. PASS.
- **B4:** All diffs in range, streams distinct. PASS.

3/3 byte-identical runs. SHA256: `38b6535173e4c1721625da9125a1685273808d241d80115eec506a8b0d1ce28c`

## Design

**Strategy = contradiction-management policy.** On switch episodes (trial 96/160):
- **Fork** (12–14/16 answers change): old mapping probed later → SPLIT (new regime) is right.
- **Revision** (2–4/16 change): new mapping probed → OVERWRITE (update in place) is right.

**Contextual bandit:** At first post-switch contradiction, freeze slots for 4-trial watch. ctx=HIGH if ≥2 contradictions else LOW. Bandit chooses SPLIT vs OVERWRITE per ctx (4 arms, epsilon-greedy 10%, optimistic init).

**T-POLICY vs T-FIXED ablation:** Identical base machinery (slots, prior, regimes, watch). Only the policy-selection code path differs. This isolates strategy-level from base-rate.

**Shadow oracle:** Counterfactual. Copy learner state, run each action through episode+probe, take min combined cost. Pure measurement; learner never sees it.

## Results

### B5a: Regret improves 14 → 3
The bandit learns. Early episodes include exploration and mistakes (E04: chose SPLIT on LOW ctx, regret 9). By E15, it chooses correctly (OVERWRITE on LOW, regret 0). Final performance: 3/6 = 0.5 regret/ep (near-oracle).

### B5b: T-POLICY beats T-FIXED by 30
T-POLICY (149) vs T-FIXED always-SPLIT (179). The 30-point gap comes from correctly choosing OVERWRITE on revisions (saving ~9/ep) while matching SPLIT on forks.

### B5c: R shows no improvement
R (reset per episode) regret flat at 0. No lifetime → no meta-learning. Control passes.

### B5d: Retention preserved
Fork probes: 100% (E14,E21,E27,E31). Revision probes: 100,100,100,100,100,0,100 (mean 85.7%). E29 (c2r) failed due to false-HIGH ctx leading to mistaken SPLIT + orientation tie-break. Single outlier; bar passes with margin (600 ≥ 560).

### Key distinction from LM3
LM3 measured **base-rate** meta-learning (does the prior improve?). It failed because within-episode learning washes out cross-episode gains.

LM4 measures **strategy-level** meta-learning (does the policy improve?). It succeeds because the policy (ctx→action mapping) is a compact, reusable structure that accumulates value across episodes, unlike the prior which gets overwritten by within-episode learning.

## Honest framing (B6)

The policy menu (SPLIT vs OVERWRITE) is researcher-enumerated. The **selection** is learner-owned (bandit qval in learner state, updated only from experienced cost). This is **L1/L2 strategy selection**, not L3 invention. The bandit does not invent new policies; it learns which of the given policies works in which context.

## Files
- `lm4.zag`: Implementation (pure Zag, ~930 lines).
- `output.txt`: Full 3/3 output (byte-identical).
- `PREREG.md`: Frozen preregistration (committed before implementation).
- `NAMECHECK.md`: Toolchain guard verification.

## Reproduction
```bash
export PATH="$HOME/safebin"
znc lm4.zag -o lm4_bin
./lm4_bin > out.txt
sha256sum out.txt  # must equal 38b6535173e4c1721625da9125a1685273808d241d80115eec506a8b0d1ce28c
```
