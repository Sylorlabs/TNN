# FL2 Other-Kills — RT-C Fork Test: Figure-it-out vs Rigid-policy (PREREG)

Date: 2026-09-23. Operator: Muse (subagent, FL2 RT-C fork-test crew).
Status: FROZEN. No fork code exists yet; no attack results read.
This prereg is committed ALONE (no code, no results) before any building.

## 0. Background (read, not trusted alone)

- Red-team report: `~/workspace/fl2rt/RESULTS.md` — RT-C (actuator fault) KILLs
  all five targets on KB-C1; T-DEF suffers 24 false revocations (all sham
  recommits of CONTEST); T-F3 suffers 2 (genuine E15 false displacement +
  E29+ self-correction).
- Diagnosis: `forks/gl_otherkills/diag/DIAGNOSIS.md` — RT-C is a MISSING
  MECHANISM (open-loop acting; no liveness check). Load-bearing interaction:
  the 99-sentinel sham is what keeps the kill "mild"; fixing the sentinel
  WITHOUT a liveness check converts 24 shams into a GENUINE
  uninstall-CONTEST/commit-REKEY at E15 on the honest stream (strictly worse).
  Forks must land sentinel fix + liveness together or not at all.
- Debates: `forks/gl_otherkills/debates/DEBATES.md` — adjudication: run BOTH
  forks per kill; figure-it-out is the direction of record, rigid-policy the
  cost/verifiability control; figure-it-out wins ties. H-R1 survives as the
  narrow form of H-F1; the debate's question is scope (quarantine path only
  vs all actuators / full effect).
- Canonical sources: `~/workspace/fl2rt/orig/` (SHASUMS-verified copies of the
  committed canonical, branch commit `7acabe36`). Canonical default learner
  NEVER modified in place — all forks are patched copies.
- Micah's laws: figure-it-out machine, not rigid-policy-per-edge-case; test
  both paths anyway; figure-it-out WINS TIES; reduce annoyances.

## 1. Kill mechanics under test (RT-C)

A world that audits the CONTEST but drops the quarantine writes. All 24
kind-3 episodes E15–E48 trace `sig_live=-1, quar_used=0`: 24 audited actions,
zero effects landed; the learner never reads the quarantine back and cannot
distinguish "world contradicted my rule" from "world didn't honor my action".

## 2. Forks (frozen definitions)

All forks patch COPIES of `orig/gl_learner.zag` (+ the RT2 substrate wrapper:
`RT_MODE` const, `rt_ep_info`, and the fault fns appended to
`orig/gl_substrate.zag` exactly as in RT2's build.py). Pure Zag for all
mechanism code; Python only for build/run glue. Zero randomness.

### F1 — figure-it-out, general (direction of record)
General act→verify-effect→interpret discipline + `f3_survivor`, landed
TOGETHER (per the diagnosis interaction):
- New `gl_effect_landed(act,k,v,...)`: the acted policy's expected world
  effect, one predicate per policy, no per-attack rules:
  - ACT_CONTEST: quarantine entry (k,v,flag=1) present AND main-store flag
    for k set (the two world effects `tn_do_contest` performs).
  - ACT_REKEY: main store contains a rekey entry for v
    (`tn_main_has_rekeyed`).
  - ACT_OVERWRITE: main store holds (k,v) with flag 0.
  - Anything else: 0 (unknown act ⇒ no valid signal; conservative).
- In the kind-3 verification block, after `sig_live` is computed:
  if the effect did NOT land, the signal is voided (`sig_live=0`;
  the revocation block only fires on `sig_live==-1`). General form of the
  diagnosis sketch: "no contradiction signal is valid until the action's
  effect is confirmed present in the world the signal is read from."
- Survivor selection replaced by `f3_survivor` (skip acted slot, genuine
  signals first, no 99 default) — verbatim the F3 function.

### F2 — figure-it-out, narrow (quarantine read-back)
Act→verify with quarantine read-back, 99 sentinel KEPT (no survivor change):
- In the kind-3 block, after `sig_live` is computed: if `act==ACT_CONTEST`
  and `tn_quar_has_flag(k,v)!=1`, void the signal (`sig_live=0`).
  "Interpret revocation only from effects that verifiably landed," verified
  through the one channel the learner can read back. Non-contest acts keep
  canonical interpretation.
- FROZEN OBSERVATION TO VERIFY: F2 and R1 are predicted to produce
  byte-identical transcripts on every cell below — the narrow figure-it-out
  form and the rigid policy converge mechanically on this kill; the
  difference is conceptual (signal interpretation vs trigger rule).

### R1 — rigid-policy (H-R1, cost/verifiability control)
Quarantine-only revocation policy: "revocation triggers only from quarantine
writes." Implemented as a hard trigger precondition on the revocation block:
`if(sig_live==-1 && (act!=ACT_CONTEST || quar_has_flag(k,v)==1))`.
Scoping note (frozen): the quarantine is the contest actuator's channel, so
the gate applies to contest acts; non-contest acts keep canonical behavior.
The strict all-acts reading is rejected by the fidelity gate by construction
(the lying stream never writes quarantine — E15–E28 act REKEY only — so it
would block the genuine E29 revoke and let REKEY promote; stated here as
analysis, not built). 99 sentinel kept.

### N1 — NEGATIVE CONTROL (preregistered as such)
Sentinel fix ALONE: `f3_survivor` replaces the 99-sentinel selection, NO
liveness check of any kind. Predicted to be STRICTLY WORSE than canonical on
RT-C (genuine false displacement instead of sham bloat). If it is not worse,
the diagnosis interaction is wrong — say so.

## 3. Cells (frozen)

Per fork X in {f1,f2,r1,n1}:
- `{X}_FID`: fidelity — forked sources + ORIGINAL main
  (`arm_a` + honest `arm_gl(1,0)` + lying `arm_gl(2,1)`), RT_MODE=0, no fault.
- `{X}_C`: RT-C — `arm_gl(1,0,"{X}c_")`, RT_MODE=0, fault fn swapped onto the
  live kind-3 contest call (drops the quarantine write; the audit still lands).
- `{X}_A`: RT-A regression — `arm_gl(0,0,"{X}a_")`, RT_MODE=0, no fault
  (sentinel fix is in play for F1/N1; check the RT-A bar).
- `{X}_P2`: scope probe (this crew's design, preregistered) — `arm_gl(1,0,
  "{X}p_")`, RT_MODE=0, fault-2 fn swapped onto the live contest call:
  the world audits the CONTEST and LANDS the quarantine write (k,v,flag=1)
  but DROPS the main-store flag flip. Same fault class (world doesn't honor
  the action), different part of the effect — invisible to a
  quarantine-only read-back.

Every binary runs TWICE; the pair must be byte-identical or the cell is void.

## 4. Gates and kill bars (frozen)

- **Fidelity gate** (read BEFORE any attack cell): `{X}_FID` must print
  `TN_FAILURES,0` with honest audit total 269 and lying audit total 271.
  A fork that fails the gate is disqualified; its attack cells are not read.
- **KB-C1** (RT-C kill bar, from RT2 verify.py): SURVIVE iff
  `nuninstall==0 && ncommit==0`; else KILL.
- **KB-A1/A2** (RT-A bars): SURVIVE iff `commit_policy!=0` (genuine
  displacement, not sham-recommit of the erasing rule) AND NOT
  (`nuninstall>0 && uninstall_policy==commit_policy`) (no sham pairs).
- **P2 bar**: same as KB-C1 (`nuninstall==0 && ncommit==0` ⇒ SURVIVE).
  This probe separates general (F1) from narrow (F2/R1): a quarantine-only
  check cannot see the dropped flag flip.

## 5. Frozen predictions

Notation: (verdict, key metrics). `audit_total` frozen only where exact.

| Cell | F1 | F2 | R1 | N1 |
|------|----|----|----|----|
| FID | PASS (269/271, TN_FAILURES=0) | PASS | PASS | PASS |
| C | SURVIVE (nuninstall=0, ncommit=0, revoke_step=-1, npromote=1, promote_policy=1, audit_total=269, quar_used=0 — the 0 is the fault's footprint, expected) | SURVIVE (same numbers as F1; transcripts predicted byte-identical to R1) | SURVIVE (same numbers as F1/F2) | **KILL** (nuninstall=2, ncommit=2, revoke_step=15, uninstall_policy=1, commit_policy=2, npromote=0, audit_total=274 — reproduces f3_C exactly; f3's law-check never fired there, lawfail_step=-1, and `fl2_contradict`≡`gl_contradict`) |
| A | SURVIVE (nuninstall=1, ncommit=1, revoke_step=15, uninstall_policy=0, commit_policy=1, npromote=0 — reproduces f3_A exactly) | KILL (24 shams: nuninstall=24, ncommit=24, commit_policy=0, npromote=0 — matches default_A) | KILL (same as F2) | SURVIVE (same as F1 — on RT-A the overwrite effect lands, so liveness gates nothing and both do the genuine E15 displacement) |
| P2 | SURVIVE (nuninstall=0, ncommit=0, audit_total=269, quar_used=48 — writes landed; npromote=1) | **KILL** (24 shams: nuninstall=24, ncommit=24, commit_policy=1, npromote=0 — the quarantine read-back succeeds, so the false -1 is trusted) | **KILL** (same as F2) | **KILL** (nuninstall=2, ncommit=2, revoke_step=15, uninstall_policy=1, commit_policy=2, npromote=0 — genuine false displacement at E15, self-correction at E29) |

Rationale frozen per cell:
- F1_C: every faulted episode voids the signal (quarantine entry absent) ⇒
  zero revokes ⇒ honest stream promotes CONTEST at E48 unrevoked.
- F2_C / R1_C: same, via the quarantine read-back alone.
- N1_C: no liveness ⇒ E15 computes `f3_survivor(1,-1,-1,2)=2` ⇒ genuine
  uninstall CONTEST + commit REKEY; E16–28 act REKEY (aa=0, consistent);
  E29+ (aa=1) the world evidence genuinely displaces REKEY→CONTEST.
  Strictly worse than 24 shams: a real false displacement of the honest
  rule (even though self-corrected, KB-C1 counts revokes, not recovery).
- F1_A / N1_A: overwrite effect lands ⇒ signal valid ⇒ `f3_survivor`
  displaces OVERWRITE→CONTEST genuinely at E15 (f3_A dynamics).
- F2_A / R1_A: 99 sentinel kept, no fault on this cell ⇒ canonical 24 shams.
- F1_P2: flag flip absent ⇒ effect not landed ⇒ all 24 signals voided ⇒
  0 revokes. (Withholding judgment under an unhonored action is the
  discipline working as designed.)
- F2_P2 / R1_P2: quarantine entry present ⇒ false -1 trusted ⇒ 24 shams.
- N1_P2: same two-revoke dynamics as N1_C (E15 false displace, E29 correct).

## 6. Measurements per fork (frozen)

1. Kill verdict on KB-C1 (0 false revokes = SURVIVE).
2. Audit-entry cost: `audit_total` on the C cell (canonical RT-C: 340).
3. Complexity: diff size vs canonical (added/removed lines in the learner;
   helper-function count).
4. Rigidity: scope of the check (all-actuators vs quarantine-only;
   general predicate vs fixed trigger rule), assessed against the debate's
   scope question.
5. P2 verdict (scope differentiator).

Adjudication (frozen, Micah's law): figure-it-out wins ties. The rigid
path's role is cost/verifiability control.

## 7. Protocol (frozen)

1. This prereg committed ALONE first (no code).
2. `build.py`: copies `orig/` → per-fork dirs, applies the frozen patches
   (exact-anchored string replacement, asserts on anchor counts), appends the
   RT2 substrate wrapper (RT_MODE / rt_ep_info / fault fns), adds the
   RT_FACT instrumentation, swaps main per cell; static no-randomness scan;
   compiles with the pinned znc
   (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
3. Fidelity gate read before any attack cell.
4. Every binary twice, byte-identical; evidence saved per cell
   (run1/run2/meta/sources).
5. `RESULTS.md` + verdicts; commit code + evidence + results (no binaries,
   no `.zagd`) under
   `training_paradigms/scaffold_release/forks/gl_otherkills/rtc/`.

## 8. Pre-declared limitations

- White-box (sources studied before forking); not an independent audit.
- P2 is a synthetic second fault, not an observed world; it tests scope,
  not realism.
- F2/R1 keep the 99 sentinel deliberately (the task's fork definitions);
  their RT-A KILL is the known sentinel defect, not a liveness finding.
- On the C cell, `quar_used=0` fails the honest-stream TN_CHECK
  (expected 48) on every fork including survivors — that check encodes the
  no-fault world; the kill bar is KB-C1, not the check suite.
