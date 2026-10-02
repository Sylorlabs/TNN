# NAMECHECK_IMPL TNN3H5R (implementer)

Lane: TNN3H5R. Wave: wave-20261001-2021pdt. Worker role: implementer of the
frozen H5R prereg (Option A substrate change, section 4).

Ordering check (done before any implementation write):
- `git log --oneline -5` tip is 67ed888e4 (FREEZE H5R prereg, committed
  alone). No implementation artifact in TNN3H5R/ predates it.
- Implementation authorization: RULINGS.md (Q1-Q5 all CONFIRM), committed
  at the freeze. This worker writes implementation files only after that.

## Step 0. Toolchain verification (Worker Toolchain Guard)

1. Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`.
   Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python). znc OK
   (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1).
2. `export PATH="$HOME/safebin"` used for every shell command this session.
3. `which python3` prints NOTHING (exit code 1). Confirmed absent from the
   safebin PATH at lane startup and again at implementation start.
4. Pure Zag rule: shell invokes only the pinned znc, built binaries, git
   read-only ops (log/show/status/diff), and file copies. No Python for
   glue, analysis, verifiers, harnesses, or fixture provisioning.

## Scope of this worker

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
- Write ONLY inside docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/.
- New files only: NAMECHECK_IMPL.md, IMPLEMENTATION_H5R.md,
  tnn3_h5r.zag, tnn3_h5r.bin. No modifications to the committed prereg,
  NAMECHECK.md, or RULINGS.md.
- No git operations beyond read-only (log/show/status/diff). No commit by
  this worker (coordinator commits). No push. No git reset, no rebase.
- Documentation rule: no em-dashes anywhere.
- Deliverables: NAMECHECK_IMPL.md, IMPLEMENTATION_H5R.md,
  tnn3_h5r.zag, tnn3_h5r.bin. Readiness report in IMPLEMENTATION_H5R.md.

## Process notes (KB-P1)

Step 0 recorded above. Every command in this lane ran with
PATH=$HOME/safebin. No forbidden executable was invoked.
