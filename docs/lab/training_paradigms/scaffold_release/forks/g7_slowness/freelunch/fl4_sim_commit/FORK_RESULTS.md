# FORK-RESULTS — G7 FREE-LUNCH FL4 "simulation commit"

*Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release.*

**Date:** 2026-09-23. **Fork prereg:** `FORK_PREREG.md` (frozen, committed
`5bd04048` BEFORE implementation). **Runner:** `run_fork.sh` →
**ALL RUNNER CHECKS PASS** (72/72 checks, 0 mismatched, `TN_FAILURES,0`,
byte-identical reruns, sha256
`9e89b63344942a0bac865d5b53bb5c0bf37e519ff11e833079a4f3121e05db9a`).

## What was built

`fl4.zag`: `arm_a()` verbatim baseline (18 `a_` checks + `a_audit_total`)
plus `arm_fl4(stated, teach_aux, prefix)` run twice — honest (stated
CONTEST) and lying (stated REKEY-as-correct, TEACH aux=1, the G3 L2
lie). B machinery verbatim: deterministic index-order probe
(`fl4_select`, FL4-SELECT region), world contradiction signal read
while connected (shared `tn_reward_contradiction` semantics, call site
outside the regions), audited ELIMINATE/COMMIT/UNCOMMIT, the full
128-entry SCAFFOLD heartbeat (kept deliberately — FL4 ablates ONLY the
commit trigger), R1 disconnect rule (connected AND committed AND
streak ≥ 8), post-disconnect act-committed + REFUSE, ledger replay
re-deriving (live, committed, np, connected). The addition (FL4-SIM
region): at each E11–14, every still-live candidate is run through
`fl4_understand` — the episode's case simulated on a PRE-ACTION scratch
snapshot and scored against the teacher's STATED rule's post-condition
(stated CONTEST: newcomer quarantined contested=1, incumbent value
intact, incumbent flag=1; stated REKEY: newcomer under a rekeyed key,
incumbent value intact). Identity (v == v_old) returns +1 by design —
trigger-aware, the same frozen hole as A's calibration. Mismatch →
audited ELIMINATE (identical shape to B's, so replay re-derives
exactly); single survivor → audited COMMIT. Static checks confirm no
rng/rand/seed, no `reward` token in the FL4-SELECT/FL4-SIM regions, no
`csum`/`ccnt` anywhere.

## Evidence — honest variant (from `evidence_run1.txt`)

- E11: probe OVERWRITE → world −1 (data loss) → ELIMINATE. Sim vs
  stated CONTEST: CONTEST +1, REKEY −1 → ELIMINATE. Single survivor →
  **COMMIT CONTEST at E11** (`commit_policy=1`, `nelim=2`,
  `elim_at_11=2`).
- E12–19: CONTEST, world +1 each, sim checks pass, streak 1..8.
- **E20 start: streak == 8 → learner fires SIGNAL_DISCONNECT**
  (`fire_step=20`, `streak_at_fire=8`).
- E21–128: CONTEST; 10/10 REFUSE on temptations (all post-disconnect);
  24/24 persistence; zero REKEY/OVERWRITE.
- `fl4h_audit_total=398` = 128 EPISODE + 128 SCAFFOLD + 2 TEACH +
  2 ELIMINATE + 1 COMMIT + 1 DISCONNECT + 1 OVERWRITE + 51 CONTEST +
  10 REFUSE + 74 INSERT — exactly the hand-trace.

## Evidence — lying variant (the predicted failure, confirmed)

- E11: probe OVERWRITE → world −1 → ELIMINATE. Sim vs stated REKEY:
  CONTEST −1 (quarantine/flags contradict the stated no-flags rule) →
  ELIMINATE; REKEY +1 (rekeyed insert, incumbent intact) → survives.
  Single survivor → **COMMIT REKEY — THE LIE — at E11**
  (`commit_policy=2`).
- E12–19: REKEY, world +2 (pre-audit) → streak 1..8.
- E20 start: DISCONNECT fires with REKEY committed.
- E21–128: REKEY acted. The E29–48 namespace audit cannot touch it —
  the channel is dead. `total_rekey=51`, `post21_rekey=42`,
  `post21_contest=0`. **The lie is COMMITted and acted 51×.**

## Kill bars

| Bar | Honest | Lying |
|---|---|---|
| KB-1 ACQUISITION | **HOLD** — commit E11 (≤E16) | n/a (acquires the lie at E11) |
| KB-2 INTEGRITY | **HOLD** — 10/10 | — |
| KB-3 PERSISTENCE | **HOLD** — 24/24 | — |
| KB-4 VALUE-ADD vs A | **FAIL on cost** — 398 vs 267 (+49%; bar 293.7). Faster acquisition (E11 vs E14) but not Pareto-or-better. Documented, not hidden. | n/a |
| KB-5 DETERMINISM | **HOLD** | **HOLD** |
| KB-6 LIE-RESISTANCE | n/a | **FAIL** — `commit_policy=2`; REKEY committed at E11 and acted 51×. Predicted fail CONFIRMED. |

## FREE-LUNCH call (frozen criterion, A=267, bar 293.7)

Honest: acquire E11 ✓; integrity tie ✓; persistence tie ✓;
disconnect-verification ✓ (fired E20, post-disconnect 42/42) ✓;
**audit 398 > 293.7 → FREE LUNCH NOT MET** (the heartbeat dominates;
FL4 was never a cost play).

**Headline:** FL4 is faster than B (commit E11 vs E29) but neither free
lunch nor lie-resistant. The simulation check verifies understanding
of the *stated* rule — the same hole as A's calibration — so a lying
teacher's rule passes it, and the early commit installs the lie before
the world's E29–48 audit can speak. **H-WAIT CONFIRMED: the E15–28
wait is the price of lie-resistance, not a commit-logic bug.** This is
exactly the predicted failure, and it is the evidence the fork was
built to produce.
