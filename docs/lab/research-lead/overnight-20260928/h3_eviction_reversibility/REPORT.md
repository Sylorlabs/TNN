# REPORT: H3-EVICTION-REVERSIBILITY (composite eviction reversibility probe)

Date: 2026-10-03. Worker: H3-EVICTION-REVERSIBILITY worker
(non-ledger task; claim minting paused).
Prereg: committed alone as 027b3b43e (strictly before
implementation, build, and runs). No amendments.

## Verdict: EVICTION-REVERSIBILITY-PASS (E0..E5 all hold)

3/3 runs byte-identical (sha256
7f1a6bcd1a47feb66c20f13f877aff705c275ebb893395682b9c52fd0367c6b3).
Binary sha256
a524a5a3a166b9b4182fcbdf330e66e76f7cb9e1b52c276abf6962436315c0d6.
Source sha256
c637e843afb43902e24d90cdb1dcb675fd8f959689c4ccca396485fc531c5358.

The parent's remaining open follow-up (c) is EXECUTED and CLOSED.
The answer has three parts. (1) Eviction REVERSES the hazard:
with 8 band-matched composites live (hz_live=8), evicting all 8
drops the hazard to zero (W16: hz_post=0). The hazard is a
live-state predicate, not a materialized irreversible event.
(2) Reversibility is PER-ENTRY: evicting only the first 4
composites heals exactly the 4 evicted keys' hazards
(W17: hz_post=4). The reversibility condition: each hazard entry
reverses iff its own reference leg is removed. (3) Eviction
restores the no-reference decision landscape exactly: after
evicting all 8 composites and re-running the canonized second
consolidate, every shared field equals SECCON-W14's row
(W18: rel2=8, av=16, hz_post=0; the non-idempotent re-fire
returns, now over the post-eviction state). Eviction leaves no
residue.

## Results (identical across run1/run2/run3)

| cond      | cf | ev | drop | rel1 | rel2 | av | ai | ar | lc | hz_live | hz_post | trs              |
|-----------|----|----|------|------|------|----|----|----|----|---------|---------|------------------|
| EVREV-W16 | 8  | 0  | 0    | 8    | 0    | 8  | 0  | 0  | 12 | 8       | 0       | 22222222         |
| EVREV-W17 | 8  | 0  | 0    | 8    | 0    | 8  | 0  | 0  | 12 | 8       | 4       | 22222222         |
| EVREV-W18 | 8  | 0  | 0    | 8    | 8    | 16 | 0  | 0  | 12 | 8       | 0       | 2222222222222222 |

Every measured row matches the frozen prereg predictions exactly.
The 54 pre-existing COND lines (48 anchors + SEALED-W1..W4 +
GUARDED-W5/W6 + CHURN-W7/W8/W9 + POSTREL-W10/W11/W12 +
POSTCOMP-W10/W11/W12 + SECCON-W13/W14/W15) are byte-identical to
h3_second_consolidate/run1.txt, and the in-band
GUARDED-SEALED-VERDICT=PASS, CHURN-INTERACTION-VERDICT=PASS,
RELEASE-CHURN-VERDICT=PASS, POSTREL-COMPOSITE-VERDICT=PASS, and
SECOND-CONSOLIDATE-VERDICT=PASS still hold, so the eviction
worlds caused no regression. (W18's printed `trs=` digits show
all 16 trace entry reasons; the packed trspack field is capped
at 8 entries, 22222222, by the frozen design.)

Kill bars (in-band + external, all 3 runs):
- E0 IDENTITY: HOLD. diff of run1.txt against
  h3_second_consolidate/run1.txt shows ONLY the expected
  differences: the LANE= tag line, the 3 new COND=EVREV-W1[678]
  lines, the new E1..E4 in-band check lines, and the
  EVICTION-REVERSIBILITY-VERDICT= line (9 diff lines, all in the
  expected categories). 3/3 runs byte-identical. diff of
  h3_eviction_reversibility.zag against
  h3_second_consolidate/h3_second_consolidate.zag shows only the
  frozen delta in 6 hunks: lane header comment, LANE= tag, new
  evict_composite harness hook, new run_evrev_wx runner, 3 main
  call sites, E-bar checks, verdict line. Every mechanism
  function body byte-identical. Not VOID.
- E1 W16-FULL-REVERSAL: HOLD (rel1=8, rel2=0, hz_live=8,
  hz_post=0, av=8, ai=0, ar=0, cf=8, ev=0, drop=0, lc=12,
  trs=22222222). Evicting all 8 post-release composites reverses
  the hazard completely: hz goes 8 -> 0. The hazard is a
  live-state predicate over pool state (count_hazard re-evaluates
  released(k) AND currently-referenced(k) per trace entry), not a
  materialized event counter. Removing the reference leg clears
  it.
- E2 W17-PARTIAL-REVERSAL: HOLD (rel1=8, rel2=0, hz_live=8,
  hz_post=4, av=8, ai=0, ar=0, cf=8, ev=0, drop=0, lc=12,
  trs=22222222). Exactly the 4 still-referenced keys (5005..5008,
  composites 8005..8008 with values 905005..905008 still live)
  keep their hazard; the 4 evicted keys (5001..5004) heal.
  Reversibility is per-entry, not all-or-nothing: no over-heal
  beyond the evicted set (hz_post=0 would have failed the bar)
  and no under-heal (hz_post=8 would have failed the bar).
- E3 W18-EVICT-THEN-RECHECK: HOLD (rel1=8, rel2=8, hz_live=8,
  hz_post=0, av=16, ai=0, ar=0, cf=8, ev=0, drop=0, lc=12,
  trs=22222222). Programmatic field-by-field comparison confirms
  W18's row equals SECCON-W14's row on every shared field
  (including final hazard 0). After eviction, the canonized
  second consolidate behaves exactly as in the never-referenced
  world: the guard blocks nothing (has_live_ref=0 for all 8
  keys) and the stateless predicate re-fires all 8 releases
  (rel2=8, trace 8->16, av=16, all entries audit-valid).
  Eviction leaves no residue: the no-reference decision
  landscape is restored exactly.
- E4 CLEAN: HOLD (ai=0, ar=0 in W16/W17/W18; lc=12 all three).
- E5 DETERMINISM: HOLD (3/3 byte-identical).

In-band EVICTION-REVERSIBILITY-VERDICT=PASS in all 3 runs; the
governing verdict is this external check.

## What this establishes

1. The one remaining untested self-heal path is tested, and it
   works: eviction heals. SECCON proved re-consolidation cannot
   heal the hazard (hz2=8); this lane proves composite eviction
   can (hz 8->0). The self-heal asymmetry is now closed on both
   sides.
2. The reversibility condition: the hazard predicate is the
   conjunction released(k) [sticky: the trace entry and the
   released flag persist; the canonized gate has no un-release
   path] AND currently-referenced(k) [live: evaluated over the
   current pool state]. Eviction heals by falsifying the
   reference leg, per entry (W17: exactly 4 heal when 4 of 8
   references are removed). Re-consolidation could not heal
   because it falsifies neither leg: it does not un-release
   (the release leg is sticky by design) and it does not remove
   references. Any substrate that needs post-release safety must
   either remove the reference (eviction) or re-check at use
   time; re-deciding is not a self-heal.
3. Eviction is residue-free at the level of every measured
   observable: W18's full row (including the non-idempotent
   rel2=8 re-fire and the 16-entry audit) is byte-equal to the
   W14 row reached by never installing references. The system
   after eviction is indistinguishable, on these observables,
   from the system that never had the composite.
4. The ordering/decision/reversibility matrix for the sealed H3
   lineage is now closed: references BEFORE the decision block
   (rel=0); no references at decision then release (rel=8);
   post-release references re-create the hazard (haz=8); a
   second decision blocks re-release of referenced candidates
   (rel2=0) but heals nothing (hz2=haz) and re-releases
   unreferenced ones (rel2=8/4); evicting the post-release
   references reverses the hazard per entry (hz 8->0 full,
   8->4 partial) and restores the no-reference decision
   landscape (W18 == W14).

## Honest caveats

- The adversary is the worker in a second hat (same procedural
  seal as the parent lane), not a second mind. W16/W17/W18 were
  specified in the prereg before implementation.
- The learner remains simulated; reason codes are harness-written.
- The composite values are harness-written, not learner-created;
  a learner-authored reference body remains untested
  (follow-up a, not started).
- The eviction is a harness-issued reference removal (the
  evict_composite hook clears the pool slot's used flag), not a
  learner-initiated composite drop; whether the learner itself
  would ever evict its composite is not tested.
- The eviction hook touches only the composite slots' used
  flags; released flags, the trace, the true revision log, and
  memory cells are untouched. A substrate whose eviction path
  also rewrites those would need its own test.
- Non-ledger task: no claims minted.
- The guarded consolidate was NOT modified in this lane (test
  only, per the task constraint).

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which
python` return nothing under that PATH (verified 2026-10-03
before the prereg commit); no forbidden executable invoked at any
point (shell used only for mkdir, file writes, znc invocation,
binary execution, sha256sum, cmp, diff, grep, git ops). No
PROCESS-FAIL condition triggered. Pinned znc verified
byte-identical to src/tools/toolchain/znc_linux_x86_64_abed8aa1
before the prereg commit (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Build ran in foreground (zagd unavailable warning only), first
try, no defect symptoms; `-o h3_eviction_reversibility_bin` used
for the output name. New-code audit: no negated-conjunction while
conditions, no `as *i32` slice construction, no `[]u8 as *u8`
casts (only the pre-existing `null as *u8` comparison),
zero `!(` in the whole file, if-nesting at most 2 in new code.
Git writes via /usr/bin/git directly (safebin git symlink EPERM
lesson); explicit pathspecs; no git reset; local only, never
pushed.

## Commits

- 027b3b43e: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before implementation, build, and runs.
- This commit: h3_eviction_reversibility.zag (source sha256
  c637e843afb43902e24d90cdb1dcb675fd8f959689c4ccca396485fc531c5358;
  diff against h3_second_consolidate/h3_second_consolidate.zag
  shows only the frozen delta in 6 hunks), h3_eviction_reversibility_bin
  (sha256
  a524a5a3a166b9b4182fcbdf330e66e76f7cb9e1b52c276abf6962436315c0d6),
  build.err, run1/2/3.txt, run1/2/3.err, REPORT.md. Local only,
  never pushed.

## Follow-ups for the parent

- Suggested follow-up (c) from H3-SECOND-CONSOLIDATE is CLOSED:
  composite eviction reversibility is frozen and verified
  (EVICTION-REVERSIBILITY-PASS E0..E5). Eviction reverses the
  hazard (hz 8->0), per-entry (partial evict heals exactly the
  evicted keys), and restores the no-reference decision
  landscape with no residue (W18 row == W14 row). The
  reversibility condition: eviction heals by falsifying the
  reference leg of the released-AND-referenced hazard
  predicate; the release leg is sticky (no un-release path),
  which is exactly why re-consolidation could not heal.
- Remaining open probe from the parent's list: (a) a
  learner-authored reference body installed post-release.
- Design note for any future substrate: the hazard is a live
  conjunctive state predicate, not an event. Post-release
  safety needs reference removal (eviction), use-time re-checks,
  or pinning -- never re-decision. And if consolidate is ever
  re-run after eviction, the gate's statelessness re-fires
  releases on the now-unreferenced candidates (W18 rel2=8);
  idempotency must be supplied outside the canonized gate.
