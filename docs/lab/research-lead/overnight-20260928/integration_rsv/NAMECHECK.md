# NAMECHECK: Integration Worker (Reliability to Substrate to Verification)

## Step 0: Toolchain guard (mandatory)

Activation:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returns nothing. 42 tools in safebin.
Guard check recorded 2026-10-01. Zero forbidden executables invoked.

## Provenance

- Worker: Integration Worker (Reliability to Substrate to Verification).
- Mission: Integrate C181 + C183 + C185 per Constitution One-System Rule.
- Parent task: Micah Priority 10 / governance gap "C181 + C183 + C185 combined".

## Inputs (commits verified via git log)

- C181 learner-verification: `d52666a8b` (reliability replaces expected).
- C183 provenance-learning: `96fa237b1` (source reliability from consequences).
- C185 substrate-expansion: `02a338dbf` (5 behaviors, one substrate).

## Base

- `rsv_base.zag`: copy of `se_base.zag` (frozen sc_base a29972ca, minus
  evict_node/miss_inquire/ev_query). Reference only, not modified.
- `rsv_machinery.zag`: copy of `se_machinery.zag` (substrate primitives).
- `rsv_behaviors.zag`: copy of `se_behaviors.zag` (5 behaviors).
- `rsv_patch.zag`: NEW integration (prediction + source + verification).
- `rsv_driver.zag`: NEW test batteries.

## Constraints honored

- Unfrozen variant only. Frozen source read-only.
- Pure Zag via pinned znc `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Safebin PATH active. Zero Python invocations.
- Zero em/en dashes in docs (byte-verified before commit).
- Research paper untouched. Nothing pushed. Explicit pathspecs.
- 0 modes, 0 bridges, 0 handlers, 0 semantic cases added.
