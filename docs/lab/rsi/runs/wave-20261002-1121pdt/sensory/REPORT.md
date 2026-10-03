# SENSORY Lane Final Report, wave-20261002-1121pdt (queue item 11)

Branch lane-sensory-20261002-1121pdt. Pure Zag, safebin only (which python3
empty, znc at ~/safebin/znc; NAMECHECK.md f3ee683f5). No em-dashes (verified).

## SA1b: SHORT-TIME ADAPTIVE HARMONIC REJECTION -- VERDICT BUILD-FAIL

Prereg committed alone ea028fa71; commit-order self-check PASS.
New mechanism (not SA1 re-tune): 0.25s frames, per-frame integer-lag T0,
per-frame phase-locked harmonic mean, nearest-center overlap assignment.

Sealed battery (commit 172017586), byte-identical x3 everywhere:
- Child: NEVT=0. Speech: NEVT=1. KB1 (bar 16) FAILS both atoms. Dispositive.
- KB0 PASS (deffrac 0.80/1.00; T0 max/min 11.2/10.8). T0 adaptation works.
- KB2 FAIL (child corr UNDEFINED; speech frac_ge10 0.00). KB3 FAIL (6.13 < 10).
- R2 anti-leakage PASS (0.129). Child variant == baseline bit-for-bit.

Root cause (REDTEAM_SA1b.md, synthetic control proves it): integer-period
quantization washout. Perfect period-116 sine -> residual 0.00 (implementation
CORRECT). Real speech: phase error accumulates over ~95 periods/frame,
attenuating the mean to ~65%, leaving 58-100% harmonic energy in the residual.
The 6x gate never fires on harmonic-dominated residual. The prereg bet was
wrong in a measured way: washout scales with PERIODS PER FRAME, not seconds.
KNOWLEDGE result. Fix needs a new mechanism + new prereg. No patch allowed.

## H5: PENUMBRA-DILATED CIRRUS SHADOW FIELD -- BATTERY RUNNING, VERDICT PENDING

Prereg committed alone c9da6ec2e; commit-order self-check PASS.
New mechanism (not H4 re-tune): frozen H4 cirrus field (seeds 601/602
byte-identical) through a 5-tap max kernel (center + 4 at R_P=0.03 rad,
renormalized) before the H4 shadow accumulator. Diff contract machine-verified:
3 added functions + 4 changed lines only (commit 041e54f5a).

Status:
- 256 smoke: mechanism fires. 6924/196608 pixels differ (3.5% vs H4 0.67%).
  All-darkening, zero sky/moon change at 256. Cost 0.97x baseline.
- h5_verify.zag: white-box recompute mirrors frozen block verbatim (caught
  and fixed a tap-renormalization mismatch pre-battery, dd0a8c388). Compiles
  clean. Output via single-buffer emit idiom.
- 1024 sealed battery (run_h5.sh) RUNNING in background (proc_0568aec7790a):
  2x baseline gate + validator + 3x variant + H5-KB1..KB9. At current pace
  (~33 rows/min under load) completes in ~2 hours. The renders in flight use
  the correct frozen math; only the verifier binary was swapped (fixed).

If H5 passes all bars: I will prepare the sealed blind A/B pair +
JUDGE_BRIEF.md (RENDER_SHA, FIRST_RENDERED_WAVE=wave-20261002-1121pdt,
COMPONENT_LINEAGE, NEW_KNOWLEDGE_CLAIM) and mark READY-FOR-JUDGE. Not done yet.

## Commits (lane branch, pathspec-only)
f3ee683f5, ea028fa71, c9da6ec2e, 172017586, 041e54f5a, dd0a8c388, c195a19fd,
1a3818545.

## Queued next
H5 verdict + red-team T2/T3/T5 on battery completion. SA1b is terminal
(BUILD-FAIL); its washout finding informs the next audio mechanism prereg.
