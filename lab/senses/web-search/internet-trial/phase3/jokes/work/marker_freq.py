#!/usr/bin/env python3
"""Training-only marker frequency analysis (phase 3 joke volume gate).

Input: corpus/training_corpus.json (300 items). NEVER touches held-out.
Output: work/marker_analysis.json + printed tables for TRAINING_RECORD.md.

Support rule (VOLUME_RATIONALE.md): no marker enters the decision vocabulary
on fewer than 4 exemplars (document frequency >= 4).
"""
import json, re, os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CORP = os.path.join(os.path.dirname(HERE), "corpus", "training_corpus.json")

STOP = set("""a an the and or but of to in on for with at by from as is are was were
be been being it its it's this that these those i you he she we they them his her
their our your my me him us so such no not noone none just very can could would
should will shall may might must do does did done have has had having what when
where who whom which how why if then than too also only even ever never always
often all any both each few more most other some such own same there here
out up down over under again once about into through during before after above
below between out off up s t d ll ve re m don doesn didn isn aren wasn weren
hasn haven hadn wouldn couldn shouldn won't can't cannot every per vs via
yourself himself herself themselves itself me my mine his hers ours yours
theirs am pm ok hey hi oh well now today tonight tomorrow yesterday still yet
already even back away along around among within without within""".split())

def toks(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9'\- ]", " ", text)
    return [t for t in text.split() if t and t not in STOP and len(t) > 1
            and not t.replace('.','',1).replace("'",'').isdigit()]

def main():
    d = json.load(open(CORP, encoding="utf-8"))
    items = d["items"]
    assert len(items) == 300
    fams = ["F1", "F2", "F3", "F4"]
    df = Counter()            # token -> # items containing it
    df_fam = {f: Counter() for f in fams}
    for it in items:
        ts = set(toks(it["title"] + " " + it["body"]))
        for t in ts:
            df[t] += 1
            df_fam[it["family"]][t] += 1
    # candidates: df >= 4
    cand = {t: n for t, n in df.items() if n >= 4}
    print(f"distinct tokens: {len(df)}, candidates df>=4: {len(cand)}")
    # per-family association: fam_df / total_df
    rows = []
    for t, n in sorted(cand.items(), key=lambda kv: -kv[1]):
        assoc = {f: df_fam[f][t] for f in fams}
        dom = max(fams, key=lambda f: assoc[f])
        rows.append((t, n, assoc["F1"], assoc["F2"], assoc["F3"], assoc["F4"], dom))
    print("\ntoken | df | F1 F2 F3 F4 | dominant")
    for r in rows:
        print(f"{r[0]:22s} {r[1]:3d}  {r[2]:3d} {r[3]:3d} {r[4]:3d} {r[5]:3d}  {r[6]}")
    json.dump({"tokens": [
        {"t": t, "df": n, "f1": a, "f2": b, "f3": c, "f4": e, "dom": dom}
        for (t, n, a, b, c, e, dom) in rows]},
        open(os.path.join(HERE, "marker_analysis.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
