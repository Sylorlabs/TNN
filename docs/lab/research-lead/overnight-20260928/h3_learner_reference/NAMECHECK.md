# NAMECHECK: H3-LEARNER-REFERENCE worker

Worker: H3-LEARNER-REFERENCE worker (non-ledger task; claim minting
paused). Parent: H3-EVICTION-REVERSIBILITY follow-up (a):
learner-authored reference body installed post-release.

## Step 0: toolchain guard (verified 2026-10-03, before prereg)

- Safebin active: `export PATH="$HOME/safebin"`.
- `which python3` returns nothing; `which python` returns nothing
  under the safebin PATH.
- Pinned znc at ~/safebin/znc, sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (same sha256).
- No forbidden executable will be invoked; shell only for mkdir,
  file writes, znc invocation, binary execution, sha256sum, cmp,
  diff, grep, git ops.
- All research logic in pure Zag. New-code audit before build:
  no `!(` negated conjunctions in while conditions, no
  `as *i32` slice construction, no `[]u8 as *u8` casts,
  if-nesting at most 3.

## Step 1: identity

- Lane: docs/lab/research-lead/overnight-20260928/h3_learner_reference/
- Builds on H3-EVICTION-REVERSIBILITY; the canonized guarded
  consolidate is NOT modified (test only).
- Prereg committed alone before implementation, build, and runs
  (commit-order self-check).

## Step 2: honesty pre-commitment

- "Learner-authored" is defined operationally in PREREG.md and the
  definition is frozen. It does NOT mean an autonomous learner
  invented the reference encoding; the encoding
  (value-900000==key) remains the frozen substrate convention.
- The learner remains simulated (worker-written episode
  routines). This lane is a mechanism-route comparison, not a
  demonstration of genuine learner invention. The report will
  say so explicitly.
- install_composite is not called in the new worlds.
