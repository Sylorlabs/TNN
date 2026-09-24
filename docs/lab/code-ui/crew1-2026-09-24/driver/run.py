#!/usr/bin/env python3
"""Driver for T1 guided-learning: teaching run and B1 battery.
Orchestration only. All teaching/authoring/revision DECISIONS are made by
the pure-Zag bin/learn binary (teach/compose/revise modes). This script
only: runs processes, writes files, invokes tsc/node, applies LEARN lines
to cards during teaching, and records metrics.

Usage: run.py teach | b1 <rundir>
"""
import os, re, subprocess, sys, shutil, json

ROOT = os.path.expanduser("~/workspace/code-ui/ts-teaching")
LEARN = ROOT + "/bin/learn"
TSC = ROOT + "/node_modules/.bin/tsc"
SHIM = ROOT + "/src/domshim.js"
CARDS = ROOT + "/cards"
MAXREV = 5

SECTIONS = ["PARAMS:", "LIBPARAMS:", "MAINPARAMS:", "TESTS:", "EXPECT:"]
ENDS = {"PARAMS:": "ENDPARAMS", "LIBPARAMS:": "ENDPARAMS", "MAINPARAMS:": "ENDPARAMS",
        "TESTS:": "ENDTESTS", "EXPECT:": "ENDEXPECT"}


def parse_task(path):
    txt = open(path).read()
    lines = txt.split("\n")
    hdr, secs, cur, buf = {}, {}, None, []
    for ln in lines:
        if ln in SECTIONS:
            cur, buf = ln[:-1], []
            continue
        if cur and ln == ENDS[cur + ":"]:
            secs[cur] = "\n".join(buf)
            cur = None
            continue
        if cur:
            buf.append(ln)
        elif "=" in ln and re.match(r"^[A-Za-z0-9_-]+=", ln):
            k, v = ln.split("=", 1)
            hdr[k] = v
    return hdr, secs


def curriculum_units():
    units = []
    for ln in open(ROOT + "/curriculum.txt"):
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        units.append(ln.split()[0])
    return units


def find_card_file(unit, tpl, units):
    """Installed-card retrieval, decided by the pure-Zag mechanism.

    Delegates to `bin/learn findcard`, which implements the frozen policy:
    the unit's own card first, then the remaining installed cards in
    curriculum order, matching a full `## TPL <tpl>` line. Returns the
    card filename (e.g. "U3-interfaces.card") or None when no installed
    card holds the template. Deterministic; byte-identical across reruns.
    """
    p = subprocess.run(
        [LEARN, "findcard", unit, tpl, CARDS, ROOT + "/curriculum.txt"],
        capture_output=True, text=True, cwd=ROOT)
    if p.returncode != 0:
        return None
    return (p.stdout or "").strip() or None


def write_blocks(stdout_txt, wd):
    """Parse @@FILE blocks from learn stdout into the workdir. Returns filenames."""
    names = []
    for m in re.finditer(r"@@FILE (\S+)\n(.*?)@@END", stdout_txt, re.S):
        fn, body = m.group(1), m.group(2)
        open(os.path.join(wd, fn), "w").write(body)
        names.append(fn)
    return names


def run_tsc(wd, ts_files):
    outdir = os.path.join(wd, "out")
    os.makedirs(outdir, exist_ok=True)
    cmd = [TSC, "--strict", "--target", "es2020", "--module", "commonjs",
           "--moduleResolution", "node", "--outDir", outdir] + ts_files
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    diag = (p.stdout or "") + (p.stderr or "")
    open(os.path.join(wd, "tsc.err"), "w").write(diag)
    return diag


def run_node(wd, hdr, secs, ts_files):
    """Execute the compiled program. Returns stdout."""
    outdir = os.path.join(wd, "out")
    if hdr.get("FILES") == "multi":
        p = subprocess.run(["node", os.path.join(outdir, "main.js")],
                           capture_output=True, text=True, cwd=ROOT, timeout=30)
        return p.stdout, p.stderr, p.returncode
    parts = []
    if hdr.get("NEEDS-DOM") == "1":
        parts.append(open(SHIM).read())
    for f in ts_files:
        js = os.path.join(outdir, os.path.splitext(os.path.basename(f))[0] + ".js")
        parts.append(open(js).read())
    runner = os.path.join(wd, "runner.js")
    open(runner, "w").write("\n".join(parts))
    p = subprocess.run(["node", runner], capture_output=True, text=True,
                       cwd=ROOT, timeout=30)
    return p.stdout, p.stderr, p.returncode


def norm(s):
    return "\n".join(ln.rstrip() for ln in s.strip().split("\n"))


def apply_learn(unit, kv):
    """Append key=value to the unit card's ## LEARNED section (teaching only)."""
    k, v = kv.split("=", 1)
    cf = CARDS + "/" + unit + ".card"
    txt = open(cf).read()
    if re.search(r"(?m)^" + re.escape(k) + r"=", txt):
        return "dup"
    txt = txt.replace("## LEARNED\n", "## LEARNED\n" + k + "=" + v + "\n", 1)
    open(cf, "w").write(txt)
    return "added"


def solve(task_id, task_path, phase_dir, units, frozen):
    hdr, secs = parse_task(task_path)
    unit = hdr["UNIT"]
    wd = os.path.join(phase_dir, task_id)
    if os.path.exists(wd):
        shutil.rmtree(wd)
    os.makedirs(wd)
    rec = {"id": task_id, "unit": unit, "tpl": hdr.get("TPL"),
           "revisions": 0, "fixes": [], "learned": [], "errors": []}
    # 1. compose from installed cards only
    tplname = hdr.get("TPL") if hdr.get("FILES") != "multi" else None
    cardfile = None
    if hdr.get("FILES") == "multi":
        cardfile = find_card_file(unit, hdr["LIBTPL"], units)
    else:
        cardfile = find_card_file(unit, hdr["TPL"], units)
    if cardfile is None:
        rec["outcome"] = "CARD-MISSING"
        rec["note"] = "no installed card holds the template; manual consultation would be needed (forbidden)"
        return rec
    rec["card"] = cardfile
    args = [LEARN, "compose", task_path, CARDS]
    if cardfile != unit + ".card":
        args.append(cardfile)  # transfer probe: template in another installed card
        rec["transfer"] = True
    p = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    open(os.path.join(wd, "compose.err"), "w").write(p.stderr or "")
    if p.returncode != 0:
        rec["outcome"] = "COMPOSE-FAIL"
        rec["note"] = (p.stderr or "").strip()
        return rec
    ts_files = [os.path.join(wd, f) for f in write_blocks(p.stdout, wd)]
    if hdr.get("FILES") != "multi" and secs.get("TESTS") is not None:
        tp = os.path.join(wd, "tests.ts")
        open(tp, "w").write(secs.get("TESTS", ""))
        ts_files.append(tp)
    # 2. compile / revise loop
    while True:
        diag = run_tsc(wd, ts_files)
        if "error TS" not in diag:
            break
        if rec["revisions"] >= MAXREV:
            rec["outcome"] = "REVISION-BUDGET-EXCEEDED"
            return rec
        first = [ln for ln in diag.split("\n") if "error TS" in ln]
        rec["errors"].append(first[0].strip() if first else "?")
        rp = subprocess.run(
            [LEARN, "revise", wd, os.path.join(wd, "tsc.err"), CARDS, unit],
            capture_output=True, text=True, cwd=ROOT)
        for ln in (rp.stderr or "").split("\n"):
            if ln.startswith("FIX "):
                rec["fixes"].append(ln[4:])
            elif ln.startswith("LEARN "):
                m = re.match(r"LEARN unit=(\S+) (\S+)", ln)
                if m:
                    rec["learned"].append({"unit": m.group(1), "kv": m.group(2)})
                    if not frozen:
                        apply_learn(m.group(1), m.group(2))
        if rp.returncode != 0:
            rec["outcome"] = "NOFIX"
            rec["note"] = (rp.stderr or "").strip()
            return rec
        write_blocks(rp.stdout, wd)
        rec["revisions"] += 1
    # 3. run and compare
    try:
        out, err, rc = run_node(wd, hdr, secs, ts_files)
    except subprocess.TimeoutExpired:
        rec["outcome"] = "TIMEOUT"
        return rec
    open(os.path.join(wd, "run.out"), "w").write(out)
    expected = norm(secs.get("EXPECT", ""))
    rec["expected"], rec["actual"] = expected, norm(out)
    rec["outcome"] = "PASS" if norm(out) == expected and rc == 0 else "FAIL"
    if rc != 0:
        rec["note"] = "node rc=%d stderr=%s" % (rc, (err or "").strip()[:200])
    return rec


def phase_teach():
    phase_dir = ROOT + "/runlog/teach"
    os.makedirs(phase_dir, exist_ok=True)
    units = curriculum_units()
    # sequence the curriculum; learn prints the one CONSULT per unit
    p = subprocess.run([LEARN, "teach", ROOT + "/curriculum.txt"],
                       capture_output=True, text=True, cwd=ROOT)
    open(phase_dir + "/consult.log", "w").write(p.stdout)
    if p.returncode != 0:
        print("teach failed: " + (p.stderr or ""))
        sys.exit(1)
    practice = {}
    for ln in p.stdout.split("\n"):
        if ln.startswith("PRACTICE task="):
            tf = ln.split("=", 1)[1]
            # unit for this task: from the preceding CONSULT line
            practice[tf] = True
    results = []
    # run practices in curriculum order
    idx = 0
    consult_lines = [ln for ln in p.stdout.split("\n") if ln.startswith("CONSULT")]
    for ln in p.stdout.split("\n"):
        if not ln.startswith("PRACTICE task="):
            continue
        tf = ln.split("=", 1)[1]
        unit = consult_lines[idx].split("unit=")[1].split()[0]
        idx += 1
        rec = solve("practice-" + unit, ROOT + "/practice/" + tf,
                    phase_dir, units, frozen=False)
        results.append(rec)
        print("%s %s rev=%d %s" % (rec["id"], rec["outcome"], rec["revisions"],
                                   "|".join(rec["fixes"])))
    open(phase_dir + "/results.json", "w").write(json.dumps(results, indent=1))
    return results


def phase_b1(rundir):
    phase_dir = ROOT + "/runlog/" + rundir
    os.makedirs(phase_dir, exist_ok=True)
    units = curriculum_units()
    results = []
    for i in range(1, 27):
        tid = "t%02d" % i
        rec = solve(tid, ROOT + "/battery/tasks/" + tid + ".task",
                    phase_dir, units, frozen=True)
        results.append(rec)
        print("%s %s rev=%d %s" % (rec["id"], rec["outcome"], rec["revisions"],
                                   "|".join(rec["fixes"])))
    open(phase_dir + "/results.json", "w").write(json.dumps(results, indent=1))
    # summary
    passes = sum(1 for r in results if r["outcome"] == "PASS")
    revs = sorted(r["revisions"] for r in results)
    median = revs[len(revs) // 2]
    hist = {}
    for r in results:
        for f in r["fixes"]:
            hist[f] = hist.get(f, 0) + 1
    summ = {"pass": passes, "total": len(results),
            "pass_rate": passes / len(results),
            "median_revisions": median,
            "fix_histogram": hist,
            "transfer_tasks": [r["id"] for r in results if r.get("transfer")]}
    open(phase_dir + "/summary.json", "w").write(json.dumps(summ, indent=1))
    print(json.dumps(summ, indent=1))
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: run.py teach | b1 <rundir>")
        sys.exit(1)
    if sys.argv[1] == "teach":
        phase_teach()
    elif sys.argv[1] == "b1":
        phase_b1(sys.argv[2])
    else:
        print("unknown phase")
        sys.exit(1)
