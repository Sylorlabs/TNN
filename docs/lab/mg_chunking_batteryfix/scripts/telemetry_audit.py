#!/usr/bin/env python3
"""Audit: every INTAKE line's chunk= must equal cand_name(policy_winner(kind,shape)).
Faithful port of text_shape/zoom_choose/policy_winner/cand_name/kind_name from intake.zag.
Usage: telemetry_audit.py OUT1 [OUT2 ...]"""
import re, sys

KNAMES = {"KIND0":0,"LETTER_COUNT":1,"POSITION":2,"REVERSE":3,"WORD_COUNT":4,
 "LENGTH":5,"CONTAINS":6,"FIRST_WORD":7,"POS_FIRST":8,"POS_LAST":9,
 "LETTER_COUNT_WORD":10,"LENGTH_WORD":11,"POSITION_WORD":12,"REVERSE_WORD":13,
 "FIRST_LETTER_WORD":14,"LAST_LETTER_WORD":15,"LAST_WORD":16,"CONTAINS_WORD":17,
 "GRAN_COUNT":18,"GRAN_SELECT":19,"GRAN_WORD":20,"TWO_HOP":21,"NESTED":22}
CNAMES = {1:"CHAR",2:"WORD",3:"WORD>CHAR",4:"WORD?CHARSCAN",5:"REV_WORD",
          6:"BOTH_ENDS",7:"SPAN3",8:"SPAN5",9:"END_DIRECT",10:"DELIM"}

def text_shape(t: bytes) -> int:
    return 1 if b" " in t else 0

def policy_winner(kind, shape):
    if kind == 1: return 1 if shape == 1 else 3
    if kind == 2: return 3
    if kind == 3: return 3
    if kind == 4: return 2
    if kind == 5: return 1 if shape == 1 else 2
    if kind == 6: return 3 if shape == 1 else 6
    if kind == 7: return 1 if shape == 1 else 3
    if kind == 8: return 3
    if kind == 9: return 9
    if kind == 10: return 3
    if kind == 11: return 2 if shape == 1 else 3
    if kind == 12: return 3
    if kind == 13: return 3
    if kind == 14: return 3
    if kind == 15: return 3
    if kind == 16: return 2
    if kind == 17: return 3
    if kind == 18: return 10
    if kind == 19: return 10
    if kind == 20: return 10
    if kind == 21: return 10
    if kind == 22: return 10
    return 3

def balanced(line):
    return line.count('"') % 2 == 0

rc = 0
for path in sys.argv[1:]:
    # join physical lines until quotes balance (W02 embeds a raw newline in t=)
    phys = []
    buf = ""
    for line in open(path, encoding="utf-8", errors="replace"):
        buf += line
        if balanced(buf.rstrip("\n")):
            phys.append(buf); buf = ""
    if buf: phys.append(buf)
    cur_t = None; cur_qid = None
    bad = 0; total = 0
    for line in phys:
        m = re.match(r'^[WQ] (\d+) (?:\[[A-Z0-9]+\] )?q="(.*)" t="(.*)" exp="(.*)"$', line.rstrip("\n"))
        if m:
            cur_qid, cur_t = m.group(1), m.group(3).encode()
            continue
        m = re.match(r'^INTAKE .*?kind=([A-Z0-9_]+) chunk=([A-Z0-9_>?]+)', line)
        if m and cur_t is not None:
            total += 1
            kind = KNAMES[m.group(1)]; chunk = m.group(2)
            exp = CNAMES[policy_winner(kind, text_shape(cur_t))]
            if chunk != exp:
                bad += 1
                print(f"{path}: MISMATCH qid={cur_qid} kind={kind} chunk={chunk} expected={exp}")
    print(f"{path}: audited={total} mismatches={bad}")
    rc = rc or (1 if bad else 0)
sys.exit(rc)
