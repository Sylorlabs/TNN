#!/usr/bin/env python3
# gen_kha4.py — K-HA-4: Caesar taught (examples determine k), fresh probes must be 8/8.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ALPHA = "abcdefghijklmnopqrstuvwxyz"
def caesar(s,k):
    return "".join(chr((ord(c)-97+k)%26+97) if 'a'<=c<='z'
                   else chr((ord(c)-65+k)%26+65) if 'A'<=c<='Z' else c for c in s)
def ptok(seed, ln):
    out=[]; x=seed
    for _ in range(ln):
        x=(x*1103515245+12345)&0x7fffffff
        out.append(ALPHA[x%26])
    return "".join(out)
d=os.path.join(HERE,"battery_kha4"); os.makedirs(d,exist_ok=True)
k=5
teach_toks=["abc","xyz","hello","mnopq","st","wxy","defgh","jklm"]
lens=[2,2,3,3,4,4,5,5]
with open(os.path.join(d,"teach.tsv"),"w") as f:
    for t in teach_toks: f.write(f"r9\t{t}\t{caesar(t,k)}\n")
with open(os.path.join(d,"probe.tsv"),"w") as f:
    s=777; used=set(teach_toks)
    for ln in lens:
        while True:
            t=ptok(s,ln); s+=1
            if t not in used: break
        used.add(t)
        f.write(f"r9\t{t}\t{caesar(t,k)}\n")
print("kha4 written, k =",k)
