TAG={"AFFIRM":1,"DENY":2,"NEUTRAL":0}
RTAG={1:"AFFIRM",2:"DENY",0:"NEUTRAL"}
def load_corpus(p):
    d={}
    for line in open(p):
        f=line.rstrip("\n").split("\t")
        d[f[0]]=(f[1],f[2],f[3],f[4])
    return d
def load_out(p):
    d={}
    for line in open(p):
        parts=line.rstrip("\n").split(" ",2)
        d[parts[0]]=(int(parts[1]),parts[2] if len(parts)>2 else "")
    return d

print("=== RT-A (hit = AFFIRM verdict; bar >=3 FAIL) ===")
cor=load_corpus("corpus_rtA.tsv"); out=load_out("out_rtA_r1.txt")
hits=[]; matches=0
for idx,(claim,title,snip,oracle) in cor.items():
    tag,reason=out[idx]
    om = (RTAG[tag]==oracle)
    matches+=om
    if tag==1:
        hits.append((idx,claim,title,snip,oracle,RTAG[tag],reason))
for h in hits: print("HIT:",h)
print(f"RT-A false affirms: {len(hits)}/46 | oracle-match: {matches}/46")

print("\n=== RT-B (hit = verdict != oracle; bar >=1 FAIL) ===")
cor=load_corpus("corpus_rtB.tsv"); out=load_out("out_rtB_r1.txt")
hits=[]; 
for idx,(claim,title,snip,oracle) in cor.items():
    tag,reason=out[idx]
    if RTAG[tag]!=oracle:
        hits.append((idx,claim,snip,oracle,RTAG[tag],reason))
for h in hits: print("HIT:",h)
print(f"RT-B oracle-matches: {46-len(hits)}/46 | hits: {len(hits)}")

print("\n=== CEILING probes (documented, not counted) ===")
cor=load_corpus("corpus_ceiling.tsv"); out=load_out("out_ceiling_r1.txt")
for idx,(claim,title,snip,oracle) in cor.items():
    tag,reason=out[idx]
    print(idx, "oracle="+oracle, "got="+RTAG[tag], "reason="+reason, "MATCH" if RTAG[tag]==oracle else "miss-as-documented")
