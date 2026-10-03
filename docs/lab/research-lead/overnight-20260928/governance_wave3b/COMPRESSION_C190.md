# Architecture Compression Analysis: C190-C196
## Constitution Section 4 metrics, constitution wave part 2 (2026-10-01/02)

### Step 0
Toolchain guard active (safebin, no python3/python). Governance only. Pure shell/git.

### Compression table

| Claim | Lines added | M/B/H/S | Researcher-owned structural | Learner-owned structural | Capability gained |
|---|---|---|---|---|---|
| C190 prediction-optional | ~470 (po_full.zag) | 0/0/0/0 | 4: 7-type taxonomy, dispatch order, DER rule, K=6 threshold | 3: per-query branch choices, T_PROC records, constructed MAP | process selection baseline; 86% prediction waste measured |
| C191 knowledge-composition | 0 (driver only) | 0/0/0/0 | 0 new mechanism | 0 | NEGATIVE: composition architecturally absent (evidence, not mechanism) |
| C192 learning-to-learn | ~5 (instrumentation; mechanism verbatim C186) | 0/0/0/0 | 0 new mechanism | 2: LINK ordering strategy, per-problem verify counts | 6x Family-2 cost reduction; strategy proven causal by ablation |
| C193 scaling-index | ~150 (si_patch.zag) | 0/0/0/0 | 2: 4 plen buckets, bucket key choice | 1: index contents (learner-maintained on promotion) | sublinear MAP retrieval; 140x scan reduction at 100 MAPs |
| C194 integration-rsv | ~280 (rsv_patch.zag) | 0/0/0/0 | 2: thresholds, decision structure | 3: reliability values, trust judgments, coexistence records | 6th substrate behavior; 3/3 vs 2/3 synergy; DELETED C183 private store |
| C195 p1-withholding | ~296 (wh_patch + wh_predsec) | 0/0/0/0 | 4: WT init (3), +1/-1 rule, clamp, decision structure | 3: WT values, per-query withhold/guess, withhold timing | adaptive withhold boundary; wins on regime change |

M/B/H/S = modes / bridges / handlers / semantic cases added.
C196 (hypothesis frontier) is governance docs, not a mechanism; excluded from line counts.

### Totals

- Cognition lines added (C190-C195): ~1201
- Modes/bridges/handlers/semantic cases: 0 across all 6 (One-System Rule holding)
- Distinct capabilities: 5 mechanisms + 1 negative result + 1 governance
- Lines per capability: ~240
- Net architecture change: C194 DELETED one subsystem (C183 private rel store). First net-negative integration.

### Compression trajectory

C181-C189: +2008 lines, 0 deletions.
C190-C195: +1201 lines, 1 subsystem deleted (C194).
Cumulative: +3209 lines, 1 deletion.

The deletion in C194 is the pattern Micah Section 4 rewards: integration should remove duplicated machinery. The governance_wave3 compression analysis predicted ~400+ lines of parallel scoring machinery could merge into the substrate; C194 executed the first ~150 of those lines (C183 private store removal). Remaining parallel scoring: C181 PRED nodes (tag-31), C187 U field, C182 error score E.

### Composition verdict (Micah Section 2 question: which hypothesis A/B/C won?)

None. The three composition hypotheses (A: goal-conditioned graph composition, B: fragment composition via connection history, C: constraint-driven assembly) were NOT tested because the Wave 3 composition builders were not yet spawned at time of writing. C191 is a pre-hypothesis negative: it proves the current architecture cannot compose at all (trial never uses MAPs; rebind is whole-shape only). The A/B/C experiments remain the top priority for the next wave. The negative result sharpens them: any composition mechanism must bridge the trial/MAP divide, not merely improve rebind.

### Learner-authority note

C190-C195 continue the standing pattern: learner-owned VALUES inside researcher-defined slots (reliability scores, WT values, index contents, LINK ordering). C191's negative is the sharpest SUF statement yet: 0 learner-owned structural decisions because the architecture lacks the structural vocabulary for composition entirely. The "learner creates slot" gap (H-SLOT-1) is now the single sharpest frontier item.

### Verdict
GOVERNANCE-WAVE3-COMPRESSION-COMPLETE.

No em dashes used (verified).
