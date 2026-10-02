# SENSORY Lane Report, wave-20261002-1121pdt (queue item 11)

Branch lane-sensory-20261002-1121pdt. Pure Zag, safebin only (which python3
empty, znc at ~/safebin/znc, recorded in NAMECHECK.md f3ee683f5).

## SA1b: SHORT-TIME ADAPTIVE HARMONIC REJECTION (STAHR) -- BUILD-FAIL

Prereg PREREG_SA1b.md committed alone ea028fa71 (commit-order self-check PASS).
New mechanism (not an SA1 re-tune): 0.25 s frames, per-frame integer-lag T0,
per-frame phase-locked harmonic mean, nearest-center overlap assignment,
frame-adaptive amplitude floor.

Sealed battery (run_sa1b.sh), commit 172017586:
- Determinism: EVT byte-identical x3 per atom; baseline render x3; variant x3.
- Child: NEVT=0 (KB1 bar 16: FAIL). Speech: NEVT=1 (FAIL).
- KB0 PASS both atoms (deffrac 0.80/1.00; T0 max/min 11.20/10.84 > 1.15).
  The per-frame T0 adaptation itself works; T0 tracks pitch drift.
- KB2: child (ii) UNDEFINED (zero event train); speech (iii) 0.00 < 0.50 FAIL.
- KB3: child 0.00, speech 6.13 < 10 FAIL. R2 anti-leakage PASS (0.129).
- Child variant render == baseline bit-for-bit. Speech variant differs by
  exactly one impulse (amp 144.6).

Root cause (REDTEAM_SA1b.md, proven by synthetic control): integer-period
quantization washout. A perfect period-116 sine gives residual 0.00-0.05
(implementation CORRECT); real speech with non-integer pitch washes out
because phase error accumulates linearly over ~95 periods/frame (0.3-sample
error -> 0.24 cycles drift -> mean attenuated to ~65%). The 6x local-contrast
gate then never fires on the harmonic-dominated residual. The prereg bet
"0.25 s frames fix non-stationarity" was wrong in a measured way: washout
scales with PERIODS PER FRAME, not seconds. KNOWLEDGE result: a future
mechanism needs sub-sample period precision or few-period prediction.
New mechanism + new prereg required; no patch permitted.

## H5: PENUMBRA-DILATED CIRRUS SHADOW FIELD (PDSH) -- IN PROGRESS

Prereg PREREG_H5.md committed alone c9da6ec2e (commit-order self-check PASS).
New mechanism (not an H4 re-tune): frozen H4 cirrus field (seeds 601/602
byte-identical) sampled through a 5-tap max kernel (center + 4 taps at
frozen R_P = 0.03 rad in the perpendicular frame) before the H4 shadow
accumulator. Diff contract vs r11_baseline verified: 3 added functions +
4 changed lines only.

Implementation committed 041e54f5a (h5_terrain.zag, h5_verify.zag, battery).
256 smoke: mechanism fires, 6924/196608 pixels differ (3.5% vs H4 0.67%),
all-darkening direction, cost ratio 0.97x.

Sealed 1024 battery (run_h5.sh) RUNNING in background: 2x baseline gate,
validator, 3x variant, kill bars H5-KB1..KB9 via h5_verify (incl. KB9
penumbra-specificity: >50% of shadowed pixels must have center-tap csh >
0.995). Verdict, red team, and judge-brief (if PASS) to follow on completion.

## Commits
f3ee683f5 NAMECHECK < ea028fa71 PREREG_SA1b < c9da6ec2e PREREG_H5 <
172017586 SA1b impl+eval < 041e54f5a H5 impl < dd0a8c388 h5_verify
renormalization fix < c195a19fd interim REPORT.
