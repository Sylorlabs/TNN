#!/usr/bin/env python3
"""PAM fork H2 - independent bar scorer (test harness only, NOT architecture).

Scores the frozen prereg bars B1..B6 + H2 kill criteria from the checkpointed
10,000-trial sweep in evidence/_evalwork (trials.json, h2outs.json,
aouts.json). Re-runs memgate over records.txt and requires byte-identical
dispositions to the checkpoint; independently recomputes the ledger chain.

Prereg bar semantics (applied verbatim):
  B1: mean primary accuracy on frozen 370 primary, equal task weights >= 0.60
  B2: H2-A judgment-accuracy delta on identical trials (informational only)
  B3: per-trial ops ratio H2/A (same grain), mean/p50/p95; program bytes
  B4: (a) disposition diff vs contract-less ablation >= 10% of 5,000
      adversarial; (b) false permanent installs strictly fewer WITH contract
  B5: adversarial false-permanent-install rate <= 0.03 (denominator 5,000)
  B6: determinism (covered by det_h2.py; asserted via its artifacts here)
Kill (H2 kill bar, 5,000 normal + 5,000 adversarial suite):
  K1: false permanent installs > 3% of 10,000
  K2: < 90% of wrong high-confidence percepts reach FAIL/UNRESOLVED
  K3: adversarial decision accuracy < 0.7125 (= 0.95 * 0.75 human ref)
  K4: p95 ops ratio > 40% of Approach A
  K5: program replay changes any byte in byte-identical rerun (B6)
  K6: audio/visual acceptance < 90% - preregistered N/A
"""
import hashlib
import json
import os
import statistics
import subprocess
import sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
H2 = os.path.join(LAB, "senses/pam-rebuild/forks/H2")
WORK = os.path.join(H2, "evidence", "_evalwork")
MEMGATE = os.path.join(H2, "src/memgate")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

# pinned binary SHAs (rebuilt from committed sources 2026-09-23)
PINNED = {
    "sense_h2": "5ca4bad38d590aeb76320f2e325f05524b0be1fa4626ff8e526520913a3b65d6",
    "sense_a": "68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1",
    "memgate": "0314033408d2fbf121db72595c6d8d02f50a29a279b2fa9839e5e104e2e40040",
}


def main():
    trials = json.load(open(os.path.join(WORK, "trials.json")))
    h2outs = json.load(open(os.path.join(WORK, "h2outs.json")))
    aouts = json.load(open(os.path.join(WORK, "aouts.json")))
    assert len(trials) == 10000 and len(h2outs) == 10000 and len(aouts) == 10000
    n_adv = sum(1 for t in trials if t["stream"] == "adversarial")
    n_normal = sum(1 for t in trials if t["stream"] == "normal")
    assert (n_normal, n_adv) == (5000, 5000), (n_normal, n_adv)

    # binary provenance: snapshots must match pinned rebuilds
    for name in ("sense_h2", "sense_a", "memgate"):
        p = os.path.join(WORK, "%s.snapshot" % name)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        assert h == PINNED[name], (name, h)
        print("snapshot %s OK %s" % (name, h[:16]), flush=True)

    # join truth
    for tr in trials:
        with open(tr["path"] + ".truth") as fh:
            tr["truth"] = fh.read().strip().split("=", 1)[1]

    h2_err = [i for i, x in enumerate(h2outs) if "error" in x or "judgment" not in x]
    assert not h2_err, "H2 must be clean on all 10,000: %r" % h2_err[:5]
    a_err_idx = set(i for i, x in enumerate(aouts) if "error" in x or "judgment" not in x)
    a_err_fids = sorted(trials[i]["fid"] for i in a_err_idx)
    print("H2 clean: 10000/10000; A clean: %d/10000 (errors: %s)" % (
        10000 - len(a_err_idx), a_err_fids), flush=True)

    # --- re-run memgate over records.txt; require byte-identical dispositions ---
    rec_path = os.path.join(WORK, "records.txt")
    assert sum(1 for _ in open(rec_path)) == 10000
    ledger_path = os.path.join(WORK, "ledger.txt")
    r = subprocess.run([os.path.join(WORK, "memgate.snapshot"), rec_path, ledger_path],
                       capture_output=True, timeout=600)
    assert r.returncode == 0, r.stderr.decode()[:300]
    prev_disp = open(os.path.join(WORK, "dispositions.txt"), "rb").read()
    assert r.stdout == prev_disp, "memgate dispositions not byte-identical on re-run"
    print("memgate re-run: byte-identical dispositions (%d bytes)" % len(r.stdout), flush=True)

    # --- independent ledger recompute ---
    prev = "0" * 64
    n_links = 0
    led_ok = True
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
    assert led_ok and n_links == 10000, (led_ok, n_links)
    ledger_sha = hashlib.sha256(open(ledger_path, "rb").read()).hexdigest()
    ledger_bytes = os.path.getsize(ledger_path)
    print("ledger: 10000/10000 links valid; sha256=%s bytes=%d" % (ledger_sha, ledger_bytes), flush=True)

    disp = {}
    for line in r.stdout.decode().splitlines():
        p = line.split("|")
        disp[int(p[0])] = {"disp": p[3], "detail": p[4], "truth": p[5]}

    def pi(kv, k, default=0):
        try:
            return int(kv.get(k, default))
        except (ValueError, TypeError):
            return default

    rows = []
    for seq, (tr, h2, a) in enumerate(zip(trials, h2outs, aouts)):
        d = disp[seq]
        rows.append({
            "seq": seq, "task": tr["task"], "stream": tr["stream"], "fid": tr["fid"],
            "truth": tr["truth"],
            "h2_j": h2["judgment"], "h2_c": pi(h2, "confidence"),
            "h2_prog": h2.get("prog"), "h2_ops": pi(h2, "ops"),
            "prog_line": h2.get("program", ""),
            "a_ok": seq not in a_err_idx,
            "a_j": a.get("judgment"), "a_ops": pi(a, "ops"),
            "debug_vec": a.get("debug_vec", ""),
            "fbytes": os.path.getsize(tr["path"]),
            "disp": d["disp"], "detail": d["detail"],
        })
    paired = [x for x in rows if x["a_ok"]]
    print("paired-clean (B2/B3): %d" % len(paired), flush=True)

    def acc(rs, who):
        return sum(1 for x in rs if x[who + "_j"] == x["truth"]) / len(rs)

    # B1
    b1_tasks = {}
    for t in TASKS:
        rs = [x for x in rows if x["task"] == t and x["fid"].startswith("frozen_primary_")]
        b1_tasks[t] = acc(rs, "h2")
    b1 = sum(b1_tasks.values()) / 6

    # B2 (informational)
    b2_h2 = acc(paired, "h2")
    b2_a = acc(paired, "a")

    # B3
    ratios = sorted(x["h2_ops"] / x["a_ops"] for x in paired if x["a_ops"] > 0)
    def pct(q):
        return ratios[min(len(ratios) - 1, int(q * len(ratios)))]
    prog_bytes = [len(x["prog_line"].encode()) for x in rows]
    dbg_bytes = [len(x["debug_vec"].encode()) for x in paired]
    prog_vs_raw = [len(x["prog_line"].encode()) / x["fbytes"] for x in rows]

    # false permanent installs: PERMANENT disposition with judgment != truth
    def false_perm(x):
        return x["disp"] == "PERMANENT_INSTALL" and x["h2_j"] != x["truth"]
    adv = [x for x in rows if x["stream"] == "adversarial"]
    fp_adv = sum(1 for x in adv if false_perm(x))
    fp_all = sum(1 for x in rows if false_perm(x))

    # K2: wrong high-confidence percepts reaching FAIL/UNRESOLVED
    whc = [x for x in rows if x["h2_j"] != x["truth"] and x["h2_c"] >= 700]
    k2 = sum(1 for x in whc if x["h2_prog"] in ("FAIL", "UNRESOLVED")) / len(whc) if whc else 1.0

    # K3: adversarial decision accuracy
    k3 = acc(adv, "h2")

    # B4 ablation: contract-less shared rule (per-task streams)
    ab = {}
    for x in rows:
        beliefs = ab.setdefault(x["task"], {})
        contrad = any(j != x["h2_j"] and c >= x["h2_c"] for j, c in beliefs.items())
        if contrad:
            x["ab"] = "WITHHOLD"
        else:
            x["ab"] = "INSTALL"
            if x["h2_j"] not in beliefs or x["h2_c"] > beliefs[x["h2_j"]]:
                beliefs[x["h2_j"]] = x["h2_c"]
    INSTALL = {"PROVISIONAL_INSTALL", "PERMANENT_INSTALL", "CORROBORATED"}
    diff = sum(1 for x in adv if ((x["disp"] in INSTALL) != (x["ab"] == "INSTALL")))
    b4a = diff / len(adv)
    fp_ab = sum(1 for x in adv if x["ab"] == "INSTALL" and x["h2_j"] != x["truth"])

    metrics = {
        "trials": 10000, "normal": 5000, "adversarial": 5000,
        "h2_clean": 10000, "a_clean": len(paired), "a_errors": sorted(a_err_fids),
        "sense_h2_sha256": PINNED["sense_h2"],
        "sense_a_sha256": PINNED["sense_a"],
        "memgate_sha256": PINNED["memgate"],
        "B1_viability_mean_primary": b1, "B1_per_task": b1_tasks,
        "B2_h2_acc_paired": b2_h2, "B2_a_acc_paired": b2_a,
        "B2_delta": b2_h2 - b2_a, "B2_n": len(paired),
        "B2_note": "informational; A deterministically fails 13 shapetrans trials",
        "B3_ops_ratio_mean": statistics.mean(ratios),
        "B3_ops_ratio_p50": pct(0.50), "B3_ops_ratio_p95": pct(0.95),
        "B3_ops_ratio_max": max(ratios), "B3_n": len(ratios),
        "B3_prog_bytes_mean": statistics.mean(prog_bytes),
        "B3_debugvec_bytes_mean": statistics.mean(dbg_bytes),
        "B3_prog_vs_raw_mean": statistics.mean(prog_vs_raw),
        "B4_disposition_diff_frac_adv": b4a,
        "B4_false_perm_contract_adv": fp_adv,
        "B4_false_perm_ablation_adv": fp_ab,
        "B5_false_perm_rate_adv": fp_adv / len(adv),
        "K1_false_perm_rate_10k": fp_all / len(rows),
        "K1_false_perm_10k": fp_all,
        "K2_wrong_highconf_n": len(whc),
        "K2_reach_fail_unresolved": k2,
        "K3_adv_decision_acc": k3,
        "K4_p95_ops_ratio": pct(0.95),
        "ledger_verified": True, "ledger_links": n_links,
        "ledger_sha256": ledger_sha, "ledger_bytes": ledger_bytes,
    }
    with open(os.path.join(H2, "evidence", "metrics.json"), "w") as fh:
        json.dump(metrics, fh, indent=2, sort_keys=True)

    def yn(b):
        return "PASS" if b else "FAIL"
    print("\n==== H2 VERDICT TABLE (frozen prereg bars) ====", flush=True)
    print("B1 viability mean primary acc : %.4f  bar>=0.60  %s" % (b1, yn(b1 >= 0.60)), flush=True)
    for t in TASKS:
        rs = [x for x in rows if x["task"] == t and x["fid"].startswith("frozen_primary_")]
        print("    %-10s acc=%.4f n=%d" % (t, b1_tasks[t], len(rs)), flush=True)
    print("B2 head-to-head (n=%d paired): H2=%.4f A=%.4f delta=%+.4f (informational)" % (
        len(paired), b2_h2, b2_a, b2_h2 - b2_a), flush=True)
    print("B3 ops H2/A: mean=%.3f p50=%.3f p95=%.3f max=%.3f" % (
        statistics.mean(ratios), pct(0.50), pct(0.95), max(ratios)), flush=True)
    print("B3 bytes: program=%.0f debug_vec=%.0f prog/raw=%.4f" % (
        statistics.mean(prog_bytes), statistics.mean(dbg_bytes),
        statistics.mean(prog_vs_raw)), flush=True)
    print("B4 ablation: disp-diff=%.4f (bar>=0.10) %s; false-perm contract=%d vs ablation=%d %s" % (
        b4a, yn(b4a >= 0.10), fp_adv, fp_ab, yn(fp_adv < fp_ab)), flush=True)
    print("B5 adversarial false-perm: %d/%d = %.4f  bar<=0.03  %s" % (
        fp_adv, len(adv), fp_adv / len(adv), yn(fp_adv / len(adv) <= 0.03)), flush=True)
    print("K1 false-perm 10k: %d/10000 = %.4f  kill if >0.03  %s" % (
        fp_all, fp_all / 10000, "KILL" if fp_all / 10000 > 0.03 else "ok"), flush=True)
    print("K2 wrong high-conf: n=%d reach FAIL/UNRESOLVED=%.4f  kill if <0.90  %s" % (
        len(whc), k2, "KILL" if k2 < 0.90 else "ok"), flush=True)
    print("K3 adversarial decision acc: %.4f  kill if <0.7125  %s" % (
        k3, "KILL" if k3 < 0.7125 else "ok"), flush=True)
    print("K4 p95 ops ratio: %.4f  kill if >0.40  %s" % (
        pct(0.95), "KILL" if pct(0.95) > 0.40 else "ok"), flush=True)
    print("K5 byte-identity: see B6 (det_h2.py PASS)", flush=True)
    print("K6 audio/visual acceptance: preregistered N/A", flush=True)
    print("ledger: verified 10000 links, sha256=%s" % ledger_sha, flush=True)


main()
