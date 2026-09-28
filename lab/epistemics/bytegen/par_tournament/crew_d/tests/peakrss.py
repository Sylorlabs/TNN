#!/usr/bin/env python3
"""Run a command, report wall-clock and peak RSS (VmHWM) by polling
/proc/<pid>/status. Zero RNG involved; purely observational."""
import subprocess, sys, time, os

cmd = sys.argv[1:]
t0 = time.time()
p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
peak = 0
pidpath = f"/proc/{p.pid}/status"
while p.poll() is None:
    try:
        with open(pidpath) as f:
            for line in f:
                if line.startswith("VmHWM:"):
                    kb = int(line.split()[1])
                    if kb > peak:
                        peak = kb
                    break
    except FileNotFoundError:
        pass
    time.sleep(0.05)
dt = time.time() - t0
print(f"cmd={' '.join(cmd)}")
print(f"wall_s={dt:.2f} peak_rss_kb={peak} rc={p.returncode}")
