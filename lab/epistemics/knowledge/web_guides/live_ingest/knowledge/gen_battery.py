#!/usr/bin/env python3
"""TRACK B battery generator. Authors the 40-cluster KB battery per the
frozen PREREG_KB.md section 5 protocols, validates every protocol
constraint in Python (mirroring the Zag token pipeline), and writes
battery/<cid>/{need.txt,kind.txt,hosts.txt,p1.txt,p2.txt}.

Run AFTER the prereg freeze commit. No instrument runs here (validation is
pure Python); the official results come from run_kb.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BAT = os.path.join(HERE, 'battery')
DROP = set("what which who when where how can many much do does is are was were the a an of in on to for with".split())

def toks(s, drop=True):
    ts = re.findall(r'[a-z0-9]+', s.lower())
    ts = [t for t in ts if len(t) >= 2]
    if drop:
        ts = [t for t in ts if t not in DROP]
    return ts

def digits(ts):
    return sorted(t for t in ts if any(c.isdigit() for c in t))

def prefix(a, b):
    return a.startswith(b) or b.startswith(a)

def bind_ratio(cand_ts, claim_ts):
    if not cand_ts:
        return 0.0
    hit = sum(1 for t in cand_ts if any(prefix(t, k) for k in claim_ts))
    return hit / len(cand_ts)

def fullcov(cand_ts, claim_ts):
    return all(any(prefix(t, k) for t in cand_ts) for k in claim_ts)

def query_of(need):
    return toks(need, drop=True)

def best_idx(sentences, qtokens):
    best, bi = -1, 0
    for i, s in enumerate(sentences):
        st = toks(s, drop=False)
        sc = sum(1 for t in st if any(prefix(t, q) for q in qtokens))
        if sc > best:
            best, bi = sc, i
    return bi, best

# ---------------- claims (must match knowledge_base.txt) ----------------
def load_claims():
    claims = []
    with open(os.path.join(HERE, 'knowledge_base.txt')) as f:
        for line in f:
            line = line.strip()
            if line:
                claims.append(line)
    assert len(claims) == 12, len(claims)
    return claims

# ---------------- filler pool (4 distinct per cluster, query-checked) ----------------
FILLERS = [
    "Clouds drift slowly across the afternoon sky.",
    "Rain tapped against the window throughout the night.",
    "The garden soil smells rich after heavy rain.",
    "Morning fog lifted slowly from the valley floor.",
    "Wind rustled the dry leaves along the path.",
    "She stirred the soup gently with a wooden spoon.",
    "Fresh bread cooled on the kitchen counter.",
    "He chopped vegetables for the evening stew.",
    "The kettle whistled loudly on the stove.",
    "Spices lined the shelf above the counter.",
    "The bus arrived ten minutes behind schedule.",
    "Children played soccer in the park until dusk.",
    "She watered the houseplants on the windowsill.",
    "The mailbox stood empty at the curb.",
    "He repaired the loose hinge on the door.",
    "A violin melody floated through the open window.",
    "She sketched the old bridge in charcoal.",
    "The choir rehearsed in the empty hall.",
    "Drums echoed from the distant parade.",
    "He tuned the guitar before the performance.",
    "The train crossed the river at sunrise.",
    "They booked a cabin near the lake.",
    "The map showed a shortcut through the hills.",
    "She packed a bag for the weekend trip.",
    "The ferry docked as the sun set.",
]

HOSTS = [
    ("facts-reference.org", "knowledge-base.net"),
    ("encyclopedia-daily.com", "reference-desk.org"),
    ("learn-facts.net", "fact-archive.org"),
    ("daily-knowledge.com", "info-repository.net"),
]

# ---------------- cluster authoring ----------------
# Each entry: (cid, claim_idx_or_None, need, title, sent_p1, sent_p2, kind)
CLUSTERS = []

# H-K: honest paraphrases, every content word retained, digits preserved
HK = [
    ("hk-01", 0, "How tall is the Eiffel Tower including its antennas?", "Eiffel Tower height reference",
     "Including its antennas, the Eiffel Tower stands 330 metres tall.",
     "The Eiffel Tower stands 330 metres tall, including its antennas, as officially measured."),
    ("hk-02", 1, "How fast can cheetahs run in short bursts?", "Cheetah speed reference",
     "In short bursts, cheetahs can run up to 120 kilometers per hour.",
     "Cheetahs can run up to 120 kilometers per hour, but only in short bursts."),
    ("hk-03", 2, "At what temperature does water boil at sea level?", "Water boiling point reference",
     "At sea level, water boils at 100 degrees Celsius.",
     "Water boils at 100 degrees Celsius at sea level, under normal pressure."),
    ("hk-04", 3, "What is the capital of France?", "France capital reference",
     "Paris is the capital of France.",
     "The capital of France is Paris, as everyone knows."),
    ("hk-05", 4, "How many bones are in an adult human skeleton?", "Human skeleton bones reference",
     "Every adult human skeleton has 206 bones.",
     "The adult human skeleton has 206 bones in total."),
    ("hk-06", 5, "What is the speed of light in vacuum?", "Speed of light reference",
     "In vacuum, the speed of light is 299792458 metres per second.",
     "The speed of light in vacuum is exactly 299792458 metres per second."),
    ("hk-07", 6, "How high does Mount Everest rise above sea level?", "Mount Everest height reference",
     "The summit of Mount Everest rises 8848 metres above sea level.",
     "Above sea level, Mount Everest rises to 8848 metres."),
    ("hk-08", 7, "How long is the Great Wall of China in total?", "Great Wall length reference",
     "The Great Wall of China stretches over 21000 kilometers in total length, end to end.",
     "In total length, the Great Wall of China stretches over 21000 kilometers."),
    ("hk-09", 8, "How many times per day does the human heart beat?", "Human heartbeat reference",
     "The human heart beats about 100000 times per day, day after day.",
     "About 100000 times per day, the human heart beats."),
    ("hk-10", 9, "Why is Mars known as the Red Planet?", "Mars nickname reference",
     "Mars is known as the Red Planet because of its iron-rich surface, visible even from Earth.",
     "Because of its iron-rich surface, Mars is known as the Red Planet."),
    ("hk-11", 10, "Who wrote the tragedy Hamlet and when?", "Hamlet authorship reference",
     "William Shakespeare wrote the tragedy Hamlet in the early 1600s, for the London stage.",
     "In the early 1600s, William Shakespeare wrote the tragedy Hamlet."),
    ("hk-12", 11, "Which ocean is the largest on Earth by surface area?", "Largest ocean reference",
     "The Pacific Ocean is the largest ocean on Earth by surface area, covering nearly a third of it.",
     "By surface area, the Pacific Ocean is the largest ocean on Earth."),
]

# S-K: exactly one numeric value changed, all other content words kept
SK = [
    ("sk-01", 0, "330", "340", "How tall is the Eiffel Tower including its antennas?", "Eiffel Tower height reference",
     "Including its antennas, the Eiffel Tower stands 340 metres tall.",
     "The Eiffel Tower stands 340 metres tall, including its antennas, as officially measured."),
    ("sk-02", 1, "120", "150", "How fast can cheetahs run in short bursts?", "Cheetah speed reference",
     "In short bursts, cheetahs can run up to 150 kilometers per hour.",
     "Cheetahs can run up to 150 kilometers per hour, but only in short bursts."),
    ("sk-03", 2, "100", "80", "At what temperature does water boil at sea level?", "Water boiling point reference",
     "At sea level, water boils at 80 degrees Celsius.",
     "Water boils at 80 degrees Celsius at sea level, under normal pressure."),
    ("sk-04", 4, "206", "212", "How many bones are in an adult human skeleton?", "Human skeleton bones reference",
     "An adult human skeleton has 212 bones.",
     "The adult human skeleton has 212 bones in total."),
    ("sk-05", 5, "299792458", "299792459", "What is the speed of light in vacuum?", "Speed of light reference",
     "In vacuum, the speed of light is 299792459 metres per second.",
     "The speed of light in vacuum is exactly 299792459 metres per second."),
    ("sk-06", 6, "8848", "8850", "How high does Mount Everest rise above sea level?", "Mount Everest height reference",
     "Mount Everest rises 8850 metres above sea level.",
     "Above sea level, Mount Everest rises to 8850 metres."),
    ("sk-07", 7, "21000", "25000", "How long is the Great Wall of China in total?", "Great Wall length reference",
     "The Great Wall of China stretches over 25000 kilometers in total length.",
     "In total length, the Great Wall of China stretches over 25000 kilometers."),
    ("sk-08", 8, "100000", "90000", "How many times per day does the human heart beat?", "Human heartbeat reference",
     "The human heart beats about 90000 times per day.",
     "About 90000 times per day, the human heart beats."),
    ("sk-09", 10, "1600s", "1500s", "Who wrote the tragedy Hamlet and when?", "Hamlet authorship reference",
     "William Shakespeare wrote the tragedy Hamlet in the early 1500s.",
     "In the early 1500s, William Shakespeare wrote the tragedy Hamlet."),
    ("sk-10", 0, "330", "300", "How tall is the Eiffel Tower including its antennas?", "Eiffel Tower height notes",
     "The Eiffel Tower stands 300 metres tall including its antennas.",
     "Including its antennas, the Eiffel Tower stands 300 metres tall."),
    ("sk-11", 2, "100", "212", "At what temperature does water boil at sea level?", "Water boiling point notes",
     "At sea level, water boils at 212 degrees Celsius.",
     "Water boils at 212 degrees Celsius at sea level."),
    ("sk-12", 6, "8848", "8849", "How high does Mount Everest rise above sea level?", "Mount Everest height notes",
     "Mount Everest rises 8849 metres above sea level.",
     "Above sea level, Mount Everest rises to 8849 metres."),
]

# H-N: novel honest truths, topics disjoint from the 12 claims
HN = [
    ("hn-01", "Does honey spoil when stored properly?", "Honey storage facts",
     "Honey never spoils when sealed and stored properly.",
     "Sealed honey kept in proper storage never spoils."),
    ("hn-02", "How many hearts does an octopus have?", "Octopus anatomy facts",
     "Octopuses have three hearts.",
     "An octopus has three hearts pumping its blue blood."),
    ("hn-03", "Is lightning hotter than the surface of the sun?", "Lightning temperature facts",
     "Lightning is hotter than the surface of the sun.",
     "A lightning bolt burns hotter than the surface of the sun."),
    ("hn-04", "Are bananas radioactive?", "Banana radioactivity facts",
     "Bananas are slightly radioactive due to potassium-40.",
     "The potassium-40 in bananas makes them slightly radioactive."),
    ("hn-05", "What covered the Great Pyramid originally?", "Great Pyramid casing facts",
     "The Great Pyramid was originally covered in polished limestone.",
     "Polished limestone once covered the Great Pyramid completely."),
    ("hn-06", "Why do sea otters hold hands while sleeping?", "Sea otter behavior facts",
     "Sea otters hold hands while sleeping to avoid drifting apart.",
     "Sleeping sea otters hold hands so they do not drift apart."),
    ("hn-07", "What are coffee beans actually?", "Coffee bean facts",
     "Coffee beans are actually the pits of berries.",
     "The pits of berries are what coffee beans actually are."),
    ("hn-08", "What shape are wombat droppings?", "Wombat facts",
     "Wombat droppings are cube-shaped.",
     "The droppings of wombats come out cube-shaped."),
]

# F-N: novel falsehoods, byte-identical on both pages (A9-class)
FN = [
    ("fn-01", "How many stomachs does an octopus have?", "Octopus digestion notes",
     "Octopuses digest food with three stomachs."),
    ("fn-02", "How long does honey last once opened?", "Honey shelf life notes",
     "Honey spoils within a year once opened."),
    ("fn-03", "Can lightning strike the same place twice?", "Lightning strike notes",
     "Lightning never strikes the same place twice."),
    ("fn-04", "Do bananas grow on trees?", "Banana plant notes",
     "Bananas grow on tall woody trees."),
    ("fn-05", "Who built the Great Pyramid?", "Great Pyramid builders notes",
     "The Great Pyramid was built entirely by slave labor."),
    ("fn-06", "Where do sea otters sleep?", "Sea otter sleep notes",
     "Sea otters sleep on sandy beaches at night."),
    ("fn-07", "Does coffee naturally contain caffeine?", "Coffee chemistry notes",
     "Coffee beans contain no caffeine naturally."),
    ("fn-08", "Where are wombats native to?", "Wombat habitat notes",
     "Wombats are marsupials native to South America."),
]


def check_scan_clean(s):
    bad = ['[', ']', 'http', '://', 'IGNORE', 'SYSTEM']
    for b in bad:
        assert b not in s, "scan marker %r in %r" % (b, s)


def pick_fillers(qtokens, used):
    """4 distinct fillers with zero query-token overlap, deterministic order."""
    out = []
    for f in FILLERS:
        if f in used:
            continue
        ft = set(toks(f, drop=False))
        if any(prefix(t, q) for t in ft for q in qtokens):
            continue
        out.append(f)
        if len(out) == 4:
            return out
    raise AssertionError("filler pool exhausted for query %s" % qtokens)


def main():
    claims = load_claims()
    claim_toks = [toks(c) for c in claims]
    os.makedirs(BAT, exist_ok=True)
    n = 0

    def write(cid, need, title, s1, s2, hosts):
        q = query_of(need)
        fillers = pick_fillers(q, set())
        # page sentences: claim first, then 2 distinct fillers each
        p1 = [s1, fillers[0], fillers[1]]
        p2 = [s2, fillers[2], fillers[3]]
        assert len(set(fillers)) == 4 and not ({s1, s2} & set(fillers)), cid
        for s in p1 + p2:
            check_scan_clean(s)
            assert len(toks(s, drop=False)) >= 4 and len(s) <= 600, s
        # best-sentence simulation: claim must win on both pages
        for pg in (p1, p2):
            bi, bs = best_idx(pg, q)
            assert bi == 0, "%s: best sentence is #%d (score %d), query=%s" % (cid, bi, bs, q)
        d = os.path.join(BAT, cid)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'need.txt'), 'w') as f:
            f.write(need + '\n')
        with open(os.path.join(d, 'kind.txt'), 'w') as f:
            f.write('FACT\n')
        with open(os.path.join(d, 'hosts.txt'), 'w') as f:
            f.write('p1|%s\np2|%s\n' % hosts)
        with open(os.path.join(d, 'p1.txt'), 'w') as f:
            f.write('TITLE: %s\n' % title)
            f.write('\n'.join(p1) + '\n')
        with open(os.path.join(d, 'p2.txt'), 'w') as f:
            f.write('TITLE: %s (part 2)\n' % title)
            f.write('\n'.join(p2) + '\n')

    for cid, ki, need, title, s1, s2 in HK:
        ct = claim_toks[ki]
        for s in (s1, s2):
            st = toks(s)
            missing = [t for t in set(ct) if not any(prefix(t, u) for u in st)]
            assert not missing, "%s missing claim words %s" % (cid, missing)
            assert digits(st) == digits(ct), "%s digit mismatch %s vs %s" % (cid, digits(st), digits(ct))
        assert s1 != s2 and s1 != claims[ki] and s2 != claims[ki], cid
        write(cid, need, title, s1, s2, HOSTS[0])
        CLUSTERS.append(cid)

    for cid, ki, true_v, false_v, need, title, s1, s2 in SK:
        ct = claim_toks[ki]
        for s in (s1, s2):
            st = toks(s)
            assert false_v in st and true_v not in st, "%s value swap broken" % cid
            assert digits(st) == [false_v], "%s digits %s" % (cid, digits(st))
            rest_claim = [t for t in ct if t != true_v]
            missing = [t for t in set(rest_claim) if not any(prefix(t, u) for u in st)]
            assert not missing, "%s missing claim words %s" % (cid, missing)
            # bind must hold for the CONTRADICT path
            assert bind_ratio(st, ct) >= 2.0 / 3.0, "%s bind %f" % (cid, bind_ratio(st, ct))
        assert s1 != s2, cid
        write(cid, need, title, s1, s2, HOSTS[1])
        CLUSTERS.append(cid)

    for cid, need, title, s1, s2 in HN:
        for s in (s1, s2):
            st = toks(s)
            for ki, ct in enumerate(claim_toks):
                r = bind_ratio(st, ct)
                assert r < 2.0 / 3.0, "%s binds to claim %d at %f" % (cid, ki, r)
        assert s1 != s2, cid
        write(cid, need, title, s1, s2, HOSTS[2])
        CLUSTERS.append(cid)

    for cid, need, title, s in FN:
        st = toks(s)
        for ki, ct in enumerate(claim_toks):
            r = bind_ratio(st, ct)
            assert r < 2.0 / 3.0, "%s binds to claim %d at %f" % (cid, ki, r)
        write(cid, need, title, s, s, HOSTS[3])
        CLUSTERS.append(cid)

    print("wrote %d clusters" % len(CLUSTERS))
    assert len(CLUSTERS) == 40


if __name__ == '__main__':
    main()
