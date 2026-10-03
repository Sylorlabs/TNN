# H-REVISE11 RESULT

**Date (UTC):** 2026-09-30
**Parent:** H-REVISE10 (KILLED per K-RV10-4; R10 mechanism sound,
K-RV10-1/2/3/5 PASS, 145/145 program CHECKs, 3/3 deterministic).
**Target:** governance-precision re-verdict of the R10 in-function
contradiction guard under corrected prereg premises.
**Verdict: H-REVISE11 SURVIVES 145/145. K-RV11-1/2/3/4/5 all PASS.**
**Classification:** bounded L2+ revision with firing-set contradiction
protocol plus peeling attribution plus in-function contradiction guard.
Not L3.

## 1. What H-REVISE11 is and is not

H-REVISE11 introduces NO mechanism change. The R10 in-function
contradiction guard (introduced in H-REVISE10, result commit
aa422610f) was verified sound: K-RV10-1/2/3/5 passed, 145/145 program
CHECKs passed, 3/3 deterministic. H-REVISE10 was KILLED solely because
its frozen prereg contained two incorrect factual assertions:
(1) "(all inherited calls satisfy the documented precondition)" and
(2) "GUARD MUST NOT fire outside Phase Q". In fact, inherited Phase
P3b calls `diagnose_rollback_check` with a store that already predicts
the trusted label, violating the documented precondition, and the R10
guard correctly fires there. H-REVISE11 is therefore a re-verdict of
the unchanged mechanism under a corrected frozen prereg
(PREREG_REVISE11.md, committed alone at 36b2fbc71 before any
implementation edit, build, or run).

The repair in this arc (R11) is fixture-documentation repair: the
source's own comments misdescribed Phase P3b as exercising the Branch
B veto and carried a stale expected-total comment. Both are corrected.
The diff `revise10.zag` vs `revise11.zag` was audited hunk by hunk and
contains ONLY comment lines, the banner line, and the two verdict
lines. Zero behavior change.

## 2. Preregistration and governance

- `PREREG_REVISE11.md` frozen and committed ALONE at **36b2fbc71**
  before any implementation edit, build, or run. No amendments.
- Strict ancestry verified via `git merge-base --is-ancestor`
  (36b2fbc71 is an ancestor of the implementation commit).
- `revise11.zag` starts as a cmp-verified byte-identical copy of the
  frozen `revise10.zag` blob from result commit aa422610f, plus
  exactly the frozen R11 comment/banner edits (see section 3).
- Pure Zag throughout. No Python at any stage, including builds,
  runs, greps, diffs, md5sums, and commit verification. Toolchain:
  znc 2026.07.0-dev (edition 2026). Binaries built in /tmp/rv11 only,
  never committed.
- Only H-REVISE11-owned paths staged (PREREG_REVISE11.md,
  revise11.zag, REVISE11_RAW*.txt, REVISE11_RESULT.md). Concurrent
  workers' files untouched.
- Determinism: 3/3 byte-identical via cmp, exit 0 on all runs.
  md5 `0fcb31f29db9d05a1c80809aa78619c3`.
- No em dashes in loop documentation (byte-verified with grep on the
  UTF-8 em dash byte sequence; count 0 in prereg, source, and this
  report).

## 3. The R11 change set (frozen, audited)

`diff revise10.zag revise11.zag` (against the frozen blob) contains
exactly these hunks, all comments or emit-string renames:

- R11a: header "Repairs / new protocol" list gains the R10 entry
  (guard description, defense-in-depth precedent, "carried unchanged
  into H-REVISE11").
- R11b: header "Prereg:" line now points to PREREG_REVISE11.md
  (commit 36b2fbc71); parent-preregs line gains PREREG_REVISE9.md
  (e6fbe9f77) and PREREG_REVISE10.md (3f8304e78).
- R11c: header "Known limits" gains the H-REVISE11 disclosure: P3b
  violates the documented precondition and is handled by the guard
  (expected, preregistered); the Branch B correct-member veto is
  unreachable post-R10 (subsumed by the guard), retained as
  unreachable defense-in-depth.
- R11d: the Phase P3b comment block rewritten to document the
  precondition violation (store predicts true_out via correct
  most-recent slot2) and to state that the GUARD firing there is the
  expected, preregistered, correct handling; P11/P12 pass through the
  guard path with outcomes identical to the veto path.
- R11e: the stale harness comment "Expected total: 117/117 (98
  inherited + 19 Phase O)" corrected to the frozen exact counts (145
  ntest = 133 inherited + 12 Phase Q; 129 emitted CHECK lines = 117
  inherited + 12 Phase Q; 16 silent FATAL-guarded setup checks; Q3
  verified by grep).
- R11f: banner emit H-REVISE10 -> H-REVISE11; the two verdict emits
  H-REVISE10 SURVIVES/KILLED -> H-REVISE11 SURVIVES/KILLED.

No mechanism function, no fixture logic, no CHECK condition, and no
other emit string was touched. The Phase P3b banner emit text is
unchanged (it is output covered by the regression bar).

## 4. Kill bar outcomes

### K-RV11-1 (B-RV9-3 closure): PASS

X-RV9-4 misuse fixture replicated exactly. Q1 rb==0 PASS. Q2
st1==1 and st2==1 (zero state change) PASS. Q4 vs3_apply still
predicts "qqq" (store fully intact) PASS. Q3 (GUARD line present in
the Phase Q1 window) VERIFIED via external grep: exactly 1 GUARD
line between the "Phase Q1" header (line 292) and the "Phase Q2"
header (line 300) of the raw output.

### K-RV11-2 (ACTIVE-member peel, 3 stacked wrong): PASS

Q5 rb==1 PASS. Q6 st4==0 (PROVISIONAL rolled back) PASS. Q7 st3==1
and Q8 st2==1 (ACTIVE demoted, NOT rolled back) PASS. Q9 st1==1
(correct untouched) PASS. Q10 second contradiction fells demoted
members, restoration "qqq" exact PASS.

### K-RV11-3 (forged label, mixed ACTIVE/PROVISIONAL): PASS

The R10 guard does NOT trigger (F="qqq" differs from store prediction
"zbq"). Q11 rb==1 PASS. Q12 st2==0 (PROVISIONAL rolled back) PASS.
Q13 st1==1 (ACTIVE demoted, NOT rolled back) PASS. Dual-use
disclosed (forged labels outside frozen claims, as since H-REVISE7).

### K-RV11-4 (regression): PASS

All 129 emitted CHECK lines byte-identical to the frozen REVISE10
raw (result commit aa422610f, md5
4d982372220cd116561b954fa30671bd): `diff <(grep "^CHECK "
REVISE10_RAW.txt) <(grep "^CHECK " REVISE11_RAW.txt)` empty. Full raw
diff vs the REVISE10 raw contains ONLY: (a) the banner rename
(H-REVISE10->H-REVISE11, line 1); (b) the final verdict rename
(line 330). The R10 GUARD fires exactly twice in the raw (external
grep count 2): line 276 inside the Phase P3b window (header line 273
to Phase P4 header line 280) and line 295 inside the Phase Q1 window
(header line 292 to Phase Q2 header line 300). Both firings are
preregistered expected behavior under the corrected premises. No
GUARD line appears anywhere else.

### K-RV11-5 (determinism): PASS

3 consecutive runs byte-identical via cmp, exit 0 on all three.
md5 `0fcb31f29db9d05a1c80809aa78619c3` on all three raw files.

## 5. Exact counts (frozen, verified)

- ntest_total = 145: 133 inherited (Phases A-P) + 12 Phase Q program
  CHECKs (Q1, Q2, Q4..Q13). Verified: 145
  `ntest_total=ntest_total+1` sites in revise11.zag; RESULT line
  reads 145/145.
- Emitted CHECK lines = 129: 117 inherited + 12 Phase Q. Verified by
  grep count on the raw.
- Silent FATAL-guarded setup checks = 16 (145-129), all inherited;
  they emit output only on failure. The 2 raw lines containing
  "FAIL" are inherited informational lines ("CORROBORATE FAIL: ..."),
  also present in the REVISE9 and REVISE10 raws; no test failed.
- Q3 is external grep verification, not a program CHECK, exactly as
  preregistered since PREREG_REVISE10.

## 6. Corrected causal interpretation of P3b

Phase P3b setup: VS init P0=p0a ([4,0,0]; "zbq"->"qqq"); slot1
(0,122) wprogP (wrong, predicts "zzz"); slot2 (1,98) p0aP (correct,
predicts "qqq", most recent). On inP="zbq", vs3_apply returns slot2's
"qqq", which equals true_out="qqq". No contradiction exists, so the
call violates the documented precondition ("CALL ONLY after
vs3_apply mispredicted true_out"). Pre-R10, this call reached Branch
B: not every firing member mispredicts (slot2 correct), allmiss==0,
return 0 with no emit (the "veto"). Post-R10, the in-function guard
catches it first: GUARD line, return 0, zero state change. P11/P12
pass through the guard path. The observable behavior contract of
P3b (rb==0, no state change) is preserved exactly; only the internal
path changed, and the new path is the explicitly intended
defense-in-depth handling.

New disclosed boundary (found during this arc): the Branch B
correct-member veto (allmiss==0) is unreachable post-R10. Whenever a
correct member is the most-recent firer, the store predicts true_out
and the guard fires first. With a genuine contradiction (store
mispredicts), the peel always finds a restorable proper prefix when a
correct member is in the firing set, because skipping the wrong
members more recent than the correct one exposes the correct
member's prediction. The veto logic is retained untouched as
unreachable defense-in-depth; no claim depends on reaching it.

## 7. Boundaries

- B-RV9-3: CLOSED by R10 (mechanism level); re-verdict confirms under
  corrected premises.
- B-RV8-1: forged firing-set amplification, narrowed and verified
  (carried forward).
- B-RV9-1: older wrong member below correct survives (carried forward).
- B-RV9-2: append-time underdetermination (carried forward).
- X-RV5-1: append-time detection impossible (fundamental limit,
  carried forward).
- Forged-label dual-use beyond the prefix bound (carried forward).
- Duplicate append of an ACTIVE revision (carried forward).
- Tombstone capacity (carried forward).
- Peel k=1 dead code (red-team code observation, harmless redundancy;
  carried forward).
- NEW: Branch B correct-member veto unreachable post-R10 (disclosed
  section 6; retained, not removed).
- 5-deep peel: deferred (requires capacity-5 redesign; capacity-4
  frozen in regression suite).

## 8. Raw evidence (committed)

- `revise11.zag` (R10 unchanged; R11 comment/banner edits only)
- `PREREG_REVISE11.md` (frozen at 36b2fbc71)
- `REVISE11_RAW.txt` (md5 0fcb31f29db9d05a1c80809aa78619c3, 145/145)
- `REVISE11_RAW_R2.txt`, `REVISE11_RAW_R3.txt` (3/3 byte-identical)
- `REVISE11_RESULT.md` (this report)

## 9. Commit lineage

- 3f8304e78 PREREG H-REVISE10 FROZEN (prereg alone; strict ancestor)
- aa422610f H-REVISE10 implementation + evidence + result (KILLED
  per K-RV10-4; prereg premise error, R10 sound)
- 36b2fbc71 PREREG H-REVISE11 FROZEN (prereg alone; strict ancestor
  of the implementation commit; verified via git merge-base
  --is-ancestor)
- <this commit> H-REVISE11 implementation + evidence + result
  (SURVIVES 145/145; K-RV11-1..5 PASS)

## 10. Governance disclosures

1. H-REVISE11 changes no mechanism behavior; it is a re-verdict of
   the H-REVISE10 mechanism under corrected prereg premises, plus
   fixture-documentation repair. The SURVIVES verdict applies to the
   R10 mechanism as documented, not to any new repair.
2. The P3b precondition violation was present in every generation
   since the veto test was introduced; H-REVISE10's prereg was the
   first to assert (incorrectly) that no inherited call violates the
   precondition. The violation itself is inherited, not introduced by
   R10.
3. The Branch B correct-member veto is unreachable post-R10. It was
   left in place deliberately (removal would be a behavior change
   requiring its own preregistration); it is disclosed, not depended
   upon.
4. The stale harness comment ("Expected total: 117/117") predates
   H-REVISE10 and was corrected here; it never affected execution.
5. No Python was used at any stage of this arc: implementation edits
   via file-edit tooling, builds and runs via znc, verification via
   grep/diff/cmp/md5sum in the shell.
