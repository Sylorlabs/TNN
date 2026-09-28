#!/usr/bin/env python3
# region1_analyze.py — REGION-1 analyzer (fable R1 Q4).
# Signal-level measurement of phase discontinuity at the 11 region boundaries.
# Method: two-sided least-squares phase fit. For boundary k at sample n_b,
# with region frequencies f_lo (before) and f_hi (after):
#   fit window A = last W samples before n_b at f_lo  -> phase phi_lo
#   fit window B = first W samples after n_b at f_hi  -> phase phi_hi
#   theta_lo(t_b) = phi_lo + 2*pi*f_lo*(n_b-1 - t_refA)/SR
#   theta_hi(t_b) = phi_hi + 2*pi*f_hi*(n_b   - t_refB)/SR
#   discontinuity_k = |wrap_pi(theta_hi - theta_lo)|
# Bar: mean discontinuity < 0.1 rad.
# Cross-check: renderer-analytic phases from the .diag file must agree with
# the signal fit to < 0.02 rad (validates the measurement chain).
import struct, math, sys

SR = 44100
W = 2048  # fit window samples each side

def wrap_pi(x):
    while x > math.pi: x -= 2*math.pi
    while x < -math.pi: x += 2*math.pi
    return x

def fit_phase(samples, f0, t_ref):
    # model s[i] = A*cos(2*pi*f0*(t_ref+i)/SR + phi); solve phi via projection
    C = 0.0; S = 0.0
    w = 2*math.pi*f0/SR
    for i, v in enumerate(samples):
        th = w*(t_ref+i)
        C += v*math.cos(th)
        S += v*math.sin(th)
    # C ~ (A*N/2) cos phi ; S ~ -(A*N/2) sin phi
    return math.atan2(-S, C)

def load_raw(path):
    d = open(path,'rb').read()
    n = len(d)//2
    return struct.unpack('<%dh' % n, d)

def load_diag(path):
    out = []
    for line in open(path):
        p = line.split()
        if len(p) == 4 and p[0] == 'K':
            out.append((int(p[1]), int(p[2]), int(p[3])))
    return out

def analyze(raw_path, diag_path, label):
    s = load_raw(raw_path)
    diag = load_diag(diag_path)
    discs = []
    max_diag_err = 0.0
    for (k, ph_before_q32, ph_after_q32) in diag:
        n_b = k*220500  # boundary sample index
        f_lo = 440 + (k-1)
        f_hi = 440 + k
        winA = s[n_b-W:n_b]
        winB = s[n_b:n_b+W]
        phi_lo = fit_phase(winA, f_lo, n_b-W)
        phi_hi = fit_phase(winB, f_hi, n_b)
        th_lo = phi_lo + 2*math.pi*f_lo*(n_b-1-(n_b-W))/SR
        th_hi = phi_hi  # phi_hi is already phase at t_ref=n_b
        disc = abs(wrap_pi(th_hi - th_lo))
        discs.append(disc)
        # cross-check vs renderer-analytic Q32-turn phases
        a_lo = (ph_before_q32/2**32)*2*math.pi
        a_hi = (ph_after_q32/2**32)*2*math.pi
        ana_disc = abs(wrap_pi(a_hi - a_lo))
        max_diag_err = max(max_diag_err, abs(wrap_pi(disc - ana_disc)))
    mean = sum(discs)/len(discs)
    mx = max(discs)
    print(f"== REGION-1 {label} ==")
    print(f"  per-boundary discontinuity (rad): " +
          " ".join(f"{d:.3f}" for d in discs))
    print(f"  mean={mean:.4f} rad  max={mx:.4f} rad")
    print(f"  bar mean<0.1 rad: {'PASS' if mean < 0.1 else 'FAIL'}")
    print(f"  signal-vs-analytic max disagreement: {max_diag_err:.4f} rad " +
          f"({'OK' if max_diag_err < 0.02 else 'MEASUREMENT SUSPECT'})")
    return mean

if __name__ == "__main__":
    # args: label raw diag [label raw diag ...]
    a = sys.argv[1:]
    means = {}
    for i in range(0, len(a), 3):
        means[a[i]] = analyze(a[i+1], a[i+2], a[i])
    print("== summary ==")
    for k, v in means.items():
        print(f"  {k}: mean discontinuity {v:.4f} rad -> {'PASS' if v < 0.1 else 'FAIL'}")
