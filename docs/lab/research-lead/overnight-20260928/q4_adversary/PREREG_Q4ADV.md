# PREREG Q4 ADVERSARY

## Adversary Design Preregistration

**Date:** 2026-09-30
**Purpose:** Design at least one new evaluation family for Q4 C0-C testing, post-freeze.

### Context
- Q4 Reuse: BUILD-PASS (b719bb54b). C0-D satisfied.
- C0-C requires: "At least one evaluation family designed by independent adversary after freeze."
- Existing families: CONJ, XOR, THRESH, MUX, NEST (all researcher-designed).

### What I Will Design
1. **One new family** (F-PARCOND) with a materially different structural form.
2. **Sealed specification** (hidden from learner designer until evaluation).
3. **Evaluation protocol** mirroring Q4 Phase 1/Phase 2 structure.

### Design Constraints (Frozen)
- Solvable by generic language: terminals + AND/OR/NOT/XOR, max 7 operator nodes.
- Must require DIFFERENT structural form than CONJ/XOR/THRESH.
- Must test whether discovery mechanism generalizes beyond training families.

### Kill Bars for This Design Work
- K1: New family specified in sealed document.
- K2: Structural difference from CONJ/XOR/THRESH/MUX/NEST documented with operator counts.
- K3: Evaluation protocol frozen (Phase 1 discovery, Phase 2 reuse, sample budget, scoring).

### Governance
- Design only. No implementation.
- No Python. No em dashes.
- This prereg committed alone before the specification.
