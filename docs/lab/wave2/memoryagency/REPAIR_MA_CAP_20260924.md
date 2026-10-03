# REPAIR — MA1 `MA_CAP` regression (2026-09-24)

## Root cause

After the 2026-09-19 MA1 evidence run (58/58, `EVIDENCE_20260919T222823Z/`),
`MA_CAP` in `trial/memory_core.zag` was raised **8 → 256** for the MA2/MA3
trials. `trial.zag` (the MA1 driver) was never updated to follow
PREREG_MA1's 8-slot spec, so as-committed reruns scored **54/58**
(`EVIDENCE_20260924T071233Z/`, `MA_FAILURES,4`).

The four failures, all explained by the 256-slot core:

| check | expected | actual (256-cap) | cause |
|---|---|---|---|
| `kill_badslot_callerbug` | 2001 (`cl_bad`) | 103 (`REFUSED_NOTLIVE`) | slot 99 is in-bounds under cap 256 → audited refusal instead of caller bug |
| `add_full_refused` | 104 (`REFUSED_FULL`) | 0 (`MA_OK`) | store not full at 8 adds under cap 256 |
| `add_full_slot` | -1 | 8 | 6th fill lands in slot 8 |
| `audit_count` | 28 | 29 | the in-bounds kill at slot 99 is audited (+1 entry) |

## Why the const was NOT reverted

`MA_CAP=256` is load-bearing for MA2/MA3 (`ma2_trial.zag`, `ma3_trial.zag`,
`ma_common.zag` all size loops/allocations from it; their committed
evidence was produced against it). Reverting the shared const would
invalidate MA2/MA3. The core already ships the intended mechanism for
this: `ma_add_lim` — "lets a trial run a smaller effective store on a big
core."

## Repair (this commit)

`trial/trial.zag` only — the shared core is untouched:

1. All 12 `ma_add` call sites → `ma_add_lim(&s, value, region, 8, &slot)`:
   the trial exercises exactly the prereg's 8-slot store (allocation order
   and FULL gate identical to the 8-cap core).
2. Bad-slot probe `ma_kill(&s,99)` → `ma_kill(&s,MA_CAP)` (one past the
   core bound): slot 99 is a legal empty slot on the 256-cap core, so the
   caller-bug gate must be probed out-of-range. Same property tested,
   same check name, still unaudited.
3. Header/section comments document the 8-slot discipline.

## Verification

- Repaired battery: **58/58, `MA_FAILURES,0`, exit 0** — 3 consecutive
  runs (`EVIDENCE_20260924T071431Z/`, `.../071452Z/`, `.../071512Z/`).
- `run.stdout` **byte-identical across all 3 runs**.
- Rebuilt binary SHA-256 identical across all 3 compiles:
  `f867809c9babb34484738a074d55a12fc09ca6a7fbcb37b4d12e238dd6271edf`.
- Repaired `run.stdout` is **byte-identical to the 2026-09-19 evidence
  run** (`EVIDENCE_20260919T222823Z/run.stdout`) — the repaired trial on
  the 256-cap core behaves exactly as the original 8-cap evidence run.
- Zero RNG: pure deterministic Zag, no randomness anywhere in the trial
  or core.
- MA2/MA3 untouched and unaffected (shared core unchanged).

## Standing lesson

A capacity const shared across trials is a cross-trial coupling: any
trial whose prereg pins a capacity must enforce it through its own
discipline (`ma_add_lim`-style), never by assuming the shared const.
