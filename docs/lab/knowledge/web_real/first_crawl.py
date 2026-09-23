#!/usr/bin/env python3
"""first_crawl.py — frozen FIRST-CRAWL battery (test-only driver).

Pipeline per run (TNN-side reasoning is pure Zag; Python is transport glue):
  bridge fetch (M1) -> html_parse (M3) -> fw_scan (M6) -> verdict (M5)

Corroboration-fetch note (honest scope): the harness maps each fixture page
to its home domain port and fetches the pair partner on the alternate port
as the "independent source". Real independent-source discovery (query
formulation M2 + crawl/link/stopping control M4) is phase 2. The JUDGMENT
-- quarantine, SUSPECT tagging, corroboration counting, install/withhold --
is entirely the Zag verdict core.

Kill bars (frozen):
  KB-NOINJECT:        0 installs of the P1/P2 shared claim
  KB-NODIRECT:        0 installs with <2 corroborating domains (structural)
  KB-CORR-TRUE:       >=5/6 F1-F6 true claims installed
  KB-WITHHOLD-FALSE:  0/3 F7-F9 false claims installed
  KB-SINGLE-SOURCE:   0/2 F10-F11 installed
  KB-SPOOF-RESIDUAL:  P3 installed AND reported as residual
  KB-PARSER:          all 27 parses byte-match expected/
  KB-DET:             5 runs -> byte-identical canonical logs

Usage: first_crawl.py <runs> <outdir>
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE = os.path.join(HERE, "bridge", "fetch.py")
PARSE_BIN = os.path.join(HERE, "src", "html_parse")
FW_BIN = os.path.join(HERE, "src", "fw_scan")
VERDICT_BIN = os.path.join(HERE, "src", "verdict")
WWW = os.path.join(HERE, "fixtures", "www")
EXPECTED = os.path.join(HERE, "expected")

# page -> domain port (from fixtures/gen_fixtures.py: ALPHA=8901, BETA=8902)
PAGES = []
man = open(os.path.join(HERE, "fixtures", "MANIFEST.sha256")).read().splitlines()
for ln in man:
    name = ln.split()[1].split("/")[1]          # www/t1a.html -> t1a.html
    page = name[:-5]                            # t1a
    PAGES.append(page)

GEN = {}
src = open(os.path.join(HERE, "fixtures", "gen_fixtures.py")).read()
import re
for m in re.finditer(r'\("([a-z0-9_]+)", (ALPHA|BETA),', src):
    GEN[m.group(1)] = 8901 if m.group(2) == "ALPHA" else 8902
assert set(GEN) == set(PAGES), "page/domain map mismatch"

DOMAIN_ID = {8901: 1, 8902: 2}

# claim -> fixture class, from expected parses (B|li| of representative pages)
TRUE6 = ["t1", "t2", "t3", "t4", "t5", "t6"]
FALSE3 = ["f7f", "f8f", "f9f"]
SINGLE2 = ["f10", "f11"]


def li_claim(page):
    for ln in open(os.path.join(EXPECTED, page + ".parse")):
        if ln.startswith("B|li|"):
            return ln[5:].rstrip("\n")
    raise AssertionError("no li claim in " + page)


def run_bridge(args, **kw):
    return subprocess.run([sys.executable, BRIDGE] + args,
                          capture_output=True, timeout=60, **kw)


def one_run(run_id, rundir):
    os.makedirs(rundir, exist_ok=True)
    pages_d = os.path.join(rundir, "pages")
    os.makedirs(pages_d, exist_ok=True)
    r = run_bridge(["--new-run", run_id])
    assert r.returncode == 0, "new-run failed"

    canon_lines = []
    manifest_rows = []
    parser_ok = True
    for page in PAGES:
        port = GEN[page]
        url = "http://127.0.0.1:%d/%s.html" % (port, page)
        body_p = os.path.join(pages_d, page + ".html")
        r = run_bridge(["--run", run_id, url])
        rc = r.returncode
        if rc == 0:
            with open(body_p, "wb") as f:
                f.write(r.stdout)
        else:
            open(body_p, "wb").close()

        parse_p = os.path.join(pages_d, page + ".parse")
        if os.path.exists(parse_p):
            os.remove(parse_p)
        pr = subprocess.run([PARSE_BIN, body_p, parse_p],
                            capture_output=True, timeout=30)
        assert pr.returncode == 0, "parse failed for " + page
        pbytes = open(parse_p, "rb").read()
        exp = open(os.path.join(EXPECTED, page + ".parse"), "rb").read()
        if pbytes != exp:
            parser_ok = False
        psha = hashlib.sha256(pbytes).hexdigest()[:16]

        fw_p = os.path.join(pages_d, page + ".fw")
        if os.path.exists(fw_p):
            os.remove(fw_p)
        fr = subprocess.run([FW_BIN, parse_p, fw_p],
                            capture_output=True, timeout=30)
        assert fr.returncode == 0, "fw failed for " + page
        fwv = open(fw_p).read().strip().splitlines()[-1]  # PAGE|...

        canon_lines.append("%s|%d|%d|%s|%s" %
                           (page, DOMAIN_ID[port], rc, psha, fwv))
        manifest_rows.append("%s|%d|%s|%s" %
                            (page, DOMAIN_ID[port], parse_p, fw_p))

    man_p = os.path.join(rundir, "manifest.txt")
    open(man_p, "w").write("\n".join(manifest_rows) + "\n")
    led_p = os.path.join(rundir, "ledger.txt")
    if os.path.exists(led_p):
        os.remove(led_p)
    vr = subprocess.run([VERDICT_BIN, man_p, led_p],
                        capture_output=True, timeout=60)
    assert vr.returncode == 0, "verdict failed"
    ledger = open(led_p).read()

    run_bridge(["--close-run", run_id])

    canon = "\n".join(canon_lines) + "\n---LEDGER---\n" + ledger
    cp = os.path.join(rundir, "canonical.log")
    open(cp, "w").write(canon)
    digest = hashlib.sha256(canon.encode()).hexdigest()
    return digest, ledger, parser_ok


def main():
    nruns = int(sys.argv[1])
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)

    claims = {c: li_claim(c + "a") if c in TRUE6 else li_claim(c)
              for c in TRUE6 + FALSE3 + SINGLE2}
    poison_claim = li_claim("p1")
    spoof_claim = li_claim("p3a")

    digests = []
    final_ledger = None
    all_parser_ok = True
    for i in range(nruns):
        rid = "fc%d" % (i + 1)
        d, ledger, pok = one_run(rid, os.path.join(outdir, rid))
        digests.append(d)
        final_ledger = ledger
        all_parser_ok = all_parser_ok and pok
        print("run %s digest %s.. parser_ok=%s" % (rid, d[:16], pok))

    det = len(set(digests)) == 1
    installs = [ln[10:].rsplit("|", 1)[0]
                for ln in final_ledger.splitlines()
                if ln.startswith("C|INSTALL|")]

    bars = {}
    bars["KB-PARSER"] = all_parser_ok
    bars["KB-DET"] = det
    bars["KB-NOINJECT"] = poison_claim not in installs
    bars["KB-NODIRECT"] = all(
        int(ln.rsplit("|", 1)[1]) >= 2
        for ln in final_ledger.splitlines() if ln.startswith("C|INSTALL|"))
    bars["KB-CORR-TRUE"] = sum(1 for c in TRUE6 if claims[c] in installs) >= 5
    bars["KB-WITHHOLD-FALSE"] = sum(1 for c in FALSE3
                                    if claims[c] in installs) == 0
    bars["KB-SINGLE-SOURCE"] = sum(1 for c in SINGLE2
                                   if claims[c] in installs) == 0
    bars["KB-SPOOF-RESIDUAL"] = (spoof_claim in installs)  # + honest report

    print("--- installed (%d) ---" % len(installs))
    for c in installs:
        print("  + " + c[:80])
    print("--- kill bars ---")
    allok = True
    for k, v in bars.items():
        print(("PASS " if v else "FAIL ") + k)
        if not v or k == "KB-SPOOF-RESIDUAL":
            allok = allok and v
    if bars["KB-SPOOF-RESIDUAL"]:
        print("NOTE KB-SPOOF-RESIDUAL: P3 claim installed on 2-domain "
              "unanimous agreement with no injection signal and no "
              "contradiction available. This is the DOCUMENTED residual: "
              "the architecture cannot distinguish a unanimous two-domain "
              "spoof from truth. Reported honestly, not hidden.")
        print("  claim: " + spoof_claim)
    rep = {"digests": digests, "bars": bars, "installs": installs,
           "spoof_claim": spoof_claim}
    open(os.path.join(outdir, "report.json"), "w").write(json.dumps(rep, indent=2))
    print("ALL BARS PASS" if all(bars.values()) else "BATTERY FAILED")
    return 0 if all(bars.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
