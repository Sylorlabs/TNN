#!/usr/bin/env python3
"""Parse CLN-1 judge raw files, join with sealed mapping, compute tables a/b/c."""
import json, os, re

BASE = os.path.expanduser("~/workspace/tnn-lab/coding/reflection/cleanliness")
WORK = os.path.join(BASE, "work")

LINE = re.compile(
    r"^(W|X|Y|Z)\s*:\s*T1\s*=\s*([0-2])\s+T2\s*=\s*([0-2])\s+T3\s*=\s*([0-2])\s+T4\s*=\s*([0-2])\s+AUTHOR\s*=\s*(human programmer|TNN AI coding agent|LLM assistant A|LLM assistant B)\s*$",
    re.IGNORECASE)

AUTHORS = ["human programmer", "TNN AI coding agent", "LLM assistant A", "LLM assistant B"]
ARMS = ["human", "tnn", "sol", "grok"]
ARM_AUTHOR = {"human": "human programmer", "tnn": "TNN AI coding agent",
              "sol": "LLM assistant A", "grok": "LLM assistant B"}

def norm_author(a):
    a = a.strip().lower()
    for x in AUTHORS:
        if a == x.lower():
            return x
    return None

def parse_file(path):
    """Use the last parseable full 4-label block in the file (after a retry)."""
    text = open(path).read()
    blocks = text.split("===== RETRY (format reminder) =====")
    best = None
    for block in blocks:
        got = {}
        for line in block.strip().splitlines():
            m = LINE.match(line.strip())
            if m:
                got[m.group(1).upper()] = {
                    "scores": tuple(int(m.group(i)) for i in range(2, 6)),
                    "author": norm_author(m.group(6))}
        if set(got) == {"W", "X", "Y", "Z"}:
            best = got
    return best

def main():
    mapping = json.load(open(os.path.join(WORK, "SEALED_MAPPING.json")))
    specs = mapping["specs"]
    m = mapping["mapping"]

    # parsed[judge][spec][label] = (scores tuple, author)
    parsed, missing = {}, []
    for judge in ("sol", "grok"):
        parsed[judge] = {}
        for spec in specs:
            path = os.path.join(WORK, "judge_raw", judge, spec + ".txt")
            got = parse_file(path) if os.path.exists(path) else None
            if got is None:
                missing.append((judge, spec))
            parsed[judge][spec] = got

    n_sol = sum(1 for s in specs if parsed["sol"][s])
    n_grok = sum(1 for s in specs if parsed["grok"][s])
    print(f"parseable responses: sol {n_sol}/14, grok {n_grok}/14, missing {len(missing)}")
    for j, s in missing:
        print(f"  MISSING: {j}/{s}")

    # (a) per judge, per arm, per dimension mean
    def table(judges):
        agg = {(arm, d): [] for arm in ARMS for d in range(4)}
        for judge in judges:
            for spec in specs:
                got = parsed[judge][spec]
                if not got:
                    continue
                for label in "WXYZ":
                    arm = m[spec][label]
                    for d in range(4):
                        agg[(arm, d)].append(got[label]["scores"][d])
        return {k: (sum(v) / len(v) if v else None) for k, v in agg.items()}

    ta, tb = table(["sol"]), table(["grok"])
    tc = table(["sol", "grok"])

    def show(t, title):
        print(f"\n=== {title} ===")
        hdr = "arm   " + " ".join(f"T{i+1}" for i in range(4))
        print(hdr)
        for arm in ARMS:
            row = " ".join(f"{t[(arm, d)]:.2f}" if t[(arm, d)] is not None else "NA"
                           for d in range(4))
            print(f"{arm:6s} {row}")

    show(ta, "Table (a) sol means (arm x dimension)")
    show(tb, "Table (a) grok means (arm x dimension)")
    show(tc, "Table (b) combined means (arm x dimension)")

    # (c) confusion matrices rows=true arm, cols=guessed author
    def confusion(judges):
        cm = {(arm, auth): 0 for arm in ARMS for auth in AUTHORS}
        tot = {arm: 0 for arm in ARMS}
        for judge in judges:
            for spec in specs:
                got = parsed[judge][spec]
                if not got:
                    continue
                for label in "WXYZ":
                    arm = m[spec][label]
                    auth = got[label]["author"]
                    if auth:
                        cm[(arm, auth)] += 1
                    tot[arm] += 1
        return cm, tot

    def show_cm(cm, tot, title):
        print(f"\n=== {title} (rows=true arm, cols=guessed author; counts) ===")
        print("true\\guessed  human   TNN     LLM-A   LLM-B   n")
        short = {"human programmer": "human", "TNN AI coding agent": "TNN",
                 "LLM assistant A": "LLM-A", "LLM assistant B": "LLM-B"}
        for arm in ARMS:
            row = " ".join(f"{cm[(arm, a)]:5d}" for a in AUTHORS)
            print(f"{arm:6s}       {row}   {tot[arm]}")
        # key figure
        tnn_as_tnn = cm[("tnn", "TNN AI coding agent")]
        tot_tnn = tot["tnn"]
        frac = tnn_as_tnn / tot_tnn if tot_tnn else None
        print(f"KEY: P(guessed 'TNN AI coding agent' | true tnn) = "
              f"{tnn_as_tnn}/{tot_tnn} = {frac:.3f}" if frac is not None else "KEY: NA")

    cma, ta_ = confusion(["sol"])
    cmb, tb_ = confusion(["grok"])
    cmc, tc_ = confusion(["sol", "grok"])
    show_cm(cma, ta_, "Table (c) sol attribution")
    show_cm(cmb, tb_, "Table (c) grok attribution")
    show_cm(cmc, tc_, "Table (c) combined attribution")

    # machine-readable dump for the report
    dump = {
        "sol": {f"{arm}_T{d+1}": ta[(arm, d)] for arm in ARMS for d in range(4)},
        "grok": {f"{arm}_T{d+1}": tb[(arm, d)] for arm in ARMS for d in range(4)},
        "combined": {f"{arm}_T{d+1}": tc[(arm, d)] for arm in ARMS for d in range(4)},
        "confusion": {
            "sol": {f"{arm}>{auth}": cma[(arm, auth)] for arm in ARMS for auth in AUTHORS},
            "grok": {f"{arm}>{auth}": cmb[(arm, auth)] for arm in ARMS for auth in AUTHORS},
            "combined": {f"{arm}>{auth}": cmc[(arm, auth)] for arm in ARMS for auth in AUTHORS}},
        "missing": [f"{j}/{s}" for j, s in missing],
    }
    open(os.path.join(WORK, "cln1_results.json"), "w").write(json.dumps(dump, indent=2))
    print("\nwrote work/cln1_results.json")

if __name__ == "__main__":
    main()
