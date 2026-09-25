#!/usr/bin/env python3
"""Generate the frozen WS2-L learning corpus (PREREG_WS2L.md section 4).
Deterministic: fixed templates, fixed order, NO RNG.
Format: LEARN|lid|pattern|text ; PARA lines: LEARN|lid|PARA|subj|text.
Asserts: 112 positive relations + 4 negatives."""
import sys

VOWELS = set('aeiou')

def art(w):
    return 'an' if w[0] in VOWELS else 'a'

def def_line(w1, w2):
    return f"{art(w1)} {w1} is {art(w2)} {w2}."

def syn_line(w1, w2):
    return f"{w1} and {w2} are synonyms."

# --- pair lists (frozen prereg vocabulary; data for the generator) ---
tbl = open('/home/hatch/workspace/tnn-lab/cognition_ws/ws2/SYN_TABLE_V1.txt').read().splitlines()
pairs56 = [l.split('|') for l in tbl if l and not l.startswith('#')]
assert len(pairs56) == 56, len(pairs56)

fresh = [p.split('|') for p in
    "river|stream flooded|inundated valley|vale destroyed|ruined farms|crops "
    "ocean|sea waves|billows crashed|broke loudly|noisily rocks|stones "
    "dense|thick forest|woods stretched|extended miles|leagues "
    "tall|high mountain|peak rose|towered above|over clouds|mist "
    "teacher|instructor praised|commended diligent|hardworking student|pupil warmly|kindly "
    "long|lengthy journey|voyage took|lasted ship|boat".split()]
assert len(fresh) == 28

para_pairs = ["river|stream", "valley|vale", "ocean|sea", "rocks|stones",
              "forest|woods", "miles|leagues", "mountain|peak", "clouds|mist",
              "teacher|instructor", "student|pupil", "journey|voyage", "ship|boat"]
para_frames = {
    "river|stream": [("the river flows calmly", "the stream flows calmly"),
                     ("the river runs deep", "the stream runs deep")],
    "valley|vale": [("the valley lies quiet", "the vale lies quiet"),
                    ("the valley sleeps still", "the vale sleeps still")],
    "ocean|sea": [("the ocean roars loud", "the sea roars loud"),
                  ("the ocean churns wild", "the sea churns wild")],
    "rocks|stones": [("the rocks feel rough", "the stones feel rough"),
                     ("grey rocks ahead", "grey stones ahead")],
    "forest|woods": [("the forest looks green", "the woods looks green"),
                     ("dark forest ahead", "dark woods ahead")],
    "miles|leagues": [("ten miles to go", "ten leagues to go"),
                      ("five miles remain", "five leagues remain")],
    "mountain|peak": [("the mountain rises high", "the peak rises high"),
                       ("the mountain looms large", "the peak looms large")],
    "clouds|mist": [("the clouds drift slow", "the mist drift slow"),
                    ("low clouds today", "low mist today")],
    "teacher|instructor": [("the teacher speaks clear", "the instructor speaks clear"),
                           ("the teacher guides well", "the instructor guides well")],
    "student|pupil": [("the student learns fast", "the pupil learns fast"),
                      ("the student reads daily", "the pupil reads daily")],
    "journey|voyage": [("the journey lasted long", "the voyage lasted long"),
                       ("the journey ended well", "the voyage ended well")],
    "ship|boat": [("the ship sails fast", "the boat sails fast"),
                  ("the ship docks early", "the boat docks early")],
}
assert set(para_frames) == set(para_pairs)
# each frame pair must differ in exactly one word (R3 requirement)
for pk, frames in para_frames.items():
    for s1, s2 in frames:
        w1, w2 = s1.split(), s2.split()
        assert len(w1) == len(w2), (pk, s1, s2)
        diff = sum(1 for a, b in zip(w1, w2) if a != b)
        assert diff == 1, (pk, s1, s2)

adv_pos = [p.split('|') for p in
    "dog|canine guarded|watched sheep|flock night|darkness "
    "sanction|penalty punished|fined traders|merchants cheating|fraud".split()]
assert len(adv_pos) == 8

negatives = ["a wolf is not a dog.", "borrow is not lend.",
             "cheap is not free.", "hot is not spicy."]

multihop = [p.split('|') for p in
    "sofa|couch couch|settee old|aged begin|start start|commence meeting|gathering "
    "happy|glad glad|joyful child|kid quick|fast fast|rapid jumped|leapt".split()]
assert len(multihop) == 12

morph = [p.split('|') for p in
    "go|went market|bazaar mouse|mice ate|devoured "
    "child|children played|frolicked tooth|teeth ached|throbbed".split()]
assert len(morph) == 8
morph_past = {"go|went", "ate|devoured", "played|frolicked", "ached|throbbed"}
morph_plural = {"mouse|mice", "child|children", "tooth|teeth"}

def form_sentence(w1, w2):
    key = f"{w1}|{w2}"
    if key in morph_past:
        return f"{w2} is the past form of {w1}."
    if key in morph_plural:
        return f"{w2} is the plural form of {w1}."
    # market|bazaar: plain synonym pair; inert sentence (no rule consumes it)
    return f"{w2} is another word for {w1}."

lines = []
n = [0]
def emit(pattern, text, subj=None):
    n[0] += 1
    lid = f"LEARN-{n[0]:04d}"
    if subj is None:
        lines.append(f"LEARN|{lid}|{pattern}|{text}")
    else:
        lines.append(f"LEARN|{lid}|{pattern}|{subj}|{text}")
    return lid

relations = set()
def add_rel(w1, w2):
    relations.add(tuple(sorted((w1, w2))))

for w1, w2 in pairs56:
    emit("DEF", def_line(w1, w2)); emit("SYN", syn_line(w1, w2)); add_rel(w1, w2)
for w1, w2 in fresh:
    emit("DEF", def_line(w1, w2)); emit("SYN", syn_line(w1, w2)); add_rel(w1, w2)
for pk in para_pairs:
    for si, (s1, s2) in enumerate(para_frames[pk], 1):
        subj = f"para_{pk.split('|')[0]}_{si}"
        emit("PARA", s1, subj); emit("PARA", s2, subj)
for w1, w2 in adv_pos:
    emit("DEF", def_line(w1, w2)); emit("SYN", syn_line(w1, w2)); add_rel(w1, w2)
for t in negatives:
    emit("NEG", t)
for w1, w2 in multihop:
    emit("DEF", def_line(w1, w2)); emit("SYN", syn_line(w1, w2)); add_rel(w1, w2)
for w1, w2 in morph:
    emit("SYN", syn_line(w1, w2))
    # form sentence: labeled DEF (definitional about word forms) but INERT under
    # R1, whose surface patterns are only "a|an X is a|an Y." / "X is a kind of Y."
    emit("DEF", form_sentence(w1, w2)); add_rel(w1, w2)

# --- frozen assertions ---
assert len(relations) == 112, f"positive relations: {len(relations)}"
assert sum(1 for l in lines if l.split('|')[2] == 'NEG') == 4
assert len(lines) == 276, len(lines)
# no test query text may appear: check against the frozen query files
queries = []
for qf in ['/home/hatch/workspace/tnn-lab/cognition_ws/ws2l/queries_ws2l.txt']:
    for ln in open(qf):
        ln = ln.rstrip('\n')
        if ln:
            queries.append(ln.split('|')[6])
corpus_text = '\n'.join(lines)
for q in queries:
    assert q not in corpus_text, f"query leak: {q}"
print(f"OK: {len(lines)} lines, {len(relations)} positive relations, 4 negatives")
sys.stdout.write('\n'.join(lines) + '\n')
