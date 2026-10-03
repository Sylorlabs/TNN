# S6C VERDICT: H-PI-REV2 step-6 re-execution under amendment K-AX2

Lane: docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
Frozen amendment: AMENDMENT_KAX2.md (commit 3c93a737b)
Frozen prereg: PREREG_PI_REV2_STEP6.md (commit 042318b7b)
Evidence: S6C_EXECUTION_LOG.md and the S6C run transcripts in this lane.
All measurements below are from 3/3 byte-identical runs (sha256 in the
execution log). The original step-5 BASELINE-FAIL (wave-20261001-1421pdt)
and the step-5 PASS under the amended prereg (wave-20261001-2021pdt)
are not relitigated and stand unchanged. The original step-6 verdict
(FAIL, cause K-AX2 VOID) stays in the record; this re-execution amends
it per the amendment's re-execution semantics. History is not rewritten.

## Per-bar scorecard

Bar | Threshold | Measured | Result
K-SB1 (problem real): B0 mispredicts F1r | frozen step-5 reference; M transcript byte-identical to S6 (byte-identical to step-5) | PASS
K-SB2 (revision cheaper than re-search): revision_evals < 1055, strict | revision_evals=5 (frozen step-5 reference point); M transcript byte-identical to step-5 | PASS (5 < 1055)
K-SB3 (revision beats storage on reuse): rqw->rrr with zero new revisions | "CHECK P8-F2-reuse-no-revision: PASS", "PREDICT rqw -> rrr [ok]", zero DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after | PASS
K-SB4a (revised procedure correctness): fails=0 on the 5 checks | all 5 [ok], "=== RESULT fails=0 ===" | PASS
K-SB4b (baseline competence): B1T first_fit >= 0, fails-on-T=0 | frozen step-5 reference (first-fit-index=38, fails-on-T=0) | PASS
K-SB4c (verified-impossibility recheck): B1 first_fit=-1, 1055 evaluated | frozen step-5 reference (first-fit-index=-1, programs-evaluated=1055) | PASS
K-SB5 (determinism): 12 runs, 3/3 byte-identical, exit 0, zero stderr | M/B3/B4b/D1 x3: all cmp clean, all exit 0, all 12 stderr files 0 bytes | PASS
K-SB6 (purity and docs): pure Zag, zero Python, zero em/en-dash bytes | safebin tools only; `which python3`/`which python` print nothing; byte scan of all lane files: 0 em-dash, 0 en-dash | PASS
K-AX1 (conflict rule is not a patch): B3 predicts "xy" != "xx" | b3_predict_xy=yy; b3_correct_f1r=1, b3_correct_reuse=1 (competence holds, not a strawman) | PASS: alternative A1 KILLED
K-AX2 (diagnosis beats template-aware search, amended): B4b achieves b4b_first_fit_index >= 0 (competence), and b4b_enumerated > revision_evals (5); void iff first_fit < 0 or enumerated != 88728 | b4b_first_fit_index=88727, b4b_enumerated=88728, b4b_stream_total=590879: competence satisfied, spec-fidelity satisfied (88728 == 88728), kill NOT tripped (88728 > 5) | PASS: alternative A2 KILLED
K-ABL1 (template is load-bearing): D1 fails >= 1 of the 5 checks | d1_fails_total=2 (abc->aaa, defg->ddd); DIAGNOSIS precondition "DIAGNOSIS pos=0 byte=114 conflicts=0" held | PASS: degradation shown
K-ARCH1 (zero cognition source delta) | frozen source sha256 unchanged (dd3cb02d...), delta exactly 0 | PASS
K-ARCH2 (no architecture growth) | new_semantic_cases=0, new_modes=0, new_bridges=0, new_routers=0, new_handlers=0; no protected-core changes | PASS

## Machine-greppable cost accounting

revision_evals=5
b1_enumerated=1055
b3_correct_f1r=1
b3_correct_reuse=1
b3_predict_xy=yy
b4b_first_fit_index=88727
b4b_enumerated=88728
b4b_stream_total=590879
b4b_wall_ms=4248
b3_wall_ms=29
d1_fails_total=2
d1_predict_xy=xx
revision_wall_ms=15
binary_bytes_S6_m_bin=106770
binary_bytes_S6_b3_bin=43450
binary_bytes_S6C_b4b_bin=43431
binary_bytes_S6_d1_bin=68726
source_delta_lines=435
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

K-AX2 (A2 killed under the amended bar): B4b was built exactly per the
frozen amendment and evaluated its full specified stream in frozen
order (1055 benum programs in frozen dsearch order, then 589,824 nested
two-branch template completions pos1/byte1/pos2/byte2 ascending)
against the 5 conflict-updated checks; the first full fit lands at
stream index 88727, i.e. 88,728 candidates evaluated. Competence is
satisfied (88727 >= 0) and spec fidelity is satisfied (88728 == 88728,
the amendment's predicted number), so the run is not void under either
amended clause. The kill condition (b4b_enumerated <= 5) is not tripped:
88,728 blind enumerations against 5 diagnosis-driven evals. Blind
fixed-order template-aware re-search does not match diagnosis-driven
construction on the frozen set; the efficiency claim is now actually
tested and survives this comparator. Killed, not void.

K-ABL1 (degradation shown): D1, the frozen machinery with fn specialize
(frozen lines 503-543) excised and nothing else changed, emits the
required DIAGNOSIS precondition line and then fails 2 of the 5 checks
(abc->aaa, defg->ddd) when restricted to selecting among the 1055
programs with no IF-template wrapping. The SPECIALIZE template is
load-bearing for the repair, and the bounded-L2 ceiling statement (the
authored template carries the repair) is confirmed as stated.

## Honest boundaries

- Bounded L2 ceiling, not L3: unchanged from step 5 and step 6. Nothing
  in the re-execution tests representational invention.
- The K-AX2 kill tripwire was retained and was live: a faithful
  implementation finding a fit in 5 or fewer evals would have killed the
  efficiency claim with an honest downgrade. It did not fire (88728).
- Observation (not a bar, not a kill): B4b's first fit at nested index
  87672 (pos1=0, byte1=114, pos2=0, byte2=120) is exactly the exhibited
  candidate C* from the amendment's satisfiability proof, at the
  predicted stream position 88727. The no-earlier-fit analysis in the
  amendment holds empirically for this implementation.
- This re-execution does not test K-SB4b/K-SB4c beyond the frozen
  step-5 references; those bars are preserved, not re-run, per the
  prereg.

## Verdict

step-6 verdict on re-execution: PASS under amendment K-AX2.

Reasoning, stated plainly: the amendment replaced the unsatisfiable
K-AX2 competence clause with comparator B4b and a satisfiable bar. All
12 re-execution runs held: K-AX1 killed A1, K-AX2 killed A2 with
b4b_enumerated=88728 > 5 (competence satisfied, spec fidelity exact),
K-ABL1 showed the expected degradation, the 8 step-5 bars held, and the
architecture bars held (cognition source delta 0, zero growth fields).
No kill bar tripped; the amended void rule did not fire. Per the
amendment's re-execution semantics, the step-6 verdict is amended from
"FAIL (cause K-AX2 VOID)" to "PASS on re-execution under amendment
K-AX2". The original FAIL-on-void stays in the record transparently.
The step-5 PASS record is untouched. This is not SURVIVES; the pipeline
position is unchanged (step 7 OOD remains next).

No em-dashes in this documentation.

## Builder report

BUILD-PASS: B4b built from the frozen amendment text only, all 12 runs
exit 0, 3/3 byte-identical, every bar scored per the frozen bars. No
deviations from the amendment. No forbidden executables invoked.
