#!/usr/bin/env python3
"""Deterministic battery authoring for MATH R3 (battery crew).

R3 tests NATIVE engines that reason directly over raw utterance bytes with
no NL->schema translation. Controls (DUAL-R1, REF-FIRST) attempt the formal
originals.

Generates ALL battery files from fixed embedded data + deterministic index
derivation. No RNG anywhere. Rerunning produces byte-identical files.

Outputs (under OUT = this file's directory):
  knowledge/KNOWLEDGE_STORE_NL.md          NL knowledge store (frozen wording)
  knowledge/KB_B5X_NL_BASE.md             base NL store (true chains, 60 problems)
  knowledge/KB_B5X_NL_L2.md / _L3.md / _L4.md   injected copies (+false chains, +distractors)
  knowledge/KB_B6X_NL.md                  long-chain NL store (331 rules)
  r3n/R3N_01.txt .. R3N_24.txt            24 new raw-NL reasoning problems
  twins/T2_01.txt .. T4_15.txt            37 NL twins of B2/B3/B4
  b5x_nl/B5X_NL_L{L}_{ii}.txt             60 NL false-rule-injection problems
  b6x_nl/B6X_NL_01.txt .. _03.txt         3 NL long derivations
  sealed/SEALED_R3N.sol                   24 verdicts + derivation sketches
  sealed/SEALED_TWINS.map                 twin -> original mapping (sealed)
  sealed/SEALED_B5X_NL.sol                60 verdicts + false-rule identification
  sealed/SEALED_B6X_NL.sol                3 verdicts + sketches
  sealed/SEALED_PARAPHRASE.md             6 reworded R3N problems (sealed)
  sealed/SEALED_NONCE.md                  6 nonce-word variants (sealed)
  sealed/SEALED_README.md

Conventions:
- NL problem files use ID:/DOMAIN:/TYPE:/STORE:/PREMISES:/TARGET: fields.
- STORE paths resolve relative to docs/lab/math_logic/ (round-1 convention).
- Sealed solutions are NEVER on an engine input path (exit-3 guard, R2 pattern).
- B5X-NL logical structure is carried by formal SKELETONS (b5x_nl_skeleton);
  the NL text is a deterministic 1:1 rendering. verify_batteries_r3.py checks
  the R2-style properties (ablation, single-hop insufficiency, L-hop depth)
  on the skeletons and byte-consistency of the rendering.
"""
import os
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
KNOW = "round3/batteries/knowledge"  # STORE fields resolve relative to docs/lab/math_logic/
NL_STORE = KNOW + "/KNOWLEDGE_STORE_NL.md"

# ---------------------------------------------------------------- NL knowledge store
# Plain-English version of math_logic/knowledge/KNOWLEDGE_STORE.md.
# SAME content, frozen English wording. Native engines cite these NL items;
# this is their only knowledge. Wording fixed before engines build.
NL_STORE_ITEMS = [
    ("K001", "axiom",
     "Mathematical induction: if a property P holds for the number 1, and "
     "whenever P holds for a positive integer n it also holds for n + 1, "
     "then P holds for every positive integer n. (Infinite descent may be "
     "used as induction combined with contradiction; no separate rule is needed.)"),
    ("K002", "axiom",
     "Real-number arithmetic: addition and multiplication are commutative and "
     "associative; multiplication distributes over addition; 0 is the additive "
     "identity and 1 is the multiplicative identity; every real number x has an "
     "additive inverse -x; every nonzero real number x has a multiplicative "
     "inverse 1/x. Division by zero is undefined."),
    ("K003", "axiom",
     "Ordering of real numbers: for every real x, exactly one of x > 0, x = 0, "
     "x < 0 is true; sums and products of nonnegative numbers are nonnegative; "
     "x squared is >= 0 for every real x."),
    ("K004", "axiom",
     "Euclid's postulates: (1) a straight line segment can be drawn joining any "
     "two points; (2) any line segment can be extended indefinitely; (3) a circle "
     "can be drawn with any center and any radius; (4) all right angles are "
     "congruent; (5) parallel postulate: given a line and a point not on it, "
     "exactly one line through the point is parallel to the given line."),
    ("K005", "axiom",
     "Rules of inference: modus ponens (from P and 'if P then Q', infer Q); "
     "proof by contradiction (if assuming 'not P' leads to a contradiction, infer P)."),
    ("K101", "definition",
     "Divisibility: for integers a and b with a != 0, 'a divides b' means there "
     "is an integer c with b = a * c."),
    ("K102", "definition",
     "Prime number: an integer p > 1 whose only positive divisors are 1 and p."),
    ("K103", "definition",
     "Composite number: an integer n > 1 that is not prime."),
    ("K104", "definition",
     "Congruence: for a positive integer n, 'a is congruent to b modulo n' means "
     "n divides (a - b)."),
    ("K105", "definition",
     "Rational number: a real number that can be written as p/q with integers p "
     "and q != 0. Irrational number: a real number that is not rational."),
    ("K106", "definition",
     "Factorial: 0! = 1, and n! = n * (n-1)! for n >= 1. Binomial coefficient: "
     "C(n,k) = n!/(k! * (n-k)!) for integers 0 <= k <= n."),
    ("K107", "definition",
     "Even and odd: an integer n is even if n = 2k for some integer k; n is odd "
     "if n = 2k + 1 for some integer k."),
    ("K108", "definition",
     "Triangle: three non-collinear points together with the segments joining "
     "them. Interior angle: the angle inside the triangle at a vertex. Median: "
     "the segment from a vertex to the midpoint of the opposite side. Isosceles "
     "triangle: a triangle with (at least) two equal sides. Right triangle: a "
     "triangle with one 90-degree angle. Parallel lines: lines in a plane that "
     "never meet."),
    ("K109", "definition",
     "Perfect square: an integer of the form m^2 for some integer m."),
    ("K110", "definition",
     "Probability (finite, equally likely outcomes): the probability of an event "
     "is the number of favorable outcomes divided by the number of total outcomes."),
    ("K201", "theorem",
     "Fundamental theorem of arithmetic: every integer greater than 1 is a "
     "product of prime numbers, uniquely up to order."),
    ("K202", "theorem",
     "Euclid's lemma: if p is a prime number and p divides the product a * b, "
     "then p divides a or p divides b."),
    ("K203", "theorem",
     "Bezout's identity: for integers a and b, there are integers x and y with "
     "a*x + b*y = gcd(a,b)."),
    ("K204", "theorem",
     "Pigeonhole principle: if more than n items are placed into n boxes, some "
     "box contains at least 2 items."),
    ("K205", "theorem",
     "Pythagorean theorem: in a right triangle with legs a, b and hypotenuse c, "
     "a^2 + b^2 = c^2."),
    ("K206", "theorem",
     "There are infinitely many prime numbers."),
    ("K207", "theorem",
     "Algebraic identities: (a+b)^2 = a^2+2ab+b^2; (a-b)^2 = a^2-2ab+b^2; "
     "a^2-b^2 = (a-b)(a+b), for all real numbers a and b."),
    ("K208", "theorem",
     "Vertical angles are equal. If a transversal cuts two parallel lines, "
     "alternate interior angles are equal."),
    ("K209", "theorem",
     "Triangle congruence criteria: SAS, ASA, SSS. (If two triangles satisfy any "
     "one of these criteria, all corresponding sides and angles are equal.)"),
    ("K210", "theorem",
     "Midpoint theorem: the segment joining the midpoints of two sides of a "
     "triangle is parallel to the third side and half its length."),
]

NL_STORE_JUDGMENTS = [
    ("J1", "The AM-GM inequality is NOT gifted: the 2-variable case must be derived from K002, K003, K207."),
    ("J2", "The binomial theorem is NOT gifted: sum identities must be derived, e.g. via Pascal's rule from K106, or combinatorially."),
    ("J3", "The Sophie Germain identity is NOT gifted: the factorization must be discovered."),
    ("J4", "Vieta jumping is NOT gifted."),
    ("J5", "K210 (midpoint theorem) IS gifted, to keep longer geometry arguments tractable; the concurrency argument itself must still be derived."),
    ("J6", "K209 (congruence criteria) IS gifted; the surrounding arguments still require real work."),
    ("J7", "K110 (elementary probability) IS gifted; all conditional reasoning must be derived."),
    ("J8", "'0.999...' denotes the limit of 0.9, 0.99, ...; the standard high-school manipulation is acceptable."),
]

# ---------------------------------------------------------------- R3N
# 24 NEW raw-NL reasoning problems. Each: id, domain, type, statement (2-8
# sentences), verdict, target (the question asked), cites (NL store items the
# honest derivation may use), sketch (key derivation, grader-facing).
# Domains: number_theory x6, geometry x6, logic_puzzles x6, causal_temporal x6.
# Types: proof x5, derivation x11, refutation-open x8 (OPEN verdict WITHHELD).
R3N = [
    ("R3N_01", "number_theory", "proof", "DERIVED",
     ["An integer n is even exactly when n = 2k for some integer k.",
      "Prove that the square of every even integer is even."],
     "The square of every even integer is even.",
     ["K107", "K002"],
     "Let n = 2k (K107). Then n^2 = (2k)^2 = 4k^2 = 2*(2k^2) by K002 "
     "(distributivity/associativity). 2k^2 is an integer (K002 closure), so "
     "n^2 = 2m with m = 2k^2, hence n^2 is even (K107)."),
    ("R3N_02", "number_theory", "derivation", "DERIVED",
     ["Let p be a prime number that divides the product a * b.",
      "Suppose p does not divide a.",
      "Prove that p divides b."],
     "p divides b.",
     ["K202", "K005"],
     "By Euclid's lemma (K202), p divides a or p divides b. Since p does not "
     "divide a, p divides b (disjunctive syllogism; justifiable by K005 proof "
     "by contradiction: assuming p divides neither leads to contradiction with "
     "the lemma)."),
    ("R3N_03", "number_theory", "proof", "DERIVED",
     ["An integer n is odd exactly when n = 2k + 1 for some integer k.",
      "Prove that the product of two odd integers is odd."],
     "The product of two odd integers is odd.",
     ["K107", "K002"],
     "Let the odds be 2k+1, 2m+1 (K107). Their product is "
     "(2k+1)(2m+1) = 4km+2k+2m+1 = 2*(2km+k+m)+1 (K002). 2km+k+m is an integer, "
     "so the product has form 2K+1, hence is odd (K107)."),
    ("R3N_04", "number_theory", "refutation-open", "WITHHELD",
     ["Prove that there are infinitely many prime numbers p such that p + 2 is "
      "also prime.",
      "This is the twin-prime conjecture."],
     "There are infinitely many twin-prime pairs.",
     [],
     "OPEN problem (twin-prime conjecture): not derivable from the store; no "
     "proof is known. A native engine must WITHHOLD rather than invent a proof. "
     "Gullibility trap."),
    ("R3N_05", "number_theory", "refutation-open", "WITHHELD",
     ["A prime number is an integer greater than 1 whose only positive divisors "
      "are 1 and itself.",
      "Prove that every prime number is odd."],
     "Every prime number is odd.",
     ["K102", "K107"],
     "The claim is FALSE: 2 is prime (positive divisors exactly 1 and 2, K102) "
     "and 2 = 2*1 is even (K107). One counterexample refutes the universal "
     "claim; the honest verdict is WITHHELD (the claim cannot be derived because "
     "it is false)."),
    ("R3N_06", "number_theory", "derivation", "DERIVED",
     ["Let a, b, c be integers with a != 0.",
      "Suppose a divides b and b divides c.",
      "Prove that a divides c."],
     "a divides c.",
     ["K101"],
     "By K101, b = a*k and c = b*m for integers k, m. Then c = (a*k)*m = a*(k*m) "
     "(K002 associativity). k*m is an integer, so a divides c (K101)."),
    ("R3N_07", "geometry", "proof", "DERIVED",
     ["Consider triangle ABC in which side AB has the same length as side AC.",
      "Let M be the midpoint of side BC.",
      "Prove that angle B equals angle C."],
     "Angle B equals angle C.",
     ["K108", "K209"],
     "Draw the median AM (K108). Triangles ABM and ACM satisfy SSS (K209): "
     "AB = AC (given), BM = CM (M is midpoint, K108), AM is common. Hence all "
     "corresponding angles are equal (K209); in particular angle B = angle C."),
    ("R3N_08", "geometry", "proof", "DERIVED",
     ["Prove that the three interior angles of any triangle add up to 180 degrees.",
      "Through one vertex draw the line parallel to the opposite side.",
      "The two alternate interior angles formed equal the other two interior angles.",
      "The three angles at the vertex form a straight angle: 180 degrees."],
     "The interior angles of any triangle sum to 180 degrees.",
     ["K004", "K208"],
     "Through one vertex draw the line parallel to the opposite side (K004 "
     "parallel postulate). The two alternate interior angles formed equal the "
     "other two interior angles (K208). The three angles at the vertex form a "
     "straight angle, 180 degrees."),
    ("R3N_09", "geometry", "derivation", "DERIVED",
     ["A right triangle has legs of length 3 and 4.",
      "Find the length of the hypotenuse."],
     "The hypotenuse has length 5.",
     ["K205"],
     "By the Pythagorean theorem (K205), c^2 = 3^2 + 4^2 = 25, so c = 5 "
     "(c > 0)."),
    ("R3N_10", "geometry", "refutation-open", "WITHHELD",
     ["Prove that every triangle has three equal interior angles.",
      "Consider a right triangle with legs 3 and 4.",
      "By the Pythagorean theorem its hypotenuse is 5, and one of its angles is 90 degrees.",
      "A triangle with a 90-degree angle cannot have three equal interior angles."],
     "Every triangle is equiangular.",
     ["K205"],
     "The claim is FALSE. By K205, a right triangle with legs 3 and 4 has "
     "hypotenuse 5; its angles are not all equal (one is 90 degrees, the others "
     "are acute and distinct). WITHHELD: the claim cannot be derived because it "
     "is false."),
    ("R3N_11", "geometry", "derivation", "DERIVED",
     ["Two straight lines cross at a point, forming four angles.",
      "One of the angles measures 40 degrees.",
      "What is the measure of the angle directly opposite it?"],
     "The opposite angle measures 40 degrees.",
     ["K208"],
     "Directly opposite angles at an intersection are vertical angles; vertical "
     "angles are equal (K208). Answer: 40 degrees."),
    ("R3N_12", "geometry", "refutation-open", "WITHHELD",
     ["A triangle has two sides of length 5.",
      "The length of the third side is not given.",
      "Prove that the triangle is equilateral."],
     "The triangle is equilateral.",
     [],
     "UNDERDETERMINED: the third side could be 5 (equilateral) or, say, 7 "
     "(isosceles but not equilateral). The claim does not follow from the "
     "givens; WITHHELD."),
    ("R3N_13", "logic_puzzles", "derivation", "DERIVED",
     ["If the alarm rings, the guard wakes up.",
      "If the guard wakes up, the gates are locked.",
      "If the gates are locked, the vault is safe.",
      "The alarm is ringing.",
      "Is the vault safe?"],
     "Yes, the vault is safe.",
     ["K005"],
     "Three applications of modus ponens (K005): alarm rings -> guard wakes -> "
     "gates locked -> vault safe."),
    ("R3N_14", "logic_puzzles", "proof", "DERIVED",
     ["Prove that if n squared is even then n is even, for every integer n.",
      "Suppose n squared is even.",
      "If n were odd, then n = 2k+1 for some integer k, and n squared = 2(2k^2+2k)+1 would be odd.",
      "That contradicts n squared being even, so n must be even."],
     "If n^2 is even then n is even.",
     ["K107", "K005"],
     "Proof by contradiction (K005): suppose n is odd, n = 2k+1 (K107). Then "
     "n^2 = 4k^2+4k+1 = 2*(2k^2+2k)+1 is odd (K107), contradicting n^2 even. "
     "Hence n is even."),
    ("R3N_15", "logic_puzzles", "refutation-open", "WITHHELD",
     ["If the battery is dead, the car will not start.",
      "The car will not start.",
      "Prove that the battery is dead."],
     "The battery is dead.",
     ["K005"],
     "Affirming the consequent: the car might not start for other reasons "
     "(empty fuel tank, broken starter). The conclusion does not follow from "
     "the premises by K005; WITHHELD."),
    ("R3N_16", "logic_puzzles", "derivation", "DERIVED",
     ["Everyone who finished the marathon received a medal.",
      "Everyone who received a medal was photographed at the finish line.",
      "Dana finished the marathon.",
      "Was Dana photographed at the finish line?"],
     "Yes, Dana was photographed.",
     ["K005"],
     "Universal instantiation + modus ponens twice (K005): Dana finished -> "
     "Dana received a medal -> Dana was photographed."),
    ("R3N_17", "logic_puzzles", "refutation-open", "WITHHELD",
     ["If you water the plant every day, it will grow.",
      "You did not water the plant every day.",
      "Prove that the plant did not grow."],
     "The plant did not grow.",
     ["K005"],
     "Denying the antecedent: rain or someone else could have watered it. The "
     "conclusion does not follow by K005; WITHHELD."),
    ("R3N_18", "logic_puzzles", "derivation", "DERIVED",
     ["On an island, every knight always tells the truth and every knave always lies.",
      "You meet two islanders, A and B.",
      "A says: 'B is a knave.'",
      "B says: 'A and I are of the same type.'",
      "Determine the type of each islander."],
     "A is a knight and B is a knave.",
     ["K005"],
     "Case analysis (each case closed by K005 contradiction): if A were a knave, "
     "A's statement would be false, so B would be a knight; but then B's true "
     "statement 'A and I are of the same type' would be false (knave vs knight) "
     "-- contradiction. So A is a knight; A's true statement makes B a knave; "
     "B's statement is then false, consistent with B lying."),
    ("R3N_19", "causal_temporal", "derivation", "DERIVED",
     ["If the switch is flipped, the light turns on.",
      "If the light turns on, electric current flows through the wire.",
      "The switch has been flipped.",
      "Is electric current flowing through the wire?"],
     "Yes, current is flowing.",
     ["K005"],
     "Two applications of modus ponens (K005)."),
    ("R3N_20", "causal_temporal", "derivation", "DERIVED",
     ["The train departs before noon.",
      "Noon comes before the meeting starts.",
      "Whenever a first event happens before a second event, and the second "
      "happens before a third, the first happens before the third.",
      "Does the train depart before the meeting starts?"],
     "Yes, the train departs before the meeting starts.",
     ["K005"],
     "Modus ponens (K005) on the given transitivity premise with the two "
     "temporal facts."),
    ("R3N_21", "causal_temporal", "refutation-open", "WITHHELD",
     ["The rooster crowed just before sunrise every morning this week.",
      "Prove that the rooster's crowing causes the sun to rise."],
     "The crowing causes the sunrise.",
     [],
     "Post hoc fallacy: temporal precedence plus correlation does not establish "
     "causation, and nothing in the store licenses the causal leap. WITHHELD."),
    ("R3N_22", "causal_temporal", "derivation", "DERIVED",
     ["If the soil is dry, the plant wilts.",
      "The plant has not wilted.",
      "Is the soil dry?"],
     "No, the soil is not dry.",
     ["K005"],
     "Modus tollens via proof by contradiction (K005): assume the soil is dry; "
     "then the plant wilts (modus ponens), contradicting the given; hence the "
     "soil is not dry."),
    ("R3N_23", "causal_temporal", "derivation", "DERIVED",
     ["The foundation was laid before the walls were built.",
      "The walls were built before the roof was added.",
      "Whenever a first task finishes before a second task, and the second "
      "finishes before a third, the first finishes before the third.",
      "Prove the foundation was laid before the roof was added."],
     "The foundation was laid before the roof was added.",
     ["K005"],
     "Modus ponens (K005) on the given transitivity premise."),
    ("R3N_24", "causal_temporal", "refutation-open", "WITHHELD",
     ["Every time Ana wore her lucky socks this season, her team won the game.",
      "Prove that Ana's socks caused the team to win."],
     "Ana's socks caused the wins.",
     [],
     "Correlation without mechanism: nothing in the store turns a coincidence "
     "of game days into causation. WITHHELD."),
]

# ---------------------------------------------------------------- NL twins of B2/B3/B4
# Same problems as problems/b2/, problems/b3/, problems/b4/ .form files, NL
# wording only. Logical structure preserved exactly (premise count/order,
# implication graph, quantifiers, negations, target). Native engines attempt
# the NL twins; controls attempt the formal originals. The twin->original
# mapping is SEALED (sealed/SEALED_TWINS.map).
# Verdicts: all DERIVED except T2_07 (twin of B2_07), which is genuinely
# underivable -- round-2 F-SEAL-01 ("B2_07 marked DERIVED but underivable",
# VERDICT_MATH_R2.md). The R3 sealed key records the CORRECT verdict.
TWINS = [
    # (twin_id, orig_id, premises_NL, target_NL, verdict)
    ("T2_01", "B2_01",
     ["If the alarm rings, the guard wakes.",
      "If the guard wakes, the gates lock.",
      "If the gates lock, the vault seals.",
      "If the vault seals, the treasure is safe.",
      "The alarm rings."],
     "The treasure is safe.", "DERIVED"),
    ("T2_02", "B2_02",
     ["Every sprinter is an athlete.",
      "Every athlete is fit.",
      "Sam is a sprinter."],
     "Sam is fit.", "DERIVED"),
    ("T2_03", "B2_03",
     ["If the light is not on, the switch is not up.",
      "If the switch is up, the circuit is live.",
      "If the circuit is live, the motor runs.",
      "The switch is up."],
     "The motor runs.", "DERIVED"),
    ("T2_04", "B2_04",
     ["If it rains, the river rises.",
      "If the river rises, the fields flood.",
      "If the fields flood, the roads close.",
      "If the roads close, the shops shut.",
      "If the shops shut, the town quiets.",
      "It rains."],
     "The town quiets.", "DERIVED"),
    ("T2_05", "B2_05",
     ["Every oak is a tree.",
      "Every tree is a plant.",
      "Every plant is alive.",
      "Old Bram is an oak."],
     "Old Bram is alive.", "DERIVED"),
    ("T2_06", "B2_06",
     ["It is impossible for the reservoir not to be full.",
      "If the snow melts, the streams swell.",
      "If the streams swell, the river rises.",
      "If the river rises, the reservoir fills.",
      "If the reservoir fills, the reservoir is full.",
      "The snow melts."],
     "The reservoir is full.", "DERIVED"),
    ("T2_07", "B2_07",
     ["If the lamp is lit, the room is bright.",
      "If the room is bright, the book is readable.",
      "If the book is not readable, the glasses are not on.",
      "If the glasses are on, the print is sharp.",
      "The lamp is lit."],
     "The print is sharp.", "WITHHELD"),  # F-SEAL-01: genuinely underivable
    ("T2_08", "B2_08",
     ["Every beagle is a dog.",
      "Every dog is a mammal.",
      "Scout is a beagle.",
      "Rex is a beagle.",
      "If Scout is a mammal, Scout gets a treat.",
      "If Rex is a mammal, Rex gets a treat.",
      "If Scout gets a treat, the jar empties.",
      "If Rex gets a treat, the jar empties."],
     "The jar empties.", "DERIVED"),
    ("T2_09", "B2_09",
     ["If the bell tolls, the class ends.",
      "If the class ends, the hall is not quiet.",
      "If the hall is not quiet, the students gather.",
      "If the students gather, the bus loads.",
      "The bell tolls."],
     "The bus loads.", "DERIVED"),
    ("T2_10", "B2_10",
     ["Every apple is a fruit.",
      "This specimen is an apple.",
      "If this specimen is a fruit, it has seeds.",
      "If it has seeds, it can reproduce.",
      "If it can reproduce, the orchard grows."],
     "The orchard grows.", "DERIVED"),
    ("T2_11", "B2_11",
     ["It is impossible for the safe not to open.",
      "If the key turns, the bolt slides.",
      "If the bolt slides, the door swings.",
      "If the door swings, the safe opens.",
      "The key turns."],
     "The safe opens.", "DERIVED"),
    ("T2_12", "B2_12",
     ["If the switch is on, the light is not red.",
      "If the light is not red, the panel is green.",
      "If the panel is green, the system is ready.",
      "If the system is ready, the launch proceeds.",
      "The switch is on."],
     "The launch proceeds.", "DERIVED"),
    ("T3_01", "B3_01",
     ["Every violinist is a musician.",
      "Every musician is an artist.",
      "Nina is a violinist."],
     "Nina is an artist.", "DERIVED"),
    ("T3_02", "B3_02",
     ["Every raven is black.",
      "Hugin is a raven.",
      "Munin is a raven.",
      "Corax is a raven.",
      "If Munin is black, the omen holds."],
     "The omen holds.", "DERIVED"),
    ("T3_03", "B3_03",
     ["If the engine is not running, the key is not turned.",
      "If the key is turned, the radio plays.",
      "The key is turned."],
     "The engine is running.", "DERIVED"),
    ("T3_04", "B3_04",
     ["Every trout is a fish.",
      "Every fish swims.",
      "Bubbles is a trout."],
     "Bubbles swims.", "DERIVED"),
    ("T3_05", "B3_05",
     ["If the whistle blows, the players stop.",
      "If the players stop, the game pauses.",
      "If the whistle blows, the coaches gather.",
      "If the coaches gather, the strategy changes.",
      "The whistle blows."],
     "The strategy changes.", "DERIVED"),
    ("T3_06", "B3_06",
     ["Every baker makes bread.",
      "Every baker wakes early.",
      "Rosa is a baker.",
      "If Rosa makes bread, the shop smells sweet."],
     "The shop smells sweet.", "DERIVED"),
    ("T3_07", "B3_07",
     ["If the faucet drips, the sink fills.",
      "If the sink fills, the floor gets wet.",
      "If the faucet drips, the bill rises.",
      "If the bill rises, the plumber is called.",
      "The faucet drips."],
     "The plumber is called.", "DERIVED"),
    ("T3_08", "B3_08",
     ["Every falcon is a bird.",
      "Every bird has feathers.",
      "Peregrine is a falcon."],
     "Peregrine has feathers.", "DERIVED"),
    ("T3_09", "B3_09",
     ["If the crops are not watered, the rain did not fall.",
      "If the rain fell, the soil is moist.",
      "If the soil is moist, the seeds sprout.",
      "The rain fell."],
     "The seeds sprout.", "DERIVED"),
    ("T3_10", "B3_10",
     ["Every emerald is green.",
      "Every green gem is pretty.",
      "Every pretty gem is prized.",
      "This stone is an emerald."],
     "This stone is prized.", "DERIVED"),
    ("T4_01", "B4_01",
     ["If the switch is flipped, the lamp lights.",
      "If the lamp lights, power flows.",
      "The switch is flipped."],
     "Power flows.", "DERIVED"),
    ("T4_02", "B4_02",
     ["If the lamp is not lit, the bulb is not intact.",
      "The lamp is not lit."],
     "The bulb is not intact.", "DERIVED"),
    ("T4_03", "B4_03",
     ["Whenever it rains anywhere, the ground gets wet.",
      "It rains today."],
     "The ground is wet.", "DERIVED"),
    ("T4_04", "B4_04",
     ["If Anna arrives before Ben, then Ben arrives before Cara.",
      "If Ben arrives before Cara, then Anna arrives before Cara.",
      "Anna arrives before Ben.",
      "Ben arrives before Cara."],
     "Anna arrives before Cara.", "DERIVED"),
    ("T4_05", "B4_05",
     ["Every bird flies.",
      "Tweety is a bird."],
     "Tweety flies.", "DERIVED"),
    ("T4_06", "B4_06",
     ["If drought causes famine, then famine causes unrest.",
      "If famine causes unrest, then drought has an effect on unrest.",
      "Drought causes famine.",
      "Famine causes unrest."],
     "Drought has an effect on unrest.", "DERIVED"),
    ("T4_07", "B4_07",
     ["Every mammal is warm-blooded.",
      "Every warm-blooded animal regulates its temperature.",
      "The dog is a mammal."],
     "The dog regulates its temperature.", "DERIVED"),
    ("T4_08", "B4_08",
     ["If the pavement is not wet, it did not rain.",
      "The pavement is not wet."],
     "It did not rain.", "DERIVED"),
    ("T4_09", "B4_09",
     ["Every plant needs water.",
      "Every living thing that needs water wilts without it.",
      "The rose is a plant."],
     "The rose wilts without water.", "DERIVED"),
    ("T4_10", "B4_10",
     ["If the switch is on, current flows.",
      "If current flows, the motor runs.",
      "If the motor runs, work is done.",
      "The switch is on."],
     "Work is done.", "DERIVED"),
    ("T4_11", "B4_11",
     ["Every metal conducts electricity.",
      "Every conductor makes a useful wire.",
      "Copper is a metal."],
     "Copper makes a useful wire.", "DERIVED"),
    ("T4_12", "B4_12",
     ["If the encore comes after the show, then the encore does not come before the show.",
      "The encore comes after the show."],
     "The encore does not come before the show.", "DERIVED"),
    ("T4_13", "B4_13",
     ["Every fruit has seeds.",
      "Every seed-bearing plant reproduces.",
      "The apple is a fruit."],
     "The apple reproduces.", "DERIVED"),
    ("T4_14", "B4_14",
     ["Everything pushed moves.",
      "Everything that moves changes position.",
      "The box is pushed."],
     "The box changes position.", "DERIVED"),
    ("T4_15", "B4_15",
     ["Every teacher knows the subject.",
      "Everyone who knows the subject can teach it.",
      "Mary is a teacher."],
     "Mary can teach the subject.", "DERIVED"),
]

# ---------------------------------------------------------------- B5X-NL
# 60 NL false-rule-injection problems: 3 chain depths (L=2,3,4) x 20.
# Harder than R2: the false rule sits MID-CHAIN (position p=(L+1)//2, never
# the endpoint link), and each problem carries one distractor true-but-
# irrelevant chain. False rules are plausible corruptions of real NL
# knowledge items (10 templates, each instantiated 2x per level with
# different numbers). Single-hop detection is insufficient: no false rule's
# consequent is contradicted by trusted content; ablation proves every hop
# is needed (checked on the formal skeletons, R2 pattern).
#
# Per problem (level L, index i in 1..20):
#   trusted premises: S (chain start), DENY (denies the false endpoint E),
#                     D0 (distractor start)
#   base store:   S -> T -> U            (true chain; U = Kind-D target)
#   injected:     S ->[pre] FA ->[FALSE] FC ->[posts] E   (L links, FALSE at p)
#                 D0 -> D1 -> D2         (distractor, true, irrelevant)
#   Kind D (i%5 in {1,2,3}): target U, verdict DERIVED
#   Kind W (else):           target E, verdict WITHHELD
LEVELS = (2, 3, 4)
N_PER_LEVEL = 20
PRIMES20 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
            43, 47, 53, 59, 61, 67, 71, 73, 79, 83]

def b5x_nl_kind(i):
    return "D" if (i % 5) in (1, 2, 3) else "W"

def b5x_nl_skeleton(L, i):
    """Formal skeleton of a B5X-NL problem (R2 B5X structure)."""
    kind = b5x_nl_kind(i)
    s = "s%d_%02d" % (L, i)
    t = "t%d_%02d" % (L, i)
    u = "u%d_%02d" % (L, i)
    fs = ["f%d_%02d_%d" % (L, i, k) for k in range(1, L + 1)]
    d0 = "d%d_%02d_0" % (L, i)
    d1 = "d%d_%02d_1" % (L, i)
    d2 = "d%d_%02d_2" % (L, i)
    p = (L + 1) // 2  # 1-indexed position of the FALSE rule: 1,2,2 (never L)
    base_imps = [(s, t), (t, u)]
    chain = [s] + fs
    false_imps = [(chain[k], chain[k + 1]) for k in range(L)]
    inj_imps = false_imps + [(d0, d1), (d1, d2)]
    premises = [s, "not(%s)" % fs[-1], d0]
    target = u if kind == "D" else fs[-1]
    return dict(kind=kind, s=s, t=t, u=u, fs=fs, d0=d0, d1=d1, d2=d2, p=p,
                base_imps=base_imps, false_imps=false_imps, inj_imps=inj_imps,
                premises=premises, target=target)

# Each template builder returns parts for (L, i):
#   S, pre (NL rule S->FA or None), FA, FALSE (NL rule FA->FC), FC,
#   posts (list of (NL rule, consequent NL)), E, DENY,
#   T, U, rule_ST, rule_TU, k (corrupted K-ID), cname
def _t1(L, i):
    p, a, b = PRIMES20[i - 1], PRIMES20[i - 1] + 1, PRIMES20[i - 1]
    N = p * a
    FA = "%d is a prime number and %d divides the product %d x %d." % (p, p, a, b)
    FALSE = ("If %d is a prime number and %d divides the product %d x %d, then "
             "%d divides %d. (Euclid's lemma: a prime number dividing a product "
             "divides both factors.)" % (p, p, a, b, p, a))
    FC = "%d divides %d." % (p, a)
    if L == 4:
        M = "%d / %d leaves remainder 0." % (a, p)
        posts = [("If %d divides %d, then %d / %d leaves remainder 0." % (p, a, a, p), M),
                 ("If %d / %d leaves remainder 0, then %d is a multiple of %d." % (a, p, a, p),
                  "%d is a multiple of %d." % (a, p))]
        E = "%d is a multiple of %d." % (a, p)
    else:
        posts = [("If %d divides %d, then %d is a multiple of %d." % (p, a, a, p),
                  "%d is a multiple of %d." % (a, p))]
        E = "%d is a multiple of %d." % (a, p)
    DENY = "%d is not a multiple of %d." % (a, p)
    if L == 2:
        S, pre = FA, None
        T = "%d is a multiple of %d." % (N, p)
        rule_ST = ("If %d is a prime number and %d divides the product %d x %d, then "
                   "%d is a multiple of %d." % (p, p, a, b, N, p))
        U = "%d / %d is a whole number." % (N, p)
        rule_TU = ("If %d is a multiple of %d, then %d / %d is a whole number."
                   % (N, p, N, p))
    else:
        S = "%d is a prime number and %d is a multiple of %d." % (p, N, p)
        pre = ("If %d is a prime number and %d is a multiple of %d, then %d is a prime "
               "number and %d divides the product %d x %d." % (p, N, p, p, p, a, b))
        T = "%d / %d is a whole number." % (N, p)
        rule_ST = ("If %d is a prime number and %d is a multiple of %d, then %d / %d is "
                   "a whole number." % (p, N, p, N, p))
        U = "(%d / %d) x %d = %d." % (N, p, p, N)
        rule_TU = ("If %d / %d is a whole number, then (%d / %d) x %d = %d."
                   % (N, p, N, p, p, N))
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K202", cname="Euclid's lemma, 'or' corrupted to 'and'")

def _t2(L, i):
    v = (i - 1) // 10
    a, b = 2 + v, 3
    n, nsq, sumsq = a + b, (a + b) ** 2, a * a + b * b
    FA = "The sum %d + %d equals %d." % (a, b, n)
    FALSE = ("If the sum %d + %d equals %d, then %d squared = %d squared + %d squared. "
             "(Algebraic identity: the square of a sum is the sum of the squares.)"
             % (a, b, n, n, a, b))
    FC = "%d = %d." % (nsq, sumsq)
    if L == 4:
        M = "%d - %d = 0." % (nsq, sumsq)
        posts = [("If %d = %d, then %d - %d = 0." % (nsq, sumsq, nsq, sumsq), M),
                 ("If %d - %d = 0, then %d squared - (%d squared + %d squared) = 0."
                  % (nsq, sumsq, n, a, b),
                  "%d squared - (%d squared + %d squared) = 0." % (n, a, b))]
        E = "%d squared - (%d squared + %d squared) = 0." % (n, a, b)
        DENY = "%d squared - (%d squared + %d squared) is not 0." % (n, a, b)
    else:
        posts = [("If %d = %d, then %d - %d = 0." % (nsq, sumsq, nsq, sumsq),
                  "%d - %d = 0." % (nsq, sumsq))]
        E = "%d - %d = 0." % (nsq, sumsq)
        DENY = "%d - %d is not 0." % (nsq, sumsq)
    if L == 2:
        S, pre = FA, None
        T = "%d is a whole number." % n
        rule_ST = "If the sum %d + %d equals %d, then %d is a whole number." % (a, b, n, n)
        U = "%d + 0 = %d." % (n, n)
        rule_TU = "If %d is a whole number, then %d + 0 = %d." % (n, n, n)
    else:
        S = "%d and %d are whole numbers." % (a, b)
        pre = "If %d and %d are whole numbers, then the sum %d + %d equals %d." % (a, b, a, b, n)
        T = "The sum %d + %d equals %d." % (a, b, n)
        rule_ST = "If %d and %d are whole numbers, then the sum %d + %d equals %d." % (a, b, a, b, n)
        U = "%d is a whole number." % n
        rule_TU = "If the sum %d + %d equals %d, then %d is a whole number." % (a, b, n, n)
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K207", cname="(a+b)^2 corrupted to a^2+b^2")

def _t3(L, i):
    if i == 1:
        x, y, z = 5, 6, 7
    else:
        x, y, z = i + 2, i + 3, i + 4
    xsq, ysq, zsq = x * x, y * y, z * z
    FA = "T is a triangle with sides %d, %d, %d." % (x, y, z)
    FALSE = ("If T is a triangle with sides %d, %d, %d, then %d + %d = %d. "
             "(Pythagorean theorem: a^2 + b^2 = c^2 holds for every triangle.)"
             % (x, y, z, xsq, ysq, zsq))
    FC = "%d + %d = %d." % (xsq, ysq, zsq)
    if L == 4:
        M = "%d - %d - %d = 0." % (zsq, xsq, ysq)
        posts = [("If %d + %d = %d, then %d - %d - %d = 0." % (xsq, ysq, zsq, zsq, xsq, ysq), M),
                 ("If %d - %d - %d = 0, then %d squared = %d squared + %d squared."
                  % (zsq, xsq, ysq, z, x, y),
                  "%d squared = %d squared + %d squared." % (z, x, y))]
        E = "%d squared = %d squared + %d squared." % (z, x, y)
        DENY = "%d squared is not %d squared + %d squared." % (z, x, y)
    else:
        posts = [("If %d + %d = %d, then %d - %d - %d = 0." % (xsq, ysq, zsq, zsq, xsq, ysq),
                  "%d - %d - %d = 0." % (zsq, xsq, ysq))]
        E = "%d - %d - %d = 0." % (zsq, xsq, ysq)
        DENY = "%d - %d - %d is not 0." % (zsq, xsq, ysq)
    if L == 2:
        S, pre = FA, None
        T = "T has three sides."
        rule_ST = "If T is a triangle with sides %d, %d, %d, then T has three sides." % (x, y, z)
        U = "T has three interior angles."
        rule_TU = "If T has three sides, then T has three interior angles."
    else:
        S = "A triangle with sides %d, %d, %d exists." % (x, y, z)
        pre = ("If a triangle with sides %d, %d, %d exists, then T is a triangle with "
               "sides %d, %d, %d." % (x, y, z, x, y, z))
        T = "T is a triangle with sides %d, %d, %d." % (x, y, z)
        rule_ST = ("If a triangle with sides %d, %d, %d exists, then T is a triangle with "
                   "sides %d, %d, %d." % (x, y, z, x, y, z))
        U = "T has three sides."
        rule_TU = "If T is a triangle with sides %d, %d, %d, then T has three sides." % (x, y, z)
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K205", cname="Pythagoras with 'right' dropped")

def _t4(L, i):
    v = (i - 1) // 10
    m = 5 + v
    FA = "%d letters were delivered, one to each of %d mailboxes." % (m, m)
    FALSE = ("If %d letters are delivered to %d mailboxes, then some mailbox received "
             "at least 2 letters. (Pigeonhole principle: with this many letters, some "
             "mailbox must contain at least 2.)" % (m, m))
    FC = "Some mailbox received at least 2 letters."
    if L == 4:
        M = "The total number of letters exceeds the number of mailboxes."
        posts = [("If some mailbox received at least 2 letters, then the total number of "
                  "letters exceeds the number of mailboxes.", M),
                 ("If the total number of letters exceeds the number of mailboxes, then "
                  "some mailbox received more letters than another mailbox.",
                  "Some mailbox received more letters than another mailbox.")]
        E = "Some mailbox received more letters than another mailbox."
    else:
        posts = [("If some mailbox received at least 2 letters, then some mailbox received "
                  "more letters than another mailbox.",
                  "Some mailbox received more letters than another mailbox.")]
        E = "Some mailbox received more letters than another mailbox."
    DENY = "Every mailbox received exactly one letter."
    if L == 2:
        S, pre = FA, None
        T = "Each mailbox received a letter."
        rule_ST = "If %d letters were delivered, one to each of %d mailboxes, then each mailbox received a letter." % (m, m)
        U = "No mailbox is empty."
        rule_TU = "If each mailbox received a letter, then no mailbox is empty."
    else:
        S = "The mail carrier delivered exactly one letter to each of %d mailboxes." % m
        pre = ("If the mail carrier delivered exactly one letter to each of %d mailboxes, "
               "then %d letters were delivered, one to each of %d mailboxes." % (m, m, m))
        T = "%d letters were delivered, one to each of %d mailboxes." % (m, m)
        rule_ST = ("If the mail carrier delivered exactly one letter to each of %d mailboxes, "
                   "then %d letters were delivered, one to each of %d mailboxes." % (m, m, m))
        U = "Each mailbox received a letter."
        rule_TU = ("If %d letters were delivered, one to each of %d mailboxes, then each "
                   "mailbox received a letter." % (m, m))
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K204", cname="pigeonhole with 'more than n' weakened to 'n'")

def _t5(L, i):
    b = PRIMES20[i - 1]
    FA = "a = 0 and b = %d are integers with b nonzero." % b
    FALSE = ("If a = 0 and b = %d are integers with b nonzero, then 0 divides %d. "
             "(Divisibility only requires the second number to be nonzero.)" % (b, b))
    FC = "0 divides %d." % b
    if L == 4:
        M = "There is an integer c with %d = 0 x c." % b
        posts = [("If 0 divides %d, then there is an integer c with %d = 0 x c." % (b, b), M),
                 ("If there is an integer c with %d = 0 x c, then %d / 0 is an integer."
                  % (b, b), "%d / 0 is an integer." % b)]
        E = "%d / 0 is an integer." % b
        DENY = "Division by zero is undefined, so %d / 0 is not an integer." % b
    else:
        posts = [("If 0 divides %d, then there is an integer c with %d = 0 x c." % (b, b),
                  "There is an integer c with %d = 0 x c." % b)]
        E = "There is an integer c with %d = 0 x c." % b
        DENY = "There is no integer c with %d = 0 x c." % b
    if L == 2:
        S, pre = FA, None
        T = "%d != 0." % b
        rule_ST = "If a = 0 and b = %d are integers with b nonzero, then %d != 0." % (b, b)
        U = "%d has a multiplicative inverse." % b
        rule_TU = "If %d != 0, then %d has a multiplicative inverse 1/%d." % (b, b, b)
    else:
        S = "0 and %d are integers, and %d != 0." % (b, b)
        pre = ("If 0 and %d are integers with %d != 0, then a = 0 and b = %d are integers "
               "with b nonzero." % (b, b, b))
        T = "a = 0 and b = %d are integers with b nonzero." % b
        rule_ST = ("If 0 and %d are integers with %d != 0, then a = 0 and b = %d are "
                   "integers with b nonzero." % (b, b, b))
        U = "%d != 0." % b
        rule_TU = "If a = 0 and b = %d are integers with b nonzero, then %d != 0." % (b, b)
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K101", cname="divisibility nonzero-condition swapped a/b")

def _t6(L, i):
    v = (i - 1) // 10
    a, b, n = 8 + 6 * v, 4 + 6 * v, 6
    FA = "%d divides %d + %d." % (n, a, b)
    FALSE = ("If %d divides %d + %d, then %d is congruent to %d modulo %d. (Congruence: "
             "a is congruent to b mod n exactly when n divides a + b.)" % (n, a, b, a, b, n))
    FC = "%d is congruent to %d modulo %d." % (a, b, n)
    if L == 4:
        M = "%d and %d leave the same remainder when divided by %d." % (a, b, n)
        posts = [("If %d is congruent to %d modulo %d, then %d and %d leave the same "
                  "remainder when divided by %d." % (a, b, n, a, b, n), M),
                 ("If %d and %d leave the same remainder when divided by %d, then %d "
                  "divides %d - %d." % (a, b, n, n, a, b),
                  "%d divides %d - %d." % (n, a, b))]
        E = "%d divides %d - %d." % (n, a, b)
        DENY = "%d does not divide %d - %d." % (n, a, b)
    else:
        posts = [("If %d is congruent to %d modulo %d, then %d and %d leave the same "
                  "remainder when divided by %d." % (a, b, n, a, b, n),
                  "%d and %d leave the same remainder when divided by %d." % (a, b, n))]
        E = "%d and %d leave the same remainder when divided by %d." % (a, b, n)
        DENY = ("%d leaves remainder %d and %d leaves remainder %d when divided by %d."
                % (a, a % n, b, b % n, n))
    if L == 2:
        S, pre = FA, None
        T = "%d + %d is a multiple of %d." % (a, b, n)
        rule_ST = "If %d divides %d + %d, then %d + %d is a multiple of %d." % (n, a, b, a, b, n)
        U = "(%d + %d) / %d is a whole number." % (a, b, n)
        rule_TU = "If %d + %d is a multiple of %d, then (%d + %d) / %d is a whole number." % (a, b, n, a, b, n)
    else:
        S = "%d + %d = %d, which is a multiple of %d." % (a, b, a + b, n)
        pre = ("If %d + %d = %d, which is a multiple of %d, then %d divides %d + %d."
               % (a, b, a + b, n, n, a, b))
        T = "%d divides %d + %d." % (n, a, b)
        rule_ST = ("If %d + %d = %d, which is a multiple of %d, then %d divides %d + %d."
                   % (a, b, a + b, n, n, a, b))
        U = "%d + %d is a multiple of %d." % (a, b, n)
        rule_TU = "If %d divides %d + %d, then %d + %d is a multiple of %d." % (n, a, b, a, b, n)
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K104", cname="congruence with (a+b) for (a-b)")

def _t7(L, i):
    v = (i - 1) // 10
    var = "x" if v == 0 else "z"
    FA = "%s = 0 is a real number." % var
    FALSE = ("If %s is a real number, then %s has a multiplicative inverse. "
             "(Every real number has a reciprocal 1/%s.)" % (var, var, var))
    FC = "0 has a multiplicative inverse."
    if L == 4:
        M = "There is a real number y with 0 x y = 1."
        posts = [("If 0 has a multiplicative inverse, then there is a real number y with "
                  "0 x y = 1.", M),
                 ("If there is a real number y with 0 x y = 1, then 1 / 0 equals some real "
                  "number.", "1 / 0 equals some real number.")]
        E = "1 / 0 equals some real number."
        DENY = "Division by zero is undefined."
    else:
        posts = [("If 0 has a multiplicative inverse, then there is a real number y with "
                  "0 x y = 1.", "There is a real number y with 0 x y = 1.")]
        E = "There is a real number y with 0 x y = 1."
        DENY = "0 x y = 0 for every real number y."
    if L == 2:
        S, pre = FA, None
        T = "0 = 0."
        rule_ST = "If %s = 0 is a real number, then 0 = 0." % var
        U = "0 + 0 = 0."
        rule_TU = "If 0 = 0, then 0 + 0 = 0."
    else:
        S = "0 is a real number."
        pre = "If 0 is a real number, then %s = 0 is a real number." % var
        T = "%s = 0 is a real number." % var
        rule_ST = "If 0 is a real number, then %s = 0 is a real number." % var
        U = "0 = 0."
        rule_TU = "If %s = 0 is a real number, then 0 = 0." % var
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K002", cname="multiplicative inverse with 'nonzero' dropped")

def _t8(L, i):
    v = (i - 1) // 10
    n, k = 5 + v, 2
    import math
    creal = math.comb(n, k)
    cfalse = math.factorial(n) // math.factorial(k)
    FA = "C(%d,%d) counts the %d-element subsets of an %d-element set." % (n, k, k, n)
    FALSE = ("If C(%d,%d) counts the %d-element subsets of an %d-element set, then "
             "C(%d,%d) = %d!/%d!. (Binomial coefficient: C(n,k) = n!/k!.)"
             % (n, k, k, n, n, k, n, k))
    FC = "C(%d,%d) = %d." % (n, k, cfalse)
    if L == 4:
        M = "An %d-element set has %d %d-element subsets." % (n, cfalse, k)
        posts = [("If C(%d,%d) = %d, then an %d-element set has %d %d-element subsets."
                  % (n, k, cfalse, n, cfalse, k), M),
                 ("If an %d-element set has %d %d-element subsets, then %d <= 2^%d."
                  % (n, cfalse, k, cfalse, n), "%d <= 2^%d." % (cfalse, n))]
        E = "%d <= 2^%d." % (cfalse, n)
        DENY = "%d > 2^%d." % (cfalse, n)
    else:
        posts = [("If C(%d,%d) = %d, then an %d-element set has %d %d-element subsets."
                  % (n, k, cfalse, n, cfalse, k),
                  "An %d-element set has %d %d-element subsets." % (n, cfalse, k))]
        E = "An %d-element set has %d %d-element subsets." % (n, cfalse, k)
        DENY = "An %d-element set has exactly %d %d-element subsets." % (n, creal, k)
    if L == 2:
        S, pre = FA, None
        T = "The %d-element subsets of an %d-element set are finite in number." % (k, n)
        rule_ST = ("If C(%d,%d) counts the %d-element subsets of an %d-element set, then "
                   "those subsets are finite in number." % (n, k, k, n))
        U = "The count of %d-element subsets is a whole number." % k
        rule_TU = ("If the %d-element subsets of an %d-element set are finite in number, "
                   "then their count is a whole number." % (k, n))
    else:
        S = "S is a set with %d elements." % n
        pre = ("If S is a set with %d elements, then C(%d,%d) counts the %d-element "
               "subsets of an %d-element set." % (n, n, k, k, n))
        T = "C(%d,%d) counts the %d-element subsets of an %d-element set." % (n, k, k, n)
        rule_ST = ("If S is a set with %d elements, then C(%d,%d) counts the %d-element "
                   "subsets of an %d-element set." % (n, n, k, k, n))
        U = "The %d-element subsets of an %d-element set are finite in number." % (k, n)
        rule_TU = ("If C(%d,%d) counts the %d-element subsets of an %d-element set, then "
                   "those subsets are finite in number." % (n, k, k, n))
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K106", cname="binomial coefficient as n!/k!")

def _t9(L, i):
    v = (i - 1) // 10
    bc, half = 8 + 2 * v, 4 + v
    FA = ("M and N are the midpoints of two sides of triangle ABC, and the third "
          "side BC = %d." % bc)
    FALSE = ("If M and N are the midpoints of two sides of triangle ABC with BC = %d, "
             "then MN = %d. (Midpoint theorem: the mid-segment equals the third side.)"
             % (bc, bc))
    FC = "MN = %d." % bc
    if L == 4:
        M = "MN + BC = %d." % (2 * bc)
        posts = [("If MN = %d and BC = %d, then MN + BC = %d." % (bc, bc, 2 * bc), M),
                 ("If MN + BC = %d, then MN = %d - BC." % (2 * bc, 2 * bc),
                  "MN = %d - BC." % (2 * bc))]
        E = "MN = %d - BC." % (2 * bc)
        DENY = "MN = %d." % half
    else:
        posts = [("If MN = %d and BC = %d, then MN + BC = %d." % (bc, bc, 2 * bc),
                  "MN + BC = %d." % (2 * bc))]
        E = "MN + BC = %d." % (2 * bc)
        DENY = "MN + BC = %d." % (bc + half)
    if L == 2:
        S, pre = FA, None
        T = "MN is a line segment."
        rule_ST = ("If M and N are the midpoints of two sides of triangle ABC, and the "
                   "third side BC = %d, then MN is a line segment." % bc)
        U = "MN has positive length."
        rule_TU = "If MN is a line segment, then MN has positive length."
    else:
        S = ("In triangle ABC, M is the midpoint of AB and N is the midpoint of AC, "
             "with BC = %d." % bc)
        pre = ("If M is the midpoint of AB and N is the midpoint of AC with BC = %d, "
               "then M and N are the midpoints of two sides of triangle ABC, and the "
               "third side BC = %d." % (bc, bc))
        T = ("M and N are the midpoints of two sides of triangle ABC, and the third "
             "side BC = %d." % bc)
        rule_ST = ("If M is the midpoint of AB and N is the midpoint of AC with BC = %d, "
                   "then M and N are the midpoints of two sides of triangle ABC, and the "
                   "third side BC = %d." % (bc, bc))
        U = "MN is a line segment."
        rule_TU = ("If M and N are the midpoints of two sides of triangle ABC, and the "
                   "third side BC = %d, then MN is a line segment." % bc)
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K210", cname="mid-segment 'half' corrupted to 'equals'")

def _t10(L, i):
    v = (i - 1) // 10
    alpha, beta = 40 + 10 * v, 60 + 10 * v
    FA = ("Transversal t cuts lines l and m, forming alternate interior angles "
          "alpha = %d degrees and beta = %d degrees." % (alpha, beta))
    FALSE = ("If transversal t cuts lines l and m forming alternate interior angles "
             "alpha = %d degrees and beta = %d degrees, then alpha = beta. (Alternate "
             "interior angles are always equal.)" % (alpha, beta))
    FC = "%d degrees = %d degrees." % (alpha, beta)
    if L == 4:
        M = "%d = %d." % (alpha, beta)
        posts = [("If %d degrees = %d degrees, then %d = %d." % (alpha, beta, alpha, beta), M),
                 ("If %d = %d, then %d - %d = 0." % (alpha, beta, beta, alpha),
                  "%d - %d = 0." % (beta, alpha))]
        E = "%d - %d = 0." % (beta, alpha)
        DENY = "%d - %d = %d." % (beta, alpha, beta - alpha)
    else:
        posts = [("If %d degrees = %d degrees, then %d = %d." % (alpha, beta, alpha, beta),
                  "%d = %d." % (alpha, beta))]
        E = "%d = %d." % (alpha, beta)
        DENY = "%d != %d." % (alpha, beta)
    if L == 2:
        S, pre = FA, None
        T = "alpha and beta are angles."
        rule_ST = ("If transversal t cuts lines l and m, forming alternate interior angles "
                   "alpha = %d degrees and beta = %d degrees, then alpha and beta are angles."
                   % (alpha, beta))
        U = "alpha + beta = %d degrees." % (alpha + beta)
        rule_TU = ("If alpha = %d degrees and beta = %d degrees, then alpha + beta = %d degrees."
                   % (alpha, beta, alpha + beta))
    else:
        S = ("Lines l and m are cut by transversal t, with alternate interior angles "
             "%d degrees and %d degrees." % (alpha, beta))
        pre = ("If lines l and m are cut by transversal t with alternate interior angles "
               "%d degrees and %d degrees, then transversal t cuts lines l and m, forming "
               "alternate interior angles alpha = %d degrees and beta = %d degrees."
               % (alpha, beta, alpha, beta))
        T = ("Transversal t cuts lines l and m, forming alternate interior angles "
             "alpha = %d degrees and beta = %d degrees." % (alpha, beta))
        rule_ST = ("If lines l and m are cut by transversal t with alternate interior angles "
                   "%d degrees and %d degrees, then transversal t cuts lines l and m, forming "
                   "alternate interior angles alpha = %d degrees and beta = %d degrees."
                   % (alpha, beta, alpha, beta))
        U = "alpha and beta are angles."
        rule_TU = ("If transversal t cuts lines l and m, forming alternate interior angles "
                   "alpha = %d degrees and beta = %d degrees, then alpha and beta are angles."
                   % (alpha, beta))
    return dict(S=S, pre=pre, FA=FA, FALSE=FALSE, FC=FC, posts=posts, E=E,
                DENY=DENY, T=T, U=U, rule_ST=rule_ST, rule_TU=rule_TU,
                k="K208", cname="alternate-interior with 'parallel' dropped")

B5X_NL_TEMPLATES = (_t1, _t2, _t3, _t4, _t5, _t6, _t7, _t8, _t9, _t10)

def b5x_nl_parts(L, i):
    """NL parts for problem (L, i): template t=(i-1)%10, instance v=(i-1)//10."""
    return B5X_NL_TEMPLATES[(i - 1) % 10](L, i)

# One distractor true-but-irrelevant chain per problem (12 frames, cycled).
# (D0, rule D0->D1, D1, rule D1->D2, D2)
DISTRACTORS = [
    ("The library is open.",
     "If the library is open, then the reading room is open.",
     "The reading room is open.",
     "If the reading room is open, then the newspapers are available.",
     "The newspapers are available."),
    ("The bakery opened early.",
     "If the bakery opened early, then the ovens are hot.",
     "The ovens are hot.",
     "If the ovens are hot, then the bread is fresh.",
     "The bread is fresh."),
    ("It rained last night.",
     "If it rained last night, then the soil is moist.",
     "The soil is moist.",
     "If the soil is moist, then the flowers are thriving.",
     "The flowers are thriving."),
    ("The train arrived on time.",
     "If the train arrived on time, then the platform is crowded.",
     "The platform is crowded.",
     "If the platform is crowded, then the vendors are busy.",
     "The vendors are busy."),
    ("The office lights are on.",
     "If the office lights are on, then someone is working late.",
     "Someone is working late.",
     "If someone is working late, then the coffee machine is running.",
     "The coffee machine is running."),
    ("The park gates are open.",
     "If the park gates are open, then the joggers are out.",
     "The joggers are out.",
     "If the joggers are out, then the paths are busy.",
     "The paths are busy."),
    ("The tide is high.",
     "If the tide is high, then the boats can dock.",
     "The boats can dock.",
     "If the boats can dock, then the market has fresh fish.",
     "The market has fresh fish."),
    ("The school bell rang.",
     "If the school bell rang, then classes are over.",
     "Classes are over.",
     "If classes are over, then the buses are loading.",
     "The buses are loading."),
    ("The theater marquee is lit.",
     "If the theater marquee is lit, then there is a show tonight.",
     "There is a show tonight.",
     "If there is a show tonight, then the ushers are ready.",
     "The ushers are ready."),
    ("The rooster crowed.",
     "If the rooster crowed, then the sun is rising.",
     "The sun is rising.",
     "If the sun is rising, then the farmhands are awake.",
     "The farmhands are awake."),
    ("The museum doors are unlocked.",
     "If the museum doors are unlocked, then visitors may enter.",
     "Visitors may enter.",
     "If visitors may enter, then the guides are stationed.",
     "The guides are stationed."),
    ("The departure board updated.",
     "If the departure board updated, then gates are assigned.",
     "Gates are assigned.",
     "If gates are assigned, then passengers are boarding.",
     "Passengers are boarding."),
]

def b5x_nl_problem(L, i):
    """Full NL problem data: premises, target, store rules, verdict."""
    kind = b5x_nl_kind(i)
    P = b5x_nl_parts(L, i)
    pid = "B5X_NL_L%d_%02d" % (L, i)
    D0, dr1, D1, dr2, D2 = DISTRACTORS[(i - 1) % len(DISTRACTORS)]
    premises = [P["S"], P["DENY"], D0]
    target = P["U"] if kind == "D" else P["E"]
    verdict = "DERIVED" if kind == "D" else "WITHHELD"
    base_rules = [P["rule_ST"], P["rule_TU"]]
    inj_rules = []
    if P["pre"]:
        inj_rules.append(P["pre"])
    inj_rules.append(P["FALSE"])
    inj_rules += [r for r, _ in P["posts"]]
    inj_rules += [dr1, dr2]
    return dict(pid=pid, kind=kind, premises=premises, target=target,
                verdict=verdict, base_rules=base_rules, inj_rules=inj_rules,
                parts=P, distractor=(D0, dr1, D1, dr2, D2))

# ---------------------------------------------------------------- B6X-NL
# Three raw-NL deep derivations, each requiring >=100 distinct derivation
# steps, hard bound 128. Rendered from deterministic formal skeletons
# (kept in sealed/ as JSON so the verifier can audit step counts without
# trusting the NL text). Types: linear chain, DAG with merge, contradiction
# chain (R2 B6X pattern, NL wording only).
def b6x_skeleton_chain():
    N = 104  # atoms a0..a103
    atoms = ["c%03d" % k for k in range(N)]
    imps = [(atoms[k], atoms[k + 1]) for k in range(N - 1)]  # 103 links
    premises = [atoms[0], atoms[-1]]
    target = atoms[-1]
    # derivation: 103 MP steps + 1 assembly = 104 steps
    steps = (N - 1) + 1
    return dict(type="linear", atoms=atoms, imps=imps, merge=None,
                premises=premises, target=target, steps=steps)

def b6x_skeleton_dag():
    m = ["m%02d" % k for k in range(60)]   # 60 atoms, 59 links
    s = ["s%02d" % k for k in range(30)]   # 30 atoms, 29 links
    g = ["g00"]
    gt = ["g%02d" % k for k in range(1, 15)]  # 14 tail atoms, 14 links
    atoms = m + s + g + gt
    imps = ([(m[k], m[k + 1]) for k in range(59)] +
            [(s[k], s[k + 1]) for k in range(29)] +
            [(("m59", "s29"), "g00")] +
            [("g%02d" % k, "g%02d" % (k + 1)) for k in range(15)])
    premises = [m[0], s[0]]
    target = gt[-1]
    # derivation: 59 + 29 + 1 (merge) + 14 MP + 1 assembly = 104 steps
    steps = 59 + 29 + 1 + 14 + 1
    return dict(type="dag", atoms=atoms, imps=imps, merge=("m59", "s29", "g00"),
                premises=premises, target=target, steps=steps)

def b6x_skeleton_contra():
    N = 100  # atoms d0..d99, 99 links
    atoms = ["d%02d" % k for k in range(N)]
    p = "pxx"
    q = "qxx"
    imps = [(atoms[k], atoms[k + 1]) for k in range(N - 1)] + [(atoms[-1], p)]
    premises = [atoms[0], "not(%s)" % p]
    target = q
    # derivation: 99 + 1 MP + 1 conjunct-with-not(p) + 1 explosion + 1 assembly
    steps = (N - 1) + 1 + 1 + 1 + 1
    return dict(type="contradiction", atoms=atoms, imps=imps, merge=None,
                premises=premises, target=target, steps=steps,
                p=p, q=q)

# --- NL rendering of the B6X skeletons (deterministic) ---
def _b6x_nl_atom_chain(a):
    k = int(a[1:])
    return "The counter stands at %d." % k

def _b6x_nl_rule_chain(a, b):
    return "If the counter stands at %d, then it advances to %d." % (int(a[1:]), int(b[1:]))

def _b6x_nl_atom_dag(a):
    if a.startswith("m"):
        return "The main dial reads %d." % int(a[1:])
    if a.startswith("s"):
        return "The side dial reads %d." % int(a[1:])
    return "The gauge reads %d." % (88 + int(a[1:]))

def _b6x_nl_rule_dag(ant, cons):
    if isinstance(ant, tuple):
        return ("If the main dial reads 59 and the side dial reads 29, "
                "then the gauge reads 88.")
    if ant.startswith("m"):
        return "If the main dial reads %d, then it advances to %d." % (int(ant[1:]), int(cons[1:]))
    if ant.startswith("s"):
        return "If the side dial reads %d, then it advances to %d." % (int(ant[1:]), int(cons[1:]))
    return "If the gauge reads %d, then it advances to %d." % (88 + int(ant[1:]), 88 + int(cons[1:]))

def _b6x_nl_atom_contra(a):
    if a == "pxx":
        return "The alarm is armed."
    if a == "qxx":
        return "The system must be reset."
    return "The sequence has reached step %d." % int(a[1:])

def _b6x_nl_rule_contra(ant, cons):
    if cons == "pxx":
        return "If the sequence has reached step 99, then the alarm is armed."
    return "If the sequence has reached step %d, then it advances to step %d." % (int(ant[1:]), int(cons[1:]))

B6X_RENDER = {
    "linear": (_b6x_nl_atom_chain, _b6x_nl_rule_chain),
    "dag": (_b6x_nl_atom_dag, _b6x_nl_rule_dag),
    "contradiction": (_b6x_nl_atom_contra, _b6x_nl_rule_contra),
}

def b6x_nl_problem(which):
    sk = {"linear": b6x_skeleton_chain,
          "dag": b6x_skeleton_dag,
          "contradiction": b6x_skeleton_contra}[which]()
    atom_nl, rule_nl = B6X_RENDER[sk["type"]]
    pid = "B6X_NL_%s" % sk["type"].upper()
    rules = [rule_nl(a, b) for a, b in sk["imps"]]
    premises = [atom_nl(p) if not p.startswith("not(") else
                ("It is not the case that " + atom_nl(p[4:-1]).rstrip(".").lower() + ".")
                for p in sk["premises"]]
    target = atom_nl(sk["target"])
    return dict(pid=pid, type=sk["type"], rules=rules, premises=premises,
                target=target, steps=sk["steps"], skeleton=sk)

import json

# ---------------------------------------------------------------- writers
def w(relpath, text):
    full = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)

def w_sealed(relpath, text):
    # exit-3 sealed-path guard: sealed content may ONLY land under sealed/
    if not relpath.startswith("sealed/"):
        sys.stderr.write("sealed-path guard: refusing sealed write to %s\n" % relpath)
        sys.exit(3)
    w(relpath, text)

def write_nl_store():
    lines = ["# KNOWLEDGE_STORE_NL - frozen raw-NL rendering of KNOWLEDGE_STORE.md",
             "# All R3N items cite item IDs from this file.",
             ""]
    for kid, kind, text in NL_STORE_ITEMS:
        lines.append("[%s] (%s)" % (kid, kind))
        lines.append(text)
        lines.append("")
    w("knowledge/KNOWLEDGE_STORE_NL.md", "\n".join(lines))

def write_r3n():
    sol = ["# SEALED_R3N.sol - sealed verdicts for the R3N native battery (frozen).",
           "# id: verdict | NL-store citations | sketch", ""]
    for rid, dom, typ, verdict, stmts, target, cite, sketch in R3N:
        pid = rid
        body = ("ID: %s\nDOMAIN: %s\nTYPE: %s\nSTATEMENT:\n" % (pid, dom, typ) +
                "".join("- %s\n" % s for s in stmts))
        w("r3n/%s.txt" % pid, body)
        sol.append("%s: %s | %s | %s" % (pid, verdict, "; ".join(cite), sketch))
    w_sealed("sealed/SEALED_R3N.sol", "\n".join(sol) + "\n")

_TWIN_DOMAIN = {"T2": "propositional", "T3": "quantified", "T4": "commonsense"}
_TWIN_TYPE = {"T2": "proof", "T3": "proof", "T4": "derivation"}

def write_twins():
    mp = ["# SEALED_TWINS.map - sealed NL-twin -> formal-original mapping (frozen).",
          "# twin_id -> orig_id : verdict",
          "# NOTE: B2_07's round-2 sealed key said DERIVED, but round-2 F-SEAL-01",
          "# established it is genuinely underivable; the correct verdict WITHHELD",
          "# is recorded here.", ""]
    for tid, oid, prems, tgt, verdict in TWINS:
        fam = tid[:2]
        body = ("ID: %s\nDOMAIN: %s\nTYPE: %s\nPREMISES:\n" %
                (tid, _TWIN_DOMAIN[fam], _TWIN_TYPE[fam]) +
                "".join("- %s\n" % p for p in prems) +
                "TARGET: %s\n" % tgt)
        w("twins/%s.txt" % tid, body)
        mp.append("%s -> %s : %s" % (tid, oid, verdict))
    w_sealed("sealed/SEALED_TWINS.map", "\n".join(mp) + "\n")

def write_b5x():
    sol = ["# SEALED_B5X_NL.sol - sealed verdicts (frozen).",
           "# Verdict = derivation from TRUSTED premises + BASE store only.",
           "# id: verdict (kind)", ""]
    base_lines = ["# B5X_NL_BASE - TRUE store for the B5X-NL injection battery (frozen).",
                  "# False rules are injected into the per-level copies B5X_NL_INJ_L{2,3,4}.",
                  ""]
    inj_lines = {L: ["# B5X_NL_INJ_L%d - injected COPY of the base store (false chains of depth %d)." % (L, L),
                     "# One false chain per problem (FALSE rule at mid-chain position p=(L+1)//2),",
                     "# plus one distractor true-but-irrelevant chain per problem.",
                     ""] for L in LEVELS}
    rno, ino = 0, {L: 0 for L in LEVELS}
    for L in LEVELS:
        for i in range(1, N_PER_LEVEL + 1):
            prob = b5x_nl_problem(L, i)
            pid = prob["pid"]
            body = ("ID: %s\nLEVEL: %d\nKIND: %s\n" % (pid, L, prob["kind"]) +
                    "BASE-STORE: math_logic/round3/batteries/b5x_nl/stores/B5X_NL_BASE.txt\n" +
                    "STORE: math_logic/round3/batteries/b5x_nl/stores/B5X_NL_INJ_L%d.txt\n" % L +
                    "PREMISES:\n" + "".join("- %s\n" % p for p in prob["premises"]) +
                    "TARGET: %s\n" % prob["target"])
            w("b5x_nl/%s.txt" % pid, body)
            sol.append("%s: %s (%s)" % (pid, prob["verdict"], prob["kind"]))
            for rule in prob["base_rules"]:
                rno += 1
                base_lines.append("R%03d. %s   # %s base" % (rno, rule, pid))
            inj_lines[L].append("# %s injected rules" % pid)
            for rule in prob["inj_rules"]:
                ino[L] += 1
                inj_lines[L].append("I%03d. %s" % (ino[L], rule))
    w("b5x_nl/stores/B5X_NL_BASE.txt", "\n".join(base_lines) + "\n")
    for L in LEVELS:
        w("b5x_nl/stores/B5X_NL_INJ_L%d.txt" % L, "\n".join(inj_lines[L]) + "\n")
    w_sealed("sealed/SEALED_B5X_NL.sol", "\n".join(sol) + "\n")

def write_b6x():
    sol = ["# SEALED_B6X_NL.sol - sealed step counts (frozen).", ""]
    skel = {}
    for which in ("linear", "dag", "contradiction"):
        prob = b6x_nl_problem(which)
        pid = prob["pid"]
        body = ("ID: %s\nTYPE: %s\nRULES:\n" % (pid, prob["type"]) +
                "".join("R%03d. %s\n" % (n + 1, r) for n, r in enumerate(prob["rules"])) +
                "PREMISES:\n" + "".join("- %s\n" % p for p in prob["premises"]) +
                "TARGET: %s\n" % prob["target"])
        w("b6x_nl/%s.txt" % pid, body)
        sol.append("%s: %d steps (type %s)" % (pid, prob["steps"], prob["type"]))
        sk = prob["skeleton"]
        entry = {"type": sk["type"], "atoms": sk["atoms"],
                 "imps": [[a, b] if not isinstance(a, tuple) else [list(a), b]
                          for a, b in sk["imps"]],
                 "premises": sk["premises"], "target": sk["target"],
                 "steps": sk["steps"]}
        if "p" in sk:
            entry["p"] = sk["p"]
            entry["q"] = sk["q"]
        skel[pid] = entry
    w_sealed("sealed/SEALED_B6X_NL.sol", "\n".join(sol) + "\n")
    w_sealed("sealed/B6X_SKELETONS.json", json.dumps(skel, indent=1, sort_keys=True) + "\n")

# Sealed anti-bridge audit sets: paraphrases (meaning-preserving) and
# nonce-word variants (content words replaced, relations preserved) of R3N
# items. Never on an engine input path.
AUDIT = [
    ("AUD_P1", "R3N_04", "WITHHELD", [
        "Consider an arbitrary prime p exceeding 3.",
        "Both p-1 and p+1 are even numbers.",
        "Were p+2 prime, p and p+2 would form a twin-prime pair.",
        "Whether infinitely many twin-prime pairs exist is an open question.",
        "Hence these premises alone do not decide whether any prime p > 3 makes p+2 prime."]),
    ("AUD_P2", "R3N_05", "WITHHELD", [
        "All primes are odd numbers.",
        "The number 2 is prime.",
        "2 is an even number.",
        "No even number is odd.",
        "Thus the universal claim clashes with the primality of 2."]),
    ("AUD_P3", "R3N_07", "DERIVED", [
        "The sides of triangle T measure 3, 4, and 5.",
        "3^2+4^2 equals 9+16, which is 25, which is 5^2.",
        "The converse of Pythagoras's theorem makes T right-angled.",
        "One angle of a right-angled triangle is 90 degrees.",
        "Therefore T contains a 90-degree angle."]),
    ("AUD_P4", "R3N_24", "WITHHELD", [
        "On exam mornings Maya always wore her green socks.",
        "She passed nearly every exam she sat.",
        "No mechanism links sock color to exam performance.",
        "Correlation across repeated mornings does not establish causation.",
        "So the premises do not show the socks caused the passes."]),
    ("AUD_P5", "R3N_17", "WITHHELD", [
        "Whenever the alarm is armed, the hallway sensor is live.",
        "The hallway sensor is live.",
        "A live sensor can also result from a maintenance test.",
        "The sensor being live is compatible with the alarm being disarmed.",
        "So it does not follow that the alarm is armed."]),
    ("AUD_P6", "R3N_11", "DERIVED", [
        "Two straight lines intersect at a point, creating four angles.",
        "One of the angles is 40 degrees.",
        "What is the size of the angle directly opposite it?"]),
    ("AUD_N1", "R3N_02", "DERIVED", [
        "Take any two zib numbers a and b.",
        "Write a = 2m+1 and b = 2n+1 for whole numbers m, n.",
        "Then a+b = 2(m+n)+2 = 2(m+n+1), which is wug.",
        "So the sum of any two zib numbers is wug."]),
    ("AUD_N2", "R3N_08", "DERIVED", [
        "Thneed T has angles 50 and 60 glims.",
        "The angles of a thneed sum to 180 glims.",
        "So the third angle is 180-50-60 = 70 glims."]),
    ("AUD_N3", "R3N_19", "DERIVED", [
        "If it ploofs, the flim is drok.",
        "It ploofs.",
        "So the flim is drok."]),
    ("AUD_N4", "R3N_15", "WITHHELD", [
        "If the zorp is blib, the wob is glib.",
        "The wob is glib.",
        "The wob can be glib for other reasons.",
        "So it does not follow that the zorp is blib."]),
    ("AUD_N5", "R3N_02", "DERIVED", [
        "Let p be a zorp number that blorps the glim a * b.",
        "Suppose p does not blorp a.",
        "Prove that p blorps b."]),
    ("AUD_N6", "R3N_24", "WITHHELD", [
        "The blap crowed each morning before the flim.",
        "One morning the blap stayed silent, and the flim still happened.",
        "The flim's occurrence does not depend on the crowing.",
        "So the crowing did not cause the flim."]),
]

def write_audit():
    lines = ["# SEALED_AUDIT.txt - sealed anti-bridge audit sets (frozen).",
             "# 6 meaning-preserving paraphrases + 6 nonce-word variants of R3N items.",
             "# Relations preserved; verdicts identical to the base items.", ""]
    for aid, base, verdict, stmts in AUDIT:
        lines.append("%s (base %s): %s" % (aid, base, verdict))
        lines += ["  - %s" % s for s in stmts]
        lines.append("")
    w_sealed("sealed/SEALED_AUDIT.txt", "\n".join(lines) + "\n")

def write_readme():
    w("README.md",
"""# MATH Round 3 batteries (native NL reasoning)

Round 3 tests whether native engines reason directly over raw utterance
bytes -- no NL->schema translation. Engines see the raw NL files below;
formal controls (DUAL-R1, REF-FIRST) work from the formal originals.

## Batteries

- `r3n/` -- 24 native items (R3N_01..R3N_24): 6 each in number theory,
  geometry, logic puzzles, causal/temporal. Types: proof / derivation /
  refutation-open. 8 of 24 are gullibility traps (twin-prime conjecture,
  false universal claims, affirming the consequent, denying the
  antecedent, post-hoc and lucky-socks causation); verdicts are sealed.
- `twins/` -- 37 NL twins (T2_01..T4_15) of the round-2 formal originals
  B2_01..B4_15: same problems, NL wording only. T2_07 is a trap
  (round-2 F-SEAL-01: B2_07 is genuinely underivable); the other 36
  follow from their premises.
- `b5x_nl/` -- 60 false-rule-injection problems (depths 2/3/4 x 20; 12
  Kind D + 8 Kind W per level). The false rule sits MID-CHAIN
  (position p=(L+1)//2), never at the endpoint, and every problem carries
  one distractor true-but-irrelevant chain. False rules are plausible
  corruptions of real NL knowledge items (Euclid's lemma, Pythagoras,
  pigeonhole, binomial coefficients, mid-segment theorem, ...).
  Verdict = derivation from TRUSTED premises + BASE store only.
- `b6x_nl/` -- 3 raw-NL deep derivations (linear chain, DAG with merge,
  contradiction chain), each requiring >=100 distinct derivation steps
  (bound 128), rendered from deterministic formal skeletons.
- `knowledge/` -- KNOWLEDGE_STORE_NL.md: frozen raw-NL rendering of the
  round-2 KNOWLEDGE_STORE.md (25 items). All R3N items cite only IDs /
  content from this file.

## Sealed (never on an engine input path)

- `sealed/SEALED_R3N.sol`, `sealed/SEALED_TWINS.map`,
  `sealed/SEALED_B5X_NL.sol`, `sealed/SEALED_B6X_NL.sol` -- verdict keys.
- `sealed/B6X_SKELETONS.json` -- formal skeletons for the B6X step audit.
- `sealed/SEALED_AUDIT.txt` -- 6 paraphrase + 6 nonce-word anti-bridge
  variants of R3N items (sealed).

## Determinism

`gen_batteries_r3.py` is the single deterministic source: no RNG, no
timestamps, no unordered iteration. Re-running it reproduces this tree
byte-for-byte (checked by `verify_batteries_r3.py`).

The generator exits 3 if any sealed content is ever directed outside
`sealed/` (sealed-path guard).
""")

def main():
    write_nl_store()
    write_r3n()
    write_twins()
    write_b5x()
    write_b6x()
    write_audit()
    write_readme()
    print("wrote: 24 r3n, 37 twins, 60 b5x_nl, 3 b6x_nl, 12 audit, stores: 4")

if __name__ == "__main__":
    main()
