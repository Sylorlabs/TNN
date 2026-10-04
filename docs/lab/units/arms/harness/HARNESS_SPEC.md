# HARNESS_SPEC.md — Track A shared harness (SHARED-HARNESS)

FROZEN with `ARM_INTERFACE.md`. Prereg: `units/PREREG_FREEZE.md`
(commit `b0b9140c0eda`, branch `tnn-native-lab`), frozen 2026-09-21.

## 1. What the harness is

The shared, arm-agnostic measurement rig for the 53-arm representation
bake-off. It provides:

- **Corpora** (`corpora/r1/`, built by `build_corpora.py`; 10x by `build_10x.py`).
  Documented in `CORPORA.md`. Raw sources are workspace-only, never committed.
- **The arm contract** (`ARM_INTERFACE.md`): invocation, modes, audit ledger,
  M8 gate, scorecard schema, confounder controls.
- **Runners** (`run_metric.sh`, `run_battery.sh`, `m8_gate.sh`, `m8_compare.py`,
  `scorecard_assemble.py`): every leg runs twice with stdout diffed; M8 runs
  5 perturbations × 2 reruns; RSS via `/proc` VmHWM polling (no GNU time on the
  lab VM); arm stderr kept pure for byte comparison.
- **Two reference binaries' sources**: `b64/` (the null control — fixed 64-byte
  chunk grid, pure arithmetic ID, no learning) and `memorizer/` (the M6 negative
  control — frozen prose top-5000 token policy).
- **The ambiguity register** (`AMBIGUITIES.md`): every literal-reading decision
  the prereg did not fully determine.

What the harness is NOT: it does not train, tune, or rank arms. Ranking follows
§9 C12 (reached-criterion?, then ETC, lexicographic; censored never averaged)
once real arms report.

## 2. Worked example: the B-64 null control (1x, round r1)

B-64 is deliberately the weakest possible arm: fixed 64-byte chunks, unit id =
`(corpus<<24)|chunk_index` (pure arithmetic, no stored ID→storage mapping),
slot placement = multiplicative hash of the ID, no learned representation,
recall = re-read the retained corpus buffer at the recorded span. It exists to prove the harness measures what it claims: a null
arm must score ~100% on M1/M4 (mechanical recall/revision), ETC=1 on M2,
survive M3 by brute capacity, and show terrible M5 cost (it keeps the whole
corpus in RAM). If B-64 scored badly on M1, the harness — not the arm — would
be broken.

Official 1x row (from `scorecard_assemble.py`; produced by the committed
runners, byte-identical double runs):

> Official run 2026-09-21: all 18 legs ×2 runs byte-identical, M8 gate PASS
> (5 perturbations × 2 reruns, all artifacts identical). M5's two FAILs are the
> honest null-control result — B-64 keeps the whole corpus in RAM and logs every
> ADD; the bars exist for real arms to beat.

| Metric | prose | code |
|---|---|---|
| M1 recall / boundary | 100.0 / 100.0 (84,731 u) | 100.0 / 100.0 (148,678 u) |
| M2 ETC (T1/T2/T3) | 1 / 1 / 1 | 1 / 1 / 1 |
| M2 episode-0 recall | 0.0% (leak check clean) | 0.0% |
| M3 survival / fresh recall | 100.0 / 100.0 | — |
| M3 freeze verdict | CLEAR (8,050 mgmt entries; 50/50 weaken handled) | — |
| M4 revised boundary/content | 100.0 / 100.0 | 100.0 / 100.0 |
| M4 kill rate | 0.0% (kill-substitution: false) | 0.0% |
| M5 memory / source byte | 1.719 — FAIL vs 1.5 bar (null control: keeps full corpus buffer + slot table) | — |
| M5 audit entries / KB | 16.2 — FAIL vs 10 bar (one ledger entry per ADD by construction) | — |
| M6 P→C rec/bnd/rev, tax | 100.0 / 100.0 / 100.0, tax 0.0 | — |
| M6 C→P rec/bnd/rev, tax | 100.0 / 100.0 / 100.0, tax 0.0 | — |
| Memorizer gate | P→C drop 54.8 pts (82.2 → 27.4) — PASS (≥ 15) | — |
| M7 | N/A (no ID layer); re-read bytes reported | — |
| M8 gate | PASS (5 perturbations × 2 reruns, all artifacts identical) | — |
| M9 T1 shape | fast-then-flat (takeoff 1, steepness 100.0, late gain 0.0) | fast-then-flat |

Reading the row honestly: B-64's perfect recall/revision scores are the
*ceiling* any arm can reach by mechanics alone — a real arm must beat B-64 on
M5 (cost), M6 transfer tax (B-64: 0.0 — nothing learned, nothing lost), and M9
shape is degenerate (instant memorization, no learning curve). The memorizer's
54.8-point drop gates M6: the transfer task is hard enough to matter.

## 3. §9 confounder controls — how the harness implements each

- **C1 (per-source-byte):** every cost column is normalized per source byte
  (M5) or reported separately from unit counts (M1 boundary vs content).
- **C2 (order):** fixed identical ingest order for all arms; `-rev` leg
  reserved (not yet run for the validator).
- **C3 (teacher-touch):** T2/T3 tiers are unseen-by-teacher; the ledger's
  trainer-opcode counts ride alongside M2.
- **C4 (ledger capacity):** fixed per scale leg, identical across arms;
  validator sizes generously; `LEDGER-BOUND` flag defined for arms that fill.
- **C5 (2^25):** no buffer indexed above 2^25 by construction (M8 store hashes
  use ≤2^20 chunks; the largest single buffer is the 16.6MB M8 audit ledger).
- **C6 (wall-clock):** never scored; allocator bloat lands in M5 RSS.
- **C7 (defect classes):** boundary (12 cycling magnitudes) + content
  (prose XOR patch / code rename map) — §10 M4.
- **C8 (V fixed):** the 1,000 valuable units are protocol-fixed (A2); the arm
  chooses only pin vs promote.
- **C9 (negative control):** `memorizer/` gates M6 (≥ 15-pt drop).
- **C10 (ID honesty):** M1 swap probe (ID arms; procedure proposed in A15) +
  M7 same-ID resolution.
- **C11 (schedule):** public schedule structure; unit identities from fixed
  corpus offsets; no per-arm identity choices.
- **C12 (censored ETC):** `"50+"` + `censored:true`, never averaged; rank
  lexicographic (reached-criterion?, then ETC).
- **C13 (M8 self-comparison):** each arm is compared only against its own
  five perturbations — never arm-vs-arm.
- **C14 (M9):** cutoffs frozen (40/15/3); raw (takeoff, steepness, late gain)
  always reported.
- **C15 (scale legs):** one row per attempted scale; missing 10x =
  `"ATTEMPTED — FAILED"`, never silently dropped.

## 4. Determinism architecture (why M8 passes)

- Zero randomness in any arm decision path (Micah's law). The only seeded
  generator in the pipeline is T3's corpus builder — environment input.
- No wall-clock, no addresses, no PIDs in the ledger, the store image, the
  allocator trace, or stdout. `alloc_trace.txt` logs sizes and order only.
- Slot placement is a pure function of unit ID (multiplicative hash); the
  freelist perturbation is therefore a verified no-op (A11).
- Perturbation-induced allocations (frag pattern, aslr pad) use raw syscalls
  and bypass the allocator trace — the trace captures the arm's own
  allocations, which must not move under perturbation.
- Every leg runs twice; stdout is diffed. M8 additionally runs 5
  perturbations × 2 reruns; `m8_compare.py` fails on any differing byte.
- The `m5-baseline` mode allocates the same empty store `m5-1x` uses, touches
  it, then busy-spins ~300M iterations so the harness's `/proc` VmHWM sampler
  can observe the peak RSS. The spin is measurement scaffolding, not arm
  cognition; it does not change the RSS number.
- Battery workdirs live under `~/workspace` (the lab VM's `/tmp` is a 512MB
  tmpfs — M8's 16MB ledgers × 10 runs fill it and cause silent ENOSPC
  truncation, which the runners report as rc=0 with partial artifacts).

## 5. Files (committed)

```
docs/lab/units/arms/harness/
  ARM_INTERFACE.md        the frozen arm contract
  HARNESS_SPEC.md         this file
  CORPORA.md              corpus sources, hashes, derivations
  AMBIGUITIES.md          literal-reading ambiguity register
  run_metric.sh           one mode ×2 runs, RSS via /proc, FATAL detection
  run_battery.sh          full 1x battery + M8 gate + scorecard assembly
  m8_gate.sh              5 perturbations × 2 reruns, starvation shim build
  m8_compare.py           byte-exact artifact comparison with localization
  scorecard_assemble.py   fragments + RSS → metrics-v1 row
  build_corpora.py        deterministic 1x corpus builder
  build_10x.py            deterministic 10x tiler
  b64/cl/arm.zag          B-64 null-control source (pure Zag)
  b64/substrate/          verbatim R33 substrate copies
  memorizer/cl/memorizer.zag   M6 negative-control source (pure Zag)
  memorizer/substrate/    verbatim R33 substrate copies
```

Never committed: binaries, `.zagd`, `.zag-cache/`, `corpora/` (raw or
derived), `ledger.bin` artifacts, workdirs.
