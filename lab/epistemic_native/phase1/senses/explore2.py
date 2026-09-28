import re, sys
from collections import defaultdict

STOP = set("""a an the and or but of to in on for with is are was were be been being it its this that these those as at by from has have had he she they we you i my our their his her him them us our yours mine theirs ours
not no never n't s t d ll m re ve do does did will would can could shall should may might must ought than then so such very just only also too more most less least own same other another each every all any both few many much such no nor if when where which who whom whose what how why because until while""".split())
NEG = {"not","no","never","n't","cannot","wont","dont","doesnt","isnt","arent","wasnt","werent","havent","hadnt","wouldnt","shouldnt","couldnt","aint","without"}
NUMW = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,
"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20,
"thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90,"hundred":100,"thousand":1000}

def stem(w):
    # tiny deterministic stemmer
    if len(w)>4:
        if w.endswith("ies"): return w[:-3]+"y"
        if w.endswith("es") and not w.endswith("sses"): return w[:-2]
        if w.endswith("s") and not w.endswith("ss"): return w[:-1]
    if len(w)>5 and w.endswith("ed"): return w[:-2]
    if len(w)>6 and w.endswith("ing"): return w[:-3]
    return w

def toks(s):
    s = s.lower()
    s = re.sub(r"n't\b", " n't", s)
    return re.findall(r"[a-z0-9']+", s)

items=[]
with open('/home/hatch/workspace/epi_a3/blind/train_blind.tsv') as f:
    f.readline()
    for line in f:
        line=line.rstrip('\n')
        if not line: continue
        iid,text=line.split('\t',1)
        items.append((iid,text))

def content(t): return [stem(w) for w in toks(t) if w not in STOP]
def neg(t): return set(w for w in toks(t) if w in NEG)
def nums(t):
    out=set()
    for w in toks(t):
        if re.fullmatch(r"\d+",w): out.add(int(w))
        elif w in NUMW: out.add(NUMW[w])
    return out

C=[content(t) for _,t in items]; CS=[set(c) for c in C]
NG=[neg(t) for _,t in items]; NM=[nums(t) for _,t in items]

pairs=[]
for i in range(len(items)):
    for j in range(i+1,len(items)):
        a,b=CS[i],CS[j]
        if not a or not b: continue
        inter=len(a&b); union=len(a|b); jac=inter/union
        if jac<0.30 or inter<3: continue
        negxor=bool(NG[i]^NG[j])
        numm=bool(NM[i] and NM[j] and NM[i]!=NM[j])
        if negxor or numm:
            pairs.append((items[i][0],items[j][0],round(jac,2),"negxor" if negxor else "numm",items[i][1][:75],items[j][1][:75]))
print("pairs:",len(pairs))
seen=set()
for p in pairs:
    print(p[0],p[1],p[2],p[3]); print("   A:",p[4]); print("   B:",p[5])

# For each item in a pair, count "supporters": other items with jac>=0.5 and NO negxor and NO numm
print("\n--- support structure for paired items ---")
paired=set()
for p in pairs: paired.add(p[0]); paired.add(p[1])
idx={iid:i for i,(iid,_) in enumerate(items)}
for pid in sorted(paired):
    i=idx[pid]
    sup=[]
    for j in range(len(items)):
        if j==i: continue
        a,b=CS[i],CS[j]
        inter=len(a&b); union=len(a|b); jac=inter/union if union else 0
        if jac>=0.5 and inter>=3 and not (NG[i]^NG[j]) and not (NM[i] and NM[j] and NM[i]!=NM[j]):
            sup.append(items[j][0])
    print(pid, "supporters:", sup, "| text:", items[i][1][:60])
