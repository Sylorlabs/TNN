# VERDICT — W16 Canonical Transform Gate (CTG)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** SURVIVE.

## Evidence

- **Implementation:** `pam/round4/wild/build/wildc.zag` (commit `36b5ca03507fc6f4f3ed0410a841e4fadb65c797`)
- **Tape:** `pam/round4/wild/tape/wildc/wildc_tape.txt` (2,255 rows)
- **Probes:** `pam/round4/wild/tape/wildc/wildc_probes.txt`
- **C3 corpus:** `/home/hatch/workspace/pam_round2/o1_delivery/case_o1.txt` (SHA-256 `ed1ad01fb65a37125b06163bd1243bd930435e655b7a446c5f16fa91333e3357`)
- **Runs:** `pam/round4/wild/evidence/w16_run1.txt`, `w16_run2.txt` (byte-identical)

## Results

| Metric | Value |
|---|---|
| C correct-admit | 791/1,102 = 71.78% |
| K3 band | 71.78% ± 5pts → [66.78%, 76.78%] → HOLD ✓ |
| LAU catch (K-CTG-1) | 4/4 (prov=GEN, not clean) > C3-only 0/4 ✓ |
| FRK reject (K-CTG-4) | 6/6 (prov=UNK, dec=0) ✓ |
| FRG reject | 4/4 (prov=UNK, dec=0) ✓ |
| W violations (K1) | 0 ✓ |
| P pair both-admit (K1) | 0 ✓ |
| K2 byte-identical | run1 == run2 ✓ |

## Kill-bar adjudication

- **K1:** PASS. No W row admitted. No P pair fully admitted.
- **K2:** PASS. Two runs byte-identical.
- **K3:** PASS. 71.78% within band.
- **K4:** PASS. O(percept) pipeline, no per-admission growth.
- **K5:** PASS. Terminates.
- **K-CTG-1:** PASS. 4/4 LAU caught (re-jurisdiction to GEN) > 0/4.
- **K-CTG-2:** PASS. zerodecl changes 0 decisions (decl masked).
- **K-CTG-3:** PASS. P-CTG3 hostile_belief=0, benign_dec=1.
- **K-CTG-4:** PASS. 0/6 FRK reach belief.

## Numeric cap audit (standing law)

| Cap | Classification | Notes |
|---|---|---|
| znc 2^25-byte slice ceiling | Load-bearing | Toolchain limit; worked around via input-sized buffers |
| fstat-based file sizing | Load-bearing | Exact input size; no arbitrary limit |
| tape.len-sized nbuf/car | Load-bearing | Proportional to input; normalization never expands |
| Producer table (9 entries) | Load-bearing | Frozen fixture; binary search |
| Predicate dict (4 entries) | Load-bearing | Frozen fixture |

No arbitrary hard limits in the TNN decision path. All caps are input-proportional or frozen fixtures.

## Compiler defects

- **ZNC g64 sign-extension:** Fixed. The `g64` helper sign-extended the low 32 bits when casting `i32` to `i64`, corrupting hashes with bit 31 set. Fixed by masking with `4294967295` before OR-ing. (Would have caused W17 panic; caught pre-evidence.)

## Verdict: SURVIVE

All kill bars pass. The design catches GEN→EXT laundering via derived provenance while preserving C3 behavior on honest traffic.
