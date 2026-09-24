#!/usr/bin/env python3
# KBCONTROL measurement battery: wall-clock + peak RSS + SHA256, 3 runs/arm.
import subprocess, time, resource, hashlib, json, sys, os

os.environ["TMPDIR"] = os.path.expanduser("~/workspace/tmp_commit")
BASE = os.path.expanduser("~/workspace/tnn-lab/docs/lab/consciousness_cost/kbcontrol")
BIN = os.path.join(BASE, "build")
EPISODES = {"kb_arm1": 4880, "kb_arm3": 4880, "r27auto": 4880, "r27delib": 4880,
            "ma1_trial_cap8": None, "ma1_trial": None}

def run_once(path):
    t0 = time.perf_counter()
    p = subprocess.run([path], capture_output=True, text=True)
    dt = time.perf_counter() - t0
    rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss  # KiB
    return p.returncode, dt, rss, p.stdout, p.stderr

results = {}
for arm in ["kb_arm1", "kb_arm3", "ma1_trial_cap8", "ma1_trial", "r27auto", "r27delib"]:
    path = os.path.join(BIN, arm)
    runs = []
    for i in range(3):
        rc, dt, rss, out, err = run_once(path)
        h = hashlib.sha256(out.encode()).hexdigest()
        runs.append({"rep": i, "rc": rc, "wall_s": round(dt, 4), "peak_rss_kib": rss,
                     "sha256": h, "stdout_bytes": len(out), "stderr_bytes": len(err)})
        with open(os.path.join(BASE, "logs", f"{arm}_run{i+1}.log"), "w") as f:
            f.write(out)
        if err:
            with open(os.path.join(BASE, "logs", f"{arm}_run{i+1}.stderr"), "w") as f:
                f.write(err)
    shas = {r["sha256"] for r in runs}
    walls = [r["wall_s"] for r in runs]
    results[arm] = {
        "byte_identical_3x": len(shas) == 1,
        "sha256": runs[0]["sha256"],
        "wall_mean_s": round(sum(walls) / 3, 4),
        "wall_min_s": min(walls),
        "wall_max_s": max(walls),
        "peak_rss_kib_mean": sum(r["peak_rss_kib"] for r in runs) // 3,
        "rc_all_zero": all(r["rc"] == 0 for r in runs),
        "runs": runs,
    }
    ep = EPISODES[arm]
    if ep:
        results[arm]["ms_per_episode"] = round(results[arm]["wall_mean_s"] * 1000 / ep, 4)

with open(os.path.join(BASE, "logs", "timing.json"), "w") as f:
    json.dump(results, f, indent=1)
for arm, r in results.items():
    print(f"{arm}: identical={r['byte_identical_3x']} rc0={r['rc_all_zero']} "
          f"wall_mean={r['wall_mean_s']}s rss={r['peak_rss_kib_mean']}KiB "
          f"ms/ep={r.get('ms_per_episode','n/a')} sha={r['sha256'][:16]}")
