#!/usr/bin/env python3
"""KB4-VIDEO gate head-to-head scorer.

Per fixture (30 ADV-R1 adversarial + 60 TEST-FRESH primary motion clips):
  - windowize into 4-frame windows (w1,w2) and left/right crops (cl,cr)
  - run sense (centroid) on whole/w1/w2/cl/cr; run method2 (block-match) on whole
  - gate.zag decides TEMP/SPAT/METH/ALL corroboration
Per variant (BASELINE, G-TEMP, G-SPAT, G-METH, G-ALL): KB4-style stream
(rel-sorted), shared apply_memory_rule layered over gate candidates.
Also reports pure-gate numbers (corroboration only).

Writes results/final.json. Deterministic: fixed orders, no RNG.
Usage: score_gates.py [--fresh]   (--fresh wipes subclips/ and runs/)
"""
import json, os, shutil, subprocess, sys
from multiprocessing import Pool

LAB = "/home/hatch/workspace/tnn-lab/senses"
WORK = "/home/hatch/workspace/tnn-lab/senses/youtube_ingest"
SRC = os.path.join(WORK, "code/src")
SENSE = os.path.join(SRC, "sense")
M2 = os.path.join(SRC, "method2")
GATE = os.path.join(SRC, "gate")
ADV_DIR = os.path.join(LAB, "rebuild/harness/fixtures/t6_motiondir/adversarial")
PRI_DIR = os.path.join(WORK, "fixtures_testfresh/t6_motiondir/primary")
SUB = os.path.join(WORK, "subclips")
RUNS = os.path.join(WORK, "runs")

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

def fitted_octant(dx, dy, mag):
    if mag >= 1:
        ax, ay = abs(dx), abs(dy)
        if ax >= 2 * ay:
            return "E" if dx > 0 else "W"
        if ay >= 2 * ax:
            return "S" if dy > 0 else "N"
        if dx > 0 and dy > 0: return "SE"
        if dx < 0 and dy > 0: return "SW"
        if dx > 0 and dy < 0: return "NE"
        return "NW"
    return "STILL"

def run_bin(binary, *args):
    p = subprocess.run([binary] + list(args), capture_output=True,
                       text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError("%s failed on %s: %s" % (binary, args, p.stdout[:200]))
    kv = parse_kv(p.stdout)
    dv = parse_debug_vec(kv)
    return kv, dv

def sense_judgment(path):
    kv, dv = run_bin(SENSE, "motiondir", path)
    return {"judgment": fitted_octant(dv["dx"], dv["dy"], dv["mag"]),
            "confidence": int(kv["confidence"]),
            "dx": dv["dx"], "dy": dv["dy"], "mag": dv["mag"]}

def m2_judgment(path):
    kv, dv = run_bin(M2, path)
    return {"judgment": kv["judgment"], "confidence": int(kv["confidence"]),
            "sx": dv["sx"], "sy": dv["sy"], "mag": dv["mag"]}

def gate_decide(variant, clip, pairs):
    args = [GATE, variant, clip]
    for (j, c) in pairs:
        args += [j, str(c)]
    p = subprocess.run(args, capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError("gate failed: %s" % p.stdout[:200])
    return parse_kv(p.stdout)

def windowize_job(args):
    src, outdir, stem = args
    import struct
    with open(src, "rb") as f:
        raw = f.read()
    nf, w, h = struct.unpack("<iii", raw[:12])
    fsz = w * h * 3
    frames = [raw[12 + i * fsz:12 + (i + 1) * fsz] for i in range(nf)]
    def write(p, ww, hh, frs):
        with open(p, "wb") as f:
            f.write(struct.pack("<iii", len(frs), ww, hh))
            for fr in frs:
                f.write(fr)
    def crop(x0, x1):
        out = []
        for fr in frames:
            buf = bytearray((x1 - x0) * h * 3)
            for y in range(h):
                s0 = (y * w + x0) * 3
                d0 = y * (x1 - x0) * 3
                buf[d0:d0 + (x1 - x0) * 3] = fr[s0:s0 + (x1 - x0) * 3]
            out.append(bytes(buf))
        return out
    os.makedirs(outdir, exist_ok=True)
    write(os.path.join(outdir, stem + "_w1.vid"), w, h, frames[0:4])
    write(os.path.join(outdir, stem + "_w2.vid"), w, h, frames[4:8])
    write(os.path.join(outdir, stem + "_cl.vid"), 32, h, crop(0, 32))
    write(os.path.join(outdir, stem + "_cr.vid"), 32, h, crop(32, 64))

def fixture_job(args):
    variant_dir, variant, idx = args
    name = "p%03d.vid" % idx
    src = os.path.join(variant_dir, name)
    rel = "t6_motiondir/%s/%s" % (variant, name)
    clip = "%s_%s" % (variant, name[:-4])
    truth = open(src + ".truth").read().strip().split("=", 1)[1].strip()
    sub = os.path.join(SUB, variant)
    whole = sense_judgment(src)
    w1 = sense_judgment(os.path.join(sub, name[:-4] + "_w1.vid"))
    w2 = sense_judgment(os.path.join(sub, name[:-4] + "_w2.vid"))
    cl = sense_judgment(os.path.join(sub, name[:-4] + "_cl.vid"))
    cr = sense_judgment(os.path.join(sub, name[:-4] + "_cr.vid"))
    m2 = m2_judgment(src)
    g = {}
    g["TEMP"] = gate_decide("TEMP", clip, [(w1["judgment"], w1["confidence"]),
                                           (w2["judgment"], w2["confidence"])])
    g["SPAT"] = gate_decide("SPAT", clip, [(cl["judgment"], cl["confidence"]),
                                           (cr["judgment"], cr["confidence"])])
    g["METH"] = gate_decide("METH", clip, [(whole["judgment"], whole["confidence"]),
                                           (m2["judgment"], m2["confidence"])])
    g["ALL"] = gate_decide("ALL", clip, [(w1["judgment"], w1["confidence"]),
                                         (w2["judgment"], w2["confidence"]),
                                         (cl["judgment"], cl["confidence"]),
                                         (cr["judgment"], cr["confidence"]),
                                         (whole["judgment"], whole["confidence"]),
                                         (m2["judgment"], m2["confidence"])])
    rec = {"rel": rel, "variant": variant, "truth": truth,
           "whole": whole, "w1": w1, "w2": w2, "cl": cl, "cr": cr,
           "m2": m2, "gate": g}
    with open(os.path.join(RUNS, clip + ".json"), "w") as f:
        json.dump(rec, f, sort_keys=True)
    return clip

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

def main():
    fresh = "--fresh" in sys.argv
    if fresh:
        for d in (SUB, RUNS):
            shutil.rmtree(d, ignore_errors=True)
    os.makedirs(SUB, exist_ok=True)
    os.makedirs(RUNS, exist_ok=True)

    fixtures = []
    for d, variant in ((ADV_DIR, "adversarial"), (PRI_DIR, "primary")):
        n = len([f for f in os.listdir(d) if f.endswith(".vid")])
        for i in range(n):
            fixtures.append((d, variant, i))
    fixtures.sort(key=lambda t: (t[1], t[2]))

    # stage 1: windowize (serial, fast, deterministic)
    print("windowizing %d clips..." % len(fixtures), flush=True)
    for (d, variant, i) in fixtures:
        name = "p%03d.vid" % i
        windowize_job((os.path.join(d, name),
                       os.path.join(SUB, variant), name[:-4]))
    # stage 2: per-fixture sense+gate (parallel; keyed by clip -> deterministic)
    print("running sense/gate jobs...", flush=True)
    with Pool(8) as pool:
        clips = pool.map(fixture_job, fixtures, chunksize=4)
    clips.sort()
    print("done %d fixtures" % len(clips), flush=True)

    recs = []
    for (d, variant, i) in fixtures:
        clip = "%s_p%03d" % (variant, i)
        with open(os.path.join(RUNS, clip + ".json")) as f:
            recs.append(json.load(f))
    recs.sort(key=lambda r: r["rel"])

    out = {"n_fixtures": len(recs), "variants": {}}
    for vname, gname in (("BASELINE", None), ("G-TEMP", "TEMP"),
                         ("G-SPAT", "SPAT"), ("G-METH", "METH"),
                         ("G-ALL", "ALL")):
        installed = []
        installs = adv_installs = adv_false = withholds = 0
        pure_installs = pure_adv = pure_adv_false = 0
        pri_installs = pri_correct = 0
        log = []
        for r in recs:
            if gname is None:
                j, c = r["whole"]["judgment"], r["whole"]["confidence"]
                gate_ok, reason = True, "n/a"
            else:
                gd = r["gate"][gname]
                gate_ok = (gd["decision"] == "CANDIDATE")
                reason = gd["reason"]
                j, c = gd["judgment"], int(gd["confidence"])
            entry = {"rel": r["rel"], "truth": r["truth"],
                     "gate": gname or "BASELINE", "gate_ok": gate_ok,
                     "reason": reason}
            if gate_ok:
                # pure-gate accounting (corroboration only)
                pure_installs += 1
                if r["variant"] == "adversarial":
                    pure_adv += 1
                    if j != r["truth"]:
                        pure_adv_false += 1
                action, e = apply_memory_rule(installed, j, c, r["truth"], r["rel"])
                entry["judgment"] = j
                entry["confidence"] = c
                entry["action"] = action
                if action == "INSTALL":
                    installs += 1
                    if r["variant"] == "adversarial":
                        adv_installs += 1
                        if e["false_install"]:
                            adv_false += 1
                    else:
                        pri_installs += 1
                        if not e["false_install"]:
                            pri_correct += 1
                else:
                    withholds += 1
                    entry["blocked_by"] = e["blocked_by"]
            else:
                withholds += 1
                entry["action"] = "GATE_WITHHOLD"
            log.append(entry)
        rate = adv_false / adv_installs if adv_installs else None
        wrate = withholds / len(recs)
        out["variants"][vname] = {
            "installs": installs, "withholds": withholds,
            "withhold_rate": wrate,
            "adv_installs": adv_installs, "adv_false_installs": adv_false,
            "adv_false_install_rate": rate,
            "primary_installs": pri_installs,
            "primary_install_accuracy": (pri_correct / pri_installs
                                         if pri_installs else None),
            "pure_gate": {"installs": pure_installs,
                          "adv_installs": pure_adv,
                          "adv_false_installs": pure_adv_false,
                          "adv_false_install_rate": (pure_adv_false / pure_adv
                                                     if pure_adv else None)},
            "stream": log}
        print("%-8s installs=%3d withholds=%3d (%.1f%%) adv=%d/%d rate=%s pure_adv_rate=%s" % (
            vname, installs, withholds, 100 * wrate, adv_false, adv_installs,
            ("%.1f%%" % (100 * rate)) if rate is not None else "n/a",
            ("%.1f%%" % (100 * pure_adv_false / pure_adv))
            if pure_adv else "n/a"), flush=True)

    # validity gate: BASELINE must match the frozen baseline reproduction
    b = out["variants"]["BASELINE"]
    assert (b["installs"], b["adv_installs"], b["adv_false_installs"],
            b["withholds"]) == (17, 8, 7, 73), "BASELINE drift: %r" % b
    print("BASELINE matches frozen reproduction (17/8/7/73) OK", flush=True)

    with open(os.path.join(WORK, "results/final.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("wrote results/final.json", flush=True)

main()
