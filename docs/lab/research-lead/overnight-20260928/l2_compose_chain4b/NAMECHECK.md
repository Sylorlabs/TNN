# NAMECHECK: L2-COMPOSE-CHAIN4B

Worker: L2-COMPOSE-CHAIN4B-RETRY subagent (depth 2/2), 2026-10-03.
Lane: docs/lab/research-lead/overnight-20260928/l2_compose_chain4b/
Non-ledger task (claim minting paused).

## Step 0: toolchain guard

- `export PATH="$HOME/safebin"` at startup.
- `which python3` -> empty. `which python` -> empty. Verified 2026-10-03.
- All computation in pure Zag via pinned znc. Shell only for
  git/file ops and sha256.
- No forbidden executables invoked. If one is, this wave is
  PROCESS-FAIL.

## Scope

Discrimination test: is any 4-operator chain with 4th
operator != INVERT feasible on the frozen learner?
Preregistered infeasibility hypothesis with a minimal
empirical discrimination probe ([6,5,4,2] candidate).
