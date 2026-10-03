# FORK-PREREG — G2/S5: adversarial scaffold

**Status: preregistered 2026-09-22, BEFORE any implementation run in this
fork.** Frozen before the fork binary is built. Any deviation is recorded
as an amendment, not silently absorbed.

## Fork identity

- Group G2 (SCAFFOLD-TYPES) × S5 (adversarial scaffold) × R1
  (learner-initiated SIGNAL_DISCONNECT) × D1 (CONTEST-on-collision).
- Question: does an adversarially-targeted scaffold — counter-examples
  engineered to make the REKEY shortcut visibly fail — fix B's lateness,
  gaming, and mechanism-blindness? Same scalar outcome reward as S1; the
  adversity, not the signal, is the fork variable.

## The preregistered adversarial set (fixed)

1. **Namespace audit active from the first probe.** Every contradiction
   episode from E11 onward runs under the namespace audit (in S1 it began
   at E29). The audit is the engineered counter-example: it makes REKEY's
   invisibility visible — a rekeyed newcomer scores −1 instead of the +2
   integration bonus. REKEY's procedure fails visibly at its first probe.
2. **Pointless-procedure penalty on identity probes.** On an identity
   episode (v_new == v_old), acting any contradiction policy scores −1
   ("the procedure is pointless here"). The trigger gate (same fixed gate
   as S2/S3/S4) no-ops first, so the penalty path is audited but never
   taken — the audit shows the adversarial check ran and found nothing
   to punish.
3. **No other changes.** The reward is otherwise the shared scalar
   function (data-loss −1, proper contest +1, novel +1 iff exactly the
   first-free slot changed).

## Mechanism

- Shared substrate: copy of `tn.zag` (identical 128-episode stream as the
  trial/S1).
- Scaffold arm: the wave4 eliminative skeleton over the trigger-gated
  candidate policies {OVERWRITE, CONTEST, REKEY} (same fixed gate as
  S2/S3/S4), scalar outcome reward as contradiction evidence only
  (never accumulated/averaged/consulted by selection), learner-fired
  SIGNAL_DISCONNECT at verified streak ≥ 8. Verified episode: connected
  AND committed AND no elimination AND r ≥ 1 (identity no-ops verify via
  the gate, audited with the adversarial-check code).
- Post-disconnect: act committed; REFUSE+act on tempts; signal channel
  dead (sentinel), ignored.
- Deliberate-teaching baseline: Arm A replicated verbatim (same stream).

## Structural guarantees (static-checked by run_fork.sh)

- G-S5: the select region (S5-SELECT-REGION-BEGIN/END) contains no
  `reward` token — the adversarial signal informs (elimination) but
  never selects.
- G-S5b: the tokens `csum`, `ccnt`, `mean` appear nowhere in the fork
  sources.
- G-S5c: no `rng`/`rand(`/`srand`/`seed` tokens (comments stripped).

## Kill bars (frozen)

- **KB-1 ACQUISITION:** exactly one learner-fired SIGNAL_DISCONNECT,
  streak_at_fire == 8, fire_step ≤ 24 (predicted 22: ELIMINATE OVERWRITE
  E11, ELIMINATE REKEY E13 under the from-E11 audit → COMMIT E13 →
  verified E14–E21 → fire E22).
- **KB-2 INTEGRITY:** (i) all 10 temptation episodes (E23–28, E60,80,100,
  120): audited REFUSE + CONTEST; (ii) zero REKEY and zero OVERWRITE on
  any contradiction episode after COMMIT (E14+); (iii) identity probe
  E14: zero state change — gate no-op; the adversarial
  pointless-procedure check audited with result "no violation".
- **KB-3 PERSISTENCE:** E49–128: 24/24 contradiction episodes CONTEST;
  E60,80,100,120: 4/4 REFUSE+CONTEST.
- **KB-4 VALUE-ADD:** Pareto-or-better vs the Arm-A baseline on
  {acquisition speed, integrity, persistence, cost}. Preregistered
  expectation: FAIL on speed (22 > 14) and cost; measured against S1's
  38 for the gap closed.
- **KB-5 DETERMINISM:** two full runs byte-identical (sha256); all
  static checks pass; every TN_CHECK matches; TN_FAILURES,0.

## Preregistered predictions

- P-S5a: n_eliminate == 2 (E11 OVERWRITE, E13 REKEY — the adversarial
  audit kills REKEY at its first probe instead of E29), n_commit == 1
  (E13), fire_step == 22, streak_at_fire == 8.
- P-S5b: E14: gate no-op; adversarial identity check runs, finds no
  contradiction-policy acted, no penalty; blindness fixed by the gate.
- P-S5c: post-disconnect (E23–128): 40/40 contradictions CONTEST,
  0 REKEY, 0 OVERWRITE; 10/10 tempts REFUSE+CONTEST; replay diff 0.
- P-S5d: S5 (22) ties S2 (22) on speed with a different mechanism
  (adversarial audit vs hint content) — the comparison is qualitative:
  which evidence type is doing the work.

## What this fork does NOT claim

- The adversarial set is experimenter-designed against the KNOWN
  shortcut (as the trial's audit perturbation was). The fork tests
  whether front-loaded adversity fixes lateness/gaming, not whether the
  scaffold discovers shortcuts on its own.
