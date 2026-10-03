# REPORT.md - lane BATTERY, wave-20261002-1121pdt (queue item 13)

Task: run the T-K5, T-K9, T-K11 REGRESSION BARS against the current
tnn-native-lab tip, pure Zag, each bar twice, byte-identical reruns.

## Tip tested

- Lane branch: lane-battery-20261002-1121pdt @
  0296167f0c05e4beca98fb3dfdc9a5e9fa1e1e84
- tnn-native-lab tip at run time: 05d1b7a281248dd5281ef4a336a9444b17fdcc95
- Test subject: the frozen TNN-2 shim
  docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin,
  SHA-256 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954,
  verified before every run (T-K3 holds at both tips). Tracked file,
  `git status` clean on the shim directory.

## Method

Copied the frozen battery inputs (world files, barspecs, drivers,
scorers, PI files, manifest) from
docs/lab/rsi/runs/wave-20261002-0521pdt/BATTERY into this lane's
run/ scratch directory. All copies hash-verified against the
frozen WORLD_MANIFEST.sha256. The ONLY edit to any copied file was
the mechanical DIR= relocation in the e10_m2_driver.sh copy; the
shim path, sealed PIs (PI_W1=1 PI_W2=0 PI_W3A=1 PI_W3B=1), world
contents, and barspecs are untouched. No Python anywhere: shell
glue plus the frozen pure-Zag scorer binaries under PATH=$HOME/safebin.

Each bar ran twice (pass A, pass B). All run artifacts SHA-compared
A vs B and against the frozen 0521pdt run1 artifacts.

## Verdicts

### T-K5 (M1-E10-W1 nesting; PASS iff HIT probes 0,1 and >=1 of probes 2,3)

RESULT: FAIL (exit 1). Score detail, identical both passes:
- PROBE 0 (60101,60509) exp 3 got 3 PASS
- PROBE 1 (60102,60509) exp 2 got 2 PASS
- PROBE 2 (60105,60509) exp 15 got -2 FAIL
- PROBE 3 (60106,60509) exp 9 got -2 FAIL
- HIT -> PASS; NEED 1 got 0/2 -> FAIL; LEAKCHECK clean; E10BAR FAIL

Assessment: STANDING FAILURE, not a regression. Verbatim match to
the frozen 0521pdt verdict (SEALED_EVAL.md: engagement 2/2 PASS,
nesting 0/2 FAIL). Transcripts byte-identical to frozen
m1w1_trans_run1.txt.

### T-K9 (M2-E10-W2 budget; PASS iff (a)>=1 non-NULL hidden ACT,
(b) non-NULL hidden ACTs <= 6, (c) >=3/4 final probes correct,
(d) >=2 keys stopped early, (e) vocab-verify ok)

RESULT: FAIL (exit 1). Score detail, identical both passes:
- vocab-verify ok=1 PASS (NULL_ACT=0, INQ_ACT=30, measured in situ)
- (a) nonnull hid acts=12 PASS
- (b) nonnull hid acts=12 need<=6 -> FAIL
- (c) final=0/4 need>=3 -> FAIL
- (d) early keys=0 need>=2 -> FAIL
- (e) vocab-verify PASS; collateral 2/2; E10BAR FAIL

Assessment: STANDING FAILURE, not a regression. Verbatim match to
the frozen 0521pdt verdict. All 10 m2w1/m2w2 artifacts (worlds,
transcripts, logs, truths, vocab files) byte-identical to frozen
run1 artifacts.

### T-K11 (M3-E10-W1 orphan poisoning; PASS iff HIT probes 0,1,2
and probe 3 == 65113)

RESULT: FAIL (exit 1). Score detail, identical both passes:
- PROBE 0 (65101,65509) 65103 PASS
- PROBE 1 (65101,65509) 65103 PASS
- PROBE 2 (65101,65519) 65104 PASS
- PROBE 3 (65101,65509) exp 65113 got 65103 FAIL
- PROBE 4 (65801,65800) 65811 PASS; PROBE 5 (65802,65800) 65812 PASS
- HIT -> PASS; NEED 1 got 0/1 -> FAIL; LEAKCHECK clean; E10BAR FAIL

Assessment: STANDING FAILURE, not a regression. Verbatim match to
the frozen 0521pdt verdict. Transcripts byte-identical to frozen
m3w1_trans_run1.txt.

## Determinism record

- Every artifact (transcripts, grown M2 worlds, driver logs, vocab,
  truths files) byte-identical between pass A and pass B. No
  divergence; no run voided.
- Every artifact additionally byte-identical to the frozen
  0521pdt run1 artifacts. The current tip's shim reproduces the
  frozen behavior exactly.

## Integrity checks

- T-K3 (shim hash) PASS at every invocation point.
- Scorer binaries re-verified: rebuilt e10_score.zag and
  e10_score_m2w2.zag from committed sources with the pinned znc;
  rebuilt binaries produce byte-identical scoring output to the
  committed _bin files on this run's transcripts. Frozen scorer
  chain is sound.
- Bar definitions not moved: frozen barspec files and frozen
  PREREG_E10.md section 7 semantics used as-is. The nullval/inqval
  args passed to the scorers (0, 30) are inert for the m1/m3
  barspecs (no CHOICE directives) and match the measured in-situ
  vocab for T-K9.
- Toolchain guard: `which python3` resolves to NOTHING,
  `which znc` = /home/hatch/safebin/znc, recorded in NAMECHECK.md.
  No forbidden-interpreter invocation; this lane is not
  PROCESS-FAIL.
- Prereg commit-order self-check: this lane makes no new claims
  and proposes no adoption; the frozen prereg PREREG_E10.md
  predates all battery artifacts (0521pdt SEALED_RESULTS.md
  section 1). Nothing to self-check against.

## Red-team findings (self)

1. Relocation risk: the single DIR= edit could not have changed
   semantics, proven by byte-identity with the frozen transcripts.
2. Stale-binary risk: ruled out by rebuilding both scorers from
   committed sources; outputs identical.
3. Weakened-bar risk: none. Frozen barspecs, frozen worlds,
   frozen PIs, frozen shim, frozen scorers. The exact failing
   assertions match the frozen record assertion-for-assertion.
4. Tip-drift risk: tnn-native-lab moved during the run
   (d1dc6948e -> 05d1b7a28 at coordinator level). Irrelevant to
   these bars: the test subject is the frozen shim, whose hash and
   byte-identical behavior are verified at both tips.

## Keep/discard

No adoption proposed. All three bars remain standing failures at
the current tip, exactly as frozen. They continue to define
targeted-repair scope for TNN-3 work and must not be weakened to
force passes.

## Queued next

Nothing queued in this lane. Recommendation to the coordinator:
treat T-K5/T-K9/T-K11 as confirmed standing failures; any lane
claiming to repair one must re-run this battery in the same
harness and show byte-identical reruns plus the frozen verdict
comparison.
