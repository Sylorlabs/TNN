# NAMECHECK: Grammar Encoding-Detection Worker

## Step 0: Toolchain Guard (2026-10-02)

Safebin activated:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING. Guard check done.
No Python, no forbidden executables in PATH. Pure Zag for all research
computation. Shell only for: invoking znc, running binaries, git ops,
file moves/copies, checksums, diffs, builds.

## Worker identity

Grammar Encoding-Detection Worker. Mission: make grammar induction
fail-closed on encoding mismatch (the silent-wrong repair). Design a
decode-consistency check: after inducing ranges, round-trip verify;
if the round-trip fails, REFUSE instead of writing the grammar. Test
on EXL2 (must still induce), EXL3 (must refuse with diagnostic), and
a new EXL4 (must refuse). Unfrozen variant only. Frozen read-only.

## Files

- PREREG.md: frozen preregistration, committed before implementation
  (commit b38324b6a); Amendment A1 re-froze the bars (commit e26874d43)
  after the grid round-trip false-refused the EXL2 control during
  implementation testing, before any verdict.
- NAMECHECK.md: this file.
- e4_base.zag: byte copy of grammar_third/g3_base.zag (machinery
  identity; never edited). SHA-256 a29972ca... (matches source).
- e4_patch.zag: grammar_third/g3_patch.zag PLUS the gi_codec_check guard
  function and the 4-line guard insertion in gi_induce. Stripped of the
  guard, the diff vs g3_patch.zag is exactly the doc comment and the
  call site; the five /16 decode sites are byte-identical.
- e4_driver.zag: experiment driver. EXL2 teaching (literals 0..9,
  P=a*16+b) and EXL3 teaching (literals 0..7, P=a*8+b) are renames of
  the frozen gt/g3 teachers; EXL4 teaching (literals 0..3, P=a*32+b)
  is new. Per-world induce arms with GI-EXPECT/GI-MATCH verdict lines.
- e4_build.sh: assemble + compile with pinned znc.
- e4_bin: compiled binary.
- e4_run1.txt, e4_run2.txt, e4_run3.txt: 3 deterministic runs,
  byte-identical
  (SHA-256 8aa84d504dc5639f78f5557f8a787c34a90eaa6853c78bfeead0982c47df0004).
- REPORT.md: results and verdict GRAMMAR-ENCODE-COMPLETE.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. Guard is a plain function called from
  gi_induce, not a mode.
- Frozen dirs untouched (grammar_third, grammar_transfer read-only).
- Prereg committed before implementation (commit-order self-check).
- Nothing pushed. Commits local only, explicit pathspecs.
