# NAMECHECK.md -- Catastrophic Forgetting Worker (H-CATFORGET-1)

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed. `which python3 python` returned
NOTHING. PATH=/home/hatch/safebin. Safebin active for all subsequent
work.

No forbidden executable invoked at any point. All research logic in
pure Zag via the pinned znc. Shell used only for: znc invocation,
running the binary, file moves, byte checks (grep/wc/sha256sum), git
operations. No Python, C, or other toolchains touched.

## Step 1: Task identity

Catastrophic Forgetting Worker (H-CATFORGET-1, 2026-10-02). Dedicated
interference battery for the continuing-learner question: one
persistent learner masters task A (chain composition follow->complete
on N1 worlds), then trains on interfering task B, then is re-tested on
A with learning frozen. Tests the C220 hypothesis (composition links
shield learned capability; severing them causes catastrophic
forgetting) in phased form, plus an interference gradient (B similar
to A vs B unrelated to A). Unfrozen variant only.

Design: 2x2 arms (FULL vs SEV comp-link use; SIM vs DIFF interference)
x 3 seeds, one binary, fixed order. Learner machinery: graph store,
4-instruction interpreter (MATCH/ADD/ANSWER/SETCUR) executing
learner-owned byte-array op bodies, epsilon-greedy bandit scoring
appl + comp (SEV: appl only; comp still recorded), generic consequence
credit, consequence ring. The interpreter never branches on op id; the
selector never branches on op id. No modes, bridges, handlers,
semantic cases.

## Step 2: Constraints honored

- Unfrozen only. Frozen read-only (nothing frozen touched).
- Pure Zag. Shell only for znc, binary runs, checks, git.
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper untouched:
  docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
- Nothing pushed. Commits local only on tnn-native-lab, explicit
  pathspecs.
- Prereg PREREG.md frozen and committed ALONE before any
  implementation file was written.
- Deterministic: two LCG streams, fixed seeds, fixed tie-breaks,
  3/3 byte-identical runs required.
- Per AGENTS.md toolchain lessons: no `as *i32` + slice construction
  (u8 cells with get32/set32 helpers); no `_zag_print` for dynamic
  content (single preallocated output buffer + one
  `_zag_raw_syscall(1,1,ptr,len)` write at end); no `as []f64` casts.

## Step 3: Development notes

(Filled after implementation and runs.)

## Step 4: Determinism

(Filled after runs: 3/3 byte-identical sha256, seeds, rebuild info.)

## Architecture accounting

One standalone catforget.zag. 0 modes, 0 bridges, 0 handlers,
0 hardcoded semantic cases, 0 hardcoded op sequences in learner code.
Learner-state structures: 5 op byte-array bodies, appl 5x32,
comp 5x5, consequence ring. Phase loop and Phase-3 freeze are
harness-level, not learner modes.
