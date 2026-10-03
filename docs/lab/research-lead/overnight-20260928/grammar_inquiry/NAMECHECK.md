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

## Results (2026-10-02)

3/3 runs byte-identical
(SHA-256 5d47d7da804b1bc066ce9e2848acf9d8b7c343ed47b609536e6964962fe78c73).
GI-VERDICT 7/7 against the frozen prereg:

- EXL2: GI-INDUCED 1, D=16, a=[0,9] b=[0,9]; induce 6/6 class 1;
  ablate 0/6; hardcode 6/6; zero GI-INQUIRY lines.
- EXL3: GI-INDUCED 1, D=8, a=[0,7] b=[0,7]; induce 4/4; ablate 0/4;
  hardcode 4/4; zero GI-INQUIRY lines.
- EXL4: GI-INDUCED 1, D=32, a=[0,3] b=[0,3]; induce 2/2; ablate 0/2;
  hardcode 2/2; zero GI-INQUIRY lines.
- NEG-AMB: -4 triggered inquiry; teacher answered (34,42,2); 1 query
  issued / 1 answered; resolved to the true D=8, a=[2,6] b=[2,6];
  battery 1/1 class 1.
- NEG-SHIFT: GI-INDUCED -3, zero GI-INQUIRY lines (contradiction is
  not ambiguity; inquiry never fired).
- NEG-AMB-R: teacher refused; 1 query issued / 0 answered; terminal
  -4, GI-GRAMMAR none (fail-closed preserved).
- NEG-AMB4: -4 with 4-way ambiguity {8,17,26,53}; Q1 (18,41,0)
  narrowed to {8,17}; Q2 (34,42,2) narrowed to {8}; 2 queries
  issued / 2 answered; resolved to the true D=8, a=[6,6] b=[6,6];
  battery 1/1 class 1.

Query-count table: EXL2 0/0, EXL3 0/0, EXL4 0/0, NEG-AMB 1/1,
NEG-SHIFT 0/0, NEG-AMB-R 1/0, NEG-AMB4 2/2.

K3 check: `grep` for divisor literals on i_patch.zag returns only the
same two comment lines as the codec worker; the inquiry names no
components, no op, no pair structure; candidates derive only from
divisors of the observed gcd.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. Inquiry is plain functions, not a mode.
- Frozen dirs untouched (grammar_third, grammar_transfer,
  grammar_codec read-only; sources copied, never edited).
- Prereg committed before implementation (commit-order self-check).
- Nothing pushed. Commits local only, explicit pathspecs.
