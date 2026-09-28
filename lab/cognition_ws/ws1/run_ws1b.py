#!/usr/bin/env python3
# WS1-B run driver. Frozen prereg: ws1/PREREG_WS1B.md (commit 5e24c6e2).
# Matrix: D (items_v2 x {autopilot,tocap}), RT (rt_d1 x {autopilot,tocap}),
# RF (refusal x {fastref,tocap}), S (trap_x10 x {autopilot,tocap}); 3 reruns each.
# Verifies binary SHAs before running; records SHA256 of every output.
import os, subprocess, hashlib, json, time, sys

HOME = os.environ["HOME"]
WS = HOME + "/workspace/cognition_ws/ws1"
RUNS = WS + "/runs"
os.makedirs(RUNS, exist_ok=True)
LOG = open(RUNS + "/driver.log", "a")

HC = HOME + "/workspace/tnn-lab/consciousness_cost/harness_cost"
CC = HOME + "/workspace/tnn-lab/consciousness_cost"
IV = HOME + "/workspace/tnn-lab/deliberation_depth/items_v2"
RTD1 = HOME + "/workspace/tnn-lab/deliberation_depth/depth1_discipline/batteries/rt_d1.jsonl"
BATS = WS + "/batteries"

FROZEN = {
    HC + "/cost_harness": "01c562be2c194da93008110421bd5988499c196ee42434bc3a854a12cf556137",
    HC + "/fastref": "5398177a68175011722c5b8b3475bd735a119df69c60e464ee9addbbcd3c2098",
}

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True); LOG.write(line + "\n"); LOG.flush()

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

for b, want in FROZEN.items():
    got = sha(b)
    if got != want:
        log("FATAL binary SHA mismatch %s: %s != %s" % (b, got, want)); sys.exit(1)
    log("binary %s sha OK" % os.path.basename(b))

manifest = []
def run_cell(name, argv, outs):
    t0 = time.time()
    p = subprocess.run(argv, capture_output=True, text=True, timeout=1800)
    dt = time.time() - t0
    rec = {"cell": name, "rc": p.returncode, "secs": round(dt, 2),
           "stdout": p.stdout.strip(), "stderr": p.stderr.strip()[-400:],
           "files": {}}
    for o in outs:
        rec["files"][o] = sha(o) if os.path.exists(o) else None
    manifest.append(rec)
    log("%s rc=%d %.1fs %s" % (name, p.returncode, dt, p.stdout.strip()[:80]))
    return p.returncode

cfgs = {"autopilot": CC + "/configs/autopilot.cfg",
        "tocap": CC + "/configs/tocap.cfg"}

def harness_cell(tag, batpath, cfg, r):
    o1 = "%s/%s.res.jsonl" % (RUNS, tag); o2 = "%s/%s.led.jsonl" % (RUNS, tag)
    o3 = "%s/%s.met.jsonl" % (RUNS, tag)
    return run_cell(tag, [HC + "/cost_harness", batpath, cfgs[cfg], o1, o2, o3],
                   [o1, o2, o3])

def fastref_cell(tag, batpath, r):
    o1 = "%s/%s.res.jsonl" % (RUNS, tag); o3 = "%s/%s.met.jsonl" % (RUNS, tag)
    return run_cell(tag, [HC + "/fastref", batpath, o1, o3], [o1, o3])

cells = 0
# Leg D
for bat in ["admit", "revoke", "logic", "trap", "cost"]:
    for cfg in ["autopilot", "tocap"]:
        for r in (1, 2, 3):
            harness_cell("d_%s_%s_r%d" % (cfg, bat, r), "%s/%s.jsonl" % (IV, bat), cfg, r)
            cells += 1
# Leg RT
for cfg in ["autopilot", "tocap"]:
    for r in (1, 2, 3):
        harness_cell("rt_%s_r%d" % (cfg, r), RTD1, cfg, r); cells += 1
# Leg RF
for r in (1, 2, 3):
    fastref_cell("rf_fastref_r%d" % r, CC + "/refusal.jsonl", r); cells += 1
for r in (1, 2, 3):
    harness_cell("rf_tocap_r%d" % r, CC + "/refusal.jsonl", "tocap", r); cells += 1
# Leg S (stress)
for cfg in ["autopilot", "tocap"]:
    for r in (1, 2, 3):
        harness_cell("s_%s_r%d" % (cfg, r), "%s/trap_x10.jsonl" % BATS, cfg, r)
        cells += 1

json.dump(manifest, open(RUNS + "/manifest.json", "w"), indent=1)
log("MATRIX COMPLETE: %d cells" % cells)
