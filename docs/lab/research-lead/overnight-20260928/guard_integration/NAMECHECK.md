# NAMECHECK: Guard Integration

## Step 0: Toolchain guard

- Date (UTC): 2026-10-01
- Safebin: activated at `$HOME/safebin` with 17 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack).
- `which python3 python` returned nothing (empty output, verified).
- Zero forbidden executables invoked during this task. All work was
  reading committed markdown via `git show` and writing new markdown.
- No code written or executed. Integration spec only.

## Scope

- Integrate only. No new guards, no new bars, no implementation,
  no source edits.
- Owned path only:
  `docs/lab/research-lead/overnight-20260928/guard_integration/`

## Inputs (read-only)

- Treadmill guard `1646b9732`
  (`treadmill_guard/TREADMILL_GUARD.md`): 5 checks, 7 per-capability
  treadmill analyses, 8 warning signs, 3 guard-gaming modes.
  Explicitly a development discipline document, not a kill bar.
- TNN-3 preregistration structure `206499c03`
  (`tnn3_prereg_struct/PREREG_STRUCTURE.md`): 10-section outline,
  17-bar inventory, dependencies, order, gaps, 6 open questions for
  Micah. DRAFT-NOT-FROZEN.
- Floor spec `f383dd11c`: the 6 floor capabilities F1/F2/F3/G1/G2/G3
  and the anti-gaming clause (criterion 4).
- SUF property definition `64eec921f`: Source-Underdetermined Form
  and its operational test (section 5).
- Re-clustering draft `ed2357141`: cause clusters R1/R2/R3.

## Constraints honored

- No sealed FW or GW world contents inspected.
- Research paper
  (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`)
  untouched.
- The two input documents were not edited. This task specifies
  insertion points and drafts the integration text only.
- No em dashes in this file or in GUARD_INTEGRATION.md (verified
  by byte scan before commit).
- Nothing pushed. Local commit only.

## Verdict

GUARD-INTEGRATION-COMPLETE on commit of GUARD_INTEGRATION.md.

---

# Addendum: Issue Fixer (2026-10-01)

## Step 0: Toolchain guard (this task)

- Date (UTC): 2026-10-01
- Safebin activated at `$HOME/safebin` with 20 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` applied for all commands.
- `which python3 python` returned nothing (guard-check-done).
- Zero forbidden executables invoked. Shell used only for git ops,
  coreutils file reads, and grep verification. No computation.

## Scope (this task)

Fix ONLY the 2 minor issues flagged by the integration verifier
(commit `75ea448e8`) in the guard integration spec
(`guard_integration/GUARD_INTEGRATION.md`):

1. Insertion C must say "prereg structure Section 3" explicitly, so the
   author does not search the outline's Section 3 ("Structural signature
   function") for the order summary table.
2. Insertion B draft text said "seven floor capabilities"; the floor spec
   defines six (F1/F2/F3/G1/G2/G3). Corrected to "six".

## Edits applied (4 surgical, no other changes)

- Section 3 draft text (insertion B): "seven floor capabilities" -> "six
  floor capabilities". The two remaining "seven floor tests" references
  (insertion E check 2, insertion F) were left untouched: the floor
  battery is seven verification tests, which is correct and distinct
  from the six capabilities.
- Section 4 heading, section 4 paragraph, and placement table row C:
  "Section 3" -> "prereg structure Section 3".

## Verification

- `grep -n "seven"` shows only the two correct "seven floor tests"
  references. Zero em dashes in GUARD_INTEGRATION.md (byte check).
- `git diff --stat`: 4 insertions, 4 deletions, one file
  (GUARD_INTEGRATION.md).

## Constraints honored

- Fix only the 2 issues; nothing else edited.
- No em dashes. Paper untouched. Nothing pushed.
- Explicit pathspecs on commit.

## Verdict

ISSUES-FIXED.
