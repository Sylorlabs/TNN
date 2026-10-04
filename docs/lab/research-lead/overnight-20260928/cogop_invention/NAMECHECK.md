# NAMECHECK.md -- cogop_invention

## Step 0: toolchain guard (2026-10-02)

Safebin activated before any implementation work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing; `guard-check-done` printed.
Zero forbidden executables in PATH. All research logic in pure Zag
(`cogop.zag`); shell used only to invoke znc, run the binary, and for git
file operations. build.sh re-verifies the guard on every run.

Worker: COGOP-INVENTION (subagent bca37fbe-ca6c-4a98-8ccb-400b9a28ff7d).

## Prereg commit-order self-check

- PREREG.md committed ALONE in commit `e9ffbd9f7` (exactly 1 file,
  201 insertions) BEFORE any implementation file was written. K-COGOP-1 holds.
- Commit-order repair (self-disclosed): my first `git commit` after the
  prereg accidentally swept in two `l3_redteam/` files another worker had
  staged in the shared repo. I repaired with `git reset --soft HEAD~1`,
  unstaged their files (their worktree content untouched), and recommitted
  only my own files. Lesson: always run `git status` and check for other
  workers' staged files before committing in the shared repo; use explicit
  pathspecs on every commit.

## Implementation provenance

- `cogop.zag`: written by this worker 2026-10-02, pure Zag, no Python,
  no `_zag_print`, no `as *i32`, no `as []f64`/`as []i64`, no mode/bridge/
  handler substrings (build.sh asserts all of these, all read 0).
- Learner/driver separation: the `// === DRIVER ===` marker splits the
  file; everything before it (the learner) contains zero `world_`
  references (build.sh asserts 0). Task answers live only in the driver.
- Binaries `cogop`, run outputs `run1.txt`/`run2.txt`/`run3.txt` produced
  by build.sh from the committed source.
