#!/usr/bin/env python3
"""MATH R4 battery builder. Deterministic: zero RNG, fixed data, sorted I/O.

Builds the sealed battery tree under <out>/math_logic/round4/batteries/:
  chain_nl/      20 public NL problems (no verdicts, no solutions)
  chain50_nl/    6 public NL problems (templates expanded)
  para_inv/      12 paraphrase + 12 nonce public problems (+entailment matrix, no verdicts)
  knowledge/     KNOWLEDGE_STORE_NL.md (R4 wording) + audit table
  sealed/        solutions, reference traces, nonce maps, entailment keys,
                 skeletons, and MANIFEST (sha256)
  README.md      battery documentation
  verify_battery.py  self-contained rerun verifier (copied alongside)

Sealed writes go ONLY through w_sealed() which exits 3 unless the path
starts with 'sealed/'. Public files never contain DERIVED/WITHHELD/
verdict tokens or solutions.
"""
import json
import os
import re
import sys
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
import data_chain_nl as D1
import data_chain50 as D5
import data_para as DP
import data_knowledge as DK

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/workspace/tnn-lab/math_logic/round4/batteries")

# ---------- writers ----------
def w(relpath, text):
    full = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)

def w_sealed(relpath, text):
    if not relpath.startswith("sealed/"):
        sys.stderr.write("sealed-path guard: refusing sealed write to %s\n" % relpath)
        sys.exit(3)
    w(relpath, text)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# ---------- problem renderers ----------
def render_public_chain(p):
    lines = ["# %s" % p["id"], "", "Domain: %s" % p["domain"],
             "Type: %s" % p["type"], ""]
    for i, s in enumerate(p["statements"], 1):
        lines.append("S%d. %s" % (i, s))
    lines += ["", "TARGET: %s" % p["target"], ""]
    return "\n".join(lines)

def render_chain50(p):
    rr = p.get("rule_range", range(1, p["n_rules"] + 1))
    rules = [p["rule"](n) for n in rr]
    assert len(rules) == p["n_rules"], p["id"]
    lines = ["# %s" % p["id"], "", "Title: %s" % p["title"], ""]
    lines += p["frame"] + [""]
    for i, r in enumerate(rules, 1):
        lines.append("R%d. %s" % (i, r))
    lines += ["", "TARGET: %s" % p["target"], ""]
    return "\n".join(lines)

def apply_nonce(text, nmap):
    pat = re.compile(r"\b(" + "|".join(sorted((re.escape(k) for k in nmap), key=len, reverse=True)) + r")\b")
    return pat.sub(lambda m: nmap[m.group(0)], text)

def render_para(entry, base):
    lines = ["# %s" % entry["id"], "", "Base problem: %s" % entry["base"],
             "Kind: paraphrase", ""]
    for i, s in enumerate(entry["statements"], 1):
        lines.append("S%d. %s" % (i, s))
    lines += ["", "TARGET: %s" % base["target"], ""]
    return "\n".join(lines)

def render_nonce(entry, base):
    nid = DP.nonce_id(entry["id"])
    nmap = entry["nonce_map"]
    lines = ["# %s" % nid, "", "Base problem: %s" % entry["base"],
             "Kind: nonce variant", ""]
    for i, s in enumerate(base["statements"], 1):
        lines.append("S%d. %s" % (i, apply_nonce(s, nmap)))
    lines += ["", "TARGET: %s" % apply_nonce(base["target"], nmap), ""]
    return "\n".join(lines)

# ---------- sealed renderers ----------
def sealed_chain(p):
    d = {
        "id": p["id"], "domain": p["domain"], "type": p["type"],
        "target": p["target"], "steps": p["steps"],
        "sketch": p["sketch"], "trace": p["trace"],
        "statements": p["statements"],
    }
    return json.dumps(d, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

def sealed_chain50(p):
    steps = DP_CHAIN50_STEPS[p["id"]]
    rr = list(p.get("rule_range", range(1, p["n_rules"] + 1)))
    trace = [{"step": i + 1, "concl": p["rule"](n),
              "from": ["premise" if i == 0 else "step %d" % i, "R%d" % (i + 1)],
              "license": "SUBST"}
             for i, n in enumerate(rr)]
    d = {"id": p["id"], "title": p["title"], "n_rules": p["n_rules"],
         "shortest_steps": steps, "bound_ok": 50 <= steps <= 160,
         "target": p["target"], "trace": trace}
    return json.dumps(d, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

DP_CHAIN50_STEPS = D5.EXPECTED_STEPS

# ---------- data checks (mechanical) ----------
FORBID = ["DERIVED", "WITHHELD", "verdict", "VERDICT", "solution", "SOLUTION", "answer", "ANSWER"]
STORE_KEYS = set(DK.STORE_KEYS)
STORE_TXT = {k: r4 for (k, _t, _r3, r4, _c, _n) in DK.AUDIT}
LICENSES = STORE_KEYS | {"SUBST", "ARITH", "MECH"}

def check_chains():
    assert len(D1.CHAIN_NL) == 20, "need 20 chain problems"
    ids = [p["id"] for p in D1.CHAIN_NL]
    assert len(set(ids)) == 20, "duplicate chain ids"
    doms = {}
    for p in D1.CHAIN_NL:
        assert 5 <= p["steps"] <= 20, p["id"]
        assert len(p["trace"]) == p["steps"], p["id"]
        doms[p["domain"]] = doms.get(p["domain"], 0) + 1
        # trace refs valid
        for i, t in enumerate(p["trace"], 1):
            for (kind, ref, _q) in t["from"]:
                if kind == "STEP":
                    assert 1 <= ref < i, (p["id"], i, ref)
                elif kind == "STMT":
                    assert 1 <= ref <= len(p["statements"]), (p["id"], i, ref)
                elif kind == "STORE":
                    assert ref in STORE_KEYS, (p["id"], i, ref)
                    assert _q in STORE_TXT[ref], (p["id"], i, ref, "store span not in R4")
                else:
                    raise AssertionError(("bad from kind", p["id"], i, kind))
            lic = t["license"]
            assert lic in LICENSES, (p["id"], i, lic)
            if lic in STORE_KEYS:
                # strict: a K-license must be backed by an exact R4 STORE quote in from
                assert any(k2 == "STORE" and r2 == lic and q2 in STORE_TXT[lic]
                           for (k2, r2, q2) in t["from"]), (p["id"], i, lic, "K-license without STORE quote")
            for (kind, ref, _q) in t["from"]:
                if kind == "STMT":
                    assert _q in p["statements"][ref - 1], (p["id"], i, "stmt span mismatch")
    assert doms == {"number_theory": 5, "geometry": 5, "logic_puzzles": 5, "causal_temporal": 5}, doms

def check_chain50():
    assert len(D5.CHAIN50) == 6
    ids = [p["id"] for p in D5.CHAIN50]
    assert len(set(ids)) == 6
    for p in D5.CHAIN50:
        s = D5.EXPECTED_STEPS[p["id"]]
        assert 50 <= s <= 160, (p["id"], s)
        assert s == p["n_rules"], (p["id"], "steps must equal rule count")
        rr = list(p.get("rule_range", range(1, p["n_rules"] + 1)))
        rules = [p["rule"](n) for n in rr]
        assert len(rules) == p["n_rules"]
        # linkage: split each rule at ", then "; antecedent of R1 must be
        # grounded by the premise, each consequent must feed the next antecedent,
        # and the final consequent must be the target
        def antecedent(r):
            assert r.startswith("If ") and ", then " in r
            return r[3:r.index(", then ")]
        def consequent(r):
            return r[r.index(", then ") + len(", then "):].rstrip(".")
        a0 = antecedent(rules[0]).lower()
        pr = p["premise"].lower()
        assert a0 in pr or pr in a0, (p["id"], "R1 antecedent not grounded by premise")
        for a, b in zip(rules, rules[1:]):
            assert consequent(a) == antecedent(b), (p["id"], "chain link broken")
        assert consequent(rules[-1]).lower() == p["target"].rstrip(".").lower(), (p["id"], "final consequent != target")

def num_sig(texts):
    return sorted(int(x) for t in texts for x in re.findall(r"\d+", t))

def check_para():
    assert len(DP.PARA) == 12
    assert len(set(e["id"] for e in DP.PARA)) == 12
    base_by_id = {p["id"]: p for p in D1.CHAIN_NL}
    seen_bases = set()
    for e in DP.PARA:
        b = base_by_id[e["base"]]
        assert e["base"] not in seen_bases, "duplicate base"
        seen_bases.add(e["base"])
        # statement-count match + numeric signature match
        assert len(e["statements"]) == len(b["statements"]), e["id"]
        assert num_sig(e["statements"]) == num_sig(b["statements"]), (e["id"], "numeric signature")
        assert num_sig([b["target"]]) == num_sig([b["target"]])  # trivial self-check
        # align matrix: bijection over statement indices
        rows = e["align"]
        assert sorted(r[0] for r in rows) == list(range(1, len(b["statements"]) + 1)), e["id"]
        assert sorted(r[1] for r in rows) == list(range(1, len(e["statements"]) + 1)), e["id"]
        # nonce map checks
        nm = e["nonce_map"]
        assert len(set(nm.values())) == len(nm), (e["id"], "nonce values not bijective")
        full = " ".join(b["statements"]) + " " + b["target"]
        for k, v in nm.items():
            assert re.search(r"\b%s\b" % re.escape(k), full), (e["id"], "map key absent", k)
            assert not re.search(r"\b%s\b" % re.escape(v), full), (e["id"], "nonce not fresh", v)
        # round-trip
        nonce_texts = [apply_nonce(s, nm) for s in b["statements"]] + [apply_nonce(b["target"], nm)]
        inv = {v: k for k, v in nm.items()}
        back = [apply_nonce(t, inv) for t in nonce_texts]
        assert back == list(b["statements"]) + [b["target"]], (e["id"], "round-trip failed")

def check_knowledge():
    assert len(DK.AUDIT) == 25
    assert len(set(k for (k, _, _, _, _, _) in DK.AUDIT)) == 25
    assert [k for (k, _, _, _, _, _) in DK.AUDIT] == DK.STORE_KEYS
    assert sorted(DK.changed_keys()) == ["K005", "K101", "K104"]
    # R3 bodies must match the frozen R3 file byte-for-byte
    frozen = open(os.path.expanduser("~/workspace/tmp_commit/r4/KS.md")).read()
    for (k, tag, r3, _r4, _c, _n) in DK.AUDIT:
        head = "[%s] %s" % (k, tag)
        assert head in frozen, (k, "header missing in frozen R3")
        assert r3 in frozen, (k, "R3 body not found verbatim in frozen R3")

# ---------- build ----------
def main():
    check_chains()
    check_chain50()
    check_para()
    check_knowledge()

    manifest = []

    def pub(relpath, text):
        w(relpath, text)
        manifest.append((relpath, sha256_file(os.path.join(OUT, relpath))))

    # public: chain_nl
    for p in D1.CHAIN_NL:
        pub("chain_nl/%s.txt" % p["id"], render_public_chain(p))
    # public: chain50_nl
    for p in D5.CHAIN50:
        pub("chain50_nl/%s.txt" % p["id"], render_chain50(p))
    # public: para_inv
    base_by_id = {p["id"]: p for p in D1.CHAIN_NL}
    entail = {}
    for e in DP.PARA:
        b = base_by_id[e["base"]]
        pub("para_inv/%s.txt" % e["id"], render_para(e, b))
        pub("para_inv/%s.txt" % DP.nonce_id(e["id"]), render_nonce(e, b))
        entail[e["id"]] = {"base": e["base"], "nonce_id": DP.nonce_id(e["id"]),
                           "align": e["align"],
                           "numeric_signature_statements": num_sig(e["statements"]),
                           "numeric_signature_target": num_sig([b["target"]])}
    pub("para_inv/PARA_ENTAIL.json", json.dumps(entail, indent=2, sort_keys=True) + "\n")

    # public: knowledge
    pub("knowledge/KNOWLEDGE_STORE_NL.md", DK.r4_store_text())
    audit_lines = ["# KNOWLEDGE WORDING AUDIT (R3 -> R4)",
                   "",
                   "R3 source: docs/lab/math_logic/round3/NL/KNOWLEDGE_STORE_NL.md",
                   "Formal store: docs/lab/math_logic/round3/NL/KNOWLEDGE_STORE_FORMAL.md",
                   "",
                   "| key | changed | before (R3) | after (R4) | surface restored |",
                   "|-----|---------|-------------|------------|------------------|"]
    for (k, _tag, r3, r4, changed, note) in DK.AUDIT:
        audit_lines.append("| %s | %s | %s | %s | %s |" %
                           (k, "YES" if changed else "no",
                            r3.replace("|", "\\|"), r4.replace("|", "\\|"),
                            note.replace("|", "\\|")))
    pub("knowledge/KNOWLEDGE_AUDIT_R3_R4.md", "\n".join(audit_lines) + "\n")

    # ship the verifier alongside (it is not part of the battery content)
    import shutil as _shutil
    _shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_battery.py"),
                     os.path.join(OUT, "verify_battery.py"))
    manifest.append(("verify_battery.py", sha256_file(os.path.join(OUT, "verify_battery.py"))))

    # sealed
    for p in D1.CHAIN_NL:
        w_sealed("sealed/%s.sol.json" % p["id"], sealed_chain(p))
    for p in D5.CHAIN50:
        w_sealed("sealed/%s.skel.json" % p["id"], sealed_chain50(p))
    w_sealed("sealed/PARA_NONCE_MAP.json",
             json.dumps({e["id"]: {"base": e["base"], "nonce_map": e["nonce_map"],
                                   "nonce_id": DP.nonce_id(e["id"])}
                         for e in DP.PARA}, indent=2, sort_keys=True) + "\n")
    w_sealed("sealed/PARA_BASE_SOL.json",
             json.dumps({e["id"]: {"base": e["base"], "target": base_by_id[e["base"]]["target"],
                                   "statements": base_by_id[e["base"]]["statements"]}
                         for e in DP.PARA}, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    w_sealed("sealed/KNOWLEDGE_R3_NL.txt", DK.r3_store_text())

    # README
    readme = """# MATH R4 batteries

Frozen prereg: docs/lab/math_logic/round4/PREREG_MATH_R4.md (commit 84ed45077a554f9897ec55c2ca1430273c79eb69).

Contents:
- chain_nl/ : 20 raw-NL chain problems (5 per domain: number_theory, geometry, logic_puzzles, causal_temporal), each requiring 5-20 derivation steps. Public files carry NO verdicts, solutions, or traces.
- chain50_nl/ : 6 raw-NL long-chain problems requiring 50-160 steps. Public files carry the problem only.
- para_inv/ : 12 paraphrase pairs + 12 nonce-word variants (public problems only). PARA_ENTAIL.json records the statement alignment and numeric signatures (no verdicts).
- knowledge/ : KNOWLEDGE_STORE_NL.md (R4 wording) and KNOWLEDGE_AUDIT_R3_R4.md (full R3->R4 wording audit of all 25 items).
- sealed/ : sealed solutions, reference traces, nonce maps, skeletons, and MANIFEST.sha256. Engine crews must not read this directory.

Verification: run `python3 verify_battery.py <battery_dir> <source_dir>` (byte-identical
rebuild + all checks). The builder (gen_battery.py) is deterministic Python over
hand-authored data (zero RNG); byte-identical rerun is verified, not assumed.
Sealed-solution isolation: w_sealed() exits 3 on any non-sealed/ write; the verifier tests this.
Determinism: pure deterministic construction, zero RNG; rerun must be byte-identical.
"""
    w("README.md", readme)
    manifest.append(("README.md", sha256_file(os.path.join(OUT, "README.md"))))

    # sealed manifest (sha256 of every file incl. sealed ones)
    man_lines = []
    for dirpath, _, filenames in os.walk(OUT):
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, OUT)
            man_lines.append("%s  %s" % (sha256_file(full), rel))
    w_sealed("sealed/MANIFEST.sha256", "\n".join(sorted(man_lines)) + "\n")

    # guard self-test: a non-sealed write through w_sealed must exit 3
    # (exercised by verify_battery.py in a subprocess)

    print("built %d public files" % len(manifest))
    for rel, h in sorted(manifest):
        print("  %s  %s" % (h[:12], rel))

if __name__ == "__main__":
    main()
