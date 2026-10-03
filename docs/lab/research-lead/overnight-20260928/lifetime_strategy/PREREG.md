# LM4 PREREGISTRATION — Strategy-Level Meta-Learning

**Lane:** `docs/lab/research-lead/overnight-20260928/lifetime_strategy/`
**Date:** 2026-10-03
**Status:** FROZEN (commit precedes implementation)

## Background

LIFETIME-METALEARN-3 (LM3) verdict: **RETENTION WITHOUT META-LEARNING**.
- B5d META-LEARNING: FAIL (err(E03)−err(E12) = −7 < 8).
- Key finding: "The associative prior helps base rates but within-episode learning washes out cross-episode gains. A genuine meta-learning demonstration likely needs a different operationalization (e.g., strategy-level, not base-rate)."

## Research Question

Can TNN acquire **better learning strategies** over time (strategy-level meta-learning), distinct from base-rate improvements?

**Strategy-level vs base-rate:**
- Base-rate (LM3): Does the learner's prior improve? Measured via error reduction.
- Strategy-level (LM4): Does the learner's *contradiction-management policy* improve? Measured via policy-selection accuracy and regret vs a shadow oracle.

## Design

**World:** 36 episodes, 13 switch episodes (6 fork + 7 revision), 13 dedicated probes, 10 stable.
- Switch at trial 96/160.
- **Fork:** 12–14/16 (or 3/4) answers change; old mapping probed later → SPLIT is right.
- **Revision:** 2–4/16 (or 1/4) change; new mapping probed → OVERWRITE is right.

**Strategy = contradiction-management policy.** At the first post-switch contradiction, the learner freezes slots for a 4-trial watch. At watch end:
- ctx = HIGH if ≥2 contradictions in watch, else LOW.
- Action: SPLIT (new regime) or OVERWRITE (update in place).

**Conditions:**
- **T-POLICY (cond 0):** Continuing learner + contextual bandit. Bandit selects SPLIT vs OVERWRITE per ctx (4 arms: qval[ctx*2+act]). Epsilon-greedy (10%), optimistic init (0).
- **T-FIXED (cond 1):** Continuing learner, fixed always-SPLIT (LM3-native). Identical base machinery including prior; only the policy-selection code path differs.
- **R (cond 2):** Reset per episode (control). Fixed SPLIT.

**Shadow oracle (pure measurement):** For each switch episode, copy learner state, run each candidate action (SPLIT, OVERWRITE) through episode+probe, take min combined cost (post_err + probe_err). Learner never sees it. Regret = actual_combined − oracle_min.

**T-POLICY vs T-FIXED ablation:** Identical base machinery (slots, prior, regimes, watch). Only difference is the policy-selection code path. This isolates strategy-level from base-rate.

## Frozen Kill Bars

**B4 (Apparatus validity):**
- All switch diffs in range: forks 12–14/16 (or 3/4), revs 2–4/16 (or 1/4).
- All 36 streams pairwise distinct (same-length).
- B4=1 required.

**B5a (Strategy learning):**
- regret = combined − oracle_min, summed over switch episodes.
- first6 = sum over first 6 switches (E02,E04,E07,E10,E13,E15).
- last6 = sum over last 6 switches (E20,E24,E26,E28,E30,E34).
- **PASS if:** last6 ≤ 12 AND last6 < first6.
- Rationale: Bandit must achieve near-oracle performance (≤2/ep mean) AND show strict improvement (learning, not luck).

**B5b (Beats fixed policy):**
- total_combined(T-POLICY) ≤ total_combined(T-FIXED) − 10.
- Rationale: Strategy learning must beat the fixed LM3-native policy by a clear margin.

**B5c (R control):**
- R regret(last6) ≤ R regret(first6) + 6.
- Rationale: Reset learner shows no improvement (no lifetime → no meta-learning).

**B5d (Retention sanity):**
- Fork probes (E14,E21,E27,E31) acc ≥85 each.
- Revision probes (E05,E11,E16,E19,E25,E29,E35) mean ≥80.
- Rationale: Strategy learning must not destroy retention.

**B5e (Apparatus + T-FIXED sanity):**
- T-FIXED fork probes (E03,E08,E14,E21,E27,E31) acc ≥85 each.
- Zero evictions, zero genfail, nslots ≤1024, npart ≤48 (all conds).
- Rationale: Base machinery works; T-FIXED is a valid baseline.

**B6 (No researcher meta-rule):**
- The policy menu (SPLIT vs OVERWRITE) is researcher-enumerated, but SELECTION is learner-owned (bandit qval in learner state, updated only from experienced cost).
- No researcher-written rule maps ctx→action. The bandit learns it.
- Honest framing: L1/L2 strategy *selection*, not L3 invention.

**B7 (Opaque ids):**
- Families use opaque instance numbers. No semantic labels in learner.

## Implementation

- Pure Zag, safebin mandatory (`PATH="$HOME/safebin"`, python3 unresolvable).
- 3/3 byte-identical runs (sha256).
- Deterministic seed: 20261007.

## Commit Order

1. PREREG.md + NAMECHECK.md (this commit).
2. Implementation (lm4.zag) + 3/3 runs + REPORT.md (later commit).
