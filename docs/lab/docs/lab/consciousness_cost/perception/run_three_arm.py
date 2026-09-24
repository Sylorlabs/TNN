#!/usr/bin/env python3
"""Three-arm perception cost measurement (frozen prereg PERCEPTION_PREREG.md).

Arms:
  F1 AUTOPILOT            -> tnn-lab/senses/rebuild/a_raw/sense (frozen binary)
  F2 DELIBERATIVE-TRAINED -> forks/deliberative/f2_bin (built from f2.zag)
  F3 DELIBERATIVE-UNTRAINED -> perception/f3/f3_bin (built from f3.zag)

Each arm is driven through the fair-fight binary contract:
  fork <task> <fixture-path> -> stdout key=value (see contract_out())
3 reruns per (arm, fixture); SHA256 of contract stdout must be identical.
Peak RSS of the fork process itself via os.wait4 rusage (KiB).
Fixture SHAs re-verified against MANIFEST.sha256.
Writes: ledger.jsonl, rows.jsonl, RUNLOG.md, and prints a summary table.
"""
import json, os, sys, time, hashlib, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.normpath(os.path.join(ROOT, "..", "..", "..", ".."))
FF = os.path.join(LAB, "senses", "conscious-perception")
FXT = os.path.join(FF, "fixtures", "test")
SENSE = os.path.join(LAB, "senses", "rebuild", "a_raw", "sense")
F2BIN = os.path.join(FF, "forks", "deliberative", "f2_bin")
F3BIN = os.path.join(ROOT, "f3", "f3_bin")

VOCAB = {"colordisc": {"SAME", "DIFFERENT"}, "colorconst": {"SAME_SURFACE", "DIFFERENT"},
         "shapetrans": {"CIRCLE", "TRIANGLE", "SQUARE"},
         "pitchdisc": {"SAME", "HIGHER", "LOWER"},
         "timbredisc": {"PURE", "BRIGHT", "DARK", "RICH"},
         "motiondir": {"STILL", "N", "NE", "E", "SE", "S", "SW", "W", "NW"}}
TASKMAP = {"PITCH": "pitchdisc", "TIMBRE": "timbredisc", "COLORDISC": "colordisc",
           "COLORCONST": "colorconst", "MOTION": "motiondir"}

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

def parse_kv(s):
    """Line-based key=value (a_raw/sense stdout)."""
    kv = {}
    for line in s.splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv

def parse_verdict(path):
    """Single-line comma-separated kv (values may contain '='; the votes
    value contains a comma)."""
    kv = {}
    last = None
    for tok in open(path).read().strip().split(","):
        if "=" in tok:
            k, v = tok.split("=", 1)
            kv[k.strip()] = v.strip()
            last = k.strip()
        elif last is not None:
            kv[last] += "," + tok
    return kv

def read_truth(fx):
    with open(fx + ".truth") as f:
        for line in f:
            line = line.strip()
            if line.startswith("truth="):
                return line.split("=", 1)[1]
    return None

def run_child(argv):
    """Run argv directly; return (stdout, rc, wall_s, peak_rss_kb)."""
    t0 = time.perf_counter()
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid, status, ru = os.wait4(p.pid, 0)
    dt = time.perf_counter() - t0
    out = p.stdout.read().decode("utf-8", "replace")
    rc = os.waitstatus_to_exitcode(status)
    return out, rc, dt, int(ru.ru_maxrss)

def rs_kind_for(task, sels):
    if not sels:
        return "none"
    s = set(sels)
    if task == "pitchdisc" or task == "timbredisc":
        return "window"
    if task == "colordisc":
        return "region" if (s & {10, 11, 12}) else "decoder"
    return "decoder"  # colorconst robust/absolute/consensus; motion bright-tracker

def contract_f1(task, fx):
    out, rc, dt, rss = run_child([SENSE, task, fx])
    kv = parse_kv(out)
    conf = int(kv.get("confidence", -1))
    return {
        "approach": "AUTOPILOT", "task": task, "judgment": kv.get("judgment", "?"),
        "confidence": conf, "ops": int(kv.get("ops", -1)),
        "resense": 0, "rs_kind": "none", "rs_ops": 0,
        "uncertainty": 1000 - conf if conf >= 0 else -1, "policy": "none",
        "_raw": out, "_rc": rc, "_wall": dt, "_rss": rss,
    }

def contract_f2f3(task, fx, binary, policy, outdir, tag):
    pre = os.path.join(outdir, "%s_%s" % (tag, os.path.basename(fx)))
    out, rc, dt, rss = run_child([binary, fx, pre, "100000"])
    kv = parse_verdict(pre + ".verdict") if os.path.exists(pre + ".verdict") else {}
    vtask = TASKMAP.get(kv.get("task", ""), "?")
    rounds = int(kv.get("rounds", 0))
    sels = [int(x) for x in kv.get("selectors", "").split(",") if x.strip().isdigit()]
    finalconf = int(kv.get("finalconf", -1))
    return {
        "approach": "DELIBERATIVE", "task": vtask, "judgment": kv.get("final", "?"),
        "confidence": finalconf, "ops": int(kv.get("ops_total", -1)),
        "resense": 1 if rounds > 0 else 0, "rs_kind": rs_kind_for(vtask, sels),
        "rs_ops": int(kv.get("ops_p2", 0)),
        "uncertainty": 1000 - finalconf if finalconf >= 0 else -1,
        "policy": policy,
        "p1": kv.get("p1", "?"), "p1conf": int(kv.get("p1conf", -1)),
        "p1ops": int(kv.get("p1ops", -1)),
        "_raw": out, "_rc": rc, "_wall": dt, "_rss": rss,
        "_verdict": pre + ".verdict", "_ledger": pre + ".ledger",
    }

ARMS = {
    "F1": lambda task, fx, od, tag: contract_f1(task, fx),
    "F2": lambda task, fx, od, tag: contract_f2f3(task, fx, F2BIN, "trained", od, tag),
    "F3": lambda task, fx, od, tag: contract_f2f3(task, fx, F3BIN, "untrained", od, tag),
}

def validate(arm, task, c):
    errs = []
    if c["_rc"] != 0:
        errs.append("rc=%d" % c["_rc"])
    exp_approach = "AUTOPILOT" if arm == "F1" else "DELIBERATIVE"
    if c["approach"] != exp_approach:
        errs.append("approach %r" % c["approach"])
    if c["task"] != task:
        errs.append("task %r != %r" % (c["task"], task))
    if c["judgment"] not in VOCAB[task]:
        errs.append("judgment %r" % c["judgment"])
    if not (0 <= c["confidence"] <= 1000):
        errs.append("confidence %r" % c["confidence"])
    if c["ops"] < 0:
        errs.append("ops %r" % c["ops"])
    if arm != "F1":
        if c["resense"] not in (0, 1):
            errs.append("resense")
        if c["rs_kind"] not in ("none", "region", "band", "window", "modality", "decoder"):
            errs.append("rs_kind")
        if c["resense"] == 0 and c["rs_kind"] != "none":
            errs.append("resense=0 but rs_kind set")
    return errs

def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "runs", "main")
    os.makedirs(outdir, exist_ok=True)
    manifest = {}
    for line in open(os.path.join(FF, "fixtures", "MANIFEST.sha256")):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        h, p = line.split(None, 1)
        manifest[os.path.normpath(p)] = h
    log = open(os.path.join(outdir, "RUNLOG.md"), "w")
    log.write("# three-arm battery run log\n\n")
    ledger = open(os.path.join(outdir, "ledger.jsonl"), "w")
    rows = []
    n_bi_fail = 0
    for arm in ("F1", "F2", "F3"):
        for (task, leg, fn) in BATTERY:
            fx = os.path.join(FXT, leg, fn)
            fsha = sha_file(fx)
            mkey = os.path.normpath(os.path.relpath(fx, os.path.join(FF, "fixtures")))
            man_ok = manifest.get(mkey) == fsha
            truth = read_truth(fx)
            outs, walls, rss = [], [], []
            errs_all = []
            first = None
            for r in range(3):
                c = ARMS[arm](task, fx, outdir, "%s_%s_r%d" % (arm, fn, r))
                walls.append(c["_wall"]); rss.append(c["_rss"])
                lines = ["approach=%s" % c["approach"], "task=%s" % c["task"],
                         "judgment=%s" % c["judgment"], "confidence=%d" % c["confidence"],
                         "ops=%d" % c["ops"], "resense=%d" % c["resense"],
                         "rs_kind=%s" % c["rs_kind"], "rs_ops=%d" % c["rs_ops"],
                         "uncertainty=%d" % c["uncertainty"], "policy=%s" % c["policy"]]
                s = "\n".join(lines) + "\n"
                outs.append(hashlib.sha256(s.encode()).hexdigest())
                errs_all.extend(validate(arm, task, c))
                if first is None:
                    first = c
            bi = (outs[0] == outs[1] == outs[2])
            if not bi:
                n_bi_fail += 1
            rec = {
                "arm": arm, "task": task, "leg": leg, "fixture": fn,
                "judgment": first["judgment"], "confidence": first["confidence"],
                "ops": first["ops"], "resense": first["resense"],
                "rs_kind": first["rs_kind"], "rs_ops": first["rs_ops"],
                "uncertainty": first["uncertainty"], "policy": first["policy"],
                "truth": truth, "correct": first["judgment"] == truth,
                "wall_s": walls, "peak_rss_kb": rss,
                "byte_identical": bi, "contract_errors": sorted(set(errs_all)),
                "fixture_sha": fsha, "manifest_ok": man_ok,
                "stdout_sha": outs[0],
            }
            if arm != "F1":
                rec["p1"] = first["p1"]; rec["p1conf"] = first["p1conf"]
                rec["p1ops"] = first["p1ops"]
            rows.append(rec)
            ledger.write(json.dumps(rec) + "\n"); ledger.flush()
            log.write("- %s %s/%s: %s conf=%d ops=%d resense=%d wall=%.3fs rss=%dKB bi=%s errs=%s\n" % (
                arm, leg, fn, first["judgment"], first["confidence"], first["ops"],
                first["resense"], walls[0], rss[0], bi, sorted(set(errs_all)) or "none"))
            log.flush()
            print("%s %-22s %s conf=%4d ops=%9d rs=%d wall=%7.3fs bi=%s" % (
                arm, leg + "/" + fn, first["judgment"], first["confidence"],
                first["ops"], first["resense"], walls[0], bi), flush=True)
    w = open(os.path.join(outdir, "rows.jsonl"), "w")
    for rec in rows:
        w.write(json.dumps(rec) + "\n")
    w.close()
    log.write("\nbyte-identical failures: %d\n" % n_bi_fail)
    log.close(); ledger.close()
    print("byte-identical failures:", n_bi_fail)

if __name__ == "__main__":
    main()
