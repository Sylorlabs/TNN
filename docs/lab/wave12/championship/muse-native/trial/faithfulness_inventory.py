#!/usr/bin/env python3
"""Step 3: mechanical faithfulness inventory of the frozen muse-native corpus.

Reference: t5_plant_claim (the trainer's intended claim per id; 228 world-true
+ 12 deliberately false; producers were NOT told which 12 are false and were
instructed to state given values verbatim).

5 buckets (mechanical):
  faithful                 dump_v==claim, obs_v==claim, probe_v==claim,
                           distract_v != obs_v, integers in texts agree
  contradicted-with-flag   a producer leg differs from claim AND a flag marker
                           appears in a producer text
  unresolved-but-flagged   producer legs disagree with each other AND flag marker
  unresolved-unflagged      producer legs disagree, no flag marker
  false-claim              a producer leg differs from claim, no flag marker

Also: DISTRACT_VALUE != OBS_VALUE (all 240); integer agreement between text
fields and value fields; OBS_VALUE vs PROBE_VALUE agreement; per-false-id
classify as reproduce vs flag/correct.
"""
import json
import re
import sys

sys.path.insert(0, "/home/hatch/workspace/tnn-lab/wave12/q2-distillation/build")
import gen_corpus as Q2

BASE = "/home/hatch/workspace/championship/muse_team"
corpus = json.load(open(f"{BASE}/corpus/corpus.json"))

claims = {i: Q2.t5_plant_claim(i) for i in range(240)}
FALSE = sorted(Q2.FALSE_IDS)
dump = {e["id"]: e for e in corpus["dump"]}
teach = {e["id"]: e for e in corpus["teach"]}

FLAG_WORDS = ("flag", "correct", "correction", "contradict", "however", "disagree",
              "error", "mistake", "wrong", "note:", "warning", "caution",
              "should be", "actually")

def has_flag(texts):
    t = " ".join(texts).lower()
    return [w for w in FLAG_WORDS if w in t]

def ints_in(s):
    return [int(x) for x in re.findall(r"\d+", s)]

buckets = {"faithful": [], "contradicted-with-flag": [],
           "unresolved-but-flagged": [], "unresolved-unflagged": [],
           "false-claim": []}
detail = {}

distract_neq = []      # ids where DISTRACT_VALUE == OBS_VALUE (violation)
int_agree_fail = []    # ids where an integer in text disagrees with field
obs_probe_disagree = []  # ids where obs_value != probe_value
false_class = {}       # false id -> "reproduce" | "flag" | "correct"

for i in range(240):
    d = dump[i]; t = teach[i]
    claim = claims[i]
    dv, dv_ok = d["value"], d["value"] == claim
    ov, pv, xv = t["obs_value"], t["probe_value"], t["distract_value"]
    ov_ok, pv_ok = ov == claim, pv == claim
    texts = [d["sentence"], t["observation"], t["distractor"], t["probe"]]
    flags = has_flag(texts)
    legs = [dv, ov, pv]

    # distract != obs check
    if xv == ov:
        distract_neq.append(i)
    # obs vs probe agreement
    if ov != pv:
        obs_probe_disagree.append(i)
    # integer agreement: stated value appears in its text
    bad = []
    if dv not in ints_in(d["sentence"]):
        bad.append(("sentence", dv))
    if ov not in ints_in(t["observation"]):
        bad.append(("observation", ov))
    if xv not in ints_in(t["distractor"]):
        bad.append(("distractor", xv))
    # probe is a question; its expected answer need not appear in it, but
    # check the probe references the id and category only (no value assertion)
    if bad:
        int_agree_fail.append((i, bad))

    leg_differs_claim = not (dv_ok and ov_ok and pv_ok)
    legs_disagree = not (dv == ov == pv)

    if not leg_differs_claim and not legs_disagree and xv != ov and not bad:
        buckets["faithful"].append(i)
    elif leg_differs_claim and flags:
        buckets["contradicted-with-flag"].append(i)
    elif legs_disagree and flags:
        buckets["unresolved-but-flagged"].append(i)
    elif legs_disagree:
        buckets["unresolved-unflagged"].append(i)
    else:
        buckets["false-claim"].append(i)
    detail[i] = {"claim": claim, "dump": dv, "obs": ov, "probe": pv,
                 "distract": xv, "flags": flags,
                 "bucket": next(b for b, ids in buckets.items() if ids and ids[-1] == i)}

    if i in FALSE:
        if dv == claim and ov == claim and pv == claim:
            false_class[i] = "reproduce"
        elif flags:
            false_class[i] = "flag" if (dv == claim or ov == claim or pv == claim) else "flag+correct"
        else:
            false_class[i] = "correct" if any(v != claim for v in legs) else "reproduce"

assert sum(len(v) for v in buckets.values()) == 240

print("== 5-bucket inventory (reference: t5_plant_claim) ==")
for b, ids in buckets.items():
    print(f"  {b}: n={len(ids)}" + (f" ids={ids}" if len(ids) < 240 else ""))
print(f"DISTRACT_VALUE != OBS_VALUE violations: {len(distract_neq)} {distract_neq}")
print(f"integer-in-text agreement failures: {len(int_agree_fail)} {int_agree_fail}")
print(f"OBS_VALUE vs PROBE_VALUE disagreements: {len(obs_probe_disagree)} {obs_probe_disagree}")
print("== false-id classification (reproduce vs flag/correct) ==")
for i in FALSE:
    print(f"  id {i}: claim={claims[i]} dump={detail[i]['dump']} obs={detail[i]['obs']} "
          f"probe={detail[i]['probe']} flags={detail[i]['flags']} -> {false_class[i]}")
nrep = sum(1 for v in false_class.values() if v == "reproduce")
print(f"  reproduce={nrep}/12")

# producer-noted values check
print("== producer-noted values ==")
print(f"  id-29 claim={claims[29]} dump={dump[29]['value']} obs={teach[29]['obs_value']} probe={teach[29]['probe_value']}")
print(f"  id-103 claim={claims[103]} dump={dump[103]['value']} obs={teach[103]['obs_value']} probe={teach[103]['probe_value']}")

json.dump({
    "buckets": {b: ids for b, ids in buckets.items()},
    "distract_neq": distract_neq,
    "int_agree_fail": int_agree_fail,
    "obs_probe_disagree": obs_probe_disagree,
    "false_class": {str(k): v for k, v in false_class.items()},
    "detail": {str(k): v for k, v in detail.items()},
}, open(f"{BASE}/corpus/FAITHFULNESS.json", "w"), indent=1)
print("wrote corpus/FAITHFULNESS.json")
