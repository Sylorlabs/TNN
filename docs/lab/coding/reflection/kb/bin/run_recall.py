#!/usr/bin/env python3
"""run_recall.py — deterministic plumbing for the KB-RECALL battery.

Does NOT make coding decisions. It: builds kb.dat (3x determinism check),
runs kb_main gen (3x byte-identical check), compiles emitted programs with
the pinned znc, runs frozen vectors, compares to frozen expectations,
runs the gate battery and the A1/A2 ablations, and writes results JSON.
"""
import subprocess, hashlib, json, os, sys, shutil

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
BIN = os.path.join(KB, "bin")
LOG = os.path.join(KB, "hidden_files")
os.makedirs(LOG, exist_ok=True)
os.makedirs(os.path.join(LOG, "gen"), exist_ok=True)

def run(args, **kw):
    return subprocess.run(args, capture_output=True, timeout=kw.get("timeout", 60))

def unesc(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i+1]
            out.append({"n":"\n","t":"\t","\\":"\\"}[n]); i += 2
        else:
            out.append(c); i += 1
    return "".join(out)

def load_specs():
    gens, gates = [], []
    for line in open(os.path.join(KB, "tests", "specs.txt")):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        p = line.split("\t")
        if p[0] == "GEN":
            _, sid, spec, argvf, expf, sef = p
            # "<E>" marks an intentionally-empty single argument
            argv = [unesc(a) if a != "<E>" else "" for a in argvf.split("|")] if argvf else []
            se = None
            if sef != "-":
                _, path, content = sef.split(":", 2)
                se = ("FILE", path, unesc(content))
            gens.append({"id": sid, "spec": spec, "argv": argv,
                         "expected": unesc(expf).encode(), "se": se})
        else:
            _, sid, spec, exp = p
            gates.append({"id": sid, "spec": spec, "expected": exp})
    return gens, gates

def entries_without(drop_id):
    """Return entries.txt text with the record `drop_id` removed (for ablations)."""
    txt = open(os.path.join(KB, "data", "entries.txt")).read()
    lines = txt.split("\n")
    out, skip, cur = [], False, None
    for ln in lines:
        if ln.startswith("@") and not ln.startswith("@end"):
            cur = ln[1:]
            skip = (cur == drop_id)
        if not skip:
            out.append(ln)
        if ln == "@end":
            skip = False
    return "\n".join(out)

def main():
    gens, gates = load_specs()
    res = {"install": {}, "gen": [], "gate": [], "ablation": {}}

    kb_install = os.path.join(BIN, "kb_install")
    kb_main = os.path.join(BIN, "kb_main")
    assert os.path.exists(kb_install) and os.path.exists(kb_main), "run bin/build.sh first"

    # ---- install determinism: 3 runs ----
    digests, hashes = [], []
    for r in range(3):
        p = run([kb_install, os.path.join(KB, "data", "entries.txt"),
                 os.path.join(LOG, "kb.dat")])
        assert p.returncode == 0, p.stderr.decode()
        line = p.stdout.decode().strip()
        digests.append(line)
        h = hashlib.sha256(open(os.path.join(LOG, "kb.dat"), "rb").read()).hexdigest()
        hashes.append(h)
    res["install"] = {
        "runs": 3,
        "stdout_identical": len(set(digests)) == 1,
        "kbdat_identical": len(set(hashes)) == 1,
        "digest_line": digests[0],
        "sha256": hashes[0],
    }
    kbdat = os.path.join(LOG, "kb.dat")

    # ---- fixtures for fileread ----
    open("/tmp/kb_f1.bin", "wb").write(b"0123456789abcdef")
    open("/tmp/kb_f2.bin", "wb").write(b"")
    open("/tmp/kb_f3.bin", "wb").write(b"Q" * 100000)
    for t in ("/tmp/kb_r1.txt", "/tmp/kb_r2.txt", "/tmp/kb_r3.txt"):
        if os.path.exists(t):
            os.remove(t)

    # ---- generation battery ----
    n_compile_ok = n_pass = 0
    for g in gens:
        rec = {"id": g["id"], "spec": g["spec"]}
        outs = []
        for r in range(3):
            p = run([kb_main, "gen", kbdat, g["spec"]])
            outs.append(p.stdout)
        rec["gen_deterministic"] = len(set(outs)) == 1
        rec["gen_bytes"] = len(outs[0])
        src = outs[0]
        if b"KB-MISS" in src or p.returncode != 0:
            rec["verdict"] = "FAIL"
            rec["reason"] = src.decode(errors="replace").strip()[:200]
            res["gen"].append(rec)
            continue
        # family from header comment
        first = src.split(b"\n", 1)[0].decode(errors="replace")
        rec["family"] = first.split("family=")[1].split()[0] if "family=" in first else "?"
        zag_path = os.path.join(LOG, "gen", g["id"] + ".zag")
        bin_path = os.path.join(LOG, "gen", g["id"] + ".bin")
        open(zag_path, "wb").write(src)
        c = run([ZNC, zag_path, "-o", bin_path, "--no-analyze"])
        rec["compile_rc"] = c.returncode
        if c.returncode != 0:
            rec["verdict"] = "FAIL"
            rec["reason"] = "compile: " + (c.stdout.decode() + c.stderr.decode())[:300]
            res["gen"].append(rec)
            continue
        n_compile_ok += 1
        r = run([bin_path] + g["argv"])
        ok = (r.stdout == g["expected"])
        rec["stdout_match"] = ok
        if not ok:
            rec["got"] = r.stdout[:200].decode(errors="replace")
            rec["want"] = g["expected"][:200].decode(errors="replace")
        se_ok = True
        if g["se"] is not None:
            _, path, content = g["se"]
            try:
                actual = open(path, "rb").read()
            except FileNotFoundError:
                actual = None
            se_ok = (actual == content.encode())
            rec["side_effect_match"] = se_ok
            if not se_ok:
                rec["se_got"] = None if actual is None else actual[:100].decode(errors="replace")
        rec["verdict"] = "PASS" if (ok and se_ok) else "FAIL"
        if rec["verdict"] == "PASS":
            n_pass += 1
        else:
            rec["reason"] = "output/side-effect mismatch"
        res["gen"].append(rec)

    res["compile_success_rate"] = [n_compile_ok, len(gens)]
    res["test_pass_rate"] = [n_pass, len(gens)]

    # ---- gate battery ----
    for gt in gates:
        p = run([kb_main, "gate", kbdat, gt["spec"]])
        got = p.stdout.decode().strip()
        want = gt["expected"]
        ok = got.startswith(want)
        res["gate"].append({"id": gt["id"], "got": got[:80], "want": want,
                            "verdict": "PASS" if ok else "FAIL"})

    # ---- ablations ----
    for aid, drop in (("A1", "E-FILEWRITE"), ("A2", "L-SYSCALL-NUMS")):
        vtxt = os.path.join(LOG, "entries_%s.txt" % aid)
        vdat = os.path.join(LOG, "kb_%s.dat" % aid)
        open(vtxt, "w").write(entries_without(drop))
        p = run([kb_install, vtxt, vdat])
        w1 = [g for g in gens if g["id"] == "w1"][0]
        q = run([kb_main, "gen", vdat, w1["spec"]])
        out = q.stdout.decode(errors="replace")
        first = out.split("\n", 1)[0]
        res["ablation"][aid] = {
            "dropped": drop,
            "gen_first_line": first[:160],
            "kb_miss": "KB-MISS" in out,
        }

    json.dump(res, open(os.path.join(LOG, "recall_results.json"), "w"), indent=1)

    # ---- console summary ----
    print("install: entries digest: %s" % res["install"]["digest_line"])
    print("install: 3-run stdout identical: %s, kb.dat identical: %s (%s)" % (
        res["install"]["stdout_identical"], res["install"]["kbdat_identical"],
        res["install"]["sha256"][:16]))
    print()
    print("%-4s %-12s %-5s %-4s %-4s %s" % ("id", "family", "det", "cc", "pass", "note"))
    for r in res["gen"]:
        print("%-4s %-12s %-5s %-4s %-4s %s" % (
            r["id"], r.get("family", "?"), "Y" if r["gen_deterministic"] else "n",
            "Y" if r.get("compile_rc") == 0 else "n",
            r["verdict"], r.get("reason", "")))
    print()
    print("compile success: %d/%d   test pass: %d/%d" % (
        res["compile_success_rate"][0], res["compile_success_rate"][1],
        res["test_pass_rate"][0], res["test_pass_rate"][1]))
    print("gate: %s" % ", ".join("%s=%s" % (g["id"], g["verdict"]) for g in res["gate"]))
    for aid, a in res["ablation"].items():
        print("%s (drop %s): kb_miss=%s :: %s" % (aid, a["dropped"], a["kb_miss"], a["gen_first_line"]))

if __name__ == "__main__":
    main()
