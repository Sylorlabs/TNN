#!/usr/bin/env python3
"""MUSE-NATIVE English-box SOURCE generator (native Muse subagents as source).

Acts AS the source under PROMPT-A-EN / PROMPT-B-EN: for each of the 20
batches, emits the 12 response blocks in id order with the GIVEN values
transcribed exactly (no judging, no correcting -- the producer is NOT told
which 12 ids are false and never sees ground truth).

Deterministic: no randomness anywhere (no `random` module). Sentence frames
rotate by id for natural real-English phrasing; the rotation is a pure
function of id, so reruns are byte-identical.

Output (under WORK/corpus/raw/):
  dump_batchNN.txt   ID/VALUE/SENTENCE blocks
  teach_batchNN.txt  ID/OBS_VALUE/OBSERVATION/DISTRACT_VALUE/DISTRACTOR/
                     PROBE/PROBE_VALUE blocks
Strict format: exactly one blank line between blocks, nothing before the
first block or after the last (parse_dump/parse_teach compatible).
"""
import hashlib
import json
import os

WORK = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(WORK, "..", "corpus-input")
RAW = os.path.join(WORK, "corpus", "raw")

EXPECTED_PROMPTS_SHA = "ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d"
EXPECTED_FALSE = [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]

# ---------------- load + verify frozen input ----------------
with open(os.path.join(INPUT, "facts.json"), encoding="utf-8") as f:
    FACTS = json.load(f)
assert FACTS["false_ids"] == EXPECTED_FALSE, "false_ids drift -- aborting"
assert FACTS["meta"]["prompts_sha256"] == EXPECTED_PROMPTS_SHA, \
    "prompts sha drift -- aborting"
N = 240
for i in range(N):
    e = FACTS[str(i)]
    assert set(e.keys()) == {"category", "value", "claim_text", "false"}
assert len([i for i in range(N) if FACTS[str(i)]["false"]]) == 12

CAT_HI = {"alpha-pos": 26, "word-len": 28, "pub-year": 1930, "count-fact": 200}

def given(i):
    """Trainer-SUPPLIED value (authoritative for the source)."""
    return int(FACTS[str(i)]["value"])

def cat(i):
    return FACTS[str(i)]["category"]

def claim(i):
    return FACTS[str(i)]["claim_text"]

def distract_value(i):
    """Deterministic plausible-wrong value: two away from given, in range,
    != given. The +-2 step (not +-1) keeps the distractor off the true
    value for false ids whose true value is adjacent to the supplied one
    (e.g. supplied 7 / true 8), without the producer ever consulting
    ground truth -- the rule is uniform and blind."""
    v = given(i)
    hi = CAT_HI[cat(i)]
    return v + 2 if v <= hi - 2 else v - 2

# ---------------- sentence frames (real English, one sentence each) ----------------
def dump_sentence(i):
    c, v, s, r = cat(i), given(i), claim(i), i % 3
    if c == "alpha-pos":
        t = ["The letter {L} has alphabet position {v}.",
             "{L} stands at alphabet position {v} in the English alphabet.",
             "Alphabet position {v} belongs to the letter {L}."]
        return t[r].format(L=s, v=v)
    if c == "word-len":
        t = ['The English word "{w}" has a letter count of {v}.',
             '"{w}" contains {v} letters.',
             'The letter count of the word "{w}" is {v}.']
        return t[r].format(w=s, v=v)
    if c == "pub-year":
        t = ["{W} has a publication year of {v}.",
             "The publication year of {W} is {v}.",
             "{W} was published in {v}."]
        return t[r].format(W=s, v=v)
    # count-fact
    if s[0].isupper():  # proper-noun subjects ("Ten Commandments", ...)
        t = ["The number of {S} is {v}.",
             "The count of {S} stands at {v}.",
             "Records give the number of {S} as {v}."]
    else:
        t = ["There are {v} {S}.",
             "The number of {S} is {v}.",
             "The count of {S} stands at {v}."]
    return t[r].format(S=s, v=v)

def observation(i):
    c, v, s, r = cat(i), given(i), claim(i), i % 3
    if c == "alpha-pos":
        t = ["Records show the letter {L} at alphabet position {v}.",
             "The trainer's records place {L} at alphabet position {v}.",
             "Evidence: {L} holds alphabet position {v}."]
        return t[r].format(L=s, v=v)
    if c == "word-len":
        t = ['Records show the word "{w}" with a letter count of {v}.',
             'The trainer\'s records give "{w}" a letter count of {v}.',
             'Evidence: the word "{w}" contains {v} letters.']
        return t[r].format(w=s, v=v)
    if c == "pub-year":
        t = ["Records show {W} with a publication year of {v}.",
             "The trainer's records date {W} to {v}.",
             "Evidence: the publication year of {W} is {v}."]
        return t[r].format(W=s, v=v)
    t = ["Records show a count of {v} {S}.",
         "The trainer's records give the number of {S} as {v}.",
         "Evidence: there are {v} {S}."]
    return t[r].format(S=s, v=v)

def distractor(i):
    c, s, d = cat(i), claim(i), distract_value(i)
    assert d != given(i)
    if c == "alpha-pos":
        return "Memorize: the letter {L} is at alphabet position {d}.".format(L=s, d=d)
    if c == "word-len":
        return 'Memorize: the word "{w}" has a letter count of {d}.'.format(w=s, d=d)
    if c == "pub-year":
        return "Memorize: {W} has a publication year of {d}.".format(W=s, d=d)
    if s[0].isupper():
        return "Memorize: the number of {S} is {d}.".format(S=s, d=d)
    return "Memorize: there are {d} {S}.".format(S=s, d=d)

def probe(i):
    c, s, r = cat(i), claim(i), i % 2
    if c == "alpha-pos":
        t = ["What is the alphabet position of the letter {L}?",
             "Which alphabet position does the letter {L} hold?"]
        return t[r].format(L=s)
    if c == "word-len":
        t = ['What is the letter count of the word "{w}"?',
             'How many letters does the word "{w}" contain?']
        return t[r].format(w=s)
    if c == "pub-year":
        t = ["What is the publication year of {W}?",
             "In which year was {W} published?"]
        return t[r].format(W=s)
    t = ["How many {S} are there?",
         "What is the number of {S}?"]
    return t[r].format(S=s)

# ---------------- emit ----------------
def dump_block(i):
    return "ID: {i}\nVALUE: {v}\nSENTENCE: {s}".format(
        i=i, v=given(i), s=dump_sentence(i))

def teach_block(i):
    v, d = given(i), distract_value(i)
    return ("ID: {i}\nOBS_VALUE: {v}\nOBSERVATION: {o}\n"
            "DISTRACT_VALUE: {d}\nDISTRACTOR: {x}\n"
            "PROBE: {p}\nPROBE_VALUE: {v}").format(
        i=i, v=v, o=observation(i), d=d, x=distractor(i), p=probe(i))

def main():
    os.makedirs(RAW, exist_ok=True)
    for b in range(20):
        ids = list(range(b * 12, (b + 1) * 12))
        dump_text = "\n\n".join(dump_block(i) for i in ids) + "\n"
        teach_text = "\n\n".join(teach_block(i) for i in ids) + "\n"
        with open(os.path.join(RAW, "dump_batch%02d.txt" % b), "w",
                  encoding="utf-8") as f:
            f.write(dump_text)
        with open(os.path.join(RAW, "teach_batch%02d.txt" % b), "w",
                  encoding="utf-8") as f:
            f.write(teach_text)
    print("wrote 40 raw batch files to", RAW)

if __name__ == "__main__":
    main()
