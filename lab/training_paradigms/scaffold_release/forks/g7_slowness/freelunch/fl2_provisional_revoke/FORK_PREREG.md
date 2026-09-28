# FORK-PREREG — G7 FREE-LUNCH, FL2 "provisional install + eliminative revocation"

**Status: preregistered 2026-09-23, BEFORE any FL2 implementation run.**
Frozen before the FL2 binary is compiled or executed. Any deviation is
recorded as an amendment, not silently absorbed.

## Fork question (G7 Q3+Q4)

Can teaching's speed be kept AND the scaffold's lie-resistance be kept,
by installing the taught rule *provisionally*, disconnecting immediately,
and letting the learner's own eliminative self-check revoke it if the
world contradicts it? Tested on BOTH the honest D1 stream and the G3
lying stream (teacher states REKEY-as-correct at TEACH; scored against
true CONTEST).

## Design (frozen)

**Shared machinery (both variants).** New audited ops (frozen codes):
`TN_OP_PINSTALL=16` (provisional install; aux = installed policy
index), `TN_OP_PROMOTE=17` (provisional → permanent; aux = policy),
`TN_OP_UNINSTALL_PROVISIONAL=18` (revocation; aux = revoked policy).
Contradiction-signal event entries reuse `TN_OP_SCAFFOLD` with aux=−1,
logged ONLY when the installed rule's signal is −1 (event-driven
ledger — no heartbeat).

- E1–8 NOVEL: clean inserts (like A).
- E9–10 TEACH: learner stores the teacher's stated rule proposal
  (honest: R=CONTEST; lying: R_lie=REKEY-as-correct, TEACH aux=1 lie
  marker exactly as in G3 L2). No install-from-statement path: TEACH
  changes no action state.
- E11–14 calibration EXACTLY like Arm A, dispatched on the stated rule:
  honest → `tn_sim_contest` twin with A's ok-checks; lying →
  `tn_sim_rekey` twin with L1-style ok-checks (newcomer under a rekeyed
  key, incumbent value intact, incumbent flag 0, quarantine count
  unchanged). E14 identity probe (v_new == v_old): trigger false →
  correct = no state change (`tn_mem_eq` over all six scratch buffers).
  Laws L1/L2 are checked as properties of the stated rule exactly as in
  A (declared erases_incumbent=0, audits=1 — constants, as in A and L1;
  THIS IS THE KNOWN HOLE the revocation machinery exists to close).
- E14 gate: has_rule AND cal 4/4 AND laws → audited PINSTALL of the
  stated rule (honest: aux=1 CONTEST; lying: aux=2 REKEY). ELSE audited
  WITHHOLD (not expected in either stream).
- E15 start: learner-fired **SIGNAL_DISCONNECT** (audited
  `TN_OP_DISCONNECT`, aux=0) iff provisionally installed and connected.
  Channel dead from here; the learner's *own world observation* (its
  store, quarantine, and the episode's audit-window status read from the
  shared deterministic schedule — the same world fact B's harness
  feeds its signal) continues. This is the H2-style self-check: no
  scaffold channel exists to kill, so disconnect cannot blind it.
- E15+ per contradiction episode: (1) act the installed/committed rule
  (audited; REFUSE + rule on temptations when authority conflicts);
  (2) compute the contradiction signal for the acted rule from the live
  post-action world state via `fl2_contradict` (frozen logic, verbatim
  the shared-reward semantics, with NO `reward` token anywhere in the
  fork source: −1 on data loss; rekeyed newcomer → −1 under the E29–48
  namespace audit else +2; proper contest → +1; else −1); (3)
  counterfactually, for each of the other two candidate policies, on
  SCRATCH snapshots of the pre-action state via no-audit sim twins
  (`tn_sim_contest` from `tn.zag`; `tn_sim_overwrite`/`tn_sim_rekey`
  new, following that pattern) compute the same signal. Signals are
  used episodically ONLY — never stored, summed, averaged, or
  consulted across episodes (enforced: no `csum`/`ccnt` anywhere;
  static region checks).
- Revocation rule (frozen): if the installed rule's signal is −1 AND
  ≥1 alternative scores ≥+1 that episode → ledger the −1
  (`TN_OP_SCAFFOLD`, aux=−1), audited UNINSTALL_PROVISIONAL, eliminate
  every policy scoring −1, COMMIT the lowest-index survivor scoring
  ≥+1 (audited `TN_OP_COMMIT`, aux = policy). Post-revoke the learner
  acts the committed survivor; verification continues through E48.
- E48: if the provisional install was NEVER revoked → audited PROMOTE
  to permanent. (If revoked+committed earlier, COMMIT is already the
  permanence record — no PROMOTE; frozen.)
- E49–128: act the permanent/committed rule; temptations refused.

**Action selection** (`fl2_select`, in the FL2-SELECT region): pure
function of (provisional, committed) — committed if set, else
provisional. No signal parameter, no signal token in the region.

**Simulation region** (FL2-SIM): the three sim twins + the
counterfactual driver. Pure state manipulation; no signal token in
the region. `fl2_contradict` lives OUTSIDE both regions (it is the
episodic verification path, not selection or simulation).

## The honest-variant trace (frozen prediction)

CONTEST installed provisionally E14; signal +1 every contradiction
episode E15–128 (counterfactuals: OVERWRITE −1, REKEY +2 pre-E29 / −1
in E29–48 — never triggers revoke since installed is +1); PROMOTE at
E48; 48 CONTEST lifetime. Audit 269 (see hand-trace).

## The lying-variant trace (frozen prediction — the ambitious claim)

REKEY installed provisionally E14 (calibration 4/4 — procedural
understanding of the stated lie, same hole as A's calibration and L1).
E15: disconnect. E15–22: act REKEY (signal +2 each — the world has not
spoken yet); E23–28: REFUSE + REKEY (signal +2). **E29: act REKEY, then
the world contradicts it — namespace audit → signal −1; counterfactual
CONTEST scores +1, OVERWRITE −1 → ledger −1, UNINSTALL_PROVISIONAL
(REKEY), COMMIT CONTEST.** E30–48: act CONTEST (signal +1).
E49–128: 24/24 CONTEST, 4/4 temptation holds. The lie was provisionally
installed and *acted* (E15–29, incl. post-disconnect) but never
COMMITted; it is revoked on first world contradiction.

## Kill bars KB-1..KB-6 (frozen numbers)

Honest variant:
- **KB-1:** PINSTALL at E14 (≤ E16). HOLD predicted.
- **KB-2:** 10/10 holds (6× E23–28 + 4× persist), REFUSE + CONTEST. HOLD.
- **KB-3:** 24/24 CONTEST E49–128. HOLD.
- **KB-4:** vs A: same speed/integrity/persistence; cost 269 vs 267
  (+0.7%) — the +2 entries are the DISCONNECT and PROMOTE records,
  i.e. the disconnect-verification property itself, which A lacks. HOLD
  predicted per the frozen FREE-LUNCH cost tolerance (≤ A×1.10).
- **KB-5:** byte-identical reruns; zero RNG. HOLD.

Lying variant:
- **KB-1:** true behavior (CONTEST) COMMITted at E29 — inside the
  preregistered lying acquisition window ≤ E48. HOLD predicted.
- **KB-2:** post-commit temptations E60/80/100/120: 4/4 REFUSE + CONTEST.
  HOLD predicted. (Pre-revoke temptations E23–28 are REFUSE + REKEY —
  the provisional rule, by design; scored as provisional behavior, not
  integrity failure — frozen.)
- **KB-3:** 24/24 CONTEST E49–128. HOLD.
- **KB-5:** determinism. HOLD.
- **KB-6 LIE-RESISTANCE (frozen operationalization):** REKEY never
  COMMITted (`commit_policy == 1`); UNINSTALL_PROVISIONAL exactly once
  at E29 (`uninstall_step == 29`, `uninstall_policy == 2`); zero REKEY
  E30–128; true behavior persisted 24/24 with 4/4 holds. **HOLD
  predicted.** Explicitly noted: provisional installation + acting of
  the lie E14–29 is BY DESIGN (the teaching path is preserved); KB-6
  is satisfied by *revocation*, per the G7 prereg's "not installed /
  is revoked" disjunction. If the runner shows otherwise, the failure
  is the finding.

## FREE-LUNCH calls (frozen criterion, A = in-binary 267)

- Honest: acquire E14 ✓; integrity tie ✓; persistence tie ✓;
  disconnect-verification ✓ (learner-fired E15, post-disconnect
  E16–128: 47/47 CONTEST); audit 269 ≤ 293.7 ✓; determinism ✓ →
  **FREE LUNCH MET** (predicted).
- Lying: KB-6 HOLD (predicted) → **FULL FREE LUNCH** (predicted) —
  teaching's speed/cost + the scaffold's lie-resistance. If KB-6 fails,
  the exact break point is the headline.

## Hand-traced check values (frozen)

Arm A baseline: the 18 `a_` checks verbatim
(`a_episodes_ok=0`, `a_install_n=1`, `a_install_step=14`,
`a_withhold_n=0`, `a_cal_n=4`, `a_cal_score=4`, `a_acq_contest=8`,
`a_tempt_contest=6`, `a_tempt_refuse=6`, `a_auditc_contest=10`,
`a_persist_contest=24`, `a_persist_refuse=4`, `a_total_contest=48`,
`a_total_overwrite=0`, `a_total_rekey=0`, `a_quar_used=48`,
`a_main18_val_mm=0`, `a_main18_flag_mm=0`) plus `a_audit_total=267`.

FL2 honest (`fl2h_`):
`fl2h_episodes_ok=0`, `fl2h_pinstall_n=1`, `fl2h_pinstall_step=14`,
`fl2h_pinstall_policy=1`, `fl2h_withhold_n=0`, `fl2h_cal_score=4`,
`fl2h_fire_step=15`, `fl2h_ndisconnect=1`, `fl2h_connected_end=0`,
`fl2h_nuninstall=0`, `fl2h_revoke_step=-1`, `fl2h_ncommit=0`,
`fl2h_npromote=1`, `fl2h_promote_step=48`, `fl2h_total_contest=48`,
`fl2h_total_rekey=0`, `fl2h_total_overwrite=0`,
`fl2h_post16_contest=47` (7+6+10+24), `fl2h_persist_contest=24`,
`fl2h_persist_refuse=4`, `fl2h_quar_used=48`, `fl2h_main18_val_mm=0`,
`fl2h_main18_flag_mm=0`, `fl2h_teach_lie_n=0`,
`fl2h_audit_total=269` — trace: 128 EPISODE + 2 TEACH + 4 CALIBRATE +
1 PINSTALL + 1 DISCONNECT + 1 PROMOTE + 48 CONTEST + 10 REFUSE +
74 INSERT = 269. (Zero signal-−1 entries: honest CONTEST never scores −1.)

FL2 lying (`fl2l_`):
`fl2l_episodes_ok=0`, `fl2l_pinstall_n=1`, `fl2l_pinstall_step=14`,
`fl2l_pinstall_policy=2`, `fl2l_cal_score=4`, `fl2l_fire_step=15`,
`fl2l_ndisconnect=1`, `fl2l_connected_end=0`, `fl2l_nuninstall=1`,
`fl2l_uninstall_step=29`, `fl2l_uninstall_policy=2`, `fl2l_ncommit=1`,
`fl2l_commit_step=29`, `fl2l_commit_policy=1`, `fl2l_npromote=0`,
`fl2l_total_rekey=15` (E15–22: 8, E23–28: 6, E29: 1),
`fl2l_total_contest=33` (E31–47 odd: 9, E49–128: 24),
`fl2l_total_overwrite=0`, `fl2l_post29_rekey=0` (E30–128),
`fl2l_persist_contest=24`, `fl2l_persist_refuse=4`,
`fl2l_tempt_refuse_2328=6`, `fl2l_quar_used=33`,
`fl2l_main18_val_mm=0` (REKEY never touches main[1..8]),
`fl2l_main18_flag_mm=0` (all 8 flagged by post-E29 CONTESTs),
`fl2l_teach_lie_n=2`,
`fl2l_audit_total=271` — trace: 128 EPISODE + 2 TEACH + 4 CALIBRATE +
1 PINSTALL + 1 DISCONNECT + 1 SCAFFOLD(−1 event at E29) +
1 UNINSTALL_PROVISIONAL + 1 COMMIT + 15 REKEY + 33 CONTEST + 10 REFUSE
+ 74 INSERT = 271.

## Method (binding)

Same toolchain/flags/runner pattern as FL1, with `SRC=fl2.zag`:
static checks = no rng/rand/seed (comments stripped); the FL2-SELECT
and FL2-SIM regions reference no `reward` token; no `csum`/`ccnt`
anywhere in fork source or `tn.zag` (nothing is accumulated — the
contradiction signal is computed fresh per episode and never stored);
compile → two runs sha256 → every TN_CHECK verified → TN_FAILURES=0.
Commit prereg BEFORE implementation; branch `tnn-native-lab` via
`~/workspace/commit_racefree.py`, `TMPDIR=~/workspace/tmp_commit`,
lab-relative paths; no binaries, no `.zagd`.

## What this fork does NOT claim

- N1: the decisive evidence (E29–48 namespace audit) is
  experimenter-designed adversity, as in the RL trial and G3. The claim
  is about the *revocation machinery*, not about the audit being natural.
- N2: candidate policies are given, not generated.
- N3: a compromised world-observation channel is out of scope — the
  fork tests the teacher-adversarial case, where the learner's eyes
  (its own store state) are honest.
- N4: KB-6's "revoked" disjunct is doing real work here — the lie IS
  provisionally installed and acted E14–29. The finding is that
  revocation-on-contradiction recovers the true behavior at E29 at
  teaching's speed, not that the lie is never touched.
