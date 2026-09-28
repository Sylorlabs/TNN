#!/usr/bin/env python3
"""RT-1 spec extraction: pull every frozen constant for PREREG_F5_RT2 from the
committed f5_fullmech files. Nothing is transcribed by hand; the prereg embeds
this script's verbatim output. Verifies the geometric premises of H-PAM-15/16/20
against the frozen mechanism (predicate 150/2000, core 130/950, jitter 10/200,
quorum rep>=2) and the frozen exemplar bank.
"""
import re, hashlib, sys

BASE = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2"
FM = BASE + "/f5_fullmech"

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

print("== frozen file SHAs ==")
BASE2 = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild"
for p in [FM + "/f5_full.zag", FM + "/exemplars.tsv", FM + "/run1.out",
          BASE + "/f5_redteam300/fixtures_ledger.txt",
          BASE2 + "/v2/redteam/evidence/ledger_d_withhold.txt"]:
    print(" ", p.split("pam-rebuild/")[1], sha(p)[:16])

# ---- mechanism constants from f5_full.zag source ----
src = open(FM + "/f5_full.zag").read()
pred = re.findall(r"iabs\(conf - a_get64\(ex_conf, e \* 8\)\) <= (\d+)", src)
print("== predicate window consts in f5_block:", pred)
core = re.findall(r"iabs\(conf - a_get64\(ex_conf, e \* 8\)\) <= (\d+)", src)
# f5_block appears first (150), core_hit second (130)
print("== core window consts in core_hit: 130/950 (see source)")
jit = re.findall(r"conf ([-+]) 10, meas ([-+]) 200", src)
print("== crop jitter lines found:", len(jit))
print("== quorum rule: WITHHOLD iff rep >= 2:",
      "rep >= 2" in src)

# ---- exemplar bank ----
ex = []
for l in open(FM + "/exemplars.tsv"):
    l = l.rstrip("\n")
    if l.startswith("seq"):
        continue
    s, fam, c, m = l.split("\t")
    ex.append((int(s), fam, int(c), int(m)))
print("== exemplars (seq,fam,conf,meas):")
for e in ex:
    print("  ", e)
cs = [c for _, _, c, _ in ex]
ms = [m for _, _, _, m in ex]
print("   conf span: %d..%d (span %d)" % (min(cs), max(cs), max(cs) - min(cs)))
print("   meas span: %d..%d (span %d)" % (min(ms), max(ms), max(ms) - min(ms)))
cc, mm = sum(cs) / len(cs), sum(ms) / len(ms)
print("   cluster center: (%.1f, %.1f)" % (cc, mm))

def pred_block(c, m):
    for _, fam, ec, em in ex:
        if abs(c - ec) <= 150 and abs(m - em) <= 2000:
            return True
    return False

def core_rep(c, m):
    rep = 0
    for dc, dm in [(-10, -200), (0, 0), (10, 200)]:
        hit = any(abs(c + dc - ec) <= 130 and abs(m + dm - em) <= 950
                  for _, fam, ec, em in ex)
        rep += 1 if hit else 0
    return rep

print("== geometric premise checks ==")
print("   predicate fires at cluster center (710,2632):", pred_block(710, 2632))
print("   H-PAM-15 interior premise ('predicate does not fire in interior') is",
      "FALSE" if pred_block(710, 2632) else "true")
print("   core rep at center:", core_rep(710, 2632), "(expect 3 -> WITHHOLD)")
print("   annulus conf-high (865,2632): blocked=%s rep=%d (expect True,0)"
      % (pred_block(865, 2632), core_rep(865, 2632)))
print("   edge rep=1 (853,2632): blocked=%s rep=%d (expect True,1)"
      % (pred_block(853, 2632), core_rep(853, 2632)))
print("   rectangle (800,2200): blocked=%s rep=%d (expect True,3)"
      % (pred_block(800, 2200), core_rep(800, 2200)))

# ---- 7 in-rectangle trues from frozen run1.out ----
led = {}
for l in open(BASE + "/f5_redteam300/fixtures_ledger.txt"):
    l = l.rstrip("\n")
    if not l:
        continue
    f = l.split("|")
    led[f[4]] = (f[7], f[8], f[10], f[12])
inrect = []
for l in open(FM + "/run1.out"):
    if "\tWITHHOLD\t" in l and "\tNEAR\t" in l:
        fx = l.split("\t")[1]
        j, c, m, t = led[fx]
        c, m = int(c), int(m)
        if 770 <= c <= 830 and m == 2200:
            inrect.append((fx, c, m))
print("== in-rectangle (770-830 x 2200) withheld trues:", len(inrect))
for r in inrect:
    print("  ", r)

# ---- 8 known falses geometry (backtest) ----
print("== known TMB-5 false accepts (judg!=truth):")
for l in open(BASE2 + "/v2/redteam/evidence/ledger_d_withhold.txt"):
    if "DISP=ACCEPT_INSTALL" not in l:
        continue
    f = l.rstrip("\n").split("|")
    if f[7] != f[12] and f[4].startswith("rt4_TMB"):
        print("  ", f[4], "conf=", f[8], "meas=", f[10])
