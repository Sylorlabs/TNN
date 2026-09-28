#!/usr/bin/env python3
"""Q1 scored run: 5 reps of inspect over the 24-item battery, byte-identical check."""
import subprocess, hashlib, os, sys

BB = '/home/hatch/workspace/tnn-lab/coding/bug-blindness'
INSPECT = BB + '/inspect'
BAT = BB + '/battery'
LOG = BB + '/logs'

def run_rep(rep):
    out_lines = []
    for i in range(1, 25):
        f = f'bb{i:02d}.zag'
        r = subprocess.run([INSPECT, os.path.join(BAT, f)],
                           capture_output=True, text=True, timeout=30)
        line = r.stdout.strip().split('\n')[-1]
        out_lines.append(f'{f} {line}')
    blob = '\n'.join(out_lines) + '\n'
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(f'{LOG}/bb1_rep{rep}.out', 'w') as fh:
        fh.write(blob)
    return blob, digest

def main():
    key = {}
    for ln in open(f'{BAT}/answer_key.txt'):
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        parts = ln.split()
        key[parts[0]] = ' '.join(parts[1:])
    digests = []
    blobs = []
    for rep in range(1, 6):
        blob, digest = run_rep(rep)
        digests.append(digest)
        blobs.append(blob)
        print(f'rep{rep} sha256={digest}', flush=True)
    with open(f'{LOG}/bb1_digests.txt', 'w') as fh:
        for rep, d in enumerate(digests, 1):
            fh.write(f'rep{rep} {d}\n')
    identical = len(set(digests)) == 1
    print('byte-identical across 5 reps:', identical)
    # score rep1 (all identical if deterministic)
    blob = blobs[0]
    tp = fp = fn = 0
    per_class = {}
    false_alarms = []
    misses = []
    misclass = []
    for ln in blob.strip().split('\n'):
        parts = ln.split()
        f = parts[0]
        got = ' '.join(parts[1:])
        exp = key[f]
        exp_bug = exp.startswith('BUG')
        got_bug = got.startswith('BUG')
        if exp_bug and got_bug:
            tp += 1
            cls_exp = exp.split()[1]
            cls_got = got.split()[1]
            per_class.setdefault(cls_exp, {'n': 0, 'ok': 0})
            per_class[cls_exp]['n'] += 1
            if cls_got == cls_exp and got == exp:
                per_class[cls_exp]['ok'] += 1
            else:
                misclass.append(f'{f}: got={got} exp={exp}')
        elif exp_bug and not got_bug:
            fn += 1
            misses.append(f'{f}: got={got} exp={exp}')
        elif not exp_bug and got_bug:
            fp += 1
            false_alarms.append(f'{f}: got={got} exp={exp}')
    det_acc = tp / 16
    fa_rate = fp / 8
    prec = sum(v['ok'] for v in per_class.values()) / tp if tp else 0.0
    print(f'detected buggy: {tp}/16  missed: {fn}/16  false alarms: {fp}/8')
    print(f'KB-D1: detection acc={det_acc:.4f} (>=0.70 need >=12/16), fa={fa_rate:.4f} (<=0.25 need <=2/8)')
    print(f'KB-D2: class precision={prec:.4f} (>=0.60)')
    for cls in sorted(per_class):
        v = per_class[cls]
        print(f'  {cls}: {v["ok"]}/{v["n"]} exact class+line')
    if misses:
        print('MISSES:'); [print(' ', m) for m in misses]
    if false_alarms:
        print('FALSE ALARMS:'); [print(' ', m) for m in false_alarms]
    if misclass:
        print('MISCLASSIFIED (detected, wrong class/line):'); [print(' ', m) for m in misclass]
    d1 = (tp >= 12 and fp <= 2)
    d2 = (prec >= 0.60)
    print(f'KB-D1 {"PASS" if d1 else "FAIL"}   KB-D2 {"PASS" if d2 else "FAIL"}')
    with open(f'{LOG}/bb1_score.txt', 'w') as fh:
        fh.write(f'tp={tp}/16 fn={fn}/16 fp={fp}/8 det_acc={det_acc:.4f} fa_rate={fa_rate:.4f} class_prec={prec:.4f} KB-D1={d1} KB-D2={d2} byte_identical={identical}\n')

if __name__ == '__main__':
    main()
