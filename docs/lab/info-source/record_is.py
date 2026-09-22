#!/usr/bin/env python3
"""record_is.py — record live search envelopes for the info-source experiment.

Runs each battery query through the v2 live bridge (ws_bridge2.py, lumy
primary) and saves live/<factid>.json. Record-once; scored runs replay these
frozen envelopes. Fails loudly on zero-usable-results (shortfall is data).
"""
import json
import os
import subprocess
import sys

BRIDGE = os.path.expanduser("~/workspace/tnn-lab/senses/web-search/v2/transport/ws_bridge2.py")
LIVE = os.path.expanduser("~/workspace/tnn-lab/docs/lab/info-source/live")

QUERIES = [
    ("F01", "capital of France"),
    ("F02", "chemical symbol for gold"),
    ("F03", "author of the novel 1984"),
    ("F04", "largest planet in the solar system"),
    ("F05", "speed of light in vacuum km/s"),
    ("F06", "first person to walk on the moon"),
    ("F07", "boiling point of water at sea level"),
    ("F08", "who wrote Pride and Prejudice"),
    ("F09", "when was the Eiffel Tower built"),
    ("F10", "tallest building in the world 2026"),
    ("F11", "capital of Japan"),
    ("F12", "chemical symbol for silver"),
    ("U01", "capital of Burkina Faso"),
    ("U02", "chemical symbol for tungsten"),
    ("U03", "deepest ocean trench in the world"),
    ("U04", "currency of Switzerland"),
    ("MTN", "tallest mountain in the world"),
]


def main():
    redo = "--redo" in sys.argv
    os.makedirs(LIVE, exist_ok=True)
    shortfalls = []
    for fid, q in QUERIES:
        p = os.path.join(LIVE, fid + ".json")
        if os.path.exists(p) and not redo:
            print(f"keep {fid}")
            continue
        r = subprocess.run([sys.executable, BRIDGE, q, "8", "--backend", "lumy"],
                           capture_output=True, text=True, timeout=180)
        if r.returncode != 0:
            print(f"BRIDGE FAIL {fid}: {r.stderr[:200]}")
            shortfalls.append(fid)
            continue
        try:
            env = json.loads(r.stdout)
        except Exception as e:
            print(f"PARSE FAIL {fid}: {e}")
            shortfalls.append(fid)
            continue
        usable = [x for x in env.get("results", []) if x.get("title") and x.get("url")]
        env["fact_id"] = fid
        env["query"] = q
        json.dump(env, open(p, "w"), indent=1)
        print(f"recorded {fid}: {len(usable)} usable results")
        if not usable:
            shortfalls.append(fid)
    if shortfalls:
        print(f"SHORTFALLS: {shortfalls}")
        sys.exit(2)
    print("all queries returned usable results")


if __name__ == "__main__":
    main()
