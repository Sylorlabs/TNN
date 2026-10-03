# NAMECHECK: H3-RELEASE-CHURN worker

Date: 2026-10-03. Lane:
docs/lab/research-lead/overnight-20260928/h3_release_churn/
Task: the release-then-churn ordering probe (suggested next probe
from H3-CHURN-INTERACTION). Churn arrives AFTER a guarded release
decision; test the hazard definition against post-release
reference installation: does post-release reference installation
re-create the hazard, and what is the hazard definition against
post-release references?
Non-ledger task (claim minting paused).

## Step 0: toolchain guard (worker toolchain guard, Micah's ruling)

- Safebin active: `export PATH="$HOME/safebin"`. (The
  safebin_setup/ directory does not exist in this checkout; the
  safebin itself is present and was activated the same way as the
  parent lane.)
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

Worker: H3-RELEASE-CHURN worker (subagent, non-ledger).
Parent question: churn arriving after a guarded release decision --
does post-release reference installation re-create the hazard
(released memory referenced after release), and what is the hazard
definition against post-release references?

## Step 2: scope

In scope: PREREG.md (frozen first, alone), NAMECHECK.md,
h3_release_churn.zag (copy of h3_churn_interaction.zag plus the
frozen delta only: lane header/tag, run_postrel_wx driver, 3 main
call sites, R-bar checks, verdict line), build with pinned znc,
3/3 byte-identical runs, external R0/R5 checks, REPORT.md. The
guarded consolidate is NOT modified: test only; if the guard
misbehaves under the new ordering, the report documents it, no
fix.

Out of scope: any change to the canonized gate, learner
simulation, teachers, or eviction policies; any new claim
minting; any push to GitHub.

## Step 3: kill bars (frozen in PREREG.md)

R0 IDENTITY (external, VOID on failure), R1
POSTREL-HAZARD-MATERIALIZES (W10: rel=8, haz=8), R2
POSTREL-NOREF-SAFE (W11: rel=8, haz=0), R3
PREREL-BLOCK-SURVIVES-POSTCHURN (W12: rel=0, haz=0, row
content-identical to W7), R4 CLEAN, R5 DETERMINISM (external).
Verdict RELEASE-CHURN-PASS iff R0..R5 hold.

## Step 4: derivation sanity

W10: cf=16 (8 revise + 8 collision churn), rel=8 (no refs at
decision time), debris 905001..905008 lands in free slots 8..15
(pool 16 <= 32, drop=0), haz=8 measured after churn. W11: cf=28
(8 + 20 natural), rel=8, debris implies k in 1..20, haz=0. W12:
genuine refs before decision -> rel=0; 20 churn relocates on 16
free slots -> drop=4; haz=0. Full derivations in PREREG.md.
