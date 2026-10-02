# NAMECHECK: TNN-2 Developmental Transfer Analysis

## Step 0: Toolchain guard

Executed at worker start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no python3/python path printed. Safebin active.
All computation in this analysis is pure Zag (compiled with the pinned
`znc_linux_x86_64_abed8aa1`) plus shell/git orchestration only.
No Python, C/C++, JavaScript, or other implementation language invoked.

## Step 1: Identity

Worker: TNN-2 Developmental Transfer Analyst (subagent of the TNN research
coordinator). Analysis only; no authority to modify frozen artifacts.

## Step 2: Frozen inputs (read-only)

- `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  (verified before deriving probe build; matches frozen commit `f4de7ff46`)
- `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2_bin`
  SHA-256: `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`
- TNN-1 comparison source:
  `docs/lab/research-lead/overnight-20260928/tnn1_act_remed_build/tnn1_act.zag`
  (read-only; source audit only, not executed)

## Step 3: Owned path

`docs/lab/research-lead/overnight-20260928/tnn2_transfer/`

## Step 4: Method

Derived probe binary `tnn2_transfer_bin`, built by concatenating the frozen
TNN-2 source with its test `fn main` line removed and the probe driver
`transfer_driver.zag` appended (same splice technique as the freeze shims).
TNN-2 functions are byte-identical to frozen; only the entry point differs.
Probes run multi-stage probe sequences against ONE shared learner workspace
per probe set, exercising the public interface
(`ev_teach`, `ev_query`, `ev_observe`, `ev_act`) plus white-box inspection
helpers (`find_map`, `count_tag`, `t2_sig`, `t2_exec`) that read but never
write learner state.

## Step 5: Constraints honored

- No modification of `tnn2_build/` (verified read-only; derived copy only).
- No sealed FW1-FW9 assets touched.
- No em dashes in loop documentation.
- Pure Zag for all computation; shell only for compile/run/git.
- Paper `TNN_RESEARCH_PAPER_20260929.md` untouched.
