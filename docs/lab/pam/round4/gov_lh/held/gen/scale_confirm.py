#!/usr/bin/env python3
# scale_confirm.py — 10x/100x confirmation (glue; all logic in Zag).
# Exact fixture repetition; 3 runs each; byte-identical check; rate stability vs 1x.
import hashlib, os, re, subprocess, sys

CREW = os.path.expanduser("~/workspace/pam_gov_lh/crew6_held")
SRC = os.path.join(CREW, "src")
GEN = os.path.join(CREW, "gen")
EV = os.path.join(CREW, "evidence")
BIN_BLOCK = os.path.join(SRC, "bin", "f5_sweep")
BIN_REPLAY = os.path.join(SRC, "bin", "f5_sweep_replay")
FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/f5_redteam300/fixtures_ledger.txt")
WH = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/v2/redteam/evidence/ledger_d_withhold.txt")
EX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/f5_tightened/exemplars.tsv")

WINDOWS = [(9, 15), (150, 245), (150, 500), (150, 1000), (150, 2000)]  # frontier + frozen anchor

def rep(src, dst, n):
    with open(src, "rb") as f:
        body = f.read()
    with open(dst, "wb") as f:
        for _ in range(n):
            f.write(body)
    h = hashlib.sha256()
    for _ in range(1):
        h = hashlib.sha256()
    with open(dst, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return dst, h.hexdigest()

def run3(bin_, args):
    digs, outs = [], []
    for _ in range(3):
        p = subprocess.run([bin_] + args, capture_output=True)
        if p.returncode != 0:
            raise RuntimeError(f"rc={p.returncode} stderr={p.stderr[:200]!r}")
        outs.append(p.stdout)
        digs.append(hashlib.sha256(p.stdout).hexdigest())
    if not (digs[0] == digs[1] == digs[2]):
        raise RuntimeError(f"NON-DETERMINISTIC: {args} {digs}")
    return outs[0], digs[0]

def main():
    os.makedirs(GEN, exist_ok=True)
    paths = {}
    for name, src, n in [("block_10x", FIX, 10), ("block_100x", FIX, 100),
                         ("replay_10x", WH, 10), ("replay_100x", WH, 100)]:
        dst = os.path.join(GEN, f"f5_{name}.txt")
        _, d = rep(src, dst, n)
        paths[name] = (dst, d)
        print(f"built {dst} sha={d[:16]}...")
    dig = []
    rows = []
    for rc, rm in WINDOWS:
        for tag, scale in [("10x", 10), ("100x", 100)]:
            bpath = paths[f"block_{tag}"][0]
            rpath = paths[f"replay_{tag}"][0]
            out, d1 = run3(BIN_BLOCK, [bpath, EX, str(rc), str(rm)])
            t = out.decode()
            mb = re.search(r"NEAR n=(\d+) blocked=(\d+)", t)
            mf = re.search(r"\nFAR n=(\d+) blocked=(\d+)", t)
            rout, d2 = run3(BIN_REPLAY, [rpath, EX, str(rc), str(rm)])
            rt = rout.decode()
            mr = re.search(r"SUMMARY false_blocked=(\d+)/(\d+) true_within=(\d+)/(\d+)", rt)
            n_near, b_near = int(mb.group(1)), int(mb.group(2))
            n_far, b_far = int(mf.group(1)), int(mf.group(2))
            bf, nf = int(mr.group(1)), int(mr.group(2))
            wt, nt = int(mr.group(3)), int(mr.group(4))
            rows.append((rc, rm, tag, n_near, b_near, n_far, b_far, bf, nf, wt, nt))
            dig.append(f"rc={rc} rm={rm} {tag} block={d1} replay={d2}")
            print(f"rc={rc:3d} rm={rm:4d} {tag}: near {b_near}/{n_near} far {b_far}/{n_far} ret {bf}/{nf} true {wt}/{nt}")
    # 1x baselines for rate comparison
    base = {}
    with open(os.path.join(EV, "sweep_table.tsv")) as f:
        f.readline()
        for line in f:
            p = line.strip().split("\t")
            base[(int(p[0]), int(p[1]))] = (int(p[2]), int(p[4]), int(p[6]), int(p[8]))
    with open(os.path.join(EV, "scale_confirm.tsv"), "w") as f:
        f.write("rc\trm\tscale\tnear_n\tnear_blocked\tfar_n\tfar_blocked\tcand_n\tfalse_blocked\ttrue_blocked\tret_rate_eq_1x\tover_rate_eq_1x\n")
        for rc, rm, tag, nn, bn, nf_, bf_, bfc, nfc, wt, nt in rows:
            s = scale = 10 if tag == "10x" else 100
            bb, bf1, ret1, tb1 = base[(rc, rm)]
            ret_ok = (bfc / nfc == ret1 / 9)
            over_ok = (bn / nn == bb / 300)
            f.write(f"{rc}\t{rm}\t{tag}\t{nn}\t{bn}\t{nf_}\t{bf_}\t{nfc}\t{bfc}\t{wt}\t{int(ret_ok)}\t{int(over_ok)}\n")
    with open(os.path.join(EV, "scale_digests.txt"), "w") as f:
        f.write("Scale fixtures:\n")
        for name in ["block_10x", "block_100x", "replay_10x", "replay_100x"]:
            f.write(f"  {name}: sha256={paths[name][1]}\n")
        f.write("Run digests (3/3 byte-identical each):\n" + "\n".join(dig) + "\n")
    print("wrote evidence/scale_confirm.tsv + scale_digests.txt")

if __name__ == "__main__":
    main()
