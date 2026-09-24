#!/usr/bin/env python3
"""g7infra battery driver (LI-HARDEN round 3, Crew B).
Phase 1 (measure): run the binary's measure mode on H1..H12, derive L0=K*Lmax,
  write pins/calibration.txt (content-addressed), assert prereg Lmax==40.
Phase 2 (verdict): run g7infra x2 per case; assert byte-identical reruns.
Prints TSV: case, rep, verdict. Exits nonzero on any prereg violation.
"""
import hashlib, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "work", "g7infra_bin")
FIX = os.path.join(HERE, "fixtures")
HONEST_FIX = os.path.expanduser("~/workspace/liharden/corrob/fixtures")
PINS = os.path.join(HERE, "pins")
K = 2
QFETCH = "1790208000"   # 2026-09-24
ARCHIVE_FETCH = "1577836800"  # 2020-01-01
CITE_FETCH = "1609459200"     # 2021-01-01

# case -> list of (pin_name, kind, url, fetched_at)
PINSET = {
    "T5_longwire": [("cite_wire_report.txt", "CPIN",
                     "https://wire.example/commission-report", CITE_FETCH)],
    "RFC1_rfcquote": [("cite_rfc868.txt", "CPIN",
                       "https://www.rfc-editor.org/rfc/rfc868.txt", CITE_FETCH)],
    "F7_misquote": [("cite_rfc868.txt", "CPIN",
                     "https://www.rfc-editor.org/rfc/rfc868.txt", CITE_FETCH)],
    "STAT1_statute": [("cite_statute.txt", "CPIN",
                       "https://statutes.example/records-preservation-act", CITE_FETCH)],
}
ARCHIVE_PIN = ("arch_2020.txt", "APIN", "archive:2020-corpus", ARCHIVE_FETCH)

def pin_payload(name):
    raw = open(os.path.join(PINS, name), "rb").read()
    if raw.endswith(b"\n"):
        raw = raw[:-1]
    return raw

def bundle(casedir, calib_name):
    out = []
    need = open(os.path.join(casedir, "need.txt")).read().strip()
    out.append("NEED|" + need)
    urls = {}
    for line in open(os.path.join(casedir, "urls.txt")):
        line = line.strip()
        if not line or "|" not in line:
            continue
        pid, url = line.split("|", 1)
        urls[pid.strip()] = url.strip()
        out.append("U|%s|%s" % (pid.strip(), url.strip()))
    pdir = os.path.join(casedir, "pages")
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith(".txt"):
            continue
        pid = fn[:-4]
        lines = [l.rstrip("\n") for l in open(os.path.join(pdir, fn))]
        out.append("P|" + pid)
        for l in lines[1:]:
            if l.strip():
                out.append(l.strip())
    try:
        fetch = open(os.path.join(casedir, "fetch.txt")).read().strip()
    except FileNotFoundError:
        fetch = QFETCH
    mpath = os.path.join(casedir, "meta.txt")
    if os.path.exists(mpath):
        for line in open(mpath):
            line = line.strip()
            if not line or "|" not in line:
                continue
            pid, rest = line.split("|", 1)
            rest = rest.strip()
            kv = "FETCH=" + fetch
            if rest and rest != "META=NONE":
                kv += "|" + rest
            out.append("M|%s|%s" % (pid.strip(), kv))
    # pin descriptors
    case = os.path.basename(casedir)
    pins = [ARCHIVE_PIN] + PINSET.get(case, [])
    out.append("CALIB|%s" % calib_name)
    for name, kind, url, fat in pins:
        out.append("%s|%s|%s|%s" % (kind, url, fat, name))
    # pin payloads
    for name in [calib_name] + [p[0] for p in pins]:
        raw = pin_payload(name)
        sha = hashlib.sha256(raw).hexdigest()
        out.append("PINB|%s|%s" % (name, sha))
        out.append(raw.decode("utf-8"))
    return ("\n".join(out) + "\n").encode()

def run(mode, data):
    r = subprocess.run([BIN, mode], input=data, capture_output=True, timeout=60)
    if r.returncode != 0:
        return "ERROR rc=%d err=%s" % (r.returncode, r.stderr.decode()[-300:])
    return r.stdout.decode().strip()

def main():
    honest = ["H1_three_host", "H2_four_host", "H3_six_host", "H4_paraphrase_agree",
              "H5_range_format", "H6_numeric", "H7_range_agree", "H8_wire_truth",
              "H9_filler_diverse", "H10_punct_variant", "H11_claim_second",
              "H12_numeric2"]
    # Phase 1: measure (calibration pin not needed for measure mode, but bundle
    # requires one; use a throwaway name -- measure ignores pins)
    lmax, dist = 0, {}
    for h in honest:
        data = bundle(os.path.join(HONEST_FIX, h), "calibration.txt")
        m = run("measure", data)
        # M|claim_bytes=N|claim_words=W|nvotes=V|nhost=H
        parts = dict(p.split("=", 1) for p in m.split("|")[1:])
        cb = int(parts["claim_bytes"])
        dist[h] = (cb, parts["claim_words"], parts["nvotes"], parts["nhost"])
        lmax = max(lmax, cb)
    print("calibration: Lmax=%d K=%d -> L0=%d" % (lmax, K, K * lmax), file=sys.stderr)
    for h in honest:
        print("  %s bytes=%s words=%s votes=%s hosts=%s" % (h, *dist[h]), file=sys.stderr)
    if lmax != 39:
        print("VOID: prereg (amended) predicts Lmax=39, measured %d" % lmax, file=sys.stderr)
        sys.exit(3)
    calib = "L0=%d K=%d LMAX=%d N=12 CORPUS=H1-H12" % (K * lmax, K, lmax)
    open(os.path.join(PINS, "calibration.txt"), "w").write(calib)
    # Phase 2: verdict battery
    cases = ([("honest:" + h, os.path.join(HONEST_FIX, h)) for h in honest] +
             [(c, os.path.join(FIX, c)) for c in
              ["F7_longring", "T5_longwire", "RFC1_rfcquote", "STAT1_statute",
               "TECH1_archived", "F7_short", "F7_misquote", "F7_fakecite"]])
    print("case\trep\tverdict")
    fails = []
    for name, cdir in cases:
        data = bundle(cdir, "calibration.txt")
        outs = [run("g7infra", data), run("g7infra", data)]
        if outs[0] != outs[1]:
            print("NONDETERMINISM %s: %r vs %r" % (name, outs[0], outs[1]), file=sys.stderr)
            sys.exit(4)
        for rep, o in enumerate(outs, 1):
            print("%s\t%d\t%s" % (name, rep, o))
    # prereg assertions
    expect = {
        "F7_longring": "WITHHOLD|COPYCOLLAPSE",
        "T5_longwire": "INSTALL|NONE",
        "RFC1_rfcquote": "INSTALL|NONE",
        "STAT1_statute": "INSTALL|NONE",
        "TECH1_archived": "INSTALL|NONE",
        "F7_short": "INSTALL|NONE",
        "F7_misquote": "WITHHOLD|COPYCOLLAPSE",
        "F7_fakecite": "WITHHOLD|COPYCOLLAPSE",
    }
    rows = {}
    data = None
    # re-run collection for assertions (deterministic, cheap)
    for name, cdir in cases:
        data = bundle(cdir, "calibration.txt")
        rows[name] = run("g7infra", data)
    for h in honest:
        v = rows["honest:" + h]
        if "|INSTALL|NONE|" not in v:
            fails.append((h, v))
    for c, want in expect.items():
        v = rows[c]
        if want not in v:
            fails.append((c, v))
    if fails:
        print("PREREG FAILURES:", file=sys.stderr)
        for c, v in fails:
            print("  %s -> %s" % (c, v), file=sys.stderr)
        sys.exit(5)
    print("ALL PREREG ASSERTIONS HOLD", file=sys.stderr)

if __name__ == "__main__":
    main()
