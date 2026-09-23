#!/usr/bin/env python3
"""Extract ported S5 functions from both sources, normalize renames, diff."""
import re, sys

PORTED = ["sc_alloc","sc_g32","sc_s32","sc_g64","sc_s64","sc_g16","sc_s16",
          "sc_store_init","sc_slot_chunk","sc_id2slot_get","sc_wval","sc_rval",
          "sc_pick_width","sc_compact_and_seal","sc_event_grow","sc_event_append",
          "sc_episode","sc_add","sc_recall","sc_seal_tail","sc_seal_final"]

# s5 original names -> ingest names
RENAME = {
    "t_compact_and_seal": "sc_compact_and_seal",
    "t_event_grow": "sc_event_grow",
    "t_event_append": "sc_event_append",
    "t_episode": "sc_episode",
    "t_add": "sc_add",
    "t_recall": "sc_recall",
    "t_seal_tail": "sc_seal_tail",
    "t_seal_final": "sc_seal_final",
    "t_slot_chunk": "sc_slot_chunk",
    "t_id2slot_get": "sc_id2slot_get",
    "t_wval": "sc_wval",
    "t_rval": "sc_rval",
    "t_pick_width": "sc_pick_width",
    "t_store_init": "sc_store_init",
    "t_alloc": "sc_alloc",
    "TStore": "ScStore",
}

def get_fns(path):
    src = open(path).read()
    fns = {}
    for m in re.finditer(r"^fn (\w+)\(", src, re.M):
        name = m.group(1)
        start = m.start()
        # find matching closing brace at col 0
        depth = 0
        i = src.index("{", m.end())
        j = i
        instr = False
        while True:
            c = src[j]
            if c == '"' and src[j-1] != '\\':
                instr = not instr
            if not instr:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        break
            j += 1
        fns[name] = src[start:j+1]
    return fns

s5 = get_fns("/home/hatch/workspace/tnn-lab/ops/storage-compression/src/s5_learner.zag")
ig = get_fns("/home/hatch/workspace/tnn-lab/knowledge/ingest_1gb/build/ingest.zag")

def norm(body):
    for a, b in RENAME.items():
        body = body.replace(a, b)
    # normalize whitespace runs
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n\s*\n", "\n", body)
    return body.strip()

ndiff = 0
for name in PORTED:
    s5name = name
    # find original name
    orig = None
    for o in s5:
        test = o
        for a, b in RENAME.items():
            test = test.replace(a, b)
        if test == name:
            orig = o
            break
    if orig is None:
        print(f"MISSING in s5: {name}")
        ndiff += 1
        continue
    if name not in ig:
        print(f"MISSING in ingest: {name}")
        ndiff += 1
        continue
    a, b = norm(s5[orig]), norm(ig[name])
    if a != b:
        print(f"DIFF in {name} (s5:{orig}):")
        al, bl = a.split("\n"), b.split("\n")
        import difflib
        for dl in list(difflib.unified_diff(al, bl, lineterm=""))[:20]:
            print("   ", dl)
        ndiff += 1
    else:
        print(f"IDENTICAL: {name}")
print(f"\n{ndiff} functions differ/missing of {len(PORTED)}")
