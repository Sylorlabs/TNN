# FORK RESULTS — G1-R2: sudden disconnect at fixed episode 30

**Prereg:** `FORK_PREREG.md` (frozen, commit `585602fc`, before
implementation). **Runner:** `run_fork.sh` → **ALL RUNNER CHECKS PASS**
(40/40 checks, 0 mismatched, `TN_FAILURES,0`, byte-identical reruns,
sha256 `2c0675de5de6811a4737d01d13fbdc9b6b49d7aa1bdf3151d528f95db7c7095f`).

**Fork verdict: R2 PASSES** (KB-1, KB-2, KB-3, KB-5 hold; KB-4 fails as
preregistered).

## What was built

R1's harness with the learner's streak-based fire rule replaced by a
harness-fired disconnect at the preregistered fixed episode R2_CUT=30
(audited DISCONNECT, aux=−7 harness-cut marker). Everything else —
reward, elimination, probe order — unchanged.

## Evidence (from `evidence_run1.txt`, byte-identical rerun)

- Disconnect at E30 (harness-fired, aux=−7 confirmed), streak_at_fire=0;
  exactly one DISCONNECT; eliminations at E11 and E29; one COMMIT at E29
  (CONTEST) — the commit point did not move.
- Post-release (E31–128): 33/33 contradictions CONTEST, 0 REKEY,
  0 OVERWRITE; 4/4 REFUSE on E60/80/100/120; channel dead at end;
  ledger replay exact.
- Audit entries: 392 (identical to R1 — the release point moves cost in
  episodes, not in audit entries).
- Baseline: all 18 `a_` lines byte-identical to R1's (diff clean).

## Kill bars

| Bar | Result |
|---|---|
| KB-1 ACQUISITION (commit ≤ E30, cut at E30) | HOLD |
| KB-2 INTEGRITY (33/33 + 4/4 post-release) | HOLD |
| KB-3 PERSISTENCE (24/24 E49–128) | HOLD |
| KB-4 VALUE-ADD vs A (14 eps, 193 entries) | **FAIL** — 30 eps, 392 entries; ties on integrity/persistence |
| KB-5 DETERMINISM | HOLD |

## Reading

Cutting the 8-episode verification wait changed nothing about quality:
R2's post-release integrity and persistence are identical to R1's, and
the commit still waits for the E29 audit perturbation. Release at E30
vs E38 saves 8 episodes (30 vs 38 to release) but the fork is still
2.1× slower than deliberate teaching (30 vs 14). The verification wait
is pure cost with no integrity value — and the commit logic, not the
release schedule, is where B's loss lives.
