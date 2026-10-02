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

## Results (2026-10-02)

3/3 runs byte-identical
(SHA-256 173a69f1fa4e060c94b100d221717f0efc4fdf74b56ab2e20f8a9d16edad42c4).
GI-VERDICT 5/5 against the frozen prereg:

- EXL2: GI-INDUCED 1, D=16, a=[0,9] b=[0,9]; induce 6/6 class 1;
  ablate 0/6 (class 2); hardcode 6/6.
- EXL3: GI-INDUCED 1, D=8, a=[0,7] b=[0,7]; induce 4/4 class 1;
  ablate 0/4; hardcode 4/4. (The world that went silently wrong under
  hardcoded /16 now induces the true codec and true ranges.)
- EXL4: GI-INDUCED 1, D=32, a=[0,3] b=[0,3]; induce 2/2 class 1;
  ablate 0/2; hardcode 2/2.
- NEG-AMB: GI-INDUCED -4 (ambiguous: D=8 and D=17 both consistent),
  GI-GRAMMAR none, GI-I-NOGRAMMAR.
- NEG-SHIFT: GI-INDUCED -3 (contradicted: g=1), GI-GRAMMAR none,
  GI-I-NOGRAMMAR.

K3 check: `grep -n "/16\|\*16"` on c_patch.zag returns only two
comment lines; no codec divisor literal in machinery logic (the 8/16/32
matches are node field offsets, buffer sizes, and the pre-existing
nlic<16 capacity bound). Candidates come only from divisors of the
observed gcd.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. Codec induction is plain functions called
  from gi_induce, not a mode.
- Frozen dirs untouched (grammar_third, grammar_transfer read-only).
- Prereg committed before implementation (commit-order self-check:
  prereg commit 7f3d9caae precedes the implementation commit).
- Nothing pushed. Commits local only, explicit pathspecs.
