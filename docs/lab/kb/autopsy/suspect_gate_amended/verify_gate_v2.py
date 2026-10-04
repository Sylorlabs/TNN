"""Verify the v2 (amended SS8) gate: hash chain + ledger fields + INFO-REQUEST
resolution against frozen inputs. No truth used.

Usage: verify_gate_v2.py <workdir> <mode>
Checks out_A_<mode>_rep{1,2,3}.txt and out_B_<mode>_rep{1,2,3}.txt.
"""
import hashlib
import sys

workdir, mode = sys.argv[1], sys.argv[2]
assert mode in ('live', 'ablated'), mode


def read_batch(tag):
    lines = open('%s/batch_%s.txt' % (workdir, tag)).read().splitlines()
    return [[int(x) for x in ln.split('\t')] for ln in lines]


def read_seg(tag):
    return [[int(x) for x in ln.split()] for ln in open('%s/segments_%s.txt' % (workdir, tag))]


cmap = {}
for ln in open(workdir + '/classmap.txt'):
    s, c = ln.split()
    cmap[int(s)] = int(c)
chan = {}
for ln in open(workdir + '/channel.txt'):
    c, p = ln.split()
    chan[int(c)] = int(p)

ok = True
for tag in ('A', 'B'):
    batch = read_batch(tag)
    seg = read_seg(tag)
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

    for rep in (1, 2, 3):
        out = open('%s/out_%s_%s_rep%d.txt' % (workdir, tag, mode, rep)).read().splitlines()
        ledgers = [ln for ln in out if ln.startswith('LEDGER')]
        summary = [ln for ln in out if ln.startswith('SUMMARY')]
        assert len(summary) == 1, (tag, mode, rep)
        assert len(ledgers) == 2 * len(adv_expected), (tag, mode, rep)
        prev_raw = None
        n_ch_i = n_ch_w = n_se_i = n_se_w = 0
        for i in range(len(adv_expected)):
            exp_stim, exp_ja, exp_jp, exp_conf = adv_expected[i]
            exp_cl = cmap[exp_stim]
            exp_match = 1 if exp_ja == exp_jp else 0
            exp_pc = chan[exp_cl]
            ln1 = ledgers[2 * i]
            raw1 = ln1.encode()
            f1 = ln1.split('\t')
            ln2 = ledgers[2 * i + 1]
            raw2 = ln2.encode()
            f2 = ln2.split('\t')
            exp_ph1 = '0' * 64 if 2 * i == 0 else hashlib.sha256(prev_raw).hexdigest()
            # frozen SS8.1 resolution
            if mode == 'ablated':
                exp_dec = 'INSTALL' if exp_match == 1 else 'WITHHOLD'
                exp_path = 'SELF'
                exp_pc_rec = -1
            else:
                if exp_match == 1:
                    if exp_pc >= 900:
                        exp_dec, exp_path = 'INSTALL', 'CHANNEL'
                    elif exp_pc <= 100:
                        exp_dec, exp_path = 'WITHHOLD', 'CHANNEL'
                    else:
                        exp_dec, exp_path = 'INSTALL', 'SELF'
                else:
                    if exp_pc >= 900:
                        exp_dec, exp_path = 'WITHHOLD', 'CHANNEL'
                    else:
                        exp_dec, exp_path = 'WITHHOLD', 'SELF'
                exp_pc_rec = exp_pc
            checks = [
                ('seq', int(f1[1]) == 2 * i + 1 and int(f2[1]) == 2 * i + 2),
                ('suspect_fields',
                 f1[2:8] == [str(exp_stim), str(exp_cl), str(exp_ja), str(exp_jp),
                             str(exp_match), str(exp_conf)]
                 and f1[8] == 'SUSPECT' and f1[9] == 'INFO-REQUEST' and len(f1) == 11),
                ('verdict_fields',
                 f2[2:7] == [str(exp_stim), str(exp_cl), str(exp_ja), str(exp_jp),
                             str(exp_match)]
                 and int(f2[7]) == exp_pc_rec and f2[8] == exp_dec
                 and f2[9] == exp_path and len(f2) == 11),
                ('no_terminal_suspect', f2[8] in ('INSTALL', 'WITHHOLD')),
                ('prevhash_suspect', f1[10] == exp_ph1),
                ('prevhash_verdict', f2[10] == hashlib.sha256(raw1).hexdigest()),
            ]
            for name, c_ok in checks:
                if not c_ok:
                    ok = False
                    print('MISMATCH', tag, mode, 'rep', rep, 'fixture', i, name)
                    print('  L1:', ln1[:160])
                    print('  L2:', ln2[:160])
                    break
            if exp_dec == 'INSTALL' and exp_path == 'CHANNEL':
                n_ch_i += 1
            elif exp_dec == 'WITHHOLD' and exp_path == 'CHANNEL':
                n_ch_w += 1
            elif exp_dec == 'INSTALL':
                n_se_i += 1
            else:
                n_se_w += 1
            prev_raw = raw2
        # SUMMARY: tag, mode, n_adv, ch_i, ch_w, se_i, se_w, head
        sf = summary[0].split('\t')
        head = hashlib.sha256(ledgers[-1].encode()).hexdigest()
        s_ok = (sf[1] == tag and sf[2] == mode
                and int(sf[3]) == len(adv_expected)
                and int(sf[4]) == n_ch_i and int(sf[5]) == n_ch_w
                and int(sf[6]) == n_se_i and int(sf[7]) == n_se_w
                and sf[8] == head)
        if not s_ok:
            ok = False
            print('SUMMARY MISMATCH', tag, mode, 'rep', rep, summary[0])
        print(tag, mode, 'rep', rep, 'fixtures:', len(adv_expected),
              'CH I/W = %d/%d' % (n_ch_i, n_ch_w),
              'SELF I/W = %d/%d' % (n_se_i, n_se_w),
              'chain+fields:', 'OK' if ok else 'FAIL')
print('VERIFY_V2:', 'PASS' if ok else 'FAIL')
