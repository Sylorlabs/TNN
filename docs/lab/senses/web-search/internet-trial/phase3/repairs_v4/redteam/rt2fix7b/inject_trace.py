#!/usr/bin/env python3
# inject trace prints at r7 call sites; usage: inject_trace.py in.zag out.zag
import sys, re
src = open(sys.argv[1]).read()
sites = [
    ("r7_nonfactive_veto", "VETO nonfactive"),
    ("r7_division_veto", "VETO division"),
    ("r7_equivocation_veto", "VETO equivocation"),
    ("r7_failtoprove_veto", "VETO failtoprove"),
    ("r7_pronoun_veto", "VETO pronoun"),
    ("r7_contrast_deny", "DENY contrast"),
    ("r7_average_deny", "DENY average"),
    ("r7_doubleneg_deny", "DENY doubleneg"),
    ("r7_negverb_paraphrase", "AFF negverb"),
    ("r7_neithernor", "AFF neithernor"),
    ("r7_allbut", "AFF allbut"),
    ("r7_doubleneg2", "AFF doubleneg2"),
    ("r7_dative", "AFF dative"),
    ("r7_genitive", "AFF genitive"),
    ("r7_barely", "AFF barely"),
    ("r7_stopped", "AFF stopped"),
    ("r7_conj_elim", "AFF conj_elim"),
    ("r7_zeroq_single", "AFF zeroq_single"),
    ("r7_numeric", "AFF numeric"),
]
# also numeric sub-checks
for sub in ["r7_num_mult","r7_num_pctof","r7_num_pctcomp","r7_num_ratecomp","r7_num_fracmil",
            "r7_num_halved","r7_num_dateoff","r7_num_weeklater","r7_num_firstexcl",
            "r7_num_died","r7_num_worddigit"]:
    sites.append((sub, "AFF " + sub))
n = 0
for fn, label in sites:
    # match call sites: if(FN(claim,title,snip)==1){return ...;}
    pat = re.compile(r"if\(" + fn + r"\(claim,title,snip\)==1\)\{")
    def rep(m, label=label):
        return 'if(' + fn + '(claim,title,snip)==1){_zag_print("# ' + label + '\\n");'
    src2, c = pat.subn(rep, src)
    # numeric dispatcher inner sites: if(FN(claim,title,snip)==1){return 1;}
    src = src2
    n += c
# also trace r6 sites that might matter (report_frame_rel etc.) - skip, focus r7
open(sys.argv[2], "w").write(src)
print(f"injected {n} trace sites")
