# Scale-Up Battery Result

**Verdict: SCALEUP-PASS**

Frozen prereg: `3e02255f3` (PREREG_SCALEUP.md, 320 lines).
Implementation: `scaleup.zag` + `BUILD.sh` in `scaleup_impl/`.
Arm A result code: 2 (SCALEUP-PASS). All falsifiers silent.

## Arm A immediate floors

| Floor | Observed | Bar | Pass |
|-------|----------|-----|------|
| S-P1 | 56/64 | >= 54/64 | yes |
| S-W1 | 1 (white-box) | == 1 | yes |
| S-E9a P1c | 3/3 | == 3/3 | yes |
| S-E9b P1n | 45/45 | >= 43/45 | yes |
| S-E9b neg | 8/8 | == 8/8 | yes |
| S-P2a | 1 | == 1 | yes |
| S-P2b | 7/7 | >= 6/7 | yes |
| S-P2c | 1 (app 3 < fresh 16) | app < fresh | yes |
| S-P2r | 1 (domain 1 retired) | domain 1 retired, 5 live | yes |
| S-E7b D0 | 1 | == 1 | yes |
| S-E7b P2b | 7/7 | >= 6/7 | yes |
| S-E7b P1e | 53/64 | >= 52/64 | yes |
| S-E7a schema | 623 == 623 (no bleed) | unchanged | yes |
| S-E3 I1/I2/I3 | 1,1,1 (params 13,47,71) | all 1, params exact | yes |
| S-E3 pool | 1 | == 1 | yes |
| S-E4a latency | <= 1 per flag | <= 1 | yes |
| S-E4b hedges/reobs | 3/3, K2 0/0 | exactly 3/3 | yes |
| S-E4c finals | (0,0,13), no suspects | exact | yes |
| S-E4x P1 | 53/64 | >= 52/64 | yes |
| S-E4x gate | 1 | == 1 | yes |
| S-P6a cause | 2 | == 2 | yes |
| S-P6b held-out | 4/4 | >= 3/4 | yes |
| S-E6 budget | 4 | <= 8 | yes |
| S-E5a reuse | 6 < 12 (fresh), fit 12/12 | < fresh, <= 6, 12/12 | yes |
| S-E5b reuse | 10 < 26 (fresh), fit 12/12 | < fresh, <= 14, 12/12 | yes |

## Delayed battery (S-D1..D9)

| Probe | Observed | Bar | Pass |
|-------|----------|-----|------|
| S-D1 P1d | 53/64 | >= 50/64 | yes |
| S-D2 | 1, P2b 7/7 | 1 and >= 6/7 | yes |
| S-D3 pool | 1 | == 1 | yes |
| S-D4 facts | 1 | == 1 | yes |
| S-D5 reuse | E5=1, E5b=1 (stored state, no new teaching) | both 1 | yes |
| S-D6 causal | cause=2, budget=4 | cause==2 | yes |
| S-D9 corrections | 3/3 | == 3/3 | yes |

S-D7 and S-D8 are Arm B comparisons (see relative floors).

## Relative floors (Arm A vs Arm B)

| Floor | Arm A | Arm B | Bar | Pass |
|-------|-------|-------|-----|------|
| S-REL-P1 | P1d=53 | B1 P1=53 | >= B-3 (50) | yes |
| S-REL-P2 | P2b=7 | B2 P2b=7 | >= B-0 (7) | yes |
| S-REL-P4 | (0,0,13) | B5 (0,0,13) | equal | yes |
| S-REL-E9 | P1n=45 | B1 P1n=45 | >= B-2 (43) | yes |

Arm B immediate floors: M1 (P1PRE=56, W1=1, P1=53, P1c=3/3, P1n=45/45, neg=8/8),
M2 (all 1), M3 (schema clean, D0=1, P2b=7/7), M4 (1,1,1, pool=1), M5 (E4OK=1,
P1=53, gate=1), M6 (cause=2, held=4/4), M7 (E5OK=1), M8 (E5bOK=1). All pass.

## Canary audit

10/10 intact. Regions: R_E1, R_E2, R_E3, R_E4, R_E5, R_E6, R_E7, R_E9,
R_E2T, R_E5B.

## State pressure (S-PRESS)

Workspace: 16,384 words = 65,536 bytes. Zero drops. Within [65536, 4194304].
PRESS=1. Qualifies for SCALEUP-PASS (not NOPRESSURE).

## Falsifiers

F-INTERFERE: silent. F-CORRUPT: silent. F-REUSE-FAIL: silent. F-FLOOR: silent.
F-LABEL: silent (source audit: no episode counter or task label reaches any
subsystem; routing is by sensory channel and domain index only).
F-NONDET: silent. F-PYTHON: silent (zero Python invocations; shell/znc/git only).
F-CAUSAL: silent. F-PRESSURE: silent. F-CORRECTION: silent. F-DISTRACT: silent.

## Kill bars

- K1: Prereg `3e02255f3` is an ancestor of HEAD; `scaleup_impl/` was untracked
  at prereg time. No frozen bar moved.
- K2: Arm A is one process. No resets, no recompilation. Routing by sensory
  channel only (D1). Build-time MODE constant; subsystems see no mode.
- K3: All immediate, delayed, relative, and capacity floors hold.
- K4: Pure Zag. 3/3 byte-identical stdout, zero stderr (all 9 modes).
  Zero em/en dash bytes (shell checker + non-ASCII scan clean). Canaries 10/10.
  Pressure satisfied.
- K5: Arm B modes 1..8 run from the same source, all floors compared.

## Determinism (stdout md5, 3/3 identical, stderr 0 bytes)

- mode 0: e46e4961848250d8835d3a3e6edf377f
- mode 1: 15d0a3f2b79b0b2d9291e2b92dc8b2cf
- mode 2: 8aa81f52aef095f89ba3dec1eca6cc5e
- mode 3: f072319471feaee690544aaf12adac6d
- mode 4: 921cd76ad03208784f47621dc21e625f
- mode 5: 0cc3ffeb548c23d46436a4076bcb43fc
- mode 6: 11ef05904c079e8890ce913086680026
- mode 7: 3e5d63e1eba155ed8f5dc3d92ed1cd1f
- mode 8: ece44dd8e9406b73d4cef4cefd5289e6

Binaries in `scaleup_impl/build/` (mode injected via sed at build time;
same `scaleup.zag` source for all).

## Honest scope

Bounded L2/system-level evidence for C0-D reuse (procedural structure reused
across E3/E5/E5b within one process). Not L3: thresholds are researcher-seeded
worlds with disclosed baseline specialization (generic class-change midpoint
greedy, fixed direction); E5b composition uses researcher-authored refit and
frozen AND/NOT machinery. No representational invention claimed.

## Files

- `scaleup_impl/scaleup.zag` (implementation, pure Zag)
- `scaleup_impl/BUILD.sh` (builds modes 0..8)
- `scaleup_impl/build/` (binaries + per-mode source)
- `scaleup_impl/RUN_M*_*.txt/.err` (3x run logs, deterministic)
- `scaleup_impl/SCALEUP_RESULT.md` (this file)
