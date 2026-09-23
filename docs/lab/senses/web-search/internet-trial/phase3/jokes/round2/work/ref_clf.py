#!/usr/bin/env python3
"""Reference implementation of the round-5 contradiction-first classifier.

TRANSPORT ONLY: used to (a) verify the generated Zag binaries agree
byte-for-byte on RS lines, and (b) produce the per-item miss analysis.
The gate decision path is the Zag binary; this file never feeds it.
"""
import json, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
R2 = os.path.dirname(HERE)

def fold(s):
    s = s.lower()
    out = [ch if 32 <= ord(ch) <= 126 else " " for ch in s]
    return re.sub(r"\s+", " ", "".join(out)).strip()

def has_word(hay, w):
    if not w or len(w) > len(hay):
        return False
    i = 0
    while i <= len(hay) - len(w):
        if hay[i:i+len(w)] == w:
            ok = True
            if i > 0 and hay[i-1].isalnum():
                ok = False
            if i + len(w) < len(hay) and hay[i+len(w)].isalnum():
                ok = False
            if ok:
                return True
        i += 1
    return False

SAT = ("area sources confirm says experts inside resident details developing "
       "press weigh study finds local time report full man woman peer pending "
       "review story nobody").split()
TROPE = "free ram upgrade ama findings joke pet downloaded traveler".split()

INTENT = {1: "SINCERE", 2: "JOKING", 3: "SATIRE", 4: "DECEPTIVE", 5: "UNCERTAIN"}

class Classifier:
    def __init__(self, phrases, patterns, active_patterns=None):
        self.phrases = phrases  # {"actions": {code:[phrases]}, "facts": {...}}
        self.patterns = patterns
        self.active = active_patterns or list(patterns.keys())

    def code_hits(self, text):
        """code -> list of matched phrases (whole-word, folded)."""
        hits = {}
        for grp in ("actions", "facts"):
            for code, plist in self.phrases[grp].items():
                mh = [p for p in plist if has_word(text, fold(p))]
                if mh:
                    hits[code] = mh
        return hits

    def classify(self, text):
        t = fold(text)
        hits = self.code_hits(t)
        fired = None
        for pname in self.patterns:
            if pname not in self.active:
                continue
            when = self.patterns[pname]["when"]
            if all(c in hits for c in when):
                fired = pname
                break
        markers = []
        for code in sorted(hits):
            markers.extend(hits[code])
        # R6 bridge: contradiction=CONTRADICTS(2); markers=SUPPORTS(1); else UNKNOWN(0)
        # SUPPORTS cannot install (never-SINCERE); UNKNOWN defers to evidence.
        if fired is not None:
            logic = 2
            intent = 2  # JOKING
            codes = fired
        else:
            ns = sum(1 for w in SAT if has_word(t, w))
            nt = sum(1 for w in TROPE if has_word(t, w))
            sat_hits = [w for w in SAT if has_word(t, w)]
            trope_hits = [w for w in TROPE if has_word(t, w)]
            markers.extend(sat_hits + trope_hits)
            if ns >= 2:
                logic = 1
                intent = 3  # SATIRE
                codes = "R_SATIRE"
            elif nt >= 1:
                logic = 1
                intent = 2  # JOKING
                codes = "R_TROPE"
            else:
                logic = 0
                intent = 5  # UNCERTAIN
                codes = "R_NO_PATTERN"
        return {"intent": intent, "codes": codes, "markers": markers,
                "fired": fired, "hits": hits, "logic": logic}

def main():
    cfg = sys.argv[1] if len(sys.argv) > 1 else "A"
    flags = json.load(open(os.path.join(HERE, "provenance_flags.json"), encoding="utf-8"))
    phrases = json.load(open(os.path.join(HERE, "phrases_r4.json"), encoding="utf-8"))
    patterns = json.load(open(os.path.join(HERE, "patterns_r2.json"), encoding="utf-8"))
    if cfg == "B":
        active = flags["configB_patterns"]
    elif cfg == "C":
        active = [p for p in patterns if p not in flags["H_patterns"]]
        # drop H-flagged phrases
        hph = set(flags["H_phrases"])
        for grp in ("actions", "facts"):
            for code in phrases[grp]:
                phrases[grp][code] = [p for p in phrases[grp][code] if p not in hph]
    else:
        active = list(patterns.keys())
    clf = Classifier(phrases, patterns, active)
    held = json.load(open(os.path.join(R2, "corpus", "heldout.json"), encoding="utf-8"))["items"]
    n_da = n_hit = 0
    for it in held:
        if it["arm"] != "D-A":
            continue
        n_da += 1
        r = clf.classify(it["text"])
        if r["intent"] in (2, 3):
            n_hit += 1
        else:
            when = None
            print(f"MISS {it['id']}: {it['text'][:70]}")
            print(f"   hits={ {c: v for c, v in r['hits'].items()} }")
    print(f"config {cfg}: D-A reference catch {n_hit}/{n_da}")

if __name__ == "__main__":
    main()
