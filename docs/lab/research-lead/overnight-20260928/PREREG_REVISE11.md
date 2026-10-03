# PREREG H-REVISE11: FROZEN

**Date (UTC):** 2026-09-30
**Parent:** H-REVISE10 (KILLED per K-RV10-4; R10 mechanism sound,
K-RV10-1/2/3/5 PASS, 145/145 program CHECKs, 3/3 deterministic).
**Target of this arc:** governance-precision re-verdict. H-REVISE10 was
killed by an incorrect factual assertion in its own frozen prereg, not
by a mechanism flaw. PREREG_REVISE10.md asserted "(all inherited calls
satisfy the documented precondition)" and required "GUARD MUST NOT fire
outside Phase Q". Both premises were factually wrong: inherited Phase
P3b (veto test) calls `diagnose_rollback_check` with a store that
already predicts the trusted label, violating the documented
precondition ("CALL ONLY after vs3_apply mispredicted true_out"), and
the R10 guard correctly fires there. P3b's observable outcome is
unchanged (rb==0, no state change); the guard supplies it through the
explicit precondition check instead of the implicit Branch B veto
logic. This prereg corrects those premises and freezes the exact
expected behavior, including the GUARD firing in P3b.

**This prereg is committed alone, before any implementation edit,
build, or run. No amendments.**

## Corrected factual premises (frozen)

**P3b is a precondition-violating call.** Phase P3b setup: VS init
P0=p0a ([4,0,0]; "zbq"->"qqq"); vs3_revise slot1 (0,122) wprogP (wrong,
predicts "zzz"); vs3_revise slot2 (1,98) p0aP (correct, predicts "qqq",
most recent). On input inP="zbq", vs3_apply(VSP3b) returns slot2's
prediction "qqq", which equals true_out outP="qqq". No contradiction
exists. The documented precondition of `diagnose_rollback_check`
("CALL ONLY after vs3_apply mispredicted true_out") is therefore
violated by this call. The R10 in-function guard detects exactly this
and returns 0 with zero state change, emitting the GUARD line. This is
the EXPECTED and CORRECT behavior: the guard exists precisely to make
precondition-violating calls harmless no-ops. P11 (rb==0) and P12 (no
state change) pass through the guard path with byte-identical CHECK
lines to the frozen REVISE9 raw.

**Branch B correct-member veto is unreachable post-R10 (disclosed, not
removed).** Pre-R10, P3b exercised Branch B's veto: not every firing
member mispredicts (slot2 correct), so allmiss==0 and the function
returns 0 with no emit. Post-R10, any call shaped like P3b (most-recent
firing member correct, store predicts true_out) is caught by the guard
first. With a genuine contradiction (store mispredicts true_out), the
peel always finds a restorable proper prefix whenever a correct member
is in the firing set (skipping the wrong members more recent than the
correct one exposes it), so the allmiss==0 veto path cannot be reached
either. The veto logic remains in the source as unreachable
defense-in-depth; P3b now covers the guard path. No claim depends on
reaching the veto.

**Exact counts (frozen).** ntest_total = 145 program CHECKs: 133
inherited (Phases A-P) + 12 Phase Q (Q1, Q2, Q4..Q13; Q3 is external
grep verification, not a program CHECK). Emitted CHECK lines = 129:
117 inherited + 12 Phase Q. The 16 difference (145-129) is silent
FATAL-guarded setup checks in the inherited phases, which emit output
only on failure. The R10 GUARD line appears exactly 2 times in the raw
output: once in Phase P3b (line ~276 of the REVISE10 raw) and once in
Phase Q1 (line ~295), verified by external grep. Q3 (GUARD line present
in the Q1 window) is verified via external grep on the raw output, per
the PREREG_REVISE10 precedent.

## R11 design (frozen): fixture-documentation repair, no behavior change

`revise11.zag` = `revise10.zag` (result commit aa422610f) copied
verbatim (cmp-verified) plus EXACTLY the following comment/banner
edits. No mechanism function, no fixture logic, no CHECK, no emit
string is touched:

- R11a: header "Repairs / new protocol" list gains the R10 entry
  (in-function contradiction guard, closes B-RV9-3; introduced in
  H-REVISE10, carried unchanged).
- R11b: header "Prereg:" line points to PREREG_REVISE11.md (this file,
  frozen commit recorded at implementation time); parent-preregs line
  gains PREREG_REVISE10.md (3f8304e78).
- R11c: header "Known limits" gains two disclosures: (1) Phase P3b
  violates the documented precondition and is handled by the R10
  guard (expected, preregistered); (2) the Branch B correct-member
  veto is unreachable post-R10 (subsumed by the guard), retained as
  unreachable defense-in-depth.
- R11d: the Phase P3b comment block is corrected: it documents the
  precondition violation (store predicts true_out via correct
  most-recent slot2) and states that the GUARD firing there is the
  expected, preregistered, correct handling.
- R11e: the stale harness comment "Expected total: 117/117 (98
  inherited + 19 Phase O)" is corrected to the frozen exact counts
  (145 ntest_total = 133 inherited + 12 Phase Q; 129 emitted CHECK
  lines = 117 inherited + 12 Phase Q; 16 silent FATAL-guarded setup
  checks).
- R11f: banner and verdict renames H-REVISE10 -> H-REVISE11 only.

The diff `revise10.zag` vs `revise11.zag` therefore contains ONLY
comment lines, the banner line, and the two verdict lines. A hunk
audit will confirm zero behavior change.

Revised claim (extends the H-REVISE10 claim unchanged): 1 contradiction
fells a provisional revision and 2 fell a confirmed one. When the
most-recent prefix of firing revisions jointly overrode a correct
prediction, the contradiction protocol applies to the smallest such
prefix. Calls without a genuine contradiction (the store already
predicts the trusted label) are no-ops with zero state change, handled
by the in-function guard; this explicitly includes inherited Phase P3b.
If no correct uncovered baseline exists, no action is taken.

Residuals carried forward (not repaired): X-RV5-1 append-time
underdetermination; forged-label dual-use beyond the prefix bound;
duplicate append of an ACTIVE revision; tombstone capacity; peel k=1
dead code (red-team code observation, harmless redundancy); Branch B
correct-member veto unreachable post-R10 (newly disclosed here).
5-deep peel still deferred (requires capacity-5 redesign).

## Frozen kill bars

**K-RV11-1 (B-RV9-3 closure):** Replicate the X-RV9-4 adversary fixture
exactly (same as K-RV10-1). VS init P0=p0b ([0,0,0] identity).
vs3_revise(VS,2,113,p0a,1) -> slot1 (correct, predicts "qqq" on "zbq");
vs3_revise(VS,1,98,p0a,1) -> slot2 (correct, predicts "qqq" on "zbq",
most recent). Setup sanity (FATAL if broken): vs3_apply(VS,"zbq")
predicts "qqq" exactly (no contradiction exists). Then
`diagnose_rollback_check(VS,"zbq","qqq")` MUST return exactly 0;
vs3_status(VS,1)==1 AND vs3_status(VS,2)==1 (zero state change); the
raw output MUST contain the GUARD emit line in the Phase Q1 window
(external grep; this is Q3). KILL if: return!=0, either slot touched,
or the GUARD line absent from the Q1 window.

**K-RV11-2 (ACTIVE-member peel, 3 stacked wrong):** Identical to
K-RV10-2. VS init P0=p0b (identity; "zbq"->"zbq").
vs3_revise(VS,2,113,p0a,1) -> slot1 (correct, predicts "qqq").
vs3_revise(VS,1,98,wprog,1) -> slot2 (wrong, predicts "zzz");
`diagnose_confirm_check(VS,"zbq","zzz")` MUST return 1 (FATAL if not;
slot2 fires, P0 mispredicts); vs3_status(VS,2)==2 (ACTIVE).
vs3_revise(VS,0,122,wprog,1) -> slot3 (wrong); confirm to ACTIVE the
same way (FATAL if not). vs3_revise(VS,2,113,wprog,1) -> slot4 (wrong,
most recent; duplicate cond of slot1 appends as slot4 since slot1 is
live). Setup sanity (FATAL): vs3_apply(VS,"zbq") predicts "zzz"
(genuine contradiction vs "qqq"). Then
`diagnose_rollback_check(VS,"zbq","qqq")` MUST return exactly 1;
vs3_status(VS,4)==0 (PROVISIONAL rolled back); vs3_status(VS,3)==1 AND
vs3_status(VS,2)==1 (ACTIVE members demoted, NOT rolled back);
vs3_status(VS,1)==1 (correct untouched); vs3_apply(VS,"zbq") predicts
"qqq" exactly (restoration via slot1). KILL on any deviation.

**K-RV11-3 (forged label, mixed ACTIVE/PROVISIONAL stack):** Identical
to K-RV10-3. VS init P0=p0a ([4,0,0]; "zbq"->"qqq").
vs3_revise(VS,0,122,p0b,1) -> slot1 (correct identity, predicts "zbq");
`diagnose_confirm_check(VS,"zbq","zbq")` MUST return 1 (FATAL if not);
vs3_status(VS,1)==2 (ACTIVE). vs3_revise(VS,1,98,p0b,1) -> slot2
(correct identity, predicts "zbq", PROVISIONAL). Setup sanity (FATAL):
vs3_apply(VS,"zbq") predicts "zbq". Forged F="qqq" (=P0("zbq"), differs
from store prediction so the R10 guard does not trigger; the mechanism
cannot authenticate labels). `diagnose_rollback_check(VS,"zbq",F)`
MUST return exactly 1; vs3_status(VS,2)==0 (PROVISIONAL rolled back);
vs3_status(VS,1)==1 (ACTIVE demoted, NOT rolled back). KILL on any
deviation. Dual-use disclosed (forged labels outside frozen claims, as
since H-REVISE7).

**K-RV11-4 (regression):** All 129 emitted CHECK lines byte-identical
to the frozen REVISE10 raw (result commit aa422610f, md5
4d982372220cd116561b954fa30671bd). Full raw diff vs that raw contains
ONLY: (a) banner rename H-REVISE10->H-REVISE11; (b) the final
RESULT/verdict lines rename. The R10 GUARD fires exactly twice in the
raw (Phase P3b once, Phase Q1 once), verified by external grep; both
firings are preregistered expected behavior under the corrected
premises. KILL if: any CHECK line differs, the diff contains any other
category, the GUARD count is not exactly 2, or a GUARD line appears
outside the P3b and Q1 windows.

**K-RV11-5 (determinism):** 3 consecutive runs byte-identical via cmp,
exit 0. KILL on any byte difference or nonzero exit.

## Phase Q fixtures (unchanged from H-REVISE10, hand-derived, frozen)

Q1 (guard closure, 4 CHECKs): Q1 rb==0. Q2 st1==1 and st2==1. Q3 GUARD
line present exactly once in the Phase Q1 window (external grep, not a
program CHECK). Q4 vs3_apply still predicts "qqq" (store fully intact).
Q2 (ACTIVE peel, 6 CHECKs): Q5 rb==1. Q6 st4==0. Q7 st3==1. Q8 st2==1.
Q9 st1==1. Q10 restoration "qqq" exact.
Q3 (forged mixed, 3 CHECKs): Q11 rb==1. Q12 st2==0. Q13 st1==1.

Total new: 12 program CHECKs + Q3 external grep verification. Expected
grand total: 145/145 ntest (133 inherited + 12 Phase Q); 129 emitted
CHECK lines (117 inherited + 12 Phase Q).

## Governance (frozen)

Pure Zag: implementation, fixtures, builds, runs, analysis. Zero Python
at any stage, including verification. No em dashes in loop documentation
(byte-checked before commit). Binaries built in /tmp only, never
committed. Only owned paths staged (PREREG_REVISE11.md, revise11.zag,
REVISE11_RAW*.txt, REVISE11_RESULT.md). Concurrent workers' files
untouched. No push authorized.
