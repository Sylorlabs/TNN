# NAMECHECK: H3-INCORPORATED worker

Date: 2026-10-03. Lane:
docs/lab/research-lead/overnight-20260928/h3_incorporated/
Task: investigate the remaining open question from the H3 arc:
INCORPORATED/SUPERSEDED reasons and the successful-episode
importance source. Non-ledger task (claim minting paused).

## Step 0: toolchain guard (worker toolchain guard, Micah's ruling)

- Safebin active: `export PATH="$HOME/safebin"` (49 allowed tools).
- `which python3` returns nothing; `which python` returns nothing
  (verified 2026-10-03 before the prereg commit).
- Pinned znc verified byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef)
  before the prereg commit.
- All research logic in pure Zag. Shell used only for: mkdir, file
  writes, znc invocation, binary execution, sha256sum, cmp, git ops.
- No forbidden executable will be invoked; any invocation makes this
  wave PROCESS-FAIL.

## Step 1: identity

Worker: H3-INCORPORATED worker (subagent, non-ledger).
Parent question: (a) what distinguishes INCORPORATED (belief absorbed
into a larger structure) from SUPERSEDED (belief replaced by a better
one); (b) does the distinction matter for the unpin decision (should
both release? neither? only one?); (c) what is the successful-episode
importance source (how does the learner know which beliefs matter).

## Step 2: scope

Hybrid lane: a focused Zag experiment (reasons 1/2/3 through the H3
release gate; the INCORPORATED reference hazard; a guarded consolidate
variant; a minimal importance-source ranking demo) PLUS reasoned
analysis. REPORT.md will distinguish tested vs reasoned explicitly.

## Step 3: prereg discipline

PREREG.md is committed alone, strictly before implementation, build,
or runs. Kill bars R1..R9 frozen with exact predicted numbers. No
frozen number, bar, or design element may change after this commit;
misses are reported as misses.
