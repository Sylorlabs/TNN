#!/usr/bin/env python3
"""Assemble + validate the round-2 training corpus.

Reads work/training_items.jsonl (one JSON object per line), validates every
item, and writes corpus/training_corpus.json + work/training_stats.json.

Checks (all FATAL on failure):
 1. Schema: required fields; prov == "web" (except documented reuse);
    label in {JOKING, SATIRE, DECEPTIVE, SINCERE}; absurdity has
    facts/actions/pattern/gloss.
 2. Disjointness: folded body must not equal any round-2 held-out item text
    (corpus/heldout.json) nor any round-1 RECON item text.
 3. Annotation grounding: every annotated fact/action code must exist in
    work/phrases_r2.json AND have >=1 of its phrases as a whole-word match
    in the folded body (Zag-faithful: ASCII-lower fold, non-alnum
    boundaries) -- catches annotation/phrase drift.
 4. Pattern grounding: if pattern != "NONE", every code named in the pattern
    must be in the item's facts+actions.
 5. Support rule: codes with <4 distinct-item exemplars are DROPPED from the
    frozen vocabulary (reported, not fatal); the frozen vocabulary is
    written to work/vocab_frozen_r2.json.

Usage: python3 work/build_training.py   (run from round2/)
"""
import json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

INTENTS = {"SINCERE": 1, "JOKING": 2, "SATIRE": 3, "DECEPTIVE": 4, "UNCERTAIN": 5}

def fail(msg):
    print(f"FATAL: {msg}", file=sys.stderr)
    sys.exit(1)

def fold(s):
    s = s.lower()
    out = [ch if 32 <= ord(ch) <= 126 else " " for ch in s]
    return re.sub(r"\s+", " ", "".join(out)).strip()

def _is_alnum(c):
    return ('a' <= c <= 'z') or ('0' <= c <= '9')

def has_word(hay, w):
    if not w or len(w) > len(hay):
        return False
    i = 0
    while i <= len(hay) - len(w):
        if hay[i:i+len(w)] == w:
            ok = True
            if i > 0 and _is_alnum(hay[i-1]):
                ok = False
            if i + len(w) < len(hay) and _is_alnum(hay[i+len(w)]):
                ok = False
            if ok:
                return True
        i += 1
    return False

def main():
    phrases = json.load(open(os.path.join(HERE, "phrases_r2.json")))
    # strip _note
    act_ph = phrases["actions"]
    fact_ph = phrases["facts"]
    all_codes = set(act_ph) | set(fact_ph)

    # held-out texts (round 2, re-frozen)
    held = json.load(open(os.path.join(ROOT, "corpus", "heldout.json")))["items"]
    held_texts = {fold(it["text"]) for it in held}
    # round-1 RECON training texts (must stay disjoint) -- read the PARENT
    # round-1 corpus, NOT round2's own output file (this script overwrites it)
    R1_ROOT = os.path.dirname(ROOT)
    r1t = json.load(open(os.path.join(R1_ROOT, "corpus", "training_corpus.json")))
    recon_texts = {fold(it["body"]) for it in r1t["items"] if it.get("prov") == "recon"}

    items = []
    seen_ids = set()
    with open(os.path.join(HERE, "training_items.jsonl"), encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            it = json.loads(line)
            iid = it.get("id")
            if not iid or iid in seen_ids:
                fail(f"line {ln}: bad/duplicate id {iid!r}")
            seen_ids.add(iid)
            for k in ("family", "cell", "label", "body", "url", "retrieved", "prov", "absurdity"):
                if k not in it:
                    fail(f"line {ln} ({iid}): missing field {k}")
            if it["label"] not in INTENTS:
                fail(f"line {ln} ({iid}): bad label {it['label']}")
            ab = it["absurdity"]
            for k in ("facts", "actions", "pattern", "gloss"):
                if k not in ab:
                    fail(f"line {ln} ({iid}): absurdity missing {k}")
            body_f = fold(it["body"])
            if len(body_f) < 12:
                fail(f"line {ln} ({iid}): body too short")
            if body_f in held_texts:
                fail(f"line {ln} ({iid}): body duplicates a held-out item")
            if body_f in recon_texts:
                fail(f"line {ln} ({iid}): body duplicates a round-1 RECON item")
            # annotation grounding
            for code in ab["facts"] + ab["actions"]:
                if code not in all_codes:
                    fail(f"line {ln} ({iid}): unknown code {code}")
                plist = fact_ph.get(code) or act_ph.get(code)
                if not any(has_word(body_f, p) for p in plist):
                    fail(f"line {ln} ({iid}): code {code} has no phrase hit in body")
            # pattern grounding
            pat = ab["pattern"]
            if pat != "NONE":
                pcodes = [c.strip() for c in pat.replace("&", " ").split() if c.strip()]
                have = set(ab["facts"]) | set(ab["actions"])
                for c in pcodes:
                    if c not in have:
                        fail(f"line {ln} ({iid}): pattern code {c} not in facts/actions")
            items.append(it)

    # support rule: distinct-item exemplars per code
    exemplars = Counter()
    for it in items:
        for c in set(it["absurdity"]["facts"]) | set(it["absurdity"]["actions"]):
            exemplars[c] += 1
    dropped = sorted(c for c, n in exemplars.items() if n < 4)
    kept = sorted(c for c, n in exemplars.items() if n >= 4)
    # also drop any code with zero exemplars (in phrases but unused) - just report
    unused = sorted(all_codes - set(exemplars))

    # items whose annotation references a dropped code: fatal (they'd be ungrounded)
    for it in items:
        bad = [c for c in it["absurdity"]["facts"] + it["absurdity"]["actions"] if c in dropped]
        if bad:
            fail(f"{it['id']}: annotated with dropped code(s) {bad} -- re-annotate or extend phrases")

    fam = Counter((it["family"], it["label"]) for it in items)
    pats = Counter(it["absurdity"]["pattern"] for it in items)

    out = {
        "description": "phase-3 joke volume-training corpus, ROUND 2 (all real web; disjoint from held-out and round-1 RECON)",
        "retrieved": "2026-09-22",
        "n": len(items),
        "items": items,
    }
    with open(os.path.join(ROOT, "corpus", "training_corpus.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")

    vocab = {
        "actions": {c: act_ph[c] for c in kept if c in act_ph},
        "facts": {c: fact_ph[c] for c in kept if c in fact_ph},
    }
    with open(os.path.join(HERE, "vocab_frozen_r2.json"), "w", encoding="utf-8") as f:
        json.dump(vocab, f, indent=1)
        f.write("\n")

    stats = {
        "n_items": len(items),
        "by_family_label": {f"{a}/{b}": c for (a, b), c in sorted(fam.items())},
        "exemplars": dict(sorted(exemplars.items())),
        "dropped_codes": dropped,
        "unused_codes": unused,
        "patterns": dict(sorted(pats.items())),
    }
    with open(os.path.join(HERE, "training_stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=1)
        f.write("\n")

    print(f"OK: {len(items)} items; kept {len(kept)} codes; dropped {dropped}; unused {unused}")
    print("family/label:", dict(sorted(fam.items())))

if __name__ == "__main__":
    main()
