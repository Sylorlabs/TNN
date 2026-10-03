# NAMECHECK.md - DEVANG lane, wave-20261002-1121pdt

Lane: DEVANG (developmental language track). Worker task queue item 4:
DEVANG6 with recalibrated K_ABL.
Branch: lane-devang-20261002-1121pdt. Worktree:
~/workspace/tnn-rsi-work/wave-20261002-1121pdt/devang/.
Owned run dir: docs/lab/rsi/runs/wave-20261002-1121pdt/devang/.

## Step 0: toolchain guard (recorded first, before any other work)

Setup command run:
`bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
Output tail: `linked: 36 tools`, `znc: OK
(/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`,
`verify: python3 absent from safebin PATH (OK)`,
`verify: python absent from safebin PATH (OK)`,
`SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.

Then `export PATH="$HOME/safebin"`.

Literal outputs:
- `which python3` -> (empty, exit code 1). Resolves to NOTHING. PASS.
- `which znc` -> `/home/hatch/safebin/znc`. Safebin path. PASS.

Guard: ACTIVE for every command in this lane (each shell invocation
re-exports PATH="$HOME/safebin" first). Any forbidden-interpreter
invocation anywhere in this lane's work = automatic PROCESS-FAIL for
this lane's wave, measurements quarantined; only a clean safebin
reproduction may promote. No de minimis exception.

## Provenance inherited (read-only, not re-committed)

- DEVANG5 prereg, sealed eval, build log, red-team: read from branch
  lane-devang-20261002-0821pdt,
  docs/lab/rsi/runs/wave-20261002-0521pdt/DEVANG/
  (PREREG_DEVANG5.md, SEALED_EVAL.md, BUILD-LOG.md, REDTEAM_SELF.md).
  Nothing from that branch is copied into this lane except the
  mechanism source devang5.zag, carried forward as devang6.zag with
  provenance recorded in BUILD-LOG.md and byte-level verification.
- Frozen DEVANG4 binary for the K_DISC premise: read from the same
  prior branch (sha256 verified before use, never modified).
- Sealed DEVANG5 families (sealed5/) are NOT read, NOT reused.
  DEVANG6 uses fresh sealed families under fresh frozen seeds.

## Standing rules acknowledged

Pure Zag only. No em-dashes in loop docs (check_no_dash.sh before
every commit). Prereg committed ALONE before any implementation file;
commit-order self-check before any verdict. Never weaken a frozen
kill bar; never count a prereg threshold before frozen execution.
Red lines: no spend, no publish, no contacting outsiders, no
purchases/bookings, no irreversible commitments, never git push,
never Google Drive. Commits pathspec-limited to this lane's run dir
on lane-devang-20261002-1121pdt. Never commit to tnn-native-lab;
never rebase; never git reset --hard. Do not write into
scaling_5000_fixed or scaling_10000. Hunt free lunches first; never
trade intelligence for speed.
