# NAMECHECK.md

## Step 0: Toolchain Guard

**Date:** 2026-10-01
**Worker:** Theater Auditor
**Mode:** AUDIT ONLY (read-only, no source edits)

### Toolchain verification

```bash
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

**Result:** `which python3 python` returned nothing. Safebin active. Zero forbidden executables invoked.

### Scope

Audit TNN-2 (`docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`, 1591 lines, frozen) for theater: learner-state values with no exercised production write path, or no production read path.

### Input provenance

- TNN-2 source: `tnn2_build/tnn2.zag` (read-only via grep/sed)
- Criterion mechanism analysis: commit `8a2ff4b77` (D6, D7 theater findings)
- DOF map: commit `d2af26581` (0 learner / 5 mixed / ~240 researcher)
- SUF check: commit `8ef148a42`

### Constraints honored

- Audit ONLY. No fixes proposed. No source edits.
- Read-only white-box inspection (grep, sed for viewing).
- No sealed worlds opened.
- Zero em dashes (verified).
- Paper untouched. Nothing pushed.
