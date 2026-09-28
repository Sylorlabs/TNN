import re, sys

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

DEONTIC={"should","must","ought"}
EXP_VERBS={"feel","feels","felt","think","thinks","thought","love","loves","loved","like","likes","liked","prefer","prefers","preferred","believe","believes","believed","enjoy","enjoys","enjoyed","hate","hates","hated","want","wants","wanted","hope","hopes","hoped","wish","wishes"}

def has_deontic(t):
    return any(w in DEONTIC for w in toks(t))
def has_1p_exp(t):
    ws=toks(t)
    for i,w in enumerate(ws):
        if w in ("i","my") and i+1<len(ws) and ws[i+1] in EXP_VERBS: return True
    return False
def has_comparative(t):
    tl=" "+t.lower()+" "
    if re.search(r"\bmore\b.{0,40}\bthan\b", tl): return True
    if re.search(r"\bless\b.{0,40}\bthan\b", tl): return True
    if re.search(r"\b(better|worse)\b.{0,40}\bthan\b", tl): return True
    if re.search(r"[a-z]+er\b.{0,40}\bthan\b", tl): return True
    return False
def has_superlative(t):
    tl=" "+t.lower()+" "
    if re.search(r"\bthe\b.{0,25}\bmost\b", tl): return True
    if re.search(r"\bthe\b.{0,25}\bleast\b", tl): return True
    if re.search(r"\bthe\b.{0,25}[a-z]+est\b", tl): return True
    if re.search(r"\b(best|worst)\b", tl): return True
    return False

cats={}
for iid,t in items:
    c=[]
    if has_deontic(t): c.append("DEON")
    if has_1p_exp(t): c.append("1PEXP")
    if has_comparative(t): c.append("COMP")
    if has_superlative(t): c.append("SUP")
    cats[iid]=c

from collections import Counter
cnt=Counter()
for iid,c in cats.items():
    cnt[tuple(sorted(c)) if c else ("NONE",)]+=1
print("pattern distribution:")
for k in sorted(cnt,key=lambda x:-cnt[x]): print("  ",k,cnt[k])
n_any=sum(1 for c in cats.values() if c)
print("items with >=1 pattern:",n_any,"/",len(items))
