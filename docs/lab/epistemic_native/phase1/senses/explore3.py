import re, sys
from collections import defaultdict

STOP = set("""a an the and or but of to in on for with is are was were be been being it its this that these those as at by from has have had he she they we you i my our their his her him them us our yours mine theirs ours
not no never n't s t d ll m re ve do does did will would can could shall should may might must ought than then so such very just only also too more most less least own same other another each every all any both few many much such no nor if when where which who whom whose what how why because until while""".split())
NEG = {"not","no","never","n't","cannot","wont","dont","doesnt","isnt","arent","wasnt","werent","havent","hadnt","wouldnt","shouldnt","couldnt","aint","without"}
NUMW = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,
"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20,
"thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90,"hundred":100,"thousand":1000}
def stem(w):
    if len(w)>4:
        if w.endswith("ies"): return w[:-3]+"y"
        if w.endswith("es") and not w.endswith("sses"): return w[:-2]
        if w.endswith("s") and not w.endswith("ss"): return w[:-1]
    if len(w)>5 and w.endswith("ed"): return w[:-2]
    if len(w)>6 and w.endswith("ing"): return w[:-3]
    return w
def toks(s):
    s=s.lower(); s=re.sub(r"n't\b"," n't",s)
    return re.findall(r"[a-z0-9']+",s)
items=[]
with open('/home/hatch/workspace/epi_a3/blind/train_blind.tsv') as f:
    f.readline()
    for line in f:
        line=line.rstrip('\n')
        if not line: continue
        iid,text=line.split('\t',1); items.append((iid,text))
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
N=len(items)

# full neighborhood: for each item, list neighbors with jac>=0.30, inter>=3, categorized
def nbrs(i, thresh=0.30):
    out=[]
    for j in range(N):
        if j==i: continue
        a,b=CS[i],CS[j]
        inter=len(a&b); union=len(a|b)
        if union==0: continue
        jac=inter/union
        if jac>=thresh and inter>=3:
            negxor=bool(NG[i]^NG[j])
            numm=bool(NM[i] and NM[j] and NM[i]!=NM[j])
            if negxor or numm: cat="CONTRA"
            elif jac>=0.5 and not negxor and not numm: cat="SUPP"
            else: cat="TOPIC"
            out.append((items[j][0],round(jac,2),cat))
    return sorted(out,key=lambda x:-x[1])

# distribution of neighborhood sizes
from collections import Counter
cnt=Counter()
maxn=0
for i in range(N):
    n=len(nbrs(i))
    cnt[n]+=1
    maxn=max(maxn,n)
print("neighborhood size distribution (jac>=0.30):")
for k in sorted(cnt): print("  %d neighbors: %d items"%(k,cnt[k]))
print("max neighbors:",maxn)

# items with the most neighbors
print("\n--- hub items (most neighbors) ---")
hubs=sorted(range(N),key=lambda i:-len(nbrs(i)))[:15]
for i in hubs:
    print(items[i][0], len(nbrs(i)), items[i][1][:65])

# for the 11 pair members, show FULL neighborhoods
print("\n--- full neighborhoods of pair members ---")
pairs=[("T0009","T0024"),("T0011","T0319"),("T0015","T0235"),("T0017","T0114"),("T0039","T0187"),("T0071","T0185"),("T0090","T0348"),("T0215","T0280"),("T0248","T0255"),("T0311","T0351"),("T0022","T0338")]
idx={iid:i for i,(iid,_) in enumerate(items)}
for a,b in pairs:
    for pid in (a,b):
        i=idx[pid]
        print(pid, items[i][1][:60])
        for nb in nbrs(i)[:8]:
            j=idx[nb[0]]
            print("    ->",nb[0],nb[1],nb[2],items[j][1][:55])
