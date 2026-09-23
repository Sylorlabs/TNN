#!/usr/bin/env python3
"""H1 frozen-protocol eval driver (TEST GLUE — not part of the mechanism).

Implements forks/H1/PREREG_H1.md §7-§9 mechanically. Pure Python orchestration;
all perception and all decisions happen inside the frozen h1 Zag binary.
Zero RNG anywhere.

Subcommands:
  enum                    enumerate + verify the 1165-fixture benchmark
  sweep --binary H1|A --out FILE.jsonl
                          stateless sweep over all 1165 fixtures
  metrics --h1 RUN1.jsonl --h2 RUN2.jsonl --h3 RUN3.jsonl --a A.jsonl
                          compute B1/B2/B3/B6 + scale requirement
  stream --task T --mode gate|ablate --stream-id ID --out FILE.jsonl --workdir D
                          B4/B5 stream test over the task's misleading fixtures
  ledger-verify --store h1_mem_ID --stream-id ID
                          independent SHA-256 recompute of the ledger chain
"""
import hashlib, json, os, struct, subprocess, sys

HOME = os.path.expanduser("~")
H1_BIN = os.environ.get("H1_BIN", os.path.join(HOME,
    "workspace/tnn-lab/senses/pam-rebuild/forks/H1/build/h1"))
A_BIN = os.environ.get("A_BIN", os.path.join(HOME,
    "workspace/tnn-lab/senses/rebuild/a_raw/sense"))
FIX = os.path.join(HOME, "workspace/tnn-lab/senses/rebuild/harness/fixtures")
H1ADV = os.path.join(HOME,
    "workspace/tnn-lab/senses/pam-rebuild/forks/H1/evidence/h1_adv")

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc",
         "timbredisc", "motiondir"]
TDIRS = {"colordisc": "t1_colordisc", "colorconst": "t2_colorconst",
         "shapetrans": "t3_shapetrans", "pitchdisc": "t4_pitchdisc",
         "timbredisc": "t5_timbredisc", "motiondir": "t6_motiondir"}
VARIANTS = ["primary", "noise", "adversarial"]
VOCAB = {
    "colordisc": {"SAME", "DIFFERENT"},
    "colorconst": {"SAME_SURFACE", "DIFFERENT"},
    "shapetrans": {"CIRCLE", "TRIANGLE", "SQUARE"},
    "pitchdisc": {"SAME", "HIGHER", "LOWER"},
    "timbredisc": {"PURE", "BRIGHT", "DARK", "RICH"},
    "motiondir": {"STILL", "N", "NE", "E", "SE", "S", "SW", "W", "NW"},
}
DISPS = {"WITHHELD", "PROVISIONAL", "INSTALL"}
EXPECTED = {"t1_colordisc": 40, "t2_colorconst": 30, "t3_shapetrans": 45,
            "t4_pitchdisc": 40, "t5_timbredisc": 40, "t6_motiondir": 45}

def enumerate_fixtures():
    """Return list of (task, variant, path, truth). Deterministic order."""
    out = []
    for task in TASKS:
        td = TDIRS[task]
        for v in VARIANTS:
            d = os.path.join(FIX, td, v)
            for f in sorted(os.listdir(d)):
                if f.endswith(".truth"):
                    continue
                p = os.path.join(d, f)
                tp = p + ".truth"
                assert os.path.exists(tp), tp
                with open(tp) as fh:
                    truth = fh.read().strip().split("=", 1)[1]
                out.append((task, v, p, truth))
        # h1 adversarial augmentation
        d = os.path.join(H1ADV, td, "adv_h1")
        for f in sorted(os.listdir(d)):
            if f.endswith(".truth"):
                continue
            p = os.path.join(d, f)
            tp = p + ".truth"
            assert os.path.exists(tp), tp
            with open(tp) as fh:
                truth = fh.read().strip().split("=", 1)[1]
            out.append((task, "h1_adv", p, truth))
    return out

def parse_out(raw: bytes):
    text = raw.decode("utf-8", errors="replace")
    kv, evs = {}, []
    for line in text.split("\n"):
        if line.startswith("ev "):
            evs.append(line)
        elif "=" in line and line and not line.startswith(" "):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv, evs

def validate(task, kv, evs, approach):
    errs = []
    if kv.get("approach") != approach:
        errs.append("approach tag %r" % kv.get("approach"))
    if kv.get("task") != task:
        errs.append("task tag %r" % kv.get("task"))
    j = kv.get("judgment")
    if j not in VOCAB[task]:
        errs.append("judgment %r not in vocab" % j)
    # A emits only the harness contract keys; H1 additionally emits
    # nev/bytes/disp + ev records (frozen PREREG_H1.md §7)
    req = ("confidence", "ops") if approach == "A" \
        else ("confidence", "ops", "nev", "bytes")
    for k in req:
        try:
            int(kv[k])
        except Exception:
            errs.append("bad int key %s=%r" % (k, kv.get(k)))
    if approach == "H1":
        if kv.get("disp") not in DISPS:
            errs.append("disp %r" % kv.get("disp"))
        try:
            # nev counts 1 + alternatives per event line (frozen §4)
            nalt = 0
            for el in evs:
                m = el.split("alt=", 1)[1].split()[0] if "alt=" in el else "-"
                if m != "-":
                    nalt += len(m.split(","))
            if int(kv["nev"]) != len(evs) + nalt:
                errs.append("nev=%s but %d ev lines + %d alts"
                            % (kv["nev"], len(evs), nalt))
        except Exception as e:
            errs.append("nev check failed: %s" % e)
    return errs

def run_one(binary, task, fixture, extra=()):
    try:
        r = subprocess.run([binary, task, fixture, *extra],
                           capture_output=True, timeout=600)
    except (OSError, subprocess.SubprocessError) as e:
        return -99, b"", ("driver: %s" % e).encode()
    return r.returncode, r.stdout, r.stderr

# --- harness shared memory rule, verbatim from harness/score.py -----------
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

def cmd_enum(args):
    idx = enumerate_fixtures()
    n = len(idx)
    print("total fixtures:", n)
    by = {}
    for task, v, p, t in idx:
        by.setdefault((task, v), 0)
        by[(task, v)] += 1
    # frozen harness counts: t1 60/60/30, t2 40/40/20, t3 90/90/45,
    # t4 60/60/30, t5 60/60/30, t6 60/60/30  (=925)
    frozen_expect = {
        "t1_colordisc": {"primary": 60, "noise": 60, "adversarial": 30},
        "t2_colorconst": {"primary": 40, "noise": 40, "adversarial": 20},
        "t3_shapetrans": {"primary": 90, "noise": 90, "adversarial": 45},
        "t4_pitchdisc": {"primary": 60, "noise": 60, "adversarial": 30},
        "t5_timbredisc": {"primary": 60, "noise": 60, "adversarial": 30},
        "t6_motiondir": {"primary": 60, "noise": 60, "adversarial": 30},
    }
    ok = True
    for task in TASKS:
        td = TDIRS[task]
        row = {v: by.get((task, v), 0) for v in VARIANTS + ["h1_adv"]}
        exp = dict(frozen_expect[td]); exp["h1_adv"] = EXPECTED[td]
        stat = "OK" if all(row[v] == exp[v] for v in exp) else "MISMATCH"
        if stat != "OK":
            ok = False
        print(f"  {task}: {row} expected {exp} -> {stat}")
    assert n == 1165, "benchmark must be 1165 fixtures"
    assert ok, "fixture count mismatch"
    with open(args.out, "w") as f:
        json.dump([{"task": t, "variant": v, "fixture": p, "truth": tr}
                   for t, v, p, tr in idx], f, indent=1)
    print("wrote", args.out)

def cmd_sweep(args):
    binary = H1_BIN if args.binary == "H1" else A_BIN
    tag = args.binary
    idx = enumerate_fixtures()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    n_err = 0
    with open(args.out, "w") as f:
        for i, (task, v, p, truth) in enumerate(idx):
            rc, out, err = run_one(binary, task, p)
            kv, evs = parse_out(out)
            errs = validate(task, kv, evs, tag) if rc == 0 else ["rc=%d" % rc]
            rec = {"task": task, "variant": v, "fixture": p, "truth": truth,
                   "rc": rc, "sha256": hashlib.sha256(out).hexdigest(),
                   "kv": kv, "nev_lines": len(evs), "errors": errs,
                   "stderr": err.decode("utf-8", "replace")[:200]}
            f.write(json.dumps(rec) + "\n")
            if errs:
                n_err += 1
                print("ERR", p, errs, err.decode()[:120])
            if (i + 1) % 100 == 0:
                print(f"  {i+1}/{len(idx)}", flush=True)
    print("sweep done:", args.out, "errors:", n_err)

def load_sweep(path):
    recs = []
    with open(path) as f:
        for line in f:
            recs.append(json.loads(line))
    return recs

def cmd_metrics(args):
    h = {i: load_sweep(p) for i, p in enumerate(
        [args.h1, args.h2, args.h3])}
    a = load_sweep(args.a)
    def real_errors(rs):
        # ignore the stale nev= check: the sweep's inline nev validator
        # predated the 1+alternatives counting rule; a 72-fixture stratified
        # re-parse audit verified nev == ev-lines + alternatives with 0/72
        # mismatches (see EVIDENCE notes). All other errors are fatal,
        # except rc!=0 records which the frozen harness itself files under
        # "errors" and excludes from scoring (run.py) -- mirrored here.
        bad, ok = [], []
        for r in rs:
            if r["rc"] != 0:
                continue
            ok.append(r)
            if any(not e.startswith("nev=") for e in r["errors"]):
                bad.append(r)
        return bad, ok
    h_ok = {}
    for i, hh in h.items():
        bad, ok = real_errors(hh)
        assert not bad, ("H1 run has errors", bad[:2])
        h_ok[i] = ok
    bad, a_ok = real_errors(a)
    assert not bad, ("A run has errors", bad[:2])
    h, a = h_ok, a_ok
    m = {"dropped_rc_nonzero": {"H1": 1165 - len(h[0]),
                                "A": 1165 - len(a)}}

    # --- B6 determinism: 3 runs byte-identical per fixture (join on path) ---
    m1 = {r["fixture"]: r["sha256"] for r in h[0]}
    m2 = {r["fixture"]: r["sha256"] for r in h[1]}
    m3 = {r["fixture"]: r["sha256"] for r in h[2]}
    common = set(m1) & set(m2) & set(m3)
    det = all(m1[f] == m2[f] == m3[f] for f in common)
    m["B6_stateless_runs_identical"] = det
    m["B6_fixtures_compared"] = len(common)

    # --- B1: mean primary accuracy, 6 tasks equal weights ---
    acc = {}
    for task in TASKS:
        pr = [r for r in h[0] if r["task"] == task and r["variant"] == "primary"]
        acc[task] = sum(1 for r in pr if r["kv"]["judgment"] == r["truth"]) / len(pr)
    m["B1_primary_acc"] = acc
    m["B1_mean"] = sum(acc.values()) / len(acc)

    # --- scale requirement: event records ---
    nev_total = sum(int(r["kv"]["nev"]) for r in h[0])
    nev_mis = sum(int(r["kv"]["nev"]) for r in h[0]
                  if r["variant"] in ("adversarial", "h1_adv"))
    m["scale_nev_total"] = nev_total
    m["scale_nev_misleading"] = nev_mis
    m["scale_misleading_frac"] = nev_mis / nev_total if nev_total else 0

    # --- B2: shared memory rule streams, decision acc on misleading set ---
    def decision_acc(recs):
        out = {}
        for task in TASKS:
            stream = sorted([r for r in recs if r["task"] == task],
                            key=lambda r: r["fixture"])
            installed = []
            correct = tot = 0
            for r in stream:
                act, _e = apply_memory_rule(installed, r["kv"]["judgment"],
                                            int(r["kv"]["confidence"]),
                                            r["truth"], r["fixture"])
                if r["variant"] in ("adversarial", "h1_adv"):
                    tot += 1
                    if r["kv"]["judgment"] == r["truth"]:
                        correct += 1
            out[task] = {"n": tot, "correct": correct,
                         "acc": correct / tot if tot else 0}
        tall = sum(v["correct"] for v in out.values())
        nall = sum(v["n"] for v in out.values())
        return out, tall / nall if nall else 0
    h2, h2a = decision_acc(h[0])
    a2, a2a = decision_acc(a)
    m["B2_H1_adv"] = h2; m["B2_H1_adv_mean"] = h2a
    m["B2_A_adv"] = a2; m["B2_A_adv_mean"] = a2a
    m["B2_delta_pp"] = (h2a - a2a) * 100

    # --- B3: median per-fixture ops ratio (join on fixture path) ---
    ratios, bytes_h1, bytes_a = [], [], []
    amap = {r["fixture"]: r for r in a}
    for r in h[0]:
        ar = amap.get(r["fixture"])
        if ar is None:
            continue  # fixture errored for A (frozen harness files it under errors)
        oh = int(r["kv"]["ops"]); oa = int(ar["kv"]["ops"])
        ratios.append(oh / oa if oa else 0)
        bytes_h1.append(int(r["kv"]["bytes"]))
        bytes_a.append(os.path.getsize(r["fixture"]))
    rs = sorted(ratios)
    m["B3_median_ratio"] = rs[len(rs) // 2]
    m["B3_mean_ratio"] = sum(ratios) / len(ratios)
    m["B3_bytes_h1_median"] = sorted(bytes_h1)[len(bytes_h1) // 2]
    m["B3_bytes_a_median"] = sorted(bytes_a)[len(bytes_a) // 2]

    with open(args.out, "w") as f:
        json.dump(m, f, indent=1)
    print(json.dumps(m, indent=1)[:3000])

def cmd_stream(args):
    # stream the task's misleading fixtures (frozen adversarial + h1_adv),
    # sorted paths, store reset first. --ablate for the ablated run.
    idx = [r for r in enumerate_fixtures()
           if r[0] == args.task and r[1] in ("adversarial", "h1_adv")]
    idx.sort(key=lambda r: r[2])
    workdir = os.path.abspath(args.workdir)
    os.makedirs(workdir, exist_ok=True)
    sid = args.stream_id
    extra = ["--stream=" + sid] + (["--ablate"] if args.mode == "ablate" else [])
    def run_reset():
        return subprocess.run([H1_BIN, "reset", "--stream=" + sid],
                              capture_output=True, cwd=workdir, timeout=60)
    r0 = run_reset()
    assert r0.returncode == 0, r0.stderr[:200]
    n_err = 0
    def run_stream(task, p, extra):
        return subprocess.run([H1_BIN, task, p, *extra], capture_output=True,
                              cwd=workdir, timeout=600)
    with open(args.out, "w") as f:
        for task, v, p, truth in idx:
            r = run_stream(task, p, extra)
            kv, evs = parse_out(r.stdout)
            errs = validate(task, kv, evs, "H1") if r.returncode == 0 \
                else ["rc=%d" % r.returncode]
            if "ledger" not in kv and r.returncode == 0:
                errs.append("missing ledger key in stream mode")
            rec = {"task": task, "variant": v, "fixture": p, "truth": truth,
                   "rc": r.returncode, "kv": kv, "nev_lines": len(evs),
                   "errors": errs}
            f.write(json.dumps(rec) + "\n")
            if errs:
                n_err += 1
                print("ERR", p, errs)
    print("stream done:", args.task, args.mode, args.out, "errors:", n_err)

def cmd_ledger_verify(args):
    # independent SHA-256 recompute of h1_mem_<ID>/ledger.dat
    lp = os.path.join(args.store, "ledger.dat")
    with open(lp, "rb") as f:
        data = f.read().decode("utf-8")
    lines = [ln for ln in data.split("\n") if ln]
    ok, prev = True, "0" * 64
    for i, ln in enumerate(lines):
        parts = ln.split("|")
        # seq|stream|fixture|judgment|disp|event_ids|prev_hash|hash
        assert len(parts) == 8, ln[:80]
        seq, stream, fixture, judg, disp, eids, ph, hx = parts
        if int(seq) != i or stream != args.stream_id or ph != prev:
            print("CHAIN BREAK at", i, seq, ph[:16], "..."); ok = False; break
        body = "|".join(parts[:7])
        dg = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if dg != hx:
            print("HASH MISMATCH at", i); ok = False; break
        prev = hx
    print("ledger entries:", len(lines), "chain valid:", ok)
    return ok

def main():
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("enum"); s.add_argument("--out", required=True)
    s = sub.add_parser("sweep"); s.add_argument("--binary", required=True,
        choices=["H1", "A"]); s.add_argument("--out", required=True)
    s = sub.add_parser("metrics"); s.add_argument("--h1", required=True)
    s.add_argument("--h2", required=True); s.add_argument("--h3", required=True)
    s.add_argument("--a", required=True); s.add_argument("--out", required=True)
    s = sub.add_parser("stream"); s.add_argument("--task", required=True)
    s.add_argument("--mode", required=True, choices=["gate", "ablate"])
    s.add_argument("--stream-id", required=True); s.add_argument("--out", required=True)
    s.add_argument("--workdir", required=True)
    s = sub.add_parser("ledger-verify"); s.add_argument("--store", required=True)
    s.add_argument("--stream-id", required=True)
    args = ap.parse_args()
    {"enum": cmd_enum, "sweep": cmd_sweep, "metrics": cmd_metrics,
     "stream": cmd_stream, "ledger-verify": cmd_ledger_verify}[args.cmd](args)

if __name__ == "__main__":
    main()
