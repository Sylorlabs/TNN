#!/usr/bin/env python3
"""Q4 generation: 6 fresh specs, 5 reps each, via driver.gen_task.
Labeled: pre-equivalent replay from the unchanged stateless executable
(NOT a chronological PRE — sequencing deviation, see gen_specs_sealed.txt).
"""
import sys, hashlib
sys.path.insert(0, '/home/hatch/workspace/tnn-lab/coding')
from driver import gen_task, ALL_PATTERNS

SPECS = [
    ('g1', 'T1|FUNC|name=sqr|args=i64|ret=i64|op=square', '7', '49\n'),
    ('g2', 'T1|FUNC|name=cube|args=i64|ret=i64|op=cube', '3', '27\n'),
    ('g3', 'T1|FUNC|name=add4|args=i64,i64,i64,i64|ret=i64|op=sum', '1,2,3,4', '10\n'),
    ('g4', 'T1|FUNC|name=min2|args=i64,i64|ret=i64|op=min', '8,3', '3\n'),
    ('g5', 'T1|FUNC|name=neg|args=i64|ret=i64|op=negate', '5', '-5\n'),
    ('g6', 'T1|FUNC|name=mul3|args=i64,i64,i64|ret=i64|op=product', '2,3,4', '24\n'),
]

def main():
    rep_blobs = []
    for rep in range(1, 6):
        lines = []
        for gid, spec, demo, expect in SPECS:
            task = {'id': gid, 'spec': spec, 'demo': demo,
                    'tests': [{'args': [], 'stdout': expect, 'rc': 0}]}
            ok, iters, ilog = gen_task(task, ALL_PATTERNS, max_iters=6, use_repair=True)
            lines.append(f"{gid} ok={ok} iters={iters}")
            for l in ilog:
                lines.append(f"  {l}")
        blob = "\n".join(lines) + "\n"
        rep_blobs.append(blob)
        with open(f'/home/hatch/workspace/tnn-lab/coding/bug-blindness/logs/bb1_q4_gen_rep{rep}.out', 'w') as f:
            f.write(blob)
    digests = [hashlib.sha256(b.encode()).hexdigest() for b in rep_blobs]
    print("five-rep digests identical:", len(set(digests)) == 1)
    for i, d in enumerate(digests, 1):
        print(f"  rep{i} {d}")
    print()
    print(rep_blobs[0])

if __name__ == '__main__':
    main()
