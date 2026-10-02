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

## Files (planned)

- PREREG.md: frozen preregistration (committed before implementation).
- NAMECHECK.md: this file.
- e4_base.zag: byte copy of grammar_third/g3_base.zag (machinery
  identity; never edited).
- e4_patch.zag: byte copy of grammar_third/g3_patch.zag PLUS the new
  gi_codec_check guard function and the two-line guard insertion in
  gi_induce. The five /16 decode sites are byte-unchanged.
- e4_driver.zag: experiment driver. Teaching sections for EXL2
  (literals 0..9, P=a*16+b), EXL3 (literals 0..7, P=a*8+b), EXL4
  (literals 0..3, P=a*32+b); per-world induce arms; verdict lines.
- e4_build.sh: assemble + compile with pinned znc.
- e4_full.zag: concatenated build input (generated).
- e4_compile.txt: compiler output.
- e4_bin: compiled binary.
- e4_run1.txt, e4_run2.txt, e4_run3.txt: 3 deterministic runs.
- REPORT.md: results and verdict.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. Guard is a plain function called from
  gi_induce, not a mode.
- Frozen dirs untouched (grammar_third, grammar_transfer read-only).
- Prereg committed before implementation (commit-order self-check).
- Nothing pushed. Commits local only, explicit pathspecs.
