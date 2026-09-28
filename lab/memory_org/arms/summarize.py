#!/usr/bin/env python3
"""MORG battery scorer/summarizer (crew 2 independent check; crew-1 scorer.py
is the official scorer). Pure orchestration/arithmetic; all mechanisms live
in the Zag arm binaries. Reads results/<arm>/run<R>/ and emits summary.txt.
Usage: summarize.py FIXDIR RESDIR RUN"""
import sys, os, re

def parse_corpus(path):
    items = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            p = line.split("|", 4)
            if len(p) == 5:
                items[p[0]] = {"domain": p[1], "type": p[2], "subject": p[3], "text": p[4]}
    return items

def parse_queries(path, split=None):
    qs = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            p = line.split("|", 7)
            if len(p) == 8 and (split is None or p[1] == split):
                qs.append({"qid": p[0], "split": p[1], "class": p[2], "thint": p[3],
                           "dhint": p[4], "shint": p[5], "text": p[6],
                           "gold": [g for g in p[7].split(",") if g]})
    return qs

def parse_retrieval(path):
    ret = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            qid, _, ids = line.partition("|")
            ret[qid] = [i for i in ids.split(",") if i]
    return ret

def f1(ret_ids, gold):
    r = ret_ids[:20]
    g = set(gold)
    if not r or not g:
        return 0.0
    hit = len(set(r) & g)
    p = hit / len(r)
    rec = hit / len(g)
    return 2 * p * rec / (p + rec) if (p + rec) > 0 else 0.0

def score_queries(queries, ret):
    return {q["qid"]: (q["class"], f1(ret.get(q["qid"], []), q["gold"])) for q in queries}

def macro(per_q, cls=None):
    vals = [v[1] for k, v in per_q.items() if cls is None or v[0] == cls]
    return sum(vals) / len(vals) if vals else 0.0

def interference(queries, ret, corpus):
    type_pure = [q for q in queries if q["class"] == "PURE" and q["thint"]]
    dom_pure = [q for q in queries if q["class"] == "PURE" and not q["thint"] and q["dhint"]]
    wt = [sum(1 for i in ret.get(q["qid"], [])[:10]
              if corpus.get(i, {}).get("type") != q["thint"]) / len(ret.get(q["qid"], [])[:10])
          for q in type_pure if ret.get(q["qid"], [])[:10]]
    wd = [sum(1 for i in ret.get(q["qid"], [])[:10]
              if corpus.get(i, {}).get("domain") != q["dhint"]) / len(ret.get(q["qid"], [])[:10])
          for q in dom_pure if ret.get(q["qid"], [])[:10]]
    return (sum(wt) / len(wt) if wt else 0.0, sum(wd) / len(wd) if wd else 0.0,
            len(wt), len(wd))

LEVELS = {"S1": 3, "S2": 3, "S3": 2, "S4": 3, "S5": 3, "S6": 1}

def parse_scheme(path):
    """Parse crew-1 SCHEME_FORMAT.md contract. Returns dict domain ->
    {'chosen', 'scores', 'rationale'}; the global block is kept as '_global'."""
    if not os.path.exists(path):
        return None
    per = {}
    cur_dom = "_global"
    cur = {"chosen": None, "scores": {}, "rationale": ""}
    def flush():
        if cur["chosen"] or cur["scores"]:
            per[cur_dom] = dict(cur)
    for line in open(path):
        line = line.strip()
        m = re.match(r"(?i)^domain\s*[:=]\s*(\S+)", line)
        if m:
            flush()
            cur_dom = m.group(1).lower()
            cur = {"chosen": None, "scores": {}, "rationale": ""}
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
    return per or None

def rederive(scores):
    best = max(scores.values())
    cands = [s for s, v in scores.items() if v == best]
    cands.sort(key=lambda s: (LEVELS[s], int(s[1:])))
    return cands[0]

def main():
    fix, res, run = sys.argv[1], sys.argv[2], sys.argv[3]
    corpus = parse_corpus(os.path.join(fix, "corpus.txt"))
    corpus.update(parse_corpus(os.path.join(fix, "corpus_holdout.txt")))
    qtest = parse_queries(os.path.join(fix, "queries.txt"), "test")
    qhold = parse_queries(os.path.join(fix, "queries_holdout.txt"), "test")
    arms = ["SELF", "IMPOSED", "FLAT"]
    out = ["# MORG battery summary", "fixture: %s" % fix]
    per_arm = {}
    for arm in arms:
        adir = os.path.join(res, arm, "run" + run)
        ret = parse_retrieval(os.path.join(adir, "retrieval.txt"))
        pq = score_queries(qtest, ret)
        overall = macro(pq)
        by_class = {c: macro(pq, c) for c in ("PURE", "SUBJ", "AMBIG")}
        wt, wd, nt, ndm = interference(qtest, ret, corpus)
        rh = parse_retrieval(os.path.join(adir, "retrieval_holdout.txt"))
        hold_f1 = macro(score_queries(qhold, rh)) if qhold else 0.0
        hold_old = None
        if arm == "SELF" and os.path.exists(os.path.join(adir, "retrieval_holdout_old.txt")):
            rh_old = parse_retrieval(os.path.join(adir, "retrieval_holdout_old.txt"))
            hold_old = macro(score_queries(qhold, rh_old)) if qhold else 0.0
        ops = {}
        opp = os.path.join(adir, "ops.txt")
        if os.path.exists(opp):
            for line in open(opp):
                k, _, v = line.strip().partition("=")
                if k and v:
                    ops[k] = int(v)
        kb4ok, kb4msg = None, "n/a (SELF only)"
        if arm == "SELF":
            parsed = parse_scheme(os.path.join(adir, "scheme.txt"))
            if parsed is None:
                kb4ok, kb4msg = False, "scheme.txt missing/unparseable"
            else:
                doms = {d: r for d, r in parsed.items() if d != "_global"}
                bad = []
                for d, r in sorted(doms.items()):
                    if not r["scores"]:
                        bad.append("%s: no scores" % d)
                    elif rederive(r["scores"]) != r["chosen"]:
                        bad.append("%s: recorded %s vs rederived %s" % (
                            d, r["chosen"], rederive(r["scores"])))
                kb4ok = not bad
                kb4msg = ("rederived choice matches recorded (%d domains)" % len(doms)
                          if kb4ok else "; ".join(bad))
        per_arm[arm] = {"overall": overall, "class": by_class, "wt": wt, "wd": wd,
                        "nt": nt, "ndm": ndm, "hold": hold_f1, "hold_old": hold_old,
                        "ops": ops, "kb4": kb4ok, "kb4msg": kb4msg}
        out.append("== %s ==" % arm.upper())
        out.append("B1 test F1 overall=%.4f PURE=%.4f SUBJ=%.4f AMBIG=%.4f (n=%d)" % (
            overall, by_class["PURE"], by_class["SUBJ"], by_class["AMBIG"], len(pq)))
        out.append("B2 interference: wrong-type=%.4f (n=%d) wrong-domain=%.4f (n=%d)" % (
            wt, nt, wd, ndm))
        if hold_old is not None:
            out.append("B6 holdout F1: t0(old scheme)=%.4f t1(new scheme)=%.4f" % (hold_old, hold_f1))
        out.append("B7 holdout F1=%.4f (n=%d)" % (hold_f1, len(qhold)))
        out.append("B5 ops: reads=%s writes=%s moves=%s" % (
            ops.get("reads"), ops.get("writes"), ops.get("moves")))
        out.append("KB-4 scheme re-derivation: %s (%s)" % (kb4ok, kb4msg))
    s, im = per_arm["SELF"]["overall"], per_arm["IMPOSED"]["overall"]
    out.append("== KILL BARS ==")
    out.append("%s: KB-1 non-inferiority (SELF >= IMPOSED-0.02) -- SELF=%.4f IMPOSED=%.4f delta=%+.4f" % (
        "PASS" if s >= im - 0.02 else "FAIL", s, im, s - im))
    b4msg, b4ok = [], True
    for arm in arms:
        vr = os.path.join(res, arm, "run" + run, "verify_report.txt")
        txt = open(vr).read() if os.path.exists(vr) else ""
        m = re.findall(r"(?im)^.*\bB4\b.*\b(PASS|FAIL)\b.*", txt)
        ok = (m[-1] == "PASS") if m else False
        b4ok = b4ok and ok
        b4msg.append("%s=%s" % (arm, m[-1] if m else "not found"))
    out.append("%s: KB-2 separability (B4 byte-identical, all arms) -- %s" % (
        "PASS" if b4ok else "FAIL", "; ".join(b4msg)))
    b3msg, b3ok = [], True
    for arm in arms:
        vr = os.path.join(res, arm, "run" + run, "verify_report.txt")
        txt = open(vr).read() if os.path.exists(vr) else ""
        m = re.findall(r"(?im)^.*\bB3\b.*\b(PASS|FAIL)\b.*", txt)
        ok = (m[-1] == "PASS") if m else False
        b3ok = b3ok and ok
        b3msg.append("%s=%s" % (arm, m[-1] if m else "not found"))
    out.append("%s: KB-3 revision locality (zero collateral, all arms) -- %s" % (
        "PASS" if b3ok else "FAIL", "; ".join(b3msg)))
    kb4 = per_arm["SELF"]["kb4"]
    out.append("%s: KB-4 consciousness (scheme re-derivation) -- %s" % (
        "PASS" if kb4 else "FAIL", per_arm["SELF"]["kb4msg"]))
    kb5 = []
    for c in ("PURE", "SUBJ", "AMBIG"):
        d = per_arm["SELF"]["class"][c] - per_arm["IMPOSED"]["class"][c]
        tag = ""
        if d >= 0.03:
            tag = " <-- SELF wins >=0.03"
        if d <= -0.03:
            tag = " <-- SELF loses >=0.03"
        kb5.append("%s: SELF-IMPOSED=%+.4f%s" % (c, d, tag))
    out.append("REPORT: KB-5 superiority probe -- %s" % "; ".join(kb5))
    out.append("== FLAT vs organized ==")
    for c in ("PURE", "SUBJ", "AMBIG"):
        out.append("%s: SELF-FLAT=%+.4f IMPOSED-FLAT=%+.4f" % (
            c, per_arm["SELF"]["class"][c] - per_arm["FLAT"]["class"][c],
            per_arm["IMPOSED"]["class"][c] - per_arm["FLAT"]["class"][c]))
    out.append("== B8 scheme report (SELF) ==")
    for tag, fn in (("t0", "scheme_t0.txt"), ("t1", "scheme_t1.txt")):
        sp = os.path.join(res, "SELF", "run" + run, fn)
        parsed = parse_scheme(sp)
        if parsed:
            doms = {d: r for d, r in parsed.items() if d != "_global"}
            g = parsed.get("_global", {})
            out.append("%s global=%s domains={%s}" % (
                tag, g.get("chosen"),
                ", ".join("%s:%s" % (d, r["chosen"]) for d, r in sorted(doms.items()))))
            for d, r in sorted(doms.items()):
                if r["rationale"]:
                    out.append("  rationale %s %s: %s" % (tag, d, r["rationale"]))
    for arm in arms:
        open(os.path.join(res, arm, "run" + run, "summary.txt"), "w").write(
            "\n".join(out) + "\n")
    print("\n".join(out))

if __name__ == "__main__":
    main()
