#!/usr/bin/env python3
"""Stage M2 Test-1 hard-item subset from the RESTORED battery.
Method: frozen 70%-overlap scorer tokenizer; hard = low Q/key distinctive-word
overlap (paraphrase payload / demand words absent from key). Output frozen list."""
import re, pathlib

REST = pathlib.Path("/home/hatch/workspace/growwithme_keyrepair/restored")
STOP = {"the","and","for","with","from","that","this","are","was","were","has","have",
"had","will","would","can","could","should","must","may","might","shall","not","no",
"yes","its","his","her","their","our","your","than","then","when","where","what",
"which","who","whom","whose","why","how","all","any","both","each","few","more",
"most","other","some","such","only","own","same","too","very","just","also","does",
"did","is","it","of","in","on","to","a","an","at","by","be","as","or","if"}

def normalize(s):
    s = s.lower()
    s = re.sub(r"[`'\"]", "", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def words(s):
    return [w for w in normalize(s).split() if len(w) > 3 and w not in STOP]

ITEM_RE = re.compile(r"^### (\S+).*?\n(?:(?:Pair|Target|Source)[^:\n]*: .*?\n)?Q: (.*?)\n(?:S7 key|Key): ([^\n]*)", re.M)

hard, total = [], 0
for s in range(1, 7):
    items = []
    for m in ITEM_RE.finditer((REST / f"immediate_S{s}.md").read_text()):
        qid = m.group(1)
        if qid.endswith("-Q"): qid = qid[:-2]
        items.append((qid, m.group(2).strip(), m.group(3).strip()))
    for qid, q, k in items:
        total += 1
        qw, kw = set(words(q)), set(words(k))
        ov = len(qw & kw) / len(qw) if qw else 0.0
        if ov < 0.5:
            hard.append((s, qid, round(ov, 2), q, k))

print(f"total immediate probes: {total}; hard (overlap<0.5): {len(hard)}")
print(f"{'sess':<5}{'id':<9}{'ov':<6}question")
for s, qid, ov, q, k in hard:
    print(f"S{s:<4}{qid:<9}{ov:<6}{q[:70]}")

with open("/home/hatch/workspace/growwithme_keyrepair/test1_hard_items.tsv", "w") as f:
    f.write("session\tprobe_id\tq_key_overlap\tquestion\tkey\n")
    for s, qid, ov, q, k in hard:
        f.write(f"S{s}\t{qid}\t{ov}\t{q}\t{k}\n".replace("\n", " "))
print("\nwrote test1_hard_items.tsv")
