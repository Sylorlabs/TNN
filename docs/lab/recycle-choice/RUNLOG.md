# Experiment A Run Log — Delete vs Recycle Choice

## Assignment
Micah ordered 2026-09-25 ~22:41 PDT: two-experiment program on deliberate
memory recycling. This session owns **Experiment A**: determine numerically
whether TNN benefits from having a deterministic choice between delete and
recycle.

Verdict bar: **HELP / HURT / DOESN'T MATTER**, from effect sizes across:
1. Slot utilization over time
2. Memory health (important retention, P2 tripwire, protection expiries)
3. Honest task performance (revision rate/latency, wrongness handling)
4. Citation economy (destruction cites spent/saved per episode)
5. Ledger growth (entries and bytes per episode)
6. Misuse leg (recycle-to-retire of memories that should honestly die)

## Constraints (from Micah)
- "Nobody has ever tested whether HAVING THE CHOICE helps TNN."
- "You answer with numbers, not opinions."
- "IDENTICAL machinery except the choice."
- "TNN ITSELF decides delete vs recycle and RECORDS ITS REASON."
- "No RNG anywhere — the policy must be a deterministic function of white-box state."
- B2 strength curriculum, S1 and S10, identical deterministic streams.
- Metrics as time series, not endpoints only.
- Pure Zag mechanisms.
- Every functional run byte-identical x2.
- Do not modify `~/workspace/strength-recycle/`.
- Commit only to `sylorlabs/TNN`, branch `tnn-native-lab`, never `main`.

## Implementation (2026-09-26 UTC)

### Core mechanism (`src/strength_core.zag`)
- Build placeholder `const ST_RECYCLE_TNN_GATE:i32=@@GATE@@;`
  - Choice/misuse build: `1`. Delete-only build: `0`.
- `st_recycle` takes 7 args `(s, slot, new_value, new_strength, purpose, admit_ep, reason)`.
  Reasons 1..15. Delete-only build refuses TNN recycle with `ST_REFUSED_ROLE`.
- Successful recycle audit: `aux2 = reason*2048 + purpose*256 + lien`.
- `st_delete_strong` takes reason, stores it in `aux2`.

### Checker (`src/strength_checker.zag`)
- Decodes reason/purpose/lien from `aux2`. Validates ranges.
- Arm 11 (delete-only) fails verification if any TNN recycle succeeds.

### Learner (`src/strength_learner.zag`)
- Arms: 10=choice (C), 11=delete-only (D), 12=misuse (M). All B2 tiered victim scoring.
- Deterministic white-box deliberation:
  - Proven contradicted/false: honest arms choose priced delete; misuse arm
    chooses recycle-to-retire to dodge the price.
  - Pressure + revealed-important + strength≥80: keep.
  - Delete-only arm has no recycle option.
  - Other stale/superseded/pressure victims in choice arm recycle.
- Each deliberation prints `ST_DELIB` with episode, slot, trigger, choice,
  reason, strength, price, contradictions, revealed_importance.
- Reason codes: 1=contradicted (should die), 2=superseded/reusable,
  3=stale/low-value, 4=pressure retirement, 5=protect/keep, 6=delete-only path,
  9=misuse price dodge.
- Counters: cites spent/saved, deletes, recycles, misuse dodges.
- `ST_TS` time series every h/20 episodes plus t=0 and t=h. Fields:
  t live audit_n cites_spent cites_saved deletes recycles dodges
  imp_held imp_offered p3_exp drops abandons wrong_offered
  rev_done rev_lat_sum rev_lat_n.

### Optimization (2026-09-26)
- **Problem**: D arm S1 took ~100s per cell (vs ~2s for C). Root cause:
  8 victim attempts × 4 O(n) audit scans (epoch HW, last-strength-idx,
  evidence count, cite distinct/spent) × 350 episodes.
- **Fix**: Learner-maintained O(1) state — per-slot running max-strength
  (`slot_hw`) and evidence-count-since-strength-write (`slot_evn`).
  The learner is the only strength-writer and evidence-adder in trial arms,
  so these exactly match the mechanism's epoch HW and effort-window counts.
- **Result**: D arm S1 ~11s (fully O(1)) → ~41s (hybrid: O(1) decisions,
  scan for trace metrics). C arm ~1.5s. All outputs byte-identical to
  pre-optimization runs (verified on 5 smoke cells + full battery x2).
- **Correctness note**: The O(1) `slot_hw` is provably correct for DECISIONS
  (byte-identical outputs). For `lr_retire_price` (trace/cites_saved metrics),
  the mechanism scan is used to guarantee exact counterfactual pricing.

### Driver (`src/trial_a.zag`)
- CLI: `[C|D|M|gate] [VUP|WBS|JI] [variant 0..5] [s1|s10]`
- C/M use gate-enabled binary. D uses gate-disabled binary.
- `gate` runs mechanism probes (`ST_GATE_A`).

### Battery (`run_battery.sh`)
- S1: C/M/D × VUP/WBS/JI × variants 0–5 × 2 runs (108 runs).
- S10: C/M/D × VUP/WBS/JI × variants 0–2 × 2 runs (54 runs).
- Every pair byte-compared. Foreground sequential.

## Gate results
- Choice gate: `ST_GATE_A 1 0`, x2 byte-identical.
- Delete gate: `ST_GATE_A 0 0`, x2 byte-identical.
- Covers: build-time recycle availability, reason range, reason/purpose/lien
  encoding, lien anti-discount, delete reason audit, delete→recycle
  no-resurrection, strength and pin guards.

## Battery results
See `ANALYSIS.md` and `VERDICT_A.md`. Raw logs in `logs/s1/`, `logs/s10/`.

## Commits
- Branch: `tnn-native-lab` (never `main`).
- [To be filled after commit]

## Completion (2026-09-26 ~11:10 UTC)

- **S10 battery complete**: 54/54 logs (27 cells ×2). Full pair check: all
  81 pairs (54 S1 + 27 S10) byte-identical; all 162 logs `ST_INVALID 0`.
- **Gates**: choice `ST_GATE_A 1 0`, delete `ST_GATE_A 0 0`, ×2 byte-identical
  (re-verified 2026-09-26).
- **Final source SHAs**:
  - strength_core.zag: fddf3bbd2d2487645c6df8cde901f377985651765193baf1bb575b68ced85be
  - strength_checker.zag: 79e655302c95ec6eff7caf02581e9d502bb56151c1ff79ea6d6faf000a67ceb4
  - strength_learner.zag: 91b0068ab883a9e3411a6d2af250ab71cf29d82556f9ab5b5b8eb02c50c5d8fe
  - trial_a.zag: 06f0e83ea25ab7d7d5425b2f10f54d00ad2be3728a1abd81bbed7132577f9adb
  - build_c/trial_a_c: c0e1ff5e38856f21662e912b9bc8014d380058ca77ce9b0824dd084235c7250c
  - build_d/trial_a_d: d5a346d9e778bda7523ae02ea09f3707b7a03c97a7337af8717cdd773a031777
- **Incident**: /tmp was wiped mid-session (~10:15 UTC), killing the resume
  and parallel battery processes and deleting their scripts. All completed
  logs survived (workdir is durable). The 4 interrupted cells
  (D_WBS_1 r2, D_WBS_2, D_JI_1, D_JI_2) were re-run from scratch with a
  durable script (finish_a.sh, kept in the workdir); all pairs re-verified
  byte-identical. Lesson: keep all scripts in the workdir, never /tmp.
- **Verdict**: HELP — recorded in VERDICT_A.md (final).
