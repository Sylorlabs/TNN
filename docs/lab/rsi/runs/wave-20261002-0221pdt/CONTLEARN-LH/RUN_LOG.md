# RUN_LOG: CONTLEARN-LH longer-horizon delayed reuse

Wave: wave-20261002-0221pdt. Lane: CONTLEARN-LH.

## Commits

- Prereg freeze: 8d43c6e55 (NAMECHECK.md + PREREG_CONTLEARN_LH.md, no
  implementation).
- Amendment 1: 32bfea311 (pre-implementation, no results seen: total
  event count corrected 358 to 356; per-phase sum is 356; no phase,
  tuple, bar, or decision-rule change). The worker caught its own
  arithmetic error while writing the driver, before any build.
- Implementation: this commit (see below).

## Builds (K1b)

znc_invocations_lh.log: exactly 2 entries, both before the runs, 0 new
during the 6 runs.
- `sh znc_wrap_lh.sh lh_combined_treat.zag -o lh_driver_treat` -> binary
  lh_driver_treat (warnings only, same analyzer class as prior waves).
- `sh znc_wrap_lh.sh lh_combined_control.zag -o lh_driver_control` ->
  binary lh_driver_control.

Source hashes (recorded):
- lh_core_treat.zag:
  627af6eb0e88141fdeb00baba0aab178a29df128aa0250398355db42d8557f63
  (byte copy of CONTLEARN pf_core_treat.zag; 0-line delta).
- lh_core_control.zag:
  26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d
  (byte copy of the recorded nomain derivation; 0-line delta).
- lh_driver.zag:
  ec7f059b6aef72275bba124be7e3e9c4d70aad632f3cc4eeb01d6364c69a8926.
- lh_combined_treat.zag:
  b172b98796d51b2c9bca7d00a16ce4ea4e8946d658381d1516ae69e9ee57c9da.
- lh_combined_control.zag:
  b41ca7be51521bb63ebf10cc50c3cc0e6fa248ec17fe726ab09fd797239c536a.
- Frozen tnn2.zag verified a29972ca... before the builds and after the
  runs; the frozen path was never written.

## Runs (K1a/K1c/CP-LH5)

run_lh.sh: 6 processes (TREAT x3, CONTROL x3), one process per 356-event
run, empty argv, empty environment. All rc=0. harness_lh.log:
total_spawns=6, TREAT 3, CONTROL 3, pid_leak_check=0,
znc_invocations_during_runs=2. All 6 stderr files 0 bytes.

Transcript SHA-256:
- TREAT r1/r2/r3:
  644ba03f719c185f3de04445880df0a6fcacec7c3391b2198d545b6d4d2a803d.
- CONTROL r1/r2/r3:
  3ac5697ab195b5253610b416e4bc6fd04c76cf938678e6b23062781491dd94ef.
FNV: TREAT -1320742499 x3; CONTROL 1020256801 x3. AUDIT_PASS x6 (356).

Ordering check (CP-LH1, shell): on all 3 TREAT reps, for each of the 8
novel (s,r) pairs (6 NOVEL + 2 LATE-NOVEL) the PROPOSAL occurrence
precedes its MACHINERY line with matching prop node ids; 8 PROPOSAL
occurrences, 8 MACHINERY lines, 0 MACHINERY_SKIPPED. CONTROL: 0
PROPOSAL occurrences. (Note: the PROPOSAL trace is glued to the EV line
with no separating newline, so the check matches occurrences, not
line-anchored `^PROPOSAL`.)

Result lines (identical on all 3 reps per mode):
- TREAT: STORE_OK 6/6, STORE_PROP_CITE 6/6, CONFLICT1/2/3_OK 1/1,
  CORRECT1/2/3_OK 1/1, RETENTION_OK 12/12, REUSE_A 12/12, REUSE_B 10/12,
  REUSE_C 8/12, LATE_STORE_OK 2/2, LATE_PROP_CITE 2/2, LATE_OK 2/2,
  PROPC_FINAL 8, UNCERT 0.
- CONTROL: same except STORE_PROP_CITE 0/6, LATE_PROP_CITE 0/2,
  PROPC_FINAL 0.

## Post-hoc diagnostic (not part of the sealed 6)

One extra read-only run in /tmp (identical 356-event script via a
diagnostic driver copy with an end-of-run dump appended; sealed
transcripts untouched) established the CP-LH3 mechanism: conflicted
chains have two integrated facts (original superseded, contradictory
value live); no integrated fact holds the resolved value; MAP DEP
citations intact on all chains. See SEALED_EVAL.md.

## K3

Committed 2321pdt lo_driver re-run 3x read-only with `printf 'TREAT'`
on stdin (CONTLEARN/RUN_LOG.md lesson): 3/3 rc=0, stdout SHA-256
1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9,
0 stderr bytes. PASS.

## Toolchain self-disclosure

During diagnostic setup the worker typed a stray `python3 -c` probe
inside a shell command. Under the safebin PATH `python3` does not
resolve (Step 0 verified); the probe printed nothing and no Python
process ran. No forbidden executable was invoked; no research logic
touched Python at any point. Recorded here for completeness.

## Dash scan

docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
run over all lane .md files: clean.
