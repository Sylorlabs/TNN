#!/usr/bin/env python3
"""Q3 battery runner — deterministic plumbing replicating driver.repair_task.
Imports eclass_of/details_of/run_learner/compile_src/run_tests from driver.py.
No classification or repair decisions here; all in driver.py + learner.zag.
"""
import sys, os, json, hashlib, subprocess
sys.path.insert(0, '/home/hatch/workspace/tnn-lab/coding')
from driver import eclass_of, details_of, run_learner, compile_src, run_tests

LEARNER = '/home/hatch/workspace/tnn-lab/coding/src/learner'
BB = '/home/hatch/workspace/tnn-lab/coding/bug-blindness'
os.makedirs(f'{BB}/logs', exist_ok=True)

def repair_loop(src, tests, max_iters=6):
    """Exact replica of driver.repair_task. Returns (ok, iters, log, final_src)."""
    log = []
    iters = 0
    for it in range(1, max_iters + 1):
        iters = it
        rc, err = compile_src(src, '/tmp/q3_bin')
        if rc == 0:
            ok, msg = run_tests('/tmp/q3_bin', tests)
            if ok:
                return True, iters, log + [f"attempt{it}: PASS"], src
            else:
                return False, iters, log + [f"attempt{it}: test FAIL {msg}"], src
        eclass = eclass_of(err)
        details = details_of(err, eclass)
        log.append(f"attempt{it}: {eclass} {details}")
        if it >= max_iters:
            return False, iters, log, src
        src, _, _ = run_learner('repair', eclass, details, src)
    return False, iters, log, src

def t(stdout):
    return [{'args': [], 'stdout': stdout, 'rc': 0}]

Q3A = [
 ("e1", "E0203",
  'fn label()i64 {\n  return "forty-two";\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(label()));\n  _zag_print("\\n");\n}\n',
  t("42\n")),
 ("e2", "E0203",
  'fn main()void {\n  let x:i64=7;\n  x = "oops";\n  _zag_print(_zag_i64_to_str(x));\n  _zag_print("\\n");\n}\n',
  t("7\n")),
 ("u1", "UNKNOWNFN",
  'fn main()void {\n  prnit("hi\\n");\n}\n',
  t("hi\n")),
 ("u2", "UNKNOWNFN",
  'fn add(a:i64, b:i64)i64 {\n  return a+b;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(add(ad(1,2),3)));\n  _zag_print("\\n");\n}\n',
  t("6\n")),
 ("a1", "ARITY",
  'fn add3(a:i64, b:i64, c:i64)i64 {\n  return a+b+c;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(add3(7)));\n  _zag_print("\\n");\n}\n',
  t("24\n")),
 ("a2", "ARITY",
  'fn cat2(a:[]u8, b:[]u8)i64 {\n  return 7;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(cat2("x")));\n  _zag_print("\\n");\n}\n',
  t("7\n")),
 ("p1", "PARSE",
  'fn main()void {\n  _zag_print("hi\\n");\n',
  t("hi\n")),
 ("p2", "PARSE",
  'fn f(n:i64)i64 {\n  let r:i64=0;\n  while(n>0) {\n    r=r+n;\n    n=n-1;\n  return r;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(f(3)));\n  _zag_print("\\n");\n}\n',
  t("6\n")),
 ("d1", "DUPFN",
  'fn val()i64 {\n  return 1;\n}\nfn val()i64 {\n  return 2;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(val()));\n  _zag_print("\\n");\n}\n',
  t("2\n")),
 ("d2", "DUPFN",
  'fn dbl(n:i64)i64 {\n  return n*2;\n}\nfn dbl(x:i64)i64 {\n  return x*2;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(dbl(21)));\n  _zag_print("\\n");\n}\n',
  t("42\n")),
]

T3SRC = {t['id']: t for t in json.load(
    open('/home/hatch/workspace/tnn-lab/coding/curriculum/curriculum.json'))['t3']}
Q3B = [
 ("b1", "m-arity-few", "E0203", ""),
 ("b2", "m-type-let", "ARITY", "x:1:2"),
 ("b3", "m-brace", "DUPFN", "main"),
 ("b4", "m-dup-fn", "PARSE", ""),
 ("b5", "m-unknown-call", "E0203", ""),
]

Q3C = [
 ("c1", 'fn main()void {\n  _zag_print(_zag_i64_to_str(y));\n  _zag_print("\\n");\n}\n', t("5\n")),
 ("c2", 'struct Point { x:i64, y:i64 }\nfn main()void {\n  let p:Point=Point{};\n  p.x=3;\n  p.z=4;\n  _zag_print(_zag_i64_to_str(p.x));\n  _zag_print("\\n");\n}\n', t("3\n")),
 ("c3", 'fn f()i64 {\n  return 3;\n}\n', t("3\n")),
 ("c4", 'struct P { x:i64 }\nstruct P { x:i64 }\nfn main()void {\n  _zag_print("hi\\n");\n}\n', t("hi\n")),
]

def main():
    report = {'q3a': {}, 'q3b': {}, 'q3c': {}}
    logf = open(f'{BB}/logs/q3_run.log', 'w')

    def log(s):
        logf.write(s + "\n"); logf.flush(); print(s, flush=True)

    log("=== Q3a pre-verification: each item fails to compile with claimed class ===")
    for iid, claimed, src, tests in Q3A:
        rc, err = compile_src(src, '/tmp/q3_bin')
        got = eclass_of(err) if rc != 0 else "COMPILED"
        firstline = next((l for l in err.splitlines() if 'error' in l or 'E0001' in l), '')
        status = "OK" if got == claimed else "MISMATCH"
        log(f"  {iid}: claimed={claimed} got={got} [{status}] :: {firstline[:110]}")
        report['q3a'][iid] = {'claimed': claimed, 'actual': got,
                              'errline': firstline, 'precheck': status}

    log("=== Q3a scored runs: 5 reps each ===")
    for iid, claimed, src, tests in Q3A:
        oks, digests, iters_list = [], [], []
        for rep in range(5):
            ok, iters, rlog, final = repair_loop(src, tests)
            oks.append(ok); iters_list.append(iters)
            digests.append(hashlib.sha256(final.encode()).hexdigest()[:16])
        det = "IDENTICAL" if len(set(digests)) == 1 else "DIFFER"
        res = sum(oks)
        log(f"  {iid}: repaired {res}/5 reps, iters={iters_list}, digests {det} {digests[0]}")
        report['q3a'][iid].update({'repaired': res, 'iters': iters_list,
                                   'digests': digests, 'deterministic': det})

    log("=== Q3b mislabel probe: repair mode directly ===")
    for iid, t3id, wrong_eclass, wrong_details in Q3B:
        item = T3SRC[t3id]
        out, _, _ = run_learner('repair', wrong_eclass, wrong_details, item['broken'])
        rc, err = compile_src(out, '/tmp/q3_bin')
        recovers = False
        if rc == 0:
            ok, _ = run_tests('/tmp/q3_bin', item['tests'])
            recovers = ok
        changed = "CHANGED" if out != item['broken'] else "UNCHANGED"
        log(f"  {iid}: true={t3id} wronglabel={wrong_eclass}/{wrong_details} -> {changed} recovers={recovers}")
        report['q3b'][iid] = {'true': t3id, 'wrong_eclass': wrong_eclass,
                              'changed': changed, 'recovers': recovers}

    log("=== Q3c novel-class probe ===")
    for iid, src, tests in Q3C:
        rc0, err0 = compile_src(src, '/tmp/q3_bin')
        e0 = eclass_of(err0)
        ok, iters, rlog, final = repair_loop(src, tests)
        rc1, err1 = compile_src(final, '/tmp/q3_bin')
        log(f"  {iid}: eclass={e0} repaired={ok} iters={iters} log={rlog}")
        report['q3c'][iid] = {'eclass': e0, 'repaired': ok, 'iters': iters,
                              'log': rlog}

    n_a = sum(1 for v in report['q3a'].values() if v.get('repaired', 0) >= 3)
    n_b = sum(1 for v in report['q3b'].values() if v['recovers'])
    n_c = sum(1 for v in report['q3c'].values() if v['repaired'])
    log(f"=== SUMMARY: Q3a {n_a}/10 repaired (KB-R1 bar >=7) | Q3b {n_b}/5 recover (KB-R2: 0/5=confirmed) | Q3c {n_c}/4 recover ===")
    report['summary'] = {'q3a_repaired': n_a, 'q3b_recover': n_b, 'q3c_recover': n_c,
                         'kb_r1': 'PASS' if n_a >= 7 else 'FAIL',
                         'kb_r2': 'CONFIRMED' if n_b == 0 else 'NOT-CONFIRMED'}
    json.dump(report, open(f'{BB}/logs/q3_report.json', 'w'), indent=2)
    logf.close()

if __name__ == '__main__':
    main()
