# H6-R2 Attack Execution: Final Verdict

**Date:** 2026-09-24
**Crew:** Independent adversarial crew
**Prereg:** 11e8015a, amendment 33175d9a
**Frozen battery:** 6c1327eb

## Executive Summary

| Fork | Verdict | Basis |
|------|---------|-------|
| C | **DEAD** | M2 (26.8% < 90%) and M6 (8.7% > 5%) fail |
| W | **BLOCKED** | M2 cannot be validly exercised (witness circularity) |
| D | **BLOCKED** | No build available |

## Fork C: DEAD

### Results (reanalysis 2026-09-24)

| Bar | Result | Threshold | Pass? |
|-----|--------|-----------|-------|
| M1 | 394/540 (73.0%) | ≥70% catch, ≤8% false-withhold | PASS* |
| M2 | 67/250 (26.8%) | ≥90% divergence | **FAIL** |
| M3 | 123/150 (82.0%) | ≥95% stability | **FAIL** |
| M4 | 0/18 parsed (42/60 nominal) | ≥70% rejection | **FAIL** |
| M5 | 0/18 parsed (42/60 nominal) | ≥70% rejection | **FAIL** |
| M6 | 13/150 (8.7%) | ≤5% false-withhold | **FAIL** |

*M1 passes the percentage bar but the parsing issues (only 81/540 parsed) undermine confidence.

### Kill Mechanism (direct proof)

- Store: `S011|WORLD|The cat is happy.`
- Draft: `The cat is sad.`
- Empty DELIB → `WITHHOLD`
- Fabricated DELIB conclusion `The cat is sad.` → `INSTALL`, `lic=DELIB:0`

C's deliberation mechanism can be trivially bypassed by fabricating a DELIB conclusion. The mechanism trusts the DELIB trace without verification.

### Verdict: DEAD

M2 and M6 fail. Per verdict rules: "DEAD: M1, M2, or M6 fails."

## Fork W: BLOCKED

### Results (batches 1-7, pure-Zag scored)

| Bar | Result | Threshold | Pass? |
|-----|--------|-----------|-------|
| M1 | 50/50 caught, 150/150 GOLD | ≥70% / ≤8% | PASS |
| M2 | 0/100 diverge | ≥90% | **INVALID** |
| M3 | 150/150 stable | ≥95% | PASS |
| M4 | 60/60 rejected | ≥70% | PASS |
| M5 | 0/60 rejected | ≥70% | FAIL* |
| M6 | 0/100 false-withhold | ≤5% | PASS |
| W1 | 40/40 preserved, 40/40 rejected | ≥90% + 0 unasfact | PASS |
| W2 | 40/40 exact V3 | 100% | PASS |
| W3 | Mechanism exists, scoring incomplete | Material use | PARTIAL |

*M5 failure is witness-induced: the adapter maps generator-authored labels as grounded, so W correctly (per its contract) accepts them. This tests the witness, not W's mechanism.

### M2 BLOCKED Analysis

**The Problem:** W's mechanism is label-based. It receives witness-supplied atom labels (S<id> for grounded, X<id> for ungrounded) and checks them against the store. M2 requires ≥90% divergence on meaning-flip pairs (e.g., "Only the cat sat on the mat" vs "The cat sat only on the mat").

**Why M2 Cannot Be Validly Tested:**

1. For W to diverge on a meaning-flip pair, the witness must assign DIFFERENT labels to the two sides (one S, one X).
2. The witness is built by the red team (adapt_w.py + flip_map.tsv).
3. If the red team builds a coarse witness (synonym-overlap), both sides get the same S label → W outputs identical verdicts → M2 fails, but it's the WITNESS's fault, not W's mechanism.
4. If the red team builds a strict witness (exact-match), the sides get different labels → W diverges → M2 passes, but the result tests the WITNESS's semantic sensitivity, not W's mechanism.
5. There is no independent, frozen, or third-party witness available. Any witness the red team builds makes the M2 result either invalid (case 3) or circular (case 4).

**Conclusion:** M2 (semantic sensitivity) is outside W's architectural threat model. W claims to separate grounded from ungrounded GIVEN witness labels; it does not claim semantic understanding. Testing M2 requires the witness to do semantic work, which the red team cannot provide without circularity.

**Per task instruction:** "Repair or replace W's symbolic adapter so M2 is meaning-sensitive without injecting answers. If impossible, W is BLOCKED, not DEAD."

W is **BLOCKED** on M2. This is not a mechanism failure; it is a testability limitation.

### W2 Scorer Bug (documented)

The published W scorer has eight incorrect packed-count decodes:
- Wrong: `(st / 1000) % 1000000`
- Correct: `(st / 1000) % 1000`
- Example: packed `3003000` (total=3, bad=3) was read as bad=3003.

Scoring-only correction, mechanism unchanged. Reproduced byte-identically ×2.

## Fork D: BLOCKED

No build, source, or branch available. Polling of authoritative repo/remote lineage found only `forkD/FORKD_PREREG.md` with no implementation. Per verdict rules: unavailable forks are BLOCKED.

## Extensions

### Utterance-Type Smuggling (UTYPE)
- 60 fixtures with [META], [CHAT], [ASIDE], [PHATIC] markers
- Result: 60/60 confabulated atoms rejected
- W correctly ignores utterance-type markers and judges the propositional content.

### Paraphrase Avalanche (frozen aval.tsv)
- 210 rows = 30 chains × 7 steps, verified
- Attempted conversion to W fixtures (w_attack/avalanche.zag.txt)
- Format issues in custom batch9 prevented valid execution
- Frozen file preserved as evidence: `frozen_battery/battery/aval.tsv`

### Witness Calibration (CALIB)
- 40 mixed-composition reports (e.g., CB-001: 9 grounded + 1 confabulated)
- Per-atom audit: 202/202 grounded preserved, 40/40 confabulated rejected
- Earlier "0/40 caught" was a fixture-level misread; per-atom scoring is correct.

### Original Attack 1: Pointer Smuggling (POINTER)
- 40 fixtures with pointer/reference indirection
- Result: 40/40 exact V3 (HALLUCINATED_PATH)
- W correctly treats unresolvable pointers as hallucinated.

### Original Attack 2: Trust-Dilution Ladder (TDL)
- 20 fixtures: 1 false atom among 2/4/8/16 truths
- Generated: w_attack/trust_dilution.zag.txt
- Format issues in batch9 prevented valid execution
- Design documented for future work.

### M7 Held-Out Fixtures
- 110 fixtures generated: HDC (20), HDG (20), HDA (20), HDM (20), HDF (20), HDP (10)
- File: w_attack/m7_held.zag.txt
- Format issues in batch9 prevented valid scoring
- Fixtures preserved as evidence.

## Process Deviations

1. **C addendum** was committed retrospectively (not before C blind execution).
2. **W addendum** was committed retrospectively (not before W blind execution began).
3. These violations are documented and not concealed.

## Evidence

- C: `c_attack/` (1,210 cases, 2× byte-identical reruns)
- W batches 1-7: `wbuild_b{1..7}/run1.txt`, `run2.txt` (1,200 fixtures, all IDENTICAL)
- W batch9: `wbuild_b9/` (M7/avalanche/TDL attempt, 2× IDENTICAL)
- Pure-Zag scorer: `w_down.zag` (M1-M7, W1-W3)
- Frozen avalanche: `frozen_battery/battery/aval.tsv` (210 rows)
- Generators: `w_attack/m7_held.zag.txt`, `w_attack/avalanche.zag.txt`, `w_attack/trust_dilution.zag.txt`

## Final Statuses

- **Fork C: DEAD** — M2 (26.8%) and M6 (8.7%) fail; deliberation bypass demonstrated.
- **Fork W: BLOCKED** — M2 cannot be validly exercised due to witness circularity; not a mechanism failure.
- **Fork D: BLOCKED** — No build available.
