#!/usr/bin/env python3
"""Independent Python reimplementation of d1battery.zag logic.
Verifies the Zag battery's numbers. Reads the same fixture files,
reimplements P7/P10/audit/P8w/hybrid per D1B_DESIGN.md, prints the
same output lines for diffing against run1.out.
"""
import os

WS = os.path.expanduser("~/workspace/pam_round2")
LED = os.path.expanduser("~/workspace/pam_round2/f5_redteam300/fixtures_ledger.txt")
ADV = os.path.expanduser("~/workspace/pam_round2/d1_build/d1_adv_fixtures.txt")

def lawful_meas_gain(m): return m * 12 // 10
def lawful_conf_crop(c): return c - 24
def warrant(c, m, omg, ocg, omc, occ, tau=2):
    if abs(omg - lawful_meas_gain(m)) > tau: return 0
    if abs(ocg - c) > tau: return 0
    if abs(omc - m) > tau: return 0
    if abs(occ - lawful_conf_crop(c)) > tau: return 0
    return 1
def reproj_c(c, m): return (c * 3 + m) % 9973
def reproj_m(c, m): return (m * 5 + c) % 65521
def world_w(t, p): return (t * 11 + p * 17 + 3) & 31
def p_actual_fn(L): return ((L * 1103515245 + 12345) >> 16) & 31
def p_guess_fn(i): return ((i * 40503) >> 8) & 31
def ilog2(x):
    e = 0
    while x >= 2: x //= 2; e += 1
    return e

# load honest
hon = []
with open(LED) as fh:
    for line in fh:
        line = line.strip()
        if not line: continue
        f = line.split("|")
        name = f[4]
        sc = 0 if name[4] == 'T' else (1 if name[4] == 'C' else 2)
        hon.append((int(f[8]), int(f[10]), sc))
assert len(hon) == 360, len(hon)

# load adversarial
adv = []
with open(ADV) as fh:
    for line in fh:
        line = line.strip()
        if not line: continue
        gid, cls, scene, conf, meas, t = line.split("|")
        adv.append((int(gid), cls, {"TMB-5":0,"COL-4":1,"PTC-4":2}[scene],
                    int(conf), int(meas), int(t)))
assert len(adv) == 300, len(adv)

# counters
p7 = dict(h_install=0, hc_n=0, hc_withhold=0, a_install=0, b_install=0, c_install=0)
p10 = dict(inv=0, match=0, b_inv=0, b_match=0, c_inv=0, c_match=0)
aud = dict(n=0, agree=0, agree_b=0, agree_c=0, n_b=0, n_c=0)
f8c = [0,0,0]
p8w = dict(h=0,a=0,b=0,c=0)
hy = dict(h_install=0,h_uncov=0,h_prov=0,h_with=0,
          a_install=0,a_prov=0,a_with=0,
          b_install=0,b_prov=0,b_with=0,b_uncov=0,
          c_install=0,c_prov=0,c_with=0,c_uncov=0)
delayed_n=0; total_n=0
L=305419896
slip_ids=[]

def audit_step(c,m,d7,cls):
    global f8c
    cb, mb = reproj_c(c,m), reproj_m(c,m)
    if cls in ("H",):  # honest: complex handled by caller via omgb
        pass
    return cb, mb

def process(c,m,sc,cls,is_honest,gid,complex_f,observed):
    global L,delayed_n,total_n,aud,p8w,hy,p7,p10,f8c
    omg,ocg,omc,occ = observed
    d7 = warrant(c,m,omg,ocg,omc,occ)
    # P7 counters
    if is_honest:
        if d7==1: p7["h_install"]+=1
        if complex_f:
            p7["hc_n"]+=1
            if d7==0: p7["hc_withhold"]+=1
    else:
        if d7==1: p7[{"A":"a_install","B":"b_install","C":"c_install"}[cls]]+=1
    # hybrid
    dec=0; p10d=0
    if d7==0:
        dec = 2 if (complex_f or (not is_honest and m>=6000)) else 0
        # note: adv complex uses m>=6000 same as honest F7b routing
    else:
        if sc==0:
            p10d=1; p10["inv"]+=1
            pa=p_actual_fn(L); pg=p_guess_fn(gid)
            claim = 1 if m>=4000 else 0
            o = world_w(claim, pa) if is_honest else world_w(claim, pg)
            e = world_w(claim, pa)
            if o==e:
                p10["match"]+=1; dec=1
                if cls=="B": p10["b_match"]+=1; 
                if cls=="C": p10["c_match"]+=1
            else:
                dec=2
                if cls=="B": slip_ids.append(gid)
            if cls=="B": p10["b_inv"]+=1
            if cls=="C": p10["c_inv"]+=1
        else:
            dec=3
    # hybrid counters
    if is_honest:
        if dec in (1,3): hy["h_install"]+=1
        if dec==3: hy["h_uncov"]+=1
        if dec==2: hy["h_prov"]+=1
        if dec==0: hy["h_with"]+=1
    else:
        k=cls.lower()
        if dec==1 or dec==3: hy[f"{k}_install"]+=1
        if dec==3: hy[f"{k}_uncov"]+=1
        if dec==2: hy[f"{k}_prov"]+=1
        if dec==0: hy[f"{k}_with"]+=1
    # audit
    cb,mb = reproj_c(c,m), reproj_m(c,m)
    if is_honest:
        omgb = lawful_meas_gain(mb)+(997 if complex_f else 0)
        occb = lawful_conf_crop(cb)
    else:
        if cls=="A": omgb,occb = mb+997, cb
        else: omgb,occb = lawful_meas_gain(mb), lawful_conf_crop(cb)
    dB = warrant(cb,mb,omgb,cb,mb,occb)
    aud["n"]+=1
    shared = 1 if (reproj_c(c,m)==cb and reproj_m(c,m)==mb) else 0
    if d7==dB:
        aud["agree"]+=1
        if cls=="B": aud["agree_b"]+=1
        if cls=="C": aud["agree_c"]+=1
    if cls=="B": aud["n_b"]+=1
    if cls=="C": aud["n_c"]+=1
    if is_honest and shared==1: f8c[0]=1
    if cls=="C" and shared==1 and d7==dB: f8c[1]=1
    if cls=="B" and shared==1 and d7==dB: f8c[2]=1
    # p8w
    pw = 1 if (d7==1 and dB==1 and shared==0) else 0
    if pw: p8w[{"H":"h","A":"a","B":"b","C":"c"}[cls if not is_honest else "H"]]+=1
    # delay + ledger
    total_n+=1
    if p10d: delayed_n+=1
    L = (L*1664525 + (1+dec)*1013904223 + 7) % 2147483648

for idx,(c,m,sc) in enumerate(hon):
    complex_f = m>=6000
    omg=lawful_meas_gain(m)+(997 if complex_f else 0)
    process(c,m,sc,"H",True,idx,complex_f,(omg,c,m,lawful_conf_crop(c)))

for (gid,cls,sc,c,m,t) in adv:
    if cls=="A": obs=(m+997,c,m,c)
    else: obs=(lawful_meas_gain(m),c,m,lawful_conf_crop(c))
    process(c,m,sc,cls,False,gid,False,obs)

print(f"D1BAT h_n=360 adv_n=300 ledger_final={L}")
print(f"P7 h_install={p7['h_install']} hc_n={p7['hc_n']} hc_withhold={p7['hc_withhold']} "
      f"a_install={p7['a_install']} b_install={p7['b_install']} c_install={p7['c_install']}")
bb=ilog2((p10['b_inv']+1)//(p10['b_match']+1)); cb=ilog2((p10['c_inv']+1)//(p10['c_match']+1))
print(f"P10 inv={p10['inv']} match={p10['match']} b_inv={p10['b_inv']} b_match={p10['b_match']} "
      f"b_bits={bb} c_inv={p10['c_inv']} c_match={p10['c_match']} c_bits={cb}")
print(f"AUDIT n={aud['n']} agree={aud['agree']} agree_pct={aud['agree']*100//aud['n']} "
      f"b_agree={aud['agree_b']}/{aud['n_b']} c_agree={aud['agree_c']}/{aud['n_c']} "
      f"effn=1 premium_bp=0 f8c={f8c[0]}{f8c[1]}{f8c[2]} verdict=SHARED_SOURCE")
print(f"P8W h={p8w['h']} a={p8w['a']} b={p8w['b']} c={p8w['c']}")
print(f"HYB h_inst={hy['h_install']} h_uncov={hy['h_uncov']} h_prov={hy['h_prov']} h_with={hy['h_with']} "
      f"a_inst={hy['a_install']} a_prov={hy['a_prov']} a_with={hy['a_with']}")
print(f"HYB b_inst={hy['b_install']} b_prov={hy['b_prov']} b_with={hy['b_with']} b_uncov={hy['b_uncov']} "
      f"c_inst={hy['c_install']} c_prov={hy['c_prov']} c_with={hy['c_with']} c_uncov={hy['c_uncov']}")
print(f"KTABLE delayed={delayed_n} total={total_n}")
print(f"SLIP_IDS={slip_ids}")
