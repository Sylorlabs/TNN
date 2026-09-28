#!/usr/bin/env python3
"""Train-LOO driver for native-deliberation epistemics Phase 1.

For each claim i in 0..447:
  1. Build Zag input file (constructions, candidates, pair features, second-order).
  2. Run epistemic_bin.
  3. Extract VERDICT (opaque ID).

Outputs: verdicts.tsv (claim_idx, verdict_id). No labels are read.
Deterministic: same inputs -> byte-identical outputs.
"""
import csv, subprocess, sys, os, hashlib

TRAIN = "/home/hatch/workspace/epi_a3/blind/train_blind.tsv"
SENS = "/home/hatch/workspace/epistemic_native/impl/zagwork/sensout"
BIN = "/home/hatch/workspace/epistemic_native/impl/zagwork/epistemic_bin"
WORK = "/home/hatch/workspace/epistemic_native/impl/zagwork/loowork"

VERDICT_IDS = {"FACT": "V1", "OPINION": "V2", "LIE": "V3", "UNDETERMINED": "V4"}

def id_to_ord(s):
    # 'T0001' -> 0
    return int(s[1:]) - 1

def load_constructions():
    cons = {}
    with open(os.path.join(SENS, "mass.tsv")) as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            cons[id_to_ord(row["id"])] = (
                int(row["fpexp"]), int(row["deon"]), int(row["cmp"]),
            )
    return cons

def load_pairs():
    # qid -> list of (cid, ov, neg, num, ent), sorted by ov desc
    pairs = {}
    with open(os.path.join(SENS, "pairs.tsv")) as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            q = id_to_ord(row["qid"])
            c = id_to_ord(row["cid"])
            tup = (c, int(row["ov"]), int(row["neg"]),
                   int(row["num"]), int(row["ent"]))
            pairs.setdefault(q, []).append(tup)
    for q in pairs:
        pairs[q].sort(key=lambda t: -t[1])
    return pairs

def load_texts():
    texts = {}
    with open(TRAIN, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0: continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                texts[i-1] = parts[1]
    return texts

def build_input(i, cons, pairs, texts, path):
    """Build Zag input file for claim i (LOO: exclude i from mass)."""
    fpexp, deon, cmp_ = cons[i]
    # candidates: top-8 from pairs[i], excluding i
    cands = [(c, ov, neg, num, ent) for (c, ov, neg, num, ent) in pairs.get(i, [])
             if c != i][:8]
    # overlap-track constructions for each candidate
    ot = [cons[c] for (c, _, _, _, _) in cands]
    ot_fpexp = 1 if any(x[0] == 1 for x in ot) else 0
    ot_deon = 1 if any(x[1] == 1 for x in ot) else 0
    ot_cmp = 1 if any(x[2] == 1 for x in ot) else 0

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{i}\n")
        f.write(f"{fpexp} {deon} {cmp_}\n")
        f.write(f"{ot_fpexp} {ot_deon} {ot_cmp}\n")
        f.write(f"{len(cands)}\n")
        for (c, ov, neg, num, ent) in cands:
            f.write(f"{c} {ov} {neg} {num} {ent}\n")
        # second-order blocks
        for (c, ov, neg, num, ent) in cands:
            # pairs where c is query, excluding i
            c2 = [(cc, o2, n2, u2, e2) for (cc, o2, n2, u2, e2) in pairs.get(c, [])
                  if cc != i][:8]
            f.write(f"{len(c2)}\n")
            for (cc, o2, n2_, u2, e2) in c2:
                f.write(f"{cc} {o2} {n2_} {u2} {e2}\n")
        # candidate texts
        for (c, ov, neg, num, ent) in cands:
            # text on single line (strip newlines/tabs)
            t = texts[c].replace("\n", " ").replace("\r", " ").replace("\t", " ")
            f.write(t + "\n")
        # claim text
        t = texts[i].replace("\n", " ").replace("\r", " ").replace("\t", " ")
        f.write(t + "\n")

def run_loo(out_path):
    cons = load_constructions()
    pairs = load_pairs()
    texts = load_texts()
    os.makedirs(WORK, exist_ok=True)

    results = []
    for i in range(448):
        inp = os.path.join(WORK, f"in_{i}.txt")
        build_input(i, cons, pairs, texts, inp)
        proc = subprocess.run([BIN, inp], capture_output=True, text=True, timeout=30)
        out = proc.stdout
        # extract VERDICT line
        verdict = None
        for line in out.split("\n"):
            if line.startswith("VERDICT "):
                verdict = line[8:].strip()
                break
        if verdict not in VERDICT_IDS:
            print(f"ERROR: claim {i}: bad verdict '{verdict}'", file=sys.stderr)
            print(out[-2000:], file=sys.stderr)
            sys.exit(1)
        results.append((i, VERDICT_IDS[verdict]))
        if (i+1) % 50 == 0:
            print(f"  {i+1}/448", file=sys.stderr)

    with open(out_path, "w") as f:
        f.write("claim_idx\tverdict_id\n")
        for i, v in results:
            f.write(f"{i}\t{v}\n")

    # hash
    h = hashlib.sha256()
    with open(out_path, "rb") as f:
        h.update(f.read())
    print(f"SHA256({out_path}) = {h.hexdigest()}")
    # distribution (opaque IDs only)
    from collections import Counter
    dist = Counter(v for _, v in results)
    print(f"Distribution: {dict(dist)}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORK, "verdicts.tsv")
    run_loo(out)
