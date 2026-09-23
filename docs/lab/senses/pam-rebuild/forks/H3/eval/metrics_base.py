#!/usr/bin/env python3
"""Compute B1, B2, B3, B5 from base_cache.jsonl."""
import json, sys
from collections import Counter, defaultdict

def main():
    rows = [json.loads(l) for l in open(sys.argv[1])]
    by_task = defaultdict(list)
    for r in rows:
        by_task[r["task"]].append(r)

    print("=== B1 viability (H3 judgment accuracy on primary, macro-average) ===")
    accs = []
    for t in sorted(by_task):
        prim = [r for r in by_task[t] if r["split"] == "primary"]
        a = sum(1 for r in prim if r["h3_judge"] == r["truth"]) / len(prim)
        accs.append(a)
        print("  %s: %.3f (%d/%d)" % (t, a, sum(1 for r in prim if r["h3_judge"] == r["truth"]), len(prim)))
    b1 = sum(accs) / len(accs)
    print("  B1 macro-average: %.4f  %s" % (b1, "PASS (>=0.60)" if b1 >= 0.60 else "FAIL"))

    print("\n=== B2 head-to-head (H3 - A accuracy delta, identical fixtures) ===")
    for split in ["primary", "noise", "adversarial", "h3adv"]:
        dh, da, n = 0, 0, 0
        for t in sorted(by_task):
            rs = [r for r in by_task[t] if r["split"] == split]
            for r in rs:
                n += 1
                if r["h3_judge"] == r["truth"]: dh += 1
                if r["a_judge"] == r["truth"]: da += 1
        print("  %s: H3=%.3f A=%.3f delta=%+.3f (n=%d)" % (split, dh/n, da/n, dh/n-da/n, n))

    print("\n=== B3 efficiency (ops H3/A, bytes per percept) ===")
    ratios = []
    for t in sorted(by_task):
        rs = [r for r in by_task[t] if r["split"] == "primary"]
        rr = [r["h3_ops"]/r["a_ops"] for r in rs if r["a_ops"] > 0]
        rr.sort()
        p50 = rr[len(rr)//2]
        print("  %s: mean=%.2f p50=%.2f (n=%d)" % (t, sum(rr)/len(rr), p50, len(rr)))
        ratios += rr
    ratios.sort()
    print("  overall: mean=%.2f p50=%.2f p95=%.2f" % (
        sum(ratios)/len(ratios), ratios[len(ratios)//2], ratios[int(len(ratios)*0.95)]))
    # bytes per percept
    hb = [len(r["h3_transition"] or "") for r in rows]
    print("  H3 transition bytes: mean=%.0f" % (sum(hb)/len(hb)))

    print("\n=== B5 KB4 (adversarial false-install <= 4%) ===")
    adv = [r for r in rows if r["split"] in ("adversarial", "h3adv")]
    fi = [r for r in adv if r["h3_disp"] == "INSTALLED" and r["h3_judge"] != r["truth"]]
    print("  adversarial n=%d, false installs=%d, rate=%.4f  %s" % (
        len(adv), len(fi), len(fi)/len(adv),
        "PASS (<=0.04)" if len(fi)/len(adv) <= 0.04 else "FAIL"))
    for r in fi[:20]:
        print("    FALSE-INSTALL:", r["task"], r["fixture"].split("/")[-1],
              "judge=", r["h3_judge"], "truth=", r["truth"], "disp=", r["h3_disp"])

    print("\n=== Disposition breakdown (all splits) ===")
    for split in ["primary", "noise", "adversarial", "h3adv"]:
        c = Counter(r["h3_disp"] for r in rows if r["split"] == split)
        print("  %s: %s" % (split, dict(c)))

if __name__ == "__main__":
    main()
