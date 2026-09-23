#!/usr/bin/env python3
"""Fast-loop harness driver — deterministic plumbing ONLY.

The driver makes NO coding decisions. In particular it does NOT:
  - classify compiler errors (no regexes, no keyword scans on stderr),
  - choose repair strategies,
  - edit, patch, or otherwise transform source code,
  - interpret test failures beyond byte comparison.

It invokes the learner binary, writes source files, runs znc, runs test
vectors, and hands evidence to the learner VERBATIM. Every coding
decision (generate / diagnose / revise) lives in learner.zag's
`gen` / `diagnose` modes. The driver contains no error-pattern matching.

Loop protocol per item (budget = max iterations):
  1. gate check via learner (`gate <spec>`); REFUSE -> outcome=gate-refused.
  2. initial source: `gen` output (mode=gen) or the provided seed (mode=seed).
     A gen output starting with a learner-declared failure sentinel
     (UNKNOWN_GOAL / UNTAUGHT: / NEED_CARD: / UNKNOWN_TIER / REFUSED:)
     is routed to `diagnose` as evtype=GEN. Sentinel routing is protocol
     plumbing (like checking a return code), not diagnosis.
  3. per iteration: write source -> znc compile (rc + raw stderr captured
     verbatim) -> run test vectors (stdout/rc compared byte-exact).
     On failure, build the evidence envelope and call
     `diagnose <spec> <src> <evtype> <envelope> <patterns> <demo> <card>`.
  4. parse the DIAG line + @@SRC@@ block. A strategy starting with
     "halt-" stops the loop (the LEARNER decided to stop). A revision
     byte-identical to its input also stops the loop (stall guard).
  5. every step is logged: spec, each source version (sha256), each raw
     evidence blob (sha256), each DIAG line + trace.

Determinism: the driver adds no timestamps, no randomness, no dict-order
dependence to the canonical log. Same battery + same learner binary ->
byte-identical canonical log.
"""
import json, subprocess, sys, os, time, hashlib, shutil

ZNC = '/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1'
LEARNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'learner')
ALL_PATTERNS = "p_math,p_search,p_slice,p_strrev,p_func,p_loop,p_struct,p_sort,p_argv,p_strcnt,p_slicefill"

GEN_SENTINELS = ("UNKNOWN_GOAL", "UNTAUGHT:", "NEED_CARD:", "UNKNOWN_TIER", "REFUSED:")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


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


def run_item(item, budget, workdir, tlog):
    os.makedirs(workdir, exist_ok=True)
    iid = item['id']
    spec = item.get('spec', '')
    patterns = item.get('patterns', ALL_PATTERNS)
    demo = item.get('demo', '')
    card = item.get('card', '')
    t0 = time.monotonic()
    iters = []
    outcome = None

    gate_out = run_learner(['gate', spec])
    if 'REFUSE' in gate_out:
        return {'id': iid, 'mode': item['mode'], 'budget': budget,
                'outcome': 'gate-refused', 'iters_used': 0, 'iters': [],
                'time_s': round(time.monotonic() - t0, 3)}

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

        if gen_failed and it == 1:
            evtype = 'GEN'
            ev = 'GENFAIL %s\n' % src.strip().split('\n')[0][:120] + trailer(prev_class, prev_strat, 0, 0)
            rc, stderr = None, None
        else:
            l0 = time.monotonic()
            rc, stderr = compile_src(src, zag_path, bin_path)
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
        dout = run_learner(['diagnose', spec, src, evtype, ev, patterns, demo, card])
        diag_ms = (time.monotonic() - l0) * 1000
        d, new_src = parse_diag(dout)
        if d is None or new_src is None:
            iters.append({'n': it, 'evtype': evtype, 'result': 'diag-unparseable',
                          'src_sha256': sha(src_bytes),
                          'evidence_sha256': sha(ev.encode('utf-8')),
                          'diag_raw_sha256': sha(dout.encode('utf-8')),
                          'ms': round((time.monotonic() - i0) * 1000, 1)})
            outcome = 'diag-unparseable'
            break

        new_bytes = new_src.encode('utf-8')
        rec = {'n': it, 'evtype': evtype, 'result': 'revised',
               'class': d.get('class', '?'), 'strategy': d.get('strategy', '?'),
               'score': d.get('score', '?'), 'trace': d.get('trace', '?'),
               'src_sha256': sha(src_bytes), 'new_src_sha256': sha(new_bytes),
               'evidence_sha256': sha(ev.encode('utf-8')),
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
            'time_s': round(time.monotonic() - t0, 3)}


def canonical(obj):
    """Canonical JSON for determinism digests: drop wall-clock timings."""
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in sorted(o.items())
                    if k not in ('ms', 'time_s', 'compile_ms', 'test_ms', 'diag_ms')}
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
    args = ap.parse_args()

    with open(args.battery) as bf:
        battery = json.load(bf)
    items = battery['items']
    if args.only:
        want = set(args.only.split(','))
        items = [i for i in items if i['id'] in want]
    results = []
    tlog = []
    for item in items:
        r = run_item(item, args.budget, os.path.join(args.workdir, item['id']), tlog)
        results.append(r)
        print("%-16s budget=%2d iters=%2d outcome=%-18s %.1fs" %
              (r['id'], r['budget'], r['iters_used'], r['outcome'], r['time_s']), flush=True)
    report = {'battery': battery.get('name', ''), 'budget': args.budget,
              'learner': 'learner.zag', 'items': results}
    with open(args.out, 'w') as f:
        json.dump(report, f, indent=1, sort_keys=True)
    print('wrote', args.out, 'digest', sha(canonical(report).encode()))


if __name__ == '__main__':
    main()
