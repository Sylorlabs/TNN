# S6 EXECUTION LOG: H-PI-REV2 step-6 alternative-explanation attack plus ablation (wave-20261001-2021pdt)

Lane: docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
Frozen prereg: PREREG_PI_REV2_STEP6.md (commit 042318b7b, committed alone before any implementation)
Worker: HPIREV2-S6-IMPL (implementer; distinct from the prereg author)
Toolchain: safebin only; `which python3` and `which python` print nothing; pinned znc.

## 1. Commit-order self-check

- `git log --format=%H -- <prereg>` returns exactly one commit: 042318b7b.
- `git rev-parse HEAD` at lane start: 042318b7b (the prereg commit).
- All S6_ files in this lane (S6_b3.zag, S6_b4.zag, S6_d1.zag, S6_m_bin,
  S6_b3_bin, S6_b4_bin, S6_d1_bin, S6_*_run*.txt/.err, S6_run_times.txt,
  S6_EXECUTION_LOG.md, S6_VERDICT.md) were created after the freeze.
  No implementation work predates it. No commits, no pushes, no git
  reset, no rebase performed by this worker. Result: PASS (ordering
  verifiable; coordinator commits).

## 2. Frozen code binding (K-ARCH1)

- Mechanism under test: docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/proc_revise2.zag
- Working-tree sha256 before any S6 work: dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
- Working-tree sha256 after all S6 runs: dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12 (unchanged)
- Committed blob at 847a8f10f (git cat-file): dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12 (match)
- cognition_source_delta = 0 exactly. The frozen file was never opened
  for writing; only read (and sed-extracted for byte-exact reuse).

## 3. New sources (post-freeze, from the prereg text only)

- S6_b3.zag (384 lines, sha256 5af61800cccb968234a617d6afaa49a6cb7ffc4a084a79365f99e3a68d0b066d):
  A1/B3 class-patch memory. Header (20 lines, new) plus byte-exact
  extracts of the frozen Section A discovery machinery: z_alloc through
  get_prog (frozen lines 22-142), benum through dsearch (frozen lines
  179-271), bytes_eq (frozen lines 308-320); all three ranges verified
  byte-exact by diff. New code: B3 helpers (b3_v1_predict, b3_predict,
  b3_pcheck) and main. The patch is installed from the single
  counterexample at runtime: test byte = F1r input[0], output byte = F1r
  output[0] (both read from data, not literals); position 0 and the
  repeat-output shape are the patch template fixed by the prereg.
  No diagnosis operator, no primitive-construction kit, no SPECIALIZE,
  no conflict rule, no rollback anywhere in the file.
- S6_b4.zag (409 lines, sha256 59dcd289a4f1184b6998a2fffa15bf56a5fe1afb6288c45fbf2a2e0d0b67c384):
  A2/B4 template-aware re-search. Same byte-exact extracts as B3 (diff
  verified). New code: the 5 frozen K-SB4a check pairs, b4_prog_predict,
  b4_tmpl_predict (the IF(byte-equality(pos,byte), alt, v_old) shape
  stated in the prereg), b4_prog_fails5, b4_tmpl_fails5, main.
  alt_prog is computed by frozen dsearch over F1r alone (not hardcoded);
  v_old is computed by frozen dsearch over T (not hardcoded).
  No diagnosis, no ranking, no conflict rule.
- S6_d1.zag (656 lines, sha256 cd19348a6e838a85e3a1961f95067c2086f5399857d871ed4616394f7cfa545b):
  D1 ablation. Header (new) plus byte-exact extract of frozen lines
  22-496 (z_alloc through build_test: Section A plus predict, observe,
  diagnose, build_test); diff verified byte-exact. EXCISED: fn
  specialize (frozen lines 503-543); its call sites (frozen lines 733,
  798) are not present. Not carried: rollback (544-557), check/pcheck/
  rcell and the original main (558-end); D1 supplies its own main and a
  d1_pcheck helper. The branch slot created by build_test is never
  consulted: D1 predicts with the selected program directly.
- M: rebuilt from the frozen source to S6_m_bin; byte-identical to the
  step-5 rev2_r_bin (sha256 7b4caa77d2e67e6df14f5f1fecf0f75180d50338961b80e00073ec06883a395c,
  cmp clean). Build determinism confirmed.

## 4. Builds (pinned znc)

- `znc S6_b3.zag -o S6_b3_bin`: exit 0.
- `znc S6_b4.zag -o S6_b4_bin`: exit 0.
- `znc S6_d1.zag -o S6_d1_bin`: exit 0.
- `znc <frozen proc_revise2.zag> -o S6_m_bin`: exit 0.
- Build logs kept in /tmp (s6_build_{b3,b4,d1,m}.log) with sha256:
  b3 a3a6a3d45fde2d1624cb79b3246ec34d849981295ade491dc59c30849e8e24e3,
  b4 aecfe87263c5181a42eaa45118b10682796f944b870499b42c119b6d306a3095,
  d1 2d7d9daea64127df3b338eac3b1383ebaa4536e6c4fcad07f3f8d29d067408ac,
  m  e817dce110f6f2f8af55bab31df05f3fc9b9c818e57a00d0599802e0418a17dc.
  (Raw logs stay out of the lane; the znc A0102 lint text is confined there.)
- Binary sha256 and sizes:
  S6_m_bin  7b4caa77d2e67e6df14f5f1fecf0f75180d50338961b80e00073ec06883a395c  106770
  S6_b3_bin a460b67a1c9baaa8085fe4e22781ed2be50a0df3ed7d019c0fb30ab59b6fa2b5  43450
  S6_b4_bin 62764deb723c1017639299ec37989c414964a20c2ec3cb219f07939cd51fe623  43351
  S6_d1_bin 54a12d428f4f33980befae844c482499fe46f9d0a4288b04b5eb5c51ce0196ac  68726

## 5. Run matrix (12 runs, per the prereg K-SB5 matrix)

- ./S6_m_bin r (x3); ./S6_b3_bin (x3); ./S6_b4_bin (x3); ./S6_d1_bin (x3).
- Stdout to S6_{M,B3,B4,D1}_run{1..3}.txt; stderr to .err (all 0 bytes).
- Per-run exit codes and wall times (S6_run_times.txt):
  M  run1 exit=0 ms=8;  run2 exit=0 ms=5;  run3 exit=0 ms=5
  B3 run1 exit=0 ms=3;  run2 exit=0 ms=3;  run3 exit=0 ms=3
  B4 run1 exit=0 ms=38; run2 exit=0 ms=32; run3 exit=0 ms=46
  D1 run1 exit=0 ms=3;  run2 exit=0 ms=3;  run3 exit=0 ms=3
- Confirmatory single runs of the frozen step-5 baselines (outside the
  K-SB5 matrix, to confirm the preserved bars still hold):
  b0_bin, b1t_bin, b1_bin each exit 0 and byte-identical to B0_run1.txt,
  B1T_run1.txt, B1_run1.txt respectively.

## 6. Determinism evidence (K-SB5)

- `cmp` across run1/run2/run3 stdout per binary: all clean
  (M 3/3 identical; B3 3/3; B4 3/3; D1 3/3).
- All 12 stderr files are 0 bytes.
- Stdout sha256 (run1; runs 2-3 identical):
  M  d5eb722d8b0a204ce155e7d82f237fa6682d88d9d0d885b930629e1c69913801
  B3 af43ec2c031543cadb61e9f2b120ef77e626bb6a452c97f04bcacb5a9b7212a4
  B4 03810f1eb4618e25b352295ea689c0e31da18f6efa0cd7b36e9cfb86d62ffdc8
  D1 391ba822a6d898d01104356c583246c468f88eae0694c02e8eee261950fff647
- Cross-check: S6_M_run1.txt is byte-identical to the step-5 frozen
  transcript REV_run1.txt (sha256 d5eb722d..., cmp clean).

## 7. Key measured outputs

M (S6_M_run1.txt, byte-identical to step-5):
- DIAGNOSIS pos=0 byte=114 conflicts=0; PRIMITIVE-CONSTRUCTED pos=0
  byte=114; VERSION v3 ACTIVE (parent v2).
- PREDICT abc -> ccc [ok]; PREDICT xy -> xx [ok]; PREDICT defg -> gggg
  [ok]; PREDICT rab -> rrr [ok]; CHECK P8-F2-reuse-no-revision: PASS;
  PREDICT rqw -> rrr [ok]. Zero DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION
  lines after the reuse check. Tail: === RESULT fails=0 ===.

B3 (S6_B3_run1.txt):
- B3 enumerated 1055 programs; B3 v1-index 38.
- B3 COUNTEREXAMPLE_DETECTED(rab); B3 PATCH ACTIVE
  test=(pos=0,byte=114,outbyte=114).
- B3 PREDICT rab -> rrr [ok]; B3 PREDICT rqw -> rrr [ok]
  (competence: both correct, not a strawman).
- B3 PREDICT abc -> ccc [ok]; B3 PREDICT xy -> yy; B3 PREDICT defg ->
  gggg [ok].
- b3_correct_f1r=1; b3_correct_reuse=1; b3_predict_xy=yy; B3 fails=0.

B4 (S6_B4_run1.txt):
- B4 enumerated 1055 programs; B4 alt-index 2; B4 v_old-index 38.
- B4 stream-total 1823; B4 programs-evaluated 1823;
  B4 first-fit-index -1; b4_enumerated=-1; b4_first_fit_index=-1;
  b4_stream_total=1823.
- The full specified stream (1055 benum programs in frozen dsearch
  order, then 768 template completions pos 0..2 / byte 0..255 ascending)
  was evaluated against the 5 frozen K-SB4a checks; zero candidates
  achieve fails=0.

D1 (S6_D1_run1.txt):
- D1 enumerated 1055 programs; D1 v1-index 38.
- COUNTEREXAMPLE_DETECTED(rab); DIAGNOSIS pos=0 byte=114 conflicts=0;
  D1 DIAGNOSIS-PRECONDITION-OK (matches the full run's P8 line).
- PRIMITIVE-CONSTRUCTED pos=0 byte=114.
- D1 alt-index 2 (SPECIALIZE excised, no branch installed).
- D1 PREDICT abc -> aaa [MISMATCH want ccc]; D1 PREDICT xy -> xx [ok];
  D1 PREDICT defg -> dddd [MISMATCH want gggg]; D1 PREDICT rab -> rrr
  [ok]; D1 PREDICT rqw -> rrr [ok].
- d1_fails_total=2; d1_predict_xy=xx.

## 8. Why B4 cannot satisfy its competence check (structural, verified empirically)

The prereg's B4 competence clause requires first_fit >= 0 on T+F1r
evaluated against the frozen K-SB4a expectations, i.e. the 5 checks
abc->ccc, xy->xx, defg->gggg, rab->rrr, rqw->rrr. B4's specified stream
cannot satisfy them, by construction:

- Benum stream: no single program fits. abc (n=3) requires eval=2 at
  every k while rab (n=3) requires eval=0 at every k; eval_prog is a
  deterministic pure function of (prog,k,n), so no program fits both.
  (This also re-verifies the K-RV2-1b impossibility shape on the
  conflict-updated set.)
- Template stream: each candidate is a single IF(byte-equality(pos,byte),
  alt=2, v_old=38). The 5 checks require the branch to fire on xy
  (input[0]='x'=120, needs alt for xx) and on rab/rqw (input[0]='r'=114,
  needs alt for rrr) while not firing on abc (input[0]='a'=97) or defg
  (input[0]='d'=100). No single (pos,byte) does this: pos=0 needs byte
  120 and byte 114 at once; pos=1 needs byte 121 and byte 97 at once;
  pos=2 cannot fire on xy (length 2). The conflict rule's xy->xx update
  is exactly what a single-branch template cannot express; the full
  mechanism's solution uses two branches.
- Empirical confirmation: all 1823 candidates evaluated, 0 full fits,
  first_fit_index=-1, 3/3 byte-identical.

## 9. Machine-greppable cost accounting

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

Notes: revision_evals, b1_enumerated are the frozen step-5 reference
points (reused per the prereg, not re-decided). wall_ms values are run1
of each binary (step-5 convention). source_delta_lines counts the three
new test-harness .zag sources (384+409+656); the byte-exact frozen
extracts inside them are disclosed in section 3. No Section B
revision-machinery code appears in any baseline.

## 10. Sealing protocol compliance

- The F1r-reuse input "rqw" is presented by B3 only after the B3 PATCH
  ACTIVE marker, by B4 only as a check pair (B4 has no constructor
  phase), and by D1 as a frozen check after the alt selection.
- Baselines share only what the prereg allows (disclosed in section 3);
  the red team may audit S6_b3.zag, S6_b4.zag, S6_d1.zag for leakage.
- The lane dir contained only step-5 artifacts at S6 start; all S6 files
  are new and prefixed S6_.

## 11. Executables invoked (K-SB6 audit)

- Safebin PATH tools only: bash, cat, cmp, cut, date, diff, grep, sed,
  sha256sum, stat, wc, znc, plus the built binaries. No python3, python,
  gcc, cc, perl, ruby, or node invoked at any stage. `which python3`
  and `which python` print nothing under the safebin PATH.
- Byte scan of every file in the lane dir: zero em-dash bytes and zero
  en-dash bytes. Compiler lint bytes are confined to /tmp build logs
  (hashes in section 4).

No em-dashes in this documentation.
