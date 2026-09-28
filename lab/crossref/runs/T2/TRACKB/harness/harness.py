#!/usr/bin/env python3
"""TRACKB-DISCRIM shared harness (Python glue only; all decisions in Zag).

Drives varA/varB/varC through identical logical regimes and collects
preregistered measures. Deterministic: no RNG anywhere.
"""
import struct, subprocess, os, sys, re, json, hashlib, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/tmp/t2brief")
import b_gen_stimulus as _gen
import b_props as _bp
sys.path.insert(0, "/tmp/t2brief")
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("chist", "/tmp/t2brief/varC_hist.py")
_ch = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_ch)

B = os.path.expanduser("~/workspace/trackb/build")
BIN_A = os.path.join(B, "varA", "teacherA")
BIN_B = os.path.join(B, "repo/docs/lab/units/teachers/arm3/varB", "teacherB")
BIN_C = os.path.join(B, "repo/docs/lab/units/teachers/arm3/varC", "teacherC")

# ---------------- frozen shared curriculum ----------------
LINES = _gen.LINES                      # 60 deterministic prose lines
PROSE = ("\n".join(LINES) + "\n").encode()      # varB stimulus (raw bytes)
SINGLE = (" ".join(LINES)).encode()             # varA S bytes (one line)
WORD_RE = re.compile(rb"[A-Za-z0-9_]{3,}")
GT_AB = [(m.start(), m.end()) for m in WORD_RE.finditer(SINGLE)]

def build_slice():
    rep = PROSE * ((65536 // len(PROSE)) + 1)
    return rep[:65536]

SLICE = build_slice()
assert len(SLICE) == 65536
VOCAB_WORDS = sorted(set(WORD_RE.findall(PROSE)))
assert len(VOCAB_WORDS) <= 128, len(VOCAB_WORDS)
GT_C = []
for w in VOCAB_WORDS:
    for m in re.finditer(rb"(?<![A-Za-z0-9_])" + re.escape(w) + rb"(?![A-Za-z0-9_])", SLICE):
        GT_C.append((m.start(), m.end()))

# ---- curriculum registry: std (frozen) + shift (D2, fixed transform) ----
def _load_shift():
    import json as _j
    d = _j.load(open(os.path.join(HERE, "work/shift_curr.json")))
    lines = d["lines"]
    prose = ("\n".join(lines) + "\n").encode()
    single = (" ".join(lines)).encode()
    rep = prose * ((65536 // len(prose)) + 1)
    slc = rep[:65536]
    vw = [w.encode() for w in d["vocab"]]
    return dict(prose=prose, single=single, slice=slc,
                gt_ab=[tuple(x) for x in d["gt_ab"]],
                gt_c=[tuple(x) for x in d["gt_c"]], vocab=vw)

def _noise(data: bytes, rate_pct: int) -> bytes:
    # fixed-pattern in-place corruption: byte i corrupted iff hash condition;
    # newlines preserved (keeps varB line structure). Deterministic, no RNG.
    b = bytearray(data)
    for i in range(len(b)):
        if b[i] == 10:
            continue
        if ((i * 2654435761 + 0x9E3779B9) & 0xFFFFFFFF) % 100 < rate_pct:
            b[i] = 88  # 'X'
    return bytes(b)

def _noise_curr(rate):
    return dict(prose=_noise(PROSE, rate), single=_noise(SINGLE, rate),
                slice=_noise(SLICE, rate),
                gt_ab=list(GT_AB), gt_c=list(GT_C),
                vocab=list(VOCAB_WORDS))

def _edge_curr(name):
    # edge stimuli for D3 graceful-vs-cliff probes (fixed bytes, no RNG)
    if name == "edge_oneword":
        prose = b"hello\n"
        single = b"hello"
        slc = (b"hello " * 10923)[:65536]
    elif name == "edge_nowords":
        prose = b"   \n   \n"
        single = b"   "
        slc = b" " * 65536
    elif name == "edge_1byte":
        prose = b"a\n"
        single = b"a"
        slc = b"a" * 65536
    else:
        raise ValueError(name)
    assert len(slc) == 65536
    vw = sorted(set(WORD_RE.findall(prose)))
    gt_ab = sorted({(m.start(), m.end()) for m in WORD_RE.finditer(single)})
    gt_c = []
    for w in vw:
        for m in __import__("re").finditer(
                rb"(?<![A-Za-z0-9_])" + __import__("re").escape(w) + rb"(?![A-Za-z0-9_])", slc):
            gt_c.append((m.start(), m.end()))
    return dict(prose=prose, single=single, slice=slc,
                gt_ab=gt_ab, gt_c=sorted(set(gt_c)), vocab=list(vw))

CURR = {
    "std": dict(prose=PROSE, single=SINGLE, slice=SLICE,
                gt_ab=list(GT_AB), gt_c=list(GT_C), vocab=list(VOCAB_WORDS)),
    "shift": _load_shift(),
    "noise10": _noise_curr(10),
    "noise25": _noise_curr(25),
    "edge_oneword": _edge_curr("edge_oneword"),
    "edge_nowords": _edge_curr("edge_nowords"),
    "edge_1byte": _edge_curr("edge_1byte"),
}

def write_vocab(path, vocab_words):
    out = bytearray()
    out += struct.pack("<I", len(vocab_words))
    for w in vocab_words:
        e = bytearray()
        e += bytes([0])                       # rule 0 = WORD
        e += struct.pack("<i", 100)            # judgment > 0
        e += struct.pack("<H", len(w))
        e += w
        e += b"\x00\x00\x00"
        e += bytes([ord('P')])                 # domain prose
        e += b"\x00\x00\x00\x00"               # pad to 15+plen stride
        assert len(e) == 15 + len(w)
        out += e
    open(path, "wb").write(bytes(out))

def write_fixtures(workdir, curr="std"):
    C = CURR[curr]
    fx = os.path.join(workdir, "fx")
    os.makedirs(fx, exist_ok=True)
    # varA GT file
    with open(os.path.join(fx, "curr_gt.txt"), "wb") as f:
        f.write(b"GT1 %d\n" % len(C["single"]))
        f.write(b"S " + C["single"] + b"\n")
        for (s, e) in C["gt_ab"]:
            f.write(b"U %d %d 100\n" % (s, e))
    # varB stimulus
    open(os.path.join(fx, "curr_raw.bin"), "wb").write(C["prose"])
    # varC wired dir
    wd = os.path.join(fx, "wired"); os.makedirs(wd, exist_ok=True)
    open(os.path.join(wd, "slice_S0.bin"), "wb").write(C["slice"])
    write_vocab(os.path.join(wd, "vocab.bin"), C["vocab"])
    hd = os.path.join(fx, "hist"); os.makedirs(hd, exist_ok=True)
    return fx

# ---------------- §P parsing (shared wire layout) ----------------
def fnv1a64(data: bytes) -> int:
    h = 14695981039346656037
    for b in data:
        h ^= b
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h

def parse_sp(buf: bytes, off: int = 0):
    magic, ver, tid = struct.unpack_from("<IHI", buf, off)
    if magic != 0x54505250: raise ValueError("bad magic")
    if ver != 1: raise ValueError("bad version")
    if tid != 3: raise ValueError("bad teacher")
    sid, seq = struct.unpack_from("<QQ", buf, off + 10)
    kind = buf[off + 26]
    ss, se = struct.unpack_from("<QQ", buf, off + 27)
    ac = buf[off + 43]
    go = off + 44 + 16 * ac
    gc = buf[go]
    co = go + 1 + 16 * gc
    conf = buf[co]
    ck, = struct.unpack_from("<Q", buf, co + 1)
    if fnv1a64(buf[off:co + 1]) != ck: raise ValueError("checksum")
    aux = [struct.unpack_from("<QQ", buf, off + 44 + 16 * i) for i in range(ac)]
    gnd = [struct.unpack_from("<QQ", buf, go + 1 + 16 * i) for i in range(gc)]
    return dict(seq=seq, kind=kind, ss=ss, se=se, aux=aux, gnd=gnd,
                conf=conf, nbytes=co + 1 + 8 - off), co + 1 + 8 - off

def parse_stream(buf: bytes):
    props, off = [], 0
    while off < len(buf):
        p, n = parse_sp(buf, off)
        props.append(p); off += n
    return props

# ---------------- varA tape parsing (TST-1) ----------------
def parse_tape_varA(buf: bytes):
    props, events = [], {}
    off = 0
    while off < len(buf):
        if off + 5 > len(buf): break
        typ = buf[off]
        (ln,) = struct.unpack_from("<I", buf, off + 1)
        payload = buf[off + 5: off + 5 + ln]
        events[typ] = events.get(typ, 0) + 1
        if typ == 3:  # TEACHER_MSG
            p, _ = parse_sp(payload)
            props.append(p)
        off += 5 + ln
    return props, events

# ---------------- frozen decision policies ----------------
# policy(p, i, stim_len, gt, st) -> ("ADOPT",0,None) | ("REJECT",r,None) |
#                               ("REVISE",0,(rs,re)) | ("DEFER",0,None)
def _shift_span(p, stim_len, delta=7):
    w = p["se"] - p["ss"]
    if w >= stim_len: w = max(stim_len - 1, 1)
    rs = p["ss"] + delta
    if rs + w > stim_len: rs = stim_len - w
    if rs < 0: rs = 0
    re_ = rs + w
    if re_ <= rs: re_ = rs + 1
    if re_ > stim_len: re_ = stim_len; rs = re_ - 1
    return (rs, re_)

def _iou(a, b):
    s, e = max(a[0], b[0]), min(a[1], b[1])
    inter = max(0, e - s)
    union = (a[1] - a[0]) + (b[1] - b[0]) - inter
    return inter / union if union else 0.0

def policy_adopt_all(p, i, stim_len, gt, st): return ("ADOPT", 0, None)
def policy_r1storm(p, i, stim_len, gt, st): return ("REJECT", 1, None)
def policy_r34storm(p, i, stim_len, gt, st): return ("REJECT", 3 if i % 2 == 0 else 4, None)
def policy_revise_spam(p, i, stim_len, gt, st): return ("REVISE", 0, _shift_span(p, stim_len))
def policy_mixed(p, i, stim_len, gt, st):
    k = i % 4
    if k == 0: return ("ADOPT", 0, None)
    if k == 1: return ("REVISE", 0, _shift_span(p, stim_len))
    if k == 2: return ("REJECT", 1, None)
    return ("DEFER", 0, None)
def policy_revise_then_adopt(p, i, stim_len, gt, st):
    # REVISE each span once (to +7 shifted target); ADOPT when the teacher
    # re-proposes a previously issued REVISE target. Measures whether the
    # teacher's re-proposal converges to an adoptable span.
    span = (p["ss"], p["se"])
    if span in st.setdefault("targets", set()):
        return ("ADOPT", 0, None)
    tgt = _shift_span(p, stim_len)
    st["targets"].add(tgt)
    return ("REVISE", 0, tgt)

def policy_gt(p, i, stim_len, gt, st):
    # frozen D5 student: ADOPT on exact GT match; REVISE to best-IoU GT span
    # iff IoU>=0.5; else REJECT R1, escalating to R5 once a span has 2 rejects.
    span = (p["ss"], p["se"])
    if span in gt[1]: return ("ADOPT", 0, None)
    best, bi = 0.0, None
    for g in gt[1]:
        v = _iou(span, g)
        if v > best: best, bi = v, g
    if best >= 0.5: return ("REVISE", 0, bi)
    n = st.get(span, 0)
    st[span] = n + 1
    return ("REJECT", 5 if n >= 2 else 1, None)

POLICIES = {"adopt_all": policy_adopt_all, "r1storm": policy_r1storm,
            "r34storm": policy_r34storm, "revise_spam": policy_revise_spam,
            "mixed": policy_mixed, "gt": policy_gt,
            "revise_then_adopt": policy_revise_then_adopt}

# ---------------- drivers ----------------
def _dline_a(seq, dec):
    v, r, span = dec
    if v == "ADOPT": return f"D {seq} ADOPT 0"
    if v == "REJECT": return f"D {seq} REJECT {r}"
    # varA script parser requires REVISE reason 1-5 (v_parse, vd==2 branch)
    if v == "REVISE": return f"D {seq} REVISE 1 {span[0]} {span[1]}"
    if v == "DEFER": return f"D {seq} DEFER 0"
    raise ValueError(v)

def runA(policy_name, sess_id, workdir, max_rounds=5, init_lines=160, curr="std"):
    """Iterative fixed-point driver for varA's static-script interface."""
    from harness import (BIN_A, POLICIES, parse_tape_varA,
                         _dline_a, write_fixtures, CURR)
    import os, subprocess, time, hashlib
    C = CURR[curr]
    fx = write_fixtures(workdir, curr)
    gtfile = os.path.join(fx, "curr_gt.txt")
    pol = POLICIES[policy_name]
    gt = ("ab", set(C["gt_ab"]))
    stim_len = len(C["single"])
    # NOTE: varA opens script/stimfile/tape as bare child names under cwd "."
    header = f"SESSION {sess_id} {stim_len}\nSTIMFILE curr_gt.txt\n"
    # round 0: init policy lines
    dlines = [_dline_a(i, ("ADOPT", 0, None)) for i in range(init_lines)]
    converged = False
    rounds = []
    # The session is determined by the DECISION sequence D. The teacher emits
    # one extra undecided proposal when D exhausts (clean stop), so the fixed
    # point is over D, not over proposal count.
    D = [("ADOPT", 0, None)] * init_lines
    props, decs, raw, events = [], D, b"", {}
    t0 = time.time()
    for rnd in range(max_rounds):
        script_name = f"a_sess_{policy_name}_r{rnd}.txt"
        tape_name = f"a_tape_{policy_name}_r{rnd}.bin"
        script = os.path.join(fx, script_name)
        tape = os.path.join(fx, tape_name)
        if os.path.exists(tape): os.remove(tape)
        with open(script, "w") as f:
            f.write(header)
            f.write("\n".join(_dline_a(i, d) for i, d in enumerate(D)) + "\nEND\n")
        p = subprocess.run([BIN_A, "teach", script_name, tape_name],
                           capture_output=True, cwd=fx)
        raw = open(tape, "rb").read() if os.path.exists(tape) else b""
        try:
            props, events = parse_tape_varA(raw)
        except Exception:
            props, events = [], {"parse_error": 1}
        k = min(len(D), len(props))
        st = {}  # fresh student state per fixed-point round (each round is a new session)
        Dnew = [pol(props[i], i, stim_len, gt, st) for i in range(k)]
        rounds.append(dict(rc=p.returncode, nprops=len(props), ndec=len(D),
                           stdout_tail=p.stdout.decode(errors="replace")[-160:],
                           stderr=p.stderr.decode(errors="replace")[:200]))
        if Dnew == D[:len(Dnew)] and len(Dnew) == len(D):
            converged = True
            decs = Dnew
            break
        D = Dnew
        decs = D
    wall = time.time() - t0
    # decided proposals only (drop the trailing undecided one, if any)
    decided = props[:len(decs)]
    return dict(variant="A", policy=policy_name, proposals=decided,
                decisions=decs, rounds=rounds, converged=converged,
                wall_s=wall, tape_bytes=len(raw), events=events,
                n_undecided=len(props) - len(decided))

def runB(policy_name, sess_id, workdir, max_turns=30, curr="std"):
    from harness import (BIN_B, POLICIES, write_fixtures, _bp, CURR)
    import os, subprocess, time
    C = CURR[curr]
    fx = write_fixtures(workdir, curr)
    fx_abs = os.path.abspath(fx)
    stim_len = len(C["prose"])
    pol = POLICIES[policy_name]
    st = {}  # per-leg student state (R5 escalation, etc.)
    gt = ("ab", set(C["gt_ab"]))
    VMAP = {"ADOPT": 0, "REVISE": 1, "REJECT": 2, "DEFER": 3}
    records, all_props, all_decs = [], [], []
    t0 = time.time(); turn = 0; last_rc = 0; last_err = b""
    while turn < max_turns:
        hist = os.path.join(fx, f"b_hist_{policy_name}.bin")
        _bp.write_history(hist, records)
        p = subprocess.run([BIN_B, fx_abs, "curr_raw.bin", os.path.basename(hist),
                            str(sess_id)], capture_output=True, cwd=workdir)
        last_rc, last_err = p.returncode, p.stderr
        if p.returncode != 0:
            break
        try:
            props = _bp.parse_stream(p.stdout, stim_len, expect_tid=3,
                                     expect_sess=sess_id,
                                     expect_seq0=len(all_props))
        except ValueError:
            break
        if not props:
            break
        for pr in props:
            d = pol(pr, len(all_props), stim_len, gt, st)
            v, r, span = d
            records.append((pr["seq"], pr["kind"], VMAP[v], r, pr["ss"], pr["se"]))
            all_decs.append(d)
        all_props.extend(props)
        turn += 1
    wall = time.time() - t0
    return dict(variant="B", policy=policy_name, proposals=all_props,
                decisions=all_decs, turns=turn, rc=last_rc,
                stderr=last_err.decode(errors="replace")[:200],
                wall_s=wall, stdout_bytes=sum(pr.get("length", 0) for pr in all_props))

def runC(policy_name, sess_id, workdir, max_turns=64, curr="std"):
    from harness import (BIN_C, GT_C, POLICIES, write_fixtures, _ch)
    import os, subprocess, time
    C = CURR[curr]
    fx = write_fixtures(workdir, curr)
    wd = os.path.abspath(os.path.join(fx, "wired"))
    hd = os.path.abspath(os.path.join(fx, "hist"))
    pol = POLICIES[policy_name]
    st = {}  # per-leg student state (R5 escalation, etc.)
    gt = ("c", set(C["gt_c"]))
    stim_len = 65536
    VMAP = {"ADOPT": 1, "REVISE": 2, "REJECT": 3, "DEFER": 4}
    hist = _ch.new_history(sess_id)
    all_props, all_decs = [], []
    t0 = time.time(); turn = 0; last_rc = 0; last_err = ""
    hpath = os.path.join(hd, f"c_{policy_name}.hist")
    while turn < max_turns:
        with open(hpath, "wb") as f:
            f.write(hist)
        p = subprocess.run([BIN_C, "propose", "0", str(sess_id), wd, hd,
                            os.path.basename(hpath)],
                           capture_output=True, cwd=workdir)
        last_rc = p.returncode
        last_err = p.stderr.decode(errors="replace")[:200]
        if p.returncode == 20:
            terminal = "session_cap"
            break
        if p.returncode != 0:
            terminal = f"rc={p.returncode}"
            break
        try:
            pr = _ch.parse_proposal(p.stdout)
        except ValueError:
            terminal = "parse_error"
            break
        all_props.append(pr)
        hist = _ch.append_propose(hist, pr)
        d = pol(pr, len(all_props) - 1, stim_len, gt, st)
        v, r, span = d
        rs, re_ = (span if v == "REVISE" else (0, 0))
        hist = _ch.append_decide(hist, pr["seq"], VMAP[v], r, rs, re_)
        all_decs.append(d)
        turn += 1
    else:
        terminal = "turn_cap"
    wall = time.time() - t0
    return dict(variant="C", policy=policy_name, proposals=all_props,
                decisions=all_decs, turns=turn, rc=last_rc, terminal=terminal,
                stderr=last_err, wall_s=wall,
                stdout_bytes=sum(pr["nbytes"] for pr in all_props))
