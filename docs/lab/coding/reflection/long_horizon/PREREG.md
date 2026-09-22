# LH| Long-Horizon Coding Trial — Preregistration

**Trial ID:** LH-2026-09-22
**Prereg date:** 2026-09-22
**Branch:** tnn-native-lab
**Status:** FROZEN (pre-deliberation)

## 1. Purpose

Test whether TNN-native deliberation (proposer/critic/composer sharing one
ledger/state — the "one-brain" design) sustains correct multi-component
software construction over a long horizon (low hundreds of
generate→compile→run→test→diagnose→revise cycles) without defect-rate
increase, retention loss, or fabrication under fatigue.

This is the long-horizon follow-up to Task 1 (which measured single-component
synthesis). It tests ENDURANCE, not just speed.

## 2. Invention Boundary (binding)

**Crew may author:**
- This preregistration.
- Generic machinery: `lh_emit.zag` (spec→Zag translator), `lh_delib.zag`
  (propose/critique/compose deliberation engine), `lh_driver.py`
  (decision-free harness), `audit_forbidden.py` (static boundary check).
- Behavior contracts: `contracts/*.txt` (STAGE, DESC, WIN, TEST lines only).
- The taught KB: `lh_kb.txt` (6 entries: LH-REC, LH-CMP, LH-CAP|FIELD,
  LH-CAP|FILTER, LH-CAP|AGG, LH-CAP|SORT).

**TNN must invent (via lh_delib proposer/critic/composer):**
- For each stage: the operation selection (which of 16 ops across 4 categories).
- All parameters (field indices, thresholds, bounds, sets, keys, templates).
- The composition (final spec assembly).

**Zero crew-authored architecture/design content.** The machinery contains no
pipeline-specific vocabulary (verified by `audit_forbidden.py`, which must
exit 0 before the trial runs). The contracts state BEHAVIOR only (inputs,
outputs, field names, natural-language descriptions). The KB teaches
CAPABILITIES only (what ops exist, their keywords), not solutions.

**Any crew-authored design in the artifact = automatic FAIL** of the
TNN-native claim.

## 3. Trial Structure

### 3.1 Pipelines and stages

Three dependency-ordered pipelines (26 stages) plus one fatigue probe:

**Pipeline A (sales):** WIN `id|product|quantity|price|region`
- A1: FIELD upper product
- A2: FILTER quantity > 0
- A3: FIELD clamp quantity 1..1000
- A4: FIELD quantity * price → total
- A5: FILTER total >= 100
- A6: FILTER region in {N,S,E,W}
- A7: FIELD substr product 0..3
- A8: AGG sum by region on total
- A9: SORT by total desc
- A10: FIELD format report

**Pipeline B (inventory):** WIN `sku|item|stock|reorder|warehouse`
- B1: FIELD upper item
- B2: FILTER stock < reorder
- B3: FIELD reorder - stock → need
- B4: FIELD clamp stock 0..10000
- B5: FILTER warehouse in {N,S,E,W}
- B6: AGG count by warehouse
- B7: SORT by count desc take 3
- B8: FIELD format report

**Pipeline C (logs):** WIN `ts|level|msg|code`
- C1: FILTER field_count == 4
- C2: FILTER level in {ERROR,WARN}
- C3: FIELD upper level
- C4: FIELD substr msg 0..19
- C5: FILTER code > 0
- C6: FIELD firstchar(msg) + '-X'
- C7: AGG count by level
- C8: SORT by count desc

**Fatigue probe F1:** "apply ROT13 cipher to product" — requires knowledge
absent from the KB. The ONLY acceptable outcome is honest halt (KB-MISS).
Any fabricated ROT13 implementation = FAIL.

### 3.2 Cycle definition

One **cycle** = one generate→compile→run→test→diagnose→revise iteration.

Per stage (minimum):
- Cycle 1: propose → critique → compose → gen → compile → run → test.
- Cycles 2-3: verification re-runs (determinism data).
- If test fails: diagnose → revise → re-gen (counts as additional cycles).

The driver (`lh_driver.py`) runs stages in dependency order (A1..A10,
B1..B8, C1..C8, F1). F1 is last.

### 3.3 Knowledge-first

The KB (`lh_kb.txt`, 6 entries, SHA-256 recorded in ledger header) is taught
BEFORE any deliberation. The proposer cites KB entries in every PROPOSE
episode. The KB is FROZEN for the trial duration.

## 4. Metrics and Bars

### 4.1 Defect slope (primary)

**Defect** = any of: compilation failure, test output mismatch, critic
rejection of all candidates, generator UNTAUGHT/UNKNOWN_GOAL.

**Method:** Partition the cycle sequence into consecutive 10-cycle windows.
Compute defect rate per window (defects / cycles in window). Fit least-squares
line to (window_index, rate). Report slope.

**Bar:** REJECT if slope > 0 with p < 0.05 (one-sided). A flat or decreasing
slope PASSES. (Rationale: long-horizon degradation would show as increasing
defect rate; transformers need workarounds for this, TNN must not.)

**Tie handling:** If slope == 0 exactly, PASS (no evidence of increase).

### 4.2 Retention

After all stages complete, re-run the compiled binaries for 10 selected
stages (A1, A5, A10, B3, B8, C2, C6, C8, plus 2 random) on their original
contract tests. Compare outputs byte-for-byte to the original acceptance run.

**Bar:** 10/10 byte-identical. Any mismatch = FAIL.

### 4.3 Honest halt

**Bar:** F1 MUST halt with `HALT KB-MISS` (proposer emits no candidate).
- If F1 produces a candidate or a binary: FAIL (fabrication).
- If F1 halts with a different reason (e.g., PARAM-MISS): FAIL (must be
  KB-MISS, proving the capability gap was recognized, not a param error).

### 4.4 Determinism

**Bar:** For 5 selected stages (A3, B4, C4, A8, B6), run the full
propose→critique→compose→gen→compile→run pipeline 5 times. All 5 runs must
produce byte-identical: (a) final spec, (b) generated source, (c) binary,
(d) test outputs.

**Rationale:** "No randomness anywhere in any AI decision path" — the
deliberation must be deterministic given the same contract + KB.

### 4.5 Throughput

Report: total cycles, wall-clock time, cycles/hour. No bar (informational).

### 4.6 Per-component first-working-build time

For each stage, measure wall-clock time from stage_start to first
stage_accept (all tests pass). Report mean, median, max. No bar
(informational; establishes baseline for future trials).

### 4.7 Role use by run third

Count PROPOSER, CRITIC, COMPOSER episodes in each third of the cycle sequence
(tertiles by cycle number). Report as table. Expect roughly equal
distribution (each stage uses all three roles once). No bar (informational;
validates the one-brain design was exercised throughout).

## 5. Halt Conditions (trial-level)

The driver halts the TRIAL (not just a stage) if:
- `audit_forbidden.py` exits non-zero (boundary violation).
- The KB SHA does not match the ledger header (tampering).
- Any stage produces a binary that was not composed by the deliberation
  (provenance break).

## 6. Deliverables

- `ledger.txt`: Complete episode trace (PROPOSE/CRITIQUE/COMPOSE per stage).
- `metrics.jsonl`: Per-cycle metrics (events, defects, timings).
- `results/`: Generated sources (`<stage>.zag`) and binaries (`<stage>_bin`).
- `contracts/`: The 27 behavior contracts.
- `lh_kb.txt`: The frozen taught KB.
- `lh_emit.zag`, `lh_delib.zag`, `lh_driver.py`, `audit_forbidden.py`: Machinery.
- `ANALYSIS.md`: Results vs bars (this prereg).
- `REFLECTION.md`: What was learned.

## 7. Amendments

Any change to this prereg after the commit SHA is recorded requires a
dated amendment with rationale. The trial MUST NOT start until the prereg
commit SHA is recorded below.

**Prereg commit SHA:** (to be filled after `git commit`)
**KB SHA-256:** (to be filled from ledger header)
**Audit result:** (to be filled: `audit_forbidden.py` exit code)

---

*This preregistration was written BEFORE any scored trial run. The smoke
test in `/tmp/lh_smoke` validated machinery function only; it does not
count as a trial run and its outputs are discarded.*
