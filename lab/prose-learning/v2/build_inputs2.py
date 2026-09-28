#!/usr/bin/env python3
"""Rich-comprehension v2 battery builder (Worker A).
Deterministic: NO RNG anywhere. All fact selections are hand-picked fixed
lists; all templates are fixed. Re-running produces byte-identical files.
"""
import json, os

OUT = os.path.expanduser("~/workspace/richcomp/inputs2")
os.makedirs(OUT, exist_ok=True)
CH = os.path.expanduser("~/workspace/tnn-lab/prose-learning/inputs")

def load(s):
    return json.load(open(f"{CH}/train_{s}.jsonl"))

sol_train = load("sol")
sol_test = json.load(open(f"{CH}/test_sol.jsonl"))
FALSE = set(json.load(open(f"{CH}/false_ids_sol.json"))["false_ids"])

def wline(path, obj):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def fresh(path):
    if os.path.exists(path):
        os.remove(path)

# ---------------------------------------------------------------- SUB-PARA
# 48 facts: 12/category. (entity_display, value). Truth verified vs sol test probes.
PARA_FACTS = {
    "alpha":   [("A",1),("B",2),("C",3),("E",5),("F",6),("G",7),
                ("H",8),("I",9),("J",10),("K",11),("L",12),("M",13)],
    "wordlen": [("a",1),("an",2),("the",3),("four",4),("seven",5),("minute",6),
                ("seconds",7),("afternoon",9),("dictionary",10),("handwriting",11),
                ("disappointed",12),("extraordinary",13)],
    "pubyear": [("Hamlet",1603),("Don Quixote",1605),("King Lear",1608),
                ("The King James Bible",1611),("Shakespeare's First Folio",1623),
                ("Leviathan",1651),("Paradise Lost",1667),("Robinson Crusoe",1719),
                ("Gulliver's Travels",1726),("Pamela",1740),("Tom Jones",1749),
                ("Candide",1759)],
    "count":   [("English alphabet","letters",26),("English alphabet","vowels",5),
                ("English alphabet","consonants",21),("week","days",7),
                ("year","months",12),("year","seasons",4),("year","weeks",52),
                ("day","hours",24),("hour","minutes",60),("minute","seconds",60),
                ("week","hours",168),("US Constitution","amendments",27)],
}
ALPHA_T = [
    "Starting the count at 1, the alphabet position of {e} is {v}.",
    "The alphabet position assigned to {e} equals {v}.",
    "{e} occupies alphabet position {v}.",
    "Out of all the letters, {e} holds alphabet position {v}.",
    "Look up the alphabet position of {e} and you get {v}.",
]
ALPHA_P = "Tell me the alphabet position of {e}."
WORD_T = [
    'The letter count of "{e}" is {v}.',
    'Counting its letters, "{e}" has a letter count of {v}.',
    'For the word "{e}", the letter count is {v}.',
    '"{e}" contains {v} letters; that is its letter count.',
    'Write down "{e}" and count the letters to get a letter count of {v}.',
]
WORD_P = 'What is the letter count of "{e}"?'
PUB_T = [
    'The publication year of "{e}" is {v}.',
    '"{e}" has a publication year of {v}.',
    'The book "{e}" lists a publication year of {v}.',
    'A publication year of {v} is recorded for "{e}".',
    'Historians give "{e}" a publication year of {v}.',
]
PUB_P = 'Give the publication year of "{e}".'
COUNT_T = [
    'The "{e}" has a count of {v} {p}.',
    'There is a count of {v} {p} in each "{e}".',
    'Each "{e}" contains {v} {p}.',
    'The number of {p} per "{e}" is {v}.',
    'You will find {v} {p} in a "{e}".',
]
COUNT_P = 'How many {p} are there in a "{e}"?'

para_tr = f"{OUT}/sub_para_train.jsonl"
para_te = f"{OUT}/sub_para_test.jsonl"
fresh(para_tr); fresh(para_te)
tid = 0; qid = 0
for cat, facts in PARA_FACTS.items():
    T, P = {"alpha": (ALPHA_T, ALPHA_P), "wordlen": (WORD_T, WORD_P),
            "pubyear": (PUB_T, PUB_P), "count": (COUNT_T, COUNT_P)}[cat]
    for f in facts:
        if cat == "count":
            e, p, v = f
            kw = dict(e=e, p=p, v=v)
        else:
            e, v = f
            kw = dict(e=e, v=v)
        for t in T:
            wline(para_tr, {"id": tid, "text": t.format(**kw)}); tid += 1
        wline(para_te, {"id": qid, "probe": P.format(**kw),
                        "probe_value": v, "expect": "value"}); qid += 1
assert tid == 240 and qid == 48, (tid, qid)

# ---------------------------------------------------------------- SUB-CONTR
# (entity, relation-kind, true V, wrong W, sentence1, sentence2, probe)
CONTR = [
    # alpha: 6
    ("N", 14, 15, "N has an alphabet position of 14.",
     "The alphabet position of N is 15.", "What is the alphabet position of N?"),
    ("O", 15, 16, "O has an alphabet position of 15.",
     "The alphabet position of O is 16.", "What is the alphabet position of O?"),
    ("P", 16, 17, "P has an alphabet position of 16.",
     "The alphabet position of P is 17.", "What is the alphabet position of P?"),
    ("Q", 17, 18, "Q has an alphabet position of 17.",
     "The alphabet position of Q is 18.", "What is the alphabet position of Q?"),
    ("R", 18, 19, "R has an alphabet position of 18.",
     "The alphabet position of R is 19.", "What is the alphabet position of R?"),
    ("S", 19, 20, "S has an alphabet position of 19.",
     "The alphabet position of S is 20.", "What is the alphabet position of S?"),
    # wordlen: 6
    ("four", 4, 5, 'The word "four" has a letter count of 4.',
     'The letter count of "four" is 5.', 'What is the letter count of "four"?'),
    ("seven", 5, 6, 'The word "seven" has a letter count of 5.',
     'The letter count of "seven" is 6.', 'What is the letter count of "seven"?'),
    ("minute", 6, 7, 'The word "minute" has a letter count of 6.',
     'The letter count of "minute" is 7.', 'What is the letter count of "minute"?'),
    ("seconds", 7, 8, 'The word "seconds" has a letter count of 7.',
     'The letter count of "seconds" is 8.', 'What is the letter count of "seconds"?'),
    ("afternoon", 9, 10, 'The word "afternoon" has a letter count of 9.',
     'The letter count of "afternoon" is 10.', 'What is the letter count of "afternoon"?'),
    ("dictionary", 10, 11, 'The word "dictionary" has a letter count of 10.',
     'The letter count of "dictionary" is 11.', 'What is the letter count of "dictionary"?'),
    # pubyear: 6
    ("Hamlet", 1603, 1613, 'The publication year of "Hamlet" is 1603.',
     '"Hamlet" has a publication year of 1613.', 'Give the publication year of "Hamlet".'),
    ("Don Quixote", 1605, 1615, 'The publication year of "Don Quixote" is 1605.',
     '"Don Quixote" has a publication year of 1615.', 'Give the publication year of "Don Quixote".'),
    ("King Lear", 1608, 1618, 'The publication year of "King Lear" is 1608.',
     '"King Lear" has a publication year of 1618.', 'Give the publication year of "King Lear".'),
    ("The King James Bible", 1611, 1621, 'The publication year of "The King James Bible" is 1611.',
     '"The King James Bible" has a publication year of 1621.', 'Give the publication year of "The King James Bible".'),
    ("Shakespeare's First Folio", 1623, 1633, 'The publication year of "Shakespeare\'s First Folio" is 1623.',
     '"Shakespeare\'s First Folio" has a publication year of 1633.', 'Give the publication year of "Shakespeare\'s First Folio".'),
    ("Leviathan", 1651, 1661, 'The publication year of "Leviathan" is 1651.',
     '"Leviathan" has a publication year of 1661.', 'Give the publication year of "Leviathan".'),
    # countfact: 6
    ("basketball team", 5, 6, 'A "basketball team" has 5 players on the court.',
     'A "basketball team" has 6 players on the court.', 'How many players does a "basketball team" have on the court?'),
    ("soccer team", 11, 12, 'A "soccer team" has 11 players on the field.',
     'A "soccer team" has 12 players on the field.', 'How many players does a "soccer team" have on the field?'),
    ("standard deck", 52, 53, 'A "standard deck" has 52 cards.',
     'A "standard deck" has 53 cards.', 'How many cards does a "standard deck" have?'),
    ("chessboard", 64, 65, 'A "chessboard" has 64 squares.',
     'A "chessboard" has 65 squares.', 'How many squares does a "chessboard" have?'),
    ("standard die", 6, 7, 'A "standard die" has 6 faces.',
     'A "standard die" has 7 faces.', 'How many faces does a "standard die" have?'),
    ("standard piano", 88, 89, 'A "standard piano" has 88 keys.',
     'A "standard piano" has 89 keys.', 'How many keys does a "standard piano" have?'),
]
contr_tr = f"{OUT}/sub_contr_train.jsonl"; contr_te = f"{OUT}/sub_contr_test.jsonl"
fresh(contr_tr); fresh(contr_te)
for i, (e, v, w, s1, s2, pr) in enumerate(CONTR):
    wline(contr_tr, {"id": i, "text": s1 + " " + s2})
    wline(contr_te, {"id": i, "probe": pr, "probe_value": None, "expect": "contradiction"})
assert len(CONTR) == 24

# ---------------------------------------------------------------- SUB-HEDGE
# 12 asserted+hedged (probe -> asserted value), 12 hedged-only (probe -> hedged)
HEDGE_AH = [  # (entity-display, asserted V, hedged W, s_asserted, s_hedged, probe)
    ("T", 20, 21, "T has an alphabet position of 20.",
     "I think the alphabet position of T is 21.", "Tell me the alphabet position of T."),
    ("U", 21, 22, "U has an alphabet position of 21.",
     "I believe the alphabet position of U is 22.", "Tell me the alphabet position of U."),
    ("V", 22, 23, "V has an alphabet position of 22.",
     "The alphabet position of V is probably 23.", "Tell me the alphabet position of V."),
    ("novel", 5, 6, 'The letter count of "novel" is 5.',
     'Maybe the letter count of "novel" is 6.', 'What is the letter count of "novel"?'),
    ("story", 5, 6, 'The letter count of "story" is 5.',
     'Perhaps the letter count of "story" is 6.', 'What is the letter count of "story"?'),
    ("poem", 4, 5, 'The letter count of "poem" is 4.',
     'The letter count of "poem" might be 5.', 'What is the letter count of "poem"?'),
    ("Moby-Dick", 1851, 1861, '"Moby-Dick" has a publication year of 1851.',
     'The publication year of "Moby-Dick" could be 1861.', 'Give the publication year of "Moby-Dick".'),
    ("Uncle Tom's Cabin", 1852, 1862, '"Uncle Tom\'s Cabin" has a publication year of 1852.',
     'The publication year of "Uncle Tom\'s Cabin" seems to be 1862.', 'Give the publication year of "Uncle Tom\'s Cabin".'),
    ("Walden", 1854, 1864, '"Walden" has a publication year of 1854.',
     'Allegedly, the publication year of "Walden" is 1864.', 'Give the publication year of "Walden".'),
    ("Beatles", 4, 5, 'The "Beatles" have 4 members.',
     'Reportedly, the "Beatles" have 5 members.', 'How many members do the "Beatles" have?'),
    ("Jackson 5", 5, 6, 'The "Jackson 5" have 5 members.',
     'The "Jackson 5" possibly have 6 members.', 'How many members does the "Jackson 5" have?'),
    ("United States", 50, 51, 'The "United States" has 50 states.',
     'The "United States" likely has 51 states.', 'How many states does the "United States" have?'),
]
HEDGE_HO = [  # (entity-display, hedged W, sentence, probe)
    ("A", 2, "I think the alphabet position of A is 2.", "Tell me the alphabet position of A."),
    ("B", 3, "I believe the alphabet position of B is 3.", "Tell me the alphabet position of B."),
    ("C", 4, "The alphabet position of C is probably 4.", "Tell me the alphabet position of C."),
    ("rhyme", 6, 'Maybe the letter count of "rhyme" is 6.', 'What is the letter count of "rhyme"?'),
    ("grammar", 8, 'Perhaps the letter count of "grammar" is 8.', 'What is the letter count of "grammar"?'),
    ("spelling", 9, 'The letter count of "spelling" might be 9.', 'What is the letter count of "spelling"?'),
    ("Les Miserables", 1872, 'The publication year of "Les Miserables" could be 1872.',
     'Give the publication year of "Les Miserables".'),
    ("Alice's Adventures in Wonderland", 1875,
     'It seems the publication year of "Alice\'s Adventures in Wonderland" is 1875.',
     'Give the publication year of "Alice\'s Adventures in Wonderland".'),
    ("Crime and Punishment", 1876, 'Allegedly, the publication year of "Crime and Punishment" is 1876.',
     'Give the publication year of "Crime and Punishment".'),
    ("US flag", 14, 'Reportedly, the "US flag" has 14 stripes.', 'How many stripes does the "US flag" have?'),
    ("Earth", 8, 'The "Earth" possibly has 8 continents.', 'How many continents does the "Earth" have?'),
    ("rugby union team", 16, 'A "rugby union team" likely has 16 players.',
     'How many players does a "rugby union team" have?'),
]
hedge_tr = f"{OUT}/sub_hedge_train.jsonl"; hedge_te = f"{OUT}/sub_hedge_test.jsonl"
fresh(hedge_tr); fresh(hedge_te)
qid = 0
for i, (e, v, w, sa, sh, pr) in enumerate(HEDGE_AH):
    wline(hedge_tr, {"id": i, "text": sa + " " + sh})
    wline(hedge_te, {"id": qid, "probe": pr, "probe_value": v, "expect": "value"}); qid += 1
for j, (e, w, sh, pr) in enumerate(HEDGE_HO):
    wline(hedge_tr, {"id": len(HEDGE_AH) + j, "text": sh})
    wline(hedge_te, {"id": qid, "probe": pr, "probe_value": None, "expect": "hedged"}); qid += 1
assert qid == 24

# ---------------------------------------------------------------- SUB-NEG
# 24 neg-only (probe -> unknown), 12 neg+asserted (probe -> asserted value)
NEG_ONLY = [
    ("A", 2, "The alphabet position of A is not 2.", "Tell me the alphabet position of A."),
    ("B", 3, "The alphabet position of B is not 3.", "Tell me the alphabet position of B."),
    ("C", 4, "The alphabet position of C is not 4.", "Tell me the alphabet position of C."),
    ("E", 6, "The alphabet position of E is not 6.", "Tell me the alphabet position of E."),
    ("F", 7, "The alphabet position of F is not 7.", "Tell me the alphabet position of F."),
    ("G", 8, "The alphabet position of G is not 8.", "Tell me the alphabet position of G."),
    ("four", 5, 'The letter count of "four" is not 5.', 'What is the letter count of "four"?'),
    ("seven", 6, 'The letter count of "seven" is not 6.', 'What is the letter count of "seven"?'),
    ("minute", 7, 'The letter count of "minute" is not 7.', 'What is the letter count of "minute"?'),
    ("seconds", 8, 'The letter count of "seconds" is not 8.', 'What is the letter count of "seconds"?'),
    ("afternoon", 10, 'The letter count of "afternoon" is not 10.', 'What is the letter count of "afternoon"?'),
    ("dictionary", 11, 'The letter count of "dictionary" is not 11.', 'What is the letter count of "dictionary"?'),
    ("Hamlet", 1613, 'The publication year of "Hamlet" is not 1613.', 'Give the publication year of "Hamlet".'),
    ("Don Quixote", 1615, 'The publication year of "Don Quixote" is not 1615.', 'Give the publication year of "Don Quixote".'),
    ("King Lear", 1618, 'The publication year of "King Lear" is not 1618.', 'Give the publication year of "King Lear".'),
    ("The King James Bible", 1621, 'The publication year of "The King James Bible" is not 1621.',
     'Give the publication year of "The King James Bible".'),
    ("Shakespeare's First Folio", 1633, 'The publication year of "Shakespeare\'s First Folio" is not 1633.',
     'Give the publication year of "Shakespeare\'s First Folio".'),
    ("Leviathan", 1661, 'The publication year of "Leviathan" is not 1661.', 'Give the publication year of "Leviathan".'),
    ("Beatles", 5, 'The "Beatles" do not have 5 members.', 'How many members do the "Beatles" have?'),
    ("Jackson 5", 6, 'The "Jackson 5" do not have 6 members.', 'How many members does the "Jackson 5" have?'),
    ("United States", 51, 'The "United States" does not have 51 states.', 'How many states does the "United States" have?'),
    ("US flag", 14, 'The "US flag" does not have 14 stripes.', 'How many stripes does the "US flag" have?'),
    ("Earth", 8, 'The "Earth" does not have 8 continents.', 'How many continents does the "Earth" have?'),
    ("rugby union team", 16, 'A "rugby union team" does not have 16 players.', 'How many players does a "rugby union team" have?'),
]
NEG_ASSERTED = [  # (entity, denied W, asserted V, s1, s2, probe)
    ("H", 9, 8, "H has an alphabet position of 8.", "The alphabet position of H is not 9.",
     "Tell me the alphabet position of H."),
    ("I", 10, 9, "The alphabet position of I is not 10.", "I has an alphabet position of 9.",
     "Tell me the alphabet position of I."),
    ("novel", 6, 5, 'The letter count of "novel" is 5.', 'The letter count of "novel" is not 6.',
     'What is the letter count of "novel"?'),
    ("story", 6, 5, 'The letter count of "story" is not 6.', 'The letter count of "story" is 5.',
     'What is the letter count of "story"?'),
    ("Moby-Dick", 1861, 1851, '"Moby-Dick" has a publication year of 1851.',
     'The publication year of "Moby-Dick" is not 1861.', 'Give the publication year of "Moby-Dick".'),
    ("Uncle Tom's Cabin", 1862, 1852, 'The publication year of "Uncle Tom\'s Cabin" is not 1862.',
     '"Uncle Tom\'s Cabin" has a publication year of 1852.', 'Give the publication year of "Uncle Tom\'s Cabin".'),
    ("Beatles", 5, 4, 'The "Beatles" have 4 members.', 'The "Beatles" do not have 5 members.',
     'How many members do the "Beatles" have?'),
    ("Jackson 5", 6, 5, 'The "Jackson 5" do not have 6 members.', 'The "Jackson 5" have 5 members.',
     'How many members does the "Jackson 5" have?'),
    ("J", 11, 10, "J has an alphabet position of 10.", "The alphabet position of J is not 11.",
     "Tell me the alphabet position of J."),
    ("K", 12, 11, "The alphabet position of K is not 12.", "K has an alphabet position of 11.",
     "Tell me the alphabet position of K."),
    ("poem", 5, 4, 'The letter count of "poem" is 4.', 'The letter count of "poem" is not 5.',
     'What is the letter count of "poem"?'),
    ("rhyme", 6, 5, 'The letter count of "rhyme" is not 6.', 'The letter count of "rhyme" is 5.',
     'What is the letter count of "rhyme"?'),
]
neg_tr = f"{OUT}/sub_neg_train.jsonl"; neg_te = f"{OUT}/sub_neg_test.jsonl"
fresh(neg_tr); fresh(neg_te)
for i, (e, w, s, pr) in enumerate(NEG_ONLY):
    wline(neg_tr, {"id": i, "text": s})
    wline(neg_te, {"id": i, "probe": pr, "probe_value": None, "expect": "unknown"})
for j, (e, w, v, s1, s2, pr) in enumerate(NEG_ASSERTED):
    wline(neg_tr, {"id": len(NEG_ONLY) + j, "text": s1 + " " + s2})
    wline(neg_te, {"id": len(NEG_ONLY) + j, "probe": pr, "probe_value": v, "expect": "value"})
assert len(NEG_ONLY) == 24 and len(NEG_ASSERTED) == 12

# ---------------------------------------------------------------- SUB-MULTI
# (X, relation, Y, pos(Y), derived pos(X), anchor_first)
MULTI = [
    # comes after: X after Y, anchor pos(Y) -> pos(X)=pos(Y)+1
    ("B", "after", "A", 1, True), ("F", "after", "E", 5, True),
    ("I", "after", "H", 8, False), ("L", "after", "K", 11, True),
    ("O", "after", "N", 14, False), ("R", "after", "Q", 17, True),
    ("U", "after", "T", 20, True), ("X", "after", "W", 23, False),
    ("Z", "after", "Y", 25, True), ("N", "after", "M", 13, False),
    ("Q", "after", "P", 16, True), ("T", "after", "S", 19, False),
    # comes before: X before Y, anchor pos(Y) -> pos(X)=pos(Y)-1
    ("A", "before", "B", 2, True), ("E", "before", "F", 6, False),
    ("G", "before", "H", 8, True), ("J", "before", "K", 11, False),
    ("M", "before", "N", 14, True), ("P", "before", "Q", 17, False),
    ("S", "before", "T", 20, True), ("V", "before", "W", 23, False),
    ("Y", "before", "Z", 26, True), ("I", "before", "J", 10, False),
    ("L", "before", "M", 13, True), ("W", "before", "X", 24, False),
]
multi_tr = f"{OUT}/sub_multi_train.jsonl"; multi_te = f"{OUT}/sub_multi_test.jsonl"
fresh(multi_tr); fresh(multi_te)
for i, (x, rel, y, py, anchor_first) in enumerate(MULTI):
    anchor = f"{y} has an alphabet position of {py}."
    link = f"{x} comes {rel} {y}."
    text = (anchor + " " + link) if anchor_first else (link + " " + anchor)
    derived = py + 1 if rel == "after" else py - 1
    wline(multi_tr, {"id": i, "text": text})
    wline(multi_te, {"id": i, "probe": f"What is the alphabet position of {x}?",
                     "probe_value": derived, "expect": "value"})
assert len(MULTI) == 24

# ---------------------------------------------------------------- SUB-CORE
# (s1, s2, probe, expected)
CORE = [
    # word entities, pronouns it/this/that/the word
    ('The word "four" has a letter count of 4.',
     "It was first recorded in the year 1300.",
     'In what year was the word "four" first recorded?', 1300),
    ('The word "seven" has a letter count of 5.',
     "This word appeared in print in the year 1476.",
     'In what year did the word "seven" appear in print?', 1476),
    ('The word "minute" has a letter count of 6.',
     "That word was coined in the year 1398.",
     'In what year was the word "minute" coined?', 1398),
    ('The word "seconds" has a letter count of 7.',
     "The word was added to the dictionary in 1755.",
     'In what year was the word "seconds" added to the dictionary?', 1755),
    ('The word "afternoon" has a letter count of 9.',
     "It entered common use in the year 1502.",
     'In what year did the word "afternoon" enter common use?', 1502),
    ('The word "dictionary" has a letter count of 10.',
     "This word was first defined in print in the year 1604.",
     'In what year was the word "dictionary" first defined in print?', 1604),
    ('The word "handwriting" has a letter count of 11.',
     "That word appeared in a manuscript in the year 1410.",
     'In what year did the word "handwriting" appear in a manuscript?', 1410),
    ('The word "disappointed" has a letter count of 12.',
     "The word was first used in a letter in the year 1523.",
     'In what year was the word "disappointed" first used in a letter?', 1523),
    # pubyear entities
    ('"Hamlet" has a publication year of 1603.',
     "It has a total of 30 named characters.",
     'How many named characters does "Hamlet" have?', 30),
    ('"Don Quixote" has a publication year of 1605.',
     "This novel was translated into English in the year 1612.",
     'In what year was "Don Quixote" translated into English?', 1612),
    ('"King Lear" has a publication year of 1608.',
     "That play was first performed at court in the year 1606.",
     'In what year was "King Lear" first performed at court?', 1606),
    ('"Leviathan" has a publication year of 1651.',
     "It was reprinted 12 times in its first century.",
     'How many times was "Leviathan" reprinted in its first century?', 12),
    ('"Paradise Lost" has a publication year of 1667.',
     "This poem contains over 10000 lines of verse.",
     'How many lines of verse does "Paradise Lost" contain?', 10000),
    ('"Robinson Crusoe" has a publication year of 1719.',
     "That novel has 20 chapters.",
     'How many chapters does "Robinson Crusoe" have?', 20),
    ("\"Gulliver's Travels\" has a publication year of 1726.",
     "It was illustrated in 300 editions.",
     'In how many editions was "Gulliver\'s Travels" illustrated?', 300),
    ('"Pamela" has a publication year of 1740.',
     "That novel inspired 15 imitations.",
     'How many imitations did "Pamela" inspire?', 15),
    # letter entities, "the letter" / that
    ('"Q" has an alphabet position of 17.',
     "The letter was first described in the year 1680.",
     'In what year was the letter "Q" first described?', 1680),
    ('"Z" has an alphabet position of 26.',
     "The letter appears 5 times in the alphabet song.",
     'How many times does the letter "Z" appear in the alphabet song?', 5),
    ('"M" has an alphabet position of 13.',
     "The letter was first printed in the year 1455.",
     'In what year was the letter "M" first printed?', 1455),
    ('"R" has an alphabet position of 18.',
     'That letter appears 2 times in the word "letter".',
     'How many times does the letter "R" appear in the word "letter"?', 2),
    ('"B" has an alphabet position of 2.',
     "It ranks 2 among consonants.",
     'What rank does the letter "B" hold among consonants?', 2),
    ('"K" has an alphabet position of 11.',
     'The letter occurs 2 times in "bookkeeping".',
     'How many times does the letter "K" occur in "bookkeeping"?', 2),
    ('"W" has an alphabet position of 23.',
     "It takes 3 syllables to say in English.",
     'How many syllables does it take to say the letter "W" in English?', 3),
    ('"V" has an alphabet position of 22.',
     "The letter has 2 straight strokes.",
     'How many straight strokes does the letter "V" have?', 2),
]
core_tr = f"{OUT}/sub_core_train.jsonl"; core_te = f"{OUT}/sub_core_test.jsonl"
fresh(core_tr); fresh(core_te)
for i, (s1, s2, pr, v) in enumerate(CORE):
    wline(core_tr, {"id": i, "text": s1 + " " + s2})
    wline(core_te, {"id": i, "probe": pr, "probe_value": v, "expect": "value"})
assert len(CORE) == 24

# ---------------------------------------------------------------- SUB-DISTR
# championship sol train (sentence->text) + 240 distractor sentences
DISTRACTORS = [  # (entity, value, unit)
    ("Eiffel Tower", 330, "meters"), ("Mount Everest", 8849, "meters"),
    ("Mariana Trench", 10935, "meters"), ("Nile River", 6650, "kilometers"),
    ("Amazon River", 6400, "kilometers"), ("Sahara Desert", 9200000, "square kilometers"),
    ("Great Wall of China", 21196, "kilometers"), ("Burj Khalifa", 828, "meters"),
    ("Empire State Building", 443, "meters"), ("Statue of Liberty", 93, "meters"),
    ("Big Ben tower", 96, "meters"), ("Colosseum", 189, "meters"),
    ("Sydney Opera House", 183, "meters"), ("Golden Gate Bridge", 2737, "meters"),
    ("Panama Canal", 82, "kilometers"), ("Suez Canal", 193, "kilometers"),
    ("Mississippi River", 3730, "kilometers"), ("Yangtze River", 6300, "kilometers"),
    ("Lake Baikal", 1642, "meters"), ("Dead Sea", 430, "meters"),
    ("Grand Canyon", 1800, "meters"), ("Mount Kilimanjaro", 5895, "meters"),
    ("Mount Fuji", 3776, "meters"), ("Blue whale", 30, "meters"),
    ("Giraffe", 5, "meters"), ("Cheetah", 120, "kilometers per hour"),
    ("Peregrine falcon", 389, "kilometers per hour"), ("Hummingbird", 13, "centimeters"),
    ("Ostrich", 270, "centimeters"), ("African elephant", 6000, "kilograms"),
    ("Polar bear", 800, "kilograms"), ("Great white shark", 6, "meters"),
    ("Anaconda", 9, "meters"), ("Komodo dragon", 3, "meters"),
    ("Redwood tree", 116, "meters"), ("Baobab tree", 25, "meters"),
    ("Angel Falls", 979, "meters"), ("Niagara Falls", 51, "meters"),
    ("Victoria Falls", 108, "meters"), ("Hoover Dam", 221, "meters"),
    ("Three Gorges Dam", 181, "meters"), ("London Eye", 135, "meters"),
    ("Space Needle", 184, "meters"), ("CN Tower", 553, "meters"),
    ("Tokyo Skytree", 634, "meters"), ("Shanghai Tower", 632, "meters"),
    ("One World Trade Center", 541, "meters"), ("Willis Tower", 442, "meters"),
]
assert len(DISTRACTORS) == 48
D_T = [
    "The {e} measures {v} {u}.",
    "{e} spans {v} {u}.",
    "At {v} {u}, the {e} impresses visitors.",
    "Visitors learn that the {e} measures {v} {u}.",
    "{v} {u} is the recorded measurement of the {e}.",
]
distr_tr = f"{OUT}/sub_distr_train.jsonl"; distr_te = f"{OUT}/sub_distr_test.jsonl"
fresh(distr_tr); fresh(distr_te)
for it in sol_train:
    wline(distr_tr, {"id": it["id"], "text": it["sentence"]})
did = 240
for (e, v, u) in DISTRACTORS:
    for t in D_T:
        wline(distr_tr, {"id": did, "text": t.format(e=e, v=v, u=u)})
        did += 1
assert did == 480
for it in sol_test:
    wline(distr_te, {"id": it["id"], "probe": it["probe"],
                     "probe_value": it["probe_value"], "expect": "value"})

print("done:",
      "para", sum(1 for _ in open(para_tr)), sum(1 for _ in open(para_te)),
      "contr", sum(1 for _ in open(contr_tr)), sum(1 for _ in open(contr_te)),
      "hedge", sum(1 for _ in open(hedge_tr)), sum(1 for _ in open(hedge_te)),
      "neg", sum(1 for _ in open(neg_tr)), sum(1 for _ in open(neg_te)),
      "multi", sum(1 for _ in open(multi_tr)), sum(1 for _ in open(multi_te)),
      "core", sum(1 for _ in open(core_tr)), sum(1 for _ in open(core_te)),
      "distr", sum(1 for _ in open(distr_tr)), sum(1 for _ in open(distr_te)))
