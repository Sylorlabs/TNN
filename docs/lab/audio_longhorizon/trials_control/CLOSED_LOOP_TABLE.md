# CLOSED_LOOP_TABLE — Phase B2b §2c (20 real refs)

## Battery verdict — FRESH STATE (loopfresh, depths 1–20)

| Criterion | Bar | Result | Verdict |
|-----------|-----|--------|---------|
| ERR(3)/ERR(0) | ≤ 0.80 | 0.951 | **FAIL** |
| Wilcoxon p (one-sided) | < 0.01 | 0.275 | **FAIL** |
| Strictly improve | ≥ 16/20 | 10/20 | **FAIL** |
| Sign agreement | ≥ 80% | 76.5% | **FAIL** |
| Unstable cases | ≥5 fails battery | 4 | PASS |
| Sawtooth cases | (flag) | 6 | — |

**§2c FRESH-STATE: FAIL.** The closed-loop correction does not reliably improve
over open-loop. Mean ERR ratio 0.95 (near-zero net improvement); only 10/20
cases strictly improve; 6 show sawtooth oscillation; 4 unstable.

### Cause analysis (per-case ERR decomposition)

The CV (prosody) term dominates high ERRs: cases d1/d2/d4/d5 have ERR(0)≈0.52–0.72
with cv_term=0.5 (scorer CV outside ±25%), f0_term small (0.02–0.22), env correct.
The loop adjusts vibrato but saturates at the 0.5-depth clamp (ANOM-004); refs
with CV above the vocabulary ceiling are unfixable by correction.

F0 destabilization: d16 (f0=1010.8 Hz) ERR 0.150→0.711; d3 (f0=145.7) 0.021→0.034.
The loop applies corrections even when the open-loop plan is already good, and
native-hearing biases (high-F0, vibrato-biased F0 per ANOM-005) can drive the
plan away from the reference.

Low-F0 refs (d19/d20, f0<125 Hz): F0 term excluded from ERR by prereg §5; ERR
stuck at 0.500 (env or cv miss the loop does not repair).

### B-F1 bearing (planner vs loop for prosody)

The prosody failures bear on the PLANNER side: the vibrato-depth clamp (0.5) and
the 5 Hz sinusoidal vocabulary saturate before reaching high-CV references. The
loop DOES attempt CV correction (vib adjustments visible in journal DEVIATION
lines); the limitation is representational, not a loop-stability failure. The
F0 destabilization cases are a separate loop-reliability issue, not prosody.

No structural decision is made here; the bearing is reported for B-F1.

## Battery verdict — DEEP STATE (r1, depths 121–140)

| Criterion | Bar | Result | Verdict |
|-----------|-----|--------|---------|
| ERR(3)/ERR(0) | ≤ 0.80 | 0.944 | **FAIL** |
| Wilcoxon p (one-sided) | < 0.01 | 0.045 | **FAIL** |
| Strictly improve | ≥ 16/20 | 13/20 | **FAIL** |
| Sign agreement | ≥ 80% | 88.2% | PASS |
| Unstable cases | ≥5 fails battery | 3 | PASS |
| Sawtooth cases | (flag) | 4 | — |

**§2c DEEP-STATE: FAIL.** Better than fresh (13/20 vs 10/20 improve; sign
agreement 88% vs 77%), but still misses all improvement bars. The history
helps the sign agreement (recalled deltas guide corrections) but does not
rescue the fundamental reliability issue.

## Overall §2c

**FAIL** on both fresh and deep state. The closed-loop correction, as
implemented, does not reliably improve over open-loop control on real
references. The loop helps in some cases (large initial errors get fixed)
but hurts in others (good initial plans get destabilized), with near-zero
net effect.
