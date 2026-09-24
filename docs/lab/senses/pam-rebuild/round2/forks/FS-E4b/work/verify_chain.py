#!/usr/bin/env python3
# FS-E4b: independent hash-chain verification for e4b ledgers.
# Ledger line: "<content> hash=<hex64>", hash = sha256hex(prev_raw32 ++ content),
# genesis prev = 32 zero bytes.
# Usage: verify_chain.py <ledger> [<ledger> ...]; exits 0 iff all verify.
import sys, hashlib

def verify(path):
    prev = bytes(32)
    n = 0
    with open(path) as f:
        for ln, line in enumerate(f):
            line = line.rstrip('\n')
            if not line.endswith(' hash=') and ' hash=' not in line:
                return False, 'line %d: no hash tag' % ln
            content, hx = line.rsplit(' hash=', 1)
            if len(hx) != 64:
                return False, 'line %d: bad hash length' % ln
            h = hashlib.sha256(prev + content.encode()).hexdigest()
            if h != hx:
                return False, 'line %d: hash mismatch' % ln
            prev = bytes.fromhex(hx)
            n += 1
    return True, '%d lines' % n

def main():
    ok = True
    for p in sys.argv[1:]:
        v, msg = verify(p)
        print('%s: %s (%s)' % (p, 'OK' if v else 'FAIL', msg), flush=True)
        ok = ok and v
    print('CHAIN_VERIFY: %s' % ok, flush=True)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
