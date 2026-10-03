# NAMECHECK: Cross-Domain Grammar to Construction Worker

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

Toolchain idioms honored (AGENTS.md): u8-backed cells with
little-endian get32/set32 pack/unpack; no `as *i32` + slice
construction (z_alloc uses the proven `_zag_malloc` + `*u8` slice
pattern); output via e1str/e1i64 into one preallocated buffer with a
single `_zag_raw_syscall(1,1,ptr,len)` write, never `_zag_print` for
dynamic content; every binary's stdout bytes verified before trust.

## Worker identity

Cross-Domain Grammar to Construction Worker. Mission: test whether an
induced grammar (divisor D plus literal ranges, induced per the
grammar_codec method) can CONSTRAIN a grammar-blind composition
mechanism through a GENERIC constraint channel (shared learner-state
clause registry), with ZERO per-grammar wiring of the grammar into
the composer. Arms: N (no channel: blind pick over all candidates;
grammar sits inert) vs C (channel: blind pick over reg_check
survivors). Plus a representational fidelity probe (clause check vs
independent direct grammar check on every candidate) to separate the
representational diagnosis from the architectural/control diagnosis.
Unfrozen variant only. Frozen read-only (grammar_codec used as method
reference only; no frozen file read for code, none modified).

## Files (planned)

- PREREG.md: frozen preregistration, committed alone before
  implementation (commit df4c874e2, commit-order self-check).
- NAMECHECK.md: this file.
- x_main.zag: full experiment. Sections: generic machinery (alloc,
  cells, emit); generic constraint registry (clause ABI, reg_write,
  reg_check); grammar induction (teach, gcd, candidates, op-check,
  range induction, compile to clauses); COMPOSER (grammar-blind:
  candidate generation over codec hypotheses {8,16,32}, blind
  fewest-words rule, arm selector); fidelity probe (independent direct
  check); driver (2 worlds x 6 trials x 2 arms, XD- lines).
- x_build.sh: compile with pinned znc.
- x_bin: compiled binary.
- x_compile.txt: compiler output.
- x_run1.txt, x_run2.txt, x_run3.txt: 3 deterministic runs.
- REPORT.md: results and verdict XDOMAIN-GRAMMAR-COMPLETE.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. The registry is a shared learner-state
  table with generic operations, not a mode or bridge. The arm
  selector is an experiment-harness condition flag, not a cognitive
  mode; the composer itself (generation + blind rule) has no flags.
- No manual wiring: composer section references only reg_check and
  generic clause fields; K5 grep audit in REPORT.
- Prereg committed before implementation.
- Nothing pushed. Commits local only, explicit pathspecs.

## Results (2026-10-02)

3/3 runs byte-identical
(SHA-256 b8070d0eaa22c039331496c76eb2eeade28ff54a54dc357a779149f1e5bc921d).

- W16: XD-INDUCED r=1 D=16 lo=1 hi=7. W8: XD-INDUCED r=1 D=8 lo=1 hi=7.
- Arm N (no channel): 0/12 well-formed. Picks the 1-word h=8
  candidate every trial (fewest-fields bias); the induced grammar,
  compiled and present in learner state, shapes nothing.
- Arm C (generic channel): 12/12 well-formed. Same composer,
  filtering through reg_check.
- Fidelity probe: 936/936 clause/direct agreements (78 candidates x
  12 trials). Representational form adequate.
- K5 no-wire audit: composer section (x_main.zag lines 222..298) has
  zero code references to grammar concepts, zero reads of
  induced-rule cells, one external call (reg_check). direct_check
  called only from the probe and driver scoring.

Diagnosis: learned knowledge does NOT automatically constrain
generation; the gap is architectural/control (no channel, composer
never queries), not representational. One generic clause-ABI channel
closes it 0/12 -> 12/12 with zero per-grammar wiring.

Commit-order self-check: prereg commit df4c874e2 strictly precedes
the implementation commit.
