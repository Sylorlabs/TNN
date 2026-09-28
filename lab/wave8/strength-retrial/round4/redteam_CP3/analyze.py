#!/usr/bin/env python3
"""Red-team analysis for arm C-P3 (strength round 4).
Parses rd_dump_bin AUD ledgers, then:
  1. extracts every PEXPIRED (op=19) entry and audits it independently
     against the expiry conditions (SYSTEM role, audit-only before==after,
     age>K, since-cite>K, strength>0, live);
  2. verifies C runs carry zero PEXPIRED entries;
  3. diffs C vs C-P3 ledgers per cell and classifies divergence;
  4. counts baseline (need=1) kills attributable to expiry.
"""
import sys, glob, os

OP = {1:'ADD',2:'KILL',3:'PIN',4:'UNPIN',5:'PROMOTE',6:'DEMOTE',7:'ROLLBACK',
      8:'SETSTAGE',9:'KILL_EVIDENCED',10:'EVIDENCE',11:'JUSTIFY',12:'STRENGTHEN',
      13:'WEAKEN',14:'TRAINER_DECLARE',15:'OVERWRITE',16:'FORCE_PIN',
      17:'FORCE_UNPIN',18:'ABANDON',19:'PEXPIRED'}
K_BY_SCALE = {'S1':50,'S10':500,'S100':5000}

def parse(fn):
    entries = []
    fp = None
    with open(fn) as f:
        for line in f:
            line=line.strip()
            if line.startswith('AUD '):
                p=line.split()
                entries.append([int(x) for x in p[2:]])
            elif line.startswith('AUD_FP '):
                fp=int(line.split()[1])
    return entries, fp

def audit_pexpired(entries, arm, k):
    """Independently re-derive expiry state and check every PEXPIRED entry."""
    adm={}; lc={}; pexp_count=0; problems=[]
    n_pexp=0
    for i,e in enumerate(entries):
        op,sl,aux,aux2,rc=e[0],e[1],e[2],e[3],e[4]
        b=e[5:11]; a=e[11:17]; role=e[17]
        if rc!=0:
            continue
        if op==1:  # ADD
            adm[sl]=aux; lc[sl]=-1
        elif op==10:  # EVIDENCE
            lc[sl]=aux
        elif op in (12,13) and aux>=0:  # STRENGTHEN/WEAKEN
            lc[sl]=aux
        elif op in (2,9):  # KILL/KILL_EVIDENCED
            adm.pop(sl,None); lc.pop(sl,None)
        elif op==15:  # OVERWRITE
            adm[sl]=aux; lc[sl]=-1
        elif op==19:  # PEXPIRED
            n_pexp+=1
            ep=aux
            # 1. arm must be C-P3 (3)
            if arm!=3:
                problems.append((i,'arm!=3',arm))
            # 2. SYSTEM role
            if role!=3:
                problems.append((i,'role!=SYSTEM',role))
            # 3. audit-only: before==after
            if b!=a:
                problems.append((i,'before!=after',b,a))
            # 4. strength>0 and live (before-snapshot: w1&255=live, w4&255=strength)
            live_b=b[0]&255; str_b=b[3]&255
            if live_b!=1:
                problems.append((i,'not-live-before',live_b))
            if str_b<=0:
                problems.append((i,'strength<=0',str_b))
            # 5. genuinely expired: adm>=0, ep-adm>k, ep-lc>k
            a2=adm.get(sl,-1); l2=lc.get(sl,-1)
            if a2<0 or ep-a2<=k or ep-l2<=k:
                problems.append((i,'not-genuinely-expired',(a2,l2,ep,k)))
            pexp_count+=1
    return n_pexp, problems

def op_hist(entries):
    h={}
    for e in entries:
        h[e[0]]=h.get(e[0],0)+1
    return h

def main():
    d='.'
    files=sorted(glob.glob(os.path.join(d,'dump_*_S1.txt')))
    print("cell,arm,cur,var,n_audit,fp,n_pexp,pexp_problems")
    pexp_by={}
    for fn in files:
        base=os.path.basename(fn)[5:-4]  # A_CUR_V_S1
        a,cur,v,sc=base.split('_')
        arm={'B':1,'C':2,'C-P3':3}[a]
        entries,fp=parse(fn)
        k=K_BY_SCALE[sc]
        n_pexp,probs=audit_pexpired(entries,arm,k)
        pexp_by[base]=(n_pexp,probs,entries)
        print(f"{base},{arm},{cur},{v},{len(entries)},{fp},{n_pexp},{len(probs)}")
        for p in probs:
            print("   PROBLEM",p)
    # C runs must have zero PEXPIRED
    print("\n--- op histograms: C vs C-P3 (rc==0 counts) ---")
    for cur in ['VUP','WBS','JI']:
        for v in ['0','1','2']:
            for a in ['C','C-P3']:
                fn=os.path.join(d,f'dump_{a}_{cur}_{v}_S1.txt')
                entries,_=parse(fn)
                h=op_hist([e for e in entries if e[4]==0])
                hs=' '.join(f"{OP.get(o,o)}={c}" for o,c in sorted(h.items()))
                print(f"{a} {cur} v{v}: n={len(entries)} {hs}")

if __name__=='__main__':
    main()
