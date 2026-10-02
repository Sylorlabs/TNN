# NAMECHECK: Grammar Codec Active-Inquiry Worker

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

Codec Active-Inquiry Worker. Mission: test whether ACTIVE INQUIRY
(the learner requesting a discriminating teaching example) resolves
codec ambiguity instead of refusing. From GRAMMAR-CODEC-COMPLETE:
gi_codec_induce derives D from gcd structure; NEG-AMB (diagonal-only
stream where D=8 vs D=17 both consistent) refused -4 fail-closed. The
ambiguity is inherent to the stream, not the procedure. This worker
adds a general inquiry mechanism: when 2+ divisors are consistent, the
learner requests one teaching example on which the candidate divisors
disagree (naming the hypothesis set, never components/ops/pair
structure), the (driver-simulated) teacher offers the first true fact
that strictly shrinks the consistent set, and induction re-runs.
Unfrozen variant only. Frozen read-only.

## Files (planned)

- PREREG.md: frozen preregistration, committed before implementation.
- NAMECHECK.md: this file.
- i_base.zag: byte copy of grammar_codec/c_base.zag (machinery
  identity; never edited).
- i_patch.zag: c_patch.zag plus the inquiry machinery:
  gi_fact_ok (single-fact op check factored out of gi_codec_op_ok,
  identical semantics), gi_consistent_set (candidate enumeration +
  consistency over W facts plus one hypothetical fact),
  gi_codec_induce2 (returns code plus g and the candidate list),
  gi_codec_induce kept as a thin wrapper, gi_cands_after
  (learner-side simulation of the consistent set if a hypothetical
  fact were added), gi_inquire (emits the GI-INQUIRY request).
- i_driver.zag: c_driver.zag plus NEG-AMB4 teacher (diagonal-only on
  (6,6), true D=8, 4-way ambiguity), the cooperative/refusing teacher
  c_teacher_answer (simulate-and-shrink over the true lattice), the
  QMAX=4 inquiry loop, and per-world query accounting. EXL2/3/4 and
  NEG-SHIFT teachers unchanged.
- i_build.sh: assemble + compile with pinned znc.
- i_bin: compiled binary.
- i_run1.txt, i_run2.txt, i_run3.txt: 3 deterministic runs.
- REPORT.md: results and verdict GRAMMAR-INQUIRY-COMPLETE with the
  query-count table.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. Inquiry is plain functions, not a mode.
- Frozen dirs untouched (grammar_third, grammar_transfer,
  grammar_codec read-only; sources copied, never edited).
- Prereg committed before implementation (commit-order self-check).
- Nothing pushed. Commits local only, explicit pathspecs.
