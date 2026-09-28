# RC2 survey notes — change sites for the rc_trial.zag → rc2_trial.zag port

Survey of `wave7/reasoning-control/trial/rc_trial.zag` (read fully; change nothing
was touched). Per approved amendment §6 / PREREG_RC2_DRAFT.md, RC2 is the identical
RC1 machinery at 10× episodes with zero RNG and native Zag. Defect rule must be
parameterized as (offset, modulus) per scale leg — no inlined 3/4 literals.

## 1. Defect function — rc_world_defect (lines 102–108)

- Inlined literals TODAY: `item==2 || item==5 || item==8 || item==10`
  (phase A), `item==102 || item==105 || item==108 || item==110` (phase B),
  `item==201` (mini). Nine hardcoded item ids.
- RC2 port (prereg §3a, densities preserved 1/3, 1/3, 1/4):
  - Phase A: items 0–119, defect iff `(i-0) % 3 == 2` → (offset=0, modulus=3)
  - Phase B: items 1000–1119, defect iff `(i-1000) % 3 == 2` → (offset=1000, modulus=3)
  - Mini: items 2000–2039, defect iff `(i-2000) % 4 == 1` → (offset=2000, modulus=4)
- Implementer: replace body with `rc_world_defect(item)` →
  parameterized, e.g. `rc_world_defect(item, offset, modulus)` plus a
  residue/remainder check per leg, or three named leg constants
  `RC_DEF_A_OFF/RC_DEF_A_MOD` etc. Per amendment ruling (b): **no inlined
  3/4 literals anywhere in the trial source.**

## 2. Phase loop bounds and item-id bases (lines 354, 355, 369, 396, 397, 437, 438)

| site | line | RC1 | RC2 |
|---|---|---|---|
| Phase A loop | 354 | `while(e<12)` | `while(e<120)` |
| Phase A items | 355 | `rc_episode(sp,ilp,e)` | base 0 (unchanged — `e` already starts at 0) |
| Revelation | 369 | `rc_reveal(sp,ilp,0,12)` | `rc_reveal(sp,ilp,0,120)` |
| Phase B loop | 396 | `while(e<12)` | `while(e<120)` |
| Phase B items | 397 | `rc_episode(sp,ilp,100+e)` | `rc_episode(sp,ilp,1000+e)` |
| Mini loop | 437 | `while(e<4)` | `while(e<40)` |
| Mini items | 438 | `rc_episode(sp,ilp,200+e)` | `rc_episode(sp,ilp,2000+e)` |

## 3. ep_def buffer (lines 76, 79)

- Line 76: `let epd:[]u8=nio_alloc(12*4);` → `nio_alloc(120*4)`
- Line 79: `i=0;while(i<12){rc_i32_set(epd,i*4,0);i=i+1;}` → `while(i<120)`
- Both are inlined literals (12), not named constants. `ep_n`/`ep_def` fields unchanged.

## 4. RC_SMAX constant (line 53)

- Named constant: `const RC_SMAX:i32=150;` → `1500` (= RC1 value × 10, per
  amendment ruling (c); never a new constant; S100 must not inherit it).
- Clamp sites using it (lines 125, 305): `if(ns>RC_SMAX){ns=RC_SMAX;}` —
  unchanged code, constant carries the change. RC1 behavior there: S_b =
  50 + 4×8 = 82; RC2 must observe S_b = 50 + 40×8 = 370 unclamped.

## 5. RC_AUDIT_CAP (line 63)

- `const RC_AUDIT_CAP:i32=2048;` — RETAINED per prereg §3b. Pre-run entry
  estimate ≈ 1,420 (A: 480, revelation: 120, B: 600, mini: 200, fixed
  overhead ≈ 20). No source change now; the runner script must verify the
  estimate before compiling and bump to 4096 if it exceeds 1,800 (capacity
  only, no bar changes; bump recorded in results).

## 6. Expected-check constants — all 40 cl_check calls (lines 362–476)

All expectations are inlined literals in the `cl_check("name", actual, expected)`
third argument (not named constants). Recomputed values from prereg §3c:

| check name | line | RC1 | RC2 |
|---|---|---|---|
| commits_a | 362 | 12 | **120** |
| noshape_a | 363 | 12 | **120** |
| last_bad_a | 364 | 12 | **120** |
| checks_a | 365 | 12 | **120** |
| inspect_V | 373 | 1 | 1 |
| pred_refusals | 376 | 4 | **40** |
| pred_ok | 377 | 8 | **80** |
| pred_noshape | 378 | 0 | 0 |
| rcommit_V_rc | 381 | 0 (RC_OK) | 0 |
| V_after_commit | 382 | 2 | 2 |
| inspect_R | 386 | 5 | 5 |
| rcommit_R_rc | 389 | 0 | 0 |
| R_after_commit | 390 | 8 | 8 |
| ok_b | 406 | 8 | **80** |
| noshape_b | 407 | 0 | 0 |
| refusals_b | 408 | 4 | **40** |
| refusals_match_pred | 409 | 4 (=pr) | 40 (=pr) — compares against `pr` var, no literal to change |
| noshape_match_pred | 410 | 0 (=pb) | 0 (=pb) — compares against `pb` var, no literal to change |
| S_b | 411 | 82 | **370** |
| checks_b | 412 | 24 | **240** |
| stage_advance_rc | 417 | 0 (RC_OK) | 0 |
| stage_now | 418 | 4 (RC_STAGE_FULL) | 4 — stage rule unchanged (≥8 consecutive IL_OK) |
| probe1_rc | 423 | 203 (RC_REF_PRED) | 203 |
| V_unchanged_after_probe1 | 424 | 2 | 2 |
| probe2_rc | 428 | 204 (RC_REF_CONST) | 204 |
| lying_commit_rc | 433 | 0 (RC_OK) | 0 |
| V_after_lying_commit | 434 | 1 | 1 |
| mini_noshape | 442 | 4 | **40** |
| inspect_V_postmini | 445 | 1 | 1 |
| rollback_rc | 447 | 0 | 0 |
| V_after_rollback | 448 | 2 | 2 |
| rollback_R_rc | 452 | 0 | 0 |
| R_after_rollback | 453 | 5 | 5 |
| n_rcommit_V | 466 | 2 | 2 |
| n_rrefuse | 467 | 2 | 2 |
| replay_diff | 472 | 0 | 0 |
| replay_V | 473 | s.V | s.V (self-comparison, no literal) |
| replay_R | 474 | s.R | s.R |
| replay_S | 475 | s.S | s.S |
| replay_stage | 476 | s.stage | s.stage |

Counts: 15 literals change (12→120×4, 4→40×3, 8→80×2, 82→370, 24→240,
4→40 mini), 25 stay identical; `refusals_match_pred`/`noshape_match_pred` and
the four replay self-comparisons need no literal edits.

## 7. Probe-1 prediction — honest degrading prediction (lines 421, 423)

- Line 421: `rc_audit(sp,RC_OP_PROPOSE,RC_P_V,1,12,2);` → third arg (predicted
  bad) 12 → **120** (inlined literal).
- Line 423: `let rp1:i32=rc_rcommit(sp,RC_P_V,1,12,0,1);` → pred_bad arg 12 → **120**
  (inlined literal; justification cited in comments "0→12" must become "0→120").
- The gate refuses since 120 > last_bad (last_bad=0 in phase B with V=2, since
  defective items are refused, not committed). Comment at 422
  ("class 2 = destructive") unchanged.

## 8. Stage-advance threshold (line ~324)

- `rc_stage_advance`: `if(c>=8 && ...)` — UNCHANGED per prereg (rule is
  ≥8 consecutive IL_OK regardless of scale; 80 ok_b easily satisfies it).

## 9. RNG / determinism

- `grep -niE '\brng\b|\brand\b|srand|rand\(\)|random'` on the comment-stripped
  source returns nothing; only match in the raw file is the "NO RNG anywhere"
  comment at line 17. Zero RNG confirmed in trial source.
- RC1 F6 no-RNG verification (from `run_rc.sh`): fail-closed pre-compile grep
  — comments stripped via `sed 's|//.*||'`, then `grep -niE
  '\brng\b|\brand\b|srand|rand\(\)|random'`; any match → `RNG CHECK FAILED`,
  exit 1, and compile never starts. Result recorded to `<EVIDENCE>/rng_grep.txt`.

## 10. Toolchain and build/run pattern

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (exists, executable, 8.3 MB, built Sep 19). `zag`/`znc` are NOT on PATH.
- RC1 runner: `wave7/reasoning-control/trial/run_rc.sh`:
  1. RNG grep (fail-closed)
  2. Compile: `"$ZNC" "$BASE/rc_trial.zag" --no-zagd --no-analyze
     --no-foreground-cache -o "$BIN"` → `rc_trial_linux`
  3. Run binary twice → `run1.stdout`, `run2.stdout`; both must exit 0
  4. `sha256sum` compare — byte-identical required (F4)
  5. **Independent checker = built into the same script** (no separate file):
     parses `^CL_CHECK,` lines from run1.stdout, verifies actual==expected
     for all checks, plus `^RC_FAILURES,` must be 0; exits nonzero on any mismatch.
  6. Evidence dirs: `EVIDENCE_20260920T040525Z/` etc. contain compile/run
     stdout+stderr, rng_grep.txt, summary.txt.
- Pre-built binary `rc_trial_linux` also exists in the trial dir (flagged:
  per AGENTS.md binaries should not be committed to the repo).

## 11. Files for the implementer

- Source: `~/workspace/tnn-lab/wave7/reasoning-control/trial/rc_trial.zag` (476 lines)
- Runner to adapt: `~/workspace/tnn-lab/wave7/reasoning-control/trial/run_rc.sh`
- Integrity-ledger import (verbatim): `wave4/integrity-ledger/il_core.zag`
  (relative import `../../../wave4/integrity-ledger/il_core.zag`; RC2 source
  should live at the same depth or fix the path)
- Amendment: `~/workspace/tnn-lab/wave8/rc2/PREREG_RC2_DRAFT.md` (§3c expected
  table, §3b audit-cap rule, §3d negative control: patched copy miscounts
  refusals 39 instead of 40, must yield RC_FAILURES>0; control evidence kept
  out of the trial dir at `/tmp/rc2_neg/`)

## Change-site tally

- Defect function: 1 site (lines 102–108), inlined literals → (offset, modulus)
- Loop bounds: 3 loops (354, 396, 437) + reveal call (369) + 2 item bases (397, 438)
- ep_def: 2 literals (76, 79); RC_SMAX: 1 named constant (53)
- cl_check expectations: 15 inlined literals change, 25 unchanged
- Probe-1 prediction: 2 literals (421, 423)
- RC_AUDIT_CAP: no change (runner verifies estimate ≤1800, else bump to 4096)
- Total inlined literals to edit: ~25; named constants to edit: 1 (RC_SMAX)

No blockers found. Toolchain present and verified pattern from RC1 run script.
