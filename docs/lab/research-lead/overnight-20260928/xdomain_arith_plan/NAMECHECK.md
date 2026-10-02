# NAMECHECK: xdomain_arith_plan (Cross-Domain Arithmetic-Planning Worker)

## Step 0: Toolchain Guard (mandatory, executed first)

Respawn worker executed at startup, 2026-10-02, before any research
computation:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty output before
"guard-check-done"). Safebin PATH active for all subsequent commands.

## Step 1: Task Identity
- Worker: Cross-Domain Arithmetic-Planning (Battery B).
- Mission: Test H1 (typed contracts) and H2 (value composition) generality on arithmetic→planning.
- Verdict target: XDOMAIN-ARITH-PLAN-COMPLETE.

## Step 2: Constraints Acknowledged
- Unfrozen only. Frozen source read-only.
- Pure Zag. Zero em/en dashes (byte-verified before commit).
- Paper untouched: docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md never modified.
- Nothing pushed (local commits only).
- 0 modes/bridges/handlers. No ARITH_TO_PLAN template.
- Explicit pathspecs for all git operations.
- Preregistration strictly precedes implementation.
