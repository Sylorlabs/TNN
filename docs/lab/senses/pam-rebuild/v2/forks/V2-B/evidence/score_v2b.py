#!/usr/bin/env python3
"""V2-B Python scorer: validate interventional logic before Zag port.
Program PASS iff (confG>=700) AND (all Pi: j(Pi)!=jG).
Gate: INSTALL iff (jF==jG) AND program PASS.
Ablation: INSTALL iff (jF==jG) [admission-only]."""
import json, os

LAB = "/home/hatch/workspace/tnn-lab"
V2W = "/home/hatch/workspace/v2work"

def load_sweep():
    rows = [json.loads(l) for l in open(
        LAB+"/senses/pam-rebuild/round2/forks/R2-4/evidence/clean/sweep.jsonl")]
    return {r["fid"]: r for r in rows if "err" not in r}

def load_gexp():
    items = json.load(open(V2W+"/gexp_items.json"))
    out = json.load(open(V2W+"/gexp_out.json"))
    # map fid -> (jG, confG)
    m = {}
    for it in items:
        seq = str(it["seq"])
        gpath = it["g"]
        # gpath like .../r2n_colorconst_0000.r24.g.r24
        fid = os.path.basename(gpath).replace(".g.r24", "")
        if seq in out:
            jG, confG = out[seq][0], int(out[seq][1])
            m[fid] = (jG, confG)
    return m

def load_prun():
    recs = {}
    for i in range(8):
        fp = os.path.join(V2W, f"prun_{i}.jsonl")
        if not os.path.exists(fp):
            continue
        for line in open(fp):
            r = json.loads(line)
            if "err" in r:
                continue
            key = (r["src"], r["pert"])
            recs[key] = (r["judgment"], r["conf"])
    return recs

def main():
    sweep = load_sweep()
    gexp = load_gexp()
    prun = load_prun()
    print(f"sweep={len(sweep)} gexp={len(gexp)} prun={len(prun)}", flush=True)
    
    # For each trial, compute full and ablation decisions
    full_install = 0
    abl_install = 0
    full_false = 0
    abl_false = 0
    total = 0
    
    for fid, s in sweep.items():
        if fid not in gexp:
            continue
        jF, confF = s["judgment"], s["conf"]
        truth = s["truth"]
        jG, confG = gexp[fid]
        
        # P judgments
        p_ok = True
        prog_pass = False
        if confG >= 700:
            prog_pass = True
            for pert in ("P1","P2","P3"):
                key = (fid, pert)
                if key not in prun:
                    prog_pass = False
                    break
                jP, _ = prun[key]
                # FAIL_clean = (jP != jG) [conservative, no measure]
                if jP == jG:
                    prog_pass = False
                    break
        
        # Full: INSTALL iff (jF==jG) AND prog_pass
        full = (jF == jG) and prog_pass
        # Ablation: INSTALL iff (jF==jG)
        abl = (jF == jG)
        
        if full:
            full_install += 1
            if jF != truth:
                full_false += 1
        if abl:
            abl_install += 1
            if jF != truth:
                abl_false += 1
        total += 1
    
    print(f"Total trials with G: {total}", flush=True)
    print(f"Full: install={full_install} ({full_install/total*100:.2f}%), false={full_false} ({full_false/total*100:.3f}%)", flush=True)
    print(f"Ablation: install={abl_install} ({abl_install/total*100:.2f}%), false={abl_false} ({abl_false/total*100:.3f}%)", flush=True)
    print(f"False-install reduction: {(abl_false-abl_false)/total*100:.3f}pp (abl {abl_false/total*100:.3f}% -> full {full_false/total*100:.3f}%)", flush=True)

if __name__ == "__main__":
    main()
