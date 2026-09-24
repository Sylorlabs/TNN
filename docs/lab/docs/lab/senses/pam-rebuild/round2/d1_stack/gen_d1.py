#!/usr/bin/env python3
"""gen_d1.py — D1 stack battery generator (frozen PREREG_D1_STACK.md).

Builds, deterministically (zero RNG):
  stack_records.zag  — per-stream trial tables (u8 arenas, LE i64 words)
  stack_gatt.zag     — per-stream attestation tag tables
  EXPECT_D1.tsv      — per-trial expected disposition (leg,trial_idx,disp,install)
  EXPECT_D1_CELL.tsv — per-leg aggregate counts
  gatt_leg3.txt      — generated cell attestation sidecar (frozen key)

Python mirror of the frozen stack rules (gate G1 -> guard MG6 -> hardening H6
R1-R4) produces EXPECT. Hand-verified on all kill-bar-critical trials.
"""
import hashlib, json, os, struct

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = b"PAMV2-REG-CHANNEL-2026-09-23"

# ---------- frozen tables ----------
TOLS = {0: 8, 1: 40, 2: 60, 3: 4000, 4: 120, 5: 0}
# disposition codes (same as the matrix)
D_PERM, D_PROV, D_CORR, D_CONF, D_CHAL, D_REV, D_ACC, D_WITH = 0, 1, 2, 3, 4, 5, 6, 7
DNAMES = {0: "PERM", 1: "PROV", 2: "CORR", 3: "CONF", 4: "CHAL",
          5: "REV", 6: "ACC", 7: "WITH"}

def parse_records(path):
    recs = []
    for line in open(path):
        f = line.rstrip("\n").split("|")
        recs.append({
            "seq": int(f[0]), "tcode": int(f[1]), "fixture": f[2],
            "prog": 0 if f[3] == "PASS" else 2,
            "jcode": int(f[4]), "judgment": f[5], "conf": int(f[6]),
            "pred": int(f[7]), "meas": int(f[8]), "phash": f[9],
            "truth": f[10], "jG": int(f[11]), "confG": int(f[12]),
        })
    return recs

def derive_span(phash):
    b = bytes.fromhex(phash)
    a = int.from_bytes(b[0:8], "big") % 20000
    bb = a + 1 + (int.from_bytes(b[8:16], "big") % 4000)
    return a, bb

def load_gatt(path):
    g = {}
    for line in open(path):
        s, tag = line.strip().split("|")
        g[int(s)] = tag
    return g

# ---------- streams ----------
streams = {}   # name -> list of trial dicts
gatt_src = {}  # name -> {trial_idx: tag}

# Leg 1: 43 F5 candidates, replay framing prog=PASS/pred=1
f5 = []
for li, line in enumerate(open(os.path.join(HERE, "f5_run1.out"))):
    line = line.strip()
    if not line:
        continue
    f = line.split("\t")
    if len(f) < 4:
        continue
    # fixture|truth|blocked|nearest  (fixture e.g. rt4_PTC-4_0000.r24)
    f5.append({"idx": li, "fixture": f[0], "truth": f[1],
               "blocked": f[2] == "BLOCKED"})
withrec = {r["fixture"]: r for r in
           parse_records(os.path.join(HERE, "rec_withhold.records"))}
wgatt = load_gatt(os.path.join(HERE, "withhold.gatt"))
# direct fixture-name match (verified identical 2026-09-24); all withhold
# records are UNRESOLVED by construction.
assert len(f5) == 43
leg1 = []
for c in f5:
    r0 = withrec[c["fixture"]]
    assert r0["prog"] == 2, c["fixture"]
    r = dict(r0)
    r["prog"] = 0
    r["pred"] = 1
    r["mrgF"] = r["meas"]
    r["span_a"], r["span_b"] = derive_span(r["phash"])
    r["leg_idx"] = c["idx"]
    leg1.append(r)
leg1.sort(key=lambda r: r["seq"])
streams["leg1"] = leg1
gatt_src["leg1"] = {i: wgatt[r["seq"]] for i, r in enumerate(leg1)}

# Leg 2: 12 TMB-5 install-stream wrongs, verbatim
irec = {r["seq"]: r for r in parse_records(os.path.join(HERE, "rec_install.records"))}
igatt = load_gatt(os.path.join(HERE, "install.gatt"))
leg2 = []
for sq in range(24, 36):
    r = dict(irec[sq])
    r["mrgF"] = r["meas"]
    r["span_a"], r["span_b"] = derive_span(r["phash"])
    leg2.append(r)
streams["leg2"] = leg2
gatt_src["leg2"] = {i: igatt[r["seq"]] for i, r in enumerate(leg2)}

# Leg 3: 10 CM cells, exact frozen rows
cells = json.load(open(os.path.join(HERE, "cells_frozen.json")))
CELL_ORDER = ["C1", "C2", "C3", "R1", "R2", "CC1", "CC2", "H1", "T1", "W1"]
for cn in CELL_ORDER:
    leg3 = []
    g3 = {}
    for ri, row in enumerate(cells[cn]["rows"]):
        (tcode, prog, jcode, conf, pred, meas, mrgF, truth,
         jG, confG, seq, sa, sb) = row
        fx = "%s#%d" % (cn, ri)
        ib = KEY + b"|" + str(seq).encode() + b"|" + fx.encode() + b"|" + \
            str(jG).encode() + b"|" + str(confG).encode()
        tag = hashlib.sha256(ib).hexdigest()
        g3[len(leg3)] = tag
        leg3.append({
            "seq": seq, "tcode": tcode, "fixture": fx, "prog": prog,
            "jcode": jcode, "judgment": str(jcode), "conf": conf,
            "pred": pred, "meas": meas, "phash": "00" * 32,
            "truth": str(truth), "jG": jG, "confG": confG,
            "mrgF": mrgF, "span_a": sa, "span_b": sb,
        })
    streams["leg3_"+cn] = leg3
    gatt_src["leg3_"+cn] = g3
    with open(os.path.join(HERE, "gatt_leg3_%s.txt" % cn), "w") as f:
        for i in sorted(g3):
            f.write("%d|%s\n" % (i, g3[i]))

# Leg 4: four redteam streams, verbatim fields
for sname, rfile, gfile in [
        ("leg4_clean", "rec_clean.records", "clean.gatt"),
        ("leg4_withhold", "rec_withhold.records", "withhold.gatt"),
        ("leg4_install", "rec_install.records", "install.gatt"),
        ("leg4_decoy", "rec_decoy.records", "decoy.gatt")]:
    recs = parse_records(os.path.join(HERE, rfile))
    g = load_gatt(os.path.join(HERE, gfile))
    trials = []
    for r in recs:
        r["mrgF"] = r["meas"]
        r["span_a"], r["span_b"] = derive_span(r["phash"])
        trials.append(r)
    streams[sname] = trials
    gatt_src[sname] = {i: g[r["seq"]] for i, r in enumerate(trials)}

print("streams:", {k: len(v) for k, v in streams.items()})

# ---------- Python mirror of the frozen stack rules ----------
# Gate state per tcode: dict with prov/perm/chal slots; each slot holds the
# full trial dict (or None) plus its gatt tag.

def gate_step(st, t, tag):
    tol = TOLS[t["tcode"]]
    prog, jc, conf, pred, meas = t["prog"], t["jcode"], t["conf"], t["pred"], t["meas"]
    if prog != 0 or pred != 1:
        return D_WITH, "gate-prog-pred", None
    prov, perm, chal = st["prov"], st["perm"], st["chal"]
    if perm and jc == perm["t"]["jcode"] and abs(meas - perm["t"]["meas"]) <= tol:
        return D_CORR, "gate-corr", None
    if prov and not perm and jc == prov["t"]["jcode"] \
            and abs(meas - prov["t"]["meas"]) <= tol:
        if conf >= 700:
            return "PROPOSE_PERM", "gate-propose-perm", (prov, {"t": t, "tag": tag})
        return D_PROV, "gate-prov-lowconf", None
    if perm or prov:
        ij = perm["t"]["jcode"] if perm else prov["t"]["jcode"]
        if jc != ij:
            if conf >= 700:
                if chal and chal["t"]["jcode"] == jc \
                        and abs(meas - chal["t"]["meas"]) <= tol:
                    return "PROPOSE_REV", "gate-propose-rev", (chal, {"t": t, "tag": tag})
                st["chal"] = {"t": t, "tag": tag}
                return D_CHAL, "gate-chal", None
            return D_CONF, "gate-conf-lowconf", None
        st["prov"] = {"t": t, "tag": tag}
        return D_PROV, "gate-reanchor", None
    st["prov"] = {"t": t, "tag": tag}
    return D_PROV, "gate-first-prov", None

def guard_check(pair):
    s, tt = pair[0]["t"], pair[1]["t"]
    arms = []
    if min(s["mrgF"], tt["mrgF"]) < 400:
        arms.append("margin")
    if s["span_a"] < tt["span_b"] and tt["span_a"] < s["span_b"]:
        arms.append("span")
    if abs(s["seq"] - tt["seq"]) < 20:
        arms.append("temporal")
    return arms

def att_ok(tr, tag):
    t = tr["t"]
    ib = KEY + b"|" + str(t["seq"]).encode() + b"|" + t["fixture"].encode() + \
        b"|" + str(t["jG"]).encode() + b"|" + str(t["confG"]).encode()
    return hashlib.sha256(ib).hexdigest() == tag

def harden(pair, is_rev, hist, perm, tcode):
    for tr in pair:
        t = tr["t"]
        if t["prog"] != 0:
            return False, "harden-r1"
        if not att_ok(tr, tr["tag"]):
            return False, "harden-r2"
        if not (t["conf"] >= 700 and t["jG"] == t["jcode"] and t["confG"] >= 700):
            return False, "harden-r3"
    if is_rev and perm is not None:
        # R4: revision-vs-permanent only when a permanent is installed
        tol = TOLS[tcode]
        tj = pair[1]["t"]["jcode"]
        tm = pair[1]["t"]["meas"]
        corr = any(h[0] == tcode and h[1] == tj and h[2] == 0
                   and abs(h[3] - tm) <= tol for h in hist)
        if not corr or (pair[1]["t"]["conf"] - perm["t"]["conf"]) < 100:
            return False, "harden-r4"
    return True, "harden-ok"

def run_stream(trials, gtags):
    states = {}
    hist = []
    out = []
    for ti, t in enumerate(trials):
        tc = t["tcode"]
        st = states.setdefault(tc, {"prov": None, "perm": None, "chal": None})
        tag = gtags[ti]
        disp, detail, pair = gate_step(st, t, tag)
        install = 0
        if disp == "PROPOSE_PERM" or disp == "PROPOSE_REV":
            is_rev = (disp == "PROPOSE_REV")
            arms = guard_check(pair)
            if arms:
                disp = D_CHAL if is_rev else D_PROV
                detail = "guard-veto:" + "+".join(arms)
            else:
                ok, hdetail = harden(pair, is_rev, hist, st["perm"], tc)
                if ok:
                    st["perm"] = {"t": pair[1]["t"], "tag": pair[1]["tag"]}
                    st["prov"] = None
                    st["chal"] = None
                    disp = D_REV if is_rev else D_PERM
                    detail = hdetail
                    install = 1
                else:
                    disp = D_WITH
                    detail = hdetail
        out.append((ti, disp, detail, install))
        hist.append((tc, t["jcode"], t["prog"], t["meas"]))
    return out

EXPECT = {}
CELL = {}
for sname, trials in streams.items():
    res = run_stream(trials, gatt_src[sname])
    EXPECT[sname] = res
    n_inst = sum(r[3] for r in res)
    n_false = sum(r[3] for r in res
                  if trials[r[0]]["judgment"] != trials[r[0]]["truth"])
    CELL[sname] = (len(res), n_inst, n_false)
    print("%-14s trials=%4d installs=%3d false_installs=%d"
          % (sname, len(res), n_inst, n_false))

with open(os.path.join(HERE, "EXPECT_D1.tsv"), "w") as f:
    f.write("leg\ttrial_idx\tdisp\tinstall\n")
    for sname, res in EXPECT.items():
        for ti, disp, detail, inst in res:
            f.write("%s\t%d\t%s\t%d\n" % (sname, ti, disp, inst))
with open(os.path.join(HERE, "EXPECT_D1_CELL.tsv"), "w") as f:
    f.write("leg\ttrials\tinstalls\tfalse_installs\n")
    for sname, (n, ni, nf) in CELL.items():
        f.write("%s\t%d\t%d\t%d\n" % (sname, n, ni, nf))

# ---------- emit Zag tables ----------
# Trial layout: 14 LE i64 words = 112 bytes:
#   0 seq, 1 tcode, 2 prog, 3 jcode, 4 conf, 5 pred, 6 meas, 7 mrgF,
#   8 jG, 9 confG, 10 span_a, 11 span_b, 12 fixture_off, 13 fixture_len
# Pattern follows gen_guard.py: init-functions with t_put64 / byte puts
# (Zag array literals do not support large initializers).

def emit_stream_zag(sname, trials, gtags):
    fxtab = b""
    fx_off = []
    for t in trials:
        fb = t["fixture"].encode()
        fx_off.append((len(fxtab), len(fb)))
        fxtab += fb
    gatt = bytearray()
    for ti in range(len(trials)):
        # ASCII hex (64 chars), matching ns_hex output compared in att_verify
        gatt += gtags[ti].encode("ascii")
    L = []
    L.append("// generated by gen_d1.py — do not hand-edit")
    L.append("const D1_%s_N:i64=%d;" % (sname.upper(), len(trials)))
    L.append("const D1_%s_FXLEN:i64=%d;" % (sname.upper(), len(fxtab)))
    L.append("const D1_%s_GTLEN:i64=%d;" % (sname.upper(), len(gatt)))
    L.append("fn d1_%s_init_trials(tr:[]u8) void {" % sname)
    for ti, t in enumerate(trials):
        off, ln = fx_off[ti]
        words = [t["seq"], t["tcode"], t["prog"], t["jcode"], t["conf"],
                 t["pred"], t["meas"], t["mrgF"], t["jG"], t["confG"],
                 t["span_a"], t["span_b"], off, ln]
        base = ti * 112
        for f, w in enumerate(words):
            L.append("    t_put64(tr,%d,%d);" % (base + f * 8, w))
    L.append("}")
    L.append("fn d1_%s_init_fx(fx:[]u8) void {" % sname)
    for i, b in enumerate(fxtab):
        L.append("    fx[%d]=%d;" % (i, b))
    L.append("}")
    L.append("fn d1_%s_init_gatt(gt:[]u8) void {" % sname)
    for i, b in enumerate(gatt):
        L.append("    gt[%d]=%d;" % (i, b))
    L.append("}")
    return "\n".join(L)

parts = []
for sname, trials in streams.items():
    parts.append(emit_stream_zag(sname, trials, gatt_src[sname]))
with open(os.path.join(HERE, "stack_records.zag"), "w") as f:
    f.write("\n\n".join(parts) + "\n")
print("wrote stack_records.zag (%d bytes)" %
      os.path.getsize(os.path.join(HERE, "stack_records.zag")))
