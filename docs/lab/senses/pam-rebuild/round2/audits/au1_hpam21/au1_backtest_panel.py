#!/usr/bin/env python3
"""AU-1b: H-PAM-21 backtest-panel extension.

Same reconstruction as au1_effective_n.py but over the frozen backtest
candidate ledger v2/redteam/evidence/ledger_d_withhold.txt (43
DISP=ACCEPT_INSTALL lines, 17-field format, no SET= field), validated
against the committed bt1.out replay log
(SHA 5c9eea9d8f5dbb84ea95d9c4b7ee9255ac355f95828bcb08ae41729a02a8b93f).

Panel of interest: the 8 blocked false accepts (TMB-5) whose quorum
engaged. Small-n: report vote patterns + nesting, not ICC.

Usage: au1_backtest_panel.py <ledger> <exemplars> <bt1.out> <out_report.txt>
"""
import sys, math

TC, TM = 130, 950
PB_C, PB_M = 150, 2000

def stem_of(s):
    if s.startswith("rt4_"):
        s = s[4:]
    cut = s.find("-")
    return s if cut < 0 else s[:cut]

def block_ok(stem, conf, meas, ex):
    for es, ec, em in ex:
        if es == stem and abs(conf - ec) <= PB_C and abs(meas - em) <= PB_M:
            return True
    return False

def core_hit(stem, conf, meas, ex):
    for es, ec, em in ex:
        if es == stem and abs(conf - ec) <= TC and abs(meas - em) <= TM:
            return True
    return False

def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
    vx = sum((x - mx) ** 2 for x in xs) / n
    vy = sum((y - my) ** 2 for y in ys) / n
    if vx == 0 or vy == 0:
        return float("nan")
    return cov / math.sqrt(vx * vy)

def main():
    led_path, ex_path, bt_path, rep_path = sys.argv[1:5]
    ex = []
    with open(ex_path) as f:
        lines = f.read().splitlines()
    for ln in lines[1:]:
        if not ln.strip():
            continue
        f0, f1, f2, f3 = ln.split("\t")[:4]
        ex.append((stem_of(f1), int(f2), int(f3)))

    cand = []
    with open(led_path) as f:
        for ln in f:
            flds = ln.rstrip("\n").split("|")
            if len(flds) == 17 and flds[15].startswith("DISP=ACCEPT_INSTALL"):
                cand.append((flds[4], int(flds[8]), int(flds[10]), flds[7], flds[12]))
    assert len(cand) == 43, f"expected 43 candidates, got {len(cand)}"

    rec = []
    for name, conf, meas, judg, truth in cand:
        stem = stem_of(name)
        b = block_ok(stem, conf, meas, ex)
        v1 = core_hit(stem, conf - 10, meas - 200, ex)
        v2 = core_hit(stem, conf, meas, ex)
        v3 = core_hit(stem, conf + 10, meas + 200, ex)
        verdict = "-" if not b else ("WITHHOLD" if (v1 + v2 + v3) >= 2 else "CONFIRM_INSTALL")
        rec.append((name, b, int(v1), int(v2), int(v3), verdict, judg != truth))

    with open(bt_path) as f:
        bt_lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    bt_lines = [ln for ln in bt_lines if len(ln.split("\t")) >= 3 and ln.split("\t")[2] == "BACKTEST"]
    assert len(bt_lines) == 43, f"expected 43 BACKTEST log lines, got {len(bt_lines)}"
    mism = []
    for (name, b, v1, v2, v3, verdict, _), ln in zip(rec, bt_lines):
        t = ln.split("\t")
        if not (t[1] == name and (t[3] == "BLOCKED") == b and t[5] == verdict):
            mism.append((name, b, verdict, t[3], t[5]))
    if mism:
        sys.stderr.write(f"VALIDATION FAILED: {len(mism)} mismatches\n")
        for m in mism[:10]:
            sys.stderr.write(f"  {m}\n")
        sys.exit(11)

    falses = [r for r in rec if r[6]]
    tmb_falses = [r for r in falses if r[0].split("_")[1].startswith("TMB")]
    blocked_tmb_falses = [r for r in tmb_falses if r[1]]
    vs = [(r[2], r[3], r[4]) for r in blocked_tmb_falses]

    def f(x):
        return "n/a" if (isinstance(x, float) and math.isnan(x)) else f"{x:.6f}"

    L = []
    L.append("AU-1b H-PAM-21 BACKTEST-PANEL EXTENSION")
    L.append("frozen input: v2/redteam/evidence/ledger_d_withhold.txt (43 candidates, 17-field)")
    L.append("frozen log: bt1.out (SHA 5c9eea9d8f5dbb84ea95d9c4b7ee9255ac355f95828bcb08ae41729a02a8b93f)")
    L.append(f"validation: reconstructed (blocked,quorum) matches bt1.out on 43/43 candidates: PASS")
    L.append(f"false accepts: {len(falses)} (TMB: {len(tmb_falses)}), blocked TMB falses (quorum engaged): {len(blocked_tmb_falses)}")
    L.append("")
    L.append("vote triples of the blocked TMB falses (v1v2v3):")
    for r in blocked_tmb_falses:
        L.append(f"  {r[0]}: {r[2]}{r[3]}{r[4]} -> {r[5]}")
    n = len(vs)
    if n > 0:
        pats = {}
        for v in vs:
            pats[v] = pats.get(v, 0) + 1
        L.append("pattern distribution:")
        for k in sorted(pats):
            L.append(f"  {k[0]}{k[1]}{k[2]}: {pats[k]}")
        unan = sum(1 for v in vs if v[0] == v[1] == v[2])
        nest = all(v[2] <= v[1] <= v[0] for v in vs)
        L.append(f"unanimous: {unan}/{n}; monotone nesting c3<=c2<=c1 on all: {nest}")
        q = [1 if sum(v) >= 2 else 0 for v in vs]
        L.append(f"quorum == center crop alone: {sum(1 for v,qq in zip(vs,q) if v[1]==qq)}/{n}")
        if n >= 3:
            c1 = [v[0] for v in vs]; c2 = [v[1] for v in vs]; c3 = [v[2] for v in vs]
            rhos = [pearson(c1, c2), pearson(c1, c3), pearson(c2, c3)]
            finite = [r for r in rhos if not math.isnan(r)]
            if finite:
                rm = sum(finite) / len(finite)
                L.append(f"mean pairwise rho = {f(rm)} -> n_eff = {f(3.0/(1.0+2.0*rm))} (n={n}, noisy)")
            else:
                L.append("degenerate votes (zero variance): all triples identical")
    with open(rep_path, "w") as f:
        f.write("\n".join(L) + "\n")
    print(f"validation PASS: 43/43 BACKTEST match bt log")
    print(f"blocked TMB falses: {len(blocked_tmb_falses)}, triples: {vs}")

if __name__ == "__main__":
    main()
