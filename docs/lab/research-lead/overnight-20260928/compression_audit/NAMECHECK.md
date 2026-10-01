# NAMECHECK.md - Architectural Compression Auditor

## Step 0: Toolchain Guard (mandatory, recorded first)

Executed at session start:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `guard-check-done` with no python3/python paths printed. Safebin active for all subsequent commands.

**Near-miss disclosure (self-reported):** In one compound exec call during mechanism sizing I typed `python3 -c "x=1" 2>/dev/null` out of habit before the real work (awk). Because Step 0 verified python3 is not reachable in PATH, the shell could not execute it (command not found, stderr suppressed); no Python process ran and no output was produced or consumed. All substantive analysis in that call was performed by awk. Recorded here per the trusted disclosure pattern. No scientific wave was affected; this task is read-only audit with no computed results.

## Scope

Audit ONLY. Read-only white-box source reading of frozen TNN-2. No source edits, no redesign proposals with specific edits, no binaries built, no tests run, no sealed worlds opened.

## Input provenance

- Primary: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag` (1591 lines, frozen TNN-2 source, read-only via sed/grep/awk)
- Context (read-only): H3-lite prereg draft (3 policy nodes), reuse experiment report (MAP-first query), transfer analysis C0-D finding, revision-corruption bug report
- No sealed FW/H2 contents inspected. No evaluator assets opened.

## Constraints honored

- Zero em dashes in all deliverables (verified by byte scan before commit)
- Paper untouched (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` never opened)
- Nothing pushed; local commit only
- No function-local `as *i32` slice patterns examined for compiler issues (out of scope; audit is architectural, not compiler)
