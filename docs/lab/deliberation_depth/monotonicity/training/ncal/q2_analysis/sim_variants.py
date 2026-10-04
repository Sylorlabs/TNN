#!/usr/bin/env python3
"""Byte-exact sims of m11 and m_g recording per-cell CAP binding (not ceiling-inherited)."""
import sys

def run(in_tsv, mode):
    assert mode in ("m11","mg")
    led = {}; pers = {}; prev = {}
    out = []; capbind = {}  # (iid,depth) -> 1 iff the personal CAP strictly lowered conf at this cell
    for line in open(in_tsv):
        line=line.rstrip("\n")
        if not line: continue
        iid,fam,depth,f1,f5,rel,corr = line.split("\t")
        depth,f1,f5,rel,corr = int(depth),int(f1),int(f5),int(rel),int(corr)
        conf = 0
        if rel==1:
            cls=(min(f1//150,6),min(f5//250,4))
            c,t = led.get(cls,[0,0])
            class_rate=(c*1000000+1900000)//(t+2)
            cp,tp = pers.get(iid,[0,0])
            cm = class_rate; bound = 0
            if tp>=1:
                p_raw=(cp*1000000)//tp
                do_cap = (cm>p_raw) and (mode=="m11" or corr==0)
                if do_cap: cm=p_raw; bound=1
            pc = prev.get(iid)
            if pc is not None and cm>pc: cm=pc
            prev[iid]=cm; conf=cm//1000
            capbind[(iid,depth)]=(bound, 1 if (tp>=1 and (cp*1000000)//tp < class_rate) else 0, corr)
            t+=1
            if corr==1: c+=1
            led[cls]=[c,t]; tp+=1
            if corr==1: cp+=1
            pers[iid]=[cp,tp]
        out.append(f"{iid}\t{fam}\t{depth}\t{rel}\t{corr}\t{conf}")
    return out, capbind

if __name__=="__main__":
    mode, in_tsv = sys.argv[1], sys.argv[2]
    out,_ = run(in_tsv, mode)
    sys.stdout.write("\n".join(out)+"\n")
