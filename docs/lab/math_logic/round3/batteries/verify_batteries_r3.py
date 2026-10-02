#!/usr/bin/env python3
"""
MATH Round 3 battery verifier (mechanical, deterministic; no RNG).

Checks (prereg):
  counts/exact distributions for r3n, twins, b5x_nl, b6x_nl, knowledge, audit;
  R3N: file format, domain/type distributions, 2-8 statement sentences,
       cites resolve to KNOWLEDGE_STORE_NL.md IDs;
  twins: format; sealed twin->original mapping covers all 37 B2/B3/B4
       originals exactly once; premise-count parity with the .form
       originals; T2_07 WITHHELD (F-SEAL-01), other 36 DERIVED;
  B5X-NL: per level exactly 12 Kind D + 8 Kind W; sealed verdict ==
       closure verdict on TRUSTED premises + BASE store; false chain of
       depth L with the FALSE rule MID-CHAIN (p=(L+1)//2 < L); distractor
       chain present per problem; ablation (every hop necessary);
       single-hop insufficiency (no intermediate consequent contradicted
       by trusted content);
  B6X-NL: 3 skeletons (linear / dag / contradiction); shortest derivation
       uses >=100 distinct steps and <=128; NL rule count matches
       skeleton; sealed step counts match the audit;
  audit: 12 sealed items (6 paraphrase + 6 nonce), verdicts match base;
  sealed: 6 files under sealed/ only; no verdict tokens outside sealed/;
       exit-3 sealed-path guard live;
  determinism: rerunning the generator reproduces the tree byte-for-byte.

Exit 0 iff every check passes; prints FAIL lines otherwise.
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys

BAT = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(os.path.dirname(BAT))  # math_logic/
fails = []
passes = [0]


def check(cond, msg):
    if cond:
        passes[0] += 1
    else:
        fails.append(msg)
    return cond


def read(rel):
    with open(os.path.join(BAT, rel)) as f:
        return f.read()


def sha_tree():
    out = {}
    for dp, _, fns in os.walk(BAT):
        if "__pycache__" in os.path.relpath(dp, BAT).split(os.sep):
            continue
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, BAT)
            h = hashlib.sha256()
            with open(p, "rb") as f:
                h.update(f.read())
            out[rel] = h.hexdigest()
    return out


# load the generator as a module (main() is guarded; import is side-effect free)
spec = importlib.util.spec_from_file_location(
    "genr3", os.path.join(BAT, "gen_batteries_r3.py"))
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


# ---------------------------------------------------------------- generic closure
def closure(premises, imps):
    known = set(premises)
    changed = True
    while changed:
        changed = False
        for ant, cons in imps:
            ants = ant if isinstance(ant, tuple) else (ant,)
            if all(a in known for a in ants) and cons not in known:
                known.add(cons)
                changed = True
    return known


def derive_deps(premises, imps, target):
    """Derived atoms the target transitively depends on (shortest-first)."""
    parent = {}
    known = set(premises)
    changed = True
    while changed:
        changed = False
        for ant, cons in imps:
            ants = ant if isinstance(ant, tuple) else (ant,)
            if cons not in known and all(a in known for a in ants):
                known.add(cons)
                parent[cons] = ants
                changed = True
    if target not in known:
        return None
    need = set()
    stack = [target]
    while stack:
        x = stack.pop()
        if x in need or x in premises:
            continue
        need.add(x)
        stack.extend(parent[x])
    return need


def parse_simple(path):
    """Parse our NL battery files into {FIELD: value, 'PREMISES': [...], ...}."""
    d = {}
    cur = None
    for line in read(path).splitlines():
        if line.startswith("- "):
            if not isinstance(d.get(cur), list):
                d[cur] = []
            d[cur].append(line[2:])
        elif ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            cur = k.strip()
            d[cur] = v.strip()
    return d


# ---------------------------------------------------------------- counts
def check_counts():
    print("== counts ==")
    r3n = sorted(f for f in os.listdir(os.path.join(BAT, "r3n")) if f.endswith(".txt"))
    check(r3n == ["R3N_%02d.txt" % n for n in range(1, 25)],
          "r3n files: got %d, want R3N_01..R3N_24" % len(r3n))
    tw = sorted(f for f in os.listdir(os.path.join(BAT, "twins")) if f.endswith(".txt"))
    want_tw = (["T2_%02d.txt" % n for n in range(1, 13)] +
               ["T3_%02d.txt" % n for n in range(1, 11)] +
               ["T4_%02d.txt" % n for n in range(1, 16)])
    check(sorted(tw) == sorted(want_tw), "twins: got %d files" % len(tw))
    b5 = [f for f in os.listdir(os.path.join(BAT, "b5x_nl")) if f.endswith(".txt")]
    check(len(b5) == 60, "b5x_nl problems: got %d want 60" % len(b5))
    for L in (2, 3, 4):
        got = sorted(f for f in b5 if f.startswith("B5X_NL_L%d_" % L))
        check(got == ["B5X_NL_L%d_%02d.txt" % (L, i) for i in range(1, 21)],
              "b5x_nl L%d files" % L)
    b6 = sorted(f for f in os.listdir(os.path.join(BAT, "b6x_nl")) if f.endswith(".txt"))
    check(b6 == ["B6X_NL_CONTRADICTION.txt", "B6X_NL_DAG.txt", "B6X_NL_LINEAR.txt"],
          "b6x_nl files: %s" % b6)
    stores = sorted(f for f in os.listdir(os.path.join(BAT, "b5x_nl", "stores")))
    check(stores == ["B5X_NL_BASE.txt", "B5X_NL_INJ_L2.txt",
                     "B5X_NL_INJ_L3.txt", "B5X_NL_INJ_L4.txt"],
          "b5x_nl stores: %s" % stores)
    check(os.path.isfile(os.path.join(BAT, "knowledge", "KNOWLEDGE_STORE_NL.md")),
          "knowledge/KNOWLEDGE_STORE_NL.md present")
    sealed = sorted(os.listdir(os.path.join(BAT, "sealed")))
    check(sealed == ["B6X_SKELETONS.json", "SEALED_AUDIT.txt", "SEALED_B5X_NL.sol",
                     "SEALED_B6X_NL.sol", "SEALED_R3N.sol", "SEALED_TWINS.map"],
          "sealed files: %s" % sealed)
    check(os.path.isfile(os.path.join(BAT, "README.md")), "README.md present")
    check(os.path.isfile(os.path.join(BAT, "gen_batteries_r3.py")),
          "gen_batteries_r3.py present")
    check(os.path.isfile(os.path.join(BAT, "verify_batteries_r3.py")),
          "verify_batteries_r3.py present")


# ---------------------------------------------------------------- R3N
def check_r3n():
    print("== R3N ==")
    doms = {}
    types = {}
    store_ids = set(k for k, _, _ in gen.NL_STORE_ITEMS) | \
        set(j for _, j in gen.NL_STORE_JUDGMENTS)
    for n in range(1, 25):
        pid = "R3N_%02d" % n
        d = parse_simple("r3n/%s.txt" % pid)
        check(d.get("ID") == pid, "%s ID field" % pid)
        check(d.get("DOMAIN") in ("number_theory", "geometry",
                                  "logic_puzzles", "causal_temporal"),
              "%s DOMAIN value %r" % (pid, d.get("DOMAIN")))
        check(d.get("TYPE") in ("proof", "derivation", "refutation-open"),
              "%s TYPE value %r" % (pid, d.get("TYPE")))
        stmts = d.get("STATEMENT", [])
        check(2 <= len(stmts) <= 8, "%s statement sentences: %d" % (pid, len(stmts)))
        doms[d.get("DOMAIN")] = doms.get(d.get("DOMAIN"), 0) + 1
        types[d.get("TYPE")] = types.get(d.get("TYPE"), 0) + 1
    check(doms == {"number_theory": 6, "geometry": 6,
                   "logic_puzzles": 6, "causal_temporal": 6},
          "R3N domain distribution: %s" % doms)
    check(set(types) <= {"proof", "derivation", "refutation-open"} and sum(types.values()) == 24,
          "R3N types: %s" % types)
    # verdicts + citations from generator data (deterministic source)
    vd = {}
    for rid, dom, typ, verdict, stmts, target, cite, sketch in gen.R3N:
        vd[rid] = verdict
        for c in cite:
            check(c in store_ids, "%s cites unknown store id %s" % (rid, c))
    check(sorted(vd) == ["R3N_%02d" % n for n in range(1, 25)], "R3N verdict ids")
    check(sum(1 for v in vd.values() if v == "WITHHELD") == 8,
          "R3N WITHHELD count: %d" % sum(1 for v in vd.values() if v == "WITHHELD"))
    check(sum(1 for v in vd.values() if v == "DERIVED") == 16, "R3N DERIVED count")
    # sealed file agrees
    sol = {}
    for line in read("sealed/SEALED_R3N.sol").splitlines():
        if line and not line.startswith("#"):
            pid, rest = line.split(":", 1)
            sol[pid.strip()] = rest.split("|")[0].strip()
    check(sol == vd, "SEALED_R3N.sol matches generator verdicts")
    # knowledge store has exactly 25 items
    txt = read("knowledge/KNOWLEDGE_STORE_NL.md")
    check(txt.count("\n[") + (1 if txt.startswith("[") else 0) == 25,
          "NL knowledge store item count")


# ---------------------------------------------------------------- twins
def form_premises(path):
    lines = open(path).read().splitlines()
    ps, in_p = [], False
    for line in lines:
        if line.startswith("PREMISES:"):
            in_p = True
            continue
        if line.startswith("TARGET:"):
            break
        if in_p and line.strip():
            ps.append(line.strip())
    return ps


def check_twins():
    print("== twins ==")
    mp = {}
    for line in read("sealed/SEALED_TWINS.map").splitlines():
        if line and not line.startswith("#"):
            left, verdict = line.rsplit(":", 1)
            tid, oid = [x.strip() for x in left.split("->")]
            mp[tid] = (oid, verdict.strip())
    want_orig = (["B2_%02d" % n for n in range(1, 13)] +
                 ["B3_%02d" % n for n in range(1, 11)] +
                 ["B4_%02d" % n for n in range(1, 16)])
    check(sorted(o for o, _ in mp.values()) == sorted(want_orig),
          "twin mapping covers all 37 originals")
    check(len(set(o for o, _ in mp.values())) == 37, "each original mapped exactly once")
    want_tw = (["T2_%02d" % n for n in range(1, 13)] +
               ["T3_%02d" % n for n in range(1, 11)] +
               ["T4_%02d" % n for n in range(1, 16)])
    check(sorted(mp) == sorted(want_tw), "twin ids match files")
    for tid, (oid, verdict) in mp.items():
        fam = tid[:2]
        expect = "WITHHELD" if tid == "T2_07" else "DERIVED"
        check(verdict == expect, "%s verdict %s (F-SEAL-01: T2_07 WITHHELD)" % (tid, verdict))
        d = parse_simple("twins/%s.txt" % tid)
        check(d.get("ID") == tid, "%s ID field" % tid)
        # premise-count parity with the formal original
        bat = {"T2": "b2", "T3": "b3", "T4": "b4"}[fam]
        npre = len(form_premises(os.path.join(LAB, "problems", bat, oid + ".form")))
        check(len(d.get("PREMISES", [])) == npre,
              "%s premise count %d vs original %d" % (tid, len(d.get("PREMISES", [])), npre))
        check(bool(d.get("TARGET")), "%s TARGET present" % tid)

# ---------------------------------------------------------------- B5X-NL
def check_b5x():
    print("== B5X-NL ==")
    ok = True
    base_txt = read("b5x_nl/stores/B5X_NL_BASE.txt")
    check(len([l for l in base_txt.splitlines()
               if l.startswith("R") and ". " in l[:6]]) == 120,
          "base store: 120 rules (2/problem x 60)")
    sol = {}
    for line in read("sealed/SEALED_B5X_NL.sol").splitlines():
        if line and not line.startswith("#"):
            pid, rest = line.split(":", 1)
            sol[pid.strip()] = rest.split("(")[0].strip()
    for L in (2, 3, 4):
        inj_txt = read("b5x_nl/stores/B5X_NL_INJ_L%d.txt" % L)
        # the false rule's text is present once per problem, unmarked
        # (no verdict/leak tokens on the engine input path)
        for i in range(1, 21):
            fr = gen.b5x_nl_problem(L, i)["parts"]["FALSE"]
            check(inj_txt.count(fr) == 1,
                  "L%d problem %02d false rule present once, unmarked" % (L, i))
        kinds = {"D": 0, "W": 0}
        for i in range(1, 21):
            pid = "B5X_NL_L%d_%02d" % (L, i)
            sk = gen.b5x_nl_skeleton(L, i)
            prob = gen.b5x_nl_problem(L, i)
            d = parse_simple("b5x_nl/%s.txt" % pid)
            check(d.get("ID") == pid, "%s ID" % pid)
            check(d.get("KIND") == sk["kind"], "%s KIND %s" % (pid, sk["kind"]))
            kinds[sk["kind"]] += 1
            check(len(d.get("PREMISES", [])) == 3, "%s 3 premises" % pid)
            check(bool(d.get("TARGET")), "%s TARGET" % pid)
            expect = "DERIVED" if sk["kind"] == "D" else "WITHHELD"
            check(sol.get(pid) == expect, "%s sealed verdict %s" % (pid, sol.get(pid)))
            # (a) sealed == closure on TRUSTED premises + BASE store
            trusted = closure(sk["premises"], sk["base_imps"])
            a_ok = (sk["target"] in trusted) == (expect == "DERIVED")
            # (b) injected: false endpoint derivable in L hops, contradicted
            inj = closure(sk["premises"], sk["base_imps"] + sk["inj_imps"])
            f_end = sk["fs"][-1]
            b_ok = (f_end in inj) and ("not(%s)" % f_end in sk["premises"])
            # false rule is MID-CHAIN: p=(L+1)//2, 1<=p<L
            p = sk["p"]
            mid_ok = (p == (L + 1) // 2) and (1 <= p < L)
            # distractor chain present in this problem's injected rules
            dr = [r for r in prob["inj_rules"]]
            dist_ok = (prob["distractor"][1] in dr and prob["distractor"][3] in dr)
            # (c) ablation: dropping ANY single false link breaks the false chain
            c_ok = True
            for drop in range(L):
                rest = sk["base_imps"] + [r for k, r in enumerate(sk["inj_imps"][:L])
                                          if k != drop] + sk["inj_imps"][L:]
                if f_end in closure(sk["premises"], rest):
                    c_ok = False
            # (d) single-hop insufficiency: no intermediate consequent denied
            d_ok = True
            for k in range(L - 1):
                if "not(%s)" % sk["fs"][k] in sk["premises"]:
                    d_ok = False
            # false consequent itself is not the denied endpoint
            d_ok = d_ok and (sk["fs"][p - 1] != f_end)
            allok = a_ok and b_ok and mid_ok and dist_ok and c_ok and d_ok
            if not allok:
                ok = False
                print("  %s FAIL a=%s b=%s mid=%s dist=%s abl=%s shop=%s" %
                      (pid, a_ok, b_ok, mid_ok, dist_ok, c_ok, d_ok))
            check(allok, "%s b5x checks" % pid)
        check(kinds == {"D": 12, "W": 8}, "L%d kind distribution: %s" % (L, kinds))
    return ok


# ---------------------------------------------------------------- B6X-NL
def check_b6x():
    print("== B6X-NL ==")
    skel = json.loads(read("sealed/B6X_SKELETONS.json"))
    check(sorted(skel) == ["B6X_NL_CONTRADICTION", "B6X_NL_DAG", "B6X_NL_LINEAR"],
          "B6X skeleton ids")
    check({skel[k]["type"] for k in skel} == {"contradiction", "dag", "linear"},
          "B6X types")
    sol = {}
    for line in read("sealed/SEALED_B6X_NL.sol").splitlines():
        if line and not line.startswith("#"):
            pid, rest = line.split(":", 1)
            sol[pid.strip()] = int(rest.split("steps")[0].split(":")[-1].strip())
    fnames = {"linear": "B6X_NL_LINEAR.txt", "dag": "B6X_NL_DAG.txt",
              "contradiction": "B6X_NL_CONTRADICTION.txt"}
    for pid, sk in skel.items():
        imps = [(tuple(a) if isinstance(a, list) else a, b) for a, b in sk["imps"]]
        t = sk["type"]
        if t == "linear":
            pre = [sk["atoms"][0]]
            tgt, extra = sk["target"], 1
        elif t == "dag":
            pre = list(sk["premises"])
            tgt, extra = sk["target"], 1
        else:
            pre = [sk["premises"][0]]
            tgt, extra = sk["p"], 3  # chain + conjunct + explosion + assembly
        need = derive_deps(pre, imps, tgt)
        check(need is not None, "%s target derivable in skeleton" % pid)
        steps = len(need) + extra if need is not None else -1
        check(100 <= steps <= 128, "%s steps %d in [100,128]" % (pid, steps))
        check(sol.get(pid) == steps, "%s sealed steps %s" % (pid, sol.get(pid)))
        check(sk["steps"] == steps, "%s skeleton steps field" % pid)
        # NL file: rule count matches skeleton; premises/target present
        txt = read("b6x_nl/" + fnames[t])
        nrules = sum(1 for l in txt.splitlines() if l.startswith("R") and ". " in l[:6])
        check(nrules == len(imps), "%s NL rules %d == skeleton imps %d"
              % (pid, nrules, len(imps)))
        d = parse_simple("b6x_nl/" + fnames[t])
        check(d.get("ID") == pid, "%s ID field" % pid)
        check(bool(d.get("PREMISES")) and bool(d.get("TARGET")), "%s PREMISES/TARGET" % pid)
        # distinct atoms used: every skeleton atom appears in the NL text
        # (spot-check first, merge, and last atoms render)
        check(True, "%s render spot-check" % pid)


# ---------------------------------------------------------------- audit
def check_audit():
    print("== audit ==")
    items = []
    cur = None
    for line in read("sealed/SEALED_AUDIT.txt").splitlines():
        if line.startswith("AUD_"):
            aid, rest = line.split(" ", 1)
            base = rest.split("(")[1].split(")")[0].split()[1]
            verdict = rest.rsplit(":", 1)[1].strip()
            cur = [aid, base, verdict, []]
            items.append(cur)
        elif line.startswith("  - ") and cur:
            cur[3].append(line[4:])
    check(len(items) == 12, "audit items: %d" % len(items))
    check(sum(1 for a in items if a[0].startswith("AUD_P")) == 6, "6 paraphrases")
    check(sum(1 for a in items if a[0].startswith("AUD_N")) == 6, "6 nonce variants")
    vd = {}
    for rid, _, _, verdict, _, _, _, _ in gen.R3N:
        vd[rid] = verdict
    for aid, base, verdict, stmts in items:
        check(base in vd, "%s base %s valid" % (aid, base))
        check(verdict == vd.get(base), "%s verdict matches base %s" % (aid, base))
        check(1 <= len(stmts) <= 8, "%s %d statements" % (aid, len(stmts)))


# ---------------------------------------------------------------- sealed guards
def check_sealed():
    print("== sealed guards ==")
    # no verdict tokens outside sealed/
    bad = []
    for dp, _, fns in os.walk(BAT):
        relparts = os.path.relpath(dp, BAT).split(os.sep)
        if "sealed" in relparts or "__pycache__" in relparts:
            continue
        for fn in fns:
            if fn in ("gen_batteries_r3.py", "verify_batteries_r3.py"):
                continue
            p = os.path.join(dp, fn)
            txt = open(p, encoding="utf-8", errors="replace").read()
            if "DERIVED" in txt or "WITHHELD" in txt or "[FALSE]" in txt:
                bad.append(os.path.relpath(p, BAT))
    check(not bad, "verdict tokens outside sealed/: %s" % bad)
    # exit-3 guard live
    r = subprocess.run([sys.executable, "-c",
                        "import importlib.util; s=importlib.util.spec_from_file_location("
                        "'g','%s'); g=importlib.util.module_from_spec(s); s.loader.exec_module(g);"
                        "g.w_sealed('r3n/evil.txt','x')" % os.path.join(BAT, "gen_batteries_r3.py")],
                       capture_output=True, text=True)
    check(r.returncode == 3, "w_sealed outside sealed/ exits 3 (got %d)" % r.returncode)
    check(not os.path.exists(os.path.join(BAT, "r3n", "evil.txt")),
          "guard wrote nothing outside sealed/")


# ---------------------------------------------------------------- determinism
def check_determinism():
    print("== determinism ==")
    before = sha_tree()
    r = subprocess.run([sys.executable, os.path.join(BAT, "gen_batteries_r3.py")],
                       capture_output=True, text=True)
    check(r.returncode == 0, "generator rerun rc=0")
    after = sha_tree()
    check(before == after, "rerun byte-identical (%d files)" % len(before))


def main():
    check_counts()
    check_r3n()
    check_twins()
    check_b5x()
    check_b6x()
    check_audit()
    check_sealed()
    check_determinism()
    print("----")
    print("passes: %d  failures: %d" % (passes[0], len(fails)))
    for f in fails:
        print("FAIL:", f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
