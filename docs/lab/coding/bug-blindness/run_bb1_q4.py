#!/usr/bin/env python3
"""Q4 probe scoring: inspect on 8 fresh ARITY + 8 fresh UNINIT items. tag = pre|post."""
import subprocess, hashlib, os, sys

BB = '/home/hatch/workspace/tnn-lab/coding/bug-blindness'
INSPECT = BB + '/inspect'
Q4 = BB + '/q4'
LOG = BB + '/logs'
TAG = sys.argv[1] if len(sys.argv) > 1 else 'pre'

def main():
    key = {}
    for ln in open(f'{Q4}/answer_key_q4.txt'):
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        parts = ln.split()
        key[parts[0]] = ' '.join(parts[1:])
    ids = sorted(key.keys())
    out = []
    for f in ids:
        r = subprocess.run([INSPECT, os.path.join(Q4, f)],
                           capture_output=True, text=True, timeout=30)
        line = r.stdout.strip().split('\n')[-1]
        out.append(f'{f} {line}')
    blob = '\n'.join(out) + '\n'
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(f'{LOG}/bb1_q4_{TAG}.out', 'w') as fh:
        fh.write(blob)
    ar_ok = ar_n = un_ok = un_n = 0
    det = []
    for ln in out:
        parts = ln.split()
        f = parts[0]
        got = ' '.join(parts[1:])
        exp = key[f]
        ok = (got == exp)
        det.append(f'{f}: got={got} exp={exp} {"OK" if ok else "MISS"}')
        if f.startswith('qa'):
            ar_n += 1
            ar_ok += ok
        else:
            un_n += 1
            un_ok += ok
    print(f'sha256={digest}')
    print(f'ARITY: {ar_ok}/{ar_n} = {ar_ok/ar_n:.4f}')
    print(f'UNINIT(control): {un_ok}/{un_n} = {un_ok/un_n:.4f}')
    for d in det:
        print(' ', d)
    with open(f'{LOG}/bb1_q4_{TAG}_score.txt', 'w') as fh:
        fh.write(f'arity={ar_ok}/{ar_n} uninit={un_ok}/{un_n} sha256={digest}\n')

if __name__ == '__main__':
    main()
