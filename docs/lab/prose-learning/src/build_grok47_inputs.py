#!/usr/bin/env python3
"""Build Leg C (grok-4.7) prose-learning inputs from the captured teacher-showdown corpus.

Reads the frozen grok-4.7 capture
  GROK47_OVERNIGHT/teacher/evidence/grok47_corpus/corpus.json
(sha256 111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a),
verifies its hash, and writes, in the exact line format of
src/convert_inputs.py (frozen for the 4-source battery):
  inputs/train_grok47.jsonl : [{id, sentence}]            (240 dump sentences)
  inputs/test_grok47.jsonl  : [{id, probe, probe_value}]  (240 teach probes)
  inputs/false_ids_grok47.json : {"false_ids": [...]}     (12 planted false ids)
  inputs/train_grok47.txt   : "id\\t<sentence>"
  inputs/test_grok47.txt    : "id\\t<probe_value>\\t<probe>"
  inputs/false_ids_grok47.txt : one id per line

The prose learner (src/prose_learn.zag) reads only the .txt files, relative
to the prose-learning CWD, with argv[1]="grok47".

Zero RNG. Deterministic: JSON is emitted with sort_keys and fixed separators.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INP = os.path.join(HERE, "inputs")
CORPUS = os.path.join(HERE, "..", "GROK47_OVERNIGHT", "teacher",
                       "evidence", "grok47_corpus", "corpus.json")
CORPUS_SHA = "111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a"
PLANTED = [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    got = sha256_file(CORPUS)
    if got != CORPUS_SHA:
        print(f"CORPUS SHA MISMATCH: got {got} want {CORPUS_SHA}", file=sys.stderr)
        sys.exit(1)
    print(f"corpus sha256 OK ({got[:12]}...)")

    corpus = json.load(open(CORPUS))
    dump = corpus["dump"]
    teach = corpus["teach"]
    false_ids = corpus["false_ids"]

    assert len(dump) == 240, len(dump)
    assert len(teach) == 240, len(teach)
    assert [d["id"] for d in dump] == list(range(240))
    assert [t["id"] for t in teach] == list(range(240))
    assert sorted(false_ids) == PLANTED, false_ids
    assert corpus["meta"]["model"] == "grok-4.7"

    train = [{"id": d["id"], "sentence": d["sentence"]} for d in dump]
    test = [{"id": t["id"], "probe": t["probe"], "probe_value": t["probe_value"]}
            for t in teach]

    for r in train:
        s = r["sentence"]
        assert "\t" not in s and "\n" not in s and "\r" not in s, r["id"]
    for r in test:
        p = r["probe"]
        assert "\t" not in p and "\n" not in p and "\r" not in p, r["id"]
        assert isinstance(r["probe_value"], int), r["id"]

    with open(os.path.join(INP, "train_grok47.jsonl"), "w") as f:
        json.dump(train, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")
    with open(os.path.join(INP, "test_grok47.jsonl"), "w") as f:
        json.dump(test, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")
    with open(os.path.join(INP, "false_ids_grok47.json"), "w") as f:
        json.dump({"false_ids": sorted(false_ids)}, f, sort_keys=True,
                  separators=(",", ":"))
        f.write("\n")

    with open(os.path.join(INP, "train_grok47.txt"), "w") as f:
        for r in train:
            f.write(f"{r['id']}\t{r['sentence']}\n")
    with open(os.path.join(INP, "test_grok47.txt"), "w") as f:
        for r in test:
            f.write(f"{r['id']}\t{r['probe_value']}\t{r['probe']}\n")
    with open(os.path.join(INP, "false_ids_grok47.txt"), "w") as f:
        for i in sorted(false_ids):
            f.write(f"{i}\n")

    print("wrote inputs/train_grok47.{jsonl,txt} inputs/test_grok47.{jsonl,txt} "
          "inputs/false_ids_grok47.{json,txt}")
    for fn in ("train_grok47.jsonl", "test_grok47.jsonl", "false_ids_grok47.json",
               "train_grok47.txt", "test_grok47.txt", "false_ids_grok47.txt"):
        p = os.path.join(INP, fn)
        print(f"  {fn}: {os.path.getsize(p)} bytes sha256={sha256_file(p)[:16]}...")


if __name__ == "__main__":
    main()
