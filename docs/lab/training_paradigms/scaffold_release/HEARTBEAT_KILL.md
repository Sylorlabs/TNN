# HEARTBEAT_KILL.md — per-episode scaffold heartbeat removed (2026-09-23)

Per **Micah's ruling 2026-09-23**: per-episode heartbeat auditing is dead.
Every scaffold arm under `forks/` (g1–g7) was converted from a per-episode
scaffold heartbeat to P2's proven event-driven pattern: a scaffold entry is
written **only** on the disconnect-transition episode and on actual
contradiction events (`signal == -1`, the episodes that drive elimination).
Hint/probe markers that carry real information (s2 h3, s5 ADV_OK) were kept;
null/sentinel periodic reads were removed. Replay reads no scaffold entries
in any fork, so ledgers stay exactly replayable; behavior is otherwise
byte-identical (all checks pass, two runs byte-identical per fork).

Original frozen results (FORK_RESULTS.md etc.) describe the pre-kill ledgers;
the exact pre-kill code is recoverable from git history.

| variant | scaffold entries old → new | audit total old → new | run sha256 | note |
|---|---|---|---|---|
| g1/r1 | 128 → 3 | 392 → 267 | `2a72e21922138687` | E38 fire |
| g1/r2 | 128 → 3 | 392 → 267 | `e5075f93b0b23924` | E30 harness-cut fire |
| g1/r3 | 128 → 2 | 387 → 261 | `650034fc07905898` | never fires; trans never occurs |
| g1/r4 | 128 → 3 | 392 → 267 | `1500eeb8571e6b3e` | E54 late fire |
| g1/r5 | 128 → 2 | 396 → 270 | `75e28a577c4fc911` | E20 cut, 1 elim |
| g2/s1 | 128 → 3 | None → None | `70dbcdf23a321312` | no total check |
| g2/s2 | 102+2+2 hint → 3/3/1 hint (7 total) | None → None | `72d673f80adcc70b` | hints kept as events; null reads killed |
| g2/s3 | 128 → 3 | None → None | `aa51c2ced6a5529e` | probe null-read killed |
| g2/s4 | 2 → 0 | None → None | `5c719cdded0f75b3` | teach-sentinel heartbeat only |
| g2/s5 | 128 → 4 | None → None | `58487e6c78672e24` | 3 events + ADV_OK probe marker kept |
| g3/l2 | 128 → 3 | None → None | `11dfbd3db3c6e1f4` | no total check |
| g3/l3 | 128 → 3 | None → None | `e451b090ca2ab71f` | hint events only |
| g4/r1 | per-ep → signal==-1 only | None → None | `bf291a96a383ea31` | d3s_episode gated |
| g4/r2 | per-ep → signal==-1 only | None → None | `b3f113eab28a4a44` | d3s_episode gated |
| g4/r3 | per-ep → signal==-1 only | None → None | `c7abdbca05b25392` | d3s_episode gated |
| g6/p1 | 848 → 3 | 2588 → 1743 | `7a235ff033c6a9e4` | 848-episode horizon |
| g6/p2 | 850 → 3 | 2815 → 1968 | `e18c2b831d386e4d` | 850-episode horizon, MP_ ops |
| g7/profiler/p1 | 128 → 3 | 392 → 267 | `2635df2db5281f78` | full op-profile updated |
| g7/fl4 | 128 → 2 | 398 → 272 | `750fd356afa5d3bf` | honest+lying arms |
| g7/rematch/r2_d1b | 128 → 3 | 399 → 274 | `2875348039cd867b` | old d1b arm; FL2 arm untouched |
| g7/rematch/r3_d2 | 128 → 3 | 392 → 267 | `254540a0f599452b` | old d2task arm; FL2 arm untouched |

## Excluded (inspected, no change)

- `forks/g7_slowness/profiler/p0_baseline/` — **deprecated, frozen**: the
  E38/392 reference arm. Kept byte-identical for reference/reproducibility;
  see its DEPRECATED.md. (This is the one documented exception to the
  everywhere-kill: the old arm's 392-entry ledger is the historical record.)
- `forks/g7_slowness/freelunch/fl2_provisional_revoke/` — already event-driven
  (source of the canonical `gl_default/`).
- `forks/g7_slowness/freelunch/fl1_teach_disconnect/` — no scaffold appends.
- `forks/g7_slowness/rematch/r1_d1/` — FL2 event-driven already.
- `forks/g7_slowness/profiler/p2/`, `p3/` — already event-driven (3 events each).
- `forks/g3_lying_teacher/l1_mistaught_teaching/` — no scaffold appends.
- `forks/g5_dialogue/` (f1, f2) — forks state no scaffold signal; no heartbeat found.
- `forks/g8_fl2_variants/` — sibling crew's active FL2-variant work; already
  event-driven (2 gated scaffold audits per file). Untouched (out of scope).
- `forks/g4_outcome_domain/baseline_teaching/` — teaching baseline; no scaffold
  heartbeat (verified: no per-episode scaffold audit in its loop).

## Verification

Each fork's own runner was re-run after the edit: compile OK, two runs
byte-identical (sha256 above, full hashes in the runner output / evidence
files), every check line matched, `*_FAILURES,0`. Evidence files
(evidence_run1/2.txt) regenerated in place.
