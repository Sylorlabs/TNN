# PYTHON SWEEP — G3 LYING-TEACHER

**Order (program prereg):** audit every fork codebase for Python in AI
decision paths; where found, redirect to pure Zag, re-run, document.

## Scope audited

All three G3 forks, every file in the decision path:

- `l1_mistaught_teaching/`: `tn.zag`, `l1_trial.zag`, `run_fork.sh`
- `l2_scalar_scaffold/`: `tn.zag`, `l2_trial.zag`, `run_fork.sh`
- `l3_hint_scaffold/`: `tn.zag`, `l3_trial.zag`, `run_fork.sh`

(The decision path = everything the learner, world, and harness execute
to produce the trial outcome: the znc-compiled Zag binaries plus the
bash runners that compile, execute, and verify them.)

## Method

1. Static token scan embedded in each fork's runner (step 4): strip
   `//` and `#` comments from all `.zag`/`.sh` files, then grep for
   `python3`, `/usr/bin/python`, `/usr/local/bin/python`. All three
   runners report `python-sweep OK`.
2. Manual review of the full file list per fork: the only executables
   are the znc-compiled native binaries (`lN_trial_linux`, built from
   pure Zag by the pinned znc) and the bash runners (compile → run
   twice → sha256 → grep → check-verify). No Python interpreter is
   invoked at any stage of any fork's decision path.

## Findings

- **No Python in any AI decision path in any G3 fork.** Nothing to
  redirect; no re-runs required. The trial logic (learner, world,
  reward/hint computation, elimination, disconnect, audit) is 100%
  native Zag; the harness glue is bash + coreutils.
- Python appears only **outside** the decision path: `commit_racefree.py`
  (used to commit results to GitHub — pure transport glue, runs after
  the science is done) and ad-hoc analysis commands during development.
  Neither touches learner state, action selection, or evidence.
- `tn.zag` in each fork dir is byte-identical to the RL trial's
  substrate (sha256 `0c59e21e8fced6595199d4dc5072ddd710340b33b7dc22b05b72b920ca1b9c34`
  in all three dirs) — the sweep covered these copies too; clean.

## Standing guard

The python-sweep static check is a permanent step in each fork's
`run_fork.sh`: any future edit that introduces a Python reference into
the decision path fails the runner before compile.
