#!/usr/bin/env python3
"""Assemble + validate the ROUND-4 training corpus.

Reads work/training_items_r4.jsonl (one JSON object per line), validates
every item, and writes corpus/training_corpus.json +
work/training_stats_r4.json + work/vocab_frozen_r4.json +
work/patterns_effective_r4.json.

Checks (all FATAL on failure):
 1. Schema: required fields; prov == "web"; label in
    {JOKING, SATIRE, DECEPTIVE, SINCERE}; absurdity has
    facts/actions/pattern/gloss; patterned items (pattern != "NONE")
    carry a non-empty distinct_group; NONE items carry none.
 2. Disjointness: folded body must not equal any round-2 held-out item
    text (corpus/heldout.json) nor any round-1 RECON item text.
 3. Annotation grounding: every annotated fact/action code must exist in
    work/phrases_r4.json (phrases_r2.json + documented round-4 additions)
    AND have >=1 of its phrases as a whole-word match in the folded body
    (Zag-faithful: ASCII-lower fold, non-alnum boundaries).
 4. Pattern grounding: if pattern != "NONE", every code named in the
    pattern must be in the item's facts+actions, and the pattern string
    must be a known decision-table key (work/patterns_r2.json).
 5. DISTINCT support rule (round-4 honesty fix): exemplars are counted
    per distinct_group, not per item. Codes with <4 DISTINCT groups are
    DROPPED from the frozen vocabulary (reported, not fatal); the
    effective decision table (work/patterns_effective_r4.json) keeps only
    patterns whose every code is retained.
 6. Items annotated with a dropped code: FATAL.

Usage: python3 work/build_training_r4.py   (run from round2/)
"""
import json, os, re, sys
from collections import Counter, defaultdict

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
    phrases = json.load(open(os.path.join(HERE, "phrases_r4.json")))
    act_ph = phrases["actions"]
    fact_ph = phrases["facts"]
    all_codes = set(act_ph) | set(fact_ph)
    table = json.load(open(os.path.join(HERE, "patterns_r2.json")))
    # patterns_r2.json is keyed by pattern ID (e.g. "P_DA1C"); item
    # annotations carry the code expression (e.g. "A_ADD & F_NOTFOOD").
    expr2id = {" & ".join(entry["when"]): pid for pid, entry in table.items()}

    held = json.load(open(os.path.join(ROOT, "corpus", "heldout.json")))["items"]
    held_texts = {fold(it["text"]) for it in held}
    R1_ROOT = os.path.dirname(ROOT)
    r1t = json.load(open(os.path.join(R1_ROOT, "corpus", "training_corpus.json")))
    recon_texts = {fold(it["body"]) for it in r1t["items"] if it.get("prov") == "recon"}

    items = []
    seen_ids = set()
    seen_groups = defaultdict(list)
    with open(os.path.join(HERE, "training_items_r4.jsonl"), encoding="utf-8") as f:
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
            if it["prov"] != "web":
                fail(f"line {ln} ({iid}): prov must be 'web', got {it['prov']!r}")
            if it["label"] not in INTENTS:
                fail(f"line {ln} ({iid}): bad label {it['label']}")
            ab = it["absurdity"]
            for k in ("facts", "actions", "pattern", "gloss"):
                if k not in ab:
                    fail(f"line {ln} ({iid}): absurdity missing {k}")
            pat = ab["pattern"]
            grp = it.get("distinct_group")
            if pat != "NONE":
                if not grp or not isinstance(grp, str):
                    fail(f"line {ln} ({iid}): patterned item needs distinct_group")
                if pat not in expr2id:
                    fail(f"line {ln} ({iid}): pattern {pat!r} not in decision table")
                seen_groups[grp].append(iid)
            else:
                if grp:
                    fail(f"line {ln} ({iid}): NONE-pattern item must not carry distinct_group")
            body_f = fold(it["body"])
            if len(body_f) < 12:
                fail(f"line {ln} ({iid}): body too short")
            if body_f in held_texts:
                fail(f"line {ln} ({iid}): body duplicates a held-out item")
            if body_f in recon_texts:
                fail(f"line {ln} ({iid}): body duplicates a round-1 RECON item")
            for code in ab["facts"] + ab["actions"]:
                if code not in all_codes:
                    fail(f"line {ln} ({iid}): unknown code {code}")
                plist = fact_ph.get(code) or act_ph.get(code)
                if not any(has_word(body_f, p) for p in plist):
                    fail(f"line {ln} ({iid}): code {code} has no phrase hit in body")
            if pat != "NONE":
                pcodes = [c.strip() for c in pat.replace("&", " ").split() if c.strip()]
                have = set(ab["facts"]) | set(ab["actions"])
                for c in pcodes:
                    if c not in have:
                        fail(f"line {ln} ({iid}): pattern code {c} not in facts/actions")
            items.append(it)

    # DISTINCT support rule: one exemplar per distinct_group per code.
    # (An item contributes its codes to its group; a group counts once.)
    group_codes = defaultdict(set)
    for it in items:
        if it["absurdity"]["pattern"] != "NONE":
            g = it["distinct_group"]
            for c in set(it["absurdity"]["facts"]) | set(it["absurdity"]["actions"]):
                group_codes[g].add(c)
    exemplars = Counter()
    for g, codes in group_codes.items():
        for c in codes:
            exemplars[c] += 1
    dropped = sorted(c for c, n in exemplars.items() if n < 4)
    kept = sorted(c for c, n in exemplars.items() if n >= 4)
    unused = sorted(all_codes - set(exemplars))

    for it in items:
        bad = [c for c in it["absurdity"]["facts"] + it["absurdity"]["actions"] if c in dropped]
        if bad:
            fail(f"{it['id']}: annotated with dropped code(s) {bad} -- re-annotate or drop the pattern")

    # effective decision table: patterns whose codes all survive
    kept_set = set(kept)
    effective = {}
    dropped_patterns = []
    for pname, pent in table.items():
        if all(c in kept_set for c in pent["when"]):
            effective[pname] = pent
        else:
            dropped_patterns.append(pname)

    fam = Counter((it["family"], it["label"]) for it in items)
    pats = Counter(it["absurdity"]["pattern"] for it in items)

    out = {
        "description": "phase-3 joke volume-training corpus, ROUND 4 (all real web; disjoint from held-out and round-1 RECON; distinct-group support rule)",
        "retrieved": "2026-09-23",
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
    with open(os.path.join(HERE, "vocab_frozen_r4.json"), "w", encoding="utf-8") as f:
        json.dump(vocab, f, indent=1)
        f.write("\n")

    with open(os.path.join(HERE, "patterns_effective_r4.json"), "w", encoding="utf-8") as f:
        json.dump(effective, f, indent=1)
        f.write("\n")

    stats = {
        "n_items": len(items),
        "by_family_label": {f"{a}/{b}": c for (a, b), c in sorted(fam.items())},
        "distinct_exemplars": dict(sorted(exemplars.items())),
        "dropped_codes": dropped,
        "unused_codes": unused,
        "patterns": dict(sorted(pats.items())),
        "effective_table": sorted(effective),
        "dropped_patterns": sorted(dropped_patterns),
        "n_distinct_groups": len(group_codes),
    }
    with open(os.path.join(HERE, "training_stats_r4.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=1)
        f.write("\n")

    print(f"OK: {len(items)} items, {len(group_codes)} distinct groups; "
          f"kept {len(kept)} codes; dropped codes {dropped}")
    print(f"effective patterns: {len(effective)}; dropped patterns: {dropped_patterns}")

if __name__ == "__main__":
    main()
