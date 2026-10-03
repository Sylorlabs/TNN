#!/usr/bin/env python3
"""Round-4 calibration prototype: contradiction-first joke classifier.

Mirrors the intended Zag classifier exactly (same fold, same whole-word
phrase matching, same decision order) so the later Zag build can be
checked against it. Python is transport/calibration only -- never in a
decision path.

Decision flow (ROUND2.md sec 5, composed with R6):
  1. fold text; match component-fact/action phrases (whole-word).
  2. R6 logic layer: if >=1 contradiction pattern (from the effective
     decision table) has ALL its codes hit -> logic verdict CONTRADICTS.
     r6_apply(CONTRADICTS) -> JOKING (contradiction outranks markers).
     (Local exact mirror of phase3/repairs/src/r6.zag r6_logic/r6_apply;
     the seeded C16 candidate is replaced by the joke contradiction
     table; disposition codes: 2=JOKING, 3=SATIRE, 5=UNCERTAIN.)
  3. logic UNKNOWN -> defer to marker layers:
       SAT markers >= 2 -> SATIRE
       TROPE markers >= 1 -> JOKING
       else -> UNCERTAIN
  SINCERE (1) and DECEPTIVE (4) are never emitted (withhold policy).

Usage:
  python3 work/r4_proto.py <training_corpus.json> <phrases_r4.json> \\
      <patterns_effective_r4.json> [out_report.json]
Prints a calibration summary; writes a per-item report if out given.
"""
import json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

INTENT = {2: "JOKING", 3: "SATIRE", 5: "UNCERTAIN"}

# Round-1 SAT marker list, unchanged (g_intent.zag, ns words).
SAT_MARKERS = ["area", "sources", "confirm", "says", "experts", "inside",
               "resident", "details", "developing", "press", "weigh", "study",
               "finds", "local", "time", "report", "full", "man", "woman",
               "peer", "pending", "review", "story", "nobody"]
# Round-1 TROPE marker list, unchanged (g_intent.zag, nt words).
TROPE_MARKERS = ["free", "ram", "upgrade", "ama", "findings", "joke",
                 "pet", "downloaded", "traveler"]

def fold(s):
    s = s.lower()
    return re.sub(r"\s+", " ", "".join(ch if 32 <= ord(ch) <= 126 else " " for ch in s)).strip()

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

# --- R6 bridge: exact mirror of phase3/repairs/src/r6.zag ---------------
# r6_logic: 0=UNKNOWN, 1=SUPPORTS, 2=CONTRADICTS.
# In the joke composition the "candidate" is the item and CONTRADICTS
# fires when >=1 contradiction pattern matches (replaces seeded C16).
def r6_logic(contradiction_fired):
    return 2 if contradiction_fired else 0

# r6_apply(logic_verdict, gated, evidence_disp) -> disposition.
# Dispositions here: 2=JOKING, 3=SATIRE, 5=UNCERTAIN(withhold).
def r6_apply(logic_verdict, gated, evidence_disp):
    if logic_verdict == 2:
        return 2  # CONTRADICTS > marker evidence -> JOKING
    if logic_verdict == 1:
        if gated != 0:
            return 5
        return evidence_disp
    return evidence_disp  # UNKNOWN defers to marker layers
# ------------------------------------------------------------------------

def match_codes(text_f, phrases):
    hits = {}
    for code in sorted(set(phrases["facts"]) | set(phrases["actions"])):
        plist = phrases["facts"].get(code) or phrases["actions"].get(code)
        found = sorted(p for p in plist if has_word(text_f, p))
        if found:
            hits[code] = found
    return hits

def fired_patterns(hits, table):
    out = []
    for pid in sorted(table):
        when = table[pid]["when"]
        if all(c in hits for c in when):
            out.append(pid)
    return out

def classify(text, phrases, table):
    t = fold(text)
    hits = match_codes(t, phrases)
    fired = fired_patterns(hits, table)
    logic_v = r6_logic(len(fired) > 0)
    markers = []
    for m in SAT_MARKERS:
        if has_word(t, m):
            markers.append("S:" + m)
    for m in TROPE_MARKERS:
        if has_word(t, m):
            markers.append("T:" + m)
    ns = sum(1 for m in markers if m.startswith("S:"))
    nt = sum(1 for m in markers if m.startswith("T:"))
    if ns >= 2:
        evidence_disp = 3
    elif nt >= 1:
        evidence_disp = 2
    else:
        evidence_disp = 5
    disp = r6_apply(logic_v, 0, evidence_disp)
    # ledger evidence: pattern IDs in rule field; matched phrases as markers
    ev_phrases = sorted({p for c in hits for p in hits[c]})
    return {
        "intent": INTENT[disp],
        "logic": logic_v,
        "fired": fired,
        "sat_n": ns,
        "trope_n": nt,
        "markers": markers,
        "ev_phrases": ev_phrases,
        "hit_codes": sorted(hits),
    }

def main():
    if len(sys.argv) < 4:
        print("usage: r4_proto.py <training_corpus.json> <phrases_r4.json> "
              "<patterns_effective_r4.json> [out_report.json]")
        sys.exit(1)
    raw_path = sys.argv[1]
    if raw_path.endswith(".jsonl"):
        items = [json.loads(ln) for ln in open(raw_path, encoding="utf-8")
                 if ln.strip()]
    else:
        items = json.load(open(raw_path, encoding="utf-8"))["items"]
    phrases = json.load(open(sys.argv[2], encoding="utf-8"))
    eff = json.load(open(sys.argv[3], encoding="utf-8"))
    table = eff["effective"] if "effective" in eff else eff
    per_item = []
    for it in items:
        r = classify(it["body"], phrases, table)
        r["id"] = it["id"]
        r["family"] = it["family"]
        r["label"] = it["label"]
        r["pattern"] = it.get("absurdity", {}).get("pattern", "NONE")
        per_item.append(r)

    # calibration summary (training only)
    byfam = Counter()
    catch = Counter()   # (family, label) -> predicted-correct count
    total = Counter()
    never_bad = True
    for r in per_item:
        key = (r["family"], r["label"])
        total[key] += 1
        ok = (r["intent"] == r["label"])
        if ok:
            catch[key] += 1
        if r["intent"] in ("SINCERE", "DECEPTIVE"):
            never_bad = False
        byfam[r["family"]] += 1

    print(f"items: {len(per_item)}")
    print(f"never-SINCERE/never-DECEPTIVE: {'PASS' if never_bad else 'FAIL'}")
    for key in sorted(total):
        print(f"  {key}: predicted==label {catch[key]}/{total[key]}")
    nf = sum(1 for r in per_item if r["fired"])
    print(f"contradiction fired on {nf}/{len(per_item)} items")
    # per-pattern sanity: does each effective pattern fire on >=1 training item?
    patfire = Counter(p for r in per_item for p in r["fired"])
    dead = [pid for pid in sorted(table) if patfire[pid] == 0]
    print(f"effective patterns: {len(table)}; never fired on training: {dead}")

    if len(sys.argv) >= 5:
        json.dump({"summary": {
                       "n": len(per_item),
                       "never_sincere_deceptive": never_bad,
                       "by_family_label": {f"{k[0]}/{k[1]}": [catch[k], total[k]]
                                           for k in sorted(total)},
                       "contradiction_fired": nf,
                       "dead_patterns": dead},
                   "items": per_item},
                  open(sys.argv[4], "w", encoding="utf-8"), indent=1)
        print(f"wrote {sys.argv[4]}")

if __name__ == "__main__":
    main()
