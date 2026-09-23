#!/usr/bin/env python3
"""Full verification battery for the arm-3 variation-C engagement teacher.
Writes evidence logs under ../evidence/. Exits nonzero on any failure."""
import sys, os, struct, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hist import *

VARC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(VARC, "teacher_bin")
WIRED = os.path.expanduser("~/workspace/tnn-lab/units/teachers/arm1/wired")
EV = os.path.join(VARC, "evidence")
SESS = os.path.join(EV, "sessions")
os.makedirs(SESS, exist_ok=True)

LOG = []
def log(s):
    LOG.append(s)
    print(s)

fails = []
def check(name, cond, detail=""):
    log(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)

def run_teacher(mode, slice_idx, session_id, hist_path, env_extra=None):
    hdir, hname = os.path.split(os.path.abspath(hist_path))
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    import subprocess
    p = subprocess.run([BIN, mode, str(slice_idx), str(session_id), WIRED, hdir, hname],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")

# ---------- 1. build scripted sessions ----------
def session_file(name, session_id, decisions):
    import subprocess
    out = os.path.join(SESS, name + ".hist")
    subprocess.run([sys.executable, os.path.join(VARC, "verify", "session.py"),
                    BIN, WIRED, "0", str(session_id), out, decisions, SESS],
                   check=True, capture_output=True, text=True)
    return out

log("== building scripted sessions ==")
hA = session_file("A", 2001, "ADOPT,ADOPT,ADOPT,ADOPT,ADOPT,REJECT:1,ADOPT,ADOPT,ADOPT,ADOPT,ADOPT,ADOPT")
hB = session_file("B", 2002, "ADOPT,DEFER,DEFER,REJECT:1,REJECT:1,ADOPT")
hAdopt = session_file("adopt14", 2003, ",".join(["ADOPT"] * 14))
hReject = session_file("reject12", 2004, ",".join(["REJECT:1"] * 12))

# ---------- 2. N=5 byte-identical ----------
log("== N=5 byte-identical ==")
outs = set()
for i in range(5):
    rc, out, err = run_teacher("propose", 0, 2001, hA)
    assert rc == 0, f"propose failed: {err}"
    outs.add(hashlib.sha256(out).hexdigest())
check("N=5 byte-identical (session A)", len(outs) == 1, f"{len(outs)} distinct")

# ---------- 3. adversarial heap perturbations ----------
# Two perturbation axes: (a) MALLOC_PERTURB_ allocator fill patterns;
# (b) environment block size (shifts initial stack/heap layout for real in
# any binary). The teacher reads no uninitialized memory (every arena is
# zero-filled by nio_alloc and fully written before read), so all runs
# must be byte-identical.
log("== adversarial heap perturbations ==")
outs = set()
perturbs = [({"MALLOC_PERTURB_": v}, f"perturb={v}") for v in ["0", "1", "165", "90", "213"]]
perturbs += [({"VARC_JUNK_" + str(i): "x" * (i * 1024)}, f"envjunk={i}KB") for i in (4, 16, 64)]
ok = True
for env_extra, label in perturbs:
    try:
        rc, out, err = run_teacher("propose", 0, 2001, hA, env_extra)
    except OSError as ex:
        log(f"perturbation spawn failed under {label}: {ex}")
        ok = False
        break
    if rc != 0:
        log(f"propose failed under {label}: {err.strip()[-120:]}")
        ok = False
        break
    outs.add(hashlib.sha256(out).hexdigest())
check(f"{len(perturbs)}/{len(perturbs)} heap-perturbation byte-identical", ok and len(outs) == 1,
      f"{len(outs)} distinct")

# ---------- 4. selfcheck on all sessions ----------
log("== selfcheck (recorded == recomputed) ==")
for name, hp, sid in [("A", hA, 2001), ("B", hB, 2002), ("adopt14", hAdopt, 2003), ("reject12", hReject, 2004)]:
    rc, out, err = run_teacher("selfcheck", 0, sid, hp)
    check(f"selfcheck {name}", rc == 0 and out == b"", f"rc={rc} err={err.strip()[-200:]}")

# ---------- 5. E recompute: teacher trace vs independent Python reference ----------
log("== E recompute check (teacher trace vs Python reference) ==")
def py_E_trace(hist):
    n = nevents(hist)
    E, consec = 0, 0
    out = []
    for ei in range(n):
        base = HDR + ei * REC
        tag = hist[base]
        if tag == TAG_PROPOSE:
            E = max(0, min(1000, E - 20))
        else:
            v = hist[base + 9]
            if v == ADOPT:
                E += 120; consec = 0
            elif v == REVISE:
                E += 60; consec = 0
            elif v == DEFER:
                E += 10; consec = 0
            else:
                E -= 150; consec += 1
                if consec == 2:
                    E -= 200
            E = max(0, min(1000, E))
        out.append(E)
    return out

for name, hp, sid in [("A", hA, 2001), ("B", hB, 2002), ("adopt14", hAdopt, 2003), ("reject12", hReject, 2004)]:
    rc, out, err = run_teacher("trace", 0, sid, hp)
    assert rc == 0, err
    teacher_E = []
    for line in out.decode().strip().split("\n"):
        parts = dict(tok.split("=") for tok in line.split())
        teacher_E.append(int(parts["E"]))
    hist = open(hp, "rb").read()
    ref_E = py_E_trace(hist)
    check(f"E recompute {name} ({len(ref_E)} events)", teacher_E == ref_E,
          f"teacher={teacher_E[:8]}... ref={ref_E[:8]}...")

# ---------- 6. history sensitivity: adopt vs reject on same stimulus ----------
log("== history sensitivity ==")
def diag_series(hist_path, sid):
    rc, out, err = run_teacher("trace", 0, sid, hist_path)
    return out.decode()
ta = open(hAdopt + ".trace").read()
tr = open(hReject + ".trace").read()
# adopt history must reach hot and emit relational; reject history stays cold
rc, out, err = run_teacher("propose", 0, 2003, hAdopt)
pa = parse_proposal(out)
rc, out, err = run_teacher("propose", 0, 2004, hReject)
pr = parse_proposal(out)
ha = open(hAdopt, "rb").read()
hr = open(hReject, "rb").read()
Ea, Er = py_E_trace(ha), py_E_trace(hr)
check("all-ADOPT drives E hot", Ea[-1] >= 700, f"final E={Ea[-1]}")
check("all-REJECT keeps E cold", max(Er) < 300, f"max E={max(Er)}")
# relational kinds appear in adopt session proposals
def kinds_in(hist):
    ks = set()
    n = nevents(hist)
    for ei in range(n):
        base = HDR + ei * REC
        if hist[base] == TAG_PROPOSE:
            ks.add(hist[base + 9])
    return ks
check("adopt session shows relational kinds", bool(kinds_in(ha) & {2, 3, 4}), str(kinds_in(ha)))
check("reject session stays WORD_SPAN-only", kinds_in(hr) <= {1, 5}, str(kinds_in(hr)))
check("adopt conf higher than reject conf", pa["conf"] > pr["conf"],
      f"adopt_next={pa['conf']} reject_next={pr['conf']}")
log(f"adopt E trace: {','.join(map(str, Ea))}")
log(f"reject E trace: {','.join(map(str, Er))}")

# ---------- 7. §P iron-rule battery ----------
log("== §P iron-rule battery ==")
def write_hist(path, data):
    with open(path, "wb") as f:
        f.write(data)

def corrupt_header(hist, off, fmt, val):
    h = bytearray(hist)
    struct.pack_into(fmt, h, off, val)
    return bytes(h)

# need one valid proposal to build hostile variants: propose on empty history
empty = os.path.join(EV, "_empty.hist")
write_hist(empty, new_history(9001))
rc, out, err = run_teacher("propose", 0, 9001, empty)
assert rc == 0, err
p0 = parse_proposal(out)
base_hist = append_propose(new_history(9001), p0)

cases = []
# 1 bad magic
cases.append(("bad magic", corrupt_header(base_hist, 0, "<I", 0xDEADBEEF), 1))
# 2 bad version
cases.append(("bad version", corrupt_header(base_hist, 4, "<H", 2), 2))
# 3 session mismatch
cases.append(("session mismatch", base_hist, 3, 9999))
# 4 truncated header (10 bytes)
cases.append(("truncated header", base_hist[:10], 10))
# 5 nevents lies (claims 5, file has 1)
cases.append(("nevents/size mismatch", corrupt_header(base_hist, 24, "<I", 5), 10))
# 6 unknown tag
h = bytearray(base_hist); h[HDR] = 9; cases.append(("unknown tag", bytes(h), 6))
# 7 seq gap (first propose claims seq=1)
h = bytearray(base_hist); struct.pack_into("<Q", h, HDR + 1, 1); cases.append(("seq gap", bytes(h), 4))
# 8 seq duplicate (two seq=0)
h2 = append_propose(base_hist, dict(p0, seq=0)); cases.append(("seq duplicate", h2, 4))
# 9 kind=0
h = bytearray(base_hist); h[HDR + 9] = 0; cases.append(("kind=0", bytes(h), 6))
# 10 kind=6
h = bytearray(base_hist); h[HDR + 9] = 6; cases.append(("kind=6", bytes(h), 6))
# 11 ss>=se
h = bytearray(base_hist); struct.pack_into("<QQ", h, HDR + 10, 500, 500); cases.append(("ss>=se", bytes(h), 5))
# 12 se>stim_len
h = bytearray(base_hist); struct.pack_into("<QQ", h, HDR + 10, 500, 70000); cases.append(("se>stim", bytes(h), 8))
# 13 aux_count=3
h = bytearray(base_hist); h[HDR + 27] = 3; cases.append(("aux_count=3", bytes(h), 9))
# 14 ground_count=5
h = bytearray(base_hist); h[HDR + 28] = 5; cases.append(("ground_count=5", bytes(h), 9))
# 15 aux span invalid (s>=e)
h = bytearray(append_propose(new_history(9001),
      dict(p0, aux=[(100, 200)]))); struct.pack_into("<QQ", h, HDR + 29, 300, 300)
cases.append(("aux span invalid", bytes(h), 8))
# 16 decide unknown seq
h = append_decide(new_history(9001), 7, ADOPT); cases.append(("decide unknown seq", h, 4))
# 17 decide twice (ADOPT then REJECT same seq)
h = append_decide(append_decide(base_hist, 0, ADOPT), 0, REJECT, 1)
cases.append(("decide after final", h, 4))
# 18 verdict=7
h = append_decide(base_hist, 0, 7); cases.append(("verdict=7", bytes(h), 6))
# 19 REJECT with reason=0
h = append_decide(base_hist, 0, REJECT, 0); cases.append(("reject reason=0", bytes(h), 6))

for item in cases:
    name, data = item[0], item[1]
    want = item[2]
    sid = item[3] if len(item) > 3 else 9001
    path = os.path.join(EV, "_hostile.hist")
    write_hist(path, data)
    rc, out, err = run_teacher("propose", 0, sid, path)
    check(f"hostile: {name} -> exit {want}",
          rc == want and out == b"" and len(err.strip()) > 0,
          f"rc={rc} stdout={len(out)}B stderr={err.strip()[:80]!r}")

# 20 selfcheck divergence: forged proposal (valid structure, wrong content)
h = bytearray(base_hist)
struct.pack_into("<QQ", h, HDR + 10, 1000, 1005)  # teacher would never pick this first
write_hist(os.path.join(EV, "_forged.hist"), bytes(h))
rc, out, err = run_teacher("selfcheck", 0, 9001, os.path.join(EV, "_forged.hist"))
check("selfcheck catches forged proposal -> 21", rc == 21 and out == b"", f"rc={rc}")

# ---------- 8. §C tripwire (cumulative conservative monitor) ----------
log("== §C tripwire ==")
def tripwire(proposals, decisions, stim_len=65536):
    """proposals: list of (ss,se,conf); decisions: dict seq->verdict.
    Returns 0 (no fire), 1 (window), 2 (vocab dump)."""
    for (ss, se, conf) in proposals:
        if conf == 255 and (se - ss) * 100 > stim_len * 5:
            return 2
    covered = bytearray(stim_len)
    for (ss, se, _) in proposals:
        s = max(0, ss); e = min(stim_len, se)
        covered[s:e] = b"\x01" * (e - s)
    cov = sum(covered) / stim_len
    d = len(decisions)
    a = sum(1 for v in decisions.values() if v == ADOPT)
    w = len(proposals)
    m = sum(1 for (_, _, c) in proposals if c == 255)
    if stim_len > 0 and cov >= 0.95 and d > 0 and a / d >= 0.95 and w > 0 and m / w >= 0.90:
        return 1
    return 0

def session_stream(hist):
    props, decs = [], {}
    n = nevents(hist)
    for ei in range(n):
        base = HDR + ei * REC
        if hist[base] == TAG_PROPOSE:
            ss, se = struct.unpack_from("<QQ", hist, base + 10)
            props.append((ss, se, hist[base + 26]))
        else:
            seq, = struct.unpack_from("<Q", hist, base + 1)
            decs[seq] = hist[base + 9]
    return props, decs

props, decs = session_stream(ha)
check("clean teaching (all-ADOPT) does not fire §C", tripwire(props, decs) == 0,
      f"fire={tripwire(props, decs)} coverage events={len(props)}")

# smuggle probe: 200 proposals tiling the stimulus at conf 255, all ADOPT
sprops = [(i * 327, (i + 1) * 327, 255) for i in range(200)]
sprops[-1] = (199 * 327, 65536, 255)
sdecs = {i: ADOPT for i in range(200)}
fire_at = None
for k in range(1, 201):
    if tripwire(sprops[:k], {i: ADOPT for i in range(k)}) == 1:
        fire_at = k
        break
check("smuggle tiling fires §C code 1", fire_at is not None, f"fired at #{fire_at}")

# vocab dump probe: single conf-255 proposal covering >5%
check("vocab dump fires §C code 2 immediately",
      tripwire([(0, 4000, 255)], {0: ADOPT}) == 2)

# near-miss: high coverage + high accept but conf never 255 -> no fire
nprops = [(i * 327, (i + 1) * 327, 200) for i in range(200)]
check("no-255 high-coverage stream does not fire",
      tripwire(nprops, {i: ADOPT for i in range(200)}) == 0)

log("== done ==")
with open(os.path.join(EV, "battery.log"), "w") as f:
    f.write("\n".join(LOG) + "\n")
if fails:
    log(f"FAILURES: {fails}")
    sys.exit(1)
log("ALL CHECKS PASSED")
