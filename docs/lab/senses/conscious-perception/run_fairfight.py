#!/usr/bin/env python3
"""FAIR FIGHT comparison harness (frozen protocol, preregs/FAIR_FIGHT.md).

Usage:
  run_fairfight.py --auto <autopilot-binary> --delib <deliberative-binary> [--outdir DIR]

Runs both fork binaries over the FROZEN test battery (fixtures/test/) and,
optionally, the primary speed fixtures. Validates the binary contract,
checks byte-identical reruns, scores decision-relevant catches + cost,
evaluates the frozen kill bars, and writes a run ledger.

Fork binary contract (extends senses/rebuild INTERFACE.md):
  fork <task> <fixture-path>  -> stdout key=value lines, exit 0
  required: approach=AUTOPILOT|DELIBERATIVE, task, judgment, confidence=0..1000, ops=int
  judgment vocab per task (same as INTERFACE.md).
  deliberative extras (validated when present):
    resense=0|1  rs_kind=none|region|band|window|modality|decoder
    rs_ops=<int>=0  uncertainty=0..1000
Ledger: <outdir>/ledger.jsonl — one record per (fork, fixture, run).
No RNG, no wall-clock inside binaries (harness-measured wall_s only).
"""
import json, os, subprocess, sys, time, hashlib, argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
FXT = os.path.join(ROOT, "fixtures", "test")
FXP = os.path.normpath(os.path.join(ROOT, "..", "tnn-lab", "senses", "rebuild", "harness", "fixtures"))

TASKS = {"colordisc": ("t1_colordisc", "img"), "colorconst": ("t2_colorconst", "img"),
         "shapetrans": ("t3_shapetrans", "img"), "pitchdisc": ("t4_pitchdisc", "pcm"),
         "timbredisc": ("t5_timbredisc", "pcm"), "motiondir": ("t6_motiondir", "vid")}
VOCAB = {"colordisc": {"SAME", "DIFFERENT"}, "colorconst": {"SAME_SURFACE", "DIFFERENT"},
         "shapetrans": {"CIRCLE", "TRIANGLE", "SQUARE"},
         "pitchdisc": {"SAME", "HIGHER", "LOWER"},
         "timbredisc": {"PURE", "BRIGHT", "DARK", "RICH"},
         "motiondir": {"STILL", "N", "NE", "E", "SE", "S", "SW", "W", "NW"}}
RS_KINDS = {"none", "region", "band", "window", "modality", "decoder"}
# frozen test battery: (task, leg, filename); leg=redteam scored on cost only
BATTERY = [
    ("pitchdisc", "omission", "om_p1.pcm"), ("pitchdisc", "omission", "om_p2.pcm"),
    ("pitchdisc", "omission", "om_p3.pcm"), ("pitchdisc", "omission", "om_p4.pcm"),
    ("timbredisc", "omission", "om_t1.pcm"), ("timbredisc", "omission", "om_t2.pcm"),
    ("motiondir", "inattentional", "ib_m1.vid"), ("motiondir", "inattentional", "ib_m2.vid"),
    ("pitchdisc", "ambiguity", "am_p1.pcm"), ("colordisc", "ambiguity", "am_c1.img"),
    ("colorconst", "illusion", "il_c1.img"), ("colorconst", "illusion", "il_c2.img"),
    ("pitchdisc", "redteam", "rt_p1.pcm"), ("colordisc", "redteam", "rt_c1.img"),
]

def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def parse_kv(stdout):
    kv = {}
    for line in stdout.splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv

def read_truth(fx):
    with open(fx + ".truth") as f:
        for line in f:
            line = line.strip()
            if line.startswith("truth="):
                return line.split("=", 1)[1]
    return None

def validate(tag, task, kv):
    errs = []
    for k in ("approach", "task", "judgment", "confidence", "ops"):
        if k not in kv:
            errs.append("missing " + k)
    if errs:
        return errs
    if kv["approach"] != tag:
        errs.append("approach tag %r != %r" % (kv["approach"], tag))
    if kv["task"] != task:
        errs.append("task tag mismatch")
    if kv["judgment"] not in VOCAB[task]:
        errs.append("judgment %r not in vocab" % kv["judgment"])
    try:
        c = int(kv["confidence"])
        if not (0 <= c <= 1000):
            errs.append("confidence out of range")
    except ValueError:
        errs.append("confidence not int")
    try:
        o = int(kv["ops"])
        if o < 0:
            errs.append("ops negative")
    except ValueError:
        errs.append("ops not int")
    if tag == "DELIBERATIVE":
        r = kv.get("resense", "0")
        if r not in ("0", "1"):
            errs.append("resense must be 0|1")
        if kv.get("rs_kind", "none") not in RS_KINDS:
            errs.append("bad rs_kind")
        for k in ("rs_ops", "uncertainty"):
            if k in kv:
                try:
                    v = int(kv[k])
                    if v < 0 or (k == "uncertainty" and v > 1000):
                        errs.append(k + " out of range")
                except ValueError:
                    errs.append(k + " not int")
        if r == "0" and kv.get("rs_kind", "none") != "none":
            errs.append("resense=0 but rs_kind set")
    return errs

def run_fork(binary, task, fx):
    t0 = time.perf_counter()
    try:
        p = subprocess.run([binary, task, fx], capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return None, "timeout", 0.0
    dt = time.perf_counter() - t0
    return p.stdout, ("exit=%d" % p.returncode if p.returncode != 0 else None), dt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", required=True)
    ap.add_argument("--delib", required=True)
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--speed", action="store_true",
                    help="also re-run S1-S4 speed legs on primary fixtures")
    a = ap.parse_args()
    outdir = a.outdir or os.path.join(ROOT, "evidence", "fairfight_runs",
                                      time.strftime("%Y%m%d_%H%M%S"))
    os.makedirs(outdir, exist_ok=True)
    forks = [("AUTOPILOT", a.auto), ("DELIBERATIVE", a.delib)]
    binsha = {tag: sha_file(b) for tag, b in forks}
    led = open(os.path.join(outdir, "ledger.jsonl"), "w")
    results = {}   # (tag, fixture-rel) -> record
    errors = []
    n_bi_fail = 0
    items = [(t, leg, os.path.join(FXT, leg, fn)) for (t, leg, fn) in BATTERY]
    if a.speed:
        for t, (tdir, ext) in TASKS.items():
            d = os.path.join(FXP, tdir, "primary")
            for fn in sorted(os.listdir(d)):
                if fn.endswith("." + ext):
                    items.append((t, "speed", os.path.join(d, fn)))
    for (tag, binary) in forks:
        for (task, leg, fx) in items:
            rel = os.path.relpath(fx, ROOT)
            o1, e1, dt1 = run_fork(binary, task, fx)
            o2, e2, dt2 = run_fork(binary, task, fx)
            h1 = hashlib.sha256((o1 or "").encode()).hexdigest()
            h2 = hashlib.sha256((o2 or "").encode()).hexdigest()
            bi = (h1 == h2 and not e1 and not e2)
            if not bi:
                n_bi_fail += 1
            kv = parse_kv(o1 or "")
            verrs = validate(tag, task, kv)
            if verrs:
                errors.append({"fork": tag, "fixture": rel, "errors": verrs,
                               "stdout_head": (o1 or "")[:200]})
                continue
            truth = read_truth(fx) if leg != "speed" else None
            rec = {"fork": tag, "task": task, "leg": leg, "fixture": rel,
                   "fixture_sha": sha_file(fx), "binary_sha": binsha[tag],
                   "stdout_sha": h1, "byte_identical": bi,
                   "judgment": kv["judgment"], "confidence": int(kv["confidence"]),
                   "ops": int(kv["ops"]), "truth": truth,
                   "correct": (kv["judgment"] == truth) if truth else None,
                   "wall_s": dt1,
                   "resense": kv.get("resense"), "rs_kind": kv.get("rs_kind"),
                   "rs_ops": kv.get("rs_ops"), "uncertainty": kv.get("uncertainty")}
            led.write(json.dumps(rec) + "\n")
            results[(tag, rel)] = rec
    led.close()

    # ---- scoring on the frozen battery (non-speed legs) ----
    scored = [b for b in BATTERY if b[1] != "redteam"]
    per_fx = []
    catches = 0
    ops_ratios = []
    resense_count = 0
    for (task, leg, fn) in scored:
        rel = os.path.join("fixtures", "test", leg, fn)
        ra = results.get(("AUTOPILOT", rel))
        rd = results.get(("DELIBERATIVE", rel))
        if not ra or not rd:
            continue
        catch = (rd["correct"] and not ra["correct"])
        catches += 1 if catch else 0
        ratio = rd["ops"] / ra["ops"] if ra["ops"] > 0 else float("inf")
        ops_ratios.append(ratio)
        if rd.get("resense") == "1":
            resense_count += 1
        per_fx.append({"fixture": rel, "leg": leg, "auto": ra["judgment"],
                       "auto_correct": ra["correct"], "delib": rd["judgment"],
                       "delib_correct": rd["correct"], "catch": catch,
                       "ops_ratio": round(ratio, 3),
                       "resense": rd.get("resense"), "rs_kind": rd.get("rs_kind")})
    rt = []
    rt_ratios = []
    for (task, leg, fn) in BATTERY:
        if leg != "redteam":
            continue
        rel = os.path.join("fixtures", "test", leg, fn)
        ra = results.get(("AUTOPILOT", rel))
        rd = results.get(("DELIBERATIVE", rel))
        if not ra or not rd:
            continue
        ratio = rd["ops"] / ra["ops"] if ra["ops"] > 0 else float("inf")
        wratio = rd["wall_s"] / ra["wall_s"] if ra["wall_s"] > 0 else float("inf")
        rt_ratios.append(ratio)
        rt.append({"fixture": rel, "ops_ratio": round(ratio, 3),
                   "wall_ratio": round(wratio, 3),
                   "resense": rd.get("resense"), "rs_kind": rd.get("rs_kind")})
    mean_ops = sum(ops_ratios) / len(ops_ratios) if ops_ratios else 0
    # ---- frozen kill bars ----
    kb = {
        "KB-D1_zero_catches": {"catches": catches, "killed": catches == 0},
        "KB-D2_cost_without_gain": {"mean_ops_ratio": round(mean_ops, 3),
                                    "killed": mean_ops > 2.0 and catches < len(scored) / 4},
        "KB-D3_denial_of_perception": {
            "max_rt_ops_ratio": round(max(rt_ratios), 3) if rt_ratios else 0,
            "killed": any(r > 10 for r in rt_ratios)},
        "KB-A1_autopilot_wins_speed": {"note": "evaluated from S1-S4 legs; autopilot wins recorded, never kills"},
    }
    report = {"forks": [{"tag": t, "binary": b, "sha256": binsha[t]} for t, b in forks],
              "n_battery": len(BATTERY), "n_scored": len(scored),
              "byte_identical_failures": n_bi_fail, "contract_errors": errors,
              "catches": catches, "mean_ops_ratio": round(mean_ops, 3),
              "resense_episodes": resense_count,
              "per_fixture": per_fx, "redteam": rt, "kill_bars": kb}
    with open(os.path.join(outdir, "report.json"), "w") as f:
        json.dump(report, f, indent=1)
    L = ["# FAIR FIGHT comparison run", "",
         "forks: " + ", ".join("%s=%s" % (t, binsha[t][:12]) for t, b in forks),
         f"battery fixtures: {len(BATTERY)} (scored: {len(scored)}, redteam cost-only: {len(BATTERY)-len(scored)})",
         f"byte-identical failures: {n_bi_fail}; contract errors: {len(errors)}", "",
         f"**catches (deliberative correct ^ autopilot wrong): {catches}/{len(scored)}**",
         f"mean ops ratio (delib/auto): {mean_ops:.3f}; resense episodes: {resense_count}", "",
         "## Kill bars"]
    for k, v in kb.items():
        L.append(f"- {k}: {'KILLED' if v.get('killed') else 'alive'} {v}")
    L.append("")
    L.append("## Per-fixture")
    L.append("| fixture | leg | auto | delib | catch | ops_ratio | resense |")
    for r in per_fx:
        L.append(f"| {r['fixture'].split('/')[-1]} | {r['leg']} | {r['auto']}{'✓' if r['auto_correct'] else '✗'} "
                 f"| {r['delib']}{'✓' if r['delib_correct'] else '✗'} | {r['catch']} | {r['ops_ratio']} | {r['resense']}/{r['rs_kind']} |")
    L.append("")
    L.append("## Redteam (cost only)")
    for r in rt:
        L.append(f"- {r['fixture'].split('/')[-1]}: ops_ratio={r['ops_ratio']} wall_ratio={r['wall_ratio']} resense={r['resense']}")
    txt = "\n".join(L) + "\n"
    with open(os.path.join(outdir, "REPORT.md"), "w") as f:
        f.write(txt)
    print(txt)

if __name__ == "__main__":
    main()
