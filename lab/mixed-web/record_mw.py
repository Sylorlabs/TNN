#!/usr/bin/env python3
"""record_mw.py — record live search envelopes for the mixed-web experiment.

Runs each prereg question through the v2 live bridge (ws_bridge2.py, lumy
primary) and saves live/<qid>.json. Record-once; scored runs replay these
frozen envelopes. Fails loudly on zero-usable-results (shortfall is data).
"""
import json
import os
import subprocess
import sys

BRIDGE = os.path.expanduser("~/workspace/tnn-lab/senses/web-search/v2/transport/ws_bridge2.py")
LIVE = os.path.expanduser("~/workspace/tnn-lab/mixed-web/live")

# qid, query string (from PREREG §2, frozen)
QUERIES = [
    ("M01", "oldest university in the world"),
    ("M02", "inventor of the telephone"),
    ("M03", "who discovered America"),
    ("M04", "how many countries are in Africa"),
    ("M05", "largest desert in the world"),
    ("M06", "longest river in the world"),
    ("M07", "largest lake in the world"),
    ("M08", "tallest mountain in the world"),
    ("M09", "who wrote the first novel in history"),
    ("M10", "oldest civilization in the world"),
    ("M11", "most spoken language in the world"),
    ("M12", "who invented the light bulb"),
    ("M13", "most populous city in the world"),
    ("M14", "oldest city in the world"),
    ("M15", "largest economy in the world by nominal GDP"),
    ("M16", "which country has the most natural lakes in the world"),
    ("M17", "fastest animal in the world"),
    ("R01", "tallest completed building in the world"),
    ("R02", "largest country in the world by population"),
    ("R03", "reigning FIFA World Cup champions"),
    ("R04", "president of the United States"),
    ("R05", "prime minister of the United Kingdom"),
    ("R06", "richest person in the world"),
    ("M18", "who invented the World Wide Web"),
    ("M19", "who invented the airplane"),
    ("M20", "what is the tallest waterfall in the world"),
    ("M21", "what is the oldest language in the world"),
    ("M22", "what was the first video game"),
    ("M23", "what is the largest pyramid in the world"),
]


def main():
    redo = "--redo" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    os.makedirs(LIVE, exist_ok=True)
    shortfalls = []
    for qid, q in QUERIES:
        if only and qid not in only:
            continue
        p = os.path.join(LIVE, qid + ".json")
        if os.path.exists(p) and not redo:
            print(f"keep {qid}")
            continue
        r = subprocess.run([sys.executable, BRIDGE, q, "10", "--backend", "lumy"],
                           capture_output=True, text=True, timeout=180)
        if r.returncode != 0:
            print(f"BRIDGE FAIL {qid}: {r.stderr[:200]}")
            shortfalls.append(qid)
            continue
        try:
            env = json.loads(r.stdout)
        except Exception as e:
            print(f"PARSE FAIL {qid}: {e}")
            shortfalls.append(qid)
            continue
        usable = [x for x in env.get("results", []) if x.get("title") and x.get("url")]
        env["qid"] = qid
        env["query"] = q
        json.dump(env, open(p, "w"), indent=1)
        print(f"recorded {qid}: {len(usable)} usable results")
        if not usable:
            shortfalls.append(qid)
    if shortfalls:
        print(f"SHORTFALLS: {shortfalls}")
        sys.exit(2)
    print("all queries returned usable results")


if __name__ == "__main__":
    main()
