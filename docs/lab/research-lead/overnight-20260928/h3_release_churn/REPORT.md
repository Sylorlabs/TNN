# REPORT: H3-RELEASE-CHURN (release-then-churn ordering)

Date: 2026-10-03. Worker: H3-RELEASE-CHURN worker (non-ledger
task; claim minting paused).
Prereg: committed alone as 0dd12c8b6 (strictly before
implementation, build, and runs). No amendments.

## Verdict: RELEASE-CHURN-PASS (R0..R5 all hold)

3/3 runs byte-identical (sha256
242b09bd82420c7c1b3ae88bc8c85ea94ebeec2dcfb50c35d1684e8e9f5469fe).
Binary sha256
286aaa748b1441feaf73dda322b21092b7b74a62e30aaa5e04b20e50a6fef156.

The H3-CHURN-INTERACTION suggested next probe is EXECUTED. The
hazard definition is now tested against post-release reference
installation, and the answer is frozen: the canonized guarded
gate is a DECISION-TIME predicate; `count_hazard` is a STATE
predicate. Post-release reference installation re-creates the
hazard (W10: rel=8, haz=8) even though the guard behaved exactly
as specified at decision time. The guard's protection does not
extend past the release decision.

## Results (identical across run1/run2/run3)

| cond       | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|------------|----|----|------|-----|----|----|----|----|-----|----------|
| POSTREL-W10| 16 | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 8   | 22222222 |
| POSTREL-W11| 28 | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |
| POSTREL-W12| 28 | 0  | 4    | 0   | 0  | 0  | 0  | 12 | 0   | -        |

Every measured row matches the frozen prereg predictions exactly.
The 48 pre-existing COND lines (45 from h3_guarded_sealed +
CHURN-W7/W8/W9) are byte-identical to
h3_churn_interaction/run1.txt, and the in-band
GUARDED-SEALED-VERDICT=PASS and CHURN-INTERACTION-VERDICT=PASS
still hold, so the release-then-churn worlds caused no
regression.

Kill bars (in-band + external, all 3 runs):
- R0 IDENTITY: HOLD (48/48 pre-existing COND lines byte-identical
  to h3_churn_interaction/run1.txt; 3/3 runs byte-identical; diff
  of h3_release_churn.zag against
  h3_churn_interaction/h3_churn_interaction.zag shows only the
  frozen delta in 5 hunks: lane header/tag, run_postrel_wx driver,
  3 main call sites, R1..R4 checks, verdict line). Not VOID.
  Builder erratum (no effect on verdict): PREREG.md wrote "45
  pre-existing COND lines"; the true count is 48 (45 carried from
  h3_guarded_sealed + 3 CHURN-W7/W8/W9). The executed check
  covered all 48 and all are byte-identical, so the bar holds
  under either count; the number is corrected here
  transparently, not moved as a threshold.
- R1 W10-POSTREL-HAZARD-MATERIALIZES: HOLD (rel=8, haz=8, av=8,
  ai=0, cf=16, ev=0, drop=0, lc=12, trs=22222222). At consolidate
  time no live reference existed, so the guard released all 8
  (correct per its decision-time precondition). The collision-band
  churn then installed debris 905001..905008 into free pool slots
  8..15 (pool 16 <= 32, drop=0, released slots 0..7 untouched),
  and count_hazard measured after the churn fires on all 8 trace
  entries. The hazard re-materialized after a guarded release.
- R2 W11-POSTREL-NOREF-SAFE: HOLD (rel=8, haz=0, av=8, ai=0,
  cf=28, ev=0, drop=0, lc=12, trs=22222222). Post-release natural
  churn (debris implying k in 1..20) creates no hazard: churn per
  se is inert in the post-release ordering too.
- R3 W12-PREREL-BLOCK-SURVIVES-POSTCHURN: HOLD (rel=0, haz=0,
  av=0, ai=0, cf=28, ev=0, drop=4, lc=12). Genuine references
  installed before the decision still block all 8 releases, and
  the churn arriving after the decision does not dislodge the
  block. Externally verified: the W12 row is content-identical to
  the frozen CHURN-W7 row modulo the COND tag (ordering
  invariance when the guard blocks).
- R4 CLEAN: HOLD (ai=0, ar=0 in W10/W11/W12; lc=12 all three;
  av==rel in W10 and W11).
- R5 DETERMINISM: HOLD (3/3 byte-identical).

In-band RELEASE-CHURN-VERDICT=PASS in all 3 runs; the governing
verdict is this external check.

## The frozen hazard definition against post-release references

1. The canonized guard (`learner_consolidate` + `has_live_ref`) is
   a DECISION-TIME predicate: it blocks a reason==2 release
   candidate k iff some USED pool slot holds exactly 900000+k at
   consolidate time. It does not, and in its canonized form
   cannot, protect against references installed after the release
   decision. Proven by R1 vs W7 (parent): identical reference
   values targeting identical candidate keys; references BEFORE
   the decision -> rel=0, haz=0; references AFTER the decision ->
   rel=8, haz=8. Ordering is the only variable.
2. `count_hazard` is a STATE predicate evaluated after the world
   runs: it fires for any release-trace entry whose key is
   referenced by a live pooled entry at measurement time,
   regardless of when the reference was installed relative to the
   release decision. Proven by R1: the releases were
   guarded-correct at decision time, yet haz=8.
3. The hazard is value-match-driven, not churn-driven: R1 vs R2
   differ only in debris values (collision band vs natural band)
   under identical post-release ordering -> haz=8 vs haz=0. (Same
   discrimination structure as the parent's W8 vs W9, now in the
   post-release ordering.)
4. Blocked stays blocked: R3 shows post-decision churn cannot
   dislodge a pre-decision block (rel=0, and the row is
   content-identical to W7). R1's rel=8 is therefore attributable
   to the ordering of reference installation vs the decision, not
   to churn arriving late per se.
5. The safe case is ordering-inert: R2 vs the parent's W9 (natural
   churn before vs after the decision) both yield rel=8, haz=0.

Consequence for the canonized gate: no change is proposed or
needed. The gate behaves exactly as specified in all three
release-then-churn worlds. The new frozen consequence is that the
guard's protection is decision-time only: any future substrate
that needs post-release safety must re-check at use time, pin
released entries against reference installation, or track
references genuinely (provenance) rather than decision-time
value-sniffing. The latter was already open from
H3-GUARDED-SEALED; this lane extends it from the pre-decision to
the post-decision case.

## What this establishes

1. The hazard definition covers post-release reference
   installation. A release that was guarded-correct at decision
   time can still end up hazardous (R1: haz=8), so "hazard" is a
   state property that outlives the release decision.
2. The guard's protection is decision-time only. This is now
   measured, not conjectured: the same reference values block
   before the decision (W7) and re-create the hazard after it
   (W10).
3. The ordering matrix is closed: pre-decision references block
   regardless of later churn (R3 = W7 row); post-decision natural
   churn is safe (R2 = W9 row content); only post-decision
   band-matched reference installation re-creates the hazard
   (R1).

## Honest caveats

- The adversary is the worker in a second hat (same procedural
  seal as the parent lane), not a second mind. W10/W11/W12 were
  specified in the prereg before implementation.
- The learner remains simulated; reason codes are harness-written.
- W10's collision-band churn is a targeted probe: same churn key
  (3999), owner (16), and conflict/displace mechanics as
  teach_churn, with values in the collision band. It is not a
  natural teach_churn(M,w) run; per the parent lane's clause 4,
  natural churn cannot reach the frozen candidate keys under
  policy 8 at any width, and the post-release ordering does not
  change that (W11 stays inert).
- Builder erratum in PREREG.md: "45 pre-existing COND lines"
  should read 48 (45 from h3_guarded_sealed + CHURN-W7/W8/W9).
  The check covered all 48; all byte-identical; no threshold
  moved, no effect on the verdict. Recorded here transparently.
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
try, no defect symptoms; `-o h3_release_churn_bin` used for the
output name (bare `znc <src>` names the binary without `_bin`).
New-code audit: no negated-conjunction while conditions, no
`as *i32` slice construction, no `[]u8 as *u8` casts (the two
`as *u8` hits are the pre-existing sanctioned `_zag_malloc`
pattern in z_alloc), no `!(` anywhere, if-nesting at most 2 in new
code. Git writes via /usr/bin/git directly (safebin git symlink
EPERM lesson); explicit pathspecs; no git reset; local only,
never pushed.

## Commits

- 0dd12c8b6: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before implementation, build, and runs.
- This commit: h3_release_churn.zag (source sha256
  052f254956b967fde1197b76b8f3a161065a1473e1bfa973b2e5b9484f11fafe;
  diff against h3_churn_interaction/h3_churn_interaction.zag shows
  only the frozen delta in 5 hunks), h3_release_churn_bin (sha256
  286aaa748b1441feaf73dda322b21092b7b74a62e30aaa5e04b20e50a6fef156),
  build.err, run1/2/3.txt, run1/2/3.err, REPORT.md. Local only,
  never pushed.

## Follow-ups for the parent

- The H3-CHURN-INTERACTION suggested next probe is CLOSED: the
  release-then-churn ordering is frozen and verified
  (RELEASE-CHURN-PASS R0..R5). The hazard definition against
  post-release references is frozen (clauses 1..5 above).
- The guard's protection is decision-time only. If any future
  substrate requires post-release safety (references installed
  after release must not re-create the hazard), the options are:
  re-check at use time, pin released entries against reference
  installation, or genuine reference tracking (provenance). This
  is a design question for the parent, not a defect in the
  canonized gate, which behaves exactly as specified.
- Natural next probe (not started): post-release reference
  installation via a GENUINE absorbing composite
  (install_composite after the release decision, rather than
  churn debris) — the closest analog of a real structure
  referencing released memory. Left for the parent to prioritize.
