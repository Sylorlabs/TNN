#!/usr/bin/env python3
"""REF9: lie = clash AND no support. Fixes fact->lie FPs."""
import sys, re
sys.path.insert(0, ".")
from inv_common import *
from collections import Counter

items = load_train()
idf = build_idf(items)
STANCE = set(open('stance_final.txt').read().split())
def stance_density(it):
    n=len(it["toks"])
    return sum(1 for w in it["toks"] if w in STANCE)/max(n,1)

def proper_nouns(text):
    ws = re.findall(r"[A-Za-z0-9]+", text)
    return set(w.lower() for w in ws if w and w[0].isupper() and len(w)>=3)
def numset(text):
    return set(n.replace(",","") for n in numbers(text))
ANT = {"largest":"smallest","smallest":"largest","tallest":"shortest","shortest":"tallest",
"fastest":"slowest","slowest":"fastest","hottest":"coldest","coldest":"hottest",
"longest":"shortest","shortest":"longest","highest":"lowest","lowest":"highest",
"most":"least","least":"most","better":"worse","worse":"better","always":"never","never":"always",
"true":"false","false":"true","real":"fake","fake":"real"}
def negated_values(text):
    tl=text.lower(); words=re.findall(r"[a-z0-9']+",tl); out=set()
    vals=numset(text)|proper_nouns(text)
    for i,w in enumerate(words):
        wn=w.rstrip("s")
        if wn in vals or w in vals:
            window=words[max(0,i-4):i]
            if any(x in ("not","never","no") or "n't" in x for x in window):
                out.add(wn)
    return out
def clash(h, t):
    nh, nt = numset(h["text"]), numset(t["text"])
    if nh and nt and not (nh & nt):
        chn = h["toks"] - {w for w in h["toks"] if any(c.isdigit() for c in w)}
        ctn = t["toks"] - {w for w in t["toks"] if any(c.isdigit() for c in w)}
        inter = chn & ctn; union = chn | ctn
        if union and len(inter)/len(union) >= 0.25:
            return True
    hv = numset(h["text"])|proper_nouns(h["text"])
    if hv & negated_values(t["text"]):
        return True
    if h["text"].lower()!=t["text"].lower():
        inter=h["toks"]&t["toks"]; union=h["toks"]|t["toks"]
        if union and len(inter)/len(union)>=0.8:
            return True
    for w in h["toks"]:
        if w in ANT and ANT[w] in t["toks"]:
            return True
    return False

DISPUTE = set("""causes cause damage damages unsafe staged hidden hides murdered murder
inside real undiscovered prove proves hoax warns warned escapes escaped lowers raises deter
deters reduce reduces improves improve produce produces makes prevent prevents flush heals
treats buy accurately predicts sense spike myth myths killed shooter monster visited job
damage unsafe escaped accurately predicts prove sense spike prevents shortens improves
better healthier warns violent pain left-brained multivitamins homework""".split())
def has_dispute(h):
    return any(w in h["text"].lower() for w in DISPUTE)

def has_support(h, mass):
    """Does any mass item agree with h's specific value?"""
    hv = numset(h["text"])|proper_nouns(h["text"])
    if not hv: return False
    for t in mass:
        if wsum(h["toks"],t["toks"],idf) < 2500: continue
        if clash(h,t): continue
        tv = numset(t["text"])|proper_nouns(t["text"])
        if hv & tv:
            return True
    return False

def max_wsum(h, mass):
    best=0
    for t in mass:
        w=wsum(h["toks"],t["toks"],idf)
        if w>best: best=w
    return best

def classify(h, mass, t_fact):
    if stance_density(h) >= 0.12:
        return "opinion"
    is_clash=False
    for t in mass:
        if wsum(h["toks"],t["toks"],idf) < 2500: continue
        if clash(h,t):
            is_clash=True; break
    supported = has_support(h, mass)
    if is_clash and not supported:
        return "undetermined" if has_dispute(h) else "lie"
    if is_clash and supported:
        # h clashes but has support: contested, not a lie
        pass  # fall through to fact/undetermined
    mw = max_wsum(h, mass)
    if has_dispute(h) and mw >= 2000:
        return "undetermined"
    if mw >= t_fact:
        return "fact"
    return "undetermined"

for t_fact in [3000]:
    conf=Counter(); per=Counter()
    for i,h in enumerate(items):
        mass=[t for j,t in enumerate(items) if j!=i]
        p=classify(h,mass,t_fact)
        conf[(h["class"],p)]+=1
        per[h["class"]]+=1
    def prf(cls):
        tp=conf[(cls,cls)]; fp=sum(conf[(o,cls)] for o in ["fact","opinion","lie","skepticism"] if o!=cls)
        fn=sum(conf[(cls,p)] for p in ["fact","opinion","lie","undetermined"] if p!=cls)
        return tp/max(tp+fp,1), tp/max(tp+fn,1)
    for cls in ["fact","opinion","lie"]:
        p,r=prf(cls); print(f"{cls}: P={p:.3f} R={r:.3f}")
    forced=sum(conf[("skepticism",p)] for p in ["fact","lie"])/per["skepticism"]
    print(f"skepticism forced: {forced:.3f}")
    print(f"\nFact->Lie: {conf[('fact','lie')]} (was 12)")
