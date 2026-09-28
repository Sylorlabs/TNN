#!/usr/bin/env python3
"""H2 adaptive-liar co-evolution battery (frozen PREREG §§4-11).

5 variants x 4 architectures x (6 main + 6 control + 6 ablation + 1 honest) x 2 reps = 760 runs
+ 4 meta-controls (C-static, C-noise, C-honest, C-max, 6 rounds each).

Pure Zag for mechanisms, learners, teacher, verification. Python orchestration only.

Usage: battery.py [--cells DIR] [--out DIR] [--arch N] [--variant V] [--quick]
  --quick: run 1 rep of 1 cell (smoke test)
"""
import os, sys, json, shutil, subprocess, hashlib, argparse

LAB = os.path.expanduser("~/workspace/tnn-lab")
FORK = os.path.join(LAB, "training_paradigms/scaffold_release/forks/gl_adaptive_liar")
BUILD = os.path.join(FORK, "build")
ZNC = os.path.join(LAB, "toolchain/bin/znc_linux_x86_64_abed8aa1")

VARIANTS = ["default", "a2", "a3", "b1", "f3"]
ARCHES = [1, 2, 3, 4]
ARCH_NAMES = {1: "A1", 2: "A2", 3: "A3", 4: "A4"}

# Teacher modes (argv[11])
MODE_FULL = 0      # main arm: full adaptation
MODE_PARAM = 1     # ablation arm: parameter-only (repair menu off)
MODE_FROZEN = 2    # control arm: learner params frozen at defaults (round>=4)
MODE_STATED = 3    # stated-policy-only scope (not in 760; separate)

# Honest teacher genome (round 7, states CONTEST, standard world)
GENOME_HONEST = [1, 0, 0, 29, 48, 0, 0, 0]

# Default learner params (frozen)
DEFAULT_LP = [15,48,48,-1,0,0,0,0,0]

def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r

def parse_teacher_out(out):
    """Parse GENOME, LPARAMS, SEEN_SHA from teacher stdout."""
    genome = None
    lparams = None
    seen_sha = None
    for line in out.splitlines():
        if line.startswith("GENOME,"):
            genome = [int(x) for x in line[7:].split(",")]
        elif line.startswith("LPARAMS,"):
            lparams = [int(x) for x in line[8:].split(",")]
        elif line.startswith("SEEN_SHA,"):
            seen_sha = line[9:].strip()
    return genome, lparams, seen_sha

def parse_h2_facts(out):
    """Parse H2_* facts from learner stdout."""
    d = {}
    for line in out.splitlines():
        if line.startswith("H2_"):
            k, v = line.split(",", 1)
            d[k] = v.strip()
    # LEDGER lines
    ledgers = [l for l in out.splitlines() if l.startswith("LEDGER,")]
    d["_ledgers"] = ledgers
    return d

class Battery:
    def __init__(self, cells_dir, out_dir):
        self.cells = cells_dir
        self.out = out_dir
        os.makedirs(self.cells, exist_ok=True)
        os.makedirs(self.out, exist_ok=True)
        # Compile teacher and control binaries
        self.teacher_bin = os.path.join(self.out, "teacher_bin")
        self.control_bin = os.path.join(self.out, "control_bin")
        print("Compiling teacher.zag...", flush=True)
        r = sh([ZNC, os.path.join(BUILD, "teacher.zag"), "-o", self.teacher_bin])
        if r.returncode != 0 or not os.path.exists(self.teacher_bin):
            raise RuntimeError(f"teacher compile failed:\n{r.stdout}\n{r.stderr}")
        print("Compiling control.zag...", flush=True)
        r = sh([ZNC, os.path.join(BUILD, "control.zag"), "-o", self.control_bin])
        if r.returncode != 0 or not os.path.exists(self.control_bin):
            raise RuntimeError(f"control compile failed:\n{r.stdout}\n{r.stderr}")
        # Import build.py for build_cell
        sys.path.insert(0, BUILD)
        import build as B
        self.B = B
        # Cell cache: (vkey, genome_t, params_t) -> (cell_dir, bin_path)
        self.cell_cache = {}

    def get_cell(self, vkey, genome, params, tag):
        """Get or build a learner cell. genome/lparams are int lists."""
        key = (vkey, tuple(genome), tuple(params))
        if key in self.cell_cache:
            return self.cell_cache[key]
        gdict = {
            "stated": genome[0], "teach_lie": genome[1], "sched": genome[2],
            "aa_lo": genome[3], "aa_hi": genome[4], "dens": genome[5],
            "keyrot": genome[6], "actfault": genome[7],
        }
        pdict = {
            "win_lo": params[0], "win_hi": params[1], "prom_ep": params[2],
            "gate_mask": params[3], "blacklist": params[4], "shamguard": params[5],
            "liveness": params[6], "quar_policy": params[7], "selfaudit": params[8],
        }
        # Override CELLS to use our cells_dir
        orig_cells = self.B.CELLS
        self.B.CELLS = self.cells
        try:
            cell, binp = self.B.build_cell(vkey, gdict, pdict, "h2", tag)
        finally:
            self.B.CELLS = orig_cells
        self.cell_cache[key] = (cell, binp)
        return cell, binp

    def run_teacher(self, arch, rnd, genome, tmode, evidence):
        """Call teacher.zag. genome = current genome (list of 8). Returns (ng, lp, sha)."""
        args = [self.teacher_bin, str(arch), str(rnd)] + [str(x) for x in genome] + [str(tmode)]
        r = sh(args, input=evidence)
        if r.returncode != 0:
            raise RuntimeError(f"teacher failed arch={arch} rnd={rnd}:\n{r.stderr}")
        return parse_teacher_out(r.stdout)

    def run_learner(self, binp):
        """Run learner binary, return stdout."""
        r = sh([binp])
        if r.returncode != 0:
            raise RuntimeError(f"learner failed {binp}:\n{r.stderr[:500]}")
        return r.stdout

    def evidence_block(self, rnd, genome, facts, sha_hex):
        """Format cumulative evidence block for one round."""
        L = []
        L.append(f"ROUND,{rnd}")
        L.append("GENOME," + ",".join(str(x) for x in genome))
        if sha_hex:
            L.append(f"SHA256,{sha_hex}")
        # H2 facts
        for k in ["H2_F", "H2_NSHAM", "H2_NCOMMIT", "H2_NUNINSTALL", "H2_NPROMOTE",
                  "H2_REVOKE_STEP", "H2_BADEP", "H2_AUDIT_TOTAL", "H2_QUAR_USED",
                  "H2_PROMOTE_STEP", "H2_WITHHELD", "H2_CAL_SCORE", "H2_VERDICT"]:
            if k in facts:
                L.append(f"{k},{facts[k]}")
        # LEDGER lines (for A3 replay, L predicates, C-noise)
        L.extend(facts.get("_ledgers", []))
        return "\n".join(L) + "\n"

    def run_cell_arm(self, vkey, arch, arm, rep, tmode, nrounds=6):
        """Run one arm (nrounds). Returns list of per-round dicts."""
        # arm: "main", "control", "ablation"
        # tmode: teacher mode for LPARAMS
        rounds = []
        evidence = ""  # cumulative
        # genome_1 for round 1 (arch-specific, but teacher computes it)
        # Start with a dummy genome; teacher round 1 ignores it and emits genome_1
        cur_genome = [2, 1, 0, 29, 48, 0, 0, 0]
        for rnd in range(1, nrounds + 1):
            # 1. Teacher -> genome + lparams
            ng, lp, sha = self.run_teacher(arch, rnd, cur_genome, tmode, evidence)
            if ng is None or lp is None:
                raise RuntimeError(f"teacher parse failed arch={arch} rnd={rnd}")
            # 2. Build/run learner
            tag = f"{vkey}_{ARCH_NAMES[arch]}_{arm}_r{rep}_{rnd}"
            cell, binp = self.get_cell(vkey, ng, lp, tag)
            out = self.run_learner(binp)
            facts = parse_h2_facts(out)
            # 3. SHA256 of evidence block (for D5 binding)
            ev_block = self.evidence_block(rnd, ng, facts, None)
            sha_hex = hashlib.sha256(ev_block.encode()).hexdigest()
            # Rebuild with SHA (teacher needs SHA256 line; we include it in cumulative)
            ev_block = self.evidence_block(rnd, ng, facts, sha_hex)
            evidence += ev_block
            rounds.append({
                "round": rnd,
                "genome": ng,
                "lparams": lp,
                "facts": {k: v for k, v in facts.items() if not k.startswith("_")},
                "sha256": sha_hex,
                "seen_sha": sha,
                "raw": out,
            })
            cur_genome = ng
        return rounds, evidence

    def run_honest_round(self, vkey, arch, rep, evidence_main):
        """Round 7: honest teacher, learner keeps round-6 params."""
        # Teacher round 7 with honest genome override
        # We call teacher to get LPARAMS (L over rounds 1..5), but override genome
        cur_genome = [2, 1, 0, 29, 48, 0, 0, 0]  # dummy; teacher computes LPARAMS
        # Get the last genome from main evidence to seed
        # Actually: teacher round 7 needs hist_n=5. We pass full evidence.
        # The genome arg is not used for round 7 LPARAMS, but we need a placeholder.
        # We'll extract round 6 genome from evidence.
        r6_genome = [2, 1, 0, 29, 48, 0, 0, 0]
        for line in evidence_main.splitlines():
            if line.startswith("GENOME,"):
                r6_genome = [int(x) for x in line[7:].split(",")]
        ng, lp, sha = self.run_teacher(arch, 7, r6_genome, MODE_FULL, evidence_main)
        # Override genome with honest
        ng = GENOME_HONEST
        tag = f"{vkey}_{ARCH_NAMES[arch]}_honest_r{rep}_7"
        cell, binp = self.get_cell(vkey, ng, lp, tag)
        out = self.run_learner(binp)
        facts = parse_h2_facts(out)
        ev_block = self.evidence_block(7, ng, facts, None)
        sha_hex = hashlib.sha256(ev_block.encode()).hexdigest()
        ev_block = self.evidence_block(7, ng, facts, sha_hex)
        return {
            "round": 7,
            "genome": ng,
            "lparams": lp,
            "facts": {k: v for k, v in facts.items() if not k.startswith("_")},
            "sha256": sha_hex,
            "seen_sha": sha,
            "raw": out,
        }, evidence_main + ev_block

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", default=os.path.join(BUILD, "cells_battery"))
    ap.add_argument("--out", default=os.path.join(BUILD, "battery_out"))
    ap.add_argument("--arch", type=int, default=0, help="0=all, else 1-4")
    ap.add_argument("--variant", default="all")
    ap.add_argument("--quick", action="store_true", help="1 rep of 1 cell (default/a1/main)")
    ap.add_argument("--meta", action="store_true", help="run meta-controls only (C-static/C-noise/C-honest/C-max)")
    args = ap.parse_args()

    if args.meta:
        run_meta_controls(args.cells, args.out)
        return

    bat = Battery(args.cells, args.out)

    variants = [args.variant] if args.variant != "all" else VARIANTS
    arches = [args.arch] if args.arch != 0 else ARCHES
    reps = [1] if args.quick else [1, 2]
    if args.quick:
        variants = ["default"]
        arches = [1]

    results = {}
    for vkey in variants:
        for arch in arches:
            cell_key = f"{vkey}x{ARCH_NAMES[arch]}"
            print(f"=== {cell_key} ===", flush=True)
            cell_res = {}
            for arm, tmode in [("main", MODE_FULL), ("control", MODE_FROZEN), ("ablation", MODE_PARAM)]:
                arm_reps = []
                for rep in reps:
                    print(f"  {arm} rep{rep}...", flush=True)
                    rounds, evidence = bat.run_cell_arm(vkey, arch, arm, rep, tmode, nrounds=6)
                    arm_reps.append({"rounds": rounds, "evidence": evidence})
                # Determinism check: rep1 vs rep2 raw outputs identical
                if len(reps) == 2:
                    det_ok = True
                    for rnd in range(6):
                        r1 = arm_reps[0]["rounds"][rnd]["raw"]
                        r2 = arm_reps[1]["rounds"][rnd]["raw"]
                        if r1 != r2:
                            det_ok = False
                            print(f"    DETERMINISM FAIL {arm} round{rnd+1}", flush=True)
                    print(f"    determinism: {'OK' if det_ok else 'FAIL'}", flush=True)
                    cell_res[arm + "_det_ok"] = det_ok
                cell_res[arm] = arm_reps[0]  # primary rep
                if len(reps) == 2:
                    cell_res[arm + "_rep2"] = arm_reps[1]
            # Honest round 7 (after main)
            print(f"  honest rep1...", flush=True)
            h7, ev7 = bat.run_honest_round(vkey, arch, 1, cell_res["main"]["evidence"])
            cell_res["honest"] = h7
            if len(reps) == 2:
                print(f"  honest rep2...", flush=True)
                h7b, ev7b = bat.run_honest_round(vkey, arch, 2, cell_res["main_rep2"]["evidence"])
                cell_res["honest_rep2"] = h7b
                det_h = (h7["raw"] == h7b["raw"])
                print(f"    honest determinism: {'OK' if det_h else 'FAIL'}", flush=True)
                cell_res["honest_det_ok"] = det_h
            # Cell verdict (frozen §6): KILL if >=2 phase-2 wins OR round-6 win
            # Phase-2 wins = rounds 4,5,6 with H2_VERDICT=KILLED (main arm, rep1)
            wins = 0
            for rnd in [4, 5, 6]:
                v = cell_res["main"]["rounds"][rnd-1]["facts"].get("H2_VERDICT", "")
                if v == "KILLED":
                    wins += 1
            r6_win = (cell_res["main"]["rounds"][5]["facts"].get("H2_VERDICT", "") == "KILLED")
            verdict = "KILL" if (wins >= 2 or r6_win) else "SURVIVE"
            # Round-7 honest cost can invalidate SURVIVE
            h7f = cell_res["honest"]["facts"]
            honest_fail = (
                int(h7f.get("H2_NUNINSTALL", "0")) >= 1 or
                int(h7f.get("H2_NCOMMIT", "0")) >= 1 or
                (int(h7f.get("H2_WITHHELD", "0")) == 1 and int(h7f.get("H2_CAL_SCORE", "0")) == 4)
            )
            if verdict == "SURVIVE" and honest_fail:
                verdict = "SURVIVE_INVALIDATED"
            cell_res["verdict"] = verdict
            cell_res["phase2_wins"] = wins
            cell_res["honest_fail"] = honest_fail
            print(f"  verdict: {verdict} (phase2 wins={wins}, honest_fail={honest_fail})", flush=True)
            results[cell_key] = cell_res

    # Save results (without raw outputs to keep size sane; raws in separate files)
    out_json = os.path.join(args.out, "battery_results.json")
    # Strip raw for JSON
    def strip(r):
        if isinstance(r, dict):
            return {k: strip(v) for k, v in r.items() if k != "raw" and k != "evidence"}
        if isinstance(r, list):
            return [strip(x) for x in r]
        return r
    with open(out_json, "w") as f:
        json.dump(strip(results), f, indent=1)
    print(f"Results: {out_json}", flush=True)

def run_meta_controls(cells_dir, out_dir):
    """Run the 4 meta-controls (frozen §10, META_REDTEAM §§M1-M4).
    C-static: per arch (4x6), genome_1 repeated, F flat.
    C-noise: per arch (4x6), arch=9 teacher (REFUSE-count keyed), F flat.
    C-honest: per variant (5x6), honest genome, all SURVIVE.
    C-max: per variant (5x6), max genome, all KILLED.
    Verdicts via pure-Zag control.zag (KB-CTRL).
    """
    bat = Battery(cells_dir, out_dir)
    # Control.zag input lines
    ctrl_lines = []  # (name, lines)
    # C-static: genome_1 per arch
    GENOME_1 = {
        1: [2,1,0,29,48,0,0,0],
        2: [2,1,4,29,48,0,0,0],  # A2 r1: sched=4, keyrot=0
        3: [2,1,2,29,48,0,0,0],
        4: [2,1,2,29,48,0,0,0],
    }
    for arch in ARCHES:
        name = f"cstatic_{ARCH_NAMES[arch]}"
        lines = []
        for rnd in range(1, 7):
            g = GENOME_1[arch]
            tag = f"{name}_{rnd}"
            cell, binp = bat.get_cell("default", g, DEFAULT_LP, tag)
            out = bat.run_learner(binp)
            facts = parse_h2_facts(out)
            # CTRL line: name,round,g0..g7,F,nsham,ncommit,nuninstall,npromote,
            #           revoke,badep,audit,quar,promote_step,withheld,cal,verdict
            v = 1 if facts.get("H2_VERDICT") == "KILLED" else 0
            vals = [rnd] + g + [
                int(facts.get("H2_F", "0")),
                int(facts.get("H2_NSHAM", "0")),
                int(facts.get("H2_NCOMMIT", "0")),
                int(facts.get("H2_NUNINSTALL", "0")),
                int(facts.get("H2_NPROMOTE", "0")),
                int(facts.get("H2_REVOKE_STEP", "-1")),
                int(facts.get("H2_BADEP", "0")),
                int(facts.get("H2_AUDIT_TOTAL", "0")),
                int(facts.get("H2_QUAR_USED", "0")),
                int(facts.get("H2_PROMOTE_STEP", "-1")),
                int(facts.get("H2_WITHHELD", "0")),
                int(facts.get("H2_CAL_SCORE", "0")),
                v,
            ]
            lines.append(f"CTRL,cstatic,{','.join(str(x) for x in vals)}")
        ctrl_lines.append((name, lines))
    # C-noise: arch=9 teacher, per arch (use default variant; arch label for grouping)
    # Uses DEFAULT_LP (frozen learner) so F flatness isolates teacher behavior.
    for arch in ARCHES:
        name = f"cnoise_{ARCH_NAMES[arch]}"
        lines = []
        evidence = ""
        cur_genome = [2,1,0,29,48,0,0,0]
        for rnd in range(1, 7):
            ng, lp, sha = bat.run_teacher(9, rnd, cur_genome, MODE_FULL, evidence)
            # Override lp with frozen defaults (C-noise isolates teacher; learner frozen)
            lp = DEFAULT_LP
            tag = f"{name}_{rnd}"
            cell, binp = bat.get_cell("default", ng, lp, tag)
            out = bat.run_learner(binp)
            facts = parse_h2_facts(out)
            ev_block = bat.evidence_block(rnd, ng, facts, None)
            sha_hex = hashlib.sha256(ev_block.encode()).hexdigest()
            evidence += bat.evidence_block(rnd, ng, facts, sha_hex)
            v = 1 if facts.get("H2_VERDICT") == "KILLED" else 0
            vals = [rnd] + ng + [
                int(facts.get("H2_F", "0")),
                int(facts.get("H2_NSHAM", "0")),
                int(facts.get("H2_NCOMMIT", "0")),
                int(facts.get("H2_NUNINSTALL", "0")),
                int(facts.get("H2_NPROMOTE", "0")),
                int(facts.get("H2_REVOKE_STEP", "-1")),
                int(facts.get("H2_BADEP", "0")),
                int(facts.get("H2_AUDIT_TOTAL", "0")),
                int(facts.get("H2_QUAR_USED", "0")),
                int(facts.get("H2_PROMOTE_STEP", "-1")),
                int(facts.get("H2_WITHHELD", "0")),
                int(facts.get("H2_CAL_SCORE", "0")),
                v,
            ]
            lines.append(f"CTRL,cnoise,{','.join(str(x) for x in vals)}")
            cur_genome = ng
        ctrl_lines.append((name, lines))
    # C-honest: per variant, honest genome
    for vkey in VARIANTS:
        name = f"chonest_{vkey}"
        lines = []
        for rnd in range(1, 7):
            tag = f"{name}_{rnd}"
            cell, binp = bat.get_cell(vkey, GENOME_HONEST, DEFAULT_LP, tag)
            out = bat.run_learner(binp)
            facts = parse_h2_facts(out)
            v = 1 if facts.get("H2_VERDICT") == "KILLED" else 0
            vals = [rnd] + GENOME_HONEST + [
                int(facts.get("H2_F", "0")),
                int(facts.get("H2_NSHAM", "0")),
                int(facts.get("H2_NCOMMIT", "0")),
                int(facts.get("H2_NUNINSTALL", "0")),
                int(facts.get("H2_NPROMOTE", "0")),
                int(facts.get("H2_REVOKE_STEP", "-1")),
                int(facts.get("H2_BADEP", "0")),
                int(facts.get("H2_AUDIT_TOTAL", "0")),
                int(facts.get("H2_QUAR_USED", "0")),
                int(facts.get("H2_PROMOTE_STEP", "-1")),
                int(facts.get("H2_WITHHELD", "0")),
                int(facts.get("H2_CAL_SCORE", "0")),
                v,
            ]
            lines.append(f"CTRL,chonest,{','.join(str(x) for x in vals)}")
        ctrl_lines.append((name, lines))
    # C-max: per variant, max genome (honest-stated flood+fault)
    GENOME_MAX = [1,0,1,29,48,0,0,1]
    for vkey in VARIANTS:
        name = f"cmax_{vkey}"
        lines = []
        for rnd in range(1, 7):
            tag = f"{name}_{rnd}"
            cell, binp = bat.get_cell(vkey, GENOME_MAX, DEFAULT_LP, tag)
            out = bat.run_learner(binp)
            facts = parse_h2_facts(out)
            v = 1 if facts.get("H2_VERDICT") == "KILLED" else 0
            vals = [rnd] + GENOME_MAX + [
                int(facts.get("H2_F", "0")),
                int(facts.get("H2_NSHAM", "0")),
                int(facts.get("H2_NCOMMIT", "0")),
                int(facts.get("H2_NUNINSTALL", "0")),
                int(facts.get("H2_NPROMOTE", "0")),
                int(facts.get("H2_REVOKE_STEP", "-1")),
                int(facts.get("H2_BADEP", "0")),
                int(facts.get("H2_AUDIT_TOTAL", "0")),
                int(facts.get("H2_QUAR_USED", "0")),
                int(facts.get("H2_PROMOTE_STEP", "-1")),
                int(facts.get("H2_WITHHELD", "0")),
                int(facts.get("H2_CAL_SCORE", "0")),
                v,
            ]
            lines.append(f"CTRL,cmax,{','.join(str(x) for x in vals)}")
        ctrl_lines.append((name, lines))
    # Verify each with control.zag (pure Zag, KB-CTRL)
    results = {}
    for name, lines in ctrl_lines:
        inp = "\n".join(lines) + "\n"
        r = sh([bat.control_bin], input=inp)
        ok = ("CTRL_OK" in r.stdout)
        print(f"{name}: {'OK' if ok else 'FAIL'}", flush=True)
        if not ok:
            print(r.stdout, flush=True)
        results[name] = {"ok": ok, "output": r.stdout.strip()}
    # Save
    with open(os.path.join(out_dir, "meta_controls.json"), "w") as f:
        json.dump(results, f, indent=1)
    return results

if __name__ == "__main__":
    main()
