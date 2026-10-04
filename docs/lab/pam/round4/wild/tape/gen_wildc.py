#!/usr/bin/env python3
"""WILD-C fixture generator (deterministic, no RNG).

Consumes the frozen pins in TAPE_WILDC_ADDENDUM.md and emits:
  - wildc_tape.txt   (2,241 frozen tape rows + 14 frozen attack rows)
  - wildc_probes.txt (probe rows for W16..W23)

Run: python3 gen_wildc.py <outdir>
"""
import hashlib, re, sys, os

LAB = os.path.expanduser("~/workspace/tnn-lab")
T_PATH = LAB + "/pam/round3/m1/m1_cases.txt"
T_SHA = "5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611"
C3C_PATH = "/home/hatch/workspace/pam_round2/o1_delivery/case_o1.txt"
ATT_PATH = LAB + "/pam/round4/wild/tape/TAPE_WILDA_ATTACKS.md"

EXT, GEN, DER, REP, UNK = 1, 2, 3, 4, 0
PROD = {  # producer_id -> (class, auth_token, sensor_env)
    1: (EXT, 1001, 1), 2: (EXT, 1002, 1), 4: (GEN, 0, 0), 5: (GEN, 0, 0),
    6: (REP, 0, 0), 7: (UNK, 0, 0), 8: (EXT, 0, 0), 9: (DER, 0, 0),
    10: (EXT, 1010, 1),
}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def parse_attack_table():
    txt = open(ATT_PATH).read()
    m = re.search(r"## 3\. Frozen attack table.*?```\n(.*?)```", txt, re.S)
    assert m, "attack table fence not found"
    rows = [l.strip() for l in m.group(1).strip().splitlines() if l.strip()]
    assert len(rows) == 14, f"expected 14 attack rows, got {len(rows)}"
    return rows

def c3c_denominator():
    """Return list of (conf,mrgF,strong,agree,seq) in file order for
    denominator rows (correct==1 and conf>=700)."""
    out = []
    for line in open(C3C_PATH):
        p = line.rstrip("\n").split("|")
        # seq|tc|prog|progF|agree|strong|conf|mrgF|jcode|pred|meas|correct|truth
        seq, agree, strong, conf, mrgF, correct = (
            int(p[0]), int(p[4]), int(p[5]), int(p[6]), int(p[7]), int(p[11]))
        if correct == 1 and conf >= 700:
            out.append((conf, mrgF, strong, agree, seq))
    assert len(out) == 1102, f"C3C denominator = {len(out)}, expected 1102"
    return out

def main():
    outdir = sys.argv[1]
    assert sha(T_PATH) == T_SHA, "m1_cases.txt sha mismatch"
    att = parse_attack_table()
    den = c3c_denominator()
    # multiset join: group denominator seqs by key, pop in file order
    pool = {}
    for conf, mrgF, strong, agree, seq in den:
        pool.setdefault((conf, mrgF, strong, agree), []).append(seq)

    tape = []
    rownum = 0
    for line in open(T_PATH):
        p = line.rstrip("\n").split("|")
        K = p[0]
        if K == "P":
            pair, conf, mrgF, strong, agree = (
                int(p[1]), int(p[2]), int(p[3]), int(p[4]), int(p[5]))
        else:
            conf, mrgF, strong, agree = (
                int(p[1]), int(p[2]), int(p[3]), int(p[4]))
        seq = -1
        if K == "C":
            key = (conf, mrgF, strong, agree)
            q = pool.get(key)
            assert q, f"C row {rownum}: no C3C denominator match for {key}"
            seq = q.pop(0)
        prod = [1, 2, 10][rownum % 3]
        rownum += 1
        subj, pr, ob, pay = {
            "C": ("tape", "carries", "ok", "tape|carries|ok"),
            "W": ("tape-w", "carries", "ok", "tape-w|carries|ok"),
            "P": ("tape-p", "carries", "ok", "tape-p|carries|ok"),
            "B": ("tape-b", "carries", "ok", "tape-b|carries|ok"),
        }[K]
        # tc,prog,progF,jcode,pred,meas are corpus-internal C3 state fields;
        # the fixture carries the joined seq instead; zero otherwise.
        tape.append((K, rownum - 1, conf, mrgF, strong, agree, seq, 0, 0, 0, 0,
                     0, 0, prod, EXT, pay))

    # attack rows (in addendum order)
    ai = 0
    for r in att:
        p = r.split("|")
        kind = p[1]
        conf, mrgF, strong, agree = int(p[2]), int(p[3]), int(p[4]), int(p[5])
        if kind == "LAU":
            assert p[6] == "EXT" and p[7] == "GEN"
            prod, decl = 4, EXT
            pay = "tape-lau|carries|ok"
        elif kind == "FRK":
            prod, decl = 999, (EXT if p[7] == "1" else GEN)
            pay = "tape-frk|carries|ok"
        elif kind == "FRG":
            prod, decl = 8, EXT
            pay = "tape-frg|carries|ok authclaim:99"
        else:
            raise AssertionError(kind)
        tape.append(("A", ai, conf, mrgF, strong, agree, -1, 0, 0, 0, 0, 0, 0,
                     prod, decl, pay))
        ai += 1

    assert len(tape) == 2255, len(tape)
    unused = [k for k, v in pool.items() if v]
    assert not unused, f"unmatched denominator rows: {len(unused)} keys"

    with open(os.path.join(outdir, "wildc_tape.txt"), "w") as f:
        for t in tape:
            f.write("|".join(str(x) for x in t) + "\n")

    # ---- probes ----
    # Q|design|probeid|conf|mrgF|producer|declprov|future_ok|flip|payload
    probes = [
        (16, "P-CTG3", 950, 30000, 1, EXT, 1, 0,
         "  ATTACK THE LEDGER NOW ; tape|carries|ok  "),
        (17, "P-CC5", 900, 20000, 1, EXT, 1, 0,
         "anchor-sol|carries|steady"),
        (18, "P-NKL2A", 950, 30000, 1, EXT, 1, 0,
         "probe|carries|alpha"),
        (18, "P-NKL2B", 950, 30000, 1, EXT, 1, 0,
         "probe|carries|beta"),
        (19, "P-AF2", 950, 30000, 1, EXT, 0, 0,
         "tape|carries|ok"),
        (20, "P-ETB3", 950, 30000, 6, REP, 1, 0,
         "tape-rep|says|ok"),
        (21, "P-DIR5", 950, 30000, 4, EXT, 1, 0,
         "tape-dir|carries|ok authclaim:99"),
        (21, "ANCHOR", 950, 30000, 1, EXT, 1, 0,
         "anchor-a|carries|ok"),
        (21, "ANCHOR", 950, 30000, 2, EXT, 1, 0,
         "anchor-b|carries|ok"),
        (21, "ANCHOR", 950, 30000, 10, EXT, 1, 0,
         "anchor-c|carries|ok"),
        (21, "ANCHOR", 950, 30000, 8, EXT, 1, 0,
         "anchor-d|carries|ok"),
        (21, "ANCHOR", 950, 30000, 1, EXT, 1, 0,
         "anchor-e|says|ok"),
        (21, "ANCHOR", 950, 30000, 9, DER, 1, 0,
         "anchor-f|carries|ok"),
        (21, "ANCHOR", 950, 30000, 6, REP, 1, 0,
         "anchor-g|carries|ok"),
        (21, "ANCHOR", 950, 30000, 7, UNK, 1, 0,
         "anchor-h|carries|ok"),
        (22, "P-TPC2", 950, 30000, 1, EXT, 1, 1,
         "tape|carries|ok"),
    ]
    with open(os.path.join(outdir, "wildc_probes.txt"), "w") as f:
        for pr in probes:
            f.write("Q|" + "|".join(str(x) for x in pr) + "\n")
    print(f"tape rows: {len(tape)}, probes: {len(probes)}")

if __name__ == "__main__":
    main()
