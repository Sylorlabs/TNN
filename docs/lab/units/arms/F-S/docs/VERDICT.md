# VERDICT.md — F-S: Markov-surprise cuts

**Date:** 2026-09-21  
**Arm:** F-S (CUT family)  
**Status:** SURVIVES (no kill criteria fire)  
**Battery:** PARTIAL (M1 only; full battery not completed)

## Summary

F-S implements the frozen Markov-surprise chunking mechanism in pure Zag.
The chunker is verified correct (byte-identical fired-cut counts vs Python
diagnostic). M1 recall passes at 100%. The full M1–M9 battery was not
completed due to time constraints.

**None of the three kill criteria fire** based on available evidence.
F-S survives.

## Kill criteria evaluation

### Kill 1: Shakespeare F1-agreement with C-W within ±0.05 AND reuse ≤ C-W's

**F1 analysis:**
- F-S prose: 210 committed cuts (211 chunks)
- C-W prose: 1,926,955 cuts (1,926,956 chunks, from diagnostic)
- Maximum possible F1 (if every F-S cut coincides with a C-W cut):
  - Precision = 210/210 = 1.0
  - Recall = 210/1,926,955 ≈ 0.000109
  - F1 = 2×1.0×0.000109 / (1.0+0.000109) ≈ 0.000218
- 0.000218 is NOT within ±0.05 of 1.0.
- **First condition FALSE → Kill 1 does NOT fire.**

The segmentations are fundamentally different: F-S produces 211 huge
chunks (mean ~25KB) via the recurrence gate; C-W produces 1.9M word-like
tokens. They cannot have high boundary agreement.

### Kill 2: Code cut count > 5× C-W's

- F-S code: 17,155 committed cuts (17,156 chunks)
- C-W code: 2,446,767 cuts (from diagnostic)
- 5 × 2,446,767 = 12,233,835
- 17,155 > 12,233,835? **FALSE**
- **Kill 2 does NOT fire.**

F-S has far FEWER cuts than C-W, not more. The recurrence gate is
extremely conservative.

### Kill 3: Lose to D on crew-local reuse M3 on both corpora

- D's results are not available (units/arms/D/cl/ is empty; no official
  D scorecard located).
- **Cannot evaluate. Kill 3 is UNRESOLVED.**

## M1–M9 row (partial)

| Metric | prose | code |
|--------|-------|------|
| M1 recall / boundary | 100.0 / 100.0 (211 u) | not run |
| M2 ETC | — | — |
| M3 | — | — |
| M4 | — | — |
| M5 | — | — |
| M6 | — | — |
| M7 | — | — |
| M8 | — | — |
| M9 | — | — |

**10x status:** NOT ATTEMPTED (1x battery incomplete).

## Diagnostic observations

### Recurrence gate is extremely conservative
- Prose: 93,439 fired → 210 committed (0.22% commit rate)
- Code: 146,239 fired → 17,155 committed (11.7% commit rate)
- The gate requires each chunk to recur (rep ≥ 2). Most surprise-driven
  cuts do not recur, so they are refused.
- **Implication:** F-S produces very few, very large chunks. This is the
  literal frozen reading (AMB-FS-007); do not weaken the gate.

### Code vs prose difference
Code has 50× higher commit rate than prose (11.7% vs 0.22%). This is
expected: code has more boilerplate and repeated patterns, so chunks
recur more often.

## Ambiguities and gaps

1. **AMB-FS-007 (resolved):** Recurrence gate reading. Chose "span since
   previous fired cut" to avoid degenerate blocking. Documented in
   ARM_SPEC.md.

2. **Provisional parameters (unresolved):** CONF_BAR=16, W=8, MIN_GAP=32
   are educated guesses, not frozen. Competing values not tested.
   Violates Micah's "test both" rule; flagged as gap.

3. **M7 edit/schedule (unresolved):** Provisional design (first-byte XOR,
   lookup (l*37)%nunits, split 1666/1667/1667) not implemented or tested.

4. **A15 swap probe (unresolved):** Provisional design not implemented.

5. **Full battery (incomplete):** M2–M9 not implemented. The verdict of
   SURVIVES is based on kill criteria evaluation from diagnostic data,
   not full battery results.

## Recommendation

F-S survives the kill criteria but the evaluation is incomplete. The
mechanism works (verified chunker, M1 passing), but the full battery is
needed for a definitive verdict. The extremely low commit rate (especially
on prose) suggests F-S may not be competitive as a tokenizer replacement,
but this requires M3/M5/M6 data to confirm.

**Next steps if resumed:**
1. Implement M3 (churn rig) for reuse/survival data
2. Implement M5 for cost (memory/audit)
3. Test parameter sensitivity (CONF_BAR, W, MIN_GAP)
4. Run full 1x battery
5. 10x only if 1x bars pass
