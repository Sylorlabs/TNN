# R0 ARMS — Verdict Sheet (build + smoke)

**Crew:** R0 ARMS (tournament cut-signal arms, R31 native redo)
**Date:** 2026-09-21
**Scope:** build the arm implementations + M8 smoke evidence. **Tournament
scoring and orderings have NOT been run** — these are build/smoke results only.

## What was built

`units/r0/impl/arms/` — one pure-Zag binary, `argv[1]` selects configuration
(11 selectors across the requested families):

| family | selectors |
|---|---|
| predictive_surprise | `predictive_surprise` |
| fixed_window | `fixed_window_4`, `fixed_window_8`, `fixed_window_16`, `fixed_window_64` |
| mdl | `adaptive_mdl`, `grounded_adaptive_mdl`, `hierarchical_mdl` |
| raw_micro | `raw_micro` |
| random analog | `random_chunks` — **DETERMINISTIC-ANALOG, informational only, excluded from binding B-T1** |

Files: `arms.zag` (implementation), `INTERFACE.md` (stdin/stdout harness
contract), `ARM_SPEC.md` (rule-by-rule spec), `run_smoke.sh` (M8 smoke
harness), `probe_stores.zag` (compiler-bug probe), `xcheck.py` (independent
Python cross-validation).

## Verdicts

| check | result |
|---|---|
| Compile (`znc`, pinned toolchain, pure Zag) | **PASS** — native binary, 0 external tools |
| M8 smoke: N=5 byte-identical reruns, all arms × 7 inputs | **PASS** |
| M8: 3 adversarial heap perturbations (junk malloc/free, interleaved, fragmented) | **PASS** — all outputs byte-identical to base |
| M8: ASLR-equivalent (`setarch -R`) | **PASS** — identical |
| M8: source canary (no clock/entropy/PID/RNG references) | **PASS** |
| Round-trip: segments tile `[0,n)` exactly, header/trailer valid | **PASS** — all 70 arm×input outputs |
| stderr empty on success | **PASS** |
| Python cross-validation (`xcheck.py`, independent implementation, SEG-row-for-row, all 10 arms × 7 inputs incl. 64KB) | **PASS** |
| ZNC-2026-09-19-001 store-integrity probe (`probe_stores.zag`: 4/5/8-sequential `*i64` store patterns incl. mergesort tmp pattern, negatives, i64 extremes; 365k iterations) | **PASS** — 0 mismatches |

## ZNC-2026-09-19-001 audit (coordinator hardening)

- `arms.zag` contains **zero** `[]i32` / `[]i64` slices (grep: 0 occurrences).
  All integer arrays are `*i64` pointer-indexed stores. The bug is described
  as hitting "`[]i32`/`[]i64` multi-store contexts"; the literal trigger is
  absent from this codebase.
- Rather than a full rewrite to `[]u8`-backed cells, the sanctioned probe
  option was taken: `probe_stores.zag` replicates this codebase's exact hot
  store patterns (4-sequential hash-table insert, 5-sequential candidate
  fill, mergesort tmp write + copy-back, 8-sequential with extremes) and
  verifies readback — **PASS, 0 bad cells**.
- Stronger end-to-end evidence: `xcheck.py` reimplements the native rules
  independently in Python and matches the compiled binary SEG-row-for-row on
  all arms and all inputs. A store miscompile would have to corrupt both
  implementations identically to hide — effectively impossible.
- **Cross-crew flag:** `r0/impl/core/API.md` specifies the core arena as a
  `[]i32` array — inside the bug's described blast radius. Core crew should
  audit/probe it. Not acted on here (their component).

## Deterministic-analog rule (exact, for the record)

`random_chunks` is not random. Per position `i`:
`h = (Σ(j+3)·b[i+j] + 17·i) mod 7` over the next 5 bytes (bytes past end
contribute zero), `L = 2 + h`, clamped to the remaining input. Pure function
of the input; labeled `META analog=deterministic` in output; excluded from
binding B-T1.

## Frozen-bar ambiguities (flagged, not reinterpreted)

1. Parent states the prereg was frozen and Micah signed it 2026-09-21, but
   local `PREREG_FREEZE.md` still reads "PROPOSED — NOT FROZEN" with R-1…R-9
   in approve/proposed language. Discrepancy reported, bars unchanged.
2. R-2 proposes `L_max ≤ 8`, matching the R31 core enumeration; the recovered
   tournament's MDL arm used `max_len=12`. This build uses **12** (tournament
   arm reproduction), flagged explicitly.
3. Recovered Python MDL sort used raw-bytes-descending for final ties; native
   uses bytes-ascending (canonical).
4. Reference surprise-inventory tie order used Python first-seen; native uses
   bytes-ascending (canonical).
5. Core API was absent when this interface was written (checked 2026-09-21);
   it has since landed — assessed, no adaptation needed (library contract vs
   tournament harness contract; see INTERFACE.md).
6. During the first smoke run, `/tmp` (512M tmpfs shared with other crews)
   filled mid-run (ENOSPC), truncating one output file. Environmental, not a
   determinism failure — verified by isolated repro (perturb pattern stable
   8/8). Scratch moved to workspace; suite re-ran clean.

## Binding order check (B-T1, informational — no tournament run yet)

Build order per parent: `predictive_surprise > fixed_window > raw_micro`
(raw_micro dead last). `random_chunks` excluded from binding.

## Not done / not claimed

- Tournament scoring, orderings, and the binding verdict have **not** been
  run. Nothing here claims any arm's tournament score or rank.
- Old tournament numbers (predictive_surprise 0.73756, etc.) were used as
  reference-only orderings, never targets.
- 1x only; no 10x (bars-gated per parent).
