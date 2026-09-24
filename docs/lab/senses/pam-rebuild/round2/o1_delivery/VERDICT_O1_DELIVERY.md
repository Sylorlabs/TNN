# VERDICT O1 — Knowledge-delivery repair (PAMs Round 2, hypothesis R3-1)

**Date:** 2026-09-24. **Branch:** `tnn-native-lab`. **Prereg:**
`PREREG_O1_DELIVERY.md` (commit `ca609778d2a7cbd8055e26f3068b9fd97e2b931d`,
committed alone before any build).
**Verdict: KILL.** Both KB-O1 bars fail.

## Build

Pure-Zag `o1.zag`: Delivery Adjudicator + frozen gate replay
(ported from `memgate.zag`: permanent/provisional slots, 256-entry
negative-evidence table per task, `tol_of` per tcode; []u8 arenas with
LE accessors throughout). Toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Zero RNG.

**Fidelity (repair off):** K1 1,062/1,102, K2 824/1,102, RK-3 104/1,102,
RK-1 0, RK-2 0/1,109 — all frozen numbers reproduce exactly.
3 byte-identical runs, sha256
`a946b989578809d1e09bedede44938fd83b157c362dd1481a64a929713c50ceb`.

**Repair (on):** 3 byte-identical runs, sha256
`54122164b5a9eddf6e3f416a99bf8bc9e63dcbb9d7507012986177d485b520f3`.

## Numbers vs kill bars

| Metric | Frozen | Repaired | Bar | Result |
|---|---|---|---|---|
| K1 (progF==PASS) | 1,062/1,102 (96.37%) | 1,062/1,102 (96.37%) | — | — |
| K2 (delivered) | 824/1,102 (74.77%) | 954/1,102 (86.57%) | within 2pp of K1 (≥94.37%) | **FAIL** (−9.80pp) |
| RK-3 (installed) | 104/1,102 (9.44%) | 106/1,102 (9.62%) | ≥9.44% + (11.80/2)pp = 15.34% | **FAIL** (−5.72pp) |
| RK-1 (false perm) | 0 | 0 | no regression | PASS |
| RK-2 (wrong hi-conf perm) | 0/1,109 | 0/1,109 | no regression | PASS |
| Records repaired | — | 130 | — | — |

- **KB-O1a FAIL:** K2' = 86.57% is 9.80pp below K1 = 96.37% (bar: ≤2pp).
- **KB-O1b FAIL:** closed delivery gap = 11.80pp; half = 5.90pp;
  required RK-3' ≥ 15.34% (≥169/1,102); actual 9.62% (106/1,102).
  RK-3 rose 0.18pp — 1.5% of the closed gap, not 50%.

## What the repair did

The Delivery Adjudicator admits `progF==PASS AND agree==1 AND conf>=700`
(128 trials: the disjoint span agreed but the `strong` margin flag was
unset) plus 2 deliberation-downgraded trials. Safety holds: 0 new wrong
percepts admitted (the `conf>=700` bar is load-bearing — without it, 4
wrong conf<700 percepts enter); RK-1/RK-2 unchanged at 0.

## The honest residual

**Of the 255 undelivered-but-present trials:**
- 130 admitted by the repair. Of these, only **2 installed**
  (the deliberation downgrades, seq 2366/2372 → PROVISIONAL_INSTALL).
  The other 128 were withheld by the gate's own rules:
  - 68 CONFLICT_WITHHELD (live permanents; pitchdisc's weak incumbent
    at seq 2385 blocks most),
  - 60 SUPPRESSED (negative-evidence table, mostly pitchdisc's poisoned
    entries from the program's own false-negative FAILs — AUTOPSY_R2-4 §1.4).
- 125 never admitted: the (g) check's no-agreement (`agree==0`) and
  strong-disagreement (`contra==1`) verdicts. Admitting them requires
  overriding the safety mechanism: (0,0) holds 364 wrong high-conf,
  (0,1) holds 313 wrong high-conf. Not a delivery decision — a
  sense-calibration (prereg (f)) decision.

**Fraction of the gap closed:** K2 closed 11.80pp of the 21.60pp K1−K2
gap (54.6%). But installs followed at 1.5% of the closed gap.

## Why O1 dies (as its own kill bar predicted)

"a K2 rise with no RK-3 rise means the gate withholds delivered percepts
for other reasons, and the hypothesis as stated is dead." That is exactly
what happened. The binding constraints are not in the delivery path:

1. **Gate conflict rule** (68 trials): delivered correct percepts are
   withheld by live permanents. Fix = corroborated revision (AUTOPSY_R2-4
   §4.1) — a gate-rule change, explicitly out of O1's scope.
2. **Poisoned negative evidence** (60 trials): the table was armed by the
   program's own false negatives. Fix = corroborated negative evidence
   (§4.4) + program (f) predicate revision — not delivery.
3. **The `strong` threshold** (125 trials): the remaining gap is the (g)
   check's calibration, not a missing path. The "delivery gap" was
   misdiagnosed — it is a sense-calibration gap wearing delivery clothes.

**O1 as stated — "find and fix the drops" in the delivery path — is KILLED.**
The drops it can safely fix (130) do not move RK-3; the drops that would
move RK-3 cannot be fixed in the delivery path without breaking RK-2.
The 74.8% ceiling does not yield to delivery repair. Recommended redirect:
the corroborated-revision gate rule (R3-3 D2 covers the release direction;
the admission direction needs its own prereg) and prereg-(f) (g)-predicate
revision for the 125.

## Evidence pointers

- Input: `sweep.jsonl` sha256
  `4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2`
  (11,840 rows, frozen).
- Build: `src/o1.zag`, `src/gen_case.py` (glue), `src/case_o1.txt`.
- Runs: `evidence/metrics_fidelity_*.txt`,
  `evidence/metrics_repair_*.txt` (3+3 byte-identical).
- No binaries, no `.zagd` committed.
