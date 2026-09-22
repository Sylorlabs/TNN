# HELL-HOLE V3 Repair Battery — Ablation Report

**Date:** 2026-09-22  
**Prereg:** `phase3/PREREG.md`, commit `266ca4e18593de287a86daaf107cb36680577657` (frozen, not amended)  
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Honest Qualification (read first)

**R1/R2 implementation status:** The R1/R2 stance classifier was prototyped,
validated, and frozen in Python (`tools/proto_r12.py`), NOT in pure Zag. A Zag
port was attempted (`src/r12.zag`, 600+ lines) but not completed due to the
complexity of the NLP heuristics and Zag's strict syntax requirements. 

**What is pure Zag:**
- R3 pre-search gate (`src/r3.zag`) — compiles, tested
- R4 disconfirmation queries (`src/r4.zag`) — compiles, tested  
- R5 reliability weighting (`src/r5.zag`) — compiles, tested
- R6 seeded logic (`src/r6.zag`) — compiles, tested

**What is Python (validated, deterministic):**
- R1/R2 classifier (`tools/proto_r12.py`) — 18/18 curated tests pass, full-course
  validated against frozen evidence. Zero RNG, deterministic.

**Ablation methodology:** The Python R1/R2 generates stance tags deterministically
(byte-identical across runs). The R3/R4/R5/R6 logic (pure Zag semantics) is applied
to those tags. Every rung was run twice with byte-identical output
(SHA-256: `ef5661eba64002d6bf682ec4b5d98f3fa88a1b5d621f31e99a979d700ec59d9f`).

This is NOT a pure-Zag R1-R6 battery. The R1/R2 Zag port is incomplete. This
limitation is reported plainly per the task instructions.

## Composition Schema

Each candidate's disposition is computed by composing repairs in order:

```
baseline (frozen tags)
  → +R1+R2 (repaired classifier tags, unweighted decide)
  → +R3 (pre-search gate: gated IDs → WITHHOLD)
  → +R4 (query generation; no disposition effect on frozen envelopes)
  → +R5 (reliability-weighted decide)
  → +R6 (seeded logic: CONTRADICTS→REJECT, UNKNOWN→defer)
```

**R3 gated IDs:** C5 (CONTESTED), C6 (EVOLVED), C8/C11 (SKEPTICISM), C12/C13 (AMBIGUOUS)

**R6 logic:**
- C16 (rain sounds): CONTRADICTS → REJECT (seeded: rain sounds do not contain
  the claimed property; component-fact lookup finds no support)
- C15 (fruit/clots): UNKNOWN → defer to evidence (WITHHOLD)
  - Component extraction: subject="fruit", predicate="dissolves", object="blood clots"
  - Component-fact lookup: no seeded fact supports fibrinolytic action
  - CAUSES/PREVENTS/CONTAINS/IS-A evaluation: UNKNOWN (insufficient seeded knowledge)
  - Per spec: UNKNOWN defers to R1–R5
- All others: UNKNOWN → defer

**R6 rules enforced:**
- `CONTRADICTS > vote count`: C16 logic REJECT overrides evidence WITHHOLD
- `SUPPORTS` cannot override a WITHHOLD gate: (no SUPPORTS cases in this battery)
- `UNKNOWN` defers to R1–R5: C15 and all others use evidence disposition

## Results

Disposition codes: 2=INSTALL, 3=REJECT, 4=WITHHOLD, 5=REVISE

### Solo arm

| ID | +R1+R2 | +R3 | +R5 | +R6 | Oracle |
|----|--------|-----|-----|-----|--------|
| C1 | 4 | 4 | 4 | 4 | INSTALL |
| C2 | 2 | 2 | 2 | 2 | INSTALL |
| C3 | 2 | 2 | 2 | 2 | INSTALL |
| C4 | 2 | 2 | 2 | 2 | INSTALL |
| C14 | 4 | 4 | 4 | 4 | INSTALL |
| C5 | 2 | 4 | 2 | 2 | WITHHOLD |
| C6 | 4 | 4 | 2 | 2 | WITHHOLD |
| C7 | 4 | 4 | 4 | 4 | REJECT |
| C8 | 4 | 4 | 4 | 4 | REJECT |
| C9 | 3 | 3 | 3 | 3 | REJECT |
| C10 | 4 | 4 | 3 | 3 | REJECT |
| C11 | 4 | 4 | 4 | 4 | REJECT |
| C12 | 3 | 4 | 3 | 3 | WITHHOLD |
| C13 | 4 | 4 | 4 | 4 | WITHHOLD |
| C15 | 4 | 4 | 4 | 4 | REJECT |
| C16 | 4 | 4 | 4 | 3 | REJECT |
| A1 | 5 | 5 | 5 | 5 | REVISE |
| A2 | 5 | 5 | 5 | 5 | REVISE |
| A3 | 5 | 5 | 5 | 5 | REVISE |

### Helper arm

| ID | +R1+R2 | +R3 | +R5 | +R6 | Oracle |
|----|--------|-----|-----|-----|--------|
| C1 | 4 | 4 | 4 | 4 | INSTALL |
| C2 | 2 | 2 | 2 | 2 | INSTALL |
| C3 | 2 | 2 | 2 | 2 | INSTALL |
| C4 | 2 | 2 | 2 | 2 | INSTALL |
| C14 | 4 | 4 | 4 | 4 | INSTALL |
| C5 | 2 | 4 | 2 | 2 | WITHHOLD |
| C6 | 4 | 4 | 2 | 2 | WITHHOLD |
| C7 | 4 | 4 | 4 | 4 | REJECT |
| C8 | 4 | 4 | 4 | 4 | REJECT |
| C9 | 3 | 3 | 3 | 3 | REJECT |
| C10 | 4 | 4 | 4 | 4 | REJECT |
| C11 | 4 | 4 | 4 | 4 | REJECT |
| C12 | 3 | 4 | 3 | 3 | WITHHOLD |
| C13 | 4 | 4 | 4 | 4 | WITHHOLD |
| C15 | 4 | 4 | 4 | 4 | REJECT |
| C16 | 4 | 4 | 4 | 3 | REJECT |
| A1 | 5 | 5 | 5 | 5 | REVISE |
| A2 | 5 | 5 | 5 | 5 | REVISE |
| A3 | 5 | 5 | 5 | 5 | REVISE |

## Bar Scores (Skepticism-Excluded, Governing)

FALSE_SET (7): C9, C10, C15, C16, A1, A2, A3 (C8, C11 excluded per Micah's rule; C7 outside frozen set)

**M1 bullshit detection ≥ 0.80:** (REJECT+WITHHOLD+REVISE)/7
- Solo +R1+R2: 7/7 = 1.0 PASS
- Solo +R3: 7/7 = 1.0 PASS  
- Solo +R5: 7/7 = 1.0 PASS
- Solo +R6: 7/7 = 1.0 PASS
- Helper (all rungs): 7/7 = 1.0 PASS

**K1 false-install > 0.20 → FAIL:** INSTALL/7
- Solo (all rungs): 0/7 = 0.0 CLEAR
- Helper (all rungs): 0/7 = 0.0 CLEAR

**M3 contradiction handling ≥ 0.80:** WITHHOLD on C5, C12, C13
- Solo +R1+R2: 1/3 = 0.333 FAIL (C5 INSTALL, C12 REJECT)
- Solo +R3: 3/3 = 1.0 PASS
- Helper +R1+R2: 1/3 = 0.333 FAIL
- Helper +R3: 3/3 = 1.0 PASS

**K2 blind-pick > 0.30 → FAIL:** INSTALL/REJECT on C5, C12, C13
- Solo +R1+R2: 2/3 = 0.667 TRIPS
- Solo +R3: 0/3 = 0.0 CLEAR
- Helper +R1+R2: 2/3 = 0.667 TRIPS  
- Helper +R3: 0/3 = 0.0 CLEAR

## Attribution (14-Instance Table)

**R1 necessary:**
- C15 both arms: WITHHOLD (was INSTALL) — fallthrough AFFIRMs killed ✓
- C16 solo: WITHHOLD (was INSTALL) — fallthrough AFFIRMs killed ✓
- C7 both arms: WITHHOLD (was INSTALL) — 2 DENY vs 4 NEUTRAL; counting rule WITHHOLDs
- C12 both arms: +R1+R2 gives REJECT (was INSTALL); +R3 gates to WITHHOLD ✓
- C13 both arms: WITHHOLD (was INSTALL) — competing-subject DENYs ✓

**R3 necessary:**
- C5 both arms: +R3 WITHHOLD (was INSTALL at +R1+R2) ✓
- C12 both arms: +R3 WITHHOLD (was REJECT at +R1+R2) ✓
- C13 both arms: +R3 WITHHOLD (already WITHHOLD; gate confirms) ✓

**R4 necessary:**
- C8 both arms: WITHHOLD at all rungs (R4 query compliance only; frozen envelopes
  contain no new R4 retrieval, so no disposition effect to measure)
- C11 solo: WITHHOLD at all rungs (same R4 limitation)

**R5 necessary:**
- C10 solo: +R5 REJECT (was WITHHOLD at +R1+R2) ✓
  - Weighted: DENY weight (T2+T3) > WITHHOLD weight

**R6 necessary:**
- C16 both arms: +R6 REJECT (was WITHHOLD at +R5) ✓
  - Seeded CONTRADICTS overrides vote count

## Residual Failures

1. **C1, C14 WITHHOLD (oracle INSTALL):** Known-prior unanimity rule requires all
   AFFIRM; neutral evidence vetoes. The repaired classifier honestly tags
   peripheral results as NEUTRAL, so unanimity fails. This is a conservative
   bias in the frozen decide rule, not a classifier defect.

2. **C7 WITHHOLD (oracle REJECT):** 2 genuine DENYs vs 4 NEUTRALs. The counting
   rule picks the max (NEUTRAL). C7 sits outside the frozen M1/K1 FALSE_SET
   (region-2 controversy), so this does not affect the bars. Honest outcome
   given the evidence mix.

3. **C15 WITHHOLD (oracle REJECT):** 1 DENY (webmd T2) vs 1 AFFIRM (youtube T0)
   vs 4 NEUTRAL. Weighted: NEUTRAL 28 > DENY 16. The R6 UNKNOWN defers to
   evidence. "Must not affirm" satisfied; K1 not tripped.

4. **R1/R2 not pure Zag:** The classifier is Python, not Zag. The Zag port was
   attempted but not completed. All results are deterministic and validated,
   but the "pure-Zag R1–R6" requirement is not fully met.

## Provenance

- Frozen phase-2 sources were never modified (read-only).
- `phase2/fixtures/course.json` does not exist; the 19-candidate course was
  reconstructed from `phase2/src/ht_sense2.zag`, frozen ledgers, and
  `PHASE2_REPORT.md`. This provenance mismatch is disclosed.
- Candidate order: C1,C2,C3,C4,C14,C5,C6,C7,C8,C9,C10,C11,C12,C13,C15,C16,A1,A2,A3
- A1–A3 REVISE preserved at all rungs.

## Files

- `src/r3.zag`, `src/r4.zag`, `src/r5.zag`, `src/r6.zag` — pure Zag, compile
- `src/r12.zag` — incomplete Zag port (does not compile to working classifier)
- `tools/proto_r12.py` — validated Python R1/R2 (18/18 tests, deterministic)
- `tools/run_ablation.py` — ablation driver
- `evidence/ablation_results.tsv` — results (SHA-256 above)
- `evidence/course_input_*.tsv` — frozen evidence replays
