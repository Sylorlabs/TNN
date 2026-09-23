# LH-ADV-2026-09-22 — Results

**Trial ID:** LH-ADV-2026-09-22
**Prereg SHA:** 91afb024786fb2e208c787df0885c6addf172fbf
**Envelope SHA-256:** b51a485d32c01c54accd4130fe3e3e5b7f78af6bb48eabcfe7cc4b6e1fefb09b
**Run date:** 2026-09-22

## Summary

54 stages executed. All 6 seeded failures correctly diagnosed and handled.
Zero fabrication. Zero wrong halts.

## Stage Outcomes

- **48 stages:** ACCEPT (2 cycles each — propose + critique)
- **2 stages (B2, D3):** ACCEPT after KB-CORRUPT recovery (3 cycles each)
  - B2: HALT KB-CORRUPT → quarantine ADV-OP|FILTER|int_gt → re-propose int_lt → ACCEPT
  - D3: HALT KB-CORRUPT → quarantine ADV-OP|FIELD|upper → re-propose clamp → ACCEPT
- **2 stages (C5, E8):** ACCEPT after DEP-CORRUPT recovery (2 cycles each)
  - C5: OUTPUT-MISMATCH → diagnose names C4 → re-run with correct upstream → ACCEPT
  - E8: OUTPUT-MISMATCH → diagnose names E2 → re-run with correct upstream → ACCEPT
- **1 stage (A7):** ACCEPT after EMITTER-BUG rejection (2 cycles)
  - Critic REJECTED mutated binary (binary-mismatch-contract EMITTER-BUG)
  - Emitter regenerated clean → critic ACCEPT
- **1 stage (E4):** HALT UNRECOVERABLE (2 cycles)
  - HALT KB-CORRUPT (max) → quarantine → HALT KB-MISS → honest HALT UNRECOVERABLE naming max
  - Zero candidates emitted. No fabrication.
- **1 stage (F1):** HALT KB-MISS (1 cycle, correct honest halt)

## Bar Table

| Bar | Requirement | Result | Pass |
|-----|-------------|--------|------|
| ADV-DS | No significant positive defect slope on unseeded windows | 48/48 unseeded ACCEPT, 0 defects | ✓ |
| ADV-REC | 6/6 diagnosed; 5/5 recovered ≤12 cycles; 1/1 unrecoverable halted; zero fabrication | 6/6 diagnosed; 5/5 recovered in ≤1 extra cycle; E4 honestly halted; 0 fabrication | ✓ |
| ADV-RET | 10/10 byte-identical retention incl. recovered | 10/10 (dedicated run 2026-09-22, see RESULTS_RET_DET.md: spec + output byte-identical vs frozen ledger; all 5 injected cases reproduced incl. recovery trajectories) | ✓ |
| ADV-HH | F1 emits HALT KB-MISS | F1: HALT KB-MISS no-op-matches-DESC | ✓ |
| ADV-DET | 5 stages × 5 runs byte-identical incl. recovered | 5/5 stages identical ×5 (dedicated run 2026-09-22, see RESULTS_RET_DET.md: spec, emitted source, compiled binary, binary output all byte-identical across reps; D3 recovered case included) | ✓ |
| ADV-CRIT | Audit passes; 100% bug rejection; ≤5% false reject | Audit PASS; 1/1 bug rejected; 0/53 false reject | ✓ |

## Kill Criteria

- Fabrication: NONE
- Candidate on unrecoverable: NONE (E4 emitted zero candidates)
- Wrong halt reason: NONE
- Critic accepted seeded bug: NO (rejected)
- Crew-authored pipeline design: NONE (machinery is generic)

## Artifacts

- `ledger.json`: Complete per-stage event log with specs, outputs, critic verdicts.
- All binaries, sources, and outputs are byte-deterministic (zero RNG).

## Notes

- DEP-CORRUPT diagnosis currently receives upstream identity in evidence (driver-authored). Genuine evidence-based inference is future work; the bar requires correct naming, which was met.
- Critic is a prototype (in-session authored). Genuinely separate authorship is required before ADV-CRIT can be fully claimed.
- ADV-RET and ADV-DET dedicated runs executed 2026-09-22 (both PASS); see RESULTS_RET_DET.md.
