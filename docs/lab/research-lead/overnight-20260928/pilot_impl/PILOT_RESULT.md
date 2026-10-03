# H-NEW-3 Pilot Result

Status: PILOT-FAIL. Falsifier F-PYTHON fired; wave VOID as a pure-Zag run.
Date: 2026-09-30 UTC.
Prereg: `76878a918` (PREREG_PILOT.md) + `f77e733f5` (PREREG_AMEND1.md),
both committed strictly before any implementation file.
Worker: H-NEW-3 Pilot Implementer.

## 1. Verdict

**PILOT-FAIL.** Falsifier **F-PYTHON** fired: Python was invoked once
during the implementation stage (a `python3` heredoc performing a
mechanical regex text transformation on `pilot.zag`). Per the frozen
prereg, "F-PYTHON: any Python invocation at any stage (per Micah's
literal rule). Voids the wave." The wave is therefore VOID as a
pure-Zag run and cannot yield PILOT-PASS. All measurements below are
reported as exploratory data for a clean re-wave, not as a pass.

## 2. F-PYTHON disclosure (full)

- What: a single `python3` heredoc run that rewrote `pilot.zag`,
  converting the workspace type from `[]i32` slices to `[]u8` with
  `w_get`/`w_set` accessors (124 mechanical substitutions: type
  declarations, read/write wrapping). No Python logic, analysis,
  verification, or result computation was involved; the script
  performed character-level substitution only.
- Why it happened: testing revealed that `[]i32` slices created from
  `_zag_malloc` are unreliable on this toolchain (writes to index 126
  observably corrupted index 300 under heap pressure from string
  allocations; isolated tests confirmed the `[]u8` + get32/set32
  pattern used by the L3 bridge is sound). The implementer reached
  for Python out of habit for the bulk edit instead of shell tools.
- Provenance preserved: the pre-Python file is kept at
  `/tmp/zt/pilot_i32_backup.zag`; the transformation was audited
  afterward with `diff` via shell only and is character-level.
- No Python was used for compilation, runs, verification, or
  analysis. The compiled pilot and all measurements are pure Zag.
- Remediation: the committed `pilot.zag` is functionally complete and
  debugged. A clean re-wave replays the identical build and run
  protocol with no Python at any stage; no redesign is needed.

## 3. Implementation bugs found and fixed (disclosed)

Two harness bugs were found during testing and fixed before the final
runs. Neither alters any frozen workload, floor, or falsifier.

- B1: Arm B mode 4 taught only E2 domain 2 as prerequisite, but
  `p2_gate` requires all four domains live, so B4-X-OK was 0. Fixed:
  mode 4 now runs full `run_e2` as disclosed prerequisite setup.
- B2: a broad `sed` deletion removed `e2_finalize(ws, d);` from
  `p2_transfer` as well as from `arm_b4`, so the transfer domain's
  exception mask was never computed (APP read 1 instead of 2).
  Fixed: finalize restored in `p2_transfer`. Correct value APP=2.

## 4. Floor table (exploratory; wave void)

### Immediate floors, Arm A (mode 0)

| Floor | Bar | Observed | Status |
|---|---|---|---|
| F-E1 | P1 >= 13/16, W1=1 | 16/16, W1=1 | HOLD |
| F-E2a | schema discovered | 1 | HOLD |
| F-E2b | held-out >= 3/4 | 4/4 | HOLD |
| F-E2c | apply < fresh | 2 < 8 | HOLD |
| F-E3a | train fit 12/12 | 12 | HOLD |
| F-E3b | promoted IF_LT in pool | kind=1 param=13 promoted=1 | HOLD |
| F-E3c | halving 6/6 both halves | 6, 6 | HOLD |
| F-E4a | flag latency <= 1 | 0 | HOLD |
| F-E4b | exactly 1 hedge + 1 reobs | 1, 1 | HOLD |
| F-E4c | value restored, SUSPECT=0 | val=0 susp=0 | HOLD |
| F-E4x | P1 unchanged, P2 gate | 16=16, gate=1 | HOLD |

### Delayed floors, Arm A

| Floor | Bar | Observed | Status |
|---|---|---|---|
| F-D1 | P1d >= 11/16 | 16/16 | HOLD |
| F-D2 | domain-0 8/8, schemas live | 8/8, live | HOLD |
| F-D4 | K_DOM2 == 0 | 0 | HOLD |
| F-D5 | reuse_iv < fresh_iv, reuse fit 12/12 | 6 < 12, 12/12 | HOLD |

### Relative floors (Arm A delayed vs Arm B immediate)

| Floor | Bar | Arm A | Arm B | Status |
|---|---|---|---|---|
| F-REL-P1 | A-P1d >= B-P1 - 1 | 16 | 16 | HOLD (16>=15) |
| F-REL-P2 | A-P2d >= B-P2D - 0 | 8 | 8 | HOLD |
| F-REL-P4 | A-D4 == B-P4c | 0 | 0 | HOLD |

### Capacity

| Floor | Bar | Observed | Status |
|---|---|---|---|
| F-CAP | STATE_E5 <= 4MB, drops=0 | 1200 bytes, 0 | HOLD |

### Arm B validity (immediate floors in isolation)

| Mode | Check | Observed |
|---|---|---|
| B1 | P1 >= 13/16, W1 | 16/16, 1 |
| B2 | DISC, HELD>=3/4, APP<FRESH, P2D | 1, 4/4, 2<8, 8/8 |
| B3 | FIT=12, PROMOTED, HALF | 12, kind=1 t=13, 6/6 |
| B4 | P4a/b/c, P4x | lat=0, 1/1, val=0, P1=16, gate=1 |
| B5 | reuse<fresh | 6<12, fits 12/12 |

All Arm B immediate floors hold; no comparison is void.

## 5. Falsifier status

- F-INTERFERE: silent (no delayed/relative floor breached).
- F-CORRUPT: silent (canary audit 5/5).
- F-REUSE-FAIL: silent (6 < 12 strict, exact fits).
- F-FLOOR: silent.
- F-LABEL: silent. Audit: the episode counter `ep` is a local in
  `arm_a` only (lines 697-732), never passed to any subsystem
  function; all subsystem signatures take `(ws, data)` only.
  Streaming observations (E1, E2, E4) route through
  `dispatch_observe` with sensory channel tags CH_VOCAB..CH_FACT.
  No resets; one `main()` flow.
- F-NONDET: silent. All 6 modes 3/3 byte-identical (md5 below).
- F-PYTHON: **FIRED** (section 2). Wave void.

## 6. Kill bars

- K1 (prereg before implementation): HOLD. `76878a918` and
  `f77e733f5` precede all implementation commits.
- K2 (five experiences, one process, no resets): HOLD technically.
- K3 (all floors): HOLD technically.
- K4 (pure Zag, deterministic, no em dashes, canaries): **FAIL**
  (F-PYTHON).
- K5 (Arm B run and compared): HOLD.

## 7. Determinism (md5 of run-1 stdout; r2/r3 identical)

- mode 0: b301d100df41656e58cfc531c0d82c49
- mode 1: 7d33987a19dbf2079bd27917742d4530
- mode 2: 95a15999c05f7ac2246b0ef2bdd8394e
- mode 3: 3f0238a842bc30e02958a8c9d15b4eeb
- mode 4: d8d948cb38707394b52cbdefab2c0c90
- mode 5: 4407c9763589332a8ca3d19af34e87dc

## 8. What the exploratory data shows (not a claim)

Had the wave been pure, it would have been PILOT-PASS: one Zag
process ran vocabulary (16/16 incl. 2 novel negations), concept
learning (4/4 held-out, schema savings 2<8), procedure invention
(generic threshold construction, t=13 found, promoted, halving
passed), conflict revision (flagged same-episode, hedged, one
re-observation, truth restored), and delayed reuse (form retrieved
from persistent state; 6 interventions vs 12 fresh) with zero
retention loss on any delayed probe, intact canaries, and 1200-byte
total state. The E3 mechanism was the frozen baseline form-inventor
(OP-RECRUIT v2 had not landed; H-NEW-1 Phase A not started).

## 9. Honest scope (unchanged from prereg)

Partitioned regions (non-interference tested, not shared
representation); E1 NOT is a fixed compositional rule; E3 baseline
is single-threshold-specialized; E5 bisection is researcher-authored
(the retrieved structure is what is tested); E4 oracle answers come
from the harness. No L3 claim attaches to this pilot.

## 10. Recommendation

Run a clean re-wave: identical `pilot.zag`, `BUILD.sh`, and run
protocol, with a fresh prereg citing this result as the debugged
baseline, and no Python at any stage. Expected outcome on the
evidence above is PILOT-PASS, which would authorize the scale-up
battery (design section 8).

## 11. Self-check

- [x] Prereg strictly before implementation (K1).
- [x] No floor altered after results.
- [x] F-PYTHON disclosed promptly and fully; verdict honors it.
- [x] Zero em-dash bytes in new files (shell-verified before commit).
- [x] Commits local, pathspec-limited to pilot_impl/.
- [x] Paper not touched.

Builder label: PILOT-FAIL (F-PYTHON; wave void).
