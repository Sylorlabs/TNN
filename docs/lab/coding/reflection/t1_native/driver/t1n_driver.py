#!/usr/bin/env python3
"""T1N invention driver — deterministic plumbing ONLY (prereg §7.2, RK4).

The driver compiles the deliberation engine's queues, runs binaries, and
records rc/stdout/stderr VERBATIM. It makes NO coding or architectural
decision: no branch on the CONTENT of compiler output, test output, or
candidate code. Orchestration branches (file existence, queue emptiness,
loop counters, budget accounting) are allowed.

Budgets are CHECKED and reported, never enforced by truncation: if the
engine exceeds max_compilations the driver keeps compiling, records the
violation, and FAILS the run.

Pipeline per arm:
  teach -> build engine + IV-P0 sweep -> deliberate
  (propose/critique/compose/validate/validate2/diagnose/freeze) ->
  IV-P1/IV-P2 checks -> build wrapper -> Phase-2 battery (N reps) ->
  bar table.

Queue/escape formats: driver/QUEUE_PROTOCOL.md (frozen).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

T1N = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFLECTION = os.path.dirname(T1N)
TASK1 = os.path.join(REFLECTION, "task1")
ZNC = "/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"

KB_ENTRIES_SRC = os.path.join(REFLECTION, "kb", "data", "entries.txt")
CORPUS_SRC = os.path.join(TASK1, "corpus", "records.txt")

# Frozen digests (teach audit compares against these; mismatch => VOID).
# KB entries.txt sha256: recorded in task3/stores/informed.sha256 as
# coding_entries_sha256 and in the kb install audit log (69 entries).
KB_FROZEN_SHA256 = "f7de7f4667878770e1fceb8cd673a277cd1399dd526757c13a1bd87eb691fe96"
# Corpus records.txt sha256: task1/corpus/CORPUS_FREEZE.md.
CORPUS_FROZEN_SHA256 = "3ff512a3367350374c19e6c26615fd4f5547d1bb2353098e2f37bcb30d71c2c7"

MAX_NOVEL_ROUNDS = 3
MAX_BASIC_ROUNDS = 1
MAX_COMPILATIONS = 120
CRITIQUE_LOOP_GUARD = 8

ENGINE_MODES = ["propose", "critique", "compose", "validate", "validate2",
                "diagnose", "freeze"]

# Pinned baseline, prereg §5 (pass counts per tier).
BASELINE = {"T1": (10, 10), "T2": (8, 8), "T3": (10, 10), "T4": (12, 12),
            "T4M": (4, 4), "T4X": (0, 8), "T5": (6, 6)}
TIER_ORDER = ["T1", "T2", "T3", "T4", "T4M", "T4X", "T5"]


class DriverFail(Exception):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def esc(b):
    """Queue-protocol escaping (§3.3): backslash, CR, LF, TAB. ASCII-safe."""
    if b is None:
        b = b""
    t = b.decode("ascii", "backslashreplace")
    t = t.replace("\\", "\\\\").replace("\r", "\\r")
    t = t.replace("\n", "\\n").replace("\t", "\\t")
    return t


def wpath(workdir, *parts):
    return os.path.join(workdir, *parts)


def run(cmd, cwd, timeout):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        return -99, (e.stdout or b""), (e.stderr or b"")


def count_records(path):
    n = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.rstrip("\n") == "@end":
                n += 1
    return n


# ---------------- Phase 0: teach ----------------

def phase0_teach(arm, workdir):
    os.makedirs(workdir, exist_ok=True)
    audit = []
    audit.append("arm=" + arm)

    eh = sha256_file(KB_ENTRIES_SRC)
    shutil.copy(KB_ENTRIES_SRC, wpath(workdir, "entries.txt"))
    n_entries = count_records(wpath(workdir, "entries.txt"))
    audit.append("entries_sha256=" + eh)
    audit.append("entries_frozen=" + KB_FROZEN_SHA256)
    audit.append("entries_count=%d" % n_entries)
    entries_ok = (eh == KB_FROZEN_SHA256) and (n_entries == 69)
    audit.append("entries_match=" + ("yes" if entries_ok else "NO"))

    if arm == "informed":
        ch = sha256_file(CORPUS_SRC)
        shutil.copy(CORPUS_SRC, wpath(workdir, "corpus.txt"))
        n_rec = count_records(wpath(workdir, "corpus.txt"))
        audit.append("corpus_sha256=" + ch)
        audit.append("corpus_frozen=" + CORPUS_FROZEN_SHA256)
        audit.append("corpus_records=%d" % n_rec)
        corpus_ok = (ch == CORPUS_FROZEN_SHA256) and (n_rec == 12)
        audit.append("corpus_match=" + ("yes" if corpus_ok else "NO"))
    else:
        cp = wpath(workdir, "corpus.txt")
        if os.path.exists(cp):
            os.remove(cp)
        audit.append("corpus_present=no (scratch arm: prior-art records withheld)")
        corpus_ok = True

    shutil.copy(os.path.join(T1N, "driver", "probes.txt"),
                wpath(workdir, "probes.txt"))
    audit.append("probes_copied=yes (driver/probes.txt, 8 probes)")

    with open(wpath(workdir, "config.txt"), "w") as f:
        f.write("arm=%s\n" % arm)
        f.write("max_novel_rounds=%d\n" % MAX_NOVEL_ROUNDS)
        f.write("max_basic_rounds=%d\n" % MAX_BASIC_ROUNDS)
        f.write("max_compilations=%d\n" % MAX_COMPILATIONS)
    audit.append("config_written=yes")

    with open(wpath(workdir, "teach_audit.txt"), "w") as f:
        f.write("\n".join(audit) + "\n")

    if not (entries_ok and corpus_ok):
        raise DriverFail("teach VOID: taught file digest mismatch\n" +
                         "\n".join(audit))
    return audit


# ---------------- Phase 1: engine build + IV-P0 ----------------

def phase1_engine(workdir, engine_src, engine_bin_arg):
    if engine_bin_arg:
        engine_bin = engine_bin_arg
        if not (os.path.isfile(engine_bin) and os.access(engine_bin, os.X_OK)):
            raise DriverFail("engine binary not executable: " + engine_bin)
        build_log = "rc=0\nSTDOUT:\n\nSTDERR:\n(external engine binary; build skipped)\n"
    else:
        engine_dir = os.path.dirname(os.path.abspath(engine_src))
        out_dir = wpath(workdir, "engine_bin")
        os.makedirs(out_dir, exist_ok=True)
        # Absolute: znc runs with cwd=engine_dir, so a relative -o path
        # would resolve under the engine dir and fail to write.
        engine_bin = os.path.abspath(wpath(out_dir, "t1n_delib"))
        rc, out, err = run([ZNC, os.path.abspath(engine_src), "-o", engine_bin,
                            "--no-analyze"], cwd=engine_dir, timeout=600)
        build_log = "rc=%d\nSTDOUT:\n%s\nSTDERR:\n%s\n" % (rc, esc(out), esc(err))
        if rc != 0 or not os.path.isfile(engine_bin):
            with open(wpath(workdir, "engine_build.log"), "w") as f:
                f.write(build_log)
            raise DriverFail("engine build failed (rc=%d)" % rc)
    with open(wpath(workdir, "engine_build.log"), "w") as f:
        f.write(build_log)

    sweep = os.path.join(T1N, "driver", "sweep_forbidden.py")
    rc, out, err = run([sys.executable, sweep, os.path.abspath(engine_src)],
                       cwd=T1N, timeout=120)
    ivp0 = "rc=%d\n%s%s" % (rc, out.decode("utf-8", "replace"),
                            err.decode("utf-8", "replace"))
    with open(wpath(workdir, "ivp0_result.txt"), "w") as f:
        f.write(ivp0)
    audits_dir = os.path.join(T1N, "audits")
    os.makedirs(audits_dir, exist_ok=True)
    with open(os.path.join(audits_dir, "ivp0_result.txt"), "w") as f:
        f.write(ivp0)
    if rc != 0:
        raise DriverFail("IV-P0 VOID: forbidden vocabulary in engine source")
    return engine_bin


# ---------------- Phase 2: deliberation ----------------

def run_engine(engine_bin, mode, workdir):
    rc, out, err = run([engine_bin, mode], cwd=workdir, timeout=600)
    with open(wpath(workdir, "engine_%s.log" % mode), "w") as f:
        f.write("rc=%d\nSTDOUT:\n%s\nSTDERR:\n%s\n"
                % (rc, esc(out), esc(err)))
    return rc


def process_compile_queue(workdir):
    q = wpath(workdir, "compile_queue.txt")
    blocks = []
    n = 0
    if os.path.exists(q):
        with open(q, "r", encoding="utf-8", errors="replace") as f:
            qlines = f.read().split("\n")
        for line in qlines:
            p = line.strip()
            if not p:
                continue
            rc, out, err = run([ZNC, p, "-o", p + ".bin", "--no-analyze"],
                               cwd=workdir, timeout=180)
            n += 1
            blocks.append("@@FILE %s\nrc=%d\nSTDERR:\n%s\n@@END\n"
                          % (p, rc, esc(err)))
        os.remove(q)
    with open(wpath(workdir, "compile_results.txt"), "w") as f:
        f.write("".join(blocks))
    return n


def process_run_queue(workdir):
    q = wpath(workdir, "run_queue.txt")
    blocks = []
    if os.path.exists(q):
        with open(q, "r", encoding="utf-8", errors="replace") as f:
            qlines = f.read().split("\n")
        for line in qlines:
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != 3 or not parts[2].startswith("CAPTURE="):
                raise DriverFail("malformed run_queue line: " + line[:120])
            binary, args, cap = parts[0], parts[1], parts[2][len("CAPTURE="):]
            argv = [a for a in args.split(" ") if a != ""]
            binpath = wpath(workdir, binary)
            if not os.path.isfile(binpath):
                # orchestration: the binary is absent (its compile failed or
                # never produced it). Recorded, not interpreted.
                rc, out = -98, b""
            else:
                rc, out, err = run([binpath] + argv, cwd=workdir, timeout=30)
            if cap:
                cp = wpath(workdir, cap)
                cdir = os.path.dirname(cp)
                if cdir:
                    os.makedirs(cdir, exist_ok=True)
                with open(cp, "wb") as f:
                    f.write(out)
            blocks.append("@@RUN %s\t%s\nrc=%d\nSTDOUT:\n%s\n@@END\n"
                          % (binary, args, rc, esc(out)))
        os.remove(q)
    with open(wpath(workdir, "run_results.txt"), "w") as f:
        f.write("".join(blocks))


def process_queues(workdir, counter):
    counter[0] += process_compile_queue(workdir)
    process_run_queue(workdir)


def phase2_deliberate(workdir, engine_bin):
    counter = [0]

    def step(mode):
        rc = run_engine(engine_bin, mode, workdir)
        if rc != 0:
            raise DriverFail("engine mode '%s' failed (rc=%d)" % (mode, rc))
        process_queues(workdir, counter)

    step("propose")
    it = 0
    while not os.path.exists(wpath(workdir, "critique_done.txt")):
        rc = run_engine(engine_bin, "critique", workdir)
        if rc != 0:
            raise DriverFail("engine mode 'critique' failed (rc=%d)" % rc)
        process_queues(workdir, counter)
        it += 1
        if it > CRITIQUE_LOOP_GUARD:
            raise DriverFail("critique did not terminate (no critique_done.txt)")
    for mode in ["compose", "validate", "validate2", "diagnose"]:
        step(mode)
    if os.path.exists(wpath(workdir, "revise2.txt")):
        os.remove(wpath(workdir, "revise2.txt"))
        for mode in ["validate", "validate2", "diagnose"]:
            step(mode)
    rc = run_engine(engine_bin, "freeze", workdir)
    if rc != 0:
        raise DriverFail("engine mode 'freeze' failed (rc=%d)" % rc)

    total = counter[0]
    t4x_found = False
    for _root, _dirs, files in os.walk(workdir):
        for fn in files:
            if fn == "t4x.json":
                t4x_found = True
    trace_hash = sha256_file(wpath(workdir, "trace_frozen.txt"))
    arch_hash = sha256_file(wpath(workdir, "t1n_arch.zag"))
    with open(wpath(workdir, "arch_frozen.sha256"), "w") as f:
        f.write(arch_hash + "\n")
    freeze_rec = []
    freeze_rec.append("compilations_during_invention=%d" % total)
    freeze_rec.append("max_compilations=%d" % MAX_COMPILATIONS)
    freeze_rec.append("budget_violation=" + ("YES" if total > MAX_COMPILATIONS else "no"))
    freeze_rec.append("t4x_json_in_workdir=" + ("YES" if t4x_found else "no"))
    freeze_rec.append("trace_frozen_sha256=" + trace_hash)
    freeze_rec.append("t1n_arch_sha256=" + arch_hash)
    freeze_rec.append("note=no t4x.json was read before freeze: the workdir never "
                 "contained it and the engine was never invoked with its path")
    with open(wpath(workdir, "phase2_freeze_record.txt"), "w") as f:
        f.write("\n".join(freeze_rec) + "\n")

    problems = []
    if total > MAX_COMPILATIONS:
        problems.append("compilation budget exceeded: %d > %d (recorded, run FAILs)"
                        % (total, MAX_COMPILATIONS))
    if t4x_found:
        problems.append("t4x.json present in workdir before freeze")
    if problems:
        raise DriverFail("; ".join(problems))
    return total

# ---------------- Phase 3: IV-P1 / IV-P2 ----------------

def _read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def phase3_checks(workdir, engine_src, arm):
    """Returns (overall_ok, result_text). Missing files raise DriverFail;
    check failures are RECORDED (invention claim FAIL) without raising."""
    results = []

    def rec(name, ok, detail=""):
        results.append((name, ok, detail))

    mod_path = wpath(workdir, "t1n_arch.zag")
    trace_path = wpath(workdir, "trace_frozen.txt")
    for p in (mod_path, trace_path):
        if not os.path.isfile(p):
            raise DriverFail("phase3: missing " + p)
    mod = _read_text(mod_path)
    trace = _read_text(trace_path)
    mlines = mod.split("\n")
    tlines = trace.split("\n")

    # module functions: top-level `fn name(`
    fns = []
    for i, ln in enumerate(mlines):
        if ln.startswith("fn "):
            rest = ln[3:]
            j = rest.find("(")
            if j > 0:
                fns.append((rest[:j], i))

    # taught entry ids from workdir copies
    taught = set()
    for tp in (wpath(workdir, "entries.txt"), wpath(workdir, "corpus.txt")):
        if os.path.isfile(tp):
            for ln in _read_text(tp).split("\n"):
                if ln.startswith("@") and ln != "@end":
                    taught.add(ln[1:])

    # trace episode ids
    ep_ids = set()
    for ln in tlines:
        parts = ln.split(" ")
        if len(parts) >= 2 and parts[0] == "EP":
            ep_ids.add(parts[1])

    # (a) every fn has a preceding // EP: + CITES: comment
    ok_a = True
    det_a = []
    cited_eps = []
    cited_entries = []
    for (name, idx) in fns:
        j = idx - 1
        comments = []
        while j >= 0 and mlines[j].startswith("//"):
            comments.append(mlines[j])
            j -= 1
        has_ep = False
        has_cites = False
        for c in comments:
            if "EP:" in c:
                has_ep = True
                cited_eps.extend(t.strip(" ,;") for t in c.split("EP:", 1)[1].split())
            if "CITES:" in c:
                has_cites = True
                cited_entries.extend(t.strip(" ,;") for t in c.split("CITES:", 1)[1].split())
        if not (has_ep and has_cites):
            ok_a = False
            det_a.append(name)
    rec("IV-P1(a) every fn carries // EP: + CITES:", ok_a,
        "missing on: " + ",".join(det_a) if det_a
        else "%d fns, all cited" % len(fns))

    # (b) every cited EP exists in the frozen trace
    ep_cited = [t for t in cited_eps if t.startswith("EP")]
    missing_ep = [t for t in ep_cited if t not in ep_ids]
    rec("IV-P1(b) cited episodes exist in trace", not missing_ep,
        "missing: " + ",".join(missing_ep) if missing_ep
        else "%d cited, all resolve" % len(ep_cited))

    # (c) every cited entry exists in the taught read-set
    missing_en = [t for t in cited_entries if t not in taught]
    rec("IV-P1(c) cited entries are taught", not missing_en,
        "untaught: " + ",".join(missing_en) if missing_en
        else "%d cited, all taught" % len(cited_entries))

    # (d) no 200+ char contiguous substring of the module appears in any
    # crew-authored source (engine / driver / wrapper)
    crew_paths = [os.path.abspath(engine_src),
                  os.path.join(T1N, "driver", "t1n_driver.py"),
                  os.path.join(T1N, "wrapper", "wrapper_main.zag")]
    crew_texts = [(p, _read_text(p)) for p in crew_paths]
    matches = []
    W = 200
    if len(mod) >= W:
        i = 0
        while i + W <= len(mod):
            w = mod[i:i + W]
            for (p, text) in crew_texts:
                if w in text:
                    matches.append((os.path.basename(p), i))
                    break
            if len(matches) >= 5:
                break
            i += 1
    rec("IV-P1(d) no 200+ char crew overlap", not matches,
        "matches: " + str(matches[:5]) if matches else "clean")

    # (e) deliberation completeness over the frozen trace
    ROLE2TYPE = {"PROPOSER": "PROPOSE", "CRITIC": "CRITIQUE",
                 "COMPOSER": "COMPOSE", "DIAGNOSER": "DIAGNOSE"}
    ETYPES = ["PROPOSE", "CRITIQUE", "COMPOSE", "DIAGNOSE"]

    def covers(ln, etype):
        toks = ln.split(" ")
        if etype in toks:
            return True
        role = toks[1] if len(toks) > 1 else ""
        return ROLE2TYPE.get(role) == etype

    def alt_present(ln):
        toks = ln.split(" ")
        for tok in toks:
            if tok.upper().startswith("ALT"):
                return True
        return "alternative" in ln.lower()

    ok_e = True
    det_e = []
    subjects = [name for (name, _i) in fns if name.startswith("mech_")]
    subjects.extend(["selection", "revision"])
    for sub in subjects:
        sublow = sub.lower()
        for t in ETYPES:
            hit = False
            for ln in tlines:
                if covers(ln, t) and sublow in ln.lower():
                    hit = True
                    break
            if not hit:
                ok_e = False
                det_e.append(sub + ": no " + t)
        if sub in ("selection", "revision"):
            n_alt = sum(1 for ln in tlines
                        if sublow in ln.lower() and alt_present(ln))
            if n_alt < 2:
                ok_e = False
                det_e.append(sub + ": %d alternatives (<2)" % n_alt)
            if not any(sublow in ln.lower() and "compar" in ln.lower()
                       for ln in tlines):
                ok_e = False
                det_e.append(sub + ": no recorded comparison")
    rec("IV-P2 deliberation completeness", ok_e,
        "; ".join(det_e) if det_e else "all subjects fully episoded")

    overall = all(ok for (_n, ok, _d) in results)
    out_lines = ["arm=" + arm, "overall=" + ("PASS" if overall else "FAIL")]
    for (name, ok, detail) in results:
        out_lines.append("%s: %s%s" % (name, "PASS" if ok else "FAIL",
                                       " | " + detail if detail else ""))
    out_lines.append("note=heuristic mechanical check; coordinator manual "
                     "review follows (grep is necessary, not sufficient)")
    text = "\n".join(out_lines) + "\n"
    with open(wpath(workdir, "ivp1_ivp2_result.txt"), "w") as f:
        f.write(text)
    audits_dir = os.path.join(T1N, "audits")
    os.makedirs(audits_dir, exist_ok=True)
    with open(os.path.join(audits_dir,
                           "ivp1_ivp2_result_%s.txt" % arm), "w") as f:
        f.write(text)
    return overall, text

# ---------------- Phase 4: wrapper build + battery ----------------

def load_orig_driver():
    path = os.path.join(TASK1, "harness", "driver.py")
    spec = importlib.util.spec_from_file_location("orig_driver", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def phase4_battery(arm, workdir, battery_budget, reps):
    # the frozen module must be unchanged since freeze
    af = sha256_file(wpath(workdir, "t1n_arch.zag"))
    frozen = _read_text(wpath(workdir, "arch_frozen.sha256")).strip()
    if af != frozen:
        raise DriverFail("t1n_arch.zag changed after freeze")

    # per-arm wrapper build: wbuild/wrapper_main.zag imports ../t1n_arch.zag
    wbuild = wpath(workdir, "wbuild")
    os.makedirs(wbuild, exist_ok=True)
    shutil.copy(os.path.join(T1N, "wrapper", "wrapper_main.zag"),
                wpath(wbuild, "wrapper_main.zag"))
    rc, out, err = run([ZNC, "wrapper_main.zag", "-o", "../wrapper.bin",
                        "--no-analyze"], cwd=wbuild, timeout=600)
    with open(wpath(workdir, "wrapper_build.log"), "w") as f:
        f.write("rc=%d\nSTDOUT:\n%s\nSTDERR:\n%s\n"
                % (rc, esc(out), esc(err)))
    wrapper_bin = wpath(workdir, "wrapper.bin")
    if rc != 0 or not os.path.isfile(wrapper_bin):
        raise DriverFail("wrapper build failed (rc=%d)" % rc)

    # 58-item battery with the ORIGINAL driver.py battery loop.
    # t4x.json is first read HERE, after freeze (see phase2_freeze_record).
    orig = load_orig_driver()
    battery = os.path.join(TASK1, "batteries", "task1.json")
    store = wpath(workdir, "entries.txt")  # accepted-but-ignored by wrapper
    n_items = len(json.load(open(battery))["items"])
    if n_items != 58:
        raise DriverFail("battery item count changed: %d != 58" % n_items)
    saved_argv = sys.argv
    try:
        for r in range(1, reps + 1):
            # Leaf dir name is identical ("rep") for every rep: the original
            # driver's evidence envelope folds the run workdir to its
            # basename, so same-leaf rep dirs yield byte-identical canonical
            # logs (RK3). Parents r1..rN keep the reps separated on disk.
            repdir = wpath(workdir, "battery", "r%d" % r, "rep")
            os.makedirs(repdir, exist_ok=True)
            out_path = wpath(repdir, "canonical.json")
            sys.argv = ["driver.py", wrapper_bin, store, battery, out_path,
                        str(battery_budget), repdir]
            orig.main()
    finally:
        sys.argv = saved_argv

    blobs = []
    for r in range(1, reps + 1):
        with open(wpath(workdir, "battery", "r%d" % r, "rep",
                         "canonical.json"), "rb") as f:
            blobs.append(f.read())
    identical = all(b == blobs[0] for b in blobs)
    with open(wpath(workdir, "rep_compare.txt"), "w") as f:
        f.write("reps=%d\nbyte_identical=%s\n" %
                (reps, "yes" if identical else "NO"))
        for r in range(1, reps + 1):
            f.write("rep%d_sha256=%s\n" %
                    (r, hashlib.sha256(blobs[r - 1]).hexdigest()))
    if not identical:
        raise DriverFail("reps not byte-identical (RK3)")
    return blobs[0]


# ---------------- Phase 5: bar table ----------------

def tier_stats(canon):
    tiers = {}
    for r in canon:
        t = tiers.setdefault(r["tier"], {"n": 0, "pass": 0, "iters": 0,
                                         "znc": 0, "first": 0})
        t["n"] += 1
        if r["outcome"] == "pass":
            t["pass"] += 1
            if r["iters_used"] == 1:
                t["first"] += 1
        t["iters"] += r["iters_used"]
        t["znc"] += r["znc_calls"]
    return tiers


def phase5_results(work_base, arms, reps):
    per_arm = {}
    for arm in arms:
        workdir = wpath(work_base, arm)
        with open(wpath(workdir, "battery", "r1", "rep", "canonical.json")) as f:
            canon = json.load(f)
        per_arm[arm] = tier_stats(canon)

    # RK4: static audit of driver + wrapper
    audit = os.path.join(T1N, "driver", "audit_driver.py")
    rc, out, err = run([sys.executable, audit,
                        os.path.join(T1N, "driver", "t1n_driver.py"),
                        os.path.join(T1N, "wrapper", "wrapper_main.zag")],
                       cwd=T1N, timeout=120)
    rk4_pass = (rc == 0)
    rk4_text = out.decode("utf-8", "replace") + err.decode("utf-8", "replace")

    # RK5: frozen artifacts unchanged since freeze
    rk5 = {}
    for arm in arms:
        workdir = wpath(work_base, arm)
        th = sha256_file(wpath(workdir, "trace_frozen.txt"))
        th_rec = _read_text(wpath(workdir, "trace_frozen.sha256")).strip()
        ah = sha256_file(wpath(workdir, "t1n_arch.zag"))
        ah_rec = _read_text(wpath(workdir, "arch_frozen.sha256")).strip()
        # EP ids unique + monotonic
        ids = []
        for ln in _read_text(wpath(workdir, "trace_frozen.txt")).split("\n"):
            parts = ln.split(" ")
            if len(parts) >= 2 and parts[0] == "EP":
                ids.append(parts[1])
        rk5[arm] = (th == th_rec and ah == ah_rec and
                    len(ids) == len(set(ids)) and ids == sorted(ids))

    # IV-P0: from phase-1 result; IV-P1/P2: from phase-3 result
    iv = {}
    for arm in arms:
        workdir = wpath(work_base, arm)
        ivp0_txt = _read_text(wpath(workdir, "ivp0_result.txt"))
        ivp0 = ivp0_txt.startswith("rc=0")
        ivp1p2_txt = _read_text(wpath(workdir, "ivp1_ivp2_result.txt"))
        ivp1p2 = "overall=PASS" in ivp1p2_txt.split("\n")[1]
        iv[arm] = (ivp0, ivp1p2)

    L = []
    L.append("# T1N bar table")
    L.append("")
    L.append("## Mastery per tier (pass/total)")
    L.append("")
    L.append("| tier | baseline | " +
             " | ".join(arms) + " |")
    L.append("|---|---|" + "|".join(["---"] * len(arms)) + "|")
    for t in TIER_ORDER:
        bp, bn = BASELINE[t]
        cells = []
        for arm in arms:
            s = per_arm[arm].get(t, {"pass": 0, "n": 0})
            cells.append("%d/%d" % (s["pass"], s["n"]))
        L.append("| %s | %d/%d | %s |" % (t, bp, bn, " | ".join(cells)))
    L.append("")
    L.append("## Bars")
    L.append("")
    L.append("| bar | " + " | ".join(arms) + " |")
    L.append("|---|" + "|".join(["---"] * len(arms)) + "|")
    bar_rows = []
    for arm in arms:
        tiers = per_arm[arm]
        r1_ok, better = True, False
        for t in TIER_ORDER:
            bp, _bn = BASELINE[t]
            s = tiers.get(t, {"pass": 0})
            if s["pass"] < bp:
                r1_ok = False
            if s["pass"] > bp:
                better = True
        t4x = tiers.get("T4X", {"first": 0})
        t5 = tiers.get("T5", {"pass": 0})
        eff = tiers.get("T3", {"iters": 0, "znc": 0, "n": 1})
        for t in ("T4", "T4X"):
            s = tiers.get(t, {"iters": 0, "znc": 0})
            eff["iters"] += s["iters"]
            eff["znc"] += s["znc"]
        nn = (tiers.get("T3", {"n": 0})["n"] + tiers.get("T4", {"n": 0})["n"]
              + tiers.get("T4X", {"n": 0})["n"])
        mean_iters = eff["iters"] / nn if nn else 0
        ivp0, ivp1p2 = iv[arm]
        bar_rows.append({
            "KB-R1": "PASS" if (r1_ok and better) else "FAIL",
            "KB-R2": "challenger mean-iters=%.2f znc=%d on T3+T4+T4X; "
                     "baseline efficiency not pinned in prereg §5" % (mean_iters, eff["znc"]),
            "KB-R3": "PASS (%d/8 T4X first-attempt)" % t4x["first"] if t4x["first"] >= 6
                     else "FAIL (%d/8 T4X first-attempt)" % t4x["first"],
            "RK1": "PASS" if r1_ok else "FAIL",
            "RK2": "PASS" if t5["pass"] == 6 else "FAIL",
            "RK3": "PASS (%d reps byte-identical)" % reps,
            "RK4": "PASS" if rk4_pass else "FAIL",
            "RK5": "PASS" if rk5[arm] else "FAIL",
            "IV-P0": "PASS" if ivp0 else "FAIL",
            "IV-P1/P2": "PASS" if ivp1p2 else "FAIL",
        })
    bar_names = ["KB-R1", "KB-R2", "KB-R3", "RK1", "RK2", "RK3", "RK4", "RK5",
                 "IV-P0", "IV-P1/P2"]
    for b in bar_names:
        L.append("| %s | %s |" % (b, " | ".join(r[b] for r in bar_rows)))
    L.append("")
    L.append("## Notes")
    L.append("")
    L.append("- Baseline: prereg §5 pinned numbers (T1 10/10, T2 8/8, T3 10/10, "
             "T4 12/12, T4m 4/4, T4x 0/8, T5 6/6).")
    L.append("- KB-R2 baseline efficiency (mean iters / znc on T3+T4+T4X) is not "
             "pinned in prereg §5; challenger values reported for the "
             "coordinator's comparison against the Task-1 final report.")
    L.append("- RK4 detail:")
    for ln in rk4_text.strip().split("\n"):
        L.append("  - " + ln)
    L.append("- IV-P1/P2 are the driver's mechanical checks; coordinator manual "
             "review follows (grep is necessary, not sufficient).")
    L.append("- Invention-claim FAIL (IV-P1/P2) does not void the mastery "
             "numbers (prereg §6.1: separate finding).")
    results_dir = os.path.join(T1N, "results")
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, "T1N_RESULTS.md"), "w") as f:
        f.write("\n".join(L) + "\n")


# ---------------- main ----------------

def run_arm(arm, workdir, args):
    print("== T1N arm=%s workdir=%s" % (arm, workdir), flush=True)
    print("-- phase0 teach", flush=True)
    phase0_teach(arm, workdir)
    print("-- phase1 engine build + IV-P0", flush=True)
    engine_bin = phase1_engine(workdir, args.engine_src, args.engine_bin)
    print("-- phase2 deliberate", flush=True)
    total = phase2_deliberate(workdir, engine_bin)
    print("-- phase2 done, compilations=%d" % total, flush=True)
    print("-- phase3 IV-P1/IV-P2", flush=True)
    ok, _text = phase3_checks(workdir, args.engine_src, arm)
    print("-- phase3 invention claim: %s" % ("PASS" if ok else "FAIL (recorded; continuing)"),
          flush=True)
    print("-- phase4 wrapper + battery", flush=True)
    phase4_battery(arm, workdir, args.battery_budget, args.reps)
    print("-- arm %s complete" % arm, flush=True)


# ---------------- preflight: RK4 static audit BEFORE any measurement ----------------

def preflight_audit():
    """Run audit_driver.py on this driver + the wrapper before either arm.

    RK4 requires the plumbing to be certified decision-free BEFORE the
    engine deliberates or any battery item runs. Nonzero => VOID.
    """
    audit = os.path.join(T1N, "driver", "audit_driver.py")
    rc, out, err = run([sys.executable, audit,
                        os.path.join(T1N, "driver", "t1n_driver.py"),
                        os.path.join(T1N, "wrapper", "wrapper_main.zag")],
                       cwd=T1N, timeout=120)
    text = out.decode("utf-8", "replace") + err.decode("utf-8", "replace")
    adir = os.path.join(T1N, "audits")
    os.makedirs(adir, exist_ok=True)
    with open(os.path.join(adir, "preflight_audit.txt"), "w") as f:
        f.write("rc=%d\n%s" % (rc, text))
    if rc != 0:
        raise DriverFail("preflight static audit FAILED (rc=%d): %s"
                         % (rc, text.strip()[:200]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="both",
                    choices=["informed", "scratch", "both"])
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--engine-src",
                    default=os.path.join(T1N, "engine", "t1n_delib.zag"))
    ap.add_argument("--engine-bin", default=None)
    ap.add_argument("--work-base", default=os.path.join(T1N, "runs"))
    ap.add_argument("--battery-budget", type=int, default=6)
    args = ap.parse_args()

    os.environ.setdefault("TMPDIR",
                          os.path.expanduser("~/workspace/tmp_commit"))
    os.makedirs(os.path.expanduser("~/workspace/tmp_commit"), exist_ok=True)

    arms = ["informed", "scratch"] if args.arm == "both" else [args.arm]
    try:
        print("-- preflight static audit (RK4)", flush=True)
        preflight_audit()
        print("-- preflight audit PASS", flush=True)
        for arm in arms:
            run_arm(arm, wpath(args.work_base, arm), args)
        phase5_results(args.work_base, arms, args.reps)
    except DriverFail as e:
        print("DRIVER FAIL: %s" % e, file=sys.stderr)
        return 1
    print("T1N driver complete", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
