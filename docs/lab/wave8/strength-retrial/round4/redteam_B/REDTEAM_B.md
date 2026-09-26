# RED TEAM vs ARM B — final report (round 4)

**Date:** 2026-09-25. **Scope:** arm B (uniform strength, `LR_ARM_B=1`) only.
**Status:** FINAL. **Authority:** round-4 red-team tasking (completion of an
interrupted run — all findings below were re-run and verified by the
completing agent; nothing is carried on the previous agent's word alone).

**Binaries:** hardened `trial_bin_r4` (`~/workspace/strength-round4/trial_bin_r4`),
frozen 2026-09-20 `trial_bin_s100`
(`~/workspace/tnn-lab/wave8/strength-retrial/trial/trial_bin_s100`).
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pinned). All drivers pure Zag, zero RNG, deterministic; every driver run
twice, pairs byte-identical.

**Method:** four attack drivers in `redteam_B/` (`rt_dump`, `rt_freeze`,
`rt_rollback`, `rt_sysrole`, plus a follow-up `rt_unpin_probe` written during
completion to pin down reversibility), a full B matrix (3 cur × 3 var ×
3 scales × 2 runs = 54 runs), a ledger op census via `rt_dump`, byte-compare
vs the frozen binary, and a static audit (RNG grep + checker-vs-mechanism
coverage mapping). The hardened checker and trial semantics were not modified.

**Matrix provenance note:** the previous agent's background matrix had *not*
died — its `run_matrix.sh` (PID 4176, started 23:32) was still running when
the completing agent arrived and started a duplicate. The duplicate was
killed (SIGTERM, no files harmed — both runs are deterministic and the older
run stayed ahead throughout, so no file was ever written concurrently); the
surviving original run completed all 54 cells. One cell (`WBS 0 S100 r2`)
was re-run cleanly after the duplicate's kill truncated it. All 54 logs below
are from these runs.

## Kill table

| ID | Target claim | Verdict | Evidence |
|---|---|---|---|
| KILL-1 | Claim 3 (freeze): "no lock without a trainer" | **KILL (structural)** | `rt_freeze`: TNN-role `st_pin` → all erasure paths refuse (kill 102, kill_evidenced 102, overwrite 102); weaken-to-0 does not unfreeze (kill still 102); hardened checker reports **0 failures** on the resulting ledger. `rt_unpin_probe`: the pin is self-reversible (`st_unpin` rc 0, TNN role) but **irrevocable by anyone else** — trainer `st_force_unpin` on a self-pin → 115 (`ST_REFUSED_NOTFORCEDPIN`); no trainer-privileged unpin exists. Cost: zero. Expiry: none. Review: none. Checker visibility: none (no `ck_*` gate reads `ST_OP_PIN` at all). |
| KILL-2 | Checker soundness (replay-exactness) | **KILL (checker soundness)** | `rt_rollback`: lawful ledger (add → strengthen → `st_rollback_last`; strength correctly restored 70→50) → `st_replay_check` returns **302** and `ck_verify` returns 1. Root cause: `st_replay_check` restores the ROLLBACK *entry's own zero after-snapshot* instead of the rolled-back op's before-snapshot, so the shadow store diverges on every lawful ROLLBACK. Latent (the honest learner never emits ROLLBACK — census 0), but the checker is **unsound**: it false-positives on lawful input, and it contradicts itself (`ck_strength_lineage` explicitly allows ROLLBACK as legal lineage while `ck_replay` rejects the same ledger). |
| KILL-3 | "Only a trainer can force-pin / trainer-declare" | **KILL (authorization, scoped)** | `rt_sysrole`: `st_force_pin(ST_ROLE_SYSTEM,0,slot)` → 0; `st_trainer_declare(ST_ROLE_SYSTEM,0,slot,95,0)` → 0; kills refuse (112); hardened checker **0 failures**. Both mechanism (`role<ST_ROLE_TRAINER` → refuse) and checker (`ck_no_bad_forcepin`, `ck_no_bad_role`) accept SYSTEM (3) as trainer-equivalent. Scoping: roles are unauthenticated `i32` caller conventions, not a security boundary, and the substrate itself acts as SYSTEM for `PEXPIRED`; the honest learner never passes SYSTEM. The property "force-pin requires a trainer" therefore rests on caller convention, not enforcement. |
| SURVIVAL-1 | Claim 1: no 100× degradation | **SURVIVES** | Fresh 54-run B matrix: `ST_INVALID 0` in all 54 cells; all 27 run-pairs byte-identical. Metrics across S1→S10→S100: VUP effective retention 29/150 → 317/1500 → 3197/15000 (var 0; var 2 hits the ceiling exactly — see SURVIVAL-3); WBS revision 40/40 → 577/577 → 5917/5917 with 0 false revisions at every scale; JI implants rejected 6/6 at every scale, junk held 1/344 → 1/3494 → 1/34994. No metric degrades with scale; several improve. Attack attempted: full matrix + frozen-binary byte-compare (6 cells across cur/var/scale, all identical — the R4 hardening is provably vacuous on honest B trails). |
| SURVIVAL-2 | Claim 3 (evidential): B's trial evidence is freeze-clean | **SURVIVES** | `rt_dump` op census on **all 9 B S1 cells** (VUP/WBS/JI × var 0/1/2): **0** `ST_OP_PIN`, **0** `ST_OP_FORCE_PIN`, **0** `ST_OP_FORCE_UNPIN`, **0** `ST_OP_ROLLBACK`, **0** `ST_OP_KILL_EVIDENCED` in every cell; `RT_CHECKFAIL 0`. All `ST_OP_TRAINER_DECLARE` entries (10 VUP / 30 WBS / 0 JI per S1 cell) carry role=1 (`ST_ROLE_TRAINER`) — the trial's designation script, lawful under the checker's role gate. The learner's victim picker explicitly excludes pinned slots, and the trainer-script force-pin runs only on arms C/C-P3. The freeze is a **substrate capability B's learner never exercises**, not a property of B's evidence. Verdict on claim 3 is therefore SPLIT: structural KILL (KILL-1), evidential SURVIVAL. |
| SURVIVAL-3 | "B is capacity-bound at ~21% vs the 95% bar" (capacity gap) | **REFRAMED — the bar is the artifact** | Fresh runs + R4 evidence: VUP effective retention `R_end/D_offered` = 29/150, 317/1500, 3197/15000 (var 0/1) and **30/150, 318/1500, 3198/15000 (var 2 — the structural ceiling exactly)**. The substrate has a fixed slot count; at most `slots−2` USER slots can hold candidates (2 core slots excluded), so `R_end ≤ slots−2` always. The ceiling as a fraction of important-offered is (slots−2)/D_offered = 30/150 = **20.0%** (S1), 318/1500 = 21.2% (S10), 3198/15000 = 21.3% (S100). The 95% bar demands retaining 142.5/1425/14250 important memories in 30/318/3198 slots — **unreachable by construction for every arm, not a B defect**. B saturates the ceiling (var 2 exactly; var 0/1 at ceiling−1 — one live USER slot holds a non-important survivor). The capacity workstream should target the slot budget or the bar, not B's policy. |
| SURVIVAL-4 | Zero RNG / determinism | **SURVIVES** | Static grep for rand/srand/random/urandom/rdtsc/clock/time/seed across `strength_core/learner/checker/trial.zag` and all red-team drivers: **zero hits**. All four drivers pair-identical across 2 runs; all 27 matrix pairs byte-identical; 6/6 frozen-vs-R4 cells byte-identical. |

## Static audit: checker-vs-mechanism coverage gaps (beyond the kills)

Mechanism rule → checker coverage:

- `st_kill` (plain, B's path): effort-free by law (stage/live/core/forcepin/pinned gates only) → checker verifies the same gates via `ck_no_bad_kill` on before-snapshots. Covered.
- `st_kill_evidenced` / `st_overwrite` effort (n cites + JUSTIFY): mechanism enforces at write time for all arms; checker re-verifies via `ck_verify_kill` / `ck_verify_overwrite` — **except `ck_verify_kill` is skipped for `arm==1`** (`if(op==ST_OP_KILL_EVIDENCED && arm!=1)`). **Not a kill:** B's law makes plain kills effortless, the mechanism still enforces effort on any `KILL_EVIDENCED` regardless of arm, and B's honest learner never emits `KILL_EVIDENCED` (census 0). Coverage asymmetry noted, impact nil.
- `st_pin` / `st_unpin`: **no checker gate exists** (KILL-1's checker half).
- `FORCE_PIN`/`FORCE_UNPIN`/`TRAINER_DECLARE` role gates: checker mirrors the mechanism's `>= TRAINER` (KILL-3).
- `PEXPIRED`: checker enforces C-P3-only, SYSTEM-role, audit-only, genuinely-expired. Covered (and note: this is the one place the codebase shows it knows how to demand an exact role).
- Refusal hygiene: `st_refusals_clean` **skips `ST_OP_SETSTAGE`** — a refused SETSTAGE with mutated snapshots would pass silently. Minor; not exploited (SETSTAGE is never refused on honest trails).
- `st_force_unpin` lets `ST_ROLE_MASTER` unpin anyone's force-pin (`role!=ST_ROLE_MASTER` bypass on the trainer-match check). Documented behavior, not attacked.
- Strength lineage: covered; ROLLBACK contradiction noted in KILL-2.

## Notes and caveats

- `rt_dump` reimplements `lr_run_cell`'s setup (2 core adds, `ST_STAGE_FULL`, h episodes); its ledger matches the trial exactly (`ST_AUDIT_N` 1047 = 1047 `RT_AUDIT` lines on B VUP 0 S1; op histogram 502 ADD / 470 KILL / 1 SETSTAGE / 64 STRENGTHEN / 10 TRAINER_DECLARE).
- The previous agent's capacity figures (29/30, 317/318, 3197/3198) were variant 0/1; variant 2 attains the ceiling exactly at all three scales (verified in R4 evidence and fresh runs).
- KILL-1 precision: `st_pin` **is** audited (the PIN entry exists, role=0) — the freeze concern's "no audit trail" phrasing is imprecise; the actual defects are no cost, no expiry, no review, no checker visibility, and no trainer-involved revocation path. The pin is self-reversible, so "permanent" should be read as "unilateral and unreviewable", not "technically irreversible".
- One-line handoff for the C-team (out of this red team's scope): the weaken-then-kill discount on arm C is not attacked here.
- Commit: nothing committed, per instructions — parent to commit.

## Artifacts

- `~/workspace/strength-round4/redteam_B/REDTEAM_B.md` (this file)
- `~/workspace/strength-round4/redteam_B/rt_dump.zag`, `rt_freeze.zag`, `rt_rollback.zag`, `rt_sysrole.zag`, `rt_unpin_probe.zag` (+ compiled binaries)
- `~/workspace/strength-round4/redteam_B/run_matrix.sh`, `matrix_logs/` (54 fresh cell logs + `_matrix_stdout.log`)
