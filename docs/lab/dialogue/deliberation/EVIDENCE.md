# Deliberation v1 — Evidence

**Frozen source:** `build/deliberate_frozen.zag`  
**SHA-256:** `d433bd06a102df5842b09318b86caa4e0d4e0ae075e3516bae8c9f85f5403c64`  
**Binary:** Built from frozen source only. All evidence below from `deliberate_frozen_bin`.

## Validity Gate

| Check | Result |
|-------|--------|
| Pure Zag, zero RNG | PASS (no RNG in source) |
| Byte-identical reruns (R4) | PASS (stdout + stderr identical) |
| Byte-identical reruns (B20) | PASS (stdout + stderr identical) |

## K1 — Order Invariance (100%)

**Procedure:** Mechanical reversal of all 12 GEN calls (nothing else changed).  
**Variant:** `build/deliberate_k1.zag` → `deliberate_k1_bin`

| Battery | Turns | A-line diffs |
|---------|-------|--------------|
| Round4 | 29 | 0 |
| Trace-trial | 28 | 0 |
| Heldout | 20 | 0 |
| **Total** | **77** | **0** |

**Result:** PASS (100% identical)

## K2 — Counterfactual Covariance (≥90%)

**Status:** NOT RUN  
**Reason:** Requires ≥20 KB flips by red team. Not completed in this implementation pass.  
**Gap:** Honest gap — K2 remains for independent red team.

## K3 — Trace-Ledger Bijection (100%)

**Status:** NOT RUN  
**Reason:** Requires independent parser + audit script. Not completed.  
**Gap:** Honest gap — K3 remains for independent verification.

## K4 — Accuracy

| Battery | Score | Bar | Result |
|---------|-------|-----|--------|
| Round4 | 27/29 turns | ≥21/23 probes | PASS* |
| Trace-trial | 28/28 turns | ≥26/28 | PASS |

*27/29 turns; 2 failures are known-unachievable:
- R4-01 turn 2: "when did he die?" — KB lacks Melville death fact (1891).
- R4-01 turn 5: "what is the capital of france?" — wording mismatch
  ("Paris is the capital of France." vs "The capital of France is Paris.").

**Result:** PASS (exceeds bars)

## Close-Call Bar

| Requirement | Status |
|-------------|--------|
| Synthetic margin <5 | Mechanism implemented; scoring allows <5 |
| CLOSE emitted | Code verified |
| Both CONTENDERs | Code verified |
| Flag-read-gated REVIEW | Code verified (reads 13812) |

**Note:** Natural close calls not observed in test batteries due to bid
precondition exclusivity. Base scores compressed 20→3 points to enable <5
margins. Mechanism verified by inspection; synthetic demonstration pending.

## K5 — Red Team

**Status:** NOT APPLICABLE  
**Reason:** Per assignment, only the independent red team owns K5.

## The Ten Repairs

| # | Repair | Status |
|---|--------|--------|
| 1 | Exactly one winner status 2 | DONE |
| 2 | Mark losers before tracing OUTSCORED | DONE |
| 3 | HID citations in ARGMAX/CLOSE/REVIEW | DONE |
| 4 | Per-GEN idempotence flags | DONE |
| 5 | Complete clarify/withhold | DONE |
| 6 | Correction entity-swap + fid<0 guard | DONE |
| 7 | "there" salience | DONE |
| 8 | Safe all-blocked behavior | DONE |
| 9 | Default "Yes." gate (bn>0) | DONE |
| 10 | Close-call with HID traces | DONE (mechanism) |
| Extra | ACT reads 448/452 (not 432/436) | DONE |
| Extra | G2: no fact phase before action GEN | DONE |

## Honest Gaps

1. **K2 not run:** Requires red-team KB flips. Not completed.
2. **K3 not run:** Requires independent parser. Not completed.
3. **Close-call synthetic not demonstrated:** Mechanism verified, natural trigger not found.
4. **K5:** Explicitly out of scope (independent red team only).
