#!/usr/bin/env python3
"""Coding trial driver — deterministic plumbing only.
Invokes the pure-Zag learner, writes source, compiles, runs vectors,
returns compiler evidence, retries up to 6 iterations.
Makes NO coding decisions itself.
"""
import json, subprocess, sys, os, re, time

ZNC = '/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1'
LEARNER = '/home/hatch/workspace/tnn-lab/coding/src/learner'
CURRICULUM = '/home/hatch/workspace/tnn-lab/coding/curriculum/curriculum.json'
WORKDIR = '/tmp/coding_driver'

ALL_PATTERNS = "p_math,p_search,p_slice,p_strrev,p_func,p_loop,p_struct,p_sort,p_argv,p_strcnt,p_slicefill"

# T4m: same patterns (tests generalization, not memorization)
# No-T2 ablation: T2 patterns removed
NO_T2_PATTERNS = "p_math,p_slice,p_strrev,p_func,p_loop,p_struct,p_argv,p_strcnt"

PARSE_INT_CARD = 'Parse: ```fn parse_int(s:[]u8,n:i64)i64 { let neg:i64=0; let i:i64=0; if(n>0){if(s[0]==45){neg=1;i=1;}} let v:i64=0; while(i<n){if(s[i]>=48){if(s[i]<=57){v=v*10+((s[i] as i64)-48);}}i=i+1;} if(neg==1){v=0-v;} return v; }```'

def eclass_of(err):
    if 'E0203' in err: return 'E0203'
    if 'unknown function' in err: return 'UNKNOWNFN'
    if 'passes' in err and 'argument(s)' in err: return 'ARITY'
    if 'E0001' in err: return 'PARSE'
    if 'duplicate fn' in err: return 'DUPFN'
    return 'UNKNOWN'

def details_of(err, eclass):
    if eclass == 'UNKNOWNFN':
        m = re.search(r'unknown function `([^`]+)`', err)
        return m.group(1) if m else ''
    if eclass == 'ARITY':
        m = re.search(r"call to '(\w+)' passes (\d+) argument\(s\), expected (\d+)", err)
        return f"{m.group(1)}:{m.group(2)}:{m.group(3)}" if m else ''
    if eclass == 'DUPFN':
        m = re.search(r"duplicate fn definition '(\w+)'", err)
        return m.group(1) if m else ''
    return ''

def run_learner(mode, *args):
    r = subprocess.run([LEARNER, mode] + list(args),
                       capture_output=True, text=True, timeout=30)
    return r.stdout, r.stderr, r.returncode

def compile_src(src, out_bin):
    with open('/tmp/driver_src.zag', 'w') as f:
        f.write(src)
    r = subprocess.run([ZNC, '/tmp/driver_src.zag', '-o', out_bin, '--no-analyze'],
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout + r.stderr

def run_tests(bin_path, tests):
    for test in tests:
        try:
            r = subprocess.run([bin_path] + test['args'],
                               capture_output=True, text=True, timeout=10)
            if r.stdout != test['stdout'] or r.returncode != test['rc']:
                return False, f"got={repr(r.stdout)} rc={r.returncode} expect={repr(test['stdout'])} rc={test['rc']}"
        except Exception as e:
            return False, str(e)
    return True, "all pass"

def gen_task(task, patterns, card='', max_iters=6, use_repair=True):
    """Run gen -> compile -> test loop. Returns (success, iters, log)."""
    spec = task['spec']
    demo = task.get('demo', '')
    log = []
    # check gate first
    gate_out, _, _ = run_learner('gate', spec)
    if 'REFUSE' in gate_out:
        return False, 0, [f"GATE_REFUSED: {gate_out.strip()}"]
    src, _, _ = run_learner('gen', spec, patterns, demo, card)
    for it in range(1, max_iters + 1):
        rc, err = compile_src(src, '/tmp/driver_bin')
        if rc == 0:
            ok, msg = run_tests('/tmp/driver_bin', task['tests'])
            if ok:
                return True, it, log + [f"iter{it}: compile+test PASS"]
            else:
                log.append(f"iter{it}: compiled but test FAIL: {msg}")
                # test failure isn't a compiler error; can't repair via compiler evidence
                # per prereg, repair uses compiler evidence; test failures end the loop
                return False, it, log
        else:
            eclass = eclass_of(err)
            details = details_of(err, eclass)
            log.append(f"iter{it}: compile FAIL eclass={eclass} details={details}")
            if not use_repair or it >= max_iters:
                return False, it, log
            # repair via learner
            src, _, _ = run_learner('repair', eclass, details, src)
            log.append(f"iter{it}: repaired via {eclass}")
    return False, max_iters, log

def repair_task(t3item, max_iters=6, use_repair=True):
    """T3: start from broken source, repair loop."""
    src = t3item['broken']
    log = []
    iters = 0
    # allow up to max_iters repair attempts
    attempts = max_iters if use_repair else 1
    for it in range(1, attempts + 1):
        iters = it
        rc, err = compile_src(src, '/tmp/driver_bin')
        if rc == 0:
            ok, msg = run_tests('/tmp/driver_bin', t3item['tests'])
            if ok:
                return True, iters, log + [f"attempt{it}: PASS"]
            else:
                return False, iters, log + [f"attempt{it}: test FAIL {msg}"]
        eclass = eclass_of(err)
        details = details_of(err, eclass)
        log.append(f"attempt{it}: {eclass} {details}")
        if it >= attempts:
            return False, iters, log
        src, _, _ = run_learner('repair', eclass, details, src)
    return False, iters, log

def main():
    os.makedirs(WORKDIR, exist_ok=True)
    c = json.load(open(CURRICULUM))
    print("=== Coding Trial Driver ===", flush=True)
    print(f"Tasks: {len(c['tasks'])}, T3: {len(c['t3'])}", flush=True)
    # This is a smoke test; full evaluation is run via run_full.py
    print("Driver loaded. Use run_full.py for scored evaluation.", flush=True)

if __name__ == '__main__':
    main()
