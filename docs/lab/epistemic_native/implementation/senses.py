#!/usr/bin/env python3
"""Mechanical senses for native-deliberation epistemics (Phase 1).

Reads:  ~/workspace/epi_a3/blind/train_blind.tsv (opaque IDs, no labels)
Writes: mass.tsv, pairs.tsv  (under outdir)

These are SENSES: deterministic, mechanical, judgment-free.
- Tokenization / stemming / stopword filtering (syntax-level).
- IDF-weighted lexical retrieval index (top-8 per item).
- Constructional feature codes: fpexp (first-person experiencer),
  deon (deontic modal), cmp (comparative/superlative syntax).
- Pairwise mechanical features: OV (idf-weighted overlap 0..100),
  nshared, neg (sentential negation asymmetry), num (numeric divergence),
  ent (entity divergence).

No epistemic judgment here. No labels touched. No verdict logic.
"""
import sys, os, math, re
from collections import defaultdict

TRAIN = "/home/hatch/workspace/epi_a3/blind/train_blind.tsv"

STOP = set("""a an the and or but if then else when while of at by for with
about into through during before after above below to from up down in out on
off over under again further once here there all any both each few more most
other some such no nor not only own same so than too very can will just don
should now is are was were be been being have has had having do does did
doing would could ought i you he she it we they them his her its our their
this that these those am as at because been before between during either
neither nor whether while within without would s t d ll m re ve ll""".split())

IRREG = {
    "children":"child","men":"man","women":"woman","teeth":"tooth",
    "feet":"foot","mice":"mouse","geese":"goose","oxen":"ox",
    "wore":"wear","worn":"wear","went":"go","gone":"go","came":"come",
    "come":"come","ate":"eat","eaten":"eat","drank":"drink","drunk":"drink",
    "sang":"sing","sung":"sing","rang":"ring","rung":"ring","began":"begin",
    "begun":"begin","broke":"break","broken":"break","chose":"choose",
    "chosen":"choose","froze":"freeze","frozen":"freeze","spoke":"speak",
    "spoken":"speak","stole":"steal","stolen":"steal","swore":"swear",
    "sworn":"swear","tore":"tear","torn":"tear","wove":"weave",
    "woven":"weave","dove":"dive","dived":"dive","dug":"dig","hung":"hang",
    "stung":"sting","struck":"strike","stuck":"stick","swam":"swim",
    "swum":"swim","threw":"throw","thrown":"throw","woke":"wake",
    "woken":"wake","wrote":"write","written":"write","rode":"ride",
    "ridden":"ride","rose":"rise","risen":"rise","drove":"drive",
    "driven":"drive","forgot":"forget","forgotten":"forget","forbade":"forbid",
    "forbidden":"forbid","got":"get","gotten":"get","hid":"hide",
    "hidden":"hide","held":"hold","kept":"keep","knelt":"kneel",
    "leapt":"leap","learnt":"learn","left":"leave","lent":"lend",
    "meant":"mean","paid":"pay","pled":"plead","sent":"send","shone":"shine",
    "shot":"shoot","showed":"show","shown":"show","slept":"sleep",
    "slid":"slide","smelt":"smell","spelt":"spell","spent":"spend",
    "spilt":"spill","spoilt":"spoil","stood":"stand","swept":"sweep",
    "taught":"teach","thought":"think","told":"tell","understood":"understand",
    "wept":"weep","wound":"wind","bound":"bind","found":"find",
    "ground":"grind","is":"be","are":"be","was":"be","were":"be",
    "been":"be","being":"be","has":"have","had":"have","having":"have",
    "does":"do","did":"do","doing":"do","says":"say","said":"say",
    "makes":"make","made":"make","takes":"take","took":"take","taken":"take",
    "comes":"come","goes":"go","knows":"know","knew":"know","known":"know",
    "thinks":"think","feels":"feel","felt":"feel","seems":"seem",
    "becomes":"become","became":"become","become":"become",
}

def stem(w):
    if w in IRREG: return IRREG[w]
    if len(w) <= 3: return w
    if w.endswith("ies") and len(w) > 4: return w[:-3] + "y"
    if w.endswith("es") and len(w) > 4:
        b = w[:-2]
        if b.endswith(("s","x","z","ch","sh","o")): return b
        return w[:-1]
    if w.endswith("s") and not w.endswith("ss"): return w[:-1]
    if w.endswith("ing") and len(w) > 5:
        b = w[:-3]
        if len(b) >= 3 and b[-1] == b[-2]: return b[:-1]
        return b
    if w.endswith("ed") and len(w) > 4:
        b = w[:-2]
        if len(b) >= 3 and b[-1] == b[-2]: return b[:-1]
        if b.endswith("i"): return b[:-1] + "y"
        return b
    if w.endswith("er") and len(w) > 4: return w[:-2]
    if w.endswith("est") and len(w) > 5: return w[:-3]
    if w.endswith("ly") and len(w) > 4: return w[:-2]
    return w

TOK_RE = re.compile(r"[a-z]+(?:'[a-z]+)?|[0-9]+(?:\.[0-9]+)?")
NEG_SENT = {"not","never","n't"}

def raw_toks(text):
    return TOK_RE.findall(text.lower())

def content_toks(text):
    out=[]
    for w in raw_toks(text):
        if w in STOP: continue
        if w[0].isdigit(): continue
        out.append(stem(w))
    return out

def entities(text):
    toks = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)
    ents=set()
    for i,w in enumerate(toks):
        if i==0: continue
        if w[0].isupper() and w.lower() not in STOP:
            ents.add(w.lower())
    return ents

def numerics(text):
    return set(re.findall(r"[0-9]+(?:\.[0-9]+)?", text.lower()))

def has_sent_neg(text):
    toks = raw_toks(text)
    for i,w in enumerate(toks):
        if w in NEG_SENT: return True
        if w.endswith("n't"): return True
    return False

FP1 = {"i","we"}
def constructions(text):
    toks = raw_toks(text)
    low = [t.lower() for t in toks]
    # first-person experiencer: I/we + experiencer verb/adjective nearby
    fpexp = 0
    for i,w in enumerate(low):
        if w in FP1:
            window = low[i+1:i+4]
            if any(v in window for v in ("feel","think","believe","love","hate","like","prefer","find","seem","consider")):
                fpexp = 1; break
    # deontic: should/must/ought/have to/need to (obligation sense markers)
    deon = 0
    for i,w in enumerate(low):
        if w in ("should","must","ought"):
            deon=1; break
        if w=="have" and i+1<len(low) and low[i+1]=="to":
            deon=1; break
        if w=="need" and i+1<len(low) and low[i+1]=="to":
            deon=1; break
    # comparative/superlative syntax
    cmp = 0
    for w in low:
        if w in ("more","most","less","least","better","best","worse","worst",
                 "greater","greatest","smaller","smallest","higher","highest",
                 "lower","lowest","longer","longest","faster","fastest",
                 "slower","slowest","easier","easiest","harder","hardest"):
            cmp=1; break
    if not cmp:
        for w in raw_toks(text):
            lw=w.lower()
            if len(lw)>5 and (lw.endswith("ier") or lw.endswith("iest")):
                cmp=1; break
    return fpexp, deon, cmp

def load_train(path):
    items=[]
    with open(path, encoding="utf-8") as f:
        lines=f.read().splitlines()
    assert lines[0].lower().startswith("id"), "unexpected header: "+lines[0][:40]
    for ln in lines[1:]:
        if not ln.strip(): continue
        parts=ln.split("\t")
        assert len(parts)>=2, "bad line: "+ln[:60]
        items.append((parts[0], parts[1]))
    return items

def main():
    outdir = sys.argv[1] if len(sys.argv)>1 else "."
    os.makedirs(outdir, exist_ok=True)
    items = load_train(TRAIN)
    N=len(items)
    print(f"loaded {N} items", flush=True)

    ctoks=[content_toks(t) for _,t in items]
    tset=[set(c) for c in ctoks]
    ents=[entities(t) for _,t in items]
    nums=[numerics(t) for _,t in items]
    negs=[1 if has_sent_neg(t) else 0 for _,t in items]
    constr=[constructions(t) for _,t in items]

    # document frequency + idf weights (fixed-point: w = 1 + 128*(9-bitlen(df)))
    df=defaultdict(int)
    for s in tset:
        for w in s: df[w]+=1
    def bitlen(x): return x.bit_length()
    W={w: 1+128*(9-bitlen(c)) for w,c in df.items()}
    wsum=[sum(W[w] for w in s) for s in tset]

    # inverted index
    post=defaultdict(list)
    for i,s in enumerate(tset):
        for w in s: post[w].append(i)

    # mass.tsv
    with open(os.path.join(outdir,"mass.tsv"),"w",encoding="utf-8") as f:
        f.write("id\ttext\ttokens\tentities\tnumerics\thas_neg\tfpexp\tdeon\tcmp\n")
        for i,(bid,text) in enumerate(items):
            f.write("\t".join([
                bid, text.replace("\t"," ").replace("\n"," "),
                " ".join(sorted(tset[i])),
                " ".join(sorted(ents[i])),
                " ".join(sorted(nums[i], key=lambda x: float(x))),
                str(negs[i]),
                str(constr[i][0]), str(constr[i][1]), str(constr[i][2]),
            ])+"\n")

    # pairs.tsv : top-8 per q (excluding self), with mechanical features
    npairs=0
    with open(os.path.join(outdir,"pairs.tsv"),"w",encoding="utf-8") as f:
        f.write("qid\tcid\tov\tnshared\tneg\tnum\tent\n")
        for q in range(N):
            acc=defaultdict(int)
            for w in tset[q]:
                for j in post[w]:
                    if j==q: continue
                    acc[j]+=W[w]
            ranked=sorted(acc.items(), key=lambda kv:(-kv[1],kv[0]))[:8]
            qid=items[q][0]
            for c,_ in ranked:
                sa,sb=tset[q],tset[c]
                sh=sa&sb
                sw=sum(W[w] for w in sh)
                denom=wsum[q]+wsum[c]-sw
                ov=(100*sw//denom) if denom>0 else 0
                neg=1 if (negs[q]!=negs[c]) else 0
                num=1 if (nums[q] and nums[c] and nums[q]!=nums[c]) else 0
                ea,eb=ents[q],ents[c]
                ent=1 if (ea and eb and ea.isdisjoint(eb)) else 0
                f.write(f"{qid}\t{items[c][0]}\t{ov}\t{len(sh)}\t{neg}\t{num}\t{ent}\n")
                npairs+=1
            if (q+1)%100==0: print(f"  {q+1}/{N}", flush=True)
    print(f"wrote pairs: {npairs}", flush=True)

if __name__=="__main__":
    main()
