#!/usr/bin/env python3
"""Scorer for the contradiction-matrix battery (glue only).

Reads a cm_bin stdout file, compares per-trial dispositions against
EXPECT.tsv and per-cell final state against EXPECT_CELL.tsv (both generated
from the frozen prereg). Prints a per-gate-cell PASS/FAIL table and a summary.
Exit 0 iff every gate-cell passes.
"""
import sys
sys.path.insert(0, ".")
from gen_cells import CELLS
CORRECT_FINAL = {c["name"]: c["correct_final_j"] for c in CELLS}

DISP = {0:"PERM",1:"PROV",2:"CORR",3:"CONF",4:"CHAL",5:"REV",6:"ACC",7:"WITH"}
INSTALLS = {0,1,2,4,5,6}

def load(path):
    exp = {}
    for line in open(path):
        line=line.strip()
        if not line or line.startswith("cell"):
            continue
        c,g,t,d = line.split("\t")
        exp.setdefault((c,int(g)), {})[int(t)] = int(d)
    return exp

def load_cell(path):
    exp = {}
    for line in open(path):
        line=line.strip()
        if not line or line.startswith("cell"):
            continue
        c,g,fj,fi,ni = line.split("\t")
        exp[(c,int(g))] = (int(fj),int(fi),int(ni))
    return exp

def main():
    run = sys.argv[1]
    base = sys.argv[2] if len(sys.argv)>2 else "."
    exp = load(base+"/EXPECT.tsv")
    expc = load_cell(base+"/EXPECT_CELL.tsv")
    got = {}
    for line in open(run):
        line=line.strip()
        if not line.startswith("CM|"):
            continue
        _,c,g,t,d,pj,ps = line.split("|")
        got.setdefault((c,int(g)), {})[int(t)] = (int(d),int(pj),int(ps))
    fails = 0
    total = 0
    print("cell gate | expected seq            | actual seq              | final_perm exp/act | fi exp/act | installs | verdict")
    for (c,g) in sorted(got):
        total += 1
        eseq = [exp[(c,g)][t] for t in sorted(exp[(c,g)])]
        aseq = [got[(c,g)][t][0] for t in sorted(got[(c,g)])]
        efj,efi,eni = expc[(c,g)]
        correct = CORRECT_FINAL[c]
        last = max(got[(c,g)])
        afj = got[(c,g)][last][1]
        # false install: a REVISED/ACCEPT install occurred AND the final permanent
        # judgment differs from the cell's correct final jcode (prereg §5)
        rev_or_acc = any(got[(c,g)][t][0] in (5,6) for t in got[(c,g)])
        afi = 1 if (rev_or_acc and correct != -1 and afj != correct) else 0
        ains = sum(1 for t in got[(c,g)] if got[(c,g)][t][0] in INSTALLS)
        ok = (eseq==aseq) and (afi==efi) and (afj==efj or (efj==-1 and afj==-1))
        if c=="W1":
            ok = ok and (ains==0)
        if not ok:
            fails += 1
        es = ",".join(DISP[d] for d in eseq)
        as_ = ",".join(DISP[d] for d in aseq)
        print("%-4s %-4d | %-22s | %-22s | %3d / %-3d        | %d / %d     | %-8d | %s" % (
            c,g,es,as_,efj,afj,efi,afi,ains,"PASS" if ok else "FAIL"))
    print("summary: %d/%d gate-cells PASS" % (total-fails,total))
    return 1 if fails else 0

if __name__=="__main__":
    sys.exit(main())
