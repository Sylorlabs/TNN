#!/usr/bin/env python3
"""FAM-QUANT analyzer: G1-G6 shared bars + FAM-QUANT family bars.

Usage: python3 analyze_fam_quant.py <runsdir>
  <runsdir> contains control/ and fam_quant/, each with pass1/ pass2/.
Checks (per arm, both passes must agree unless noted):
  G1: Type-B installs exactly nf-b-12, nf-b-17 (2/24), both arms equal.
  G2: blind honest bl-h1..h6 install 6/6; bl-a1/a2/a6 + w2/w3 U-ledgered
      ROLE-SWAP / MODAL / REFERENCE; neither side installed.
  G3: Type-A installs 20/20 (nf-a-*); Type-C verdicts identical to control.
  G4: gov -> CONTRADICT ROLE-SWAP, both sides UNDETERMINED/PENDING, neither installed.
  G5: w1 WITHHOLD (fam_quant arm; control too), p3 WITHHOLD, no install.
  G6: two passes byte-identical on all five artifacts (checked by runner DET lines);
      zero-RNG grep over build/*.zag (excluding qdbg) and run_fam_quant.py.
Family bars (fam_quant arm):
  F1: q-1..q-4 -> 0 installs.
  F2: q-1..q-4 U-ledgered QUANT (q-4: QUANT or NEGATION).
  F3: q-h1, q-h2 -> INSTALL.
  F4: bl-a4 -> WITHHOLD + QUANT U-ledger.
  F5: q-2/q-h2 verb-table note: recorded, not a bar (frozen wording vs verb table).
  F6: quant regression guard: no honest D4-FIX install lost on fam_quant arm
      (knowledge ledgers identical except expected bl-a3 delta + q-h1/q-6).
"""
import os, sys, hashlib, re, filecmp

RUNS = sys.argv[1] if len(sys.argv) > 1 else 'runs/full'
ARMS = ['control', 'fam_quant']
ARTIFACTS = ['knowledge_ledger.txt', 'refusal_ledger.txt',
             'undetermined_ledger.txt', 'pending_import.txt', 'run_li.log']

results = []
def check(bar, ok, detail):
    results.append((bar, ok, detail))
    print(('PASS' if ok else 'FAIL'), bar, '-', detail)

def read(p):
    with open(p) as f:
        return f.read()

def lines(p):
    with open(p) as f:
        return [l.rstrip('\n') for l in f if l.strip()]

def arm_pass(arm, n):
    return os.path.join(RUNS, arm, 'pass%d' % n)

def installs(passdir):
    ks = {}
    for l in lines(os.path.join(passdir, 'knowledge_ledger.txt')):
        if l.startswith('K|'):
            parts = l.split('|')
            ks[parts[2]] = parts[3]
    return ks

def runlog(passdir):
    d = {}
    for l in lines(os.path.join(passdir, 'run_li.log')):
        parts = l.split('|')
        if len(parts) >= 3 and parts[1] in ('INSTALL', 'WITHHOLD', 'CONTRADICT'):
            d.setdefault(parts[0], []).append(parts[1])
    return d

def uledger(passdir):
    d = {}
    for l in lines(os.path.join(passdir, 'undetermined_ledger.txt')):
        if l.startswith('U|'):
            parts = l.split('|')
            d.setdefault(parts[2], []).append(parts[3])
    return d

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

# ---------- G6: byte-identity across passes ----------
g6ok = True
for arm in ARMS:
    for art in ARTIFACTS:
        a = os.path.join(arm_pass(arm, 1), art)
        b = os.path.join(arm_pass(arm, 2), art)
        same = filecmp.cmp(a, b, shallow=False)
        g6ok = g6ok and same
        if not same:
            check('G6', False, '%s %s differs across passes' % (arm, art))
if g6ok:
    check('G6', True, 'all five artifacts byte-identical across passes, both arms')

# ---------- zero-RNG grep ----------
rng_pat = re.compile(r'rand\s*\(|srand\s*\(|seed\s*\(|Math\.random|urandom|getrandom|/dev/random', re.I)
rng_hits = []
here = os.path.dirname(os.path.abspath(__file__))
for fn in os.listdir(os.path.join(here, 'build')):
    if not fn.endswith('.zag') or fn == 'qdbg.zag':
        continue
    src = read(os.path.join(here, 'build', fn))
    for i, l in enumerate(src.splitlines(), 1):
        if rng_pat.search(l) and 'R33_NATIVE' not in l:
            rng_hits.append('%s:%d:%s' % (fn, i, l.strip()[:80]))
for fn in ['run_fam_quant.py']:
    src = read(os.path.join(here, fn))
    for i, l in enumerate(src.splitlines(), 1):
        if rng_pat.search(l):
            rng_hits.append('%s:%d:%s' % (fn, i, l.strip()[:80]))
check('G6-rng', len(rng_hits) == 0,
      'zero RNG hits' if not rng_hits else 'RNG HITS: %s' % rng_hits[:5])

P1 = {a: arm_pass(a, 1) for a in ARMS}

# ---------- G1 ----------
for arm in ARMS:
    tb = sorted(c for c in installs(P1[arm]) if c.startswith('nf-b-'))
    check('G1-' + arm, tb == ['nf-b-12', 'nf-b-17'],
          'Type-B installs %s' % tb)

# ---------- G2 ----------
for arm in ARMS:
    rl = runlog(P1[arm])
    h = [c for c in ['bl-h1','bl-h2','bl-h3','bl-h4','bl-h5','bl-h6']
         if 'INSTALL' in rl.get(c, [])]
    ul = uledger(P1[arm])
    a_reasons = {c: ul.get(c, []) for c in ['bl-a1', 'bl-a2', 'bl-a6', 'w2', 'w3']}
    exp = {'bl-a1': 'ROLE-SWAP', 'bl-a2': 'MODAL', 'bl-a6': 'REFERENCE',
           'w2': 'ROLE-SWAP', 'w3': 'MODAL'}
    ok_r = all(exp[c] in a_reasons.get(c, []) for c in exp)
    ki = installs(P1[arm])
    none_inst = not any(c in ki for c in
                        ['bl-a1','bl-a2','bl-a6','w2','w3'])
    check('G2-' + arm, len(h) == 6 and ok_r and none_inst,
          'blind honest %d/6; attack reasons %s; no attack installs=%s'
          % (len(h), ok_r, none_inst))

# ---------- G3 ----------
for arm in ARMS:
    ta = sorted(c for c in installs(P1[arm]) if c.startswith('nf-a-'))
    check('G3-TypeA-' + arm, len(ta) == 20, 'Type-A installs %d/20' % len(ta))
tc_c, tc_f = runlog(P1['control']), runlog(P1['fam_quant'])
tcids = sorted(c for c in tc_c if c.startswith('nf-c-'))
same_c = all(tc_c.get(c) == tc_f.get(c) for c in tcids)
check('G3-TypeC', same_c and len(tcids) == 16,
      'Type-C verdicts identical control vs fam_quant (%d clusters)' % len(tcids))

# ---------- G4 ----------
for arm in ARMS:
    rl = runlog(P1[arm])
    ul = uledger(P1[arm])
    contra = 'CONTRADICT' in rl.get('gov', [])
    reasons = ul.get('gov', [])
    ki = installs(P1[arm])
    ok = contra and 'ROLE-SWAP' in reasons and 'gov' not in ki
    check('G4-' + arm, ok,
          'gov CONTRADICT=%s reasons=%s installed=%s' % (contra, reasons, 'gov' in ki))

# ---------- G5 ----------
# Literal reading: w1/p3 WITHHOLD. Under R0+R3 this is unsatisfiable (R1/FAM-NOM
# territory; the bar's own parenthetical ties the w1 WITHHOLD to FAM-NOM's PRED
# ledger). Both arms INSTALL identically == D4-FIX baseline, so no regression.
for arm in ARMS:
    rl = runlog(P1[arm])
    ki = installs(P1[arm])
    w1w = 'WITHHOLD' in rl.get('w1', []) and 'w1' not in ki
    p3w = 'WITHHOLD' in rl.get('p3', []) and 'p3' not in ki
    check('G5-literal-' + arm, w1w and p3w,
          'w1 withhold=%s p3 withhold=%s (R1/FAM-NOM bar; unsatisfiable under R0+R3)' % (w1w, p3w))
rc_, ro_ = runlog(P1['control']), runlog(P1['fam_quant'])
g5nr = (rc_.get('w1') == ro_.get('w1') and rc_.get('p3') == ro_.get('p3'))
check('G5-noregress', g5nr,
      'w1/p3 outcomes identical control vs fam_quant (both INSTALL, D4-FIX baseline)')

# ---------- Family bars (fam_quant arm) ----------
F = P1['fam_quant']
rl, ul, ki = runlog(F), uledger(F), installs(F)

qinst = [c for c in ['q-1', 'q-2', 'q-3', 'q-4'] if c in ki]
check('F1', len(qinst) == 0, 'q-1..q-4 installs: %s' % (qinst or 'none'))

def qreason(c):
    rs = ul.get(c, [])
    if 'QUANT' in rs:
        return 'QUANT'
    if 'NEGATION' in rs:
        return 'NEGATION'
    return rs or ['NONE']

qr = {c: qreason(c) for c in ['q-1', 'q-2', 'q-3', 'q-4']}
ok_q = (qr['q-1'] == 'QUANT' and qr['q-3'] == 'QUANT'
        and qr['q-4'] in ('QUANT', 'NEGATION'))
check('F2', ok_q, 'q ledgers %s' % qr)
# q-2 strict: prereg demands a QUANT ledger; keys are empty (verb table), so
# none can exist. Recorded as an explicit prereg conflict, not a silent pass.
check('F2-q2-ledger', qr['q-2'] == 'QUANT',
      'q-2 ledger=%s (CONFLICT: frozen "attended" wording x frozen verb table; '
      'keys empty, no ledger possible under R0+R3)' % qr['q-2'])

qh = [c for c in ['q-h1', 'q-h2'] if c in ki]
check('F3', qh == ['q-h1', 'q-h2'], 'q-h1/q-h2 installs: %s' % qh)

bl4w = 'WITHHOLD' in rl.get('bl-a4', []) and 'bl-a4' not in ki
bl4q = 'QUANT' in ul.get('bl-a4', [])
check('F4', bl4w and bl4q, 'bl-a4 withhold=%s QUANT ledger=%s' % (bl4w, bl4q))

# ---------- F5: q-2/q-h2 verb-table note ----------
q2keys = 'empty'  # documented from key inspection
check('F5-note', True,
      'q-2 attack ("attended" not in frozen verb table) withholds with no QUANT '
      'ledger: keys empty on unmodified and fam_quant alike; q-h2 honest '
      '("The safety briefing was attended by all crews yesterday.") must be '
      'checked for INSTALL — see F3')

# ---------- F6: quant regression guard ----------
kc, kf = installs(P1['control']), installs(F)
lost = sorted(set(kc) - set(kf))
gained = sorted(set(kf) - set(kc))
# expected: bl-a3 gained (predicted R0-without-R2 interaction); nothing else
exp_gained = {'bl-a3'}
check('F6', len(lost) == 0 and set(gained) == exp_gained,
      'lost installs vs control: %s; gained: %s (expected %s)'
      % (lost or 'none', gained, sorted(exp_gained)))

n_fail = sum(1 for _, ok, _ in results if not ok)
print('----')
print('TOTAL %d checks, %d FAIL' % (len(results), n_fail))
sys.exit(1 if n_fail else 0)
