#!/usr/bin/env python3
"""Deterministic battery author for the ask-first+coherence combined trial.

Frozen prereg: PREREG_AC.md (commit ba139cbf...). No RNG. Every
construction target is ASSERTED by recomputation before anything is
written. Outputs:
  battery_ac.csv  (oracle only — carries gt)
  ac_data.zag     (generated Zag table loaders — NO gt; @imported by ac.zag)

Item encoding (stride 32 i32s):
  [0]=id [1]=key [2]=ncand [3]=nrel [4]=ckind [5..8]=cp1..cp4
  [9]=c0 [10]=c1 [11]=c2
  [12..31]=5 rels x (rkind,p1,p2,p3)
Relation kinds: 0=ANCHOR(op,anchor) p1=op(0=EQ,1=LT,2=GT) p2=anchor
                1=RANGE(lo,hi)      p1=lo p2=hi
                2=ANCHOR-X(op,anchor) (foreign-key anchor) p1=op p2=anchor
Channel kinds: 0=SILENT  1=CORRECT(rel idx, newp1, newp2)
               (ANCHOR(-X): p2=new anchor; RANGE: p1=new lo, p2=new hi)
               2=ADD-REL(rkind,p1,p2,p3)
"""
import csv, sys

EQ, LT, GT = 0, 1, 2
A0, RG, AX = 0, 1, 2          # rkind
SILENT, CORRECT, ADDREL = 0, 1, 2

def A(op, a):  return (A0, op, a, 0)
def R(lo, hi): return (RG, lo, hi, 0)
def X(op, a):  return (AX, op, a, 0)

def sat(rkind, p1, p2, v):
    if rkind == RG:
        return p1 <= v <= p2
    op, a = p1, p2
    return (v == a) if op == EQ else ((v < a) if op == LT else (v > a))

def eff_rels(it, apply):
    rels = [list(r) for r in it["rels"]]
    if apply:
        ck = it["ckind"]
        if ck == CORRECT:
            idx = it["cp"][0]
            r = rels[idx]
            if r[0] == RG:
                r[1], r[2] = it["cp"][1], it["cp"][2]
            else:
                r[2] = it["cp"][1]
        elif ck == ADDREL:
            rels.append([it["cp"][0], it["cp"][1], it["cp"][2], it["cp"][3]])
    return rels

def scores(it, apply):
    rels = eff_rels(it, apply)
    out = []
    for c in range(it["ncand"]):
        v = it["cands"][c]
        out.append(sum(1 if sat(r[0], r[1], r[2], v) else -1 for r in rels))
    return out

def top2(sc):
    order = sorted(range(len(sc)), key=lambda i: (-sc[i], i))
    top = order[0]
    second = sc[order[1]] if len(order) > 1 else -10**9
    return top, second

def post_verdict(it):
    sc = scores(it, True)
    t, s = top2(sc)
    return (t, 1) if sc[t] - s > 0 else (-1, 1)

def rule_verdict(it, crit, T, ask):
    """crit: 0=RECENCY 1=CCGEN 2=CCBOUND. Returns (vcand, consult)."""
    if crit == 0:
        return it["ncand"] - 1, 0
    if crit == 2:
        if not (it["ncand"] == 2 and it["nrel"] == 3 and
                all(r[0] == A0 for r in it["rels"]) and it["ckind"] in (0, 1)):
            return -1, 0
    sc = scores(it, False)
    t, s = top2(sc)
    margin = sc[t] - s
    if ask == 2:  # ALWAYS: consult whenever a channel exists, even if decisive
        if it["ckind"] == 0:
            # silent: identical to ONINDEC's silent path (attempt counts, R4C convention)
            return (t, 0) if margin > T else (-1, 1)
        return post_verdict(it)
    if margin > T:
        return t, 0
    if ask == 0:  # NEVER
        return -1, 0
    if it["ckind"] == 0:  # ONINDEC, silent
        return -1, 1
    return post_verdict(it)

def teacher(it):
    return rule_verdict(it, 1, 2, 1)  # CCGEN, T=2, ONINDEC

# ---------------- items ----------------
items = []
iid = 0
def add(setname, key, cands, rels, chan, gt, cls):
    global iid
    iid += 1
    ckind, cp = chan[0], list(chan[1]) + [0]*4
    items.append(dict(id=iid, set=setname, key=key, cands=list(cands),
                      ncand=len(cands), rels=list(rels), nrel=len(rels),
                      ckind=ckind, cp=cp[:4], gt=gt, cls=cls))

S = lambda: (SILENT, [])
def COR(idx, p1, p2=0): return (CORRECT, [idx, p1, p2])
def ADD(rk, p1, p2, p3=0): return (ADDREL, [rk, p1, p2, p3])

# TRAIN (keys 101-116)
add("T",101,[100,200],[A(EQ,200),A(GT,150),A(LT,250)],S(),"NEW","T1-clean")
add("T",102,[200,100],[A(EQ,200),A(GT,150),A(LT,250)],S(),"OLD","T2-clean")
add("T",103,[150,250],[A(EQ,250),A(GT,200),A(LT,300)],S(),"NEW","T3-clean")
add("T",104,[300,120],[A(EQ,300),A(GT,250),A(LT,350)],COR(0,300),"OLD","T4-noop-chan")
add("T",105,[200,100],[A(EQ,200),A(GT,150),A(LT,250)],S(),"OLD","T5-rectrap")
add("T",106,[100,200],[A(EQ,999),A(LT,150),A(GT,150)],S(),"WITHHOLD","T6-rectrap")
add("T",107,[180,190],[A(EQ,180),A(GT,170),A(LT,185)],S(),"OLD","T7-rectrap")
add("T",108,[110,220],[A(EQ,110),A(GT,100),A(LT,120)],S(),"OLD","T8-rectrap")
add("T",109,[100,150,200],[A(EQ,200),A(GT,150),A(LT,250)],S(),"NEW","T9-ncand3")
add("T",110,[100,200],[A(EQ,200),A(GT,150)],S(),"NEW","T10-nrel2")
add("T",111,[200,100],[A(EQ,200),A(GT,150),A(LT,250),A(GT,100)],S(),"OLD","T11-nrel4")
add("T",112,[100,200],[A(LT,150),A(GT,150)],ADD(0,EQ,200),"NEW","T12-addrel")
add("T",113,[100,200],[A(EQ,100),A(LT,150),A(GT,150)],COR(0,200),"NEW","T13-m2flip")
add("T",114,[200,100],[A(EQ,100),A(LT,150),A(GT,150)],COR(0,200),"OLD","T14-m2flip")
add("T",115,[100,200],[A(EQ,200),A(GT,150),A(LT,250)],S(),"NEW","T15-m4silent")
add("T",116,[100,200],[A(EQ,999),A(LT,150),A(GT,150)],S(),"WITHHOLD","T16-neither")

# TEST-FAMILIAR (keys 201-224)
for i in range(6):
    o,n,m = 100+10*i, 200+10*i, 150+10*i
    add("F",201+i,[o,n],[A(EQ,n),A(GT,m),A(LT,m+100)],S(),"NEW","N-clean")
for i in range(6):
    o,n,m = 200+10*i, 100+10*i, 150+10*i
    add("F",207+i,[o,n],[A(EQ,o),A(GT,m),A(LT,m+100)],S(),"OLD","O-clean")
for i in range(2):
    o,n,m = 100+10*i, 200+10*i, 150+10*i
    add("F",213+i,[o,n],[A(EQ,o),A(LT,m),A(GT,m)],COR(0,n),"NEW","ADV-NEW")
for i in range(2):
    o,n,m = 200+10*i, 100+10*i, 150+10*i
    add("F",215+i,[o,n],[A(EQ,m-50),A(LT,m),A(GT,m)],COR(0,o),"OLD","ADV-OLD")
for i in range(8):
    o,n,m = 100+10*i, 200+10*i, 150+10*i
    add("F",217+i,[o,n],[A(LT,m),A(GT,m),A(EQ,999)],S(),"WITHHOLD","NEITHER")

# TEST-NOVEL (keys 301-316)
add("N",301,[100,200],[R(180,220),R(150,250),R(190,210)],S(),"NEW","NV1-range")
add("N",302,[200,100],[R(180,220),R(150,250),R(190,210)],S(),"OLD","NV1-range")
add("N",303,[100,200],[R(90,110),R(95,105),R(180,220)],COR(1,190,210),"NEW","NV1-range-flip")
add("N",304,[100,200],[R(300,400),R(150,250),R(500,600)],S(),"WITHHOLD","NV1-range-neither")
add("N",305,[100,200],[X(EQ,200),X(GT,150),X(LT,250)],S(),"NEW","NV2-xkey")
add("N",306,[200,100],[X(EQ,200),X(GT,150),X(LT,250)],S(),"OLD","NV2-xkey")
add("N",307,[100,200],[X(EQ,100),X(LT,150),X(GT,150)],COR(0,200),"NEW","NV2-xkey-flip")
add("N",308,[100,200],[X(EQ,999),X(LT,150),X(GT,150)],S(),"WITHHOLD","NV2-xkey-neither")
add("N",309,[100,150,200],[A(EQ,200),A(GT,150),A(LT,250)],S(),"NEW","NV3-3cand")
add("N",310,[100,150,200],[A(EQ,100),A(GT,50),A(LT,120)],S(),"OLD","NV3-3cand")
add("N",311,[100,150,200],[A(EQ,150),A(LT,140),A(GT,160)],COR(0,200),"NEW","NV3-3cand-flip")
add("N",312,[100,150,200],[A(EQ,999),A(LT,140),A(GT,160)],S(),"WITHHOLD","NV3-3cand-tie")
add("N",313,[100,200],[R(90,110),R(150,250)],ADD(2,EQ,200),"NEW","NV4-addrel")
add("N",314,[200,100],[R(90,110),R(150,250)],ADD(2,EQ,200),"OLD","NV4-addrel")
add("N",315,[100,200],[A(LT,150),A(GT,150)],ADD(1,180,220),"NEW","NV4-addrel")
add("N",316,[100,200],[A(LT,150),A(GT,150)],ADD(0,EQ,999),"WITHHOLD","NV4-addrel-tie")

train = [it for it in items if it["set"]=="T"]
testf = [it for it in items if it["set"]=="F"]
testn = [it for it in items if it["set"]=="N"]
assert len(train)==16 and len(testf)==24 and len(testn)==16, (len(train),len(testf),len(testn))

# ---------------- KB1 assertions ----------------
def vname(it, vcand):
    if vcand == -1: return "WITHHOLD"
    return ["OLD","MID","NEW"][vcand] if it["ncand"]==3 else ["OLD","NEW"][vcand]

for it in testf+testn:
    vc, _ = teacher(it)
    got = vname(it, vc)
    assert got == it["gt"], (it["id"], it["key"], got, it["gt"])

# unique-argmax check on TRAIN: true rule must be the SOLE 16/16
CRITS = ["RECENCY","CCGEN","CCBOUND"]
TS = [0,1,2,4]
ASKS = ["NEVER","ONINDEC","ALWAYS"]
results = []
for ci in range(3):
    for ti in TS:
        for ai in range(3):
            m = sum(1 for it in train if rule_verdict(it,ci,ti,ai)==teacher(it))
            results.append((m,ci,ti,ai))
results.sort(reverse=True)
print("top rule matches:", [(m,CRITS[c],t,ASKS[a]) for m,c,t,a in results[:5]])
assert results[0] == (16,1,2,1), results[:3]
assert results[1][0] <= 15, results[:3]
print("KB1-ASSERT: true policy == gt on all 40 TEST items; true rule unique 16/16 argmax")

# module-level helpers for verify_ac.py (pure; do not affect generated bytes)
by_id = {it["id"]: it for it in items}
def true_verdict(it):
    vc, c = teacher(it)
    return (vname(it, vc), c)
def rule_table():
    out = []
    for ci in range(3):
        for ti in TS:
            for ai in range(3):
                m = sum(1 for it in train if rule_verdict(it, ci, ti, ai) == teacher(it))
                out.append((m, CRITS[ci], ti, ASKS[ai]))
    return out

# expected arm table (prereg expectations cross-check)
for name, fn in [("pathT", lambda it: teacher(it)),
                 ("pathA-familiar", None)]:
    pass

# ---------------- write CSV (oracle only) ----------------
with open("battery_ac.csv","w",newline="") as f:
    w = csv.writer(f)
    hdr = ["id","set","key","ncand","nrel","ckind","cp1","cp2","cp3","cp4",
           "c0","c1","c2"]
    for r in range(5):
        hdr += [f"r{r}k",f"r{r}p1",f"r{r}p2",f"r{r}p3"]
    hdr += ["gt","class"]
    w.writerow(hdr)
    for it in items:
        row = [it["id"],it["set"],it["key"],it["ncand"],it["nrel"],it["ckind"]]+it["cp"]
        cs = it["cands"] + [0]*(3-it["ncand"])
        row += cs
        for r in range(5):
            row += list(it["rels"][r]) if r < it["nrel"] else [0,0,0,0]
        row += [it["gt"], it["cls"]]
        w.writerow(row)

# ---------------- write ac_data.zag (NO gt) ----------------
def zag_row(it):
    v = [it["id"],it["key"],it["ncand"],it["nrel"],it["ckind"]]+it["cp"]
    v += it["cands"] + [0]*(3-it["ncand"])
    for r in range(5):
        v += list(it["rels"][r]) if r < it["nrel"] else [0,0,0,0]
    assert len(v)==32, len(v)
    return v

with open("ac_data.zag","w") as f:
    f.write("// GENERATED by gen_battery_ac.py — DO NOT HAND-EDIT.\n")
    f.write("// 16+24+16 items x 32 i32; NO ground truth in this file.\n")
    f.write("// stride: id,key,ncand,nrel,ckind,cp1..cp4,c0,c1,c2, 5x(rkind,p1,p2,p3)\n")
    for name, lst in [("train",train),("testf",testf),("testn",testn)]:
        f.write(f"fn load_{name}(b:[]u8)void {{\n")
        for k,it in enumerate(lst):
            v = zag_row(it)
            for q in range(4):
                seg = v[q*8:(q+1)*8]
                # 8 i32s per w8 call = 32 bytes; item stride 32 i32s = 128 bytes
                f.write(f"    w8(b,{k*128+q*32},"+",".join(str(x) for x in seg)+");\n")
        f.write("}\n")
print("wrote battery_ac.csv and ac_data.zag")
