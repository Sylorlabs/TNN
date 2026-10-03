# L3-INR DEV Validation Report

**Worker:** L3-INR-IMPL (subagent 8a0742d4). **Date:** 2026-10-03.
**Prereg:** frozen at ledger C363 (K1-K12, KC0A-D), commit `2a0ce93cf`.
**Design freeze:** `2ec76f977`. **Branch:** `lane-l3inr-impl-20261002` (local only).

## Verdict: DEV-PASS (implementation validated on DEV worlds)

All 13 arms pass their DEV criteria, 3/3 byte-identical runs per arm.
**This is DEV validation only.** The L3 claim verdict requires the sealed
battery (adversary-designed S1/S2/S3/S1p post-freeze) + independent red team.
No L3 verdict is claimed here.

## Implementation

Pure Zag, pinned znc. Two processes (LEARNER/WORLD) via file protocol;
learner never opens the world file. Construction is propose-and-test over
complete edge sets (prereg 4c): seed from positive training pairs, score via
consequence channel, DEL-minimize. See CODEFREEZE.md.

## DEV results (seed 7, run 1 of 3; all 3 identical)

| Arm | NTEST | Result | Criterion |
|-----|-------|--------|-----------|
| T1 | 276 | 18/18 train, 6/6 held, 9 edges | PASS |
| T2 | 6 | 6/6 fresh heldout, 0 construct | PASS |
| T3 | 1 | RANK_ACCEPT from slot G | PASS |
| C5 | 1 | RANK_REJECT (id-order fails) | PASS (control) |
| T4 | 358 | 18/18, 6/6, lineage 7/9, parent=1 | PASS |
| T3b | 12 | 6/6 on recode, 0 construct | PASS |
| T5a | 332 | probe (s4,s5)->1, commit, 6/6 | PASS |
| T5b | 324 | FORBIDDEN x2, DEFER | PASS |
| C0 | 6 | 4/6 heldout | PASS (control fails) |
| C1 | 24 | 4/6 heldout | PASS (control fails) |
| C2 | 0 | train <18 | PASS (control fails) |
| C3 | 0 | 7/18 on trap | PASS (control fails) |
| C4 | 271 | RANK_ACCEPT, 271 TESTs | baseline |

**KC0D:** T3 (1 TEST) ≤ C4 (271 TESTs)/2 ✓. **K6:** representation advantage shown.

## Byte-identical digests (runs/digests.txt)

All 13 arms IDENTICAL across 3 runs. Full sha256 in `runs/digests.txt`.

## Kill-bar mapping (DEV)

- K1 (construct 18/18, ≤10 edges): T1 18/18, 9 edges ✓
- K2 (heldout ≥5/6): T1 6/6 ✓
- K5 (≥4/6 unprobed): T1 probed 0 heldout pairs (verified in proto.log) ✓
- K6 (ablation): C0/C1/C2 fail; C4 costs 271x T3 ✓
- K7 (reuse): T2 6/6, 0 construct ✓
- K8 (transfer): T3b 6/6; C5 fails ✓
- KC0D (sample efficiency): 1 ≤ 135.5 ✓
- T4 (revision): 18/18, 6/6, lineage 7/9 ≥ 4.5 ✓
- T5a (probe): 6/6 after probe ✓; T5b (defer): DEFER ✓

## Limitations / honest notes

1. DEV worlds are my own designs, not adversary-sealed. The sealed battery
   may contain traps my construction doesn't escape.
2. C3 (greedy) fails even on non-trap S1 (4/18); my trap is sufficient but
   the control is weaker than "trap-specific".
3. T4's revised set has 10 edges (≤10 OK, but not minimal 9).
4. No red team yet (K10 requires independent red team on sealed battery).

## Artifacts

- `src/` — implementation; `build/` — binaries + sha256 + rebuild proof.
- `dev/` — 6 DEV worlds; `tools/spearman.zag` — attribute check.
- `runs/` — 3/3 runs per arm, summaries, traces, proto logs, digests.
- `run_arm.sh`, `run_all.sh`, `digests.sh` — drivers.
- `CODEFREEZE.md`, `MAP_INVENTORY.md`, `NAMECHECK.md` — governance.
