# NAMECHECK: Grammar Transfer Worker

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
file moves/copies, checksums, diffs.

## Worker identity

Grammar Transfer Worker. Mission: test whether the grammar induction
machinery (commit 62c6a7734) transfers to a second formal system EXL2
with different operators and constraint shape, with the induction code
byte-identical. Unfrozen variant only. Frozen read-only.

## Files

- gt_base.zag: byte copy of grammar_induction/gi_base.zag.
  SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  (matches source).
- gt_patch.zag: byte copy of grammar_induction/gi_patch.zag.
  SHA-256 ae94800e0167d72aaba3879216699c3be2fbdc5d7c60eeea62428594c3db50d3
  (matches source). THE machinery-identity proof.
- gt_driver.zag: experiment driver. Teaching section rewritten for EXL2
  (SUB/DIV examples); arm functions gi_report_grammar, gi_arm_induce,
  gi_arm_base, gi_arm_hardcode byte-identical to gi_driver.zag
  (verified with cmp); gi_test_targets uses EXL2 targets; main adds
  W5a/W5b contradiction arms.
- gt_build.sh: assemble + compile with pinned znc.
- gt_bin: compiled binary.
- gt_run1.txt, gt_run2.txt, gt_run3.txt: 3 deterministic runs,
  byte-identical (SHA-256 ed1cce4063683a8d65309fee5715992d7a0b177b1a570ed2b0ec3b2f8f43488f).
- REPORT.md: results and verdict.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. 0 new semantic cases. 0 base modifications.
- NO hardcoded EXL2 grammar: induction discovers licensor relations
  {44,43} from data; no 43/44 literals in the induction or construction
  path of gt_patch.zag (it is byte-identical to the EXL patch).
- Relation-id labels 41/42/43/44/45 reused for EXL2 by documented
  design decision (world labeling convention, not machinery change);
  all operator semantics come from the example stream.
- Nothing pushed. Commits local only.
