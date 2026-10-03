# NAMECHECK: H3-POSTREL-COMPOSITE worker

Date: 2026-10-03. Lane:
docs/lab/research-lead/overnight-20260928/h3_postrel_composite/
Task: the suggested next probe from H3-RELEASE-CHURN. Post-release
reference installation via a GENUINE absorbing composite
(install_composite after the release decision, rather than churn
debris) -- the closest analog of a real structure referencing
released memory. Does a real structure referencing released memory
re-create the hazard (or is debris special)? What is the hazard
definition against genuine post-release references?
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
  casts, if-nesting at most 3, no `!(A && B)` in while conditions,
  no `!(` anywhere in new code.

## Step 1: identity

Worker: H3-POSTREL-COMPOSITE worker (subagent, non-ledger).
Parent question: a genuine absorbing composite installed after a
guarded release decision -- does it re-create the hazard the guard
was designed to prevent (or was the parent's W10 debris-specific)?
What is the hazard definition against genuine post-release
references?

## Step 2: scope

In scope: PREREG.md (frozen first, alone), NAMECHECK.md,
h3_postrel_composite.zag (copy of h3_release_churn.zag plus the
frozen delta only: lane header/tag, three new chw modes in
run_postrel_wx, 3 main call sites, P-bar checks, verdict line),
build with pinned znc, 3/3 byte-identical runs, external P0/P5
checks, REPORT.md. The guarded consolidate is NOT modified: test
only; if the guard misbehaves under the new worlds, the report
documents it, no fix.

Out of scope: any change to the canonized gate, learner
simulation, teachers, or eviction policies; any new claim
minting; any push to GitHub.

## Step 3: kill bars (frozen in PREREG.md)

P0 IDENTITY (external, VOID on failure), P1
GENUINE-POSTREL-HAZARD (W10: rel=8, haz=8, cf=8), P2
GENUINE-NOREF-SAFE (W11: rel=8, haz=0, cf=8), P3
PARTIAL-REFERENCE-GRANULARITY (W12: rel=8, haz=4, cf=8), P4 CLEAN,
P5 DETERMINISM (external).
Verdict POSTREL-COMPOSITE-PASS iff P0..P5 hold.

## Step 4: derivation sanity

All three worlds share the parent W10/W11 substrate through the
consolidate decision: 8 revise conflicts (cf=8); 8 candidates
(keys 5001..5008, reason 2); no live references at decision time
-> rel=8, av=8, ai=0, trs=22222222, lc=12. install_composite
performs no mem_write and no conflicts: cf stays 8. The 8
composites land in first-free slots 8..15 (pool 16 <= 32 ->
ev=0, drop=0); the 4-composite world lands in 8..11.
W10: values 905001..905008 match trace keys 5001..5008 ->
haz=8. W11: values 905021..905028 imply k in 5021..5028, no
candidate key matches -> haz=0. W12: values 905001..905004 match
trace keys 5001..5004 only -> haz=4. Full derivations in
PREREG.md.
