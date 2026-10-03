# H-NEW-3 Pilot Clean Re-wave Result

Status: PILOT-CLEAN-PASS. No falsifier fired; K1..K5 all hold.
Date: 2026-09-30 UTC.
Prereg: `d47bc8b28` (PREREG_PILOT_CLEAN.md), committed strictly
before any re-wave build.
Baseline: `fed72668c` (v1 implementation, PILOT-FAIL on F-PYTHON
only; all exploratory floors held).
Worker: H-NEW-3 Pilot Clean Re-wave Worker.

## 1. Verdict

**PILOT-CLEAN-PASS.** The identical build and run protocol was
replayed with zero Python at any stage. Every frozen floor holds,
all five falsifiers that can fire on behavior are silent, F-PYTHON
is silent, and all kill bars hold. The clean re-wave confirms the
v1 exploratory evidence under the literal purity rule.

## 2. Purity (K4)

- Source `pilot.zag` and `BUILD.sh` adopted byte-for-byte from
  `fed72668c` (sha256 MATCH on both files before the first build).
- Build: `sed` MODE injection + `znc` compile, shell only.
  Six binaries, exit 0 each.
- Runs: 18 process invocations (6 modes x 3), shell only.
- Verification: `md5sum`, `sha256sum`, `grep`, `diff`, `wc`,
  shell only. No Python invoked at any stage, including this
  report's preparation.
- Zero em-dash bytes in all new committed files
  (shell-verified before commit).

## 3. Determinism (F-NONDET silent)

All 6 modes 3/3 byte-identical on stdout, zero stderr bytes:

- mode 0: b301d100df41656e58cfc531c0d82c49
- mode 1: 7d33987a19dbf2079bd27917742d4530
- mode 2: 95a15999c05f7ac2246b0ef2bdd8394e
- mode 3: 3f0238a842bc30e02958a8c9d15b4eeb
- mode 4: d8d948cb38707394b52cbdefab2c0c90
- mode 5: 4407c9763589332a8ca3d19af34e87dc

Each md5 equals the baseline exploratory value exactly, confirming
a faithful replay.

## 4. Floor table

### Immediate floors, Arm A (mode 0)

| Floor | Bar | Observed | Status |
|---|---|---|---|
| F-E1 | P1 >= 13/16, W1=1 | 16/16, W1=1 | HOLD |
| F-E2a | schema discovered | DISC=1 | HOLD |
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
| F-REL-P1 | A-P1d >= B-P1 - 1 | 16 | 16 | HOLD |
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
- F-CORRUPT: silent (canary audit 5/5, A-CANARY=5/5).
- F-REUSE-FAIL: silent (6 < 12 strict; reuse fit 12/12).
- F-FLOOR: silent (every immediate floor holds in Arm A).
- F-LABEL: silent. Re-audited on the adopted source: the episode
  counter `ep` is a local in `arm_a` (line 698), incremented
  after each experience call, never passed to any subsystem
  function (calls take `(ws)` only); no `g_episode` global exists.
  All observations route through `dispatch_observe` with sensory
  channel tags CH_VOCAB..CH_FACT. One `main()` flow, no resets.
- F-NONDET: silent (section 3).
- F-PYTHON: silent (section 2).

## 6. Kill bars

- K1 (prereg before build): HOLD. `d47bc8b28` strictly precedes
  the first build; self-checked at report time.
- K2 (five experiences, one process, no resets): HOLD. Mode 0
  runs E1..E5 in one process (PILOT-A-RESULT=1), D1 discipline
  held (F-LABEL silent).
- K3 (all floors): HOLD (section 4).
- K4 (pure Zag, deterministic, no em dashes, canaries): HOLD.
- K5 (Arm B run and compared): HOLD (section 4, validity table).

## 7. What this establishes

One pure-Zag process experienced vocabulary (16/16 including 2
novel negations), concept learning (4/4 held-out, schema savings
2<8), procedure invention (generic threshold construction, t=13
found, promoted, halving passed), conflict revision (flagged
same-episode, hedged, exactly one re-observation, truth
restored), and delayed reuse (form retrieved from persistent
state; 6 interventions vs 12 fresh) with zero retention loss on
any delayed probe, intact canaries, and 1200-byte total state.

## 8. Honest scope (unchanged)

Partitioned regions (non-interference tested, not shared
representation); E1 NOT is a fixed compositional rule; E3 baseline
is single-threshold-specialized; E5 bisection is researcher-authored
(what is tested is whether retrieved persistent structure reduces
later cost, system-level C0-D); E4 oracle answers come from the
harness. Per the prereg, no L3 claim attaches to this pilot. This
is retention/interference evidence for the continuing-learner
integration path, authorizing the scale-up battery per design
section 8 as a named follow-up wave.

## 9. Self-check

- [x] Prereg strictly before build (K1).
- [x] No floor altered after results.
- [x] Zero Python at every stage (section 2).
- [x] Zero em-dash bytes in new files (shell-verified).
- [x] Commits local, pathspec-limited to pilot_clean/.
- [x] Paper not touched.

Builder label: PILOT-CLEAN-PASS.
