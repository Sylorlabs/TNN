#!/usr/bin/env python3
"""Arm-3 varB end-to-end verification driver.

Runs: build check, turn1, history-sensitivity (4 phases), N=5 determinism,
5 adversarial heap perturbations, §P iron-rule battery, §C tripwire battery,
no-RNG/no-wallclock scan. Writes evidence/ logs. Exits nonzero on any failure.
"""
import hashlib
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tools"))
from props import parse_stream, write_history, kind_name, verdict_name
from tripwire import tripwire, rolling200

BIN = os.path.join(HERE, "build", "teacher_bin")
FIX = os.path.join(HERE, "fixtures")
EV = os.path.join(HERE, "evidence")
SESS = 1001

fails = []
log_lines = []

def log(s=""):
    log_lines.append(s)
    print(s)

def check(name, cond, detail=""):
    log(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        fails.append(name)

def run_teacher(stim, hist, sess, env=None, cwd=None):
    p = subprocess.run([BIN, FIX, stim, hist, str(sess)],
                       capture_output=True, env=env, cwd=cwd or HERE)
    return p.returncode, p.stdout, p.stderr

def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]

def main():
    os.makedirs(EV, exist_ok=True)
    stim = open(os.path.join(FIX, "stimulus.txt"), "rb").read()
    STIM_LEN = len(stim)
    log(f"stimulus: {STIM_LEN} bytes")

    # ---- 0. static no-RNG / no-wallclock scan ----
    src = open(os.path.join(HERE, "teacher.zag")).read()
    code = "\n".join(l for l in src.splitlines()
                     if not l.strip().startswith("//"))
    import re
    bad = re.findall(r"(?i)rand|srand|_zag_time|wallclock|gettimeofday|"
                     r"clock_gettime|rdtsc|/dev/urandom|lcg|entropy", code)
    # 'consec_rej' etc. contain no banned token; filter word-boundary noise
    bad = [b for b in bad if b.lower() not in ()]
    check("no-RNG/no-wallclock tokens", not bad, f"hits={bad}")

    # ---- 1. turn 1 (empty history) ----
    rc, out1, err1 = run_teacher("stimulus.txt", "hist_empty.bin", SESS)
    check("turn1 exit 0", rc == 0, f"rc={rc} err={err1[:120]}")
    t1 = parse_stream(out1, STIM_LEN, expect_sess=SESS, expect_seq0=0)
    check("turn1: 8 WORD_SPAN proposals", len(t1) == 8 and
          all(p["kind"] == 1 for p in t1))
    check("turn1: confidence band 120-180",
          all(120 <= p["conf"] <= 180 for p in t1),
          f"confs={[p['conf'] for p in t1]}")
    check("turn1: single grounding each", all(p["grounds"] and len(p["grounds"]) == 1 for p in t1))
    open(os.path.join(EV, "turn1.out"), "wb").write(out1)
    open(os.path.join(EV, "turn1.err"), "wb").write(err1)

    # ---- 2. build histories + turn 2 for each phase ----
    r = subprocess.run([sys.executable, os.path.join(FIX, "gen_hist.py"),
                        os.path.join(EV, "turn1.out"), FIX],
                       capture_output=True, text=True)
    check("gen_hist", r.returncode == 0, r.stderr[:200])

    phases = {}
    for name, want_phase, want_name in [
            ("hist_adopt4", 1, "CORROBORATE"),
            ("hist_adopt8", 2, "RELATE"),
            ("hist_reject", 0, "INTRODUCE"),
            ("hist_consol", 3, "CONSOLIDATE")]:
        rc, out, err = run_teacher("stimulus.txt", name + ".bin", SESS)
        check(f"turn2/{name} exit 0", rc == 0, f"rc={rc}")
        errt = err.decode()
        m = [l for l in errt.splitlines() if l.startswith("V3TRACE")]
        check(f"turn2/{name} has V3TRACE", len(m) == 1, m[0] if m else "")
        trace = m[0] if m else ""
        kv = dict(kv.split("=") for kv in trace.split()[1:])
        phases[name] = kv
        check(f"turn2/{name} phase={want_name}", kv.get("name") == want_name,
              trace)
        # parse proposals: seq continues after history maxseq
        n_hist = {"hist_adopt4": 4, "hist_adopt8": 8,
                  "hist_reject": 8, "hist_consol": 11}[name]
        props = parse_stream(out, STIM_LEN, expect_sess=SESS,
                             expect_seq0=n_hist)
        kinds = sorted(set(p["kind"] for p in props))
        check(f"turn2/{name} proposals parse ({len(props)})", True,
              f"kinds={[kind_name(k) for k in kinds]}")
        check(f"turn2/{name} conf never 255",
              all(p["conf"] != 255 for p in props))
        open(os.path.join(EV, f"turn2_{name}.out"), "wb").write(out)
        open(os.path.join(EV, f"turn2_{name}.err"), "wb").write(err)
        phases[name]["_props"] = props
        phases[name]["_out"] = out

    # ---- 2b. three-turn chain: INTRODUCE -> CORROBORATE -> RELATE ----
    chain_recs = [(i, 1, 0, 0, t1[i]["ss"], t1[i]["se"]) for i in range(4)]
    t2props = phases["hist_adopt4"]["_props"]
    for p in t2props:
        chain_recs.append((p["seq"], 1, 0, 0, p["ss"], p["se"]))
    write_history(os.path.join(FIX, "hist_chain3.bin"), chain_recs)
    rc, out3, err3 = run_teacher("stimulus.txt", "hist_chain3.bin", SESS)
    check("chain turn3 exit 0", rc == 0)
    tr3 = [l for l in err3.decode().splitlines() if l.startswith("V3TRACE")][0]
    check("chain turn3 phase=RELATE", "name=RELATE" in tr3, tr3)
    p3 = parse_stream(out3, STIM_LEN, expect_sess=SESS, expect_seq0=8)
    check("chain turn3 kinds GROUP/SAME_AS/BOUNDARY",
          {q["kind"] for q in p3} == {2, 3, 4})
    open(os.path.join(EV, "turn3_chain.out"), "wb").write(out3)
    open(os.path.join(EV, "turn3_chain.err"), "wb").write(err3)
    # appeal grounding carries NEW evidence (occurrence #2, not the original)
    rj = phases["hist_reject"]["_props"]
    t1g0 = t1[0]["grounds"][0]
    check("appeal grounding is new evidence",
          rj[0]["grounds"][0] != t1g0 and rj[0]["grounds"][0] != (t1[0]["ss"], t1[0]["se"]),
          f"orig ground={t1g0} appeal ground={rj[0]['grounds'][0]}")
    tr = {k: v for k, v in phases.items()}
    check("sensitivity: reject->INTRODUCE(fresh) vs adopt4->CORROBORATE",
          tr["hist_reject"]["name"] == "INTRODUCE"
          and tr["hist_reject"]["fresh"] == "1"
          and tr["hist_adopt4"]["name"] == "CORROBORATE",
          f"reject={tr['hist_reject']['name']}/fresh={tr['hist_reject']['fresh']} "
          f"adopt4={tr['hist_adopt4']['name']}")
    rk = [kind_name(p["kind"]) for p in tr["hist_reject"]["_props"]]
    ak = [kind_name(p["kind"]) for p in tr["hist_adopt4"]["_props"]]
    rk8 = [kind_name(p["kind"]) for p in tr["hist_adopt8"]["_props"]]
    check("sensitivity: different proposal character (reject vs adopt4)",
          set(rk) != set(ak) or rk != ak,
          f"reject kinds={sorted(set(rk))} adopt4 kinds={sorted(set(ak))}")
    # strong form of the requirement: rejection-heavy -> INTRODUCE/WORD_SPAN,
    # adoption-heavy (8 adopts) -> RELATE/GROUP+SAME_AS+BOUNDARY: disjoint kinds
    check("sensitivity: disjoint proposal kinds (reject vs adopt8)",
          set(rk).isdisjoint(set(rk8)),
          f"reject={sorted(set(rk))} adopt8={sorted(set(rk8))}")
    # corroborate specifics: re-proposals of adopted spans, 2-3 grounds, conf 180-220
    cp = tr["hist_adopt4"]["_props"]
    t1spans = {(p["ss"], p["se"]) for p in t1[:4]}
    check("corroborate: re-proposes adopted spans",
          all((p["ss"], p["se"]) in t1spans for p in cp) and len(cp) == 4)
    check("corroborate: 2-3 grounding spans",
          all(2 <= len(p["grounds"]) <= 3 for p in cp),
          f"ng={[len(p['grounds']) for p in cp]}")
    check("corroborate: conf 180-220",
          all(180 <= p["conf"] <= 220 for p in cp),
          f"confs={[p['conf'] for p in cp]}")
    # relate specifics: has GROUP, SAME_AS, BOUNDARY
    rkp = {p["kind"] for p in tr["hist_adopt8"]["_props"]}
    check("relate: GROUP+SAME_AS+BOUNDARY present", rkp == {2, 3, 4},
          f"kinds={sorted(rkp)}")
    # consolidate specifics: 2 RETRACTs then boundary summaries
    sp = tr["hist_consol"]["_props"]
    check("consolidate: 2 RETRACTs first",
          [p["kind"] for p in sp[:2]] == [5, 5],
          f"kinds={[p['kind'] for p in sp]}")
    check("consolidate: retract targets 7 and 10",
          [(p["ss"], p["se"]) for p in sp[:2]] == [(7, 8), (10, 11)])
    check("consolidate: low rate <=4", len(sp) <= 4, f"n={len(sp)}")
    # reject specifics: 2 appeals (re-proposals of seq0/seq1 spans) + 6 fresh
    jp = tr["hist_reject"]["_props"]
    check("reject: 2 appeals + fresh words",
          len(jp) == 8 and (jp[0]["ss"], jp[0]["se"]) == (t1[0]["ss"], t1[0]["se"])
          and (jp[1]["ss"], jp[1]["se"]) == (t1[1]["ss"], t1[1]["se"])
          and jp[2]["ss"] >= 296,
          f"first3={[ (p['ss'],p['se']) for p in jp[:3]]}")
    check("reject: appeal conf escalated (162/170)",
          [p["conf"] for p in jp[:2]] == [162, 170],
          f"confs={[p['conf'] for p in jp[:2]]}")

    # ---- 3. determinism: N=5 byte-identical ----
    outs, errs = [], []
    for i in range(5):
        rc, out, err = run_teacher("stimulus.txt", "hist_adopt4.bin", SESS)
        check(f"det run{i} exit 0", rc == 0)
        outs.append(out)
        errs.append(err)
    check("N=5 stdout byte-identical", all(o == outs[0] for o in outs),
          f"sha={sha(outs[0])}")
    check("N=5 stderr byte-identical", all(e == errs[0] for e in errs))

    # ---- 4. adversarial heap perturbations (5 scenarios x 3 runs) ----
    base_out, base_err = outs[0], errs[0]
    # P1: different session_id -> deterministic, differs
    p1 = [run_teacher("stimulus.txt", "hist_adopt4.bin", 424242) for _ in range(3)]
    check("P1 session_id: 3/3 identical", all(p[1] == p1[0][1] for p in p1))
    check("P1 session_id: differs deterministically", p1[0][1] != base_out)
    # P2: junk env + cwd=/tmp -> identical to baseline
    env2 = dict(os.environ, V3_JUNK="x" * 5000, V3_NOISE="1")
    p2 = [run_teacher("stimulus.txt", "hist_adopt4.bin", SESS, env=env2, cwd="/tmp")
          for _ in range(3)]
    check("P2 env/cwd: 3/3 identical", all(p[1] == p2[0][1] for p in p2))
    check("P2 env/cwd: equals baseline", p2[0][1] == base_out and p2[0][2] == base_err)
    # P3: stimulus flip outside any span -> identical
    stim3 = bytearray(stim)
    flip_at = stim3.index(b" ", 500)  # a space mid-text
    stim3[flip_at] = 0x09  # tab: still a non-word byte
    open(os.path.join(FIX, "stim_p3.bin"), "wb").write(stim3)
    p3 = [run_teacher("stim_p3.bin", "hist_adopt4.bin", SESS) for _ in range(3)]
    check("P3 flip-outside: 3/3 identical", all(p[1] == p3[0][1] for p in p3))
    check("P3 flip-outside: equals baseline", p3[0][1] == base_out,
          f"flipped byte {flip_at}")
    # P4: stimulus flip inside adopted span (seq0 'the'@0-3) -> differs deterministically
    stim4 = bytearray(stim)
    stim4[2] = ord("x")  # 'the' -> 'txe' at 0..3
    open(os.path.join(FIX, "stim_p4.bin"), "wb").write(stim4)
    p4 = [run_teacher("stim_p4.bin", "hist_adopt4.bin", SESS) for _ in range(3)]
    check("P4 flip-inside: 3/3 identical", all(p[1] == p4[0][1] for p in p4))
    check("P4 flip-inside: differs deterministically", p4[0][1] != base_out)
    # P5: history + trailing DEFER on a fresh span -> signals untouched -> identical
    import re as _re
    m5 = _re.search(rb"[A-Za-z0-9_]{3,}", bytes(stim[100:]))
    dss, dse = 100 + m5.start(), 100 + m5.end()
    recs = [(i, 1, 0, 0, t1[i]["ss"], t1[i]["se"]) for i in range(4)]
    recs.append((4, 1, 3, 0, dss, dse))
    write_history(os.path.join(FIX, "hist_p5.bin"), recs)
    p5 = [run_teacher("stimulus.txt", "hist_p5.bin", SESS) for _ in range(3)]
    check("P5 trailing DEFER: 3/3 identical", all(p[1] == p5[0][1] for p in p5))
    # maxseq advanced by the defer record, so seqs shift by one; the teaching
    # decisions must be identical modulo seq.
    p5props = parse_stream(p5[0][1], STIM_LEN, expect_sess=SESS, expect_seq0=5)
    baseprops = parse_stream(base_out, STIM_LEN, expect_sess=SESS, expect_seq0=4)
    strip = lambda ps: [(p["kind"], p["ss"], p["se"], p["aux"],
                         p["grounds"], p["conf"]) for p in ps]
    check("P5 trailing DEFER: same teaching decisions (mod seq)",
          strip(p5props) == strip(baseprops),
          f"defer span=({dss},{dse})")

    # ---- 4b. adversarial heap battery: 5 perturbations, byte-identical ----
    # Allocator finding (strace, 2026-09-21): this runtime uses no glibc
    # malloc -- large arenas are raw anonymous mmaps (kernel-zeroed), small
    # arenas come from a 1 MiB bump region with no frees. The honest
    # adversarial surface is therefore: glibc perturb (no-op; documents no
    # dependence), ASLR on/off (mmap bases move every exec -- catches pointer
    # leaks into the stream), environment size, stack limit, cwd+stdin.
    heap_base = subprocess.run([BIN, FIX, "stimulus.txt", "hist_empty.bin",
                                str(SESS)], capture_output=True)
    heap_base_out, heap_base_err = heap_base.stdout, heap_base.stderr
    heap_cases = []
    heap_cases.append(("H1 MALLOC_PERTURB_=165",
                       ["env", "MALLOC_PERTURB_=165", BIN, FIX,
                        "stimulus.txt", "hist_empty.bin", str(SESS)], None, None))
    heap_cases.append(("H2 ASLR disabled",
                       ["setarch", "-R", BIN, FIX,
                        "stimulus.txt", "hist_empty.bin", str(SESS)], None, None))
    big_env = dict(os.environ)
    for _i in range(200):
        big_env[f"VARB_JUNK_{_i:03d}"] = "z" * 1024
    heap_cases.append(("H3 200KB environment",
                       [BIN, FIX, "stimulus.txt", "hist_empty.bin", str(SESS)],
                       big_env, None))
    heap_cases.append(("H4 tiny stack",
                       ["bash", "-c",
                        f"ulimit -s 512; exec {BIN} {FIX} stimulus.txt"
                        f" hist_empty.bin {SESS}"], None, None))
    env5 = dict(os.environ, MALLOC_PERTURB_="219")
    heap_cases.append(("H5 cwd+perturb+stdin-closed",
                       [BIN, FIX, "stimulus.txt", "hist_empty.bin", str(SESS)],
                       env5, "/tmp"))
    for label, argv, env, cwd in heap_cases:
        kw = {}
        if env is not None:
            kw["env"] = env
        if cwd is not None:
            kw["cwd"] = cwd
            kw["stdin"] = subprocess.DEVNULL
        r = subprocess.run(argv, capture_output=True, **kw)
        check(f"heap/{label} exit 0", r.returncode == 0)
        check(f"heap/{label} stdout byte-identical", r.stdout == heap_base_out,
              f"{len(r.stdout)}B")
        check(f"heap/{label} stderr byte-identical", r.stderr == heap_base_err)

    # ---- 5. §P iron-rule battery ----
    def mal_hist(path, mutate):
        with open(os.path.join(FIX, "hist_adopt4.bin"), "rb") as f:
            b = bytearray(f.read())
        mutate(b)
        open(path, "wb").write(b)

    cases = []
    # (name, stimulus, history, expected_exit)
    cases.append(("no-args-special", None, None, 1))
    cases.append(("bad-dir", "stimulus.txt", "hist_adopt4.bin", 2))
    cases.append(("bad-name", "stimulus.txt", "hist_adopt4.bin", 3))
    cases.append(("missing-stimulus", "stimulus.txt", "hist_adopt4.bin", 4))
    cases.append(("empty-stimulus", "stimulus.txt", "hist_adopt4.bin", 5))
    open(os.path.join(FIX, "stim_empty.bin"), "wb").write(b"")
    cases.append(("missing-history", "stimulus.txt", "hist_adopt4.bin", 20))

    muts = [
        ("bad-magic", lambda b: b.__setitem__(slice(0, 4), b"\x00\x00\x00\x00"), 10),
        ("bad-version", lambda b: struct.pack_into("<H", b, 4, 2), 11),
        ("truncated", lambda b: b.__delitem__(slice(len(b) - 1, len(b))), 12),
        ("extended", lambda b: b.extend(b"\x00"), 12),
        ("bad-kind", lambda b: b.__setitem__(18, 9), 13),
        ("bad-verdict", lambda b: b.__setitem__(19, 7), 13),
        ("bad-reason-reject", lambda b: (b.__setitem__(19, 2), b.__setitem__(20, 9)), 13),
        ("reason-on-adopt", lambda b: b.__setitem__(20, 1), 13),
        ("dup-seq", lambda b: struct.pack_into("<Q", b, 10 + 32, 0), 14),
        ("bad-span-order", lambda b: struct.pack_into("<Q", b, 10 + 32 + 12, 9), 15),
        ("span-past-end", lambda b: struct.pack_into("<Q", b, 10 + 32 + 20, STIM_LEN + 1), 15),
        ("reserved-nonzero", lambda b: struct.pack_into("<I", b, 10 + 32 + 28, 1), 16),
    ]
    # retract-target violation needs a kind-5 record; craft separately
    recs5 = [(i, 1, 0, 0, t1[i]["ss"], t1[i]["se"]) for i in range(4)]
    recs5.append((4, 5, 0, 0, 99, 100))  # target 99 >= seq 4
    write_history(os.path.join(FIX, "hist_badretract.bin"), recs5)

    for name, stimf, histf, want in cases:
        if name == "no-args-special":
            p = subprocess.run([BIN], capture_output=True, cwd=HERE)
        elif name == "bad-dir":
            p = subprocess.run([BIN, "/nonexistent_dir_xyz", stimf, histf, str(SESS)],
                               capture_output=True, cwd=HERE)
        elif name == "bad-name":
            p = subprocess.run([BIN, FIX, "../evil", histf, str(SESS)],
                               capture_output=True, cwd=HERE)
        elif name == "missing-stimulus":
            p = subprocess.run([BIN, FIX, "no_such_stim.bin", histf, str(SESS)],
                               capture_output=True, cwd=HERE)
        elif name == "empty-stimulus":
            p = subprocess.run([BIN, FIX, "stim_empty.bin", histf, str(SESS)],
                               capture_output=True, cwd=HERE)
        elif name == "missing-history":
            p = subprocess.run([BIN, FIX, stimf, "no_such_hist.bin", str(SESS)],
                               capture_output=True, cwd=HERE)
        ok = p.returncode == want and len(p.stdout) == 0 and len(p.stderr) > 0
        check(f"iron/{name}", ok,
              f"want={want} got={p.returncode} stdout={len(p.stdout)}B "
              f"stderr={p.stderr[:60]!r}")
    for name, mut, want in muts:
        mp = os.path.join(FIX, f"hist_m_{name}.bin")
        mal_hist(mp, mut)
        rc, out, err = run_teacher("stimulus.txt", f"hist_m_{name}.bin", SESS)
        ok = rc == want and len(out) == 0 and len(err) > 0
        check(f"iron/{name}", ok,
              f"want={want} got={rc} stdout={len(out)}B stderr={err[:60]!r}")
    rc, out, err = run_teacher("stimulus.txt", "hist_badretract.bin", SESS)
    check("iron/bad-retract-target",
          rc == 15 and len(out) == 0 and len(err) > 0, f"got={rc}")

    # ---- 6. §C tripwire ----
    # clean: all four turn-2 streams with their scripted decisions
    hist_decs = {
        "hist_adopt4": [(i, 1, 0, 0, t1[i]["ss"], t1[i]["se"]) for i in range(4)],
        "hist_adopt8": [(i, 1, 0, 0, t1[i]["ss"], t1[i]["se"]) for i in range(8)],
        "hist_reject": [(i, 1, 2, 1, t1[i]["ss"], t1[i]["se"]) for i in range(8)],
        "hist_consol": ([(i, 1, 0, 0, t1[i]["ss"], t1[i]["se"]) for i in range(6)]
                        + [(6, 1, 2, 1, t1[6]["ss"], t1[6]["se"]),
                           (7, 1, 2, 1, t1[6]["ss"], t1[6]["se"]),
                           (8, 1, 0, 0, t1[7]["ss"], t1[7]["se"]),
                           (9, 1, 2, 1, t1[7]["ss"], t1[7]["se"]),
                           (10, 1, 2, 1, t1[7]["ss"], t1[7]["se"])]),
    }
    all_clean = True
    for name in ["hist_adopt4", "hist_adopt8", "hist_reject", "hist_consol"]:
        props = phases[name]["_props"]
        decs = {s: (v, r) for (s, k, v, r, a, b) in hist_decs[name]}
        # merge: turn-2 proposals have no decisions yet in this scenario; the
        # monitor runs over prior proposals + decisions (the teacher's past)
        t1props = parse_stream(open(os.path.join(EV, "turn1.out"), "rb").read(),
                               STIM_LEN, expect_sess=SESS, expect_seq0=0)
        fired, code, detail = tripwire(t1props, decs, STIM_LEN)
        fired2, code2, _ = rolling200(t1props, decs, STIM_LEN)
        ok = not fired and not fired2
        all_clean = all_clean and ok
        check(f"tripwire/clean-{name}", ok, f"cumul={detail} rolling200={fired2}")
    # smuggle probe: 200 conf-255 proposals tiling the stimulus, all ADOPT
    smug = []
    for i in range(200):
        a = (i * STIM_LEN) // 200
        b = ((i + 1) * STIM_LEN) // 200
        smug.append(dict(seq=i, kind=1, ss=a, se=b, aux=[], grounds=[],
                         conf=255, length=70))
    decs_smug = {i: (0, 0) for i in range(200)}
    fired, code, detail = tripwire(smug, decs_smug, STIM_LEN)
    check("tripwire/smuggle-fires", fired and code == 1, f"{detail}")
    # vocab-dump probe: one conf-255 proposal covering 50%
    dump = [dict(seq=0, kind=1, ss=0, se=STIM_LEN // 2, aux=[], grounds=[],
                 conf=255, length=70)]
    fired, code, detail = tripwire(dump, {0: (0, 0)}, STIM_LEN)
    check("tripwire/vocab-dump-fires", fired and code == 2, f"{detail}")
    # near-miss: tiled at conf 200 (never 255) -> must NOT fire
    near = [dict(p, conf=200) for p in smug]
    fired, code, detail = tripwire(near, decs_smug, STIM_LEN)
    check("tripwire/near-miss-clean", not fired, f"{detail}")

    # ---- summary ----
    log("")
    log(f"RESULT: {'ALL PASS' if not fails else f'{len(fails)} FAILURES: {fails}'}")
    open(os.path.join(EV, "VERIFY_LOG.txt"), "w").write("\n".join(log_lines) + "\n")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
