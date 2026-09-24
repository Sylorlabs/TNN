#!/usr/bin/env python3
"""Verify an F1 AUTOPILOT hash-chained ledger.
Recomputes GENESIS and every CHAIN link from the ledger bytes alone.
Usage: verify_ledger.py <ledger> ; prints VERIFY lines, rc=0 iff all links hold.
"""
import sys, hashlib

def sha(b): return hashlib.sha256(b).digest()

def main():
    path = sys.argv[1]
    raw = open(path, 'rb').read()
    lines = raw.decode('ascii').split('\n')
    # raw ends with trailing newline; drop the final empty piece
    assert lines[-1] == '', "ledger must end with newline"
    lines = lines[:-1]

    # split header / genesis / episodes
    gi = next(i for i, l in enumerate(lines) if l.startswith('GENESIS '))
    header = ('\n'.join(lines[:gi]) + '\n').encode('ascii')
    gprev, gentry = lines[gi].split(' ')[1], lines[gi].split(' ')[2]
    assert gprev == 'prev=' + '00' * 32, "GENESIS prev must be 32 zero bytes"
    calc = sha(b'\x00' * 32 + header).hex()
    assert gentry == 'entry=' + calc, f"GENESIS entry mismatch: {gentry} vs entry={calc}"
    print(f"VERIFY genesis=OK entry={calc}")

    prev = bytes.fromhex(calc)
    n_ep = 0
    i = gi + 1
    while i < len(lines):
        assert lines[i].startswith('EPISODE '), f"expected EPISODE at line {i}: {lines[i][:40]}"
        j = i
        while not lines[j].startswith('PERCEPT '):
            j += 1
            assert j < len(lines), "unterminated episode body"
        body = ('\n'.join(lines[i:j + 1]) + '\n').encode('ascii')
        cl = lines[j + 1]
        assert cl.startswith('CHAIN '), f"expected CHAIN at line {j+1}"
        parts = dict(kv.split('=', 1) for kv in cl.split(' ')[1:])
        assert parts['prev'] == prev.hex(), f"episode {n_ep}: CHAIN prev mismatch"
        calc_e = sha(prev + body).hex()
        assert parts['entry'] == calc_e, f"episode {n_ep}: CHAIN entry mismatch"
        prev = bytes.fromhex(calc_e)
        n_ep += 1
        i = j + 2
    print(f"VERIFY episodes={n_ep} chain=OK head={prev.hex()}")
    print(f"VERIFY ledger_bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")

main()
