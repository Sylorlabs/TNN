#!/usr/bin/env python3
"""Generate the frozen dialogue battery: kb.txt, gaz.txt, battery.txt, KB.md.
All expected answers are the mechanism-honest targets derived in the prereg;
the binary + independent oracle decide pass/fail. Deterministic output.
"""
import os

D = os.path.dirname(os.path.abspath(__file__))

FACTS = [
    "Herman Melville wrote the novel Moby Dick.",
    "Herman Melville was born in 1819.",
    "Moby Dick was published in 1851.",
    "Moby Dick was written by Herman Melville.",
    "Jane Austen wrote the novel Pride and Prejudice.",
    "Jane Austen was born in 1775.",
    "Pride and Prejudice was published in 1813.",
    "Pride and Prejudice was written by Jane Austen.",
    "Charles Darwin wrote On the Origin of Species.",
    "Charles Darwin was born in 1809.",
    "On the Origin of Species was published in 1859.",
    "On the Origin of Species was written by Charles Darwin.",
    "Marie Curie discovered radium.",
    "Marie Curie was born in 1867.",
    "Marie Curie won the Nobel Prize in 1903.",
    "Andy Weir wrote The Martian.",
    "Andy Weir was born in 1972.",
    "The Martian was published in 2011.",
    "The Eiffel Tower is in Paris.",
    "The Eiffel Tower was built in 1889.",
    "The Eiffel Tower is 330 meters tall.",
    "The Montparnasse Tower is in Paris.",
    "The Montparnasse Tower was built in 1973.",
    "The Montparnasse Tower is 210 meters tall.",
    "The Louvre is in Paris.",
    "The Louvre opened as a museum in 1793.",
    "The Statue of Liberty is a landmark in New York.",
    "The Statue of Liberty was dedicated in 1886.",
    "The Statue of Liberty is 93 meters tall.",
    "Big Ben is a landmark in London.",
    "Big Ben is 96 meters tall.",
    "The Colosseum is in Rome.",
    "The Colosseum was completed in 80 AD.",
    "Paris is the capital of France.",
    "Berlin is the capital of Germany.",
    "Water boils at 100 degrees Celsius at sea level.",
    "Mount Everest is 8849 meters tall.",
    "The Amazon River is 6400 kilometers long.",
]
F = {i: t for i, t in enumerate(FACTS)}

# (name, class 0=person 1=other)
ENTITIES = [
    ("herman melville", 0), ("jane austen", 0), ("charles darwin", 0),
    ("marie curie", 0), ("andy weir", 0),
    ("moby dick", 1), ("pride and prejudice", 1), ("on the origin of species", 1),
    ("the martian", 1), ("radium", 1), ("nobel prize", 1),
    ("eiffel tower", 1), ("montparnasse tower", 1), ("louvre", 1),
    ("statue of liberty", 1), ("big ben", 1), ("colosseum", 1),
    ("paris", 1), ("berlin", 1), ("france", 1), ("germany", 1),
    ("new york", 1), ("london", 1), ("rome", 1),
    ("mount everest", 1), ("amazon river", 1), ("water", 1),
]

dialogues = []  # (id, type, [(U, E), ...])

def add(did, typ, turns):
    dialogues.append((did, typ, turns))

# ---------------- FOLLOWUP (15) ----------------
fu_chains = [
    [("Who wrote Moby Dick?", F[0]), ("And when was he born?", F[1]),
     ("When was Moby Dick published?", F[2])],
    [("Who wrote Pride and Prejudice?", F[4]), ("And when was she born?", F[5]),
     ("When was Pride and Prejudice published?", F[6])],
    [("Who wrote On the Origin of Species?", F[8]), ("And when was he born?", F[9]),
     ("When was On the Origin of Species published?", F[10])],
    [("Tell me about the Eiffel Tower.", F[18]), ("How tall is it?", F[20]),
     ("When was it built?", F[19])],
    [("Tell me about the Montparnasse Tower.", F[21]), ("How tall is it?", F[23]),
     ("When was it built?", F[22])],
    [("Tell me about the Statue of Liberty.", F[27]), ("How tall is it?", F[28]),
     ("When was it dedicated?", F[27])],
    [("Who discovered radium?", F[12]), ("When was she born?", F[13]),
     ("What prize did she win?", F[14])],
    [("How tall is Mount Everest?", F[36]), ("How tall is it?", F[36]),
     ("What about the Amazon River?", F[37])],
    [("What is the capital of France?", F[33]), ("And Germany?", F[34]),
     ("Berlin is in Germany.", "NOTED.")],
]
# 9 chains -> need 15 dialogues: repeat first 6 chains with new ids (same coverage, fresh state)
fu_all = fu_chains + fu_chains[:6]
for i, ch in enumerate(fu_all):
    add(f"FU-{i+1:02d}", "FOLLOWUP", ch)

# ---------------- CORRECTION (15 = 5 pairs x 3 phrasings) ----------------
corr_pairs = [
    [("Tell me about the tower.", F[18]), ("<C>", F[21]), ("How tall is it?", F[23])],
    [("Tell me a European capital.", F[33]), ("<C>", F[34]),
     ("What country is it the capital of?", F[34])],
    # novel pair: 3 novels in KB, so "the other one" is ambiguous for v1;
    # name the work directly to keep the correction unambiguous
    [("Who wrote Moby Dick?", F[0]), ("<C-NOVEL>", F[4]), ("When was she born?", F[5])],
    [("Tell me about a landmark.", F[29]), ("<C>", F[26]), ("How tall is it?", F[28])],
    [("How tall is the Eiffel Tower?", F[20]), ("<C>", F[23]), ("When was it built?", F[22])],
]
corr_phrase = ["No, I meant the other one.", "Not that one, the other.", "No \u2014 the other one."]
corr_phrase_novel = ["No, I meant the one Jane Austen wrote.", "Not that one, the one Jane Austen wrote.", "No \u2014 the one Jane Austen wrote."]
n = 0
for pi, pair in enumerate(corr_pairs):
    phs = corr_phrase_novel if pi==2 else corr_phrase
    for ph in phs:
        n += 1
        turns = [(pair[0][0], pair[0][1]), (ph, pair[1][1]), (pair[2][0], pair[2][1])]
        add(f"CO-{n:02d}", "CORRECTION", turns)

# ---------------- REFERENT (15 = 5 x 3) ----------------
ref_chains = [
    [("Tell me about the Eiffel Tower.", F[18]), ("How tall is it?", F[20]),
     ("What about the Louvre?", F[24]), ("When did it open?", F[25])],
    [("Who wrote Moby Dick?", F[0]), ("When was he born?", F[1]),
     ("Who wrote Pride and Prejudice?", F[4]), ("When was she born?", F[5])],
    [("Tell me about the Statue of Liberty.", F[27]), ("How tall is it?", F[28]),
     ("What about Big Ben?", F[30]), ("Is it a landmark?", F[29])],
    [("Who discovered radium?", F[12]), ("When was she born?", F[13]),
     ("Who wrote The Martian?", F[15]), ("When was he born?", F[16])],
    [("What is the capital of France?", F[33]), ("And Germany?", F[34]),
     ("Which country is Paris the capital of?", F[33]), ("And Berlin?", F[34])],
]
ref_all = ref_chains * 3
for i, ch in enumerate(ref_all):
    add(f"RE-{i+1:02d}", "REFERENT", ch)

# ---------------- WEIRD (15) + WEIRD_CLEAN (15) ----------------
weird_pairs = [
    # (weird turn, expected, clean twin, expected, follow-up, expected)
    ("Who wrote Moby Dickk?", F[0], "Who wrote Moby Dick?", F[0],
     "And when was he born?", F[1]),
    ("so like, who wrote moby dick fr", F[0], "Who wrote Moby Dick?", F[0],
     "And when was he born?", F[1]),
    ("moby dick \u2014 written by whom?", F[3], "By whom was Moby Dick written?", F[3],
     "When was it published?", F[2]),
    ("tell me about the dude who wrote moby dick", F[0], "Who wrote Moby Dick?", F[0],
     "And when was he born?", F[1]),
    ("pride and prejudice was written by whom?", F[7],
     "By whom was Pride and Prejudice written?", F[7],
     "When was it published?", F[6]),
    ("yo, how tall is that eiffel tower thing?", F[20], "How tall is the Eiffel Tower?", F[20],
     "When was it built?", F[19]),
    ("When was Herman Melvile born?", F[1], "When was Herman Melville born?", F[1],
     "When was Moby Dick published?", F[2]),
    ("eiffel tower \u2014 built when?", F[19], "When was the Eiffel Tower built?", F[19],
     "How tall is it?", F[20]),
    # hard case: indirect wording the keyword core cannot bridge (honest gap probe)
    ("i'm curious about the birth year of the guy who wrote the martian", F[16],
     "When was Andy Weir born?", F[16],
     "When was The Martian published?", F[17]),
    ("big ben \u2014 how tall??", F[30], "How tall is Big Ben?", F[30],
     "Is it a landmark?", F[29]),
    ("who discovered radium???", F[12], "Who discovered radium?", F[12],
     "When was she born?", F[13]),
    ("the louvre \u2014 where is it??", F[24], "Where is the Louvre?", F[24],
     "When did it open?", F[25]),
    ("moby dick published when??", F[2], "When was Moby Dick published?", F[2],
     "Who wrote it?", F[0]),
    ("capital of france??", F[33], "What is the capital of France?", F[33],
     "And Germany?", F[34]),
    ("tell me bout the colosseum", F[31], "Tell me about the Colosseum.", F[31],
     "When was it completed?", F[32]),
]
for i, (w, we, c, ce, f2, f2e) in enumerate(weird_pairs):
    add(f"WE-{i+1:02d}", "WEIRD", [(w, we), (f2, f2e)])
    add(f"WC-{i+1:02d}", "WEIRD_CLEAN", [(c, ce), (f2, f2e)])

# ---------------- TOPIC (15 = 5 x 3) ----------------
topic_chains = [
    [("Tell me about the Eiffel Tower.", F[18]), ("What about the Louvre?", F[24]),
     ("Anyway, back to the tower.", F[18]), ("And how tall is it?", F[20])],
    [("Who wrote Moby Dick?", F[0]), ("What about Pride and Prejudice?", F[6]),
     ("Back to Moby Dick.", F[0]), ("When was he born?", F[1])],
    [("What is the capital of France?", F[33]), ("What is the capital of Germany?", F[34]),
     ("Anyway, back to the first one.", F[33]), ("And Germany?", F[34])],
    [("Who discovered radium?", F[12]), ("Who wrote The Martian?", F[15]),
     ("Back to Curie.", F[12]), ("When was she born?", F[13])],
    [("How tall is Mount Everest?", F[36]), ("How long is the Amazon River?", F[37]),
     ("Anyway, back to the mountain.", F[36]), ("And how tall is it?", F[36])],
]
topic_all = topic_chains * 3
for i, ch in enumerate(topic_all):
    add(f"TO-{i+1:02d}", "TOPIC", ch)

# ---------------- CONTRADICT (15 = 12 true + 3 consistent) ----------------
contras = [
    [("Who wrote Moby Dick?", F[0]),
     ("Herman Melville wrote Moby Dick.", "NOTED."),
     ("When was he born?", F[1]),
     ("Actually, Jane Austen wrote Moby Dick.", "CONTRADICTION: turn 2 said herman melville."),
     ("OK, when was Moby Dick published?", F[2])],
    [("Who wrote Pride and Prejudice?", F[4]),
     ("Jane Austen wrote Pride and Prejudice.", "NOTED."),
     ("When was she born?", F[5]),
     ("But Charles Darwin wrote Pride and Prejudice.", "CONTRADICTION: turn 2 said jane austen."),
     ("OK, when was Pride and Prejudice published?", F[6])],
    [("Who wrote The Martian?", F[15]),
     ("Andy Weir wrote The Martian.", "NOTED."),
     ("When was he born?", F[16]),
     ("But Herman Melville wrote The Martian.", "CONTRADICTION: turn 2 said andy weir."),
     ("When was The Martian published?", F[17])],
    [("When was Herman Melville born?", F[1]),
     ("Herman Melville was born in 1819.", "NOTED."),
     ("Who wrote Moby Dick?", F[0]),
     ("But Herman Melville was born in 1820.", "CONTRADICTION: turn 2 said 1819."),
     ("When was Moby Dick published?", F[2])],
    [("When was Jane Austen born?", F[5]),
     ("Jane Austen was born in 1775.", "NOTED."),
     ("Who wrote Pride and Prejudice?", F[4]),
     ("But Jane Austen was born in 1800.", "CONTRADICTION: turn 2 said 1775."),
     ("When was Pride and Prejudice published?", F[6])],
    [("When was Marie Curie born?", F[13]),
     ("Marie Curie was born in 1867.", "NOTED."),
     ("Who discovered radium?", F[12]),
     ("But Marie Curie was born in 1900.", "CONTRADICTION: turn 2 said 1867."),
     ("What prize did she win?", F[14])],
    [("How tall is the Eiffel Tower?", F[20]),
     ("The Eiffel Tower is 330 meters tall.", "NOTED."),
     ("When was it built?", F[19]),
     ("But the Eiffel Tower is 300 meters tall.", "CONTRADICTION: turn 2 said 330."),
     ("Where is the Eiffel Tower?", F[18])],
    [("How tall is Big Ben?", F[30]),
     ("Big Ben is 96 meters tall.", "NOTED."),
     ("Is it a landmark?", F[29]),
     ("But Big Ben is 100 meters tall.", "CONTRADICTION: turn 2 said 96."),
     ("Is Big Ben a landmark?", F[29])],
    [("How tall is the Montparnasse Tower?", F[23]),
     ("The Montparnasse Tower is 210 meters tall.", "NOTED."),
     ("When was it built?", F[22]),
     ("But the Montparnasse Tower is 250 meters tall.", "CONTRADICTION: turn 2 said 210."),
     ("Where is the Montparnasse Tower?", F[21])],
    [("What is the capital of France?", F[33]),
     ("Paris is the capital of France.", "NOTED."),
     ("What is the capital of Germany?", F[34]),
     ("But Berlin is the capital of France.", "CONTRADICTION: turn 2 said paris."),
     ("And Germany?", F[34])],
    [("What is the capital of Germany?", F[34]),
     ("Berlin is the capital of Germany.", "NOTED."),
     ("What is the capital of France?", F[33]),
     ("But Paris is the capital of Germany.", "CONTRADICTION: turn 2 said berlin."),
     ("Tell me about Berlin.", F[34])],
    [("Where is the Eiffel Tower?", F[18]),
     ("The Eiffel Tower is in Paris.", "NOTED."),
     ("How tall is it?", F[20]),
     ("But the Eiffel Tower is in London.", "CONTRADICTION: turn 2 said paris."),
     ("When was it built?", F[19])],
    # consistent controls: no false alarms
    [("How tall is Big Ben?", F[30]),
     ("Big Ben is 96 meters tall.", "NOTED."),
     ("Big Ben is 96 meters tall.", "NOTED."),
     ("Is it in London?", F[29])],
    [("Who wrote Moby Dick?", F[0]),
     ("Moby Dick was written by Herman Melville.", "NOTED."),
     ("Herman Melville wrote Moby Dick.", "NOTED."),
     ("When was he born?", F[1])],
    [("What is the capital of France?", F[33]),
     ("Paris is the capital of France.", "NOTED."),
     ("Paris is the capital of France.", "NOTED."),
     ("And Germany?", F[34])],
]
for i, ch in enumerate(contras):
    add(f"CT-{i+1:02d}", "CONTRADICT", ch)

# ---------------- COMPOSE (10) ----------------
composes = [
    [("Who wrote Moby Dick?", F[0]),
     ("When was the Eiffel Tower built?", F[19]),
     ("Was the author of Moby Dick born before the Eiffel Tower was built?", "yes.")],
    [("Who wrote Pride and Prejudice?", F[4]),
     ("When was the Eiffel Tower built?", F[19]),
     ("Was the author of Pride and Prejudice born before the Eiffel Tower was built?", "yes.")],
    [("Who wrote The Martian?", F[15]),
     ("When was the Montparnasse Tower built?", F[22]),
     ("Was the author of The Martian born before the Montparnasse Tower was built?", "yes.")],
    [("Who wrote The Martian?", F[15]),
     ("When was the Eiffel Tower built?", F[19]),
     ("Was the author of The Martian born before the Eiffel Tower was built?", "no.")],
    [("How tall is the Eiffel Tower?", F[20]),
     ("How tall is the Montparnasse Tower?", F[23]),
     ("Which is taller, the Eiffel Tower or the Montparnasse Tower?", "the eiffel tower is taller.")],
    [("How tall is the Statue of Liberty?", F[28]),
     ("How tall is Big Ben?", F[30]),
     ("Which is taller, the Statue of Liberty or Big Ben?", "big ben is taller.")],
    [("How tall is the Eiffel Tower?", F[20]),
     ("How tall is Big Ben?", F[30]),
     ("Which is taller, the Eiffel Tower or Big Ben?", "the eiffel tower is taller.")],
    [("Who wrote Moby Dick?", F[0]),
     ("Who wrote Pride and Prejudice?", F[4]),
     ("Did the author of Moby Dick write Pride and Prejudice?", "no.")],
    [("Who wrote Pride and Prejudice?", F[4]),
     ("Did Jane Austen write Pride and Prejudice?", "yes.")],
    [("Who wrote On the Origin of Species?", F[8]),
     ("Did Charles Darwin write On the Origin of Species?", "yes.")],
]
for i, ch in enumerate(composes):
    add(f"CP-{i+1:02d}", "COMPOSE", ch)

# ---------------- write files ----------------
with open(os.path.join(D, "kb.txt"), "w") as f:
    for i, t in F.items():
        f.write(f"{i}\t{t}\n")

with open(os.path.join(D, "gaz.txt"), "w") as f:
    for i, (name, cls) in enumerate(ENTITIES):
        f.write(f"{i}\t{cls}\t{name}\n")

with open(os.path.join(D, "battery.txt"), "w") as f:
    for did, typ, turns in dialogues:
        f.write(f"DIALOGUE {did} {typ}\n")
        for u, e in turns:
            f.write(f"U {u}\nE {e}\n")
        f.write("END\n")

with open(os.path.join(D, "KB.md"), "w") as f:
    f.write("# Dialogue battery knowledge base (38 facts)\n\n")
    for i, t in F.items():
        f.write(f"{i}. {t}\n")
    f.write("\n## Entities\n\n")
    for i, (name, cls) in enumerate(ENTITIES):
        f.write(f"{i}. {name} ({'person' if cls == 0 else 'other'})\n")

n_turns = sum(len(t) for _, _, t in dialogues)
print(f"dialogues={len(dialogues)} turns={n_turns}")
from collections import Counter
print(Counter(typ for _, typ, _ in dialogues))
