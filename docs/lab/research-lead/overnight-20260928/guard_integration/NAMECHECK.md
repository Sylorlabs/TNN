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
- Floor spec `f383dd11c`: the 7 floor capabilities F1/F2/F3/G1/G2/G3
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
