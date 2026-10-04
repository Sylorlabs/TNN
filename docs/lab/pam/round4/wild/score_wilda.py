#!/usr/bin/env python3
"""WILD-A round-4 battery scorer. Asserts frozen tape SHA, runs each design
2x (K2 byte-identical), parses per-row ledgers, applies kill bars
mechanically (K1-K5 + per-design added bars). Writes evidence files."""
import hashlib, json, subprocess, sys, time, os

WILD = os.path.expanduser("~/workspace/tnn-lab/pam/round4/wild")
TAPE = os.path.expanduser("~/workspace/tnn-lab/pam/round3/m1/m1_cases.txt")
TAPE_SHA = "5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611"

def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def run_bin(d, tape=TAPE):
    b = os.path.join(WILD, d, d)
    t0 = time.time()
    r = subprocess.run([b, tape], capture_output=True, timeout=300)
    dt = time.time() - t0
    assert r.returncode == 0, f"{d} rc={r.returncode} stderr={r.stderr[:200]}"
    return r.stdout, dt

def parse(out):
    rows, kv = [], {}
    for line in out.decode().splitlines():
        if line.startswith("R|"):
            rows.append(line.split("|"))
        elif "=" in line:
            k, v = line.split("=", 1)
            kv[k] = v
    return rows, kv

def verdict(name, kv, rows, checks, notes):
    """checks: list of (bar, status, detail) with status in KILL/HOLD/PASS."""
    status = "SURVIVE"
    for bar, st, _ in checks:
        if st == "KILL":
            status = "KILL"
            break
    if status != "KILL":
        for bar, st, _ in checks:
            if st == "HOLD":
                status = "HOLD"
                break
    return {"design": name, "status": status, "kv": kv,
            "nrows": len(rows), "bars": checks, "notes": notes}

def k4_probe(d):
    """K4: per-row wall time on 1000-row prefix vs full tape; report ratio."""
    with open(TAPE) as f:
        lines = f.readlines()
    pre = "/tmp/k4_prefix.txt"
    with open(pre, "w") as f:
        f.writelines(lines[:1000])
    _, dt1 = run_bin(d, pre)
    _, dt2 = run_bin(d, TAPE)
    per1 = dt1 / 1000.0
    per2 = dt2 / 2241.0
    ratio = per2 / per1 if per1 > 0 else 0
    return per1, per2, ratio

results = {}
timings = {}

# Tape SHA gate: no metric is computed unless the frozen tape matches.
got = sha_file(TAPE)
assert got == TAPE_SHA, f"TAPE SHA MISMATCH: {got}"
print(f"tape_sha_ok {got[:16]}", file=sys.stderr)

# ---------------- W1 ----------------
d = "w1"
out1, dt1 = run_bin(d); out2, dt2 = run_bin(d)
k2 = (out1 == out2)
rows, kv = parse(out1)
checks = []
checks.append(("K2", "KILL" if not k2 else "PASS", f"2x sha={hashlib.sha256(out1).hexdigest()[:16]}"))
c = int(kv["c_admit"]); checks.append(("K3", "HOLD" if c / 1102 < 0.6678 else "PASS", f"{c}/1102={c/1102*100:.2f}%"))
checks.append(("K1", "KILL" if int(kv["w_admit"]) > 0 else "PASS", f"w_admit={kv['w_admit']}"))
checks.append(("K1", "KILL" if int(kv["p_pair_installs"]) > 0 else "PASS", f"pair_installs={kv['p_pair_installs']}"))
# F-K4: every false percept (W/P/A) must have CON_sum > 0
bad = [r for r in rows if r[2] in ("1", "2", "4", "5", "6") and int(r[4]) <= 0]
checks.append(("F-K4", "KILL" if bad else "PASS", f"{len(bad)} false percepts with CON_sum=0"))
checks.append(("K5", "PASS", "terminated"))
p1, p2, ratio = k4_probe(d); timings[d] = (p1, p2, ratio)
checks.append(("K4", "KILL" if ratio > 4 else "PASS", f"per-row {p1*1e6:.1f}us-> {p2*1e6:.1f}us ratio={ratio:.2f}"))
results[d] = verdict("W1_DELIB_VOTE", kv, rows, checks,
    [f"a_admit={kv['a_admit']}", f"b_admit={kv['b_admit']}"])

# ---------------- W2 ----------------
d = "w2"
out1, _ = run_bin(d); out2, _ = run_bin(d)
k2 = (out1 == out2)
rows, kv = parse(out1)
checks = []
checks.append(("K2", "KILL" if not k2 else "PASS", f"2x sha={hashlib.sha256(out1).hexdigest()[:16]}"))
c = int(kv["c_admit"]); checks.append(("K3", "HOLD" if c / 1102 < 0.6678 else "PASS", f"{c}/1102={c/1102*100:.2f}%"))
checks.append(("K1", "KILL" if int(kv["w_admit"]) > 0 else "PASS", f"w_admit={kv['w_admit']}"))
checks.append(("K1", "KILL" if int(kv["p_pair_installs"]) > 0 else "PASS", f"pair_installs={kv['p_pair_installs']}"))
checks.append(("W2-A1", "KILL" if int(kv["a_admit"]) > 0 else "PASS", f"a_admit={kv['a_admit']}"))
checks.append(("W2-A2", "KILL" if int(kv["fork_fail"]) > 0 else "PASS", f"fork_fail={kv['fork_fail']}"))
checks.append(("K5", "PASS", "terminated"))
p1, p2, ratio = k4_probe(d); timings[d] = (p1, p2, ratio)
checks.append(("K4", "KILL" if ratio > 4 else "PASS", f"ratio={ratio:.2f}"))
results[d] = verdict("W2_ADV_PAIR", kv, rows, checks, [f"b_admit={kv['b_admit']}"])

# ---------------- W3 ----------------
d = "w3"
out1, _ = run_bin(d); out2, _ = run_bin(d)
k2 = (out1 == out2)
rows, kv = parse(out1)
checks = []
checks.append(("K2", "KILL" if not k2 else "PASS", f"2x sha={hashlib.sha256(out1).hexdigest()[:16]}"))
c = int(kv["c_admit"]); checks.append(("K3", "HOLD" if c / 1102 < 0.6678 else "PASS", f"{c}/1102={c/1102*100:.2f}%"))
checks.append(("K1", "KILL" if int(kv["w_admit"]) > 0 else "PASS", f"w_admit={kv['w_admit']}"))
checks.append(("K1", "KILL" if int(kv["p_pair_installs"]) > 0 else "PASS", f"pair_installs={kv['p_pair_installs']}"))
checks.append(("W3-A1", "KILL" if int(kv["a_admit"]) > 0 else "PASS", f"a_admit={kv['a_admit']}/a_vetoed={kv['a_vetoed']}"))
checks.append(("W3-A2", "KILL" if int(kv["fork_fail"]) > 0 else "PASS", f"fork_fail={kv['fork_fail']}"))
checks.append(("K5", "PASS", "terminated"))
p1, p2, ratio = k4_probe(d); timings[d] = (p1, p2, ratio)
checks.append(("K4", "KILL" if ratio > 4 else "PASS", f"ratio={ratio:.2f}"))
results[d] = verdict("W3_VETO_ONLY", kv, rows, checks, [f"b_admit={kv['b_admit']}"])

# ---------------- W6 ----------------
d = "w6"
out1, _ = run_bin(d); out2, _ = run_bin(d)
k2 = (out1 == out2)
rows, kv = parse(out1)
checks = []
checks.append(("K2", "KILL" if not k2 else "PASS", f"2x sha={hashlib.sha256(out1).hexdigest()[:16]}"))
c = int(kv["c_admit"]); checks.append(("K3", "HOLD" if c / 1102 < 0.6678 else "PASS", f"{c}/1102={c/1102*100:.2f}%"))
checks.append(("K1", "KILL" if int(kv["w_admit"]) > 0 else "PASS", f"w_admit={kv['w_admit']}"))
checks.append(("K1", "KILL" if int(kv["p_pair_installs"]) > 0 else "PASS", f"pair_installs={kv['p_pair_installs']}"))
checks.append(("W6-A1", "KILL" if int(kv["a_admit"]) > 0 else "PASS", f"a_admit={kv['a_admit']}"))
checks.append(("W6-A2", "KILL" if int(kv["fork_fail"]) > 0 else "PASS", f"fork_fail={kv['fork_fail']}"))
checks.append(("K5", "PASS", "terminated"))
p1, p2, ratio = k4_probe(d); timings[d] = (p1, p2, ratio)
checks.append(("K4", "KILL" if ratio > 4 else "PASS", f"ratio={ratio:.2f}"))
results[d] = verdict("W6_ARGUE", kv, rows, checks, [f"b_admit={kv['b_admit']}"])

# ---------------- W8 ----------------
d = "w8"
out1, _ = run_bin(d); out2, _ = run_bin(d)
k2 = (out1 == out2)
rows, kv = parse(out1)
checks = []
checks.append(("K2", "KILL" if not k2 else "PASS", f"2x sha={hashlib.sha256(out1).hexdigest()[:16]}"))
c = int(kv["c_confirmed"]); checks.append(("K3", "HOLD" if c / 1102 < 0.6678 else "PASS", f"confirmed {c}/1102={c/1102*100:.2f}%"))
checks.append(("K1", "KILL" if int(kv["w_confirmed"]) > 0 else "PASS", f"w_confirmed={kv['w_confirmed']}"))
checks.append(("K1", "KILL" if int(kv["p_pair_installs"]) > 0 else "PASS", f"pair_installs={kv['p_pair_installs']}"))
checks.append(("R1", "KILL" if int(kv["fence_cross"]) > 0 else "PASS", f"fence_cross={kv['fence_cross']}"))
wrongs_revoked = int(kv["w_revoked"]) + int(kv["p_revoked"])
checks.append(("R2", "KILL" if wrongs_revoked < 15 else "PASS", f"revoked {wrongs_revoked}/30 frozen wrongs"))
checks.append(("R3", "KILL" if int(kv["c_revoked"]) >= 110 else "PASS", f"c_revoked={kv['c_revoked']}"))
checks.append(("R4", "KILL" if int(kv["backlog"]) > 0 else "PASS", f"backlog={kv['backlog']}"))
checks.append(("K5", "PASS", "terminated"))
p1, p2, ratio = k4_probe(d); timings[d] = (p1, p2, ratio)
checks.append(("K4", "KILL" if ratio > 4 else "PASS", f"ratio={ratio:.2f}"))
results[d] = verdict("W8_RETRO", kv, rows, checks,
    [f"a_revoked={kv['a_revoked']}/a_confirmed={kv['a_confirmed']}", f"b_confirmed={kv['b_confirmed']}"])

# ---------------- W9 ----------------
d = "w9"
out1, _ = run_bin(d); out2, _ = run_bin(d)
k2 = (out1 == out2)
rows, kv = parse(out1)
checks = []
checks.append(("K2", "KILL" if not k2 else "PASS", f"2x sha={hashlib.sha256(out1).hexdigest()[:16]}"))
c = int(kv["c_admit"]); checks.append(("K3", "HOLD" if c / 1102 < 0.6678 else "PASS", f"{c}/1102={c/1102*100:.2f}%"))
checks.append(("K1", "KILL" if int(kv["w_pass"]) > 0 else "PASS", f"w_pass={kv['w_pass']}"))
checks.append(("K1", "KILL" if int(kv["p_pair_installs"]) > 0 else "PASS", f"pair_installs={kv['p_pair_installs']}"))
checks.append(("F1", "KILL" if int(kv["m1c_admit"]) < 774 else "PASS",
               f"m1c_admit={kv['m1c_admit']}/{kv['m1c_total']} (need>=774)"))
checks.append(("F2", "KILL" if int(kv["w_pass"]) + int(kv["p_pass"]) >= 3 else "PASS",
               f"wrongs_pass={int(kv['w_pass']) + int(kv['p_pass'])}"))
checks.append(("K5", "PASS", "terminated"))
p1, p2, ratio = k4_probe(d); timings[d] = (p1, p2, ratio)
checks.append(("K4", "KILL" if ratio > 4 else "PASS", f"ratio={ratio:.2f}"))
results[d] = verdict("W9_RENDER", kv, rows, checks, [f"b_pass={kv['b_pass']}"])

# ---------------- W14 ----------------
d = "w14"
out1, _ = run_bin(d); out2, _ = run_bin(d)
k2 = (out1 == out2)
rows, kv = parse(out1)
checks = []
checks.append(("K2", "KILL" if not k2 else "PASS", f"2x sha={hashlib.sha256(out1).hexdigest()[:16]}"))
c = int(kv["c_admit"]); checks.append(("K3", "HOLD" if c / 1102 < 0.6678 else "PASS", f"{c}/1102={c/1102*100:.2f}%"))
checks.append(("K1", "KILL" if int(kv["w_admit"]) > 0 else "PASS", f"w_admit={kv['w_admit']}"))
checks.append(("K1", "KILL" if int(kv["p_pair_installs"]) > 0 else "PASS", f"pair_installs={kv['p_pair_installs']}"))
checks.append(("F-K2a", "KILL" if int(kv["fk2a_viol"]) > 0 else "PASS", f"false margin>0: {kv['fk2a_viol']}"))
checks.append(("F-K2b", "KILL" if int(kv["fk2b_min_c_admit_margin"]) < 400 else "PASS",
               f"min C-admit margin={kv['fk2b_min_c_admit_margin']}"))
checks.append(("W14-A1", "KILL" if int(kv["fork_fail"]) > 0 else "PASS", f"fork_fail={kv['fork_fail']}"))
checks.append(("K5", "PASS", "terminated"))
p1, p2, ratio = k4_probe(d); timings[d] = (p1, p2, ratio)
checks.append(("K4", "KILL" if ratio > 4 else "PASS", f"ratio={ratio:.2f}"))
creds = [kv["cred_0"], kv["cred_1"], kv["cred_2"], kv["cred_3"], kv["cred_4"]]
results[d] = verdict("W14_AUCTION", kv, rows, checks,
    [f"a_admit={kv['a_admit']}", f"deactivations={kv['deactivations']}", f"creds={creds}", f"b_admit={kv['b_admit']}"])

print(json.dumps({"tape_sha_ok": True, "timings_us_per_row": {k: [round(a * 1e6, 1), round(b * 1e6, 1), round(c, 2)] for k, (a, b, c) in timings.items()}, "results": results}, indent=1))
