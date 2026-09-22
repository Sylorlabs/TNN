#!/usr/bin/env python3
"""Proof input plumbing (NOT part of the mechanism): convert synth.json and
the v2 inputs2 sub_para jsonl pair into the Zag .txt line format.

train_<s>.txt : "id\\t<text>"
test_<s>.txt  : "id\\t<probe_value>\\t<probe>\\t<expect>"  (expect defaults to probe_value)
false_ids_<s>.txt : one id per line (empty file when none)

Tab/CR/LF inside text fields are replaced with a single space (the mechanism
splits sentences on [.?!] only, so this is semantics-preserving).
Deterministic: no RNG.
"""
import hashlib
import json
import os
import sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean(s):
    s = s.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    return s


def write_set(outdir, s, train_recs, test_recs, false_ids):
    os.makedirs(os.path.join(outdir, "inputs"), exist_ok=True)
    with open(os.path.join(outdir, "inputs", f"train_{s}.txt"), "w") as f:
        for r in train_recs:
            text = r.get("text", r.get("sentence", ""))
            f.write(f"{r['id']}\t{clean(text)}\n")
    with open(os.path.join(outdir, "inputs", f"test_{s}.txt"), "w") as f:
        for r in test_recs:
            pv = r["probe_value"]
            expect = r.get("expect", pv)
            f.write(f"{r['id']}\t{pv}\t{clean(r['probe'])}\t{expect}\n")
    with open(os.path.join(outdir, "inputs", f"false_ids_{s}.txt"), "w") as f:
        for i in sorted(false_ids):
            f.write(f"{i}\n")
    for fn in (f"train_{s}.txt", f"test_{s}.txt", f"false_ids_{s}.txt"):
        p = os.path.join(outdir, "inputs", fn)
        print(f"sha256 {fn} {sha256_file(p)}")


def main():
    base = os.path.expanduser("~/workspace/tnn-lab/prose-learning/v3/proof")
    # synth.json -> source name "synth"
    sj = json.load(open(os.path.expanduser(
        "~/workspace/tnn-lab/prose-learning/v3/src/synth.json")))
    print("sha256 synth.json", sha256_file(os.path.expanduser(
        "~/workspace/tnn-lab/prose-learning/v3/src/synth.json")))
    write_set(os.path.join(base, "synth"), "synth",
              sj["train"], sj["test"], set(sj.get("false_ids", [])))
    # v2 inputs2 sub_para jsonl -> source name "sub_para"
    i2 = os.path.expanduser("~/workspace/tnn-lab/prose-learning/v2/inputs2")
    tr = [json.loads(l) for l in open(os.path.join(i2, "sub_para_train.jsonl"))]
    te = [json.loads(l) for l in open(os.path.join(i2, "sub_para_test.jsonl"))]
    for fn in ("sub_para_train.jsonl", "sub_para_test.jsonl"):
        print(f"sha256 {fn} {sha256_file(os.path.join(i2, fn))}")
    write_set(os.path.join(base, "subpara"), "sub_para", tr, te, set())


if __name__ == "__main__":
    main()
