# NAMECHECK.md -- IVWC-LEARNEREVAL (learner-owned evaluation)

## Step 0: toolchain guard (worker toolchain guard, Micah's 2026-09-30 ruling)

- Safebin activated at lane start: `export PATH="$HOME/safebin"` (2026-10-03,
  before any lane work).
- `which python3` returns nothing; `which python` returns nothing
  (verified in the safebin PATH, same shell session as all builds/runs).
- All computation in pure Zag, compiled with the pinned znc
  (`$HOME/safebin/znc`, version 2026.07.0-dev, edition 2026).
- Shell used only for: invoking znc, running the binary, git ops,
  file moves, text inspection via safebin coreutils (grep/sed/awk/sha256sum/cmp).
- No python3/python invocation at any step of this lane. If one occurs,
  this wave is PROCESS-FAIL per the guard.

## Lane identity

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_learnereval/`
- Task: IVWC-LEARNEREVAL -- learner-owned evaluation (Micah Priority #4:
  internal verification; reduce dependence on harness expected answers).
- Non-ledger task (claim minting paused).
- Branch: `tnn-native-lab`. Commits local, explicit pathspecs only.
- Push note: per task instructions, do NOT attempt push via `gh_push_api.py`
  (known HTTP 403; credential lacks git-database write scope; remote ref at
  `99c5691d`). Push blockage documented in REPORT.md; parent must fix the
  credential.

## Source provenance

- `src/ivwc_learnereval.zag` is adapted from the committed IVWC-LEARNERK
  source (`a3c4c3f70:docs/lab/research-lead/overnight-20260928/ivwc_learnerk/src/ivwc_learnerk.zag`,
  1123 lines). World / belief / composer / stepper / seeds / biases / UCB
  tables / verdict bars / consequence machinery are verbatim; the new
  mechanism is the learner-owned self-evaluation module (prospective
  train-only estimates, knife-edge fragility penalty, self-error flag,
  retrospective experienced-net self-report). See PREREG.md for the
  operational definitions and frozen predictions.
