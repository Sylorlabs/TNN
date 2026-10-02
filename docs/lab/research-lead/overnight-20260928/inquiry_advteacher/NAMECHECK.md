# NAMECHECK: Adversarial Teacher Worker

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

Adversarial Teacher Worker. Mission: test whether the active-inquiry
mechanism (GRAMMAR-INQUIRY-COMPLETE: learner names the candidate
divisor set on -4, teacher provides a discriminating fact,
re-induction resolves) can be exploited by an adversarial teacher.
Three attacks, all on NEG-AMB worlds (true D=8, literals {2,4,6},
diagonal-only teaching, g=18, consistent set {8,17}):
- ADV-LIE: false fact (35,42,2) that kills the true divisor d=8 and
  keeps the wrong divisor d=17. Tests lie detection.
- ADV-WASTE: true-but-non-discriminating facts
  (20,41,-2),(34,41,2),(38,41,-2),(52,41,2) until QMAX exhausts.
  Tests query-budget conservation.
- ADV-POISON: false decomp fact (0,43,63), invisible to the op check
  (relations 43/44 never scanned), trusted into W, corrupting the
  induced grammar's literal ranges to a=[2,7] b=[2,7] while D=8
  still resolves. Tests verification of the inquiry channel.
Plus ADV-CTRL: cooperative teacher reproducing grammar_inquiry NEG-AMB
as a driver-fidelity control. Unfrozen variant only. Frozen read-only:
grammar_inquiry/ sources are copied byte-identical, never edited.
Scoring is KILL/SURVIVE/BOUND per teacher against the preregistered
rubric. Do NOT fix what is killed.

## Files

- PREREG.md: frozen preregistration, committed before implementation
  (commit-order self-check).
- NAMECHECK.md: this file.
- a_base.zag: byte copy of grammar_inquiry/i_base.zag (never edited).
- a_patch.zag: byte copy of grammar_inquiry/i_patch.zag (learner
  machinery unchanged; never edited).
- a_driver.zag: adversarial driver: NEG-AMB teaching (copied),
  cooperative teacher (copied, ADV-CTRL), the three adversarial
  teachers (plain functions, 0 modes/bridges/handlers), the QMAX=4
  inquiry loop, per-world reporting, and a single-target battery on
  code==1 worlds.
- a_build.sh: assemble (strip base main, concatenate) + compile with
  the pinned znc. Pure shell + znc.
- a_full.zag: assembled source. a_compile.txt: compiler output.
- a_bin: compiled binary.
- a_run1.txt, a_run2.txt, a_run3.txt: 3 deterministic runs.
- REPORT.md: results, per-teacher scores, verdict
  INQUIRY-ADVTEACHER-COMPLETE.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. Teachers are plain driver functions.
- Frozen dirs untouched (grammar_inquiry/ read-only; sources copied,
  never edited; SHA-256 verified).
- Prereg committed before implementation (commit-order self-check).
- Paper untouched. Nothing pushed. Commits local only, explicit
  pathspecs.
