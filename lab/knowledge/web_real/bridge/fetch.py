#!/usr/bin/env python3
"""fetch.py — NARROW AUDITED fetch bridge (M1). Transport only, never TNN-side.

The AI (Zag) chooses the URL; this program moves bytes and logs everything.
It never interprets content, never follows redirects, never retries, never
chooses follow-up URLs. Implements Sol's bridge design (recs 7-13):
 7. exact allow-list: http, host exactly 127.0.0.1, configured port, no
    userinfo, no fragment, absolute path; proxies disabled; fail closed.
 8. no redirect following; 3xx = failure. One request per invocation.
 9. hash-chained JSONL audit log, canonical encoding, fixed key order.
10. budgets outside AI control: max_bytes_per_fetch in config; per-run fetch
    count in bridge-owned state file keyed by supervisor-assigned run_id,
    incremented before network access. Unknown run_id -> fail closed.
11. read at most max_bytes+1; oversize -> discard body, nothing on stdout.
12. fixed exit codes / outcomes.
13. byte mover only.

Usage:
  fetch.py --new-run RUN_ID            (supervisor only: create run state)
  fetch.py --run RUN_ID URL            (fetch; body -> stdout)
  fetch.py --close-run RUN_ID          (supervisor only: remove run state)

Exit codes: 0 success | 2 rejected_url | 3 budget_exhausted | 4 timeout |
5 network_error | 6 oversize | 7 http_error | 8 audit/state unavailable |
9 delivery_error.
"""
import fcntl
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


CFG = load_config()
ALLOW_PORTS = set(CFG["allow_ports"])
MAX_BYTES = int(CFG["max_bytes_per_fetch"])
MAX_FETCHES = int(CFG["max_fetches_per_run"])
AUDIT_LOG = os.path.join(HERE, CFG["audit_log"])
STATE_DIR = os.path.join(HERE, CFG["state_dir"])
TIMEOUT = float(CFG.get("timeout_seconds", 10))
ZERO_HASH = "00" * 32


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # do not follow; caller sees the 3xx response


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")


def sha_hex(b):
    return hashlib.sha256(b).hexdigest()


def audit_append(fields):
    """Append one hash-chained record. Returns (ok, record). Fail closed."""
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    rec = {"v": 1}
    rec.update(fields)
    try:
        fd = os.open(AUDIT_LOG, os.O_RDWR | os.O_CREAT, 0o600)
    except OSError:
        return False, None
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        with os.fdopen(os.dup(fd), "r", encoding="utf-8") as rf:
            lines = rf.read().splitlines()
        prev = ZERO_HASH
        seq = 1
        if lines:
            last = json.loads(lines[-1])
            prev = last["record_hash"]
            seq = int(last["seq"]) + 1
        rec["seq"] = seq
        rec["prev_hash"] = prev
        rec["record_hash"] = sha_hex(canon({k: v for k, v in rec.items()
                                           if k != "record_hash"}))
        line = canon(rec) + b"\n"
        os.lseek(fd, 0, os.SEEK_END)
        os.write(fd, line)
        os.fsync(fd)
    except (OSError, ValueError):
        try:
            os.close(fd)
        except OSError:
            pass
        return False, None
    os.close(fd)
    return True, rec


def log_attempt(run_id, url, outcome, status, bytes_read, exit_code):
    ok, _ = audit_append({
        "run_id": run_id,
        "ts": time.time(),
        "url": url,
        "outcome": outcome,
        "status": status,
        "bytes_read": bytes_read,
        "exit_code": exit_code,
    })
    return ok


def valid_url(url):
    """Exact allow-list check (rec 7). Returns (ok, reason)."""
    try:
        p = urllib.parse.urlsplit(url)
    except ValueError:
        return False, "unparseable"
    if p.scheme != "http":
        return False, "scheme"
    if p.hostname != "127.0.0.1":
        return False, "host"
    if p.username is not None or p.password is not None:
        return False, "userinfo"
    try:
        port = p.port
    except ValueError:
        return False, "port"
    if port not in ALLOW_PORTS:
        return False, "port"
    if p.fragment:
        return False, "fragment"
    if not p.path.startswith("/"):
        return False, "path"
    return True, ""


def state_path(run_id):
    # run_id restricted to safe charset by supervisor contract
    if not run_id or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-_"
                         for c in run_id):
        return None
    return os.path.join(STATE_DIR, run_id + ".json")


def new_run(run_id):
    sp = state_path(run_id)
    if sp is None:
        print("bad run_id", file=sys.stderr)
        return 8
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = sp + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write('{"count":0}\n')
        os.replace(tmp, sp)
    except OSError:
        return 8
    return 0


def close_run(run_id):
    sp = state_path(run_id)
    if sp is None:
        return 8
    try:
        os.remove(sp)
    except FileNotFoundError:
        pass
    except OSError:
        return 8
    return 0


def fetch(run_id, url):
    # --- URL validation first (fail closed) ---
    ok, reason = valid_url(url)
    if not ok:
        log_attempt(run_id, url, "rejected_url", None, 0, 2)
        print("rejected_url: %s" % reason, file=sys.stderr)
        return 2
    # --- budget: bridge-owned counter, incremented BEFORE network ---
    sp = state_path(run_id)
    if sp is None:
        return 8
    try:
        fd = os.open(sp, os.O_RDWR)
    except OSError:
        print("unknown run_id", file=sys.stderr)
        return 8
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        with os.fdopen(os.dup(fd), "r", encoding="utf-8") as rf:
            st = json.load(rf)
        count = int(st["count"])
        if count >= MAX_FETCHES:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
            log_attempt(run_id, url, "budget_exhausted", None, 0, 3)
            print("budget_exhausted", file=sys.stderr)
            return 3
        # Rewrite the counter from offset 0: fdopen("w") on an already-open
        # fd does not truncate, so seek + ftruncate explicitly. Without
        # this, successive writes append and json.load fails ("Extra data").
        os.lseek(fd, 0, os.SEEK_SET)
        os.ftruncate(fd, 0)
        with os.fdopen(os.dup(fd), "w", encoding="utf-8") as wf:
            wf.write('{"count":%d}\n' % (count + 1))
        fcntl.flock(fd, fcntl.LOCK_UN)
    except (OSError, ValueError, KeyError):
        try:
            os.close(fd)
        except OSError:
            pass
        print("state corrupt", file=sys.stderr)
        return 8
    os.close(fd)
    # --- single request, no redirects, no proxies, bounded read ---
    # ProxyHandler({}) disables environment proxies (rec 7: loopback must
    # never egress through a proxy).
    opener = urllib.request.build_opener(NoRedirect,
                                         urllib.request.ProxyHandler({}),
                                         urllib.request.HTTPHandler)
    req = urllib.request.Request(url, headers={"User-Agent": "tnn-fetch/1.0"})
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            status = resp.status
            body = resp.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as e:
        # includes 3xx (not followed) and 4xx/5xx
        log_attempt(run_id, url, "http_error", e.code, 0, 7)
        print("http_error %s" % e.code, file=sys.stderr)
        return 7
    except TimeoutError:
        log_attempt(run_id, url, "timeout", None, 0, 4)
        print("timeout", file=sys.stderr)
        return 4
    except (urllib.error.URLError, OSError) as e:
        log_attempt(run_id, url, "network_error", None, 0, 5)
        print("network_error %s" % e, file=sys.stderr)
        return 5
    if status != 200:
        log_attempt(run_id, url, "http_error", status, 0, 7)
        print("http_error %s" % status, file=sys.stderr)
        return 7
    if len(body) > MAX_BYTES:
        log_attempt(run_id, url, "oversize", status, MAX_BYTES + 1, 6)
        print("oversize", file=sys.stderr)
        return 6
    # --- audit BEFORE delivery (rec 11) ---
    if not log_attempt(run_id, url, "success", status, len(body), 0):
        print("audit unavailable", file=sys.stderr)
        return 8
    try:
        out = os.fdopen(os.dup(1), "wb", closefd=False)
        out.write(body)
        out.flush()
    except OSError:
        log_attempt(run_id, url, "delivery_error", status, len(body), 9)
        print("delivery_error", file=sys.stderr)
        return 9
    return 0


def main(argv):
    if len(argv) == 3 and argv[1] == "--new-run":
        return new_run(argv[2])
    if len(argv) == 3 and argv[1] == "--close-run":
        return close_run(argv[2])
    if len(argv) == 4 and argv[1] == "--run":
        return fetch(argv[2], argv[3])
    print("usage: fetch.py --new-run RUN_ID | --run RUN_ID URL | "
          "--close-run RUN_ID", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
