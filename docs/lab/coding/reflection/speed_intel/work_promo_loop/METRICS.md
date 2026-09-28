# P1/P2/P3 loop promotion — run metrics (2026-09-22)

Battery: `coding/reflection/speed_intel/work_a1/battery_si.json` (FROZEN 2026-09-22;
20 items: 18 fixable + X3/X4 unfixable). Pinned znc:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

`pass` below counts full passes; honest halts are X3→`halt-genfail`,
X4→`halt-no-patch` in every run. Canonical digest = sha256 of the
timing-free canonical log (drops ms/time_s/compile_ms/test_ms/diag_ms).

## Quality / cost table

| run | condition | budget | pass | halts | iters | znc | hyp-evals | wall (Σtime_s) | canonical digest |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_r1 | pre-port mainline, classic, no precheck | 6 | 18/18 | 2/2 | 46 | 45 | 129 | 65.8s | 72468b38a464856c… |
| ctrl_r2 | same | 6 | 18/18 | 2/2 | 46 | 45 | 129 | 68.7s | 72468b38a464856c… |
| ctrl_r3 | same | 6 | 18/18 | 2/2 | 46 | 45 | 129 | 55.5s | 72468b38a464856c… |
| new_r1 | NEW defaults (combo+precheck) | 4 | 18/18 | 2/2 | 46 | 28 | 45 | 52.5s | 6e6ee2caea39f8648… |
| new_r2 | NEW defaults (combo+precheck) | 4 | 18/18 | 2/2 | 46 | 28 | 45 | 47.8s | 6e6ee2caea39f8648… |
| new_r3 | NEW defaults (combo+precheck) | 4 | 18/18 | 2/2 | 46 | 28 | 45 | 51.4s | 6e6ee2caea39f8648… |
| classic_r1 | post-port, `--budget 6 --no-precheck --mask classic` | 6 | 18/18 | 2/2 | 46 | 45 | 129 | 77.7s | dbab58208e3fbb79… |

Full digests:
- control: `72468b38a464856cae4368643585117f349d163b95d58941aa4bf9c5e150c1b9` (3/3 identical)
- new defaults: `6e6ee2caea39f864880e91df8bb0f18a2fad96d010dc47de4947d25eac047559` (3/3 identical)
- classic escape hatch: `dbab58208e3fbb79279a96768e56a6ea53328fd8dbe6a5b014bba48cea24f001` (×1)

## Deltas (new defaults vs pre-port control)

| metric | control | new | Δ |
|---|---|---|---|
| pass | 18/18 | 18/18 | 0 (identical) |
| honest halts | 2/2 | 2/2 | 0 (identical) |
| iterations | 46 | 46 | 0 |
| znc invocations | 45 | 28 | **−37.8%** |
| hypothesis-evals | 129 | 45 | **−65.1%** |
| wall-clock (end-to-end `real`) | 66.5 / 69.7 / 56.5 s (mean 64.2) | 53.6 / 48.9 / 51.9 s (mean 51.5) | **≈ −20%** |

Matches Arm 4's combo cell exactly (46 iters, 28 znc, 45 hyp-evals at budget 4).

## Determinism

- 3 reruns byte-identical canonical logs in BOTH conditions (control 3/3,
  new defaults 3/3). Zero RNG anywhere (pure Zag learner; Python glue only).
- Precheck false-positive validation: all 17 unique precheck-FAIL sources
  (3 reruns) compiled offline with znc — 17/17 real compile failures,
  **0 false positives** (validation invocations excluded from znc counts).

## Escape-hatch fidelity (classic path vs pre-port control)

Quality table identical (18/18, 2/2 halts, 46 iters, 45 znc, 129 hyp-evals).
Per-item trajectory comparison (outcome/evtype/class/strategy/score/src-hashes):
20/20 identical on all decision fields. 2 items (S03-dupfn-name, S09-type-dupfn)
differ ONLY in trace-line ORDER (DUPFN contributions logged before NAME in the
new binary) — inherited verbatim from the proven si4 baseline branch, which
evaluates classes in order SYNTAX, DUPFN, NAME, ARITY, TYPE vs the original
inline order SYNTAX, NAME, ARITY, TYPE, DUPFN. No decision, score, strategy, or
revised source differs; outcomes and all cost metrics identical. Decision-neutral.

## Files

- `ctrl_r{1,2,3}.json` — pre-port control runs (old driver + old learner, budget 6)
- `new_r{1,2,3}.json` + `.fp_candidates.jsonl` — new defaults (budget 4, combo+precheck)
- `classic_r1.json` — post-port classic-path control
- `si4none_r1.json` — Arm 4 baseline binary sanity (mask "", budget 6; trajectories
  20/20 identical to ctrl_r1, 46 iters / 45 znc)
- `smoke.json` — single-item new-defaults smoke test
- `metrics.py` — table/digest generator used above
- `*_work/` — per-iteration sources (text only; binaries and .zag-cache removed)
