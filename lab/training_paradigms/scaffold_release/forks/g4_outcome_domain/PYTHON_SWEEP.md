# PYTHON SWEEP — G4 outcome-domain (2026-09-22)

Per the program prereg: audit every fork codebase for Python in AI
decision paths; redirect to pure Zag where found; Python is glue/
analysis only.

## Result

- `find forks/g4_outcome_domain -name "*.py"` → **0 files.**
- No `.py` in any fork dir, in `shared/`, or anywhere in the G4 tree.
- All learner logic (teaching learner: store/simulate/install/refuse;
  scaffold learner: probe/eliminate/commit/disconnect), the world
  (stimulus, outcome channel, fade schedule, temptation schedule), and
  the harness (episode loop, checks) are **pure Zag**, compiled with the
  pinned znc (`znc_linux_x86_64_abed8aa1`).
- Runners are POSIX shell (`run.sh`): compile → run twice → sha256 →
  grep-based static checks → check-line verification. Glue only; no
  decisions.
- The only Python that touched this work is
  `~/workspace/commit_racefree.py` (commit transport to GitHub) —
  outside every decision path.

## Redirects required

None. Nothing to redirect, nothing re-run.
