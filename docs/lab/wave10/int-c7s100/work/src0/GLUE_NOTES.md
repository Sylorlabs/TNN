# GLUE_NOTES.md — INT-1 Integration Glue

## Purpose
The glue (`loop.zag`, `seam.zag`, `main.zag`) integrates the five delivered
organs (O1–O5) into a single developmental system. It provides:
- Six seams: the ONLY cross-organ paths (L1–L6 in prereg section 4)
- One append-only 16-word shared ledger (organ tag in op high 16 bits)
- Deterministic developmental curriculum (DC-0 through DC-5)
- Ten probes (P1–P10) and seven controls (C1–C7) as read-only instruments

## Six Seams (only cross-organ paths)
1. **Seam 1 (O1)**: deliberate add/pin/kill via O1 API; ledgered with JUSTIFIED flag on success
2. **Seam 2 (O2)**: hypothesis open, observe, verdict; CONFIRMED→L2, REFUTED→L3
3. **Seam 3 (O3)**: consolidation (requires ≥2 corroborations); preempt selects victim, seam kills via O1
4. **Seam 4 (O4)**: need → compose → verify → commit; ABSTAIN opens O2 hypothesis (L1)
5. **Seam 5 (O5)**: propose → verify → commit; teacher-gated (DC-5 only)
6. **Seam 6 (Glue)**: anchors, stage transitions, audit ticks

No organ touches another's memory directly. L5 static scan verifies.

## Ledger
- 16 words per entry: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60
- Organ in op high 16 bits; op code in low 16 bits
- 16 chunks (ch0..ch15), 524,288 entries each = 8,388,608 total capacity
- Append-only; replay reconstructs exact state

## Determinism
- Zero RNG in AI decision paths (verified by G0 static scan)
- Byte-identical reruns (SHA-256 verified)
- All "randomness" is deterministic PRNG seeded from episode (for world signals only)

## Known Limitations (INT-1)
- **P7 temporal race**: O3 consolidates on CONFIRM; O2 may later REFUTE if world flips. Cross-context gate (b1≥2) enforced; temporal check disabled.
- **Controls C3/C4/C5/C7**: Lesions do not measurably change probe scores (system robust or probes insensitive). Bites pass; control sensitivity is open.
- **DC-2 rollbacks**: Natural refusals via req_ops=15 every 100th episode (selects unverified traces). Gate requires ≥2 rollbacks.
- **P2 drop ceiling**: Unresolved; do not invent a frozen value (per task constraints).
