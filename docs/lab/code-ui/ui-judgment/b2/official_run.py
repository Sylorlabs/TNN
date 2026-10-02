#!/usr/bin/env python3
"""CODEUI-1 official B2 run. Frozen protocol; mirrors b2/dryrun.py exactly
except: bads = the INDEPENDENT set in ~/workspace/code-ui/b2-bads/
(built by a party that never saw ui-judgment/). 14 pairs; superiors cycled
deterministically. Traces archived to traces/b2_official/.
"""
import subprocess, sys, re, os
BASE = os.path.expanduser("~/workspace/code-ui/ui-judgment")
os.chdir(BASE)
sups = ["arc1","figma1","github1","github2","linear2","notion1","slack1","slack2","slack3","stripe2"]
bads = ["bad%02d_%s" % (i+1, fam) for i, fam in enumerate([
    "clutter_landing","clutter_dashboard","clutter_marketplace",
    "misalign_signup","misalign_blog","contrast_gray","contrast_clash",
    "type_soup","type_magazine","flat_docs","flat_ecommerce",
    "riot_portfolio","riot_restaurant","riot_fitness"])]
TRACE_DIR = os.path.join(BASE, "traces", "b2_official")
os.makedirs(TRACE_DIR, exist_ok=True)

def judge(img, rep, trace):
    out = subprocess.run(["python3","driver.py","judge",img,rep,trace],
                         capture_output=True, text=True).stdout
    return out

def parse(out):
    d = {}
    for m in re.finditer(r"^(judgment|score|defects)=(.+)$", out, re.M):
        d[m.group(1)] = m.group(2)
    return d

lines = []
for rep in ["a","b"]:
    tag = "A(raw-values)" if rep=="a" else "B(percepts)"
    lines.append("=== OFFICIAL B2 — representation %s ===" % tag)
    wins = 0; det_all = True; reason_all = True
    for i in range(14):
        s, b = sups[i % 10], bads[i]
        sp = "examples/b2superior/%s.img" % s
        bp = os.path.expanduser("~/workspace/code-ui/b2-bads/%s.img" % b)
        ss = [parse(judge(sp, rep, os.path.join(TRACE_DIR, "p%02d_%s_sup.txt" % (i,s)))) for _ in range(3)]
        bs = [parse(judge(bp, rep, os.path.join(TRACE_DIR, "p%02d_%s_bad.txt" % (i,b)))) for _ in range(3)]
        det = (ss[0]==ss[1]==ss[2]) and (bs[0]==bs[1]==bs[2])
        det_all = det_all and det
        ssc, bsc = int(ss[0]['score']), int(bs[0]['score'])
        win = ssc > bsc
        if win: wins += 1
        else: reason_all = False  # lost pairs counted separately below
        reasons = bs[0].get('defects','MISSING')
        ok_reason = (reasons != "none")
        lines.append("pair%02d %s sup=%s(%d) bad=%s(%d) det=%s reason_ok=%s bad_defects=%s" % (
            i, "WIN " if win else "LOSS", s, ssc, b, bsc, det, ok_reason, reasons))
    lines.append("OFFICIAL B2 wins: %d/14  determinism_all=%s" % (wins, det_all))
    lines.append("")

out = "\n".join(lines)
open(os.path.join(BASE, "b2", "OFFICIAL_RESULTS.txt"), "w").write(out)
print(out)
