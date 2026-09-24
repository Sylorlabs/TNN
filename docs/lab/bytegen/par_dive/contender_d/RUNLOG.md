# Contender D — RUNLOG (reproducibility)

Date: 2026-09-24. Pinned toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Zero RNG in every binary and every script.

## Build

```
$ZNC build src/render_d1.zag -o src/render_d1
$ZNC build src/render_d2.zag -o src/render_d2
```
Both succeed (inherited A0107 dead-loop analyzer warnings in copied IO loops;
builds unaffected). Final source SHAs in `results/sources.sha256`.
Binaries are build artifacts: never committed.

## Battery

`tests/run_battery.sh` — rebuilds both, renders references with
`~/workspace/bytegen/fork_par/src/render_par`, then per scheme:
clean render → `cmp` vs PAR (mix + wav) → 3 rerenders + `sha256sum` →
`gate_bin` → CHOP with `tests/events_full.txt` → `tests/coherence_full.py` →
cost (`time`, falls back to bash builtin) → RT-LONG (+near-miss/multi for D2)
→ RT-CASCADE (`tests/postcut_diff.py`) → RT-EDGE (frozen + D1 15 s extension)
→ order permutation → D2 sustained corruption.
Log: `runs/battery.log` (rc=0). Per-leg outputs in `results/`.

Manual additions after the battery (all deterministic, rerun-safe):
- `tests/coherence_full.py` fixed twice (zero-variance corr; plan-derived IOI).
- `tests/postcut_diff.py` fixed (cut-sample bucketing).
- D1 `seq+susfaultmix` mode added (src edit), rebuilt, re-verified:
  D1-C1 (`cmp` vs PAR mix), D1-C4 (seq==rev), determinism.
- Interleaved COST: `results/cost_interleaved.txt` (9 runs, `date +%s.%N`).
- Adversarial plans `plans/plan_adv_*.txt` (5 runs, `timeout`-guarded).
- Formation prototype `formation/expand_motif.py`.
- Excerpts in `excerpts/` (see RESULTS.md).

## Key rerun commands

```
./src/render_d1 ~/workspace/bytegen/fixture/plan_v1.txt out.wav seq
./src/render_d1 plans/plan_edge_midnote.txt out.wav seq 15        # extension
./src/render_d1 plans/plan_edge_midnote.txt out.wav seq 15 nofade # control
./src/render_d2 tests_plan_long.txt out.wav seq                   # latch trace on stderr
python3 tests/coherence_full.py <wav>
python3 tests/postcut_diff.py <clean.mix> <fault.mix> 3.0015
```

## Provenance of reference numbers

- PAR baseline (9/9 bars, recurrence 1.0, ~9.7 s): `~/workspace/bytegen/FINDINGS.md`
  (observed 2026-09-24, not re-measured here except where `cmp`-compared).
- Hybrid v2 latch + 76.7c near-miss abstain: `~/workspace/bytegen/hybrid/results/RESULTS.md`.
- Frozen plans: `~/workspace/bytegen/tests/plan_long.txt`,
  `plan_edge_cut.txt`; `~/workspace/bytegen/hybrid/tests/plan_long_multi.txt`.
- Gate binary: `~/workspace/bytegen/tests/gate_bin`; CHOP: `~/workspace/aud_v10/chop.py`.
