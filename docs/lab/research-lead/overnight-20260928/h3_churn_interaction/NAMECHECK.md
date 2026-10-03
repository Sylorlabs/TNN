# NAMECHECK: H3-CHURN-INTERACTION worker

Date: 2026-10-03. Lane:
docs/lab/research-lead/overnight-20260928/h3_churn_interaction/
Task: resolve the H3-GUARDED-SEALED caveat on churn x reason==2:
run reason==2 worlds WITH churn through the canonized guarded
gate, verify the guard still blocks the hazard and does not
over-block, and re-derive the guard's interaction with
churn-displaced values (the churn value range (900001+j)
overlaps the reference-pattern range [900000,910000)).
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

Worker: H3-CHURN-INTERACTION worker (subagent, non-ledger).
Parent question: does the canonized guarded consolidate behave
correctly when reason==2 entries meet churn -- still blocking the
INCORPORATED reference hazard, not over-blocking -- and what is
the exact interaction between the guard and churn-displaced values
given the value-range overlap?

## Step 2: scope

In scope: PREREG.md (frozen first, alone), NAMECHECK.md,
h3_churn_interaction.zag (copy of h3_guarded_sealed.zag plus the
frozen delta only: lane header/tag, R alloc bump, run_churn_wx
driver, 3 main call sites, C-bar checks, verdict line), build with
pinned znc, 3/3 byte-identical runs, external C0/C5 checks,
REPORT.md. The guarded consolidate is NOT modified: test only; if
the guard misbehaves under churn, the report documents it, no fix.

Out of scope: any change to the canonized gate, learner
simulation, teachers, or eviction policies; any new claim
minting; any push to GitHub.

## Step 3: kill bars (frozen in PREREG.md)

C0 IDENTITY (external, VOID on failure), C1 W7 hazard blocked
under churn, C2 W8 debris blocks (re-derived), C3 W9 no
over-block, C4 CLEAN, C5 DETERMINISM (external). Verdict
CHURN-INTERACTION-PASS iff C0..C5 hold.

## Step 4: derivation sanity

W7: cf=28 (8 revise + 20 churn), drop=4 (pool fills at 32 under
policy 8 no-reclaim pinning; last 4 churn relocates drop++),
rel=0 via genuine references. W8: cf=16 (8 revise + 8 collision
churn), rel=0 via debris value-match (provenance-blindness).
W9: cf=28, rel=8 (no value collision; churn per se inert).
Full derivations in PREREG.md.
