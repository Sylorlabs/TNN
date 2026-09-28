#!/usr/bin/env python3
"""Tier-2 falsification battery driver. Python drives; all decisions in Zag."""
import hashlib, os, subprocess, sys

BIN = os.path.expanduser('~/workspace/liharden/tier2/build/tier2_bin')
FX = os.path.expanduser('~/workspace/liharden/tier2/fixtures')
OUT = os.path.expanduser('~/workspace/liharden/tier2/battery_out')
os.makedirs(OUT, exist_ok=True)
CLAIM = open(os.path.join(FX, 'claim.txt')).read().strip()

def run(mode, *args):
    r = subprocess.run([BIN, mode, *args], capture_output=True, timeout=60)
    assert r.returncode == 0, (mode, args, r.returncode, r.stderr[:200])
    return r.stdout

CASES = []
def case(cid, mode, args, checks):
    CASES.append((cid, mode, args, checks))

# ---------- HL-6 ----------
for t in ['T6-1_footer', 'T6-2_ariahidden', 'T6-3_comment', 'T6-4_jsonld', 'T6-5_ugc']:
    case(t, 'extract', [f'{FX}/{t}/page.html'], [
        ('false-sentence absent', lambda o: b'9999' not in o),
        ('body intact', lambda o: b'quick brown fox' in o and b'liquor jugs' in o),
    ])
case('T6-6_honest', 'extract', [f'{FX}/T6-6_honest/page.html'], [
    ('body present', lambda o: b'quick brown fox' in o and b'liquor jugs' in o),
    ('footer dropped', lambda o: b'Copyright' not in o),
    ('nav dropped', lambda o: b'Home About' not in o),
])

# ---------- HL-6 extensions (labeled; post-freeze probes) ----------
case('T6-7_nestedhidden', 'extract', [f'{FX}/T6-7_nestedhidden/page.html'], [
    ('hidden variants absent', lambda o: b'hidden one' not in o and b'hidden two' not in o
     and b'hidden three' not in o and b'hidden four' not in o),
    ('body intact', lambda o: b'Visible body one.' in o and b'two <tag>.' in o),
])

# ---------- HL-7 ----------
def nlines(o): return [l for l in o.decode('utf-8').split('\n') if l.startswith('N|')]
def slines(o): return [l for l in o.decode('utf-8').split('\n') if l.startswith('S|')]
case('T7-1_ligature', 'norm', [f'{FX}/T7-1_ligature/lines.txt'],
     [('distinct', lambda o: len(set(nlines(o))) == 2)])
case('T7-2_fullwidth', 'norm', [f'{FX}/T7-2_fullwidth/lines.txt'],
     [('distinct', lambda o: len(set(nlines(o))) == 2)])
case('T7-3_numbers', 'norm', [f'{FX}/T7-3_numbers/lines.txt'],
     [('distinct', lambda o: len(set(nlines(o))) == 2)])
case('T7-4_zerowidth', 'norm', [f'{FX}/T7-4_zerowidth/lines.txt'],
     [('identical (invisible)', lambda o: len(set(nlines(o))) == 1)])
case('T7-5_abbrev', 'sentsplit', [f'{FX}/T7-5_abbrev/text.txt'], [
    ('2 sentences', lambda o: len(slines(o)) == 2),
    ('no split on Dr./3.1', lambda o: slines(o)[0] == 'S|Dr. Smith drove 3.1 miles.'),
])
case('T7-6_abbrev2', 'sentsplit', [f'{FX}/T7-6_abbrev2/text.txt'], [
    ('2 sentences', lambda o: len(slines(o)) == 2),
    ('first intact', lambda o: slines(o)[0] == 'S|Mr. Jones left.'),
])
case('T7-7_controls', 'norm', [f'{FX}/T7-7_controls/lines.txt'],
     [('stripped', lambda o: nlines(o) == ['N|abc'])])

# ---------- HL-8 ----------
case('T8-1_swap', 'attr', [f'{FX}/T8-1_swap/chains.txt'], [
    ('attributed to attacker', lambda o: b'A|p1|evil-plant.example|evil-plant.example|hops=1|xreg=1' in o),
])
case('T8-2_sameorigin', 'attr', [f'{FX}/T8-2_sameorigin/chains.txt'], [
    ('origin kept', lambda o: b'A|p1|www.shop.example|shop.example|hops=2|xreg=0' in o),
])
case('T8-3_noamp', 'attr', [f'{FX}/T8-3_noamp/chains.txt'], [
    ('one final regdom', lambda o: b'Q|distinct_final_regdoms=1' in o),
])
case('T8-4_failclosed', 'attr', [f'{FX}/T8-4_failclosed/chains.txt'], [
    ('empty host', lambda o: b'A|p1|||hops=0|xreg=0' in o),
    ('no votes', lambda o: b'Q|distinct_final_regdoms=0' in o),
])

case('T8-5_userinfoport', 'attr', [f'{FX}/T8-5_userinfoport/chains.txt'], [
    ('userinfo/port/dot stripped', lambda o: b'A|p1|cdn.example|cdn.example|hops=1|xreg=1' in o),
    ('case/dot single hop', lambda o: b'A|p2|www.example.com|example.com|hops=0|xreg=0' in o),
])

# ---------- HL-9 ----------
def platq(o, key):
    for l in o.decode('utf-8').split('\n'):
        if l.startswith('Q|') and key in l: return True
    return False
case('T9-1_twoplatform', 'plat', [f'{FX}/T9-1_twoplatform/votes.txt', CLAIM], [
    ('withhold', lambda o: platq(o, 'verdict=WITHHOLD')),
    ('2 clusters', lambda o: platq(o, 'clusters=2')),
])
case('T9-2_oneaccount', 'plat', [f'{FX}/T9-2_oneaccount/votes.txt', CLAIM], [
    ('withhold', lambda o: platq(o, 'verdict=WITHHOLD')),
    ('1 cluster', lambda o: platq(o, 'clusters=1')),
])
case('T9-3_mixed', 'plat', [f'{FX}/T9-3_mixed/votes.txt', CLAIM], [
    ('install', lambda o: platq(o, 'verdict=INSTALL')),
    ('3 clusters 1 nonplatform', lambda o: platq(o, 'clusters=3|nonplatform=1')),
])
case('T9-4_threeplain', 'plat', [f'{FX}/T9-4_threeplain/votes.txt', CLAIM], [
    ('install', lambda o: platq(o, 'verdict=INSTALL')),
])
case('T9-5_account2sites', 'plat', [f'{FX}/T9-5_account2sites/votes.txt', CLAIM], [
    ('withhold', lambda o: platq(o, 'verdict=WITHHOLD')),
    ('1 cluster', lambda o: platq(o, 'clusters=1')),
])
case('T9-6_lookalike', 'plat', [f'{FX}/T9-6_lookalike/votes.txt', CLAIM], [
    ('lookalikes not platform', lambda o: platq(o, 'verdict=INSTALL') and platq(o, 'nonplatform=3')),
])

# ---------- HL-10 ----------
def dedupq(o, key):
    return any(l.startswith('Q|') and key in l for l in o.decode('utf-8').split('\n'))
case('T10-1_mirrorfarm', 'dedup', [f'{FX}/T10-1_mirrorfarm/pages.txt'], [
    ('1 vote', lambda o: dedupq(o, 'surviving_votes=1')),
    ('withhold', lambda o: dedupq(o, 'verdict=WITHHOLD')),
])
case('T10-1b_neardup', 'dedup', [f'{FX}/T10-1b_neardup/pages.txt'], [
    ('1 vote', lambda o: dedupq(o, 'surviving_votes=1')),
    ('withhold', lambda o: dedupq(o, 'verdict=WITHHOLD')),
])
case('T10-2_wiretruth', 'dedup', [f'{FX}/T10-2_wiretruth/pages.txt'], [
    ('4 votes', lambda o: dedupq(o, 'surviving_votes=4')),
    ('install', lambda o: dedupq(o, 'verdict=INSTALL')),
])
case('T10-3_boundary_lo', 'dedup', [f'{FX}/T10-3_boundary_lo/pages.txt'], [
    ('2 votes (J~0.37 separate)', lambda o: dedupq(o, 'surviving_votes=2')),
])
case('T10-4_boundary_hi', 'dedup', [f'{FX}/T10-4_boundary_hi/pages.txt'], [
    ('1 vote (J~0.54 merged)', lambda o: dedupq(o, 'surviving_votes=1')),
])
for gi in range(1, 7):
    case(f'T10-5_guard{gi}', 'dedup', [f'{FX}/T10-5_guard{gi}/pages.txt'], [
        ('install', lambda o: dedupq(o, 'verdict=INSTALL')),
        ('3 votes', lambda o: dedupq(o, 'surviving_votes=3')),
    ])
# T10-6: documented residual — attacker diversifies surroundings past 0.5.
# Expected: INSTALL (4 surviving votes). This is the known escape hatch,
# reported honestly, not a kill.
case('T10-6_diversifiedmirror', 'dedup', [f'{FX}/T10-6_diversifiedmirror/pages.txt'], [
    ('residual: 4 votes survive', lambda o: dedupq(o, 'surviving_votes=4')),
    ('residual: installs (documented)', lambda o: dedupq(o, 'verdict=INSTALL')),
])

rows = []
fails = 0
for cid, mode, args, checks in CASES:
    outs = [run(mode, *args) for _ in range(2)]
    h1 = hashlib.sha256(outs[0]).hexdigest()
    h2 = hashlib.sha256(outs[1]).hexdigest()
    det = 'IDENTICAL' if h1 == h2 else 'MISMATCH'
    with open(f'{OUT}/{cid}.out', 'wb') as f:
        f.write(outs[0])
    for name, fn in checks:
        try:
            ok = bool(fn(outs[0]))
        except Exception as e:
            ok = f'ERROR {e}'
        status = 'PASS' if ok is True else 'FAIL'
        if status == 'FAIL': fails += 1
        rows.append((cid, mode, h1[:12], det, name, status))
    if det == 'MISMATCH':
        fails += 1
        rows.append((cid, mode, h1[:12], det, 'determinism', 'FAIL'))

with open(f'{OUT}/battery_summary.tsv', 'w') as f:
    f.write('case\tmode\tsha12\tdeterminism\tcheck\tstatus\n')
    for r in rows:
        f.write('\t'.join(r) + '\n')
npass = sum(1 for r in rows if r[5] == 'PASS')
print(f'{npass}/{len(rows)} checks PASS, {fails} failures')
sys.exit(1 if fails else 0)
