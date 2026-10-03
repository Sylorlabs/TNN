# REPRODUCTION LOG: DDES V2 steps 4+5

Wave: wave-20261002-0221pdt. Lane: DDES. Worker: depth 2/2, no children.
All commands run with PATH="$HOME/safebin" (36 tools, no python3/python).

## Step 0 (toolchain guard)

- setup_safebin.sh: SAFEBIN-READY, 36 tools, no python.
- `which python3`: nothing (exit 1). `which python`: nothing.
- `which znc`: /home/hatch/safebin/znc (abed8aa1, 2026.07.0-dev).
- Recorded in NAMECHECK.md before any other work.

## Provenance

- Source commit: 947675258 (wave-20261001-1721pdt wave record).
- f461e812d deleted the DDESv2 lane from the committed tree
  (mass deletion; that wave's GIT-HEALTH commit flags it).
- Working-copy lane dir is untracked; its five .zag sources
  sha256-match the 947675258 blobs exactly.
- Extraction: `git show 947675258:...` for each of the five
  .zag sources into this lane dir as src_*.zag; sha256 verified
  against the prereg pins (all five match; R-R1 source side PASS).
- Ablation diffs vs main: 2, 4, 2 changed (< / >) lines =
  1, 2, 1 changed lines, matching the frozen record.

## Prereg freeze

- PREREG_DDES_REPRO.md written, dash-scanned clean
  (check_no_dash.sh), committed ALONE at 7dc99b131 before any
  extraction/build/run. (One stale .git/index.lock from a
  concurrent worker's git add blocked the first two commit
  attempts; lock verified as held by a live git process, waited
  for it to clear, retried per the ref-lock rule.)

## Rebuild (plain znc, no instrumentation)

- znc src_ddesv2_s7.zag -o repro_s7_bin: exit 0, 93-byte stderr
- znc src_ddesv2_pre.zag -o repro_pre_bin: exit 0, 93-byte stderr
- znc src_abl_noclamp.zag -o repro_noclamp_bin: exit 0, 93-byte stderr
- znc src_abl_noguard.zag -o repro_noguard_bin: exit 0, 93-byte stderr
- znc src_abl_zerorecord.zag -o repro_zerorecord_bin: exit 0, 93-byte stderr
- 93 bytes = the unconditional zagd-availability warning, as frozen.

## R-R2 (byte-identical rebuild)

All five rebuilt binaries sha256-match the committed _bin blobs
at 947675258. MATCH on all five. No divergence.

## Runs (3/3 each, exit 0, zero stderr bytes every run)

- repro_s7_bin: 359531a8d94a6fa172597a7d448a14848cb09ba34a60985ed3e607a9a1260743 (matches frozen)
- repro_pre_bin: 3226c6f11660db13519f87daa08c92695ded91aa5b9416cede3a0f7ae6313c93 (matches frozen)
- repro_noclamp_bin: ac0ff81f359edae5b080cc2c8c14f13b296cf57cb97b187899c5f04e129bbcaa (matches frozen)
- repro_noguard_bin: dc2e239e81ee7454c741ead6f1f483a2e5abe04a22cbe2d741b76306dd5430b3 (matches frozen)
- repro_zerorecord_bin: d3c1d19c29ddf078be97caa9d24a90572fe2595a69f3c81d0f34d8a223afa360 (matches frozen)

R-R3 PASS (hash level), R-R5 PASS (determinism).

## K-R1..K-R9 re-verification from rebuilt transcripts

- K-R1: PASS (5/5 exit 0, 93-byte stderr).
- K-R2: PASS (pre: 0 FLAG, 2 CONVERGE-OK, PLAN [S,OY],
  ELIM h0 true in cfg0).
- K-R3: PASS (s7: 8 FLAG lines, 0 zero-wait plans).
- K-R4: PASS (1 NO-DISCRIMINATING-PLAN; J: CLASS-MISMATCH
  record=(1,2,0) world=(1,2,3), CONVERGE-FAIL, 0 EXEC, no
  RECORD-LOAD).
- K-R5: PASS (noclamp: FLAG + [S,OY] + ELIM h0 + CONVERGE-OK;
  noguard: 1 ABL-PROBE, 0 SCAFFOLD-VIOLATION, SCAFFOLD-CALLS 0;
  zerorecord: phase-B 5 CLASS-MISMATCH + 5 CONVERGE-FAIL,
  0 phase-B EXEC).
- K-R6: PASS (RECORD-LOAD-H byte-exact, REPLAN [S,W,OZ],
  truth survives both configs on sealed I).
- K-R7: PASS (RT1 2/2 CONVERGE-OK; RT2 2/2 PRED h0=1 h1=1,
  SURVIVE h0, SURVIVE h1, CONVERGE-FAIL).
- K-R8: PASS (pure Zag; dash scan clean; caveats restated
  verbatim; cost fields recorded; new_semantic_cases=0,
  new_modes=0, new_bridges=0; no commits outside lane; no push).
- K-R9: PASS (5 binaries x 3 runs byte-identical).

## Baseline (step 5)

- ddes_randbase.zag written after prereg commit, per frozen spec.
- Build: exit 0, 93-byte stderr (one analyzer warning about a
  placeholder assignment was fixed; final build has only the
  zagd warning).
- Simulator validated mechanically: 7/7 frozen EXEC real values
  reproduced (F 1/0, A 0/1, H 1/0, RT1 cfg0 1).
- Runs 3/3 byte-identical, exit 0, zero stderr:
  672a32f6f3d114a55c530e5cb265c6e6a04a85b78be723a3275e776e5cebb736
- Results: F CORRECT, A CORRECT, H CORRECT, K LOUD-FAIL,
  RT1 CORRECT, RT2 LOUD-FAIL; correct=4, loud_fail=2,
  candidates_evaluated=156; wall_ms 2/2/2; binary 17091 bytes.
- Per-world verdicts identical to the guided derivation on all
  6 worlds. Interpretation and self-red-team in
  BASELINE_COMPARISON.md.

## Verdict

BUILD-PASS (reproduction step). R-R1 through R-R5 all PASS.
No REPRODUCTION-FAIL: zero byte or verdict divergence from the
committed record. No SURVIVES claim; ceiling remains bounded L2
with persistence; the three binding caveats still bind every
citation.
