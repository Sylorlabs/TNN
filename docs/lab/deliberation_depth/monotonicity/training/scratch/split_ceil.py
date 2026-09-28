import json, sys
base = sys.argv[1]
src = base + '/ceiling/items/ceiling_battery.jsonl'
out = {k: open(f'{base}/monotonicity/training/items/ceiling_{k}.jsonl','w') for k in
       ['P_even','P_odd','D_even','D_odd','O_even','O_odd']}
n = 0
with open(src) as f:
    for line in f:
        line = line.strip()
        if not line: continue
        d = json.loads(line)
        iid = d['id']
        fam = iid.split('-')[1]
        rep = int(iid.split('-')[-1])
        key = f"{fam}_{'even' if rep % 2 == 0 else 'odd'}"
        out[key].write(line + '\n'); n += 1
for k, fh in out.items(): fh.close()
print("total", n)
