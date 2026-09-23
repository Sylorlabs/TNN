import os
D="/home/hatch/workspace/scratch-hellhole/crews/a4"
T={0:"NEUTRAL",1:"AFFIRM",2:"DENY"}
for fam in ["cond","qnt","hedge","tmp","cmp"]:
    oracle={}
    for line in open(os.path.join(D,"corpus_%s.tsv"%fam)):
        p=line.rstrip("\n").split("\t")
        oracle[p[0]]=int(p[4])
    pred={}
    for line in open(os.path.join(D,"out_%s_run1.txt"%fam)):
        p=line.split()
        pred[p[0]]=(int(p[1]),p[2])
    n=len(oracle); ok=0; mis=[]
    for idx,o in oracle.items():
        pr,rs=pred[idx]
        if pr==o: ok+=1
        else: mis.append((idx,o,pr,rs))
    print("== %s: %d/%d correct (%.1f%%)"%(fam,ok,n,100.0*ok/n))
    for idx,o,pr,rs in mis:
        print("   MISTAG %s oracle=%s pred=%s(%s)"%(idx,T[o],T[pr],rs))
