#!/usr/bin/env python3
"""R2-6 completion-crew evaluation.

Runs the frozen R2-6 build (sense_r26 + memgate_r26) on every fixture the
build can consume (the round-1 harness formats: 370 primary + 370 noise +
185 adversarial), then scores the prereg bars that are evaluable and
documents the ones that are not (the frozen R2A r2fx suite is
fixture-format-incompatible with this build).

Harness-only glue. Deterministic: fixed trial order, no RNG, no timestamps.
"""
import glob
import hashlib
import json
import os
import re
import statistics
import subprocess
import sys

WORK = os.environ.get("R26_WORK", "/tmp/r26work/eval")
BINDIR = "/tmp/r26work/bin"
SENSE = os.path.join(BINDIR, "sense_r26")
MEMGATE = os.path.join(BINDIR, "memgate_r26")
SENSE_A = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/a_raw/sense")
HARN = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures")
os.makedirs(WORK, exist_ok=True)

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TSUB = ["t1_colordisc", "t2_colorconst", "t3_shapetrans",
        "t4_pitchdisc", "t5_timbredisc", "t6_motiondir"]
TOL = [8, 40, 60, 4000, 120, 0]      # memgate_r26 tol_of per task

JCODES = {
    "colordisc": {"SAME": 0, "DIFFERENT": 1},
    "colorconst": {"SAME_SURFACE": 0, "DIFFERENT": 1},
    "shapetrans": {"CIRCLE": 0, "SQUARE": 1, "TRIANGLE": 2},
    "motiondir": {"STILL": 0, "N": 1, "NE": 2, "E": 3, "SE": 4, "S": 5, "SW": 6, "W": 7, "NW": 8},
    "pitchdisc": {"SAME": 0, "HIGHER": 1, "LOWER": 2},
    "timbredisc": {"PURE": 0, "DARK": 1, "RICH": 2, "BRIGHT": 3},
}

PROG_OF = {"PASS": 0, "FAIL": 1, "UNRESOLVED": 2}
INSTALL_DISPS = {"PROVISIONAL_INSTALL", "PERMANENT_INSTALL", "CORROBORATED"}
PERM_DISPS = {"PERMANENT_INSTALL"}  # durable installs; CORROBORATED counted separately


def build_trials():
    trials = []
    for ti, tsub in enumerate(TSUB):
        task = TASKS[ti]
        for split, okind in [("primary", 0), ("noise", 1), ("adversarial", 2)]:
            d = os.path.join(HARN, tsub, split)
            for p in sorted(glob.glob(os.path.join(d, "*"))):
                if p.endswith(".truth"):
                    continue
                fid = os.path.relpath(p, HARN)
                trials.append({"task": task, "path": p, "fid": fid,
                               "kind": "adv" if split == "adversarial" else "normal",
                               "split": split,
                               "order": (okind, ti, fid)})
    trials.sort(key=lambda t: t["order"])
    for i, t in enumerate(trials):
        t["seq"] = i
    return trials


def read_truth(tr):
    with open(tr["path"] + ".truth") as fh:
        return fh.read().strip().split("=", 1)[1]


def parse_out(data):
    kv = {}
    for line in data.decode("utf-8", "replace").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k] = v
    return kv


def run_one(binary, task, path, timeout=300):
    r = subprocess.run([binary, task, path], capture_output=True, timeout=timeout)
    kv = parse_out(r.stdout)
    kv["_rc"] = r.returncode
    kv["_raw"] = r.stdout
    return kv


def gint(kv, k, default=0):
    try:
        return int(kv.get(k, default))
    except (ValueError, TypeError):
        return default


def sense_sweep(trials, tag):
    """Run sense on all trials in parallel; write ordered raw log; return (results, sha)."""
    from concurrent.futures import ThreadPoolExecutor
    print("sense sweep [%s]: %d trials..." % (tag, len(trials)), flush=True)

    def _one(tr):
        return (tr["seq"], run_one(SENSE, tr["task"], tr["path"]))

    results = {}
    with ThreadPoolExecutor(max_workers=12) as ex:
        for seq, kv in ex.map(_one, trials):
            results[seq] = kv
            if len(results) % 250 == 0:
                print("  sense %d/%d" % (len(results), len(trials)), flush=True)
    raw_path = os.path.join(WORK, "sense_raw_%s.log" % tag)
    h = hashlib.sha256()
    with open(raw_path, "wb") as fh:
        for tr in trials:
            kv = results[tr["seq"]]
            blk = b"### seq=%d task=%s fid=%s\n" % (tr["seq"], tr["task"].encode(), tr["fid"].encode())
            blk += kv["_raw"]
            fh.write(blk)
            h.update(blk)
    print("  raw log %s sha256=%s" % (raw_path, h.hexdigest()), flush=True)
    return results, h.hexdigest()


def build_records(trials, results, truthmap):
    rec_path = os.path.join(WORK, "records.txt")
    ckpt = os.path.join(WORK, "sweep.jsonl")
    outf = open(ckpt, "w")
    recf = open(rec_path, "w")
    n_err = 0
    for tr in trials:
        seq = tr["seq"]
        task = tr["task"]
        tc = TASKS.index(task)
        kv = results[seq]
        truth = truthmap[seq]
        if kv.get("_rc") != 0 or "judgment" not in kv:
            outf.write(json.dumps({"seq": seq, "err": kv.get("error", "rc=%s" % kv.get("_rc"))}) + "\n")
            n_err += 1
            continue
        prog = PROG_OF.get(kv.get("prog", ""), 2)
        jcode = JCODES[task].get(kv["judgment"], -1)
        conf = gint(kv, "confidence")
        pred = gint(kv, "pred")
        meas = gint(kv, "measure")
        ops = gint(kv, "ops")
        # phash: sha256 of canonical `program=` line (binds ledger to program text)
        progline = ""
        for line in kv["_raw"].decode("utf-8", "replace").splitlines():
            if line.startswith("program="):
                progline = line
                break
        phash = hashlib.sha256(progline.encode()).hexdigest()
        recf.write("%d|%d|%s|%d|%d|%s|%d|%d|%d|%s|%s\n" % (
            seq, tc, tr["fid"], prog, jcode, kv["judgment"], conf, pred, meas, phash, truth))
        outf.write(json.dumps({
            "seq": seq, "task": task, "fid": tr["fid"], "kind": tr["kind"], "split": tr["split"],
            "truth": truth, "judgment": kv["judgment"], "conf": conf, "prog": kv.get("prog"),
            "pred": pred, "measure": meas, "ops": ops, "phash": phash,
            "normcmp": kv.get("normcmp"),
        }) + "\n")
    outf.close()
    recf.close()
    print("records written (%d trials, %d errors)" % (len(trials) - n_err, n_err), flush=True)
    return rec_path, ckpt


def run_gate(rec_path):
    ledger_path = os.path.join(WORK, "ledger.txt")
    disp_path = os.path.join(WORK, "dispositions.txt")
    if os.path.exists(ledger_path):
        os.remove(ledger_path)
    r = subprocess.run([MEMGATE, rec_path, ledger_path], capture_output=True, timeout=600)
    if r.returncode != 0:
        print("MEMGATE FAILED", r.stdout.decode()[-500:], r.stderr.decode()[-500:], flush=True)
        sys.exit(1)
    open(disp_path, "w").write(r.stdout.decode())
    print("gate done: %d disposition lines" % len(r.stdout.decode().splitlines()), flush=True)
    return disp_path, ledger_path


def verify_ledger(rec_path, ledger_path):
    """Independent Python recompute of the memgate hash chain."""
    prev = bytes(32)
    n = 0
    with open(rec_path) as rf, open(ledger_path) as lf:
        for rline, lline in zip(rf, lf):
            rline = rline.rstrip("\n")
            parts = lline.rstrip("\n").split("|", 2)
            if len(parts) != 3:
                return False, n, "ledger line %d malformed" % n
            ph, hh, canon = parts
            if ph != prev.hex():
                return False, n, "prev-link mismatch at %d" % n
            h = hashlib.sha256(prev + canon.encode()).hexdigest()
            if h != hh:
                return False, n, "hash mismatch at %d" % n
            prev = bytes.fromhex(hh)
            n += 1
    return True, n, "ok"


def contractless_decide(prog, pred):
    """Decision each trial would get with NO memory contract: PASS installs
    directly (no provisional/permanent staging, no negative evidence,
    no corroboration, no conflict-withhold); FAIL->NEGATIVE, UNRESOLVED->WITHHELD."""
    if prog == 1:
        return "NEGATIVE_EVIDENCE"
    if prog == 2:
        return "WITHHELD"
    if pred == 0:
        return "WITHHELD"
    return "PROVISIONAL_INSTALL"  # direct install, no staging


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    trials = build_trials()
    print("trials: %d (primary=%d noise=%d adv=%d)" % (
        len(trials),
        sum(1 for t in trials if t["split"] == "primary"),
        sum(1 for t in trials if t["split"] == "noise"),
        sum(1 for t in trials if t["split"] == "adversarial")), flush=True)
    truthmap = {t["seq"]: read_truth(t) for t in trials}

    results = None
    if cmd in ("all", "sweep"):
        results, sha1 = sense_sweep(trials, "run1")
        results2, sha2 = sense_sweep(trials, "run2")
        results3, sha3 = sense_sweep(trials, "run3")
        det = (sha1 == sha2 == sha3)
        print("B6 byte-identity: run1=%s run2=%s run3=%s identical=%s" % (sha1, sha2, sha3, det), flush=True)
        json.dump({"run1": sha1, "run2": sha2, "run3": sha3, "identical": det},
                  open(os.path.join(WORK, "byte_identity.json"), "w"), indent=1)

    if cmd in ("all", "gate"):
        if results is None:
            results, _ = sense_sweep(trials, "run1")
        rec_path, ckpt = build_records(trials, results, truthmap)
        disp_path, ledger_path = run_gate(rec_path)
        ok, n, msg = verify_ledger(rec_path, ledger_path)
        print("ledger verify: ok=%s n=%d %s" % (ok, n, msg), flush=True)
        json.dump({"ok": ok, "n": n, "msg": msg},
                  open(os.path.join(WORK, "ledger_verify.json"), "w"), indent=1)

    if cmd in ("all", "score"):
        score(trials, truthmap)

    if cmd in ("all", "approach_a"):
        run_approach_a(trials, truthmap)


def score(trials, truthmap):
    rows = [json.loads(l) for l in open(os.path.join(WORK, "sweep.jsonl"))]
    rows = [r for r in rows if "err" not in r]
    by_seq = {r["seq"]: r for r in rows}
    disps = {}
    for line in open(os.path.join(WORK, "dispositions.txt")):
        p = line.rstrip("\n").split("|")
        disps[int(p[0])] = {"disp": p[3], "detail": p[4], "truth": p[5]}

    def correct(r):
        return r["judgment"] == r["truth"]

    prim = [r for r in rows if r["split"] == "primary"]
    adv = [r for r in rows if r["split"] == "adversarial"]
    norm = [r for r in rows if r["kind"] == "normal"]

    # B1: mean primary accuracy >= 60%
    acc = sum(1 for r in prim if correct(r)) / len(prim)
    per_task = {}
    for t in TASKS:
        rt = [r for r in prim if r["task"] == t]
        per_task[t] = (sum(1 for r in rt if correct(r)), len(rt),
                       sum(1 for r in rt if correct(r)) / len(rt) if rt else 0)

    # Installs under the contract
    def is_install(seq):
        return disps[seq]["disp"] in INSTALL_DISPS

    def is_perm(seq):
        return disps[seq]["disp"] in PERM_DISPS or (
            disps[seq]["disp"] == "CORROBORATED" and disps[seq]["detail"] == "perm")

    # RK-1 analog: false installs (install-type disposition, judgment wrong)
    false_inst = [r for r in rows if is_install(r["seq"]) and not correct(r)]
    perm_false = [r for r in rows if is_perm(r["seq"]) and not correct(r)]

    # Contract-less ablation (B4): decisions without the contract
    changed_adv = 0
    cl_false = 0
    cl_installs = 0
    for r in rows:
        seq = r["seq"]
        cl = contractless_decide(PROG_OF[r["prog"]], r["pred"])
        if cl != disps[seq]["disp"]:
            if r["kind"] == "adv":
                changed_adv += 1
        if cl == "PROVISIONAL_INSTALL":
            cl_installs += 1
            if not correct(r):
                cl_false += 1
    contract_false = len(false_inst)
    adv_n = len(adv)

    # RK-2: wrong-high-conf installed / all wrong-high-conf
    whc = [r for r in rows if r["conf"] >= 700 and not correct(r)]
    whc_inst = [r for r in whc if is_install(r["seq"])]
    # RK-3: correct-high-conf PASS-and-install / all correct-high-conf
    chc = [r for r in rows if r["conf"] >= 700 and correct(r)]
    chc_pi = [r for r in chc if r["prog"] == "PASS" and is_install(r["seq"])]
    # RK-5: wrong-high-conf reaching FAIL/UNRESOLVED
    whc_fu = [r for r in whc if r["prog"] in ("FAIL", "UNRESOLVED")]
    # RK-6: escalations (none in this design) + p95 ops vs Approach A
    ops = sorted(r["ops"] for r in rows)
    p95 = ops[int(0.95 * (len(ops) - 1))] if ops else 0

    m = {
        "n_trials": len(rows),
        "B1_primary_accuracy": acc,
        "B1_per_task": {t: {"correct": c, "n": n, "acc": a} for t, (c, n, a) in per_task.items()},
        "false_installs_any": len(false_inst),
        "false_installs_rate_runnable": len(false_inst) / len(rows),
        "false_permanent_installs": len(perm_false),
        "B4_changed_adv": changed_adv, "B4_changed_adv_rate": changed_adv / adv_n if adv_n else 0,
        "B4_contractless_false_installs": cl_false, "B4_contract_false_installs": contract_false,
        "RK4_contractless_installs": cl_installs,
        "RK2_wrong_highconf": len(whc), "RK2_wrong_highconf_installed": len(whc_inst),
        "RK2_rate": len(whc_inst) / len(whc) if whc else None,
        "RK3_correct_highconf": len(chc), "RK3_correct_highconf_pass_install": len(chc_pi),
        "RK3_rate": len(chc_pi) / len(chc) if chc else None,
        "RK5_wrong_highconf": len(whc), "RK5_reach_fail_unres": len(whc_fu),
        "RK5_rate": len(whc_fu) / len(whc) if whc else None,
        "escalations": 0,
        "p95_ops_r26": p95,
    }
    json.dump(m, open(os.path.join(WORK, "metrics.json"), "w"), indent=1)
    print(json.dumps(m, indent=1))


def run_approach_a(trials, truthmap):
    from concurrent.futures import ThreadPoolExecutor
    print("approach A sweep: %d trials..." % len(trials), flush=True)

    def _one(tr):
        return (tr["seq"], run_one(SENSE_A, tr["task"], tr["path"]))

    outs = {}
    with ThreadPoolExecutor(max_workers=12) as ex:
        for seq, kv in ex.map(_one, trials):
            outs[seq] = kv
    prim = [t for t in trials if t["split"] == "primary"]
    ok = sum(1 for t in prim if outs[t["seq"]].get("judgment") == truthmap[t["seq"]])
    ops = []
    nerr = 0
    for t in trials:
        kv = outs[t["seq"]]
        if kv.get("_rc") != 0 or "judgment" not in kv:
            nerr += 1
            continue
        try:
            ops.append(int(kv.get("ops", 0)))
        except (ValueError, TypeError):
            pass
    ops.sort()
    p95 = ops[int(0.95 * (len(ops) - 1))] if ops else 0
    res = {"approach_a_primary_accuracy": ok / len(prim) if prim else 0,
           "approach_a_p95_ops": p95, "n_errors": nerr, "n": len(trials)}
    json.dump(res, open(os.path.join(WORK, "approach_a.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
