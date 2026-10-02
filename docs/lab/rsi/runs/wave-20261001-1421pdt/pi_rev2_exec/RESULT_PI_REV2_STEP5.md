# RESULT: H-PI-REV2 step 5 simple-baseline comparison (wave-20261001-1421pdt)

Lane: H-PI-REV2 step 5 of the 11-step frontier pipeline (baseline
comparison for the F3a3 BUILD-PASS mechanism).
Frozen prereg:
docs/lab/rsi/runs/wave-20261001-1121pdt/pi_rev2/PREREG_PI_REV2_STEP5_BASELINE.md
(tracked via git ls-files; committed writing-only before any
implementation). Work dir was empty at lane start: NOT CONTAMINATED.
No git commits made by this worker; all files left uncommitted.

## Execution summary

- Mechanism under test: proc_revise2.zag, working-tree sha256
  dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12,
  matching the committed blob at 847a8f10f (git status clean). Built
  with the pinned znc as rev2_r_bin.
- Adversary byte: 'r' (114), the last letter of the frozen set {k,m,r}
  per the ADVERSARY_BYTE_SET4.md selection rule. The frozen binary's P8
  gate (allowed set "ijklmnortuvw") accepts 'r'; the P8 phase ran and
  emitted COUNTEREXAMPLE_DETECTED(rab).
- Baselines B0, B1, B2 implemented in pure Zag (b0.zag, b1.zag, b2.zag;
  shared code disclosed below). Built with the pinned znc; all builds
  exit 0.
- Comparison protocol: revision binary with argv[1]="r" x3; each
  baseline x3. 12 runs total, all exit 0.

## Machine-greppable cost accounting

revision_evals=5
b1_enumerated=1055
b1_first_fit_index=-1
b1_wall_ms=12
revision_wall_ms=43
binary_bytes_rev2_r_bin=106770
binary_bytes_b0_bin=22331
binary_bytes_b1_bin=34776
binary_bytes_b2_bin=26588
source_delta_lines=647
source_new_lines=150
new_semantic_cases=0
new_modes=0
new_bridges=0

Wall-clock detail (ms per run; run1 values used for the ms fields):
rev 43/38/39; b0 15/20/13; b1 12/28/22; b2 20/41/24.
source_delta_lines counts all baseline .zag lines (647); source_new_lines
counts headers plus mains (150); the remainder is byte-exact shared
extracts of the frozen discovery machinery (disclosed below).

Derivation of revision_evals=5 (prereg formula: diagnosis (p,byte)
candidates ranked plus primitive-construction byte-equality tests plus
the single SPECIALIZE application), for the P8-r revision (v2 to v3):

- Diagnosis candidates ranked: 3. Under v2 the failing set is the single
  record ("rab","rrr"); candidate positions 0,1,2 yield (0,114),
  (1,97), (2,98), all covering F, ranked position-ascending; the winner
  is emitted as "DIAGNOSIS pos=0 byte=114 conflicts=0".
- Primitive-construction byte-equality tests: 1. build_test constructs
  exactly one byte-equality test (0,114), emitted as
  "PRIMITIVE-CONSTRUCTED pos=0 byte=114".
- SPECIALIZE applications: 1 (v2 to v3), emitted as
  "VERSION v3 ACTIVE (parent v2)".
- Supplementary disclosure (not in the prereg formula): the P8 alt
  search (frozen dsearch order over F alone) evaluated 3 programs
  (indices 0,1,2; first fit at index 2, C0 broadcast-first). Even
  5+3=8 is far below 1055.

## Per-bar scorecard

- K-SB1 (problem real): PASS. B0 output (3/3 byte-identical):
  "B0 PREDICT rab -> bbb". The kill needed B0 to predict "rrr"; it
  predicts "bbb", so the revision problem is real.
- K-SB2 (revision cheaper than re-search): PASS. 5 < 1055 strictly.
  B1 evaluated all 1055 programs ("B1 programs-evaluated: 1055") without
  a full fit; the revision used 5 candidate evaluations and succeeded.
- K-SB3 (revision beats storage on reuse): PASS. The revised procedure
  predicts "PREDICT rqw -> rrr [ok]" with "CHECK P8-F2-reuse-no-revision:
  PASS"; zero DIAGNOSIS, PRIMITIVE-CONSTRUCTED, or VERSION lines occur
  after the reuse check (transcript lines 68-84). B2 predicts
  "B2 PREDICT rqw -> www" (mispredict: no stored entry, v1 fallback
  broadcast-last) while "B2 PREDICT rab -> rrr" (stored entry, correct).
- K-SB4 (correctness parity): FAIL. The revised procedure is correct on
  all required inputs: "abc"->"ccc", "xy"->"xx" (updated expectation per
  the frozen conflict rule), "defg"->"gggg", "rab"->"rrr",
  "rqw"->"rrr", R cell 8/8, "=== RESULT fails=0 ===", BUILD-PASS. But
  B1 reports "B1 first-fit-index: -1": all 1055 programs evaluated,
  none fits T+F1r. This is provably impossible in the benum program
  space: output position (k=0,n=3) requires eval=2 from "abc"->"ccc"
  and eval=0 from "rab"->"rrr" simultaneously. B1 therefore produces no
  fitted program, so the bar's requirement "B1's fitted program is
  correct on T+F1r" is unsatisfiable as written. Kill evidence: B1 run
  transcript (0c5f9370..., 3/3 identical) showing programs-evaluated
  1055 and first-fit-index -1. This is a design flaw in the frozen
  step-5 prereg (it presupposes a B1 fit that the inherited K-RV2-1b
  impossibility result rules out), not a defect in the revision
  machinery, which met every behavioral requirement placed on it.
- K-SB5 (determinism): PASS. 12/12 runs exit 0. Stdout sha256 per
  binary, 3/3 identical (cmp clean): REV
  d5eb722d8b0a204ce155e7d82f237fa6682d88d9d0d885b930629e1c69913801;
  B0 c910b18728e5cd8c14da09ac49597700c2ea1c447c75a530976ad3b8b96ad2ab;
  B1 0c5f9370256fcb37b3e92730fd44e8d98bb645c84fa8eefaba0d78ae844043c4;
  B2 ca3df82dd472f039db719c54adaabc867058ddb5b555c719fa146543cb528c7c.
  All 12 stderr files are 0 bytes.
- K-SB6 (purity and docs): PASS. Pure Zag only: implementation, build,
  run, and analysis used shell orchestration via safebin tools only; no
  python3, python, perl, ruby, or node was invoked at any stage
  (executables used: bash plus safebin awk, cat, cmp, date, git, grep,
  mv, sed, sha256sum, stat, tee, wc, znc). Zero em-dash and zero
  en-dash bytes in all lane files (byte scan clean). Note: znc's own
  A0102 lint text contains a compiler-emitted em-dash, so the raw build
  logs were moved to /tmp (hashes recorded below) to keep the lane
  byte-clean; this changes no evidence, only the location of a
  tool-emitted log.

Build log hashes (/tmp): build_b0/b1/b2.err
d5937fe2f12d87d239a58a30ad4c1de9c10215e3dfa234062d662d6e87e29df4;
build_rev.err
abc082619c40608821d09eb94db89af2d5346c77b6335e1ce1c2cb9f3fbac4a5.
Build diagnostics were only the environmental zagd warning and the
pre-existing A0102 lint on an ignored loadseq return at line 607,
identical to the lint recorded in RESULT_F3A3.md for the original
build.

## Shared-code disclosure (sealing protocol)

Baselines share byte-exact sed extracts of the frozen Section A
discovery machinery from proc_revise2.zag at 847a8f10f: helpers
(lines 22-43), eval (lines 44-93; b0 and b2 use 44-64), program store
(lines 95-141), benum (lines 179-225), sequence staging (lines 228-268,
b1 only). No Section B revision-machinery code is shared: no observe,
diagnose, build_test, specialize, branch predict, or rollback. New code
(150 lines: hdr_*.txt and main_*.txt): the three mains and the
b2_predict exception-table lookup. B1's instrumented first-fit scan
mirrors the frozen dsearch order exactly and adds only an evaluation
counter.

## Honest boundaries

Bounded L2 ceiling per the prereg: the revision machinery repairs a
supplied procedure after a counterexample; nothing here is evidence
toward L3 and must not be claimed as such. No protected-core changes
(new_semantic_cases=0, new_modes=0, new_bridges=0). Sealing held: the
F1r-reuse input "rqw" is presented by the frozen binary only after
VERSION v3 is ACTIVE.

## Provenance

Prior records consulted: PREREG_PI_REV2.md (wave-20260929-1721pdt
design lane), RESULT_PI_REV2.md and proc_revise2.zag
(wave-20260929-2321pdt), PREREG_PI_REV2_F3a3.md
(wave-20260930-1121pdt), REPRO_F3A3_STEP4.md (wave-20260930-2321pdt),
ADVERSARY_BYTE_SET4.md (wave-20261001-0221pdt), the frozen step-5
prereg (wave-20261001-1121pdt).

## Verdict

BASELINE-FAIL. Failing bar: K-SB4 (B1 cannot fit T+F1r; no fitted
program exists, so correctness parity is unsatisfiable as the frozen
prereg wrote it). All other bars hold: K-SB1 PASS, K-SB2 PASS (5 <
1055), K-SB3 PASS, K-SB5 PASS, K-SB6 PASS. The revision machinery met
every behavioral requirement (correct revision on first execution,
within-class reuse with zero new revisions, far cheaper than exhaustive
re-search); the failure lies in the frozen baseline design, which needs
a transparent amendment and re-freeze, not a patch around the result.

No em-dashes in this documentation.
