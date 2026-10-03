# NAMECHECK: Belief Formation Worker (Micah Priority 9)

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
Zag compiled with the pinned toolchain
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`. Shell used only to invoke znc,
run the binary, and do git/file operations.

## Provenance

- Worker: Belief Formation Worker.
- Mission: Test rational belief formation from evidence (Micah Priority 9):
  weak evidence to provisional belief, contrary evidence to uncertainty,
  strong independent evidence to revision. Score rationality relative to the
  evidence available at the time, not omniscience.
- Parent task: 2026-10-01 overnight directive, priority 9 verbatim.

## Inputs

- No frozen source read or modified. This experiment is a self contained
  unfrozen variant; it does not build on TNN-2 node machinery. The design
  follows the shared substrate pattern (learner state tables, no new
  cognitive subsystems) so a later merge into the tag-61 consequence
  substrate is specified in REPORT.md.
- Design informed by prior ledgered results: C182 adaptive threshold
  (thresholds from experienced quantities), C183 source reliability from
  consequences (no hardcoded authority hierarchy), C194 integrated
  substrate (one shared store, net negative lines preferred).

## What was built

- `belief.zag` (406 lines): belief state, evidence store, source reliability
  learning, independence discount, status derivation, three phase world
  script, calibration phase, verification phase, two ablation arms, one
  adversarial probe, in binary assertions.
- `belief_bin`: compiled native binary (pinned znc).
- `run1.txt`, `run2.txt`, `run3.txt`: three deterministic runs,
  byte identical (sha256 `9eca77362447e781484e48add05eaad52fa616fa9f366956e53d94e680118e4b`).
- `compile.log`: toolchain output.

## Constraints honored

- Unfrozen variant only. Frozen source untouched and unread for this build.
- Pure Zag for all research computation. Safebin PATH active.
- Zero em/en dashes in docs (byte verified before commit).
- Research paper untouched. Nothing pushed. Explicit pathspecs on add/commit.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- Preregistration: the phase by phase expected statuses were fixed in the
  task brief (provisional H1, uncertain, revise H2) and asserted in binary;
  no thresholds were tuned after seeing output. One genuine bug was fixed
  during development (revision detector compared against status code 32
  instead of 23); the fix was to the detector, not to any expectation.

## Verdict

BELIEF-FORMATION-COMPLETE. Rationality 3/3 phases relative to evidence at
time. Details in REPORT.md.
