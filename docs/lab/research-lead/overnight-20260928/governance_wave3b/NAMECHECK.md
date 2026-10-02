# NAMECHECK.md - Governance/Frontier Worker (Wave 3)

## Step 0: Toolchain guard

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no python3/python paths printed. Guard active.

## Step 1: Role confirmation

Governance only. No experiment files modified. Pure shell/git reads. Ledger appends, compression table, hypothesis frontier updates. Zero em/en dashes in all docs (byte-verified before commit).

## Step 2: Scope

- Ledger C190-C196 for constitution-wave results (commits verified via git log).
- Compression table update C190-C195 (mechanisms) per Constitution Section 4.
- Hypothesis frontier: mark tested hypotheses, add new ones.
- Pending: formal_errors (worker active), p2_lifetime (report complete, uncommitted).
- Wave 3 new workers (composition A/B/C, selection, scaling-emergent, strong L2L, formal-understanding, redteam): NOT yet spawned at time of writing. Flagged for parent.
