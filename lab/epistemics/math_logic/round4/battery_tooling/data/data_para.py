"""MATH R4 battery data: PARA-INV (hand-authored paraphrases + nonce maps).

12 meaning-preserving paraphrase pairs + 12 nonce-word variants, drawn
from 12 CHAIN_NL problems (3 per domain). The paraphrase keeps the same
statement count and all numeric content; TARGET is byte-identical.
Nonce maps replace content words (domain nouns/verbs/adjectives and
mathematical relation words) with nonce words; logical connectives,
quantifiers, temporal order words, numbers, and copulas are kept.
The substitution map is sealed (sealed/PARA_NONCE_MAP.json); the nonce
problem files carry no map and no verdicts.
"""

PARA = [
{
 "id": "PARA_PAIR_01", "base": "CHAIN_NL_01", "kind": "paraphrase",
 "statements": [
  "Take an integer n, and suppose n is even.",
  "Demonstrate that n to the 4th power is a multiple of 16.",
 ],
 "align": [[1, 1], [2, 2]],
 "nonce_map": {"even": "eeb", "integer": "inba", "divides": "blorp"},
},
{
 "id": "PARA_PAIR_02", "base": "CHAIN_NL_03", "kind": "paraphrase",
 "statements": [
  "10! denotes the product 1 * 2 * 3 * 4 * 5 * 6 * 7 * 8 * 9 * 10.",
  "The only multiples of 3 between 1 and 10 inclusive are 3, 6, and 9.",
  "We have 3 = 3 * 1, 6 = 3 * 2, and 9 = 3 * 3.",
  "The numbers 1 and 2 are not multiples of 3.",
  "Show that 3^4 is the exact power of 3 dividing 10!.",
 ],
 "align": [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]],
 "nonce_map": {"factorial": "zib", "product": "wug", "multiples": "thneed",
               "number": "glim", "numbers": "glimm", "exact": "drok",
               "power": "pof", "dividing": "blorp"},
},
{
 "id": "PARA_PAIR_03", "base": "CHAIN_NL_04", "kind": "paraphrase",
 "statements": [
  "Mira arranges coins into 20 rows, with 1 coin in row 1, 2 coins in row 2, continuing in this way until row 20 with 20 coins.",
  "Group the rows into pairs (1,20), (2,19), (3,18), (4,17), (5,16), (6,15), (7,14), (8,13), (9,12), (10,11), making 10 pairs total.",
  "Compute how many coins there are altogether.",
 ],
 "align": [[1, 1], [2, 2], [3, 3]],
 "nonce_map": {"coins": "zib", "coin": "zibb", "rows": "wug", "row": "wugg",
               "stacks": "thneed", "holds": "drok", "holding": "drokke",
               "Pair": "Glim", "pairs": "glim", "number": "glimx"},
},
{
 "id": "PARA_PAIR_04", "base": "CHAIN_NL_06", "kind": "paraphrase",
 "statements": [
  "A surveyor is measuring a pair of right-triangular plots.",
  "Plot one has legs of 6 and 8 meters, and its hypotenuse is painted red.",
  "Plot two is right-angled; one of its legs is 24 meters and the other matches the red hypotenuse of plot one in length.",
  "Determine the hypotenuse of plot two.",
 ],
 "align": [[1, 1], [2, 2], [3, 3], [4, 4]],
 "nonce_map": {"surveyor": "zib", "plots": "wug", "plot": "wugg",
               "legs": "thneed", "leg": "thne", "hypotenuse": "drok",
               "painted": "glim", "red": "plor", "meters": "blap",
               "right-triangular": "zorp", "right-angled": "zorpx"},
},
{
 "id": "PARA_PAIR_05", "base": "CHAIN_NL_08", "kind": "paraphrase",
 "statements": [
  "Consider triangle ABC, and let D bisect side AB and E bisect side AC.",
  "In triangle ADE, let F bisect side AD and G bisect side AE.",
  "Give the length FG as a function of the length BC, and describe the direction of FG relative to BC.",
 ],
 "align": [[1, 1], [2, 2], [3, 3]],
 "nonce_map": {"triangle": "zib", "midpoint": "wug", "side": "thneed",
               "length": "drok", "directed": "glim", "Express": "Zorp",
               "parallel": "plor"},
},
{
 "id": "PARA_PAIR_06", "base": "CHAIN_NL_10", "kind": "paraphrase",
 "statements": [
  "Triangle ABC is isosceles, with sides AB and AC equal.",
  "Let M be the midpoint of BC; thus M is on the segment BC.",
  "Angles AMB and AMC jointly form a straight angle, 180 degrees.",
  "Any triangle's three interior angles sum to 180 degrees.",
  "The measure of angle ABC is 65 degrees.",
  "Show that AM meets BC at a right angle, and compute angle BAM.",
 ],
 "align": [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]],
 "nonce_map": {"Triangle": "Zib", "isosceles": "zib", "midpoint": "wug",
               "segment": "thneed", "side": "qux", "angles": "drok",
               "angle": "drokke", "Angle": "Drok", "straight": "glim",
               "perpendicular": "plor", "measures": "blap"},
},
{
 "id": "PARA_PAIR_07", "base": "CHAIN_NL_11", "kind": "paraphrase",
 "statements": [
  "Every inhabitant of the island is a knight, who never lies, or a knave, who never tells the truth.",
  "A's statement is that B is a knave.",
  "B's statement is that A and B share a type.",
  "C's statement is that A is a knight.",
  "D's statement is that C is a knave.",
  "Work out the type of each person.",
 ],
 "align": [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]],
 "nonce_map": {"knight": "zib", "knave": "wug", "island": "thneed",
               "person": "drok", "truth": "glim", "lies": "plor",
               "type": "blap"},
},
{
 "id": "PARA_PAIR_08", "base": "CHAIN_NL_13", "kind": "paraphrase",
 "statements": [
  "Look at every representation of the square root of 2 in the form p/q where p and q are integers with q != 0, and select one whose positive denominator q is minimal.",
  "An odd integer squared is odd.",
  "Establish that the square root of 2 is irrational.",
 ],
 "align": [[1, 1], [2, 2], [3, 3]],
 "nonce_map": {"square": "squib", "root": "zib", "fraction": "wug",
               "integers": "thneed", "integer": "thneet",
               "denominator": "drok", "smallest": "glim", "positive": "plor",
               "odd": "obble", "irrational": "qux", "ways": "zorp"},
},
{
 "id": "PARA_PAIR_09", "base": "CHAIN_NL_15", "kind": "paraphrase",
 "statements": [
  "Firing of the vase preceded its glazing.",
  "Its glazing came before its painting.",
  "Its painting preceded its shipping.",
  "Its shipping came before its sale.",
  "Its sale preceded its donation.",
  "Its donation came before its display.",
  "Its display preceded its photographing.",
  "Whenever a first event precedes a second and the second precedes a third, the first precedes the third.",
  "The insurance purchase occurred after the sale and before the donation.",
  "Show that the firing of the vase preceded its photographing, that the insurance was bought after the shipping of the vase, and that the insurance was bought before the display of the vase.",
 ],
 "align": [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10]],
 "nonce_map": {"vase": "zib", "fired": "wug", "glazed": "thneed",
               "painted": "drok", "shipped": "glim", "sold": "plor",
               "donated": "blap", "displayed": "qux",
               "photographed": "zorp", "insurance": "wibble",
               "sale": "sorp", "donation": "dorp"},
},
{
 "id": "PARA_PAIR_10", "base": "CHAIN_NL_16", "kind": "paraphrase",
 "statements": [
  "A row of ten dominoes is set up, numbered 1 through 10.",
  "Whenever a domino falls, it topples the domino with the next number.",
  "The domino numbered 1 is pushed.",
  "Show that the domino numbered 10 falls.",
 ],
 "align": [[1, 1], [2, 2], [3, 3], [4, 4]],
 "nonce_map": {"Domino": "Zib", "dominoes": "zib", "domino": "zibb",
               "row": "wug", "falling": "thneed", "falls": "thnoop",
               "knocks": "drok", "pushed": "glim", "numbered": "plor"},
},
{
 "id": "PARA_PAIR_11", "base": "CHAIN_NL_18", "kind": "paraphrase",
 "statements": [
  "A patient is feverish due to an infection that is getting worse.",
  "Medicine M suppresses the body's fever signal, invariably lowering the fever within two hours.",
  "At 6 o'clock the patient is given a dose of medicine M.",
  "No other medicine is taken by the patient that day.",
  "An infection that is worsening will not resolve by itself within two hours.",
  "By 8 o'clock the fever has left the patient.",
  "Decide if medicine M is what broke the fever.",
 ],
 "align": [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
 "nonce_map": {"patient": "zib", "fever": "wug", "infection": "thneed",
               "worsening": "drok", "Medicine": "Glim", "medicine": "glim",
               "blocks": "plor", "signal": "blap", "dose": "qux",
               "o'clock": "zorp"},
},
{
 "id": "PARA_PAIR_12", "base": "CHAIN_NL_20", "kind": "paraphrase",
 "statements": [
  "Train A departs the depot at 8:00, takes 3 hours to reach Midtown, waits there for 20 minutes, then takes 2 hours to reach Harbor.",
  "Train B departs Midtown at 11:30 and needs 2 hours to get to Harbor.",
  "Demonstrate that train A arrives at Harbor ahead of train B, and determine the time difference.",
 ],
 "align": [[1, 1], [2, 2], [3, 3]],
 "nonce_map": {"Train": "Zib", "train": "zib", "depot": "wug",
               "travels": "thneed", "Midtown": "Glim", "Harbor": "Drok",
               "waits": "plor", "minutes": "blap", "hours": "qux",
               "reaches": "zorp"},
},
]

# Nonce file ids: PARA_NONCE_01..12 correspond 1:1 to PARA_PAIR_01..12 bases.
def nonce_id(pair_id):
    return pair_id.replace("PARA_PAIR_", "PARA_NONCE_")
