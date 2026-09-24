# VERDICT O3-REBRIEFED — Blockage repair (PAMs Round 3, Crew 4)

**Overall: KILL** (KB-O3a conversion bar failed: 78/128 < 100).
All safety bars PASS. The kill is on the conversion bar only, as pre-registered
(the prereg predicted ~73 and an expected KILL on this bar).

## Build/run

- Pure Zag, zero randomness. Three runs, byte-identical.
- Metrics SHA-256 (all three runs): `897ddcdaa0112c402a70c32f7630cad0c8605ce7272aaa7ace9188a322c8d8e2`
- Instrument: `src/o3.zag` (O1 adjudicator retained + R1–R4).
- Case: `case_o3.txt` (11,840 rows; sweep.jsonl sha256 `4163fffa…83f2`).
- An independent exact-match Python reimplementation reproduces every Zag
  metric exactly (validates the Zag logic).

## Kill bars

| Bar | Rule (re-briefed) | Result | Verdict |
|-----|-------------------|--------|---------|
| KB-O3a | ≥100 of 128 O1-residual convert | **78/128** (60.9%) | **KILL** |
| KB-O3b | adv wrong-install ≤ 3.02% (frozen 1.02% + 2pp) | 1.02% (36/3,528), unchanged | PASS |
| KB-O3c | <2 of six timbredisc wrongs get REVISED/PERMANENT install | 0 | PASS |
| KB-O3d | RK-3 ≥ 8.48% (88.48% typo corrected) | 74.50% (821/1,102) | PASS |
| P-DISJOINT | 0 wrong high-conf REVISED_INSTALL | 0 | PASS |

## What the repair did

- **78 of the 128 O1-residual trials convert** to installs (all correct;
  the residual is 100% correct by the adjudicator).
- **50 do not convert**: all 50 are SUPPRESSED by negative entries armed by
  MULTIPLE false-negative FAILs (e.g. 11 FAILs on one pitchdisc percept).
  R2's two-FAIL corroboration fix cannot disarm them. This confirms O1's
  diagnosis: the poisoning is program-side (prereg (f)), not gate-side.
- **Mechanism attribution** (from the run): R1 (corroborated revision) fired
  0 REVISED_INSTALLs and stored 1 challenger. The conversions came via R4
  (confidence bar on permanence): by refusing PERMANENT_INSTALL to sub-700
  provisional incumbents, R4 eliminated the weak permanents that blocked the
  68 conflicts — they then installed via the provisional path. R1 stands as
  the safety net for genuine conflicts (none arose). R2 recovered the
  singly-poisoned suppressions.
- **RK-3: 821/1,102 = 74.50%** (frozen 9.44%, O1 9.62%). The rise is driven
  by R4 unblocking the frozen conflicts (the 621 install via the provisional
  path once the weak permanents are gone), plus the 78 residual conversions.
- **RK-2: 0/1,109. RK-1: 0.** No wrong high-conf permanent installs.
- **Six timbredisc wrongs**: all CORROBORATED (as under frozen rules); zero
  new installs. The recalibrated margin bar (timbredisc 383) was never the
  binding constraint — they never conflicted — but the canary set is intact.
- **Seq 1145** (the §2.2 counterexample: wrong, conf 874, mrgF 10410,
  agree==1): PROVISIONAL_INSTALL (as under frozen rules; it was already
  provisionally installed before the re-brief). It did NOT receive
  REVISED_INSTALL (it is a singleton; cf1's corroboration requirement held).

## O3c measurement (the 125) — prediction PARTIALLY FALSIFIED

Pre-registered prediction: no per-task margin threshold separates the
(g)-blocked correct trials from wrong trials.

- colorconst: 0 correct above wrong-max → holds.
- colordisc: 0 correct above wrong-max → holds.
- **pitchdisc: 44 correct trials above the wrong-max (mrgF > 34,186) → FALSIFIED.**
- **timbredisc: 5 correct trials above the wrong-max (mrgF > 382) → FALSIFIED.**

Discovery for prereg (f): a high-margin override on the (g) check could
convert 49 (g)-blocked trials with zero wrong admissions on this battery.
O3 does NOT install on this threshold (retrospective fitting; explicitly
out of scope per the prereg). O1's "sense-calibration gap" diagnosis is
refined: for pitchdisc/timbredisc the gap is addressable by calibration;
for colorconst/colordisc it is not (no threshold separates).

## Why O3-rebriefed dies (on its own kill bar)

KB-O3a required 100/128. The gate-side repair converts 78. The remaining 50
are multiply-poisoned suppressions that no gate rule can fix without
overriding the program's own FAIL history — which is prereg (f) territory.
The blockage O1 diagnosed is real, and the gate-side repair is insufficient:
O3-rebriefed as a conversion offense is KILLED, as its own kill bar
predicted.

What survives: the safety bars all pass (the repair installs no wrong
percepts), RK-3 rises to 74.50% without breaking RK-2, and the O3c
measurement hands prereg (f) a concrete 49-trial calibration target.

## Evidence

- `src/o3.zag` — the instrument (pure Zag).
- `src/gen_case_o3.py` — glue (reformats frozen bytes; not the instrument).
- `src/R33_NATIVE_IO_V1.zag`, `src/R33_NATIVE_SHA256_V2.zag` — substrate.
- `case_o3.txt` — frozen case stream (11,840 rows).
- `metrics_run1/2/3.txt` — byte-identical metric outputs (sha256 above).
- `PREREG_O3_REBRIEFED.md` — committed alone before the build
  (commit `6f4713a72578a54b6c147f976b5aa08be869d230`).
