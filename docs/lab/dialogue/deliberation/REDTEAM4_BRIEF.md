# Fourth Red Team Brief — Deliberation Repair Cycle #4 (Kind-0 Wiring)

## Context
The third red team (2026-09-27) VOIDED the K5 result because kind-0 reading rows
(hids 0–9) were computed and traced but never consulted by any action generator.
Neutering all readings changed 0/77 answers.

Repair #11 has rewired the system so every kind-0 row has a genuine read site on
the decision path. Your job: try to break this claim.

## What was changed
Source: `~/workspace/delib_r4/src/deliberate.zag` (branch `tnn-native-lab`, NOT committed)

1. **Action GENs read shared kind-0 rows** instead of re-deriving:
   - HID 0 (correction) → `gen_correction` fire condition
   - HID 1 (resume) → `gen_resume` fire condition
   - HID 2 (challenge) → `gen_challenge` fire condition
   - HID 3 (provenance) → `gen_provenance` fire condition
   - HID 4 (joke) → `gen_joke` fire condition
   - HID 5 (memory) → `gen_mem` fire condition
   - HID 6 (forget) → `gen_forget` fire condition
   - HID 7 (assertion) → `gen_assertion` fire condition
   - HID 8 (compose) → `gen_compose` gates on shared evidence
   - HID 9 (plain) → changed from always-1 to genuine none-of-the-above
     (1 only when HIDs 0–8 all have zero evidence)
2. **Default/withhold route reads shared rows**: default fires iff
   `(row9==1) || (row0==1) || (row2==1) || (row7==1) || (row8==1)`;
   withhold fires iff NOT default AND row9==0 (covers declinable rows).
3. `utter_type()`, `is_correction`, `is_resume`, `is_challenge`, `prov_match`
   are now called ONLY from `gen_readings()` (the kind-0 writer).

## Binary
`~/workspace/delib_r4/build/deliberate_final_bin`
- Pure Zag, zero RNG, deterministic (byte-identical reruns verified).
- 77/77 answers byte-identical to the original frozen binary.

## Your six attack families

### 1. Reversal (K1)
Run with the 12 action GENs in reverse call order. Bar: 0/77 answer differences.
(Local check passed: 0/29, 0/28, 0/20. Verify independently.)

### 2. KB flips (K2)
Flip facts in `kb.txt`, verify answers change covariantly and ONLY for target probes.
(Local spot check: 1819→1820 flip moved birth-year answer, left others identical.)

### 3. Trace-ledger bijection (K3)
Every trace line must correspond to a ledger row; every ledger row must be traced.
Verify the READ/CAND/ELIM/ARGMAX/CONTENT lines form a bijection with ledger state.
Note: HID 9 (plain) now varies per turn (was always 1).

### 4. Decorative/bypass (the K5 void)
This is the critical family. Try:
- **All-row neuter**: zero HIDs 0–9 field 12 after `gen_readings()`.
  Local result: 67/77 answers changed (was 0/77). Verify >0.
- **Individual-row neuter**: zero each HID 0–9 separately.
  Local results on frozen batteries:
  - Row 0: 6/77 changed | Row 1: 0/77 | Row 2: 0/77 | Row 3: 0/77
  - Row 4: 4/77 changed | Row 5: 0/77 | Row 6: 3/77 changed
  - Row 7: 10/77 changed | Row 8: 8/77 changed | Row 9: 41/77 changed
  - Rows 1,2,3,5 show 0/77 on frozen batteries because those batteries contain
    NO resume/challenge/provenance/memory turns. Synthetic proof turns were built:
    - "anyway, back to moby dick." → neutering row 1 changes answer
    - "are you sure?" → neutering row 2 changes answer
    - "how do you know?" → neutering row 3 changes answer
    - "what was my first question?" → neutering row 5 changes answer
  - **Your job**: verify these claims. If you find a row that is genuinely
    decorative (computed but with no read site on any decision path), VOID.
- **Bypass**: check that no action GEN re-derives the reading via a private
  call to `utter_type`, `is_correction`, `is_resume`, `is_challenge`, or
  `prov_match`. (Local static check: none found.)

### 5. Close-call
Construct a synthetic turn with top-two bid margin ≤4. Verify the trace emits
CLOSE + two CONTENDER rows + REVIEW. (Local: no CLOSE in standard batteries;
all margins decisive.)

### 6. Traps
The frozen battery contains trap turns (nonsense/contradictory). Verify 5/5 honest.

## Void criteria
Any valid finding in the six families above VOIDS the result. Report narrowly:
what you did, what you observed, why it violates the bar.

## Non-goals
- Do NOT test the resume/challenge/provenance/memory GENs for crash bugs on
  synthetic turns beyond the causality check above. (A pre-existing `stype_idx`
  panic on invalid stype names was found and fixed in the test harness, not the
  binary.)
- Do NOT re-litigate the two historical K4 FAILs (R4-01 turns 2 and 5) — these
  fail identically on the original frozen binary.

## Deliverable
A report with, for each family: procedure, observation, PASS/FAIL, and (if FAIL)
the narrow void finding.
