# NAMECHECK: CONTLEARN-LH (continuing learner, longer-horizon delayed reuse)

Wave: wave-20261002-0221pdt. Lane: CONTLEARN-LH. Working copy:
~/workspace/tnn-rsi, branch tnn-native-lab. Lane dir:
docs/lab/rsi/runs/wave-20261002-0221pdt/CONTLEARN-LH/.
Worker phase log. Only hyphens are used in this file; no em or en dashes.

## Step 0: worker toolchain guard (completed before any other work)

- Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`;
  output: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`,
  `verify: python3 absent from safebin PATH (OK)`,
  `verify: python absent from safebin PATH (OK)`.
- `which python3` under `PATH=$HOME/safebin` returns nothing
  (exit 1, empty output). Recorded in the setup log above.
- Every shell in this lane runs with `export PATH="$HOME/safebin"`.
- Research logic is pure Zag; shell is used only to invoke znc, run the
  compiled binaries, move/copy files, and run git. No Python, C, JS, or
  Rust anywhere in verifiers, scorers, harnesses, or analysis.
- Forbidden-executable invocation would be automatic PROCESS-FAIL and
  would be disclosed immediately in RUN_LOG.md; none has occurred.

## Step 1: id and subject freshness (pre-prereg)

New subject/object/relation ranges for this lane, checked unused by any
prior battery in wave-20261001 and wave-20261002 sources (grep -w over
*.zag in tnn2_build, wave-20261001, wave-20261002-0221pdt: 0 files each):
- relations 561, 562 (unrelated-domain interference facts);
  relations 581, 582, 583 (late-novel chains: concept, anchor, novel query);
- subjects 31001..31361, objects 32001..32361 (interference episodes);
- objects 22101..22104 (contradictory chain-fact values),
  22111..22114 (resolved chain-fact values);
- subjects 41001..41002, 43001..43002, objects 42001..42002
  (late-novel chains).
Ranges overlap none of the CONTLEARN3 ranges
(21001..23006, 24001..25006, 26001, 27001..27003, 28001..29024;
relations 511, 521, 522, 531, 541, 551). A broader range regex over
3[12]xxx, 41xxx, 42xxx, 43xxx, 2210x, 2211x returned only two false
positives: the frozen core's edge-offset constant 41024 (field-offset
arithmetic, not a subject id) and allocation-size constants 32768. No
battery script uses any id in the LH ranges.

## Step 2: reuse of frozen instruments

- Frozen core: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag,
  SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd.
- Recorded nomain derivation (CONTLEARN lane, verified again before any
  build; never written): SHA-256
  26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d.
- TREAT core: byte copy of CONTLEARN's pf_core_treat.zag (the proposal-gate
  instrument; SHA-256 627af6eb0e88141fdeb00baba0aab178a29df128aa0250398355db42d8557f63);
  verified by hash before any build. The instrument is unchanged: this lane
  tests it over a longer horizon, it does not modify it.
- CONTROL core: byte copy of CONTLEARN's pf_core_control.zag
  (SHA-256 26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d,
  the recorded nomain derivation itself).
- K3 instrument: the committed 2321pdt lo_driver binary, re-run read-only;
  feed "TREAT" on stdin (lesson recorded in CONTLEARN/RUN_LOG.md).

## Step 3: lane-local files (this dir only)

NAMECHECK.md (this file), PREREG_CONTLEARN_LH.md (frozen alone first),
lh_core_treat.zag, lh_core_control.zag (byte copies above),
lh_driver.zag (extended 358-event script), lh_combined_*.zag,
lh_driver_treat, lh_driver_control (built binaries), znc_wrap_lh.sh,
znc_invocations_lh.log, run_lh.sh, transcripts, SEALED_EVAL.md,
REDTEAM_SELF.md, VERDICT_CONTLEARN_LH.md, RUN_LOG.md.

## Step 4: commit log (this lane only)

- Prereg freeze: 8d43c6e55 (NAMECHECK.md + PREREG_CONTLEARN_LH.md, no
  implementation).
- Amendment 1: 32bfea311 (pre-implementation event-count correction
  358 to 356; no design change).
- Implementation + sealed results: recorded in RUN_LOG.md (this commit).
