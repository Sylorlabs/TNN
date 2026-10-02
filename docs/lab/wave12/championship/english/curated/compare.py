#!/usr/bin/env python3
"""PURE-MUSE CURATION crew: deliberation-protocol comparison pass v2.

Protocol (deliberated from the frozen prompt ENGLISH_PROMPT_SET.md):
- The TEACH VALUE = the fact taught: obs_value (observation), probe_value
  (must equal obs), dump_value (planted as trainer evidence in D1).
  The frozen prompt REQUIRES obs/probe to state the GIVEN (supplied) value
  exactly; DISTRACT_VALUE is "an integer DIFFERENT from OBS_VALUE" chosen
  by each teacher -- variation across teachers is BY DESIGN, not disagreement.
- ADOPT iff: unanimous 5-source agreement on (obs, probe, dump) AND the
  unanimous fact == the frozen prompt's supplied claim (claim envelope) AND
  every row is mechanically valid (ints parse; probe==obs; obs text contains
  obs; dump sentence contains dump value).
- Distractor: defective distractors (== obs, non-int, text/value mismatch)
  are EXCLUDED from selection; the crew selects one healthy distractor per
  id by majority vote, ties -> closest to obs, then lowest. Recorded.
- ANY fact disagreement or envelope break -> WITHHOLD + AUDIT.

The `false` flag / `false_ids` in facts.json are NEVER read here.
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(BASE, "..")
SOURCES = ["sol", "grok", "step", "swe", "muse-native"]

corpora = {}
for s in SOURCES:
    with open(os.path.join(CH, s, "corpus", "corpus.json")) as f:
        corpora[s] = json.load(f)

facts = json.load(open(os.path.join(CH, "corpus-input", "facts.json")))
supplied = {int(k): (facts[k]["category"], facts[k]["claim_text"],
                     facts[k]["value"])
            for k in facts if k not in ("false_ids", "meta")}

# Crew deliberation (ids 0-11, 230, 231): some teachers spell the value as an
# English word ("first", "seven") instead of digits. The sentence still states
# the value unambiguously, and the numeric lane (what the learner consumes)
# is unanimous. The crew judges this a benign wording variation, NOT a
# mechanical defect. Normalize before the text-contains-value check.
WORD2N = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
          "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
          "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
          "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
          "twenty": 20, "thirty": 30,
          "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
          "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
          "eleventh": 11, "twelfth": 12}


def text_states_value(text, value):
    if str(value) in text:
        return True
    import re
    for w in re.findall(r"[a-z]+", text.lower()):
        if WORD2N.get(w) == value:
            return True
    return False


def row_defects(row, dump_val, dump_sent):
    d = []
    for k in ("obs_value", "distract_value", "probe_value"):
        v = row.get(k)
        if not isinstance(v, int) or isinstance(v, bool):
            d.append(f"{k} not int: {v!r}")
    for k in ("observation", "distractor", "probe"):
        v = row.get(k)
        if not isinstance(v, str) or not v.strip():
            d.append(f"{k} empty/non-str")
    if d:
        return d, True
    if row["probe_value"] != row["obs_value"]:
        d.append(f"probe {row['probe_value']} != obs {row['obs_value']}")
    if not text_states_value(row["observation"], row["obs_value"]):
        d.append("observation text lacks obs_value")
    if not isinstance(dump_val, int) or isinstance(dump_val, bool):
        d.append(f"dump value not int: {dump_val!r}")
    elif not dump_sent or not text_states_value(dump_sent, dump_val):
        d.append("dump sentence lacks dump value")
    return d, False


def distract_defects(row):
    d = []
    dv = row.get("distract_value")
    if not isinstance(dv, int) or isinstance(dv, bool):
        return ["distract_value not int"]
    if dv == row.get("obs_value"):
        d.append(f"distract_value == obs_value ({dv}): prompt requires DIFFERENT")
    if not text_states_value(row.get("distractor", ""), dv):
        d.append("distractor text lacks distract_value")
    return d


records = []
for i in range(240):
    rows, dumps, dsents = {}, {}, {}
    for s in SOURCES:
        rows[s] = next(r for r in corpora[s]["teach"] if r["id"] == i)
        dr = next(r for r in corpora[s]["dump"] if r["id"] == i)
        dumps[s] = dr["value"]
        dsents[s] = dr["sentence"]
    fact_def = {s: row_defects(rows[s], dumps[s], dsents[s])[0]
                for s in SOURCES}
    fact_def = {s: v for s, v in fact_def.items() if v}
    dis_def = {s: distract_defects(rows[s]) for s in SOURCES}
    dis_def = {s: v for s, v in dis_def.items() if v}

    obs = [rows[s]["obs_value"] for s in SOURCES]
    prb = [rows[s]["probe_value"] for s in SOURCES]
    dmp = [dumps[s] for s in SOURCES]
    fact_agree = len(set(obs)) == 1 and len(set(prb)) == 1 and len(set(dmp)) == 1
    cat, claim_text, sup_val = supplied[i]
    envelope = fact_agree and obs[0] == sup_val and dmp[0] == sup_val

    # distractor selection: healthy candidates only
    healthy = {s: rows[s]["distract_value"] for s in SOURCES if s not in dis_def}
    chosen, chosen_src, sel_reason = None, None, None
    if healthy:
        vals = list(healthy.values())
        counts = {}
        for v in vals:
            counts[v] = counts.get(v, 0) + 1
        top = max(counts.values())
        cands = sorted(v for v, c in counts.items() if c == top)
        if len(cands) == 1:
            chosen = cands[0]
            sel_reason = f"majority {top}/5"
        else:
            bydist = sorted(cands, key=lambda v: (abs(v - obs[0]), v))
            chosen = bydist[0]
            sel_reason = (f"tie {[ (v, counts[v]) for v in cands ]} -> "
                          f"closest to obs {chosen}")
        # text source: first source (in order) with the chosen value
        for s in SOURCES:
            if s in healthy and healthy[s] == chosen:
                chosen_src = s
                break
    else:
        sel_reason = "NO HEALTHY DISTRACTOR"

    reasons = []
    if not fact_agree:
        reasons.append(
            "FACT DISAGREEMENT obs=%s probe=%s dump=%s" % (obs, prb, dmp))
    if fact_def:
        reasons.append("fact mechanical defects: %s" % fact_def)
    if fact_agree and not envelope:
        reasons.append(
            f"ENVELOPE BREAK: taught obs={obs[0]} dump={dmp[0]} vs "
            f"supplied claim={sup_val}")
    if not healthy:
        reasons.append("no healthy distractor available")
    decision = "ADOPT" if not reasons else "WITHHOLD"
    records.append({
        "id": i, "category": cat, "claim_text": claim_text,
        "supplied_value": sup_val,
        "obs": {s: rows[s]["obs_value"] for s in SOURCES},
        "probe": {s: rows[s]["probe_value"] for s in SOURCES},
        "dump": dumps,
        "distract": {s: rows[s]["distract_value"] for s in SOURCES},
        "fact_agree": fact_agree, "fact_defects": fact_def,
        "distract_defects": dis_def,
        "envelope_ok": envelope,
        "chosen_distract": chosen, "chosen_src": chosen_src,
        "selection_reason": sel_reason,
        "decision": decision, "reasons": reasons,
        "texts": {s: {"observation": rows[s]["observation"],
                      "distractor": rows[s]["distractor"],
                      "probe": rows[s]["probe"],
                      "dump_sentence": dsents[s]} for s in SOURCES},
    })

adopt = [r for r in records if r["decision"] == "ADOPT"]
withhold = [r for r in records if r["decision"] == "WITHHOLD"]
print(f"ADOPT: {len(adopt)} / WITHHOLD: {len(withhold)}")
for r in withhold:
    print(f"  id {r['id']:3d} ({r['category']:9s} '{r['claim_text']}' sup={r['supplied_value']}): "
          + "; ".join(r["reasons"]))
# distractor defect summary
nd = sum(1 for r in records if r["distract_defects"])
print(f"ids with >=1 defective distractor: {nd}")
for r in records:
    if r["distract_defects"]:
        print(f"  id {r['id']}: {r['distract_defects']} -> chose {r['chosen_distract']} "
              f"({r['selection_reason']}, text from {r['chosen_src']})")
with open(os.path.join(BASE, "comparison.json"), "w") as f:
    json.dump(records, f, indent=1)
print("wrote comparison.json")
