# D4 battery — RUNLOG (Crew B-D4, 2026-09-24)

## Freeze sequence (honest record)
- Extracted frozen base prereg from bfab522a by script →
  PREREG_D4_FROZEN_bfab522a.md (SHA e601e8dd…).
- Drafted Amendment 1 (F10c testability) BEFORE any frozen commit.
- A scratch implementation (d4batt.zag) was written LOCALLY before the
  amendment was committed — a freeze-sequence violation in the working
  process. It was NEVER committed and never ran as evidence.
  Remediation: the amendment + generator + frozen fixtures were committed
  ALONE as 6e035891; the implementation was committed separately as
  9260bc9e only after the amendment froze. The pre-freeze scratch is
  discarded; nothing from it entered the evidence chain except the
  corrected source below.
- Bugs caught in LOCAL smoke tests (pre-freeze, not evidence):
  1. Honest conf/meas parse aliasing: `getf(10)` overwrote `tmp` before
     `p_atoi(tmp,0,cl)` read the conf field → conf read as meas prefix.
     P7 leg looked right (self-consistent warrant) but the S-profile
     band check rejected everything (honfire=0). Fixed: parse each field
     immediately after its getf.
  2. M1 formula: the draft amendment cited "(as probed: 1.7 vs 0.7)" —
     the frozen probe's P3 actually reports dpc_x100 = 136 vs 11.
     M1 redefined as an exact replication of the probe's P3 method
     (ilog2 bits per class, +1 smoothing; dpc_x100 = 100*bits*10 /
     (3*mean_cost_x10_per_percept)); predictions updated to 47 vs ≈16.
  3. Targeted-elicitation counters et1..et3 counted PING firings on
     non-PING-targeted fixtures; corrected to count target_action firings
     (0 by construction for REACH/MOVE_SENSOR/ASK).

## Frozen runs
- Source: committed blob 9705164c… (d4batt.zag), SHA256
  2f222e977618a10008d8382b14ce2f8214b8bb0c2a74913e15c96fd23a0b3b5d —
  byte-identical to the smoke-tested source.
- Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
  (pinned). Built in a clean dir with the R33_NATIVE_IO_V1.zag import
  shim; binary d4batt_frozen (79036 bytes main, 0 external tools).
- Fixtures: fixtures_ledger.txt (SHA 0c5e2c0d…), d4_classS.txt
  (70879da8…), d4_classA.txt (7636e7ab…), d4_classM.txt (a1b93d77…) —
  all matching the frozen amendment §A7.
- 3 runs, stdout captured: run1.out / run2.out / run3.out
  SHA256 (all three): 820bdcd37f1d1c222a6532e6195488db5311a1b17c30c11bd0bb631f94271ead
  → K6 PASS (byte-identical).
- No randomness anywhere: deterministic fixture order, ledger-derived
  sampler, integer arithmetic only.

## Committed predictions vs measured (all hit)
| K | predicted | measured |
|---|---|---|
| K1 | FIRES (25%<50%) | FIRES |
| K2 | FIRES: P10P 120, SWAP ≈30; targeted 30 / ≈8–11 | 120 / 30; et0=30/11, et1-3=0 |
| K3 | FIRES (120/120) | 120/120 |
| K4 | P7 wins (47 vs ≈16) | 47 vs 16 |
| K5 | PASS (swap ≈17/100 ≤ 25) | 18/100 |
| K7 | PASS (swap ≈17% ≤ 25%) | 18% |
| K8 | PASS (swap S ≈80% < 100%; honest 252=252) | 97/120=81%; 252=252 |
| M2 | premium ≈3–4 bits | 3 bits (P10P leg; 4 on ORA leg) |
