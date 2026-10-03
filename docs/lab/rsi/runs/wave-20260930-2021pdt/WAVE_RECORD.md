# Wave record: wave-20260930-2021pdt

INCOMPLETE as of wave start; will be marked complete or INCOMPLETE at wave end.

Run-start tip: f9b2d999f. Lock written 20:21:54 PDT Wed 2026-09-30
(the scheduler wrote it at wave start; this run's own lock).
Local branch tnn-native-lab is 1767 commits ahead of
origin/tnn-native-lab; origin is 0 ahead; no merge needed, no
reset, no rebase.

Previous wave 20260930-1721pdt died on the descendant-subagent
runtime defect (ninth kill; four of the last five waves dead) and
rendered no verdicts. Its recovery commits preserved:
b42b10db5 / 448ec4ae1 / 886b8cdcc / a004459e2.

11:21 recovery debate standing verdicts (commit caf07be92),
carried as this wave's queue seeds:
- M1 F3a3 ADOPTED with bar-text caveat (bar-text addendum queued)
- M2 F3b ADOPTED narrowed to drop-last L2+ (f3b_len evidence at
  886b8cdcc)
- M3 H-EXP2 v2 prereg FROZEN with audit precondition (ready to
  implement this wave)
- M4 DDES R2 PROVISIONAL pending independent re-verification of
  K-R2.1..K-R2.6 (implementation b42b10db5)

Wave coordinator: subagent for the parent (main) agent. It fans out
about 10 lane workers plus red-team review, replacing completed
workers with the highest-information queued work. If the descendant
defect kills lanes, the mandatory debate runs INLINE by the
coordinator (advocate/skeptic/judge with provenance probe) and is
recorded here and in LOOP_STATE.md. No verdict ships un-debated.

Lane directory map (all under docs/lab/rsi/runs/wave-20260930-2021pdt/):
- fork_battery: enumerate every local+remote branch/fork, frozen
  test battery, per-fork PASS/FAIL
- exp2: H-EXP2 v2 implementation (frozen prereg from 11:21, audit
  precondition satisfied)
- ddes_r2_verify: independent re-verification of DDES R2 kill bars
  K-R2.1..K-R2.6 (M4 PROVISIONAL resolution)
- ddes_followup: DDES schema-persistence follow-ups
- devang2: DEVANG2 retry (DEVANG1 BUILD-FAIL on training crash)
- f1_execsem: F1 generic executable semantics builder (highest
  frontier priority)
- arena: arena composition workstream toward 1.0 from clean 0.573
  baseline
- sensory: SENSORY HEADSPACE realism levers (no micro-grain tweaks;
  human eyes outrank metrics; sealed A/B if candidate ready)
- trades: INTELLIGENCE TRADES expensive candidate with frozen kill
  bars
- gov: governance/red-team reviewer (commit-order self-check
  support, contamination scan, second opinions on lane candidates)

Documentation rule: no em dashes in any loop documentation. Use
colons or parentheses. Byte check via
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
(shell only; never python3 for byte checks).

All work is pure Zag. Toolchain guard: every worker activates the
safebin (docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh)
and records `which python3` returning empty in its lane NAMECHECK.md
Step 0. If a forbidden executable is invoked, that lane is
PROCESS-FAIL.

Status: lanes spawning at wave start. Verdicts recorded below when
debated.
