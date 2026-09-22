#!/usr/bin/env python3
"""Convert rich-comprehension v2 inputs (jsonl) to a trivial line format.

Input plumbing only -- NOT part of the frozen mechanism. The frozen mechanism
starts at parsed items {id, text} / {id, probe, probe_value, expect}.

Reads <indir>/{train,test}_<s>.jsonl + false_ids_<s>.json, writes to <outdir>:
  train_<s>.txt : "id\\t<text>"                       (text = "text" key, else "sentence" alias)
  test_<s>.txt  : "id\\t<probe_value>\\t<probe>\\t<expect>"  (expect = "expect" key, else probe_value)
  false_ids_<s>.txt : one id per line

Tab/CR/LF inside text fields are replaced with a single space (the mechanism
splits sentences on [.?!] only, so this is semantics-preserving; counts are
reported). Prints sha256 of every input file for the run record.

Usage: convert_inputs2.py <indir> <outdir> <s1> [s2 ...]
"""
import hashlib, json, os, sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean(s):
    n_tab = s.count("\t") + s.count("\n") + s.count("\r")
    s = s.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    return s, n_tab


def main():
    indir, outdir, sources = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(outdir, exist_ok=True)
    for s in sources:
        tr = json.load(open(os.path.join(indir, f"train_{s}.jsonl")))
        te = json.load(open(os.path.join(indir, f"test_{s}.jsonl")))
        fi = json.load(open(os.path.join(indir, f"false_ids_{s}.json")))["false_ids"]
        for fn in (f"train_{s}.jsonl", f"test_{s}.jsonl", f"false_ids_{s}.json"):
            print(f"sha256 {fn} {sha256_file(os.path.join(indir, fn))}")
        n_fix = 0
        with open(os.path.join(outdir, f"train_{s}.txt"), "w") as f:
            for r in tr:
                # "text" wins if both keys present ("sentence" is the single-sentence alias)
                text = r.get("text", r.get("sentence", ""))
                text, n = clean(text)
                n_fix += n
                f.write(f"{r['id']}\t{text}\n")
        with open(os.path.join(outdir, f"test_{s}.txt"), "w") as f:
            for r in te:
                probe, n1 = clean(r["probe"])
                n_fix += n1
                pv = r["probe_value"]
                expect = r.get("expect", pv)
                f.write(f"{r['id']}\t{pv}\t{probe}\t{expect}\n")
        with open(os.path.join(outdir, f"false_ids_{s}.txt"), "w") as f:
            for i in sorted(fi):
                f.write(f"{i}\n")
        print(f"{s}: train={len(tr)} test={len(te)} false={len(fi)} whitespace_fixes={n_fix}")


if __name__ == "__main__":
    main()
