#!/usr/bin/env python3
"""Step 0: measure the BASELINE (coding/src/learner.zag, pinned sha) on the
frozen T4x battery.

Protocol: EXACTLY the baseline's native measurement protocol from
coding/run_full.py::eval_gen_task (the protocol behind CODING_REPORT.md's
frozen bars): gate -> gen -> write -> znc -> run test vectors ->
on compile failure, driver-classified repair (eclass_of/details_of copied
verbatim from run_full.py — the documented driver-classification correction
is CARRIED, not fixed, so the numbers stay comparable to the frozen bars),
max 6 iterations; test failure breaks (not compiler-repairable).

The baseline does not speak the loop harness's diagnose protocol, so it
cannot run under loop/driver.py; this script is its native harness.
Deterministic plumbing only. 5 reps; per-rep sha256 digest must match.

Usage: measure_baseline_t4x.py <battery.json> <out.json>
"""
import json, subprocess, sys, os, re, hashlib

ZNC = '/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1'
LEARNER = '/home/hatch/workspace/tnn-lab/coding/src/learner'
ALL_PATTERNS = "p_math,p_search,p_slice,p_strrev,p_func,p_loop,p_struct,p_sort,p_argv,p_strcnt,p_slicefill"
WORK = '/home/hatch/workspace/tnn-lab/coding/reflection/task1/harness/work/baseline_t4x'


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
    return r.stdout


def compile_src(src, tag):
    zp = os.path.join(WORK, f'{tag}.zag')
    bp = os.path.join(WORK, f'{tag}.bin')
    with open(zp, 'w') as f:
        f.write(src)
    r = subprocess.run([ZNC, zp, '-o', bp, '--no-analyze', '--no-zagd'],
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout + r.stderr, bp


def run_tests(binpath, tests):
    for t in tests:
        r = subprocess.run([binpath] + t['args'], capture_output=True,
                           text=True, timeout=10)
        if r.stdout != t['stdout'] or r.returncode != t['rc']:
            return False
    return True


def eval_gate(item):
    out = run_learner('gate', item['spec'])
    refused = 'REFUSE' in out
    return {'refused': refused, 'final': refused, 'first': refused,
            'iters': 0, 'znc': 0, 'eclasses': []}


def eval_item(item, max_iters=6):
    if item.get('mode') == 'seed':
        return eval_seed(item, max_iters)
    if item.get('mode') == 'gate':
        return eval_gate(item)
    spec = item['spec']
    if 'REFUSE' in run_learner('gate', spec):
        return {'first': False, 'final': False, 'iters': 0, 'znc': 0,
                'note': 'gate-refused', 'eclasses': []}
    src = run_learner('gen', spec, ALL_PATTERNS, item.get('demo', ''),
                      item.get('card', ''))
    first_src_head = src.strip().split('\n')[0][:80]
    first_ok = final_ok = False
    iters = 0
    eclasses = []
    znc_n = 0
    for it in range(1, max_iters + 1):
        iters = it
        rc, err, bp = compile_src(src, f"{item['id']}_i{it}")
        znc_n += 1
        if rc == 0:
            if run_tests(bp, item['tests']):
                if it == 1:
                    first_ok = True
                final_ok = True
                break
            else:
                break  # test failure, not repairable via compiler
        if it >= max_iters:
            break
        ec = eclass_of(err)
        eclasses.append(ec)
        src = run_learner('repair', ec, details_of(err, ec), src)
    return {'first': first_ok, 'final': final_ok, 'iters': iters,
            'znc': znc_n,
            'gen_head': first_src_head, 'eclasses': eclasses}


def eval_seed(item, max_iters=6):
    # baseline-native T3 protocol from run_full.py::eval_t3
    src = item['seed']
    first_ok = final_ok = False
    iters = 0
    znc_n = 0
    eclasses = []
    attempts = max_iters
    for it in range(1, attempts + 1):
        iters = it
        rc, err, bp = compile_src(src, f"{item['id']}_i{it}")
        znc_n += 1
        if rc == 0:
            if run_tests(bp, item['tests']):
                if it == 1:
                    first_ok = True
                final_ok = True
            break
        if it >= attempts:
            break
        ec = eclass_of(err)
        eclasses.append(ec)
        src = run_learner('repair', ec, details_of(err, ec), src)
    return {'first': first_ok, 'final': final_ok, 'iters': iters,
            'znc': znc_n, 'eclasses': eclasses}


def main():
    battery = json.load(open(sys.argv[1]))['items']
    out_path = sys.argv[2]
    os.makedirs(WORK, exist_ok=True)
    digests = []
    all_reps = []
    for rep in range(1, 6):
        res = {}
        for item in battery:
            res[item['id']] = eval_item(item)
        summ = {k: (v['first'], v['final'], v['iters']) for k, v in res.items()}
        dg = hashlib.sha256(json.dumps(summ, sort_keys=True).encode()).hexdigest()
        digests.append(dg)
        all_reps.append(res)
        n_first = sum(1 for v in res.values() if v['first'])
        n_final = sum(1 for v in res.values() if v['final'])
        print(f"rep {rep}: first {n_first}/{len(battery)} final {n_final}/{len(battery)} digest {dg[:16]}",
              flush=True)
        for iid, v in res.items():
            print(f"   {iid}: first={v['first']} final={v['final']} "
                  f"iters={v['iters']} znc={v.get('znc')} gen={v.get('gen_head', '-')!r} eclasses={v['eclasses']}",
                  flush=True)
    print("digests:", digests, flush=True)
    det = len(set(digests)) == 1
    print("DETERMINISM:", "PASS 5/5 byte-identical" if det else "FAIL", flush=True)
    with open(out_path, 'w') as f:
        json.dump({'reps': all_reps, 'digests': digests,
                   'deterministic': det}, f, indent=1, sort_keys=True)


if __name__ == '__main__':
    main()
