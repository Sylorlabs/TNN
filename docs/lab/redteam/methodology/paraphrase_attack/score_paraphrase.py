#!/usr/bin/env python3
"""Redteam adversarial-paraphrase scorer (Sol #1).

Uses the EXISTING independent oracle pipeline (prose-learning/src/oracle.py:
pipeline(), Jaccard argmax, lowest-id tiebreak) — the 0-diff-verified
implementation of the frozen v1 mechanism. No new learner build; the mechanism
under test is byte-identical to the v1 verdict's. Deterministic, zero RNG.
"""
import json, sys
sys.path.insert(0, "/home/hatch/workspace/tnn-lab/prose-learning/src")
from oracle import Vocab, pipeline  # exact frozen v1 pipeline
sys.path.insert(0, "/home/hatch/workspace/tnn-lab/docs/lab/redteam/methodology/paraphrase_attack")
from paraphrases import PARAPHRASES

INPDIR = "/home/hatch/workspace/tnn-lab/prose-learning/inputs"
SOURCES = ["sol", "grok"]

def install(source):
    vocab = Vocab()
    facts = []  # (fact_id, key_set, value), id order
    for line in open(f"{INPDIR}/train_{source}.txt"):
        fid_s, sent = line.rstrip("\n").split("\t", 1)
        _, key, value, _ = pipeline(vocab, sent)
        if value is not None:
            facts.append((int(fid_s), set(key), value))
    return vocab, facts

def probe_key(vocab, text):
    _, key, _, _ = pipeline(vocab, text)
    return set(key)

def answer_for(facts, kset):
    best = None; best_id = None
    for fid, fkey, fval in facts:
        inter = len(kset & fkey); union = len(kset | fkey)
        if union == 0:
            score = (0, 1)
        else:
            score = (inter, union)
        if best is None or score[0] * best[1] > best[0] * score[1]:
            best = score; best_id = fid
        # tie: keep lowest fact id (facts in id order) -> do nothing
    return best_id, dict((f[0], f[2]) for f in facts)[best_id]

def main():
    tests = {}
    for s in SOURCES:
        t = {}
        for line in open(f"{INPDIR}/test_{s}.txt"):
            p = line.rstrip("\n").split("\t", 2)
            t[p[0]] = (int(p[1]), p[2])
        tests[s] = t
    # cross-source sanity: probe values must agree (same facts)
    for fid, _, _, _, _ in PARAPHRASES:
        k = str(fid)
        assert tests["sol"][k][0] == tests["grok"][k][0], f"probe_value mismatch at {fid}"
    rows = []
    summary = {}
    for s in SOURCES:
        vocab, facts = install(s)
        tiers = {"original": 0, "mild": 0, "adversarial": 0}
        fam = {}
        for fid, family, entity, mild, adv in PARAPHRASES:
            k = str(fid)
            pv, orig = tests[s][k]
            probes = {"original": orig, "mild": mild, "adversarial": adv}
            r = {"fact_id": fid, "family": family, "entity": entity,
                 "probe_value": pv, "source": s}
            for tier, text in probes.items():
                _, ans = answer_for(facts, probe_key(vocab, text))
                ok = 1 if ans == pv else 0
                tiers[tier] += ok
                r[tier] = {"probe": text, "answer": ans, "correct": ok}
            fam.setdefault(family, {"original": 0, "mild": 0, "adversarial": 0, "n": 0})
            fam[family]["n"] += 1
            for tier in tiers:
                fam[family][tier] += r[tier]["correct"]
            rows.append(r)
        n = len(PARAPHRASES)
        summary[s] = {"n": n,
                      "original": tiers["original"] / n,
                      "mild": tiers["mild"] / n,
                      "adversarial": tiers["adversarial"] / n,
                      "by_family": fam}
    out = {"summary": summary, "rows": rows}
    json.dump(out, open("/home/hatch/workspace/tnn-lab/docs/lab/redteam/methodology/paraphrase_attack/results.json", "w"), indent=1)
    for s in SOURCES:
        sm = summary[s]
        print(f"== {s}: n={sm['n']} original={sm['original']:.4f} mild={sm['mild']:.4f} adversarial={sm['adversarial']:.4f}")
        for f, d in sm["by_family"].items():
            print(f"   {f}: n={d['n']} orig={d['original']/d['n']:.3f} mild={d['mild']/d['n']:.3f} adv={d['adversarial']/d['n']:.3f}")

if __name__ == "__main__":
    main()
