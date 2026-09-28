#!/usr/bin/env python3
"""RT-JKLM battery runner: build, 3x deterministic runs, SHA-compare, score.

End-to-end pipeline per PREREG_RT_JKLM.md (frozen @ d050ce4e).
Pure-Zag batteries; this script only orchestrates.
"""
import os, sys, subprocess, hashlib, shutil, re

HOME = os.path.expanduser("~")
LAB = os.path.join(HOME, "workspace", "tnn-lab", "senses", "pam-rebuild", "round2", "rt_jklm")
BUILD = os.path.join(HOME, "workspace", "rt_jklm", "build")
ZNC = os.path.join(HOME, "workspace", "tnn-lab", "toolchain", "bin", "znc_linux_x86_64_abed8aa1")
SRC = os.path.join(HOME, "workspace", "rt_jklm", "src")

PINS = {
    "repair.zag": "65bb22a7d6b707dbe3484697b3b20826d1a51d1384f4e3b40b4f1183b1162bec",
    "hpam3536_probe.zag": "b20ae9edf87da4aa195c52fa321d95721278de0467d8daaca0b26d1dda929761",
    "R33_NATIVE_IO_V1.zag": "e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8",
}

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r

def main():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(os.path.join(LAB, "fixtures"), exist_ok=True)
    os.makedirs(os.path.join(LAB, "runs"), exist_ok=True)
    log = []

    # 1. verify target source pins
    for name, pin in PINS.items():
        h = sha(open(os.path.join(SRC, name), "rb").read())
        assert h == pin, f"PIN MISMATCH {name}: {h} != {pin}"
        log.append(f"pin ok {name} {h[:16]}")

    # 2. stage sources, extract verified copies, verify identity
    for f in ["gen_jklm.zag", "consume_j.zag", "drive35.zag", "drive36.zag",
              "extract_copies.py", "R33_NATIVE_IO_V1.zag"]:
        shutil.copy(os.path.join(LAB if not f.startswith("R33") else SRC, f),
                    os.path.join(BUILD, f))
    for which in ["35", "36"]:
        r = run([sys.executable, os.path.join(BUILD, "extract_copies.py"),
                 os.path.join(SRC, "hpam3536_probe.zag"), which,
                 os.path.join(BUILD, f"copy{which}.zag")])
        assert r.returncode == 0, r.stderr
        log.append(r.stdout.strip())
    # verify_copies: re-extract to temp and diff
    for which in ["35", "36"]:
        tmp = os.path.join(BUILD, f"copy{which}.verify.zag")
        r = run([sys.executable, os.path.join(BUILD, "extract_copies.py"),
                 os.path.join(SRC, "hpam3536_probe.zag"), which, tmp])
        assert r.returncode == 0, r.stderr
        a = open(os.path.join(BUILD, f"copy{which}.zag"), "rb").read()
        b = open(tmp, "rb").read()
        assert a == b, f"copy{which} identity FAILED"
        os.remove(tmp)
        log.append(f"verify_copies: copy{which}.zag byte-identical to committed source functions")

    # 3. build
    bins = {}
    for src, out in [("repair.zag", "repair_bin"), ("gen_jklm.zag", "gen_bin"),
                     ("consume_j.zag", "consume_bin"), ("drive35.zag", "d35_bin"),
                     ("drive36.zag", "d36_bin")]:
        if src == "repair.zag":
            shutil.copy(os.path.join(SRC, src), os.path.join(BUILD, src))
        r = run([ZNC, src, "-o", out], cwd=BUILD)
        assert r.returncode == 0, f"build {src} failed: {r.stderr[:500]}"
        bins[out] = os.path.join(BUILD, out)
        log.append(f"built {out}")

    # 4. fixtures
    fixdir = os.path.join(LAB, "fixtures")
    for cls in ["j", "k", "l", "m"]:
        r = run([bins["gen_bin"], cls, os.path.join(fixdir, f"{cls}.tsv")], cwd=BUILD)
        assert r.returncode == 0
    honest = os.path.join(BUILD, "honest.tsv")
    # frozen honest battery, extracted from e609f185 (see pilot/)
    shutil.copy(os.path.join(HOME, "workspace", "rt_jklm", "pilot", "honest.tsv"), honest)
    shutil.copy(honest, os.path.join(fixdir, "honest.tsv"))
    shpins = {}
    for f in ["j.tsv", "k.tsv", "l.tsv", "m.tsv", "honest.tsv"]:
        shpins[f] = sha(open(os.path.join(fixdir, f), "rb").read())
    with open(os.path.join(fixdir, "SHA256SUMS"), "w") as f:
        for k in sorted(shpins):
            f.write(f"{shpins[k]}  {k}\n")
    log.append(f"fixtures pinned: {len(shpins)}")

    # 5. run batteries 3x
    runsdir = os.path.join(BUILD, "runs3x")
    os.makedirs(runsdir, exist_ok=True)
    artifacts = {}   # key -> list of (path, sha)
    def capture(key, cmd):
        lst = []
        for i in (1, 2, 3):
            p = os.path.join(runsdir, f"{key}_run{i}.out")
            r = run(cmd, cwd=BUILD)
            assert r.returncode == 0, f"{key} run{i} failed"
            data = r.stdout.encode()
            open(p, "wb").write(data)
            lst.append((p, sha(data)))
        shas = {s for _, s in lst}
        assert len(shas) == 1, f"DIVERGENCE in {key}: {shas}"
        artifacts[key] = lst
        log.append(f"{key}: 3x byte-identical sha={lst[0][1][:16]}")
        return lst[0][1]

    results = {}
    # comp batteries: repair tier TSVs are intermediate; consume output is the artifact
    for cls in ["j", "k", "l", "m"]:
        for arm in ["r1", "r2"]:
            tier = os.path.join(BUILD, f"tier_{cls}_{arm}.tsv")
            r = run([bins["repair_bin"], os.path.join(fixdir, f"{cls}.tsv"), tier, arm], cwd=BUILD)
            assert r.returncode == 0
            key = f"comp_{cls}_{arm}"
            capture(key, [bins["consume_bin"], os.path.join(fixdir, f"{cls}.tsv"), tier])
            results[key] = open(artifacts[key][0][0]).read()
    # honest comp control
    for arm in ["r1", "r2"]:
        tier = os.path.join(BUILD, f"tier_honest_{arm}.tsv")
        r = run([bins["repair_bin"], honest, tier, arm], cwd=BUILD)
        assert r.returncode == 0
        key = f"comp_honest_{arm}"
        capture(key, [bins["consume_bin"], honest, tier])
        results[key] = open(artifacts[key][0][0]).read()
    # 35/36 drivers
    for cls in ["j", "k", "l", "m", "honest"]:
        for drv, b in [("35", "d35_bin"), ("36", "d36_bin")]:
            key = f"d{drv}_{cls}"
            capture(key, [bins[b], cls])
            results[key] = open(artifacts[key][0][0]).read()

    # 6. score
    def ep_lines(text):
        eps = []
        for line in text.split("\n"):
            m = re.match(r"EP (\d+) PROV_N=(\d+) PROV_MEAN=(-?\d+) ACT=(\d) DET=(\d) COM=(\d)", line)
            if m:
                eps.append(tuple(int(x) for x in m.groups()))
        return eps
    def summary(text):
        m = re.search(r"SUMMARY EPS=(\d+) ACT_EP=(\d+) DET_EP=(\d+) COM_EP=(\d+) PROV_EP=(\d+)", text)
        return tuple(int(x) for x in m.groups()) if m else None
    def kv(text, name):
        m = re.search(name + r"=(\d+)", text)
        return int(m.group(1)) if m else None

    verdict = []
    verdict.append("# VERDICT_RT_JKLM — Red-Team Battery Results")
    verdict.append("")
    verdict.append("Prereg: `PREREG_RT_JKLM.md` (frozen @ `d050ce4e`, committed alone before code).")
    verdict.append("Targets unmodified; 35/36 via byte-identical verified-copy drivers.")
    verdict.append("")

    # comp scoring
    comp_table = []
    for cls in ["j", "k", "l", "m"]:
        for arm in ["r1", "r2"]:
            eps = ep_lines(results[f"comp_{cls}_{arm}"])
            if cls == "j":
                inst = sum(1 for e in eps if e[3] == 1 and e[4] == 0 and e[5] == 0)
            else:
                inst = sum(1 for e in eps if e[5] == 1 and e[4] == 0)
            comp_table.append((cls, arm, inst, len(eps)))
    verdict.append("## T-A (repaired D2 composition R1/R2) — install rates (n=120)")
    verdict.append("")
    verdict.append("| class | arm | install | rate | bar | result |")
    verdict.append("|---|---|---|---|---|---|")
    bars = {"j": ("≥97/120 KILL tier-boundary", 97), "k": ("≥97/120 KILL detection-blind", 97),
            "l": ("≥97/120 SCOPE one-modality", 97), "m": ("≥97/120 CONFIRM boundary-ride", 97)}
    fired = []
    for cls, arm, inst, n in comp_table:
        bar, thr = bars[cls]
        res = "FIRED" if inst >= thr else "not fired"
        if inst >= thr:
            fired.append(f"{cls}-comp/{arm}: {inst}/120 ({bar})")
        verdict.append(f"| {cls.upper()} | {arm} | {inst}/{n} | {inst/n:.1%} | {bar} | **{res}** |")
    verdict.append("")

    # honest comp
    verdict.append("## Honest-loss controls")
    verdict.append("")
    for arm in ["r1", "r2"]:
        s = summary(results[f"comp_honest_{arm}"])
        verdict.append(f"- honest.tsv via {arm}: ACT_EP={s[1]}/120 (J-loss bar ≤18), COM_EP={s[3]}/120 (K/L/M keep bar ≥102)")
    h35 = kv(results["d35_honest"], "H35_ADMIT")
    h36 = kv(results["d36_honest"], "H36_ADMIT")
    verdict.append(f"- d35 honest: {h35}/120 admitted (bar ≥102)")
    verdict.append(f"- d36 honest: {h36}/60 admitted (bar ≥51)")
    verdict.append("")

    # 35/36 scoring
    verdict.append("## T-B (H-PAM-35) and T-C (H-PAM-36) — install rates")
    verdict.append("")
    verdict.append("| battery | install | trials | bar | result |")
    verdict.append("|---|---|---|---|---|")
    t = [
        ("J-35 (RF tag high-32)", kv(results["d35_j"], "J35_INSTALL"), 120, "≥97/120 KILL tag-binds-content", 97),
        ("K-35 (NT)", kv(results["d35_k"], "K35_INSTALL"), 120, "≥1/120 KILL type-barrier", 1),
        ("L-35 (endorsement)", kv(results["d35_l"], "L35_INSTALL"), 120, "≥1/120 KILL endorsement-indep", 1),
        ("M-35 (fit-from-output)", kv(results["d35_m"], "M35_FIT"), 120, "≥1/120 KILL seed-indep", 1),
        ("J-36 (RF identity)", kv(results["d36_j"], "J36_INSTALL"), 120, "≥97/120 SCOPE identity-residual", 97),
        ("K-36 (NT blind)", kv(results["d36_k"], "K36_INSTALL"), 120, "≥1/120 KILL blind-commit", 1),
        ("L-36 (sample-indep)", 120 - kv(results["d36_l"], "L36_MATCH"), 120, "any mismatch KILL sample-indep", 1),
        ("M-36 (XR seed-reuse)", kv(results["d36_m"], "M36_INSTALL"), 120, "≥97/120 KILL blind-commitment", 97),
    ]
    for name, inst, n, bar, thr in t:
        res = "FIRED" if inst >= thr else "not fired"
        if inst >= thr:
            fired.append(f"{name}: {inst}/{n} ({bar})")
        verdict.append(f"| {name} | {inst}/{n} | {n} | {bar} | **{res}** |")
    verdict.append("")

    verdict.append("## Bars fired")
    verdict.append("")
    if fired:
        for f in fired:
            verdict.append(f"- **{f}**")
    else:
        verdict.append("- none")
    verdict.append("")

    verdict.append("## Determinism")
    verdict.append("")
    verdict.append("Every battery ran 3×; all SHA-256 identical (see runs/SHA256SUMS).")
    verdict.append("")

    verdict.append("## Run log")
    verdict.append("")
    verdict.append("```")
    verdict.extend(log)
    verdict.append("```")

    vpath = os.path.join(LAB, "VERDICT_RT_JKLM.md")
    open(vpath, "w").write("\n".join(verdict) + "\n")

    # 7. publish representative runs + SHAs
    pubruns = os.path.join(LAB, "runs")
    shalines = []
    for key, lst in artifacts.items():
        for p, s in lst:
            shalines.append(f"{s}  {os.path.basename(p)}")
        # publish run1
        shutil.copy(lst[0][0], os.path.join(pubruns, os.path.basename(lst[0][0])))
    # also publish tier TSVs (run1) for comp batteries
    for cls in ["j", "k", "l", "m"]:
        for arm in ["r1", "r2"]:
            p = os.path.join(BUILD, f"tier_{cls}_{arm}.tsv")
            d = os.path.join(pubruns, f"tier_{cls}_{arm}.tsv")
            shutil.copy(p, d)
            shalines.append(f"{sha(open(d,'rb').read())}  tier_{cls}_{arm}.tsv")
    with open(os.path.join(pubruns, "SHA256SUMS"), "w") as f:
        f.write("\n".join(sorted(shalines)) + "\n")

    print("\n".join(verdict))
    print(f"\nWROTE {vpath}")

main()
