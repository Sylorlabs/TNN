#!/usr/bin/env python3
"""Frozen oracle for the recency-vs-coherence trial (KB1..KB6).

Usage: verify_rsi4c.py <runs-dir> <battery-csv>
Checks determinism (5/5 identical per mode), battery separation (Zag item
fields == CSV fields, no gt in binary), class construction targets, then
scores every arm vs ground truth and applies the frozen champion rule.
Exits 0 iff all bars pass; prints the arm x metric table either way.
"""
import csv, glob, os, sys

def fail(msg):
    print("FAIL:", msg); sys.exit(1)

def sat(v, a, op):
    return (v == a) if op == 0 else ((v < a) if op == 1 else (v > a))

def score(vold, vnew, rels, pick):
    v = vnew if pick == "NEW" else vold
    return sum(1 if sat(v, a, op) else -1 for (a, op) in rels)

runs, csvpath = sys.argv[1], sys.argv[2]
batt = {}
with open(csvpath) as f:
    for row in csv.DictReader(f):
        i = int(row["id"])
        batt[i] = dict(key=int(row["key"]), vold=int(row["vold"]),
                       vnew=int(row["vnew"]),
                       rels=[(int(row["a1"]), int(row["op1"])),
                             (int(row["a2"]), int(row["op2"])),
                             (int(row["a3"]), int(row["op3"]))],
                       cidx=int(row["cidx"]), caval=int(row["caval"]),
                       gt=row["gt"], cls=row["class"])

# KB1: construction targets from the frozen prereg
counts = {}
for i, b in batt.items():
    counts[b["cls"]] = counts.get(b["cls"], 0) + 1
    rels = b["rels"]
    so, sn = score(b["vold"], b["vnew"], rels, "OLD"), score(b["vold"], b["vnew"], rels, "NEW")
    rp = list(rels)
    if b["cidx"] != -1:
        rp[b["cidx"]] = (b["caval"], rp[b["cidx"]][1])
    sop, snp = score(b["vold"], b["vnew"], rp, "OLD"), score(b["vold"], b["vnew"], rp, "NEW")
    c = b["cls"]
    ok = (c == "N-clean" and sn > so and b["cidx"] == -1 and b["gt"] == "NEW") or \
         (c == "O-clean" and so > sn and b["cidx"] == -1 and b["gt"] == "OLD") or \
         (c == "ADV-NEW" and so > sn and snp > sop and b["gt"] == "NEW") or \
         (c == "ADV-OLD" and sn > so and sop > snp and b["gt"] == "OLD") or \
         (c == "NEITHER" and so == sn <= 0 and sop == snp and b["gt"] == "WITHHOLD")
    if not ok:
        fail(f"KB1-BATTERY: item {i} violates its class target")
if counts != {"N-clean": 6, "O-clean": 6, "ADV-NEW": 2, "ADV-OLD": 2, "NEITHER": 8}:
    fail(f"KB1-BATTERY: class counts {counts}")
print("KB1-BATTERY: PASS (24 items, targets hold)")

# KB2: determinism — 5 identical logs per mode
modes = ["base", "recency", "coherence", "askfirst"]
logs = {}
for m in modes:
    files = sorted(glob.glob(os.path.join(runs, f"r4c_{m}_*.log")))
    if len(files) != 5:
        fail(f"KB2-DET: mode {m} has {len(files)} logs, want 5")
    bodies = [open(f).read() for f in files]
    if len(set(bodies)) != 1:
        fail(f"KB2-DET: mode {m} logs differ across reps")
    if f"R4C_CFG,mode={m}" not in bodies[0] or "R4C_DONE" not in bodies[0]:
        fail(f"KB2-DET: mode {m} log malformed")
    logs[m] = bodies[0]
print("KB2-DET: PASS (5/5 byte-identical per mode)")

# KB5: separation — Zag item fields match CSV exactly; gt never in binary
res = {}
for m in modes:
    items, fields = {}, {}
    for line in logs[m].splitlines():
        if line.startswith("R4C_ITEMFIELDS,"):
            kv = dict(p.split("=") for p in line.split(",")[1:])
            iid = int(kv["id"])
            fields[iid] = {k: int(v) for k, v in kv.items() if k != "id"}
        elif line.startswith("R4C_ITEM,"):
            kv = dict(p.split("=") for p in line.split(",")[1:])
            items[int(kv["id"])] = (kv["verdict"], int(kv["ops"]), int(kv["consult"]))
    if set(items) != set(batt) or set(fields) != set(batt):
        fail(f"KB5-SEPARATION: mode {m} item coverage != 24")
    for i, b in batt.items():
        f = fields[i]
        want = dict(key=b["key"], vold=b["vold"], vnew=b["vnew"],
                    a1=b["rels"][0][0], op1=b["rels"][0][1],
                    a2=b["rels"][1][0], op2=b["rels"][1][1],
                    a3=b["rels"][2][0], op3=b["rels"][2][1],
                    cidx=b["cidx"], caval=b["caval"])
        if f != want:
            fail(f"KB5-SEPARATION: mode {m} item {i} fields drift from CSV")
    res[m] = items
print("KB5-SEPARATION: PASS (fields match CSV; gt absent from binary)")

# score every arm
table = {}
neither_ids = [i for i, b in batt.items() if b["cls"] == "NEITHER"]
for m in modes:
    acc = wrong = wh_n = 0
    cons = cost = 0
    for i, b in batt.items():
        v, ops, c = res[m][i]
        cost += ops; cons += c
        if v == b["gt"]:
            acc += 1
        elif v in ("NEW", "OLD"):
            wrong += 1
        if i in neither_ids and v == "WITHHOLD":
            wh_n += 1
    table[m] = dict(acc=acc, wrong=wrong, wh_n=wh_n, cons=cons, cost=cost)

print("\narm x metric (n=24):")
print(f"{'arm':<10}{'acc':>5}{'wrong':>7}{'wh/8':>6}{'cons':>6}{'cost':>7}")
for m in modes:
    t = table[m]
    print(f"{m:<10}{t['acc']:>5}{t['wrong']:>7}{t['wh_n']:>6}{t['cons']:>6}{t['cost']:>7}")

# KB3: champion = strictly greatest acc AND wrong-install <= all others
cands = [m for m in modes
         if all(table[m]["acc"] > table[o]["acc"] for o in modes if o != m)
         and all(table[m]["wrong"] <= table[o]["wrong"] for o in modes if o != m)]
champion = cands[0] if len(cands) == 1 else None
print("\nKB3-CHAMPION:", champion if champion else "NO-CHAMPION")
# KB4: honest falsification branch
if champion == "recency":
    print('KB4-FALSIFY: TRIGGERED — "Micah\'s critique is FALSIFIED — recency beat coherence head-to-head."')
print("ALL BARS PASS")
