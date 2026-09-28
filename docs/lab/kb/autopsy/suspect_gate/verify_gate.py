"""Verify the gate's hash chain + ledger fields against frozen inputs (no truth)."""
import hashlib, sys

build = '/home/hatch/workspace/scratch_suspect1/build'
rerun = '/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun'

def read_batch(tag):
    lines = open('%s/batch_%s.txt' % (rerun, tag)).read().splitlines()
    return [[int(x) for x in ln.split('\t')] for ln in lines]

def read_seg(tag):
    return [[int(x) for x in ln.split()] for ln in open('%s/segments_%s.txt' % (build, tag))]

cmap = {}
for ln in open(build + '/classmap.txt'):
    s, c = ln.split(); cmap[int(s)] = int(c)
chan = {}
for ln in open(build + '/channel.txt'):
    c, p = ln.split(); chan[int(c)] = int(p)

ok = True
for tag in ('A', 'B'):
    batch = read_batch(tag)
    seg = read_seg(tag)
    # task spans
    spans = []
    for i, (t, start, np, nn) in enumerate(seg):
        end = seg[i + 1][1] if i + 1 < len(seg) else len(batch)
        spans.append((t, start, np, nn, end))
    jp = {}
    adv_expected = []  # (stim, Ja, Jp, conf)
    for L, (stim, judg, conf, src) in enumerate(batch):
        t, start, np, nn, end = next(x for x in spans if x[1] <= L < x[4])
        c = L - start
        if c < np:
            jp[stim] = judg
        elif c >= np + nn:
            adv_expected.append((stim, judg, jp[stim], conf))

    out = open('%s/out_%s_smoke.txt' % (build, tag)).read().splitlines()
    ledgers = [ln for ln in out if ln.startswith('LEDGER')]
    summary = [ln for ln in out if ln.startswith('SUMMARY')]
    assert len(summary) == 1, tag
    assert len(ledgers) == len(adv_expected), (tag, len(ledgers), len(adv_expected))

    prev_raw = None
    for i, ln in enumerate(ledgers):
        raw = ln.encode()
        f = ln.split('\t')
        seq, stim, cl, ja, jpv, match, pc, dec, conf, ph = \
            int(f[1]), int(f[2]), int(f[3]), int(f[4]), int(f[5]), int(f[6]), int(f[7]), f[8], int(f[9]), f[10]
        exp_stim, exp_ja, exp_jp, exp_conf = adv_expected[i]
        # chain check
        exp_ph = '0' * 64 if i == 0 else hashlib.sha256(prev_raw).hexdigest()
        checks = [
            ('seq', seq == i + 1), ('stim', stim == exp_stim),
            ('class', cl == cmap[exp_stim]), ('Ja', ja == exp_ja),
            ('Jp', jpv == exp_jp), ('match', match == (1 if exp_ja == exp_jp else 0)),
            ('pc', pc == chan[cmap[exp_stim]]), ('conf', conf == exp_conf),
            ('prevhash', ph == exp_ph),
        ]
        # decision rule check
        m = 1 if exp_ja == exp_jp else 0
        p = chan[cmap[exp_stim]]
        if m == 1:
            exp_dec = 'INSTALL' if p >= 900 else ('WITHHOLD' if p <= 100 else 'SUSPECT')
        else:
            exp_dec = 'WITHHOLD' if p >= 900 else 'SUSPECT'
        checks.append(('dec', dec == exp_dec))
        for name, c_ok in checks:
            if not c_ok:
                ok = False
                print('MISMATCH', tag, 'line', i + 1, name, 'got', ln)
                break
        prev_raw = raw
    # summary check
    sf = summary[0].split('\t')
    nI = sum(1 for ln in ledgers if '\tINSTALL\t' in ln)
    nW = sum(1 for ln in ledgers if '\tWITHHOLD\t' in ln)
    nS = sum(1 for ln in ledgers if '\tSUSPECT\t' in ln)
    head = hashlib.sha256(ledgers[-1].encode()).hexdigest()
    s_ok = (sf[1] == tag and int(sf[2]) == len(ledgers) and int(sf[3]) == nI and
            int(sf[4]) == nW and int(sf[5]) == nS and sf[6] == head)
    if not s_ok:
        ok = False
        print('SUMMARY MISMATCH', tag, summary[0])
    print(tag, 'ledger lines:', len(ledgers), 'I/W/S = %d/%d/%d' % (nI, nW, nS),
          'chain+fields:', 'OK' if ok else 'FAIL')
print('VERIFY:', 'PASS' if ok else 'FAIL')
