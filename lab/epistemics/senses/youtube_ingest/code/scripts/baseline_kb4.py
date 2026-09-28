#!/usr/bin/env python3
"""KB4 baseline reproduction on motiondir at rematch-T4 fitted params.

Mirrors rematch/code/fit.py kb4() for (A, motiondir): stream = ADV-R1
adversarial + TEST-FRESH primary motion fixtures sorted by rel path;
fitted judgments (mag < 1 -> STILL, else octant); binary-emitted
confidence (frozen rule); shared round-1 apply_memory_rule.

Expected (rematch T4): installs=17, adv_false=16, withholds=73.
"""
import json, os, subprocess, sys

LAB = "/home/hatch/workspace/tnn-lab/senses"
WORK = "/home/hatch/workspace/tnn-lab/senses/youtube_ingest"
SENSE = os.path.join(WORK, "code/src/sense")
ADV_DIR = os.path.join(LAB, "rebuild/harness/fixtures/t6_motiondir/adversarial")
PRI_DIR = os.path.join(WORK, "fixtures_testfresh/t6_motiondir/primary")

OCT = {0: "STILL", 1: "N", 2: "NE", 3: "E", 4: "SE",
       5: "S", 6: "SW", 7: "W", 8: "NW"}

def fitted_octant(dx, dy, mag):
    """byte-faithful to sense.zag task_motiondir + relations.a_octant"""
    if mag >= 1:
        ax, ay = abs(dx), abs(dy)
        if ax >= 2 * ay:
            d = 3 if dx > 0 else 7
        elif ay >= 2 * ax:
            d = 5 if dy > 0 else 1
        else:
            d = 4
            if dx < 0 and dy > 0: d = 6
            elif dx > 0 and dy < 0: d = 2
            elif dx < 0 and dy < 0: d = 8
        return OCT[d]
    return "STILL"

def parse_kv(stdout):
    kv = {}
    for line in stdout.splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv

def parse_debug_vec(kv):
    d = {}
    for part in kv.get("debug_vec", "").split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            try:
                d[k.strip()] = int(v.strip())
            except ValueError:
                d[k.strip()] = v.strip()
    return d

def run_sense(path):
    p = subprocess.run([SENSE, "motiondir", path], capture_output=True,
                       text=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError("sense failed on %s: %s" % (path, p.stdout[:200]))
    kv = parse_kv(p.stdout)
    dv = parse_debug_vec(kv)
    return {"judgment_raw": kv.get("judgment"),
            "confidence": int(kv["confidence"]),
            "dx": dv["dx"], "dy": dv["dy"], "mag": dv["mag"]}

# vendored verbatim from rebuild/harness/score.py (shared round-1 rule)
def apply_memory_rule(installed, judgment, confidence, truth, fixture):
    for (j, c, _fx) in installed:
        if j != judgment and c >= confidence:
            return ("WITHHOLD",
                    {"fixture": fixture, "judgment": judgment,
                     "confidence": confidence,
                     "blocked_by": {"judgment": j, "confidence": c}})
    installed.append((judgment, confidence, fixture))
    false_install = (judgment != truth)
    return ("INSTALL", {"fixture": fixture, "judgment": judgment,
                        "confidence": confidence, "truth": truth,
                        "false_install": false_install})

def collect():
    recs = []
    for d, variant in ((ADV_DIR, "adversarial"), (PRI_DIR, "primary")):
        for i in range(len([f for f in os.listdir(d)
                            if f.endswith(".vid")])):
            name = "p%03d.vid" % i
            path = os.path.join(d, name)
            r = run_sense(path)
            truth = open(path + ".truth").read().strip().split("=", 1)[1].strip()
            r.update({"rel": "t6_motiondir/%s/%s" % (variant, name),
                      "truth": truth, "variant": variant})
            r["judgment"] = fitted_octant(r["dx"], r["dy"], r["mag"])
            recs.append(r)
    recs.sort(key=lambda r: r["rel"])
    return recs

def main():
    recs = collect()
    installed = []
    installs = adv_installs = adv_false = withholds = 0
    log = []
    for r in recs:
        action, entry = apply_memory_rule(installed, r["judgment"],
                                          r["confidence"], r["truth"], r["rel"])
        rec = {"rel": r["rel"], "truth": r["truth"], "judgment": r["judgment"],
               "confidence": r["confidence"], "action": action,
               "dx": r["dx"], "dy": r["dy"], "mag": r["mag"]}
        if action == "INSTALL":
            installs += 1
            rec["false_install"] = entry["false_install"]
            if r["variant"] == "adversarial":
                adv_installs += 1
                if entry["false_install"]:
                    adv_false += 1
        else:
            withholds += 1
            rec["blocked_by"] = entry["blocked_by"]
        log.append(rec)
    rate = adv_false / adv_installs if adv_installs else None
    print("stream=%d installs=%d adv_installs=%d adv_false=%d rate=%s withholds=%d"
          % (len(recs), installs, adv_installs, adv_false,
             ("%.4f" % rate) if rate is not None else "n/a", withholds))
    ok = (installs == 17 and adv_installs == 17 and adv_false == 16
          and withholds == 73)
    print("REPRODUCTION:", "PASS (17/16/73)" if ok else "FAIL — harness invalid")
    out = os.path.join(WORK, "results/baseline_kb4.json")
    with open(out, "w") as f:
        json.dump({"installs": installs, "adv_installs": adv_installs,
                   "adv_false": adv_false,
                   "adv_false_install_rate": rate,
                   "withholds": withholds, "stream": log}, f, indent=1,
                  sort_keys=True)
    print("wrote", out)
    return 0 if ok else 1

sys.exit(main())
