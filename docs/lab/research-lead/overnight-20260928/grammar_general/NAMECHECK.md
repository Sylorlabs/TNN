# NAMECHECK: Grammar Generalization Worker

## Step 0: Toolchain Guard

Executed at worker startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with NO python3/python paths printed.
`which python3 python` returns nothing. Safebin active.

All computation via pinned znc or compiled Zag binaries.
Shell used only for: invoking znc, running binaries, git ops, file moves.
No Python. No forbidden executables. Zero invocations.

## Frozen artifacts (byte-identical copies)

- `gg_base.zag`: byte copy of `grammar_induction/gi_base.zag`
  SHA-256: a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- `gg_patch_frozen.zag`: byte copy of `grammar_induction/gi_patch.zag`
  SHA-256: ae94800e0167d72aaba3879216699c3be2fbdc5d7c60eeea62428594c3db50d3
  Verified via `cmp`: PATCH-FROZEN-OK

The induction mechanism (gi_induce, gi_ablate, gi_grammar_read,
gi_trial_build2, gi_eval_known) is FROZEN. No modifications.

## New code (driver only)

`gg_driver.zag`: new formal system EXL2, new tests, new classifier.
Contains NO grammar rules for EXL2. Licensor IDs (46/47) and literal
ranges are discovered by the frozen gi_induce, never hardcoded in the
driver's induction path.

## Constraints observed

- Unfrozen only. Frozen source read-only (copied, not modified).
- Pure Zag. Zero em/en dashes (byte-verified before commit).
- Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
- NO hardcoded new grammar: the driver teaches examples; gi_induce discovers.
