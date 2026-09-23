#!/usr/bin/env python3
"""B-T1 rank aggregation. Reads per-(arm,corpus) bt1_score.py JSONs, emits the
tournament rank table + binding-bar verdict. Deterministic, zero RNG.
Usage: bt1_rank.py <results_dir>   (expects <arm>__<corpus>.json files)
"""
import json
import os
import sys

BINDING = ["predictive_surprise", "fixed_window_4", "raw_micro"]


def main():
    d = sys.argv[1]
    per = {}
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json"):
            continue
        r = json.load(open(os.path.join(d, fn)))
        per.setdefault(r["arm"], {})[r["corpus"]] = r
    rows = []
    for arm, cs in per.items():
        prose = cs.get("pg100.txt")
        code = cs.get("sqlite3.c")
        assert prose and code, ("missing corpus", arm)
        score = (prose["capability_composite"] + code["capability_composite"]) / 2.0
        rows.append({
            "arm": arm,
            "informational": arm == "random_chunks",
            "score_prose": prose["capability_composite"],
            "score_code": code["capability_composite"],
            "tournament_score": score,
            "grounded_hard_prose": prose["grounded_hard"],
            "grounded_hard_code": code["grounded_hard"],
            "retrieval_20way_prose": prose["retrieval_20way"],
            "retrieval_20way_code": code["retrieval_20way"],
            "compression_prose": prose["compression"],
            "compression_code": code["compression"],
            "mean_purity_prose": prose["mean_purity"],
            "mean_purity_code": code["mean_purity"],
            "n_chunks_prose": prose["n_chunks"],
            "n_chunks_code": code["n_chunks"],
            "vocab_probed_prose": prose["vocab_probed"],
            "vocab_probed_code": prose["vocab_probed"],
            "reconstruction": prose["reconstruction"] + "/" + code["reconstruction"],
        })
    rows.sort(key=lambda r: (-r["tournament_score"], r["arm"]))
    binding = [r for r in rows if not r["informational"]]
    brank = {r["arm"]: i + 1 for i, r in enumerate(binding)}
    ps, fw, rm = (brank["predictive_surprise"], brank["fixed_window_4"],
                  brank["raw_micro"])
    order_ok = ps < fw < rm
    last_ok = brank["raw_micro"] == len(binding)
    verdict = "PASS" if (order_ok and last_ok) else "FAIL"
    out = {
        "battery": "B-T1",
        "binding_bar": "predictive_surprise > fixed_window_4 > raw_micro, raw_micro dead last",
        "binding_verdict": verdict,
        "binding_ranks": {"predictive_surprise": ps, "fixed_window_4": fw,
                          "raw_micro": rm, "n_binding": len(binding)},
        "order_ok": "true" if order_ok else "false",
        "dead_last_ok": "true" if last_ok else "false",
        "full_rank_table": [
            dict(rank=i + 1, **{k: r[k] for k in r if k != "arm"},
                 arm=r["arm"]) for i, r in enumerate(rows)
        ],
    }
    json.dump(out, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")


main()
