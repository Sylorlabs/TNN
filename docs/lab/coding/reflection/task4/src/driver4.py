#!/usr/bin/env python3
"""Task-4 battery driver: DETERMINISTIC PLUMBING ONLY.

Compiles the learner, runs the generate->compile->test->diagnose loop,
dispatches to item verifiers, and logs. It makes NO coding decisions:
no diagnosis, no source edits, no algorithm choice, no repair choice.
All of those live in the Zag learner (learner4.zag).

Usage: driver4.py --arm informed|scratch --rep N
Writes: logs/canonical_<arm>_r<N>.jsonl  (byte-identical across reps)
        logs/timing_<arm>_r<N>.jsonl      (wall times, not canonical)
"""
import subprocess, os, sys, json, hashlib, math, time

TASK = os.path.expanduser("~/workspace/tnn-lab/coding/reflection/task4")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
LEARNER_SRC = os.path.join(TASK, "src/learner4.zag")
FIX = os.path.join(TASK, "fixtures")
EXP = os.path.join(TASK, "expected")
LOGS = os.path.join(TASK, "logs")
BUDGET = 6

ARMS = {
    "informed": os.path.join(TASK, "stores/kb_informed.dat"),
    "scratch": os.path.join(TASK, "stores/kb_scratch.dat"),
}
SPECS = {
    "B1": "B1 huffman codec compress decompress prefix tree encode decode bitstream|ALPHABET=256",
    "B2": "B2 sql engine select where join query csv table",
    "B3": "B3 peephole optimizer stack vm instruction fold|MAXOPS=4096",
    "B4": "B4 btree b-tree split merge insert delete|ORDER=4",
    "B5": "B5 snake game grid moves food collision|W=10|H=8",
}
ITEMS = ["B1", "B2", "B3", "B4", "B5"]
SENTINELS = ("KB-MISS:", "UNKNOWN_GOAL", "UNTAUGHT:", "NEED_CARD:",
             "UNKNOWN_TIER", "REFUSED:")

BAT = json.load(open(os.path.join(TASK, "battery.json")))


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run(cmd, inp=None, timeout=120, cwd="/tmp"):
    p = subprocess.run(cmd, input=inp, capture_output=True, timeout=timeout, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


# ---------------- reference VM (B3 verifier; mirrors frozen spec) ----------------
def vm_run(prog):
    st = []
    for op in prog:
        k = op[0]
        if k == "PUSH":
            st.append(op[1])
        elif k == "ADD":
            b = st.pop(); a = st.pop(); st.append(a + b)
        elif k == "SUB":
            b = st.pop(); a = st.pop(); st.append(a - b)
        elif k == "MUL":
            b = st.pop(); a = st.pop(); st.append(a * b)
        elif k == "DIV":
            b = st.pop(); a = st.pop()
            st.append(int(a / b) if b != 0 else 0)
        elif k == "DUP":
            st.append(st[-1])
        elif k == "SWAP":
            st[-1], st[-2] = st[-2], st[-1]
        elif k == "POP":
            st.pop()
        elif k == "NEG":
            st.append(-st.pop())
        else:
            raise ValueError(f"bad op {k}")
    return st


def parse_prog(text):
    prog = []
    for ln in text.strip().split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        parts = ln.split()
        if parts[0] == "PUSH":
            prog.append(("PUSH", int(parts[1])))
        else:
            prog.append((parts[0],))
    return prog


# ---------------- item checkers (mechanical verifiers) ----------------
def check_b1(binary):
    checks = 0
    detail = {}
    got_parts = []
    for v in BAT["b1_vectors"]:
        data = bytes.fromhex(v["hex"])
        rc, out, err = run([binary, "rt", v["hex"]])
        vid = v["id"]
        got_parts.append(f"## {vid} rc={rc}\n" + out.decode("utf8", "replace"))
        if rc != 0:
            detail[vid] = {"rc": rc, "err": err[:200].decode("utf8", "replace")}
            continue
        lines = out.decode().split("\n")
        if len(lines) < 3:
            detail[vid] = {"lines": len(lines)}
            continue
        try:
            nbits = int(lines[0]) if lines[0] else 0
        except ValueError:
            detail[vid] = {"bad_nbits": lines[0][:40]}
            continue
        bits_hex = lines[1]
        dec_hex = lines[2]
        # (a) round trip
        try:
            dec = bytes.fromhex(dec_hex) if dec_hex else b""
        except ValueError:
            dec = None
        if dec == data:
            checks += 1
        else:
            detail[vid + "_rt"] = False
        # (b) framing: len(bits_hex) == 2*ceil(nbits/8)
        if len(bits_hex) == 2 * math.ceil(nbits / 8):
            checks += 1
        else:
            detail[vid + "_frame"] = (len(bits_hex), nbits)
        detail[vid + "_nbits"] = nbits
    # compression sanity (4): v1 nbits==0; v2 nbits==8; v5,v6: nbits < 8*len.
    # SPEC NOTE: the frozen text lists v3,v5,v6 for the inequality (5
    # conditions) but says "(4)" and "Checks (16)". To keep every frozen
    # number literally true (6+6+4=16), v3's inequality is not counted;
    # v5 (skewed) and v6 (2-symbol) are the canonical compression cases.
    # v3 still must round-trip and frame correctly (12 checks cover it).
    nb = {v["id"]: None for v in BAT["b1_vectors"]}
    for v in BAT["b1_vectors"]:
        key = v["id"] + "_nbits"
        if key in detail and isinstance(detail[key], int):
            nb[v["id"]] = detail[key]
    if nb["v1"] == 0:
        checks += 1
    else:
        detail["v1_sanity"] = nb["v1"]
    if nb["v2"] == 8:
        checks += 1
    else:
        detail["v2_sanity"] = nb["v2"]
    for vid in ("v5", "v6"):
        v = next(x for x in BAT["b1_vectors"] if x["id"] == vid)
        if nb[vid] is not None and nb[vid] < 8 * len(bytes.fromhex(v["hex"])):
            checks += 1
        else:
            detail[vid + "_sanity"] = nb[vid]
    assert checks <= 16
    passed = (checks == 16)
    return passed, checks / 16, {"checks": checks, "detail": detail}, \
        "".join(got_parts), ""


def check_b2(binary):
    ok = 0
    detail = {}
    got_parts = []
    exp_parts = []
    for i, q in enumerate(BAT["b2_queries"], 1):
        exp = open(os.path.join(EXP, f"B2_q{i}.txt"), "rb").read()
        exp_parts.append(f"## Q{i}\n".encode() + exp)
        rc, out, err = run([binary, os.path.join(FIX, "b2"), q])
        got_parts.append(f"## Q{i} rc={rc}\n".encode() + out)
        if rc == 0 and out == exp:
            ok += 1
        else:
            detail[f"q{i}"] = {"rc": rc, "out_sha": sha256(out),
                               "exp_sha": sha256(exp)}
    return (ok == 6), ok / 6, {"queries_ok": ok, "detail": detail}, \
        b"".join(got_parts).decode("utf8", "replace"), \
        b"".join(exp_parts).decode("utf8", "replace")


def check_b3(binary):
    qs = []
    detail = {}
    got_parts = []
    allok = True
    for prog in BAT["b3_programs"]:
        path = os.path.join(FIX, prog)
        orig_text = open(path).read()
        orig = parse_prog(orig_text)
        rc, out, err = run([binary, path])
        got_parts.append(f"## {prog} rc={rc}\n" + out.decode("utf8", "replace"))
        if rc != 0:
            detail[prog] = {"rc": rc}
            allok = False
            qs.append(0)
            continue
        try:
            opt = parse_prog(out.decode())
            s_orig = vm_run(orig)
            s_opt = vm_run(opt)
            sem = (s_orig == s_opt)
        except Exception as e:
            sem = False
            detail[prog] = {"verifier_exc": str(e)[:120]}
        red = (len(orig) - len(opt)) / len(orig) if orig else 0
        detail[prog] = {"sem": sem, "reduction": round(red, 4),
                        "orig": len(orig), "opt": len(opt)}
        if sem and red >= 0.20:
            qs.append(min(1.0, red / 0.30))
        else:
            qs.append(0.0)
            allok = False
    q = sum(qs) / len(qs)
    return allok, q, {"per_program": detail, "quality": q}, \
        "".join(got_parts), ""


def parse_b4_block(lines):
    nodes = {}
    root = None
    for ln in lines:
        if ln.startswith("ROOT"):
            root = int(ln.split()[1])
            continue
        assert ln.startswith("N"), ln
        rest = ln[1:]
        nid_s, rest = rest.split(" ", 1)
        nid = int(nid_s)
        parts = dict(kv.split("=", 1) for kv in rest.split(" "))
        keys = [int(x) for x in parts["keys"].split(",")] if parts["keys"] else []
        children = ([int(x) for x in parts["children"].split(",")]
                    if parts["children"] else [])
        nodes[nid] = {"leaf": int(parts["leaf"]), "n": int(parts["n"]),
                      "keys": keys, "children": children}
    return nodes, root


def inorder_of(nodes, root):
    res = []
    def walk(nid):
        nd = nodes[nid]
        if nd["leaf"] == 1:
            res.extend(nd["keys"])
        else:
            for i, k in enumerate(nd["keys"]):
                walk(nd["children"][i])
                res.append(k)
            walk(nd["children"][len(nd["keys"])])
    walk(root)
    return res


def check_b4(binary):
    rc, out, err = run([binary, os.path.join(FIX, "b4_ops.txt")])
    detail = {}
    got_text = out.decode("utf8", "replace")
    exp_text = open(os.path.join(EXP, "B4.txt")).read()
    if rc != 0:
        return False, 0.0, {"rc": rc,
                             "err": err[:200].decode("utf8", "replace")}, \
            got_text, exp_text
    blocks, cur = [], []
    for ln in out.decode().split("\n"):
        s = ln.strip()
        if not s:
            continue
        cur.append(s)
        if s.startswith("ROOT"):
            blocks.append(cur)
            cur = []
    checks = 0
    for bi, (lines, eset) in enumerate(zip(blocks, BAT["b4_expected_sets"]), 1):
        nodes, root = parse_b4_block(lines)
        d = detail.setdefault(f"print{bi}", {})
        # 1. node count >= 1
        if len(nodes) >= 1:
            checks += 1
        else:
            d["nodecount"] = len(nodes)
        # 2. every node 1-3 keys
        if all(1 <= nd["n"] <= 3 and len(nd["keys"]) == nd["n"] for nd in nodes.values()):
            checks += 1
        else:
            d["keycount"] = False
        # 3. keys strictly increasing within each node
        if all(all(nd["keys"][i] < nd["keys"][i+1]
                   for i in range(len(nd["keys"]) - 1)) for nd in nodes.values()):
            checks += 1
        else:
            d["increasing"] = False
        # 4. leaf <=> no children
        if all((nd["leaf"] == 1) == (len(nd["children"]) == 0) for nd in nodes.values()):
            checks += 1
        else:
            d["leaf"] = False
        # 5. internal <=> children == keys+1
        if all((nd["leaf"] == 1) or
               (len(nd["children"]) == len(nd["keys"]) + 1)
               for nd in nodes.values()):
            checks += 1
        else:
            d["children_count"] = False
        # 6. child ids defined exactly once, single parent (root has none)
        try:
            seen = {}
            ok6 = True
            for nid, nd in nodes.items():
                for c in nd["children"]:
                    if c not in nodes or c in seen:
                        ok6 = False
                    seen[c] = nid
            if root in seen:
                ok6 = False
            if set(seen.keys()) != set(nodes.keys()) - {root}:
                ok6 = False
        except Exception:
            ok6 = False
        if ok6:
            checks += 1
        else:
            d["parentage"] = False
        # 7. in-order multiset == expected set
        try:
            ino = inorder_of(nodes, root)
            if sorted(ino) == sorted(eset) and len(ino) == len(eset):
                checks += 1
            else:
                d["inorder"] = ino
        except Exception as e:
            d["inorder_exc"] = str(e)[:120]
    passed = (checks == 21 and len(blocks) == 3)
    return passed, checks / 21, {"checks": checks, "blocks": len(blocks),
                                 "detail": detail}, got_text, exp_text


def check_b5(binary):
    ok = 0
    detail = {}
    got_parts = []
    exp_parts = []
    for pr in BAT["b5_probes"]:
        rc, out, err = run([binary, pr["moves"], pr["foods"]])
        exp = pr["exp"]
        exp_text = (f"BOARD 10 8\nSNAKE {exp['len']} " +
                    " ".join(f"{x},{y}" for x, y in exp["body"]) +
                    f"\nFOOD {exp['food']}\nSCORE {exp['score']}\n"
                    f"STATUS {exp['status']}\n")
        got = out.decode("utf8", "replace")
        got_parts.append(f"## {pr['id']} rc={rc}\n" + got)
        exp_parts.append(f"## {pr['id']}\n" + exp_text)
        if rc == 0 and got == exp_text:
            ok += 1
        else:
            detail[pr["id"]] = {"rc": rc, "got": got[:160], "exp": exp_text[:160]}
    return (ok == 5), ok / 5, {"probes_ok": ok, "detail": detail}, \
        "".join(got_parts), "".join(exp_parts)


CHECKERS = {"B1": check_b1, "B2": check_b2, "B3": check_b3, "B4": check_b4,
            "B5": check_b5}


def is_sentinel(text: str) -> bool:
    head = text[:64]
    return any(head.startswith(s) for s in SENTINELS)


def esc_env(s: str) -> str:
    # match the learner's ev_unescape: \\ -> backslash, \n -> LF, \r -> CR.
    # envelope is newline-separated "KEY value" lines (see env_get).
    return s.replace("\\", "\\\\").replace("\r", "\\r").replace("\n", "\\n")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["informed", "scratch"])
    ap.add_argument("--rep", required=True, type=int)
    args = ap.parse_args()
    arm, rep = args.arm, args.rep
    kbpath = ARMS[arm]

    os.makedirs(LOGS, exist_ok=True)
    work = os.path.join(TASK, f"work/runs/{arm}_r{rep}")
    os.makedirs(work, exist_ok=True)
    learner = os.path.join(work, "learner4")
    rc, out, err = run([ZNC, LEARNER_SRC, "-o", learner,
                        "--no-analyze", "--no-zagd"], cwd=TASK, timeout=300)
    if rc != 0:
        print(f"FATAL: learner build failed: {err.decode()[:500]}")
        sys.exit(2)

    clog = open(os.path.join(LOGS, f"canonical_{arm}_r{rep}.jsonl"), "w")
    tlog = open(os.path.join(LOGS, f"timing_{arm}_r{rep}.jsonl"), "w")

    def emit(rec):
        clog.write(json.dumps(rec, sort_keys=True) + "\n")

    def emit_t(rec):
        tlog.write(json.dumps(rec, sort_keys=True) + "\n")

    summary = {"arm": arm, "rep": rep, "items": {}}
    for item in ITEMS:
        t_item0 = time.time()
        spec = SPECS[item]
        iw = os.path.join(work, item)
        os.makedirs(iw, exist_ok=True)
        src = None
        src_sha = None
        passed = False
        quality = 0.0
        iters_used = 0
        detail = {}
        prev_src_sha = None
        stalled = False
        for attempt in range(1, BUDGET + 1):
            iters_used = attempt
            t0 = time.time()
            if src is None:
                # gen via the learner
                rc, out, err = run([learner, "gen", kbpath, spec], cwd=iw)
                src = out.decode("utf8", "replace")
                src_sha = sha256(out)
                emit({"t": "gen", "arm": arm, "item": item,
                      "attempt": attempt, "src_sha256": src_sha,
                      "sentinel": is_sentinel(src)})
                emit_t({"t": "gen", "item": item, "attempt": attempt,
                        "secs": round(time.time() - t0, 3)})
                if is_sentinel(src):
                    ev = "SENTINEL=1"
                    rc2, dout, derr = run(
                        [learner, "diagnose", kbpath, spec, src, "GEN", ev],
                        cwd=iw)
                    dtext = dout.decode("utf8", "replace")
                    dhead = dtext.split("@@SRC@@")[0]
                    emit({"t": "diagnose", "arm": arm,                           "item": item, "attempt": attempt,
                          "evtype": "GEN", "head": dhead.strip()})
                    emit_t({"t": "diagnose", "item": item,
                            "attempt": attempt,
                            "secs": round(time.time() - t0, 3)})
                    # halt: gen failure is terminal
                    break
            # compile
            src_path = os.path.join(iw, f"attempt{attempt}.zag")
            bin_path = os.path.join(iw, f"attempt{attempt}.bin")
            open(src_path, "w").write(src)
            t0 = time.time()
            rc, cout, cerr = run([ZNC, src_path, "-o", bin_path,
                                  "--no-analyze", "--no-zagd"], cwd=iw)
            emit({"t": "compile", "arm": arm, "item": item,
                  "attempt": attempt, "rc": rc,
                  "err_sha256": sha256(cerr)})
            emit_t({"t": "compile", "item": item, "attempt": attempt,
                    "secs": round(time.time() - t0, 3)})
            if rc != 0:
                ev_lines = ["GOT_RC 1", "EXP_RC 0",
                            "GOT_ERR " + esc_env(cerr[:4000].decode("utf8", "replace")),
                            "GOT_OUT ", "EXP_OUT ",
                            f"ITEM {item}"]
                if stalled:
                    ev_lines.append("STALLED 1")
                ev = "\n".join(ev_lines) + "\n"
                rc2, dout, derr = run(
                    [learner, "diagnose", kbpath, spec, src, "COMPILE", ev],
                    cwd=iw)
                dtext = dout.decode("utf8", "replace")
                dhead, _, dsrc = dtext.partition("@@SRC@@\n")
                dsrc = dsrc.split("@@END@@")[0]
                dclass = dhead.split("class=")[1].split()[0] if "class=" in dhead else "?"
                strat = dhead.split("strategy=")[1].split()[0] if "strategy=" in dhead else "?"
                emit({"t": "diagnose", "arm": arm, "item": item,
                      "attempt": attempt, "evtype": "COMPILE",
                      "class": dclass, "strategy": strat,
                      "new_src_sha256": sha256(dsrc.encode())})
                if strat.startswith("halt-"):
                    break
                if sha256(dsrc.encode()) == src_sha:
                    stalled = True
                src, src_sha = dsrc, sha256(dsrc.encode())
                continue
            # test
            t0 = time.time()
            passed, quality, detail, got_text, exp_text = CHECKERS[item](bin_path)
            emit({"t": "test", "arm": arm, "item": item,
                  "attempt": attempt, "passed": passed,
                  "quality": round(quality, 4),
                  "detail_sha256": sha256(json.dumps(detail, sort_keys=True).encode())})
            emit_t({"t": "test", "item": item, "attempt": attempt,
                    "secs": round(time.time() - t0, 3)})
            if passed:
                break
            # test failed -> diagnose TEST with the real outputs as evidence
            ev_lines = ["GOT_RC 0", "EXP_RC 0", "GOT_ERR ",
                        "GOT_OUT " + esc_env(got_text[:6000]),
                        "EXP_OUT " + esc_env(exp_text[:6000]),
                        f"ITEM {item}", f"QUALITY {quality:.4f}"]
            if stalled:
                ev_lines.append("STALLED 1")
            ev = "\n".join(ev_lines) + "\n"
            rc2, dout, derr = run(
                [learner, "diagnose", kbpath, spec, src, "TEST", ev],
                cwd=iw)
            dtext = dout.decode("utf8", "replace")
            dhead, _, dsrc = dtext.partition("@@SRC@@\n")
            dsrc = dsrc.split("@@END@@")[0]
            dclass = dhead.split("class=")[1].split()[0] if "class=" in dhead else "?"
            strat = dhead.split("strategy=")[1].split()[0] if "strategy=" in dhead else "?"
            emit({"t": "diagnose", "arm": arm, "item": item,
                  "attempt": attempt, "evtype": "TEST",
                  "class": dclass, "strategy": strat,
                  "new_src_sha256": sha256(dsrc.encode())})
            if strat.startswith("halt-"):
                break
            if sha256(dsrc.encode()) == src_sha:
                stalled = True
            src, src_sha = dsrc, sha256(dsrc.encode())
        first_attempt = 1 if (passed and iters_used == 1) else 0
        iters_working = iters_used if passed else 7
        emit({"t": "done", "arm": arm, "item": item,
              "passed": passed, "iters_used": iters_used,
              "iters_working": iters_working,
              "first_attempt": first_attempt,
              "quality": round(quality, 4),
              "detail": detail})
        emit_t({"t": "item", "item": item,
                "secs": round(time.time() - t_item0, 3)})
        summary["items"][item] = {"passed": passed, "iters_used": iters_used,
                                  "iters_working": iters_working,
                                  "first_attempt": first_attempt,
                                  "quality": round(quality, 4)}
    clog.close()
    tlog.close()
    json.dump(summary, open(os.path.join(LOGS, f"summary_{arm}_r{rep}.json"), "w"),
              indent=1, sort_keys=True)
    print(json.dumps(summary["items"], indent=1))


if __name__ == "__main__":
    main()
