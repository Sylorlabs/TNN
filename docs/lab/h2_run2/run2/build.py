#!/usr/bin/env python3
"""H2 run-2 T-MC build/run orchestration.

Python does NO decisions: compile, run twice, byte-compare, passive extract.
All mechanism/teacher/learner/verification logic is pure Zag.
"""
import os
import re
import subprocess
import sys
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
BUILD = os.path.join(HERE, "build")
EV = os.path.join(HERE, "evidence")
os.makedirs(BUILD, exist_ok=True)
os.makedirs(EV, exist_ok=True)

FAIL = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" : " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)

def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

# ---------- static checks (no rng in decision paths, etc.) ----------
RNG_RE = re.compile(r"\brng\b|\brand\b|\bseed\b|\btime\b|_zag_time|getrandom|/dev/urandom", re.I)
def static_scan(path):
    src = open(path).read()
    bad = []
    for i, line in enumerate(src.splitlines(), 1):
        code = re.sub(r"//.*", "", line)
        if RNG_RE.search(code):
            bad.append((i, code.strip()[:80]))
    return bad

def select_region_ok(path):
    src = open(path).read()
    m = re.search(r"MC-SELECT-REGION-BEGIN(.*?)MC-SELECT-REGION-END", src, re.S)
    if not m:
        return False, "markers missing"
    body = m.group(1)
    # strip comments
    body = re.sub(r"//.*", "", body)
    if re.search(r"\bep\b", body):
        return False, "episode operand in select region"
    if re.search(r"signal|teacher", body, re.I):
        return False, "signal/teacher token in select region"
    # mc_select must not take ep/signal params: check its signature line
    sm = re.search(r"fn mc_select\((.*?)\)", body)
    if sm and re.search(r"\bep\b|signal", sm.group(1)):
        return False, "bad mc_select params"
    return True, ""

def close_no_stable(path):
    src = open(path).read()
    m = re.search(r"fn mc_close\(.*?^}", src, re.M | re.S)
    if not m:
        return False, "mc_close not found"
    body = m.group(0)
    if "stable" in body.lower() or "tmc_set_stable" in body:
        return False, "mc_close touches stability"
    return True, ""

def op_allowlist(path):
    """Every tmc_audit call's op arg must be a known code (const or EV_*)."""
    src = open(path).read()
    known = {"OP_PINSTALL","OP_PROMOTE","OP_UNINSTALL_PROV","OP_AV_REISSUE",
             "OP_AV_LATCH","OP_AV_SUSP_TRIP","OP_MC_PROBE","OP_MC_OBSERVE_BIT",
             "OP_MC_TAG_CHECK","OP_MC_MARK_R","OP_MC_MARK_S","OP_MC_CLOSE",
             "OP_MC_READOUT","OP_MC_SEAL","OP_MC_DOUBLE_DERIVE","OP_MC_DISCONNECT",
             "OP_MC_UNSEAL","OP_MC_REATTRIBUTE","OP_SR_ATTRIBUTE","OP_SR_RHYTHM_FREEZE",
             "EV_AV_FAULT_SUSPECT","EV_AV_FAULT_CONFIRM","EV_AV_LATCH_HOLD",
             "EV_AV_LATCH_CLEAR","EV_FLAP_HOLD","EV_MC_HOSTILE","EV_AV_SENSOR_DIVERGE",
             "EV_MC_REISSUE_MATCH","EV_MC_DECLARE_SCHEMA"}
    bad = []
    for mt in re.finditer(r"tmc_audit\(st,audit,&?acount,([A-Za-z_0-9]+)", src):
        if mt.group(1) not in known:
            bad.append(mt.group(1))
    return (len(bad) == 0), ",".join(sorted(set(bad))[:5])

ZAG_SOURCES = ["t_mc.zag", "d1_record.zag", "d1_driver.zag", "d4_driver.zag"]
print("== static scans ==")
for z in ZAG_SOURCES:
    p = os.path.join(HERE, z)
    if not os.path.exists(p):
        print("SKIP (not yet written) " + z)
        continue
    bad = static_scan(p)
    check("no-rng " + z, not bad, str(bad[:3]) if bad else "")
check("select-region", *select_region_ok(os.path.join(HERE, "t_mc.zag")))
check("close-no-stable", *close_no_stable(os.path.join(HERE, "t_mc.zag")))
check("op-allowlist", *op_allowlist(os.path.join(HERE, "t_mc.zag")))

def compile_zag(src, out):
    r = sh([ZNC, src, "-o", out], cwd=HERE)
    ok = r.returncode == 0 and os.path.exists(out)
    if not ok:
        print(r.stdout[-2000:] if r.stdout else "")
        print(r.stderr[-2000:] if r.stderr else "")
    return ok

def run_twice(binary, ev_base):
    outs = []
    for i in (1, 2):
        r = sh([binary], cwd=HERE)
        if r.returncode not in (0, 1):
            print("run %d rc=%d stderr=%s" % (i, r.returncode, r.stderr[-500:]))
            return None
        outs.append(r.stdout)
    p1 = os.path.join(EV, ev_base + "_run1.txt")
    p2 = os.path.join(EV, ev_base + "_run2.txt")
    open(p1, "w").write(outs[0])
    open(p2, "w").write(outs[1])
    h1 = hashlib.sha256(outs[0].encode()).hexdigest()
    h2 = hashlib.sha256(outs[1].encode()).hexdigest()
    return (outs[0], h1, h2)

# ---------- D1: record tape ----------
print("== D1 record ==")
ok = compile_zag(os.path.join(HERE, "d1_record.zag"), os.path.join(BUILD, "d1_record"))
check("compile d1_record", ok)
tape_lines = []
tape_n = 0
if ok:
    r = sh([os.path.join(BUILD, "d1_record")], cwd=HERE)
    for line in r.stdout.splitlines():
        if line.startswith("TAPE,"):
            tape_lines.append(line)
        if line.startswith("TAPE_N,"):
            tape_n = int(line.split(",")[1])
    check("tape extracted", tape_n == 37 and len(tape_lines) == 37,
          "n=%d lines=%d" % (tape_n, len(tape_lines)))
    open(os.path.join(EV, "d1_tape.txt"), "w").write("\n".join(tape_lines) + "\n")
    # generate d1_tape.zag (tape as Zag source; no parsing in Zag)
    with open(os.path.join(HERE, "d1_tape.zag"), "w") as f:
        f.write("// generated by build.py from the recorded D1 tape; do not hand-edit\n")
        f.write("// 7xi32 LE per entry: kind,c,a,expect,actual,s,r1\n")
        f.write("fn d1_tape_fill(tape:[]u8,tn:*i32)void {\n")
        for line in tape_lines:
            parts = line.split(",")[1:]
            f.write("    tmc_tape_put(tape,tn,%s);\n" % ",".join(parts))
        f.write("    return;\n}\n")
    check("d1_tape.zag generated", True, "%d entries" % len(tape_lines))

# ---------- D1: decider ----------
print("== D1 decider ==")
ok = compile_zag(os.path.join(HERE, "d1_driver.zag"), os.path.join(BUILD, "tmc_d1"))
check("compile tmc_d1", ok)
d1 = None
if ok:
    d1 = run_twice(os.path.join(BUILD, "tmc_d1"), "d1")
    if d1 is None:
        check("d1 two runs", False)
    else:
        out, h1, h2 = d1
        check("d1 byte-identical reruns", h1 == h2, h1[:16])
        m = re.search(r"D1_VERDICT,(PASS|FAIL.*)", out)
        check("d1 verdict PASS", bool(m and m.group(1) == "PASS"),
              m.group(1) if m else "no verdict")
        for line in out.splitlines():
            if line.startswith("D1_K,"):
                print("  " + line)

# ---------- D4: T-DEF comparator (fixture-specific FL2 default) ----------
print("== D4 T-DEF comparator ==")
tdef_p2 = -1
r = sh([sys.executable, os.path.join(HERE, "build_tdef.py")], cwd=HERE)
check("build tdef", r.returncode == 0, (r.stdout + r.stderr)[-800:] if r.returncode else "")
if r.returncode == 0:
    tdef_bin = os.path.join(BUILD, "tdef_storm", "tdef_storm")
    tdef_p2 = 0
    tdef_ok = True
    for rnd in (1, 2, 3, 4, 5, 6):
        rr = sh([tdef_bin, str(rnd)], cwd=os.path.dirname(tdef_bin))
        if rr.returncode != 0:
            check("tdef storm round %d rc" % rnd, False, rr.stderr[-500:])
            tdef_ok = False
            break
        open(os.path.join(EV, "tdef_storm_r%d.txt" % rnd), "w").write(rr.stdout)
        m = re.search(r"H2_VERDICT,(KILLED|SURVIVE)", rr.stdout)
        v = m.group(1) if m else "?"
        print("  T-DEF storm round %d: %s" % (rnd, v))
        if rnd >= 4 and v == "KILLED":
            tdef_p2 += 1
    if tdef_ok:
        check("tdef storm 6 rounds", True, "phase-2 KILLs=%d" % tdef_p2)

# ---------- D4: decider ----------
print("== D4 decider ==")
ok = compile_zag(os.path.join(HERE, "d4_driver.zag"), os.path.join(BUILD, "tmc_d4"))
check("compile tmc_d4", ok)
if ok and tdef_p2 >= 0:
    d4bin = os.path.join(BUILD, "tmc_d4")
    outs = []
    for i in (1, 2):
        rr = sh([d4bin, str(tdef_p2)], cwd=HERE)
        if rr.returncode not in (0, 1):
            check("d4 run %d rc" % i, False, "rc=%d %s" % (rr.returncode, rr.stderr[-500:]))
            outs = []
            break
        outs.append(rr.stdout)
    if len(outs) == 2:
        p1 = os.path.join(EV, "d4_run1.txt")
        p2 = os.path.join(EV, "d4_run2.txt")
        open(p1, "w").write(outs[0])
        open(p2, "w").write(outs[1])
        h1 = hashlib.sha256(outs[0].encode()).hexdigest()
        h2 = hashlib.sha256(outs[1].encode()).hexdigest()
        check("d4 byte-identical reruns", h1 == h2, h1[:16])
        m = re.search(r"D4_VERDICT,(PASS|FAIL.*)", outs[0])
        check("d4 verdict PASS", bool(m and m.group(1) == "PASS"),
              m.group(1) if m else "no verdict")
        for line in outs[0].splitlines():
            if line.startswith("D4_STORM,") or line.startswith("D4_HONEST,") or \
               line.startswith("D4_VERDICT,") or line.startswith("D4_TDEF_P2,"):
                print("  " + line)
        # honest-arm audit delta across reruns (<=2; expect 0)
        def honest_audit_n(txt):
            for line in txt.splitlines():
                if line.startswith("D4_HONEST,"):
                    mm = re.search(r"audit_n,(\d+)", line)
                    if mm:
                        return int(mm.group(1))
            return -1
        n1, n2 = honest_audit_n(outs[0]), honest_audit_n(outs[1])
        check("honest audit delta<=2", abs(n1 - n2) <= 2 and n1 > 0,
              "n1=%d n2=%d" % (n1, n2))

print("== summary ==")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)
print("ALL CHECKS PASSED")
