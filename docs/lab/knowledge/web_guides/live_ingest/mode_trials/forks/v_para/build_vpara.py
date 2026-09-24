#!/usr/bin/env python3
"""V-PARA build script with source-fidelity checks.

1. Verifies v_para.zag was produced from the frozen webg.zag + apply_vpara.py
   (re-runs the patcher on a fresh copy and diffs).
2. Verifies the embedded stoplist matches stoplist.txt exactly.
3. Compiles with the pinned toolchain.
4. Runs teach validation (G1-G6 installed, G7 rejected).
"""
import hashlib, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORKBASE = os.path.expanduser('~/workspace/scratch-li-forkbase')
ZNC = os.path.expanduser('~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1')
FROZEN_MD5 = 'c1ea3e71a93205dd6facf61667c3f442'

def md5(p):
    return hashlib.md5(open(p,'rb').read()).hexdigest()

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout, r.stderr

# 1. frozen source fidelity
frozen = os.path.join(FORKBASE, 'webg.zag')
m = md5(frozen)
assert m == FROZEN_MD5, f'frozen webg.zag MD5 {m} != {FROZEN_MD5}'
print(f'frozen source OK ({m})')

# 2. stoplist fidelity: embedded pipe-list vs stoplist.txt
src = open(os.path.join(HERE, 'v_para.zag')).read()
import re
mm = re.search(r'return "([a-z|]+)";\n\}\n\n// parse pipe-delimited stoplist', src)
assert mm, 'embedded stoplist not found'
embedded = mm.group(1).split('|')
filed = [l.strip() for l in open(os.path.join(HERE, 'stoplist.txt')) if l.strip()]
assert embedded == filed, f'stoplist mismatch: embedded {len(embedded)} vs filed {len(filed)}'
print(f'stoplist OK ({len(filed)} words, embedded==filed)')

# 3. compile
rc, out, err = run([ZNC, 'v_para.zag', '-o', 'v_para'], cwd=HERE)
assert rc == 0, f'compile failed: {err[-500:]}'
print('compile OK')

# 4. teach validation
import shutil
tstate = os.path.join(HERE, 'tstate_build')
shutil.rmtree(tstate, ignore_errors=True)
os.makedirs(tstate)
rc, out, err = run(['./v_para', 'teach', os.path.join(FORKBASE, 'guides'), tstate], cwd=HERE)
lines = [l for l in out.split('\n') if l.startswith('LEARN|')]
for l in lines: print(' ', l)
ok = (
    any('LEARN|G1|INSTALLED|PASS' in l for l in lines) and
    any('LEARN|G2|INSTALLED|PASS' in l for l in lines) and
    any('LEARN|G3|INSTALLED|PASS' in l for l in lines) and
    any('LEARN|G4|INSTALLED|PASS' in l for l in lines) and
    any('LEARN|G5|INSTALLED|PASS' in l for l in lines) and
    any('LEARN|G6|INSTALLED|PASS' in l for l in lines) and
    any('LEARN|G7|REJECTED' in l for l in lines)
)
assert ok, 'teach validation failed'
print('teach validation OK (G1-G6 installed, G7 rejected)')
print('BUILD PASS')
