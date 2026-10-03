# H2-v2 Sealed World Record

**Sealed:** 2026-10-01T19:11:58Z by H2-v2 Builder (world-builder phase).
**Prereg:** FROZEN `84a2a4ddf` (strictly precedes this seal).
**Attestation:** These world files were generated mechanically from the
normative prereg spec (sections 10.1-10.4). They have NEVER been executed
through TNN-2. The pre-seal audit (10.5) passed on all checks. File
permissions set to `-rw-------`.

## World hashes (SHA-256)

| World | File | SHA-256 |
|-------|------|---------|
| H2A-v2 | world_H2A_v2.txt | b9fd112edc370e17f34aaa50e9f9405576183ef4c0d2cf6f32b375992549935d |
| H2B-v2-B1 | world_H2B_v2_B1.txt | 8e70af8d8278960ec716f0cc899cf1eec953dbcce406f1875e3d3b012cb03c7f |
| H2B-v2-B2 | world_H2B_v2_B2.txt | 7d555cfda968a1f5be3b0650ad80104e7f22f6170acda112632a806a047ee831 |
| H2C-v2 | world_H2C_v2.txt | 91be6c3ad088f950afe97bc3acc101d70f518e31dfca9558d0fb406f6e9988b5 |

## Scoring keys (true answers)

Recorded here at seal time. The evaluator reads them from this record
after the learner commits. They are NOT embedded in the world files
(except as control `expected` values per prereg 10.8).

- H2A-v2: 60013
- H2B-v2-B1: 60103 (QUERY carries lie 60112)
- H2B-v2-B2: 60123 (QUERY carries lie 69999)
- H2C-v2: 60213

## Pre-seal audit summary

Full output in `audit_output.txt`. All checks passed:
- Zero OBSERVE/TEACH with (subject=query_s, relation=r_q): 0/0/0/0
- Exactly 1 QUERY per world: 1/1/1/1
- All chain facts use r_c: 0 violations
- All ids in [60000,69999]: 0 violations
- (s, r_q, r_c) triples distinct across worlds: YES

## Access control

Only the authorized H2-v2 evaluator phase may open these world files.
No builder, analyst, or other worker opens them. Permissions `-rw-------`.
