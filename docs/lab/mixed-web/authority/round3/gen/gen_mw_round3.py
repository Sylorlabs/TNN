#!/usr/bin/env python3
"""gen_mw_round3.py — generate round-3 (reliability sweep) case files.

Implements PREREG-MW-R3 section R1 exactly (frozen 2026-09-22, committed
before this generator was written or run).

Envelope blocks (420 synthetic envelopes, fictional entities):
  Block R: 9 reliability levels x 20 CORROBORATED dispute (S1-shape)
           envelopes. At level r: n_A(r)=round(20*r) S1A-twins (gold=A1),
           rest S1B-twins (gold=A2). Twin placement: envelope i (0-based
           within level) is S1A iff (i*n_A) mod 20 < n_A (Bresenham).
  Block U (AMENDMENT-A3): 9 reliability levels x 20 UNCORROBORATED dispute
           (U1-shape) envelopes — same levels, counts, and interleave as R.
           The loose-vs-conservative margin lives here: C withholds (veto),
           D converges (loose-unique).
  Block G: 20 corroborated dispute envelopes, 50/50 mix (n_A=10),
           rel_ind=UNKNOWN.
  Block G2 (AMENDMENT-A3): 20 UNCORROBORATED dispute envelopes, 50/50 mix,
           rel_ind=UNKNOWN — self-estimation stress on the licensed shape.
  Block S: 20 genuine-2v2 tie envelopes, gold UNDETERMINABLE, latent truth
           A1 iff (i mod 2 == 0) else A2 (modeling device for wrong-guess).

Arms: B = mw_deliberate (frozen PREREG s4), C = mw_deliberate_c
(conservative PRIMARY, PREREG-MW-C M1), D = mw_deliberate_d (PRIMARY_LOOSE,
PREREG-MW-D D1). Mechanism expectations below drive the binaries'
self-checks; stipulated golds live in ENVELOPES/manifest for the verifier.
"""
import json
import os
import re
import sys

BASE = os.path.expanduser("~/workspace/tnn-lab/mixed-web")
sys.path.insert(0, BASE)
from gen_mw import zg  # noqa  (escape helper only; no mechanism code)

R3 = os.path.join(BASE, "authority", "round3")
SRC = os.path.join(R3, "src")

# ---- frozen name pools (PREREG-MW-R3 R1) ----
PRIMARIES = ["zorbian.com", "quellar.org", "myndax.net",
             "velkora.io", "dravnik.com", "osselyn.org"]
PAIRS = [("Marco Venn", "Luis Okafor"),
         ("Petra Halvorsen", "Dario Mensah"),
         ("Ines Kovac", "Tomas Reyes"),
         ("Anya Petrova", "Kwame Diallo"),
         ("Sofia Marchetti", "Jonas Lindqvist"),
         ("Ravi Chandran", "Elena Vasquez")]
RIVALS = ["racefeed.net", "speedway.org", "pitwall.io",
          "apexwire.com", "gridtalk.net", "laptime.org"]

LEVELS = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
K = 20


def dispute_rows(j):
    prim = PRIMARIES[j % 6]
    a1, a2 = PAIRS[j % 6]
    r1 = RIVALS[j % 6]
    r2 = RIVALS[(j + 1) % 6]
    cr = RIVALS[(j + 2) % 6]
    return (prim, a1, [(prim, a1, 2026), (prim, a1, 2024),
                       (r1, a2, 2026), (r2, a2, 2026), (cr, a1, 2025)])


def dispute_rows_uncorr(j):
    """AMENDMENT-A3 U1 shape: uncorroborated dispute, split equally-new
    contradiction. No domain corroborates the primary's newest answer."""
    prim = PRIMARIES[j % 6]
    a1 = PAIRS[j % 6][0]
    r1 = RIVALS[j % 6]
    a2 = PAIRS[(j + 1) % 6][1]
    r2 = RIVALS[(j + 1) % 6]
    a3 = PAIRS[(j + 2) % 6][0]
    return (prim, a1, [(prim, a1, 2026), (prim, a1, 2024),
                       (r1, a2, 2026), (r2, a3, 2026)])


def tie_rows(j):
    prim = PRIMARIES[j % 6]
    a1, a2 = PAIRS[j % 6]
    r1 = RIVALS[j % 6]
    r2 = RIVALS[(j + 1) % 6]
    r3 = RIVALS[(j + 3) % 6]
    return (prim, a1, [(prim, a1, 2026), (r1, a2, 2026),
                       (r2, a1, 2026), (r3, a2, 2026)])


def question_for(prim):
    label = prim.split(".")[0]
    return f"Who won the 2026 {label} grand prix?"


def build_envelopes():
    envs = []
    # Block R
    for r in LEVELS:
        n_a = round(K * r)
        tag = f"{int(round(r * 100)):d}"
        for i in range(K):
            j = LEVELS.index(r) * K + i
            prim, a1, rows = dispute_rows(j)
            is_a = (i * n_a) % K < n_a
            twin = "S1A" if is_a else "S1B"
            a2 = PAIRS[j % 6][1]
            envs.append({
                "qid": f"R{tag}_{i:02d}",
                "block": "R", "level": r, "twin": twin,
                "question": question_for(prim),
                "rows": rows,
                "stip_gold": a1 if is_a else a2,
                "rel_ind": r, "latent": None,
            })
    # Block U (AMENDMENT-A3): 9 reliability levels x 20 UNCORROBORATED
    # disputes (U1 shape). The loose-vs-conservative margin lives here.
    for r in LEVELS:
        n_a = round(K * r)
        tag = f"{int(round(r * 100)):d}"
        for i in range(K):
            j = 180 + LEVELS.index(r) * K + i
            prim, a1, rows = dispute_rows_uncorr(j)
            is_a = (i * n_a) % K < n_a
            twin = "S1A" if is_a else "S1B"
            a2 = rows[2][1]
            envs.append({
                "qid": f"U{tag}_{i:02d}",
                "block": "U", "level": r, "twin": twin,
                "question": question_for(prim),
                "rows": rows,
                "stip_gold": a1 if is_a else a2,
                "rel_ind": r, "latent": None,
            })
    # Block G
    n_a = 10
    for i in range(K):
        j = 900 + i
        prim, a1, rows = dispute_rows(j)
        is_a = (i * n_a) % K < n_a
        twin = "S1A" if is_a else "S1B"
        a2 = PAIRS[j % 6][1]
        envs.append({
            "qid": f"G_{i:02d}",
            "block": "G", "level": 0.50, "twin": twin,
            "question": question_for(prim),
            "rows": rows,
            "stip_gold": a1 if is_a else a2,
            "rel_ind": None, "latent": None,
        })
    # Block G2 (AMENDMENT-A3): 20 UNCORROBORATED disputes, 50/50 mix,
    # rel_ind=UNKNOWN — self-estimation stress on the licensed shape.
    n_a = 10
    for i in range(K):
        j = 960 + i
        prim, a1, rows = dispute_rows_uncorr(j)
        is_a = (i * n_a) % K < n_a
        twin = "S1A" if is_a else "S1B"
        a2 = rows[2][1]
        envs.append({
            "qid": f"G2_{i:02d}",
            "block": "G2", "level": None, "twin": twin,
            "question": question_for(prim),
            "rows": rows,
            "stip_gold": a1 if is_a else a2,
            "rel_ind": None, "latent": None,
        })
    # Block S
    for i in range(K):
        j = 950 + i
        prim, a1, rows = tie_rows(j)
        a2 = PAIRS[j % 6][1]
        envs.append({
            "qid": f"S8_{i:02d}",
            "block": "S", "level": None, "twin": None,
            "question": question_for(prim),
            "rows": rows,
            "stip_gold": "UNDETERMINABLE",
            "rel_ind": None,
            "latent": a1 if (i % 2 == 0) else a2,
        })
    return envs


ENVELOPES = build_envelopes()


# ---- mechanism expectations for the binaries' self-checks ----
def loose_expected(question, rows):
    """PREREG-MW-D D1 (no condition-4 veto). Returns (fires, answer)."""
    toks = {t for t in re.split(r"[^a-z]", question.lower()) if len(t) >= 4}

    def lab(dom):
        d = dom.lower()
        if d.startswith("www."):
            d = d[4:]
        return d.split(".")[0]

    seen, prim = set(), []
    for d, _a, _r in rows:
        if d in seen:
            continue
        seen.add(d)
        if lab(d) in toks:
            prim.append(d)
    if len(prim) != 1:
        return (False, "")
    D = prim[0]
    own = [(a, r) for d, a, r in rows if d == D and a]
    if not own:
        return (False, "")
    rp = max(r for _a, r in own)
    A = next(a for a, r in own if r == rp)
    if rp < 2000:
        return (False, "")
    if rp != max(r for _d, _a, r in rows):
        return (False, "")
    return (True, A)


def cons_expected(question, rows):
    """PREREG-MW-C M1, faithful to the frozen binary (AMENDMENT-A3 A3.1):
    cond4 = corrob (checked FIRST, takes precedence) OR unique; the
    equally-new-contradiction veto applies ONLY when no corroboration
    exists. Feed-time dedup on (domain, answer) replicated. Returns
    (fires, answer)."""
    f, A = loose_expected(question, rows)
    if not f:
        return (False, "")
    toks = {t for t in re.split(r"[^a-z]", question.lower()) if len(t) >= 4}

    def lab(dom):
        d = dom.lower()
        if d.startswith("www."):
            d = d[4:]
        return d.split(".")[0]

    seen_pairs, res = set(), []
    for d, a, r in rows:
        if (d, a) not in seen_pairs:
            seen_pairs.add((d, a))
            res.append((d, a, r))
    D = next(d for d, _a, _r in res if lab(d) in toks)
    rp = max(r for d, _a, r in res if d == D and _a)
    gmax = max(r for _d, _a, r in res)
    if any(d != D and a == A for d, a, _r in res):
        return (True, A)  # corrob disjunct: fires despite contradiction
    if any(d != D and a and a != A and r == gmax for d, a, r in res):
        return (False, "")  # veto: equally-new contradiction, no corroboration
    return (True, A)  # unique


def emit_feed(lines, tag, qid, question, rows):
    lines.append(f"fn feed{tag}_{qid}(w:*MwF) void {{")
    lines.append(f'    mw_fact_begin(w, "{qid}", "{zg(question)}", 1);')
    for d, a, r in rows:
        lines.append(f'    mw_add_result(w, "{zg(d)}", "{zg(a)}", {r});')
    lines.append("    return;")
    lines.append("}")


def emit_q(lines, tag, arm, qid, exp_verdict, exp_chosen, exp_rule,
           deliberate, cite_rule):
    lines.append(f"fn q{tag}_{qid}() i32 {{")
    lines.append("    let w:*MwF=mw_new();")
    lines.append(f"    feed{tag}_{qid}(w);")
    lines.append(f"    let v:i32={deliberate}(w);")
    lines.append("    mw_fact_end(w);")
    lines.append(f'    _zag_print("V|{arm}|");')
    lines.append(f'    _zag_print("{qid}|");')
    lines.append('    if(v==1){_zag_print("CONVERGE|");}else{_zag_print("WITHHOLD|");}')
    lines.append('    _zag_print(w.*.chosen);_zag_print("|");')
    lines.append('    _zag_print(w.*.rule);_zag_print("|");')
    lines.append('    _zag_print(mw_chain(w));_zag_print("|");')
    if cite_rule is None:
        # arm B: mw_sense.zag defines no mw_primary_cite_of; the authority
        # branch would be dead code (rule never PRIMARY_L) and an undefined
        # reference, so emit the supp print directly.
        lines.append('    _zag_print(mw_supp(w,w.*.chosen));')
    else:
        lines.append(f'    if(mw_equal(w.*.rule,"{cite_rule}")==1){{_zag_print(mw_primary_cite_of(w));}}'
                     'else{_zag_print(mw_supp(w,w.*.chosen));}')
    lines.append('    _zag_print("|");')
    lines.append('    _zag_print(mw_head(w));_zag_println("");')
    lines.append("    let ok:i32=1;")
    if exp_verdict == "CONVERGE":
        lines.append("    if(v!=1){ok=0;}")
        lines.append(f'    if(mw_equal(w.*.chosen, "{zg(exp_chosen)}")!=1){{ok=0;}}')
    else:
        lines.append("    if(v!=2){ok=0;}")
    lines.append(f'    if(mw_equal(w.*.rule, "{exp_rule}")!=1){{ok=0;}}')
    lines.append("    return ok;")
    lines.append("}")


DRIVERS = {
    "B": ("mw_sense.zag", "mw_deliberate", "run_r3b_all", "b",
          None),             # no primary-cite fn in mw_sense.zag; supp only
    "C": ("mw_sense_c.zag", "mw_deliberate_c", "run_r3c_all", "c",
          "PRIMARY"),     # conservative cite code; never fires here
    "D": ("mw_sense_d.zag", "mw_deliberate_d", "run_r3d_all", "d",
          "PRIMARY_L"),
}


def expected_for(arm, question, rows):
    if arm == "B":
        return ("WITHHOLD", "", "TIE")
    if arm == "C":
        # AMENDMENT-A3: frozen M1's corrob disjunct fires on the corroborated
        # R/G/S shapes (CONVERGE); the veto holds on the uncorroborated
        # U/G2 shapes (WITHHOLD). cons_expected implements the true rule.
        f, _a = cons_expected(question, rows)
        return ("CONVERGE", _a, "PRIMARY") if f else ("WITHHOLD", "", "TIE")
    f, a = loose_expected(question, rows)
    return ("CONVERGE", a, "PRIMARY_L") if f else ("WITHHOLD", "", "TIE")


def build_arm(arm):
    sense, deliberate, runfn, cli, cite_rule = DRIVERS[arm]
    tag = "R3" + arm
    lines = [f"// mw_cases_r3{arm.lower()}.zag — GENERATED by gen_mw_round3.py. Do not hand-edit.",
             "// PREREG-MW-R3 R1 + AMENDMENT-A3 envelope families (420 synthetic envelopes).",
             f'@import("{sense}")', ""]
    manifest = []
    qids = []
    for e in ENVELOPES:
        qid = e["qid"]
        v, ch, rule = expected_for(arm, e["question"], e["rows"])
        emit_feed(lines, tag, qid, e["question"], e["rows"])
        emit_q(lines, tag, arm, qid, v, ch, rule, deliberate, cite_rule)
        qids.append(qid)
        manifest.append(
            f"{qid}: block={e['block']} level={e['level']} twin={e['twin']} "
            f"stip_gold={e['stip_gold']} rel_ind={e['rel_ind']} latent={e['latent']} "
            f"exp={v}/{ch or '-'}/{rule} "
            f"rows={e['rows']}")
    lines.append(f"fn {runfn}() i32 {{")
    lines.append("    let p:i32=1;")
    for qid in qids:
        lines.append(f"    if(q{tag}_{qid}()!=1){{p=0;}}")
    lines.append("    return p;")
    lines.append("}")
    out = os.path.join(SRC, f"mw_cases_r3{arm.lower()}.zag")
    open(out, "w").write("\n".join(lines) + "\n")
    drv = [f"// mw_trial_r3{arm.lower()}.zag — round-3 arm-{arm} trial driver.",
           f"// Usage: mw_trial_r3{arm.lower()} <{cli}>",
           "// Deterministic: no timestamps, no RNG. N=5 replays byte-identical.",
           f'@import("{sense}")',
           f'@import("mw_cases_r3{arm.lower()}.zag")', "",
           "fn main()i32 {",
           "    let m:[]u8=_zag_arg(1);",
           f'    if(mw_equal(m,"{cli}")==1){{',
           f"        let p:i32={runfn}();",
           f'        if(p==1){{_zag_println("{arm}|ALL_CHECKS_PASS");}}',
           f'        if(p!=1){{_zag_println("{arm}|CHECKS_FAILED");}}',
           "        if(p==1){return 0;}",
           "        return 1;",
           "    }",
           f'    _zag_println("usage: mw_trial_r3{arm.lower()} <{cli}>");',
           "    return 2;",
           "}"]
    open(os.path.join(SRC, f"mw_trial_r3{arm.lower()}.zag"), "w").write("\n".join(drv) + "\n")
    return manifest


def main():
    os.makedirs(SRC, exist_ok=True)
    man = []
    for arm in ("B", "C", "D"):
        man.extend(build_arm(arm))
        print(f"arm {arm}: {len(ENVELOPES)} questions")
    open(os.path.join(R3, "manifest_r3.txt"), "w").write("\n".join(man) + "\n")
    # sanity: counts per level
    for r in LEVELS:
        n_a = sum(1 for e in ENVELOPES
                  if e["block"] == "R" and e["level"] == r and e["twin"] == "S1A")
        print(f"level {r}: S1A={n_a} S1B={20 - n_a} (expect {round(20 * r)}/{20 - round(20 * r)})")
    print(f"Block G: {sum(1 for e in ENVELOPES if e['block'] == 'G')} envelopes")
    print(f"Block G2: {sum(1 for e in ENVELOPES if e['block'] == 'G2')} envelopes")
    print(f"Block S: {sum(1 for e in ENVELOPES if e['block'] == 'S')} envelopes")
    print(f"Block U: {sum(1 for e in ENVELOPES if e['block'] == 'U')} envelopes")
    for r in LEVELS:
        n_a = sum(1 for e in ENVELOPES
                  if e["block"] == "U" and e["level"] == r and e["twin"] == "S1A")
        ok = "OK" if n_a == round(20 * r) else "MISMATCH"
        print(f"  U level {r}: S1A={n_a} [{ok}]")


if __name__ == "__main__":
    main()
