#!/usr/bin/env python3
"""QB coding driver — deterministic plumbing ONLY (variant of driver_si4.py).

Same law as the original: the driver makes NO coding decisions. It does NOT
classify errors, choose repairs, edit code, or interpret test failures beyond
byte comparison. QB additions vs driver_si4.py:

- `--mech {none,a,b,c}` selects the Arm 3 mechanism under test. The mech tag
  is passed to the learner's `diagnose` as argv[9] (mask) — a fixed
  experiment constant, like --budget. The driver never branches on error
  content.
- `--qbmode {d0..d5}` selects the QB deliberation structure. It is passed to
  the learner's `diagnose` as argv[10] — a fixed experiment constant, like
  --mech. The driver never branches on error content; all deliberation
  structure lives inside the learner (learner_qb.zag).
- `--mech c` (3c fail-fast precheck): before each znc invocation the driver
  asks the LEARNER (`precheck <spec> <src>`) whether the source will compile.
  Routing is sentinel-style (first output line only, like GEN_SENTINELS /
  a return code): `PRECHECK FAIL` -> diagnose with evtype=PRECHECK, skipping
  znc; `PRECHECK OK` -> compile as usual. The reason text travels VERBATIM
  into the evidence envelope. Every precheck-FAIL source is logged to
  <out>.fp_candidates.jsonl for post-hoc false-positive validation
  (compiled separately; those validation invocations are NOT counted in
  the loop's znc cost).
- Per-iteration records add: `znc` (1/0), `precheck` (ok/fail/n/a[-gen]),
  `evals` (learner-reported hypothesis-evaluations).

Verify the no-classification law with the INTERFACE.md grep (compiler
error-code and stderr-phrase patterns): it must hit nothing in this file
outside comments and docstrings.
"""

import json, subprocess, sys, os, time, hashlib, shutil, resource

ZNC = '/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1'
LEARNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', 'learner_qb')
ALL_PATTERNS = "p_math,p_search,p_slice,p_strrev,p_func,p_loop,p_struct,p_sort,p_argv,p_strcnt,p_slicefill"

GEN_SENTINELS = ("UNKNOWN_GOAL", "UNTAUGHT:", "NEED_CARD:", "UNKNOWN_TIER", "REFUSED:")

# SI Arm 4 mechanism selection (experiment plumbing, not error classification):
#   none  -> si4 binary, mask "", no precheck (baseline-behavior sanity cell)
#   a/b/c -> as in driver_si.py (transfer re-check cells)
#   combo -> mask "ab" (3a prune + 3b B&B over pruned set) + 3c precheck routing
#   none -> si3 binary, mask "", no precheck  (baseline-behavior sanity cell)
#   a    -> 3a prune provably-dead branches (diagnose mask "a")
#   b    -> 3b one-brain branch-and-bound   (diagnose mask "b")
#   c    -> 3c fail-fast precheck (precheck before every znc invocation)
MECH_MASK = {'none': '', 'a': 'a', 'b': 'b', 'c': '', 'combo': 'ab'}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def child_cpu(ru0):
    # CPU seconds consumed by child processes (learner, znc, test binaries)
    ru1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return round((ru1.ru_utime - ru0.ru_utime) + (ru1.ru_stime - ru0.ru_stime), 3)


def run_learner(args, timeout=30):
    r = subprocess.run([LEARNER] + args, capture_output=True, timeout=timeout)
    return r.stdout.decode('utf-8', errors='replace')


def esc(b: bytes) -> str:
    # lossless byte escaping for envelope fields
    return b.replace(b'\\', b'\\\\').replace(b'\r', b'\\r').replace(b'\n', b'\\n').decode('ascii')


def compile_src(src_text: str, zag_path: str, bin_path: str):
    # plain truncating write (O_TRUNC semantics); never O_EXCL
    with open(zag_path, 'w') as f:
        f.write(src_text)
    r = subprocess.run([ZNC, zag_path, '-o', bin_path, '--no-analyze', '--no-zagd'],
                       capture_output=True, timeout=60)
    err = r.stderr.decode('utf-8', errors='replace')
    # determinism normalization (plumbing): znc echoes the source path in
    # diagnostics; the run-specific directory carries no diagnostic content,
    # so fold it to the stable basename before logging / handing to learner.
    err = err.replace(zag_path, os.path.basename(zag_path))
    return r.returncode, err


def run_tests(bin_path: str, tests):
    """Byte-exact test harness. Returns (ok, failure_dict|None)."""
    for ti, t in enumerate(tests):
        try:
            r = subprocess.run([bin_path] + t['args'], capture_output=True, timeout=10)
        except Exception as e:
            return False, {'idx': ti, 'error': 'harness-exception: %s' % e,
                           'got_rc': 'EXC', 'got_out': b'', 'got_err': b'',
                           'exp_rc': t['rc'], 'exp_out': t['stdout'].encode()}
        exp_out = t['stdout'].encode('utf-8')
        if r.stdout != exp_out or r.returncode != t['rc']:
            return False, {'idx': ti, 'got_rc': r.returncode, 'got_out': r.stdout,
                           'got_err': r.stderr, 'exp_rc': t['rc'], 'exp_out': exp_out}
    return True, None


def parse_diag(out: str):
    """Parse learner diagnose output -> (diag dict, revised source)."""
    lines = out.split('\n')
    if not lines or not lines[0].startswith('DIAG '):
        return None, None
    head = lines[0]
    d = {}
    for tok in head[5:].split(' '):
        if '=' in tok:
            k, v = tok.split('=', 1)
            d[k] = v
    try:
        si = lines.index('@@SRC@@')
        ei = lines.index('@@END@@')
    except ValueError:
        return None, None
    src = '\n'.join(lines[si + 1:ei]) + '\n'
    return d, src


def trailer(prev_class, prev_strat, stalled, cycle):
    return "PREV %s/%s\nSTALLED %d\nCYCLE %d\n" % (prev_class, prev_strat, stalled, cycle)


def run_precheck(spec, src):
    """Ask the LEARNER whether src will compile. Returns (ok, reason_text).

    Sentinel-style routing (like GEN_SENTINELS): the driver only checks the
    first output line, exactly as it checks a return code. The reason text
    is passed VERBATIM to diagnose as the evidence envelope; the driver
    classifies nothing.
    """
    out = run_learner(['precheck', spec, src])
    lines = out.split('\n')
    if lines and lines[0] == 'PRECHECK FAIL':
        return False, '\n'.join(lines[1:])
    return True, ''


def run_item(item, budget, workdir, tlog, mech, fp_log, stats, qbmode):
    mask = MECH_MASK[mech]
    use_precheck = (mech == 'c' or mech == 'combo')
    os.makedirs(workdir, exist_ok=True)
    iid = item['id']
    spec = item.get('spec', '')
    patterns = item.get('patterns', ALL_PATTERNS)
    demo = item.get('demo', '')
    card = item.get('card', '')
    t0 = time.monotonic()
    ru0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    iters = []
    outcome = None

    gate_out = run_learner(['gate', spec])
    if 'REFUSE' in gate_out:
        return {'id': iid, 'mode': item['mode'], 'budget': budget,
                'outcome': 'gate-refused', 'iters_used': 0, 'iters': [],
                'time_s': round(time.monotonic() - t0, 3),
                'cpu_s': child_cpu(ru0)}

    if item['mode'] == 'gen':
        src = run_learner(['gen', spec, patterns, demo, card])
        gen_failed = src.startswith(GEN_SENTINELS)
    else:
        src = item['seed']
        gen_failed = False

    src_bytes = src.encode('utf-8')
    seen = {sha(src_bytes)}
    prev_src_bytes = None
    prev_class, prev_strat = 'none', 'none'

    for it in range(1, budget + 1):
        i0 = time.monotonic()
        compile_ms, test_ms = 0, 0
        zag_path = os.path.join(workdir, '%s_i%d.zag' % (iid, it))
        bin_path = os.path.join(workdir, '%s_i%d.bin' % (iid, it))

        zag_path = os.path.join(workdir, '%s_i%d.zag' % (iid, it))
        bin_path = os.path.join(workdir, '%s_i%d.bin' % (iid, it))

        # 3c fail-fast precheck: the LEARNER predicts compile failure from
        # the source alone (brace balance, defined names, dup defs, arity).
        # Sentinel routing only: first output line decides the branch.
        precheck_ok, precheck_reason = True, ''
        if use_precheck and not (gen_failed and it == 1):
            stats['precheck_calls'] += 1
            precheck_ok, precheck_reason = run_precheck(spec, src)

        if gen_failed and it == 1:
            evtype = 'GEN'
            ev = 'GENFAIL %s\n' % src.strip().split('\n')[0][:120] + trailer(prev_class, prev_strat, 0, 0)
            rc, stderr = None, None
            precheck_status = 'n/a-gen'
            znc_invoked = 0
        elif use_precheck and not precheck_ok:
            # learner predicts compile failure: route straight to diagnose
            # with evtype=PRECHECK, skipping the znc invocation.
            evtype = 'PRECHECK'
            ev = precheck_reason + trailer(prev_class, prev_strat, 0, 0)
            rc, stderr = None, None
            precheck_status = 'fail'
            znc_invoked = 0
            stats['precheck_fail'] += 1
            fp_log.append({'id': iid, 'iter': it, 'src': src})
        else:
            precheck_status = 'ok' if use_precheck else 'n/a'
            l0 = time.monotonic()
            rc, stderr = compile_src(src, zag_path, bin_path)
            stats['znc_invocations'] += 1
            znc_invoked = 1
            compile_ms = (time.monotonic() - l0) * 1000
            if rc == 0:
                l0 = time.monotonic()
                ok, fail = run_tests(bin_path, item['tests'])
                test_ms = (time.monotonic() - l0) * 1000
                if ok:
                    iters.append({'n': it, 'evtype': 'NONE', 'result': 'pass',
                                  'src_sha256': sha(src_bytes),
                                  'compile_ms': round(compile_ms, 1),
                                  'test_ms': round(test_ms, 1),
                                  'znc': 1, 'precheck': precheck_status,
                                  'ms': round((time.monotonic() - i0) * 1000, 1)})
                    outcome = 'pass'
                    break
                stalled = 1 if (prev_src_bytes is not None and src_bytes == prev_src_bytes) else 0
                cycle = 1 if sha(src_bytes) in seen and it > 1 else 0
                # note: src was added to seen at end of previous iteration,
                # so membership here means a genuine revisit
                ev = ("COMPILE_OK\nGOT_RC %s\nEXP_RC %s\nGOT_ERR %s\nGOT_OUT %s\nEXP_OUT %s\n"
                      % (fail['got_rc'], fail['exp_rc'], esc(fail['got_err']),
                         esc(fail['got_out']), esc(fail['exp_out'])))
                ev += trailer(prev_class, prev_strat, stalled, cycle)
                evtype = 'TEST'
            else:
                test_ms = 0
                stalled = 1 if (prev_src_bytes is not None and src_bytes == prev_src_bytes) else 0
                cycle = 1 if sha(src_bytes) in seen and it > 1 else 0
                ev = "RC %d\n%s" % (rc, stderr) + trailer(prev_class, prev_strat, stalled, cycle)
                evtype = 'COMPILE'

        l0 = time.monotonic()
        dout = run_learner(['diagnose', spec, src, evtype, ev, patterns, demo, card, mask, qbmode])
        diag_ms = (time.monotonic() - l0) * 1000
        d, new_src = parse_diag(dout)
        if d is None or new_src is None:
            iters.append({'n': it, 'evtype': evtype, 'result': 'diag-unparseable',
                          'src_sha256': sha(src_bytes),
                          'evidence_sha256': sha(ev.encode('utf-8')),
                          'diag_raw_sha256': sha(dout.encode('utf-8')),
                          'znc': znc_invoked, 'precheck': precheck_status,
                          'ms': round((time.monotonic() - i0) * 1000, 1)})
            outcome = 'diag-unparseable'
            break

        new_bytes = new_src.encode('utf-8')
        rec = {'n': it, 'evtype': evtype, 'result': 'revised',
               'class': d.get('class', '?'), 'strategy': d.get('strategy', '?'),
               'score': d.get('score', '?'), 'evals': d.get('evals', '?'),
               'trace': d.get('trace', '?'),
               'src_sha256': sha(src_bytes), 'new_src_sha256': sha(new_bytes),
               'evidence_sha256': sha(ev.encode('utf-8')),
               'znc': znc_invoked, 'precheck': precheck_status,
               'ms': round((time.monotonic() - i0) * 1000, 1)}
        if evtype == 'COMPILE':
            rec['compile_ms'] = round(compile_ms, 1)
        else:
            rec['test_ms'] = round(test_ms, 1)
        rec['diag_ms'] = round(diag_ms, 1)
        iters.append(rec)

        strat = d.get('strategy', '')
        if strat.startswith('halt-'):
            outcome = strat  # the LEARNER decided to stop
            break
        if new_bytes == src_bytes:
            outcome = 'stall-guard-halt'  # belt and braces; learner should halt itself
            break
        seen.add(sha(src_bytes))
        prev_src_bytes = src_bytes
        src, src_bytes = new_src, new_bytes
        prev_class, prev_strat = d.get('class', '?'), strat
        gen_failed = False

    if outcome is None:
        outcome = 'budget-exhausted'
    return {'id': iid, 'mode': item['mode'], 'budget': budget, 'outcome': outcome,
            'iters_used': len(iters), 'iters': iters,
            'time_s': round(time.monotonic() - t0, 3),
            'cpu_s': child_cpu(ru0)}


def canonical(obj):
    """Canonical JSON for determinism digests: drop wall-clock timings."""
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in sorted(o.items())
                    if k not in ('ms', 'time_s', 'cpu_s', 'compile_ms', 'test_ms', 'diag_ms')}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    return json.dumps(strip(obj), sort_keys=True, separators=(',', ':'))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('battery')
    ap.add_argument('--budget', type=int, default=6)
    ap.add_argument('--workdir', default='work/run')
    ap.add_argument('--out', default='work/run.json')
    ap.add_argument('--only', default='')
    ap.add_argument('--mech', default='none', choices=['none', 'a', 'b', 'c', 'combo'],
                    help='mechanism: none (sanity), a (3a prune), b (3b bnb), '
                         'c (3c precheck), combo (3a+3b+3c)')
    ap.add_argument('--qbmode', default='d0', choices=['d0', 'd1', 'd2', 'd3', 'd4', 'd5'],
                    help='QB deliberation structure (plumbing only; the learner '
                         'selects the diagnose path)')
    args = ap.parse_args()

    with open(args.battery) as bf:
        battery = json.load(bf)
    items = battery['items']
    if args.only:
        want = set(args.only.split(','))
        items = [i for i in items if i['id'] in want]
    results = []
    tlog = []
    fp_log = []  # every precheck-FAIL source, for post-hoc false-positive validation
    stats = {'znc_invocations': 0, 'precheck_calls': 0, 'precheck_fail': 0}
    for item in items:
        r = run_item(item, args.budget, os.path.join(args.workdir, item['id']), tlog,
                     args.mech, fp_log, stats, args.qbmode)
        results.append(r)
        print("%-16s budget=%2d iters=%2d outcome=%-18s %.1fs" %
              (r['id'], r['budget'], r['iters_used'], r['outcome'], r['time_s']), flush=True)
    report = {'battery': battery.get('name', ''), 'budget': args.budget,
              'learner': 'learner_qb.zag', 'mech': args.mech, 'qbmode': args.qbmode,
              'stats': stats, 'items': results}
    with open(args.out, 'w') as f:
        json.dump(report, f, indent=1, sort_keys=True)
    if fp_log:
        fp_path = args.out + '.fp_candidates.jsonl'
        with open(fp_path, 'w') as f:
            for e in fp_log:
                f.write(json.dumps(e) + '\n')
        print('wrote', fp_path, '(%d precheck-fail sources)' % len(fp_log))
    print('wrote', args.out, 'digest', sha(canonical(report).encode()),
          'znc_invocations', stats['znc_invocations'],
          'precheck', '%d/%d' % (stats['precheck_fail'], stats['precheck_calls']))


if __name__ == '__main__':
    main()
