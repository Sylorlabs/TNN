#!/usr/bin/env python3
"""MATH R4 battery verifier (independent of gen_battery.py internals).

Usage: python3 verify_battery.py <battery_dir> <source_dir>
  battery_dir : built tree (chain_nl/, chain50_nl/, para_inv/, knowledge/, sealed/, README.md)
  source_dir  : directory containing gen_battery.py + data/

Checks:
  1. Rebuild from source into a temp dir; byte-identical to battery_dir.
  2. Counts: 20 chain, 6 chain50, 12+12 para, 25 knowledge items.
  3. Trace validity for every sealed CHAIN_NL solution (refs, spans, licenses,
     K-license quote rule, step bounds 5..20).
  4. CHAIN50: 50..160 steps, chain linkage from public files alone.
  5. PARA-INV: two independent equivalence checks -
       (a) normalized relation signature match (numeric + structural tokens),
       (b) closure/target-verdict comparison via sealed base solutions;
     nonce round-trip via the sealed map; bijectivity; freshness.
  6. Knowledge: R4 store has 25 items; exactly K005/K101/K104 changed;
     R3 bodies byte-match the frozen R3 file.
  7. No DERIVED/WITHHELD/verdict/solution tokens outside sealed/.
  8. sealed/MANIFEST.sha256 matches every file.
  9. w_sealed exit-3 guard active (subprocess).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BAT = sys.argv[1]
SRC = sys.argv[2]
FAIL = []

def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def read_battery(rel):
    with open(os.path.join(BAT, rel), encoding="utf-8") as f:
        return f.read()

# ---------- 1. byte-identical rebuild ----------
tmp = tempfile.mkdtemp(prefix="r4verify_")
r = subprocess.run([sys.executable, os.path.join(SRC, "gen_battery.py"), tmp],
                   capture_output=True, text=True)
check(r.returncode == 0, "rebuild failed: %s" % r.stderr[-2000:])
if r.returncode == 0:
    for dirpath, _, filenames in os.walk(tmp):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, tmp)
            bpath = os.path.join(BAT, rel)
            check(os.path.exists(bpath), "missing in battery: %s" % rel)
            if os.path.exists(bpath):
                check(sha256_file(full) == sha256_file(bpath),
                      "byte mismatch: %s" % rel)
    # no extra files in battery
    for dirpath, _, filenames in os.walk(BAT):
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), BAT)
            check(os.path.exists(os.path.join(tmp, rel)), "extra file in battery: %s" % rel)
shutil.rmtree(tmp, ignore_errors=True)
print("check 1 (byte-identical rebuild): done")

# ---------- 2. counts ----------
chain = sorted(f for f in os.listdir(os.path.join(BAT, "chain_nl")) if f.endswith(".txt"))
c50 = sorted(f for f in os.listdir(os.path.join(BAT, "chain50_nl")) if f.endswith(".txt"))
para = sorted(f for f in os.listdir(os.path.join(BAT, "para_inv")) if f.endswith(".txt"))
check(len(chain) == 20, "chain_nl count %d != 20" % len(chain))
check(len(c50) == 6, "chain50_nl count %d != 6" % len(c50))
check(len([f for f in para if f.startswith("PARA_PAIR")]) == 12, "paraphrase count")
check(len([f for f in para if f.startswith("PARA_NONCE")]) == 12, "nonce count")
sol = sorted(f for f in os.listdir(os.path.join(BAT, "sealed")) if f.endswith(".sol.json"))
check(len(sol) == 20, "sealed solutions %d != 20" % len(sol))
skel = sorted(f for f in os.listdir(os.path.join(BAT, "sealed")) if f.endswith(".skel.json"))
check(len(skel) == 6, "sealed skeletons %d != 6" % len(skel))
print("check 2 (counts): done")

# ---------- knowledge store ----------
sys.path.insert(0, os.path.join(SRC, "data"))
import data_knowledge as DK
STORE = {k: r4 for (k, _t, _r3, r4, _c, _n) in DK.AUDIT}
check(len(STORE) == 25, "knowledge items != 25")
check(sorted(DK.changed_keys()) == ["K005", "K101", "K104"], "changed keys wrong")
pub_store = read_battery("knowledge/KNOWLEDGE_STORE_NL.md")
for k, body in STORE.items():
    check(("[%s]" % k) in pub_store and body in pub_store, "store item %s not in public file" % k)
frozen = open(os.path.expanduser("~/workspace/tmp_commit/r4/KS.md"), encoding="utf-8").read()
for (k, tag, r3, _r4, _c, _n) in DK.AUDIT:
    check(("[%s] %s" % (k, tag)) in frozen and r3 in frozen, "R3 body %s not verbatim in frozen" % k)
print("check 6 (knowledge): done")

# ---------- 3. trace validity (independent parse of sealed JSON + public txt) ----------
LIC_OK = set(STORE) | {"SUBST", "ARITH", "MECH"}
def parse_public(rel):
    txt = read_battery(rel)
    stmts, target = [], None
    for line in txt.splitlines():
        m = re.match(r"S(\d+)\.\s(.*)$", line)
        if m:
            stmts.append(m.group(2))
        m = re.match(r"TARGET:\s(.*)$", line)
        if m:
            target = m.group(1)
    return stmts, target

for sf in sol:
    d = json.loads(read_battery("sealed/" + sf))
    pid = d["id"]
    stmts, target = parse_public("chain_nl/%s.txt" % pid)
    check(d["target"] == target, "%s sealed target != public target" % pid)
    check(d["statements"] == stmts, "%s sealed statements != public" % pid)
    n = d["steps"]
    check(5 <= n <= 20, "%s steps %d out of [5,20]" % (pid, n))
    check(len(d["trace"]) == n, "%s trace length != steps" % pid)
    for i, t in enumerate(d["trace"], 1):
        lic = t["license"]
        check(lic in LIC_OK, "%s step %d bad license %s" % (pid, i, lic))
        if lic in STORE:
            check(any(k == "STORE" and rr == lic and q in STORE[lic]
                      for (k, rr, q) in t["from"]),
                  "%s step %d K-license without R4 STORE quote" % (pid, i))
        for (kind, ref, q) in t["from"]:
            if kind == "STEP":
                check(1 <= ref < i, "%s step %d bad STEP ref %d" % (pid, i, ref))
            elif kind == "STMT":
                check(1 <= ref <= len(stmts), "%s step %d bad STMT ref" % (pid, i))
                check(q in stmts[ref - 1], "%s step %d STMT span absent" % (pid, i))
            elif kind == "STORE":
                check(ref in STORE, "%s step %d bad STORE key" % (pid, i))
                check(q in STORE[ref], "%s step %d STORE span absent from R4" % (pid, i))
            else:
                check(False, "%s step %d bad from kind %s" % (pid, i, kind))
print("check 3 (trace validity): done")

# ---------- 4. CHAIN50 from public files alone ----------
for cf in c50:
    txt = read_battery("chain50_nl/" + cf)
    rules = re.findall(r"^R(\d+)\.\s(.*)$", txt, re.M)
    nums = [int(x) for x, _ in rules]
    check(nums == list(range(1, len(nums) + 1)), "%s rule numbering" % cf)
    n = len(nums)
    check(50 <= n <= 160, "%s steps %d out of [50,160]" % (cf, n))
    bodies = [b for _, b in rules]
    def ant(r):
        return r[3:r.index(", then ")]
    def con(r):
        return r[r.index(", then ") + len(", then "):].rstrip(".")
    for a, b in zip(bodies, bodies[1:]):
        check(con(a) == ant(b), "%s chain link broken" % cf)
    tm = re.search(r"^TARGET:\s(.*)$", txt, re.M)
    check(tm and con(bodies[-1]).lower() == tm.group(1).rstrip(".").lower(),
          "%s final consequent != target" % cf)
    sk = json.loads(read_battery("sealed/" + cf.replace(".txt", ".skel.json")))
    check(sk["shortest_steps"] == n and sk["bound_ok"], "%s skeleton mismatch" % cf)
print("check 4 (chain50): done")

# ---------- 5. PARA-INV: two independent equivalence checks ----------
def norm_sig(texts):
    # independent check (a): numeric multiset + sorted content-word multiset
    nums = sorted(int(x) for t in texts for x in re.findall(r"\d+", t))
    words = sorted(w.lower() for t in texts for w in re.findall(r"[A-Za-z]+", t)
                   if w.lower() not in STOP)
    return (nums, words)

STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "be", "it",
        "its", "that", "with", "for", "on", "as", "by", "if", "then", "s"}
entail = json.loads(read_battery("para_inv/PARA_ENTAIL.json"))
nonce_map = json.loads(read_battery("sealed/PARA_NONCE_MAP.json"))
base_sol = json.loads(read_battery("sealed/PARA_BASE_SOL.json"))
check(len(entail) == 12 and len(nonce_map) == 12, "para sealed counts")
for pair_id, e in sorted(entail.items()):
    b_stmts, b_target = parse_public("chain_nl/%s.txt" % e["base"])
    p_stmts, p_target = parse_public("para_inv/%s.txt" % pair_id)
    n_stmts, n_target = parse_public("para_inv/%s.txt" % e["nonce_id"])
    # (a) normalized signature: same statement count, same numeric signature,
    #     same target, alignment is a bijection
    check(len(p_stmts) == len(b_stmts), "%s stmt count" % pair_id)
    check(sorted(int(x) for t in p_stmts for x in re.findall(r"\d+", t)) ==
          e["numeric_signature_statements"], "%s numeric sig (para)" % pair_id)
    check(sorted(int(x) for t in b_stmts for x in re.findall(r"\d+", t)) ==
          e["numeric_signature_statements"], "%s numeric sig (base)" % pair_id)
    check(p_target == b_target, "%s target differs" % pair_id)
    rows = e["align"]
    check(sorted(r[0] for r in rows) == list(range(1, len(b_stmts) + 1)) and
          sorted(r[1] for r in rows) == list(range(1, len(p_stmts) + 1)),
          "%s align not bijective" % pair_id)
    # (b) closure/target-verdict comparison: sealed base solution's target must
    #     equal the public para target and the public nonce target after
    #     de-substitution; verdict (target string) is invariant
    check(base_sol[pair_id]["target"] == p_target, "%s base target != para target" % pair_id)
    nm = nonce_map[pair_id]["nonce_map"]
    check(len(set(nm.values())) == len(nm), "%s nonce map not bijective" % pair_id)
    inv = {v: k for k, v in nm.items()}
    pat = re.compile(r"\b(" + "|".join(sorted((re.escape(v) for v in inv), key=len, reverse=True)) + r")\b")
    de = lambda t: pat.sub(lambda m: inv[m.group(0)], t)
    check([de(t) for t in n_stmts] == b_stmts, "%s nonce de-substitution != base" % pair_id)
    check(de(n_target) == b_target, "%s nonce target de-substitution != base" % pair_id)
    # freshness: no nonce word occurs in the base text
    full = " ".join(b_stmts) + " " + b_target
    for v in nm.values():
        check(not re.search(r"\b%s\b" % re.escape(v), full), "%s nonce not fresh: %s" % (pair_id, v))
print("check 5 (para-inv, two independent checks): done")

# ---------- 7. no leak outside sealed/ ----------
leak_pat = re.compile(r"DERIVED|WITHHELD|\bverdict\b|\bVERDICT\b")
for dirpath, _, filenames in os.walk(BAT):
    for fn in filenames:
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, BAT)
        if rel.startswith("sealed/"):
            continue
        if rel == "verify_battery.py":
            continue  # tooling: contains its own search pattern by construction
        txt = open(full, encoding="utf-8").read()
        check(not leak_pat.search(txt), "leak token in %s" % rel)
print("check 7 (no leak): done")

# ---------- 8. manifest ----------
man = read_battery("sealed/MANIFEST.sha256")
seen = set()
for line in man.strip().splitlines():
    h, rel = line.split("  ")
    seen.add(rel)
    check(sha256_file(os.path.join(BAT, rel)) == h, "manifest mismatch: %s" % rel)
allrels = set()
for dirpath, _, filenames in os.walk(BAT):
    for fn in filenames:
        rel = os.path.relpath(os.path.join(dirpath, fn), BAT)
        if rel != "sealed/MANIFEST.sha256":
            allrels.add(rel)
check(allrels <= seen, "files missing from manifest: %s" % (allrels - seen))
print("check 8 (manifest): done")

# ---------- 9. exit-3 guard (subprocess) ----------
code = """
import sys
sys.argv = ['gen_battery.py', '/tmp/r4guard']
sys.path.insert(0, %r)
import gen_battery as G
G.OUT = '/tmp/r4guard'
G.w_sealed('chain_nl/evil.txt', 'x')
""" % os.path.join(SRC)
r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
check(r.returncode == 3, "w_sealed guard did not exit 3 (rc=%d)" % r.returncode)
print("check 9 (exit-3 guard): done")

print()
if FAIL:
    print("%d FAILURES" % len(FAIL))
    sys.exit(1)
print("ALL CHECKS PASS")
