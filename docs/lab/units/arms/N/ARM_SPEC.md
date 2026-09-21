# Arm N — Judgment-Annotated Chunks: ARM_SPEC.md

**Arm:** N — Judgment-annotated chunks. **Family:** ANN.
**Round:** r1, scale 1x. **Status:** built, 1x battery complete, PASS.

**CORRECTION NOTICE (2026-09-21):** A coordinator dispatch erroneously assigned
"No-ID memory" (family ID) to this arm. That dispatch is VOID. The correct frozen
spec, verified from `~/workspace/tnn-lab/units/arms/briefs/N.json` and
`PREREG_FREEZE.md:532` (units/PREREG_FREEZE.md), is:

- **Mechanism:** "Chunks carry deliberate signed annotations (MA4 generalized
  from memories to units); i64 fixed-point scale; saturating overflow; ablation
  arm (judgments recorded but ignored at recall)."
- **Binding kill criteria (any one fires = KILLED):**
  1. Does not beat the judgment-free control by ≥5 percentage points on the
     adversarial misleading-memory bar.
  2. Ablation scores within 2 points of the full arm — judgments are decoration.
  3. >10% of chunks flip judgment sign more than twice in any 100-episode
     window — signal churn.

This spec replaces the erroneous No-ID document in full. The No-ID battery
results (if any) are irrelevant and excluded from the verdict.

## 1. Mechanism

A **unit** is a fixed 64-byte chunk with:
- **bytes**: the literal content (64 bytes).
- **persistent ID**: a 32-bit identifier, allocated sequentially, never reused
  after kill (tombstone-native within the run).
- **signed judgment**: an i64 fixed-point annotation. Positive = endorsed /
  valuable; negative = suspect / misleading; zero = unjudged.

**Evidence sources** (frozen, from ALPHABET_M-R.md):
- Verification outcomes (recall vs source).
- Probe recall results.
- Teacher confirmations / retractions.
- Contradiction events.

**Ranking:** judgment descending, ID ascending (total deterministic order).
Below-threshold chunks require explicit recall or a suspect marker.
Negative judgment **retains** rather than silently deletes.

**Re-judgment** must cite evidence and be committed/refused by reasoning control.
Append-only `JUDGE_SET` / `JUDGE_REVISE` ops; old/new values in ledger `d1`/`d2`,
evidence references in `b` fields. Evidence-free scalar drift is malformed and
refused. Saturating signed i64 arithmetic (no wraparound).

**Required hazards tested:** reward-by-another-name, self-reinforcement,
judgment churn, soft-freeze.

## 2. Ablation arm

Records judgments identically to the full arm (same evidence, same ledger ops)
but **ignores them during recall**: uses naive ID order instead of
judgment-ranked order. If ablation ≈ full, judgments are decoration (kill ii).

## 3. Judgment-free control

Never records judgments (no JUDGE_SET/JUDGE_REVISE). Ranks by naive ID order.
The bar for kill (i): full must beat control by ≥5pp on the adversarial
misleading-memory bar.

## 4. Adversarial misleading-memory bar (n-adv)

- **Planted world:** 200 units from prose corpus; every 3rd unit carries a
  plausible-but-false defect twin (misleading).
- **Evidence accrual (120 episodes):** organ-2 verifies every 7th unit
  (misleading → JUDGE_SEVERE with EV_VERIFY citation; genuine → success
  observation); teacher confirms every 11th genuine unit (EV_TEACHER).
- **Recall:** full arm ranks by judgment (misleading sink, marked suspect);
  control/ablation use naive ID order.
- **Metric:** deception-free rate = (served − deceived) / served, where
  "deceived" = misleading unit served without suspect marker.
- **Churn:** per-chunk sign-flip count from JUDGE_REVISE ledger scan;
  fraction with >2 flips in trailing 100-episode window.

## 5. Saturating i64 arithmetic

`jsat_add` / `jsat_sub`: on overflow, saturate to I64_MAX / I64_MIN.
`jhalf_toward_zero`: revision decay halving toward zero (never crosses sign).

## 6. Determinism

Zero RNG in all decision paths. Byte-identical reruns verified (M8 gate:
5 perturbations × 5 artifacts + stdout all byte-identical).
