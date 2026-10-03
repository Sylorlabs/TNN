# NAMECHECK: H3-SECOND-CONSOLIDATE worker

Date: 2026-10-03. Lane:
docs/lab/research-lead/overnight-20260928/h3_second_consolidate/
Task: suggested follow-up (b) from H3-POSTREL-COMPOSITE. After the
post-release genuine composite install re-creates the hazard
(POSTCOMP-W10: rel=8, haz=8), run a SECOND guarded consolidate.
Does the guard catch the post-release references on the second
pass (rel2=0, blocks)? Is the hazard permanent (hz2=8, no
self-heal)? Or does re-running the decision change anything?
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
  casts, if-nesting at most 2, no `!(A && B)` in while conditions,
  no `!(` anywhere in new code.

## Step 1: identity

Worker: H3-SECOND-CONSOLIDATE worker (subagent, non-ledger).
Parent question: post-release composite installation re-creates
the hazard after a guarded-correct release (POSTCOMP-W10:
rel=8, haz=8). Re-run the guarded consolidate AFTER the
post-release composite install. Does the guard now catch the
references (block the re-release)? Does the hazard persist, or
does the system self-heal?

## Step 2: scope

In scope: PREREG.md (frozen first, alone), NAMECHECK.md,
h3_second_consolidate.zag (copy of h3_postrel_composite.zag plus
the frozen delta only: lane header/tag, new run_seccon_wx
runner with the second guarded consolidate, 3 main call sites,
S-bar checks, verdict line), build with pinned znc, 3/3
byte-identical runs, external S0/S5 checks, REPORT.md. The
guarded consolidate is NOT modified: test only; if the guard
misbehaves under the new worlds, the report documents it, no fix.

Out of scope: any change to the canonized gate, learner
simulation, teachers, or eviction policies; learner-authored
reference bodies (follow-up a); composite eviction reversibility
(follow-up c); any new claim minting; any push to GitHub.

## Step 3: kill bars (frozen in PREREG.md)

S0 IDENTITY (external, VOID on failure), S1 W13-BLOCK-BUT-NO-HEAL
(rel1=8, rel2=0, hz_post=8, hz2=8), S2 W14-NOREF-DOUBLE-RELEASE
(rel1=8, rel2=8, hz_post=0, hz2=0, av=16), S3 W15-PARTIAL-BLOCK
(rel1=8, rel2=4, hz_post=4, hz2=4, av=12), S4 CLEAN, S5
DETERMINISM (external).
Verdict SECOND-CONSOLIDATE-PASS iff S0..S5 hold.

## Step 4: derivation sanity

Pass 1 is the byte-identical POSTCOMP decision: 8 candidates
(keys 5001..5008, reason 2), no live references at decision
time -> rel1=8, cf=8, lc=12, trs=22222222. learner_unpin does
NOT clear slot candidacy (used flag, key, value unchanged), so
pass 2 re-examines the same 8 slots with the identical
predicate: verify=1 re-fires (mem cells untouched by
install_composite), blocked iff has_live_ref(M,k)==1 now.
W13: all 8 keys referenced -> rel2=0, trace stays 8, av=8,
hz_post=hz2=8 (permanent, no self-heal). W14: no key referenced
-> all 8 re-release -> rel2=8, trace 8->16, av=16, hz stays 0
(stateless, non-idempotent re-fire). W15: keys 5001..5004
blocked, 5005..5008 re-released -> rel2=4, trace 8->12, av=12,
hz_post=hz2=4. Composite slots (8xxx keys) are never candidates
(lholds=0, no log entries). trspack capped at 8 entries
(i32-safe). Full derivations in PREREG.md.
