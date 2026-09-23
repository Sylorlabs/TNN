import re
from collections import defaultdict
oracle = {}
subtype = {}
for line in open("corpus_cau.tsv"):
    p = line.rstrip("\n").split("\t")
    oracle[p[0]] = int(p[4])
got = {}
reason = {}
for line in open("run_1.txt"):
    m = re.match(r"(\S+) (\d) (\S+)", line)
    got[m.group(1)] = int(m.group(2)); reason[m.group(1)] = m.group(3)
# subtype from idx letter code
code2sub = {"B":"because","C":"causes","L":"leads-to","D":"due-to","R":"results-in",
            "T":"the-reason","M":"mechanism","H":"chain","P":"prevented-cause",
            "K":"hedge","N":"deny-dir","X":"control"}
stats = defaultdict(lambda: [0,0])  # sub -> [correct, total]
mistags = []
for idx in sorted(oracle):
    sub = code2sub[idx.split("-")[1][0]]
    ok = oracle[idx] == got[idx]
    stats[sub][1] += 1
    stats[sub][0] += ok
    if not ok:
        mistags.append((idx, sub, oracle[idx], got[idx], reason[idx]))
tot_c = sum(v[0] for v in stats.values()); tot = sum(v[1] for v in stats.values())
print(f"OVERALL {tot_c}/{tot} = {tot_c/tot:.1%}")
for s in ["because","causes","leads-to","due-to","results-in","the-reason","mechanism","chain","prevented-cause","hedge","deny-dir","control"]:
    c,t = stats[s]; print(f"  {s:15s} {c}/{t} = {c/t:.0%}")
print(f"\nMISTAGS ({len(mistags)}):")
for m in mistags:
    print(f"  {m[0]} [{m[1]}] oracle={m[2]} got={m[3]} ({m[4]})")
