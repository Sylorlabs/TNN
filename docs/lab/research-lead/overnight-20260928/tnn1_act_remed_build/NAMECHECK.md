# NAMECHECK.md: TNN-1 ACT Remediation Builder

Date: 2026-09-30. Worker: TNN-1 ACT Remediation Builder (subagent).
Task: Port the full ACT 24/24 suite into TNN-1.

## Step 0: Toolchain guard check

Safebin setup (per AGENTS.md mandatory safebin rule):
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no python3/python paths printed.
`which python3` returns nothing under the restricted PATH.
Safebin activated at task start. All subsequent shell work uses
`export PATH="$HOME/safebin"` prefix.

This is a builder task (Zag implementation). Pure Zag for all
computational research. Shell only for znc invocation, binary
execution, git ops, file moves. Zero forbidden invocations.

## K1 ordering

Prereg: `docs/lab/research-lead/overnight-20260928/tnn1_act_remed/ACT_REMED_PREREG.md` @ `669aeb56b`.
Review disposition: `docs/lab/research-lead/overnight-20260928/tnn1_act_remed/REVIEW_DISPOSITION.md` @ `10a9b2d0d`.
K1 anchor: `10a9b2d0d`. Implementation commit must strictly follow it.
Verified via `git merge-base --is-ancestor 10a9b2d0d HEAD` before results commit.

## Scope

Owned path: `docs/lab/research-lead/overnight-20260928/tnn1_act_remed_build/` only.
Read-only on: prereg, TNN-1 build (`tnn1_build/tnn1.zag` @ `0323b97d5`),
ACT standalone (`act_build/act.zag`).

Governance: no em dashes; contaminated paper
`TNN_RESEARCH_PAPER_20260929.md` zero-diff; no sealed FW1-FW9
accessed; explicit pathspecs only.
