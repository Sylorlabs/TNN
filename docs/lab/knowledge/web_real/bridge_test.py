#!/usr/bin/env python3
"""bridge_test.py — M1 bridge verification (test-only)."""
import hashlib
import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
BR = os.path.join(HERE, "bridge", "fetch.py")
CFG = os.path.join(HERE, "bridge", "config.json")

# add an oversize fixture page (not part of frozen manifest; sha256sum -c
# only checks listed files)
BIG = os.path.join(HERE, "fixtures", "www", "big.html")
if not os.path.exists(BIG):
    with open(BIG, "w") as f:
        f.write("<html><body><p>" + "x" * 70000 + "</p></body></html>\n")


class RH(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/redir":
            self.send_response(302)
            self.send_header("Location", "http://127.0.0.1:8903/t1a.html")
            self.end_headers()
            return
        self.send_error(404)


srv = HTTPServer(("127.0.0.1", 8903), RH)
threading.Thread(target=srv.serve_forever, daemon=True).start()

fails = []


def check(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + (" " + extra if extra else ""))
    if not cond:
        fails.append(name)


def run(*args):
    r = subprocess.run([sys.executable, BR] + list(args),
                       capture_output=True, timeout=30)
    return r


# point config at test audit/state dirs (restored afterwards by battery)
run("--new-run", "btest")
r = run("--run", "btest", "http://127.0.0.1:8901/t1a.html")
body = r.stdout
want = open(os.path.join(HERE, "fixtures", "www", "t1a.html"), "rb").read()
check("allowed fetch exit 0", r.returncode == 0, "rc=%d" % r.returncode)
check("body byte-identical", body == want)

bad = [
    ("https scheme", "https://127.0.0.1:8901/t1a.html"),
    ("hostname", "http://localhost:8901/t1a.html"),
    ("alt port", "http://127.0.0.1:8903/t1a.html"),
    ("userinfo", "http://u:p@127.0.0.1:8901/t1a.html"),
    ("fragment", "http://127.0.0.1:8901/t1a.html#x"),
    ("rel path", "t1a.html"),
    ("ipv6", "http://[::1]:8901/t1a.html"),
]
for name, url in bad:
    r = run("--run", "btest", url)
    check("reject %s -> 2, no body" % name,
          r.returncode == 2 and r.stdout == b"", "rc=%d" % r.returncode)

# redirect test needs 8903 temporarily allow-listed (restored right after)
cfg = json.load(open(CFG))
cfg["allow_ports"] = [8901, 8902, 8903]
json.dump(cfg, open(CFG, "w"), indent=2)
r = run("--run", "btest", "http://127.0.0.1:8903/redir")
cfg["allow_ports"] = [8901, 8902]
json.dump(cfg, open(CFG, "w"), indent=2)
check("redirect 302 -> 7, no body, no follow",
      r.returncode == 7 and r.stdout == b"", "rc=%d" % r.returncode)

r = run("--run", "btest", "http://127.0.0.1:8901/big.html")
check("oversize -> 6, no body", r.returncode == 6 and r.stdout == b"",
      "rc=%d" % r.returncode)

r = run("--run", "btest-nope", "http://127.0.0.1:8901/t1a.html")
check("unknown run_id -> 8", r.returncode == 8, "rc=%d" % r.returncode)

# budget: fetch until the bridge-owned counter exhausts (64/run)
r = None
for i in range(70):
    r = run("--run", "btest", "http://127.0.0.1:8901/t2a.html")
    if r.returncode == 3:
        break
check("budget exhausted -> 3", r is not None and r.returncode == 3,
      "rc=%d" % (r.returncode if r else -1))
r = run("--run", "btest", "http://127.0.0.1:8901/t2a.html")
check("budget stays exhausted", r.returncode == 3)

# audit chain verification (independent recomputation)
alog = os.path.join(HERE, "bridge", "_audit_test", "audit.jsonl")
lines = open(alog, encoding="utf-8").read().splitlines()
prev = "00" * 32
okc = True
seq = 1
for ln in lines:
    rec = json.loads(ln)
    if rec["seq"] != seq or rec["prev_hash"] != prev:
        okc = False
        break
    rh = rec["record_hash"]
    h = hashlib.sha256(json.dumps(
        {k: v for k, v in rec.items() if k != "record_hash"},
        sort_keys=True, separators=(",", ":"),
        ensure_ascii=True).encode()).hexdigest()
    if h != rh:
        okc = False
        break
    prev = rh
    seq += 1
check("audit hash chain verifies (%d records)" % len(lines), okc and seq > 1)
outcomes = [json.loads(l)["outcome"] for l in lines]
for o in ["success", "rejected_url", "http_error", "oversize",
          "budget_exhausted"]:
    check("audit has " + o, o in outcomes)

run("--close-run", "btest")
check("close-run removes state",
      not os.path.exists(os.path.join(HERE, "bridge", "_state_test",
                                      "btest.json")))
r = run("--run", "btest", "http://127.0.0.1:8901/t1a.html")
check("fetch after close -> 8", r.returncode == 8)

print("---")
print("FAILURES: %d" % len(fails))
sys.exit(1 if fails else 0)
