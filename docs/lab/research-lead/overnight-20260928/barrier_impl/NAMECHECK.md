# NAMECHECK: Barrier-Break Implementer

## Step 0: Toolchain Guard (mandatory)

**Date:** 2026-10-01 UTC
**Worker:** Barrier-Break Implementer (subagent)

### Safebin activation

```sh
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

**Result:** `which python3 python` returned nothing. `guard-check-done` printed.
Zero forbidden executables invoked. All computation in Zag via pinned
`znc_linux_x86_64_abed8aa1` (resolved from safebin).

### UNFROZEN VARIANT DECLARATION

This work is on an **UNFROZEN VARIANT ONLY**.

- Base: `../xfer_experiment/tnn2_xfer_variant.zag`
  (SHA-256: `655d94bde41f1f2890a2b287f6bcf42db2123f6b9239caacbd93b22f360c3403`)
- Copy: `tnn2_barrier_variant.zag`
  (SHA-256 verified identical before modification: `655d94bde41f1f2890a2b287f6bcf42db2123f6b9239caacbd93b22f360c3403`)
- Frozen `tnn2.zag`, `tnn2_bin`, build `f4de7ff46`: **UNTOUCHED**.
- Frozen xfer variant source/binary: **UNTOUCHED** (read-only source).

Per Micah: "try stuff unfrozen as you go on." This is an experiment,
not TNN-3 implementation.

## Scope

Implement barrier-1 break (visibility) ONLY, per design `f0f223029`:
- `gather_structures(W)` helper (~15 lines)
- Call site in `t2_gather` (~3 lines)
- White-box counters `hg(W,53)` (visible) and `hg(W,54)` (referenced)
- Counter init in `tnn2_init`

Do NOT implement barriers 2/3/4. No new opcodes, modes, bridges,
handlers, semantic cases. No hardcoded cross-domain mappings.

## Input provenance

- Design: `f0f223029` (BARRIER-BREAK-DESIGN-COMPLETE), read-only.
- Xfer experiment: `cbd7bc803` (XFER-EXPERIMENT-COMPLETE), read-only.
- Xfer probes: `../xfer_experiment/xfer_probes.zag`, read-only basis for
  barrier probes.

## Constraints

- UNFROZEN ONLY. Frozen source/binary untouched.
- Implement ONLY barrier 1 (not 2/3/4).
- Zero em dashes in documentation (byte-verified before commit).
- Paper untouched. Nothing pushed. Local commits only.
- 3/3 byte-identical runs required for probe results.
- Honest reporting: the predicted result is ZERO transfer with
  53 > 0 and 54 = 0. Report what actually happens.
