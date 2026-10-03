# NAMECHECK.md -- IVWC-ADVERSARIAL (sealed adversarial worlds vs the fragility signal)

## Step 0: toolchain guard (worker toolchain guard, Micah's 2026-09-30 ruling)

- Safebin activated at lane start: `export PATH="$HOME/safebin"` (2026-10-03,
  before any lane work). The canonical setup script path from the guard docs
  did not exist in this checkout; `$HOME/safebin` was already provisioned
  (znc, git, coreutils) and used directly.
- `which python3` returns nothing; `which python` returns nothing
  (verified in the safebin PATH, same shell session as all builds/runs).
- All computation in pure Zag, compiled with the pinned znc
  (`$HOME/safebin/znc`, version 2026.07.0-dev, edition 2026).
- Shell used only for: invoking znc, running the binary, git ops,
  file moves, text inspection via safebin coreutils (grep/sed/awk/sha256sum/cmp).
- No python3/python invocation at any step of this lane. If one occurs,
  this wave is PROCESS-FAIL per the guard.

## Lane identity

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_adversarial/`
- Task: IVWC-ADVERSARIAL -- sealed adversarial worlds testing the
  IVWC-LEARNEREVAL fragility signal (Micah Priority #4: internal
  verification without expected-answer oracle).
- Non-ledger task (claim minting paused).
- Branch: `tnn-native-lab` (worktree `~/workspace/tnn-rsi-gpi3`). Commits
  local, explicit pathspecs only, confined to `ivwc_adversarial/`.
- Push note: per task instructions, do NOT attempt push via `gh_push_api.py`
  (known HTTP 403; credential lacks git-database write scope; remote ref at
  `99c5691d`). Push blockage documented in REPORT.md; parent must fix the
  credential.

## Source provenance

- `src/ivwc_adversarial.zag` is written fresh for this wave (not adapted
  from the LEARNEREVAL source, which carries the full world stepper).
  Worlds are committed tables (train + sealed); the mechanism under test
  is the evaluation signal, not world generation. The learner-side
  self-evaluation functions (se_p, se_pen, se_ppb, se_ppenb, se_cpfw,
  se_cpfl, se_retro) implement the frozen LEARNEREVAL rule verbatim plus
  the preregistered contested-profit alternative. See PREREG.md for the
  operational definitions and frozen predictions.

## Dual-role disclosure

- The adversarial worlds were designed post-freeze by this same worker
  with the explicit goal of breaking the frozen rule. Mitigations: the
  rule is frozen verbatim (no tuning to the new worlds), all tables and
  all predictions are committed in PREREG.md before any implementation
  source is written, and the report discusses what a truly independent
  adversary would add.
