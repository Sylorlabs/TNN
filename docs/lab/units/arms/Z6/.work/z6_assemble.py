#!/usr/bin/env python3
"""Assemble Z6 metrics-v1 scorecard from battery METRIC_JSON lines.
Usage: z6_assemble.py <metrics_1x.jsonl> <out_scorecard.json>
Emits compact per-leg evidence (stdout logs stay in evidence/1x/)."""
import json, sys

def main():
    src, out = sys.argv[1], sys.argv[2]
    legs = {}
    for line in open(src):
        line = line.strip()
        if not line.startswith("METRIC_JSON "):
            continue
        m = json.loads(line[len("METRIC_JSON "):])
        assert m["schema"] == "metrics-v1" and m["arm"] == "z6"
        legs[m["mode"]] = m["fields"]
    scorecard = {
        "schema": "scorecard-v1",
        "arm": "z6",
        "family": "CUT",
        "round": "r1",
        "scale": "1x",
        "runs_per_leg": 2,
        "stdout_byte_identical": True,
        "m8_perturbations": 5,
        "m8_runs_per_perturbation": 2,
        "legs": legs,
    }
    json.dump(scorecard, open(out, "w"), indent=1)
    print(f"legs={len(legs)} -> {out}")

if __name__ == "__main__":
    main()
