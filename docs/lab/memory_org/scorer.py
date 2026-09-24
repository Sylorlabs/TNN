#!/usr/bin/env python3
"""MORG scorer (crew 1). Scores arm retrieval results against frozen fixtures.

Usage:
  scorer.py [--fixtures DIR] [--results DIR] [--out SCORES.md]

Results layout (produced by crew 2):
  results/<arm>/run<R>/retrieval.txt            qid|ranked_ids (top-20)
  results/<arm>/run<R>/retrieval_holdout.txt    qid|ranked_ids (top-20)
  results/<arm>/run<R>/scheme.txt              SELF: chosen + scores + rationale
  results/<arm>/run<R>/scheme_t0.txt           SELF: scheme before holdout ingest
  results/<arm>/run<R>/scheme_t1.txt           SELF: scheme after holdout ingest
  results/<arm>/run<R>/retrieval_holdout_old.txt  holdout queries under t0 scheme
  results/<arm>/run<R>/verify_report.txt       B3/B4/B5 PASS/FAIL lines
  results/<arm>/run<R>/ops.txt                 op counts

Writes SCORES.md with: B1 macro F1 per arm/class/overall (test queries only),
B2 interference fractions, B7 holdout F1, B6 drift table, KB-1..KB-5 verdicts,
B3/B4/B5 evidence ingested from verify_report.txt.
Zero RNG: every computation is a deterministic function of the inputs.
"""
import argparse
import hashlib
import os
import re
import sys
from collections import defaultdict

ARMS = ["SELF", "IMPOSED", "FLAT"]
SCHEMES = ["S1", "S2", "S3", "S4", "S5", "S6"]
# frozen tie-break: fewer levels wins, then lowest scheme index
LEVELS = {"S1": 3, "S2": 3, "S3": 2, "S4": 3, "S5": 3, "S6": 1}
CLASSES = ["PURE", "SUBJ", "AMBIG"]
KB1_TOL = 0.02
KB5_NOTE = 0.03
DRIFT_NEUTRAL = 0.01


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def load_items(path):
    items = {}  # id -> (domain, type, subject)
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            i, d, t, s, _x = line.split("|", 4)
            items[i] = (d, t, s)
    return items


def load_queries(path):
    qs = {}  # qid -> dict
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            q, sp, cl, th, dh, sh, tx, gold = line.split("|", 7)
            qs[q] = {"split": sp, "class": cl, "thint": th, "dhint": dh,
                     "shint": sh, "text": tx, "gold": gold.split(",") if gold else []}
    return qs


def load_retrieval(path):
    ret = {}
    if not os.path.exists(path):
        return None
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            q, ids = line.split("|", 1)
            ret[q] = [x for x in ids.split(",") if x]
    return ret


def f1(retrieved, gold):
    r = retrieved[:20]
    g = set(gold)
    if not r or not g:
        return 0.0
    hit = len(set(r) & g)
    p = hit / len(r)
    rec = hit / len(g)
    return 2 * p * rec / (p + rec) if (p + rec) > 0 else 0.0


def macro_f1(ret, queries, qids):
    vals = [f1(ret.get(q, []), queries[q]["gold"]) for q in qids]
    return sum(vals) / len(vals) if vals else 0.0


# ---------------------------------------------------------------- scheme parsing
def parse_scheme_file(path):
    """Return (per_domain dict, global dict) where each maps
    {'chosen': 'S2', 'scores': {'S1':..,...}, 'rationale': str} or None."""
    if not os.path.exists(path):
        return None
    per_domain = {}
    cur_dom = None
    cur = {"chosen": None, "scores": {}, "rationale": ""}
    has_domain_sections = False

    def flush():
        if cur["chosen"] or cur["scores"]:
            if cur_dom:
                per_domain[cur_dom] = dict(cur)
            else:
                per_domain["_global"] = dict(cur)

    with open(path) as f:
        for line in f:
            line = line.strip()
            m = re.match(r"(?i)^domain\s*[:=]\s*(\S+)", line)
            if m:
                flush()
                cur_dom = m.group(1).lower()
                cur = {"chosen": None, "scores": {}, "rationale": ""}
                has_domain_sections = True
                continue
            m = re.match(r"(?i)^chosen\s*[:=]\s*(S[1-6])", line)
            if m:
                cur["chosen"] = m.group(1).upper()
                continue
            m = re.match(r"^(S[1-6])\s*[:=]\s*([0-9]*\.?[0-9]+)", line)
            if m:
                cur["scores"][m.group(1).upper()] = float(m.group(2))
                continue
            m = re.match(r"(?i)^rationale\s*[:=]\s*(.*)", line)
            if m:
                cur["rationale"] = m.group(1)
    flush()
    if has_domain_sections:
        per_domain.pop("_global", None)
        return per_domain or None
    g = per_domain.get("_global")
    return {"_global": g} if g else None


def rederive(scores):
    """Frozen selection rule: argmax mean F1; tie-break fewer levels, then lowest index."""
    if not scores:
        return None
    best = max(scores.values())
    cands = [s for s, v in scores.items() if v == best]
    cands.sort(key=lambda s: (LEVELS[s], int(s[1:])))
    return cands[0]


def scheme_label(parsed):
    if not parsed:
        return "MISSING"
    if "_global" in parsed:
        return parsed["_global"]["chosen"] or "?"
    return "{" + ", ".join("%s:%s" % (d, v["chosen"] or "?")
                            for d, v in sorted(parsed.items())) + "}"


# ---------------------------------------------------------------- main scoring
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", default=os.path.expanduser("~/workspace/morg/fixture"))
    ap.add_argument("--results", default=os.path.expanduser("~/workspace/morg/results"))
    ap.add_argument("--out", default=os.path.expanduser("~/workspace/morg/SCORES.md"))
    a = ap.parse_args()

    fx = a.fixtures
    corpus = load_items(os.path.join(fx, "corpus.txt"))
    corpus.update(load_items(os.path.join(fx, "corpus_holdout.txt")))
    queries = load_queries(os.path.join(fx, "queries.txt"))
    hqueries = load_queries(os.path.join(fx, "queries_holdout.txt"))

    test_q = sorted(q for q, v in queries.items() if v["split"] == "test")
    test_by_class = {c: sorted(q for q in test_q if queries[q]["class"] == c) for c in CLASSES}
    pure_test = test_by_class["PURE"]
    type_pure = [q for q in pure_test if queries[q]["thint"]]
    dom_pure = [q for q in pure_test if not queries[q]["thint"] and queries[q]["dhint"]]
    hq = sorted(hqueries)
    hq_by_class = {c: sorted(q for q in hq if hqueries[q]["class"] == c) for c in CLASSES}

    fix_sha = {n: sha256_file(os.path.join(fx, n)) for n in
               ("corpus.txt", "corpus_holdout.txt", "queries.txt", "queries_holdout.txt")}

    arms = {}
    notes = []
    for arm in ARMS:
        adir = os.path.join(a.results, arm)
        if not os.path.isdir(adir):
            notes.append("%s: results dir MISSING" % arm)
            continue
        runs = sorted(d for d in os.listdir(adir)
                      if os.path.isdir(os.path.join(adir, d)))
        if not runs:
            notes.append("%s: no run dirs" % arm)
            continue
        # rerun byte-identity check
        files = ["retrieval.txt", "retrieval_holdout.txt", "scheme.txt",
                 "scheme_t0.txt", "scheme_t1.txt", "retrieval_holdout_old.txt",
                 "verify_report.txt", "ops.txt"]
        mismatch = []
        for fn in files:
            shas = set()
            for r in runs:
                p = os.path.join(adir, r, fn)
                if os.path.exists(p):
                    shas.add(sha256_file(p))
            if len(shas) > 1:
                mismatch.append(fn)
        if mismatch:
            notes.append("%s: NON-IDENTICAL reruns in %s" % (arm, ",".join(mismatch)))
        rdir = os.path.join(adir, runs[0])
        arms[arm] = {
            "runs": runs,
            "ret": load_retrieval(os.path.join(rdir, "retrieval.txt")) or {},
            "ret_h": load_retrieval(os.path.join(rdir, "retrieval_holdout.txt")) or {},
            "ret_h_old": load_retrieval(os.path.join(rdir, "retrieval_holdout_old.txt")),
            "scheme": parse_scheme_file(os.path.join(rdir, "scheme.txt")),
            "scheme_t0": parse_scheme_file(os.path.join(rdir, "scheme_t0.txt")),
            "scheme_t1": parse_scheme_file(os.path.join(rdir, "scheme_t1.txt")),
            "verify": (open(os.path.join(rdir, "verify_report.txt")).read()
                       if os.path.exists(os.path.join(rdir, "verify_report.txt")) else None),
            "ops": (open(os.path.join(rdir, "ops.txt")).read()
                    if os.path.exists(os.path.join(rdir, "ops.txt")) else None),
        }

    # ---- B1
    b1 = {}
    for arm, d in arms.items():
        per = {c: macro_f1(d["ret"], queries, test_by_class[c]) for c in CLASSES}
        per["overall"] = macro_f1(d["ret"], queries, test_q)
        b1[arm] = per

    # ---- B2 interference (test PURE queries, top-10)
    b2 = {}
    for arm, d in arms.items():
        wt, wd = [], []
        for q in type_pure:
            top = d["ret"].get(q, [])[:10]
            th = queries[q]["thint"]
            if top:
                wt.append(sum(1 for i in top if corpus.get(i, (None, None, None))[1] != th) / len(top))
        for q in dom_pure:
            top = d["ret"].get(q, [])[:10]
            dh = queries[q]["dhint"]
            if top:
                wd.append(sum(1 for i in top if corpus.get(i, (None, None, None))[0] != dh) / len(top))
        b2[arm] = {"type_pure_wrong_type": sum(wt) / len(wt) if wt else None,
                   "domain_pure_wrong_domain": sum(wd) / len(wd) if wd else None,
                   "n_type": len(wt), "n_dom": len(wd)}

    # ---- B7 holdout F1
    b7 = {}
    for arm, d in arms.items():
        per = {c: macro_f1(d["ret_h"], hqueries, hq_by_class[c]) for c in CLASSES}
        per["overall"] = macro_f1(d["ret_h"], hqueries, hq)
        b7[arm] = per

    # ---- B6 drift
    b6 = {}
    for arm, d in arms.items():
        old = d["ret_h_old"] if d["ret_h_old"] is not None else d["ret_h"]
        f_old = macro_f1(old, hqueries, hq)
        f_new = macro_f1(d["ret_h"], hqueries, hq)
        t0, t1 = scheme_label(d["scheme_t0"]), scheme_label(d["scheme_t1"])
        changed = "n/a" if (d["scheme_t0"] is None or d["scheme_t1"] is None) else (
            "y" if t0 != t1 else "n")
        delta = f_new - f_old
        outcome = "neutral" if abs(delta) < DRIFT_NEUTRAL else ("helped" if delta > 0 else "hurt")
        b6[arm] = {"t0": t0, "t1": t1, "changed": changed,
                   "f_old": f_old, "f_new": f_new, "delta": delta, "outcome": outcome}

    # ---- verify_report evidence: B3/B4/B5
    vb = {}
    for arm, d in arms.items():
        v = d["verify"]
        row = {}
        if v is None:
            row = {"B3": "MISSING", "B4": "MISSING", "B5": "MISSING"}
        else:
            for b in ("B3", "B4", "B5"):
                m = re.findall(r"(?im)^.*\b%s\b.*\b(PASS|FAIL)\b.*" % b, v)
                row[b] = m[-1] if m else "not found"
            row["raw"] = v.strip()
        vb[arm] = row

    # ---- KB-4: re-derive SELF choice
    kb4_lines, kb4_pass = [], None
    sd = arms.get("SELF", {}).get("scheme")
    if sd is None:
        kb4_lines.append("SELF scheme.txt MISSING -> KB-4 FAIL")
        kb4_pass = False
    else:
        ok = True
        for dom, rec in sorted(sd.items()):
            if not rec or not rec["scores"]:
                kb4_lines.append("%s: no scores recorded -> cannot re-derive" % dom)
                ok = False
                continue
            der = rederive(rec["scores"])
            match = (der == rec["chosen"])
            ok = ok and match
            kb4_lines.append("%s: recorded=%s re-derived=%s scores=%s -> %s" % (
                dom, rec["chosen"], der,
                " ".join("%s:%.4f" % (s, rec["scores"].get(s, float("nan"))) for s in SCHEMES),
                "MATCH" if match else "MISMATCH"))
            if rec["rationale"]:
                kb4_lines.append("  rationale: %s" % rec["rationale"])
        kb4_pass = ok

    # ---- KB-1, KB-5
    kb1 = kb5 = None
    kb_lines = []
    if "SELF" in b1 and "IMPOSED" in b1:
        s_o, i_o = b1["SELF"]["overall"], b1["IMPOSED"]["overall"]
        kb1 = s_o >= i_o - KB1_TOL
        kb_lines.append("KB-1 non-inferiority: SELF %.4f >= IMPOSED %.4f - %.2f -> %s"
                        % (s_o, i_o, KB1_TOL, "PASS" if kb1 else "FAIL"))
        deltas = {c: b1["SELF"][c] - b1["IMPOSED"][c] for c in CLASSES + ["overall"]}
        wins = [c for c in CLASSES if deltas[c] >= KB5_NOTE]
        losses = [c for c in CLASSES if deltas[c] <= -KB5_NOTE]
        kb_lines.append("KB-5 deltas SELF-IMPOSED: " +
                        ", ".join("%s %+.4f" % (c, deltas[c]) for c in CLASSES + ["overall"]))
        kb_lines.append("KB-5: SELF wins>=0.03: %s; loses>=0.03: %s (REPORTED, not a kill)"
                        % (wins or "none", losses or "none"))
    kb2 = all(vb.get(arm, {}).get("B4") == "PASS" for arm in ARMS if arm in arms) and \
        all(arm in arms for arm in ARMS)
    kb3 = all(vb.get(arm, {}).get("B3") == "PASS" for arm in ARMS if arm in arms) and \
        all(arm in arms for arm in ARMS)

    # ---- write SCORES.md
    L = []
    L.append("# MORG SCORES")
    L.append("")
    L.append("Fixtures (sha256): " + ", ".join("%s=%s" % (k, v[:12]) for k, v in fix_sha.items()))
    for n in notes:
        L.append("")
        L.append("NOTE: " + n)
    L.append("")
    L.append("Test queries: %d (PURE %d, SUBJ %d, AMBIG %d). Holdout queries: %d." % (
        len(test_q), len(test_by_class["PURE"]), len(test_by_class["SUBJ"]),
        len(test_by_class["AMBIG"]), len(hq)))
    L.append("")
    L.append("## B1 retrieval macro F1 (test queries, top-20)")
    L.append("")
    L.append("| arm | PURE | SUBJ | AMBIG | overall |")
    L.append("|---|---|---|---|---|")
    for arm in ARMS:
        if arm in b1:
            p = b1[arm]
            L.append("| %s | %.4f | %.4f | %.4f | %.4f |" % (
                arm, p["PURE"], p["SUBJ"], p["AMBIG"], p["overall"]))
        else:
            L.append("| %s | MISSING | MISSING | MISSING | MISSING |" % arm)
    L.append("")
    L.append("## B2 interference (test PURE queries, top-10)")
    L.append("")
    L.append("| arm | type-pure: frac wrong type | domain-pure: frac wrong domain | n |")
    L.append("|---|---|---|---|")
    for arm in ARMS:
        if arm in b2:
            e = b2[arm]
            L.append("| %s | %s | %s | %d/%d |" % (
                arm,
                "%.4f" % e["type_pure_wrong_type"] if e["type_pure_wrong_type"] is not None else "n/a",
                "%.4f" % e["domain_pure_wrong_domain"] if e["domain_pure_wrong_domain"] is not None else "n/a",
                e["n_type"], e["n_dom"]))
        else:
            L.append("| %s | MISSING | MISSING | - |" % arm)
    L.append("")
    L.append("## B7 holdout F1 (astronomy queries, top-20)")
    L.append("")
    L.append("| arm | PURE | SUBJ | AMBIG | overall |")
    L.append("|---|---|---|---|---|")
    for arm in ARMS:
        if arm in b7:
            p = b7[arm]
            L.append("| %s | %.4f | %.4f | %.4f | %.4f |" % (
                arm, p["PURE"], p["SUBJ"], p["AMBIG"], p["overall"]))
        else:
            L.append("| %s | MISSING | MISSING | MISSING | MISSING |" % arm)
    L.append("")
    L.append("## B6 drift (scheme t0 vs t1; holdout F1 under old vs new scheme)")
    L.append("")
    L.append("| arm | scheme t0 | scheme t1 | changed | F1 old | F1 new | delta | outcome |")
    L.append("|---|---|---|---|---|---|---|---|")
    for arm in ARMS:
        if arm in b6:
            e = b6[arm]
            L.append("| %s | %s | %s | %s | %.4f | %.4f | %+.4f | %s |" % (
                arm, e["t0"], e["t1"], e["changed"], e["f_old"], e["f_new"],
                e["delta"], e["outcome"]))
        else:
            L.append("| %s | MISSING |" % arm)
    L.append("")
    L.append("## B3/B4/B5 evidence (from verify_report.txt)")
    L.append("")
    L.append("| arm | B3 revision locality | B4 separability | B5 reorg cost |")
    L.append("|---|---|---|---|")
    for arm in ARMS:
        r = vb.get(arm, {})
        L.append("| %s | %s | %s | %s |" % (arm, r.get("B3", "MISSING"),
                                           r.get("B4", "MISSING"), r.get("B5", "MISSING")))
    L.append("")
    for arm in ARMS:
        if arms.get(arm, {}).get("ops"):
            L.append("ops.txt [%s]:" % arm)
            L.append("```")
            L.append(arms[arm]["ops"].strip())
            L.append("```")
            L.append("")
    L.append("## Kill bars")
    L.append("")
    for ln in kb_lines:
        L.append("- " + ln)
    L.append("- KB-2 separability (ALL arms B4 PASS): %s" % ("PASS" if kb2 else "FAIL"))
    L.append("- KB-3 revision locality (ALL arms B3 zero collateral): %s" % ("PASS" if kb3 else "FAIL"))
    L.append("- KB-4 consciousness (scorer re-derives SELF argmax under frozen tie-break): %s"
             % ("PASS" if kb4_pass else "FAIL"))
    for ln in kb4_lines:
        L.append("  - " + ln)
    L.append("")
    L.append("## Cross-arm deltas")
    L.append("")
    if "SELF" in b1 and "IMPOSED" in b1 and "FLAT" in b1:
        L.append("- SELF - IMPOSED overall: %+.4f" % (b1["SELF"]["overall"] - b1["IMPOSED"]["overall"]))
        L.append("- SELF - FLAT overall: %+.4f" % (b1["SELF"]["overall"] - b1["FLAT"]["overall"]))
        L.append("- IMPOSED - FLAT overall: %+.4f" % (b1["IMPOSED"]["overall"] - b1["FLAT"]["overall"]))
    else:
        L.append("- insufficient arms present")
    L.append("")
    L.append("## SELF per-domain scheme choices")
    L.append("")
    if sd:
        for dom, rec in sorted(sd.items()):
            L.append("- %s: %s" % (dom, rec["chosen"] if rec else "?"))
    else:
        L.append("- MISSING")
    L.append("")
    L.append("## Failure-mode pointers (sol's list, checked against evidence; pointers, not verdicts)")
    L.append("")
    L.append("- self-reinforcing misorganization: see B6 drift outcome + SELF scheme rationale above.")
    L.append("- popularity bias: see B2 interference (wrong-type/wrong-domain leakage into top-10).")
    L.append("- misleading cross-domain links: see B1 AMBIG vs PURE F1 gap per arm.")
    L.append("")
    with open(a.out, "w") as f:
        f.write("\n".join(L) + "\n")
    print("wrote %s" % a.out)
    print("KB-1:", kb1, "| KB-2:", kb2, "| KB-3:", kb3, "| KB-4:", kb4_pass)


if __name__ == "__main__":
    main()
