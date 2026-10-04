# NAMECHECK: Persistent Cross-Domain Connections Worker

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

Build persistent A-B connections, not just functional reuse (Micah Priority 2).
Unfrozen variant only. Frozen TNN-2 source read-only.

## Input provenance

- Base cognition: `../rebinding_adversary/adv_base.zag`, SHA-256 prefix
  `a29972ca8183b285`, verified equal to frozen TNN-2 base.
- Rebind mechanism: `../rebinding_adversary/adv_patch.zag` (vanilla rebind,
  used verbatim for the control arm).
- World-stream pattern: `../spontaneous_lifetime/sl_driver_treat.zag`.

## Mechanism delta (this worker)

`pc_patch.zag` replaces `ev_query`/`rebind_try`:
- LINK edge type 14 (unused in base), written built-MAP -> helper-MAP on
  every verified rebind. Written by the rebind success event, never by
  the driver. No researcher-authored A-B mapping.
- `rebind_try` pass 1: MAPs with outgoing type-14 edge, newest first.
  Pass 2: all other MAPs in id order.
- `pc_del_links`: edge-table scan deleting type-14 edges (ablation).

## Constraints

Pure Zag via pinned znc. Zero em/en dashes in docs. Paper untouched.
Nothing pushed. 0 modes, 0 bridges, 0 handlers, 0 semantic cases.
