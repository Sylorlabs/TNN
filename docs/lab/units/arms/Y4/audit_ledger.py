#!/usr/bin/env python3
"""Audit a Y4 ledger.bin: verify lazy ordering and opcode semantics.
Opcode namespace (from cl/arm.zag): frozen 1..9,16..18 + Y4 32/33.
Layout (16 words): op@0 slot@1 rc@2 b1..b5@3..7 a1..a5@8..12 stage@13 d1@14 d2@15.
No clock word; implicit clock = entry position.
"""
import struct, sys

OP_ADD=1; OP_KILL=2; OP_PIN=3; OP_WEAKEN=4; OP_PROMOTE=5; OP_REVISE=6
OP_SCAN=7; OP_REFUSE=8; OP_EVICT=9; OP_TDB=16; OP_TDC=17; OP_TMV=18
OP_CAND=32; OP_QUESTION=33
Q_FULL=0; Q_SPAN=1
NAMES={1:"ADD",2:"KILL",3:"PIN",4:"WEAKEN",5:"PROMOTE",6:"REVISE",7:"SCAN",
       8:"REFUSE",9:"EVICT",16:"TDB",17:"TDC",18:"TMV",32:"CAND",33:"QUESTION"}

def main(path):
    raw=open(path,'rb').read()
    assert len(raw)%64==0, "ledger not a multiple of 64 bytes"
    n=len(raw)//64
    entries=[struct.unpack('<16i',raw[e*64:(e+1)*64]) for e in range(n)]
    issues=[]
    # per-corpus lazy ordering: all CAND(C) precede first QUESTION(C);
    # first ADD(C) strictly after first QUESTION(C); ADD implies a QUESTION
    byc={}
    for e,w in enumerate(entries):
        op=w[0]; b4=w[6]; b5=w[7]
        if op==OP_CAND: byc.setdefault(b4,{"cands":[],"qs":[],"adds":[]})["cands"].append(e)
        elif op==OP_QUESTION: byc.setdefault(b4,{"cands":[],"qs":[],"adds":[]})["qs"].append(e)
        elif op==OP_ADD: byc.setdefault(b4,{"cands":[],"qs":[],"adds":[]})["adds"].append(e)
    for corpus,d in sorted(byc.items()):
        if d["cands"] and d["qs"] and max(d["cands"])>min(d["qs"]):
            issues.append(f"corpus {corpus}: CAND at {max(d['cands'])} after first QUESTION at {min(d['qs'])}")
        if d["adds"] and d["qs"] and min(d["adds"])<min(d["qs"]):
            issues.append(f"corpus {corpus}: ADD before first QUESTION")
        if d["adds"] and not d["qs"]:
            issues.append(f"corpus {corpus}: ADDs with no QUESTION")
    # QUESTION entries: valid type; corpus ingested (has candidates)
    for e,w in enumerate(entries):
        if w[0]==OP_QUESTION:
            if w[14] not in (Q_FULL,Q_SPAN):
                issues.append(f"entry {e}: QUESTION bad type d1={w[14]}")
            if w[6] not in byc or not byc[w[6]]["cands"]:
                issues.append(f"entry {e}: QUESTION on corpus {w[6]} with no candidates")
    # no ADD after KILL for the same chunk id (b5 of ADD/KILL is the chunk id)
    id_events={}
    for e,w in enumerate(entries):
        if w[0] in (OP_ADD,OP_KILL):
            id_events.setdefault(w[7],[]).append((e,w[0]))
    for idv,evs in id_events.items():
        for j in range(1,len(evs)):
            if evs[j][1]==OP_ADD and evs[j-1][1]==OP_KILL:
                issues.append(f"id {idv}: ADD after KILL")
    # REFUSE entries must name a reason (d1)
    for e,w in enumerate(entries):
        if w[0]==OP_REFUSE and w[14]==0:
            issues.append(f"entry {e}: REFUSE with no reason code")
    counts={}
    for w in entries:
        k=NAMES.get(w[0],f"UNK{w[0]}"); counts[k]=counts.get(k,0)+1
    print(f"entries={n} issues={len(issues)}")
    for i in issues[:20]: print("  ISSUE:",i)
    print("opcodes:",dict(sorted(counts.items())))
    return 1 if issues else 0

sys.exit(main(sys.argv[1]))
