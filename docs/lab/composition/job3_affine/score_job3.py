#!/usr/bin/env python3
"""score_job3.py — deterministic bar-checker for the Job-3 affine-memorizer test.
Parses affine_test mode outputs, asserts the preregistered (PREREG_JOB3.md section 7)
exact signatures, evaluates K-J3-1..K-J3-3, and writes SCORES_JOB3.md. No RNG.
Usage: score_job3.py <rundir> <outdir>
"""
import sys, os

RUNDIR, OUTDIR = sys.argv[1], sys.argv[2]
os.makedirs(OUTDIR, exist_ok=True)

P0IDX = [100,101,102,103,105,106,107,109,110,111,113,114,115,117,118,119,120,121,
         122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,
         140,141,142,143,144,145,146,147,148,149,150,151]
LEN2 = {i for i in P0IDX if (2 + i % 4) == 2}

def parse(path):
    p0 = {}; p2 = {}; p3 = {}; gates = {}; sums = {}
    for line in open(path):
        t = line.split()
        if not t: continue
        if t[0] == 'P0':
            _, r, idx, ok, exp, got = t
            p0[(int(r), int(idx))] = (ok == '1', exp, got)
        elif t[0] == 'P2':
            _, a, b, idx, ok, exp, got = t
            p2[(int(a), int(b), int(idx))] = (ok == '1', exp, got)
        elif t[0] == 'P3':
            _, idx, ok, exp, got = t
            p3[int(idx)] = (ok == '1', exp, got)
        elif t[0] == 'GATE':
            gates[t[1]] = int(t[2])
        elif t[0] == 'SUM':
            sums[t[1]] = t[2]
    return p0, p2, p3, gates, sums

def check(name, cond, notes, detail=""):
    notes.append(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    return cond

def main():
    notes = []
    ok_all = True
    D = {}
    for m in ['genA','genB','genC','memA','memB','memC']:
        D[m] = parse(os.path.join(RUNDIR, m + '.out'))

    # ---- gates ----
    for m in D:
        _, _, _, g, _ = D[m]
        ok_all &= check(f"{m} G1==0", g['G1'] == 0, notes)
        ok_all &= check(f"{m} G3==1", g['G3'] == 1, notes)
    for m, exp_g2 in [('genA', 360), ('memA', 360), ('genB', 0), ('memB', 0),
                      ('genC', 0), ('memC', 0)]:
        _, _, _, g, _ = D[m]
        ok_all &= check(f"{m} G2p=={exp_g2}", g['G2p'] == exp_g2, notes,
                        f"got {g['G2p']}")

    # ---- genuine combiner: salt-invariant perfect (K-J3-3) ----
    for m in ['genA','genB','genC']:
        p0, p2, p3, _, s = D[m]
        ok_all &= check(f"{m} P0 48/48", s['P0'] == '48/48', notes)
        ok_all &= check(f"{m} P2 120/120", s['P2'] == '120/120', notes)
        ok_all &= check(f"{m} P3 8/8", s['P3'] == '8/8', notes)

    # ---- memA fidelity: P0 == [0,0,0,8,8,0] (K-J3-2) ----
    p0, p2, p3, _, s = D['memA']
    per_rule = [sum(1 for j in range(8) if p0[(r, P0IDX[r*8+j])][0]) for r in range(6)]
    ok_all &= check("memA P0==[0,0,0,8,8,0]", per_rule == [0,0,0,8,8,0], notes,
                    f"got {per_rule}")
    ok_all &= check("memA P0 total 16/48", s['P0'] == '16/48', notes)
    # memA P2: (3,4)=3/4 on lengths 3,4,5; accidents idx312 (5,3), idx316 (5,4); else 0
    hits34 = [idx for (a,b,idx), (ok,_,_) in p2.items() if a==3 and b==4 and ok]
    acc = [(a,b,idx) for (a,b,idx), (ok,_,_) in p2.items()
           if ok and not (a==3 and b==4)]
    lens34 = sorted(2 + i % 4 for i in hits34)
    ok_all &= check("memA (3,4)==3/4 on lengths {3,4,5}",
                    sorted(hits34) == [i for i in hits34] and lens34 == [3,4,5],
                    notes, f"hit idx {sorted(hits34)} lens {lens34}")
    ok_all &= check("memA (4,3)==0/4",
                    not any(ok for (a,b,idx),(ok,_,_) in p2.items() if a==4 and b==3),
                    notes)
    ok_all &= check("memA P2 accidents exactly {(5,3,312),(5,4,316)}",
                    sorted(acc) == [(5,3,312),(5,4,316)], notes, f"got {sorted(acc)}")
    ok_all &= check("memA P2 total 5/120", s['P2'] == '5/120', notes)
    ok_all &= check("memA P3 0/8", s['P3'] == '0/8', notes)

    # ---- memB/memC discrimination (K-J3-1) ----
    for m in ['memB','memC']:
        p0, p2, p3, _, s = D[m]
        per_rule = [sum(1 for j in range(8) if p0[(r, P0IDX[r*8+j])][0]) for r in range(6)]
        ok_all &= check(f"{m} P0==[0,0,0,2,2,0]", per_rule == [0,0,0,2,2,0], notes,
                        f"got {per_rule}")
        hit_idx = {r: [idx for j in range(8) for idx in [P0IDX[r*8+j]]
                       if p0[(r,idx)][0]] for r in range(6)}
        vac_exact = (set(hit_idx[3]) | set(hit_idx[4])) <= LEN2 and \
                    not hit_idx[0] and not hit_idx[1] and not hit_idx[2] and not hit_idx[5]
        ok_all &= check(f"{m} P0 hits exactly length-2 probes of rules 3,4",
                        vac_exact, notes, f"hits {hit_idx}")
        acc = [(a,b,idx) for (a,b,idx), (ok,_,_) in p2.items() if ok]
        ok_all &= check(f"{m} P2 accidents exactly {(5,3,312),(5,4,316)}",
                        sorted(acc) == [(5,3,312),(5,4,316)], notes, f"got {sorted(acc)}")
        ok_all &= check(f"{m} P2 total 2/120", s['P2'] == '2/120', notes)
        miss3 = sorted(idx for idx, (ok,_,_) in p3.items() if not ok)
        ok_all &= check(f"{m} P3==6/8, misses exactly [400,404] (length-2 vacuous)",
                        s['P3'] == '6/8' and miss3 == [400,404], notes,
                        f"got {s['P3']}, misses {miss3}")

    report = ["# Job-3 bar-check results (score_job3.py, deterministic)",
              "", f"rundir: {RUNDIR}", "", *notes, "",
              f"OVERALL: {'ALL CHECKS PASS' if ok_all else 'FAILURES PRESENT'}", ""]
    open(os.path.join(OUTDIR, 'SCORES_JOB3.md'), 'w').write("\n".join(report))
    print("\n".join(notes))
    print("OVERALL:", "ALL CHECKS PASS" if ok_all else "FAILURES PRESENT")
    sys.exit(0 if ok_all else 1)

main()
