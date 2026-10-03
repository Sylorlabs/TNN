TAG={"AFFIRM":1,"DENY":2,"NEUTRAL":0}
RTAG={1:"AFFIRM",2:"DENY",0:"NEUTRAL"}
def load_corpus(p):
    rows=[]
    for line in open(p):
        f=line.rstrip("\n").split("\t")
        rows.append((f[0],f[1],f[2],f[3],f[4]))
    return rows
def load_out(p):
    d={}
    for line in open(p):
        parts=line.rstrip("\n").split(" ",2)
        d[parts[0]]=(int(parts[1]),parts[2] if len(parts)>2 else "")
    return d
for fam,cf,of in (("rtA","corpus_rtA.tsv","out_rtA_r1.txt"),("rtB","corpus_rtB.tsv","out_rtB_r1.txt"),("ceiling","corpus_ceiling.tsv","out_ceiling_r1.txt")):
    cor=load_corpus(cf); out=load_out(of)
    print(f"--- {fam}: {len(cor)} items, {len(out)} outputs ---")
    n_hit=0
    for idx,claim,title,snip,oracle in cor:
        tag,reason=out[idx]; got=RTAG[tag]
        if fam=="rtA": hit=(tag==1)
        else: hit=(got!=oracle)
        n_hit+=hit
        flag="HIT" if hit else ("ok " if got==oracle else "swp")
        print(f"{flag} {idx} oracle={oracle:8s} got={got:8s} reason={reason:16s} claim={claim!r} ev={snip!r}")
    print(f"{fam}: hits={n_hit}")
