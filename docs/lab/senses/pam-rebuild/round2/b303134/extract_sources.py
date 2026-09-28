#!/usr/bin/env python3
"""B-303134 source extraction. Pulls H-30/31/34 definitions, narrowed scopes,
cheap-probe results, J/K/L/M classes from the frozen Round-C doc, and N/O/P
classes from the frozen evidence commits — by script, no transcription."""
import re, sys

SRC = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/round_c/HYPOTHESES_ROUND_C.md"
GROK = "/home/hatch/workspace/tmp_commit/grok_r2.md"
RTS = "/home/hatch/workspace/tmp_commit/verdict_rts.md"
OUT = "/home/hatch/workspace/b303134/EXTRACTED_SOURCES.md"

doc = open(SRC).read()

def section(doc, num, title):
    # capture from "## <num>. <title>" to the next "## " heading
    pat = re.compile(r"^## %s\. %s.*?\n(.*?)(?=^## \d+\. |\Z)" % (num, re.escape(title)),
                     re.M | re.S)
    m = pat.search(doc)
    assert m, f"section {num} {title} not found"
    return m.group(0).strip()

parts = []
parts.append("# B-303134 EXTRACTED SOURCES (script-extracted, not transcribed)\n")
parts.append("Source: HYPOTHESES_ROUND_C.md (Round-C commits 0db769f2 + 64daa8b6)\n")
for num, title in [("2","H-PAM-30"),("3","H-PAM-31"),("6","H-PAM-34"),
                   ("9","Conjunctions"),("10","Fixture-class")]:
    parts.append(section(doc, num, title))
    parts.append("\n")

grok = open(GROK).read()
for head in ["### Class-N", "### Class-O", "### Class-P"]:
    i = grok.find(head)
    assert i >= 0, head
    j = grok.find("### What grok is NOT claiming", i)
    seg = grok[i:j].strip()
    parts.append(f"\n# {head} (from GROK_OBJECTOR_R2.md @ 36b1d5fc2)\n\n{seg}\n")

rts = open(RTS).read()
parts.append("\n# RT-S battery numbers (from VERDICT_RT_S.md @ 9f8ff63b)\n\n")
i = rts.find("## Battery results")
parts.append(rts[i:rts.find("## What each kill means")].strip() + "\n")

open(OUT, "w").write("\n".join(parts))
print("wrote", OUT, len(open(OUT).read()), "chars")
