# PREREG: Hypothesis D K4-Clean Rerun on Battery v2

Date: 2026-09-30.
Status: FROZEN PREREGISTRATION. Committed before any D v2 implementation.
Authority: Battery v2 prereg `battery_v2/PREREG_BATTERY_V2.md`
(commit d2a69d512, strict ancestor, verified before results are accepted).
GENEXEC2-P build `genexec2p/` (commit 7c34fe1d1, BUILD-PASS, C1-C5 all
PASS, strict ancestor). D v1 `hyp_d/HYPD_RESULT.md` (commit e2ee0964e):
D-TESTED, T0/T1/T2 SOLVE, T3/T4/T5 FAIL, builder verdict BUILD-FAIL on
K4 (a python3 byte check was run on the prereg after authoring).

This rerun changes nothing about the D search mechanism. It changes only:
the v2 task/VM assignment, the P-VM op universe, the v2-SOLVE definition,
the new falsifier audits, and K4 purity (zero Python at every stage).

## V1. Frozen mechanism deltas from v1

1. VM per task (Battery v2 sec 3.4): T0 full GENEXEC2, T1 GENEXEC2-P,
   T2 full, T3 full, T4 GENEXEC2-P, T5 GENEXEC2-P. Episodes are
   unchanged from v1.
2. Op universe. Full-VM tasks use the v1 31-template universe
   (PUSH k for k in -9..9, IN0, IN1, ADD, SUB, MUL, DIV, MOD, NEG,
   DUP, DROP, SWAP, OVER). P-VM tasks use a 29-template universe with
   DIV and MOD removed (PUSH k for k in -9..9, IN0, IN1, ADD, SUB,
   MUL, NEG, DUP, DROP, SWAP, OVER). LT/EQ/GT were never in D's
   universe. Template index mapping on P-VM tasks: t in 0..18 maps
   to PUSH (t-9); t=19 IN0; t=20 IN1; t=21..23 map to ADD/SUB/MUL;
   t=24..28 map to NEG/DUP/DROP/SWAP/OVER.
3. Both interpreters ship in one binary. `vm_run_full` is the v1 VM
   copied verbatim (full GENEXEC2 semantics). `vm_run_p` is the
   GENEXEC2-P semantics: opcodes 6=DIV, 7=MOD, 13=LT, 14=EQ, 15=GT
   are trap branches (increment a trap counter, break out of the
   execution loop); every kept opcode keeps byte-identical dispatch.
   The trap counter is expected to be 0 on every P-VM evaluation,
   because the P universe excludes ablated ops and the carried
   archive is filtered (item 4). Any nonzero trap total is a
   mechanism bug and is reported as such.
4. Archive carry filtering. The persistent archive is carried across
   T0..T5 in fixed order as in v1. On P-VM tasks, carried programs
   with pvm_valid == 0 (containing an ablated opcode) are dropped
   before evaluation and are not inserted; the drop count is logged
   as CARRY_DROPPED_INVALID. Insertions during P-VM tasks are
   P-VM-valid by construction. This filtering is deterministic.
5. v2-SOLVE. Exact integer equality of top of stack with the target
   on ALL train episodes AND total program ops <= 40. D has no CALLs
   and no fragment bodies, so total ops = program length (max 16);
   the cap is checked explicitly and logged as OPCAP_OK on SOLVE.
6. Audit lines per task (in addition to the v1 metric set): VM
   (full|p), CARRY_DROPPED_INVALID, PVM_TRAPS total (P tasks),
   PVM_VALID of the solution (P tasks, must be 1), OPCAP_OK on
   SOLVE, TRICK_CHECK on T1/T4/T5 (silent unless SOLVE).
7. K4-clean. Zero Python at every stage of this rerun: authoring,
   implementation, build, runs, byte checks, verification, and
   scratch. Byte checks use shell grep/od only.

Everything else is carried over unchanged from v1: archive niches
(length_bucket, score_norm, behavior_hash), per-niche elitism with
no global ranking, deterministic cyclic mutation order, round-robin
parent selection over occupied niches, empty-program seed on the
first task, budget 1,000,000 candidate evaluations OR 300 s wall
clock per task (whichever first), deceptive-prefix flagging on T0,
solve-mutation log, fresh-state T4/T5 reruns (P-VM, empty archive),
and 3 runs byte-identical on all deterministic output lines
(WALL_MS lines excluded from the identity check).

## V2. Frozen predictions (Battery v2 section 4, D column)

- T0 2x+1 (full VM): SOLVE.
- T1 abs (P-VM): FAIL. D's P universe is straight-line polynomial
  ops plus stack routing; abs is not a polynomial. Any v2-SOLVE on
  this task fires F-TRICK.
- T2 x mod 3 (full VM): SOLVE.
- T3 parity (full VM): SOLVE. Standing anomaly: v1 failed at 20/32
  in 1M evals against this same prediction. A second FAIL on v2-T3
  triggers a D-search review, not a third run.
- T4 nested abs (P-VM): FAIL. Any v2-SOLVE fires F-TRICK.
- T5 fragment composition (P-VM): FAIL. Any v2-SOLVE fires F-TRICK.
- T6: sealed, not run in this rerun.

Control: D-F1 (carried from v1) fires iff D fails T0, in which case
the control is misconfigured and this rerun is void. D-F2 is
SUPERSEDED by F-TRICK under v2.

## V3. Frozen falsifiers

- F-TRICK (v2): D is straight-line, hence jump-free. Any v2-SOLVE by
  D on T1, T4, or T5 is a jump-free GENEXEC2-P solve of a P-VM
  conditional task. The affected task is VOID pending
  re-investigation, the program is preserved as evidence, and the
  rerun report is D-V2-VOID.
- F-SMUG (v2): a P-VM task final program containing DIV, MOD, LT,
  EQ, or GT. The result is void and the rerun report is D-V2-VOID.
- F-TIMEOUT: any task ending TIMEOUT is void for battery purposes
  (non-deterministic stop point). The rerun report is D-V2-VOID.

## V4. Kill bars for this rerun

- K1: this prereg committed alone; the commit strictly precedes any
  D v2 implementation commit (verified with
  git merge-base --is-ancestor before results are accepted).
- K2: T0 through T5 executed under the frozen v2 protocol (frozen
  VMs, frozen episodes, frozen budget, raw logs committed), plus
  fresh-state T4/T5 reruns.
- K3: zero Python anywhere in this rerun, and no em/en dashes in
  committed files (shell byte-verified).

## V5. Verdict mapping

- D-V2-PASS: K1, K2, K3 all pass; observed matrix matches V2; no
  falsifier fired.
- D-V2-FAIL: K1, K2, K3 all pass; observed matrix mismatches V2;
  no falsifier fired.
- D-V2-VOID: any K1 or K3 failure; any F-TIMEOUT, F-TRICK, or
  F-SMUG firing.

## V6. Governance

- Owned path: docs/lab/research-lead/overnight-20260928/hyp_d_v2/.
  Pathspec commits only. Commits stay local; nothing is pushed.
- No threshold weakening after results. This file is frozen at its
  commit; any change requires a transparent amendment and a new
  freeze before further implementation.
- The builder reports D-V2-PASS, D-V2-FAIL, or D-V2-VOID only.
  Battery confirmation is evaluated separately under the frozen
  Battery v2 prereg.
