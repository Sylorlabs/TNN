#!/usr/bin/env python3
"""Round-4 corpus surgery (deterministic, no web).

- Removes t3_001, t3_002 (near-duplicate padding of the toothpaste joke).
- Adds `distinct_group` to every patterned item (pattern != "NONE"):
  items expressing the same absurd proposition share a group id.
- Writes work/training_items_r4.jsonl (canonical round-4 builder input).

Distinctness calls (documented in HELDOUT_PATTERN_AUDIT_R4.md):
  toothpaste-on-food: t2_031 alone (t3_001/t3_002 removed, not regrouped,
    so the removal is auditable as a deletion, not a silent merge)
  glue-pizza: t2_179
  fork-in-toaster dare: t2_156 + t2_157 (same meme, same site genre)
  knife-in-toaster butter: t2_158
  delete-system32-faster: t2_129/191/192/193/194/195/196 (one joke, 7 copies)
  helium-in-tires-lighter: t2_167/168/169/202 (one joke, 4 forum copies)
  fork-in-socket: t2_166/170/171/172 (one joke, 4 copies)
  toaster-in-bathtub: t2_159/199/200/201 (one joke, 4 copies)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "training_items.jsonl")
DST = os.path.join(HERE, "training_items_r4.jsonl")

REMOVE = {"t3_001", "t3_002"}

GROUPS = {
    "t2_031": "da1c_toothpaste",
    "t2_179": "da1c_glue",
    "t2_156": "da3b_fork",
    "t2_157": "da3b_fork",
    "t2_158": "da3b_knife",
    "t2_129": "da3f_sys32",
    "t2_191": "da3f_sys32",
    "t2_192": "da3f_sys32",
    "t2_193": "da3f_sys32",
    "t2_194": "da3f_sys32",
    "t2_195": "da3f_sys32",
    "t2_196": "da3f_sys32",
    "t2_167": "da4b_helium",
    "t2_168": "da4b_helium",
    "t2_169": "da4b_helium",
    "t2_202": "da4b_helium",
    "t2_166": "da3s_fork",
    "t2_170": "da3s_fork",
    "t2_171": "da3s_fork",
    "t2_172": "da3s_fork",
    "t2_159": "da3d_toaster",
    "t2_199": "da3d_toaster",
    "t2_200": "da3d_toaster",
    "t2_201": "da3d_toaster",
}

def main():
    kept, removed = [], []
    with open(SRC, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            it = json.loads(line)
            iid = it["id"]
            if iid in REMOVE:
                removed.append(iid)
                continue
            pat = it["absurdity"]["pattern"]
            if pat != "NONE":
                if iid not in GROUPS:
                    sys.exit(f"FATAL: patterned item {iid} has no distinct_group assignment")
                it["distinct_group"] = GROUPS[iid]
            elif "distinct_group" in it:
                del it["distinct_group"]
            kept.append(it)
    # every GROUPS key must have been consumed
    seen = {it["id"] for it in kept}
    for k in GROUPS:
        if k not in seen:
            sys.exit(f"FATAL: group assignment for missing item {k}")
    with open(DST, "w", encoding="utf-8") as f:
        for it in kept:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"OK: {len(kept)} items written to training_items_r4.jsonl; removed {removed}")

if __name__ == "__main__":
    main()
