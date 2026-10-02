# RUN_LOG: CONTLEARN3 mechanism-proposal-first

Wave: wave-20261002-0221pdt. Lane: CONTLEARN.

## Commits

- Prereg freeze: 3bacc8903 (NAMECHECK.md + PREREG_CONTLEARN3.md, no
  implementation).
- Amendment 1: 29a11bd85 (STORE_OK / proposal-citation split;
  pre-implementation, no results seen). A ref-lock collision with another
  worker's commit delayed this commit by one retry; the retry committed
  only the lane pathspec.
- Implementation: this commit (see below).

## Builds (K1b)

znc_invocations_pf.log: exactly 2 entries, both before the runs, 0 new
during the 6 runs.
- `sh znc_wrap_pf.sh pf_combined_treat.zag -o pf_driver_treat` -> binary
  pf_driver_treat (warnings only, same analyzer class as prior waves).
- `sh znc_wrap_pf.sh pf_combined_control.zag -o pf_driver_control` ->
  binary pf_driver_control.

Source hashes (recorded):
- pf_core_control.zag:
  26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d
  (byte copy of the recorded nomain derivation; diff empty).
- pf_core_treat.zag:
  627af6eb0e88141fdeb00baba0aab178a29df128aa0250398355db42d8557f63
  (diff vs derivation: 2 lines removed, 60 added, 48 non-comment).
- pf_driver.zag:
  b9ab9953672880546dd4067c6c6ff82e76d863ddde0e9531c44ef287323a25a9.
- pf_combined_treat.zag:
  6835b23da95abd2d4ff2ac3047ea1bd797daee3c36ce65d454139d9ee4cfad86.
- pf_combined_control.zag:
  d94539b6b2f9aa797fd58aafc86827fb88dbae2da747c180413ad50563035a88.

## Runs (K1a/K1c/CP-5)

run_pf.sh: 6 processes (TREAT x3, CONTROL x3), one process per 76-event
run, empty argv, empty environment. All rc=0. harness_pf.log:
total_spawns=6, TREAT 3, CONTROL 3, pid_leak_check=0,
znc_invocations_during_runs=2. All 6 stderr files 0 bytes.

Transcript SHA-256:
- TREAT r1/r2/r3:
  1067bd5e51da07e6be9412539a8e430c26465c720de54a65919b3752158e621f.
- CONTROL r1/r2/r3:
  eac3f4246bcbf84300bd5fc435675957e5bdf79ba3f20a066877c1170abd6995.
FNV: TREAT -1094991477 x3; CONTROL -621112903 x3. AUDIT_PASS x6.

Ordering check (CP-1, shell): on all 3 TREAT reps, for each of the 6
novel (s,r) pairs the PROPOSAL trace line precedes the MACHINERY line and
the prop node ids match; 6 PROPOSAL lines, 6 MACHINERY lines,
0 MACHINERY_SKIPPED lines. CONTROL: 0 PROPOSAL lines.

## K3 note (lesson for future workers)

The committed 2321pdt lo_driver reads its run mode from /dev/stdin
(cl_driver.zag: `_zag_read_file("/dev/stdin")`; "TREAT" selects mode 1).
Running it with the harness's inherited stdin blocks forever on
anon_pipe_read; with </dev/null it prints MODE_FAIL and exits 1. The
correct invocation is `printf 'TREAT' | bash -c "exec -c ./lo_driver"`.
With that input: 3/3 rc=0, stdout SHA-256
1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9,
0 stderr bytes. K3 PASS.
