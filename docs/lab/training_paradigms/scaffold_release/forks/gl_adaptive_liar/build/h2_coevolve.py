#!/usr/bin/env python3
"""H2 co-evolution harness: pure-Zag teacher + pure-Zag learner, Python orchestrates only.

For each round 1..7:
  1. Run teacher.zag (arch, round, genome, evidence-stdin) -> GENOME, LPARAMS (stdout).
  2. Build learner cell with genome + lparams (via build.py build_cell).
  3. Run learner -> parse H2_F, H2_NSHAM, ..., H2_VERDICT, LEDGER lines.
  4. Append to cumulative evidence for next round.

Usage: python3 h2_coevolve.py <arch 1..4> <variant default|a2|a3|b1|f3> <outdir>
"""
import sys, os, subprocess, re, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build

TEACHER_BIN = os.path.join(os.path.expanduser("~/workspace/h2_scratch"), "teacher_test")

def parse_teacher_out(out):
    genome = None; lparams = None
    for line in out.split("\n"):
        if line.startswith("GENOME,"):
            genome = list(map(int, line.split(",")[1:]))
        elif line.startswith("LPARAMS,"):
            lparams = list(map(int, line.split(",")[1:]))
    assert genome and len(genome) == 8, f"bad GENOME: {out[:200]}"
    assert lparams and len(lparams) == 9, f"bad LPARAMS: {out[:200]}"
    return genome, lparams

def genome_to_dict(g):
    keys = ["stated","teach_lie","sched","aa_lo","aa_hi","dens","keyrot","actfault"]
    return dict(zip(keys, g))

def lparams_to_dict(lp):
    keys = ["win_lo","win_hi","prom_ep","gate_mask","blacklist","shamguard","liveness","quar_policy","selfaudit"]
    return dict(zip(keys, lp))

def parse_learner_out(out):
    d = {}
    for line in out.split("\n"):
        if line.startswith("H2_F,"):
            d["F"] = int(line.split(",")[1])
        elif line.startswith("H2_NSHAM,"):
            d["nsham"] = int(line.split(",")[1])
        elif line.startswith("H2_VERDICT,"):
            d["verdict"] = line.split(",")[1].strip()
    # Also capture LEDGER lines for evidence
    ledger = [l for l in out.split("\n") if l.startswith("LEDGER,")]
    # Capture H2_ lines for evidence
    h2lines = [l for l in out.split("\n") if l.startswith("H2_") and "," in l]
    return d, ledger, h2lines

def run_coevolution(arch, vkey, outdir, rounds=7):
    os.makedirs(outdir, exist_ok=True)
    # Initial genome: GENOME_1 (from build.py)
    genome = [build.GENOME_1[k] for k in ["stated","teach_lie","sched","aa_lo","aa_hi","dens","keyrot","actfault"]]
    evidence_lines = []  # cumulative
    results = []
    for rnd in range(1, rounds+1):
        # 1. Teacher
        t_args = [TEACHER_BIN, str(arch), str(rnd)] + [str(x) for x in genome]
        ev_input = "\n".join(evidence_lines) + ("\n" if evidence_lines else "")
        # Prepend ROUND and GENOME for this round
        ev_for_teacher = f"ROUND,{rnd}\nGENOME,{','.join(map(str,genome))}\n" + ev_input
        p = subprocess.run(t_args, input=ev_for_teacher.encode(), capture_output=True, timeout=60)
        assert p.returncode == 0, f"teacher failed round {rnd}: {p.stderr.decode()[:500]}"
        new_genome, lparams = parse_teacher_out(p.stdout.decode())
        # 2. Build learner
        gdict = genome_to_dict(new_genome)
        pdict = lparams_to_dict(lparams)
        cellname = f"h2_{vkey}_a{arch}_r{rnd}"
        cell, binp = build.build_cell(vkey, gdict, pdict, "h2", cellname)
        # 3. Run learner
        p2 = subprocess.run([binp], input=b"", capture_output=True, timeout=120)
        assert p2.returncode == 0, f"learner failed round {rnd}: {p2.stderr.decode()[:500]}"
        out = p2.stdout.decode()
        res, ledger, h2lines = parse_learner_out(out)
        # 4. Save
        with open(os.path.join(outdir, f"round{rnd}.txt"), "w") as f:
            f.write(f"GENOME_IN,{','.join(map(str,genome))}\n")
            f.write(f"GENOME_OUT,{','.join(map(str,new_genome))}\n")
            f.write(f"LPARAMS,{','.join(map(str,lparams))}\n")
            f.write(out)
        # 5. Update evidence for next round
        evidence_lines.append(f"ROUND,{rnd}")
        evidence_lines.append(f"GENOME,{','.join(map(str,new_genome))}")
        for hl in h2lines:
            # Convert H2_F,123 -> H2_F,123 (already in right format)
            # But teacher expects H2_F,<n> etc. - extract key and value
            parts = hl.split(",")
            if len(parts) >= 2:
                evidence_lines.append(f"{parts[0]},{parts[1]}")
        evidence_lines.extend(ledger)
        genome = new_genome
        results.append((rnd, new_genome, res.get("F"), res.get("verdict")))
        print(f"Round {rnd}: genome={new_genome} F={res.get('F')} verdict={res.get('verdict')}", flush=True)
        # Clean up cell to save space (keep the round output)
        shutil.rmtree(cell, ignore_errors=True)
    return results

if __name__ == "__main__":
    arch = int(sys.argv[1]); vkey = sys.argv[2]; outdir = sys.argv[3]
    results = run_coevolution(arch, vkey, outdir)
    print("Done:", results)
