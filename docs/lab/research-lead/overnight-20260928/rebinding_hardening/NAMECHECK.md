# NAMECHECK.md -- Rebinding Hardening (Scale/Deception)

## Step 0: Toolchain Guard (MANDATORY, recorded 2026-10-01)

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
`guard-check-done` printed. Safebin active. Pinned znc at
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Zero forbidden executables invoked. Verified before any compile.

## Scope

ADVERSARIAL HARDENING ONLY. Unfrozen variant. This worker attacks the
structural rebinding mechanism from `91585087c` (REBINDING-COMPLETE PASS,
hardened in `db263d74c` REBIND-ADV-COMPLETE) with four new hardening
worlds per Micah Priority 3:

1. H1 Scale 100: A has 100 chain MAPs (95 wrong-plen decoys + 4 wrong
   plen-5 + 1 correct plen-5 last). B needs plen-5. Measures verifies,
   wall time, completion.
2. H2 Deceptive similar: A has 5 plen-5 MAPs from different A-worlds
   (functionally identical shape, different provenance). B has two
   plen-5 paths (one correct, one wrong endpoint). Tests whether
   verification selects correctly with multiple identical-shape MAPs.
3. H3 Partial applicability: A has plen-4 MAP. B needs plen-5.
   Tests adaptation vs exact reuse (expect: all-or-nothing, fallback).
4. H4 Adaptation: A has plen-4 and plen-6 MAPs. B needs plen-5.
   Tests extend/truncate (expect: no adaptation, fallback).

Each world: treatment (experienced) vs fresh control. 3/3 byte-identical
per test, except H1 which may run 1x if too slow (documented).

## Input provenance

- `hard_base.zag`: verbatim copy of `rb_base.zag` from `91585087c`
  (frozen TNN-2 + trial machinery, SHA-256 verified before use).
- `hard_patch.zag`: verbatim copy of `rb_patch.zag` from `91585087c`
  (rebinding mechanism, unfrozen pilot, verified by diff against
  `adv_patch.zag` from `db263d74c`).
- `hard_driver.zag`: this worker's hardening worlds (new).
- Frozen source: read-only. Never modified.

## Constraints

- Unfrozen variant only. Frozen source untouched.
- Pure Zag via pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell: znc invocation, binary runs, git ops, file moves only.
- Zero em/en dashes in all docs (byte-verified before commit).
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- No sealed worlds. Nothing pushed (local commits only).
