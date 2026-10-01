# NAMECHECK.md (devang2 prereg, wave-20261001-1421pdt)

## Step 0: Toolchain verification (MANDATORY, recorded before any work)

- Ran `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  at wave start. Output: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`,
  `znc: OK`, verify `python3 absent from safebin PATH (OK)`, `python absent from safebin PATH (OK)`.
- Ran `export PATH="$HOME/safebin"` then `which python3`: prints nothing
  (exit code 1). Confirmed: no `python3` and no `python` resolve in the
  active PATH.
- All shell work in this lane uses the safebin PATH only.
- This task is writing-only (prereg draft); no programs were written or
  executed for the research itself, so no toolchain contamination is
  possible in this lane's artifacts. Implementation, when it happens, must
  be pure Zag compiled with the pinned znc.

## Step 1: Task understanding

- Draft the FROZEN prereg for the DEVANG2 RETRY in
  `docs/lab/rsi/runs/wave-20261001-1421pdt/devang2/`. Writing only: no
  implementation, no evaluation. The coordinator commits the prereg alone
  before any implementation.
- Prior located and read:
  - `docs/lab/research-lead/overnight-20260928/devlang/PREREG_DEVANG1.md`
    (frozen, commit e23627a40) and `RESULT_DEVANG1.md` (BUILD-FAIL,
    training crash "slice index out of bounds").
  - `docs/lab/research-lead/overnight-20260928/devlang2/PREREG_DEVANG2.md`
    (commit 402e53d32) and `RESULT_DEVANG2.md` (BUILD-FAIL on mechanism,
    13/20; distinct earlier artifact, disambiguated in the prereg).
  - `docs/lab/research-lead/overnight-20260928/devang3/PREREG_DEVANG3.md`
    and `RESULT_DEVANG3.md` (BUILD-FAIL close, 16/20; two-pass redesign
    line, kept separate from this retry).
  - wave-20261001-1121pdt debate record: DEVANG2 retry QUEUED (no frozen
    prereg existed); this document fills that gap.
  - No DEVANG1 mentions in the 1121pdt/0821pdt LOOP_STATE.md files
    (checked; no matches).
- Documentation rule honored: no em dashes anywhere in the files written
  (checked by construction; colons and parentheses used instead).

## Step 2: Files produced

- `docs/lab/rsi/runs/wave-20261001-1421pdt/devang2/PREREG_DEVANG2.md`
  (prereg draft; NOT yet committed; coordinator freezes it alone).
- This `NAMECHECK.md`.

## Step 3: Git state

- No commits, pushes, checkouts, or branch changes made by this worker.
  Both files are left uncommitted for the coordinator to freeze.
