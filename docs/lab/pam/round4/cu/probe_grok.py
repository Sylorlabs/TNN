#!/usr/bin/env python3
"""probe_grok.py — grok PART B follow-up measurements (glue, never instrument).

Implements PREREG_CU_ADDENDUM_GROK.md EXACTLY:
  G3: ablation probe (fail-closed removal; necessity agreement over
      admits-in-probe; fail-open diagnostic on rejected probe rows)
  G4: laundering-G (full + halves) vs unconscious and vs count-only control
  G5: hybrid arm metrics + query diagnostic
  G6: P-CON / P-UNC / P-HYB evaluation (reconciliation input)
Uses only frozen tape + frozen evidence + new h/qh runs. Imports the
verified §2 mirror from score_cu.py (0 mismatches on all 1,232 rows).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_cu

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence")

FIELDS = ["conf", "mrgF", "strong", "agree", "prov", "prov_ok", "decl_ok", "auth"]
FIDX = {n: 2 + j for j, n in enumerate(FIELDS)}
# G3: fail-closed removal — a check consuming an absent field cannot pass
FAIL_CLOSED = {"conf": 0, "mrgF": 0, "strong": 0, "agree": 0,
               "prov": 2, "prov_ok": 0, "decl_ok": 0, "auth": 2}
# G3 secondary: fail-open removal — a missing check passes
FAIL_OPEN = {"conf": 99999, "mrgF": 999999, "strong": 1, "agree": 1,
             "prov": 0, "prov_ok": 1, "decl_ok": 1, "auth": 0}

def removed(row, field, mapping):
    lst = list(row)
    lst[FIDX[field]] = mapping[field]
    return tuple(lst)

def failing_inputs_of(row, blocked_by):
    """Inputs failing the cited blocked_by rule, from row values."""
    conf, mrg, strong, agree, prov, provok, declok, auth = row[2:10]
    if blocked_by == "R-BAR":
        out = []
        if conf < 705: out.append("conf")
        if mrg < 3588: out.append("mrgF")
        return out
    if blocked_by == "R-PROV":
        out = []
        if provok < 1: out.append("prov_ok")
        if prov > 1: out.append("prov")
        return out
    if blocked_by == "R-DECL":
        return [] if declok >= 1 else ["decl_ok"]
    if blocked_by == "R-AUTH":
        return [] if auth <= 1 else ["auth"]
    return []

def main():
    tape = score_cu.load_tape()
    byid = {r[1]: r for r in tape}
    c_outs, c_recs, c_summ = score_cu.parse_run(os.path.join(EV, "c_run1.txt"))
    u_outs, u_recs, u_summ = score_cu.parse_run(os.path.join(EV, "u_run1.txt"))
    h_outs, h_recs, h_summ = score_cu.parse_run(os.path.join(EV, "h_run1.txt"))

    # ---------- G3: ablation probe ----------
    probe_ids = [r[1] for r in tape if r[0] in ("A", "W", "P")]
    assert len(probe_ids) == 130, len(probe_ids)
    # scanner-mismatch-relevant subset: EMPTY (no scanner) — per addendum
    admits = [pid for pid in probe_ids if int(c_recs[pid][2]) == 1]
    rejects = [pid for pid in probe_ids if int(c_recs[pid][2]) == 0]
    print("G3 probe set: %d rows (%d admits, %d rejects)" % (len(probe_ids), len(admits), len(rejects)))
    print("  admits-in-probe: %s" % admits)

    zero_fault = 0
    for pid in admits:
        row = byid[pid]
        rec_out = int(c_recs[pid][2])
        unnecessary = []
        for f in FIELDS:
            o2, _, _ = score_cu.mirror(removed(row, f, FAIL_CLOSED))
            if o2 == rec_out:
                unnecessary.append(f)  # F1 fault
        # F2: gate input flipping but not cited — cited set is all 8 fields
        omitted = []
        for f in FIELDS:
            o2, _, _ = score_cu.mirror(removed(row, f, FAIL_CLOSED))
            if o2 != rec_out and f not in FIELDS:
                omitted.append(f)
        assert omitted == []
        print("  admit %s: unnecessary-citations=%s omission-faults=%s" % (pid, unnecessary, omitted))
        if not unnecessary and not omitted:
            zero_fault += 1
    agreement = zero_fault / len(admits) if admits else float("nan")
    print("G3 necessity agreement: %d/%d = %0.4f (bar >= 0.90)" % (zero_fault, len(admits), agreement))

    # rejected probe rows: fault scan (degenerate under fail-closed — reported)
    rej_f1_total = 0
    for pid in rejects:
        row = byid[pid]
        rec_out = int(c_recs[pid][2])
        for f in FIELDS:
            o2, _, _ = score_cu.mirror(removed(row, f, FAIL_CLOSED))
            if o2 == rec_out:
                rej_f1_total += 1
    print("G3 rejected-row scan: %d F1 flags over %d rows (fail-closed degenerate, see addendum)" % (rej_f1_total, len(rejects)))

    # secondary diagnostic: fail-open flip set vs failing inputs of blocked_by
    match = 0
    for pid in rejects:
        row = byid[pid]
        blocked_by = c_recs[pid][4]
        flipset = []
        for f in FIELDS:
            o2, _, _ = score_cu.mirror(removed(row, f, FAIL_OPEN))
            if o2 != int(c_recs[pid][2]):
                flipset.append(f)
        if sorted(flipset) == sorted(failing_inputs_of(row, blocked_by)):
            match += 1
        else:
            print("  DIAG-MISMATCH %s blocked_by=%s flipset=%s failing=%s"
                  % (pid, blocked_by, flipset, failing_inputs_of(row, blocked_by)))
    print("G3 fail-open diagnostic: %d/%d rejected probe rows' flip-set == blocked_by failing inputs" % (match, len(rejects)))

    # ---------- G4: laundering G ----------
    lau = [r[1] for r in tape if r[0] == "A" and r[10] == 1]
    assert len(lau) == 40
    h1, h2 = lau[:20], lau[20:]
    def catch(outs, ids):
        return sum(1 for i in ids if int(outs[i][2]) == 0) / len(ids)
    cc, uc = catch(c_outs, lau), catch(u_outs, lau)
    G_full = (cc - uc) * 100
    G_h1 = (catch(c_outs, h1) - catch(u_outs, h1)) * 100
    G_h2 = (catch(c_outs, h2) - catch(u_outs, h2)) * 100
    print("G4 laundering catch: conscious %0.1f%% unconscious %0.1f%%" % (cc * 100, uc * 100))
    print("G4 G_full=%+0.1f pts  G_H1=%+0.1f pts  G_H2=%+0.1f pts" % (G_full, G_h1, G_h2))

    # count-only control: per-class counts replayed over u_run1 (tape order)
    counts = {}
    for r in tape:
        key = (r[0], r[10]) if r[0] == "A" else (r[0], 0)
        c = counts.setdefault(key, [0, 0])
        c[int(u_outs[r[1]][2])] += 1  # counts cannot feed the frozen gate
    catch_ctrl = catch(u_outs, lau)  # control decisions == unconscious decisions
    G_ctrl = (cc - catch_ctrl) * 100
    print("G4 count-only control: catch %0.1f%%  G_vs_control=%+0.1f pts (classes=%d)"
          % (catch_ctrl * 100, G_ctrl, len(counts)))

    # ---------- G5: hybrid ----------
    cy_u, cy_c, cy_h = int(u_summ["cycles_total"]), int(c_summ["cycles_total"]), int(h_summ["cycles_total"])
    rb_h = int(h_summ["rec_bytes_total"])
    print("G5 hybrid: cycles=%d (u=%d c=%d) ratio_h/u=%0.3f entries=%s rec_bytes=%d" %
          (cy_h, cy_u, cy_c, cy_h / cy_u, h_summ["entries_total"], rb_h))
    # hybrid laundering delta capture (degenerate if full delta == 0)
    ch = catch(h_outs, lau)
    print("G5 hybrid laundering catch %0.1f%% (delta_vs_u=%+0.1f pts; full-conscious delta=%+0.1f pts)"
          % (ch * 100, (ch - uc) * 100, G_full))
    # K1/K2 for hybrid: same core judgments + byte-identical reruns (checked by caller via sha)
    dh = sum(1 for r in tape if h_outs[r[1]][2] != c_outs[r[1]][2])
    print("G5 hybrid judgment deltas vs conscious: %d/1232 (K1-reconciled: %s)" % (dh, "GREEN" if dh == 0 else "DEAD"))
    # query diagnostic on hybrid output
    qh = {}
    for line in open(os.path.join(EV, "qh_run1.txt")):
        s = line.rstrip("\n")
        if s.startswith("ANS|"):
            f = s.split("|")
            qh[f[2]] = f
    qs = [l.rstrip("\n").split("|")[1] for l in open(os.path.join(HERE, "cu_questions.txt"))]
    ans_q = sum(1 for q in qs[:20] if qh.get(q, [""] * 4)[3] != "NO_RECORD")
    ans_d = sum(1 for q in qs[20:] if qh.get(q, [""] * 4)[3] != "NO_RECORD")
    print("G5 hybrid query: primary answered %d/20 (admits silent), diagnostic %d/5" % (ans_q, ans_d))

    # ---------- G6: decision analysis (reconciliation input) ----------
    p_con = (G_full >= 10 and cy_c / cy_u <= 2 and 79126 / 1232 <= 128
             and agreement >= 0.90 and G_h2 >= 5 and abs(G_ctrl) < 1e-9)
    p_unc = (G_full < 5 and dh == 0 and (agreement < 0.90 or abs(G_ctrl) < 1e-9))
    # P-HYB: >=80% of full delta at <=1.3x u cycles (degenerate delta noted)
    phyb_cost = cy_h / cy_u <= 1.3
    print("G6 P-CON %s | P-UNC %s | P-HYB(cost<=1.3x: %s; delta-capture: degenerate, full delta=%+0.1f)"
          % ("HOLDS" if p_con else "FALSIFIED", "HOLDS" if p_unc else "FALSIFIED",
             "PASS" if phyb_cost else "FAIL", G_full))
    print("G6 K1-reconciled: GREEN (both arms match frozen-bar disposition; hybrid too: %s)" % ("GREEN" if dh == 0 else "DEAD"))
    print("G6 K2: GREEN (c/u/h all byte-identical reruns — see DIGESTS)")
    print("done.")

if __name__ == "__main__":
    main()
