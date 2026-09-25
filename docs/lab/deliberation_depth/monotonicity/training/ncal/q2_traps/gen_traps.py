#!/usr/bin/env python3
"""Generate TRAP batteries for NCAL Q2. Deterministic. See ADDENDUM_Q2_TRAPS_2026-09-25.md §2."""
# T1: fresh class (5,3): f1=825, f5=875
rows = []
def emit(iid, fam, depth, f1, f5, rel, corr):
    rows.append(f"{iid}\t{fam}\t{depth}\t{f1}\t{f5}\t{rel}\t{corr}")
DEPTHS = [1,2,4,8,16]
# group C: all correct
for n in range(1,13):
    iid = f"T1C-{n:03d}"
    for d in DEPTHS: emit(iid,"t1trap",d,825,875,1,1)
# group T: wrong at d1 only
for n in range(1,13):
    iid = f"T1T-{n:03d}"
    for d in DEPTHS: emit(iid,"t1trap",d,825,875,1,0 if d==1 else 1)
# group W: wrong at d1,d2
for n in range(1,7):
    iid = f"T1W-{n:03d}"
    for d in DEPTHS: emit(iid,"t1trap",d,825,875,1,0 if d in (1,2) else 1)
# leg order: all d1, then d2, d4, d8, d16 (id order within)
order = {d:i for i,d in enumerate(DEPTHS)}
rows.sort(key=lambda r:(order[int(r.split("\t")[2])], r.split("\t")[0]))
with open("trap_t1.tsv","w") as f: f.write("\n".join(rows)+"\n")
print("trap_t1.tsv rows:", len(rows))

# T3: five fresh classes, d1 only, known true rates
t3 = [
    # (mb,cb,f1,f5,true_rate, wrong_predicate)
    (0,3,75,875,1.00, lambda i: False),
    (0,4,75,1125,0.75, lambda i: i%4==3),
    (1,4,225,1125,0.50, lambda i: i%2==1),
    (2,3,375,875,0.25, lambda i: i%4!=0),
    (4,3,675,875,0.00, lambda i: True),
]
rows3 = []
for ci,(mb,cb,f1,f5,rate,wp) in enumerate(t3):
    assert min(f1//150,6)==mb and min(f5//250,4)==cb, (mb,cb,f1,f5)
    for i in range(40):
        iid = f"T3C{ci}-{i:03d}"
        corr = 0 if wp(i) else 1
        rows3.append(f"{iid}\tt3trap\t1\t{f1}\t{f5}\t1\t{corr}")
with open("trap_t3.tsv","w") as f: f.write("\n".join(rows3)+"\n")
print("trap_t3.tsv rows:", len(rows3))
# record true rates
with open("trap_t3_truth.tsv","w") as f:
    for ci,(mb,cb,f1,f5,rate,wp) in enumerate(t3):
        f.write(f"C{ci}\t{mb}\t{cb}\t{rate:.2f}\n")
