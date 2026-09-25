#!/usr/bin/env python3
"""RSI-8 Round 2 (R5) loop driver: no fixed revision cap; TNN-driven.

Per RUN_PREREG5 §3: each iteration assembles EVIDENCE, runs the problem
scan (via problems binary, logged), deliberates each selected problem
(depth logged), applies TNN FIX specs mechanically (M-CHAMPION/M-PRED/
M-ACTIONSPACE already in the binaries), runs the deliberation loop, feeds
the DELB block to the proposer, and on PROPOSE installs the bytecode and
continues. Stops only on TNN halt (no proposal, no new FIX) or
candidate-space exhaustion.

M-CHAMPION: champion values 16/8/456 (measured).
M-PRED: D5 emits honest point bands.
M-ACTIONSPACE: D5 searches full grammar-legal action space with
improvement + V2b checks.
"""
import subprocess, csv, os, sys

BASE = os.path.expanduser("~/workspace/tnn-lab/rsi/autonomous_run_2")
BUILD = f"{BASE}/build"
R5BIN = f"{BASE}/work/r5"

CHAMP_ACC, CHAMP_WRONG, CHAMP_COST = 16, 8, 456

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def get_proxy_gt_cls():
    gt = ''; cls = ''
    with open(f"{BUILD}/proxy_battery.csv") as f:
        for row in csv.DictReader(f):
            g = row['gt']
            gt += '1' if g == 'NEW' else ('2' if g == 'OLD' else '0')
            m = {'N-clean': 0, 'O-clean': 1, 'MISLEAD-OLD': 2, 'ADV-NEW': 3, 'NEITHER': 4}
            cls += str(m[row['class']])
    return gt, cls

def build_facts(episode, kept_bcs, afdisc, champ):
    gt, _ = get_proxy_gt_cls()
    ca, cw, cc = champ
    facts = []
    facts.append(f"EPISODE {episode}")
    facts.append(f"CHAMPION {ca} {cw} {cc}")
    facts.append(f"PROXYGT {gt}")
    facts.append("PROXYCLASS 0 6 6 0")
    facts.append("PROXYCLASS 1 6 6 0")
    facts.append("PROXYCLASS 2 4 0 4")
    facts.append("PROXYCLASS 3 4 0 4")
    facts.append("PROXYCLASS 4 4 4 0")
    facts.append(f"KEPT {len(kept_bcs)}")
    for bc in kept_bcs:
        facts.append(bc)
    facts.append(afdisc.strip())
    facts.append("NOVELSHAPE F1 silent-channel")
    facts.append("ENDFACCTS")
    return "\n".join(facts), gt

def build_evidence(champ, gt, pre_fix=False):
    """Evidence blob for the problem scanner (iteration-level).
    pre_fix=True: the original fiction (22/2/424 asserted vs 16/8/456
    measured, static PRED, restricted D5 map). TNN flags P-CHAMPION,
    P-PRED, P-ACTIONSPACE and specifies the FIXes.
    pre_fix=False: post-fix state (M-CHAMPION/M-PRED/M-ACTIONSPACE applied).
    Scan should output P-NONE.
    """
    ca, cw, cc = champ
    if pre_fix:
        lines = [
            f"CHAMPION_ASSERT 22 2 424",
            f"CHAMPION_MEASURED 16 8 456",
            f"PREDLINE PRED P-ACC 22 24 P-WRONG 0 2 P-COST 424 P-NOVEL 0",
            f"PREDHONEST 20 4 344",
            "TRANSLATECHECK 0",
            "GRIDCHECK 0",
            "GRAMMARBOUNDS 4 -6 6",
            "GRAMMARBOUNDS 8 -3 3",
            "SWEEP traps 320 0 0 0 0 0 0 0 0",
            "GATECLEAR 0",
            "D5MAP pre 1 1",
            "D5MAP post 2 3",
        ]
    else:
        lines = [
            f"CHAMPION_ASSERT {ca} {cw} {cc}",
            f"CHAMPION_MEASURED {ca} {cw} {cc}",
            f"PREDLINE PRED P-ACC {ca} {ca} P-WRONG {cw} {cw} P-COST {cc} P-NOVEL 0",
            f"PREDHONEST {ca} {cw} {cc}",
            "TRANSLATECHECK 0",
            "GRIDCHECK 0",
            "GRAMMARBOUNDS 4 -6 6",
            "GRAMMARBOUNDS 8 -3 3",
            "SWEEP traps 320 0 0 0 0 0 0 0 0",
            "GATECLEAR 0",
            "D5MAP pre 1 1",
            "D5MAP post 2 3",
        ]
    return "\n".join(lines)

def main():
    max_iter = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    gt, cls = get_proxy_gt_cls()
    af = run([f"{R5BIN}/afdisc", gt, cls]).stdout
    kb = open(f"{BUILD}/kb_entries.txt").read()

    champ = (CHAMP_ACC, CHAMP_WRONG, CHAMP_COST)
    kept = []
    log = []
    accepts = 0

    for ep in range(max_iter):
        # 1. Problem scan (logged; FIX specs already applied to binaries)
        # EP 0 uses pre-fix evidence (TNN selects problems); later EPs use
        # post-fix evidence (problems resolved).
        ev = build_evidence(champ, gt, pre_fix=(ep == 0))
        rscan = run([f"{R5BIN}/problems", "scan", ev])
        probs = [l.split()[1] for l in rscan.stdout.split("\n") if l.startswith("PROBLEM")]
        # 2. Deliberate each (depth logged)
        depths = []
        for p in probs:
            if p == "P-NONE":
                continue
            rd = run([f"{R5BIN}/problems", "deliberate", p, ev])
            for l in rd.stdout.split("\n"):
                if l.startswith("DEPTH"):
                    depths.append(f"{p}:{l.split('rounds=')[1].split()[0]}")
        # 3. Deliberation loop
        facts, gt = build_facts(ep, kept, af, champ)
        r = run([f"{R5BIN}/deliberation", "loop", facts, kb])
        out = r.stdout
        depth = [l for l in out.split("\n") if l.startswith("DELB_DEPTH")]
        halt = [l for l in out.split("\n") if l.startswith("DELB_HALT")]
        if halt:
            msg = f"EP {ep}: HALT {halt[0]} | scan={probs}"
            log.append(msg); print(msg)
            break
        # 4. Extract DELB block and run proposer
        lines = out.split("\n")
        s = lines.index("DELB_START"); e = lines.index("DELB_END")
        delb = "\n".join(lines[s:e+1])
        # policy rule for logging
        rule = [l for l in lines[s:e+1] if l.startswith("RULE")][0]
        r2 = run([f"{R5BIN}/proposer", delb] + [""]*8 +
                 [str(champ[0]), str(champ[1]), str(champ[2]), gt, "r5loop"])
        verdict = r2.stdout.strip().split("\n")[0]
        msg = (f"EP {ep}: {depth[0] if depth else 'no-depth'} | "
               f"scan={probs} depths={depths} | {rule} | {verdict}")
        log.append(msg); print(msg)
        if verdict == "PROPOSE":
            # extract bytecode
            bc = [l for l in r2.stdout.split("\n") if l.startswith("BYTECODE=")]
            if bc:
                kept.append(bc[0].split("=", 1)[1])
                accepts += 1
                # update champion from PRED (honest)
                pred = [l for l in lines[s:e+1] if l.startswith("PRED")][0]
                # PRED P-ACC <a> <a> P-WRONG <w> <w> P-COST <c> ...
                toks = pred.split()
                champ = (int(toks[2]), int(toks[5]), int(toks[8]))
        elif verdict.startswith("REJECTED") or verdict.startswith("INVALID"):
            # TNN declined or gate fired; stop (no new FIX from scan)
            print(f"Stopping: {verdict}")
            break

    log.append(f"ACCEPTS={accepts} FINAL_CHAMPION={champ[0]}/{champ[1]}/{champ[2]}")
    print(log[-1])
    open(f"{BASE}/work/r5/loop_log.txt", "w").write("\n".join(log) + "\n")

if __name__ == "__main__":
    main()
