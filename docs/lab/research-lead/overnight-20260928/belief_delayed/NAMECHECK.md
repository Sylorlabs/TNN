# NAMECHECK: Belief Delayed-Evidence Worker (H extension)

## Step 0: Toolchain guard (mandatory)

Activation:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returns nothing. Guard check recorded 2026-10-02.
Zero forbidden executables invoked during this wave. All research logic is pure
Zag compiled with the pinned toolchain. Shell used only to invoke znc, run the
binary, and do git/file operations.

## Provenance

- Worker: Belief Delayed-Evidence Worker.
- Mission: Belief under delayed evidence and rediscovery (Priority H
  extension of belief formation, commit 78e5a5eac): (1) delayed evidence
  after a settled belief, (2) evidence evicted under memory pressure then
  rediscovered, double count vs provenance, (3) reliable then adversarial
  source turn.
- Parent task: 2026-10-02 research lead directive, verbatim.

## Inputs

- Prior work read only: `belief_formation/` (commit 78e5a5eac) for the
  mechanism baseline. No frozen source read or modified. This is a self
  contained unfrozen variant; it does not build on TNN-2 node machinery.
- Design follows the shared substrate pattern (learner state tables, no
  new cognitive subsystems).

## What was built

- `belief_delayed.zag`: belief state with finite evidence table, FIFO
  eviction under memory pressure (score persists, receipt forgotten),
  event identity register with duplicate rejection, source reliability
  learning, independence discount, band status derivation, four phase
  world script, PROV and NAIVE (identity ablated) arms, Phase D
  adversarial turn arm, in binary assertions.
- `belief_delayed_bin`: compiled native binary (pinned znc).
- `run1.txt`, `run2.txt`, `run3.txt`: three deterministic runs.
- `compile.log`: toolchain output.

## Constraints honored

- Unfrozen variant only. Frozen source untouched and unread for this build.
- Pure Zag for all research computation. Safebin PATH active.
- Zero em/en dashes in docs (byte verified before commit).
- Research paper untouched. Nothing pushed. Explicit pathspecs on add/commit.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- Preregistration: PREREG.md committed before implementation; all
  expectations and kill bars fixed there.

## Verdict

BELIEF-DELAYED-COMPLETE. Details in REPORT.md.
