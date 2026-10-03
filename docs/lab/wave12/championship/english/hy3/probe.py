#!/usr/bin/env python3
"""hy3 English-box probe: ONE batch (batch00_dump) via UnoRouter.

Opportunistic leg policy (parent task, 2026-09-21):
- Probe once. On failure, paced 90s waits, retry until the ~1h deadline.
- If still 503/unreachable after ~1h: print BLOCKED, exit 2.
- If reachable: save the raw response bytes verbatim (resumable for the full
  capture), print REACHABLE + sha256, exit 0.
A definitive model-not-found (HTTP 404/400 naming hy3:free) also exits 2 with
the error body recorded — no point waiting out a routing-table problem.
"""
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

BASE = "https://api.unorouter.com/v1"
MODEL = "hy3:free"
HERE = os.path.dirname(os.path.abspath(__file__))
PROMPT = os.path.join(HERE, "..", "..", "championship-english",
                      "corpus-input", "batch00_dump.txt")
OUT_RAW = os.path.join(HERE, "corpus", "raw", "dump_batch00.txt")
OUT_LOG = os.path.join(HERE, "probe.log")
DEADLINE_S = 3600          # ~1h of paced retries
WAIT_S = 90                # paced waits
REQ_TIMEOUT_S = 120        # per-attempt request timeout


def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
    print(line, flush=True)
    with open(OUT_LOG, "a") as f:
        f.write(line + "\n")


def attempt_once():
    with open(PROMPT, "r") as f:
        prompt = f.read()
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "temperature": 0, "seed": 42, "stream": False}
    req = urllib.request.Request(
        BASE + "/chat/completions", data=json.dumps(payload).encode(),
        method="POST")
    req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, "custom.unorouter",
                             allowed_hosts=("api.unorouter.com",
                                            "unorouter.com"))
    with urllib.request.urlopen(req, timeout=REQ_TIMEOUT_S) as resp:
        body = read_json_response(resp)
    return body["choices"][0]["message"]["content"]


def main():
    log("probe start: model=hy3:free batch=batch00_dump "
        f"deadline={DEADLINE_S}s waits={WAIT_S}s")
    t0 = time.time()
    n = 0
    while True:
        n += 1
        try:
            content = attempt_once()
            raw_bytes = content.encode("utf-8")
            os.makedirs(os.path.dirname(OUT_RAW), exist_ok=True)
            with open(OUT_RAW, "wb") as f:
                f.write(raw_bytes)
            sha = hashlib.sha256(raw_bytes).hexdigest()
            log(f"REACHABLE on attempt {n}; raw bytes saved sha256={sha} "
                f"len={len(raw_bytes)}")
            print(f"REACHABLE sha256={sha}")
            return 0
        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode("utf-8", "replace")[:300]
            except Exception:
                err_body = ""
            log(f"attempt {n}: HTTPError {e.code} {e.reason} body={err_body!r}")
            if e.code in (400, 404) and "hy3" in err_body.lower():
                log("MODEL-NOT-FOUND signature: hy3:free not routable; "
                    "BLOCKED (no point in waiting)")
                print("BLOCKED: model not found on connector")
                return 2
        except Exception as e:  # URLError, TimeoutError, KeyError, ...
            log(f"attempt {n}: {type(e).__name__}: {str(e)[:200]}")
        if time.time() - t0 >= DEADLINE_S:
            log(f"deadline reached after {n} attempts; BLOCKED")
            print("BLOCKED: still unreachable after ~1h")
            return 2
        log(f"sleeping {WAIT_S}s before attempt {n + 1}")
        time.sleep(WAIT_S)


if __name__ == "__main__":
    sys.exit(main())
