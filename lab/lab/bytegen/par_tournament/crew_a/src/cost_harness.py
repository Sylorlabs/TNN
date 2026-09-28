#!/usr/bin/env python3
"""cost_harness.py — interleaved wall-clock + peak-RSS runs of A vs native.
Usage: cost_harness.py <plan> <reps> ; binaries ./render_a, ./render_nat in cwd.
Prints per-run wall seconds and peak RSS (VmHWM) in MB.
"""
import os, subprocess, sys, time

PLAN = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/workspace/tnn-lab/bytegen/fixture/plan_v1.txt")
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 6

def peak_rss_mb(pid):
    try:
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                if line.startswith("VmHWM:"):
                    return int(line.split()[1]) / 1024.0
    except FileNotFoundError:
        return 0.0
    return 0.0

def run(cmd, out):
    t0 = time.time()
    p = subprocess.Popen(cmd + [out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    peak = 0.0
    while True:
        alive = False
        try:
            with open(f"/proc/{p.pid}/stat") as f:
                st = f.read().rsplit(')', 1)[1].split()
                alive = st[0] != 'Z'
        except FileNotFoundError:
            alive = False
        if not alive: break
        r = peak_rss_mb(p.pid)
        if r > peak: peak = r
        time.sleep(0.01)
    # reap with resource usage: CPU seconds (robust under VM contention)
    _, status, rusage = os.wait4(p.pid, 0)
    cpu = rusage.ru_utime + rusage.ru_stime
    wall = time.time() - t0
    return wall, cpu, peak, status

def main():
    a_times, n_times, a_rss, n_rss = [], [], [], []
    for i in range(REPS):
        # interleave: alternate who goes first each rep
        order = [("A", ["./render_a", PLAN, "x.mix", "seq+mix"]),
                 ("N", ["./render_nat", PLAN, "x.mix", "seqmix"])]
        if i % 2: order.reverse()
        for tag, cmd in order:
            wall, cpu, rss, status = run(cmd, f"cost_{tag}{i}.mix")
            assert status == 0, (tag, status)
            if tag == "A": a_times.append((wall, cpu)); a_rss.append(rss)
            else: n_times.append((wall, cpu)); n_rss.append(rss)
            print(f"rep{i} {tag}: wall={wall:.2f}s cpu={cpu:.2f}s rss={rss:.1f}MB", flush=True)
    import statistics
    print(f"A   median wall={statistics.median(w for w,c in a_times):.2f}s "
          f"median cpu={statistics.median(c for w,c in a_times):.2f}s maxRSS={max(a_rss):.1f}MB")
    print(f"NAT median wall={statistics.median(w for w,c in n_times):.2f}s "
          f"median cpu={statistics.median(c for w,c in n_times):.2f}s maxRSS={max(n_rss):.1f}MB")

if __name__ == "__main__":
    main()
