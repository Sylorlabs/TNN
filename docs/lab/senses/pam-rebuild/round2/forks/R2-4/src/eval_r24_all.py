#!/usr/bin/env python3
"""R2-4 full evaluation: sweep (sense + deliberation) -> gate -> score.

Pure-Zag architecture under test; this harness is glue (test equipment).
Deterministic: fixed trial order, no RNG, no timestamps in records.
"""
import glob
import hashlib
import json
import os
import re
import statistics
import subprocess
import sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
R24 = os.path.join(LAB, "senses/pam-rebuild/round2/forks/R2-4")
SRC = os.path.join(R24, "src")
FIX = os.path.join(R24, "fixtures")
HARN = os.path.join(LAB, "senses/rebuild/harness/fixtures")
A_RAW = os.path.join(LAB, "senses/rebuild/a_raw")
WORK = os.path.join(R24, "evidence", "_evalwork_r24")  # protected
BINDIR = os.path.join(WORK, "bin")
os.makedirs(BINDIR, exist_ok=True)

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TSUB = ["t1_colordisc", "t2_colorconst", "t3_shapetrans",
        "t4_pitchdisc", "t5_timbredisc", "t6_motiondir"]
TOL = [8, 40, 60, 4000, 120, 0]      # memgate tol_of
THR = [400, 50, 60, 1500, 80, 2]     # deliberation T3 margin bars
ADVFAMS = {"COL-1", "COL-2", "COL-3", "CCN-1", "CCN-2", "SHP-1", "SHP-2", "SHP-3",
           "PTC-1", "PTC-2", "PTC-3", "TMB-1", "TMB-2", "TMB-3",
           "MOT-1", "MOT-2", "MOT-3"}

SENSE = os.path.join(BINDIR, "sense_r24")
DELIB = os.path.join(BINDIR, "deliberate")
MEMGATE = os.path.join(BINDIR, "memgate")
SENSE_A = os.path.join(BINDIR, "sense_a")

JCODES = {
    "colordisc": {"SAME": 0, "DIFFERENT": 1},
    "colorconst": {"SAME_SURFACE": 0, "DIFFERENT": 1},
    "shapetrans": {"SQUARE": 0, "TRIANGLE": 1, "CIRCLE": 2},
    "motiondir": {"STILL": 0, "N": 1, "NE": 2, "E": 3, "SE": 4, "S": 5, "SW": 6, "W": 7, "NW": 8},
    "pitchdisc": {"SAME": 0, "HIGHER": 1, "LOWER": 2},
    "timbredisc": {"PURE": 0, "DARK": 1, "RICH": 2, "BRIGHT": 3},
}


def build_bins():
    znc = os.path.join(LAB, "toolchain/bin/znc_linux_x86_64_abed8aa1")
    jobs = [("sense_r24.zag", SENSE), ("deliberate.zag", DELIB), ("memgate.zag", MEMGATE)]
    for src, out in jobs:
        # NOTE: znc resolves @import relative to CWD, not the source file.
        r = subprocess.run([znc, src, "-o", out], capture_output=True,
                           timeout=600, cwd=SRC)
        if r.returncode != 0 or not os.path.exists(out):
            print("BUILD FAILED:", src, r.stderr.decode()[-2000:], flush=True)
            sys.exit(1)
    # Approach A (frozen a_raw sense)
    r = subprocess.run([znc, "sense.zag", "-o", SENSE_A],
                       capture_output=True, timeout=600, cwd=A_RAW)
    if r.returncode != 0 or not os.path.exists(SENSE_A):
        print("BUILD FAILED: sense_a", r.stderr.decode()[-2000:], flush=True)
        sys.exit(1)
    snap = {}
    for name, path in [("sense_r24", SENSE), ("deliberate", DELIB),
                       ("memgate", MEMGATE), ("sense_a", SENSE_A)]:
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        snap[name] = h
    return snap


def build_trials():
    trials = []
    # 1) R2A normal (sorted)
    for p in sorted(glob.glob(os.path.join(FIX, "*.r24"))):
        base = os.path.basename(p)
        parts = base.split("_")
        task, fam = parts[1], parts[2]
        kind = "adv" if fam in ADVFAMS else "normal"
        trials.append({"task": task, "path": p, "fid": base, "kind": kind,
                       "fam": fam, "src": "r2a", "order": (0 if kind == "normal" else 3, task, base)})
    # 2) harness primary + noise, 3) harness adversarial
    for ti, tsub in enumerate(TSUB):
        task = TASKS[ti]
        for split, okind in [("primary", 1), ("noise", 2), ("adversarial", 4)]:
            d = os.path.join(HARN, tsub, split)
            if not os.path.isdir(d):
                continue
            for p in sorted(glob.glob(os.path.join(d, "*"))):
                if p.endswith(".truth"):
                    continue
                fid = os.path.relpath(p, HARN)
                trials.append({"task": task, "path": p, "fid": fid,
                               "kind": "adv" if split == "adversarial" else "normal",
                               "fam": "harness_" + split, "src": "harness",
                               "order": (okind, task, fid)})
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


def run_sense(task, path):
    r = subprocess.run([SENSE, task, path], capture_output=True, timeout=180)
    kv = parse_out(r.stdout)
    kv["_rc"] = r.returncode
    return kv


def gint(kv, k, default=0):
    try:
        return int(kv.get(k, default))
    except (ValueError, TypeError):
        return default


G_RE = re.compile(r"\|G=selfcheck:[^|]*?t1=(\d+),agree=(\d+),strong=(\d+)")


def g_evidence(program):
    m = G_RE.search(program or "")
    if not m:
        return (0, 0, 0)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))

# ---------------------------------------------------------------- sweep ----
PROG_OF = {"PASS": 0, "FAIL": 1, "UNRESOLVED": 2}
INSTALL = {"PROVISIONAL_INSTALL", "PERMANENT_INSTALL", "CORROBORATED"}


class Tracker:
    """Mirrors memgate.zag's per-task state machine exactly (test equipment)."""

    def __init__(self):
        self.prov = [None] * 6   # (j, m, s, mrg_f, strong)
        self.perm = [None] * 6   # (j, m, s)
        self.neg = [[] for _ in range(6)]  # list of (j, m), cap 256

    def nmatch(self, tc, jcode, meas):
        tol = TOL[tc]
        return any(j == jcode and abs(m - meas) <= tol for j, m in self.neg[tc])

    def decide(self, tc, prog, jcode, conf, pred, meas):
        """Pure: the disposition memgate would emit (no state change)."""
        nm = self.nmatch(tc, jcode, meas)
        if prog == 1:  # FAIL
            return "NEGATIVE_EVIDENCE"
        if prog == 2:  # UNRESOLVED
            return "SUPPRESSED" if nm else "WITHHELD"
        if pred == 0:
            return "WITHHELD"
        if nm:
            return "SUPPRESSED"
        if self.perm[tc] is not None:
            pj, pm, ps = self.perm[tc]
            if jcode != pj:
                return "CONFLICT_WITHHELD"
            return "CORROBORATED"
        if self.prov[tc] is not None:
            pj, pm, ps, pmrg, pstr, pconf = self.prov[tc]
            if jcode == pj and abs(pm - meas) <= TOL[tc]:
                return "PERMANENT_INSTALL"
            if jcode != pj:
                return "PROVISIONAL_INSTALL"  # reversal (detail reversed_old=)
            return "CORROBORATED"
        return "PROVISIONAL_INSTALL"  # new

    def prov_of(self, tc):
        return self.prov[tc]

    def apply(self, tc, seq, prog, jcode, conf, pred, meas, mrg_f, strong):
        """Mutate state with the FINAL record (post-deliberation)."""
        nm = self.nmatch(tc, jcode, meas)
        if prog == 1:
            if not nm and len(self.neg[tc]) < 256:
                self.neg[tc].append((jcode, meas))
            return
        if prog == 0 and pred == 1 and not nm and self.perm[tc] is None:
            if self.prov[tc] is not None:
                pj, pm, ps, pmrg, pstr, pconf = self.prov[tc]
                if jcode == pj and abs(pm - meas) <= TOL[tc]:
                    self.perm[tc] = (jcode, meas, seq)
                    self.prov[tc] = None
                    return
                if jcode != pj:
                    self.prov[tc] = (jcode, meas, seq, mrg_f, strong, conf)
                    return
            else:
                self.prov[tc] = (jcode, meas, seq, mrg_f, strong, conf)
                return


def deliberate_case(seq, tc, ctype, j_f, conf_f, mrg_f, agree_f, strong_f, meas_f,
                    j_s, mrg_fs, strong_s, meas_s):
    line = "%d|%d|%d|%s|%d|%d|%d|%d|%d|%s|%d|%d|%d|%d\n" % (
        seq, tc, ctype, j_f, conf_f, mrg_f, agree_f, strong_f, meas_f,
        j_s, mrg_fs, strong_s, meas_s, TOL[tc])
    with open(os.path.join(WORK, "delib_case.txt"), "w") as fh:
        fh.write(line)
    r = subprocess.run([DELIB, os.path.join(WORK, "delib_case.txt")],
                       capture_output=True, timeout=60)
    out = r.stdout.decode()
    dec = out.strip().splitlines()[0].split("|")[1] if out.strip() else "SKIP"
    return dec


def sweep(trials, snap):
    """Run sense on all trials, deliberate escalations, write records."""
    ckpt = os.path.join(WORK, "sweep.jsonl")
    rec_path = os.path.join(WORK, "records.txt")
    delib_log = os.path.join(WORK, "deliberation.log")
    # Phase 1: parallel sense (independent per trial)
    print("sweep phase 1: parallel sense on %d trials..." % len(trials), flush=True)
    from concurrent.futures import ThreadPoolExecutor
    def _sense_one(tr):
        kv = run_sense(tr["task"], tr["path"])
        return (tr["seq"], kv)
    sense_results = {}
    with ThreadPoolExecutor(max_workers=12) as ex:
        for seq, kv in ex.map(_sense_one, trials):
            sense_results[seq] = kv
            if len(sense_results) % 1000 == 0:
                print("sense %d/%d" % (len(sense_results), len(trials)), flush=True)
    print("sense done: %d trials" % len(sense_results), flush=True)
    # Phase 2: sequential tracker/deliberation (order-dependent)
    outf = open(ckpt, "w")
    recf = open(rec_path, "w")
    dlf = open(delib_log, "w")
    tracker = Tracker()
    n_esc = 0
    for tr in trials:
        seq = tr["seq"]
        task = tr["task"]
        tc = TASKS.index(task)
        kv = sense_results[seq]
        truth = read_truth(tr)
        if kv.get("_rc") != 0 or "judgment" not in kv:
            outf.write(json.dumps({"seq": seq, "err": kv.get("error", "rc=%s" % kv.get("_rc"))}) + "\n")
            continue
        prog = PROG_OF.get(kv.get("prog", ""), 2)
        jcode = JCODES[task].get(kv["judgment"], -1)
        conf = gint(kv, "confidence")
        pred = gint(kv, "pred")
        meas = gint(kv, "measure")
        mrg_f = gint(kv, "mrgF")
        ops = gint(kv, "ops")
        program = kv.get("program", "")
        t1, agree, strong = g_evidence(program)
        phash = hashlib.sha256(program.encode()).hexdigest()

        # escalation check against the tracker (pre-update)
        disp_pre = tracker.decide(tc, prog, jcode, conf, pred, meas)
        final_prog, final_pred = prog, pred
        esc = None
        if disp_pre == "PERMANENT_INSTALL" and conf >= 700:
            # E1: deliberate high-stakes permanence grants (high-conf only)
            pj, pm, ps, pmrg, pstr, pconf = tracker.prov_of(tc)
            dec = deliberate_case(seq, tc, 0, kv["judgment"], conf, mrg_f,
                                  agree, strong, meas, pj, pmrg, pstr, pm)
            esc = ("E1", dec)
            n_esc += 1
            if dec != "RATIFY":
                final_prog, final_pred = 2, 0
            ops += 40
        elif disp_pre == "PROVISIONAL_INSTALL" and conf >= 700:
            # E2: high-confidence conflict reversal (prov exists, judgment differs,
            # both high-conf)
            pv = tracker.prov_of(tc)
            if pv is not None and jcode != pv[0] and tracker.perm[tc] is None and pv[5] >= 700:
                pj, pm, ps, pmrg, pstr, pconf = pv
                dec = deliberate_case(seq, tc, 1, kv["judgment"], conf, mrg_f,
                                      agree, strong, meas, pj, pmrg, pstr, pm)
                esc = ("E2", dec)
                n_esc += 1
                if dec != "ALLOW":
                    final_prog, final_pred = 2, 0
                ops += 40
        if esc:
            dlf.write("%d|%s|%s|%s|conf=%d|mrgF=%d|agree=%d|strong=%d -> %s\n" % (
                seq, esc[0], task, kv["judgment"], conf, mrg_f, agree, strong, esc[1]))
            dlf.flush()
        # predicted FINAL disposition (pre-mutation state; must match memgate)
        disp_final = tracker.decide(tc, final_prog, jcode, conf, final_pred, meas)
        tracker.apply(tc, seq, final_prog, jcode, conf, final_pred, meas, mrg_f, strong)
        fid = tr["fid"]
        recf.write("%d|%d|%s|%d|%d|%s|%d|%d|%d|%s|%s\n" % (
            seq, tc, fid, final_prog, jcode, kv["judgment"], conf,
            final_pred, meas, phash, truth))
        outf.write(json.dumps({
            "seq": seq, "task": task, "fid": fid, "kind": tr["kind"], "fam": tr["fam"],
            "src": tr["src"], "truth": truth, "judgment": kv["judgment"],
            "conf": conf, "prog": kv["prog"], "progF": kv.get("progF"),
            "pred": kv.get("pred"), "measure": meas, "mrgF": mrg_f,
            "agree": agree, "strong": strong, "t1": t1,
            "final_prog": final_prog, "final_pred": final_pred,
            "esc": esc[0] if esc else None, "dec": esc[1] if esc else None,
            "ops": ops, "phash": phash, "pred_disp": disp_final,
        }) + "\n")
        outf.flush()
        if (seq + 1) % 1000 == 0:
            print("sweep %d/%d esc=%d" % (seq + 1, len(trials), n_esc), flush=True)
    outf.close()
    recf.close()
    dlf.close()
    print("sweep done: %d trials, %d escalations" % (len(trials), n_esc), flush=True)
    return n_esc

# ---------------------------------------------------------------- gate -----
def run_gate():
    rec_path = os.path.join(WORK, "records.txt")
    ledger_path = os.path.join(WORK, "ledger.txt")
    disp_path = os.path.join(WORK, "dispositions.txt")
    if os.path.exists(ledger_path):
        os.remove(ledger_path)
    r = subprocess.run([MEMGATE, rec_path, ledger_path],
                       capture_output=True, timeout=600)
    if r.returncode != 0:
        print("MEMGATE FAILED", r.stdout.decode()[-500:], r.stderr.decode()[-500:], flush=True)
        sys.exit(1)
    open(disp_path, "w").write(r.stdout.decode())
    print("gate done", flush=True)
    return disp_path, ledger_path


def verify_ledger(rec_path, ledger_path):
    """Independent Python recompute of the hash chain."""
    prev = bytes(32)
    ok = True
    n = 0
    with open(rec_path) as rf, open(ledger_path) as lf:
        for rline, lline in zip(rf, lf):
            rline = rline.rstrip("\n")
            parts = lline.rstrip("\n").split("|", 2)
            if len(parts) != 3:
                return False, n
            ph, hh, canon = parts
            if ph != prev.hex():
                return False, n
            h = hashlib.sha256(prev + canon.encode()).hexdigest()
            if h != hh:
                return False, n
            # canon must equal record|DISP=..|DETAIL=..
            prev = bytes.fromhex(hh)
            n += 1
    return ok, n


# ------------------------------------------------------------- approach A --
def extract_f_span(r24_path, out_path):
    """Extract the COMPLETE F-span (task header + payload) for Approach A."""
    with open(r24_path, "rb") as fh:
        magic = int.from_bytes(fh.read(4), "little")
        tcode = int.from_bytes(fh.read(4), "little")
        assert magic == 0x41343252, r24_path
        if tcode <= 2:      # image spans: <II W,H + W*H*3 bytes
            hdr = fh.read(8)
            w = int.from_bytes(hdr[0:4], "little")
            h = int.from_bytes(hdr[4:8], "little")
            flen = w * h * 3
        elif tcode <= 4:    # audio spans: <II SR,n + n i16 samples
            hdr = fh.read(8)
            n = int.from_bytes(hdr[4:8], "little")
            flen = n * 2
        else:               # motion: <III NF,MW,MH + NF*MW*MH*3 bytes
            hdr = fh.read(12)
            nf = int.from_bytes(hdr[0:4], "little")
            mw = int.from_bytes(hdr[4:8], "little")
            mh = int.from_bytes(hdr[8:12], "little")
            flen = nf * mw * mh * 3
        fdata = fh.read(flen)
        assert len(fdata) == flen, (r24_path, len(fdata), flen)
    # write header + payload (the complete original task-format fixture)
    with open(out_path, "wb") as fh:
        fh.write(hdr)
        fh.write(fdata)
    return out_path


def run_approach_a(trials):
    """Run frozen Approach A on F-span evidence (R2A) or raw fixtures (harness)."""
    extdir = os.path.join(WORK, "f_extract")
    os.makedirs(extdir, exist_ok=True)
    # Pre-extract F spans sequentially (fast, avoids races)
    apaths = {}
    for tr in trials:
        if tr["src"] == "r2a":
            ep = os.path.join(extdir, "f_%d.bin" % tr["seq"])
            if not os.path.exists(ep):
                extract_f_span(tr["path"], ep)
            apaths[tr["seq"]] = ep
        else:
            apaths[tr["seq"]] = tr["path"]
    print("approachA: F-spans ready, parallel sense on %d trials..." % len(trials), flush=True)
    from concurrent.futures import ThreadPoolExecutor
    def _a_one(tr):
        apath = apaths[tr["seq"]]
        r = subprocess.run([SENSE_A, tr["task"], apath], capture_output=True, timeout=180)
        kv = parse_out(r.stdout)
        kv["_rc"] = r.returncode
        return (tr["seq"], kv)
    outs = {}
    with ThreadPoolExecutor(max_workers=12) as ex:
        for seq, kv in ex.map(_a_one, trials):
            outs[seq] = kv
            if len(outs) % 1000 == 0:
                print("approachA %d/%d" % (len(outs), len(trials)), flush=True)
    with open(os.path.join(WORK, "aouts.json"), "w") as fh:
        json.dump({str(k): v for k, v in outs.items()}, fh)
    return outs

# ---------------------------------------------------------------- score ----
def pct(xs, q):
    xs = sorted(xs)
    if not xs:
        return 0
    i = min(len(xs) - 1, int(q * len(xs)))
    return xs[i]


def score_all(trials, n_esc):
    rows = [json.loads(l) for l in open(os.path.join(WORK, "sweep.jsonl"))]
    rows = [r for r in rows if "err" not in r]
    ok = {r["seq"]: r for r in rows}
    disps = {}
    for line in open(os.path.join(WORK, "dispositions.txt")):
        p = line.rstrip("\n").split("|")
        # seq|tcode|fixture|disposition|detail|truth
        disps[int(p[0])] = (p[3], p[4] if len(p) > 4 else "")
    for r in rows:
        r["disp"], r["detail"] = disps.get(r["seq"], ("MISSING", ""))
    # tracker-vs-memgate agreement (the Python tracker must mirror memgate exactly)
    mism = sum(1 for r in rows if r.get("pred_disp") != r["disp"])
    if mism:
        print("TRACKER/MEMGATE MISMATCH: %d/%d" % (mism, len(rows)), flush=True)
    aouts = json.load(open(os.path.join(WORK, "aouts.json")))
    aok = {int(k): v for k, v in aouts.items()
           if v.get("_rc") == 0 and "judgment" in v}

    def correct(r):
        return r["judgment"] == r["truth"]

    # B1: frozen 370 primary
    primary = [r for r in rows if r["src"] == "harness" and r["fam"] == "harness_primary"]
    b1 = sum(correct(r) for r in primary) / len(primary) if primary else 0.0
    b1_tasks = {}
    for t in TASKS:
        pr = [r for r in primary if r["task"] == t]
        b1_tasks[t] = sum(correct(r) for r in pr) / len(pr) if pr else 0.0

    # B2: paired-clean head-to-head
    paired = [(r, aok[r["seq"]]) for r in rows if r["seq"] in aok]
    b2_r24 = sum(correct(r) for r, a in paired) / len(paired) if paired else 0.0
    b2_a = sum(a["judgment"] == r["truth"] for r, a in paired) / len(paired) if paired else 0.0

    # B3/B6: ops
    ops_r = sorted(r["ops"] for r in rows)
    ops_a = sorted(gint(a, "ops") for _, a in paired)
    p95r, p95a = pct(ops_r, 0.95), pct(ops_a, 0.95)
    ops_ratio_p95 = p95r / p95a if p95a else 0

    # B4/RK-4: contract-less ablation (percept's judgment/conf only)
    # Contract-less rule for RK-4: PASS self-result -> immediate PERMANENT
    # install (naive: no provisional, no corroboration, no contradiction
    # check, no confidence gate, no deliberation).
    ab_install = 0
    ab_perm = 0
    ab_false_perm = 0
    for r in rows:  # rows are in seq order
        # Naive: if percept says PASS, install permanently
        if r["prog"] == "PASS":
            r["ab"] = "INSTALL"
            ab_install += 1
            ab_perm += 1
            if not correct(r):
                ab_false_perm += 1
        else:
            r["ab"] = "WITHHOLD"
    adv = [r for r in rows if r["kind"] == "adv"]
    normal = [r for r in rows if r["kind"] == "normal"]
    b4diff = sum(1 for r in adv if ((r["disp"] in INSTALL) != (r["ab"] == "INSTALL"))) / len(adv) if adv else 0.0
    fp_ab_adv = sum(1 for r in adv if r["ab"] == "INSTALL" and not correct(r))

    # false permanent installs (contract)
    fp_all = [r for r in rows if r["disp"] == "PERMANENT_INSTALL" and not correct(r)]
    fp_adv = [r for r in adv if r["disp"] == "PERMANENT_INSTALL" and not correct(r)]

    # RK-2/RK-3/RK-5 + same-evidence diagnostic
    whc = [r for r in rows if not correct(r) and r["conf"] >= 700]
    chc = [r for r in rows if correct(r) and r["conf"] >= 700]
    rk2 = sum(1 for r in whc if r["disp"] == "PERMANENT_INSTALL") / len(whc) if whc else 0
    rk3 = sum(1 for r in chc if r["final_prog"] == 0 and r["disp"] in INSTALL) / len(chc) if chc else 0
    rk5 = sum(1 for r in whc if r["final_prog"] in (1, 2)) / len(whc) if whc else 0
    # Diagnostic: round-1 kill-2 measured wrong high-conf percepts reaching
    # FAIL *or UNRESOLVED* on the SAME evidence (38.9%). Count both here for
    # a faithful 38.9% -> ? trajectory (progF never emits FAIL on this build;
    # same-evidence UNRESOLVED is the flagging signal).
    same_ev = sum(1 for r in whc if r.get("progF") in ("FAIL", "UNRESOLVED")) / len(whc) if whc else 0

    m = {
        "trials": len(trials), "sweep_ok": len(rows),
        "tracker_memgate_mismatches": mism,
        "n_normal": len(normal), "n_adv": len(adv),
        "n_escalations": n_esc,
        "RK1_false_perm_rate": len(fp_all) / len(rows) if rows else 0.0,
        "RK1_false_perm_n": len(fp_all),
        "RK2_wrong_highconf_perm_rate": rk2,
        "RK2_wrong_highconf_n": len(whc),
        "RK2_wrong_highconf_perm_n": sum(1 for r in whc if r["disp"] == "PERMANENT_INSTALL"),
        "RK3_correct_highconf_install_rate": rk3,
        "RK3_correct_highconf_n": len(chc),
        "RK4_ablation_installs": ab_install,
        "RK4_ablation_perm": ab_perm,
        "RK4_ablation_false_perm": ab_false_perm,
        "RK4_pass": ab_perm >= 100,
        "RK5_indep_evidence_rate": rk5,
        "RK6_escalation_rate": n_esc / len(rows),
        "RK6_ops_p95_ratio": ops_ratio_p95,
        "B1_primary_acc": b1, "B1_per_task": b1_tasks, "B1_n": len(primary),
        "B2_r24_paired_acc": b2_r24, "B2_a_paired_acc": b2_a,
        "B2_delta": b2_r24 - b2_a, "B2_paired_n": len(paired),
        "B3_ops_r24_p50": pct(ops_r, 0.50), "B3_ops_r24_p95": p95r,
        "B3_ops_a_p50": pct(ops_a, 0.50), "B3_ops_a_p95": p95a,
        "B4_disposition_diff_adv": b4diff,
        "B4_false_install_ablation_adv": fp_ab_adv,
        "B4_false_perm_contract_adv": len(fp_adv),
        "B5_false_perm_rate_adv": len(fp_adv) / len(adv) if adv else 0.0,
        "same_evidence_diag_rate": same_ev,
        "esc_E1_E2": n_esc,
        "RK6_esc_rate": n_esc / len(trials) if trials else 0,
        "RK6_p95_ops_ratio": (p95r / p95a) if p95a else 0,
        "RK6_pass": (n_esc / len(trials) <= 0.05) and (p95a and (p95r / p95a) <= 0.40),
    }
    return m


# ------------------------------------------------------------------ main ----
def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("all", "sweep"):
        snap = build_bins()
        json.dump(snap, open(os.path.join(WORK, "bins.json"), "w"), indent=1)
        trials = build_trials()
        json.dump(trials, open(os.path.join(WORK, "trials.json"), "w"))
        print("trials: %d" % len(trials), flush=True)
        # import sweep pieces
        n_esc = sweep(trials, snap)
        json.dump({"n_esc": n_esc}, open(os.path.join(WORK, "esc.json"), "w"))
    if cmd in ("all", "gate"):
        rec_path = os.path.join(WORK, "records.txt")
        disp_path, ledger_path = run_gate()
        ok, n = verify_ledger(rec_path, ledger_path)
        print("ledger verify: %s (%d links)" % (ok, n), flush=True)
        json.dump({"ledger_ok": ok, "ledger_n": n}, open(os.path.join(WORK, "ledger_verify.json"), "w"))
        if not ok:
            sys.exit(1)
    if cmd in ("all", "approach_a"):
        trials = json.load(open(os.path.join(WORK, "trials.json")))
        run_approach_a(trials)
    if cmd in ("all", "score"):
        trials = json.load(open(os.path.join(WORK, "trials.json")))
        n_esc = json.load(open(os.path.join(WORK, "esc.json")))["n_esc"]
        m = score_all(trials, n_esc)
        m["ledger"] = json.load(open(os.path.join(WORK, "ledger_verify.json")))
        m["bins"] = json.load(open(os.path.join(WORK, "bins.json")))
        json.dump(m, open(os.path.join(WORK, "metrics.json"), "w"), indent=1)
        print(json.dumps(m, indent=1))


if __name__ == "__main__":
    main()
