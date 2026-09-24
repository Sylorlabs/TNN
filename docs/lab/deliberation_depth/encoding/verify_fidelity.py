#!/usr/bin/env python3
"""Fidelity check F1 (SPEC section 5): independent GT re-derivation.

For every translated item, recompute argmax_h (sum supports - sum attacks)
with ties broken to the lowest hypothesis index (the harness's tie rule),
independently of the harness code. Requires 877/877 == ground_truth.

Usage: verify_fidelity.py <items_v2_dir>
"""
import json
import sys


def main():
    d = sys.argv[1]
    files = ["admit.jsonl", "revoke.jsonl", "logic.jsonl", "trap.jsonl",
             "cost.jsonl"]
    n = 0
    failures = []
    for fn in files:
        with open(f"{d}/{fn}", encoding="utf-8") as f:
            for ln, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                n += 1
                o = json.loads(line)
                hyps = [h["id"] for h in o["input"]["hypotheses"]]
                score = {h: 0 for h in hyps}
                for e in o["input"]["evidence"]:
                    for h, w in e["supports"].items():
                        score[h] += w
                    for h, w in e["attacks"].items():
                        score[h] -= w
                # argmax, ties -> lowest hypothesis index
                best = hyps[0]
                for h in hyps[1:]:
                    if score[h] > score[best]:
                        best = h
                if best != o["ground_truth"]:
                    failures.append((fn, ln, o["id"], best,
                                     o["ground_truth"], dict(score)))
    print(f"F1: {n - len(failures)}/{n} items re-derive their ground truth")
    for f_ in failures[:20]:
        print("  FAIL:", f_)
    if n != 877:
        print(f"F1: expected 877 items, got {n}")
        sys.exit(2)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
