#!/usr/bin/env python3
"""Task-1 challenger driver — deterministic plumbing ONLY.

The driver makes NO coding decisions. In particular it does NOT:
  - classify compiler errors (no regexes, no keyword scans on stderr),
  - choose repair strategies,
  - edit, patch, or otherwise transform source code,
  - interpret test failures beyond byte comparison.

It invokes the challenger learner binary, writes source files, runs znc,
runs test vectors, and hands evidence to the learner VERBATIM. Every coding
decision (generate / diagnose / revise / halt) lives in the learner's
`gen` / `diagnose` / `gate` modes.

Learner protocol (challenger):
  gate <spec>                                     -> ALLOW | REFUSE:G<n>
  gen <spec> <store> <demo>                       -> Zag source | sentinel
  diagnose <spec> <src> <evtype> <evidence> <demo> <store>
       -> DIAG class=.. strategy=.. score=.. trace=..
          @@SRC@@
          <revised source>
          @@END@@

Loop per item (budget = max iterations, set by caller):
  1. mode=gate: gate check IS the item; pass iff output starts with REFUSE.
  2. mode=gen: gate check; REFUSE -> outcome gate-refused.
     gen output starting with a sentinel (UNKNOWN_GOAL / UNKNOWN_TIER /
     REFUSED:) is routed to diagnose as evtype=GEN (protocol plumbing).
  3. mode=seed: the provided seed is iteration 0 (no gate; a broken program
     is not a request).
  4. per iteration: write source -> znc compile (rc + raw stderr verbatim)
     -> run test vectors (stdout/rc byte-compared).
  5. on failure: build the evidence envelope, call diagnose, parse DIAG +
     @@SRC@@. A strategy starting with "halt-" stops the loop (the LEARNER
     decided). A revision byte-identical to its input also stops the loop
     (stall guard, belt and braces).
  6. every step is logged; the canonical log drops wall-clock timings.

Determinism: no timestamps, no randomness, no dict-order dependence in the
canonical log. Same battery + same learner binary + same store -> byte-
identical canonical log.
"""
import json, subprocess, sys, os, time, hashlib

ZNC = '/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1'
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)

GEN_SENTINELS = ("UNKNOWN_GOAL", "UNKNOWN_TIER", "REFUSED:")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def esc(b: bytes) -> str:
    return b.replace(b'\\', b'\\\\').replace(b'\r', b'\\r').replace(b'\n', b'\\n').decode('ascii', 'backslashreplace')


def run_learner(learner, args, timeout=60):
    r = subprocess.run([learner] + args, capture_output=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def parse_diag(out: bytes):
    """Return (class, strategy, score, trace, new_src) or None."""
    try:
        text = out.decode('utf-8')
    except UnicodeDecodeError:
        return None
    lines = text.split('\n')
    dclass = strategy = trace = None
    score = None
    for ln in lines:
        if ln.startswith('DIAG '):
            parts = ln[5:].split(' ')
            kv = {}
            for p in parts:
                if '=' in p:
                    k, v = p.split('=', 1)
                    kv[k] = v
            dclass = kv.get('class')
            strategy = kv.get('strategy')
            trace = kv.get('trace')
            try:
                score = int(kv.get('score', '0'))
            except ValueError:
                score = 0
            break
    if dclass is None or strategy is None:
        return None
    si = text.find('@@SRC@@\n')
    ei = text.find('\n@@END@@')
    if si < 0 or ei < 0 or ei < si:
        return None
    new_src = text[si + len('@@SRC@@\n'):ei]
    return dclass, strategy, score, trace, new_src


def run_item(learner, store, item, workdir, budget):
    iid = item['id']
    mode = item['mode']
    t0 = time.time()
    iters = []
    znc_calls = 0

    def log(**kw):
        iters.append(kw)

    if mode == 'gate':
        spec = item.get('spec', '')
        rc, out, err = run_learner(learner, ['gate', spec])
        refused = out.decode('utf-8', 'replace').startswith('REFUSE')
        return {'id': iid, 'tier': item['tier'], 'mode': mode,
                'outcome': 'pass' if refused else 'fail-gate-allowed',
                'iters_used': 0, 'znc_calls': 0,
                'iterations': iters, 'time_s': round(time.time() - t0, 3)}

    if mode == 'gen':
        spec = item.get('spec', '')
        demo = item.get('demo', '')
        rc, out, err = run_learner(learner, ['gate', spec])
        if out.decode('utf-8', 'replace').startswith('REFUSE'):
            return {'id': iid, 'tier': item['tier'], 'mode': mode,
                    'outcome': 'gate-refused', 'iters_used': 0,
                    'znc_calls': 0, 'iterations': iters,
                    'time_s': round(time.time() - t0, 3)}
        rc, out, err = run_learner(learner, ['gen', spec, store, demo])
        src = out.decode('utf-8')
        if src.startswith(GEN_SENTINELS):
            ev = 'GENFAIL %s\nPREV none/none\nSTALLED 0\nCYCLE 0\n' % src.split('\n')[0]
            d = run_learner(learner, ['diagnose', spec, src, 'GEN', ev, demo, store])[1]
            p = parse_diag(d)
            outcome = 'halt-genfail' if p and p[1].startswith('halt-') else 'diag-unparseable'
            log(n=0, evtype='GEN', outcome=outcome, diag=p[0] + '/' + p[1] if p else None)
            return {'id': iid, 'tier': item['tier'], 'mode': mode,
                    'outcome': outcome, 'iters_used': 0, 'znc_calls': 0,
                    'iterations': iters, 'time_s': round(time.time() - t0, 3)}
    elif mode == 'seed':
        spec = ''
        demo = ''
        src = item['seed']
    else:
        raise ValueError('unknown mode ' + mode)

    seen = set()
    prev = 'none/none'
    prev_src_hash = None
    outcome = 'budget-exhausted'
    src_path = os.path.join(workdir, iid + '.zag')
    bin_path = os.path.join(workdir, iid + '.bin')

    for it in range(1, budget + 1):
        src_bytes = src.encode('utf-8')
        src_hash = sha(src_bytes)
        stalled = 1 if prev_src_hash == src_hash else 0
        prev_src_hash = src_hash
        # write source (truncating)
        with open(src_path, 'wb') as f:
            f.write(src_bytes)
        # compile
        cr = subprocess.run([ZNC, src_path, '-o', bin_path, '--no-analyze'],
                            capture_output=True, timeout=120)
        znc_calls += 1
        c_rc = cr.returncode
        c_err = cr.stderr
        if c_rc != 0 or not os.path.exists(bin_path):
            ev = ('RC %d\n' % c_rc) + c_err.decode('utf-8', 'replace')
            evtype = 'COMPILE'
            fail = True
            got_out = b''
            got_rc = c_rc
        else:
            fail = False
            got_out = b''
            got_rc = 0
            first_fail = None
            for t in item['tests']:
                args = t.get('args', [])
                try:
                    rr = subprocess.run([bin_path] + args, capture_output=True, timeout=10)
                except subprocess.TimeoutExpired:
                    rr = None
                if rr is None:
                    first_fail = (t, -99, b'', b'TIMEOUT')
                    break
                exp_out = t['stdout'].encode('utf-8')
                exp_rc = t.get('rc', 0)
                if rr.stdout != exp_out or rr.returncode != exp_rc:
                    first_fail = (t, rr.returncode, rr.stdout, rr.stderr)
                    break
            if first_fail is not None:
                t, got_rc, got_out, got_err = first_fail
                ev = ('COMPILE_OK\nGOT_RC %d\nEXP_RC %d\nGOT_ERR %s\nGOT_OUT %s\nEXP_OUT %s\n'
                      % (got_rc, t.get('rc', 0), esc(got_err), esc(got_out),
                         esc(t['stdout'].encode('utf-8'))))
                evtype = 'TEST'
                fail = True

        if not fail:
            outcome = 'pass'
            log(n=it, evtype='OK', src_sha256=src_hash, znc_rc=c_rc)
            break

        cyc = 1 if src_hash in seen else 0
        seen.add(src_hash)
        ev_full = ev + 'PREV %s\nSTALLED %d\nCYCLE %d\n' % (prev, stalled, cyc)
        # Determinism (INTERFACE.md evidence-envelope rule): fold the
        # run-specific workdir to its basename inside the envelope. The
        # filename and all diagnostic content are preserved; only the
        # directory, which varies per repetition workdir, is folded.
        # Applied to the whole envelope (COMPILE/TEST/GEN) uniformly.
        _bn = os.path.basename(os.path.abspath(workdir))
        for _wd in (workdir, os.path.abspath(workdir)):
            ev_full = ev_full.replace(_wd, _bn)
        rc, d_out, d_err = run_learner(
            learner, ['diagnose', spec, src, evtype, ev_full, demo, store])
        p = parse_diag(d_out)
        if p is None:
            outcome = 'diag-unparseable'
            log(n=it, evtype=evtype, src_sha256=src_hash,
                evidence_sha256=sha(ev_full.encode('utf-8')),
                outcome=outcome)
            break
        dclass, strategy, score, trace, new_src = p
        new_hash = sha(new_src.encode('utf-8'))
        log(n=it, evtype=evtype, src_sha256=src_hash,
            evidence_sha256=sha(ev_full.encode('utf-8')),
            diag_class=dclass, diag_strategy=strategy, diag_score=score,
            diag_trace=trace, new_src_sha256=new_hash)
        prev = dclass + '/' + strategy
        if strategy.startswith('halt-'):
            outcome = strategy
            break
        if new_hash == src_hash:
            outcome = 'stall-guard-halt'
            break
        src = new_src
    else:
        pass

    return {'id': iid, 'tier': item['tier'], 'mode': mode,
            'outcome': outcome, 'iters_used': len(iters),
            'znc_calls': znc_calls, 'iterations': iters,
            'time_s': round(time.time() - t0, 3)}


def canonical(rec):
    r = dict(rec)
    r.pop('time_s', None)
    for it in r.get('iterations', []):
        it.pop('time_s', None)
    return r


def main():
    learner = sys.argv[1]
    store = sys.argv[2]
    battery = sys.argv[3]
    out_path = sys.argv[4]
    budget = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    workdir = sys.argv[6] if len(sys.argv) > 6 else os.path.join(HERE, 'work', 'run')
    os.makedirs(workdir, exist_ok=True)
    items = json.load(open(battery))['items']
    results = []
    for item in items:
        results.append(run_item(learner, store, item, workdir, budget))
        sys.stderr.write('%s %s\n' % (item['id'], results[-1]['outcome']))
        sys.stderr.flush()
    canon = [canonical(r) for r in results]
    blob = json.dumps(canon, sort_keys=True, indent=1).encode('utf-8')
    with open(out_path, 'wb') as f:
        f.write(blob)
    digest = sha(blob)
    with open(out_path + '.sha256', 'w') as f:
        f.write(digest + '\n')
    # human summary table
    tiers = {}
    for r in results:
        t = tiers.setdefault(r['tier'], {'n': 0, 'pass': 0, 'iters': 0, 'znc': 0})
        t['n'] += 1
        if r['outcome'] == 'pass':
            t['pass'] += 1
        t['iters'] += r['iters_used']
        t['znc'] += r['znc_calls']
    print('tier items pass iters znc')
    for t in sorted(tiers):
        v = tiers[t]
        print(t, v['n'], v['pass'], v['iters'], v['znc'])
    print('CANONICAL_SHA256', digest)


if __name__ == '__main__':
    main()
