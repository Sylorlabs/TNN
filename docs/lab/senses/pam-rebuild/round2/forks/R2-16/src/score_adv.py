#!/usr/bin/env python3
"""score_adv.py -- Score false installs from adversarial ledger."""
import json, re, os, sys, math

HERE=os.path.dirname(os.path.abspath(__file__))
FORK=os.path.normpath(os.path.join(HERE,".."))
R27=os.path.normpath(os.path.join(FORK,"..","R2-7"))

TASKS=["colordisc","colorconst","shapetrans","pitchdisc","timbredisc","motiondir"]
JMAP={
    "colordisc":{"SAME":0,"DIFFERENT":1},
    "colorconst":{"SAME_SURFACE":0,"DIFFERENT":1},
    "shapetrans":{"CIRCLE":0,"TRIANGLE":1,"SQUARE":2},
    "pitchdisc":{"SAME":0,"HIGHER":1,"LOWER":2},
    "timbredisc":{"PURE":0,"BRIGHT":1,"DARK":2,"RICH":3},
    "motiondir":{"STILL":0,"N":1,"NE":2,"E":3,"SE":4,"S":5,"SW":6,"W":7,"NW":8},
}

def wilson_ucb(k,n,z=1.96):
    if n==0: return 1.0
    p=k/n
    den=1+z*z/n
    ctr=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return min(1.0,ctr+half)

def main():
    ledger_path=sys.argv[1] if len(sys.argv)>1 else "/tmp/b_adv_test.ledger"
    list_path=os.path.join(FORK,"evidence","b_adv.list")
    # Load truth
    truth={}
    for line in open(os.path.join(R27,"evidence","gen_ledger.jsonl")):
        d=json.loads(line)
        truth[d["id"]]=d["truth"]
    # Load list order
    with open(list_path) as f:
        paths=[l.strip() for l in f]
    # Parse ledger
    pat=re.compile(r'fixture=r2fx_t(\d+)_i(\d+)_f(\d+)\s+task=(\w+)\s+judgment=(\S+)\s+conf=\d+\s+challenge=\S+\s+outcome=\S+\s+disp=(\w+)')
    total_fi=0
    per_task={}
    per_family={}
    with open(ledger_path) as f:
        for lineno,line in enumerate(f):
            m=pat.search(line)
            if not m: continue
            t_idx,idx,fam,task,jname,disp=m.groups()
            if disp!="INSTALL": continue
            # Get truth
            if lineno>=len(paths): continue
            p=paths[lineno]
            mm=re.match(r'.*/(r2n|r2a|r2a2)_(\w+)_(\d+)\.r2fx$',p)
            if not mm: continue
            split,ltask,lidx=mm.groups()
            oid="%s_%s_%s"%(split,ltask,lidx)
            ttruth=truth.get(oid)
            if not ttruth: continue
            jid=JMAP[task].get(jname,-1)
            tid=JMAP[task].get(ttruth,-1)
            if jid!=tid:  # False install
                total_fi+=1
                per_task[task]=per_task.get(task,0)+1
                famkey=(task,fam)
                per_family[famkey]=per_family.get(famkey,0)+1
    n=10000
    print("Total false installs: %d/%d = %.2f%%"%(total_fi,n,100.0*total_fi/n))
    print("Overall UCB (95%%): %.3f%%"%(100*wilson_ucb(total_fi,n)))
    print("\nPer-task:")
    for task in TASKS:
        k=per_task.get(task,0)
        # Count per task total (need to count from list)
        print("  %s: %d"%(task,k))
    print("\nPer-family (nonzero):")
    for (task,fam),k in sorted(per_family.items()):
        print("  %s f%s: %d"%(task,fam,k))

if __name__=="__main__":
    main()
