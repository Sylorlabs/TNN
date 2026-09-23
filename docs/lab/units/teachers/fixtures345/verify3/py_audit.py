#!/usr/bin/env python3
"""verify3/py_audit.py — independent auditor for the arm-3 (muse-live) teacher fixture.

Independent of the Zag implementation: re-implements the §P wire format (B.3),
the TST-1 tape framing (B.4), the §C tripwire (B.8), and the sha256 tape chain,
then cross-checks the arm3 driver binary against them:

  1. violation battery — one RAW-injection script per iron-rule violation kind:
     asserts process exit == V code, exactly one INTEGRITY event with code
     1000+V, TAPE_FOOTER "HALTED:VIOLATION", expected TEACHER_MSG count,
     and byte-identical tapes across two fresh-dir runs.
  2. valid cross-check — Python-encoded proposals fed via RAW; asserts the
     driver logs the §P bytes verbatim and Python-decode matches field-for-field.
  3. §C audit — replays each tape's TEACHER_MSG/DECISION stream through an
     independent tripwire; asserts the driver's fire/no-fire decision matches,
     and reports strict-windowed coverage (conformance note vs cumulative).
  4. adversarial perturbations — reorder / confidence / stimulus-length /
     P-path tripwire fires (window + dump); asserts deterministic,
     input-dependent behavior and the exit-11 contract on P-path fires.
  5. live-vs-dryrun — same script in both modes: event streams identical
     except the header descriptor.

Writes results to verify3/audit_results.json and prints a human log.
Exit 0 iff every check passes.
"""
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.dirname(HERE)          # fixtures345/
BIN = os.path.join(FIX, "arm3_bin")
WORK = os.path.join(HERE, "work")

MAGIC = 0x54505250

# ---------------- §P codec (independent) ----------------
def fnv1a64(data: bytes) -> int:
    h = 14695981039346656037
    for b in data:
        h = ((h ^ b) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h

def sp_encode(tid, sid, seq, kind, ss, se, conf, aux=(), ground=()):
    b = bytearray()
    b += struct.pack("<I", MAGIC)
    b += struct.pack("<H", 1)
    b += struct.pack("<I", tid)
    b += struct.pack("<Q", sid)
    b += struct.pack("<Q", seq)
    b += bytes([kind])
    b += struct.pack("<Q", ss)
    b += struct.pack("<Q", se)
    b += bytes([len(aux)])
    for s, e in aux:
        b += struct.pack("<QQ", s, e)
    b += bytes([len(ground)])
    for s, e in ground:
        b += struct.pack("<QQ", s, e)
    b += bytes([conf & 0xFF])
    b += struct.pack("<Q", fnv1a64(bytes(b)))
    return bytes(b)

def sp_decode(b: bytes):
    assert len(b) >= 54, "too short"
    magic, ver, tid = struct.unpack("<IHI", b[0:10])
    assert magic == MAGIC and ver == 1
    sid, seq = struct.unpack("<QQ", b[10:26])
    kind = b[26]
    ss, se = struct.unpack("<QQ", b[27:43])
    ac = b[43]
    pos = 44
    aux = [struct.unpack("<QQ", b[pos + i * 16:pos + i * 16 + 16]) for i in range(ac)]
    pos += ac * 16
    gc = b[pos]; pos += 1
    ground = [struct.unpack("<QQ", b[pos + i * 16:pos + i * 16 + 16]) for i in range(gc)]
    pos += gc * 16
    conf = b[pos]; pos += 1
    (chk,) = struct.unpack("<Q", b[pos:pos + 8])
    assert pos + 8 == len(b), "length mismatch"
    assert fnv1a64(b[:pos]) == chk, "checksum mismatch"
    return dict(tid=tid, sid=sid, seq=seq, kind=kind, ss=ss, se=se,
                conf=conf, aux=aux, ground=ground)

# ---------------- tape framing (independent) ----------------
def parse_tape(data: bytes):
    evs = []
    i = 0
    while i < len(data):
        t = data[i]
        (ln,) = struct.unpack("<I", data[i + 1:i + 5])
        payload = data[i + 5:i + 5 + ln]
        assert len(payload) == ln
        evs.append((t, payload))
        i += 5 + ln
    return evs

def verify_chain(evs):
    ch = bytes(32)
    for t, payload in evs:
        ch = hashlib.sha256(ch + bytes([t]) + struct.pack("<I", len(payload)) + payload).digest()
    return ch

def parse_integrity(payload):
    (code,) = struct.unpack("<I", payload[0:4])
    cs = struct.unpack("<8Q", payload[4:68])
    return code, cs

def parse_footer(payload):
    memhash = payload[0:8]
    chain = payload[8:40]
    (ecount,) = struct.unpack("<Q", payload[40:48])
    (vlen,) = struct.unpack("<I", payload[48:52])
    verdict = payload[52:52 + vlen].decode()
    return chain, ecount, verdict

# ---------------- §C tripwire (independent, mirrors frozen B.8) ----------------
class Tripwire:
    """Mirrors sp345.zag TW semantics: cumulative coverage bitmap, rolling
    200-window for decided/accept/maxconf rates."""
    def __init__(self, stim_len):
        self.stim = stim_len
        self.slots = []          # list of dicts in propose order
        self.covered = set()
        self.fired = False
        self.fire_code = 0
        self.fire_at = None      # (kind, index) kind in {"propose","decide"}

    def _window(self):
        w = self.slots[-200:]
        d = sum(1 for s in w if s["decided"])
        a = sum(1 for s in w if s["accept"])
        m = sum(1 for s in w if s["maxconf"])
        return d, a, m, len(w)

    def _window_fires(self):
        d, a, m, w = self._window()
        return (self.stim > 0 and len(self.covered) * 100 >= self.stim * 95
                and d > 0 and a * 100 >= d * 95 and w > 0 and m * 100 >= w * 90)

    def propose(self, ss, se, conf):
        idx = len(self.slots)
        if self.fired:
            return self.fire_code
        self.slots.append({"decided": False, "accept": False,
                           "maxconf": conf == 255})
        for x in range(max(ss, 0), min(se, self.stim)):
            self.covered.add(x)
        if conf == 255 and (se - ss) * 100 > self.stim * 5:
            self.fired, self.fire_code, self.fire_at = True, 2, ("propose", idx)
            return 2
        if self._window_fires():
            self.fired, self.fire_code, self.fire_at = True, 1, ("propose", idx)
            return 1
        return 0

    def decide(self, seq, verdict):
        if seq < 0 or seq >= len(self.slots):
            return
        s = self.slots[seq]
        if s["decided"]:
            return
        s["decided"] = True
        if verdict == 1:
            s["accept"] = True
        if not self.fired and self._window_fires():
            self.fired, self.fire_code, self.fire_at = True, 1, ("decide", seq)

    def strict_windowed_coverage_max(self):
        """Conformance note: B.8's most literal reading scopes coverage to the
        200-window. Report the max over all windows."""
        best = 0.0
        n = len(self.slots)
        spans = [(s["ss"], s["se"]) for s in self.slots]
        for lo in range(n):
            cov = set()
            for ss, se in spans[max(0, lo - 199):lo + 1]:
                cov.update(range(max(ss, 0), min(se, self.stim)))
            best = max(best, len(cov) / self.stim if self.stim else 0.0)
        return best

    def attach_spans(self, spans):
        for s, (ss, se) in zip(self.slots, spans):
            s["ss"], s["se"] = ss, se

# ---------------- harness ----------------
RESULTS = {"checks": [], "pass": True}

def check(name, cond, detail=""):
    RESULTS["checks"].append({"name": name, "pass": bool(cond), "detail": detail})
    if not cond:
        RESULTS["pass"] = False
        print(f"FAIL {name} :: {detail}")
    else:
        print(f"ok   {name}")

def freshdir(case):
    d = os.path.join(WORK, case)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    shutil.copy(BIN, d)
    return d

def run_case(case, script_text, runs=2):
    """Write script, run `runs` times in fresh dirs, return (exit, tape_bytes, stdout)."""
    outs = []
    for r in range(runs):
        d = freshdir(f"{case}_r{r}")
        sp = os.path.join(d, "script.txt")
        with open(sp, "w") as f:
            f.write(script_text)
        p = subprocess.run(["./arm3_bin", "dryrun", "script.txt", "tape.tape"],
                           cwd=d, capture_output=True, text=True, timeout=120)
        with open(os.path.join(d, "tape.tape"), "rb") as f:
            tape = f.read()
        outs.append((p.returncode, tape, p.stdout))
    # determinism across runs
    same = all(o[1] == outs[0][1] for o in outs)
    check(f"{case}.deterministic_x{runs}", same,
          f"tape sha256={hashlib.sha256(outs[0][1]).hexdigest()}")
    return outs[0]

# ---------------- part 2: violation battery ----------------
SID, STIM = 4242, 123

def base_fields():
    return dict(tid=3, sid=SID, seq=0, kind=1, ss=0, se=5, conf=200)

def mutate(fields, fn):
    f = dict(fields)
    fn(f)
    return f

def raw_line(b: bytes):
    return "RAW " + b.hex().upper()

def script_of(*raws):
    return f"SESSION {SID} {STIM}\n" + "\n".join(raws) + "\nEND\n"

def vbyte_set(b: bytes, off: int, fmt: str, val: int) -> bytes:
    b = bytearray(b)
    struct.pack_into(fmt, b, off, val)
    return bytes(b)

def build_violations():
    V = []
    bf = base_fields()
    enc = lambda f: sp_encode(f["tid"], f["sid"], f["seq"], f["kind"], f["ss"],
                             f["se"], f["conf"], f.get("aux", ()), f.get("ground", ()))
    base = enc(bf)
    V.append(("magic", vbyte_set(base, 0, "<I", 0xDEADBEEF), 1))
    V.append(("version", vbyte_set(base, 4, "<H", 2), 2))
    # semantic mutations go through the encoder (fresh checksum): the driver
    # must report the SEMANTIC violation, not a checksum failure.
    V.append(("teacher2", enc(mutate(bf, lambda f: f.update(tid=2))), 3))
    V.append(("teacher0", enc(mutate(bf, lambda f: f.update(tid=0))), 3))
    V.append(("sess_mismatch", enc(mutate(bf, lambda f: f.update(sid=9999))), 3))
    V.append(("span_invert", enc(mutate(bf, lambda f: f.update(ss=10, se=5))), 5))
    V.append(("kind0", enc(mutate(bf, lambda f: f.update(kind=0))), 6))
    V.append(("kind6", enc(mutate(bf, lambda f: f.update(kind=6))), 6))
    c = bytearray(base); c[30] ^= 1
    V.append(("checksum", bytes(c), 7))
    V.append(("range_span", enc(mutate(bf, lambda f: f.update(se=200))), 8))
    V.append(("range_aux", enc(mutate(bf, lambda f: f.update(aux=[(200, 300)]))), 8))
    V.append(("range_ground", enc(mutate(bf, lambda f: f.update(ground=[(0, 500)]))), 8))
    # structural: truncated / extended / tiny
    aux1 = enc(mutate(bf, lambda f: f.update(aux=[(2, 6)])))   # 70 bytes
    assert len(aux1) == 70
    V.append(("len_trunc", aux1[:60], 10))
    V.append(("len_extend", base + b"\x00\x00\x00\x00", 10))
    V.append(("len_tiny", base[:30], 1))                      # <54 -> BAD_MAGIC
    # counts: need padding so the length pre-checks pass before V_COUNTS
    V.append(("counts_aux", vbyte_set(base, 43, "<B", 9) + bytes(189 - len(base)), 9))
    V.append(("counts_ground", vbyte_set(base, 44, "<B", 9) + bytes(64 - len(base)), 9))
    # seq gap / duplicate need two proposals
    seq0 = enc(bf)
    seq2 = enc(mutate(bf, lambda f: f.update(seq=2)))
    V.append(("seq_gap", (seq0, seq2), 4))
    seq0b = enc(bf)
    V.append(("seq_dup", (seq0, seq0b), 4))
    return V

def run_violation_battery():
    for name, payload, vcode in build_violations():
        raws = [raw_line(payload)] if isinstance(payload, bytes) \
            else [raw_line(p) for p in payload]
        n_teacher_expected = 1 if name in ("seq_gap", "seq_dup") else 0
        ec, tape, out = run_case(f"viol_{name}", script_of(*raws))
        evs = parse_tape(tape)
        types = [t for t, _ in evs]
        integ = [(t, p) for t, p in evs if t == 7]
        foot = [(t, p) for t, p in evs if t == 9]
        check(f"viol_{name}.exit", ec == vcode, f"exit={ec} want={vcode}")
        check(f"viol_{name}.integrity_logged",
              len(integ) == 1 and parse_integrity(integ[0][1])[0] == 1000 + vcode,
              f"integrity events={len(integ)}")
        check(f"viol_{name}.footer_halted",
              len(foot) == 1 and parse_footer(foot[0][1])[2] == "HALTED:VIOLATION",
              "")
        check(f"viol_{name}.teacher_msgs", types.count(3) == n_teacher_expected,
              f"TEACHER_MSG={types.count(3)} want={n_teacher_expected}")
        # halt is terminal: nothing after FOOTER
        check(f"viol_{name}.halt_terminal", types[-1] == 9, f"last={types[-1]}")

# ---------------- part 3: valid cross-check ----------------
def run_valid_crosscheck():
    p1 = sp_encode(3, SID, 0, 1, 10, 20, 200, aux=[(1, 2)], ground=[(3, 4), (5, 6)])
    p2 = sp_encode(3, SID, 1, 3, 65, 70, 180, aux=[(65, 70), (71, 76)], ground=[(65, 70)])
    p3 = sp_encode(3, SID, 2, 5, 1, 2, 128)          # RETRACT seq 1
    script = script_of(raw_line(p1), raw_line(p2), raw_line(p3))
    ec, tape, out = run_case("valid_xcheck", script)
    evs = parse_tape(tape)
    check("xcheck.exit", ec == 0, f"exit={ec}")
    msgs = [p for t, p in evs if t == 3]
    check("xcheck.n_msgs", len(msgs) == 3, f"got {len(msgs)}")
    for i, (sent, logged) in enumerate(zip((p1, p2, p3), msgs)):
        check(f"xcheck.msg{i}_verbatim", sent == logged, "bytes differ")
        dec = sp_decode(logged)
        exp = sp_decode(sent)
        check(f"xcheck.msg{i}_fields", dec == exp, f"{dec} vs {exp}")
    # chain verifies end-to-end (footer embeds the pre-footer chain)
    foot = [p for t, p in evs if t == 9][0]
    chain, ecount, verdict = parse_footer(foot)
    check("xcheck.chain", verify_chain(evs[:-1]) == chain, "chain mismatch")
    check("xcheck.footer_ok", verdict == "OK" and ecount == len(evs) - 1,
          f"verdict={verdict} ecount={ecount}")

# ---------------- part 4: §C audit over tapes ----------------
def replay_tape(evs, stim_len):
    tw = Tripwire(stim_len)
    spans = []
    tripwire_by_driver = None   # (integrity code) — only codes 1/2 are tripwire fires
    violation_by_driver = None  # 1000+V iron-rule codes
    for t, p in evs:
        if t == 3:
            d = sp_decode(p)
            spans.append((d["ss"], d["se"]))
            tw.propose(d["ss"], d["se"], d["conf"])
        elif t == 12:
            (pseq,) = struct.unpack("<Q", p[0:8])
            verdict = p[8]
            tw.decide(pseq, verdict)
        elif t == 7:
            code, _ = parse_integrity(p)
            if code in (1, 2) and tripwire_by_driver is None:
                tripwire_by_driver = code
            elif code >= 1000 and violation_by_driver is None:
                violation_by_driver = code
    tw.attach_spans(spans)
    return tw, tripwire_by_driver, violation_by_driver

def audit_tape(name, tape_path, stim_len, expect_fire=None, expect_violation=None):
    """expect_fire: None/False/True for tripwire; expect_violation: V code or None."""
    with open(tape_path, "rb") as f:
        tape = f.read()
    evs = parse_tape(tape)
    foot = [p for t, p in evs if t == 9][0]
    chain, ecount, verdict = parse_footer(foot)
    # the footer embeds the pre-footer chain: verify over all but the last event
    check(f"c_{name}.chain", verify_chain(evs[:-1]) == chain,
          "footer chain != recomputed chain")
    tw, trip_by_driver, viol_by_driver = replay_tape(evs, stim_len)
    check(f"c_{name}.tripwire_agree", (tw.fired == (trip_by_driver is not None)),
          f"audit_fired={tw.fired} driver_tripwire={trip_by_driver}")
    if expect_fire:
        check(f"c_{name}.fire_code", tw.fired and tw.fire_code == trip_by_driver,
              f"audit_code={tw.fire_code} driver_code={trip_by_driver}")
        check(f"c_{name}.fire_at", tw.fire_at is not None, f"{tw.fire_at}")
    else:
        check(f"c_{name}.no_tripwire", not tw.fired and trip_by_driver is None, "")
    if expect_violation is not None:
        check(f"c_{name}.violation_code", viol_by_driver == 1000 + expect_violation,
              f"driver_violation={viol_by_driver}")
    wmax = tw.strict_windowed_coverage_max()
    print(f"info c_{name}: cumulative_cov={len(tw.covered)/stim_len:.3f} "
          f"strict_windowed_max={wmax:.3f} proposals={len(tw.slots)} verdict={verdict}")
    RESULTS["checks"].append({"name": f"c_{name}.coverage_report", "pass": True,
        "detail": f"cumulative={len(tw.covered)/stim_len:.3f} windowed_max={wmax:.3f}"})
    return tw

# ---------------- part 5: adversarial perturbations ----------------
def perturb_reorder():
    with open(os.path.join(FIX, "dryrun_teach.txt")) as f:
        lines = f.read().splitlines()
    # swap the seq-3 and seq-4 P lines
    i3 = next(i for i, l in enumerate(lines) if l.startswith("P 3 3 "))
    i4 = next(i for i, l in enumerate(lines) if l.startswith("P 3 4 "))
    lines[i3], lines[i4] = lines[i4], lines[i3]
    ec, tape, out = run_case("perturb_reorder", "\n".join(lines) + "\n")
    evs = parse_tape(tape)
    integ = [p for t, p in evs if t == 7]
    check("perturb_reorder.exit", ec == 4, f"exit={ec}")
    check("perturb_reorder.integrity", len(integ) == 1 and
          parse_integrity(integ[0])[0] == 1004, "")

def perturb_conf():
    with open(os.path.join(FIX, "dryrun_teach.txt")) as f:
        lines = f.read().splitlines()
    out_lines = []
    for l in lines:
        toks = l.split()
        # P/PAUX grammar: <dir> tid seq kind ss se conf ... -> conf is token 6
        if toks and toks[0] in ("P", "PAUX") and len(toks) >= 7:
            toks[6] = "1"
        out_lines.append(" ".join(toks))
    script = "\n".join(out_lines) + "\n"
    ec, tape, out = run_case("perturb_conf1", script)
    evs = parse_tape(tape)
    check("perturb_conf.exit", ec == 0, f"exit={ec}")
    msgs = [p for t, p in evs if t == 3]
    check("perturb_conf.n", len(msgs) == 12, f"got {len(msgs)}")
    check("perturb_conf.applied", all(sp_decode(m)["conf"] == 1 for m in msgs), "")
    with open(os.path.join(FIX, "tape_teach.tape"), "rb") as f:
        base = f.read()
    check("perturb_conf.differs_from_baseline",
          hashlib.sha256(tape).hexdigest() != hashlib.sha256(base).hexdigest(),
          "tape identical despite perturbed input")

def perturb_stimlen():
    with open(os.path.join(FIX, "dryrun_teach.txt")) as f:
        script = f.read().replace("SESSION 4242 123", "SESSION 4242 5000")
    ec, tape, out = run_case("perturb_stim5000", script)
    evs = parse_tape(tape)
    check("perturb_stim.exit", ec == 0, f"exit={ec}")
    msgs = [p for t, p in evs if t == 3]
    with open(os.path.join(FIX, "tape_teach.tape"), "rb") as f:
        base_evs = parse_tape(f.read())
    base_msgs = [p for t, p in base_evs if t == 3]
    check("perturb_stim.proposals_identical", msgs == base_msgs,
          "proposal bytes changed with stimulus length")

def ppath_window_fire():
    lines = ["SESSION 4244 1000"]
    for k in range(190):
        lines.append(f"P 3 {k} 1 {5*k} {5*k+5} 255")
        lines.append(f"D {k} ADOPT 0")
    lines.append("END")
    ec, tape, out = run_case("ppath_window", "\n".join(lines) + "\n")
    evs = parse_tape(tape)
    types = [t for t, _ in evs]
    integ = [p for t, p in evs if t == 7]
    check("ppath_window.exit11", ec == 11, f"exit={ec}")
    check("ppath_window.code1", len(integ) == 1 and
          parse_integrity(integ[0])[0] == 1, "")
    check("ppath_window.n_msgs", types.count(3) == 190, f"got {types.count(3)}")
    check("ppath_window.halt_terminal", types[-1] == 9, "")

def ppath_dump_fire():
    script = "SESSION 4245 1000\nP 3 0 1 0 60 255\nEND\n"
    ec, tape, out = run_case("ppath_dump", script)
    evs = parse_tape(tape)
    integ = [p for t, p in evs if t == 7]
    check("ppath_dump.exit11", ec == 11, f"exit={ec}")
    check("ppath_dump.code2", len(integ) == 1 and
          parse_integrity(integ[0])[0] == 2, "")

# ---------------- part 6: live vs dryrun ----------------
def live_vs_dryrun():
    with open(os.path.join(HERE, "teach_live.txt")) as f:
        script = f.read()
    outs = {}
    for mode in ("dryrun", "live"):
        d = freshdir(f"livecmp_{mode}")
        sp = os.path.join(d, "script.txt")
        with open(sp, "w") as f:
            f.write(script)
        p = subprocess.run(["./arm3_bin", mode, "script.txt", "tape.tape"],
                           cwd=d, capture_output=True, text=True, timeout=120)
        with open(os.path.join(d, "tape.tape"), "rb") as f:
            outs[mode] = (p.returncode, parse_tape(f.read()))
    check("live.exit", outs["live"][0] == 0, f"exit={outs['live'][0]}")
    check("dry.exit", outs["dryrun"][0] == 0, f"exit={outs['dryrun'][0]}")
    strip = lambda evs: [(t, p) for t, p in evs if t not in (1, 9)]
    check("live.equiv_dryrun", strip(outs["live"][1]) == strip(outs["dryrun"][1]),
          "event streams differ beyond header/footer")
    hdr = [p for t, p in outs["live"][1] if t == 1][0]
    check("live.descr", b"arm3-live" in hdr, "")
    hdr_d = [p for t, p in outs["dryrun"][1] if t == 1][0]
    check("dry.descr", b"arm3-dryrun" in hdr_d, "")

# ---------------- main ----------------
def main():
    os.makedirs(WORK, exist_ok=True)
    assert os.path.isfile(BIN), f"missing binary {BIN}"
    # static: no RNG / wallclock / flaw manifest in the arm-3 path sources.
    # (comment lines declaring their ABSENCE, e.g. "no wallclock", are not hits —
    # same exclusion run_all.sh applies.)
    src = "".join(open(os.path.join(FIX, f)).read()
                  for f in ("arm3.zag", "sp345.zag", "tape345.zag"))
    code_lines = [l for l in src.splitlines()
                  if "no wallclock" not in l.lower() and "no-wallclock" not in l.lower()]
    code_src = "\n".join(code_lines)
    check("static.no_rng", not re.search(r"urandom|rand\(\)|getrandom", code_src), "")
    check("static.no_wallclock",
          not re.search(r"gettimeofday|clock_gettime", code_src, re.I), "")
    check("static.no_flaw_manifest",
          "flaw manifest" not in src.lower() or "NO flaw manifest" in src, "")
    check("static.arm3_only_speaks_for_3",
          'teacher_id!=3' in src.replace(" ", ""), "")
    run_violation_battery()
    run_valid_crosscheck()
    # §C audit over the canonical tapes (regenerate teach/violation/smuggle first
    # via the canonical scripts so the audit runs on fresh driver output)
    for scr, tape in (("dryrun_teach.txt", "tape_teach.tape"),
                      ("dryrun_violation.txt", "tape_violation.tape"),
                      ("dryrun_smuggle.txt", "tape_smuggle.tape")):
        d = freshdir("regen")
        shutil.copy(os.path.join(FIX, scr), os.path.join(d, "s.txt"))
        p = subprocess.run(["./arm3_bin", "dryrun", "s.txt", "t.tape"],
                           cwd=d, capture_output=True, text=True, timeout=180)
        shutil.copy(os.path.join(d, "t.tape"), os.path.join(WORK, tape))
        print(f"regen {scr}: exit={p.returncode}")
    audit_tape("teach", os.path.join(WORK, "tape_teach.tape"), 123)
    audit_tape("violation", os.path.join(WORK, "tape_violation.tape"), 123,
               expect_violation=4)
    audit_tape("smuggle", os.path.join(WORK, "tape_smuggle.tape"), 1000,
               expect_fire=True)
    perturb_reorder()
    perturb_conf()
    perturb_stimlen()
    ppath_window_fire()
    ppath_dump_fire()
    live_vs_dryrun()
    with open(os.path.join(HERE, "audit_results.json"), "w") as f:
        json.dump(RESULTS, f, indent=1)
    n = len(RESULTS["checks"])
    bad = sum(1 for c in RESULTS["checks"] if not c["pass"])
    print(f"AUDIT_RESULT,checks={n},bad={bad}")
    return 0 if RESULTS["pass"] else 1

if __name__ == "__main__":
    sys.exit(main())
