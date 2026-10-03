#!/usr/bin/env python3
"""Q4 repair experience: 6 ARITY repairs with compiler feedback via driver.repair_task."""
import sys, json
sys.path.insert(0, '/home/hatch/workspace/tnn-lab/coding')
from driver import repair_task

ADD2 = """fn add(a:i64,b:i64)i64 {
    return a+b;
}
fn main()void {
    let r:i64=ADD_CALL;
    _zag_print(_zag_i64_to_str(r));
    _zag_print("\\n");
    return;
}
"""
ADD3 = """fn add3(a:i64,b:i64,c:i64)i64 {
    return a+b+c;
}
fn main()void {
    let r:i64=ADD3_CALL;
    _zag_print(_zag_i64_to_str(r));
    _zag_print("\\n");
    return;
}
"""
MUL2 = """fn mul(a:i64,b:i64)i64 {
    return a*b;
}
fn main()void {
    let r:i64=MUL_CALL;
    _zag_print(_zag_i64_to_str(r));
    _zag_print("\\n");
    return;
}
"""

items = [
    ('r1', ADD2.replace('ADD_CALL', 'add(4,5,6)'), '9\n'),    # too many -> drop
    ('r2', ADD2.replace('ADD_CALL', 'add(4)'), '9\n'),         # too few -> fill 4,5
    ('r3', ADD3.replace('ADD3_CALL', 'add3(1,2,3,4)'), '6\n'), # too many -> drop
    ('r4', ADD3.replace('ADD3_CALL', 'add3(1,2)'), '6\n'),     # too few -> fill 1,2,3
    ('r5', MUL2.replace('MUL_CALL', 'mul(3,4,5)'), '12\n'),   # too many -> drop
    ('r6', MUL2.replace('MUL_CALL', 'mul(3)'), '12\n'),       # too few -> fill 3,4
]

def main():
    log = []
    ok_n = 0
    for rid, broken, expect in items:
        item = {'id': rid, 'broken': broken,
                'tests': [{'args': [], 'stdout': expect, 'rc': 0}]}
        ok, iters, ilog = repair_task(item, max_iters=6, use_repair=True)
        ok_n += ok
        log.append(f'=== {rid} expect={expect.strip()} ok={ok} iters={iters}')
        log.extend('  ' + l for l in ilog)
    blob = '\n'.join(log) + '\n'
    print(blob)
    print(f'repaired: {ok_n}/6')
    with open('/home/hatch/workspace/tnn-lab/coding/bug-blindness/logs/bb1_q4_repairs.log', 'w') as fh:
        fh.write(blob + f'repaired: {ok_n}/6\n')

if __name__ == '__main__':
    main()
