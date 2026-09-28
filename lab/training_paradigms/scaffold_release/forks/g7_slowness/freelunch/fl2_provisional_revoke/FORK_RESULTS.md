# FORK-RESULTS — G7 FREE-LUNCH FL2 "provisional install + eliminative revocation"

*Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release.*

**Date:** 2026-09-23. **Fork prereg:** `FORK_PREREG.md` (frozen, committed
`5bd04048` BEFORE implementation). **Runner:** `run_fork.sh` →
**ALL RUNNER CHECKS PASS** (78/78 checks, 0 mismatched, `TN_FAILURES,0`,
byte-identical reruns, sha256
`20fee727aaf7746c7b86e93e6bf441381dab9e1e1f4d85437e0b7c5882582263`).

## What was built

`fl2.zag`: `arm_a()` verbatim baseline (18 `a_` checks + `a_audit_total`)
plus `arm_fl2(stated, teach_aux, prefix)` run twice — honest (stated
CONTEST) and lying (stated REKEY-as-correct, TEACH aux=1, exactly the G3
L2 lie). New audited ops: PINSTALL(16), PROMOTE(17),
UNINSTALL_PROVISIONAL(18); contradiction-signal events reuse SCAFFOLD
with aux=−1, logged only on signal −1 (event-driven ledger, no
heartbeat). Per contradiction episode E15–48 the learner acts the
installed/committed rule AND computes the contradiction signal for it
from its own observed world state, plus counterfactually for the other
two candidates on scratch snapshots via no-audit sim twins (the
`tn_sim_contest` pattern). Signals are episodic only — static checks
confirm no `reward` token anywhere in the fork source, no `csum`/`ccnt`
anywhere, and the FL2-SELECT / FL2-SIM regions are signal-free.

## Evidence — honest variant (from `evidence_run1.txt`)

- PINSTALL of CONTEST at E14 (`pinstall_policy=1`), calibration 4/4,
  learner-fired disconnect at E15, PROMOTE at E48, zero revocations.
- 48/48 CONTEST lifetime; post-disconnect E16–128: 47/47; 10/10
  temptation holds; 24/24 persistence; zero REKEY/OVERWRITE.
- `fl2h_audit_total=269` = 267 + DISCONNECT + PROMOTE (zero signal-−1
  entries — honest CONTEST never scores −1).

## Evidence — lying variant (the ambitious claim)

- PINSTALL of REKEY at E14 (`pinstall_policy=2`) — calibration 4/4 on
  the stated lie (procedural understanding, same hole as A's
  calibration; the fork prereg names this explicitly).
- Disconnect fired at E15 with the lie still installed. E15–28: REKEY
  acted (signal +2 pre-audit — the world has not spoken yet).
- **E29: REKEY acted, then the namespace audit contradicts it (signal
  −1); counterfactual CONTEST scores +1, OVERWRITE −1 → signal-−1
  event ledgered, UNINSTALL_PROVISIONAL(REKEY), COMMIT(CONTEST)
  (`revoke_step=29`, `commit_policy=1`).**
- E30–48: CONTEST acted (signal +1); no PROMOTE (COMMIT is the
  permanence record). E49–128: 24/24 CONTEST, 4/4 temptation holds,
  zero REKEY post-E29 (`post29_rekey=0`).
- `fl2l_audit_total=271`; `teach_lie_n=2`; the lie was never COMMITted.

## Kill bars

| Bar | Honest | Lying |
|---|---|---|
| KB-1 ACQUISITION | **HOLD** — E14 (≤E16) | **HOLD** — true CONTEST committed E29 (≤E48 window) |
| KB-2 INTEGRITY | **HOLD** — 10/10 | **HOLD** — 4/4 post-commit holds (E23–28 REFUSE+REKEY is provisional behavior, per frozen prereg) |
| KB-3 PERSISTENCE | **HOLD** — 24/24 | **HOLD** — 24/24 |
| KB-4 VALUE-ADD vs A | **HOLD** — 269 vs 267 (+0.7%) | n/a (vs L1-style: blowout) |
| KB-5 DETERMINISM | **HOLD** | **HOLD** |
| KB-6 LIE-RESISTANCE | n/a | **HOLD** — REKEY never committed; revoked at E29 on first world contradiction; true behavior persisted |

## FREE-LUNCH calls (frozen criterion, A=267, bar 293.7)

- Honest: acquire E14 ✓; integrity/persistence tie A ✓;
  disconnect-verification ✓ (fired E15, post-disconnect 47/47) ✓;
  audit 269 ≤ 293.7 ✓; determinism ✓ → **FREE LUNCH MET**.
- Lying: KB-6 HOLD → **FULL FREE LUNCH**.

**Headline:** FL2 revokes the lie at E29 AND matches A on speed
(acquire E14, release E15) and cost (269/271 vs 267 — within 1.6%).
Teaching's speed and cost with the guided-learning scaffold's
lie-resistance: the revocation machinery — provisional install,
immediate learner-fired disconnect, per-episode eliminative
self-verification against the learner's own world observation with
counterfactual simulation of the alternatives — recovers the true
behavior on first world contradiction. The disconnect does not blind
the self-check because there is no scaffold channel to kill: the
learner reads its own store state.
