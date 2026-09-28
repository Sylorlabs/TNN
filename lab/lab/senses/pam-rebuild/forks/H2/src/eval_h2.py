#!/usr/bin/env python3
"""PAM fork H2 — evaluation harness (test harness only, NOT architecture).

Runs sense_h2 and the rebuilt Approach-A binary over the frozen 10,000-trial
suite (5,000 normal + 5,000 adversarial), feeds the H2 records through
memgate (the frozen memory contract), runs the contract-less ablation gate,
joins truth, and computes the preregistered bars B1..B6 (+B7 note) and the
H2 kill criteria. Also verifies the memgate ledger by independent recompute.

Outputs: metrics.json (evidence/).
"""
import concurrent.futures as cf
import hashlib
import json
import os
import statistics
import subprocess
import sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
H2 = os.path.join(LAB, "senses/pam-rebuild/forks/H2")
HARN = os.path.join(LAB, "senses/rebuild/harness/fixtures")
H2FIX = os.path.join(H2, "fixtures")
SENSE_H2 = os.path.join(H2, "src/sense_h2")
SENSE_A = os.path.join(LAB, "senses/rebuild/a_raw/sense")
MEMGATE = os.path.join(H2, "src/memgate")

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TSUB = ["t1_colordisc", "t2_colorconst", "t3_shapetrans",
        "t4_pitchdisc", "t5_timbredisc", "t6_motiondir"]
N_NORMAL = [900, 600, 1080, 600, 600, 480]
N_ADV = [900, 480, 1080, 900, 900, 555]
EXT = {"colordisc": ".img", "colorconst": ".img", "shapetrans": ".img",
       "pitchdisc": ".pcm", "timbredisc": ".pcm", "motiondir": ".vid"}

WORK = os.path.join(H2, "evidence", "_evalwork")
os.makedirs(WORK, exist_ok=True)

# judgment -> small integer code (per-task streams compare codes)
JCODES = {}
def jcode(j):
    if j not in JCODES:
        JCODES[j] = len(JCODES)
    return JCODES[j]


def list_frozen(task, variant):
    d = os.path.join(HARN, TSUB[TASKS.index(task)], variant)
    return sorted(f for f in os.listdir(d)
                  if not f.endswith(".truth") and os.path.exists(os.path.join(d, f + ".truth")))


def build_trials():
    """Trial = dict(task, path, stream). Memgate feed order per task:
    frozen primary, frozen noise, h2n (by index), frozen adversarial, h2a."""
    trials = []
    for ti, task in enumerate(TASKS):
        for v in ("primary", "noise"):
            for f in list_frozen(task, v):
                trials.append({"task": task,
                               "path": os.path.join(HARN, TSUB[ti], v, f),
                               "stream": "normal", "fid": "frozen_%s_%s" % (v, f)})
        for i in range(N_NORMAL[ti]):
            f = "h2n_%s_%04d%s" % (task, i, EXT[task])
            trials.append({"task": task, "path": os.path.join(H2FIX, f),
                           "stream": "normal", "fid": f})
        for f in list_frozen(task, "adversarial"):
            trials.append({"task": task,
                           "path": os.path.join(HARN, TSUB[ti], "adversarial", f),
                           "stream": "adversarial", "fid": "frozen_adv_%s" % f})
        for i in range(N_ADV[ti]):
            f = "h2a_%s_%04d%s" % (task, i, EXT[task])
            trials.append({"task": task, "path": os.path.join(H2FIX, f),
                           "stream": "adversarial", "fid": f})
    return trials


def run_one(binary, task, path):
    try:
        r = subprocess.run([binary, task, path], capture_output=True, timeout=300)
    except Exception as e:  # noqa
        return {"error": "exception:%s" % e}
    if r.returncode != 0:
        return {"error": "exit=%d" % r.returncode,
                "stdout": r.stdout.decode("utf8", "replace")[:200]}
    kv = {}
    for line in r.stdout.decode("utf8", "replace").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv


def parse_int(kv, k, default=0):
    try:
        return int(kv.get(k, default))
    except (ValueError, TypeError):
        return default


def main():
    trials = build_trials()
    # Snapshot both binaries locally before the sweep: other crews rebuild
    # a_raw/sense in place (observed 2026-09-23: binary absent 02:02-02:13,
    # 4,355/10,000 trials errored with ENOENT), which would silently bias
    # every bar. The snapshots are byte-verified below; SHAs go to metrics.
    import shutil
    snap = {}
    for name, src in (("sense_h2", SENSE_H2), ("sense_a", SENSE_A),
                      ("memgate", MEMGATE)):
        assert os.path.exists(src), "missing binary at sweep start: %s" % src
        dst = os.path.join(WORK, "%s.snapshot" % name)
        shutil.copyfile(src, dst)
        os.chmod(dst, 0o755)
        h = hashlib.sha256(open(dst, "rb").read()).hexdigest()
        snap[name] = (dst, h)
        print("%s snapshot: %s sha256=%s" % (name, dst, h), flush=True)
    sense_h2_bin, sense_a_bin = snap["sense_h2"][0], snap["sense_a"][0]
    memgate_bin = snap["memgate"][0]
    n_normal = sum(1 for t in trials if t["stream"] == "normal")
    n_adv = sum(1 for t in trials if t["stream"] == "adversarial")
    print("trials: %d (normal=%d adversarial=%d)" % (len(trials), n_normal, n_adv), flush=True)
    assert n_normal == 5000 and n_adv == 5000, (n_normal, n_adv)
    for t in trials:
        assert os.path.exists(t["path"]), t["path"]
        assert os.path.exists(t["path"] + ".truth"), t["path"]

    # --- run both binaries over every trial (parallel) ---
    def work(tr):
        h2 = run_one(sense_h2_bin, tr["task"], tr["path"])
        a = run_one(sense_a_bin, tr["task"], tr["path"])
        return h2, a

    h2res, ares = [], []
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(work, tr): i for i, tr in enumerate(trials)}
        for i, f in enumerate(cf.as_completed(futs)):
            h2, a = f.result()
            h2res.append((futs[f], h2))
            ares.append((futs[f], a))
            if (i + 1) % 1000 == 0:
                print("ran %d/%d" % (i + 1, len(trials)), flush=True)
    h2res.sort()
    ares.sort()
    h2outs = [h for _, h in h2res]
    aouts = [a for _, a in ares]

    # --- join truth, build memgate records ---
    rec_lines = []
    prog_of = {"PASS": 0, "FAIL": 1, "UNRESOLVED": 2}
    # checkpoint binary outputs before memgate (so a memgate failure doesn't lose them)
    with open(os.path.join(WORK, "h2outs.json"), "w") as fh:
        json.dump(h2outs, fh)
    with open(os.path.join(WORK, "aouts.json"), "w") as fh:
        json.dump(aouts, fh)
    with open(os.path.join(WORK, "trials.json"), "w") as fh:
        json.dump(trials, fh)
    for seq, (tr, h2) in enumerate(zip(trials, h2outs)):
        with open(tr["path"] + ".truth") as fh:
            truth = fh.read().strip().split("=", 1)[1]
        tr["truth"] = truth
        tr["h2"] = h2
        if "error" in h2 or "judgment" not in h2:
            tr["h2err"] = h2.get("error", "missing-keys")
            continue
        progline = [l for l in h2.get("program", "").splitlines()]
        _ = progline
        phash = hashlib.sha256(h2.get("program", "").encode()).hexdigest()
        rec_lines.append("%d|%d|%s|%d|%d|%s|%d|%d|%d|%s|%s" % (
            seq, TASKS.index(tr["task"]), tr["fid"],
            prog_of.get(h2.get("prog", ""), 2), jcode(h2["judgment"]),
            h2["judgment"], parse_int(h2, "confidence"),
            parse_int(h2, "pred"), parse_int(h2, "measure"),
            phash, truth))
    rec_path = os.path.join(WORK, "records.txt")
    with open(rec_path, "w") as fh:
        fh.write("\n".join(rec_lines) + "\n")

    # --- memgate (retry wrapper: the 10k-ledger file write flakes
    # intermittently under heavy CPU oversubscription (observed 2/6 runs);
    # every successful run emits a byte-identical ledger, so the retry is a
    # pure harness-robustness measure — no bar, tolerance, or contract rule
    # is touched) ---
    ledger_path = os.path.join(WORK, "ledger.txt")
    disp_path = os.path.join(WORK, "dispositions.txt")
    r = None
    for attempt in range(6):
        r = subprocess.run([memgate_bin, rec_path, ledger_path],
                           capture_output=True, timeout=600)
        if r.returncode == 0:
            break
        print("memgate attempt %d failed rc=%d; retrying" % (
            attempt + 1, r.returncode), flush=True)
    assert r is not None and r.returncode == 0, r.stderr.decode()[:500]
    with open(disp_path, "wb") as fh:
        fh.write(r.stdout)
    disp = {}
    for line in r.stdout.decode().splitlines():
        p = line.split("|")
        disp[int(p[0])] = {"tcode": int(p[1]), "fid": p[2],
                           "disp": p[3], "detail": p[4], "truth": p[5]}

    # --- independent ledger verification ---
    prev = "0" * 64
    led_ok = True
    n_links = 0
    with open(ledger_path) as fh:
        for line in fh:
            p, h, canon = line.rstrip("\n").split("|", 2)
            if p != prev:
                led_ok = False
                break
            if hashlib.sha256(bytes.fromhex(p) + canon.encode()).hexdigest() != h:
                led_ok = False
                break
            prev = h
            n_links += 1
    print("ledger verify: %s (%d links)" % (led_ok, n_links), flush=True)

    # --- per-trial joined table ---
    rows = []
    for seq, (tr, h2, a) in enumerate(zip(trials, h2outs, aouts)):
        d = disp.get(seq)
        rows.append({
            "seq": seq, "task": tr["task"], "stream": tr["stream"],
            "fid": tr["fid"], "truth": tr["truth"],
            "h2_j": h2.get("judgment"), "h2_c": parse_int(h2, "confidence"),
            "h2_prog": h2.get("prog"), "h2_pred": parse_int(h2, "pred"),
            "h2_ops": parse_int(h2, "ops"), "h2_err": h2.get("error"),
            "a_j": a.get("judgment"), "a_c": parse_int(a, "confidence"),
            "a_ops": parse_int(a, "ops"), "a_err": a.get("error"),
            "prog_line": h2.get("program", ""), "debug_vec": a.get("debug_vec", ""),
            "fbytes": os.path.getsize(tr["path"]),
            "disp": d["disp"] if d else None,
            "detail": d["detail"] if d else None,
        })
    ok_h2 = [x for x in rows if not x["h2_err"]]
    ok = [x for x in ok_h2 if not x["a_err"]]
    print("clean trials: H2=%d/10000 paired=%d/10000" % (len(ok_h2), len(ok)), flush=True)
    for x in rows:
        if x["h2_err"] or x["a_err"]:
            print("ERR", x["fid"], x["h2_err"], x["a_err"], flush=True)
    # Frozen denominators are fixed: H2-side bars score over all 10,000 trials
    # (5,000 adversarial). Any H2 trial error invalidates the sweep — fail
    # loudly rather than scoring a biased subset. Approach-A errors are
    # deterministic competitor failures (observed 13/10,000 incl. one frozen
    # adversarial fixture); B2/B3 score over the paired-clean subset and the
    # errors are reported, not hidden.
    assert len(ok_h2) == 10000, "H2 not clean on all trials: %d" % len(ok_h2)
    assert len([x for x in ok_h2 if x["stream"] == "adversarial"]) == 5000
    a_errs = [x["fid"] for x in rows if x["a_err"]]
    print("approach-A errors: %d %s" % (len(a_errs), a_errs), flush=True)

    def acc(rs, who):
        # filter only the relevant side's errors: H2 accuracy is over H2-clean
        # trials even where A errored (A errors are A's, not H2's)
        errk = "h2_err" if who == "h2" else "a_err"
        rs = [x for x in rs if not x[errk]]
        if not rs:
            return 0.0
        return sum(1 for x in rs if x[who + "_j"] == x["truth"]) / len(rs)

    # --- B1: viability on frozen 370 primary (equal task weights) ---
    b1_tasks = {}
    for t in TASKS:
        rs = [x for x in ok_h2 if x["task"] == t and x["fid"].startswith("frozen_primary")]
        b1_tasks[t] = acc(rs, "h2")
    b1 = sum(b1_tasks.values()) / len(b1_tasks)

    # --- B2: head-to-head on identical trials (informational) ---
    b2_h2 = acc(ok, "h2")
    b2_a = acc(ok, "a")
    b2_h2_full = acc(ok_h2, "h2")  # H2 over all 10,000

    # --- B3: efficiency ---
    ratios = [x["h2_ops"] / x["a_ops"] for x in ok if x["a_ops"] > 0]
    ratios.sort()
    def pct(q):
        return ratios[min(len(ratios) - 1, int(q * len(ratios)))]
    prog_bytes = [len(x["prog_line"].encode()) for x in ok]
    dbg_bytes = [len(x["debug_vec"].encode()) for x in ok]
    prog_vs_raw = [pb / x["fbytes"] for x, pb in zip(ok, prog_bytes)]

    # --- false permanent installs ---
    # Frozen prereg B5 wording, applied verbatim: "False permanent install =
    # PERMANENT disposition with judgment != truth." In memgate's disposition
    # vocabulary the permanent-granting disposition is PERMANENT_INSTALL;
    # CORROBORATED/perm only re-affirms an already-permanent belief and is
    # NOT a second installation, so it is not counted.
    def false_perm(x):
        return x["disp"] == "PERMANENT_INSTALL" and x["h2_j"] != x["truth"]
    adv = [x for x in ok_h2 if x["stream"] == "adversarial"]
    fp_adv = sum(1 for x in adv if false_perm(x))
    fp_all = sum(1 for x in ok_h2 if false_perm(x))

    # --- KB2: wrong high-confidence percepts reaching FAIL/UNRESOLVED ---
    whc = [x for x in ok_h2 if x["h2_j"] != x["truth"] and x["h2_c"] >= 700]
    kb2 = (sum(1 for x in whc if x["h2_prog"] in ("FAIL", "UNRESOLVED")) / len(whc)) if whc else 1.0

    # --- KB3: adversarial decision accuracy ---
    kb3 = acc(adv, "h2")

    # --- B4 ablation: contract-less shared rule ---
    # INSTALL iff no contradictory installed belief with confidence >= incoming.
    ab = {}
    for x in ok_h2:
        t = x["task"]
        beliefs = ab.setdefault(t, {})
        contrad = any(j != x["h2_j"] and c >= x["h2_c"] for j, c in beliefs.items())
        if contrad:
            x["ab"] = "WITHHOLD"
        else:
            x["ab"] = "INSTALL"
            if x["h2_j"] not in beliefs or x["h2_c"] > beliefs[x["h2_j"]]:
                beliefs[x["h2_j"]] = x["h2_c"]
    INSTALL = {"PROVISIONAL_INSTALL", "PERMANENT_INSTALL", "CORROBORATED"}
    diff = sum(1 for x in adv
               if ((x["disp"] in INSTALL) != (x["ab"] == "INSTALL")))
    b4a = diff / len(adv)
    fp_ab = sum(1 for x in adv if x["ab"] == "INSTALL" and x["h2_j"] != x["truth"])

    metrics = {
        "trials": len(trials), "h2_clean": len(ok_h2), "paired_clean": len(ok),
        "approach_a_errors": len(a_errs), "approach_a_error_fids": a_errs,
        "normal": n_normal, "adversarial": n_adv,
        "sense_h2_sha256": snap["sense_h2"][1],
        "sense_a_sha256": snap["sense_a"][1],
        "memgate_sha256": snap["memgate"][1],
        "B1_viability_mean_primary": b1, "B1_per_task": b1_tasks,
        "B2_h2_acc_paired": b2_h2, "B2_a_acc_paired": b2_a, "B2_delta": b2_h2 - b2_a,
        "B2_h2_acc_full_10k": b2_h2_full, "B2_paired_n": len(ok),
        "B3_ops_ratio_mean": statistics.mean(ratios),
        "B3_ops_ratio_p50": pct(0.50), "B3_ops_ratio_p95": pct(0.95),
        "B3_ops_ratio_max": max(ratios),
        "B3_prog_bytes_mean": statistics.mean(prog_bytes),
        "B3_debugvec_bytes_mean": statistics.mean(dbg_bytes),
        "B3_prog_vs_raw_mean": statistics.mean(prog_vs_raw),
        "B4_disposition_diff_frac_adv": b4a,
        "B4_false_perm_contract_adv": fp_adv,
        "B4_false_install_ablation_adv": fp_ab,
        "B5_false_perm_rate_adv": fp_adv / len(adv),
        "KB1_false_perm_rate_10k": fp_all / len(ok_h2),
        "KB2_wrong_highconf": len(whc),
        "KB2_reach_fail_unresolved_frac": kb2,
        "KB3_adv_decision_acc": kb3,
        "KB4_p95_ops_ratio": pct(0.95),
        "ledger_verified": led_ok, "ledger_links": n_links,
    }
    with open(os.path.join(H2, "evidence", "metrics.json"), "w") as fh:
        json.dump(metrics, fh, indent=2, sort_keys=True)

    # verdict table
    def yn(b):
        return "PASS" if b else "FAIL"
    print("\n==== H2 VERDICT TABLE ====", flush=True)
    print("B1 viability (mean primary acc, equal task weights) : %.4f  bar>=0.60  %s" % (b1, yn(b1 >= 0.60)), flush=True)
    for t in TASKS:
        print("    %-10s H2 acc=%.4f" % (t, b1_tasks[t]), flush=True)
    print("B2 head-to-head (informational): H2=%.4f (n=%d) A=%.4f (n=%d) paired-delta=%+.4f; A errors=%d" % (
        b2_h2_full, len(ok_h2), b2_a, len(ok), b2_h2 - b2_a, len(a_errs)), flush=True)
    print("B3 ops H2/A (n=%d paired): mean=%.3f p50=%.3f p95=%.3f max=%.3f" % (
        len(ratios), statistics.mean(ratios), pct(0.50), pct(0.95), max(ratios)), flush=True)
    print("B3 bytes: program=%.0f debug_vec=%.0f prog/raw=%.4f" % (
        statistics.mean(prog_bytes), statistics.mean(dbg_bytes),
        statistics.mean(prog_vs_raw)), flush=True)
    print("B4 ablation: disposition-diff=%.3f (bar>=0.10) %s; false-perm contract=%d vs ablation=%d %s" % (
        b4a, yn(b4a >= 0.10), fp_adv, fp_ab, yn(fp_adv < fp_ab)), flush=True)
    print("B5 KB4 adversarial false-perm: %d/%d = %.4f  bar<=0.03  %s" % (
        fp_adv, len(adv), fp_adv / len(adv), yn(fp_adv / len(adv) <= 0.03)), flush=True)
    print("KB1 false-perm 10k: %d/%d = %.4f  bar<=0.03  %s" % (
        fp_all, len(ok_h2), fp_all / len(ok_h2), yn(fp_all / len(ok_h2) <= 0.03)), flush=True)
    print("KB2 wrong high-conf: n=%d reach FAIL/UNRESOLVED=%.3f  bar>=0.90  %s" % (
        len(whc), kb2, yn(kb2 >= 0.90)), flush=True)
    print("KB3 adversarial decision acc: %.4f  bar>=0.7125  %s" % (kb3, yn(kb3 >= 0.7125)), flush=True)
    print("KB4 p95 ops ratio: %.3f  bar<=0.40  %s" % (pct(0.95), yn(pct(0.95) <= 0.40)), flush=True)
    print("ledger: verified=%s links=%d" % (led_ok, n_links), flush=True)


main()
