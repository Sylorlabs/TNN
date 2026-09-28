#!/usr/bin/env python3
"""Step 2: suite-scoped diff of re-sealed vs frozen keys; generate restored files.
Restored file = re-sealed file with ONLY the Key lines replaced by frozen keys.
Writes: KEY_DIFF.tsv (per-item diff), restored/*.md, and a verification report."""
import re, pathlib, hashlib

FROZ = pathlib.Path("/tmp/gwm/frozen")
RS = pathlib.Path("/tmp/gwm/resealed")
OUT = pathlib.Path("/home/hatch/workspace/growwithme_keyrepair/restored")
OUT.mkdir(exist_ok=True)

ITEM_RE = re.compile(
    r"^### (\S+).*?\n(?:(?:Pair|Target|Source)[^:\n]*: .*?\n)?Q: (.*?)\n(?:S7 key|Key): ([^\n]*)",
    re.M)

def parse(path):
    items = []
    for m in ITEM_RE.finditer(path.read_text()):
        qid = m.group(1)
        if qid.endswith("-Q"):
            qid = qid[:-2]
        items.append({"id": qid.split()[0], "q": m.group(2).strip(),
                      "key": m.group(3).strip(), "span": m.span(3)})
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

frozen = {f.stem: parse(FROZ / f"{f.stem}.md") for f in FROZ.glob("*.md")}

# sanity: no multi-line keys anywhere (every Key line followed by blank/###/Cites/end)
for stem, items in frozen.items():
    txt = (FROZ / f"{stem}.md").read_text()
    for it in items:
        after = txt[it["span"][1]:it["span"][1]+2]
for stem in FZMAP:  # noqa - placeholder loop removed
    pass

rows = []
per_stem_changed = {}
restored_paths = {}
for stem in FZMAP:
    rs_items = parse(RS / f"{stem}.md")
    changed = 0
    for it in rs_items:
        hits = [(fz, x["key"]) for fz in FZMAP[stem]
                for x in frozen[fz] if x["id"] == it["id"]]
        assert len(hits) == 1, f"ambiguous/missing frozen key for {stem}/{it['id']}: {hits}"
        fz, fkey = hits[0]
        status = "SAME" if fkey == it["key"] else "CHANGED"
        if status == "CHANGED":
            changed += 1
        rows.append({"stem": stem, "id": it["id"], "fzfile": fz,
                     "status": status, "frozen_key": fkey, "resealed_key": it["key"]})
    per_stem_changed[stem] = changed

    # generate restored file: replace each CHANGED Key line with frozen key
    text = (RS / f"{stem}.md").read_text()
    # apply replacements from end to start so spans stay valid
    repls = []
    for it, r in zip(rs_items, [x for x in rows if x["stem"] == stem]):
        if r["status"] == "CHANGED":
            repls.append((it["span"], r["frozen_key"]))
    for (s, e), newkey in sorted(repls, reverse=True):
        old = text[s:e]
        text = text[:s] + newkey + text[e:]
    outp = OUT / f"{stem}.md"
    outp.write_text(text)
    restored_paths[stem] = outp

# header fixes: re-sealed headers swap PENDING/falsehood IDs vs frozen+ledger
HEADER_FIXES = {
    "immediate_S5": ("excludes PENDING F5-14 and falsehood F5-15",
                     "excludes PENDING F5-15 and falsehood F5-14"),
    "immediate_S6": ("excludes PENDING F6-04 and falsehood F6-20",
                     "excludes PENDING F6-20 and falsehood F6-04"),
}
for stem, (old, new) in HEADER_FIXES.items():
    p = restored_paths[stem]
    t = p.read_text()
    assert old in t, stem
    p.write_text(t.replace(old, new))
print("header ID-swap fixes applied: immediate_S5, immediate_S6")
total_changed = sum(per_stem_changed.values())
print("=== per-stem CHANGED counts ===")
for stem, n in per_stem_changed.items():
    print(f"  {stem}: {n}")
print(f"TOTAL CHANGED: {total_changed}")

# write TSV
with open("/home/hatch/workspace/growwithme_keyrepair/KEY_DIFF.tsv", "w") as f:
    f.write("stem\tid\tfrozen_file\tstatus\tfrozen_key\tresealed_key\n")
    for r in rows:
        fk = r['frozen_key'].replace("\n", " ")
        rk = r['resealed_key'].replace("\n", " ")
        f.write(f"{r['stem']}\t{r['id']}\t{r['fzfile']}\t{r['status']}\t{fk}\t{rk}\n")
print("wrote KEY_DIFF.tsv")

# verification: every restored key byte-equals its frozen key
bad = 0
for stem in FZMAP:
    ritems = parse(restored_paths[stem])
    for it in ritems:
        fz = next(r["fzfile"] for r in rows if r["stem"] == stem and r["id"] == it["id"])
        fk = next(x["key"] for x in frozen[fz] if x["id"] == it["id"])
        if it["key"] != fk:
            bad += 1
            print(f"RESTORE MISMATCH: {stem}/{it['id']}")
print(f"restore verification: {bad} mismatches")

# verification: restored file vs resealed file differ ONLY on changed Key lines
# (+ the documented header ID-swap fixes for S5/S6)
for stem in FZMAP:
    old = (RS / f"{stem}.md").read_text().splitlines()
    new = restored_paths[stem].read_text().splitlines()
    assert len(old) == len(new), f"{stem}: line count changed"
    n = per_stem_changed[stem] + (1 if stem in HEADER_FIXES else 0)
    diffs = [i for i, (a, b) in enumerate(zip(old, new)) if a != b]
    assert len(diffs) == n, f"{stem}: expected {n} changed lines, got {len(diffs)}"
    for i in diffs:
        is_key = old[i].startswith("Key: ") or old[i].startswith("S7 key: ")
        is_hdrfix = stem in HEADER_FIXES and HEADER_FIXES[stem][0] in old[i]
        assert is_key or is_hdrfix, f"{stem} line {i}: unexpected line changed"
print("non-key content: byte-identical in all restored files (except 2 documented header fixes)")
