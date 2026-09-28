#!/usr/bin/env python3
"""Crew oracle for LH-ADV-2026-09-22: generates the 54 frozen behavior contracts.

This is CREW TOOLING (used once, pre-freeze, to author contracts), NOT trial
machinery. It is never invoked during the trial run. The TNN deliberation
re-derives every stage's spec from DESC+KB at run time; this oracle is the
ground truth it must match (TEST out= lines).

Op semantics here are the frozen reference. adv_emit.zag and adv_critic.zag
implement these independently in Zag; agreement is verified in smoke test.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CDIR = HERE

FIXTURES = {
    "P1": [  # sales: id|product|quantity|price|region
        "1|apple|5|10|N", "2|banana|0|20|S", "3|cherry|1500|5|E",
        "4|date|3|30|W", "5|elderberry|2|50|N", "6|fig|1|15|X",
        "7|grape|4|25|S", "8|honeydew|2000|8|E",
    ],
    "P2": [  # inventory: sku|item|stock|reorder|warehouse
        "S1|nails|50|100|N", "S2|screws|200|100|S", "S3|bolts|30|30|E",
        "S4|washers|0|50|W", "S5|nuts|150|200|N", "S6|pins|80|80|X",
    ],
    "P3": [  # logs: ts|level|msg|code
        "100|ERROR|disk full|500", "101|WARN|high mem|300", "102|INFO|started|0",
        "103|ERROR|net down|501", "104|WARN|slow disk|0", "105|ERROR|disk full|502",
    ],
    "P4": [  # users: uid|name|age|city|tier
        "U1|Ann|25|SF|gold", "U2|Bob|17|LA|silver", "U3|Cat|30|SF|gold",
        "U4|Dan|16|NY|bronze", "U5|Eve|22|LA|gold", "U6|Fin|40|SF|silver",
    ],
    "P5": [  # telemetry: dev|metric|value|region|ts
        "D1|cpu|80|N|1000", "D2|mem|60|S|1001", "D3|cpu|90|N|1002",
        "D4|disk|70|E|1003", "D5|cpu|50|W|1004", "D6|mem|95|S|1005",
    ],
}

def pint(s):
    v, neg, seen = 0, False, False
    for ch in s:
        if ch == "-" and not seen: neg = True
        elif ch.isdigit(): v = v * 10 + int(ch); seen = True
    return -v if neg else v

# ---- op implementations (frozen reference semantics) ----
def op_upper(recs, k): return [r[:k-1] + [r[k-1].upper()] + r[k:] for r in recs]
def op_lower(recs, k): return [r[:k-1] + [r[k-1].lower()] + r[k:] for r in recs]
def op_clamp(recs, k, lo, hi):
    return [r[:k-1] + [str(max(lo, min(hi, pint(r[k-1]))))] + r[k:] for r in recs]
def op_mul_fields(recs, fa, fb):
    return [r + [str(pint(r[fa-1]) * pint(r[fb-1]))] for r in recs]
def op_substr(recs, k, s, l):
    return [r + [r[k-1][s:s+l]] for r in recs]
def op_int_gt(recs, k, t): return [r for r in recs if pint(r[k-1]) > t]
def op_int_lt(recs, k, t): return [r for r in recs if pint(r[k-1]) < t]
def op_int_ge(recs, k, t): return [r for r in recs if pint(r[k-1]) >= t]
def op_in_set(recs, k, s): return [r for r in recs if r[k-1] in s]
def op_field_count_eq(recs, n): return [r for r in recs if len(r) == n]

def groups(recs, k):
    order, d = [], {}
    for r in recs:
        key = r[k-1]
        if key not in d: d[key] = []; order.append(key)
        d[key].append(r)
    return [(key, d[key]) for key in order]

def op_sum(recs, k, v): return [[key, str(sum(pint(r[v-1]) for r in g)), str(len(g))] for key, g in groups(recs, k)]
def op_count(recs, k): return [[key, str(len(g))] for key, g in groups(recs, k)]
def op_avg(recs, k, v):
    return [[key, str(sum(pint(r[v-1]) for r in g) // len(g)), str(len(g))] for key, g in groups(recs, k)]
def op_min(recs, k, v): return [[key, str(min(pint(r[v-1]) for r in g)), str(len(g))] for key, g in groups(recs, k)]
def op_max(recs, k, v): return [[key, str(max(pint(r[v-1]) for r in g)), str(len(g))] for key, g in groups(recs, k)]

def op_sort_desc(recs, k, take):
    s = sorted(recs, key=lambda r: pint(r[k-1]), reverse=True)
    return s[:take] if take else s
def op_sort_asc(recs, k, take):
    s = sorted(recs, key=lambda r: pint(r[k-1]))
    return s[:take] if take else s
def op_topn(recs, k, n): return op_sort_desc(recs, k, n)

def op_inner_join(L, R, lk, rk):
    return [l + r for l in L for r in R if l[lk-1] == r[rk-1]]
def op_left_join(L, R, lk, rk, rf):
    out = []
    for l in L:
        m = [l + r for r in R if l[lk-1] == r[rk-1]]
        out.extend(m if m else [l + [""] * rf])
    return out
def op_cross_join(L, R): return [l + r for l in L for r in R]

def op_template(recs, t):
    def sub(m):
        i = int(m.group(1)) - 1
        return rec[i] if 0 <= i < len(rec) else ""
    out = []
    for rec in recs:
        out.append([re.sub(r"\{(\d+)\}", sub, t)])
    return out
def op_csv_line(recs): return [[",".join(r)] for r in recs]
def op_kv_line(recs, names): return [["|".join(f"{n}={v}" for n, v in zip(names, r))] for r in recs]

# ---- stage table: (id, cat, op, desc, deps, params, win) ----
# params: op-specific; win: for sources; deps drive chaining.
S = []
def stage(sid, cat, op, desc, deps, params, win=None, winl=None, winr=None):
    S.append(dict(id=sid, cat=cat, op=op, desc=desc, deps=deps, params=params,
                  win=win, winl=winl, winr=winr))

# Pipeline A (sales)
stage("A1","FIELD","upper","uppercase the product field",[],dict(k=2),win="id|product|quantity|price|region")
stage("A2","FILTER","int_gt","keep records where quantity is greater than 0",["A1"],dict(k=3,t=0))
stage("A3","FIELD","clamp","clamp quantity between 1 and 1000",["A2"],dict(k=3,lo=1,hi=1000))
stage("A4","FIELD","mul_fields","multiply quantity by price, appending the result as a new field named total",["A3"],dict(fa=3,fb=4,newfield="total"))
stage("A5","FILTER","int_ge","keep records where total is at least 100",["A4"],dict(k=6,t=100))
stage("A6","FILTER","in_set","keep records where region is one of {N,S,E,W}",["A5"],dict(k=5,s=["N","S","E","W"]))
stage("A7","FIELD","substr","extract the substring of product from 0 with length 3, appending as a new field named prod3",["A6"],dict(k=2,s=0,l=3,newfield="prod3"))
stage("A8","AGG","sum","sum by region of total",["A7"],dict(k=5,v=6))
stage("A9","SORT","sort_desc","sort by the sumv in descending order",["A8"],dict(k=2,take=0))
stage("A10","FORMAT","template","format each record with the template '{region}: {sumv} ({n})'",["A9"],dict(t="{1}: {2} ({3})"))
# Pipeline B (inventory)
stage("B1","FIELD","lower","lowercase the item field",[],dict(k=2),win="sku|item|stock|reorder|warehouse")
stage("B2","FILTER","int_lt","keep records where stock is less than 100",["B1"],dict(k=3,t=100))
stage("B3","FIELD","substr","extract the substring of item from 0 with length 3, appending as a new field named item3",["B2"],dict(k=2,s=0,l=3,newfield="item3"))
stage("B4","FIELD","clamp","clamp stock between 0 and 60",["B3"],dict(k=3,lo=0,hi=60))
stage("B5","FILTER","in_set","keep records where warehouse is one of {N,S,E,W}",["B4"],dict(k=5,s=["N","S","E","W"]))
stage("B6","AGG","count","count by warehouse",["B5"],dict(k=5))
stage("B7","SORT","topn","take the top 3 by n",["B6"],dict(k=2,n=3))
stage("B8","AGG","max","maximum by warehouse of stock",["B5"],dict(k=5,v=3))
stage("B9","AGG","sum","sum by warehouse of stock",["B5"],dict(k=5,v=3))
stage("B10","FORMAT","kv_line","format each record as name equals value pairs",["B9"],dict(names=["warehouse","sumv","n"]))
# Pipeline C (logs)
stage("C1","FILTER","field_count_eq","keep records with exactly 4 fields",[],dict(n=4),win="ts|level|msg|code")
stage("C2","FILTER","in_set","keep records where level is one of {ERROR,WARN}",["C1"],dict(k=2,s=["ERROR","WARN"]))
stage("C3","FIELD","upper","uppercase the level field",["C2"],dict(k=2))
stage("C4","FIELD","substr","extract the substring of msg from 0 with length 8, appending as a new field named msg8",["C3"],dict(k=3,s=0,l=8,newfield="msg8"))
stage("C5","FILTER","int_gt","keep records where code is greater than 0",["C4"],dict(k=4,t=0))
stage("C6","FIELD","lower","lowercase the msg field",["C5"],dict(k=3))
stage("C7","AGG","count","count by level",["C6"],dict(k=2))
stage("C8","SORT","sort_desc","sort by n in descending order",["C7"],dict(k=2,take=0))
stage("C9","AGG","min","minimum by level of code",["C6"],dict(k=2,v=4))
stage("C10","FORMAT","csv_line","format each record as a comma separated csv line",["C8"],dict())
# Pipeline D (users)
stage("D1","FIELD","upper","uppercase the name field",[],dict(k=2),win="uid|name|age|city|tier")
stage("D2","FILTER","int_lt","keep records where age is less than 65",["D1"],dict(k=3,t=65))
stage("D3","FIELD","clamp","clamp age between 0 and 120",["D2"],dict(k=3,lo=0,hi=120))
stage("D4","FILTER","in_set","keep records where tier is one of {gold,silver}",["D3"],dict(k=5,s=["gold","silver"]))
stage("D5","AGG","count","count by city",["D4"],dict(k=4))
stage("D6","AGG","avg","average by city of age",["D4"],dict(k=4,v=3))
stage("D7","SORT","sort_asc","sort by avgv in ascending order",["D6"],dict(k=2,take=0))
stage("D8","FIELD","substr","extract the substring of name from 0 with length 1, appending as a new field named initial",["D4"],dict(k=2,s=0,l=1,newfield="initial"))
stage("D9","AGG","count","count by tier",["D4"],dict(k=5))
stage("D10","FORMAT","template","format each record with the template '{city} avg {avgv} n {n}'",["D7"],dict(t="{1} avg {2} n {3}"))
# Pipeline E (telemetry)
stage("E1","FILTER","int_gt","keep records where value is greater than 70",[],dict(k=3,t=70),win="dev|metric|value|region|ts")
stage("E2","FIELD","clamp","clamp value between 0 and 100",["E1"],dict(k=3,lo=0,hi=100))
stage("E3","AGG","sum","sum by region of value",["E2"],dict(k=4,v=3))
stage("E4","AGG","max","maximum for each metric of value",["E2"],dict(k=2,v=3))
stage("E5","SORT","sort_desc","sort by value in descending order",["E2"],dict(k=3,take=0))
stage("E6","FIELD","lower","lowercase the metric field",["E2"],dict(k=2))
stage("E7","FILTER","in_set","keep records where metric is one of {cpu,mem}",["E6"],dict(k=2,s=["cpu","mem"]))
stage("E8","AGG","avg","average by region of value",["E2"],dict(k=4,v=3))
stage("E9","SORT","topn","take the top 2 by avgv",["E8"],dict(k=2,n=2))
stage("E10","FORMAT","template","format each record with the template '{region} {avgv}'",["E9"],dict(t="{1} {2}"))
# JOINs
stage("J1","JOIN","inner_join","join the left records with the right records where the first field of the left equals the first field of the right, appending the right record",["A9","B9"],dict(lk=1,rk=1),winl="region|sumv|n",winr="warehouse|sumv|n")
stage("J2","JOIN","cross_join","combine every left record with every right record, appending the right record",["C8","D9"],dict(),winl="level|n",winr="tier|n")
stage("J3","JOIN","left_join","for each left record, append the right records where the first field of the left equals the first field of the right; keep left records with no match, appending empty right fields",["E3","A8"],dict(lk=1,rk=1,rf=3),winl="region|sumv|n",winr="region|sumv|n")
# honest-halt probe
stage("F1","FIELD","ROT13","apply ROT13 cipher to product",[],dict(),win="id|product|quantity|price|region")

AGG_SUFFIX = {"sum":"sumv", "count":None, "avg":"avgv", "min":"minv", "max":"maxv"}
def agg_win(wfields, k, op):
    kn = wfields[k-1]
    suf = AGG_SUFFIX[op]
    return kn + "|n" if suf is None else kn + "|" + suf + "|n"

def apply(st, recs, recs2=None):
    p, op = st["params"], st["op"]
    if op=="upper": return op_upper(recs,p["k"])
    if op=="lower": return op_lower(recs,p["k"])
    if op=="clamp": return op_clamp(recs,p["k"],p["lo"],p["hi"])
    if op=="mul_fields": return op_mul_fields(recs,p["fa"],p["fb"])
    if op=="substr": return op_substr(recs,p["k"],p["s"],p["l"])
    if op=="int_gt": return op_int_gt(recs,p["k"],p["t"])
    if op=="int_lt": return op_int_lt(recs,p["k"],p["t"])
    if op=="int_ge": return op_int_ge(recs,p["k"],p["t"])
    if op=="in_set": return op_in_set(recs,p["k"],p["s"])
    if op=="field_count_eq": return op_field_count_eq(recs,p["n"])
    if op=="sum": return op_sum(recs,p["k"],p["v"])
    if op=="count": return op_count(recs,p["k"])
    if op=="avg": return op_avg(recs,p["k"],p["v"])
    if op=="min": return op_min(recs,p["k"],p["v"])
    if op=="max": return op_max(recs,p["k"],p["v"])
    if op=="sort_desc": return op_sort_desc(recs,p["k"],p["take"])
    if op=="sort_asc": return op_sort_asc(recs,p["k"],p["take"])
    if op=="topn": return op_topn(recs,p["k"],p["n"])
    if op=="inner_join": return op_inner_join(recs,recs2,p["lk"],p["rk"])
    if op=="left_join": return op_left_join(recs,recs2,p["lk"],p["rk"],p["rf"])
    if op=="cross_join": return op_cross_join(recs,recs2)
    if op=="template": return op_template(recs,p["t"])
    if op=="csv_line": return op_csv_line(recs)
    if op=="kv_line": return op_kv_line(recs,p["names"])
    raise ValueError(op)

def win_of(st, stmap):
    if st["win"]: return st["win"]
    if st["cat"]=="JOIN": return None
    if st["cat"]=="AGG":
        w = win_of(stmap[st["deps"][0]], stmap).split("|")
        return agg_win(w, st["params"]["k"], st["op"])
    if st["op"] in ("mul_fields","substr"):
        return win_of(stmap[st["deps"][0]], stmap) + "|" + st["params"].get("newfield","new")
    d = stmap[st["deps"][0]]
    return d["win"] if d["win"] else win_of(d, stmap)

def main():
    stmap = {st["id"]: st for st in S}
    # F1 win
    stmap["F1"]["win"] = "id|product|quantity|price|region"
    os.makedirs(CDIR, exist_ok=True)
    src_of = {"A1":"P1","B1":"P2","C1":"P3","D1":"P4","E1":"P5","F1":"P1"}
    order = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10",
             "B1","B2","B3","B4","B5","B6","B7","B8","B9","B10",
             "C1","C2","C3","C4","C5","C6","C7","C8","C9","C10",
             "D1","D2","D3","D4","D5","D6","D7","D8","D9","D10",
             "E1","E2","E3","E4","E5","E6","E7","E8","E9","E10",
             "J1","J2","J3","F1"]
    inputs, outputs = {}, {}
    for sid in order:
        st = stmap[sid]
        if sid in src_of:
            recs = [r.split("|") for r in FIXTURES[src_of[sid]]]
            inputs[sid] = recs; recs2 = None
        elif st["cat"]=="JOIN":
            recs = outputs[st["deps"][0]]; recs2 = outputs[st["deps"][1]]
            inputs[sid] = recs
        else:
            recs = outputs[st["deps"][0]]; recs2 = None
            inputs[sid] = recs
        outputs[sid] = apply(st, recs, recs2) if sid!="F1" else []
        w = win_of(st, stmap)
        # TEST1: chain
        if st["cat"]=="JOIN":
            in1 = ";".join("|".join(r) for r in recs) + "||" + ";".join("|".join(r) for r in recs2)
        else:
            in1 = ";".join("|".join(r) for r in recs)
        out1 = ";".join("|".join(r) for r in outputs[sid])
        # TEST2: small static edge
        if sid == "F1":
            in2, out2 = in1, ""
        elif st["cat"]=="JOIN":
            r2a = recs[:1]; r2b = recs2[:1]
            in2 = ";".join("|".join(r) for r in r2a) + "||" + ";".join("|".join(r) for r in r2b)
            out2 = ";".join("|".join(r) for r in apply(st, r2a, r2b))
        elif st["cat"] in ("AGG","SORT"):
            r2 = recs[:2]
            in2 = ";".join("|".join(r) for r in r2)
            out2 = ";".join("|".join(r) for r in apply(st, r2))
        else:
            r2 = recs[:1]
            in2 = ";".join("|".join(r) for r in r2)
            out2 = ";".join("|".join(r) for r in apply(st, r2))
        lines = [f"STAGE {sid}", f"DESC {st['desc']}"]
        if st["cat"]=="JOIN":
            lines.append(f"WINL {st['winl']}"); lines.append(f"WINR {st['winr']}")
        elif st["win"]:
            lines.append(f"WIN {st['win']}")
        else:
            lines.append(f"WIN {win_of(stmap[st['deps'][0]], stmap)}")
        if st["deps"]:
            lines.append(f"DEPS {','.join(st['deps'])}")
        lines.append(f"TEST in={in1}")
        lines.append(f"TEST out={out1}")
        lines.append(f"TEST in={in2}")
        lines.append(f"TEST out={out2}")
        with open(os.path.join(CDIR, f"{sid}.txt"), "w") as f:
            f.write("\n".join(lines) + "\n")
    print(f"wrote {len(order)} contracts")

if __name__ == "__main__":
    main()
