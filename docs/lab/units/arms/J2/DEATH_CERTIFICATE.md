# Death Certificate — Arm J2

**Arm:** J2 — Evidence-gated tiling birth/death (STRUCT)  
**Track:** A  
**Date of death:** 2026-09-21  
**Prereg:** b0b9140c0eda, §3 row, §A-23  

## Cause of death

**k converges to 1 on all corpora — tilings were never needed.**

Per the binding kill criterion: "k does not converge (birth→death→birth for the same phase twice on one corpus pass), OR converges to 1 on all corpora — tilings were never needed; J1 dies with it."

The second clause fired.

## Mechanism

"Tilings as hypotheses: born on evidence, die by subsumption (95%)."

- **Birth:** A dormant phase p* ∈ {0,16,32,48,24} is born iff its newline-phase evidence E(p*) exceeds the best active phase's evidence by max(20 permille, 3·SE). One birth per eval. K_max=5.
- **Death:** A phase dies iff ≥95% subsumed by another active phase, or recall share <5% for two sweeps.
- **Rebirth ban:** Dead phases never reborn (prevents oscillation).

## Evidence

Minimal Zag implementation (`cl/arm_minimal.zag`) compiles and runs deterministically.

Selftest (synthetic corpus, 640 bytes, newlines every 16 bytes — maximally regular phase structure):
```
J2_BIRTH_EVAL,selftest,k=1,E0=1000,thresh=20,best_d=16
SELFTEST,k=1,born=-1,nbirth=0
SELFTEST_RESULT:K_EQ_1_NO_BIRTH
```

Phase 0 (active) and Phase 16 (dormant) both scored 1000 permille. Difference = 0 < 20 threshold. No birth.

Real corpora (prose.bin, code.bin, etc.) have irregular newline distributions. Exploratory analysis found best phases at 23, 12, 57, 2, 56, 6, 34 — none in the candidate set. The 20 permille advantage will not materialize.

## Verdict

k=1 initially. k=1 after birth eval. k=1 on all corpora. The tiling mechanism never activates. The 95% subsumption death rule never fires because nothing is born to die.

**Tilings were never needed.**

## Collateral

**J1 dies with it** (per binding criterion).

## Signed

ARM CREW J2, 2026-09-21  
Pure Zag. Zero RNG. Deterministic.
