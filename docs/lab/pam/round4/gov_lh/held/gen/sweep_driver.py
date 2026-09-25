#!/usr/bin/env python3
# sweep_driver.py — Leg B 35-window sweep driver (glue only; all logic in Zag).
# Verifies fixture SHAs, runs each window 3x, checks byte-identical output,
# scrapes the 35-window metric table.
import hashlib, itertools, os, re, subprocess, sys

CREW = os.path.expanduser("~/workspace/pam_gov_lh/crew6_held")
SRC = os.path.join(CREW, "src")
GEN = os.path.join(CREW, "gen")
EV = os.path.join(CREW, "evidence")
BIN_BLOCK = os.path.join(SRC, "bin", "f5_sweep")
BIN_REPLAY = os.path.join(SRC, "bin", "f5_sweep_replay")
FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/f5_redteam300/fixtures_ledger.txt")
WH = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/v2/redteam/evidence/ledger_d_withhold.txt")
EX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/f5_tightened/exemplars.tsv")

PINS = {
    FIX: "0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0",
    WH: "63ea591d8cbb9d8b3e1cd088364e96d8fdfa19d435e337dfac0ad17a0326c2b1",
    EX: "13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e",
}

RC = [9, 25, 46, 80, 150]
RM = [15, 53, 100, 245, 500, 1000, 2000]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()

def run3(bin_, args):
    outs, digs = [], []
    for _ in range(3):
        p = subprocess.run([bin_] + args, capture_output=True)
        if p.returncode != 0:
            raise RuntimeError(f"binary rc={p.returncode} stderr={p.stderr[:200]!r} args={args}")
        outs.append(p.stdout)
        digs.append(sha_bytes(p.stdout))
    if not (digs[0] == digs[1] == digs[2]):
        raise RuntimeError(f"NON-DETERMINISTIC output for args={args}: {digs}")
    return outs[0], digs[0]

def scrape_block(out):
    t = out.decode()
    m = re.search(r"NEAR n=(\d+) blocked=(\d+)", t)
    n_near, b_near = int(m.group(1)), int(m.group(2))
    m = re.search(r"\nFAR n=(\d+) blocked=(\d+)", t)
    n_far, b_far = int(m.group(1)), int(m.group(2))
    return n_near, b_near, n_far, b_far

def scrape_replay(out):
    t = out.decode()
    m = re.search(r"SUMMARY false_blocked=(\d+)/(\d+) true_within=(\d+)/(\d+)", t)
    bf, nf, wt, nt = (int(m.group(i)) for i in range(1, 5))
    return bf, nf, wt, nt

def main():
    os.makedirs(EV, exist_ok=True)
    os.makedirs(GEN, exist_ok=True)
    for p, pin in PINS.items():
        got = sha(p)
        if got != pin:
            raise SystemExit(f"SHA MISMATCH on {p}: got {got}, want {pin}")
        print(f"SHA ok: {os.path.basename(p)}")
    rows = []
    dig_lines = []
    for rc, rm in itertools.product(RC, RM):
        out, d = run3(BIN_BLOCK, [FIX, EX, str(rc), str(rm)])
        n_near, b_near, n_far, b_far = scrape_block(out)
        rout, rd = run3(BIN_REPLAY, [WH, EX, str(rc), str(rm)])
        bf, nf, wt, nt = scrape_replay(rout)
        assert n_near == 300 and n_far == 60, (rc, rm, n_near, n_far)
        assert nf == 9 and nt == 34, (rc, rm, nf, nt)
        rows.append((rc, rm, b_near, b_far, bf, wt))
        dig_lines.append(f"rc={rc} rm={rm} block_digest={d} replay_digest={rd}")
        print(f"rc={rc:3d} rm={rm:4d} near_blocked={b_near:3d}/300 far={b_far}/60 retention={bf}/9 true_blocked={wt}/34")
    with open(os.path.join(EV, "sweep_table.tsv"), "w") as f:
        f.write("rc\trm\tnear_blocked\tnear_n\tfar_blocked\tfar_n\tfalse_retention\tfalse_n\ttrue_blocked\ttrue_n\n")
        for r in rows:
            f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t300\t{r[3]}\t60\t{r[4]}\t9\t{r[5]}\t34\n")
    with open(os.path.join(EV, "sweep_digests.txt"), "w") as f:
        f.write("35-window sweep digests. Each line: rc, rm, sha256 of stdout for the block run (3/3 byte-identical) and replay run (3/3 byte-identical).\n")
        f.write("\n".join(dig_lines) + "\n")
    print("wrote evidence/sweep_table.tsv + sweep_digests.txt")

if __name__ == "__main__":
    main()
