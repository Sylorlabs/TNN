# D4 intervention-locus battery — VERDICT (Crew B-D4, 2026-09-24)

Prereg: PREREG_D4_AMEND1_F10c (frozen 6e035891, amends bfab522a base).
Runs: 3× byte-identical, stdout SHA
820bdcd37f1d1c222a6532e6195488db5311a1b17c30c11bd0bb631f94271ead.

## Leg results (720 percepts: 360 honest + 120 S + 120 A + 120 M)

- LEG P7:  ins_h=252 ins_s=120 ins_a=0 ins_m=120 hc_withhold=108
  cost=3024.0 bits(S/A/M)=0/6/0 dpc_x100=47
- LEG P10P: ins_h=360 ins_s=7 ins_a=120 ins_m=6 fired=491 honfire=251
  elicit_any=120 et0=30 et1=0 et2=0 et3=0
  cost=10311.0 bits=3/0/4 dpc_x100=16
- LEG SWAP: ins_h=252 ins_s=97 ins_a=0 ins_m=91 fired=135 honfire=80
  elicit_any=30 et0=11 et1=0 et2=0 et3=0
  cost=5859.0 bits=0/6/0 dpc_x100=24
- LEG M2C: s_ins=120 s_bits=0 premium_bits=3 (live-d 3 bits − known-d 0)
- LEG ORA: s_ins=3 s_bits=4 (oracle-routed upper bound, labeled)

## K evaluations

- K1 FIRES — frozen repertoire coverage 25% < 50% (battery 6-class: 17%).
- K2 FIRES — elicitation_any: P10P 120/120, SWAP 30/120; targeted
  breakdown: PING-targeted 30 (P10P) / 11 (SWAP), REACH/MOVE_SENSOR/ASK
  targeted 0 (no trigger exists). Elicitation differential (SWAP):
  P(fire|M) − P(fire|honest) = 25% − 22% = +3pp — the adversary gains
  firing control by profile-matching. F10c CONFIRMED as a measured rate;
  P10 BARRED from promotion beyond specialist.
- K3 FIRES — P7 installs 120/120 S (honest-blind by construction).
- K4: P7 WINS — discrimination-per-cost dpc_x100 = 47 (P7) vs 16 (P10P),
  replicating the frozen probe's P3 direction (136 vs 11 at 2 classes).
- K5 PASS — SWAP firing 18/100 ≤ 25; PING reversible by construction.
  (P10-primary: 68/100 — would fail as a general policy.)
- K6 PASS — 3/3 byte-identical stdout.
- K7 PASS — SWAP delayed 18% ≤ 25%. (P10-primary: 68% — fails as
  general policy; delay is the binding constraint.)
- K8 PASS — SWAP S-install 97/120 (81%) < P7 120/120 strict ✓;
  SWAP honest retention 252 = P7 honest retention 252 (≥ 252−18) ✓.

## Discrimination-per-cost
P7: 6 bits / 3024.0 = 1.98e-3 (dpc_x100=47).
P10-primary: 7 bits / 10311.0 = 6.8e-4 (dpc_x100=16).
P7 delivers ~2.9× the discrimination-per-cost at ~1/3.4 the per-percept
cost (4.2 vs 14.3). Cost ratio P10/P7 = 5.0× (frozen).

## Fallback-swap behavior
All 720 percepts pass through P7; 108 complex-honest WITHHOLDs stand
(P10 never sees them); P7 INSTALL + S-suspect profile + 1/4 ledger
sampler → 135 P10 invocations (18.75%). Elicitation residual on M in
swap: 30/120 = 25% (named, F10c honesty requirement). Honest retention
identical to P7 standalone (252/252). swap_survive = 1 (K1 named, K2 rate
named, K5, K6, K7, K8 all pass).

## Verdict
- Locus = P7. K1 fires (coverage), K4 goes to P7 (discrimination-per-cost).
- P10 = Class-S specialist fallback via the §A6 swap; swap SURVIVES all
  bars (K5/K6/K7/K8 pass; K1 named; K2 rate named as residual).
- F10c = CONFIRMED_RATE_NAMED (elicitation_any 120 P10P / 30 SWAP;
  targeted: PING only). F10b = COVERAGE_25PCT_NAMED.
- Every committed prediction in the frozen amendment hit (see RUNLOG).
