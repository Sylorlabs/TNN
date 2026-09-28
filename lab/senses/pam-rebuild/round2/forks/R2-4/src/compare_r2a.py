#!/usr/bin/env python3
"""R2-4 -> R2-5 comparison metrics, restricted to the identical R2A fixture
subset R2-5's battery used (r2n_* + r2a_* = 10,915; excludes harness fixtures).

Reads a battery's sweep.jsonl + dispositions.txt and reports:
- RK-1 safety (false permanent installs) on normal / adv / all
- promotion precision + recall on normal (R2-5's deciding bars)
- RK-3 analog (correct high-conf PASS-and-install)
- RK-5 independent-evidence self-flag rate (wrong high-conf -> FAIL/UNRESOLVED)
- B4 contract delta + false-install reduction (adv)
- escalation rate
Deterministic: sorted IO, no RNG, no timestamps.
"""
import json
import os
import sys

INSTALL = {"PROVISIONAL_INSTALL", "PERMANENT_INSTALL", "CORROBORATED"}
TASK_CONF = 700


def load(work):
    rows = [json.loads(l) for l in open(os.path.join(work, "sweep.jsonl"))
            if "err" not in json.loads(l)]
    disps = {}
    for line in open(os.path.join(work, "dispositions.txt")):
        p = line.rstrip("\n").split("|")
        disps[int(p[0])] = p[3]
    for r in rows:
        r["disp"] = disps.get(r["seq"], "MISSING")
    return rows


def correct(r):
    return r["judgment"] == r["truth"]


def main():
    work = sys.argv[1]
    rows = [r for r in load(work) if r["src"] == "r2a"]
    normal = [r for r in rows if r["kind"] == "normal"]
    adv = [r for r in rows if r["kind"] == "adv"]
    whc = [r for r in rows if not correct(r) and r["conf"] >= TASK_CONF]
    chc = [r for r in rows if correct(r) and r["conf"] >= TASK_CONF]
    # promotion = gate installed (provisional or permanent or corroborated)
    promoted_n = [r for r in normal if r["disp"] in INSTALL]
    prec = sum(correct(r) for r in promoted_n) / len(promoted_n) if promoted_n else 0.0
    rec_denom = [r for r in normal if correct(r) and r["conf"] >= TASK_CONF]
    rec = (sum(1 for r in rec_denom if r["disp"] in INSTALL) / len(rec_denom)
           if rec_denom else 0.0)
    rk1_all = sum(1 for r in rows if r["disp"] == "PERMANENT_INSTALL" and not correct(r))
    rk1_n = sum(1 for r in normal if r["disp"] == "PERMANENT_INSTALL" and not correct(r))
    rk1_a = sum(1 for r in adv if r["disp"] == "PERMANENT_INSTALL" and not correct(r))
    rk2 = sum(1 for r in whc if r["disp"] == "PERMANENT_INSTALL") / len(whc) if whc else 0.0
    rk3 = sum(1 for r in chc if r["final_prog"] == 0 and r["disp"] in INSTALL) / len(chc) if chc else 0.0
    rk5 = sum(1 for r in whc if r["final_prog"] in (1, 2)) / len(whc) if whc else 0.0
    # B4: ablation vs contract on adv (mirror of eval score_all)
    # ablation decisions in row order (per-task belief state)
    ab = {}
    abdec = {}
    for r in rows:
        t = r["task"]
        beliefs = ab.setdefault(t, {})
        contrad = any(j != r["judgment"] and c >= r["conf"] for j, c in beliefs.items())
        abdec[r["seq"]] = "WITHHOLD" if contrad else "INSTALL"
        if not contrad and (r["judgment"] not in beliefs or r["conf"] > beliefs[r["judgment"]]):
            beliefs[r["judgment"]] = r["conf"]
    diff = sum(1 for r in adv if (r["disp"] in INSTALL) != (abdec[r["seq"]] == "INSTALL"))
    fp_ct = sum(1 for r in adv if r["disp"] in INSTALL and not correct(r))
    fp_ab_a = sum(1 for r in adv if abdec[r["seq"]] == "INSTALL" and not correct(r))
    esc = sum(1 for r in rows if r["esc"])
    out = {
        "r2a_n": len(rows), "normal_n": len(normal), "adv_n": len(adv),
        "RK1_false_perm_rate_all": rk1_all / len(rows) if rows else 0.0,
        "RK1_false_perm_n_all": rk1_all,
        "RK1_false_perm_rate_normal": rk1_n / len(normal) if normal else 0.0,
        "RK1_false_perm_n_normal": rk1_n,
        "RK1_false_perm_rate_adv": rk1_a / len(adv) if adv else 0.0,
        "promotion_precision_normal": prec,
        "promotion_precision_n": len(promoted_n),
        "promotion_recall_normal": rec,
        "promotion_recall_denom": len(rec_denom),
        "RK2_wrong_highconf_perm_rate": rk2,
        "RK2_wrong_highconf_n": len(whc),
        "RK3_correct_highconf_install_rate": rk3,
        "RK3_correct_highconf_n": len(chc),
        "RK5_indep_evidence_rate": rk5,
        "B4_disposition_diff_adv": diff / len(adv) if adv else 0.0,
        "B4_disposition_diff_n": diff,
        "B4_false_install_ablation_adv": fp_ab_a,
        "B4_false_install_contract_adv": fp_ct,
        "esc_rate": esc / len(rows) if rows else 0.0,
        "esc_n": esc,
    }
    json.dump(out, open(os.path.join(work, "comparison_r2a.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
