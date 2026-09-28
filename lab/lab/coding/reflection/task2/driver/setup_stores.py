#!/usr/bin/env python3
"""Task 2 store setup: teach ceremony for the informed arm.

Runs `learner corpus-teach <id> <digest>` for each frozen corpus entry.
On AUDIT installed=1, appends the ID to the installed set and records the
audit line. The scratch arm uses the coding-only installed set (no teach).

Deterministic: fixed entry order, no timestamps in the canonical record.
"""
import subprocess, os, hashlib, csv

HERE = os.path.dirname(os.path.abspath(__file__))
TASK2 = os.path.dirname(HERE)
LEARNER = os.path.join(TASK2, 'work', 'learner')
STORE = os.path.join(TASK2, 'store')

ENTRIES = ["SYN-FLOAT", "SYN-OSC", "SYN-ENV", "SYN-MIX", "SYN-STRUCT", "SYN-NOTE"]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main():
    # frozen digests from the corpus manifest
    digests = {}
    with open(os.path.join(STORE, 'corpus', 'MANIFEST.md')) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2 and parts[0].startswith('SYN-'):
                digests[parts[0]] = parts[1]

    with open(os.path.join(STORE, 'installed_scratch.csv')) as f:
        installed = f.read().strip().split(',')

    audit_lines = []
    for eid in ENTRIES:
        dg = digests[eid]
        r = subprocess.run([LEARNER, 'corpus-teach', eid, dg],
                           capture_output=True, timeout=30)
        out = r.stdout.decode('utf-8').strip()
        audit_lines.append(out)
        print(out)
        assert 'installed=1' in out, "teach failed for %s" % eid
        installed.append(eid)

    installed = sorted(installed)
    informed_csv = ",".join(installed)
    with open(os.path.join(STORE, 'installed_informed.csv'), 'w') as f:
        f.write(informed_csv)

    with open(os.path.join(STORE, 'audit.log'), 'w') as f:
        for line in audit_lines:
            f.write(line + "\n")

    # verify: scratch digest must equal the coding-knowledge-only baseline
    with open(os.path.join(STORE, 'installed_scratch.csv'), 'rb') as f:
        scratch_digest = sha(f.read())
    with open(os.path.join(STORE, 'installed_informed.csv'), 'rb') as f:
        informed_digest = sha(f.read())
    print("scratch digest :", scratch_digest)
    print("informed digest:", informed_digest)

    # the coding-knowledge-only baseline (recorded here, frozen)
    baseline = "ef6d81ae72d93e8973329336201c227541f2e8755a823ab0d4a9664bc843089c"
    assert scratch_digest == baseline, "SCRATCH DRIFT: %s != %s" % (scratch_digest, baseline)
    print("scratch == coding-knowledge-only baseline: OK")


if __name__ == '__main__':
    main()
