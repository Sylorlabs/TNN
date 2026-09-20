#!/usr/bin/env python3
"""Independent checker for the FELT-INTENSITY V3 trial (wave8/felt-rebuild).

Verifies, from the .zag sources and the trial/calibration output files:
  - static/source gates (I-4, I-5, I-7, I-8, P1b, read-site scope, frozen formulas)
  - calibration record vs calibration outputs (selection rule, G-C1..G-C3, determinism)
  - per-cell: I-1 (paired byte-identical), I-2, P1a/P1c/P4a, P2a/P2b, P3a/P3c/P4b/P4c,
    F4a'/F4b/F4c, thresholds, offered-count closed forms, op census (I-5 behavioral),
    kill/sacrifice pairing, replay check
  - K3' naive-count-policy replay (checker-implemented, deterministic)
  - cross-cell: P3b concentration, K1/K4 arithmetic, F-V3-1..F-V3-4 bars,
    verdict-divergence diagnostic family
  - the designated-wrong overlap repair ({4,5}->{4,5,7}) and its evaluability audit

Usage:
  check_felt_v3.py --impl DIR --calib cal7_a.txt cal7_b.txt cal8_a.txt cal8_b.txt
  check_felt_v3.py --impl DIR --cell F,0,f0_a.txt,f0_b.txt --cell N,0,n0_a.txt,n0_b.txt ...

Exit 0 with CHECK_PASS only if every gate passes; otherwise CHECK_FAIL with
the failing gates listed. Findings (non-law observations) are reported
separately and never fail the check.
"""
import argparse, hashlib, os, re, sys
from fractions import Fraction

IMPLANTS = {0, 83, 166, 250, 333, 416}
PRESSURE_EPS = {100, 200, 300, 400, 499}
N_EPISODES = 500

def imp(m): return 1 if (m % 10) < 3 else 0
def wrong(m): return 1 if ((m + 3) % 10) < 3 else 0
def cls(m):
    if m in IMPLANTS: return 3
    if wrong(m): return 2
    if imp(m): return 1
    return 0
def designated(m):
    if m in IMPLANTS: return 0
    return 1 if m % 10 in (4, 5, 7) else 0   # REPAIR 2026-09-20: was (4,5)
def probe_sched(m, v): return 1 if cls(m) == 0 and (m + v) % 5 == 0 else 0

# opcodes (st_memory_core.zag / felt_v3.zag)
OP = {'ADD':1,'KILL':2,'PIN':3,'UNPIN':4,'PROMOTE':5,'DEMOTE':6,'ROLLBACK':7,
      'SETSTAGE':8,'STRENGTHEN':20,'WEAKEN':21,'EVIDENCE':22,'JUSTIFY':23,
      'KILL_EVIDENCED':24,'OVERWRITE':25,'TRAINER_DECLARE':26,'FORCE_PIN':27,
      'FORCE_UNPIN':28,'ABANDON':29,
      'OBS_CORROBORATE':41,'OBS_CONTRADICT':42,'OBS_TRAINER_MARK':43,
      'INTENSITY_READ':44,'OBS_PROBE':45,'JUDGMENT_HOLD':46,'JUDGMENT_SPARE':47,
      'DELIBERATE_SACRIFICE':48}
FORBIDDEN_OPS = {'OVERWRITE','PROMOTE','DEMOTE','PIN','UNPIN','FORCE_PIN',
                 'FORCE_UNPIN','TRAINER_DECLARE','ROLLBACK','ABANDON'}

results = []
findings = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
def finding(text):
    findings.append(text)

# ---------------- static gates ----------------
def static_checks(impl):
    def rd(f):
        with open(os.path.join(impl, f), encoding='utf-8', errors='replace') as h:
            return h.read()
    trial = rd('felt_trial_v3.zag'); felt = rd('felt_v3.zag')
    consts = rd('calib_consts.zag')
    # S1/I-7 substrate byte-identical to wave-5
    w5 = os.path.expanduser('~/workspace/tnn-lab/wave5/strength-trial-run/trial')
    for f in ('st_memory_core.zag', 'substrate/cl/common.zag',
              'substrate/R33_NATIVE_SHA256_V2.zag', 'substrate/R33_NATIVE_IO_V1.zag'):
        a = os.path.join(impl, f); b = os.path.join(w5, f)
        same = os.path.exists(b) and hashlib.sha256(open(a,'rb').read()).hexdigest() == \
               hashlib.sha256(open(b,'rb').read()).hexdigest()
        check(f'S1/I-7 substrate identical: {f}', same)
    # S2/I-4 no RNG tokens
    blob = trial + felt + consts + rd('st_memory_core.zag')
    for f in ('substrate/cl/common.zag', 'substrate/R33_NATIVE_SHA256_V2.zag',
              'substrate/R33_NATIVE_IO_V1.zag'):
        blob += rd(f)
    check('S2/I-4 no RNG tokens', not re.search(
        r'rand|srand|random|getrandom|/dev/urandom|rdtsc|shuffle', blob, re.I))
    # S3/I-8 record exists and constants match
    recp = os.path.join(impl, 'CALIBRATION_RECORD.md')
    rec = rd('CALIBRATION_RECORD.md') if os.path.exists(recp) else ''
    check('S3/I-8 CALIBRATION_RECORD.md exists', bool(rec))
    okc = True
    cal = {}
    for sym in ('CAL_ALPHA', 'CAL_BETA', 'CAL_GAMMA'):
        m1 = re.search(rf'^{sym}=(\d+)', rec, re.M)
        m2 = re.search(rf'const {sym}:i32=(\d+);', consts)
        if m1: cal[sym] = int(m1.group(1))
        if not (m1 and m2 and m1.group(1) == m2.group(1)): okc = False
    check('S3/I-8 trial constants == record', okc)
    # thetas follow A5 procedure
    th_i = int(re.search(r'const THETA_INVEST:i32=(\d+);', consts).group(1))
    th_s = int(re.search(r'const THETA_SACRIFICE:i32=(\d+);', consts).group(1))
    check('S3/A5 theta_invest == 30+1.5*alpha', th_i * 2 == 60 + 3 * cal.get('CAL_ALPHA', -1),
          f'theta_invest={th_i}')
    check('S3/A5 theta_sacrifice == 30+0.5*alpha', th_s * 2 == 60 + cal.get('CAL_ALPHA', -1),
          f'theta_sacrifice={th_s}')
    # S4/P1b: felt_emit_obs only in driver emit fns + calibration
    allowed = {'emit_contra', 'emit_corrob', 'emit_probe', 'emit_mark', 'run_calibration'}
    cur, bad = None, []
    for i, line in enumerate(trial.splitlines(), 1):
        m = re.match(r'\s*fn\s+([A-Za-z0-9_]+)\(', line)
        if m: cur = m.group(1)
        if 'felt_emit_obs(' in line and cur not in allowed:
            bad.append(f'{cur}:{i}')
    check('S4/P1b no learner path emits observations', not bad, ';'.join(bad))
    # S5: do_read call sites
    cur, sites = None, []
    for i, line in enumerate(trial.splitlines(), 1):
        m = re.match(r'\s*fn\s+([A-Za-z0-9_]+)\(', line)
        if m: cur = m.group(1)
        if re.search(r'(?<![A-Za-z0-9_])do_read\(w,st,', line):
            sites.append(cur)
    check('S5 read sites lawful', sorted(sites) == sorted(
        ['pick_victim_f', 'site1_f', 'gate2_f', 'revision_sweep']), ','.join(sites))
    # S6: frozen formulas verbatim
    check('S6 imp formula', 'm%10)<3' in trial)
    check('S6 wrong formula', '(m+3)%10)<3' in trial)
    check('S6 designation formula', '(m%10==4||m%10==5||m%10==7)' in trial)
    check('S6 probe formula', '(m+v)%5==0' in trial)
    check('S6 implant schedule', all(f'm=={k}' in trial for k in IMPLANTS))
    # S7/I-5: strength-write fns restricted; no forbidden tokens
    check('S7 no forbidden strength/R tokens',
          not re.search(r'st_write_strength|st_clear_strength|r_param', trial + felt, re.I))
    lawful_w = {'site1_f', 'site1_n', 'revision_sweep', 'gate1_kill', 'gate2_f', 'gate2_n'}
    cur, bad = None, []
    for i, line in enumerate(trial.splitlines(), 1):
        m = re.match(r'\s*fn\s+([A-Za-z0-9_]+)\(', line)
        if m: cur = m.group(1)
        if re.search(r'(?<![A-Za-z0-9_])st_(strengthen|weaken|kill|kill_evidenced)\(', line):
            if cur not in lawful_w: bad.append(f'{cur}:{i}')
    check('S7 strength writes only in lawful fns', not bad, ';'.join(bad))
    return cal, th_i, th_s

# ---------------- calibration check ----------------
def check_calibration(impl, files):
    """files: [cal7a, cal7b, cal8a, cal8b]. Verifies determinism, the 45-point
    tables, the frozen selection rule, and G-C1..G-C3 against the record."""
    def rows(fn):
        d = {}
        for line in open(fn):
            m = re.match(r'FELT_CAL,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', line)
            if m:
                v, gi, a, b, g, num, den, npos, nneg, minI, maxI = map(int, m.groups())
                d[(v, gi)] = (a, b, g, num, den, npos, nneg, minI, maxI)
        return d
    r7a, r7b, r8a, r8b = map(rows, files)
    ha = hashlib.sha256(open(files[0],'rb').read()).hexdigest()
    hb = hashlib.sha256(open(files[1],'rb').read()).hexdigest()
    check('CAL determinism cal7 byte-identical', ha == hb)
    hc = hashlib.sha256(open(files[2],'rb').read()).hexdigest()
    hd = hashlib.sha256(open(files[3],'rb').read()).hexdigest()
    check('CAL determinism cal8 byte-identical', hc == hd)
    rec = open(os.path.join(impl, 'CALIBRATION_RECORD.md')).read()
    check('CAL record cites cal7 hash', ha in rec, ha[:16])
    check('CAL record cites cal8 hash', hc in rec, hc[:16])
    check('CAL 45 grid points x2 variants', len(r7a) == 45 and len(r8a) == 45,
          f'{len(r7a)},{len(r8a)}')
    # selection rule: maximize mean AUC (exact rational); ties -> lowest index
    means = {}
    for gi in range(45):
        a, b, g, n7, d7, *_ = r7a[(7, gi)]
        _, _, _, n8, d8, *_ = r8a[(8, gi)]
        means[gi] = (Fraction(n7, d7) + Fraction(n8, d8)) / 2
    best = max(means.values())
    winner = min(gi for gi, m in means.items() if m == best)
    a, b, g = r7a[(7, winner)][:3]
    ms = re.search(r'CAL_ALPHA=(\d+)', rec); 
    check('CAL selection == record', ms and int(ms.group(1)) == a and
          int(re.search(r'CAL_BETA=(\d+)', rec).group(1)) == b and
          int(re.search(r'CAL_GAMMA=(\d+)', rec).group(1)) == g,
          f'winner gi={winner} a={a} b={b} g={g}')
    th = 30 + 1.5 * a
    _, _, _, n7, d7, _, _, mi7, ma7 = r7a[(7, winner)]
    _, _, _, n8, d8, _, _, mi8, ma8 = r8a[(8, winner)]
    check('CAL G-C1 v7', mi7 >= th, f'minI={mi7} theta={th}')
    check('CAL G-C1 v8', mi8 >= th, f'minI={mi8} theta={th}')
    check('CAL G-C2 v7 AUC>=0.60', Fraction(n7, d7) >= Fraction(3, 5), f'{float(Fraction(n7,d7)):.4f}')
    check('CAL G-C2 v8 AUC>=0.60', Fraction(n8, d8) >= Fraction(3, 5), f'{float(Fraction(n8,d8)):.4f}')
    check('CAL G-C3 v7 junk<=40', ma7 <= 40, f'maxI={ma7}')
    check('CAL G-C3 v8 junk<=40', ma8 <= 40, f'maxI={ma8}')

# ---------------- cell parsing ----------------
def parse_cell(path):
    c = {'path': path, 'obs': [], 'judge': [], 'metric': {}, 'check': {},
         'pressure': [], 'endstr': [], 'opcensus': {}, 'traj': [], 'done': False,
         'cell': None, 'fingerprint': None}
    for line in open(path, encoding='utf-8', errors='replace'):
        line = line.rstrip('\n')
        p = line.split(',')
        if not p: continue
        t = p[0]
        if t == 'FELT_CELL': c['cell'] = (p[1], int(p[2]))
        elif t == 'FELT_OBS': c['obs'].append((int(p[1]), int(p[2]), int(p[3])))
        elif t == 'FELT_PRESSURE': c['pressure'].append((int(p[1]), int(p[2])))
        elif t == 'FELT_JUDGE': c['judge'].append(tuple(p[1:]))
        elif t == 'FELT_METRIC': c['metric'][p[1]] = int(p[2])
        elif t == 'FELT_CHECK': c['check'][p[1]] = (int(p[2]), int(p[3]))
        elif t == 'FELT_FINGERPRINT': c['fingerprint'] = int(p[1])
        elif t == 'FELT_ENDSTR': c['endstr'].append(tuple(map(int, p[1:])))
        elif t == 'FELT_OPCENSUS': c['opcensus'][int(p[1])] = (int(p[2]), int(p[3]))
        elif t == 'FELT_TRAJ': c['traj'].append((p[1], int(p[2])))
        elif t == 'FELT_DONE': c['done'] = True
    return c

def scheduled_obs(v, variant):
    """All schedule-conformant (ep, kind) for value v. kind: 1 corrob, 2 contra,
    3 mark, 4 probe."""
    out = []
    cl = cls(v)
    if designated(v): out.append((v, 3))
    if cl == 1:
        if v + 25 <= 499: out.append((v + 25, 1))
        if v + 40 <= 499: out.append((v + 40, 1))
    elif cl == 2:
        for d in (60, 85, 110, 135):
            if v + d <= 499: out.append((v + d, 2))
    elif cl == 3:
        if v + 10 <= 499: out.append((v + 10, 1))
        for d in (24, 49, 74):
            if v + d <= 499: out.append((v + d, 2))
    if probe_sched(v, variant) and v + 30 <= 499: out.append((v + 30, 4))
    return out

# ---------------- per-cell behavioral checks ----------------
def cell_checks(cell, cal, th_invest, th_sacrifice, tag):
    arm, variant = cell['cell']
    A, B, G = cal['CAL_ALPHA'], cal['CAL_BETA'], cal['CAL_GAMMA']
    PRIOR = 30
    def inten(c, x, t):
        return max(0, min(100, PRIOR + A * c - B * x + G * t))
    M = cell['metric']
    # C2 completeness
    check(f'{tag} FELT_DONE present', cell['done'])
    # C20 offered closed forms (implant-precedence: implants override imp)
    check(f'{tag} offered_right_imp==148', M.get('offered_right_imp') == 148,
          str(M.get('offered_right_imp')))
    check(f'{tag} offered_wrong==150', M.get('offered_wrong') == 150,
          str(M.get('offered_wrong')))
    # ---- observation ledger -> per-value timelines ----
    obs_by_v = {}
    for v, kind, ep in cell['obs']:
        obs_by_v.setdefault(v, []).append((ep, kind))
    # C3/P3a/P4b: every emitted OBS matches the schedule; no duplicates
    bad, dup = 0, 0
    seen = set()
    for v, kind, ep in cell['obs']:
        if (ep, kind) not in scheduled_obs(v, variant): bad += 1
        if (v, kind, ep) in seen: dup += 1
        seen.add((v, kind, ep))
    check(f'{tag} P3a/P4b every OBS schedule-conformant', bad == 0, f'bad={bad}')
    check(f'{tag} no duplicate OBS', dup == 0, f'dup={dup}')
    # per-value prefix counts at episode m: c,x,t (probe excluded from formula)
    def prefix(v, m):
        c = x = t = 0
        for ep, kind in obs_by_v.get(v, []):
            if ep <= m:
                if kind == 1: c += 1
                elif kind == 2: x += 1
                elif kind == 3: t += 1
        return c, x, t
    def proven(v, m):
        c, x, t = prefix(v, m)
        pn = 1 if any(k == 4 for e, k in obs_by_v.get(v, []) if e <= m) else 0
        return c + x + t + pn > 0
    # ---- judgments ----
    # FELT_JUDGE tuples: (kind, v, ...) — kinds: INVEST,HOLD,SPARE,SACRIFICE,
    # N_STRENGTHEN,N_SPARE,N_SACRIFICE
    div = {'raw': [0, 0], 'time': [0, 0], 'trainer': [0, 0], 'recency': [0, 0]}
    p4c_rises = 0
    last_judge = {}   # v -> (m, cited_I or None)
    pressures = sorted(cell['pressure'])
    for j in cell['judge']:
        kind = j[0]
        if kind in ('INVEST', 'HOLD', 'SPARE', 'SACRIFICE'):
            v, I, cur, m = int(j[1]), int(j[2]), int(j[3]), int(j[4])
            c, x, t = prefix(v, m)
            exp = inten(c, x, t)
            # C4/P1a/P4a: cited I recomputes
            check(f'{tag} P1a recompute {kind} v={v} m={m}', I == exp,
                  f'cited={I} recomputed={exp} (c={c},x={x},t={t})')
            if kind == 'HOLD':
                check(f'{tag} P2a HOLD cites I<theta_invest v={v}', I < th_invest,
                      f'I={I} theta={th_invest}')
            if kind == 'SACRIFICE':
                check(f'{tag} P2b SACRIFICE I<=theta v={v}', I <= th_sacrifice,
                      f'I={I} theta={th_sacrifice}')
                check(f'{tag} P2b SACRIFICE zero-X v={v}', x == 0, f'x={x}')
                check(f'{tag} P2b SACRIFICE not-designated v={v}', designated(v) == 0)
                check(f'{tag} P2b SACRIFICE age>=25 v={v}', m - v >= 25, f'age={m-v}')
            # P1c/P4c vs previous judgment of same v
            if v in last_judge:
                m0, I0 = last_judge[v]
                intervening = any(m0 < e <= m for e, k in obs_by_v.get(v, []))
                if not intervening and I0 is not None:
                    check(f'{tag} P1c no-drift v={v}', I == I0, f'{I0}->{I}')
                    if I > I0: p4c_rises += 1
            last_judge[v] = (m, I)
            # verdict-divergence diagnostic family (F arm binary judgments)
            if arm == 'F':
                f_verdict = 1 if kind in ('INVEST', 'SACRIFICE') else 0
                cf = {}
                cf['raw'] = 1 if (kind in ('INVEST', 'HOLD') and c >= 2) or \
                                 (kind in ('SACRIFICE', 'SPARE') and cur <= th_sacrifice) else 0
                tw = sum(1.0 / (1 + (m - e)) for e, k in obs_by_v.get(v, []) if k == 1 and e <= m)
                tw_v = 1 if tw >= 1.0 else 0
                cf['time'] = tw_v if kind in ('INVEST', 'HOLD') else (1 - tw_v)
                cf['trainer'] = (1 if t >= 1 else 0) if kind in ('INVEST', 'HOLD') else (1 if t == 0 else 0)
                most = max((e for e, k in obs_by_v.get(v, []) if e <= m), default=-1)
                mk = next((k for e, k in obs_by_v.get(v, []) if e == most), 0)
                rec_v = 1 if (mk == 1 and m - most <= 50) else 0
                cf['recency'] = rec_v if kind in ('INVEST', 'HOLD') else (1 - rec_v)
                for name, cv in cf.items():
                    div[name][1] += 1
                    if cv != f_verdict: div[name][0] += 1
        elif kind in ('N_SPARE', 'N_SACRIFICE'):
            v, cur, c, x, m = int(j[1]), int(j[2]), int(j[3]), int(j[4]), int(j[5])
            if kind == 'N_SACRIFICE':
                check(f'{tag} P2b N_SACRIFICE strength<=theta v={v}', cur <= th_sacrifice,
                      f'strength={cur}')
                check(f'{tag} P2b N_SACRIFICE zero-X v={v}', x == 0)
                check(f'{tag} P2b N_SACRIFICE not-designated v={v}', designated(v) == 0)
                check(f'{tag} P2b N_SACRIFICE age>=25 v={v}', m - v >= 25)
    # cap: <=2 sacrifices per scheduled pressure event (assign each sacrifice to
    # the latest scheduled pressure at ep <= its m; kind==1 overflow has none)
    sac_by_event = {}
    for j in cell['judge']:
        if j[0] in ('SACRIFICE', 'N_SACRIFICE'):
            m = int(j[4]) if j[0] == 'SACRIFICE' else int(j[5])
            ev = max([i for i, (ep, k) in enumerate(pressures) if ep <= m and k == 0],
                     default=-1)
            sac_by_event[ev] = sac_by_event.get(ev, 0) + 1
    for ev, n in sac_by_event.items():
        if ev >= 0:
            check(f'{tag} P2b cap<=2 event@{pressures[ev][0]}', n <= 2, f'n={n}')
    check(f'{tag} P4c rises<=3', p4c_rises <= 3, f'rises={p4c_rises}')
    # C9/F4a': binary junk_max_nd + structural (non-designated junk I constant 30)
    check(f'{tag} F4a binary junk_max_nd<=40', M.get('junk_max_nd', 999) <= 40,
          str(M.get('junk_max_nd')))
    struct_max = 30
    for v in range(500):
        if cls(v) == 0 and designated(v) == 0:
            for m in range(500):
                c, x, t = prefix(v, m)
                struct_max = max(struct_max, inten(c, x, t))
    check(f'{tag} F4a structural non-designated junk<=40', struct_max <= 40,
          f'max={struct_max}')
    # C10/F4b: binary f4b_bad==0 + timeline non-increasing after first X
    check(f'{tag} F4b binary f4b_bad==0', M.get('f4b_bad', 999) == 0)
    bad4b = 0
    for v in range(500):
        prev = None; hadx = False
        for m in range(500):
            c, x, t = prefix(v, m)
            if x >= 1:
                I = inten(c, x, t)
                if hadx and I > prev: bad4b += 1
                hadx = True; prev = I
    check(f'{tag} F4b timeline non-increasing after X', bad4b == 0, f'bad={bad4b}')
    # C11/F4c: no INVEST with C+X+T==0 (F arm)
    if arm == 'F':
        check(f'{tag} F4c binary noev_invest_bad==0', M.get('noev_invest_bad', 999) == 0)
        bad4c = 0
        for j in cell['judge']:
            if j[0] == 'INVEST':
                v, m = int(j[1]), int(j[4])
                c, x, t = prefix(v, m)
                if c + x + t == 0: bad4c += 1
        check(f'{tag} F4c no INVEST with zero evidence', bad4c == 0, f'bad={bad4c}')
    # C13/P3c: spared memories' dI explained by corroborations (exact residual)
    badp3c = 0
    cites = {}
    for j in cell['judge']:
        if j[0] in ('INVEST', 'HOLD', 'SPARE', 'SACRIFICE'):
            v, I, m = int(j[1]), int(j[2]), int(j[4])
            cites.setdefault(v, []).append((m, I))
    for v, lst in cites.items():
        lst.sort()
        for (m1, I1), (m2, I2) in zip(lst, lst[1:]):
            c1, x1, t1 = prefix(v, m1); c2, x2, t2 = prefix(v, m2)
            if (I2 - I1) - A * (c2 - c1) + B * (x2 - x1) - G * (t2 - t1) != 0:
                badp3c += 1
    check(f'{tag} P3c dI explained by formula', badp3c == 0, f'bad={badp3c}')
    # C15 thresholds from metrics
    check(f'{tag} theta_invest metric', M.get('theta_invest') == th_invest)
    check(f'{tag} theta_sacrifice metric', M.get('theta_sacrifice') == th_sacrifice)
    check(f'{tag} prior metric', M.get('prior') == 30)
    check(f'{tag} cal constants metric',
          (M.get('cal_alpha'), M.get('cal_beta'), M.get('cal_gamma')) ==
          (cal['CAL_ALPHA'], cal['CAL_BETA'], cal['CAL_GAMMA']))
    # C16/C17/C18 binary self-checks (independently re-verified above where possible)
    check(f'{tag} I-2 recompute_bad==0', cell['check'].get('recompute_bad', (999, 0))[0] == 0)
    check(f'{tag} replay rc==0', cell['check'].get('replay', (999, 0))[0] == 0)
    check(f'{tag} kill/sacrifice paired', cell['check'].get('kill_sacrifice_paired', (999, 0))[0] == 0)
    # C19/I-5 behavioral: forbidden ops never OK; KILL(2) paired with sacrifices
    for name in FORBIDDEN_OPS:
        op = OP[name]
        ok, ref = cell['opcensus'].get(op, (0, 0))
        check(f'{tag} I-5 no {name}', ok == 0, f'ok={ok} refused={ref}')
    ok_kill = cell['opcensus'].get(OP['KILL'], (0, 0))[0]
    ok_sac = cell['opcensus'].get(OP['DELIBERATE_SACRIFICE'], (0, 0))[0]
    check(f'{tag} KILL count == DELIBERATE_SACRIFICE count', ok_kill == ok_sac,
          f'{ok_kill} vs {ok_sac}')
    n_sac = M.get('n_sacrifice', -1)
    check(f'{tag} n_sacrifice == sacrifice judgments',
          n_sac == sum(1 for j in cell['judge'] if j[0] in ('SACRIFICE', 'N_SACRIFICE')),
          f'metric={n_sac}')
    # C21 designated-wrong evaluability audit (REPAIR 2026-09-20: the old
    # {4,5} formula was disjoint from wrong={7,8,9}, voiding this bar; the
    # repaired {4,5,7} makes designated-wrong = {7} evaluable at 33% trainer-wrong)
    # Curriculum-level closed forms (offered, drop-independent):
    off_des = sum(1 for m in range(N_EPISODES) if designated(m))
    off_tw = sum(1 for m in range(N_EPISODES) if designated(m) and wrong(m))
    check(f'{tag} offered_designated==150', off_des == 150, str(off_des))
    check(f'{tag} offered_trainerwrong==50', off_tw == 50, str(off_tw))
    split = off_tw / off_des
    check(f'{tag} trainer split 0.30-0.36', 0.30 <= split <= 0.36, f'{split:.4f}')
    # Driver-level evaluability: the prereg bar's denominator must be > 0
    check(f'{tag} admitted_trainerwrong_cens>0 (bar evaluable)',
          M.get('admitted_trainerwrong_cens', 0) > 0,
          str(M.get('admitted_trainerwrong_cens')))
    # C22 F-V3-2 refusal bar
    rr = M.get('n_drops', 0) / N_EPISODES
    check(f'{tag} F-V3-2 refusal_rate<=10%', rr <= 0.10, f'{rr:.3f}')
    return div, obs_by_v

# ---------------- K3': counterfactual outcome replay ----------------
def k3_replay(variant, th_sacrifice):
    """Deterministic naive count policy through the same 500-episode schedule.
    Returns dict with ER_vup, R_wbs, F_wbs (naive).

    Interpretation (documented; the prereg leaves these implicit):
    - Site-1: INVEST iff C>=2 at a corroboration trigger, target strength 80
      (the N arm's invest level; 80 vs 90 does not change Gate-1 need).
    - Gate-1 victim selection: strength-ordered (weakest first, tiebreak
      smallest v), i.e. the N arm's count-based triage; the evidence gate
      itself (need=ceil(strength/25), kill iff X>=need) is identical.
    - Gate-2: SACRIFICE iff strength<=theta_sacrifice, X==0, non-designated,
      age>=25, cap 2/event (prereg-explicit).
    This is a diagnostic, not law; the verdict-divergence family in
    cell_checks() is the prereg-primary K3 signal."""
    CAP = 32
    # slot state: dict(value=v, strength, c, x, desig) or None
    slots = [None] * CAP
    admitted = {}   # v -> dict(cls, desig, cens_wrong)
    revised_cens = set()
    killed_ri = set()
    def live_vals():
        return [s for s in slots if s is not None]
    def obs_for(v, m):
        """scheduled (kind) observations for value v firing at episode m."""
        out = []
        for ep, kind in scheduled_obs(v, variant):
            if ep == m:
                out.append(kind)
        return out
    def gate1_victim_order():
        cands = [(s['strength'], s['v'], i) for i, s in enumerate(slots)
                 if s is not None and m_cur - s['v'] >= 25 and i not in tried]
        cands.sort()
        return cands
    for m_cur in range(N_EPISODES):
        tried = set()
        # 1. observations for live memories
        new_corrob = set()
        for i, s in enumerate(slots):
            if s is None: continue
            v = s['v']
            for kind in obs_for(v, m_cur):
                if kind == 1:
                    s['c'] += 1; new_corrob.add(i)
                elif kind == 2:
                    s['x'] += 1
                # kind 3 (mark) only at admission; kind 4 probe: no state
        # 2. revision sweep (slot order): >=2 contradictions -> weaken, kill
        for i, s in enumerate(slots):
            if s is None: continue
            if s['x'] >= 2:
                if 30 < s['strength']: s['strength'] = 30
                v = s['v']
                a = admitted[v]
                if a['cls'] == 2 and v <= 389: revised_cens.add(v)
                if a['cls'] == 1: killed_ri.add(v)
                slots[i] = None
        # 3. site-1 naive: new corroboration, zero X -> INVEST iff C>=2 -> 80
        for i in new_corrob:
            s = slots[i]
            if s is not None and s['x'] == 0 and s['c'] >= 2:
                if 80 > s['strength']: s['strength'] = 80
        # 4. scheduled pressure: free 2 slots
        if m_cur in PRESSURE_EPS:
            freed = 0
            guard = 0
            # pressure short-circuit: live but none eligible
            any_live = any(s is not None for s in slots)
            any_elig = any(s is not None and m_cur - s['v'] >= 25 for s in slots)
            if not (any_live and not any_elig):
                while freed < 2 and guard < 100:
                    guard += 1
                    cands = gate1_victim_order()
                    if not cands:
                        break
                    _, _, i = cands[0]
                    s = slots[i]
                    need = (s['strength'] + 24) // 25 if s['strength'] > 0 else 0
                    if s['x'] >= need:
                        # Gate 1 (constitutional effort gate): kill
                        v = s['v']; a = admitted[v]
                        if a['cls'] == 2 and v <= 389 and s['x'] >= 2:
                            revised_cens.add(v)
                        if a['cls'] == 1: killed_ri.add(v)
                        slots[i] = None; freed += 1
                    else:
                        # naive Gate 2: sacrifice iff strength<=theta, x==0,
                        # not designated, age>=25; cap 2 per event
                        if (s['strength'] <= th_sacrifice and s['x'] == 0 and
                                s['desig'] == 0 and m_cur - s['v'] >= 25 and
                                freed < 2):
                            v = s['v']; a = admitted[v]
                            if a['cls'] == 1: killed_ri.add(v)
                            slots[i] = None; freed += 1
                        else:
                            tried.add(i)
        # 5. admission (default strength 0)
        free = next((i for i, s in enumerate(slots) if s is None), None)
        if free is None:
            # admission overflow: free 1 via triage
            tried = set()
            guard = 0
            while free is None and guard < 100:
                guard += 1
                cands = gate1_victim_order()
                if not cands: break
                _, _, i = cands[0]
                s = slots[i]
                need = (s['strength'] + 24) // 25 if s['strength'] > 0 else 0
                if s['x'] >= need:
                    v = s['v']; a = admitted[v]
                    if a['cls'] == 2 and v <= 389 and s['x'] >= 2: revised_cens.add(v)
                    if a['cls'] == 1: killed_ri.add(v)
                    slots[i] = None; free = i
                else:
                    if (s['strength'] <= th_sacrifice and s['x'] == 0 and
                            s['desig'] == 0 and m_cur - s['v'] >= 25):
                        v = s['v']; a = admitted[v]
                        if a['cls'] == 1: killed_ri.add(v)
                        slots[i] = None; free = i
                    else:
                        tried.add(i)
        if free is not None:
            v = m_cur
            slots[free] = {'v': v, 'strength': 0, 'c': 0, 'x': 0,
                           'desig': designated(v)}
            for kind in obs_for(v, m_cur):  # trainer mark at admission
                if kind == 3: pass
            admitted[v] = {'cls': cls(v), 'desig': designated(v)}
        # (drops: no free slot even after overflow pressure -> refused)
    held_ri = sum(1 for s in slots if s is not None and cls(s['v']) == 1)
    offered_ri = sum(1 for m in range(500) if cls(m) == 1)
    admitted_ri = sum(1 for a in admitted.values() if a['cls'] == 1)
    adm_wc = sum(1 for v, a in admitted.items() if a['cls'] == 2 and v <= 389)
    return {
        'ER_vup': held_ri / offered_ri,
        'R_wbs': len(revised_cens) / adm_wc if adm_wc else float('nan'),
        'F_wbs': len(killed_ri) / admitted_ri if admitted_ri else float('nan'),
        'held_ri': held_ri, 'offered_ri': offered_ri,
        'revised_cens': len(revised_cens), 'adm_wc': adm_wc,
        'killed_ri': len(killed_ri), 'admitted_ri': admitted_ri,
    }

# ---------------- cross-cell checks ----------------
def metrics_of(cell):
    M = cell['metric']
    ER = M['held_right_imp'] / M['offered_right_imp']
    Rw = M['revised_wrong_cens'] / M['admitted_wrong_cens']
    # REPAIR 2026-09-20 (DOUBLE_COUNT_NOTE.md): killed_rightimp is double-counted
    # by the driver (record_kill + call-site increments); kill_c1 is incremented
    # exactly once per class-1 kill and is the prereg-faithful F_wbs numerator.
    Fw = M['kill_c1'] / M['admitted_right_imp']
    auc = Fraction(M['auc_p_num'], M['auc_p_den']) if M['auc_p_den'] else Fraction(0)
    return {'ER_vup': ER, 'R_wbs': Rw, 'F_wbs': Fw, 'AUC': float(auc),
            'nneg': M.get('auc_pn_n', 0),
            # R_wbs_trainerwrong per prereg A6/Q8: denominator is admitted
            # designated-wrong, censored m<=389 (evaluable since the repair)
            'R_wbs_trainerwrong':
                M['revised_trainerwrong_cens'] / M['admitted_trainerwrong_cens']
                if M.get('admitted_trainerwrong_cens', 0) else float('nan')}

def cross_checks(fcell, ncell, th_sacrifice, tag):
    fm = metrics_of(fcell); nm = metrics_of(ncell)
    variant = fcell['cell'][1]
    # P3b concentration: top-decile strength share |F-N| <= 15pp
    def topdec(cell):
        ss = sorted([s for _, s, _, _ in cell['endstr']], reverse=True)
        if not ss: return 0.0
        k = max(1, len(ss) // 10)
        return sum(ss[:k]) / sum(ss) if sum(ss) else 0.0
    gap = abs(topdec(fcell) - topdec(ncell))
    check(f'{tag} P3b concentration gap<=15pp', gap <= 0.15, f'gap={gap:.3f}')
    # K1 equivalence
    gaps = {'ER_vup': abs(fm['ER_vup'] - nm['ER_vup']),
            'R_wbs': abs(fm['R_wbs'] - nm['R_wbs']),
            'F_wbs': abs(fm['F_wbs'] - nm['F_wbs']),
            'AUC': abs(fm['AUC'] - nm['AUC'])}
    k1 = gaps['ER_vup'] <= 0.05 and gaps['R_wbs'] <= 0.05 and \
         gaps['F_wbs'] <= 0.05 and gaps['AUC'] <= 0.05
    check(f'{tag} K1 evaluated', True,
          f"gaps ER={gaps['ER_vup']:.4f} R={gaps['R_wbs']:.4f} F={gaps['F_wbs']:.4f} "
          f"AUC={gaps['AUC']:.4f} -> {'RETIRE' if k1 else 'survives'}")
    # K3' replay
    naive = k3_replay(variant, th_sacrifice)
    d = {'ER_vup': abs(fm['ER_vup'] - naive['ER_vup']),
         'R_wbs': abs(fm['R_wbs'] - naive['R_wbs']),
         'F_wbs': abs(fm['F_wbs'] - naive['F_wbs'])}
    k3 = d['ER_vup'] <= 0.05 and d['R_wbs'] <= 0.05 and d['F_wbs'] <= 0.05
    check(f'{tag} K3p replay executed', True,
          f"naive ER={naive['ER_vup']:.4f} R={naive['R_wbs']:.4f} F={naive['F_wbs']:.4f}; "
          f"gaps ER={d['ER_vup']:.4f} R={d['R_wbs']:.4f} F={d['F_wbs']:.4f} -> "
          f"{'RETIRE (restatement)' if k3 else 'survives'}")
    # K4 harm
    k4 = fm['ER_vup'] < nm['ER_vup'] - 0.05 or fm['F_wbs'] > nm['F_wbs'] + 0.02 or \
         fm['R_wbs'] < 1.0
    check(f'{tag} K4 evaluated', True,
          f"ER {fm['ER_vup']:.4f} vs N {nm['ER_vup']:.4f}; "
          f"F {fm['F_wbs']:.4f} vs N {nm['F_wbs']:.4f}; R_wbs(F)={fm['R_wbs']:.4f} -> "
          f"{'RETIRE (harm)' if k4 else 'survives'}")
    # F-V3-1 thermometer
    check(f'{tag} F-V3-1 AUC>=0.65', fm['AUC'] >= 0.65, f"AUC={fm['AUC']:.4f}")
    check(f'{tag} F-V3-1 nneg>=50', fm['nneg'] >= 50, f"nneg={fm['nneg']}")
    # F-V3-3 revision integrity (R_wbs<100% also K4; trainerwrong now evaluable)
    check(f'{tag} F-V3-3 R_wbs==100%', fm['R_wbs'] == 1.0, f"{fm['R_wbs']:.4f}")
    check(f'{tag} F-V3-3 R_wbs_trainerwrong==100%',
          fm.get('R_wbs_trainerwrong') == 1.0, f"{fm.get('R_wbs_trainerwrong')}")
    return fm, nm, naive

# ---------------- main ----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--impl', required=True)
    ap.add_argument('--calib', nargs=4, metavar=('CAL7A','CAL7B','CAL8A','CAL8B'))
    ap.add_argument('--cell', action='append', default=[],
                    help='ARM,VARIANT,FILE_A,FILE_B (paired runs)')
    a = ap.parse_args()
    impl = a.impl
    cal, th_invest, th_sacrifice = static_checks(impl)
    if a.calib:
        check_calibration(impl, a.calib)
    cells = {}
    for spec in a.cell:
        arm, var, fa, fb = spec.split(',')
        var = int(var)
        ca, cb = parse_cell(fa), parse_cell(fb)
        check(f'CELL {arm} v{var} I-1 paired byte-identical',
              hashlib.sha256(open(fa,'rb').read()).hexdigest() ==
              hashlib.sha256(open(fb,'rb').read()).hexdigest())
        check(f'CELL {arm} v{var} cell header', ca['cell'] == (arm, var), str(ca['cell']))
        div, _ = cell_checks(ca, cal, th_invest, th_sacrifice, f'{arm}v{var}')
        for name, (diff, tot) in div.items():
            finding(f'{arm}v{var} verdict-divergence {name}: {diff}/{tot} = '
                    f'{diff/tot if tot else 0:.3f}')
        cells[(arm, var)] = ca
    for var in (0, 1, 2):
        if ('F', var) in cells and ('N', var) in cells:
            cross_checks(cells[('F', var)], cells[('N', var)], th_sacrifice, f'v{var}')
    fails = [(n, d) for n, ok, d in results if not ok]
    print(f'CHECKS: {len(results)-len(fails)}/{len(results)} passed')
    for n, d in fails:
        print(f'  FAIL {n} :: {d}')
    if findings:
        print('FINDINGS:')
        for f in findings:
            print(f'  - {f}')
    print('CHECK_' + ('PASS' if not fails else 'FAIL'))

if __name__ == '__main__':
    main()
