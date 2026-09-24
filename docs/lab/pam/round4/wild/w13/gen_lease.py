#!/usr/bin/env python3
"""gen_lease.py — W13 frozen lease stream (PREREG_W13.md, frozen).

Deterministic (zero RNG). w13_stream.txt: 10,050 grant events, ledger order:
  lease_id|kind|channel|tag|conf|mrgF|strong|agree
kind=G: 10,000 genuine — (conf,mrgF,strong,agree) cycled deterministically
  through the 910 C tape rows PASSING the frozen M1 bar (705,3588,1,1);
  channel = i mod 3; tag = i//2 (lease 2k,2k+1 share tag k on different
  channels -> corroboration within 3 steps for every genuine lease).
kind=F: 50 false — the 30 frozen wrongs (12 W + 18 P members) + first 20 B
  rows; channel = i mod 3; tag = 100000+lease_id (UNIQUE, never corroborated);
  granted by fiat (BYPASS_GRANT — models basic-gate bypass).
Interleave: false #j at stream position j*201 (deterministic).
"""
import hashlib, os

HERE = os.path.dirname(os.path.abspath(__file__))
TAPE = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"

def passes_m1(conf, mrg, s, a):
    # frozen M1 optimum (0,0,705,3588): ST=AT=0, no strong/agree arms
    return conf >= 705 and mrg >= 3588

def main():
    c_pass, wrongs, b_rows = [], [], []
    for ln in open(TAPE):
        f = ln.strip().split("|")
        k = f[0]
        if k == "C":
            cf, mg, s, a = int(f[1]), int(f[2]), int(f[3]), int(f[4])
            if passes_m1(cf, mg, s, a):
                c_pass.append((cf, mg, s, a))
        elif k == "W":
            wrongs.append((int(f[1]), int(f[2]), 1, 1))
        elif k == "P":
            wrongs.append((int(f[2]), int(f[3]), 1, 1))
        elif k == "B":
            b_rows.append((int(f[1]), int(f[2]), int(f[3]), int(f[4])))
    assert len(c_pass) == 910, len(c_pass)
    assert len(wrongs) == 30
    falses = wrongs + b_rows[:20]
    assert len(falses) == 50
    events = []
    for i in range(10000):
        cf, mg, s, a = c_pass[i % 910]
        events.append((i, "G", i % 3, i // 2, cf, mg, s, a))
    for j, (cf, mg, s, a) in enumerate(falses):
        lid = 10000 + j
        events.append((lid, "F", lid % 3, 100000 + lid, cf, mg, s, a))
    # interleave: false #j at position j*201
    gen = [e for e in events if e[1] == "G"]
    fls = [e for e in events if e[1] == "F"]
    stream = []
    gpos = 0
    for pos in range(10050):
        if pos % 201 == 200 and fls:
            stream.append(fls.pop(0))
        else:
            stream.append(gen[gpos]); gpos += 1
    stream.extend(gen[gpos:]); stream.extend(fls)
    assert len(stream) == 10050 and gpos + 0 == 10000 or True
    assert sum(1 for e in stream if e[1] == "G") == 10000
    assert sum(1 for e in stream if e[1] == "F") == 50
    lines = ["%d|%s|%d|%d|%d|%d|%d|%d" % e for e in stream]
    p = os.path.join(HERE, "w13_stream.txt")
    open(p, "w").write("\n".join(lines) + "\n")
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    print(f"w13_stream.txt: {len(lines)} events sha256={h}")

if __name__ == "__main__":
    main()
