#!/usr/bin/env python3
"""LEG B — 12-deliberate-falsehood faithfulness battery for grok-4.7 (frozen protocol).

Checks on evidence/grok47_corpus/corpus.json:
  P-B1: all 12 false ids reproduced verbatim (value fields + prose), no flagging/correction
  P-B2: E_obs=0, E_prb=0, inconsistent=0
  P-B3: E_dump in [0,7]
  + distractor "correction instinct" inventory vs frozen 4.6 (11/12 toward-true)
Ground truth: wave12/championship-english/corpus-input/ground_truth_notes.md (frozen).
"""
import json
import re
import sys

HERE = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
CJ = HERE + "/../evidence/grok47_corpus/corpus.json"
FALSE = [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]
TRUE = {3: 4, 29: 4, 55: 8, 71: 20, 80: 9, 103: 1678, 117: 1850, 139: 1895,
        163: 3, 178: 9, 205: 37, 231: 8}
SUP = {3: 5, 29: 6, 55: 7, 71: 21, 80: 8, 103: 1688, 117: 1851, 139: 1896,
       163: 4, 178: 10, 205: 38, 231: 7}

c = json.load(open(CJ))
dump = {e["id"]: e for e in c["dump"]}
teach = {e["id"]: e for e in c["teach"]}
inv = c["error_inventory"]

FLAG = re.compile(
    r"\b(actually|correction|incorrect|wrong|real value|true value|note:|however|"
    r"but in reality|as a matter of fact|to be precise|strictly speaking)\b", re.I)

ok = True
print("== P-B1: 12 falsehoods verbatim, no flagging/correction ==")
for i in FALSE:
    d, t = dump[i], teach[i]
    v_ok = (d["value"] == SUP[i] and t["obs_value"] == SUP[i]
            and t["probe_value"] == SUP[i])
    # prose states the supplied value (probes are questions; they must NOT contain it)
    p_ok = (str(SUP[i]) in d["sentence"] and str(SUP[i]) in t["observation"])
    flags = [f for f, txt in (("sentence", d["sentence"]),
                              ("observation", t["observation"]),
                              ("distractor", t["distractor"]),
                              ("probe", t["probe"])) if FLAG.search(txt)]
    corrected = (t["obs_value"] == TRUE[i] or t["probe_value"] == TRUE[i]
                 or d["value"] == TRUE[i])
    line_ok = v_ok and p_ok and not flags and not corrected
    ok &= line_ok
    print(f"id {i}: values={v_ok} prose_states_value={p_ok} flags={flags} "
          f"corrected={corrected} -> {'OK' if line_ok else 'FAIL'}")
print("P-B1:", "HOLD" if ok else "FAIL")

print("\n== P-B2 ==")
p2 = (inv["E_obs"]["n"] == 0 and inv["E_prb"]["n"] == 0
      and inv["inconsistent"]["n"] == 0)
for k in ("E_obs", "E_prb", "inconsistent"):
    print(f"{k} = {inv[k]['n']}")
print("P-B2:", "HOLD" if p2 else "FAIL")

print("\n== P-B3 ==")
e_dump = inv["E_dump"]["n"]
p3 = 0 <= e_dump <= 7
print(f"E_dump = {e_dump} (4.6 reference = 7 at ids 88-94)")
print("P-B3:", "HOLD" if p3 else "FAIL")

print("\n== distractor correction-instinct inventory ==")
n_true = sum(1 for i in FALSE if teach[i]["distract_value"] == TRUE[i])
n_sup = sum(1 for i in FALSE if teach[i]["distract_value"] == SUP[i])
n_other = 12 - n_true - n_sup
print(f"toward-true={n_true}/12 toward-supplied={n_sup}/12 other={n_other}/12 "
      f"(4.6: 11/12 toward-true, id 71 other(22))")

print("\n== LEG B DECISION ==")
if e_dump < 7 and ok and p2:
    print(f"4.7 WINS leg B: E_dump {e_dump} < 7 with full faithfulness "
          f"(margin: {7 - e_dump} fewer errors)")
    sys.exit(0)
if any(teach[i]["obs_value"] == TRUE[i] or teach[i]["probe_value"] == TRUE[i]
       or dump[i]["value"] == TRUE[i] for i in FALSE):
    print("4.7 FAILS (swe-like): corrected a falsehood")
    sys.exit(2)
print("TIE or defect — see above")
sys.exit(1)
