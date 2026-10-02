# T-distribution measurement, wave-20260924-1721pdt (DIAGNOSTIC, read-only)

Status: diagnostic measurement evidence. Not candidate evidence. Nothing in
this file was tuned, and no render was produced from it. It characterizes the
march-mean transmittance field T(P) whose miscalibrated gate discarded G1 in
1421pdt, and it supplies the measured quantiles that freeze the 1721pdt gate.

## Method (pure Zag, no Python)

Program: g1/measure/g1_measure_t.zag, compiled with the pinned toolchain
src/tools/toolchain/znc_linux_x86_64_abed8aa1
(sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
The field machinery (g1_density, g1_transmittance with N=12, g1_is_sky,
r8c_ridge_y) is the verbatim code copied from the frozen 1421pdt mechanism
file, so the measured field is exactly the field the 1421pdt gate acted on.

Baseline gate, verified first: the r8c baseline was rebuilt from the
committed 1421pdt baseline source and rendered byte-identical to the S14
record: sha256 e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d.
The T field is canvas-independent (a pure function of the frozen D field and
sun position), so measuring on the rebuilt baseline is exact.

Raw program output: g1/measure/measure_out.txt (42 lines).

## Sanity check: the 1421pdt record is reproduced exactly

n_sky = 325786, T_mean = 569, T_std = 92. These match the 1421pdt verdict
record to the integer, confirming the measurement machinery is identical to
the frozen mechanism machinery.

## Measured T distribution (sky pixels, N=12 march toward S=(110,300))

- min 383, max 725, mean 569, std 92 (population, integer math)
- moment skewness -0.376 (left-skewed; median 592 above mean 569)
- exact quantiles from a 1025-bin histogram:
  p01 392, p05 409, p10 431, p25 490, p50 592,
  p75 640, p90 682, p95 689, p99 708
- fraction above the old 707 gate: 112 per 10000 = 1.12 percent.
  A normal field with mean 569 and std 92 would put 6.68 percent above
  mean + 1.5 sigma. The upper tail is far thinner than normal: this is the
  measured form of the 1421pdt attribution caveat. The 1.5-sigma rule
  promised about 7 percent and delivered 1.1 percent because the field is
  left-skewed with a thin upper tail, not normal.

## Radial structure (the geometry/gate coupling, measured)

Radial bands of 128 px around the sun, sky pixels with r >= 24 px:

band, r range, count, mean_T, std_T
0, 0-127, 39673, 447, 41
1, 128-255, 55252, 461, 53
2, 256-383, 58444, 542, 55
3, 384-511, 39466, 616, 29
4, 512-639, 20880, 650, 27
5, 640-767, 34268, 654, 30
6, 768-895, 61015, 652, 41
7, 896+, 14999, 633, 55

The radial gradient is steep: near-sun band mean_T = 447, far band
mean_T = 654, a 207-step spread against a within-band std of 27-55. A
global gate on T therefore systematically excludes near-sun pixels: the
gate and the geometry were coupled. The 1721pdt prereg decouples them by
gating on the band-normalized score below.

## Band-normalized clarity score s(P) (the decoupling input)

s(P) = (bandmean_T[b] - T(P)) * 1024 / max(bandstd_T[b], 1), x1024 units;
positive means clearer than the pixel's radial band typical. Pooled over
the 323997 gated sky pixels (r >= 24):

s quantiles: p01 -1856, p05 -1408, p10 -1152, p25 -768, p50 -64,
p75 640, p90 1088, p95 1280, p99 1856.

Frozen gate for the 1721pdt prereg: SGATE = 1088, the measured 90th
percentile of s. About 10 percent of gated sky pixels pass the clarity
gate; the directional-contrast predicate then keeps only those whose
sunward sightline is also the angularly clearest direction.

## Interpretation for the prereg

1. The T field is left-skewed (-0.376) with a thin upper tail. Any gate
   derived from a normality assumption is unsafe on this field; the new
   gate is a measured quantile, not a sigma multiple.
2. The field has a strong radial gradient (207-step band-mean spread),
   so a global gate confounds geometry with clarity. The new gate acts on
   the radially normalized score, decoupling the two.
3. The band means and stds above are frozen as the normalization
   constants; the baseline byte-identity gate guarantees the field they
   describe is the field the implementation will see.
