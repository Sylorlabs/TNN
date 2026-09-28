#!/usr/bin/env python3
# Commit a file set to sylorlabs/TNN branch tnn-native-lab via GitHub API.
# Usage: commit_batch.py <message> <head_sha> <local_base> <repo_base> <path...>
# Paths are relative to local_base; committed under repo_base.
# Excludes: sealed/map.txt is only included if explicitly listed.
import sys, os, subprocess, json

MSG, HEAD, LOCAL_BASE, REPO_BASE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
PATHS = sys.argv[5:]
GH = os.path.expanduser('~/workspace/skills/github/bin/gh-api')
REPO = 'sylorlabs/TNN'

def api(method, path, data=None):
    cmd = [GH, method, f'/repos/{REPO}{path}']
    if data is not None:
        cmd += ['--data', json.dumps(data)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f'API FAIL {method} {path}: {r.stderr[:500]}', file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout)

# collect files
files = []
for p in PATHS:
    lp = os.path.join(LOCAL_BASE, p)
    if os.path.isdir(lp):
        for root, _, fns in os.walk(lp):
            for fn in fns:
                # skip caches, binaries, and the sealed plaintext map unless listed
                ap = os.path.join(root, fn)
                rel = os.path.relpath(ap, LOCAL_BASE)
                if '.zagd' in rel or '.zag-cache' in rel or rel.endswith('.bin'):
                    continue
                files.append(rel)
    else:
        files.append(p)
files = sorted(set(files))
print(f'{len(files)} files')

# base tree
base_tree = api('GET', f'/git/commits/{HEAD}')['tree']['sha']
# blobs
entries = []
for rel in files:
    with open(os.path.join(LOCAL_BASE, rel), 'rb') as f:
        content = f.read()
    # binary-safe: use base64 via API (data API expects utf-8; encode)
    import base64
    b = api('POST', '/git/blobs', {'content': base64.b64encode(content).decode(),
                                   'encoding': 'base64'})
    entries.append({'path': f'{REPO_BASE}/{rel}', 'mode': '100644',
                    'type': 'blob', 'sha': b['sha']})
tree = api('POST', '/git/trees', {'base_tree': base_tree, 'tree': entries})
commit = api('POST', '/git/commits', {'message': MSG, 'tree': tree['sha'],
                                      'parents': [HEAD]})
# update ref only if head is still what we built on (compare-and-swap)
cur = api('GET', '/git/ref/heads/tnn-native-lab')['object']['sha']
if cur != HEAD:
    print(f'HEAD MOVED during commit ({HEAD[:8]} -> {cur[:8]}); NOT updating ref.', file=sys.stderr)
    print(f'commit created: {commit["sha"]} (rebase needed)')
    sys.exit(2)
r = subprocess.run([GH, 'PATCH', f'/repos/{REPO}/git/refs/heads/tnn-native-lab',
                    '--data', json.dumps({'sha': commit['sha'], 'force': False})],
                   capture_output=True, text=True)
if r.returncode != 0:
    print(f'REF UPDATE FAILED (head moved?): {r.stderr[:300]}', file=sys.stderr)
    print(f'commit created: {commit["sha"]} (not pushed to branch)')
    sys.exit(2)
print('branch now at', json.loads(r.stdout)['object']['sha'])
print('commit', commit['sha'])
