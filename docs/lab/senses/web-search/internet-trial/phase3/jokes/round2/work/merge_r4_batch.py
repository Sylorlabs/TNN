#!/usr/bin/env python3
"""Merge a round-4 collection batch into the corpus inputs.

Usage: python3 work/merge_r4_batch.py work/r4_batch_NN.jsonl

Validates each item (schema, id uniqueness vs training_items_r4.jsonl,
annotation grounding against work/phrases_r4.json, pattern grounding vs
work/patterns_r2.json, distinct_group present, disjointness vs held-out
and round-1 RECON), appends to work/training_items_r4.jsonl and to
work/r4_new.jsonl (the round-4-only audit trail). Refuses to run if the
batch contains an id already present.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INTENTS = {"SINCERE": 1, "JOKING": 2, "SATIRE": 3, "DECEPTIVE": 4, "UNCERTAIN": 5}

def fail(msg):
    print(f"FATAL: {msg}", file=sys.stderr); sys.exit(1)

def fold(s):
    s = s.lower()
    return re.sub(r"\s+", " ", "".join(ch if 32 <= ord(ch) <= 126 else " " for ch in s)).strip()

def _is_alnum(c): return ('a' <= c <= 'z') or ('0' <= c <= '9')

def has_word(hay, w):
    if not w or len(w) > len(hay): return False
    i = 0
    while i <= len(hay) - len(w):
        if hay[i:i+len(w)] == w:
            ok = True
            if i > 0 and _is_alnum(hay[i-1]): ok = False
            if i + len(w) < len(hay) and _is_alnum(hay[i+len(w)]): ok = False
            if ok: return True
        i += 1
    return False

def main():
    if len(sys.argv) != 2: fail("usage: merge_r4_batch.py work/r4_batch_NN.jsonl")
    batch_p = sys.argv[1]
    phrases = json.load(open(os.path.join(HERE, "phrases_r4.json")))
    act_ph, fact_ph = phrases["actions"], phrases["facts"]
    all_codes = set(act_ph) | set(fact_ph)
    table = json.load(open(os.path.join(HERE, "patterns_r2.json")))
    expr2id = {" & ".join(entry["when"]): pid for pid, entry in table.items()}
    pat_expr = None
    held = json.load(open(os.path.join(ROOT, "corpus", "heldout.json")))["items"]
    held_texts = {fold(it["text"]) for it in held}
    r1t = json.load(open(os.path.join(os.path.dirname(ROOT), "corpus", "training_corpus.json")))
    recon_texts = {fold(it["body"]) for it in r1t["items"] if it.get("prov") == "recon"}

    existing_ids = set()
    with open(os.path.join(HERE, "training_items_r4.jsonl"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line: existing_ids.add(json.loads(line)["id"])

    new_items = []
    with open(batch_p, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line: continue
            it = json.loads(line)
            iid = it.get("id")
            if not iid or iid in existing_ids or any(x["id"] == iid for x in new_items):
                fail(f"batch line {ln}: bad/duplicate id {iid!r}")
            for k in ("family", "cell", "label", "body", "url", "retrieved", "prov", "absurdity"):
                if k not in it: fail(f"{iid}: missing field {k}")
            if it["prov"] != "web": fail(f"{iid}: prov must be web")
            if it["label"] not in INTENTS: fail(f"{iid}: bad label")
            ab = it["absurdity"]
            for k in ("facts", "actions", "pattern", "gloss"):
                if k not in ab: fail(f"{iid}: absurdity missing {k}")
            pat = ab["pattern"]
            if pat == "NONE": fail(f"{iid}: round-4 batches must be patterned (NONE not allowed here)")
            if pat not in expr2id: fail(f"{iid}: pattern {pat!r} not in decision table")
            pat_id = expr2id[pat]  # noqa: F841 (kept for audit clarity)
            if not it.get("distinct_group"): fail(f"{iid}: missing distinct_group")
            body_f = fold(it["body"])
            if len(body_f) < 12: fail(f"{iid}: body too short")
            if body_f in held_texts: fail(f"{iid}: duplicates a held-out item")
            if body_f in recon_texts: fail(f"{iid}: duplicates a round-1 RECON item")
            for code in ab["facts"] + ab["actions"]:
                if code not in all_codes: fail(f"{iid}: unknown code {code}")
                plist = fact_ph.get(code) or act_ph.get(code)
                if not any(has_word(body_f, p) for p in plist):
                    fail(f"{iid}: code {code} has no phrase hit in body")
            pcodes = [c.strip() for c in pat.replace("&", " ").split() if c.strip()]
            have = set(ab["facts"]) | set(ab["actions"])
            for c in pcodes:
                if c not in have: fail(f"{iid}: pattern code {c} not in facts/actions")
            new_items.append(it)

    with open(os.path.join(HERE, "training_items_r4.jsonl"), "a", encoding="utf-8") as f:
        for it in new_items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    with open(os.path.join(HERE, "r4_new.jsonl"), "a", encoding="utf-8") as f:
        for it in new_items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"OK: merged {len(new_items)} items from {os.path.basename(batch_p)}")

if __name__ == "__main__":
    main()
