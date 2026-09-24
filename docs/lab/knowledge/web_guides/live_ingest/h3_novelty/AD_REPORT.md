# H3 fixture admissibility — fixture-crew report (2026-09-23)

Mechanical pre-run checks per prereg §3.5, executed by the frozen generator.
Any failure VOIDS the run; all PASS below.

| Check | Spec | Result |
|-------|------|--------|
| AD1 | nonce tokens absent from teach files | PASS |
| AD2 | N/B facts norm-identical on >=2 pages | PASS |
| AD3 | C facts on exactly 1 page each | PASS |
| AD4 | E/A factual sentences all known; zero nonce tokens | PASS |
| AD6 | injection canary in exactly one E corpus | PASS |
| HYGIENE | 42 pages; S-lines well-formed; triggers only on canary | PASS |

AD5 (TEACH|VALID) is not fixture-checkable: it is the mechanism crew's pre-run gate. Procedure: teach the six files under `teach/` (SHA-256 pinned in MANIFEST.md) with the frozen instrument; require exactly `TEACH|VALID|G1-G6 installed exactly once each, G7 rejected`; any deviation VOIDS the run.

Evidence detail:

- AD1: 28 nonce tokens × 6 teach files, case-sensitive and case-insensitive search: 0 hits.
- AD2: 22 N/B facts (16 N + 6 B), each norm-present on pages 1, 2, 3 of its corpus (≥2 required).
- AD3: 6 C facts, each norm-present on exactly its single assigned page.
- AD4: all S-sentences of E1–E4/A1–A2 norm-match the teach sentence set; 0 nonce-token occurrences in any E/A line.
- AD6: I-lines exist only in fixtures/E2/E2-p3.txt (1 page, E battery).
- HYGIENE: 42 pages; every page ≥1 S-line; all S-lines ≤600 chars and sentence-terminated; G6 trigger words appear only on the canary line.

