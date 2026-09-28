#!/usr/bin/env python3
"""Crew 3 re-seal audit v2: handles all md formats (Key:/S7 key:, Pair: lines,
-Q suffixes) and split agent-visible .q files."""
import re, hashlib, pathlib

BASE = pathlib.Path.home() / "workspace/growwithme_retry"
RS = BASE / "probes_resealed"
manifest = (RS / "MANIFEST.md").read_text()

blocks = []
for m in re.finditer(r"## (\S+)\nold Q: (.*?)\nnew Q: (.*?)\nsha256: `([0-9a-f]{64})`", manifest, re.DOTALL):
    blocks.append({"id": m.group(1), "old": m.group(2).strip(), "new": m.group(3).strip(), "sha": m.group(4)})
print(f"manifest blocks: {len(blocks)} (amendment claims 151 unique probes)")

bad_hash = [b["id"] for b in blocks if hashlib.sha256(b["new"].encode()).hexdigest() != b["sha"]]
print(f"[1] manifest hash mismatches: {len(bad_hash)}")

olds = {b["old"] for b in blocks}
reuse = [b["id"] for b in blocks if b["new"] in olds]
print(f"[2] new Q exactly reusing any old Q text: {len(reuse)}")

seen, dups = {}, []
for b in blocks:
    if b["new"] in seen: dups.append(b["id"])
    seen[b["new"]] = b["id"]
print(f"[2b] duplicate new Qs: {len(dups)}")

def parse_md(path):
    md = path.read_text()
    items = []
    for m in re.finditer(r"^### (\S+).*?\n(?:\w[^:\n]*: .*?\n)?Q: (.*?)\n(?:S7 key|Key): ([^\n]*)",
                         md, re.M):
        qid = m.group(1)
        if qid.endswith("-Q"): qid = qid[:-2]
        items.append((qid, m.group(2).strip(), m.group(3).strip()))
    return items

# map re-sealed md -> agent-visible .q file(s)
QMAP = {
    "immediate_S1": ["immediate_S1"], "immediate_S2": ["immediate_S2"],
    "immediate_S3": ["immediate_S3"], "immediate_S4": ["immediate_S4"],
    "immediate_S5": ["immediate_S5"], "immediate_S6": ["immediate_S6"],
    "S7_recall": ["S7_recall"], "composition": ["composition"],
    "corrections_pending_falsehoods": ["corrections", "pending", "falsehoods"],
    "dependency_contradiction": ["dependency_pre_S4", "dependency_post_S7", "contradiction_resolution"],
}
issues, total_q, total_md = [], 0, 0
for stem, qnames in QMAP.items():
    items = parse_md(RS / f"{stem}.md")
    total_md += len(items)
    qlines = []
    for qn in qnames:
        qf = BASE / "probes" / f"{qn}.q"
        if not qf.exists():
            issues.append(f"{qn}.q MISSING"); continue
        qlines += [l[5:].strip() for l in qf.read_text().splitlines() if l.startswith("Q || ")]
        if "Key:" in qf.read_text() or "S7 key:" in qf.read_text():
            issues.append(f"{qn}.q contains key material")
    total_q += len(qlines)
    if len(qlines) != len(items):
        issues.append(f"{stem}: md={len(items)} vs .q={len(qlines)}")
        continue
    md_qs = {q for _, q, _ in items}
    for ql in qlines:
        if ql not in md_qs:
            issues.append(f"{stem}: .q line not in re-sealed md: {ql[:60]!r}")
print(f"[3] md items={total_md} .q lines={total_q} issues={len(issues)}")
for i in issues[:12]: print("   " + i)

# [4] old Q texts vs frozen probe mds
old_qs = {}
for p in (BASE / "_src/docs/lab/growwithme/frozen/probes").glob("*.md"):
    for m in re.finditer(r"^### (\S+).*?\n(?:(?:Pair|Target)[^:\n]*: .*?\n)?Q: (.*?)\n(?:S7 key|Key): ",
                         p.read_text(), re.M):
        qid = m.group(1)
        if qid.endswith("-Q"): qid = qid[:-2]
        old_qs[qid] = m.group(2).strip()
print(f"[4] frozen old Qs indexed: {len(old_qs)}")
unmatched = [b["id"] for b in blocks if b["id"] not in old_qs]
print(f"    manifest IDs with no frozen old Q: {len(unmatched)} {unmatched[:10]}")
mism = [b["id"] for b in blocks if b["id"] in old_qs and old_qs[b["id"]] != b["old"]]
print(f"    manifest old-Q text != frozen old Q: {len(mism)} {mism[:10]}")

# [5] keys: re-sealed md keys vs frozen keys (original, or S7-corrected where applicable)
old_keys = {}
for p in (BASE / "_src/docs/lab/growwithme/frozen/probes").glob("*.md"):
    for m in re.finditer(r"^### (\S+).*?\n(?:(?:Pair|Target)[^:\n]*: .*?\n)?Q: .*?\n(?:S7 key|Key): ([^\n]*)",
                         p.read_text(), re.M):
        qid = m.group(1)
        if qid.endswith("-Q"): qid = qid[:-2]
        old_keys[qid] = m.group(2).split("\n")[0].strip()
key_bad = 0
for stem in QMAP:
    for qid, newq, key in parse_md(RS / f"{stem}.md"):
        if qid not in old_keys or old_keys[qid] != key:
            key_bad += 1
print(f"[5] re-sealed keys differing from frozen keys: {key_bad}")
print(f"    (S7 keys are EXPECTED to differ on the 6 corrected facts)")
