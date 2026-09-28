#!/usr/bin/env python3
"""Mechanical faithfulness inventory for the hy3 ENGLISH frozen corpus.

The frozen batch files are PROMPTS ONLY; the model's responses live in
corpus.json. Faithfulness = the model stating the GIVEN value (facts.json),
not the real-world truth. Compares corpus.json against:
- the trainer's given values (facts.json "value"): E_dump / E_obs / E_prb
  (model's stated integer != given value => transcription error)
- obs/probe agreement: OBS_VALUE vs PROBE_VALUE
- distractor != observation (structural)
- integer/text agreement: the sentence text contains the stated integer
- the 12 false-id classification: reproduce (faithful to the given false
  value) vs correct-toward-truth (unfaithful "helpfulness")

Writes ERROR_INVENTORY.md. Fails loudly if the corpus is absent.
"""
import hashlib
import json
import os
import re
import sys

HY3 = os.path.dirname(os.path.abspath(__file__))
CORPUS_JSON = os.path.join(HY3, "corpus", "corpus.json")
CORPUS_SHA = os.path.join(HY3, "corpus", "SHA256.txt")
TABLES = os.path.join(HY3, "tnn", "gen", "english_tables.json")

tabs = json.load(open(TABLES))
TRUE = {int(k): v for k, v in tabs["true"].items()}
GIVEN = {int(k): v for k, v in tabs["supplied"].items()}
FALSE_IDS = set(tabs["false_ids"])

def main():
    raw = open(CORPUS_JSON, "rb").read()
    if hashlib.sha256(raw).hexdigest() != open(CORPUS_SHA).read().strip():
        sys.exit("FATAL: corpus.json sha mismatch")
    corpus = json.loads(raw)
    DUMP = {e["id"]: e for e in corpus["dump"]}
    TEACH = {e["id"]: e for e in corpus["teach"]}

    E_dump = [i for i in range(240) if DUMP[i]["value"] != GIVEN[i]]
    E_obs = [i for i in range(240) if TEACH[i]["obs_value"] != GIVEN[i]]
    E_prb = [i for i in range(240) if TEACH[i]["probe_value"] != GIVEN[i]]
    INCONS = [i for i in range(240)
              if TEACH[i]["obs_value"] != TEACH[i]["probe_value"]]
    DIS_EQ_OBS = [i for i in range(240)
                  if TEACH[i]["distract_value"] == TEACH[i]["obs_value"]]
    # integer/text agreement: the sentence must contain its stated integer
    def has_int(text, v):
        return re.search(rf"(?<![0-9]){v}(?![0-9])", text) is not None
    T_dump = [i for i in range(240)
              if not has_int(DUMP[i]["sentence"], DUMP[i]["value"])]
    T_obs = [i for i in range(240)
             if not has_int(TEACH[i]["observation"], TEACH[i]["obs_value"])]
    T_dis = [i for i in range(240)
             if not has_int(TEACH[i]["distractor"], TEACH[i]["distract_value"])]
    # false-id classification
    cls = {}
    for i in sorted(FALSE_IDS):
        o, p = TEACH[i]["obs_value"], TEACH[i]["probe_value"]
        if o == GIVEN[i] and p == GIVEN[i]:
            cls[i] = "reproduce (faithful to given false value)"
        elif o == TRUE[i] or p == TRUE[i]:
            cls[i] = "CORRECT-TOWARD-TRUTH (unfaithful)"
        else:
            cls[i] = f"other(obs={o},prb={p})"

    L = []
    L.append("# hy3 ENGLISH — mechanical faithfulness inventory")
    L.append("")
    L.append(f"corpus sha256: `{open(CORPUS_SHA).read().strip()}`")
    L.append("")
    L.append("## Transcription errors (model value != trainer's GIVEN value)")
    L.append(f"- E_dump: n={len(E_dump)} ids={E_dump}")
    L.append(f"- E_obs: n={len(E_obs)} ids={E_obs}")
    L.append(f"- E_prb: n={len(E_prb)} ids={E_prb}")
    L.append("")
    L.append("## Consistency")
    L.append(f"- obs/probe inconsistencies: n={len(INCONS)} ids={INCONS}")
    L.append(f"- distractor == observation violations: n={len(DIS_EQ_OBS)} ids={DIS_EQ_OBS}")
    L.append(f"- integer/text disagreement (dump): n={len(T_dump)} ids={T_dump}")
    L.append(f"- integer/text disagreement (observation): n={len(T_obs)} ids={T_obs}")
    L.append(f"- integer/text disagreement (distractor): n={len(T_dis)} ids={T_dis}")
    L.append("")
    L.append("## False-id classification (12 deliberate falsehoods)")
    for i in sorted(FALSE_IDS):
        L.append(f"- id {i}: {cls[i]} (given={GIVEN[i]}, truth={TRUE[i]})")
    L.append("")
    nrep = sum(1 for i in FALSE_IDS if cls[i].startswith("reproduce"))
    L.append(f"reproduced (faithful): {nrep}/12")

    out = os.path.join(HY3, "ERROR_INVENTORY.md")
    open(out, "w").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
