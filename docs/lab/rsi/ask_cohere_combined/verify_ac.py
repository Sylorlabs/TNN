#!/usr/bin/env python3
"""verify_ac.py — mechanical oracle for the ASK-FIRST+COHERENCE combined trial.

Frozen WITH the instrument (not in prereg commit ba139cbf — the prereg's KB
table names this oracle as frozen; that timing is disclosed in VERDICT_AC.md).
Runs ./ac 5x per mode (teacher/learn/pathT/pathA), checks KB1..KB7, prints the
metric table, exits nonzero on any FAIL bar.
"""
import csv, hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "ac")
RUNS = os.path.join(HERE, "runs")
CSV_PATH = os.path.join(HERE, "battery_ac.csv")
sys.path.insert(0, HERE)
import gen_battery_ac as G

MODES = ["teacher", "learn", "pathT", "pathA"]
REPS = 5
fails = []
def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ((" — " + detail) if detail and not cond else ""))
    if not cond:
        fails.append(name + (": " + detail if detail else ""))

def run(mode, rep, cwd=HERE):
    p = subprocess.run([BIN, mode, str(rep)], cwd=cwd, capture_output=True, text=True, timeout=120)
    assert p.returncode == 0, f"{mode} rep {rep} rc={p.returncode}: {p.stderr[:300]}"
    return p.stdout

def sha(s): return hashlib.sha256(s.encode()).hexdigest()

def parse_kv(line):
    d = {}
    for tok in line.split(",")[1:]:
        if "=" in tok:
            k, v = tok.split("=", 1); d[k] = v
    return d

# ---------- load oracle battery ----------
rows = list(csv.DictReader(open(CSV_PATH)))
by_id = {int(r["id"]): r for r in rows}
TRAIN = [r for r in rows if r["set"] == "T"]
TESTF = [r for r in rows if r["set"] == "F"]
TESTN = [r for r in rows if r["set"] == "N"]

# ---------- KB1: battery construction ----------
check("KB1-counts", len(TRAIN) == 16 and len(TESTF) == 24 and len(TESTN) == 16,
      f"T={len(TRAIN)} F={len(TESTF)} N={len(TESTN)}")
cls = {}
for r in rows: cls[r["class"]] = cls.get(r["class"], 0) + 1
exp_cls = {"T1-clean":1,"T2-clean":1,"T3-clean":1,"T4-noop-chan":1,"T5-rectrap":1,
 "T6-rectrap":1,"T7-rectrap":1,"T8-rectrap":1,"T9-ncand3":1,"T10-nrel2":1,
 "T11-nrel4":1,"T12-addrel":1,"T13-m2flip":1,"T14-m2flip":1,"T15-m4silent":1,
 "T16-neither":1,"N-clean":6,"O-clean":6,"ADV-NEW":2,"ADV-OLD":2,"NEITHER":8,
 "NV1-range":2,"NV1-range-flip":1,"NV1-range-neither":1,"NV2-xkey":2,
 "NV2-xkey-flip":1,"NV2-xkey-neither":1,"NV3-3cand":2,"NV3-3cand-flip":1,
 "NV3-3cand-tie":1,"NV4-addrel":3,"NV4-addrel-tie":1}
check("KB1-classes", cls == exp_cls, f"mismatch: { {k:(cls.get(k),v) for k,v in exp_cls.items() if cls.get(k)!=v} }")
pol_ok = all(G.true_verdict(G.by_id[int(r["id"])])[0] == r["gt"] for r in TESTF + TESTN)
check("KB1-policy==gt", pol_ok)
tab = G.rule_table()
top = sorted(tab, reverse=True)
check("KB1-unique-argmax", top[0][1:] == ("CCGEN", 2, "ONINDEC") and top[0][0] == 16 and top[1][0] <= 15,
      f"top={top[:3]}")

# ---------- run all modes 5x ----------
logs = {}
for m in MODES:
    logs[m] = [run(m, r) for r in range(REPS)]
    for r in range(REPS):
        open(os.path.join(RUNS, f"ac_{m}_r{r}.log"), "w").write(logs[m][r])

# ---------- KB2: determinism ----------
for m in MODES:
    shas = {sha(l) for l in logs[m]}
    check(f"KB2-det-{m}", len(shas) == 1, f"{len(shas)} distinct shas")
L = {m: logs[m][0] for m in MODES}  # canonical logs

def lines(tag, log):
    return [l for l in log.splitlines() if l.startswith(tag + ",") or l == tag]

for m in MODES:
    check(f"cfg-{m}", any(l == f"AC_CFG,mode={m}" for l in L[m].splitlines()))
    check(f"done-{m}", "AC_DONE" in L[m].splitlines())
    check(f"batt-recall-{m}", "AC_BATT,id=RECALL,metric=10000" in L[m].splitlines())
    check(f"batt-cost-{m}", "AC_BATT,id=COST,metric=200" in L[m].splitlines())
    check(f"no-gt-in-log-{m}", "gt=" not in L[m] and "ADV-" not in L[m] and "NV1" not in L[m])

# ---------- KB5a: ground truth absent from binary sources ----------
src = open(os.path.join(HERE, "ac.zag")).read() + open(os.path.join(HERE, "ac_data.zag")).read()
leak_toks = ["battery_ac.csv", "ADV-NEW", "ADV-OLD", "NV1", "NV2", "NV3", "NV4",
             "T1-clean", "rectrap", "NEITHER", "xkey", "3cand", "addrel",
             "range-neither", "_zag_raw_syscall"]
found = [t for t in leak_toks if t in src]
check("KB5a-no-gt-in-sources", not found, f"leaked: {found}")

# KB5b: binary behaves identically with the oracle CSV absent
tmpd = "/tmp/ac_nocsv_probe"
os.makedirs(tmpd, exist_ok=True)
nocsv = run("pathT", 0, cwd=tmpd)
check("KB5b-csv-independent", sha(nocsv) == sha(L["pathT"]), "output changed without CSV")

# ---------- KB5c: printed fields match CSV exactly ----------
def fields_of(log):
    d = {}
    for l in lines("AC_ITEMFIELDS", log):
        kv = parse_kv(l); d[int(kv["id"])] = kv
    return d
def fields_match(kv, r):
    if kv["set"] != r["set"] or int(kv["key"]) != int(r["key"]) or int(kv["ncand"]) != int(r["ncand"]) \
       or int(kv["nrel"]) != int(r["nrel"]) or int(kv["ckind"]) != int(r["ckind"]): return False
    if int(kv["c0"]) != int(r["c0"]) or int(kv["c1"]) != int(r["c1"]) or int(kv["c2"]) != int(r["c2"]): return False
    for j in range(5):
        if int(kv[f"r{j}k"]) != int(r[f"r{j}k"]) or int(kv[f"r{j}p1"]) != int(r[f"r{j}p1"]) \
           or int(kv[f"r{j}p2"]) != int(r[f"r{j}p2"]) or int(kv[f"r{j}p3"]) != int(r[f"r{j}p3"]): return False
    return True
f_t = fields_of(L["teacher"])
check("KB5c-train-fields", len(f_t) == 16 and all(fields_match(f_t[int(r["id"])], r) for r in TRAIN))
for m in ("pathT", "pathA"):
    f_m = fields_of(L[m])
    ok = len(f_m) == 40 and all(fields_match(f_m[int(r["id"])], r) for r in TESTF + TESTN)
    check(f"KB5c-test-fields-{m}", ok, f"n={len(f_m)}")

# ---------- KB7: learn selects the true rule, whole table cross-checked ----------
cand = {}
for l in lines("AC_RULECAND", L["learn"]):
    kv = parse_kv(l); cand[(kv["crit"], int(kv["T"]), kv["ask"])] = int(kv["match"])
py_tab = {(c, t, a): m for m, c, t, a in G.rule_table()}
check("KB7-table-crosscheck", cand == py_tab,
      f"diff keys: {set(cand) ^ set(py_tab)}")
rule_l = lines("AC_RULE", L["learn"])
check("KB7-rule-selected", len(rule_l) == 1 and rule_l[0] == "AC_RULE,crit=CCGEN,T=2,ask=ONINDEC,match=16",
      f"got: {rule_l}")
best = max(py_tab.values())
check("KB7-unique-16", best == 16 and sum(1 for v in py_tab.values() if v == 16) == 1
      and py_tab[("CCGEN", 2, "ONINDEC")] == 16)

# teacher log cross-check vs Python teacher
teach = {}
for l in lines("AC_TEACH", L["teacher"]):
    kv = parse_kv(l); teach[int(kv["id"])] = (kv["verdict"], int(kv["vcand"]), int(kv["consult"]))
py_teach = {}
for it in G.items:
    if it["set"] == "T":
        v, c = G.teacher(it)
        vn = "WITHHOLD" if v < 0 else ("NEW" if v == it["ncand"] - 1 else ("OLD" if v == 0 else "MID"))
        py_teach[it["id"]] = (vn, v, c)
check("KB7-teacher-crosscheck", teach == py_teach,
      f"diff: {[(k, teach.get(k), py_teach.get(k)) for k in py_teach if teach.get(k) != py_teach[k]]}")

# ---------- path item cross-checks + metrics ----------
def items_of(log):
    d = {}
    for l in lines("AC_ITEM", log):
        kv = parse_kv(l); d[int(kv["id"])] = kv
    return d

def py_archaic(it):
    # mirrors archaic_vc: shape gate + fixed 2-cand/3-ANCHOR scorer
    ok = it["ncand"] == 2 and it["nrel"] == 3 and it["ckind"] <= 1 and \
         all(r[0] == 0 for r in it["rels"][:3])
    if not ok: return (-1, 0)
    def sc(c, cap):
        v = it["cands"][c]; s = 0
        for r in range(3):
            rk, op, a, _ = it["rels"][r]
            if cap and it["ckind"] == 1 and r == it["cp"][0]: a = it["cp"][1]
            sat = (v == a) if op == 0 else (v < a if op == 1 else v > a)
            s += 1 if sat else -1
        return s
    s0, s1 = sc(0, 0), sc(1, 0)
    top = 0 if s0 >= s1 else 1
    if (s0 if top == 0 else s1) - (s1 if top == 0 else s0) > 2: return (top, 0)
    if it["ckind"] == 0: return (-1, 1)
    q0, q1 = sc(0, 1), sc(1, 1)
    if q0 == q1: return (-1, 1)
    return ((0 if q0 > q1 else 1), 1)

def vname(it, v):
    if v < 0: return "WITHHOLD"
    if it["ncand"] == 3: return ["OLD", "MID", "NEW"][v]
    return "OLD" if v == 0 else "NEW"

metrics = {}
for m, rule in (("pathT", ("CCGEN", 2, "ONINDEC")), ("pathA", None)):
    it = items_of(L[m])
    check(f"items-present-{m}", len(it) == 40, f"n={len(it)}")
    for batt, brows in (("F", TESTF), ("N", TESTN)):
        acc = wi = cons = wh = whn = ops = 0
        for r in brows:
            gi = G.by_id[int(r["id"])]
            kv = it[int(r["id"])]
            if rule: v, c = G.rule_verdict(gi, 1, 2, 1)
            else: v, c = py_archaic(gi)
            vn = vname(gi, v)
            if not (kv["set"] == batt and kv["verdict"] == vn and int(kv["vcand"]) == v
                    and int(kv["consult"]) == c):
                check(f"xcheck-{m}-{batt}-{r['id']}", False,
                      f"log={kv['verdict']},{kv['vcand']},{kv['consult']} py={vn},{v},{c}")
            gt = r["gt"]
            if vn == gt: acc += 1
            if vn in ("NEW", "MID", "OLD") and vn != gt: wi += 1
            cons += c
            if gt == "WITHHOLD":
                whn += 1
                if vn == "WITHHOLD": wh += 1
            ops += int(kv["ops"])
        n = len(brows)
        metrics[(m, batt)] = dict(acc=acc, n=n, wi=wi, cons=cons, wh=wh, whn=whn, ops=ops)

print("\npath x battery: acc | wrong-install | consult | withhold-on-neither | ops")
for m in ("pathT", "pathA"):
    for batt in ("F", "N"):
        d = metrics[(m, batt)]
        print(f"  {m:6s} x TEST-{batt}: {d['acc']:2d}/{d['n']} | {d['wi']:2d} | {d['cons']:2d}/{d['n']} | "
              f"{d['wh']:2d}/{d['whn']} | {d['ops']}")

# preregistered expectations (not bars — reported)
eT = metrics[("pathT", "F")]; eA = metrics[("pathA", "F")]
nT = metrics[("pathT", "N")]; nA = metrics[("pathA", "N")]
check("EXP-pathT-familiar", eT["acc"] == 24 and eT["wi"] == 0, str(eT))
check("EXP-pathA-familiar", eA["acc"] == 24 and eA["wi"] == 0, str(eA))
check("EXP-pathT-novel", nT["acc"] == 16 and nT["wi"] == 0, str(nT))
check("EXP-pathA-novel", nA["acc"] == 4 and nA["wi"] == 0, str(nA))

# ---------- KB3: champion on TEST-NOVEL ----------
champ = None
if nT["acc"] > nA["acc"] and nT["wi"] <= nA["wi"]: champ = "pathT"
elif nA["acc"] > nT["acc"] and nA["wi"] <= nT["wi"]: champ = "pathA"
print("\nKB3-CHAMPION (TEST-NOVEL):", champ if champ else "NO-CHAMPION")
check("KB3-champion-exists", champ is not None)
# ---------- KB4: falsification ----------
if champ == "pathA":
    print("Micah's hypothesis is FALSIFIED — the hardwired architecture generalized "
          "as well or better than the trained behavior.")
    check("KB4-not-falsified", False, "PATH-A champion on TEST-NOVEL")
else:
    print("KB4: not triggered — PATH-A is not the novel-set champion.")
    check("KB4-not-falsified", True)

# ---------- KB6: scope (reported) ----------
print("\nKB6-SCOPE: winner =", champ)
print("  residual boundary: correlated-wrong independent channels (R4C) untested here;")
print("  rkind frontier crossed by the documented generality prior (§7), not by training fit.")

print("\n" + ("ALL BARS PASS" if not fails else f"{len(fails)} FAILURES: {fails}"))
sys.exit(1 if fails else 0)
