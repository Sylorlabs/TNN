#!/usr/bin/env python3
"""Analyze the RT-B fork-test battery against the frozen prereg.

Usage: verify.py [FID|B|PSH|ALL] — checks one cell class at a time so the
fidelity gate is evaluated before attack results are read.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(ROOT, "evidence")


def parse_run(tag):
    d = {}
    for line in open(os.path.join(EV, "%s_run1.txt" % tag)):
        p = line.strip().split(",")
        if p[0] == "TN_CHECK" and len(p) == 4:
            d["%s,%s" % (p[0], p[1])] = int(p[2])
        if p[0] == "RT_FACT" and len(p) == 3:
            d["%s,%s" % (p[0], p[1])] = int(p[2])
    return d


def kb_b1(m):
    n_un = m.get("TN_CHECK,rtb_nuninstall", -999)
    n_pr = m.get("TN_CHECK,rtb_npromote", -999)
    ok = n_un >= 1 and n_pr == 0
    return ("SURVIVE" if ok else "KILL",
            "nuninstall=%d npromote=%d" % (n_un, n_pr))


def check_fid(tag):
    """Returns (ok, notes). FID gate per frozen prereg §4."""
    m = parse_run(tag)
    notes = []
    # FID-H: honest arm exact
    h_fail = 0
    for k, v in m.items():
        if k.startswith("TN_CHECK,glh_"):
            exp = None
            # re-derive expected from run line
            h_fail += 0  # computed below properly
    # simpler: count failing checks by prefix from the raw file
    gh = gl = 0
    gh_bad, gl_bad = [], []
    for line in open(os.path.join(EV, "%s_run1.txt" % tag)):
        p = line.strip().split(",")
        if p[0] == "TN_CHECK" and len(p) == 4:
            bad = p[2] != p[3]
            if p[1].startswith("glh_"):
                gh += 1
                if bad:
                    gh_bad.append(p[1])
            elif p[1].startswith("gll_"):
                gl += 1
                if bad:
                    gl_bad.append(p[1])
    notes.append("honest: %d checks, %d failing %s" % (gh, len(gh_bad), gh_bad))
    notes.append("lying: %d checks, %d failing %s" % (gl, len(gl_bad), gl_bad))
    h_total = m.get("TN_CHECK,glh_audit_total", -1)
    l_total = m.get("TN_CHECK,gll_audit_total", -1)
    notes.append("audit totals: honest=%d lying=%d" % (h_total, l_total))
    return (len(gh_bad) == 0 and h_total == 269, gh_bad, gl_bad, h_total, l_total, notes)


FID6 = {"gll_revoke_step", "gll_commit_step", "gll_neg_signal_n",
        "gll_total_contest", "gll_total_rekey", "gll_quar_used"}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "ALL"
    forks = ["f1", "f2", "f3", "r1a", "r1b"]
    if which in ("FID", "ALL"):
        print("=== FIDELITY GATE ===")
        for fk in forks + ["ctl"]:
            tag = "%s_FID" % fk
            ok_h, gh_bad, gl_bad, h_total, l_total, notes = check_fid(tag)
            for n in notes:
                print("%-8s %s" % (tag, n))
            if fk in ("f2", "r1a", "r1b", "ctl"):
                gate = ok_h and len(gl_bad) == 0 and l_total == 271
                print("%-8s GATE(exact 269/271, TN_FAILURES=0): %s"
                      % (tag, "PASS" if gate else "FAIL"))
            else:
                gate = (ok_h and set(gl_bad) == FID6 and l_total == 271)
                print("%-8s GATE(269 + 271 w/ 6 frozen deviations): %s"
                      % (tag, "PASS" if gate else "FAIL"))
            print()
    if which in ("B", "ALL"):
        print("=== RT-B ATTACK CELLS (KB-B1) ===")
        for fk in forks + ["ctl"]:
            tag = "%s_B" % fk
            m = parse_run(tag)
            verdict, detail = kb_b1(m)
            total = m.get("TN_CHECK,rtb_audit_total", -1)
            rs = m.get("TN_CHECK,rtb_revoke_step", -999)
            up = m.get("RT_FACT,rtb_uninstall_policy", -999)
            cp_ = m.get("RT_FACT,rtb_commit_policy", -999)
            pp = m.get("RT_FACT,rtb_promote_policy", -999)
            badep = m.get("RT_FACT,rtb_badep", -999)
            print("%-8s %s | KB-B1=%s total=%d revoke_step=%d u/c/p=%d/%d/%d badep=%d"
                  % (tag, detail, verdict, total, rs, up, cp_, pp, badep))
    if which in ("PSH", "ALL"):
        print("=== P-SH SILENT-HONEST PROBE (secondary) ===")
        for fk in forks:
            tag = "%s_PSH" % fk
            m = parse_run(tag)
            npr = m.get("RT_FACT,psh_npromote", m.get("TN_CHECK,psh_npromote", -999))
            total = m.get("TN_CHECK,psh_audit_total", -1)
            print("%-8s npromote=%s audit_total=%s" % (tag, npr, total))


if __name__ == "__main__":
    sys.exit(main())
