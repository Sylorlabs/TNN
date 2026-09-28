# F2 DELIBERATIVE

Two-pass perception fork: declared-sampling pass 1 (bit-exact F1) +
goal-directed re-sense pass 2 with changed evidence only, under a hard
acquisition budget and op deadline, with interrupt-only background scan,
install-time verification for high-stake installs, and provisional-flagged
fallback (never refusal).

## Layout

- `src/fio.zag` — file I/O, LE accessors, `z_i64a` scratch allocator.
- `src/f1.zag` — bit-exact Zag port of frozen F1 (`ref_f1.py`).
- `src/f2.zag` — the deliberative driver (ledger, background, triggers,
  selectors, adjudication, verification, install).
- `src/t1.zag` — bit-exactness driver (diff against `ref_f1.py`).
- `src/run_battery.sh` — run all 26 fixtures: `run_battery.sh <outdir> [opcap]`.
- `src/score.py` — score a run dir against `.truth` + F1 baseline.
- `src/R33_NATIVE_IO_V1.zag`, `src/R33_NATIVE_SHA256_V2.zag` — native support.
- `evidence/batt1/` — main battery (opcap=100000), 26 verdicts + 26 ledgers.
- `evidence/batt_tight30/`, `evidence/batt_tight50/` — high-rate leg.
- `DESIGN_NOTES.md`, `RUNLOG.md` — design and measured results.

Build (from `src/`, per znc @import rules — imports are cwd-relative):

```
export TMPDIR=~/workspace/tmp_commit
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 f2.zag -o f2_bin --no-analyze
```

Run one trial:

```
./f2_bin <fixture> <out_prefix> [opcap]
# writes <out_prefix>.verdict and <out_prefix>.ledger
```

## Frozen inputs (not amended)

- `conscious_perception/preregs/PREREG_FORKS.md`
- `conscious_perception/debates/SYNTHESIS.md`
- Shared fixtures in `conscious_perception/fixtures/` (consumed, never written).
