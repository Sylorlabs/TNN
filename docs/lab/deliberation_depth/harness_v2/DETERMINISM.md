# Determinism proof (H5 deliberation harness, Phase 1)

Claim: for fixed inputs (items file + depth config), `delib_harness` produces
byte-identical `results.jsonl` and `ledger.jsonl` on every run — no RNG, no
timestamps, no PIDs anywhere in the decision or output paths.

## How it was proven

`run_determinism.sh` (re-run it anytime):

1. Rebuilds `delib_harness` from source with the pinned znc
   (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
2. Runs the 6-item smoke battery **twice** under each depth config
   (`smoke_shallow.cfg`, `smoke_deep.cfg`, `smoke_adaptive.cfg`).
3. Requires `cmp`-clean equality of both output files between the two runs.
4. Runs a malformed-input battery twice (bad `task_type`, missing fields) and
   requires `cmp`-clean equality of the error-path outputs too.
5. Records SHA256 of every artifact.

The full transcript is `DETERMINISM_LOG.txt` (generated 2026-09-23).

## Result

**PASS.** All comparisons byte-identical:

| Config | results.jsonl SHA256 | ledger.jsonl SHA256 |
|---|---|---|
| shallow | `58d28048…a7790e875` | `817edd20…8d22f1032f` |
| deep | `a94b94a6…45ed2dd4d6` | `ac2704b1…38d6c9a6817` |
| adaptive | `89ac4501…b44cab4613` | `59b8961e…3fc20cce011` |

Bonus (reported, not gated): rebuilding the binary from the same sources is
itself byte-identical (`033962a9…cc8bea1` both times).

## Independent cross-check

A from-scratch Python reimplementation of the deliberation algorithm
(`~/workspace/scratch-h5/xcheck/xcheck.py`, scratch-only, not committed)
re-derived all 18 smoke verdicts (6 items × 3 configs): verdict, confidence,
rounds_used, and evidence_consumed match the Zag binary exactly, 0 mismatches.
The same script recomputed every SHA256 ledger link from genesis: all chains
verify (49 / 69 / 69 steps).

## Smoke accuracy (sanity, not gated)

shallow 5/6, deep 6/6, adaptive 6/6. The shallow miss (item S4) is by design:
two fixed rounds cannot reach the decisive refutation evidence — the depth
effect H5 exists to measure. No full measurement matrix was run (Phase 1 only,
per the task; awaits prereg freeze).
