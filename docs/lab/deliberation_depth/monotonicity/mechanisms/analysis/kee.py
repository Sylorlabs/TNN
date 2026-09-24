#!/usr/bin/env python3
"""KEE: Kernel-Existence Experiment (grok Phase 1) for H5B evidential items.

Defines a 'dumb kernel' K_dumb that validates a 'proof' (a cited evidence set
for an answer) iff every cited item was consumed and the net weight
(supports - attacks) for that answer is > 0.

Measures (grok's Phase-1 gate):
  - On O items at shallow depths (correct): does a K-valid proof of GT exist?
  - On O items at deep depths (wrong): does a K-valid proof of the wrong answer exist?
  - On trap items at d1 (wrong): does a K-valid proof of the trap answer exist?

Gate: GO if >=80% shallow-correct extract AND <=5% deep-wrong extract.
       NO-GO if >10% deep-wrong extract OR <30% shallow-correct extract.
"""
import json, glob

def load_items(pat):
    items=[]
    for fn in glob.glob(pat):
        for ln in open(fn):
            ln=ln.strip()
            if ln: items.append(json.loads(ln))
    return items

def k_dumb_accept(item, answer, evidence_ids):
    """K_dumb: all cited evidence consumed (trivially true here) and net>0."""
    net=0
    evmap={e["id"]:e for e in item["input"]["evidence"]}
    for eid in evidence_ids:
        e=evmap[eid]
        net+=e.get("supports",{}).get(answer,0)
        net-=e.get("attacks",{}).get(answer,0)
    return net>0, net

def main():
    base="/home/hatch/workspace/tnn-lab/deliberation_depth/ceiling/items/ceiling_battery.jsonl"
    items=load_items(base)
    o_items=[it for it in items if it["id"].startswith("H5B-O-")]
    print(f"O items: {len(o_items)}")
    # Shallow-correct: GT proof using first-half evidence
    # Deep-wrong: wrong-answer proof using second-half evidence
    shallow_ok=0; deep_ok=0; n=0
    for it in o_items:
        gt=it["ground_truth"]
        hyps=[h["id"] for h in it["input"]["evidence"] and it["input"]["hypotheses"]]
        wrong=[h for h in hyps if h!=gt][0]
        evs=it["input"]["evidence"]
        ne=len(evs)
        # shallow: first min(4,ne) items for GT
        s_ids=[e["id"] for e in evs[:min(4,ne)]]
        ok_s,_=k_dumb_accept(it,gt,s_ids)
        # deep: last min(4,ne) items for wrong answer
        d_ids=[e["id"] for e in evs[max(0,ne-4):]]
        ok_d,net_d=k_dumb_accept(it,wrong,d_ids)
        # also try full evidence for wrong (adversarial best case)
        ok_d_full,net_df=k_dumb_accept(it,wrong,[e["id"] for e in evs])
        if ok_s: shallow_ok+=1
        if ok_d or ok_d_full: deep_ok+=1
        n+=1
        if n<=3:
            print(f"  {it['id']}: GT={gt} shallow_proof={ok_s} wrong={wrong} deep_proof={ok_d or ok_d_full} (net_full={net_df})")
    print(f"\nShallow-correct extract: {shallow_ok}/{n} = {shallow_ok/n:.2f}")
    print(f"Deep-wrong extract: {deep_ok}/{n} = {deep_ok/n:.2f}")
    go = (shallow_ok/n>=0.80) and (deep_ok/n<=0.05)
    nogo = (deep_ok/n>0.10) or (shallow_ok/n<0.30)
    print(f"\nGate: {'GO' if go else ('NO-GO' if nogo else 'INCONCLUSIVE')}")
    if nogo:
        print("Verdict: NO-GO — the deliberator's reasons do not discriminate truth;")
        print("a dumb kernel validates misleading evidence. No sound kernel exists")
        print("for the evidential domain without validating truth itself (circular).")

main()
