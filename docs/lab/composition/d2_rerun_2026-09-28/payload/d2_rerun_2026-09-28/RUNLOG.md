# D2 re-run run log — 2026-09-28

## Timeline (UTC)

- 00:14 — fetched origin; branch head `b825f54dd91a5d8570a33f07b5287345e1816c5c`.
  `docs/lab/composition/` absent at head (deleted in `13c557cd`).
- 00:15 — extracted clean source from `a61b5b94c` (pre-deletion) to
  `~/workspace/composition_d2_rerun/src/docs/lab/composition/`:
  `d2/` (scenarios, source), `d2spec/` (frozen spec), `amendments/`,
  `redo_2026-09-27/` (repaired learner source).
- 00:16 — verified all committed D2 scenario SHA-256: OK.
- 00:17 — rebuilt `wb3_learner` from source; SHA-256 reproduced pinned
  `16c023cabfedf5af36b12ec2c03a3c9802ec5f83c646b318f2f0010b98369d48`.
  Required imports copied: `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`.
- 00:18 — rebuilt `d2bin`; sanity OK (F-24 refok 120 ticks; FW-48 refok
  200 ticks ward built; N-72 null exact 80×WAIT).
- 00:19 — smoke test: teaching → "Noted."; OBS → no digit (invalid ×3,
  abort). Predicted P0 0/24 before the full run.
- 00:20 — launched full `drive_d2.py`. **Crashed in P1** (broken pipe):
  learner panicked `slice index out of bounds`. P0 24/24 logged before
  the crash.
- 00:25 — root-caused: every chat turn appends input+response to fixed
  64 KB `histb` (no bounds check). Reproduced standalone: dies at
  ~64.8 KB cumulative. Unrepaired `wb_dialogue_bin` dies at ~63.9 KB —
  legacy defect, both builds.
- 00:26 — measured protocol volume: teaching 5.0 KB; through P0 62.8 KB
  (survives); P1 → 83.3 KB (dies). Matches crash point exactly.
- 00:27 — checked independent red team: verdict STANDS, no kill
  (`REDTEAM_2026-09-27.md`); clearance to proceed confirmed 2026-09-28.
- 00:28 — wrote `p0_only.py` (teaching+practice+P0, single session) and
  `p1_only.py` (fresh session, teaching re-sent + 24 questions).
- 00:30 — p0_run1: **0/24**, EXIT 0. p1_run1: **0/24**, EXIT 0.
- 00:45 — p0_run2: 0/24; p1_run2: 0/24. Byte-identity vs run1: exact.
- 00:50 — p0_pert (`MALLOC_PERTURB_=165`): 0/24, byte-identical.
  p1_pert: 0/24, byte-identical.
- 00:55 — re-ran §10 reference gate on rebuilt instrument: refok P0
  24/24, P2 24/24; null 0/24; singlerule 0/24; wrongorder 24/24.
- 01:00 — wrote VERDICT.md, RUNLOG.md (this file), DETERMINISM.md,
  AMENDMENT_2026-09-28_D2-4_PROPOSED.md.

## Protocol deviation (documented)

P1 run in a fresh session (teaching re-sent) because the single-session
protocol exceeds the 64 KB history arena before P1 completes. P0 measured
in the standard single session. See VERDICT.md "Session-length finding".

## Numbers

- P0: 0/24 (F 0/8, W 0/8, T 0/8) — 3/3 byte-identical runs.
- P1: 0/24 — 3/3 byte-identical runs.
- P2/P3: not run (K2 VOID). P4: not derived. K1/K3/K4/K5/K6: not adjudicated.
- Controls: NULL 0/24, SINGLE-RULE 0/24, WRONG-ORDER 24/24, REF-OK 24/24.
