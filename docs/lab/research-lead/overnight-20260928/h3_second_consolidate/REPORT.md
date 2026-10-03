# REPORT: H3-SECOND-CONSOLIDATE (second guarded consolidate probe)

Date: 2026-10-03. Worker: H3-SECOND-CONSOLIDATE worker (non-ledger
task; claim minting paused).
Prereg: committed alone as 9cd71c7fd (strictly before
implementation, build, and runs). No amendments.

## Verdict: SECOND-CONSOLIDATE-PASS (S0..S5 all hold)

3/3 runs byte-identical (sha256
23514e7f96add46cc1db9b50e7a4eef1b801a458a5df76fec41972b7ca6a3d3b).
Binary sha256
36447f4c98e2f2f8a5667dfd0b609030dcc75c7679b66f45265ffce880f812d3.

The H3-POSTREL-COMPOSITE suggested next probe (b) is EXECUTED. The
answer has three parts. (1) The guard DOES catch the post-release
references on the second pass: with 8 band-matched composites
live, the second guarded consolidate blocks all 8 re-releases
(W13: rel1=8, rel2=0). The guard was never broken; it is a
decision-time predicate, and the second decision is as correct as
the first. (2) The hazard is PERMANENT: hz_post=8 -> hz2=8. The
system does NOT self-heal. Re-running the consolidate cannot
un-release or re-protect already-released entries; the hazard that
materialized from the pass-1 release persists unchanged. (3) The
second decision is decision-time-local in a second sense: the
guard predicate is STATELESS with respect to past decisions.
Where it has no value match to block on, it re-fires the release
decision and re-releases the already-released candidates (W14:
rel2=8, trace grows 8->16, all 16 entries audit-valid). "Re-check
later" is therefore not a substitute for idempotent reference
tracking: re-running the gate blocks the referenced and
double-releases the unreferenced, per key (W15: rel2=4, exactly
the 4 unreferenced keys).

## Results (identical across run1/run2/run3)

| cond      | cf | ev | drop | rel1 | rel2 | av | ai | ar | lc | hz_post | hz2 | trs      |
|-----------|----|----|------|------|------|----|----|----|----|---------|-----|----------|
| SECCON-W13| 8  | 0  | 0    | 8    | 0    | 8  | 0  | 0  | 12 | 8       | 8   | 22222222 |
| SECCON-W14| 8  | 0  | 0    | 8    | 8    | 16 | 0  | 0  | 12 | 0       | 0   | 22222222 |
| SECCON-W15| 8  | 0  | 0    | 8    | 4    | 12 | 0  | 0  | 12 | 4       | 4   | 22222222 |

Every measured row matches the frozen prereg predictions exactly.
The 51 pre-existing COND lines (48 anchors + SEALED-W1..W4 +
GUARDED-W5/W6 + CHURN-W7/W8/W9 + POSTREL-W10/W11/W12 +
POSTCOMP-W10/W11/W12) are byte-identical to
h3_postrel_composite/run1.txt, and the in-band
GUARDED-SEALED-VERDICT=PASS, CHURN-INTERACTION-VERDICT=PASS,
RELEASE-CHURN-VERDICT=PASS, and POSTREL-COMPOSITE-VERDICT=PASS
still hold, so the second-consolidate worlds caused no
regression. (Note: W14's printed `trs=` digits show all 16 trace
entry reasons, 2222222222222222; the packed trspack field is
capped at 8 entries, 22222222, by the frozen design.)

Kill bars (in-band + external, all 3 runs):
- S0 IDENTITY: HOLD. diff of run1.txt against
  h3_postrel_composite/run1.txt shows ONLY the expected
  differences: the LANE= tag line, the 3 new COND=SECCON-W1[345]
  lines, the new S1..S4 in-band check lines, and the
  SECOND-CONSOLIDATE-VERDICT= line (10 diff lines, all in the
  expected categories). 3/3 runs byte-identical. diff of
  h3_second_consolidate.zag against
  h3_postrel_composite/h3_postrel_composite.zag shows only the
  frozen delta in 5 hunks: lane header/tag, LANE= tag, new
  run_seccon_wx runner, 3 main call sites, S-bar checks, verdict
  line. Not VOID.
- S1 W13-BLOCK-BUT-NO-HEAL: HOLD (rel1=8, rel2=0, hz_post=8,
  hz2=8, av=8, ai=0, cf=8, ev=0, drop=0, lc=12, trs=22222222).
  On the second pass the guard sees the 8 live band-matched
  references and blocks every re-release candidate -- the guard
  is decision-time-correct on re-check. But the hazard that
  already materialized does not heal: hz2==hz_post==8.
- S2 W14-NOREF-DOUBLE-RELEASE: HOLD (rel1=8, rel2=8, hz_post=0,
  hz2=0, av=16, ai=0, cf=8, ev=0, drop=0, lc=12, trs=22222222).
  With no value match the guard blocks nothing on pass 2 and the
  8 already-released candidates re-release: the guard predicate
  is stateless w.r.t. past decisions (learner_unpin does not
  clear slot candidacy), so re-running consolidate re-fires the
  release decision. The trace grows 8->16 and all 16 entries
  audit-valid, proving the duplicates are well-formed
  re-releases, not corruption. This discriminates the W13 block
  as value-match-specific rather than pass-2-inert.
- S3 W15-PARTIAL-BLOCK: HOLD (rel1=8, rel2=4, hz_post=4, hz2=4,
  av=12, ai=0, cf=8, ev=0, drop=0, lc=12, trs=22222222). Exactly
  the 4 unreferenced keys (5005..5008) re-release on pass 2; the
  4 referenced keys (5001..5004) are blocked. Per-key
  granularity of the second decision, mirroring the per-entry
  granularity of the hazard itself.
- S4 CLEAN: HOLD (ai=0, ar=0 in W13/W14/W15; lc=12 all three).
- S5 DETERMINISM: HOLD (3/3 byte-identical).

In-band SECOND-CONSOLIDATE-VERDICT=PASS in all 3 runs; the
governing verdict is this external check.

## What this establishes

1. The guard catches post-release references when re-run. W13's
   rel2=0 is the positive control the parent's follow-up (b)
   asked for: the canonized gate, unmodified, sees the live
   references at the second decision and blocks. The guard's
   limitation was never blindness to references -- it is
   decision-time locality, and the second decision is as local
   and as correct as the first.
2. The hazard is permanent under re-consolidation. W13's
   hz_post=8 -> hz2=8: blocking future re-releases does not
   heal the already-materialized hazard. The system does not
   self-heal. Any substrate that needs post-release safety must
   do something the guard does not do: re-check at use time,
   pin released entries against reference installation, or
   track references genuinely (provenance) -- the parent's
   frozen consequence stands, now tested against the re-check
   option itself.
3. Re-running the gate is not idempotent reference tracking.
   W14's rel2=8 is a genuine mechanism finding, not a defect:
   the consolidate predicate has no memory of past decisions
   (no idempotency check on the released flag), so a second
   decision re-fires on unreferenced candidates. W15's rel2=4
   shows the two behaviors compose per key: referenced keys
   blocked, unreferenced keys re-released.
4. The ordering/decision matrix is now closed for the sealed
   H3 lineage: references BEFORE the decision block
   (CHURN-W7/GUARDED-W5, rel=0); no references at decision then
   release (rel=8); post-release references re-create the hazard
   (POSTREL-W10/POSTCOMP-W10, haz=8); a second decision blocks
   re-release of referenced candidates (rel2=0) but heals
   nothing (hz2=haz) and re-releases unreferenced ones
   (rel2=8/4).

## Honest caveats

- The adversary is the worker in a second hat (same procedural
  seal as the parent lane), not a second mind. W13/W14/W15 were
  specified in the prereg before implementation.
- The learner remains simulated; reason codes are harness-written.
- The composite values are harness-written, not learner-created;
  a learner-authored reference body remains untested
  (follow-up a, not started).
- The second consolidate is a harness-issued re-decision, not a
  learner-initiated re-check; whether the learner itself would
  ever re-consolidate is not tested.
- The W14 double-release is derived mechanism behavior of the
  canonized gate (stateless predicate), reported not fixed, per
  the task constraint. If any future substrate re-runs
  consolidate, it must supply idempotency itself.
- Non-ledger task: no claims minted.
- The guarded consolidate was NOT modified in this lane (test
  only, per the task constraint).

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which
python` return nothing under that PATH (verified 2026-10-03 before
the prereg commit); no forbidden executable invoked at any point
(shell used only for mkdir, file writes, znc invocation, binary
execution, sha256sum, cmp, diff, grep, git ops). No
PROCESS-FAIL condition triggered. Pinned znc verified
byte-identical to src/tools/toolchain/znc_linux_x86_64_abed8aa1
before the prereg commit (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Build ran in foreground (zagd unavailable warning only), first
try, no defect symptoms; `-o h3_second_consolidate_bin` used for
the output name. New-code audit: no negated-conjunction while
conditions, no `as *i32` slice construction, no `[]u8 as *u8`
casts, zero `!(` in the added diff hunks, if-nesting at most 2 in
new code. Git writes via /usr/bin/git directly (safebin git
symlink EPERM lesson); explicit pathspecs; no git reset; local
only, never pushed.

## Commits

- 9cd71c7fd: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before implementation, build, and runs.
- This commit: h3_second_consolidate.zag (source sha256
  56aedbafa2a87c5917181c84fb47b07f184e1ad6f9497aed26eb041a3a5b3fc5;
  diff against h3_postrel_composite/h3_postrel_composite.zag shows
  only the frozen delta in 5 hunks), h3_second_consolidate_bin
  (sha256
  36447f4c98e2f2f8a5667dfd0b609030dcc75c7679b66f45265ffce880f812d3),
  build.err, run1/2/3.txt, run1/2/3.err, REPORT.md. Local only,
  never pushed.

## Follow-ups for the parent

- Suggested next probe (b) from H3-POSTREL-COMPOSITE is CLOSED:
  the second guarded consolidate after post-release composite
  install is frozen and verified (SECOND-CONSOLIDATE-PASS
  S0..S5). Re-checking catches the references (blocks) but does
  not heal the hazard; re-running the gate is non-idempotent.
- Remaining open probes from the parent's list: (a) a
  learner-authored reference body installed post-release; (c)
  evicting the post-release composite to test hazard
  reversibility (the state-predicate reversibility test -- the
  one remaining untested self-heal path, since re-consolidation
  is now proven not to heal).
- Design note for any future substrate: if consolidate is ever
  re-run, idempotency must be supplied outside the canonized
  gate (the gate's predicate is stateless by construction); and
  post-release safety cannot come from re-deciding -- it needs
  use-time re-checks, pinning, or genuine reference tracking.
