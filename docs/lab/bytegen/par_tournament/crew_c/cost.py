#!/usr/bin/env python3
"""COST battery: wall-clock + peak RSS (VmHWM) for a render command."""
import subprocess, sys, time, os

def measure(cmd):
    t0 = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    peak = 0
    while p.poll() is None:
        try:
            with open(f"/proc/{p.pid}/status") as f:
                for ln in f:
                    if ln.startswith("VmHWM"):
                        kb = int(ln.split()[1])
                        if kb > peak:
                            peak = kb
                        break
        except FileNotFoundError:
            break
        time.sleep(0.005)
    dt = time.time() - t0
    return dt, peak, p.returncode

if __name__ == "__main__":
    # args: label binary plan outfile nruns
    label, binary, plan, out, n = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
    dts, rss = [], []
    for i in range(n):
        dt, peak, rc = measure([binary, plan, out, "seqmix"])
        assert rc == 0, f"render failed rc={rc}"
        dts.append(dt)
        rss.append(peak)
    dts.sort()
    print(f"{label}: wall median={dts[n//2]:.2f}s min={dts[0]:.2f}s max={dts[-1]:.2f}s peakRSS_max={max(rss)}KB")
