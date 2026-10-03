#!/usr/bin/env python3
"""Independent key-diff: re-sealed keys (b825f54dd) vs frozen keys (origin head).
Suite-scoped (file-stem, probe-id). Step 1: inventory + collision check."""
import re, pathlib

FROZ = pathlib.Path("/tmp/gwm/frozen")
RS = pathlib.Path("/tmp/gwm/resealed")

def parse(path):
    md = path.read_text()
    items = []
    # header lines like "### COMP-01-Q" or "### CORR-01 (targets C1 ...)" then optional Pair:/Target: line, Q:, Key:
    for m in re.finditer(
        r"^### (\S+).*?\n(?:(?:Pair|Target|Source)[^:\n]*: .*?\n)?Q: (.*?)\n(?:S7 key|Key): ([^\n]*)",
        md, re.M):
        qid = m.group(1)
        if qid.endswith("-Q"):
            qid = qid[:-2]
        # strip parenthetical like " (targets C1 ...)"? keep full for display, key on base
        base = qid.split()[0]
        items.append({"raw": qid, "id": base, "q": m.group(2).strip(), "key": m.group(3).strip()})
    return items

FZMAP = {
    "immediate_S1": ["immediate_S1"], "immediate_S2": ["immediate_S2"],
    "immediate_S3": ["immediate_S3"], "immediate_S4": ["immediate_S4"],
    "immediate_S5": ["immediate_S5"], "immediate_S6": ["immediate_S6"],
    "composition": ["composition"],
    "corrections_pending_falsehoods": ["corrections", "pending", "falsehoods"],
    "dependency_contradiction": ["dependency_pre_S4", "dependency_post", "contradiction_resolution"],
    "S7_recall": ["S7_recall"],
}

frozen = {}
for f in FROZ.glob("*.md"):
    frozen[f.stem] = parse(f)

print("=== frozen inventory ===")
for stem in sorted(frozen):
    ids = [i["id"] for i in frozen[stem]]
    print(f"  {stem}: {len(ids)} items")

print("\n=== re-sealed inventory ===")
rs_items = {}
for stem in FZMAP:
    items = parse(RS / f"{stem}.md")
    rs_items[stem] = items
    ids = [i["id"] for i in items]
    dupes = {x for x in ids if ids.count(x) > 1}
    print(f"  {stem}: {len(items)} items" + (f" DUPES={dupes}" if dupes else ""))

print("\n=== cross-file ID collisions in frozen maps ===")
for stem, fzstems in FZMAP.items():
    if len(fzstems) < 2:
        continue
    seen = {}
    for fz in fzstems:
        for i in frozen[fz]:
            seen.setdefault(i["id"], []).append(fz)
    coll = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"  {stem}: {len(coll)} colliding ids" + (f" {list(coll)[:6]}" if coll else ""))

print("\n=== re-sealed ids with no frozen counterpart (suite-scoped) ===")
for stem in FZMAP:
    for i in rs_items[stem]:
        hits = [(fz, k) for fz in FZMAP[stem] for k in [None]
                for k in [next((x["key"] for x in frozen[fz] if x["id"] == i["id"]), None)]
                if k is not None]
        if not hits:
            print(f"  MISSING: {stem}/{i['id']}")
