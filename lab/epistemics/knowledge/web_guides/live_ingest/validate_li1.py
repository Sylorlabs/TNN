#!/usr/bin/env python3
"""LI-1 full-record validator: manifest order, exact URLs, no dupes/omissions,
status<->snapshot<->fidelity consistency. Exits 0 iff all checks pass."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(HERE, 'li-1', 'urls_manifest.txt')
MAN_CU = os.path.join(HERE, 'li-1', 'urls_manifest_cu.txt')
SNAP = os.path.join(HERE, 'corpus_snap_full')
STAT = os.path.join(SNAP, 'manifest_fetch_status.txt')
FID = os.path.join(SNAP, 'snapshot_fidelity.txt')

errs = []
def fail(msg):
    errs.append(msg)

def load_manifest(path):
    order = []  # (cid, pid, url)
    clusters = []
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            p = line.split('|')
            if p[0] == 'C':
                clusters.append(p[1])
            elif p[0] == 'U':
                cid = p[1]
                n = sum(1 for o in order if o[0] == cid) + 1
                order.append((cid, '%s-p%d' % (cid, n), '|'.join(p[2:])))
            elif p[0] == 'CLUSTER':
                cid = p[1]
                if cid not in clusters:
                    clusters.append(cid)
                n = sum(1 for o in order if o[0] == cid) + 1
                order.append((cid, '%s-p%d' % (cid, n), '|'.join(p[3:])))
    return clusters, order

clusters, order = load_manifest(MAN)
_, order_cu = load_manifest(MAN_CU)

failures = 0
# 1. counts
if len(order) != 213: fail('manifest URL count %d != 213' % len(order))
if len(clusters) != 55: fail('manifest cluster count %d != 55' % len(clusters))
if [(c, u) for c, _, u in order] != [(c, u) for c, _, u in order_cu]:
    fail('urls_manifest.txt and urls_manifest_cu.txt URL sequences differ')

# 2. status records
stat = {}
with open(STAT) as f:
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('F|'):
            _, cid, pid, url, ok, note = line.split('|', 5)
            stat[(cid, pid)] = (url, ok)
if len(stat) != 213: fail('status record count %d != 213' % len(stat))
for i, (cid, pid, url) in enumerate(order):
    if (cid, pid) not in stat:
        fail('missing status record %s' % pid); continue
    surl, ok = stat[(cid, pid)]
    if surl != url:
        fail('URLMISMATCH %s: manifest=%s status=%s' % (pid, url, surl))

# 3. status<->file consistency
ok_recs = [k for k, v in stat.items() if v[1] == 'ok']
fail_recs = [k for k, v in stat.items() if v[1] != 'ok']
for cid, pid in ok_recs:
    p = os.path.join(SNAP, cid, pid + '.txt')
    if not os.path.exists(p):
        fail('ok record but no snapshot file: %s' % pid)
for cid, pid in fail_recs:
    p = os.path.join(SNAP, cid, pid + '.txt')
    if os.path.exists(p):
        fail('FAIL record but snapshot file exists: %s' % pid)

# 4. fidelity records
fid = {}
with open(FID) as f:
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('V|'):
            p = line.split('|', 4)
            fid[(p[1], p[2])] = p[3]
if set(fid) != set(k for k, v in stat.items() if v[1] == 'ok'):
    only_fid = set(fid) - set(k for k, v in stat.items() if v[1] == 'ok')
    only_ok = set(k for k, v in stat.items() if v[1] == 'ok') - set(fid)
    if only_fid: fail('fidelity records without ok status: %s' % sorted(only_fid)[:5])
    if only_ok: fail('ok records without fidelity: %s' % sorted(only_ok)[:5])
ver = sum(1 for v in fid.values() if v == 'VERIFIED')
unv = sum(1 for v in fid.values() if v == 'UNVERIFIED')

# 5. orphan snapshot files
for cid in clusters:
    d = os.path.join(SNAP, cid)
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if fn.endswith('.txt'):
            key = (cid, fn[:-4])
            if key not in stat:
                fail('orphan snapshot file: %s/%s' % (cid, fn))

# 6. duplicate URLs
seen = {}
for cid, pid, url in order:
    seen.setdefault(url, []).append(pid)
dups = {u: p for u, p in seen.items() if len(p) > 1}
if dups: fail('duplicate URLs: %d distinct' % len(dups))

print('urls=%d clusters=%d status_ok=%d status_fail=%d fidelity_verified=%d fidelity_unverified=%d dupes=%d'
      % (len(order), len(clusters), len(ok_recs), len(fail_recs), ver, unv, len(dups)))
if errs:
    print('FAILURES:')
    for e in errs:
        print('  ' + e)
    sys.exit(1)
print('VALIDATOR: ALL CHECKS PASS')
