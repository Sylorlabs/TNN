#!/usr/bin/env python3
"""verify_mw_round3.py — independent oracle for round 3 (reliability sweep).

Written fresh from PREREG-MW-R3 (frozen 2026-09-22). Imports ONLY the
envelope DATA from gen_mw_round3 (rows, questions, stipulated golds,
levels, latent truths) — never its mechanism functions. Reimplements
separately: derive_b (frozen PREREG s4), the loose rule (PREREG-MW-D D1),
the conservative rule (PREREG-MW-C M1: cond4 = corrob OR unique, with the
equally-new-contradiction veto applying ONLY when no corroboration exists —
faithful to the frozen mw_sense_c.zag; see AMENDMENT-A3), the citation
builders, the hash-chained ledger-head recomputation, the r-hat
self-estimators, and every analysis in PREREG-MW-R3 sections R2 (value
table, crossover, licensed curve, sensitivity, D-vs-C delta), R3 (gate
analysis), R4 (S8 fiat cost for arms D and C).

Checks against authority/round3/evidence/:
  KB-R3-DET, KB-R3-ORACLE, KB-R3-MIX, KB-R3-CONS (A3-corrected), KB-R3-SHAPE,
  KB-R3-U-SHAPE, KB-R3-U-ORACLE, KB-R3-U-VALUE.
Covers all 420 envelopes (Blocks R/U/G/G2/S) x 3 arms x 5 runs.
"""
import hashlib
import os
import re
import sys

BASE = os.path.expanduser("~/workspace/tnn-lab/mixed-web")
R3 = os.path.join(BASE, "authority", "round3")
EV = os.path.join(R3, "evidence")
sys.path.insert(0, os.path.join(R3, "gen"))
from gen_mw_round3 import ENVELOPES, LEVELS  # DATA ONLY, not mechanism code

VALID_RULES = {"MAJORITY", "RECENCY", "CORROB", "TIE", "INSUFFICIENT",
               "STALE_CONFLICT", "PRIMARY", "PRIMARY_L"}


def lab(dom):
    d = dom.lower()
    if d[:4] == "www.":
        d = d[4:]
    return d.split(".")[0]


def table_rows(rows):
    """Replicate the binary's feed-time dedup on (domain, answer): first wins."""
    seen, out = set(), []
    for d, a, r in rows:
        if (d, a) not in seen:
            seen.add((d, a))
            out.append((d, a, r))
    return out


def primary_dom(question, res):
    """Binary mw_primary_dom: the unique distinct domain whose label-token
    occurs as a full [a-z] token in the lowercased question; else ''."""
    q = question.lower()
    found, cnt, seen = "", 0, set()
    for d, _a, _r in res:
        if d in seen:
            continue
        seen.add(d)
        if tok_in_q(q, lab(d)):
            cnt += 1
            found = d
    return found if cnt == 1 else ""


def tok_in_q(q, tok):
    # binary mw_tok_in_q/mw_tok_at: tok (len>=4) occurs as a full [a-z] token
    if len(tok) < 4:
        return False
    L = len(tok)
    i = 0
    while i < len(q):
        if i + L <= len(q) and q[i:i + L] == tok:
            left_ok = (i == 0) or not ('a' <= q[i - 1] <= 'z')
            right_ok = (i + L == len(q)) or not ('a' <= q[i + L] <= 'z')
            if left_ok and right_ok:
                return True
        i += 1
    return False


def derive_b(temporal, results):
    """Frozen PREREG section 4 deliberation (arm B), reimplemented."""
    order, data = [], {}
    seen_pairs = set()
    for d, a, r in results:
        k = (d, a)
        if k in seen_pairs:
            continue
        seen_pairs.add(k)
        if a not in data:
            data[a] = {"doms": set(), "rec": 0}
            order.append(a)
        data[a]["doms"].add(d)
        data[a]["rec"] = max(data[a]["rec"], r)
    cands = [(a, len(data[a]["doms"]), data[a]["rec"]) for a in order]
    if not cands:
        return ("WITHHOLD", "", "INSUFFICIENT", cands)
    bi, bc = 0, cands[0][1]
    rc = 0
    for i in range(1, len(cands)):
        n = cands[i][1]
        if n > bc:
            rc, bc, bi = bc, n, i
        elif i != bi and n > rc:
            rc = n
    tot = len({d for d, _a, _r in results})
    if temporal == 1:
        ni, nr, sr = 0, cands[0][2], 0
        for i in range(1, len(cands)):
            r = cands[i][2]
            if r > nr:
                sr, nr, ni = nr, r, i
            elif i != ni and r > sr:
                sr = r
        nn = cands[ni][1]
        if nr >= 2000 and nn >= 2 and nr - sr >= 3:
            na, ba = cands[ni][0], cands[bi][0]
            if na == ba:
                return ("CONVERGE", na, "RECENCY", cands)
            if bc >= 2 * nn:
                return ("WITHHOLD", "", "STALE_CONFLICT", cands)
            return ("CONVERGE", na, "RECENCY", cands)
    if bc >= 3 and bc >= 2 * rc:
        return ("CONVERGE", cands[bi][0], "MAJORITY", cands)
    if bc >= 2 and tot <= 4 and rc <= 1:
        return ("CONVERGE", cands[bi][0], "CORROB", cands)
    return ("WITHHOLD", "", "TIE" if rc >= 1 else "INSUFFICIENT", cands)


def loose_oracle(question, results):
    """PREREG-MW-D D1 PRIMARY_LOOSE (no condition-4 veto)."""
    qtokens = {t for t in re.split("[^a-z]", question.lower()) if len(t) >= 4}
    seen, primaries = set(), []
    for d, _a, _r in results:
        if d in seen:
            continue
        seen.add(d)
        if lab(d) in qtokens:
            primaries.append(d)
    if len(primaries) != 1:
        return (False, "", "")
    D = primaries[0]
    own = [(a, r) for d, a, r in results if d == D and a]
    if not own:
        return (False, "", "")
    rp = max(r for _a, r in own)
    A = next(a for a, r in own if r == rp)
    if rp < 2000:
        return (False, "", "")
    if rp != max(r for _d, _a, r in results):
        return (False, "", "")
    if any(d != D and a == A for d, a, _r in results):
        return (True, A, "loose-corrob")
    return (True, A, "loose-unique")


def cons_oracle(question, results):
    """PREREG-MW-C M1 conservative PRIMARY, faithful to the frozen binary
    (mw_sense_c.zag mw_primary_cond4 + mw_deliberate_c): cond4 is the
    disjunction  corrob OR unique  where
      corrob = some OTHER domain asserts the primary's newest answer
               (no recency filter; checked FIRST — takes precedence), else
      veto   = some other domain asserts a DIFFERENT answer at max recency
               (fires only when there is NO corroboration), else
      unique = no equally-new contradiction.
    The equally-new-contradiction veto does NOT apply when corroboration
    exists. Includes the no-override guard (frozen B must withhold).
    Returns (fired, answer, basis, binary-format citation)."""
    res = table_rows(results)
    dom = primary_dom(question, res)
    if not dom:
        return (False, "", "", "")
    rp = max((r for d, a, r in res if d == dom and a), default=-1)
    if rp < 2000:
        return (False, "", "", "")
    seen_a, cands = set(), []
    for d, a, r in res:
        if a and a not in seen_a:
            seen_a.add(a)
            cands.append(a)
    g = max(max(r for d, a, r in res if a == ca) for ca in cands)
    if rp != g:
        return (False, "", "", "")
    A = next((a for d, a, r in res if d == dom and r == rp and a), "")
    if not A:
        return (False, "", "", "")
    if any(d != dom and a == A for d, a, _r in res):
        basis = "corrob"
    elif any(d != dom and r == g and a and a != A for d, a, r in res):
        return (False, "", "", "")
    else:
        basis = "unique"
    bv, _bch, _brule, _ctab = derive_b(1, res)
    if bv == "CONVERGE":
        return (False, "", "", "")
    return (True, A, basis, cite_oracle(res, dom, A, rp, basis))


def cite_oracle(results, dom, ans, rec, basis):
    """PRIMARY_L citation, mirroring mw_primary_cite incl. feed dedup."""
    deduped, seen_pairs = [], set()
    for d, a, r in results:
        k = (d, a)
        if k in seen_pairs:
            continue
        seen_pairs.add(k)
        deduped.append((d, a, r))
    parts, skipped = [], False
    for d, a, r in deduped:
        if d != dom or not a:
            continue
        if not skipped and r == rec:
            skipped = True
            continue
        parts.append(f"{a}@{r}")
    sup = ",".join(parts) if parts else "-"
    return f"primary={dom} newest={ans}@{rec} superseded={sup} cond4={basis}"


def cons_cite_oracle(results, dom, ans, rec, basis):
    return cite_oracle(results, dom, ans, rec, basis)


def primary_dom_of(question, results):
    qtokens = {t for t in re.split("[^a-z]", question.lower()) if len(t) >= 4}
    seen, prims = set(), []
    for d, _a, _r in results:
        if d in seen:
            continue
        seen.add(d)
        if lab(d) in qtokens:
            prims.append(d)
    return prims[0] if len(prims) == 1 else ""


def head_recompute(qid, question, results, entries):
    prev = b"\x00" * 32
    seq = 0
    ops = [(66, qid, question, qid, qid)]
    for d, a, r in results:
        ops.append((82, qid, d, a, str(r) if r > 0 else ""))
    ops.extend(entries)
    for op, f1, f2, f3, f4 in ops:
        e = (prev + seq.to_bytes(8, "little") + bytes([op, 0]) +
             f1.encode() + b"\x00" + f2.encode() + b"\x00" +
             f3.encode() + b"\x00" + f4.encode())
        prev = hashlib.sha256(e).digest()
        seq += 1
    return prev.hex()


def supp_expected(results, chosen):
    if not chosen:
        return ""
    seen, out = set(), []
    for d, a, _r in results:
        if a == chosen and d not in seen:
            seen.add(d)
            out.append(d)
            if len(out) == 3:
                break
    return ",".join(out)


# ---- R3 self-estimators (dispute-internal only) ----
def rhat_max(question, results):
    D = primary_dom_of(question, results)
    pa = next(a for d, a, r in results if d == D and a
              and r == max(r2 for d2, a2, r2 in results if d2 == D and a2))
    gmax = max(r for _d, _a, r in results)
    doms = sorted({d for d, _a, r in results if r == gmax})
    num = sum(1 for d in doms if d != D and
              any(d2 == d and a2 == pa and r2 == gmax
                  for d2, a2, r2 in results))
    return num / len(doms) if doms else 0.0


def rhat_all(question, results):
    D = primary_dom_of(question, results)
    pa = next(a for d, a, r in results if d == D and a
              and r == max(r2 for d2, a2, r2 in results if d2 == D and a2))
    doms = sorted({d for d, _a, _r in results})
    newest = {}
    for d in doms:
        own = [(a, r) for d2, a, r in results if d2 == d and a]
        newest[d] = max(own, key=lambda x: x[1])[0] if own else ""
    num = sum(1 for d in doms if newest[d] == pa)
    return num / len(doms) if doms else 0.0


def main():
    fails = []
    oracle = {}
    for e in ENVELOPES:
        qid, q, rows = e["qid"], e["question"], e["rows"]
        bv, bch, brule, ctab = derive_b(1, rows)
        pf, pa, basis = loose_oracle(q, rows)
        if pf and bv == "CONVERGE":
            dexp = (bv, bch, brule)      # no-override guard
        elif pf:
            dexp = ("CONVERGE", pa, "PRIMARY_L")
        else:
            dexp = (bv, bch, brule)
        cf, ca, cbasis, ccite = cons_oracle(q, rows)
        if cf and bv == "CONVERGE":
            cexp = (bv, bch, brule)
        elif cf:
            cexp = ("CONVERGE", ca, "PRIMARY")
        else:
            cexp = (bv, bch, brule)
        oracle[qid] = {"e": e, "b": (bv, bch, brule), "dexp": dexp,
                       "cexp": cexp, "pf": pf, "pa": pa, "basis": basis,
                       "cf": cf, "ca": ca, "cbasis": cbasis, "ccite": ccite,
                       "ctab": ctab, "res": [(d, a, r) for d, a, r in rows]}

    # KB-R3-SHAPE: arm B withholds on all 420 (shape validity for D1's
    # no-override guard and C's no-override guard)
    for qid, o in oracle.items():
        if o["b"][0] != "WITHHOLD":
            fails.append(f"KB-R3-SHAPE: {qid} arm-B would {o['b']} — not a dispute/tie shape")

    # KB-R3-MIX: level mixes and Bresenham interleave positions
    for r in LEVELS:
        n_a = round(20 * r)
        got = [e for e in ENVELOPES if e["block"] == "R" and e["level"] == r]
        if len(got) != 20:
            fails.append(f"KB-R3-MIX: level {r} has {len(got)} envelopes, want 20")
        na = sum(1 for e in got if e["twin"] == "S1A")
        if na != n_a:
            fails.append(f"KB-R3-MIX: level {r} S1A={na}, prereg n_A={n_a}")
        for i, e in enumerate(got):
            want_a = (i * n_a) % 20 < n_a
            if (e["twin"] == "S1A") != want_a:
                fails.append(f"KB-R3-MIX: level {r} envelope {i} twin={e['twin']} "
                             f"violates Bresenham placement")
    g = [e for e in ENVELOPES if e["block"] == "G"]
    if len(g) != 20 or sum(1 for e in g if e["twin"] == "S1A") != 10:
        fails.append("KB-R3-MIX: Block G is not 20 envelopes at 50/50")
    g2 = [e for e in ENVELOPES if e["block"] == "G2"]
    if len(g2) != 20 or sum(1 for e in g2 if e["twin"] == "S1A") != 10:
        fails.append("KB-R3-MIX: Block G2 is not 20 envelopes at 50/50")
    for e in g2:
        if e["level"] is not None or e["twin"] not in ("S1A", "S1B"):
            fails.append(f"KB-R3-MIX: Block G2 envelope {e['qid']} malformed")
            break
    s = [e for e in ENVELOPES if e["block"] == "S"]
    if len(s) != 20:
        fails.append("KB-R3-MIX: Block S is not 20 envelopes")
    # Block U: 9 levels x 20, Bresenham interleave identical to Block R
    for r in LEVELS:
        n_a = round(20 * r)
        got = [e for e in ENVELOPES if e["block"] == "U" and e["level"] == r]
        if len(got) != 20:
            fails.append(f"KB-R3-MIX: Block U level {r} has {len(got)} envelopes, want 20")
        na = sum(1 for e in got if e["twin"] == "S1A")
        if na != n_a:
            fails.append(f"KB-R3-MIX: Block U level {r} S1A={na}, prereg n_A={n_a}")
        for i, e in enumerate(got):
            want_a = (i * n_a) % 20 < n_a
            if (e["twin"] == "S1A") != want_a:
                fails.append(f"KB-R3-MIX: Block U level {r} envelope {i} twin={e['twin']} "
                             f"violates Bresenham placement")
    # manifest cross-check
    man = open(os.path.join(R3, "manifest_r3.txt")).read()
    for e in ENVELOPES:
        needle = f"{e['qid']}: block={e['block']} level={e['level']} twin={e['twin']}"
        if needle not in man:
            fails.append(f"KB-R3-MIX: manifest missing/mismatched for {e['qid']}")

    # ---- evidence logs ----
    arm_logs = {}
    for arm in ("B", "C", "D"):
        logs = [open(os.path.join(EV, f"mw_r3{arm.lower()}_r{i}.log")).read()
                for i in range(5)]
        if not all(l == logs[0] for l in logs):
            fails.append(f"KB-R3-DET: arm {arm} logs differ across 5 runs")
        if f"{arm}|ALL_CHECKS_PASS" not in logs[0]:
            fails.append(f"arm {arm}: trial self-checks did not all pass")
        vlines = {}
        for line in logs[0].splitlines():
            if line.startswith(f"V|{arm}|"):
                p = line.split("|")
                vlines[p[2]] = {"verdict": p[3], "chosen": p[4], "rule": p[5],
                                "chain": "|".join(p[6:-2]), "supp": p[-2],
                                "head": p[-1]}
        arm_logs[arm] = vlines

    # KB-R3-ORACLE: every cell
    for qid, o in oracle.items():
        e, res, ctab = o["e"], o["res"], o["ctab"]
        bv, bch, brule = o["b"]
        echain = "|".join(f"{a},{n},{r}" for a, n, r in ctab)
        for arm, expkey, rulecode in (("B", "b", None),
                                      ("C", "cexp", "PRIMARY"),
                                      ("D", "dexp", "PRIMARY_L")):
            ev, ech, erule = o[expkey]
            vlines = arm_logs[arm]
            if qid not in vlines:
                fails.append(f"arm {arm}: missing V-line for {qid}")
                continue
            c = vlines[qid]
            if erule == "PRIMARY_L":
                D = primary_dom_of(e["question"], res)
                rp = max(r for d, a, r in res if d == D and a)
                esupp = cite_oracle(res, D, ech, rp, o["basis"])
                entries = [(68, "PRIMARY_L", ech, echain, esupp),
                           (70, qid, "PRIMARY_L", ech, qid)]
            elif erule == "PRIMARY":
                esupp = o["ccite"]  # binary-format citation from the oracle
                entries = [(68, "PRIMARY", ech, echain, esupp),
                           (70, qid, "PRIMARY", ech, qid)]
            else:
                esupp = supp_expected(res, ech)
                entries = [(68, erule, ech, echain, esupp),
                           (70, qid, erule, ech, qid)]
            hgot = head_recompute(qid, e["question"], res, entries)
            if hgot != c["head"]:
                fails.append(f"KB-R3-ORACLE: {arm} {qid} head mismatch")
            if c["supp"] != esupp:
                fails.append(f"KB-R3-ORACLE: {arm} {qid} supp {c['supp']!r} != {esupp!r}")
            if (c["verdict"], c["chosen"], c["rule"]) != (ev, ech, erule):
                fails.append(f"arm {arm}: {qid} got ({c['verdict']},{c['chosen']},{c['rule']}) "
                             f"oracle=({ev},{ech},{erule})")
            if c["rule"] not in VALID_RULES:
                fails.append(f"KB-R3-ORACLE: {arm} {qid} invalid rule {c['rule']}")
            else:
                try:
                    chain = {a2: (int(n2), int(r2))
                             for a2, n2, r2 in (it.split(",") for it in c["chain"].split("|"))}
                except Exception:
                    chain = None
                    fails.append(f"KB-R3-ORACLE: {arm} {qid} unparsable chain")
                if chain is not None and chain != {a: (n, r) for a, n, r in ctab}:
                    fails.append(f"KB-R3-ORACLE: {arm} {qid} chain != oracle")
                if ev == "CONVERGE" and not c["supp"]:
                    fails.append(f"KB-R3-ORACLE: {arm} {qid} converge without citation")
                if ev == "WITHHOLD" and c["chosen"]:
                    fails.append(f"KB-R3-ORACLE: {arm} {qid} withhold with chosen set")
            # NONREG: authority may only convert withholds
            fired = (rulecode is not None and c["rule"] == rulecode)
            if not fired and (c["verdict"], c["chosen"], c["rule"]) != (bv, bch, brule):
                fails.append(f"KB-R3-NONREG-{arm}: {qid} != B without authority firing")
            if fired and bv != "WITHHOLD":
                fails.append(f"KB-R3-NONREG-{arm}: {qid} authority fired where B converged")

    # KB-R3-CONS (corrected per AMENDMENT-A3): the prereg's withhold-everywhere
    # expectation was wrong — the frozen M1 corrob disjunct fires on the
    # corroborated dispute/tie shapes. The bar is oracle parity (checked in
    # KB-R3-ORACLE above); here we REPORT arm C's measured behavior.
    nconv_c = sum(1 for c in arm_logs["C"].values() if c["verdict"] == "CONVERGE")
    print(f"arm C measured: {nconv_c}/420 CONVERGE "
          f"(frozen-M1 corrob disjunct on R/G/S; veto on U/G2; every cell oracle-explained)")

    # ---- R2 value table ----
    print("=== reliability x value (Block R, arm D vs conservative) ===")
    e_r = {}
    for r in LEVELS:
        tot = 0
        for e in ENVELOPES:
            if e["block"] != "R" or e["level"] != r:
                continue
            c = arm_logs["D"][e["qid"]]
            if c["verdict"] == "CONVERGE":
                tot += 1 if c["chosen"] == e["stip_gold"] else -1
        e_r[r] = tot / 20
        n_a = round(20 * r)
        pred = (n_a - (20 - n_a)) / 20
        match = "MATCH" if abs(e_r[r] - pred) < 1e-9 else "DEVIATION"
        print(f"level {r:.2f}: n_A={n_a:2d} n_B={20 - n_a:2d} "
              f"measured E={e_r[r]:+.2f} predicted={pred:+.2f} {match}")
    # crossover: linear interpolation across E=0
    below = max(r for r in LEVELS if e_r[r] < 0)
    above = min(r for r in LEVELS if e_r[r] >= 0)
    eb, ea = e_r[below], e_r[above]
    rstar = below + (0 - eb) * (above - below) / (ea - eb) if ea != eb else above
    print(f"crossover: measured r*={rstar:.4f} (interp {below}->{above}); analytic 2r-1=0 -> 0.50")
    print("--- sensitivity: crossover r*(k) for false-install cost k ---")
    for k in (1, 2, 3, 5):
        print(f"  k={k}: r*={k / (1 + k):.4f}")
    print("--- licensed-value curve: gate 'fire only if rel_ind >= t' ---")
    for t in (0.50, 0.60, 0.70, 0.80, 0.90, 0.95):
        lv = sum(e_r[r] for r in LEVELS if r >= t) / sum(1 for r in LEVELS if r >= t)
        print(f"  t={t:.2f}: licensed EV={lv:+.3f}/case over levels >= {t}")
    print("--- D-minus-C value delta (loose minus conservative) per level ---")
    for r in LEVELS:
        d = 0
        for e in ENVELOPES:
            if e["block"] != "R" or e["level"] != r:
                continue
            cd, cc = arm_logs["D"][e["qid"]], arm_logs["C"][e["qid"]]
            vd = (1 if cd["chosen"] == e["stip_gold"] else -1) \
                if cd["verdict"] == "CONVERGE" else 0
            vc = (1 if cc["chosen"] == e["stip_gold"] else -1) \
                if cc["verdict"] == "CONVERGE" else 0
            d += vd - vc
        print(f"level {r:.2f}: delta={d / 20:+.2f}/case")

    # ---- Block U: the TRUE loose-vs-conservative margin (AMENDMENT-A3) ----
    # Here arm C withholds (veto) and arm D converges, so D-vs-C = D's value.
    print("=== Block U: reliability x value (loose D vs conservative C) ===")
    eu_r, eu_c = {}, {}
    u_ok = True
    for r in LEVELS:
        td = tc = 0
        for e in ENVELOPES:
            if e["block"] != "U" or e["level"] != r:
                continue
            cd, cc = arm_logs["D"][e["qid"]], arm_logs["C"][e["qid"]]
            if cd["verdict"] == "CONVERGE":
                td += 1 if cd["chosen"] == e["stip_gold"] else -1
            if cc["verdict"] == "CONVERGE":
                tc += 1 if cc["chosen"] == e["stip_gold"] else -1
        eu_r[r] = td / 20
        eu_c[r] = tc / 20
        n_a = round(20 * r)
        pred = (n_a - (20 - n_a)) / 20
        match = "MATCH" if abs(eu_r[r] - pred) < 1e-9 else "DEVIATION"
        cmatch = "C=0" if abs(eu_c[r]) < 1e-9 else "C!=0 DEVIATION"
        if match != "MATCH" or cmatch != "C=0":
            u_ok = False
        print(f"level {r:.2f}: n_A={n_a:2d} D-vs-C E={eu_r[r] - eu_c[r]:+.2f} "
              f"predicted={pred:+.2f} {match} [{cmatch}]")
    if not u_ok:
        fails.append("KB-R3-U-VALUE: Block U value deviates from 2r-1 or C!=0")
    below = max(r for r in LEVELS if eu_r[r] - eu_c[r] < 0)
    above = min(r for r in LEVELS if eu_r[r] - eu_c[r] >= 0)
    eb, ea = eu_r[below] - eu_c[below], eu_r[above] - eu_c[above]
    rstar = below + (0 - eb) * (above - below) / (ea - eb) if ea != eb else above
    print(f"Block U crossover: measured r*={rstar:.4f} (interp {below}->{above}); "
          f"predicted 0.50")
    if abs(rstar - 0.50) > 0.025:
        fails.append(f"KB-R3-U-VALUE: Block U crossover r*={rstar:.4f} != 0.50")
    print("--- Block U sensitivity: crossover r*(k) for false-install cost k ---")
    for k in (1, 2, 3, 5):
        print(f"  k={k}: r*={k / (1 + k):.4f}")
    print("--- Block U licensed-value curve: fire only if rel_ind >= t ---")
    for t in (0.50, 0.60, 0.70, 0.80, 0.90, 0.95):
        lv = sum(eu_r[r] - eu_c[r] for r in LEVELS if r >= t) / \
            sum(1 for r in LEVELS if r >= t)
        print(f"  t={t:.2f}: licensed EV={lv:+.3f}/case over levels >= {t}")

    # ---- R3 self-estimation stress ----
    print("=== Block G: self-estimation stress ===")
    twin_id_ok = True
    rows_g = []
    for e in ENVELOPES:
        if e["block"] != "G":
            continue
        rm, ra = rhat_max(e["question"], e["rows"]), rhat_all(e["question"], e["rows"])
        rows_g.append((e["qid"], e["twin"], e["stip_gold"], rm, ra))
    # twin-identity: group envelopes by identical rows; r-hat must be
    # CONSTANT within each group (any dispute-internal estimator is
    # twin-identical by construction — rows carry no twin information).
    # Group sizes vary (period-6 name rotation vs 20-envelope levels) and
    # twin composition varies (level 0.99 is all-S1A); constancy is the
    # load-bearing property: the gate then admits all or none of a group.
    by_rows = {}
    for qid, twin, _g, rm, ra in rows_g:
        key = repr(next(o for o in ENVELOPES if o["qid"] == qid)["rows"])
        by_rows.setdefault(key, []).append((qid, twin, rm, ra))
    for key, grp in by_rows.items():
        rms = {round(x[2], 9) for x in grp}
        ras = {round(x[3], 9) for x in grp}
        if len(rms) != 1 or len(ras) != 1:
            twin_id_ok = False
    print(f"twin-identity (r-hat constant across every identical-rows group): {twin_id_ok}")
    if not twin_id_ok:
        fails.append("KB-R3-ORACLE: twin-identity of r-hat estimators failed")
    for est_i, est_name in ((3, "rhat_max"), (4, "rhat_all")):
        print(f"--- gate on {est_name} ---")
        for t in (0.30, 0.50, 0.70, 0.90):
            adm_a = adm_b = val = 0
            for qid, twin, gold, rm, ra in rows_g:
                rh = rm if est_i == 3 else ra
                if rh >= t:
                    c = arm_logs["D"][qid]
                    v = 0
                    if c["verdict"] == "CONVERGE":
                        v = 1 if c["chosen"] == gold else -1
                    val += v
                    if twin == "S1A":
                        adm_a += 1
                    else:
                        adm_b += 1
            n = adm_a + adm_b
            ev = val / n if n else 0.0
            print(f"  t={t:.2f}: admitted S1A={adm_a} S1B={adm_b} EV={ev:+.2f}/case")

    # ---- Block G2: self-estimation stress on the UNCORROBORATED (licensed) shape
    print("=== Block G2: self-estimation stress (uncorroborated shape) ===")
    twin_id_ok2 = True
    rows_g2 = []
    for e in ENVELOPES:
        if e["block"] != "G2":
            continue
        rm, ra = rhat_max(e["question"], e["rows"]), rhat_all(e["question"], e["rows"])
        rows_g2.append((e["qid"], e["twin"], e["stip_gold"], rm, ra))
    by_rows2 = {}
    for qid, twin, _g, rm, ra in rows_g2:
        key = repr(next(o for o in ENVELOPES if o["qid"] == qid)["rows"])
        by_rows2.setdefault(key, []).append((qid, twin, rm, ra))
    for key, grp in by_rows2.items():
        rms = {round(x[2], 9) for x in grp}
        ras = {round(x[3], 9) for x in grp}
        if len(rms) != 1 or len(ras) != 1:
            twin_id_ok2 = False
    print(f"twin-identity G2 (r-hat constant across identical-rows groups): {twin_id_ok2}")
    if not twin_id_ok2:
        fails.append("KB-R3-ORACLE: G2 twin-identity of r-hat estimators failed")
    for est_i, est_name in ((3, "rhat_max"), (4, "rhat_all")):
        print(f"--- G2 gate on {est_name} ---")
        for t in (0.30, 0.50, 0.70, 0.90):
            adm_a = adm_b = val = 0
            for qid, twin, gold, rm, ra in rows_g2:
                rh = rm if est_i == 3 else ra
                if rh >= t:
                    c = arm_logs["D"][qid]
                    v = 0
                    if c["verdict"] == "CONVERGE":
                        v = 1 if c["chosen"] == gold else -1
                    val += v
                    if twin == "S1A":
                        adm_a += 1
                    else:
                        adm_b += 1
            n = adm_a + adm_b
            ev = val / n if n else 0.0
            print(f"  t={t:.2f}: admitted S1A={adm_a} S1B={adm_b} EV={ev:+.2f}/case")

    # ---- R4 S8 fiat cost ----
    print("=== Block S: fiat-breaking cost ===")
    wrong = conf = 0
    wrong_c = conf_c = 0
    for e in ENVELOPES:
        if e["block"] != "S":
            continue
        c = arm_logs["D"][e["qid"]]
        if c["verdict"] == "CONVERGE":
            conf += 1
            if c["chosen"] != e["latent"]:
                wrong += 1
        cc = arm_logs["C"][e["qid"]]
        if cc["verdict"] == "CONVERGE":
            conf_c += 1
            if cc["chosen"] != e["latent"]:
                wrong_c += 1
    print(f"D fiat convergences: {conf}/20; wrong guesses vs latent truth: {wrong}/20 "
          f"({100 * wrong / 20:.0f}%); false-confidence rate: {100 * conf / 20:.0f}%")
    print(f"C fiat convergences: {conf_c}/20; wrong guesses vs latent truth: {wrong_c}/20 "
          f"({100 * wrong_c / 20:.0f}%); false-confidence rate: {100 * conf_c / 20:.0f}%")

    if fails:
        print(f"FAILURES ({len(fails)}):")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("ALL BARS HOLD")


if __name__ == "__main__":
    main()
