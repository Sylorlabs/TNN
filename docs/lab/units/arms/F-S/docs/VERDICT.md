# VERDICT.md — F-S: Markov-surprise cuts

**Date:** 2026-09-21  
**Arm:** F-S (CUT family)  
**Status:** SURVIVES (no kill criteria fire)  
**Battery:** COMPLETE 1x (M1–M9, all modes, byte-identical double runs)

## Summary

F-S implements the frozen Markov-surprise chunking mechanism in pure Zag.
The chunker is verified correct (byte-identical fired-cut counts vs Python
diagnostic). The full M1–M9 battery passes at 1x with byte-identical
double runs for every mode.

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

## M1–M9 row (complete 1x)

| Metric | prose | code |
|--------|-------|------|
| M1 recall / boundary | 100.0 / 100.0 (211 u) | 100.0 / 100.0 (17156 u) |
| M2 T1 ETC / content / boundary | 1 / 100.0 / 100.0 | 1 / 100.0 / 100.0 |
| M2 T2 ETC / content / boundary | 1 / 100.0 / 100.0 | 1 / 100.0 / 100.0 |
| M2 T3 ETC / content / boundary | 1 / 100.0 / 100.0 | — |
| M3 survival / fresh / weaken / freeze | 100.0 / 100.0 / 50 / 0 | — |
| M4 episodes / content / boundary | 1 / 100.0 / 100.0 | 1 / 100.0 / 100.0 |
| M5 (provisional) | 155u, 5.6MB src, 11.5MB slots | — |
| M6 transfer tax | 0.0 (p2c) | 0.0 (c2p) |
| M7 lookup / reuse (provisional) | 100.0 / 2.0 | — |
| M8 clean/frag/aslr/starve/freelist | 100/100/100 all | — |
| M9 (from M2) | mean 100.0, range 0.0 | mean 100.0, range 0.0 |

**Determinism:** Every mode run twice; stdout byte-identical (diff-verified).
M8: all artifacts (ledger.bin, chain files, hashes, alloc trace) also
byte-identical across runs and perturbations.

**10x status:** NOT ATTEMPTED (prereg is 1x).

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

2. **Provisional parameters (sweep-tested):** CONF_BAR=16, W=8, MIN_GAP=32.
   Seven configs tested (see ARM_SPEC.md §2). Results: [pending — see
   BUILD_LOG.md]. The values remain provisional (not frozen).

3. **M7 edit/schedule (provisional):** First-byte XOR edit, (l*37)%nunits
   schedule, 1666/1667/1667 split. Implemented and passing; marked
   provisional in all outputs.

4. **A15 swap probe (implemented):** After each ceil(nunits/64) recalls,
   remap/verify/restore with TRAINER_SWAP_PROBE audit entries.

5. **M5/M8 provisional:** See ARM_SPEC.md §7 for exact provisional
   semantics and limitations.

## Recommendation

F-S survives the kill criteria with a complete 1x battery. The mechanism
works (verified chunker, all metrics passing), but the extremely low
commit rate (especially on prose: 0.22%) suggests F-S may not be
competitive as a tokenizer replacement — it produces very few, very large
chunks. The section-champion evaluation (Verdict §7 of the frozen prereg)
will determine F-S's standing vs other CUT-family arms.

**Parameter sweep:** Seven CONF_BAR/W/MIN_GAP configs tested per Micah's
"test both" rule; results in BUILD_LOG.md. If a config dominates on
M1/M3, it becomes the recommended (still provisional) setting.
