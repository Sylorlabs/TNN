# NAMECHECK.md: TNN-2 Revision Red Team

Date: 2026-09-30. Task: Aggressive red-team review of TNN-2's generic revision operator.

## Step 0: Toolchain guard check

Safebin activated at task start:
```
mkdir -p $HOME/safebin
(for 19 tools) ln -sf $(which $t) $HOME/safebin/$t
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned nothing. PATH restricted to `/home/hatch/safebin`.
Zero forbidden invocations during this task.

This is analysis-only work: source reading via `read`/`grep`, no research
computation, no scoring, no binary execution of research code. No Python
invoked at any point.

## Scope

Owned path: `docs/lab/research-lead/overnight-20260928/tnn2_redteam_revision/`

Contains: NAMECHECK.md (this file), REVISION_REDTEAM.md (attack report).

Target (read-only): `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
at commit `f4de7ff46` (SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
1591 lines). Focus: `revise_on_contradict` (line 685), `t2_revise_graph`
(line 706), test `t_t2_revise` (line 1275).

## Governance

- Read-only on `tnn2_build/`. Nothing modified.
- No em dashes (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff.
- No sealed FW assets accessed.
- Explicit pathspecs only.
