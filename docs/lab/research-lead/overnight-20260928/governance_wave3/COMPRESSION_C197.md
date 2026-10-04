# Architecture Compression Analysis: C197-C200
## Constitution Section 4 metrics, constitution wave part 3 (2026-10-02)

### Step 0
Toolchain guard active (safebin, no python3/python). Governance only. Pure shell/git.

### Compression table

| Claim | Lines added | M/B/H/S | Researcher-owned structural | Learner-owned structural | Capability gained |
|---|---|---|---|---|---|
| C197 unlabeled-selection | ~600 | 0/0/0/0 | 4: op definitions, preconditions, DER rules, tie-break | 3: consequence records, per-goal selections, MAP promotions | operation selection without researcher taxonomy; 19/19 |
| C198 strong-l2l | ~113 (mech; +121 driver) | 0/0/0/0 | 3: E update rule, T formula, arm design | 3: T/E values, write timing, threshold trajectory | cross-regime meta-transfer; 11 vs 26 revs |
| C199 composition-C | ~250 | 0/0/0/0 | 3: search bias, config, driver world | 4: relseq values, candidate choices, segment MAPs, Z graph | X+Y->Z via constraint-driven assembly (first positive composition) |
| C200 substrate-selection | ~431 | 0/0/0/0 | 5: signature bits, score formula, default order, curriculum, cost scale | 2: success records, per-situation selections | 7th substrate behavior (operation selection); 7/7 vs 3/7 |

M/B/H/S = modes / bridges / handlers / semantic cases added.

### Totals

- Cognition lines added (C197-C200): ~1394
- Modes/bridges/handlers/semantic cases: 0 across all 4 (One-System Rule holding)
- Distinct capabilities: 4 mechanisms
- Lines per capability: ~349

### Cumulative trajectory

- C181-C189: +2008 lines, 0 deletions
- C190-C195: +1201 lines, 1 subsystem deleted (C194 removed C183 private store)
- C197-C200: +1394 lines, 0 deletions
- Cumulative: +4603 lines, 1 deletion

### Key compression-relevant findings

1. **C199 resolves the composition question.** C191 proved TNN-2 cannot compose (0 learner-owned structural decisions; architecture lacks the vocabulary). C199 Hypothesis C (constraint-driven assembly) is the first positive: X+Y->Z with no paired examples, ~250 lines, 0 new architectural constructs. The trial/MAP divide is bridged by structural property extraction from executable graphs, not by a new engine.

2. **C200 is the 7th substrate behavior.** The shared tag-61 consequence store now drives: policy, withholding, abandonment, retention, search-order (C185), verification (C194), and operation selection (C200). Seven behaviors, one store, zero new modes/bridges. This is the One-System Rule working as intended.

3. **C197 removes a researcher taxonomy.** C190 measured 86% prediction waste with a 7-type researcher-authored process taxonomy. C197 deletes the taxonomy: goals are (s,r) only, selection is from learned consequence history. The ~600 lines are mostly op definitions and preconditions (researcher machinery), but the SELECTION is learner-owned. Next compression: can the op definitions themselves be learner-constructed?

4. **C198 is meta-transfer, not more facts.** The learned caution parameter T transfers across structurally different evidential regimes (11 vs 26 revs, 0 burst-traps). This is Constitution Section 16 (learning to learn) with the sharpest evidence yet: the advantage is in the meta-parameter, ablation proves causality.

### Remaining parallel machinery (updated)

C194 deleted the C183 private reliability store (~150 lines). Still parallel:
- C181 PRED nodes (tag-31) for prediction reliability
- C187 U field (+-1) for predictive utility
- C182 error score E for threshold adaptation
- C197 consequence records (tag-61 op,sig) for operation selection
- C200 signature-based scores for substrate selection

C197 and C200 both use consequence history for selection; C200 explicitly builds on the substrate. The next deletion candidate: merge C197's op-selection records into C200's substrate-selection machinery (both select operations from consequence history; C197 has no taxonomy, C200 has signature bits).

### Verdict
GOVERNANCE-COMPRESSION-C197-COMPLETE.

No em dashes used (verified).
