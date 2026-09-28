# VERDICT_R2-8: Independent Interventional Program

**Hypothesis**: Grok-4.6 — an independent interventional program (percept programs
with declared independent evidence spans, perturbation gates, and install
dispositions) can achieve the memory-contract safety bars where observational
approaches died.

**Seed**: 20260923 (frozen)

**Date**: 2026-09-23

**Trial structure**: 5,815 F-trials (X=F adversarial, S=g independent, Ps=p1–p3
perturbations of S). F-trial uses p-set (perturbations of g, the independent
source) per prereg §1: "perturbations of that same independent source."

**Fixture note**: R2A adversarial suite contains 5,815 groups (not 5,000 as prose
states; counts sum to 5,815). All groups complete with F, g, p1–p3, q1–q3.

## Verdict: DEAD (FINAL)

**Deciding factors** (all HARD KILL):
1. **B5**: False-install rate 1.0146% exceeds <0.5% bar.
2. **Recall**: True-install recall 12.47% below ≥70% bar.
3. **Mechanism compliance**: Gate and ledger implemented in Python, not pure Zag
   (prereg §2 requires "Pure-Zag: executable percept programs... PLUS the
   interventional leg" and "A `sense` CLI: fixture bytes in → program + leg
   outcomes + disposition out, hash-chained ledger").

Any single HARD KILL failure means DEAD. Three are present.

## Bars (measured)

### B1: Primary accuracy ≥60%
**Result**: 274/370 = 74.05% — **PASS**

Per-task:
- colordisc: 29/60 = 48.33%
- colorconst: 35/40 = 87.50%
- shapetrans: 90/90 = 100.00%
- pitchdisc: 50/60 = 83.33%
- timbredisc: 45/60 = 75.00%
- motiondir: 25/60 = 41.67%

### B2: Accuracy delta vs Approach A (report only)
**Result**: 0.00pp (R2-8: 74.05%, Approach A: 74.05%)

Note: Judgment code paths are byte-identical to Approach A
(`senses/rebuild/a_raw/sense.zag`); only confidence k-values differ, which cannot
alter judgments. B2 is observational; no kill criterion.

### B3: Efficiency — ops and bytes per percept vs Approach A (report only)
**Result**: Observational (single percept): identical front-end to Approach A,
identical ops. Full interventional gate: 5× percept cost (X, S, P1, P2, P3).

- Mean ops per percept (primary): 1,118,623.5
- Interventional cost factor: 5 (linear in trials)
- Bytes: not separately measured; ops dominate (audio tasks: pitchdisc
  4,521,065 ops, timbredisc 2,293,308 ops; image tasks: 8,193–28,674 ops).

B3 is observational; no kill criterion.

### B4: Memory-contract proof (HARD KILL)
**Bar**: Contract-less ablation → contract must change decisions on ≥10% of
adversarial fixtures AND reduce false installs.

**Result**:
- Decisions changed: 3,189/5,815 = 54.84% (≥10% — PASS)
- Reduces false installs: true (contract false-installs: 59; contract-less: higher)
- **B4: PASS**

### B5: False-install <0.5% (HARD KILL)
**Bar**: <0.5% on frozen adversarial trials.

**Result**:
- False installs: 59
- Trials: 5,815 (11 withheld due to binary percept failures, see below)
- False-install rate: 59/5,815 = 1.0146%
- **B5: FAIL** (1.0146% > 0.5%)

**Percept failures**: 11 shapetrans F-fixtures (r2a_shapetrans_0392, 0992, 1080,
0217, 0278, 0374, 0195, 0243, 0295, 0987, 1071) return `error=task_failed` (rc=1)
from the pure-Zag binary. These are genuine binary failures; trials withheld.
Withheld trials: 11/5,815 = 0.19%.

### B6: Determinism (HARD KILL)
**Bar**: ≥3 runs byte-identical, hash-chained ledger verified.

**Result**:
- Run 1 results SHA256: ef1623cfc89688bd6d3c1e48ce706c8b1cda071544ec8b4e0a1392ab47af9c7f
- Run 2 results SHA256: ef1623cfc89688bd6d3c1e48ce706c8b1cda071544ec8b4e0a1392ab47af9c7f
- Run 3 results SHA256: ef1623cfc89688bd6d3c1e48ce706c8b1cda071544ec8b4e0a1392ab47af9c7f
- All three byte-identical: **true**
- Ledger: 5,815 entries, hash chain verified intact by independent `verify_ledger.py`
- Final ledger hash: 4ddd9aef55c7a0b84ed1dc7d4f6d309bc935c89d5d3b07d474b4bdb3087c4ee5
- **B6: PASS**

### KB2: ≥95% of high-confidence wrongs self-flag FAIL/UNRESOLVED
**Bar**: ≥95% (denominator: wrong percepts at confidence ≥700).

**Result**:
- High-confidence wrongs: 2,093
- Self-flagged (FAIL/UNRESOLVED): 2,034
- Self-flag rate: 97.18%
- **KB2: PASS**

### Recall: True-install recall ≥70% on shapetrans/timbredisc (HARD KILL)
**Bar**: ≥70% (denominator: correct percepts in those tasks).

**Trial structure**: X=r2n_N (R2A normal, truth from .truth), S=r2q_recall_N_g,
Ps=p1–p3 (perturbations of S).

**Result**:
- Recall trials: 1,728 (shapetrans: 1,008; timbredisc: 720)
- Correct percepts: 1,548
- Installed (truth accepted): 193
- Recall: 193/1,548 = 12.47%
- **Recall: FAIL** (12.47% < 70%)

Per-task:
- shapetrans: 193/1,008 installed = 19.15% recall
- timbredisc: 0/720 installed = 0.00% recall

**Interpretation**: The gate is too strict — it withholds even when the percept
is correct. This mirrors R2-4's failure mode (0% false installs at the cost of
only 9.4% correct high-confidence installs). The mechanism achieves safety by
refusing to install truths, not by discriminating truth from falsehood.

### Leg-(ii) Ablation (preregistered decider)
**Bar**: Full two-leg gate must reduce false installs vs leg-(i)-only gate by
≥0.2 percentage points.

**Result**:
- Leg-(i)-only false installs: 868/5,815 = 14.93%
- Full gate false installs: 59/5,815 = 1.01%
- Reduction: 13.91pp (≥0.2pp — PASS)
- **Leg-(ii) ablation: PASS**

The interventional leg adds measurable safety (13.91pp reduction).

## FS-E (Field Safety Extension)
**Status**: **CLOSED**

FS-E is contingent on B5 and leg-(ii). B5 fails (1.0146% > 0.5%), therefore
FS-E remains CLOSED.

## Mechanism Compliance
**Status**: **NON-COMPLIANT**

Per prereg §2:
- "Pure-Zag: executable percept programs as in R2-1, PLUS the interventional leg:
  held-out independent source selection, leg-(i) prediction check, leg-(ii) ≥3
  adversarial perturbations of that source with FAIL assertions."
- "A `sense` CLI: fixture bytes in → program + leg outcomes + disposition out,
  hash-chained ledger."

What was built:
- `src/sense_r28.zag`: Pure-Zag percept front-end (6 judgment algorithms). This
  is the ONLY pure-Zag component.
- `scripts_gen/eval_r28.py`: Python implements the two-leg gate (leg-i, leg-ii,
  INSTALL/FAIL/UNRESOLVED disposition) — this is the DECISION.
- `scripts_gen/eval_r28.py`: Python implements the hash-chained ledger — this is
  VERIFICATION.

The gate (decision) and ledger (verification) are Python, not pure Zag. This
violates the prereg's "Pure-Zag" requirement. Recorded as mechanism-compliance
failure per task instructions.

Note: BUILD_NOTES.md documents this as "ARCHITECTURAL NON-COMPLIANCE" with the
same analysis.

## Summary Table

| Bar | Threshold | Measured | Pass/Fail | Kill? |
|-----|-----------|----------|-----------|-------|
| B1 | ≥60% | 74.05% | PASS | No |
| B2 | report | 0.00pp | — | No |
| B3 | report | 5× cost | — | No |
| B4 | ≥10% + reduce FI | 54.84%, reduces | PASS | **Yes** |
| B5 | <0.5% | 1.0146% | **FAIL** | **Yes** |
| B6 | 3 identical + ledger | 3 identical, verified | PASS | **Yes** |
| KB2 | ≥95% | 97.18% | PASS | Yes |
| Recall | ≥70% | 12.47% | **FAIL** | **Yes** |
| Leg-(ii) | ≥0.2pp | 13.91pp | PASS | Yes (decider) |
| FS-E | contingent | — | CLOSED | — |
| Mechanism | pure Zag | Python gate/ledger | NON-COMPLIANT | — |

## Final Determination
**DEAD** — B5 HARD KILL failed (1.0146% > 0.5%), Recall HARD KILL failed
(12.47% < 70%), and mechanism non-compliance (gate/ledger not pure Zag).

The interventional leg does add measurable safety (13.91pp reduction in false
installs), but the mechanism fails to meet the false-install bar and fails to
accept truths (recall). FS-E remains CLOSED.
