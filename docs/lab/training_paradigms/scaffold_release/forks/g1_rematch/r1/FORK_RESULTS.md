# FORK RESULTS — G1-R1: learner-initiated SIGNAL_DISCONNECT (replication)

**Prereg:** `FORK_PREREG.md` (frozen, commit `585602fc`, before
implementation). **Runner:** `run_fork.sh` → **ALL RUNNER CHECKS PASS**
(39/39 checks, 0 mismatched, `TN_FAILURES,0`, byte-identical reruns,
sha256 `8076dfc1cb53ad4f4ab5bd96abe6c1a80717f3a5824acc3314a29314eeac43f4`).

**Fork verdict: R1 PASSES** (KB-1, KB-2, KB-3, KB-5 hold; KB-4 fails as
preregistered — this fork replicates B's loss).

## What was built

`tn.zag` copied byte-identical from the RL trial (sha256
`0c59e21e…b33b7dc22b05b72b920ca1b9c34`); `g1.zag` = trial harness minus
Arm C, with Arm B renamed to `arm_r1` (mechanical extraction, no
hand-transcription) plus one added check (`r1_audit_n`). Baseline Arm A
replicated in the same binary, checks asserted verbatim from the trial.

## Evidence (from `evidence_run1.txt`, byte-identical rerun)

- Replication exact: fire at E38, streak_at_fire = 8, one DISCONNECT;
  eliminations at E11 (OVERWRITE) and E29 (REKEY); one COMMIT at E29
  (CONTEST); probe order 0/1/2 at E11–13; E14 acted CONTEST
  (mechanism-blindness, as in the trial).
- Post-release (E39–128): 29/29 contradictions CONTEST, 0 REKEY,
  0 OVERWRITE; 4/4 REFUSE on E60/80/100/120; channel dead at end;
  ledger replay re-derives exactly.
- Audit entries: 392 (matches the trial's decomposition).
- Baseline: all 18 `a_` lines byte-identical to the RL trial's
  `evidence_run1.txt` (diff clean) — install at E14, 193 audit entries.

## Kill bars

| Bar | Result |
|---|---|
| KB-1 ACQUISITION (commit ≤ E38, fire E38/streak 8) | HOLD |
| KB-2 INTEGRITY (29/29 + 4/4 post-release) | HOLD |
| KB-3 PERSISTENCE (24/24 E49–128) | HOLD |
| KB-4 VALUE-ADD vs A (14 eps, 193 entries) | **FAIL** — 38 eps, 392 entries; ties on integrity/persistence |
| KB-5 DETERMINISM | HOLD |

## Reading

R1 confirms the RL-trial B numbers on an independent build: the
learner-initiated release schedule reproduces B's loss exactly (2.7×
slower than teaching, 2× the audit). The loss is in place before the
release machinery even matters — commit waits for the E29 audit
perturbation regardless of who fires the disconnect.
