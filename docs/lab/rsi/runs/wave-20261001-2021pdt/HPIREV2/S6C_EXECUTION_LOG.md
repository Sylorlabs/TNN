# S6C EXECUTION LOG: H-PI-REV2 step-6 re-execution under amendment K-AX2 (wave-20261001-2021pdt)

Lane: docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
Frozen amendment: AMENDMENT_KAX2.md (committed alone at 3c93a737b)
Frozen prereg: PREREG_PI_REV2_STEP6.md (commit 042318b7b)
Worker: HPIREV2-S6C (B4b implementer and re-execution worker; distinct
from the S6 implementer and from the amendment authors; implements from
the frozen amendment text only)
Toolchain: safebin only; `which python3` and `which python` print
nothing; pinned znc.

## 1. Commit-order self-check

- `git log --format=%H -- AMENDMENT_KAX2.md` returns exactly one commit:
  3c93a737b.
- At this worker's start, HEAD was 3c93a737b. While this worker read the
  frozen documents, the coordinator advanced HEAD to 6b4ed149e (wave H5
  sealed evaluation, a different lane; no HPIREV2 file touched).
  3c93a737b is an ancestor of HEAD.
- No S6C_ file existed in the working tree or in git before this
  worker's first write (verified before writing NAMECHECK_S6C.md).
  The amendment strictly precedes every B4b artifact. Ordering is
  verifiable; UNVERIFIABLE ORDERING does not apply.
- No commits, no pushes, no git reset, no rebase performed by this
  worker. No existing lane file was modified; all S6C_ files are new.

## 2. Frozen code binding (K-ARCH1)

- Mechanism under test: docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/proc_revise2.zag
- Working-tree sha256 before any S6C work:
  dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
- Working-tree sha256 after all S6C runs:
  dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12 (unchanged)
- cognition_source_delta = 0 exactly. The frozen file was never opened
  for writing.

## 3. New sources (post-amendment, from the amendment text only)

- S6C_b4b.zag (435 lines, sha256
  a27b11284aa4e33f1930aeb993d82b77c01f2dc26b1d93b18b27589e5d441c54):
  A2/B4b repaired template-aware comparator. Structure: byte-exact
  extracts of the frozen Section A discovery machinery (z_alloc through
  get_prog, benum through dsearch, bytes_eq, matching the S6 extracts);
  new code: the 5 frozen K-SB4a check pairs, b4b_prog_predict,
  b4b_nested_predict (the exact nested IF shape from the amendment:
  IF(byte-equality(pos1,byte1), alt,
  IF(byte-equality(pos2,byte2), alt, v_old))), b4b_prog_fails5,
  b4b_nested_fails5, main. alt is computed by frozen dsearch over F1r
  alone (measured index 2, printed, never hardcoded); v_old is computed
  by frozen dsearch over T (measured index 38, printed, never
  hardcoded). Stream: 1055 benum programs in frozen dsearch order, then
  the nested template completions pos1 ascending, byte1 ascending, pos2
  ascending, byte2 ascending (589,824 candidates); stream total 590,879.
  Scan stops at the first full fit (fails=0).
- Machinery-leakage audit of S6C_b4b.zag: no fn observe, no fn
  diagnose, no fn build_test, no fn specialize, no conflict rule, no fn
  rollback. The only matches for those tokens are the header disclosure
  comment (lines 25-27) and one emit string stating what B4b does not
  use (line 335). B4b is blind fixed-order enumeration.

## 4. Builds (pinned znc)

- `znc S6C_b4b.zag -o S6C_b4b_bin`: exit 0. Build log kept in /tmp
  (sha256 d5937fe2f12d87d239a58a30ad4c1de9c10215e3dfa234062d662d6e87e29df4;
  the znc lint bytes are confined there).
- S6C_b4b_bin sha256
  52a2900ce202282bf4e9cb1a01136b1dd02fc1bbe657af1e981666b16ca7c19c, 43431 bytes.
- M, B3, D1 binaries are the S6 builds (S6_m_bin, S6_b3_bin,
  S6_d1_bin), already built from frozen step-6 sources; the amended
  matrix reuses them. S6C_m_bin-style rebuilds were not needed: the
  binaries are the exact S6 artifacts and S6 verified their build.

## 5. Run matrix (12 runs, per the amended K-SB5 wording)

- ./S6_m_bin r (x3); ./S6_b3_bin (x3); ./S6C_b4b_bin (x3);
  ./S6_d1_bin (x3).
- Stdout to S6C_{M,B3,B4b,D1}_run{1..3}.txt; stderr to .err
  (all 12 files 0 bytes).
- Per-run exit codes and wall times (S6C_run_times.txt):
  M   run1 exit=0 ms=15;  run2 exit=0 ms=39;  run3 exit=0 ms=39
  B3  run1 exit=0 ms=29;  run2 exit=0 ms=14;  run3 exit=0 ms=14
  B4b run1 exit=0 ms=4248; run2 exit=0 ms=4086; run3 exit=0 ms=3293
  D1  run1 exit=0 ms=30;  run2 exit=0 ms=16;  run3 exit=0 ms=10

## 6. Determinism evidence (K-SB5)

- `cmp` across run1/run2/run3 stdout per binary: all clean
  (M 3/3 identical; B3 3/3; B4b 3/3; D1 3/3). Determinism PASS.
- All 12 stderr files are 0 bytes. All 12 exit codes are 0.
- Stdout sha256 (run1; runs 2-3 identical):
  M   d5eb722d8b0a204ce155e7d82f237fa6682d88d9d0d885b930629e1c69913801
  B3  af43ec2c031543cadb61e9f2b120ef77e626bb6a452c97f04bcacb5a9b7212a4
  B4b 0b2c12d48be8bca20806ffd0d61bab26aa64f7102ac7a8ec520b4aeffc7b1e89
  D1  391ba822a6d898d01104356c583246c468f88eae0694c02e8eee261950fff647
- Cross-check: S6C_M_run1.txt is byte-identical to S6_M_run1.txt
  (sha256 d5eb722d..., cmp clean); S6C_B3_run1.txt is byte-identical to
  S6_B3_run1.txt (sha256 af43ec2c..., cmp clean); S6C_D1_run1.txt is
  byte-identical to S6_D1_run1.txt (sha256 391ba822..., cmp clean).
  M, B3, D1 reproduce their S6 transcripts byte-identically, as the
  amendment expected.

## 7. Key measured outputs

M (S6C_M_run1.txt, byte-identical to S6):
- DIAGNOSIS pos=0 byte=114 conflicts=0; PRIMITIVE-CONSTRUCTED pos=0
  byte=114; VERSION v3 ACTIVE (parent v2).
- PREDICT abc -> ccc [ok]; PREDICT xy -> xx [ok]; PREDICT defg -> gggg
  [ok]; PREDICT rab -> rrr [ok]; CHECK P8-F2-reuse-no-revision: PASS;
  PREDICT rqw -> rrr [ok]. Zero DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION
  lines after the reuse check. Tail: === RESULT fails=0 ===.

B3 (S6C_B3_run1.txt, byte-identical to S6):
- B3 enumerated 1055 programs; B3 v1-index 38.
- B3 COUNTEREXAMPLE_DETECTED(rab); B3 PATCH ACTIVE
  test=(pos=0,byte=114,outbyte=114).
- B3 PREDICT rab -> rrr [ok]; B3 PREDICT rqw -> rrr [ok]
  (competence: both correct, not a strawman).
- B3 PREDICT abc -> ccc [ok]; B3 PREDICT xy -> yy; B3 PREDICT defg ->
  gggg [ok].
- b3_correct_f1r=1; b3_correct_reuse=1; b3_predict_xy=yy.

B4b (S6C_B4b_run1.txt):
- B4b enumerated 1055 programs; B4b alt-index 2; B4b v_old-index 38
  (both computed by frozen dsearch, never hardcoded).
- B4b stream-total 590879; B4b programs-evaluated 88728;
  B4b first-fit-index 88727; b4b_enumerated=88728;
  b4b_first_fit_index=88727; b4b_stream_total=590879.

D1 (S6C_D1_run1.txt, byte-identical to S6):
- D1 enumerated 1055 programs; D1 v1-index 38.
- COUNTEREXAMPLE_DETECTED(rab); DIAGNOSIS pos=0 byte=114 conflicts=0;
  D1 DIAGNOSIS-PRECONDITION-OK.
- D1 PREDICT abc -> aaa [MISMATCH want ccc]; D1 PREDICT xy -> xx [ok];
  D1 PREDICT defg -> dddd [MISMATCH want gggg]; D1 PREDICT rab -> rrr
  [ok]; D1 PREDICT rqw -> rrr [ok].
- d1_fails_total=2; d1_predict_xy=xx.

## 8. K-AX2 spec-fidelity and competence checks (amended bar)

- Competence: b4b_first_fit_index=88727 >= 0. Satisfied; the run is not
  void under clause (a).
- Spec fidelity: b4b_enumerated=88728 equals the amendment's predicted
  88728 exactly (and b4b_first_fit_index=88727, b4b_stream_total=590879
  match the predicted 88727 and 590879). Satisfied; the run is not void
  under clause (b). The implementation is a faithful realization of the
  frozen enumeration order and candidate shape.
- Kill tripwire: b4b_enumerated=88728 > revision_evals=5. The kill
  condition (b4b_enumerated <= 5) is NOT tripped. Template-aware
  re-search needs 88,728 blind enumerations against diagnosis-driven
  construction in 5 evals: the efficiency claim is actually tested and
  survives this comparator.

## 9. Machine-greppable cost accounting (amended field names)

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

Notes: revision_evals and b1_enumerated are the frozen step-5 reference
points (reused per the prereg, not re-decided). wall_ms values are run1
of each binary (step-5 convention). source_delta_lines counts the one
new test-harness source (S6C_b4b.zag, 435 lines); the byte-exact frozen
extracts inside it are disclosed in section 3. No Section B
revision-machinery code appears in the baseline.

## 10. Sealing protocol compliance

- The F1r-reuse input "rqw" is presented by B3 only after the B3 PATCH
  ACTIVE marker, by B4b only as a check pair (B4b has no constructor
  phase), and by D1 as a frozen check after the alt selection.
- Baselines share only what the amendment allows (disclosed in
  section 3); the red team may audit S6C_b4b.zag for leakage.
- The lane dir contained only S6 and step-5 artifacts at S6C start; all
  S6C files are new and prefixed S6C_.

## 11. Executables invoked (K-SB6 audit)

- Safebin PATH tools only: bash, cat, cmp, cut, date, diff, grep, sed,
  sha256sum, stat, wc, znc, plus the built binaries. No python3, python,
  gcc, cc, perl, ruby, or node invoked at any stage. `which python3`
  and `which python` print nothing under the safebin PATH.
- Byte scan of every file in the lane dir: zero em-dash bytes and zero
  en-dash bytes. Compiler lint bytes are confined to /tmp build logs
  (hashes in section 4).

No em-dashes in this documentation.
