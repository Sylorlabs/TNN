# NAMECHECK: DDES-ALT lane

Wave: wave-20261002-0221pdt. Lane: DDES-ALT (promotion step 6,
alternative-explanation attack on the DDES t*=0 repair).
Worker: depth 2/2, no children. Working copy ~/workspace/tnn-rsi,
branch tnn-native-lab.

## Step 0 (toolchain guard, recorded before any other work)

- Ran bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  from ~/workspace/tnn-rsi: SAFEBIN-READY, 36 tools, no python.
- export PATH="$HOME/safebin" in every shell used below.
- `which python3`: nothing (exit 1). `which python`: nothing (exit 1).
- `which znc`: /home/hatch/safebin/znc (2026.07.0-dev, abed8aa1).
- Pure Zag only for all implementation, build, run, and analysis steps.
  No Python invoked at any stage. Any forbidden-executable invocation
  would be disclosed here immediately as PROCESS-FAIL; none occurred.

## Lane scope

- Write ONLY under docs/lab/rsi/runs/wave-20261002-0221pdt/DDES-ALT/.
- Commit ONLY with an explicit pathspec of this lane dir.
- NEVER: git stash, git reset (any form), git clean, git checkout -- .,
  git add -A, git add .. No push (local commits only).
- Retry commits on ref-lock failure after verifying the lock holder.
- Dash scans via docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
  on every lane doc. Zero em/en dashes required.

## Step log

- Step 0: toolchain guard (this file), done before any other work.
- Prereg: PREREG_DDES_ALT.md written, dash-scanned clean, committed
  ALONE at d64688fa6 before any implementation existed.
- Implementation: ddes_alt.zag written after the prereg commit, pure
  Zag, no Python. Build: znc exit 0, 93-byte stderr (the
  unconditional zagd-availability warning only), binary 55018 bytes.
- Runs: 3/3 byte-identical, exit 0, zero stderr bytes every run.
  Transcript sha256 (all three):
  f9030bb7dadef25201b112d15e7f237ecc724ed7f8788dad6ad2ac4aa494d31f
- Mechanical check H1(b): V_nomarker vs V_full on P, FLAG lines
  removed: every TARGET/PLAN/EXEC/PRED/ELIM/SURVIVE/CONVERGE line
  byte-identical on all 3 runs (only the CELL variant labels and
  the FLAG lines differ).
- Results: ATTACK_RESULTS.md. Verdicts: H1 ATTACK-SUCCEEDS, H2
  EVIDENCE-HOLDS, H3 ATTACK-SUCCEEDS. Lane build verdict:
  BUILD-PASS (attack lane only; no promotion claim; steps 4+5
  verdict untouched).
- Forbidden executables invoked: none. PROCESS-FAIL triggers: none.
