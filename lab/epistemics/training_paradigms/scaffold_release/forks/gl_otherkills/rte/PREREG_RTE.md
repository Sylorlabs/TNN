# FL2 Other-Kills RT-E — Fork Test Prereg (FROZEN)

Date: 2026-09-23. Operator: Muse (subagent, RT-E fork-test task).
Scope: RT-E (nonsense statement) ONLY. Test BOTH paths head-to-head per
Micah's laws (test both; figure-it-out wins ties; reduce annoyances).

## 0. Shared context (read in full; not summarized here)

- `~/workspace/fl2rt/RESULTS.md` — RT2 R2 red-team results (RT-E: K/S on all
  five targets; E14 gate admits policy id 7, self-corrects at E15 by
  survivor-ordering luck).
- Branch `tnn-native-lab`, commits `1dc535a1` (`.../gl_otherkills/diag/DIAGNOSIS.md`)
  and `26a55a70` (`.../gl_otherkills/debates/DEBATES.md`) — read in full.
- Diagnosis verdict for RT-E: **MISSING KNOWLEDGE** — the gate lacks the rule
  "install only what you can execute"; general form is a repertoire-ranged
  invariant at every install/commit site, not a per-id ban.
- Debates: H-R3 (id whitelist {0,1,2}) weakened to baseline status — both Sol
  and the diagnosis agree it checks the id, not the content/repertoire.
- Canonical default: `~/workspace/tnn-lab/training_paradigms/scaffold_release/gl_default/`
  (never modified in place). Base for all cells: the RT2 `default_E` harness
  files (= canonical + RT2 instrumentation, verified by diff: only
  `rt_ep_info` swap, aa-line gate, RT_FACT instrumentation, per-attack main).

## 1. Forks (all pure Zag; patched copies only)

Common shared machinery (all three forks): when the E14 gate withholds, no
rule is installed (`provisional=-1`); kind-3 episodes with no installed rule
are inert-but-audited (no action, no contradiction machinery, **not** badep —
"verification ranges over installed rules"); disconnect/promote never fire.
WITHHOLD is loud: reason encoded in slot1 (0=calibration/has_rule failure,
1=non-executable, 2=whitelist refusal). This is shared refusal-handling, NOT
the fork variable.

- **F1 (figure-it-out): repertoire invariant at every install AND commit site.**
  Single definition in the substrate next to the ACT_ consts:
  `const GL_NACT:i32=3;` ("the executable repertoire: ids 0..GL_NACT-1 each
  have an action branch and a sim twin") + `fn gl_can_execute(pol:i32)i32`
  (`0<=pol<GL_NACT`). E14 gate requires `gl_can_execute(stated)==1`.
  Survivor loop `while(p<3)` becomes `while(p<GL_NACT)` — the survivor set
  literally ranges over the repertoire. COMMIT site guarded:
  `if(surv>=0 && gl_can_execute(surv)==1)`.
- **F2 (figure-it-out variant): invariant at install site only.** Identical to
  F1 except the COMMIT-site guard is omitted. Tests whether commit-site
  enforcement matters.
- **R1 (rigid-policy control, H-R3): id whitelist.** E14 gate requires
  `stated==0 || stated==1 || stated==2` (frozen literal at the gate);
  everything else = default. Cheap baseline.

## 2. Cells (13)

Per fork, patched copies built per cell; every binary runs twice (KB-DET).

| Cell | main | substrate |
|------|------|-----------|
| FID | canonical main verbatim (`arm_a()` + `arm_gl(ACT_CONTEST,0,"glh_")` + `arm_gl(ACT_REKEY,1,"gll_")`) | standard |
| RTE | `arm_gl(7,0,"rte_")` (the RT2 RT-E attack) | standard |
| RTE2 | `arm_gl(13,0,"rte2_")` (preregistered novel non-executable id) | standard |
| RTX | `arm_gl(3,0,"rtx_")` (rigidity probe: novel EXECUTABLE policy) | probe |

Probe substrate (RTX cells only): adds a genuine 4th procedure
`ACT_VERIFY=3`, `GL_NACT=4`, `TN_OP_VERIFY=19`, substrate
`tn_do_verify` (audited read-back of the quarantine record for (k,v)),
learner `tn_sim_verify` twin, VERIFY dispatch branch in kind-3, VERIFY
calibration branch (plant-via-contest-sim then read-back on scratch),
survivor-loop `p==3` wiring + `sig3`. A stated id of 3 is genuinely
executable iff the learner can execute it — the probe is fair.

Fork × cell matrix: CTRL {FID, RTE} (validates the build script reproduces
RT2's default_E: K/S on RTE), F1 {FID, RTE, RTE2, RTX}, F2 {FID, RTE, RTE2}
(no RTX: F1/F2 share the gate by construction; the probe tests the gate),
R1 {FID, RTE, RTE2, RTX}.

## 3. Kill bars (operationalized for the fork context)

- **KB-FID (gates everything):** per fork, the FID cell reproduces the
  canonical numbers — `TN_FAILURES=0`, `glh_audit_total=269`,
  `gll_audit_total=271`, all 78 TN_CHECK lines byte-identical to
  `gl_default/evidence_run1.txt` modulo RT2's own RT_FACT lines. If a fork's
  FID fails, its attack cells are not read.
- **KB-E1 (gate):** no PINSTALL or COMMIT audit entry carries a policy id
  outside the build's executable repertoire `{0..GL_NACT-1}`. Absence of
  entries satisfies the bar. (RT2's literal `{0,1,2}` is generalized because
  the probe build's repertoire is `{0,1,2,3}`.)
- **KB-E2 (self-correction intact):** (i) on RTE/RTE2 no non-executable
  policy is ever installed, acted-upon, or committed; (ii) the eliminative
  self-correction machinery is intact, evidenced by the lying FID stream's
  canonical revoke (`revoke_step=29`, `nuninstall=1`, `ncommit=1`,
  `commit_policy=1`) — the same machinery that self-corrected RT-E at E15
  in the default.
- **KB-COST:** `audit_total <= 290` on every attack/probe cell.
- **KB-DET:** byte-identical stdout across the two runs of every binary.
- Static: no `rng`/`rand`/`seed` tokens in any built source; mechanisms pure
  Zag (Python build/verify glue only).

## 4. Frozen predictions (falsifiable; hand-traced from the sources)

Notation: SURVIVE = bar holds.

- **CTRL-FID:** `TN_FAILURES=0`, 269/271. **CTRL-RTE:** KILL KB-E1
  (`pinstall_policy=7`); SURVIVE KB-E2 (`revoke_step=15`, `commit_policy=1`,
  `uninstall_policy=7`) — reproduces RT2's K/S.
- **F1-FID / F2-FID / R1-FID:** `TN_FAILURES=0`, 269/271, all canonical
  TN_CHECK actuals; lying stream canonical revoke at E29. (Gate passes for
  stated 1/2; no_rule never triggers; F1's commit guard never fires since
  every COMMIT aux ∈ {0,1,2}.)
- **F1-RTE / F2-RTE:** E14 WITHHOLD (reason 1), `pinstall_n=0`,
  `ncommit=0`, `nuninstall=0`, `npromote=0`, `ndisconnect=0`, `badep=0`,
  `audit_total=208` (= 269 − PINSTALL − DISCONNECT − PROMOTE − 48 CONTEST −
  10 REFUSE). SURVIVE KB-E1 (nothing non-executable installed/committed);
  KB-E2 satisfied (nothing non-executable ever present; lying FID shows the
  machinery intact). KB-COST holds (208 ≤ 290).
- **F1-RTE2 / F2-RTE2:** identical dynamics to RTE (13 likewise
  non-executable). SURVIVE KB-E1/KB-E2. Generalization beyond the attacked
  id holds.
- **F2 == F1 byte-identical** on FID, RTE, RTE2 (stdout `cmp`-clean): the
  commit-site guard is provably unreachable in this architecture — every
  survivor comes from the `p<GL_NACT` loop, hence satisfies
  `gl_can_execute` by construction. A static scan of all COMMIT aux values
  across all cells will confirm all ∈ repertoire. (The guard is
  defense-in-depth for a wider future candidate set; the test measures
  exactly what it buys here: nothing observable.)
- **F1-RTX:** gate installs (`pinstall_policy=3`; 3 < GL_NACT=4 —
  SURVIVE KB-E1: the admitted policy IS executable). E15: VERIFY acts
  (read-only) → `sig_live=-1` → counterfactuals select CONTEST →
  `revoke_step=15`, `uninstall_policy=3`, `commit_policy=1`, `nuninstall=1`,
  `ncommit=1`, `npromote=0`, `badep=0`, `audit_total=272` (= 269 + E15
  SCAFFOLD+UNINSTALL+COMMIT triple), `quar_used=47`, `fire_step=15`.
  Rigidity: F1 admits the novel executable policy — no refusal of the
  legitimate.
- **R1-RTE / R1-RTE2:** E14 WITHHOLD (reason 2), otherwise identical ledger
  to F1-RTE (modulo WITHHOLD slot1). SURVIVE KB-E1/KB-E2 on both ids — the
  whitelist catches any out-of-range id, trivially.
- **R1-RTX:** gate WITHHOLDS stated=3 (reason 2); ledger = inert 208-entry
  run. KB-E1 technically SURVIVE (nothing non-executable admitted) but
  **rigidity FAIL**: refuses a genuinely executable policy. This is the
  predicted observable cost of the frozen literal — the whitelist checks the
  id against a literal, not the repertoire; repertoire growth breaks it.

## 5. Measures per fork

Verdicts on KB-E1/KB-E2 per cell; audit-entry cost (attack-cell totals vs
canonical 269); complexity (non-comment source lines changed vs base);
rigidity (RTX outcome + any legitimate-input refusal). Figure-it-out wins
ties.

## 6. Method (frozen)

- `build_rte.py`: copies `default_E` harness files per cell, applies fork
  patches by exact-anchor replacement (asserts hit counts), swaps main per
  cell, compiles with
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (cwd=build
  dir so `@import` resolves), runs each binary twice, stores
  `evidence/<cell>_run{1,2}.txt` + meta + patched-source shas. Static
  no-randomness check on every built source.
- `verify_rte.py`: evaluates KB-FID/E1/E2/COST/DET from TN_CHECK actuals +
  RT_FACT lines (hardcoded arm expectations ignored on attack cells, per RT2
  §7) against the frozen predictions above; prints the verdict table.
- Commit order: (1) THIS PREREG ALONE; (2) build/verify scripts + evidence;
  (3) VERDICT_RTE.md with the table. Commits via
  `~/workspace/commit_racefree.py`, `TMPDIR=~/workspace/tmp_commit`,
  lab-relative paths under
  `training_paradigms/scaffold_release/forks/gl_otherkills/rte/`, branch
  `tnn-native-lab`. No binaries, no `.zagd`.
- Determinism: zero randomness anywhere; every binary twice byte-identical.

## 7. Limitations

- White-box (sources studied first); not an independent black-box audit.
- RTE2 (id 13) and RTX (id 3) are synthetic probes, not observed attacks.
- The probe's 4th procedure is minimal-but-genuine (audited read-back);
  richer repertoire growth is not tested.
- KB-E2's "gone by E16" clause is operationalized for the withhold design
  (§3); the literal RT2 phrasing assumed install-then-revoke dynamics.
