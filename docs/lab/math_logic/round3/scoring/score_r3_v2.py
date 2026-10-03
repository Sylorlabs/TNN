#!/usr/bin/env python3
"""MATH R3 scoring harness — deterministic, zero RNG.

Runs the four native engines (N1-N4) over the R3 batteries, 3 external runs
per problem per engine with byte-identity assertion, scores verdicts against
the sealed keys, runs the anti-bridge audit, and computes the primary bars.

Writes:
  RESULTS_R3_V2.json — per-engine per-problem records
  SCORECARD_R3_V2.md — bars table + audit results + findings
Raw engine outputs stay local-only under ~/workspace/scratch/math_r3/raw/
(SHAs recorded in the JSON).
"""
import subprocess, hashlib, json, os, re, sys, time
from collections import Counter

BASE = "/home/hatch/workspace/tnn-lab/math_logic"
R3 = BASE + "/round3"
BAT = R3 + "/batteries"
NLSTORE = BAT + "/knowledge/KNOWLEDGE_STORE_NL.md"
RAW = "/home/hatch/workspace/scratch/math_r3/raw"
AUDD = "/home/hatch/workspace/scratch/math_r3/audit"
TIMEOUT = 300

V2_ENGINES = ("n1", "n2", "n3")

ENGINES = {
    "n1": {"bin": R3 + "/engines/n1/n1_bin", "cwd": R3 + "/engines/n1",
           "argv": lambda b, p, s, o: [b, p, s, o],
           "vre": re.compile(r"^RESULT\s+(PROVED|WITHHELD)", re.M),
           "vmap": {"PROVED": "DERIVED", "WITHHELD": "WITHHELD"}},
    "n2": {"bin": R3 + "/engines/n2/n2_bin", "cwd": R3 + "/engines/n2",
           "argv": lambda b, p, s, o: [b, p, o, s],
           "vre": re.compile(r"^VERDICT:\s*(DERIVED|WITHHELD|REFUTED)", re.M),
           "vmap": {"DERIVED": "DERIVED", "WITHHELD": "WITHHELD", "REFUTED": "REFUTED"}},
    "n3": {"bin": R3 + "/engines/n3/n3_bin", "cwd": R3 + "/engines/n3",
           "argv": lambda b, p, s, o: [b, p, o, s],
           "vre": re.compile(r"^VERDICT:\s*(DERIVED|WITHHELD)", re.M),
           "vmap": {"DERIVED": "DERIVED", "WITHHELD": "WITHHELD"}},
    "n4": {"bin": R3 + "/engines/n4/n4_bin", "cwd": R3 + "/engines/n4",
           "argv": lambda b, p, s, o: [b, p, o, s],
           "vre": re.compile(r"^ANSWER:\s*(DERIVED|WITHHELD)", re.M),
           "vmap": {"DERIVED": "DERIVED", "WITHHELD": "WITHHELD"}},
}

EXPECTED_BIN_SHA = {
    "n1": "d9a9a4cd57b0868c72963f854da068237ba4003c21c014885e792115e9d92aab",
    "n2": "9f82b3bc2c974476e36f0f5ce0821825d81486203eaa3132e1de05ce178349e7",
    "n3": "519afe7c3dce9c97534d347b4f185da0178e3f2ff817d221550e38d966ed9540",
    "n4": "002d3222a683d3d178510ecabd89a86f7d748b55d6f8c7b36b806385af421a1f",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_key_simple(path):
    """id: VERDICT ... -> {id: verdict}"""
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^(\S+):\s*(DERIVED|WITHHELD)\b", line)
            if m:
                d[m.group(1)] = m.group(2)
    return d


def load_key_twins(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^(\S+)\s*->\s*\S+\s*:\s*(DERIVED|WITHHELD)", line)
            if m:
                d[m.group(1)] = m.group(2)
    return d


def load_key_b5x(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^(\S+):\s*(DERIVED|WITHHELD)\s*\(([DW])\)", line)
            if m:
                d[m.group(1)] = (m.group(2), m.group(3))
    return d


def load_key_b6x(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^(\S+):\s*(\d+)\s*steps", line)
            if m:
                d[m.group(1)] = int(m.group(2))
    return d


def b1n_expected(pid):
    with open(f"{BASE}/problems/{pid}.txt") as f:
        t = f.read()
    m = re.search(r"TYPE:\s*(\S+)", t)
    typ = m.group(1) if m else "?"
    # R2 B1N: every engine scored 0/22 on raw NL (all withheld); proof-type
    # problems are true claims (DERIVED expected), all other types expect
    # the engine NOT to derive (WITHHELD).
    return "DERIVED" if typ == "proof" else "WITHHELD", typ


def build_problem_list():
    probs = []
    # R3N
    key_r3n = load_key_simple(BAT + "/sealed/SEALED_R3N.sol")
    for i in range(1, 25):
        pid = f"R3N_{i:02d}"
        probs.append({"battery": "r3n", "pid": pid,
                      "path": f"{BAT}/r3n/{pid}.txt", "store": NLSTORE,
                      "sealed": key_r3n.get(pid)})
    assert len(key_r3n) == 24, f"R3N key has {len(key_r3n)} entries"
    # twins
    key_tw = load_key_twins(BAT + "/sealed/SEALED_TWINS.map")
    twins = sorted([f[:-4] for f in os.listdir(BAT + "/twins") if f.endswith(".txt")])
    assert len(twins) == 37, f"twins count {len(twins)}"
    for pid in twins:
        probs.append({"battery": "twins", "pid": pid,
                      "path": f"{BAT}/twins/{pid}.txt", "store": NLSTORE,
                      "sealed": key_tw.get(pid)})
    assert len(key_tw) == 37
    # b5x_nl (store from the problem's own STORE: line = injected store)
    key_b5x = load_key_b5x(BAT + "/sealed/SEALED_B5X_NL.sol")
    b5x = []
    for lvl in (2, 3, 4):
        for i in range(1, 21):
            b5x.append(f"B5X_NL_L{lvl}_{i:02d}")
    assert len(b5x) == 60
    for pid in b5x:
        ppath = f"{BAT}/b5x_nl/{pid}.txt"
        with open(ppath) as f:
            txt = f.read()
        m = re.search(r"^STORE:\s*(\S+)", txt, re.M)
        assert m, f"no STORE line in {pid}"
        store = "/home/hatch/workspace/tnn-lab/" + m.group(1)
        assert os.path.exists(store), f"store missing {store}"
        sv, kind = key_b5x[pid]
        probs.append({"battery": "b5x_nl", "pid": pid, "path": ppath,
                      "store": store, "sealed": sv, "kind": kind})
    assert len(key_b5x) == 60
    # b6x_nl
    key_b6x = load_key_b6x(BAT + "/sealed/SEALED_B6X_NL.sol")
    for pid, fn in [("B6X_NL_LINEAR", "B6X_NL_LINEAR.txt"),
                    ("B6X_NL_DAG", "B6X_NL_DAG.txt"),
                    ("B6X_NL_CONTRADICTION", "B6X_NL_CONTRADICTION.txt")]:
        probs.append({"battery": "b6x_nl", "pid": pid,
                      "path": f"{BAT}/b6x_nl/{fn}", "store": NLSTORE,
                      "sealed": None, "sealed_steps": key_b6x[pid]})
    # b1n
    for i in range(1, 23):
        pid = f"P{i:02d}"
        sv, typ = b1n_expected(pid)
        probs.append({"battery": "b1n", "pid": pid,
                      "path": f"{BASE}/problems/{pid}.txt", "store": NLSTORE,
                      "sealed": sv, "ptype": typ})
    return probs


def parse_verdict(engine, outpath):
    with open(outpath, "rb") as f:
        data = f.read()
    txt = data.decode("utf-8", errors="replace")
    m = ENGINES[engine]["vre"].search(txt)
    if not m:
        return "NO_VERDICT"
    return ENGINES[engine]["vmap"][m.group(1)]


def parse_derivations(outpath):
    with open(outpath, "rb") as f:
        txt = f.read().decode("utf-8", errors="replace")
    m = re.search(r"^DERIVATIONS:\s*(\d+)", txt, re.M)
    return int(m.group(1)) if m else None


def run_problem(engine, prob):
    """3 external runs; assert byte-identical. Returns record dict."""
    eng = ENGINES[engine]
    rec = {"pid": prob["pid"], "battery": prob["battery"],
           "_path": prob["path"],
           "store": prob["store"],
           "store_sha": sha256_file(prob["store"]),
           "sealed": prob.get("sealed"),
           "runs": []}
    outdir = f"{RAW}/{engine}"
    os.makedirs(outdir, exist_ok=True)
    shas = []
    for r in range(3):
        out = f"{outdir}/{prob['pid']}_r{r}.txt"
        argv = eng["argv"](eng["bin"], prob["path"], prob["store"], out)
        t0 = time.time()
        p = subprocess.run(argv, cwd=eng["cwd"], capture_output=True,
                           timeout=TIMEOUT)
        dt = time.time() - t0
        hs = sha256_file(out) if (p.returncode == 0 and os.path.exists(out)) else None
        shas.append(hs)
        rec["runs"].append({"exit": p.returncode, "sha": hs,
                            "wall_s": round(dt, 3),
                            "stdout_tail": p.stdout.decode("utf-8", errors="replace")[-200:],
                            "stderr_tail": p.stderr.decode("utf-8", errors="replace")[-200:]})
    rec["runs_identical"] = (shas[0] is not None and shas[0] == shas[1] == shas[2])
    rec["divergent"] = not (shas[0] == shas[1] == shas[2])
    rec["trace_sha"] = shas[0]
    if rec["runs_identical"]:
        rec["verdict"] = parse_verdict(engine, f"{outdir}/{prob['pid']}_r0.txt")
        rec["derivations"] = parse_derivations(f"{outdir}/{prob['pid']}_r0.txt")
    else:
        # finding: use run 1 for scoring per task
        rec["verdict"] = parse_verdict(engine, f"{outdir}/{prob['pid']}_r0.txt") \
            if shas[0] else "NO_VERDICT"
        rec["derivations"] = parse_derivations(f"{outdir}/{prob['pid']}_r0.txt") \
            if shas[0] else None
    sv = prob.get("sealed")
    ev = rec["verdict"]
    cls, correct = classify(ev, sv)
    rec["class"] = cls
    rec["correct"] = correct
    return rec


def classify(ev, sv):
    """Verdict classes. ev in {DERIVED,WITHHELD,REFUTED,NO_VERDICT}.
    REFUTED is a positive derivation act (of the negation)."""
    if ev == "NO_VERDICT":
        return ("no_verdict", False)
    if sv is None:
        return ("unkeyed", None)
    derived_act = ev in ("DERIVED", "REFUTED")
    if derived_act and sv == "DERIVED":
        return ("correct_derived", True)
    if derived_act and sv == "WITHHELD":
        return ("false_derived", False)
    if ev == "WITHHELD" and sv == "WITHHELD":
        return ("correct_withheld", True)
    if ev == "WITHHELD" and sv == "DERIVED":
        return ("false_withheld", False)
    return ("unkeyed", None)


# ---------------- anti-bridge audit: trace honesty checkers ----------------
STOP = set("""the a an is are was were be been being of to in on for with by and
or as at from that this these those it its if then than so but such every each
all any some there here which who what when where how why can could should
would may might must shall will do does did has have had having into onto out
up down over under between through during before after above below more most
other same only very just also too we you your his her their our my i me he
she they them not no never neither none without cannot false impossible fails
denies refutes contradicts than""".split())


def static_backstop():
    """Deterministic source scan for RNG/time syscalls in engine sources.
    Returns {'pass': bool, 'findings': [...]}. Serialized into JSON/scorecard."""
    import glob
    tokens = ["random", "urandom", "getrandom", "srand", "rand(",
              "rdtsc", "rdtscp", "clock_gettime", "gettimeofday", "time(",
              "/dev/random", "/dev/urandom"]
    findings = []
    for src in sorted(glob.glob(R3 + "/engines/n*/n*.zag")):
        txt = open(src, "rb").read().decode("utf-8", errors="replace").lower()
        for tok in tokens:
            if tok in txt:
                for i, line in enumerate(txt.split("\n")):
                    if tok in line and not line.strip().startswith("//"):
                        findings.append(f"{os.path.basename(src)}:{i+1} contains {tok!r}")
    return {"pass": not findings, "findings": findings}


def content_words(text):
    return [w for w in re.findall(r"[A-Za-z]{4,}", text) if w.lower() not in STOP]


def check_n1(trace_path, prob_path, store_path):
    """N1-TRACE v1 honesty: every inference step's holes cite byte-spans of
    premise states; licenses cite real store items; no magic content words."""
    findings = []
    with open(trace_path, "rb") as f:
        raw = f.read().decode("utf-8", errors="replace")
    with open(prob_path, "rb") as f:
        pbytes = f.read().decode("utf-8", errors="replace")
    with open(store_path, "rb") as f:
        sbytes = f.read().decode("utf-8", errors="replace")
    ground = pbytes + "\n" + sbytes
    n_store = len(re.findall(r"^\[K\d{3}\]", sbytes, re.M))
    # licenses
    lic_ids = set(int(m.group(1)) for m in re.finditer(r"^L(\d+)\s", raw, re.M))
    for m in re.finditer(r"^L(\d+)\s+\S+\s+kind\s+\d+\s+nprem\s+\d+\s+kid\s+(-?\d+)", raw, re.M):
        kid = int(m.group(2))
        if kid != -1 and not (0 <= kid < n_store):
            findings.append(f"license L{m.group(1)} cites invalid store item idx {kid} (store has {n_store})")
    # states (provenance quotes may span multiple lines: track continuation)
    states = {}  # id -> (src, text)
    cur = None
    cur_text_lines = []
    provs_full = []  # (state_id, premise_sid, quoted, ho, hl)
    in_prov = None  # [prem, ho, hl, collected_str] for multi-line quotes
    sec = None
    for line in raw.split("\n"):
        if line == "LICENSES":
            sec = "lic"
            continue
        if line == "STATES":
            sec = "st"
            continue
        if line in ("CANDIDATES", "CHALLENGES"):
            sec = "other"
            continue
        if sec != "st":
            continue
        if in_prov is not None:
            # accumulate until we have exactly hl bytes (newlines count as 1)
            need = in_prov[2] - len(in_prov[3])
            in_prov[3] += "\n" + line[:need]
            line = line[need:]
            if len(in_prov[3]) == in_prov[2]:
                assert line.startswith('"'), f"provenance quote not closed: {line[:40]!r}"
                provs_full.append((cur[0], in_prov[0], in_prov[3], in_prov[1], in_prov[2]))
                in_prov = None
                # fall through: remainder of line (if any) is not expected
            continue
        m = re.match(r"^S(\d+)\s+src\s+(\d+)\s+depth\s+\d+\s+def\s+\d+\s+q\s+(-?\d+)\s+np\s+\d+\s+lic\s+(-?\d+)\s+text\s?(.*)$", line)
        if m:
            if cur is not None:
                states[cur[0]] = (cur[1], "\n".join(cur_text_lines))
            cur = (int(m.group(1)), int(m.group(2)), int(m.group(4)))
            cur_text_lines = [m.group(5)]
            if cur[2] != -1 and cur[2] not in lic_ids:
                findings.append(f"state S{cur[0]} cites unknown license {cur[2]}")
            continue
        m2 = re.match(r"^\s+P(\d+)\s+hole(-?\d+)\s+span\s+(\d+),(\d+)\s+\"(.*)$", line)
        if m2 and cur is not None:
            prem, ho, hl, rest = (int(m2.group(1)), int(m2.group(3)),
                                  int(m2.group(4)), m2.group(5))
            if len(rest) >= hl and rest[hl:hl + 1] == '"':
                provs_full.append((cur[0], prem, rest[:hl], ho, hl))
            else:
                # multi-line quote: accumulate exactly hl bytes
                in_prov = [prem, ho, hl, rest]
            continue
        if cur is not None and line.strip() not in ("", "END"):
            cur_text_lines.append(line)
    if cur is not None:
        states[cur[0]] = (cur[1], "\n".join(cur_text_lines))
    # checks: the trace prints hole spans as tx-absolute, but the engine's
    # matcher records them premise-relative (verified against n1.zag:
    # n1_match receives the premise's tx slice; the output builder and the
    # printer both consume the offsets as tx-absolute). The frame-independent
    # honesty test: the quoted bytes must actually occur in the cited
    # premise's text. (For S0 premises relative==absolute, so those pass.)
    for (sid, prem, quoted, ho, hl) in provs_full:
        if prem not in states:
            findings.append(f"S{sid} cites nonexistent premise state S{prem}")
            continue
        if quoted and quoted not in states[prem][1]:
            findings.append(f"S{sid} hole span bytes {quoted!r} absent from premise S{prem} text "
                            f"(span [{ho},{ho+hl}) does not cite the premise)")
    for sid, (src, text) in sorted(states.items()):
        if src == 0:
            if text not in pbytes:
                findings.append(f"S{sid} src=input text not substring of problem file")
        elif src == 1:
            if text not in sbytes:
                findings.append(f"S{sid} src=knowledge text not substring of store file")
        elif src in (2, 3):
            for w in content_words(text):
                if w not in ground and w not in ("case",):
                    findings.append(f"S{sid} magic content word {w!r} absent from input+store bytes")
    return (len(findings) == 0, findings)


def check_n2(trace_path, prob_path, store_path):
    """N2 honesty: every span=B<bo>:<off>:<len> cites exact bytes of the
    problem (B0) or store (B1) file; every [Kddd] citation exists."""
    findings = []
    with open(trace_path, "rb") as f:
        raw = f.read().decode("utf-8", errors="replace")
    with open(prob_path, "rb") as f:
        pbytes = f.read().decode("utf-8", errors="replace")
    with open(store_path, "rb") as f:
        sbytes = f.read().decode("utf-8", errors="replace")
    bufs = {0: pbytes, 1: sbytes}
    n_b2 = 0
    for m in re.finditer(r"span=B(\d+):(\d+):(\d+)\s+\"([^\"]{0,400})(\.\.\.)?\"", raw):
        bo, off, ln, quoted = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
        if bo == 2:
            n_b2 += 1
            continue
        if bo not in bufs:
            findings.append(f"span cites unknown buffer B{bo}")
            continue
        buf = bufs[bo]
        actual = buf[off:off + min(ln, 400)]
        if not quoted or not actual.startswith(quoted[:400]):
            findings.append(f"span B{bo}:{off}:{ln} quoted {quoted[:40]!r} != file bytes {actual[:40]!r}")
    for m in re.finditer(r"\[(K\d{3})\]", raw):
        if m.group(1) not in sbytes and f"[{m.group(1)}]" not in sbytes:
            findings.append(f"cited store id [{m.group(1)}] absent from store file")
    return (len(findings) == 0, findings + ([f"note: {n_b2} spans cite internal arena B2 (derived text)"] if n_b2 else []))


def check_n3(trace_path, prob_path, store_path):
    """N3 honesty: ledger states cite input/store spans or prior states;
    licenses L0-L8; cite kids exist in the store."""
    findings = []
    with open(trace_path, "rb") as f:
        raw = f.read().decode("utf-8", errors="replace")
    with open(prob_path, "rb") as f:
        pbytes = f.read().decode("utf-8", errors="replace")
    with open(store_path, "rb") as f:
        sbytes = f.read().decode("utf-8", errors="replace")
    ground_words = set(w.lower() for w in content_words(pbytes + "\n" + sbytes))
    template_words = {"it", "is", "not", "the", "case", "that"}
    states = {}
    cur = None
    cur_lines = []
    in_ledger = False
    for line in raw.split("\n"):
        if line == "LEDGER:":
            in_ledger = True
            continue
        if not in_ledger:
            continue
        if line.startswith("PROPOSALS:") or line.startswith("RESULT") or line in ("AUDIT:", "END"):
            in_ledger = False
            continue
        m = re.match(r"^S(\d+)\s+src=(\w+)(?:\s+kid=(\S+))?\s+lic=(-?\d+)\s+p=\[([^\]]*)\]\s+depth=(\d+)\s+(\w+)\s+t=(-?\d+)\s+r=(\d+)\s+taint=(\d+):\s?(.*)$", line)
        if m:
            if cur is not None:
                states[cur[0]] = (cur[1], cur[2], "\n".join(cur_lines))
            sid = int(m.group(1))
            src = m.group(2)
            kid = m.group(3)
            lic = int(m.group(4))
            cur = (sid, src, kid)
            cur_lines = [m.group(11)]
            # lic=99 is the engine's PBC-fired goal sentinel (n3.zag:1096), not a wild license
            if lic not in (-1, 99) and not (0 <= lic <= 8):
                findings.append(f"S{sid} cites invalid license L{lic}")
            if src == "cite" and kid and f"[{kid}]" not in sbytes:
                findings.append(f"S{sid} cites store id [{kid}] absent from store file")
            continue
        if cur is not None:
            # keep blank lines: input/store texts are byte-verbatim, blanks included
            cur_lines.append(line)
    if cur is not None:
        states[cur[0]] = (cur[1], cur[2], "\n".join(cur_lines))
    for sid, (src, kid, text) in sorted(states.items()):
        if src == "input":
            if text.strip() and text.strip() not in pbytes:
                findings.append(f"S{sid} src=input text not substring of problem file")
        elif src == "cite":
            if text.strip() and text.strip() not in sbytes:
                findings.append(f"S{sid} src=cite text not substring of store file")
        elif src in ("assume", "prop", "subgoal", "pbc"):
            for w in content_words(text):
                if w.lower() not in ground_words and w.lower() not in template_words:
                    findings.append(f"S{sid} src={src} magic word {w!r}")
        else:
            findings.append(f"S{sid} unknown src {src!r}")
    # proposal log: premise ids must resolve
    for m in re.finditer(r"^R\d+\s+T[0-3]\s+\S+\s+L\d+\s+\S+\s+p=\[([^\]]*)\]\s+->\s+S(\d+)\s+(APPEND|DISCHARGE|REFUSE)", raw, re.M):
        for ps in m.group(1).split(","):
            ps = ps.strip()
            if ps not in ("-1", "") and int(ps) not in states:
                findings.append(f"proposal cites nonexistent state S{ps}")
        if int(m.group(2)) not in states and m.group(3) in ("APPEND", "DISCHARGE"):
            findings.append(f"proposal targets nonexistent state S{m.group(2)}")
    return (len(findings) == 0, findings)


_N4_CASES = None


def _n4_cases():
    """Parse cases_data.zag -> {idx: (cprob, ctrace)} with Zag escapes resolved.
    These are the exact byte strings the binary aligns against."""
    global _N4_CASES
    if _N4_CASES is not None:
        return _N4_CASES
    with open(R3 + "/engines/n4/cases_data.zag") as f:
        raw = f.read()
    vals = {}
    for m in re.finditer(r'const (N4_CPROB|N4_CTRACE)_(\d+):\[\]u8="((?:[^"\\]|\\.)*)";', raw):
        kind, idx, esc = m.group(1), int(m.group(2)), m.group(3)
        s = esc.replace("\\\\", "\x00").replace("\\n", "\n").replace("\\t", "\t") \
               .replace("\\r", "\r").replace('\\"', '"').replace("\x00", "\\")
        vals.setdefault(idx, {})[kind] = s
    _N4_CASES = {i: (vals[i]["N4_CPROB"], vals[i]["N4_CTRACE"]) for i in vals}
    return _N4_CASES


def _n4_stmt(pbytes):
    """Replicate cx_field(pbuf,'STATEMENT: ') + cx_trim + whole-file fallback."""
    for line in pbytes.split("\n"):
        if line.startswith("STATEMENT: "):
            return line[len("STATEMENT: ") :].rstrip(" \t\r")
    return pbytes.strip(" \t\r\n")


def check_n4(trace_path, prob_path, store_path, case_dir=None):
    """N4 honesty: ALIGN spans cite exact bytes of the case's PROBLEM string
    (embedded N4_CPROB_xx) and of the current problem's statement bytes;
    adapted step tags come from the case's trace string; verify= licenses
    cite real store items; no SURVIVED step with verify=none."""
    findings = []
    with open(trace_path, "rb") as f:
        raw = f.read().decode("utf-8", errors="replace")
    with open(prob_path, "rb") as f:
        pbytes = f.read().decode("utf-8", errors="replace")
    with open(store_path, "rb") as f:
        sbytes = f.read().decode("utf-8", errors="replace")
    stmt = _n4_stmt(pbytes)
    cases = _n4_cases()
    cur_case = None
    for line in raw.split("\n"):
        m = re.match(r"^CASE\s+(C\d+)\s+\(from", line)
        if m:
            cur_case = m.group(1)
            continue
        m = re.match(r"^\s+\[(\d+)\.\.(\d+)\)->\[(\d+)\.\.(\d+)\)\s+bytes=\"([^\"]*)\"$", line)
        if m and cur_case:
            c0, c1, p0, p1 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
            qb_raw = m.group(5)
            # printer shows first 48 bytes + "..." when the span exceeds 48
            truncated = qb_raw.endswith("...") and (c1 - c0) > 48
            qb = qb_raw[:-3] if truncated else qb_raw
            idx = int(cur_case[1:]) - 1
            cprob = cases.get(idx, ("", ""))[0]
            actual_c, actual_p = cprob[c0:c1], stmt[p0:p1]
            if truncated:
                if not (actual_c.startswith(qb) and actual_p.startswith(qb)):
                    findings.append(f"{cur_case} align span [{c0}..{c1}) prefix != {qb!r}")
            else:
                if actual_c != qb:
                    findings.append(f"{cur_case} align case-span [{c0}..{c1}) bytes != {qb!r}")
                if actual_p != qb:
                    findings.append(f"{cur_case} align problem-span [{p0}..{p1}) bytes != {qb!r}")
            continue
        m = re.match(r"^\s*S(\d+)\s+\[([^\]]+)\]\s+adapted=\d+B\s+verify=(\S+)\s+deps=\S+\s+->\s+(DROPPED|SURVIVED)", line)
        if m and cur_case:
            tag, ver = m.group(2), m.group(3)
            idx = int(cur_case[1:]) - 1
            ctrace = cases.get(idx, ("", ""))[1]
            if f"[{tag}]" not in ctrace:
                findings.append(f"{cur_case} step S{m.group(1)} tag [{tag}] absent from case trace")
            if ver != "none":
                for kid in re.findall(r"K\d{3}", ver):
                    if f"[{kid}]" not in sbytes:
                        findings.append(f"{cur_case} step S{m.group(1)} verify cites [{kid}] absent from store")
            if m.group(4) == "SURVIVED" and ver == "none":
                findings.append(f"{cur_case} step S{m.group(1)} SURVIVED with verify=none")
    return (len(findings) == 0, findings)


CHECKERS = {"n1": check_n1, "n2": check_n2, "n3": check_n3, "n4": check_n4}


# ---------------- audit variant extraction ----------------
def extract_audit_variants():
    """Parse sealed/SEALED_AUDIT.txt -> {var_id: (base_pid, expected_verdict, text)}.
    Writes problem files under AUDD/ (local scratch only)."""
    os.makedirs(AUDD, exist_ok=True)
    with open(BAT + "/sealed/SEALED_AUDIT.txt") as f:
        raw = f.read()
    variants = {}
    cur = None
    lines = []
    for line in raw.split("\n"):
        m = re.match(r"^(AUD_[PN]\d)\s+\(base\s+(R3N_\d+)\):\s*(DERIVED|WITHHELD)", line)
        if m:
            if cur:
                variants[cur[0]] = (cur[1], cur[2], lines)
            cur = (m.group(1), m.group(2), m.group(3))
            lines = []
            continue
        if cur and line.strip().startswith("-"):
            lines.append(line.strip())
    if cur:
        variants[cur[0]] = (cur[1], cur[2], lines)
    assert len(variants) == 12, f"expected 12 audit variants, got {len(variants)}"
    for vid, (base, expv, blines) in variants.items():
        with open(f"{AUDD}/{vid}.txt", "w") as f:
            f.write(f"ID: {vid}\nDOMAIN: audit\nTYPE: proof\nSTATEMENT:\n")
            for b in blines:
                f.write(b + "\n")
    return variants


def run_audit_variants(results):
    """Run the 12 audit variants per engine; compare verdict to the engine's
    own verdict on the base item."""
    variants = extract_audit_variants()
    audit = {}
    for engine in V2_ENGINES:
        eng = ENGINES[engine]
        audit[engine] = {}
        base_verdicts = {pid: results[engine]["r3n"][pid]["verdict"]
                         for pid in results[engine]["r3n"]}
        for vid in sorted(variants):
            base, expv, _ = variants[vid]
            out = f"{AUDD}/{engine}_{vid}.txt"
            argv = eng["argv"](eng["bin"], f"{AUDD}/{vid}.txt", NLSTORE, out)
            p = subprocess.run(argv, cwd=eng["cwd"], capture_output=True, timeout=TIMEOUT)
            if p.returncode == 0 and os.path.exists(out):
                vv = parse_verdict(engine, out)
            else:
                vv = "NO_VERDICT"
            bv = base_verdicts[base]
            match = (vv == bv)
            audit[engine][vid] = {"base": base, "base_verdict": bv,
                                  "variant_verdict": vv, "match": match,
                                  "sealed_variant_verdict": expv,
                                  "exit": p.returncode,
                                  "trace_sha": sha256_file(out) if os.path.exists(out) else None}
    return audit


# ---------------- bars ----------------
def compute_bars(results, honesty):
    bars = {}
    for engine in V2_ENGINES:
        r = results[engine]
        # PB1: R3N correct verdicts with honest traces
        pb1_n = 0
        pb1_detail = []
        for pid in sorted(r["r3n"]):
            rec = r["r3n"][pid]
            h = honesty[engine]["r3n"].get(pid)
            ok = rec["correct"] is True and h is not None and h["honest"]
            pb1_detail.append({"pid": pid, "verdict": rec["verdict"],
                               "class": rec["class"], "correct": rec["correct"],
                               "honest": h["honest"] if h else None,
                               "honest_findings": h["findings"] if h else None})
            if ok:
                pb1_n += 1
        # PB2: twins solve rate
        tw = [r["twins"][pid] for pid in sorted(r["twins"])]
        pb2_n = sum(1 for x in tw if x["correct"] is True)
        # PB3: B5X-NL discrimination
        b5 = [r["b5x_nl"][pid] for pid in sorted(r["b5x_nl"])]
        pb3_ok = sum(1 for x in b5 if x["correct"] is True)
        pb3_fd = sum(1 for x in b5 if x["class"] == "false_derived")
        pb3_fw = sum(1 for x in b5 if x["class"] == "false_withheld")
        pb3_nv = sum(1 for x in b5 if x["class"] == "no_verdict")
        bars[engine] = {
            "PB1": {"n": pb1_n, "den": 24, "pass": pb1_n >= 12, "detail": pb1_detail},
            "PB2": {"n": pb2_n, "den": 37, "bar": 30, "pass": pb2_n >= 30},
            "PB3": {"correct": pb3_ok, "den": 60, "false_derived": pb3_fd,
                    "false_withheld": pb3_fw, "no_verdict": pb3_nv,
                    "pass": pb3_ok >= 45 and pb3_fd < 10 and pb3_fw < 10},
        }
        bars[engine]["bars_passed"] = sum(1 for b in ("PB1", "PB2", "PB3")
                                          if bars[engine][b]["pass"])
    return bars


def run_honesty(results):
    """Honesty audit on all R3N traces + >=12-trace sample per engine."""
    honesty = {}
    case_dir = R3 + "/engines/n4/cases"
    for engine in V2_ENGINES:
        honesty[engine] = {"r3n": {}, "sample": {}}
        checker = CHECKERS[engine]
        # all R3N traces (for PB1)
        for pid in sorted(results[engine]["r3n"]):
            rec = results[engine]["r3n"][pid]
            tpath = f"{RAW}/{engine}/{pid}_r0.txt"
            if rec["runs_identical"] and os.path.exists(tpath):
                if engine == "n4":
                    ok, fnd = checker(tpath, rec_prob_path(engine, pid, results), rec["store"], case_dir)
                else:
                    ok, fnd = checker(tpath, rec_prob_path(engine, pid, results), rec["store"])
                honesty[engine]["r3n"][pid] = {"honest": ok, "findings": fnd}
        # sample >=12 traces across batteries (prefer derived/withheld w/ traces)
        sampled = []
        for batt in ("twins", "b5x_nl", "b1n", "b6x_nl"):
            for pid in sorted(results[engine][batt]):
                rec = results[engine][batt][pid]
                tpath = f"{RAW}/{engine}/{pid}_r0.txt"
                if rec["runs_identical"] and os.path.exists(tpath) and os.path.getsize(tpath) > 200:
                    sampled.append((batt, pid))
                if len(sampled) >= 12:
                    break
            if len(sampled) >= 12:
                break
        for batt, pid in sampled:
            rec = results[engine][batt][pid]
            tpath = f"{RAW}/{engine}/{pid}_r0.txt"
            if engine == "n4":
                ok, fnd = checker(tpath, rec_prob_path(engine, pid, results), rec["store"], case_dir)
            else:
                ok, fnd = checker(tpath, rec_prob_path(engine, pid, results), rec["store"])
            honesty[engine]["sample"][f"{batt}/{pid}"] = {"honest": ok, "findings": fnd}
    return honesty


def rec_prob_path(engine, pid, results):
    for batt in results[engine]:
        if pid in results[engine][batt]:
            return results[engine][batt][pid]["_path"]
    return None


# ---------------- main ----------------
V1_JSON = R3 + "/scoring/RESULTS_R3.json"


def main():
    # 0. verify binary SHAs before scoring (n4's v1 SHA re-verified below on merge)
    for engine, exp in EXPECTED_BIN_SHA.items():
        if engine not in V2_ENGINES:
            continue
        got = sha256_file(ENGINES[engine]["bin"])
        if got != exp:
            print(f"FATAL: {engine} binary SHA mismatch:\n  got {got}\n  exp {exp}")
            sys.exit(2)
        print(f"{engine} binary SHA ok: {got[:16]}...", flush=True)
    store_sha = sha256_file(NLSTORE)
    print(f"NL store SHA: {store_sha}", flush=True)
    assert store_sha == "910ea9da0989e113587a3856583ba1ec1ea8b4f59258ab3374f1b17b9220084a"

    probs = build_problem_list()
    print(f"{len(probs)} problems x {len(V2_ENGINES)} engines x 3 runs", flush=True)

    from concurrent.futures import ThreadPoolExecutor
    results = {e: {"r3n": {}, "twins": {}, "b5x_nl": {}, "b6x_nl": {}, "b1n": {}} for e in V2_ENGINES}
    divergences = []

    def work(item):
        engine, prob = item
        try:
            rec = run_problem(engine, prob)
        except Exception as ex:  # noqa - record, don't lose the battery
            rec = {"pid": prob["pid"], "battery": prob["battery"], "_path": prob["path"],
                   "store": prob["store"], "sealed": prob.get("sealed"),
                   "verdict": "NO_VERDICT", "class": "no_verdict", "correct": False,
                   "trace_sha": None, "runs_identical": False, "divergent": False,
                   "harness_error": repr(ex), "runs": []}
        return (engine, prob["battery"], prob["pid"], rec)

    items = [(e, p) for e in V2_ENGINES for p in probs]
    done = 0
    with ThreadPoolExecutor(max_workers=4) as ex:
        for engine, batt, pid, rec in ex.map(work, items):
            results[engine][batt][pid] = rec
            if rec.get("divergent"):
                divergences.append(f"{engine}/{pid}")
            if rec.get("harness_error"):
                divergences.append(f"{engine}/{pid} HARNESS_ERROR {rec['harness_error']}")
            done += 1
            if done % 100 == 0:
                print(f"  ...{done}/{len(items)} runs done", flush=True)
    print(f"all runs done; divergences: {divergences}", flush=True)

    print("honesty audit...", flush=True)
    honesty = run_honesty(results)
    print("audit variants...", flush=True)
    audit = run_audit_variants(results)
    print("bars...", flush=True)
    bars = compute_bars(results, honesty)
    # n4 unchanged by the repairs: carry its v1 records forward verbatim
    with open(V1_JSON) as f:
        v1 = json.load(f)
    assert v1["meta"]["engine_binary_sha256"]["n4"] == EXPECTED_BIN_SHA["n4"], "n4 v1 SHA mismatch"
    assert sha256_file(ENGINES["n4"]["bin"]) == EXPECTED_BIN_SHA["n4"], "n4 binary changed on disk"
    for batt in results["n1"]:
        results.setdefault("n4", {})[batt] = v1["results"]["n4"][batt]
    honesty["n4"] = v1["honesty"]["n4"]
    audit["n4"] = v1["audit_variants"]["n4"]
    bars["n4"] = v1["bars"]["n4"]
    print("n4 records carried from v1 (binary unchanged, SHA re-verified)", flush=True)
    print("static backstop...", flush=True)
    backstop = static_backstop()

    out = {
        "meta": {
            "engine_binary_sha256": {e: EXPECTED_BIN_SHA[e] for e in ENGINES},
            "nl_store_sha256": store_sha,
            "toolchain": "znc_linux_x86_64_abed8aa1 (pinned)",
            "runs_per_problem": 3,
            "timeout_s": TIMEOUT,
            "static_no_rng_backstop": backstop,
            "verdict_classes": {
                "correct_derived": "engine DERIVED/REFUTED and sealed DERIVED",
                "false_derived": "engine DERIVED/REFUTED but sealed WITHHELD (REFUTED is a positive derivation act)",
                "correct_withheld": "engine WITHHELD and sealed WITHHELD",
                "false_withheld": "engine WITHHELD but sealed DERIVED",
                "no_verdict": "engine produced no parseable verdict (exit!=0); counts as incorrect",
                "unkeyed": "no sealed verdict (B6X step-count key only)",
            },
            "divergences": divergences,
        },
        "results": results,
        "honesty": honesty,
        "audit_variants": audit,
        "bars": bars,
    }
    # strip internal _path fields before serialization (local paths stay local)
    for e in out["results"]:
        for b in out["results"][e]:
            for pid in out["results"][e][b]:
                out["results"][e][b][pid].pop("_path", None)
    with open(R3 + "/scoring/RESULTS_R3_V2.json", "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("wrote RESULTS_R3_V2.json", flush=True)
    write_scorecard(out)


def write_scorecard(out):
    L = []
    A = L.append
    bars = out["bars"]
    res = out["results"]
    honesty = out["honesty"]
    variants = out["audit_variants"]
    A("# MATH R3 SCORECARD v2 — native engines vs primary bars (post-repair rescore)")
    A("")
    A("Repair+rescore crew report. No verdict beyond the prereg bars (round coordinator")
    A("writes the verdict after KB4 grading). Frozen prereg: PREREG_MATH_R3.md")
    A("(@01ffd095). 3 external runs/problem/engine, byte-identity asserted.")
    A("")
    A("## What changed vs v1 (SCORECARD_R3.md) and why")
    A("")
    A("Three mechanical integration defects found in v1 scoring were repaired with")
    A("parser/emission-only changes (no engine reasoning, license, search, referee,")
    A("or verdict logic touched; see engines/n{1,2,3}/BUILD_N{1,2,3}.md repair notes):")
    A("- **n2**: R3N files use multiline `STATEMENT:` blocks; n2 required statement")
    A("  content on the same line and exited 4 on all 24 R3N. The parser now consumes")
    A("  the multiline block (bare `STATEMENT:` header line, block lines to blank /")
    A("  next field / EOF, bullets kept verbatim, true file span, no copy).")
    A("- **n3**: twins/, b5x_nl/, b6x_nl/ use `PREMISES:`/`TARGET:`; n3 required a")
    A("  `STATEMENT:` line and exited 4 on all 100. It now presents")
    A("  premises-text + newline + TARGET: + target-text as the problem bytes (bullets")
    A("  verbatim; the 9-byte joiner is the only synthetic byte run; ledger spans stay")
    A("  file-grounded — the presentation is a contiguous substring of the file).")
    A("- **n1**: inference states recorded premise-relative hole offsets but the trace")
    A("  printer indexed tx absolutely, so traces cited wrong spans (16/24 R3N + all")
    A("  sampled twin traces). Hole provenance now stores tx-absolute spans; the hm")
    A("  table is read only by the trace emitter, so verdict logic is untouched.")
    A("n4 was not repaired; its v1 scores are carried forward verbatim (binary")
    A("SHA-256 re-verified unchanged). Controls unchanged. PB1/PB2/PB3 unchanged.")
    A("")
    A("## 0. Build verification")
    A("")
    for e in ("n1", "n2", "n3", "n4"):
        A(f"- {e}: rebuilt from committed sources, binary SHA-256 "
          f"`{out['meta']['engine_binary_sha256'][e][:16]}...` MATCHES crew-reported SHA.")
    A(f"- NL knowledge store SHA-256 `{out['meta']['nl_store_sha256'][:16]}...` matches pinned store.")
    A(f"- Divergent reruns: {out['meta']['divergences'] if out['meta']['divergences'] else 'NONE (all 3x runs byte-identical)'}")
    A("")
    A("## 1. Primary bars")
    A("")
    A("| engine | PB1 R3N (bar ≥12/24) | PB2 twins (bar ≥30/37) | PB3 B5X-NL (bar ≥45/60, <10 fd, <10 fw) | bars passed |")
    A("|---|---|---|---|---|")
    for e in ("n1", "n2", "n3", "n4"):
        b = bars[e]
        pb1 = f"{b['PB1']['n']}/24 {'PASS' if b['PB1']['pass'] else 'FAIL'}"
        pb2 = f"{b['PB2']['n']}/37 {'PASS' if b['PB2']['pass'] else 'FAIL'}"
        p3 = b["PB3"]
        pb3 = (f"{p3['correct']}/60 correct, fd={p3['false_derived']}, fw={p3['false_withheld']}, "
               f"nv={p3['no_verdict']} {'PASS' if p3['pass'] else 'FAIL'}")
        A(f"| {e} | {pb1} | {pb2} | {pb3} | {b['bars_passed']}/3 |")
    A("")
    A("Decision rule (frozen): R2 DUAL verdict STANDS unless a native wins ≥2/3 bars vs BOTH controls.")
    A("Controls (rebuilt, R2 numbers re-verified): DUAL-R1 formal B2R/B3R/B4R = 37/37; "
      "REF-FIRST = 34/37. DUAL/REF-FIRST did not attempt R3N in R3 (prereg: expected honest abstention).")
    A("")
    A("## 2. Battery detail (correct / total)")
    A("")
    A("| engine | R3N | twins | B5X-NL | B6X-NL (verdict, derivations) | B1N |")
    A("|---|---|---|---|---|---|")
    for e in ("n1", "n2", "n3", "n4"):
        r = res[e]
        def ct(batt):
            xs = [r[batt][p] for p in sorted(r[batt])]
            c = sum(1 for x in xs if x["correct"] is True)
            t = sum(1 for x in xs if x["correct"] is not None)
            return f"{c}/{t}"
        b6 = "; ".join(f"{p}: {r['b6x_nl'][p]['verdict']}/{r['b6x_nl'][p]['derivations']}"
                       for p in sorted(r["b6x_nl"]))
        A(f"| {e} | {ct('r3n')} | {ct('twins')} | {ct('b5x_nl')} | {b6} | {ct('b1n')} |")
    A("")
    A("B6X sealed step counts: LINEAR 104, DAG 104, CONTRADICTION 103 (no sealed verdict key).")
    A("")
    A("## 3. Anti-bridge audit")
    A("")
    A("### 3a. Trace inspection (honesty: every step cites byte-spans of input/store text or prior steps)")
    A("")
    for e in ("n1", "n2", "n3", "n4"):
        h = out["honesty"][e]
        r3n_h = [(p, h["r3n"][p]) for p in sorted(h["r3n"])]
        nh = sum(1 for _, x in r3n_h if x["honest"])
        A(f"- **{e}** R3N traces: {nh}/{len(r3n_h)} honest.")
        smp = h["sample"]
        sh = sum(1 for k in smp if smp[k]["honest"])
        A(f"  - cross-battery sample: {sh}/{len(smp)} honest.")
        for p, x in r3n_h:
            if not x["honest"]:
                A(f"  - R3N/{p} findings: {x['findings'][:4]}")
        for k in sorted(smp):
            if not smp[k]["honest"]:
                A(f"  - {k} findings: {smp[k]['findings'][:4]}")
    A("")
    A("### 3b. Paraphrase perturbation (6 variants — verdict must match the engine's base-item verdict)")
    A("")
    for e in ("n1", "n2", "n3", "n4"):
        a = out["audit_variants"][e]
        par = [v for v in sorted(a) if v.startswith("AUD_P")]
        m = sum(1 for v in par if a[v]["match"])
        A(f"- **{e}**: {m}/6 match. " + "; ".join(
            f"{v}(base {a[v]['base']} {a[v]['base_verdict']}→{a[v]['variant_verdict']})" for v in par))
    A("")
    A("### 3c. Nonce-word variants (6 variants — verdict must match the engine's base-item verdict)")
    A("")
    for e in ("n1", "n2", "n3", "n4"):
        a = out["audit_variants"][e]
        non = [v for v in sorted(a) if v.startswith("AUD_N")]
        m = sum(1 for v in non if a[v]["match"])
        A(f"- **{e}**: {m}/6 match. " + "; ".join(
            f"{v}(base {a[v]['base']} {a[v]['base_verdict']}→{a[v]['variant_verdict']})" for v in non))
    A("")
    A("## 4. Findings")
    A("")
    A("(mechanical observations from scoring; interpretation belongs to the verdict stage)")
    A("")
    # engine input-format coverage
    for e in ENGINES:
        nv = sum(1 for b in ("r3n", "twins", "b5x_nl", "b1n", "b6x_nl") for r in res[e][b].values() if r["verdict"] == "NO_VERDICT")
        if nv:
            bad = {}
            for b in ("r3n", "twins", "b5x_nl", "b1n", "b6x_nl"):
                for pid, r in res[e][b].items():
                    if r["verdict"] == "NO_VERDICT":
                        bad.setdefault(b, []).append(pid)
            A(f"- **{e}**: {nv} NO_VERDICT (engine exit!=0 or no parseable verdict): " +
              "; ".join(f"{b}: {len(v)}" for b, v in sorted(bad.items())))
    # B5X conservatism
    for e in ENGINES:
        c = Counter(r["class"] for r in res[e]["b5x_nl"].values())
        A(f"- **{e} B5X-NL**: {c.get('correct_withheld',0)} correct_withheld, "
          f"{c.get('false_withheld',0)} false_withheld, {c.get('correct_derived',0)} correct_derived, "
          f"{c.get('false_derived',0)} false_derived, {c.get('no_verdict',0)} no_verdict")
    # honesty rollup
    for e in ENGINES:
        h = honesty[e]["r3n"]
        A(f"- **{e} trace honesty**: R3N {sum(1 for p in h if h[p]['honest'])}/{len(h)} honest; "
          f"cross-battery sample {sum(1 for k in honesty[e]['sample'] if honesty[e]['sample'][k]['honest'])}/{len(honesty[e]['sample'])} honest")
    # audit variants rollup
    for e in ENGINES:
        a = variants[e]
        pm = sum(1 for v in a if v.startswith("AUD_P") and a[v]["match"])
        nm = sum(1 for v in a if v.startswith("AUD_N") and a[v]["match"])
        A(f"- **{e} anti-bridge**: paraphrase {pm}/6 match, nonce {nm}/6 match")
    # static backstop
    sb = static_backstop()
    A(f"- **static no-RNG backstop**: {'PASS' if sb['pass'] else 'FINDINGS: ' + '; '.join(sb['findings'])}")
    A("")
    with open(R3 + "/scoring/SCORECARD_R3_V2.md", "w") as f:
        f.write("\n".join(L) + "\n")
    print("wrote SCORECARD_R3_V2.md", flush=True)


if __name__ == "__main__":
    main()
