# NAMECHECK: Frontier Backlog Maintainer

## Step 0: Toolchain guard (mandatory)

- Safebin activated: `export PATH="$HOME/safebin"` run at session start.
- `which python3 python` returned nothing (empty output, verified).
- Zero forbidden executables invoked. All work: file reads (`git show`, `head`, `grep`, `ls`), directory creation, document writing, git add/commit.
- Shell used only for: invoking git, moving files, reading files. No computation in shell.

## Scope

Document ONLY. Maintain the frontier backlog of at least 15 substantive research questions per Micah's continuous-operation directive (2026-10-01).

## Input provenance

- Micah's rulings from the parent transcript (2026-10-01): enumerated-schema diagnosis accepted, freeze 4/9, Alt C, H2 approved, H3-lite prereg approved, reuse high priority, copy-and-commit approved, H1 deferred, SUF entrance criterion, standing architectural metric, continuous adaptive learner clarification, lifetime evaluation as primary long-term AGI evaluation, ~10 workers, backlog of at least 15 questions.
- Recent commits surveyed: `ea8fc0ac1` (reuse experiment), `cabe77934` (C160), `c15a47d63` (H2 prereg frozen), `dab50dd68` (H3-lite draft), `8556c3f32` (freeze report corrected), `bc24e8402` (floor erratum), `17768f516` (decision tracker).
- Decision tracker: 4 banked decisions (Decisions 1 and 2 now decided by Micah per latest ruling; tracker predates the ruling and is not edited here).

## Constraints honored

- Document ONLY. No experiments, no source changes, no binaries built.
- Zero em dashes (byte-verified before commit).
- Paper untouched (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` never opened).
- No sealed FW or H2 world contents inspected.
- Nothing pushed. Local commit only.
- No frozen files modified.

## Output

- `FRONTIER_BACKLOG.md`: 18 substantive research questions, ranked by expected information gain, each with question, why it matters, confirm/falsify criteria, dependencies, and ACTIONABLE NOW vs BLOCKED status.
