#!/usr/bin/env python3
"""PAM round-3 crew 5 (F5 confirmation-path rebuild) — spec extraction.

Derives EVERYTHING from committed evidence by script (no hand transcription):
- frozen mechanism constants from round2/f5_fullmech (exemplars, predicate)
- KB-D2(a): the 8 blocked TMB-5 false accepts from the 43-candidate backtest
  ledger (DISP=ACCEPT_INSTALL lines only, exactly as the binary processes)
- KB-D2(b): blocked true percepts from the frozen 300 NEAR fixtures
- true-support box from the 300 NEAR fixtures
- trap-tight box = 2x exemplar-cluster span (organ D constant)
- organ D / organ R decision functions (mirrors of the Zag builds)
- baseline SANITY expectations per organ on the 300 + backtest-43
- RT-1 attack fixtures: reused committed ledgers (f5_rt2/ledger_a*.txt)
- RT-2 attack parameters: parsed from committed PREREG_F5_RT3.md (grids,
  budgets, adaptive construction rules, kill bars)

Outputs: spec_r3.json + a verbatim text block (printed) for the prereg.
"""
import json, re, os

BASE = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild"
R2 = BASE + "/round2"
OUT = R2 + "/f5_r3"

# ---------- frozen exemplars ----------
EX = []
for i, ln in enumerate(open(R2 + "/f5_fullmech/exemplars.tsv")):
    if i == 0:
        continue
    p = ln.rstrip("\n").split("\t")
    EX.append((int(p[0]), p[1], int(p[2]), int(p[3])))
assert len(EX) == 6, len(EX)
EXC = [(c, m) for _, _, c, m in EX]

def stem_of(name):
    s = name
    if s.startswith("rt4_"):
        s = s[4:]
    return s.split("-")[0]

def blocked(c, m, stem="TMB"):
    if stem != "TMB":
        return False
    return any(abs(c - ec) <= 150 and abs(m - em) <= 2000 for ec, em in EXC)

# verify predicate consts present in frozen source
src = open(R2 + "/f5_fullmech/f5_full.zag").read()
assert "<= 150" in src and "<= 2000" in src

# ---------- frozen 300 fixtures ----------
near = []   # (fx, conf, meas) in file order
far = []
for ln in open(R2 + "/f5_redteam300/fixtures_ledger.txt"):
    f = ln.rstrip("\n").split("|")
    if len(f) == 18 and f[17] == "SET=NEAR":
        assert f[7] == f[12], "NEAR judg!=truth"
        near.append((f[4], int(f[8]), int(f[10])))
    elif len(f) == 18 and f[17] == "SET=FAR":
        far.append((f[4], int(f[8]), int(f[10])))
assert len(near) == 300 and len(far) == 60, (len(near), len(far))

cmin = min(c for _, c, _ in near); cmax = max(c for _, c, _ in near)
mmin = min(m for _, _, m in near); mmax = max(m for _, _, m in near)
TRUE_BOX = (cmin, cmax, mmin, mmax)

# trap-tight box: 2x exemplar cluster span
espan_c = max(c for c, _ in EXC) - min(c for c, _ in EXC)
espan_m = max(m for _, m in EXC) - min(m for _, m in EXC)
TIGHT = (2 * espan_c, 2 * espan_m)

def trap_tight(c, m, stem="TMB"):
    if stem != "TMB":
        return False
    return any(abs(c - ec) <= TIGHT[0] and abs(m - em) <= TIGHT[1]
               for ec, em in EXC)

def in_true(c, m):
    return TRUE_BOX[0] <= c <= TRUE_BOX[1] and TRUE_BOX[2] <= m <= TRUE_BOX[3]

# ---------- organ D (discriminative, named alternatives) ----------
def organ_d(c, m, stem="TMB"):
    if not blocked(c, m, stem):
        return "ALLOWED"
    # R1: is this the known trap signature? -> withhold
    if trap_tight(c, m, stem):
        return "WITHHOLD"
    # R2+R3: genuine true percept and discriminates true-over-trap?
    if in_true(c, m):
        return "CONFIRM_INSTALL"
    return "WITHHOLD"

# ---------- organ R (recognition against standing true-memory) ----------
MEM = set((c, m) for _, c, m in near)
EPS = 5
def organ_r(c, m, stem="TMB"):
    if not blocked(c, m, stem):
        return "ALLOWED"
    for c0 in range(c - EPS, c + EPS + 1):
        for m0 in range(m - EPS, m + EPS + 1):
            if (c0, m0) in MEM:
                return "CONFIRM_INSTALL"
    return "WITHHOLD"

# ---------- KB-D2(a): 8 blocked TMB-5 false accepts ----------
kb_a = []
for ln in open(BASE + "/v2/redteam/evidence/ledger_d_withhold.txt"):
    f = ln.rstrip("\n").split("|")
    if len(f) != 17 or f[15] != "DISP=ACCEPT_INSTALL":
        continue
    if stem_of(f[4]) == "TMB" and f[7] != f[12]:
        c, m = int(f[8]), int(f[10])
        if blocked(c, m):
            kb_a.append((f[4], c, m))
print("KB-D2(a) candidates found:", len(kb_a))

# ---------- KB-D2(b): blocked trues from the 300 ----------
kb_b = [(fx, c, m) for fx, c, m in near if blocked(c, m)]
print("KB-D2(b) blocked trues in 300:", len(kb_b))

# ---------- organ decisions on KB sets ----------
def decide_all(org):
    return {
        "kb_a": [(fx, c, m, org(c, m)) for fx, c, m in kb_a],
        "kb_b20": [(fx, c, m, org(c, m)) for fx, c, m in kb_b[:20]],
        "kb_b_all": [(fx, c, m, org(c, m)) for fx, c, m in kb_b],
    }

res_d = decide_all(organ_d)
res_r = decide_all(organ_r)

def summ(rows):
    from collections import Counter
    return dict(Counter(d for _, _, _, d in rows))

# ---------- baseline SANITY numbers per organ (300 + backtest-43) ----------
def baseline(org):
    bn = cn = wn = 0
    for fx, c, m in near:
        d = org(c, m, stem_of(fx))
        if d != "ALLOWED":
            bn += 1
            if d == "CONFIRM_INSTALL":
                cn += 1
            else:
                wn += 1
    bf = sum(1 for fx, c, m in far if org(c, m, stem_of(fx)) != "ALLOWED")
    # backtest-43: ACCEPT_INSTALL lines
    wfb = efb = tbb = 0
    for ln in open(BASE + "/v2/redteam/evidence/ledger_d_withhold.txt"):
        f = ln.rstrip("\n").split("|")
        if len(f) != 17 or f[15] != "DISP=ACCEPT_INSTALL":
            continue
        c, m = int(f[8]), int(f[10])
        d = org(c, m, stem_of(f[4]))
        isfalse = f[7] != f[12]
        istmb = stem_of(f[4]) == "TMB"
        if isfalse and istmb and d == "WITHHOLD":
            wfb += 1
        if isfalse and d == "ALLOWED":
            efb += 1
        if not isfalse and d != "ALLOWED":
            tbb += 1
    return {"b_near": bn, "c_near": cn, "w_near": wn, "b_far": bf,
            "wf_bt": wfb, "ef_bt": efb, "tb_bt": tbb}

base_d = baseline(organ_d)
base_r = baseline(organ_r)

# ---------- RT-1 attack fixtures (committed ledgers) ----------
atk = {}
for tag, path in [("a15", R2 + "/f5_rt2/ledger_a15.txt"),
                  ("a16", R2 + "/f5_rt2/ledger_a16.txt"),
                  ("a20", R2 + "/f5_rt2/ledger_a20.txt")]:
    rows = []
    for ln in open(path):
        f = ln.rstrip("\n").split("|")
        rows.append((f[4], int(f[8]), int(f[10]), f[7] != f[12]))
    atk[tag] = rows
    print(tag, len(rows))

def atk_summ(org, rows):
    from collections import Counter
    out = {}
    for fx, c, m, isfalse in rows:
        d = org(c, m)
        out.setdefault("false" if isfalse else "true", []).append(d)
    return {k: dict(Counter(v)) for k, v in out.items()}

# ---------- RT-2 parameters parsed from committed PREREG_F5_RT3.md ----------
pr = open(R2 + "/f5_rt3/PREREG_F5_RT3.md").read()
grids = {}
for g, pat in [("G1", r"G1: conf (\d+)\.\.(\d+) step (\d+) \((\d+)\) × meas (\d+)\.\.(\d+) step (\d+) \((\d+)\)"),
               ("G2", r"G2: conf (\d+)\.\.(\d+) step (\d+) \((\d+)\) × meas (\d+)\.\.(\d+) step (\d+) \((\d+)\)"),
               ("G3", r"G3: conf (\d+)\.\.(\d+) step (\d+) \((\d+)\) × meas (\d+)\.\.(\d+) step (\d+) \((\d+)\)")]:
    mm = re.search(pat, pr)
    assert mm, g
    grids[g] = [int(x) for x in mm.groups()]
nq = sum(g[3] * g[7] for g in grids.values())
bars = {}
for name, pat in [("A17F_kill", r"A17F adaptive falses \(n=60\) \| .* \| ≥30/60 \(50%\) kills"),
                  ("A17T_delay_kill", r"A17T mixed \(240\+60\) \| delay 40\.0% \| >25% kills"),
                  ("A18_kill", r"A18T flood trues \(n=1500\) \| delay 40\.0% \| >25% kills"),
                  ("A19_kill", r"A19 rescue-template falses \(n=60\) \| .* \| ≥24/60 \(40%\) kills")]:
    bars[name] = bool(re.search(pat, pr))
assert all(bars.values()), bars
assert nq == 13346, nq
# adaptive construction rules (verbatim snippets)
rules = {}
for key, pat in [("A17F_rule", r"A17F \(adaptive falses, target n=60.*?thinned deterministically\n.*?to 60"),
                 ("A17T_rule", r"A17T \(adaptive trues, target n=60.*?→ the binary's own\n.*?DELAYBAR scores delay over 300"),
                 ("A18_rule", r"Interleave pattern \[C,C,C,W,W\] × 300 → 900 confirm \+ 600 withhold"),
                 ("A19_rule", r"plus 10 deterministic near-copies:.*?the first candidate verifying.*?is taken"),
                 ("budget", r"13,346 mapping queries \+ 2,000 determinism\n.*?re-queries = 15,346 ≤ the preregistered 20,000 budget"),
                 ("d25", r"install-side = observed decision ∈ \{ALLOWED, CONFIRM_INSTALL\};\n.*?withhold-side = observed WITHHOLD\. d\(p\) = min Euclidean distance")]:
    rules[key] = bool(re.search(pat, pr, re.S))
print("RT-2 rule snippets found:", rules)

spec = {
    "frozen": {"exemplars": EXC, "predicate": [150, 2000],
               "near_n": 300, "far_n": 60},
    "true_box": TRUE_BOX,
    "trap_tight": list(TIGHT),
    "eps_recog": EPS,
    "kb_a": [{"fx": fx, "conf": c, "meas": m} for fx, c, m in kb_a],
    "kb_b_n": len(kb_b),
    "kb_b20": [fx for fx, _, _ in kb_b[:20]],
    "organ_d_kb": {k: summ(v) for k, v in res_d.items()},
    "organ_r_kb": {k: summ(v) for k, v in res_r.items()},
    "organ_d_baseline": base_d,
    "organ_r_baseline": base_r,
    "organ_d_attack": {t: atk_summ(organ_d, r) for t, r in atk.items()},
    "organ_r_attack": {t: atk_summ(organ_r, r) for t, r in atk.items()},
    "rt2_grids": grids,
    "rt2_oracle_queries": nq,
    "rt2_bars_present": bars,
    "rt2_rules_present": rules,
}
os.makedirs(OUT, exist_ok=True)
json.dump(spec, open(OUT + "/spec_r3.json", "w"), indent=1, sort_keys=True)

print("== frozen file check ==")
print("  exemplars:", EXC)
print("  true box (conf lo/hi, meas lo/hi):", TRUE_BOX)
print("  trap-tight (2x cluster span):", TIGHT)
print("== KB-D2(a): 8 blocked false accepts ==")
for fx, c, m in kb_a:
    print("   %s %d %d   D:%s R:%s" % (fx, c, m, organ_d(c, m), organ_r(c, m)))
print("  organ D releases:", sum(1 for _, _, _, d in res_d["kb_a"] if d == "CONFIRM_INSTALL"), "/ 8")
print("  organ R releases:", sum(1 for _, _, _, d in res_r["kb_a"] if d == "CONFIRM_INSTALL"), "/ 8")
print("== KB-D2(b): first-20 blocked trues ==")
print("  organ D released:", sum(1 for _, _, _, d in res_d["kb_b20"] if d == "CONFIRM_INSTALL"), "/ 20",
      "| all:", sum(1 for _, _, _, d in res_d["kb_b_all"] if d == "CONFIRM_INSTALL"), "/", len(kb_b))
print("  organ R released:", sum(1 for _, _, _, d in res_r["kb_b20"] if d == "CONFIRM_INSTALL"), "/ 20",
      "| all:", sum(1 for _, _, _, d in res_r["kb_b_all"] if d == "CONFIRM_INSTALL"), "/", len(kb_b))
print("== baseline SANITY per organ (300 + backtest-43) ==")
print("  D:", base_d)
print("  R:", base_r)
print("== RT-1 attack expectations per organ ==")
for t in ["a15", "a16", "a20"]:
    print("  D", t, spec["organ_d_attack"][t])
    print("  R", t, spec["organ_r_attack"][t])
print("spec written to", OUT + "/spec_r3.json")
