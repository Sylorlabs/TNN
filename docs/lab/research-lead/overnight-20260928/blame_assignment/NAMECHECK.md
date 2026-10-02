# NAMECHECK: Blame Assignment Analyst

## Step 0: Toolchain guard

Executed at task start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. `guard-check-done` printed.
Safebin active. Zero forbidden executables invoked during this task.
All source inspection via `sed`/`grep` (read-only). No binaries built.
No evaluators run. Analysis only.

## Scope

ANALYSIS ONLY. Read-only white-box inspection of frozen TNN-2
(`docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`,
1591 lines, build `f4de7ff46`). No source edits, no implementation,
no new files outside this directory.

## Input provenance

- Revision substrate report `880c87c4c`
  (`revision_substrate/REVISION_SUBSTRATE.md`): copy-and-commit +
  MAP retargeting, V1/V2/V3 results, honest scope.
- Plan constructor analysis `61402fd25`
  (`plan_constructor/PLAN_CONSTRUCTOR_ANALYSIS.md`): G1-G6 gaps,
  open question 4 (blame assignment in composed-plan revision),
  SUF relation.
- Criterion mechanism `8a2ff4b77`
  (`criterion_mechanism/CRITERION_MECHANISM.md`): D4 revision
  acceptance is researcher-owned (source literal).
- Frozen source line references verified by direct read:
  `revise_on_contradict` (line 685), `t2_revise_graph` (line 706),
  `contradict_map` (line 578), `ev_observe` (line 840).

## Constraints honored

- No sealed worlds opened.
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- Nothing pushed. Commits local only.
- Zero em dashes (byte-verified before commit).
- No new cognition lines, modes, bridges, handlers, semantic cases.
