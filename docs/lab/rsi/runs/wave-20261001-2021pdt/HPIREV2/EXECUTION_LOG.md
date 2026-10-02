# EXECUTION LOG: H-PI-REV2 step-5 re-execution under amended prereg (wave-20261001-2021pdt)

Lane: docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
Amended prereg: docs/lab/rsi/runs/wave-20261001-1721pdt/HPIREV2/PREREG_PI_REV2_STEP5_BASELINE_AMENDED.md
Frozen amendment commit: 72168c60803b95b3b586eb1cf6f1fc9bd001b174
Original step-5 verdict (BASELINE-FAIL, wave-20261001-1421pdt) stands
unchanged; this log covers the re-execution under the AMENDED bars only.

## 1. Commit-order self-check

- `git log --format=%H -- docs/lab/rsi/runs/wave-20261001-1721pdt/HPIREV2/PREREG_PI_REV2_STEP5_BASELINE_AMENDED.md`
  returns exactly one commit: 72168c60803b95b3b586eb1cf6f1fc9bd001b174
  (dated 2026-10-02), the frozen amendment commit.
- Lane dir docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/ was empty at
  lane start. All baseline sources and runs below were created after the
  freeze. No implementation work predates it.
- Result: PASS.

## 2. Frozen code binding

- Mechanism under test:
  docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/proc_revise2.zag
- Working-tree sha256:
  dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
- Committed blob at 847a8f10f, git cat-file verified:
  dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
  (match).
- Adversary byte: 'r' (114), last letter of the frozen set {k,m,r} per
  ADVERSARY_BYTE_SET4.md. Disjoint from every frozen fixture input
  string by that audit.

## 3. Baseline sources

- b0.zag, b1.zag, b2.zag: byte-exact copies (cp) of the original
  wave-20261001-1421pdt step-5 baseline sources. sha256 after copy
  matches the source lane exactly:
  b0 c6ccc64ab57e962607ef3cccc37c3374c9d0b486b21e4bb4542bfd6c7202f7d6
  b1 532ec1df6d4acc56dcaf1841feb69815770641700688374bed61f8a00dd936ae
  b2 9c476796b1bdb8336a93feb1fb3352081848982e8043d80b9e387d376b0100ca
- b1t.zag (new, required by amended K-SB4b): lines 1-224 are
  byte-exact identical to b1.zag lines 1-224 (diff of the two ranges
  is empty; the shared frozen discovery machinery), followed by the new
  main in main_b1t.txt (75 lines): stages only the 3 T sequences
  ("abc"->"ccc", "xy"->"yy", "defg"->"gggg"), scans the same 1055
  programs in the frozen dsearch order counting evaluations, emits
  first-fit-index, then re-verifies the fitted program over T and
  emits fails-on-T. No revision-machinery code anywhere in any
  baseline; no revision-machinery code in b1t.zag.
- New code written for the amended run: main_b1t.txt only (75 lines of
  pure Zag following the same idioms as the frozen shared code).
- new_semantic_cases=0, new_modes=0, new_bridges=0. No protected-core
  changes.

## 4. Builds (pinned znc)

- Command: `znc <src>.zag -o <bin>` for b0, b1, b2, b1t, and the frozen
  proc_revise2.zag to rev2_r_bin. All 5 builds exit 0.
- Raw build logs kept in /tmp (they contain a compiler-emitted em-dash
  from the znc A0102 lint text; K-SB6 keeps the lane byte-clean):
  build logs stdout sha256:
  b0 a77779cc2ae7ea3b1e70659c2094d7834798fe4c8235cb7d9515f8f279f4342c
  b1 675a0f1420eb1894f6dd024339c1377c66ef5aa76266f7ac9b83e61ae69ed114
  b1t fa05a0b329e4811c014616d131266fc537c15142d6134de68a2f4efd38094264
  b2 8668528059d6624866d2c7e71a9effd00b61a67979e0aab9aa2a1c8324220513
  rev 3ae1a9f70feb76a4e697eea712303904d67ed1e833420410669dba128cec07fa
  stderr sha256:
  b0/b1/b1t/b2 d5937fe2f12d87d239a58a30ad4c1de9c10215e3dfa234062d662d6e87e29df4
  (identical to the original lane's recorded build stderr hash)
  rev 0b550bf867ef8aa0882a12e99449d0f9f2df6a5c89a268143ecd099f836118b4
  Build diagnostics: only the environmental zagd warning and the
  pre-existing A0102 lint on an ignored loadseq return at line 607,
  identical to the lint recorded for the original build.
- Binary sha256 and sizes:
  b0_bin   4f5698c6a4a980e153ba866108cedd335aee0598c882545eaed9af254478290f  22331
  b1_bin   ba47b700f03d34701371ee7d3aafdd570f99e0f5451b10df6a52b0e08480a7d2  34776
  b1t_bin  dbd735384feeffc188fe28ee9c83275fbc0dc310a356a5ec8e9a74c4f6f109a6  34825
  b2_bin   5de7632da1fd1cb1a8d2145932fb8afc4865f6990e51674c4e014930b370c2b3  26588
  rev2_r_bin 7b4caa77d2e67e6df14f5f1fecf0f75180d50338961b80e00073ec06883a395c 106770
  Binary sizes match the original lane record for b0/b1/b2/rev2
  (22331/34776/26588/106770).

## 5. Run matrix (15 runs)

- ./rev2_r_bin r (x3); ./b0_bin (x3); ./b1_bin (x3); ./b1t_bin (x3);
  ./b2_bin (x3).
- Per-run exit codes and wall times (run_times.txt):
  REV run1 exit=0 ms=5; run2 exit=0 ms=5; run3 exit=0 ms=5
  B0  run1 exit=0 ms=5; run2 exit=0 ms=3; run3 exit=0 ms=3
  B1  run1 exit=0 ms=4; run2 exit=0 ms=4; run3 exit=0 ms=6
  B1T run1 exit=0 ms=3; run2 exit=0 ms=3; run3 exit=0 ms=5
  B2  run1 exit=0 ms=3; run2 exit=0 ms=3; run3 exit=0 ms=5

## 6. Determinism evidence (K-SB5)

- `cmp` across run1/run2/run3 stdout per binary: all clean
  (REV 3/3 identical; B0 3/3; B1 3/3; B1T 3/3; B2 3/3).
- All 15 stderr files are 0 bytes.
- Stdout sha256 (run1, identical runs 2-3):
  REV d5eb722d8b0a204ce155e7d82f237fa6682d88d9d0d885b930629e1c69913801
  B0  c910b18728e5cd8c14da09ac49597700c2ea1c447c75a530976ad3b8b96ad2ab
  B1  0c5f9370256fcb37b3e92730fd44e8d98bb645c84fa8eefaba0d78ae844043c4
  B1T 3599e93a07f0e6bb3041e8a140bc446435f9910c74cebcedf59ca7f2b6a3afd5
  B2  ca3df82dd472f039db719c54adaabc867058ddb5b555c719fa146543cb528c7c
- Cross-lane check: the REV, B0, B1, and B2 run hashes are byte-identical
  to the original wave-20261001-1421pdt step-5 run transcripts
  (d5eb722d..., c910b187..., 0c5f9370..., ca3df82d... respectively).
  Rebuilt binaries reproduce the original frozen runs exactly.

## 7. Key measured outputs (grounding the per-bar scorecard)

- B0_run1.txt: "B0 PREDICT rab -> bbb" (3/3 identical).
- REV_run1.txt P8 section (lines 51-84):
  COUNTEREXAMPLE_DETECTED(rab)
  DIAGNOSIS pos=0 byte=114 conflicts=0
  PRIMITIVE-CONSTRUCTED pos=0 byte=114
  VERSION v3 ACTIVE (parent v2)
  PREDICT rab -> rrr [ok]
  PREDICT abc -> ccc [ok]
  PREDICT xy -> xx [ok]
  PREDICT defg -> gggg [ok]
  CHECK P8-F2-reuse-no-revision: PASS
  PREDICT rqw -> rrr [ok]
  Zero DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after the reuse
  check (lines 69-84 contain none; the only P9 entries are the frozen
  ablation ROLLBACK to v1, not a new revision).
  Tail: "=== RESULT fails=0 ===" / BUILD-PASS.
- B1_run1.txt: "B1 programs-evaluated: 1055", "B1 first-fit-index: -1".
- B1T_run1.txt: "B1T programs-evaluated: 39",
  "B1T first-fit-index: 38", "B1T fails-on-T: 0".
  (Index 38 matches the frozen v1 discovery index 38 [N C1 SUB].)
- B2_run1.txt: "B2 PREDICT rab -> rrr" (stored entry, correct),
  "B2 PREDICT rqw -> www" (mispredict: no stored entry for it).

## 8. revision_evals re-derivation (per the prereg formula)

Formula: diagnosis (p, byte) candidates ranked plus
primitive-construction byte-equality tests plus the single
SPECIALIZE application. For the P8-r revision (v2 to v3):

- Diagnosis candidates ranked: 3. Under v2 the failing set is the
  single record ("rab","rrr"); candidate positions 0,1,2 yield
  (0,114), (1,97), (2,98), all covering F, ranked position-ascending;
  the winner is emitted as "DIAGNOSIS pos=0 byte=114 conflicts=0"
  (frozen diagnose, proc_revise2.zag lines 380-478: candidates are the
  deduped (pos, byte) pairs covering all failing records, winner is
  minimum position then minimum byte).
- Primitive-construction byte-equality tests: 1. build_test constructs
  exactly one byte-equality test (0,114), emitted as
  "PRIMITIVE-CONSTRUCTED pos=0 byte=114".
- SPECIALIZE applications: 1 (v2 to v3), emitted as
  "VERSION v3 ACTIVE (parent v2)".
- revision_evals = 3 + 1 + 1 = 5.
- Supplementary disclosure (not in the prereg formula): the P8 alt
  search (frozen dsearch order over F alone) evaluated 3 programs
  (indices 0,1,2; first fit at index 2, C0 broadcast-first). Even
  5+3=8 is far below 1055.

## 9. Machine-greppable cost accounting

revision_evals=5
b1_enumerated=1055
b1_first_fit_index=-1
b1_wall_ms=4
b1t_wall_ms=3
revision_wall_ms=5
b0_wall_ms=5
b2_wall_ms=3
binary_bytes_rev2_r_bin=106770
binary_bytes_b0_bin=22331
binary_bytes_b1_bin=34776
binary_bytes_b1t_bin=34825
binary_bytes_b2_bin=26588
source_delta_lines=946
new_semantic_cases=0
new_modes=0
new_bridges=0

Notes: wall_ms values are run1 of each binary (same convention as the
original lane). source_delta_lines counts all baseline .zag lines
(b0 176 + b1 269 + b2 202 + b1t 299 = 946); 224 lines of b1t.zag are
byte-exact shared extracts of the frozen discovery machinery,
identical to b1.zag lines 1-224. No Section B revision-machinery code
is shared with any baseline.

## 10. Sealing protocol compliance

- The F1r-reuse input "rqw" is presented by the frozen binary only
  after VERSION v3 is ACTIVE (lines 62-69 of REV_run1.txt).
- Baselines share only the frozen benum algorithm (B1, B1T) and the
  frozen v1 procedure (B0, B2); no revision-machinery code is shared.
  Shared-code disclosed above and in the verdict doc; red team may
  audit b1t.zag and main_b1t.txt for leakage.
- Work dir was empty at lane start. No contamination.

## 11. Executables invoked (K-SB6 audit)

- Safebin PATH tools only: bash, awk, cat, cmp, cp, cut, date, diff,
  git, grep, head, mkdir, sha256sum, stat, tail, tee, timeout, touch,
  tr, uniq, wc, which, znc. No python3, python, gcc, cc, perl, ruby,
  or node invoked at any stage (implementation, build, run,
  analysis). `which python3` and `which python` return nothing under
  the safebin PATH.
- Byte scan of all lane text files (*.md, *.zag, *.txt): zero
  em-dash bytes and zero en-dash bytes. Compiler-emitted em-dash in
  znc lint text is confined to /tmp build logs (hashes in section 4).
