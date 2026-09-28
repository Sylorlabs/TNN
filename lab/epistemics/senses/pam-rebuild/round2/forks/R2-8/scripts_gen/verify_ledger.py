#!/usr/bin/env python3
"""Independent ledger verification for R2-8 B6.

Re-chains the hash ledger from genesis using only the canonical trial bytes
in ledger.txt (not trusting any stored entry hash). Verifies:
  1. each entry's prev_hash equals the previous entry's computed hash,
  2. each entry_hash == sha256(prev_hash + canonical_bytes),
  3. genesis matches sha256("R2-8-genesis-20260923"),
  4. the trial count and final hash match the summary.
"""
import hashlib
import json
import os
import sys

BASE = os.path.expanduser('~/workspace/tnn-lab/senses/pam-rebuild/round2')
OUTDIR = os.path.join(BASE, 'forks', 'R2-8', 'evidence', 'battery')

def main():
    led = open(os.path.join(OUTDIR, 'ledger.txt')).read().splitlines()
    assert led[0].startswith('genesis ')
    genesis = led[0].split(' ', 1)[1]
    expect_gen = hashlib.sha256(b'R2-8-genesis-20260923').hexdigest()
    assert genesis == expect_gen, 'genesis mismatch'
    prev = genesis
    n = 0
    for ln in led[1:]:
        ph, eh, cb = ln.split(' ', 2)
        assert ph == prev, 'chain break at entry %d' % n
        calc = hashlib.sha256((ph + cb).encode()).hexdigest()
        assert calc == eh, 'entry hash mismatch at entry %d' % n
        prev = eh
        n += 1
    summary = json.load(open(os.path.join(OUTDIR, 'summary.json')))
    assert summary['n_trials'] == n, 'trial count mismatch'
    assert summary['ledger_final_hash'] == prev, 'final hash mismatch'
    print('LEDGER VERIFIED: %d entries, chain intact, final=%s' % (n, prev))
    return 0

if __name__ == '__main__':
    sys.exit(main())
