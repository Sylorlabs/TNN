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

Single implementation version (v1), written after the prereg commit
(5de0d76a7); one typo fix before compile (results-array index
`(si*4+3)*1+1` corrected to `(si*4+3)*3+1`; caught by reading the
verdict code, no behavior had been observed yet). Compiled first try
with the pinned znc; only benign E0101 analyzer warnings (adding 0 in
`(si*4+0)*3+1` index arithmetic; no effect).

One design point worth recording: the first-draft design made
retention = episode success with a tight step limit, but hand
simulation showed the severed arm could still succeed by trying gather
late in the episode, making the bar step-limit-dependent. The frozen
prereg instead defines retention as Phase-3 success under greedy
frozen evaluation, and the actual mechanism turned out cleaner than
the draft: the severed arm fails via wrong answers (gather outscores
complete at the shared context), not via timeout, so the result does
not depend on the step limit at all.

## Step 4: Determinism

3/3 runs byte-identical. sha256:
3572d18999898f2e4d7b6cb5ab08cf83469c78c47bdd539c9308212ae0b67dc8
(run1.txt, run2.txt, run3.txt). Fixed LCG seeds (111, 222, 333;
learn stream seeded seed*7+13), fixed tie-breaks (least-tried then
lowest op id). Rebuild: pinned znc
(~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
on catforget.zag. Binary stdout verified byte-wise before trusting
(single preallocated buffer + one _zag_raw_syscall write; exit 0,
empty stderr).

## Architecture accounting

One standalone catforget.zag. 0 modes, 0 bridges, 0 handlers,
0 hardcoded semantic cases, 0 hardcoded op sequences in learner code.
Learner-state structures: 5 op byte-array bodies, appl 5x32,
comp 5x5, consequence ring. Phase loop and Phase-3 freeze are
harness-level, not learner modes.
