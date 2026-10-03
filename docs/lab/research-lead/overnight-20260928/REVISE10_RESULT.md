# H-REVISE10 RESULT

**Date (UTC):** 2026-09-30
**Parent:** H-REVISE9 (SURVIVES 133/133; red team SURVIVES 17/17)
**Target:** B-RV9-3 (no-contradiction direct-call misuse)
**Verdict: H-REVISE10 KILLED per K-RV10-4 (GUARD fired in inherited Phase P3b; prereg factual premise incorrect). R10 mechanism correct; K-RV10-1/2/3/5 PASS.**
**Classification:** bounded L2+ revision with firing-set contradiction protocol plus peeling attribution plus in-function contradiction guard. Not L3.

## 1. The repair (R10)

Added an in-function contradiction guard at the top of
`diagnose_rollback_check` in `revise10.zag`:

```
// H-REVISE10 R10: in-function contradiction guard (closes B-RV9-3).
let pre:[]u8=z_alloc(16);
let preok:i32=vs3_apply(VS, inp, pre);
if(preok==1 && streq(pre[0..inp.len], true_out)==1){
  emit("GUARD: no contradiction (store predicts trusted label); no state change\n");
  return 0;
}
```

If the store's actual prediction on `inp` already matches `true_out`,
no contradiction exists; return 0 with zero state change.
Precondition-violating calls are now harmless no-ops.

No other mechanism function touched. Branch A, R7 peeling loop, Branch B,
all helpers, all Phase A-P code unchanged except the new Phase Q block.

## 2. Preregistration and governance

- `PREREG_REVISE10.md` frozen and committed ALONE at **3f8304e78**
  before any implementation edit, build, or run.
- Strict ancestry verified via `git merge-base --is-ancestor`.
- `revise10.zag` = `revise9.zag` plus the frozen R10 change set
  (12-line guard + Phase Q tests + banner/verdict rename).
- Pure Zag throughout. No Python at any stage. Toolchain:
  znc 2026.07.0-dev (edition 2026). Binaries built in /tmp/rv10 only,
  never committed.
- Only H-REVISE10-owned paths staged
  (PREREG_REVISE10.md, revise10.zag, REVISE10_RAW*.txt,
  REVISE10_RESULT.md). Concurrent workers' files untouched.
- Determinism: 3/3 byte-identical via cmp, exit 0.
  md5 `4d982372220cd116561b954fa30671bd`.
- No em dashes in loop documentation (byte-verified).

## 3. Kill bar outcomes

### K-RV10-1 (B-RV9-3 closure): PASS

X-RV9-4 misuse fixture replicated exactly. VS init P0=p0b (identity);
slot1 (2,113) p0aP -> "qqq"; slot2 (1,98) p0aP -> "qqq".
Setup sanity held: vs3_apply -> "qqq" (no contradiction).
`diagnose_rollback_check(VS,"zbq","qqq")`:
- Q1 rb==0: PASS.
- Q2 st1==1 and st2==1 (zero state change): PASS.
- Q3 GUARD line present in Phase Q1 window: VERIFIED via grep
  (line 295 of raw output).
- Q4 vs3_apply still predicts "qqq" (store intact): PASS.

B-RV9-3 is closed at the mechanism level. Precondition-violating calls
are no-ops.

### K-RV10-2 (ACTIVE-member peel, 3 stacked wrong): PASS

VS init P0=p0b. slot1 (2,113) p0aP correct. slot2 (1,98) wprogP wrong,
confirmed to ACTIVE. slot3 (0,122) wprogP wrong, confirmed to ACTIVE.
slot4 (2,113) wprogP wrong PROVISIONAL (most recent).
`diagnose_rollback_check(VS,"zbq","qqq")`:
- Q5 rb==1: PASS.
- Q6 st4==0 (PROVISIONAL rolled back): PASS.
- Q7 st3==1 (ACTIVE demoted, NOT rolled back): PASS.
- Q8 st2==1 (ACTIVE demoted, NOT rolled back): PASS.
- Q9 st1==1 (correct untouched): PASS.
- Q10 second contradiction fells demoted members, restoration "qqq"
  exact: PASS.

The peel applies the per-member protocol correctly through the
peel path: PROVISIONAL members roll back, ACTIVE members demote on
first contradiction, then roll back on second.

### K-RV10-3 (forged label, mixed ACTIVE/PROVISIONAL): PASS

VS init P0=p0aP. slot1 (0,122) p0bP correct, confirmed to ACTIVE.
slot2 (1,98) p0bP correct, PROVISIONAL. Forged F="qqq" (=P0("zbq")).
The R10 guard does NOT trigger (F differs from store prediction "zbq").
`diagnose_rollback_check(VS,"zbq",F)`:
- Q11 rb==1: PASS.
- Q12 st2==0 (PROVISIONAL rolled back): PASS.
- Q13 st1==1 (ACTIVE demoted, NOT rolled back): PASS.

Forged labels against mixed stacks apply the per-member protocol via
Branch B. Dual-use disclosed (as since H-REVISE7).

### K-RV10-4 (regression): KILL

All 117 inherited CHECK lines byte-identical to frozen REVISE9 raw
(sorted diff confirms). P11/P12 (P3b veto) still PASS with identical
output lines.

**Kill trigger:** The R10 GUARD fired in inherited Phase P3b (line 276
of raw output), outside Phase Q. Per frozen K-RV10-4: "KILL if...
GUARD fires outside Phase Q."

**Root cause (prereg error, not mechanism error):** PREREG_REVISE10.md
asserted "(all inherited calls satisfy the documented precondition)".
This factual premise was incorrect. Phase P3b (veto test) calls
`diagnose_rollback_check` with a store that predicts true_out
(slot2 correct and most-recent), violating the documented
precondition. The R10 guard correctly identifies the absence of
contradiction and returns 0. P3b's outcome is unchanged (rb==0, no
state change); the guard provides the same result via an explicit
precondition check rather than the implicit veto logic.

The mechanism (R10) is correct. The kill is triggered by the prereg's
incorrect factual assertion, not by a mechanism flaw.

**Additional prereg imprecision:** PREREG_REVISE10.md expected
"146/146 (133 inherited + 13 Phase Q)". The program has 145 CHECKs
(133 inherited ntest + 12 Phase Q program CHECKs; Q3 GUARD line
verified via external grep, not a program CHECK). The "133 inherited"
refers to ntest_total, not CHECK line count (117 CHECK lines).

### K-RV10-5 (determinism): PASS

3 consecutive runs byte-identical via cmp, exit 0.
md5 `4d982372220cd116561b954fa30671bd`.

## 4. Verdict

**H-REVISE10 KILLED per frozen K-RV10-4.**

The R10 in-function contradiction guard works exactly as designed:
- K-RV10-1 PASS: B-RV9-3 closed. Misuse calls are no-ops.
- K-RV10-2 PASS: ACTIVE-member peeling correct through peel path.
- K-RV10-3 PASS: Forged labels on mixed stacks handled per-member.
- K-RV10-5 PASS: Deterministic.

The KILL is triggered solely by K-RV10-4's explicit "GUARD fires
outside Phase Q" condition. The guard fired in inherited Phase P3b
because P3b violates the documented precondition (store predicts
true_out). The prereg incorrectly asserted all inherited calls satisfy
the precondition. P3b's observable outcome is unchanged.

This is a prereg precision failure, not a mechanism failure. The R10
repair is sound and B-RV9-3 is closed.

## 5. Boundaries

- B-RV9-3: CLOSED by R10 (mechanism level).
- B-RV8-1: forged firing-set amplification, narrowed and verified
  (carried forward).
- B-RV9-1: older wrong member below correct survives (carried forward).
- B-RV9-2: append-time underdetermination (carried forward).
- 5-deep peel: deferred (requires capacity-5 redesign; capacity-4
  frozen in regression suite).

## 6. Recommended follow-up

H-REVISE11: clean re-preregistration with corrected factual premises:
(1) acknowledge P3b as a precondition-violating call correctly handled
by the R10 guard; (2) correct CHECK counts (117 CHECK lines, 133
ntest_total); (3) Q3 as external grep verification. The R10 mechanism
itself requires no change.

## 7. Raw evidence (committed)

- `revise10.zag` (R10 guard + Phase Q)
- `PREREG_REVISE10.md` (frozen at 3f8304e78)
- `REVISE10_RAW.txt` (md5 4d982372220cd116561b954fa30671bd, 145/145)
- `REVISE10_RAW_R2.txt`, `REVISE10_RAW_R3.txt` (3/3 byte-identical)
- `REVISE10_RESULT.md` (this report)

## 8. Commit lineage

- 3f8304e78 PREREG H-REVISE10 FROZEN (prereg alone; strict ancestor)
- <this commit> H-REVISE10 implementation + evidence + result (KILLED per K-RV10-4)
