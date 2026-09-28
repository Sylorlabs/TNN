#!/usr/bin/env python3
"""RT-3 spec extraction (H-PAM-17/18/19 vs the F5 full mechanism).

Reads ONLY frozen committed files; prints the frozen mechanism spec,
verifies the committed binary is unmodified, and extracts the geometric
facts the three attacks' construction rules need (rescue coordinates,
backtest-false coordinates, NEAR-subset baseline). No attack code here.
"""
import hashlib, re

D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2"
FMD = D + "/f5_fullmech"

def sha16(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]

print("== frozen file SHAs ==")
for p in [FMD + "/f5_full.zag", FMD + "/exemplars.tsv", FMD + "/run1.out",
          FMD + "/bt1.out", D + "/f5_redteam300/fixtures_ledger.txt",
          D + "/../v2/redteam/evidence/ledger_d_withhold.txt"]:
    print("  ", p.split("round2/")[-1] if "round2/" in p else p.split("tnn-lab/")[-1],
          sha16(p))

binsha = sha16(FMD + "/f5_full")
print("== committed binary f5_full sha16:", binsha)
assert binsha == "f633243774a7153a", "binary differs from RT-1's frozen record"

src = open(FMD + "/f5_full.zag").read()
mw = re.findall(r"\|\s*dconf\s*\|\s*<=\s*(\d+)", src)
print("== predicate window consts (dconf/dmeas):",
      re.findall(r"dconf\|\s*<=\s*(\d+)", src)[:2],
      re.findall(r"dmeas\|\s*<=\s*(\d+)", src)[:2])
print("== core window consts:",
      re.findall(r"\|\s*dconf\s*\|\s*<=\s*(\d+)", src)[:4])
print("== crop jitter: (-10,-200),(0,0),(+10,+200):",
      ("conf - 10" in src) and ("meas - 200" in src))
print("== quorum WITHHOLD iff rep>=2:", "rep >= 2" in src)
print("== delay: allowed 0 / confirmed 3 / withheld -1:",
      "delay = -1" in src)
print("== NEAR CORRUPT abort on judg!=truth (falses cannot be NEAR):",
      "CORRUPT trial=" in src)

# ---- exemplars ----
ex = []
for l in open(FMD + "/exemplars.tsv"):
    f = l.rstrip("\n").split("\t")
    if len(f) >= 4 and f[0].strip().isdigit():
        ex.append((int(f[2]), int(f[3])))
cs = [c for c, m in ex]; ms = [m for c, m in ex]
print("== exemplars: n=%d conf %d..%d (span %d) meas %d..%d (span %d)" %
      (len(ex), min(cs), max(cs), max(cs) - min(cs),
       min(ms), max(ms), max(ms) - min(ms)))

# ---- 300-battery composition ----
near_lines = [l for l in open(D + "/f5_redteam300/fixtures_ledger.txt")
              if "SET=NEAR" in l]
far_lines = [l for l in open(D + "/f5_redteam300/fixtures_ledger.txt")
             if "SET=FAR" in l]
print("== 300-battery: %d NEAR + %d FAR lines" % (len(near_lines), len(far_lines)))

def coords_of(ledger_path):
    d = {}
    for l in open(ledger_path):
        f = l.rstrip("\n").split("|")
        if len(f) >= 16 and "DISP=ACCEPT_INSTALL" in f[15]:
            d[f[4]] = (int(f[8]), int(f[10]), f[7], f[12])
    return d

fx300 = coords_of(D + "/f5_redteam300/fixtures_ledger.txt")

# ---- rescue geometry: CONFIRM_INSTALL fixtures in the frozen run ----
rescued = []
withheld = []
for l in open(FMD + "/run1.out"):
    if l.startswith(("SETSUM", "BACKTEST", "DELAYBAR", "HIST", "SERIAL", "SANITY")):
        continue
    f = l.rstrip("\n").split("\t")
    fx, dec = f[1], f[5]
    if dec == "CONFIRM_INSTALL":
        rescued.append(fx)
    elif dec == "WITHHOLD":
        withheld.append(fx)
rc = [fx300[fx][:2] for fx in rescued]
print("== frozen run: %d CONFIRM_INSTALL (rescued), %d WITHHOLD" %
      (len(rescued), len(withheld)))
print("   rescued conf range %d..%d meas range %d..%d" %
      (min(c for c, m in rc), max(c for c, m in rc),
       min(m for c, m in rc), max(m for c, m in rc)))
print("   rescued coords (conf,meas) n=%d:" % len(rc))
print("   ", sorted(rc))

# ---- 8 backtest falses' coordinates ----
btled = D + "/../v2/redteam/evidence/ledger_d_withhold.txt"
fxbt = coords_of(btled)
btfalse = [(fx, fxbt[fx][:2]) for fx in fxbt
           if fxbt[fx][2] != fxbt[fx][3] and fx.split("_")[1] == "TMB-5"]
print("== backtest TMB-5 false accepts: %d" % len(btfalse))
for fx, (c, m) in sorted(btfalse, key=lambda x: x[1]):
    print("   ", fx, c, m)

# ---- NEAR-subset baseline for the A17T mixed battery ----
# deterministic subset: first 240 SET=NEAR lines in file order
sub = near_lines[:240]
subfx = set()
for l in sub:
    subfx.add(l.rstrip("\n").split("|")[4])
w240 = sum(1 for fx in withheld if fx in subfx)
b240 = sum(1 for fx in set(withheld) | set(rescued) if fx in subfx)
print("== A17T mixed-battery baseline: 240-NEAR subset has %d blocked (%d withheld)" %
      (b240, w240))
print("   frozen full-battery delay 60/300=20.0%%; 240-subset withheld fraction %.1f%%" %
      (100.0 * w240 / 240))
print("   predicted mixed delay with 60 adaptive withhold-trues: (%d+60)/300 = %.1f%%" %
      (w240, 100.0 * (w240 + 60) / 300))

# ---- geometric premise checks for the three attacks ----
def blocked(c, m):
    return any(abs(c - ec) <= 150 and abs(m - em) <= 2000 for ec, em in ex)
def rep(c, m):
    n = 0
    for dc, dm in [(-10, -200), (0, 0), (10, 200)]:
        if any(abs(c + dc - ec) <= 130 and abs(m + dm - em) <= 950 for ec, em in ex):
            n += 1
    return n
print("== premise: rescued points are predicate-marginal & rep<2:",
      all(blocked(c, m) and rep(c, m) < 2 for c, m in rc))
print("== premise: annulus exists (blocked & rep<2 points adjacent to boundary):",
      blocked(860, 2632), rep(860, 2632), "|", blocked(849, 2632), rep(849, 2632))
