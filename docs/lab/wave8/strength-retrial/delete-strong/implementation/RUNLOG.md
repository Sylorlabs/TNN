# RUNLOG — strength-delete workstream (DELETE-STRONG merged stack)

## 2026-09-26 ~04:15 UTC — setup
- Created ~/workspace/strength-delete/ with root copies:
  - strength_core.zag ← f1/strength_core.zag (SHA aa0e5015..., F1-forkA) ✓
  - strength_checker.zag ← f1/strength_checker.zag (SHA 2fb1e00e..., F1-forkA) ✓
  - strength_learner.zag ← f1/capacity/src/strength_learner.zag (B2 tiers) ✓
  - strength_trial.zag ← f1/capacity/src/strength_trial.zag ✓
  - substrate/ ← f1/substrate/ ✓
- r4val/trial/substrate/ ← f1/r4val/trial/substrate/ ✓
- Ported attack drivers into r4val/: f1_attack.zag, f2_attack.zag, f4_attacks.zag,
  r4_overwrite.zag, rt_redteam.zag (verbatim copies).
- Verified: SHA sums of all 4 merge ingredients match the task's pins.
- Verified: 121 unused in f1 base core (no ST_REFUSED_CONSUMED).
- Verified: for arm B, capacity lr_b_score reduces to old formula
  (vj+50*slot_revimp) — honest B trails unaffected by learner swap.
- f1/r4val/run_a1.log == f4/f4b/r4val/run_a1.log byte-identical; forkA logs
  (f1/logs/forkA/r4_attack_*.log) add the ck_ow_cite_distinct line (stale
  r4val run logs predate that print) — the merged checker WILL print it,
  so forkA logs are the right control target for r4_overwrite.

## 2026-09-26 ~04:20 UTC — merge complete (merge_core.py / merge_checker.py)
- Core: F1-forkA base + ST_REFUSED_CONSUMED=121 + ST_OP_DELETE_STRONG=20 +
  F4b bufferless cites (st_cite_consumed, st_count_spent_cites, fresh-count,
  121-for-consumed-reuse) + st_delete_strong + rollback/replay/P3 wiring.
  DELETE_STRONG explicitly excluded from st_last_strength_idx and
  st_epoch_highwater (neither strength write nor judgment birth).
- Checker: F1-forkA base + F4b fresh-count/genuineness + ck_verify_delete +
  DELETE_STRONG in ck_verify dispatch + legal strength-lineage ops.
- trial/strength_core.zag = root core + verbatim st_overwrite_direct hook only
  (diff confirmed). trial/strength_checker.zag byte-identical to root checker.
- Built trial_bin (build.log). GATE: B/C/C-P3/B2 all ST_GATE f=0.

## 2026-09-26 ~04:30 UTC — honest regression PASS
- S1 matrix 27/27 (B/C/C-P3 × 9 cells): r1==r2 byte-identical; merged r1 ==
  ~/workspace/strength-f1f2f4/f1/evidence_r4f/ byte-identical.
- B2 S1 matrix 9/9: r1==r2; merged r1 ==
  ~/workspace/strength-round4/capacity/evidence/ byte-identical.
- S10/S100 spots B_VUP_2, B_JI_0 (S1/S10/S100): r1==r2 and == evidence_r4.
- NOTE: background `&` jobs with relative-path redirects silently produce
  empty output in this sandbox; foreground sequential runs work. All
  determinism runs done in foreground from here on.

## 2026-09-26 ~04:45 UTC — attack batteries PASS (all 2× byte-identical)
- f1_attack: 2× identical; F1_* lines == f1/logs/forkA/f1_attack_r1.log.
  All discount variants closed (109), legit paths pass, cf=0.
- f2_attack: 2× identical; F2_* lines == f2/logs/forkA/f2_attack_forkA_r1.log
  EXCEPT A8/A9: merged gives ow/kill refused 109 (mechanism-side F1-forkA
  HW pricing, which subsumes F2-forkA's checker-side rule); forkA log shows
  ow/kill 0 + checker flag (F2's losing fork-B-shaped outcome was 109 too).
  All variants flagged (cf>=1) or closed (109) — requirement met.
- f4_attacks: 2× identical; FA_* lines == f4/logs/fa_f4b_r3.log byte-identical.
  A5/V1B/V2/V2B/V4 closed (121), V3 closed (109), V5 flagged, C1-C3 pass.
- rt_redteam: 2× identical; RT_* lines == f1/logs/forkA/rt_redteam_r1.log
  EXCEPT A5: merged ow_rc=121 (F4b double-spend closure) vs forkA ow_rc=0
  (the F4 vulnerability). All other RT_* lines byte-identical.
- r4_overwrite positions a/b/c: 2× identical; == f1/logs/forkA/r4_attack_{a,b,c}.log.
- del_attack (new, D1–D11): 2× identical; all expectations met (see MERGE_REPORT).

## 2026-09-26 ~05:00 UTC — verification probes
- Static grep: strength_learner.zag contains zero calls to st_delete_strong,
  st_weaken, st_overwrite (honest learner never touches destruction paths).
- Mirror audit: every ST_OP_KILL_EVIDENCED switch in core+checker mirrors
  ST_OP_DELETE_STRONG (cite-consumption, rollback-mutating, replay-restore,
  replay-P3-clear, checker lineage). Exclusions (st_last_strength_idx,
  st_epoch_highwater) are by design, documented in MERGE_REPORT.
- ZNC CODEGEN NOTE: rt_redteam.zag full-driver builds show a deterministic
  diagnostic-print artifact in ck_verify_overwrite sections (e.g. A3 prints
  ck_ow_effort,4,4 + ck_ow_effort,1,1 instead of single ck_ow_effort,1,4).
  Isolated probes (probe2/probe3: verbatim rt_a3, small or single-call
  drivers) print the correct single line. Same artifact present in the
  committed forkA baseline (built from the same driver shape) — verdicts
  (cf values, all rc values) are unaffected and match baselines. Treated as
  a large-driver codegen quirk (ZNC-2026-09-21-015 family), not a logic defect:
  2× runs byte-identical, flagged/closed verdicts all correct.
- GATE logs saved: logs/gate_{B,C,CP3,B2}_{r1,r2}.log, all 2× identical,
  all ST_GATE f=0.

## Final source SHAs (2026-09-26)
- strength_core.zag: 5b2397f1a8f827e696217008c134f817b349cd7b9d640936c247248c594795fd
- strength_checker.zag: c0143d2b31b396812667681dda98fa9fb02b70464c32d43d9cc9c282a200da96
- strength_learner.zag: 13b7ada59f854d1f5dd2ff4b00fd98800ae062a7d0c32eac7f3f9349e38b9143
- strength_trial.zag: a08e2210b7f820cf533749182ac6d6d806321aef1d863a15c0c9639d61cecc2d
- r4val/trial/strength_core.zag: 47abc088cf565d946091554201ba2782c912a75dae65053a03a88d15e19fb542
- r4val/trial/strength_checker.zag: c0143d2b31b396812667681dda98fa9fb02b70464c32d43d9cc9c282a200da96
- r4val/del_attack.zag: 4b581dd7bf8cf25a0ed5872f457dd3dd12a2d079baff3309fa37e74eec1b519d

## Status: COMPLETE — no commit (coordinator commits).
