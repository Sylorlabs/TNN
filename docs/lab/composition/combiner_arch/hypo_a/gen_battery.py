#!/usr/bin/env python3
# gen_battery.py — deterministic capability battery for H-A (BUILDER-A).
# teach.tsv: r1..r8 taught (r1..r6 = D1 six from frozen items.tsv; r7 swap-first-last,
#   r8 sort-descending hand-written); r9 (caesar) NOT taught -> P3 echo probes.
# probe.tsv: 8 held-out probes per rule, lengths 2,2,3,3,4,4,5,5.
# Also writes battery_abl/{teach,probe}.tsv with caesar (k=3) TAUGHT for K-HA-3.
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = "/home/hatch/workspace/tnn-native-lab-work/docs/lab/composition/battery_amended/items.tsv"

def rule_fn(name):
    if name == "reverse":      return lambda s: s[::-1]
    if name == "dupfirst":     return lambda s: s[0] + s
    if name == "rotleft":      return lambda s: s[1:] + s[:1] if s else s
    if name == "droplast":     return lambda s: s[:-1]
    if name == "upperfirst":   return lambda s: s[0].upper() + s[1:] if s else s
    if name == "sortchars":    return lambda s: "".join(sorted(s))
    if name == "swap":         return lambda s: s[-1] + s[1:-1] + s[0] if len(s) >= 2 else s
    if name == "sortdesc":     return lambda s: "".join(sorted(s, reverse=True))
    if name == "caesar3":      return lambda s: "".join(chr((ord(c)-97+3)%26+97) if 'a'<=c<='z' else c for c in s)
    raise ValueError(name)

# frozen D1 teaches from the amended battery
teaches = {}
for line in open(ITEMS):
    f = line.rstrip("\n").split("\t")
    if f[0] != "TEACH": continue
    name = f[2].split("=")[1]
    inp = f[4].split("=",1)[1]; exp = f[5].split("=",1)[1]
    teaches.setdefault(name, []).append((inp, exp))
assert all(len(v)==12 for v in teaches.values()), {k:len(v) for k,v in teaches.items()}

D1 = ["reverse","dupfirst","rotleft","droplast","upperfirst","sortchars"]
RIDS = {"reverse":"r1","dupfirst":"r2","rotleft":"r3","droplast":"r4","upperfirst":"r5","sortchars":"r6"}

# deterministic probe token generator: disjoint-ish from teaches by construction
ALPHA = "abcdefghijklmnopqrstuvwxyz"
def ptok(seed, ln):
    # counter-based, fixed
    out = []
    x = seed
    for _ in range(ln):
        x = (x*1103515245 + 12345) & 0x7fffffff
        out.append(ALPHA[x % 26])
    return "".join(out)

def probes_for(fn, n, seed0):
    lens = [2,2,3,3,4,4,5,5][:n]
    res = []
    s = seed0
    used = set()
    for ln in lens:
        while True:
            t = ptok(s, ln); s += 1
            if t not in used: break
        used.add(t)
        res.append((t, fn(t)))
    return res, s

# hand-written teaches for swap / sortdesc / caesar(k=3)
SWAP_T = ["abcd","hello","xy","truck","zebra","mnopqr","st","wxyzv"]
SDESC_T = ["abc","hello","zyx","cba","mnp","qrst","wxy","defg"]
CAES_T = ["abc","xyz","hello","mnopq","st","wxy","defgh","jklm"]

def build(with_caesar_taught):
    teach, probe = [], []
    seed = 1000
    for d in D1:
        fn = rule_fn(d); rid = RIDS[d]
        for (i,e) in teaches[d]: teach.append((rid,i,e))
        pr,_ = probes_for(fn, 8, seed); seed += 100
        for (i,e) in pr: probe.append((rid,i,e))
    # r7 swap-first-last
    fn = rule_fn("swap")
    for t in SWAP_T: teach.append(("r7",t,fn(t)))
    pr,_ = probes_for(fn,8,seed); seed += 100
    for (i,e) in pr: probe.append(("r7",i,e))
    # r8 sort-descending
    fn = rule_fn("sortdesc")
    for t in SDESC_T: teach.append(("r8",t,fn(t)))
    pr,_ = probes_for(fn,8,seed); seed += 100
    for (i,e) in pr: probe.append(("r8",i,e))
    # r9 caesar
    fn = rule_fn("caesar3")
    if with_caesar_taught:
        for t in CAES_T: teach.append(("r9",t,fn(t)))
        pr,_ = probes_for(fn,8,seed)
        for (i,e) in pr: probe.append(("r9",i,e))
    else:
        # untaught: honest withhold is the correct behavior -> expected = "?"
        pr,_ = probes_for(lambda s: s,8,seed)
        for (i,e) in pr: probe.append(("r9",i,"?"))
    # sanity: no probe input collides with a teach input of the same rule
    tset = {}
    for (r,i,e) in teach: tset.setdefault(r,set()).add(i)
    for (r,i,e) in probe:
        assert i not in tset.get(r,set()), ("collision",r,i)
    return teach, probe

def write(d, teach, probe):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d,"teach.tsv"),"w") as f:
        for (r,i,e) in teach: f.write(f"{r}\t{i}\t{e}\n")
    with open(os.path.join(d,"probe.tsv"),"w") as f:
        for (r,i,e) in probe: f.write(f"{r}\t{i}\t{e}\n")
    print(d, "teach:",len(teach),"probe:",len(probe))

t,p = build(False); write(os.path.join(HERE,"battery_cap"),t,p)
t,p = build(True);  write(os.path.join(HERE,"battery_abl"),t,p)
