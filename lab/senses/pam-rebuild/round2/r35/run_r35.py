#!/usr/bin/env python3
"""run_r35.py — build + full R-35 battery, 3x byte-identical runs, bar scoring.

Batteries (per PREREG_R35.md):
  B1: repaired probe mode 35 x3, + original probe mode 35 x3 (regression:
      repaired stdout byte-identical to original)
  B2: J-35 class vs repaired driver x3            (repair bar: installs <= 15/120)
  B3: J-35 honest control x3                     (void if admits < 102/120)
  B4: K-35 / L-35 / M-35 vs repaired driver x3   (expect 0/120 each)
  B5: mode 36 repaired x3 vs original x3         (regression: byte-identical)

Outputs: runs/<battery>_run<N>.out, runs/SHA256SUMS, RUNLOG entry.
Any 3x SHA divergence -> VOID (exit 2).
"""
import hashlib, os, re, subprocess, sys

D = os.path.dirname(os.path.abspath(__file__))
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
ORIGSRC = os.path.join(D, "..", "round_c", "probe3536")
RUNS = os.path.join(D, "runs")
os.makedirs(RUNS, exist_ok=True)

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r

def build(src, out, cwd):
    r = run([ZNC, src, "-o", out], cwd=cwd)
    if r.returncode != 0 or not os.path.exists(out):
        print("BUILD FAILED:", src, r.stderr[:2000]); sys.exit(1)
    print("built", out)

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def bat(name, exe, args, n=3):
    """Run exe args n times; return (shas, outs). All stdout captured."""
    shas, outs = [], []
    for i in range(1, n + 1):
        r = run([exe] + args, cwd=D)
        if r.returncode != 0:
            print(f"RUN FAILED: {name} run{i}: {r.stderr[:500]}"); sys.exit(1)
        data = r.stdout.encode()
        p = os.path.join(RUNS, f"{name}_run{i}.out")
        with open(p, "wb") as f: f.write(data)
        shas.append(sha(data)); outs.append(data)
    return shas, outs

def grab(pat, data):
    m = re.search(pat, data.decode())
    return int(m.group(1)) if m else None

log = []
def note(s):
    print(s); log.append(s)

# --- builds ---
build("hpam3536_r35.zag", os.path.join(D, "probe_r35_bin"), D)
build("drive35_r35.zag", os.path.join(D, "drive35_r35_bin"), D)
build(os.path.join(ORIGSRC, "hpam3536_probe.zag"), os.path.join(D, "orig_probe_bin"), ORIGSRC)

# --- B1: repaired m35 x3 ---
sh_r35, out_r35 = bat("r35_m35", os.path.join(D, "probe_r35_bin"), ["35"])
sh_orig, out_orig = bat("orig_m35", os.path.join(D, "orig_probe_bin"), ["35"])
note(f"B1 r35_m35: 3x identical={len(set(sh_r35))==1} sha={sh_r35[0][:16]}")
note(f"B1 orig_m35: 3x identical={len(set(sh_orig))==1} sha={sh_orig[0][:16]}")
b1_regress = sh_r35[0] == sh_orig[0]
note(f"B1 REGRESSION repaired==original stdout: {b1_regress}")
d = out_r35[0].decode()
tot_adv = grab(r"p35_adv_total_admitted=(\d+)", out_r35[0])
h2 = grab(r"p35_h2_admitted=(\d+)", out_r35[0])
h1 = grab(r"p35_h1_admitted=(\d+)", out_r35[0])
delay = grab(r"p35_h1_max_delay=(\d+)", out_r35[0])
note(f"B1 bars: adv={tot_adv}/760 h2={h2}/40 h1={h1}/60 delay={delay}")

# --- B2: J-35 x3 ---
sh_j, out_j = bat("r35_j35", os.path.join(D, "drive35_r35_bin"), ["j"])
j_inst = grab(r"J35_INSTALL=(\d+)", out_j[0])
note(f"B2 J-35: 3x identical={len(set(sh_j))==1} installs={j_inst}/120 sha={sh_j[0][:16]}")

# --- B3: honest x3 ---
sh_h, out_h = bat("r35_honest", os.path.join(D, "drive35_r35_bin"), ["honest"])
h_admit = grab(r"H35_ADMIT=(\d+)", out_h[0])
note(f"B3 honest: 3x identical={len(set(sh_h))==1} admits={h_admit}/120 sha={sh_h[0][:16]}")

# --- B4: k/l/m x3 ---
results = {}
for cls, pat in [("k", r"K35_INSTALL=(\d+)"), ("l", r"L35_INSTALL=(\d+)"), ("m", r"M35_FIT=(\d+)")]:
    sh, out = bat(f"r35_{cls}35", os.path.join(D, "drive35_r35_bin"), [cls])
    v = grab(pat, out[0])
    results[cls] = v
    note(f"B4 {cls.upper()}-35: 3x identical={len(set(sh))==1} installs={v}/120 sha={sh[0][:16]}")

# --- B5: mode 36 regression x3 ---
sh_36r, _ = bat("r35_m36", os.path.join(D, "probe_r35_bin"), ["36"])
sh_36o, _ = bat("orig_m36", os.path.join(D, "orig_probe_bin"), ["36"])
note(f"B5 r35_m36: 3x identical={len(set(sh_36r))==1} sha={sh_36r[0][:16]}")
note(f"B5 orig_m36: 3x identical={len(set(sh_36o))==1} sha={sh_36o[0][:16]}")
b5_regress = sh_36r[0] == sh_36o[0]
note(f"B5 REGRESSION repaired==original mode36 stdout: {b5_regress}")

# --- SHA256SUMS ---
with open(os.path.join(RUNS, "SHA256SUMS"), "w") as f:
    for p in sorted(os.listdir(RUNS)):
        if p.endswith(".out"):
            with open(os.path.join(RUNS, p), "rb") as g:
                f.write(f"{sha(g.read())}  {p}\n")
note("wrote runs/SHA256SUMS")

# --- verdict scoring vs PREREG_R35.md §4 ---
fails, voids = [], []
def bar(cond, name):
    (fails if not cond else []).append(name) if False else None
    if not cond: fails.append(name)

det3 = all(len(set(s)) == 1 for s in [sh_r35, sh_orig, sh_j, sh_h, sh_36r, sh_36o])
for cls in ["k", "l", "m"]:
    pass
all3 = [sh_r35, sh_orig, sh_j, sh_h, sh_36r, sh_36o]
det_ok = all(len(set(s)) == 1 for s in all3)

if not det_ok: voids.append("3x SHA divergence")
if h_admit is None or h_admit < 102: voids.append(f"B3 honest {h_admit}/120 < 102 (void)")
if tot_adv != 0: fails.append(f"B1 adv {tot_adv}/760 > 0")
if h2 != 0: fails.append(f"B1 H2 {h2}/40 > 0")
if h1 is None or h1 < 57 or delay != 0: fails.append(f"B1 H1 {h1}/60 delay {delay}")
if not b1_regress: fails.append("B1 m35 stdout diverged from original")
if j_inst is None or j_inst > 15: fails.append(f"B2 J-35 installs {j_inst}/120 > 15")
for cls in ["k", "l", "m"]:
    if results[cls] != 0: fails.append(f"B4 {cls.upper()}-35 {results[cls]}/120 != 0")
if not b5_regress: fails.append("B5 mode36 stdout diverged from original")

note("=" * 60)
if voids:
    note("BATTERY VOID: " + "; ".join(voids)); sys.exit(2)
if fails:
    note("REPAIR FAILED: " + "; ".join(fails)); sys.exit(1)
note("REPAIR SUCCEEDS: all §4 bars green -> H-PAM-35 TESTED-survived (repaired)")

with open(os.path.join(D, "RUNLOG_R35.md"), "w") as f:
    f.write("# RUNLOG_R35\n\n" + "\n".join(log) + "\n")
print("wrote RUNLOG_R35.md")
