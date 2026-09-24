#!/usr/bin/env python3
"""Stated-policy-only ablation (§11 decision 2).

A1 and A2 × T-DEF (default variant), 6 rounds, full L active.
Teacher sets `stated` only, all other genome fields frozen at genome_1.
- A1: stated cycles {2,0,7}
- A2: repeats genome_1
A3/A4 are void in this scope.

2 arch × 6 rounds × 2 reps = 24 runs.
"""
import os, sys, subprocess, hashlib, json

sys.path.insert(0, os.path.dirname(__file__))
from battery import Battery, parse_h2_facts

def main():
    bat = Battery("/tmp/stated_cells", "/tmp/stated_out")
    results = {}
    for arch, aname in [(1, "A1"), (2, "A2")]:
        for rep in [1, 2]:
            print(f"=== {aname} rep{rep} ===", flush=True)
            evidence = ""
            cur_genome = [2,1,0,29,48,0,0,0]
            rounds = []
            for rnd in range(1, 7):
                # tmode=3: stated-policy-only
                ng, lp, sha = bat.run_teacher(arch, rnd, cur_genome, 3, evidence)
                tag = f"stated_{aname}_r{rep}_{rnd}"
                cell, binp = bat.get_cell("default", ng, lp, tag)
                r = subprocess.run([binp], capture_output=True, text=True)
                facts = parse_h2_facts(r.stdout)
                print(f"  r{rnd}: genome={ng} F={facts.get('H2_F')} verdict={facts.get('H2_VERDICT')}", flush=True)
                # evidence
                ev_lines = [f"ROUND,{rnd}", f"GENOME,{','.join(str(x) for x in ng)}"]
                for k in ["H2_F","H2_NSHAM","H2_NCOMMIT","H2_NUNINSTALL","H2_NPROMOTE",
                          "H2_REVOKE_STEP","H2_BADEP","H2_AUDIT_TOTAL","H2_QUAR_USED",
                          "H2_PROMOTE_STEP","H2_WITHHELD","H2_CAL_SCORE","H2_VERDICT"]:
                    if k in facts:
                        ev_lines.append(f"{k},{facts[k]}")
                ev_lines.extend(facts.get("_ledgers", []))
                ev = "\n".join(ev_lines) + "\n"
                sha_hex = hashlib.sha256(ev.encode()).hexdigest()
                evidence += ev + f"SHA256,{sha_hex}\n"
                rounds.append({"round": rnd, "genome": ng, "F": facts.get("H2_F"),
                               "verdict": facts.get("H2_VERDICT")})
                cur_genome = ng
            # verdict: KILL if >=2 phase-2 wins OR r6 win
            wins = sum(1 for r in rounds[3:6] if r["verdict"] == "KILLED")
            r6_win = (rounds[5]["verdict"] == "KILLED")
            verdict = "KILL" if (wins >= 2 or r6_win) else "SURVIVE"
            print(f"  verdict: {verdict} (wins={wins})", flush=True)
            results[f"{aname}_rep{rep}"] = {"rounds": rounds, "verdict": verdict, "wins": wins}
    with open("/tmp/stated_out/stated_results.json", "w") as f:
        json.dump(results, f, indent=1)
    print("Done.", flush=True)

if __name__ == "__main__":
    main()
