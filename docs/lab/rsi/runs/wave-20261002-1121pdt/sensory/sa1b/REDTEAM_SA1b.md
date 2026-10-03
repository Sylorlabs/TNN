# RED TEAM SA1b: short-time adaptive harmonic rejection

Frozen prereg: PREREG_SA1b.md (committed alone ea028fa71). Mechanism: STAHR.
Result: child NEVT=0, speech NEVT=1. KB1 (>= 16 both atoms) FAILS. BUILD-FAIL.

## R1: stdout byte-verification
sa1b_isolate and sa1b_check use the single preallocated buffer + cursor emit
helpers (e1str/e1i64/e1f64) + one _zag_raw_syscall write. No _zag_print for
dynamic content. Outputs cross-checked: checker NEVT/nsrc match isolator logs
(child 0/220500, speech 1/220500); KB0 fractions match (0.80, 1.00); P matches
(16423, 20107). No miscompile signature. PASS.

## R2: anti-leakage (R2 = max|amp| / short-time hrms, kill if > 10)
Child: vacuous (0 events). Speech: 144.61 / 1118.98 = 0.129. PASS, no kill.
The global-P bound (ar <= P) held: speech maxamp 144.61 << P 20107.

## R3: determinism and timing
EVT byte-identical x3 per atom (sha256 49c90f8b child, e73581c5 speech).
Baseline render byte-identical x3; variant render byte-identical x3.
Isolator wall: child 3.5 s, speech 3.4 s. No RNG in decision paths. PASS.

## R4: switch-point clustering
0-1 events total; clustering analysis moot. The +-2 exclusion zones were
exercised (no events within 2 samples of any bpt(f)). No kill.

## R5: KB0 degeneracy re-tune kill
KB0 PASSED on both atoms (deffrac 0.80/1.00 >= 0.50; max/min 11.20/10.84 >
1.15), so the R5 re-tune kill does not trigger. The failure is NOT degenerate
T0s; it is downstream.

## Root cause: integer-period quantization washout (mechanism flaw, proven)
1. dev_probe (diagnostic, not in battery) measured per-frame signal RMS vs
   residual RMS on child: voiced frames with correct T0 barely reject.
   Frame 15 (T0=116, the true pitch): 4492 -> 4499 (0% rejection).
   Frame 12 (T0=112): 3486 -> 2025 (42%). Frame 11: 822 -> 555 (33%).
2. dev_synth generated a mathematically perfect period-116 sine WAV.
   dev_probe on it: T0=116 in all 25 frames, residual RMS 0.00-0.05
   (machine precision). The phase-locked mean implementation is CORRECT;
   when the true period is an integer, rejection is total.
3. Therefore the failure is physics, not code: real pitch is non-integer
   (e.g. 116.3). Integer-lag binning accumulates phase error linearly:
   after k periods, error = k * (true - lag)/true cycles. A 0.25 s frame at
   T0=116 spans ~95 periods; a 0.3-sample period error drifts 0.24 cycles
   across the frame, attenuating the 95-period mean to ~65% amplitude and
   leaving 58-100% of harmonic energy in the residual.
4. The 6x local-contrast gate was designed for impulses in a CLEAN residual.
   The residual is harmonic-dominated (crest factor 2-3, far below 6), so
   the gate never fires: child 0 candidates, speech 1 candidate (contrast
   6.13, below the KB3 bar of 10).

## Knowledge vs architecture
KNOWLEDGE. The prereg bet that 0.25 s frames are "short enough that integer
period phase locking works". That bet was wrong in a precise, now-measured
way: washout scales with PERIODS PER FRAME (~95), not seconds. Short-time
framing alone cannot fix harmonic rejection; the averaging window must span
few periods (2-5) or period estimation must be sub-sample. The per-frame T0
adaptation itself works (KB0 passes; T0 tracks 112-139 across child frames);
it is the full-frame phase-locked MEAN built on those T0s that washes out.
A future mechanism needs sub-sample period precision or single-period
(delay-line) prediction. That is a NEW mechanism requiring a NEW prereg,
not a patch to SA1b.

## Verdict on red team
No harness flaw, no miscompile, no determinism failure, no leakage.
The mechanism fails on its own terms. BUILD-FAIL stands.
