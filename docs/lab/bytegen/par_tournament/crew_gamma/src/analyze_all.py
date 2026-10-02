#!/usr/bin/env python3
"""CREW GAMMA — head-to-head metrics for every variant x fixture.

For each WAV: peak, rail% (+-32767), RMS, crest, per-1s-window RMS ratio vs
the control render (dynamics preservation: uniform scaling => constant
ratio), and the 9-bar gate (analyze_gate port).
Deterministic, zero RNG.
"""
import sys, os, struct
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_gate import gate as gate9, read_wav

BASE = os.path.expanduser("~/workspace/tnn-lab/bytegen/par_tournament/crew_gamma")
VARIANTS = ["ctl", "h1", "h2a", "h2b", "h2c", "h2d", "revert"]
FIXTURES = [("f3song_hifi.wav", "song"), ("f3mood_happy.wav", "happy"),
            ("f3mood_scary.wav", "scary"), ("f3mood_calm.wav", "calm")]

def stats(pcm):
    nsamp = len(pcm)
    peak = np.abs(pcm).max()
    rail = ((pcm == 32767) | (pcm == -32768)).mean() * 100.0
    rms = np.sqrt((pcm.astype(np.float64) ** 2).mean())
    crest = (peak / 32768.0) / (rms / 32768.0) if rms > 0 else 0.0
    return peak, rail, rms, crest

def win_rms(pcm, w=44100):
    n = len(pcm) // w
    r = pcm[:n * w].reshape(n, w).astype(np.float64)
    return np.sqrt((r ** 2).mean(axis=1))

def main():
    ctl_pcm = {}
    for fn, fx in FIXTURES:
        ctl_pcm[fx] = read_wav(os.path.join(BASE, "out", "ctl", fn))
    print("variant fixture peak rail_pct rms crest winrms_ratio_mean winrms_ratio_maxdev_db gate")
    for v in VARIANTS:
        for fn, fx in FIXTURES:
            p = os.path.join(BASE, "out", v, fn)
            pcm = read_wav(p)
            peak, rail, rms, crest = stats(pcm)
            c = ctl_pcm[fx]
            n = min(len(pcm), len(c)) // 44100
            rv = win_rms(pcm)[:n]
            cv = win_rms(c)[:n]
            with np.errstate(divide="ignore", invalid="ignore"):
                ratio = np.where(cv > 1e-9, rv / np.where(cv < 1e-9, 1e-9, cv), np.nan)
            ratio = ratio[np.isfinite(ratio)]
            rmean = ratio.mean()
            # max deviation of per-window ratio from the mean, in dB
            dev = np.abs(20 * np.log10(ratio / rmean))
            devmax = dev.max() if len(dev) else float("nan")
            bars = gate9(p, 2.0)
            fails = sum(1 for _, val, bar in bars if val > bar)
            clipv = [val for name, val, bar in bars if name == "G-CLIP"][0]
            print("%-6s %-5s %6d %7.3f %9.1f %6.3f %8.5f %8.3f %d/9 %s" %
                  (v, fx, int(peak), rail, rms, crest, rmean, devmax, 9 - fails,
                   " ".join("%s:%s" % (n_, "P" if val <= bar else "F")
                             for n_, val, bar in bars)))

main()
