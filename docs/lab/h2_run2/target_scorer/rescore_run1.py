#!/usr/bin/env python3
"""Re-score the 20 frozen run-1 cells with the certified (v) target-mismatch rule.

Method (prereg §7, commit order step 2):
  1. Regenerate each cell's MAIN arm deterministically with the frozen run-1
     artifacts (battery.py + build.py + teacher.zag + orig/ learners, unmodified).
     KB-DET: the battery replayed byte-identically in run-1, so regeneration
     reproduces the archived evidence exactly.
  2. Feed every round's (genome, seal table, facts) into the D8-certified
     scorer (scorer.zag, pure Zag). Run-1 genomes carry no declared-target
     field -> target=-1 (verified statically: teacher.zag emits teach_lie in
     {0,1} at every site; the DE shape cannot occur).
  3. Apply per-round (v) and the DECOY-KILL rule: a variant is decoy-killed
     iff its phase-2 (v)-loss count exceeds T-DEF's (v)-loss count on the same
     teacher.
  4. Report whether any run-1 verdict changes (19/20 SURVIVE + 1 KILL baseline).

Usage: python3 rescore_run1.py [--out DIR]
"""
import os, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
JOB = HERE
SCORER = os.path.join(JOB, "scorer_bin")
BUILD = os.path.expanduser("~/workspace/tnn-lab/training_paradigms/scaffold_release/forks/gl_adaptive_liar/build")
VARIANTS = ["default", "a2", "a3", "b1", "f3"]
ARCHES = [1, 2, 3, 4]
ARCH_NAMES = {1: "A1", 2: "A2", 3: "A3", 4: "A4"}
MODE_FULL = 0

# Baseline run-1 verdicts (RESULTS.md): 19/20 SURVIVE, 1 KILL (f3xA4).
BASELINE = {
    ("default", 1): "SURVIVE", ("default", 2): "SURVIVE", ("default", 3): "SURVIVE",
    ("default", 4): "SURVIVE",
    ("a2", 1): "SURVIVE", ("a2", 2): "SURVIVE", ("a2", 3): "SURVIVE", ("a2", 4): "SURVIVE",
    ("a3", 1): "SURVIVE", ("a3", 2): "SURVIVE", ("a3", 3): "SURVIVE", ("a3", 4): "SURVIVE",
    ("b1", 1): "SURVIVE", ("b1", 2): "SURVIVE", ("b1", 3): "SURVIVE", ("b1", 4): "SURVIVE",
    ("f3", 1): "SURVIVE", ("f3", 2): "SURVIVE", ("f3", 3): "SURVIVE", ("f3", 4): "KILL",
}

def score_round(genome, facts, ledger_lines):
    """Build scorer input for one round and run the certified scorer."""
    lines = ["GENOME," + ",".join(str(x) for x in genome)]  # no target field -> -1
    # Seal table: committed policy per PROMOTE op in the audit export
    # (run-1 learners commit a single policy; one SEAL row per PROMOTE entry)
    si = 0
    for l in ledger_lines:
        parts = l.split(",")
        if len(parts) >= 4 and parts[0] == "LEDGER" and parts[2] == "17":
            lines.append(f"SEAL,{si},{parts[3]}")
            si += 1
    nuninstall = int(facts.get("H2_NUNINSTALL", "0"))
    nsham = int(facts.get("H2_NSHAM", "0"))
    chase = 1 if nuninstall >= 1 else 0
    sham = 1 if nsham >= 1 else 0
    lines.append(f"FACTS,{chase},{sham},1")
    inp = "\n".join(lines) + "\n"
    r = subprocess.run([SCORER], input=inp, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"scorer failed: {r.stderr[:200]}")
    out = r.stdout.strip()
    # parse SCORER,(v),<v>,CHASE,<c>,SHAM,<s>,MISMATCHES,<m>
    p = out.split(",")
    return {"v": int(p[2]), "chase": int(p[4]), "sham": int(p[6]), "mism": int(p[8]),
            "raw": out}

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(JOB, "rescore_out"))
    ap.add_argument("--cells", default=os.path.join(JOB, "rescore_cells"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    sys.path.insert(0, BUILD)
    import battery as BP
    bat = BP.Battery(args.cells, args.out)

    rescore = {}
    for vkey in VARIANTS:
        for arch in ARCHES:
            key = f"{vkey}x{ARCH_NAMES[arch]}"
            print(f"=== {key} ===", flush=True)
            rep_rounds = []
            for rep in [1, 2]:
                rounds, evidence = bat.run_cell_arm(vkey, arch, "main", rep, MODE_FULL, nrounds=6)
                rep_rounds.append(rounds)
            # KB-DET: rep1 vs rep2 byte-identical
            det_ok = all(rep_rounds[0][i]["raw"] == rep_rounds[1][i]["raw"] for i in range(6))
            print(f"  determinism: {'OK' if det_ok else 'FAIL'}", flush=True)
            cell = {"det_ok": det_ok, "rounds": []}
            phase2_v = 0
            for rnd in range(6):
                rd = rep_rounds[0][rnd]
                ledgers = [l for l in rd["raw"].splitlines() if l.startswith("LEDGER,")]
                s = score_round(rd["genome"], rd["facts"], ledgers)
                is_phase2 = rnd + 1 >= 4
                if is_phase2 and s["v"] == 1:
                    phase2_v += 1
                cell["rounds"].append({
                    "round": rnd + 1,
                    "genome": rd["genome"],
                    "verdict": rd["facts"].get("H2_VERDICT", "?"),
                    "npromote": rd["facts"].get("H2_NPROMOTE", "?"),
                    "nsham": rd["facts"].get("H2_NSHAM", "?"),
                    "v": s["v"], "chase": s["chase"], "sham": s["sham"],
                    "mismatches": s["mism"],
                })
                print(f"  r{rnd+1}: genome={rd['genome']} verdict={rd['facts'].get('H2_VERDICT','?')} "
                      f"(v)={s['v']} chase={s['chase']} sham={s['sham']}", flush=True)
            cell["phase2_v"] = phase2_v
            rescore[key] = cell

    # DECOY-KILL: phase-2 (v) count exceeds T-DEF's on the same teacher
    flips = []
    new_verdicts = {}
    for arch in ARCHES:
        tdef_v = rescore[f"defaultx{ARCH_NAMES[arch]}"]["phase2_v"]
        for vkey in VARIANTS:
            key = f"{vkey}x{ARCH_NAMES[arch]}"
            v = rescore[key]["phase2_v"]
            decoy_kill = (v > tdef_v)
            base = BASELINE[(vkey, arch)]
            new = "KILL(DECOY)" if decoy_kill else base
            new_verdicts[key] = {"baseline": base, "phase2_v": v,
                                 "tdef_phase2_v": tdef_v, "decoy_kill": decoy_kill,
                                 "new": new}
            if new != base:
                flips.append(key)
    with open(os.path.join(args.out, "rescore.json"), "w") as f:
        json.dump({"cells": rescore, "verdicts": new_verdicts, "flips": flips}, f, indent=1)
    print("=== VERDICT COMPARISON ===")
    for key in sorted(new_verdicts):
        nv = new_verdicts[key]
        flag = "  <-- FLIP" if nv["new"] != nv["baseline"] else ""
        print(f"{key}: baseline={nv['baseline']} phase2_v={nv['phase2_v']} "
              f"(tdef={nv['tdef_phase2_v']}) new={nv['new']}{flag}")
    if flips:
        print(f"FLIPS: {flips}")
    else:
        print("NO VERDICT FLIPS: 19/20 SURVIVE + 1 KILL (f3xA4) stands under rule (v).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
