# NAMECHECK.md -- Invention H3 Repair Worker

## Step 0: Toolchain guard (mandatory)

Executed at startup and before every build/run command batch:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returns nothing. `guard-check-done` printed.
Safebin active for all subsequent commands. Zero forbidden executables
invoked. Pure Zag for all computational research operations. No Python,
no C, no other interpreter at any point.

## Step 1: Identity

Worker: Invention H3 repair (UNFROZEN variant).
Target: the three concrete defects found by the H3 red team
(commit 9ef522189) against the frozen
`invention_constraint/invent_patch.zag`:
- Attack 1 KILL: first DFS hit taken with no scoring; teach order decides
  the form; no continued search after verify-fail.
- Attack 5 KILL: degenerate stuttering chain promoted with check=1;
  `first_lit` (C[20]) never read by invent_dfs.
- Missing: any deterministic tie-breaking policy.
Attack 3 (search scaling) is documented only, per tasking; it needs
redesign, not repair. Attack 4 (constraint smuggling BOUND) is out of
scope for this repair.

## Step 2: Base and mechanism provenance

- Base: `fix_base.zag`, byte-identical copy of the red team's frozen
  `rt_base.zag`. SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  (matches the red-team record, which matches
  `../composition_C/cc_base.zag`). Never modified.
- Frozen mechanism reference: `../invention_constraint/invent_patch.zag`,
  SHA-256
  4fc5493061363bc8ab9a228cb6a67db17f080a01114a5a920efcc87ced47d0bf
  (matches the red team's `rt_mech.zag`). Never modified (frozen,
  read-only).
- Repaired mechanism: `fix_mech.zag` (new, unfrozen). Derived from the
  frozen source; the frozen original is untouched. Repairs:
  (a) full enumeration with verify-and-select instead of first-hit stop;
  (b) invent_dfs reads C[20] (first_lit) with an entry check;
  (c) documented deterministic tie-break policy (fewest repeated values,
  then lexicographically smallest value sequence, then DFS encounter
  order).
- Driver: `fix_driver.zag` (new). Red-team helpers copied verbatim;
  Attacks 1 and 5 rebuilt with IDENTICAL worlds and constraints (kill
  bars not weakened); Attack 2 and the three exact H3 worlds included as
  no-regression checks. Only the expected outcomes changed where a
  defect was repaired (documented in REPORT.md).

## Step 3: Outputs

- `NAMECHECK.md` (this file)
- `REPORT.md`: per-fix verification and re-run verdicts
- `fix_base.zag`: frozen base reference copy (unmodified)
- `fix_mech.zag`: repaired mechanism (new, unfrozen)
- `fix_driver.zag`: verification driver (new)
- `fix_full.zag`: assembled source (base + mech + driver)
- `fix_bin`: compiled binary (pinned znc)
- `fix_compile.txt`: build log (warnings only, same analyzer class as
  the H3 and red-team builds)
- `fix_run1.txt`, `fix_run2.txt`, `fix_run3.txt`: run transcripts,
  3/3 byte-identical (SHA-256
  afcfd91479c20f9fdfee95263116afca7b8b66a10e5ceeb9934053af608d085b)

Pure Zag. Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
No em/en dashes in loop documentation.
