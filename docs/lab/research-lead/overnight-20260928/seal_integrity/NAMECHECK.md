# NAMECHECK.md - Sealed World Integrity Checker

## Step 0: Toolchain Guard (mandatory)

Activated: 2026-10-01 UTC.

Commands run:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with NO output from `which python3 python`.
Python3 and python do NOT resolve in the safebin PATH. Zero forbidden
executables invoked. Pure safebin toolchain confirmed.

## Scope

Verification only. No inspection of sealed world contents. No source edits
to any research artifacts. Owned path:
`docs/lab/research-lead/overnight-20260928/seal_integrity/`

Read-only on all sealed assets, the freeze prereg commit, and git history.
The TNN research paper is untouched.

## Verdict target

SEAL-INTEGRITY-CHECK-COMPLETE (or SEAL-INTEGRITY-VIOLATION if found).
