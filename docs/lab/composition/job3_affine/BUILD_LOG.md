# Job-3 build & run log

Date: 2026-09-27. Operator: Job-3 crew (subagent). All commands below were
run verbatim; outputs are committed alongside.

## Toolchain

- `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Source: `affine_test.zag` (pure Zag, zero RNG; SHA-256
  `e358cb59c4285cdd915f9f31b999cdff3007271c5623753896fb0ec4a5755c6c`)

## Compile

```
cd ~/workspace/composition_followup/job3_affine
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 affine_test.zag -o affine_test
```

Result: success. Six warnings, all "ignored return value" on `_zag_print`
calls (cosmetic; prints still emitted — verified by non-empty outputs).
No errors.

## Runs (determinism pair)

```
mkdir -p runs/run1 runs/run2
for m in genA genB genC memA memB memC; do ./affine_test $m > runs/run1/$m.out; echo "$m rc=$?"; done
for m in genA genB genC memA memB memC; do ./affine_test $m > runs/run2/$m.out; echo "$m rc=$?"; done
```

All 12 invocations returned rc=0. `diff -r runs/run1 runs/run2` → no
differences; SHA-256 manifest confirms all 6 output pairs byte-identical
(see SHA_MANIFEST.txt).

## Scoring

```
python3 score_job3.py runs/run1 scored
```

45/45 bar checks PASS (see scored/SCORES_JOB3.md). Exit 0.

## Red team

```
cd redteam && python3 rt_attacks.py > rt_output.txt 2>&1
```

rc=0. Six attacks, all green (see redteam/REDTEAM_REPORT.md).

## Notes

- The compiled binary `affine_test` and any `.zagd` cache are build
  artifacts: present in scratch, deliberately NOT committed.
- Prototype scripts (`scratch/gen3.py`, `scratch/mem3.py`,
  `scratch/xcheck.py`) are builder working files; the committed source of
  record is `affine_test.zag`, and the independent red-team code is
  `redteam/rt_attacks.py`.
