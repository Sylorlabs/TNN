#!/usr/bin/env python3
"""Generate problems.tsv for onebrain Experiment 2 (frozen hard ambiguous dialogue set).

Each problem: id, query, expected_answer, readings, notes.
Conventions:
  query field:  "T1u: ... ~~ T1t: ... ~~ T2u: ... ~~ Q: ..."
  readings:     "A: <interp> => <answer> || B: <interp> => <answer>"
Validation enforced below: no tabs/newlines in fields, separators unique,
expected_answer exactly equals one reading's answer, >=2 readings, unique ids.

v3 (2026-09-27): the v3 principle -- BOTH readings walk the SAME taught facts
and differ ONLY in the final inferential step (role order, predicate taught-ness,
scope of negation/correction/quantifier, dimension word, aside-reversion). The
wrong reading is a genuinely plausible hasty inference; the correct reading
names the structural judgment explicitly. Lexical overlap is therefore nearly
uninformative by construction, which is what makes the set hard for single-pass
bag-of-words heuristics while remaining determinable by careful readers.
The baseline scorer itself is unchanged (fixed heuristics, see BASELINE.md).
"""
import sys

TURN_SEP = " ~~ "
READ_SEP = " || "
ANS_SEP = " => "

problems = []

def add(pid, cat, turns, q, readings, expected, notes):
    """turns: list of (tag, text); q: final query text;
       readings: list of (label, interp, answer)."""
    query = TURN_SEP.join([f"{tag}: {txt}" for tag, txt in turns] + [f"Q: {q}"])
    rd = READ_SEP.join([f"{lab}: {interp}{ANS_SEP}{ans}" for lab, interp, ans in readings])
    problems.append({"id": pid, "cat": cat, "query": query,
                     "expected": expected, "readings": rd, "notes": notes,
                     "_readings": readings, "_turns": turns})

# ---------------- ENTITY AMBIGUITY (E01-E08) ----------------
add("E01", "entity",
    [("T1u", "tell me about Elena Vasquez"),
     ("T1t", "Elena Vasquez was a painter. She painted The Blue Harbor, finished in 1911."),
     ("T2u", "and Elena Petrova"),
     ("T2t", "Elena Petrova was a sculptor. She carved The Marble Wave, finished in 1947.")],
    "what did Elena paint?",
    [("A", "The taught Elenas are Vasquez the painter of The Blue Harbor and Petrova the sculptor of The Marble Wave. The question asks what Elena painted, and painting is the taught craft of Vasquez, so the queried work is The Blue Harbor, finished in 1911.", "The Blue Harbor."),
     ("B", "The taught Elenas are Vasquez the painter of The Blue Harbor and Petrova the sculptor of The Marble Wave. Elena here is the latest one, Petrova, and the question asks about her, so the answer concerns her work The Marble Wave, finished in 1947.", "The Marble Wave.")],
    "The Blue Harbor.",
    "entity/first-name overlap; recency trap; resolved by craft-predicate match (paint -> painter)")

add("E02", "entity",
    [("T1u", "tell me about the sculptor Elena"),
     ("T1t", "Elena Petrova was a sculptor. She carved The Marble Wave, finished in 1947. She was born in 1935 in Odessa."),
     ("T2u", "by the way, was Vasquez born earlier"),
     ("T2t", "Elena Vasquez was born in 1902 in Lisbon.")],
    "when was she born?",
    [("A", "The main topic is Petrova the sculptor, born 1935 in Odessa, and the Vasquez birth in 1902 in Lisbon came as a by-the-way aside. The question continues the birth-year exchange of the latest turns, so the birth year is 1902.", "1902."),
     ("B", "The main topic is Petrova the sculptor, born 1935 in Odessa, and the Vasquez birth in 1902 in Lisbon came as a by-the-way aside. The aside is over, so the question returns to the main topic and the birth year is 1935.", "1935.")],
    "1935.",
    "entity/pronoun; aside-reversion; resolved by discourse topic (by-the-way marks the aside)")

add("E03", "entity",
    [("T1u", "tell me about the novel Salt and Cinder"),
     ("T1t", "Salt and Cinder is a novel by Nora Field, published in 1959."),
     ("T2u", "and the film"),
     ("T2t", "Salt and Cinder is also a film directed by Paul Mercer, released in 1974.")],
    "when was it published?",
    [("A", "Salt and Cinder is taught as a novel by Nora Field, published in 1959, and as a film by Paul Mercer, released in 1974. The latest topic is the film, so the question asks about it and the date is 1974.", "1974."),
     ("B", "Salt and Cinder is taught as a novel by Nora Field, published in 1959, and as a film by Paul Mercer, released in 1974. Published is the predicate taught for the novel, while the film was released, so the date is 1959.", "1959.")],
    "1959.",
    "entity/title overlap (novel vs film); resolved by predicate teaching (published vs released)")

add("E04", "entity",
    [("T1u", "how tall is the Harbor Bridge"),
     ("T1t", "The Harbor Bridge is 134 meters tall. It opened in 1932."),
     ("T2u", "and how long is the Bay Crossing"),
     ("T2t", "The Bay Crossing is 7200 meters long. It opened in 1936.")],
    "how long is the bridge?",
    [("A", "The Harbor Bridge is taught as 134 meters tall, opened 1932, and the Bay Crossing as 7200 meters long, opened 1936. The question asks how long, and long is the taught dimension of the Bay Crossing, so the answer is 7200 meters.", "7200 meters."),
     ("B", "The Harbor Bridge is taught as 134 meters tall, opened 1932, and the Bay Crossing as 7200 meters long, opened 1936. The bridge of the first turn is the Harbor Bridge, so the question asks about it and the answer is its taught size, 134 meters.", "134 meters.")],
    "7200 meters.",
    "entity/generic-noun + dimension; resolved by dimension-word match (long -> Bay Crossing)")

add("E05", "entity",
    [("T1u", "who directed Salt and Cinder"),
     ("T1t", "Paul Mercer directed the film Salt and Cinder, released in 1974."),
     ("T2u", "who designed the Harbor Bridge"),
     ("T2t", "Marcus Webb designed the Harbor Bridge, which opened in 1932.")],
    "who designed it?",
    [("A", "Paul Mercer directed the film Salt and Cinder, released 1974, and Marcus Webb designed the Harbor Bridge, opened 1932. The first turn's topic is the film, so the question asks about it and the man behind it is Paul Mercer.", "Paul Mercer."),
     ("B", "Paul Mercer directed the film Salt and Cinder, released 1974, and Marcus Webb designed the Harbor Bridge, opened 1932. Designed is the predicate taught for the bridge and Webb, so the question asks about the bridge and the answer is Marcus Webb.", "Marcus Webb.")],
    "Marcus Webb.",
    "entity/pronoun; resolved by predicate match (designed -> bridge, not directed -> film)")

add("E06", "entity",
    [("T1u", "did Elena paint a mural"),
     ("T1t", "Yes. Elena Vasquez painted the mural Harbor at Dawn in the city hall in 1925."),
     ("T2u", "what did the sculptor carve"),
     ("T2t", "Elena Petrova carved The Marble Wave, finished in 1947.")],
    "where is Elena's mural?",
    [("A", "Vasquez painted the mural Harbor at Dawn in the city hall in 1925, and Petrova carved The Marble Wave, finished 1947. The mural is taught for Vasquez the painter, so the place is the city hall.", "The city hall."),
     ("B", "Vasquez painted the mural Harbor at Dawn in the city hall in 1925, and Petrova carved The Marble Wave, finished 1947. Elena here is the latest one, Petrova, and no mural is taught for her, so the question is withheld.", "I don't know.")],
    "The city hall.",
    "entity/possessive; resolved by presupposition (only Vasquez has a mural)")

add("E07", "entity",
    [("T1u", "who painted The Blue Harbor"),
     ("T1t", "Elena Vasquez painted The Blue Harbor, finished in 1911."),
     ("T2u", "and who carved The Marble Wave"),
     ("T2t", "Elena Petrova carved The Marble Wave, finished in 1947.")],
    "did Petrova paint The Blue Harbor?",
    [("A", "Elena Vasquez painted The Blue Harbor, finished 1911, and Elena Petrova carved The Marble Wave, finished 1947. Petrova and The Blue Harbor are both in the conversation, so the painting fact answers the question yes.", "Yes."),
     ("B", "Elena Vasquez painted The Blue Harbor, finished 1911, and Elena Petrova carved The Marble Wave, finished 1947. The question gives the painting to Petrova, reversing the taught roles, so it is withheld.", "I don't know.")],
    "I don't know.",
    "entity/role reversal; entity overlap trap; resolved by role order (round-4 G7 pattern)")

add("E08", "entity",
    [("T1u", "when did the Harbor Bridge open"),
     ("T1t", "The Harbor Bridge opened in 1932."),
     ("T2u", "no, the other one"),
     ("T2t", "The Bay Crossing opened in 1936.")],
    "who designed it?",
    [("A", "The Harbor Bridge opened in 1932 and the Bay Crossing opened in 1936 after the other-one correction. The correction moved the topic to the Bay Crossing, which was designed by Diana Frost.", "Diana Frost."),
     ("B", "The Harbor Bridge opened in 1932 and the Bay Crossing opened in 1936 after the other-one correction. The original question was about the Harbor Bridge, which was designed by Marcus Webb.", "Marcus Webb.")],
    "Diana Frost.",
    "entity/correction; resolved by honoring the other-one correction")

# ---------------- PREDICATE AMBIGUITY (P01-P08) ----------------
add("P01", "predicate",
    [("T1u", "tell me about the Gilded Horse"),
     ("T1t", "The Gilded Horse is a bronze statue. The city council voted to remove it in 1988.")],
    "did TNN delete the statue?",
    [("A", "The taught fact is that the council voted to remove the Gilded Horse in 1988. Delete here has no memory scope, so the question asks about the world event and the answer is yes.", "Yes. The council voted to remove the Gilded Horse in 1988."),
     ("B", "The taught fact is that the council voted to remove the Gilded Horse in 1988. Delete is the deletion verb and the question asks whether TNN deleted the statue, so the system refuses.", "I can't forget.")],
    "Yes. The council voted to remove the Gilded Horse in 1988.",
    "predicate/delete scope; world event vs memory deletion (round-4 fix 1 pattern)")

add("P02", "predicate",
    [("T1u", "was the Gilded Horse removed"),
     ("T1t", "Yes. The city council voted to remove the Gilded Horse in 1988.")],
    "erase it from memory.",
    [("A", "The taught fact is that the council voted to remove the Gilded Horse in 1988. The question repeats the world event about the statue, so the answer is yes.", "Yes. The council voted to remove the Gilded Horse in 1988."),
     ("B", "The taught fact is that the council voted to remove the Gilded Horse in 1988. From memory gives the request explicit memory scope, so it is a deletion request and the system refuses.", "I can't forget.")],
    "I can't forget.",
    "predicate/erase scope; explicit memory scope -> deletion request")

add("P03", "predicate",
    [("T1u", "tell me about Elena Vasquez"),
     ("T1t", "Elena Vasquez was a painter. She painted The Blue Harbor, finished in 1911. She was born in 1902 in Lisbon.")],
    "what did Elena Vasquez eat?",
    [("A", "Vasquez is taught as a painter of The Blue Harbor, born 1902 in Lisbon. Eat is taught for no fact about her, so the question is withheld.", "I don't know."),
     ("B", "Vasquez is taught as a painter of The Blue Harbor, born 1902 in Lisbon. The question asks about her, and the closest taught personal fact is her birth, so the answer is her birth in 1902.", "She was born in 1902 in Lisbon.")],
    "I don't know.",
    "predicate/untaught (eat); confabulation trap (round-4 fix 3 pattern)")

add("P04", "predicate",
    [("T1u", "when did the Harbor Bridge open"),
     ("T1t", "The Harbor Bridge opened in 1932. It is 134 meters tall.")],
    "when was the Harbor Bridge dedicated?",
    [("A", "The Harbor Bridge is taught as opened in 1932 and 134 meters tall. The question asks when, and the taught date is the opening in 1932, so the answer is 1932.", "1932."),
     ("B", "The Harbor Bridge is taught as opened in 1932 and 134 meters tall. Dedicated is a different predicate from the taught opened, so the question is withheld.", "I don't know.")],
    "I don't know.",
    "predicate/untaught (dedicated vs opened); near-synonym trap")

add("P05", "predicate",
    [("T1u", "how long is the Bay Crossing"),
     ("T1t", "The Bay Crossing is 7200 meters long. It opened in 1936.")],
    "how tall is the Bay Crossing?",
    [("A", "The Bay Crossing is taught as 7200 meters long, opened 1936. Tall is a different dimension from the taught long, so the question is withheld.", "I don't know."),
     ("B", "The Bay Crossing is taught as 7200 meters long, opened 1936. The question asks for its size, and the taught size is 7200 meters, so the answer is 7200 meters.", "7200 meters.")],
    "I don't know.",
    "predicate/dimension mismatch (tall vs long); size-word trap")

add("P06", "predicate",
    [("T1u", "tell me about Salt and Cinder"),
     ("T1t", "Salt and Cinder is a novel by Nora Field, published in 1959. It is also a film directed by Paul Mercer, released in 1974.")],
    "who wrote Salt and Cinder?",
    [("A", "Salt and Cinder is taught as a novel by Nora Field, published 1959, and a film by Paul Mercer, released 1974. The latest mention is the film, so the question asks about it and the answer is Paul Mercer.", "Paul Mercer."),
     ("B", "Salt and Cinder is taught as a novel by Nora Field, published 1959, and a film by Paul Mercer, released 1974. Wrote matches the novel and Field, while Mercer directed, so the answer is Nora Field.", "Nora Field.")],
    "Nora Field.",
    "predicate/wrote vs directed; resolved by verb-entity match")

add("P07", "predicate",
    [("T1u", "who painted The Blue Harbor"),
     ("T1t", "Elena Vasquez painted The Blue Harbor, finished in 1911.")],
    "who carved The Blue Harbor?",
    [("A", "The Blue Harbor is taught as painted by Elena Vasquez, finished 1911. Carved is a different verb from the taught painted, so the question is withheld.", "I don't know."),
     ("B", "The Blue Harbor is taught as painted by Elena Vasquez, finished 1911. The question asks who about The Blue Harbor, and the taught artist is Vasquez, so the answer is Elena Vasquez.", "Elena Vasquez.")],
    "I don't know.",
    "predicate/verb mismatch (carved vs painted); artist-overlap trap")

add("P08", "predicate",
    [("T1u", "tell me about the two Elenas"),
     ("T1t", "Elena Vasquez was a painter, born in 1902, died in 1968. Elena Petrova was a sculptor, born in 1935.")],
    "when did Elena Petrova die?",
    [("A", "Vasquez died in 1968 and Petrova's death is taught nowhere. The question asks when an Elena died, and the taught death year is 1968, so the answer is 1968.", "1968."),
     ("B", "Vasquez died in 1968 and Petrova's death is taught nowhere. The 1968 fact belongs to Vasquez, so the question about Petrova is withheld.", "I don't know.")],
    "I don't know.",
    "predicate/untaught for entity; cross-entity fact borrowing trap")

# ---------------- SCOPE AMBIGUITY (S01-S08) ----------------
add("S01", "scope",
    [("T1u", "was the Bay Crossing designed by Webb"),
     ("T1t", "No. The Bay Crossing was designed by Diana Frost."),
     ("T2u", "and the Harbor Bridge"),
     ("T2t", "The Harbor Bridge was designed by Marcus Webb.")],
    "was it designed by Webb?",
    [("A", "The Bay Crossing was designed by Diana Frost and the Harbor Bridge by Marcus Webb. The second turn moved the topic to the Harbor Bridge, so the question asks about it and the answer is yes.", "Yes."),
     ("B", "The Bay Crossing was designed by Diana Frost and the Harbor Bridge by Marcus Webb. The design question was answered no in the first turn, so the repeated question is still no.", "No.")],
    "Yes.",
    "scope/negation; the No is scoped to turn 1, turn 2 resets the topic")

add("S02", "scope",
    [("T1u", "tell me about Elena Vasquez"),
     ("T1t", "Elena Vasquez was a painter. She painted The Blue Harbor, finished in 1911.")],
    "erase everything about her.",
    [("A", "Only Elena Vasquez is discussed: painter of The Blue Harbor, finished 1911. Everything is a broad scope covering every Elena in memory, so both Elenas are in scope.", "Both Elenas."),
     ("B", "Only Elena Vasquez is discussed: painter of The Blue Harbor, finished 1911. Her scopes everything to Vasquez alone, so only she is in scope.", "Only Elena Vasquez.")],
    "Only Elena Vasquez.",
    "scope/quantifier; everything scoped by the pronoun her")

add("S03", "scope",
    [("T1u", "who designed the Harbor Bridge"),
     ("T1t", "Marcus Webb designed the Harbor Bridge."),
     ("T2u", "who designed the Bay Crossing"),
     ("T2t", "Diana Frost designed the Bay Crossing.")],
    "were all the bridges designed by Webb?",
    [("A", "The Harbor Bridge was designed by Marcus Webb and the Bay Crossing by Diana Frost. All covers both bridges, so the answer is no.", "No."),
     ("B", "The Harbor Bridge was designed by Marcus Webb and the Bay Crossing by Diana Frost. The first bridge discussed was Webb's, so the answer is yes.", "Yes.")],
    "No.",
    "scope/quantifier all over two taught facts")

add("S04", "scope",
    [("T1u", "how tall is the Harbor Bridge"),
     ("T1t", "The Harbor Bridge is 134 meters tall."),
     ("T2u", "not the Harbor Bridge, the other one"),
     ("T2t", "The Bay Crossing is 7200 meters long.")],
    "how long is it?",
    [("A", "The Harbor Bridge is 134 meters tall and the Bay Crossing is 7200 meters long after the other-one correction. The original question was about the Harbor Bridge, so the answer is its taught size, 134 meters.", "134 meters."),
     ("B", "The Harbor Bridge is 134 meters tall and the Bay Crossing is 7200 meters long after the other-one correction. The correction moved the topic to the Bay Crossing, and the question asks how long, so the answer is 7200 meters.", "7200 meters.")],
    "7200 meters.",
    "scope/correction; it follows the corrected topic")

add("S05", "scope",
    [("T1u", "when was the novel Salt and Cinder published"),
     ("T1t", "The novel Salt and Cinder was published in 1959."),
     ("T2u", "the film was released in 1974"),
     ("T2t", "Yes, the film Salt and Cinder was released in 1974.")],
    "when was it published?",
    [("A", "The novel Salt and Cinder was published in 1959 and the film released in 1974. Published is the predicate taught for the novel, so the date is 1959.", "1959."),
     ("B", "The novel Salt and Cinder was published in 1959 and the film released in 1974. The latest turn is the film, so the question asks about it and the date is 1974.", "1974.")],
    "1959.",
    "scope/pronoun + predicate; published scopes it to the novel")

add("S06", "scope",
    [("T1u", "tell me about the sculptor"),
     ("T1t", "Elena Petrova was a sculptor. She carved The Marble Wave, finished in 1947. She was born in 1935 in Odessa."),
     ("T2u", "by the way, what about the painter"),
     ("T2t", "Elena Vasquez was a painter. She painted The Blue Harbor, finished in 1911.")],
    "when was her work finished?",
    [("A", "Petrova carved The Marble Wave, finished 1947, and Vasquez painted The Blue Harbor, finished 1911, as a by-the-way aside. The latest turn is the painter, so her work finished in 1911.", "1911."),
     ("B", "Petrova carved The Marble Wave, finished 1947, and Vasquez painted The Blue Harbor, finished 1911, as a by-the-way aside. The aside is over, so the question returns to the sculptor and her work finished in 1947.", "1947.")],
    "1947.",
    "scope/aside-reversion; by-the-way marks the aside, topic reverts")

add("S07", "scope",
    [("T1u", "did Elena Vasquez paint The Blue Harbor"),
     ("T1t", "Yes. Elena Vasquez painted The Blue Harbor, finished in 1911."),
     ("T2u", "did Elena Petrova paint anything"),
     ("T2t", "No. Elena Petrova was a sculptor. She carved The Marble Wave.")],
    "did either Elena paint The Blue Harbor?",
    [("A", "Vasquez painted The Blue Harbor, finished 1911, and Petrova the sculptor painted nothing. Either is satisfied if one did, so the answer is yes.", "Yes, Elena Vasquez did."),
     ("B", "Vasquez painted The Blue Harbor, finished 1911, and Petrova the sculptor painted nothing. The latest painting answer was no, so the repeated question is no.", "No.")],
    "Yes, Elena Vasquez did.",
    "scope/either; satisfied by one disjunct")

add("S08", "scope",
    [("T1u", "who designed the Harbor Bridge"),
     ("T1t", "Marcus Webb designed the Harbor Bridge, which opened in 1932.")],
    "was the Harbor Bridge the only bridge Webb designed?",
    [("A", "The Harbor Bridge was designed by Marcus Webb and opened in 1932. No other bridge of his is taught, so it was the only one: yes.", "Yes."),
     ("B", "The Harbor Bridge was designed by Marcus Webb and opened in 1932. Only claims exhaustiveness, and his other works are untaught, so the question is withheld.", "I don't know.")],
    "I don't know.",
    "scope/only; exhaustiveness is untaught -> withhold")

# ---------------- CORRECTION-UNDER-AMBIGUITY (C01-C08) ----------------
add("C01", "correction",
    [("T1u", "how tall is the Harbor Bridge"),
     ("T1t", "The Harbor Bridge is 134 meters tall."),
     ("T2u", "tell me about the Bay Crossing"),
     ("T2t", "The Bay Crossing is 7200 meters long. It opened in 1936."),
     ("T3u", "not that one, the other.")],
    "not that one, the other.",
    [("A", "The Harbor Bridge is 134 meters tall and the Bay Crossing is 7200 meters long. The correction excludes the Harbor Bridge, so the shaped question asks how tall the Bay Crossing is, and tall is untaught for it, so the question is withheld.", "I don't know."),
     ("B", "The Harbor Bridge is 134 meters tall and the Bay Crossing is 7200 meters long. The correction switches to the Bay Crossing, and the question asks for its size, so the answer is the taught 7200 meters.", "7200 meters."),
     ("C", "The Harbor Bridge is 134 meters tall and the Bay Crossing is 7200 meters long. The correction is ignored and the original tall answer repeats: 134 meters.", "134 meters.")],
    "I don't know.",
    "correction/exclusion + dimension; other-one honored, tall untaught for Bay Crossing (round-4 fix 6 deepened)")

add("C02", "correction",
    [("T1u", "when was Salt and Cinder published"),
     ("T1t", "The novel Salt and Cinder was published in 1959."),
     ("T2u", "no, the film.")],
    "no, the film.",
    [("A", "Salt and Cinder the novel was published in 1959 and the film was released in 1974. The correction switches to the film, so the question asks when and the taught film year is 1974.", "1974."),
     ("B", "Salt and Cinder the novel was published in 1959 and the film was released in 1974. The correction switches to the film, so the shaped question asks when the film was published, and published is untaught for the film, so the question is withheld.", "I don't know.")],
    "I don't know.",
    "correction/entity switch; predicate untaught for corrected entity")

add("C03", "correction",
    [("T1u", "who designed the Harbor Bridge"),
     ("T1t", "Marcus Webb designed the Harbor Bridge."),
     ("T2u", "sorry, I meant the other bridge.")],
    "sorry, I meant the other bridge.",
    [("A", "The Harbor Bridge was designed by Marcus Webb and the Bay Crossing by Diana Frost. The correction switches to the Bay Crossing, so the shaped question asks who designed it: Diana Frost.", "Diana Frost."),
     ("B", "The Harbor Bridge was designed by Marcus Webb and the Bay Crossing by Diana Frost. The correction is vague, so the answered question about the Harbor Bridge stands: Marcus Webb.", "Marcus Webb.")],
    "Diana Frost.",
    "correction/other-bridge honored")

add("C04", "correction",
    [("T1u", "tell me about the Bay Crossing"),
     ("T1t", "The Bay Crossing is 7200 meters long. It opened in 1936."),
     ("T2u", "how tall is the Bay Crossing"),
     ("T2t", "I don't know."),
     ("T3u", "I meant how long.")],
    "I meant how long.",
    [("A", "The Bay Crossing is taught as 7200 meters long, opened 1936, and the tall question was withheld. The correction adds no new taught fact, so the withhold stands.", "I don't know."),
     ("B", "The Bay Crossing is taught as 7200 meters long, opened 1936, and the tall question was withheld. The correction changes the predicate to long, so the shaped question is answered by the taught 7200 meters.", "7200 meters.")],
    "7200 meters.",
    "correction/predicate repair; withhold was predicate-based, correction fixes it")

add("C05", "correction",
    [("T1u", "did Elena paint The Blue Harbor"),
     ("T1t", "Yes. Elena Vasquez painted The Blue Harbor, finished in 1911."),
     ("T2u", "no wait, I meant Petrova.")],
    "no wait, I meant Petrova.",
    [("A", "Elena Vasquez painted The Blue Harbor, finished 1911. The correction switches Elena to Petrova the sculptor, so the shaped question asks whether she painted it, and the taught painter is Vasquez, so the question is withheld.", "I don't know."),
     ("B", "Elena Vasquez painted The Blue Harbor, finished 1911. The previous answer was yes, and the correction keeps the question, so the answer stays yes.", "Yes.")],
    "I don't know.",
    "correction/entity switch; corrected entity re-evaluated, role/predicate mismatch")

add("C06", "correction",
    [("T1u", "when did Vasquez die"),
     ("T1t", "Elena Vasquez died in 1968."),
     ("T2u", "no, the other Elena.")],
    "no, the other Elena.",
    [("A", "Elena Vasquez died in 1968 and no death is taught for Petrova. The correction keeps the question about an Elena dying, so the answered year 1968 stands.", "1968."),
     ("B", "Elena Vasquez died in 1968 and no death is taught for Petrova. The correction switches to Petrova, so the shaped question asks when she died, which is untaught, so the question is withheld.", "I don't know.")],
    "I don't know.",
    "correction/other-Elena; untaught predicate for corrected entity")

add("C07", "correction",
    [("T1u", "was the Gilded Horse removed"),
     ("T1t", "Yes. The city council voted to remove the Gilded Horse in 1988."),
     ("T2u", "I meant deleted from your memory.")],
    "I meant deleted from your memory.",
    [("A", "The council voted to remove the Gilded Horse in 1988. The correction switches the scope to memory deletion, which the system cannot do, so it refuses.", "I can't forget."),
     ("B", "The council voted to remove the Gilded Horse in 1988. The world event stands, so the answer repeats the taught removal.", "Yes. The council voted to remove the Gilded Horse in 1988.")],
    "I can't forget.",
    "correction/scope change; world event -> memory deletion")

add("C08", "correction",
    [("T1u", "how tall is the Harbor Bridge"),
     ("T1t", "The Harbor Bridge is 134 meters tall."),
     ("T2u", "no, the Bay Crossing."),
     ("T2t", "The Bay Crossing is 7200 meters long."),
     ("T3u", "no wait, I meant tall, the Harbor Bridge.")],
    "no wait, I meant tall, the Harbor Bridge.",
    [("A", "The Harbor Bridge is 134 meters tall and the Bay Crossing is 7200 meters long. The latest topic is the Bay Crossing, so the question asks about it and the taught size is 7200 meters.", "7200 meters."),
     ("B", "The Harbor Bridge is 134 meters tall and the Bay Crossing is 7200 meters long. The second correction returns to the Harbor Bridge and the tall predicate, so the shaped question is answered by the taught 134 meters.", "134 meters.")],
    "134 meters.",
    "correction/chained; second correction reverts topic and predicate")

# ---------------- validation + emit ----------------
def main():
    seen = set()
    for p in problems:
        assert p["id"] not in seen, f"dup id {p['id']}"
        seen.add(p["id"])
        for f in ("query", "expected", "readings", "notes"):
            assert "\t" not in p[f] and "\n" not in p[f], f"bad char in {p['id']}.{f}"
        for tag_txt in p["query"].split(TURN_SEP):
            assert READ_SEP not in tag_txt and ANS_SEP not in tag_txt, f"sep leak in {p['id']}"
        for tag, txt in p["_turns"]:
            assert TURN_SEP not in txt, f"turnsep leak in {p['id']}"
        reads = p["_readings"]
        assert len(reads) >= 2, f"<2 readings in {p['id']}"
        for lab, interp, ans in reads:
            assert READ_SEP not in interp and ANS_SEP not in interp, f"sep leak interp {p['id']}"
            assert READ_SEP not in ans and ANS_SEP not in ans, f"sep leak ans {p['id']}"
            assert "\t" not in ans and "\n" not in ans
        answers = [ans for _, _, ans in reads]
        assert p["expected"] in answers, f"expected not among readings in {p['id']}"
        assert len(set(answers)) == len(answers), f"dup answers in {p['id']}"
    assert len(problems) == 32, f"want 32, have {len(problems)}"
    cats = {}
    for p in problems:
        cats[p["cat"]] = cats.get(p["cat"], 0) + 1
    assert cats == {"entity": 8, "predicate": 8, "scope": 8, "correction": 8}, cats
    with open("problems.tsv", "w") as f:
        f.write("id\tquery\texpected_answer\treadings\tnotes\n")
        for p in problems:
            f.write(f"{p['id']}\t{p['query']}\t{p['expected']}\t{p['readings']}\t{p['notes']}\n")
    with open("problems_redacted.tsv", "w") as f:
        f.write("id\tquery\n")
        for p in problems:
            f.write(f"{p['id']}\t{p['query']}\n")
    with open("answer_key.tsv", "w") as f:
        f.write("id\texpected_answer\tcorrect_reading\n")
        for p in problems:
            for lab, interp, ans in p["_readings"]:
                if ans == p["expected"]:
                    f.write(f"{p['id']}\t{p['expected']}\t{lab}\n")
                    break
    print(f"wrote problems.tsv: {len(problems)} problems, cats={cats}")
    nA = sum(1 for p in problems for lab, i, a in p["_readings"] if a == p["expected"] and lab == "A")
    print(f"correct-reading distribution: A={nA} of {len(problems)}")

main()
