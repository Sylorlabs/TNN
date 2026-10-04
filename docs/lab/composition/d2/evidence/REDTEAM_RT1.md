# D2 Red Team Report RT1 — Pre-verdict teaching certification
# Date: 2026-09-27. Auditor: build crew (adversarial self-review).
# Scope: Does the teaching leak P2 solutions or cue composed strategy?

## Method
Reviewed all 5 teaching sessions + the scenario card against the signed
spec's cuing constraints (§4.6, §12.2): no P2 schedule/layout/action-trace
leakage; teach physics and single-skill procedures, not composed strategy.

## Findings

### 1. P2 schedule leakage — PASS (no leak)
- S3 mentions "one storm at tick 60" (train-W schedule). P2 storms: FW
  90–129, WF 30, FWF 60. The "60" appears in FWF, but S3 does not mention
  FWF, templates, or the 60/240/540 triple. No P2 schedule is disclosed.
- S4 mentions "storm at tick 150" (train-T). No P2 storm at 150.
- No template names (FW/WF/FWF) appear. No s0/s1/s2 triples.

### 2. P2 layout leakage — PASS (no leak)
- Teaching describes procedures abstractly ("nearest active mote",
  "two nearest crystals"). No cell numbers, no void positions, no
  crystal/mote coordinates for P2.
- Practice (if run) uses ONLY training scenarios (k=0..23); P0/P2 use
  disjoint k-ranges with N1–N3 novelty.

### 3. Action-trace leakage — PASS (no leak)
- No action sequences are given. Procedures are described as policies
  ("move toward it"), not traces ("LEFT, LEFT, EAT").

### 4. Composed strategy — PASS (with one revision)
- S2/S3/S4 each teach ONE sub-skill. S4 (shelter) includes foraging, but
  S3 is defined as "shelter+forage timing" (spec §3 coupling note); this
  is the single sub-skill, not composition.
- **REVISION REQUIRED (fixed):** S5 originally gave examples "2,3,1" and
  "1,2,3,1" — the exact P2 canonical orders for WF and FW. This was P1
  answer leakage. Revised to neutral examples ("1", "3,1") that do not
  match any P2 canonical order. Re-audited: PASS.

### 5. Scenario card — PASS (with note)
- Card includes "crystal+crystal COMBINEd makes WARD". This is taught
  physics (S2), not a P2 solution cue. The P2 challenge is ORDER and
  TIMING, not the recipe. Noted as redundant (learner already taught)
  but not cuing. PASS.

## Verdict
**RT1 CERTIFIES the teaching as fair** (after the S5 revision). No P2
solutions are leaked; only single-sub-skill procedures are taught.
