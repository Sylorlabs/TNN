# FORK RESULTS — G1-R4: late release (extended scaffold, streak 24)

**Prereg:** `FORK_PREREG.md` (frozen, commit `585602fc`, before
implementation). **Runner:** `run_fork.sh` → **ALL RUNNER CHECKS PASS**
(39/39 checks, 0 mismatched, `TN_FAILURES,0`, byte-identical reruns,
sha256 `6ffcac6be692c722f4074ccdeac76425ca74a2e2b441dfcb2686b5f90578b190`).

**Fork verdict: R4 PASSES** (KB-1, KB-2, KB-3, KB-5 hold; KB-4 fails as
preregistered).

## What was built

R1's harness with the learner's verified-streak threshold tripled to the
preregistered R4_STABLE_K=24 (own `r4_b_legal` / `r4_b_disconnect`;
everything else — reward, elimination, probe order — unchanged).

## Evidence (from `evidence_run1.txt`, byte-identical rerun)

- Commit (CONTEST) at E29, exactly as R1 — the threshold change does
  not touch elimination.
- 24 consecutive verified episodes E30–53 → fire at E54 start,
  streak_at_fire = 24; exactly one DISCONNECT.
- Post-release (E55–128): 23/23 contradictions CONTEST, 0 REKEY,
  0 OVERWRITE; 4/4 REFUSE on E60/80/100/120; channel dead at end;
  ledger replay exact.
- Audit entries: 392 (identical to R1/R2).
- Baseline: all 18 `a_` lines byte-identical to R1's (diff clean).

## Kill bars

| Bar | Result |
|---|---|
| KB-1 ACQUISITION (commit ≤ E54, fire E54/streak 24) | HOLD |
| KB-2 INTEGRITY (23/23 + 4/4 post-release) | HOLD |
| KB-3 PERSISTENCE (24/24 E49–128) | HOLD |
| KB-4 VALUE-ADD vs A (14 eps, 193 entries) | **FAIL** — 54 eps, 392 entries; ties on integrity/persistence |
| KB-5 DETERMINISM | HOLD |

## Reading

Tripling the verification wait bought nothing: R4's post-release
integrity and persistence are identical to R1's (and R2's), at 16 more
episodes of scaffold. More verification is pure cost — the committed
policy was already correct at E29, and the extra 16 verified episodes
confirmed what the first 8 already showed. Combined with R2 (8 fewer
verified episodes, same quality), the pattern is clean: release timing
moves cost, not quality.
