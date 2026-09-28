# CURRICULUM_NOTES.md — INT-1 Developmental Curriculum

## Stages (prereg section 3)
| Stage | Name | Organs | Autonomy | Episodes (scale=10) |
|-------|------|--------|----------|---------------------|
| DC-0 | Deliberate memory | O1 | ADD | 640 |
| DC-1 | Situated belief | O1+O2 | MANAGE | 640 |
| DC-2 | Trace composition | O1+O2+O4 | MANAGE | 640 |
| DC-3 | Structural revision | O1+O2+O3+O5 | KILL | 640 |
| DC-4 | Consolidation | O1+O2+O3 | KILL | 640 |
| DC-5 | Teaching | All | KILL+teacher | 640 |

## Provisional Numbers (parameterized, not frozen)
Per task constraints, these are parameters, not fixed values:
- `scale`: 10 (S10), 100 (S100 projection)
- `slots`: 8*scale (O1 capacity)
- `ledger_cap`: 64*scale (episodes per stage = 64*scale)
- `req_ops`: 19 (normal), 15 (every 100th ep, forces refusal)
- `O1_PIN_EXPIRY`: 48 episodes
- P2 drop ceiling: **UNRESOLVED** — do not invent a frozen value

## Stage Gates
- **DC-0**: ≥95% of successful O1 ops justified; no KILL-op; replay exact; anchors hold
- **DC-1**: every surprise opens hypothesis; corroborated elimination only; zero <2-refute kills
- **DC-2**: ≥75% of ≥12 composites verified; ≥2 rollbacks; endpoint retention
- **DC-3**: ≥1 constructive commit verified; ≥1 harmful refused; zero anchor regression
- **DC-4**: L2 fires (consolidations); links hold; replay exact
- **DC-5**: teacher proposes; learner verifies; zero unverified commits

## Sizing (S100 projection)
- S10 (scale=10): 640 episodes/stage, 3,840 total; binary 506,443 bytes
- S100 (scale=100): 6,400 episodes/stage, 38,400 total
- Ledger capacity: 8,388,608 entries (16 chunks × 524,288)
- Projection: exhaustion at episode 1,309,696 (from s2 sizing check)
- S100 budget: 89,200 episodes (well within capacity)
- No slice over 2^25 bytes (33,554,432); ledger chunked

## Determinism
All stages byte-identical across reruns (SHA-256 verified). Zero RNG in AI paths.
