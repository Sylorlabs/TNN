#!/usr/bin/env python3
"""Task 2 (synth probe) driver — deterministic plumbing ONLY.

Follows the same loop protocol as coding/reflection/loop/driver.py, but
scores emitted WAV FILES (byte-exact vs frozen oracle) instead of stdout.

The driver makes NO coding decisions. It does NOT classify failures,
choose repairs, or interpret sample values. It:
  - invokes the learner (gate / gen / diagnose),
  - compiles with the pinned znc,
  - runs the binary 3x (vectors 1/2/3) to produce WAV files,
  - byte-compares each against the frozen oracle WAV,
  - hands the first failing vector's facts (lengths, header match,
    first-differing byte, decoded i16 samples around it) to the learner
    VERBATIM as evidence.

Separation: this is a coding-capability probe only. Outputs are judged by
byte-exact comparison to the frozen oracle, never played or scored as audio.
"""
import json, subprocess, sys, os, hashlib, struct

ZNC = '/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1'
HERE = os.path.dirname(os.path.abspath(__file__))
TASK2 = os.path.dirname(HERE)
LEARNER = os.path.join(TASK2, 'work', 'learner')
ORACLE_DIR = os.path.join(TASK2, 'oracle')

GEN_SENTINELS = ("UNKNOWN_GOAL", "UNTAUGHT:", "NEED_CARD:", "UNKNOWN_TIER", "REFUSED:")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run_learner(args, timeout=60):
    r = subprocess.run([LEARNER] + args, capture_output=True, timeout=timeout)
    return r.stdout.decode('utf-8', errors='replace')


def compile_src(src_text: str, zag_path: str, bin_path: str):
    with open(zag_path, 'w') as f:
        f.write(src_text)
    r = subprocess.run([ZNC, zag_path, '-o', bin_path, '--no-analyze', '--no-zagd'],
                       capture_output=True, timeout=120)
    err = r.stderr.decode('utf-8', errors='replace')
    err = err.replace(zag_path, os.path.basename(zag_path))
    return r.returncode, err


def parse_diag(out: str):
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


def compare_wav(got_path, exp_path):
    """Byte-exact WAV comparison. Returns a fact dict (no interpretation)."""
    with open(got_path, 'rb') as f:
        got = f.read()
    with open(exp_path, 'rb') as f:
        exp = f.read()
    lg, le = len(got), len(exp)
    hdr = "match" if got[:44] == exp[:44] else "diff"
    if got == exp:
        return {'status': 'pass', 'len_got': lg, 'len_exp': le}
    first = next((i for i, (a, b) in enumerate(zip(got, exp)) if a != b),
                 min(lg, le))
    samples = []
    if first >= 44:
        s0 = (first - 44) // 2
        for i in range(max(0, s0 - 2), s0 + 3):
            if 44 + 2 * i + 2 <= lg and 44 + 2 * i + 2 <= le:
                g = struct.unpack('<h', got[44 + 2 * i:44 + 2 * i + 2])[0]
                e = struct.unpack('<h', exp[44 + 2 * i:44 + 2 * i + 2])[0]
                samples.append((i, g, e))
    return {'status': 'fail', 'len_got': lg, 'len_exp': le, 'hdr': hdr,
            'first_diff': first, 'samples': samples}


def run_vectors(bin_path, workdir):
    """Run the binary for vectors 1..3; byte-compare each to the oracle."""
    results = []
    for v in (1, 2, 3):
        out_path = os.path.join(workdir, 'vec%d.wav' % v)
        try:
            r = subprocess.run([bin_path, out_path, str(v)],
                               capture_output=True, timeout=60)
            rc = r.returncode
        except Exception as e:
            return None, {'vec': v, 'error': 'harness-exception: %s' % e}
        if rc != 0 or not os.path.exists(out_path):
            return None, {'vec': v, 'error': 'run-failed rc=%d' % rc,
                           'stderr': r.stderr.decode('utf-8', errors='replace')[:500]}
        exp_path = os.path.join(ORACLE_DIR, 'oracle_v%d.wav' % v)
        c = compare_wav(out_path, exp_path)
        c['vec'] = v
        results.append(c)
        if c['status'] == 'fail':
            break
    return results, None


def build_evidence(results):
    """Evidence envelope for the first failing vector (facts only)."""
    lines = ["COMPILE_OK"]
    passed = [str(r['vec']) for r in results if r['status'] == 'pass']
    failed = [r for r in results if r['status'] == 'fail']
    lines.append("PASS_VECS %s" % (",".join(passed) if passed else "none"))
    f = failed[0]
    lines.append("FAIL_VEC %d" % f['vec'])
    lines.append("LEN_GOT %d" % f['len_got'])
    lines.append("LEN_EXP %d" % f['len_exp'])
    lines.append("HDR %s" % f['hdr'])
    lines.append("FIRST_DIFF %d" % f['first_diff'])
    samp = " ".join("s=%d:got %d exp %d" % (i, g, e)
                    for i, g, e in f['samples'])
    lines.append("SAMPLES %s" % (samp if samp else "none"))
    return "\n".join(lines) + "\n"


def trailer(prev_class, prev_strat, stalled, cycle):
    return "PREV %s/%s\nSTALLED %d\nCYCLE %d\n" % (prev_class, prev_strat, stalled, cycle)


def run_arm(arm, spec, installed_csv, budget, workdir):
    os.makedirs(workdir, exist_ok=True)
    iters = []
    outcome = None

    gate_out = run_learner(['gate', spec])
    if 'REFUSE' in gate_out:
        return {'arm': arm, 'outcome': 'gate-refused', 'iters_used': 0, 'iters': []}

    src = run_learner(['gen', spec, installed_csv, '', ''])
    gen_failed = src.startswith(GEN_SENTINELS)

    src_bytes = src.encode('utf-8')
    seen = {sha(src_bytes)}
    prev_src_bytes = None
    prev_class, prev_strat = 'none', 'none'

    for it in range(1, budget + 1):
        zag_path = os.path.join(workdir, '%s_i%d.zag' % (arm, it))
        bin_path = os.path.join(workdir, '%s_i%d.bin' % (arm, it))

        if gen_failed and it == 1:
            evtype = 'GEN'
            ev = 'GENFAIL %s\n' % src.strip().split('\n')[0][:120] + trailer(prev_class, prev_strat, 0, 0)
            rc, stderr = None, None
        else:
            rc, stderr = compile_src(src, zag_path, bin_path)
            if rc == 0:
                results, herr = run_vectors(bin_path, workdir)
                if herr is not None:
                    evtype = 'TEST'
                    ev = ("COMPILE_OK\nRUNFAIL vec=%s %s\n" % (herr.get('vec'), herr.get('error'))
                          + trailer(prev_class, prev_strat, 0, 0))
                elif all(r['status'] == 'pass' for r in results):
                    iters.append({'n': it, 'evtype': 'NONE', 'result': 'pass',
                                  'src_sha256': sha(src_bytes),
                                  'vec_sha256': [sha(open(os.path.join(workdir, 'vec%d.wav' % v), 'rb').read())
                                                 for v in (1, 2, 3)]})
                    outcome = 'pass'
                    break
                else:
                    stalled = 1 if (prev_src_bytes is not None and src_bytes == prev_src_bytes) else 0
                    cycle = 1 if sha(src_bytes) in seen and it > 1 else 0
                    ev = build_evidence(results) + trailer(prev_class, prev_strat, stalled, cycle)
                    evtype = 'TEST'
            else:
                stalled = 1 if (prev_src_bytes is not None and src_bytes == prev_src_bytes) else 0
                cycle = 1 if sha(src_bytes) in seen and it > 1 else 0
                ev = "RC %d\n%s" % (rc, stderr) + trailer(prev_class, prev_strat, stalled, cycle)
                evtype = 'COMPILE'

        dout = run_learner(['diagnose', spec, src, evtype, ev, installed_csv, '', ''])
        d, new_src = parse_diag(dout)
        if d is None or new_src is None:
            iters.append({'n': it, 'evtype': evtype, 'result': 'diag-unparseable',
                          'src_sha256': sha(src_bytes),
                          'evidence_sha256': sha(ev.encode('utf-8')),
                          'diag_raw_sha256': sha(dout.encode('utf-8'))})
            outcome = 'diag-unparseable'
            break

        new_bytes = new_src.encode('utf-8')
        rec = {'n': it, 'evtype': evtype, 'result': 'revised',
               'class': d.get('class', '?'), 'strategy': d.get('strategy', '?'),
               'score': d.get('score', '?'), 'trace': d.get('trace', '?'),
               'src_sha256': sha(src_bytes), 'new_src_sha256': sha(new_bytes),
               'evidence_sha256': sha(ev.encode('utf-8'))}
        iters.append(rec)

        strat = d.get('strategy', '')
        if strat.startswith('halt-'):
            outcome = strat
            break
        if new_bytes == src_bytes:
            outcome = 'stall-guard-halt'
            break
        seen.add(sha(src_bytes))
        prev_src_bytes = src_bytes
        src, src_bytes = new_src, new_bytes
        prev_class, prev_strat = d.get('class', '?'), strat
        gen_failed = False

    if outcome is None:
        outcome = 'budget-exhausted'
    return {'arm': arm, 'outcome': outcome, 'iters_used': len(iters), 'iters': iters}


def canonical(obj):
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in sorted(o.items()) if k != 'rep'}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    return json.dumps(strip(obj), sort_keys=True, separators=(',', ':'))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', required=True, choices=['informed', 'scratch'])
    ap.add_argument('--spec', required=True)
    ap.add_argument('--budget', type=int, default=6)
    ap.add_argument('--workdir', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--rep', default='1')
    args = ap.parse_args()

    installed_path = os.path.join(TASK2, 'store',
                                  'installed_%s.csv' % ('informed' if args.arm == 'informed' else 'scratch'))
    with open(installed_path) as f:
        installed_csv = f.read().strip()

    with open(args.spec) as f:
        spec = f.read().strip()

    r = run_arm(args.arm, spec, installed_csv, args.budget, args.workdir)
    r['rep'] = args.rep
    with open(args.out, 'w') as f:
        json.dump(r, f, indent=1, sort_keys=True)
    print("arm=%-8s rep=%s outcome=%-18s iters=%d digest=%s" %
          (r['arm'], r['rep'], r['outcome'], r['iters_used'],
           sha(canonical(r).encode())[:16]))


if __name__ == '__main__':
    main()
