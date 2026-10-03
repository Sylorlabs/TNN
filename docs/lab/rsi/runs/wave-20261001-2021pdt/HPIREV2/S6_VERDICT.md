# S6 VERDICT: H-PI-REV2 step-6 alternative-explanation attack plus ablation

Lane: docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
Frozen prereg: PREREG_PI_REV2_STEP6.md (commit 042318b7b)
Evidence: S6_EXECUTION_LOG.md and the S6 run transcripts in this lane.
All measurements below are from 3/3 byte-identical runs (sha256 in the
execution log). The original step-5 BASELINE-FAIL (wave-20261001-1421pdt)
and the step-5 PASS under the amended prereg (wave-20261001-2021pdt) are
not relitigated and stand unchanged.

## Per-bar scorecard

Bar | Threshold | Measured | Result
K-SB1 (problem real): B0 mispredicts F1r | "B0 PREDICT rab -> bbb", confirmatory run byte-identical to step-5 | PASS
K-SB2 (revision cheaper than re-search): revision_evals < 1055, strict | revision_evals=5 (frozen step-5 reference point); M transcript byte-identical to step-5 | PASS (5 < 1055)
K-SB3 (revision beats storage on reuse): rqw->rrr with zero new revisions | "CHECK P8-F2-reuse-no-revision: PASS", "PREDICT rqw -> rrr [ok]", zero DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after | PASS
K-SB4a (revised procedure correctness): fails=0 on the 5 checks | all 5 [ok], "=== RESULT fails=0 ===" | PASS
K-SB4b (baseline competence): B1T first_fit >= 0, fails-on-T=0 | first-fit-index=38, fails-on-T=0, byte-identical to step-5 | PASS
K-SB4c (verified-impossibility recheck): B1 first_fit=-1, 1055 evaluated | first-fit-index=-1, programs-evaluated=1055, byte-identical to step-5 | PASS
K-SB5 (determinism): 12 runs, 3/3 byte-identical, exit 0, zero stderr | M/B3/B4/D1 x3: all cmp clean, all exit 0, all 12 stderr files 0 bytes | PASS
K-SB6 (purity and docs): pure Zag, zero Python, zero em/en-dash bytes | safebin tools only; `which python3`/`which python` print nothing; byte scan of all lane files: 0 em-dash, 0 en-dash | PASS
K-AX1 (conflict rule is not a patch): B3 predicts "xy" != "xx" | b3_predict_xy=yy; b3_correct_f1r=1, b3_correct_reuse=1 (competence holds, not a strawman) | PASS: alternative A1 KILLED
K-AX2 (diagnosis beats template-aware search): B4 first_fit >= 0 AND b4_enumerated > 5 | b4_first_fit_index=-1, b4_enumerated=-1, 1823/1823 candidates evaluated, 0 full fits | VOID (see below)
K-ABL1 (template is load-bearing): D1 fails >= 1 of the 5 checks | d1_fails_total=2 (abc->aaa, defg->ddd); DIAGNOSIS precondition "DIAGNOSIS pos=0 byte=114 conflicts=0" held | PASS: degradation shown
K-ARCH1 (zero cognition source delta) | frozen source sha256 unchanged (dd3cb02d...), delta exactly 0 | PASS
K-ARCH2 (no architecture growth) | new_semantic_cases=0, new_modes=0, new_bridges=0, new_routers=0, new_handlers=0; no protected-core changes | PASS

## Machine-greppable cost accounting

revision_evals=5
b1_enumerated=1055
b3_correct_f1r=1
b3_correct_reuse=1
b3_predict_xy=yy
b4_first_fit_index=-1
b4_enumerated=-1
b4_stream_total=1823
b4_wall_ms=38
b3_wall_ms=3
d1_fails_total=2
d1_predict_xy=xx
revision_wall_ms=8
binary_bytes_S6_m_bin=106770
binary_bytes_S6_b3_bin=43450
binary_bytes_S6_b4_bin=43351
binary_bytes_S6_d1_bin=68726
source_delta_lines=1449
cognition_source_delta=0
new_semantic_cases=0
new_modes=0
new_bridges=0
new_routers=0
new_handlers=0

## Killing evidence

K-AX1 (A1 killed): the class-patch baseline B3, built exactly per the
prereg (frozen v1 plus IF(input[0]==114, repeat 114, v_old), no
diagnosis, no conflict rule), satisfies its competence checks
(F1r and F1r-reuse both correct) yet predicts "xy"->"yy" while the
revised procedure predicts "xy"->"xx". The conflict rule's update of
the superseded record is therefore behaviorally distinguishable from a
class patch: the alternative explanation A1 does not reproduce the full
mechanism's behavior on the frozen probes. Killed, not void.

K-AX2 (VOID, not killed, not tripped): B4 was built exactly per the
frozen specification and exhaustively evaluated its full 1823-candidate
stream (1055 benum programs in frozen dsearch order, then 768
single-branch template completions) against the 5 conflict-updated
checks; zero candidates achieve fails=0, so first_fit_index=-1. The
prereg's competence clause states that a B4 failing to solve the set "is
a broken baseline and the run is void, not a kill." The void is
structural, not an implementation defect: no benum program can fit the
set (abc at n=3 needs eval=2 while rab at n=3 needs eval=0), and no
single-branch template can (the checks need a branch on 'x'=120 for xy
and a branch on 'r'=114 for rab/rqw while abc/defg stay on v_old; one
IF expresses only one). The K-AX2 competence clause as written is
therefore unsatisfiable for the B4 it specifies. Per the prereg, this
is void, explicitly not a kill, and the kill condition
(b4_enumerated <= 5) is not evaluated on a voided run.

K-ABL1 (degradation shown): D1, the frozen machinery with fn specialize
(frozen lines 503-543) excised and nothing else changed, emits the
required DIAGNOSIS precondition line and then fails 2 of the 5 checks
(abc->aaa, defg->ddd) when restricted to selecting among the 1055
programs with no IF-template wrapping. The SPECIALIZE template is
load-bearing for the repair, and the bounded-L2 ceiling statement (the
authored template carries the repair) is confirmed as stated.

## Honest boundaries

- Bounded L2 ceiling, not L3: unchanged from step 5. Nothing in step 6
  tests representational invention.
- The K-AX2 void is a prereg-specification gap, not mechanism evidence
  for or against the efficiency claim. It must not be read as a kill of
  A2 (the prereg forbids it) nor as a vindication of A2.
- Observation (not a bar, not a kill): B4's exhaustive failure shows the
  conflict rule plus the second branch do work that single-branch
  template completion cannot replicate on the frozen set. This is
  information for the coordinator, not a verdict input.

## Verdict

step-6 verdict: FAIL, cause K-AX2 VOID.

Reasoning, stated plainly: the prereg's step-6 PASS requires K-AX1 and
K-AX2 to kill their alternatives. K-AX1 killed A1. K-AX2 did not kill
A2: B4, built exactly as specified, returns first_fit=-1, which
triggers the prereg's own void-on-failure competence clause
("a B4 failing to solve the set is a broken baseline and the run is
void, not a kill"). A voided alternative is neither killed nor tripped,
so the PASS conditions are not met. No kill bar tripped; this FAIL is
void-driven, not kill-driven. No bar was weakened to reach it, and the
step-5 PASS record is not retroactively altered.

Recommended coordinator action: amend and re-freeze K-AX2 (the B4
competence clause as written is unsatisfiable for the specified B4;
a repaired bar needs a solvable competence set or a different
comparator), then re-execute step 6 under the amended text. This is not
SURVIVES; the pipeline position is unchanged otherwise.

No em-dashes in this documentation.
