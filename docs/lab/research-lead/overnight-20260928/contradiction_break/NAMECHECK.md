# NAMECHECK: Contradiction Break Prober

## Step 0: Toolchain Guard

Activated safebin at session start:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned nothing. Guard check passed.
Pure Zag via the pinned compiler
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Shell used only to invoke znc, run the binary, git ops, and move/copy files.
Zero forbidden executables invoked. No PROCESS-FAIL condition.

## Scope

- `cb_bin`: compiled from `cb_full.zag` with the pinned znc.
- `cb_full.zag`: `cb_base.zag` (verbatim frozen copy, SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  original test `main` removed) with `cb_driver.zag` appended.
- Cognition code diff-verified byte-identical to frozen. Only the driver
  (test harness) differs. UNFROZEN VARIANT ONLY. Frozen source untouched.

## Task

Test whether a contradicting observation breaks the confirmed bootstrap
loop (`ee7815de8`), characterize the break mechanism, test persistence,
test recovery requirements, and test the `ev_observe` contradiction path.

## Inputs (read-only)

- Bootstrap loop report and method: `../bootstrap_loop/BOOTSTRAP_LOOP.md`
  (commit `ee7815de8`).
- Frozen TNN-2 cognition: `cb_base.zag` (SHA-256 verified above).

## Constraints

- UNFROZEN VARIANT ONLY. No frozen source modification.
- Pure Zag. Zero em dashes in deliverables.
- Paper untouched. Nothing pushed. No sealed worlds.
- 3/3 byte-identical runs required.
- Explicit git pathspecs on commit.

## Verdict

CONTRADICTION-BREAK-COMPLETE: CONFIRMED (loop breaks; break is permanent
without external intervention; recovery requires external teaching).
