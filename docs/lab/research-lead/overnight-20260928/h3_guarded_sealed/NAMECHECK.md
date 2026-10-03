# NAMECHECK: H3-GUARDED-SEALED worker

Date: 2026-10-03. Lane:
docs/lab/research-lead/overnight-20260928/h3_guarded_sealed/
Task: build the sealed lane for the guarded consolidate proposed by
H3-INCORPORATED (no-live-reference precondition for reason==2).
Non-ledger task (claim minting paused).

## Step 0: toolchain guard (worker toolchain guard, Micah's ruling)

- Safebin active: `export PATH="$HOME/safebin"`.
- `which python3` returns nothing; `which python` returns nothing
  (verified 2026-10-03 before the prereg commit).
- Pinned znc verified byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef)
  before the prereg commit.
- All research logic in pure Zag. Shell used only for: mkdir, file
  writes, znc invocation, binary execution, sha256sum, cmp, diff,
  grep, git ops (via /usr/bin/git directly: the safebin git symlink
  EPERM lesson from AGENTS.md).
- No forbidden executable will be invoked; any invocation makes this
  wave PROCESS-FAIL.
- New-code audit before build: no negated-conjunction while
  conditions, no `as *i32` slice construction, no `[]u8 as *u8`
  casts, if-nesting at most 3, no `!(A && B)` in while conditions.

## Step 1: identity

Worker: H3-GUARDED-SEALED worker (subagent, non-ledger).
Parent question: does the guarded consolidate (H3-INCORPORATED's
proposed gate extension: no-live-reference precondition for
reason==2 INCORPORATED entries) survive the same four sealed
adversary worlds W1-W4 that H3-SEALED-B sealed for the unguarded
gate, and does it fix the INCORPORATED reference hazard without
breaking the other worlds? This lane canonizes the guarded
consolidate (or kills it).

## Step 2: scope

One Zag experiment: the H3-SEALED-B sealed mechanism plus exactly
the frozen guard delta from H3-INCORPORATED (guard hardwired ON),
run through the four sealed worlds W1-W4 (reasons all 1) plus two
new guard worlds W5 (hazard: reason 2 with live references) and W6
(no-overblock: reason 2 without live references). Kill bars G0..G14
frozen in PREREG.md.

## Step 3: prereg discipline

PREREG.md is committed alone, strictly before implementation, build,
or runs. Kill bars G0..G14 frozen with exact predicted numbers. No
frozen number, bar, or design element may change after this commit;
misses are reported as misses. VOID is terminal.
