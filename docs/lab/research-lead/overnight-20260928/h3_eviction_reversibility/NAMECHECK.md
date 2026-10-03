# NAMECHECK: H3-EVICTION-REVERSIBILITY worker

Date: 2026-10-03. Lane:
docs/lab/research-lead/overnight-20260928/h3_eviction_reversibility/
Task: parent follow-up (c) from H3-SECOND-CONSOLIDATE. After the
post-release genuine composite install re-creates the hazard
(POSTCOMP-W10: rel=8, haz=8) and re-consolidation is proven not to
heal (SECCON-W13: hz2=8), evict the post-release composite
(remove the reference). Does eviction reverse the hazard
(hz 8 -> 0)? Or is the hazard irreversible even after eviction?
What is the reversibility condition? Non-ledger task (claim
minting paused).

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
  no `!(` anywhere in new code. Verified by grep over the new
  hunks before the build.

## Step 1: identity

Worker: H3-EVICTION-REVERSIBILITY worker (subagent, non-ledger).
Parent question: the hazard is permanent under re-consolidation
(SECCON-W13: hz_post=8 -> hz2=8). Evict the post-release
composite (remove the reference): does the hazard reverse? Is
there any self-heal path left? What is the reversibility
condition (when does eviction heal vs not)?

## Step 2: scope

In scope: PREREG.md (frozen first, alone), NAMECHECK.md,
h3_eviction_reversibility.zag (copy of h3_second_consolidate.zag
plus the frozen delta only: lane header/tag, new
evict_composite harness test hook, new run_evrev_wx runner with
the eviction phase and optional second consolidate, 3 main call
sites, E-bar checks, verdict line), build with pinned znc, 3/3
byte-identical runs, external E0/E5 checks, REPORT.md. The
guarded consolidate is NOT modified: test only; if the gate
misbehaves under the new worlds, the report documents it, no fix.

Out of scope: any change to the canonized gate, learner
simulation, teachers, or eviction policies; learner-authored
reference bodies (follow-up a); any new claim minting; any push
to GitHub.

## Step 3: kill bars (frozen in PREREG.md)

E0 IDENTITY (external, VOID on failure), E1 W16-FULL-REVERSAL
(rel1=8, rel2=0, hz_live=8, hz_post=0, av=8),
E2 W17-PARTIAL-REVERSAL (rel1=8, rel2=0, hz_live=8, hz_post=4,
av=8), E3 W18-EVICT-THEN-RECHECK (rel1=8, rel2=8, hz_live=8,
hz_post=0, av=16; row equals SECCON-W14's row on every shared
field), E4 CLEAN, E5 DETERMINISM (external).
Verdict EVICTION-REVERSIBILITY-PASS iff E0..E5 hold.

## Step 4: derivation sanity

Pass 1 is the byte-identical POSTCOMP decision: 8 candidates
(keys 5001..5008, reason 2), no live references at decision
time -> rel1=8, cf=8, lc=12, trs=22222222. The 8 displaced
scratch old values (600001..600008) sit in pool slots 0..7;
learner_unpin sets released flags for slots 0..7 and appends 8
trace entries. chw=3 installs 8 band-matched composites (keys
8001..8008, values 905001..905008) in first-free slots 8..15 ->
hz_live=8.

Eviction clears the composite slots' used flags. Released flags
(slots 0..7), memory cells, the true log, and the trace are
untouched.

W16 (evict all 8): has_live_ref=0 for every trace key ->
hz_post=0. No recheck -> rel2=0, av=8, ai=0, trs=22222222,
ar=0, lc=12, cf=8, ev=0, drop=0.

W17 (evict 8001..8004): composites 8005..8008 (values
905005..905008) still reference keys 5005..5008 -> hz_post=4,
per-entry reversibility. All else as W16.

W18 (evict all 8, then second consolidate): pass 2 re-scans
slots 0..7 with the identical predicate; verify=1 re-fires
(mem cells untouched); blocked iff has_live_ref==1, now 0 for
all 8 keys -> all 8 re-release -> rel2=8, trace 8->16, av=16,
ai=0, hz_post=0, trs pack capped at 8 -> 22222222. Composite
slots (8xxx keys) are never candidates (lholds=0, no log
entries). The W14 decision landscape is reached by eviction
rather than by never installing references; the row must equal
SECCON-W14's row on every shared field.

## Step 5: reversibility-condition reading (frozen, pre-result)

count_hazard is a pure state predicate over the live pool:
released(k) [sticky, from the trace] AND currently-referenced(k)
[live pool state]. Eviction falsifies the reference leg per
entry; the release leg cannot be un-released (no un-release path
exists in the canonized gate). Expected result: eviction heals
(hz 8->0), partial eviction heals per entry (hz 8->4), and
re-consolidation could not heal because it changes neither leg.
If the measured numbers disagree, the report root-causes
without moving the bars.
