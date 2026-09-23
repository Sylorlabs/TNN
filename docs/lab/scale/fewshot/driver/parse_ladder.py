#!/usr/bin/env python3
"""Parse few-shot ladder logs into the results table."""
import re, glob, os, statistics

RDIR = os.path.expanduser("~/workspace/scale-fewshot/runs")

def parse(path):
    d = {}
    txt = open(path).read()
    pats = {
        "clean": r"SCALE_MASTERY,clean_num=(\d+),clean_den=(\d+)",
        "all": r"SCALE_MASTERY_ALL,num=(\d+),den=(\d+)",
        "abs": r"SCALE_ABSORPTION,absorbed=(\d+),den=(\d+)",
        "ops": r"ops_per_fact_x1000=(\d+)",
        "bpf": r"total_bpf=(\d+)",
        "digest": r"SCALE_DIGEST,fnv1a=([0-9a-f]+)",
        "recall": r"SCALE_RECALL_TIMING,recalls=(\d+),ns_total=(\d+),ns_per_recall_x1000=(\d+)",
        "flaw": r"SCALE_FLAW_TOTAL,pass=(\d+),total=96",
    }
    for k, p in pats.items():
        m = re.search(p, txt)
        d[k] = m.groups() if m else None
    fams = re.findall(r"SCALE_FLAW,fam([ABCD])=(\d+)", txt)
    d["fams"] = {a: int(v) for a, v in fams}
    decs = re.findall(r"SCALE_DECILE,d=(\d+),num=(\d+),den=(\d+)", txt)
    d["decs"] = {int(a): (int(b), int(c)) for a, b, c in decs}
    d["done"] = "SCALE_DONE" in txt
    return d

configs = [
    ("n192", 192, 24, 8, 0), ("n128", 128, 16, 8, 0), ("n096", 96, 24, 4, 0),
    ("n064", 64, 16, 4, 0), ("n048", 48, 24, 2, 0), ("n032", 32, 16, 2, 0),
    ("n024", 24, 24, 1, 0), ("n016", 16, 16, 1, 0), ("n008", 8, 8, 1, 0),
    ("n004", 4, 4, 1, 0), ("n002", 2, 2, 1, 0), ("n001", 1, 1, 1, 0),
    ("n001_plant", 1, 1, 1, 6), ("n002_mixed", 2, 2, 1, 5),
]

print("| N | off | clean mastery | all-fact | absorption | flaw | ops/fact | B/fact | digest match | recall ns/probe |")
print("|---|---|---|---|---|---|---|---|---|---|")
for lbl, N, C, M, OFF in configs:
    logs = sorted(glob.glob(f"{RDIR}/{lbl}_r*.log"))
    if not logs:
        print(f"| {N} | {OFF} | NO LOGS | | | | | | | |")
        continue
    ps = [parse(p) for p in logs]
    ok = all(p["done"] for p in ps)
    p0 = ps[0]
    digests = {p["digest"][0] for p in ps if p["digest"]}
    cn, cd = p0["clean"]; an, ad = p0["all"]
    clean = f"{int(cn)}/{int(cd)}={int(cn)/int(cd):.4f}" if int(cd) else "0/0"
    allf = f"{int(an)}/{int(ad)}={int(an)/int(ad):.4f}"
    bn, bd = p0["abs"]
    absor = f"{bn}/{bd}" if int(bd) else "N/A"
    flaw = p0["flaw"][0] if p0["flaw"] else "?"
    ops = f"{int(p0['ops'][0])/1000:.3f}" if p0["ops"] else "?"
    bpf = p0["bpf"][0] if p0["bpf"] else "?"
    dm = f"{len(digests)} hash" + (" OK" if len(digests) == 1 else " MISMATCH")
    rec = [int(p["recall"][2]) / 1000 for p in ps if p["recall"]]
    rstr = f"{statistics.mean(rec):.1f}" if rec else "?"
    flag = "" if ok else " **INCOMPLETE**"
    print(f"| {N} | {OFF} | {clean} | {allf} | {absor} | {flaw}/96 | {ops} | {bpf} | {dm} | {rstr} |{flag}")

print("\nDeciles (r0) for small N:")
for lbl, N, C, M, OFF in configs:
    p = parse(f"{RDIR}/{lbl}_r0.log")
    if not p["done"]:
        continue
    ds = " ".join(f"d{k}={a}/{b}" for k, (a, b) in sorted(p["decs"].items()) if b > 0)
    print(f"  {lbl}: {ds}")
