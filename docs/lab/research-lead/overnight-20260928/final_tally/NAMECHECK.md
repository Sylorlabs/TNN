# NAMECHECK.md - Final Tally Worker

**Step 0: Toolchain guard (mandatory, performed before any work)**

Safebin setup and verification commands run at worker startup:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which` itself was missing from safebin after the PATH switch, so it was linked in from the system path first, then `which python3 python` returned NOTHING. `guard-check-done` printed with no preceding output. 41 tools in safebin. Zero forbidden executables available in PATH.

Second verification: `which python3 python` under `$HOME/safebin` PATH returned empty again at tally time.

**Scope:** Tally only. No new analysis, no new documents counted as authored work, no source edits, no sealed-world inspection. Read-only on git log, filesystem counts, and committed reports.

**Input provenance:** git log on branch `tnn-native-lab`, `find` counts under `docs/lab/research-lead/overnight-20260928/`, the canonical ledger file, `bar_inventory/BAR_INVENTORY.md`, `bundle_v16_prep/BUNDLE_V16_INVENTORY.md`, `untracked_inventory/UNTRACKED_INVENTORY.md`, and the parent transcript's coordinator_completion handoffs.

**Constraints honored:** Owned path only (`docs/lab/research-lead/overnight-20260928/final_tally/`). Zero em dashes (byte-verified). Paper untouched. Nothing pushed. Commits local only.
