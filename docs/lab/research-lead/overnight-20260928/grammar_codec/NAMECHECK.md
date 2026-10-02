# NAMECHECK: Grammar Codec Induction Worker

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

Codec Induction Worker. Mission: induce the pair codec divisor D from
the taught fact stream (the deeper grammar fix diagnosed by the
third-system worker and left as refused-but-honest by the
encoding-detection worker). From SUB/DIV eval facts and DSUB/DDIV
decomp facts, build the multiple set S = {P+t} union {unit DIV P},
take g = gcd(S+), enumerate the data-derived divisor candidates
d = v-1 for v|g, keep the unique candidate passing the op-consistency
check, refuse -3 (contradicted) or -4 (ambiguous) otherwise. Store D in
the type-70 grammar node (new logical field packed in field 4) and
thread it through all five decode sites. Test EXL2 (D=16), EXL3 (D=8),
EXL4 (D=32) plus NEG-AMB (ambiguous, must refuse -4) and NEG-SHIFT
(contradicted, must refuse -3). Unfrozen variant only. Frozen
read-only.

## Files (planned)

- PREREG.md: frozen preregistration, committed before implementation.
- NAMECHECK.md: this file.
- c_base.zag: byte copy of grammar_encode/e4_base.zag (machinery
  identity; never edited).
- c_patch.zag: e4_patch.zag with gi_codec_check REPLACED by
  gi_codec_induce (+ gi_gcd, gi_codec_op_ok helpers); gi_induce
  rewritten (part-1 vacuous check deleted, codec induction inserted,
  D threaded through part 2 and the type-70 write with packed divisor
  field); gi_grammar_read exposes D at buf[32]; gi_trial_build2,
  gi_hardcode_build, gi_classify decode under the threaded D.
- c_driver.zag: experiment driver. EXL2/EXL3/EXL4 teachers are renames
  of the e4 teachers; NEG-AMB (diagonal-only D=8 world) and NEG-SHIFT
  (mixed-codec world) teachers are new. Per-world induce / ablate /
  hardcode arms with GI-EXPECT/GI-MATCH verdict lines.
- c_build.sh: assemble + compile with pinned znc.
- c_bin: compiled binary.
- c_run1.txt, c_run2.txt, c_run3.txt: 3 deterministic runs.
- REPORT.md: results and verdict GRAMMAR-CODEC-COMPLETE.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. Codec induction is plain functions called
  from gi_induce, not a mode.
- Frozen dirs untouched (grammar_third, grammar_transfer read-only).
- Prereg committed before implementation (commit-order self-check).
- Nothing pushed. Commits local only, explicit pathspecs.
