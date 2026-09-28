#!/usr/bin/env python3
"""Compare E-DE3 artifacts vs FULL-DELIB artifacts: outcomes, ledger bytes, costs.
Usage: compare.py <ref_fd_artifact> <arm_artifact> [label]
Exit 0 if ledger+outcomes compared; prints JSON-ish summary to stdout.
"""
import struct, sys, hashlib, json

W = [1.0, 12.0, 5.0, 0.2, 0.5, 0.02, 20.0, 1000.0, 0.05, 30.0, 3.0]

def u32(b, o): return struct.unpack_from('<I', b, o)[0]
def u64(b, o): return struct.unpack_from('<Q', b, o)[0]

def parse(path):
    d = open(path, 'rb').read()
    magic = d[0:8]
    if magic == b'HTD1E3A1':
        n = u32(d, 16); arm = u32(d, 12); cap = u32(d, 20)
        rp = 24
        items = []
        for i in range(n):
            o = rp + i*128
            items.append(dict(ii=u32(d,o), bat=u32(d,o+4), off=u32(d,o+8), ln=u32(d,o+12),
                              winner=struct.unpack_from('<i', d, o+16)[0],
                              nh=u32(d,o+20), mask=u32(d,o+24),
                              q=(u32(d,o+28), u32(d,o+32), u32(d,o+36), u32(d,o+40), u32(d,o+44))))
        ap = rp + n*128
        vec = [u64(d, ap+i*8) for i in range(11)]
        summ = [u64(d, ap+88+i*8) for i in range(6)]
        llen = u32(d, ap+136)
        ledger = d[ap+140:ap+140+llen]
        assert len(ledger) == llen
        return dict(kind='ede3', n=n, arm=arm, cap=cap, items=items, vec=vec,
                    summ=dict(issued=summ[0], settle_events=summ[1], settled=summ[2],
                              overturns=summ[3], kb3_trips=summ[4], bk_words=summ[5]),
                    ledger=ledger, sha=hashlib.sha256(d).hexdigest())
    elif magic in (b'HTD1FDA1', b'HTD1B0A1'):
        n = u32(d, 16)
        rp = 24
        items = []
        for i in range(n):
            o = rp + i*128
            items.append(dict(ii=u32(d,o), bat=u32(d,o+4), off=u32(d,o+8), ln=u32(d,o+12),
                              winner=struct.unpack_from('<i', d, o+16)[0],
                              nh=u32(d,o+20), mask=u32(d,o+24),
                              q=(u32(d,o+28), u32(d,o+32), u32(d,o+36), u32(d,o+40), u32(d,o+44))))
        ap = rp + n*128
        c9 = [u64(d, ap+i*8) for i in range(9)]
        # map to 11-class vector: expand,gather,verify,memread,memwrite,
        # 64*ledger,ledger,ledger,gateeval,0,0
        vec = [c9[0], c9[1], c9[2], c9[3], c9[4], 64*c9[8], c9[8], c9[8], c9[7], 0, 0]
        llen = u32(d, ap+72)
        ledger = d[ap+76:ap+76+llen]
        assert len(ledger) == llen
        return dict(kind='fd', n=n, items=items, vec=vec, ledger=ledger,
                    sha=hashlib.sha256(d).hexdigest())
    elif magic in (b'HTD1E5a1', b'HTD1E5b1', b'HTD1E5d1', b'HTD1E5r1'):
        # E-DE5: 144B records, native 11-class vector
        n = u32(d, 16)
        rp = 24
        items = []
        for i in range(n):
            o = rp + i*144
            items.append(dict(ii=u32(d,o), bat=u32(d,o+4), off=u32(d,o+8), ln=u32(d,o+12),
                              winner=struct.unpack_from('<i', d, o+16)[0],
                              nh=u32(d,o+20), mask=u32(d,o+24),
                              q=(u32(d,o+28), u32(d,o+32), u32(d,o+36), u32(d,o+40), u32(d,o+44)),
                              skipped=u32(d,o+136)))
        ap = rp + n*144
        vec = [u64(d, ap+i*8) for i in range(11)]
        llen = u32(d, ap+88)
        ledger = d[ap+92:ap+92+llen]
        assert len(ledger) == llen
        return dict(kind='e5', n=n, arm=magic.decode(), items=items, vec=vec,
                    ledger=ledger, sha=hashlib.sha256(d).hexdigest())
    else:
        raise ValueError('bad magic %r' % magic)

def cost(vec):
    return sum(w*x for w, x in zip(W, vec))

def main():
    ref = parse(sys.argv[1])
    arm = parse(sys.argv[2])
    label = sys.argv[3] if len(sys.argv) > 3 else ''
    assert ref['n'] == arm['n']
    n = ref['n']
    div = 0
    div_idx = []
    e5 = arm.get('kind') == 'e5'
    for a, b in zip(ref['items'], arm['items']):
        if e5:
            # E-DE5 narrows the evaluated set (mask semantics differ);
            # compare winner only and report skipped-hypothesis items.
            bad = (a['winner'] != b['winner'])
        else:
            bad = (a['winner'] != b['winner'] or a['mask'] != b['mask'])
        if bad:
            div += 1
            if len(div_idx) < 10: div_idx.append(a['ii'])
    if e5:
        out_skip = sum(1 for b in arm['items'] if b['skipped'] != 0)
    cr, ca = cost(ref['vec']), cost(arm['vec'])
    # C-dagger: sibling-normalized (per-entry ledger price at baseline rate)
    def cdagger(v):
        e = v[6]  # entries
        return (W[0]*v[0]+W[1]*v[1]+W[2]*v[2]+W[3]*v[3]+W[4]*v[4]
                +W[8]*v[8]+W[9]*v[9]+W[10]*v[10]+e*(64*W[5]+W[6]+W[7]))
    cdr, cda = cdagger(ref['vec']), cdagger(arm['vec'])
    out = dict(label=label, n=n,
               ref_sha=ref['sha'][:16], arm_sha=arm['sha'][:16],
               ref_vec=ref['vec'], arm_vec=arm['vec'],
               C_ref=cr, C_arm=ca, saving=(cr-ca)/cr,
               Cd_ref=cdr, Cd_arm=cda, saving_dagger=(cdr-cda)/cdr,
               divergence=div, divergence_rate=div/n, div_idx=div_idx,
               ledger_identical=(ref['ledger'] == arm['ledger']),
               ledger_len_ref=len(ref['ledger']), ledger_len_arm=len(arm['ledger']),
               )
    if arm['kind'] == 'ede3':
        out['summary'] = arm['summ']
    if arm.get('kind') == 'e5':
        out['e5_arm'] = arm['arm']
        out['e5_items_with_skipped'] = out_skip
    print(json.dumps(out, indent=1))

main()
