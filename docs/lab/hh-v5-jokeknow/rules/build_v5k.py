#!/usr/bin/env python3
"""Assemble g_intent6_v5k.zag = v4fix4 + knowledge rule chain.
Usage: build_v5k.py <tables_zag> <outdir>
Copies base files, injects @imports and the K_ rule chain."""
import sys, shutil, os

tables = sys.argv[1]
outdir = sys.argv[2]
os.makedirs(outdir, exist_ok=True)
base = os.path.expanduser("~/workspace/hh-v5-jokeknow/base")
rules = os.path.expanduser("~/workspace/hh-v5-jokeknow/rules")

for f in ["j_ledger.zag", "r5_r6.zag", "R33_NATIVE_IO_V1.zag",
          "R33_NATIVE_SHA256_V2.zag", "run4.zag"]:
    shutil.copy(os.path.join(base, f), outdir)
shutil.copy(os.path.join(rules, "k_rules.zag"), outdir)
shutil.copy(tables, os.path.join(outdir, "k_tables.zag"))

src = open(os.path.join(base, "g_intent6_v4fix4.zag")).read()

# 1. imports
old_imp = '@import("r5_r6.zag")'
new_imp = ('@import("r5_r6.zag")\n@import("k_tables.zag")\n@import("k_rules.zag")')
assert src.count(old_imp) == 1
src = src.replace(old_imp, new_imp)

# 2. K_ rule chain after N_VALENCE
anchor = 'g_markers_append(markers,"valence");}}'
assert src.count(anchor) == 1
chain = anchor + '''
    // V5 knowledge-backed rules: shape (knowledge element present) + a genuine
    // incongruity TURN verified by a general mechanism. Knowledge never fires
    // on shape alone. Appended with contra==0 guards: nothing previously
    // caught changes verdict.
    if(contra==0){if(k_pun_turn(t)!=0){contra=57;g_codes_append(codes,"K_PUN");g_markers_append(markers,"k_pun");}}
    if(contra==0){if(k_qa_pun_turn(t)!=0){contra=58;g_codes_append(codes,"K_QA_PUN");g_markers_append(markers,"k_qa_pun");}}
    if(contra==0){if(k_idiom_turn(t)!=0){contra=59;g_codes_append(codes,"K_IDIOM");g_markers_append(markers,"k_idiom");}}
    if(contra==0){if(k_world_turn(t)!=0){contra=60;g_codes_append(codes,"K_WORLD");g_markers_append(markers,"k_world");}}
    if(contra==0){if(k_phon_turn(t)!=0){contra=61;g_codes_append(codes,"K_PHON");g_markers_append(markers,"k_phon");}}'''
src = src.replace(anchor, chain)

out = os.path.join(outdir, "g_intent6_v5k.zag")
open(out, "w").write(src)

# runner: point run4.zag at the v5k classifier
run = open(os.path.join(outdir, "run4.zag")).read()
assert run.count('@import("g_intent6_v4fix4.zag")') == 1
run = run.replace('@import("g_intent6_v4fix4.zag")', '@import("g_intent6_v5k.zag")')
open(os.path.join(outdir, "run4.zag"), "w").write(run)
print("wrote", out)
