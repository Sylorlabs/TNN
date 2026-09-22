#!/usr/bin/env python3
"""Line-based JSONL -> txt converter for the v2 sub-batteries.

Same output format as src/convert_inputs2.py (which reads whole-file JSON
arrays); this one reads true JSONL (one object per line) as in inputs2/.
Input plumbing only -- NOT part of the frozen mechanism (PREREG2).

Usage: convert_jsonl2.py <train_jsonl> <test_jsonl> <outdir> <s>
Writes outdir/train_<s>.txt, outdir/test_<s>.txt, outdir/false_ids_<s>.txt
(false_ids always empty for the constructed sub-batteries).
"""
import json, os, sys


def clean(s):
    n = s.count("\t") + s.count("\n") + s.count("\r")
    return s.replace("\t", " ").replace("\r", " ").replace("\n", " "), n


def main():
    train_jl, test_jl, outdir, s = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    os.makedirs(outdir, exist_ok=True)
    tr = [json.loads(l) for l in open(train_jl) if l.strip()]
    te = [json.loads(l) for l in open(test_jl) if l.strip()]
    n_fix = 0
    with open(os.path.join(outdir, f"train_{s}.txt"), "w") as f:
        for r in tr:
            text = r.get("text", r.get("sentence", ""))
            text, n = clean(text)
            n_fix += n
            f.write(f"{r['id']}\t{text}\n")
    with open(os.path.join(outdir, f"test_{s}.txt"), "w") as f:
        for r in te:
            probe, n = clean(r["probe"])
            n_fix += n
            f.write(f"{r['id']}\t{r['probe_value']}\t{probe}\t{r.get('expect', r['probe_value'])}\n")
    with open(os.path.join(outdir, f"false_ids_{s}.txt"), "w") as f:
        pass  # sub-batteries carry no planted falsehoods
    print(f"{s}: train={len(tr)} test={len(te)} whitespace_fixes={n_fix}")


if __name__ == "__main__":
    main()
