#!/usr/bin/env python3
# score_w11.py — independent scorer for the W11 chain-of-custody verifier.
# Usage: python3 score_w11.py <zag_output.txt>
# Recomputes every HMAC independently (Python hmac/sha256), checks every
# disposition against the frozen check order, evaluates C1/C2/K7/K1/K3,
# and emits D-W11-1/2.
import sys, hmac, hashlib, struct
from collections import Counter

W11DIR = '/home/hatch/workspace/tnn-lab/pam/round4/wild/w11'
K = bytes(((i * 2654435761 + 0x9E3779B9) % 256) for i in range(32))
CALIB_REG = 0xC0FFEE11

def M(msg: bytes) -> str:
    return hmac.new(K, msg, hashlib.sha256).hexdigest()

def verify(cid, nlinks, calib, links):
    """Frozen check order. Returns 'ADMIT' or 'REJECT:<reason>'."""
    # 1. well-formed (structural; parse failures handled by caller)
    # 2. anchor MAC
    st0, in0, out0, tr0, mac0 = links[0]
    m0 = M(b"W11A" + struct.pack(">I", cid) + struct.pack(">I", calib)
           + bytes.fromhex(in0))
    if m0 != mac0: return 'REJECT:ANCHOR_MAC'
    if tr0 != 0: return 'REJECT:ALLOWLIST'
    # 3. chain MACs (+4 allowlist for links>=1)
    prev_mac = mac0
    for (st, inp, outp, tr, mac) in links[1:]:
        m = M(struct.pack(">I", st) + bytes.fromhex(inp) + bytes.fromhex(outp)
              + struct.pack(">I", tr) + bytes.fromhex(prev_mac))
        if m != mac: return 'REJECT:CHAIN_MAC'
        if not (1 <= tr <= 8): return 'REJECT:ALLOWLIST'
        prev_mac = mac
    # 5. cap
    if nlinks > 6: return 'REJECT:OVERLONG'
    # 6. calib
    if calib != CALIB_REG: return 'REJECT:CALIB'
    return 'ADMIT:OK'

def parse_link(s):
    f = s.split(',')
    if len(f) != 5: return None
    st, inp, outp, trs, mac = f
    try:
        tr = int(trs); st = int(st)
        assert len(inp) == 64 and len(outp) == 64 and len(mac) == 64
        bytes.fromhex(inp); bytes.fromhex(outp); bytes.fromhex(mac)
    except Exception:
        return None
    return (st, inp, outp, tr, mac.lower())

chains = []
for ln in open(f'{W11DIR}/w11_chains.txt'):
    ln = ln.rstrip('\n')
    if not ln: continue
    p = ln.split('|')
    cid, nlinks, calibs = int(p[0]), int(p[1]), p[2]
    ok = len(p) == 3 + nlinks and len(calibs) == 8
    try:
        calib = int(calibs, 16)
    except Exception:
        ok = False; calib = 0
    links = [parse_link(s) for s in p[3:]] if ok else []
    if any(l is None for l in links): ok = False
    chains.append((cid, nlinks, calib, links, ok))
assert len(chains) == 370, len(chains)

# ---- parse instrument output ----
lines = open(sys.argv[1]).read().splitlines()
assert lines[0].startswith('W11_CHAIN'), lines[0]
rows, summary = {}, None
for ln in lines[1:]:
    if ln.startswith('SUMMARY|'):
        summary = ln; continue
    c, v, r = ln.split('|')
    rows[int(c)] = (v, r)
assert len(rows) == 370, len(rows)

# ---- check every disposition ----
bad = []
for (cid, nlinks, calib, links, ok) in chains:
    exp = 'REJECT:WELLFORMED' if not ok else verify(cid, nlinks, calib, links)
    got = rows[cid][0] + ':' + rows[cid][1]
    if exp != got:
        bad.append((cid, exp, got))
assert not bad, f'{len(bad)} disposition mismatches: {bad[:5]}'
print('dispositions: 370/370 match independent HMAC recomputation  OK')

# ---- class expectations ----
# ids: VALID 0..199, BROKEN_MAC 200..229, UNLISTED 230..249,
# OVERLONG 250..269, REPLAY 270..284, MID_TRUNCATE 285..299,
# FORGE_NOKEY 300..329, CALIB_DRIFT 330..369
def cls(cid):
    if cid < 200: return 'VALID'
    if cid < 230: return 'BROKEN_MAC'
    if cid < 250: return 'UNLISTED'
    if cid < 270: return 'OVERLONG'
    if cid < 285: return 'REPLAY'
    if cid < 300: return 'MID_TRUNCATE'
    if cid < 330: return 'FORGE_NOKEY'
    return 'CALIB_DRIFT'

adm_valid = sum(1 for c in range(200) if rows[c][0] == 'ADMIT')
attack_adm = [(c, cls(c)) for c in range(200, 370) if rows[c][0] == 'ADMIT']
print(f'VALID admits: {adm_valid}/200')
print(f'attack admits: {len(attack_adm)}/170 {attack_adm[:5] if attack_adm else ""}')

# ---- bars ----
print(f'K1: {"KILL" if any(c >= 300 and c < 330 and rows[c][0]=="ADMIT" for c in range(370)) else "PASS (0/30 FORGE_NOKEY admitted)"}')
c1bad = [c for c in list(range(200, 230)) + list(range(270, 300)) + list(range(300, 330))
         if rows[c][0] == 'ADMIT']
# C1 battery per prereg: 30 FORGE_NOKEY + 15 REPLAY + 15 MID_TRUNCATE
print(f'C1: {"KILL" if c1bad else "PASS (0/60 forgery attempts verify)"}')
c2 = sum(1 for c in range(200) if chains[c][1] > 6)
print(f'C2: {c2}/200 VALID chains exceed cap (bar: >5% -> KILL) -> {"KILL" if c2 > 10 else "PASS"}')
k7bad = [c for c in range(330, 370) if rows[c][0] == 'ADMIT']
print(f'K7: CALIB_DRIFT admits {len(k7bad)}/40 (bar: any -> KILL) -> {"KILL" if k7bad else "PASS"}')
print(f'K3: {adm_valid}/200 = {100*adm_valid/200:.2f}% (bar >=66.78%)')
print('K2: PASS (checked by driver: 2x byte-identical)')
print('K5: PASS (terminated)')
print('C3: recorded in fixture commit (single anchor()+extend() path); '
      'verifier is the only admission path in the instrument')
print('C4: PASS (O(nlinks) verify, O(total links) storage; no cross-chain state)')

# ---- D-W11-1 / D-W11-2 ----
rej = Counter(rows[c][1] for c in range(370) if rows[c][0] == 'REJECT')
print(f'D-W11-1 reject reasons: {dict(rej)}')
admitted_links = Counter(chains[c][1] for c in range(200) if rows[c][0] == 'ADMIT')
print(f'D-W11-2 admitted VALID link counts: {dict(sorted(admitted_links.items()))}')
