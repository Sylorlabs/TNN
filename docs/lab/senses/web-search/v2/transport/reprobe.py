#!/usr/bin/env python3
"""reprobe.py — focused re-probe of promising backends (fixed parser + bug)."""
import json, sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_backends import QUERIES, probe, build_endpoints

WANT = {"ddg_lite", "ddg_html", "wikipedia_api",
        "searxng:searx.tiekoetter.com", "searxng:search.rhscz.eu",
        "mojeek", "marginalia"}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reprobe_results.json")

def main():
    eps = [e for e in build_endpoints() if e["name"] in WANT]
    results = []
    for ep in eps:
        print("probing", ep["name"], flush=True)
        results.append(probe(ep, QUERIES))
    with open(OUT, "w") as f:
        json.dump({"probed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "queries": QUERIES, "endpoints": results}, f, indent=1)
    for r in results:
        lat = [q.get("latency_s") for q in r["queries"] if q.get("latency_s")]
        avg = round(sum(lat)/len(lat), 2) if lat else None
        print(f'{r["name"]:36s} usable={r["pass_count"]}/10 works={r["works"]} avg_lat={avg}s')

if __name__ == "__main__":
    main()
