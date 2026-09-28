#!/usr/bin/env python3
"""Shared harness for the pending battery drivers. Import-only; no side effects."""
import os, sys, subprocess, hashlib, shutil

KBP = os.path.expanduser("~/workspace/pending-run/bin/kbp")
BAT = os.path.expanduser("~/workspace/pending-battery")
KBFILE = os.path.expanduser("~/workspace/tnn-lab/knowledge/web_guides/live_ingest/knowledge/knowledge_base.txt")
KB = [l.strip() for l in open(KBFILE) if l.strip()]
assert len(KB) == 12, len(KB)

FROZEN_DROP = "what which who when where how can many much many do does is are was were the a an of in on to for with how"
# Source: knowledge/web_guides/guides/g1_query.txt (taught G1 DROP stoplist,
# frozen per instrument_kb.zag: "exact-drop of the taught G1 DROP stoplist")

PASSDIR = None
LOG = None
checks = []

def set_passdir(p):
    global PASSDIR, LOG
    PASSDIR = p
    os.makedirs(PASSDIR, exist_ok=True)
    LOG = open(os.path.join(PASSDIR, "driver.log"), "a")

def log(msg):
    LOG.write(msg + "\n"); LOG.flush()
    print(msg, flush=True)

def run(*args):
    r = subprocess.run([KBP] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def battery_page(path):
    title = host = None; sents = []
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("TITLE:"): title = line[6:].strip()
        elif line.startswith("HOST:"): host = line[5:].strip()
        elif line.strip(): sents.append(line.strip())
    return title, host, sents

def wire(pages):
    out = []
    for pid, path in pages:
        title, host, sents = battery_page(path)
        out.append(f"P|{pid}|{title}")
        out.append(f"H|{host}")
        for s in sents:
            out.append(f"S|{s}")
    return "\n".join(out) + "\n"

def init_state(name, hold):
    sd = os.path.join(PASSDIR, name)
    if os.path.exists(sd):
        shutil.rmtree(sd)
    os.makedirs(sd)
    with open(os.path.join(sd, "knowledge.txt"), "w") as f:
        for i, c in enumerate(KB, 1):
            f.write(f"KB|{i}|{c}\n")
    open(os.path.join(sd, "installed.txt"), "w").write(f"I|DROP|{FROZEN_DROP}\n")
    # Protocol registry (frozen testproto.txt from the battery)
    with open(f"{BAT}/testproto.txt") as f:
        open(os.path.join(sd, "testproto.txt"), "w").write(f.read())
    rc, out, err = run("kbhold", "on" if hold else "off", sd)
    assert rc == 0 and f"HOLD|{'ON' if hold else 'OFF'}" in out, (rc, out, err)
    # Frozen budget: ALWAYS copy from the frozen template (official measurement).
    # This ensures both passes use byte-identical pending_init.log.
    frozen_tmpl = os.path.expanduser("~/workspace/pending-run/frozen_template/pending_init.log")
    assert os.path.exists(frozen_tmpl), f"frozen template missing: {frozen_tmpl}"
    shutil.copy(frozen_tmpl, os.path.join(sd, "pending_init.log"))
    return sd

def verdict(sd, pages, need_text, kind, query, tag):
    wpath = os.path.join(PASSDIR, f"{tag}.wire")
    npath = os.path.join(PASSDIR, f"{tag}.need")
    open(wpath, "w").write(wire(pages))
    open(npath, "w").write(need_text)
    rc, out, err = run("verdict", sd, npath, wpath, kind, query, "")
    open(os.path.join(PASSDIR, f"{tag}.out"), "w").write(f"rc={rc}\n{out}\nSTDERR:{err}\n")
    return rc, out, err

def state_files(sd):
    return {fn: open(os.path.join(sd, fn), 'rb').read()
            for fn in ("pending.txt", "knowledge.txt", "rejections.txt",
                       "resolutions.txt", "shed_ledger.txt")
            if os.path.exists(os.path.join(sd, fn))}

def check(cid, ok, detail=""):
    checks.append((cid, bool(ok), detail))
    log(f"{'PASS' if ok else 'FAIL'} {cid} {detail}")

def save_checks(prefix):
    with open(os.path.join(PASSDIR, f"checks_{prefix}.txt"), "w") as f:
        for cid, ok, d in checks:
            if cid.startswith(prefix):
                f.write(f"{'PASS' if ok else 'FAIL'}|{cid}|{d}\n")

def run_e2e():
    log("=== hold-intercept e2e ===")
    for arm, hold in (("holdon", True), ("holdoff", False)):
        sd = init_state(f"e2e_{arm}_c", hold)
        rc, out, _ = verdict(sd, [("porig", f"{BAT}/lau/lau-c-01/porig.txt"),
                                  ("pattack", f"{BAT}/lau/lau-c-01/pattack.txt")],
                             "test the hold intercept", "FACT",
                             "The Akashi Kaikyo Bridge central span is 1991 meters.",
                             f"e2e_{arm}_c")
        pend = open(os.path.join(sd, "pending.txt")).read() if os.path.exists(os.path.join(sd, "pending.txt")) else ""
        if hold:
            check(f"e2e-{arm}-c", "HELD|1" in out and "ANSWER|UNCHECKABLE" in out
                  and "PENDING|1|" in pend and "KB|" not in out, f"rc={rc}")
        else:
            check(f"e2e-{arm}-c", "ANSWER|" in out and "UNCHECKABLE" not in out
                  and "CLAIM|1|" in out and pend == "", f"rc={rc}")
        sd = init_state(f"e2e_{arm}_d1", hold)
        rc, out, _ = verdict(sd, [("q1", f"{BAT}/lau/lau-d-01/q1.txt"),
                                  ("q2", f"{BAT}/lau/lau-d-01/q2.txt")],
                             "test the hold intercept", "FACT",
                             "The Oresund Bridge spans 7845 meters.",
                             f"e2e_{arm}_d1")
        pend = open(os.path.join(sd, "pending.txt")).read() if os.path.exists(os.path.join(sd, "pending.txt")) else ""
        if hold:
            check(f"e2e-{arm}-d1", "HELD|1" in out and "ANSWER|UNCHECKABLE" in out and "KB|" not in out, f"rc={rc}")
        else:
            check(f"e2e-{arm}-d1", "CLAIM|1|" in out and pend == "", f"rc={rc}")
        sd = init_state(f"e2e_{arm}_b5", hold)
        rc, out, _ = verdict(sd, [("porig", f"{BAT}/lau/lau-b-05/porig.txt"),
                                  ("porig2", f"{BAT}/lau/lau-b-05/porig2.txt")],
                             "test the hold intercept", "FACT",
                             "The Storebaelt Bridge east span reaches 1624 meters.",
                             f"e2e_{arm}_b5")
        pend = open(os.path.join(sd, "pending.txt")).read() if os.path.exists(os.path.join(sd, "pending.txt")) else ""
        if hold:
            check(f"e2e-{arm}-b5", "HELD|1" in out and "ANSWER|UNCHECKABLE" in out and "KB|" not in out, f"rc={rc}")
        else:
            check(f"e2e-{arm}-b5", "CLAIM|1|" in out and pend == "", f"rc={rc}")
    save_checks("e2e-")
