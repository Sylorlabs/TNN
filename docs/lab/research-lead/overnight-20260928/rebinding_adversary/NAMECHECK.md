# NAMECHECK.md -- Rebinding Adversary

## Step 0: Toolchain Guard (MANDATORY, recorded 2026-10-01)

Wave 1 (2026-10-01, first attempt):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty). Only
`guard-check-done` printed. Safebin active. Zero forbidden executables
invoked in this wave.

Wave 2 (2026-10-01, retry/extension): same safebin reused; `which
python3 python` again returned nothing under `$HOME/safebin` PATH.
Pinned znc at `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Zero forbidden executables invoked. Verified before any compile.

## Scope

ADVERSARIAL EXPERIMENT ONLY. Unfrozen variant. This worker attacks the
structural rebinding mechanism from `91585087c` (REBINDING-COMPLETE PASS)
with seven adversarial worlds:

Wave 1 (built, ran 3/3 byte-identical, never committed):
1. Non-chain topology (COUNT/SUM MAPs in A; COUNT query in B)
2. Deceptive MAP (corrupted chain internals in A)
3. Scale attack (20 chain MAPs, correct one last)
4. Poisoned MAP (wrong stored answer; masked-query order dependence)

Wave 2 (extension, this retry):
5. Negative transfer (10 chain MAPs, then a COUNT query; fresh control)
6. Ambiguous selection (two plen-5 paths to one endpoint; teach order
   swapped; promoted MAP's DEP edges dumped to identify bound path)
7. Depth mismatch / partial applicability (plen-5 MAPs, B needs plen-4
   chain with a plen-5 decoy; fresh control)

## Input provenance

- `adv_base.zag`: verbatim copy of `rb_base.zag` from `91585087c`
  (frozen TNN-2 + trial machinery, SHA-256 verified before use).
- `adv_patch.zag`: verbatim copy of `rb_patch.zag` from `91585087c`
  (rebinding mechanism, unfrozen pilot).
- `adv_driver.zag`: this worker's adversarial worlds (new).
- Frozen source: read-only. Never modified.

## Constraints

- Unfrozen variant only. Frozen source untouched.
- Pure Zag via pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell: znc invocation, binary runs, git ops, file moves only.
- Zero em/en dashes in all docs (byte-verified before commit).
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- No sealed worlds. Nothing pushed (local commits only).
