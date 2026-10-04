# NAMECHECK: Formal Understanding Worker

## Step 0: Toolchain guard

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
Result: `which python3 python` returned nothing. Safebin PATH active.
Guard check recorded. No forbidden executable invoked.

## Scope

Formal system mastery then novel construction (Micah Section 8,
Constitution Sections 7 and 27). Unfrozen variant only. Frozen TNN-2
source read-only.

## Input provenance

- Base cognition: `fu_base.zag`, byte copy (`cmp`-verified) of
  `../formal_errors/fe_base.zag`, which is itself a byte copy of the
  frozen TNN-2 base (SHA-256 prefix `a29972ca8183b285`, per
  persistent_connections/NAMECHECK.md).
- `fu_patch.zag`: new `fu_`-prefixed functions only. No base function
  is redefined. Treatment search (`fu_trial_build`) is a separate
  function; the base `t2_trial` is untouched and used for the control
  arm.
- `fu_driver.zag`: experiment driver (teaching, mastery, batteries,
  probes, `main`).
- Build strips `main` from the base copy (pinned znc rejects duplicate
  fn definitions) and concatenates base + patch + driver.

## Formal system under test

Tiny expression language EXL:
- Literals 0..9.
- Operators ADD (+), MUL (*).
- Grammar: E := ADD(lit,lit) | MUL(lit,lit) (one-level binary).
- Constraint: every value < 64; operators only ADD/MUL.
- Semantics: standard arithmetic.
- Pair encoding P(a,b) = a*16+b (injective for a,b in 0..15).
- Relations: ADD=41, MUL=42, DADD=43, DMUL=44, BUILD=45, SUB=46.

## Constraints

Pure Zag via pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
Zero em/en dashes in docs. Paper untouched. Nothing pushed.
0 modes, 0 bridges, 0 handlers, 0 semantic cases.
