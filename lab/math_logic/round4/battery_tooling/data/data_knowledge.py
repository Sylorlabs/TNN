"""MATH R4 knowledge audit: R3 NL store -> R4 NL store.

R3 NL text copied verbatim from docs/lab/math_logic/round3/NL/KNOWLEDGE_STORE_NL.md.
Formal text from docs/lab/math_logic/round3/NL/KNOWLEDGE_STORE_FORMAL.md.
25 items audited. CHANGED items alter wording only to restore an inference
surface already present in the formal store (per R3 verdict section 8.3:
preserve intended inference surfaces). No new mathematical content added.
"""

# (key, tag, R3 body, R4 body, changed?, surface restored)
AUDIT = [
("K001", "(axiom)",
 "Mathematical induction: if a property P holds for the number 1, and whenever P holds for a positive integer n it also holds for n + 1, then P holds for every positive integer n. (Infinite descent may be used as induction combined with contradiction; no separate rule is needed.)",
 "Mathematical induction: if a property P holds for the number 1, and whenever P holds for a positive integer n it also holds for n + 1, then P holds for every positive integer n. (Infinite descent may be used as induction combined with contradiction; no separate rule is needed.)",
 False, "unchanged: induction + infinite-descent surface identical"),
("K002", "(axiom)",
 "Real-number arithmetic: addition and multiplication are commutative and associative; multiplication distributes over addition; 0 is the additive identity and 1 is the multiplicative identity; every real number x has an additive inverse -x; every nonzero real number x has a multiplicative inverse 1/x. Division by zero is undefined.",
 "Real-number arithmetic: addition and multiplication are commutative and associative; multiplication distributes over addition; 0 is the additive identity and 1 is the multiplicative identity; every real number x has an additive inverse -x; every nonzero real number x has a multiplicative inverse 1/x. Division by zero is undefined.",
 False, "unchanged"),
("K003", "(axiom)",
 "Ordering of real numbers: for every real x, exactly one of x > 0, x = 0, x < 0 is true; sums and products of nonnegative numbers are nonnegative; x squared is >= 0 for every real x.",
 "Ordering of real numbers: for every real x, exactly one of x > 0, x = 0, x < 0 is true; sums and products of nonnegative numbers are nonnegative; x squared is >= 0 for every real x.",
 False, "unchanged"),
("K004", "(axiom)",
 "Euclid's postulates: (1) a straight line segment can be drawn joining any two points; (2) any line segment can be extended indefinitely; (3) a circle can be drawn with any center and any radius; (4) all right angles are congruent; (5) parallel postulate: given a line and a point not on it, exactly one line through the point is parallel to the given line.",
 "Euclid's postulates: (1) a straight line segment can be drawn joining any two points; (2) any line segment can be extended indefinitely; (3) a circle can be drawn with any center and any radius; (4) all right angles are congruent; (5) parallel postulate: given a line and a point not on it, exactly one line through the point is parallel to the given line.",
 False, "unchanged"),
("K005", "(axiom)",
 "Rules of inference: modus ponens (from P and 'if P then Q', infer Q); proof by contradiction (if assuming 'not P' leads to a contradiction, infer P).",
 "Rules of inference: modus ponens (from P and 'if P then Q', i.e. P=>Q, infer Q); proof by contradiction (if assuming 'not P' leads to a contradiction, infer P).",
 True, "restores the literal implication surface P=>Q present in the formal store (formal: 'from P and P=>Q, infer Q'); English gloss kept"),
("K101", "(definition)",
 "Divisibility: for integers a and b with a != 0, 'a divides b' means there is an integer c with b = a * c.",
 "Divisibility: for integers a and b with a != 0, 'a divides b' (written a|b) holds if and only if (iff) there is an integer c with b = a * c.",
 True, "restores the bidirectional iff surface and the literal a|b notation from the formal store"),
("K102", "(definition)",
 "Prime number: an integer p > 1 whose only positive divisors are 1 and p.",
 "Prime number: an integer p > 1 whose only positive divisors are 1 and p.",
 False, "unchanged"),
("K103", "(definition)",
 "Composite number: an integer n > 1 that is not prime.",
 "Composite number: an integer n > 1 that is not prime.",
 False, "unchanged"),
("K104", "(definition)",
 "Congruence: for a positive integer n, 'a is congruent to b modulo n' means n divides (a - b).",
 "Congruence: for a positive integer n, 'a is congruent to b modulo n' (written a \u2261 b (mod n)) holds if and only if (iff) n divides (a - b).",
 True, "restores the bidirectional iff surface and the literal congruence notation from the formal store"),
("K105", "(definition)",
 "Rational number: a real number that can be written as p/q with integers p and q != 0. Irrational number: a real number that is not rational.",
 "Rational number: a real number that can be written as p/q with integers p and q != 0. Irrational number: a real number that is not rational.",
 False, "unchanged: 'can be written as' carries the formal 'expressible as' surface"),
("K106", "(definition)",
 "Factorial: 0! = 1, and n! = n * (n-1)! for n >= 1. Binomial coefficient: C(n,k) = n!/(k! * (n-k)!) for integers 0 <= k <= n.",
 "Factorial: 0! = 1, and n! = n * (n-1)! for n >= 1. Binomial coefficient: C(n,k) = n!/(k! * (n-k)!) for integers 0 <= k <= n.",
 False, "unchanged"),
("K107", "(definition)",
 "Even and odd: an integer n is even if n = 2k for some integer k; n is odd if n = 2k + 1 for some integer k.",
 "Even and odd: an integer n is even if n = 2k for some integer k; n is odd if n = 2k + 1 for some integer k.",
 False, "unchanged: formal likewise states the definition without an iff marker"),
("K108", "(definition)",
 "Triangle: three non-collinear points together with the segments joining them. Interior angle: the angle inside the triangle at a vertex. Median: the segment from a vertex to the midpoint of the opposite side. Isosceles triangle: a triangle with (at least) two equal sides. Right triangle: a triangle with one 90-degree angle. Parallel lines: lines in a plane that never meet.",
 "Triangle: three non-collinear points together with the segments joining them. Interior angle: the angle inside the triangle at a vertex. Median: the segment from a vertex to the midpoint of the opposite side. Isosceles triangle: a triangle with (at least) two equal sides. Right triangle: a triangle with one 90-degree angle. Parallel lines: lines in a plane that never meet.",
 False, "unchanged"),
("K109", "(definition)",
 "Perfect square: an integer of the form m^2 for some integer m.",
 "Perfect square: an integer of the form m^2 for some integer m.",
 False, "unchanged"),
("K110", "(definition)",
 "Probability (finite, equally likely outcomes): the probability of an event is the number of favorable outcomes divided by the number of total outcomes.",
 "Probability (finite, equally likely outcomes): the probability of an event is the number of favorable outcomes divided by the number of total outcomes.",
 False, "unchanged"),
("K201", "(theorem)",
 "Fundamental theorem of arithmetic: every integer greater than 1 is a product of prime numbers, uniquely up to order.",
 "Fundamental theorem of arithmetic: every integer greater than 1 is a product of prime numbers, uniquely up to order.",
 False, "unchanged"),
("K202", "(theorem)",
 "Euclid's lemma: if p is a prime number and p divides the product a * b, then p divides a or p divides b.",
 "Euclid's lemma: if p is a prime number and p divides the product a * b, then p divides a or p divides b.",
 False, "unchanged"),
("K203", "(theorem)",
 "Bezout's identity: for integers a and b, there are integers x and y with a*x + b*y = gcd(a,b).",
 "Bezout's identity: for integers a and b, there are integers x and y with a*x + b*y = gcd(a,b).",
 False, "unchanged"),
("K204", "(theorem)",
 "Pigeonhole principle: if more than n items are placed into n boxes, some box contains at least 2 items.",
 "Pigeonhole principle: if more than n items are placed into n boxes, some box contains at least 2 items.",
 False, "unchanged"),
("K205", "(theorem)",
 "Pythagorean theorem: in a right triangle with legs a, b and hypotenuse c, a^2 + b^2 = c^2.",
 "Pythagorean theorem: in a right triangle with legs a, b and hypotenuse c, a^2 + b^2 = c^2.",
 False, "unchanged"),
("K206", "(theorem)",
 "There are infinitely many prime numbers.",
 "There are infinitely many prime numbers.",
 False, "unchanged"),
("K207", "(theorem)",
 "Algebraic identities: (a+b)^2 = a^2+2ab+b^2; (a-b)^2 = a^2-2ab+b^2; a^2-b^2 = (a-b)(a+b), for all real numbers a and b.",
 "Algebraic identities: (a+b)^2 = a^2+2ab+b^2; (a-b)^2 = a^2-2ab+b^2; a^2-b^2 = (a-b)(a+b), for all real numbers a and b.",
 False, "unchanged"),
("K208", "(theorem)",
 "Vertical angles are equal. If a transversal cuts two parallel lines, alternate interior angles are equal.",
 "Vertical angles are equal. If a transversal cuts two parallel lines, alternate interior angles are equal.",
 False, "unchanged"),
("K209", "(theorem)",
 "Triangle congruence criteria: SAS, ASA, SSS. (If two triangles satisfy any one of these criteria, all corresponding sides and angles are equal.)",
 "Triangle congruence criteria: SAS, ASA, SSS. (If two triangles satisfy any one of these criteria, all corresponding sides and angles are equal.)",
 False, "unchanged"),
("K210", "(theorem)",
 "Midpoint theorem: the segment joining the midpoints of two sides of a triangle is parallel to the third side and half its length.",
 "Midpoint theorem: the segment joining the midpoints of two sides of a triangle is parallel to the third side and half its length.",
 False, "unchanged"),
]

STORE_KEYS = [k for (k, _, _, _, _, _) in AUDIT]

def r4_store_text():
    parts = ["# KNOWLEDGE_STORE_NL - MATH R4 (raw-NL rendering)",
             "# Revised from the R3 store; see KNOWLEDGE_AUDIT_R3_R4.md for the wording audit.",
             ""]
    for (k, tag, _r3, r4, _c, _n) in AUDIT:
        parts.append("[%s] %s" % (k, tag))
        parts.append(r4)
        parts.append("")
    return "\n".join(parts)

def r3_store_text():
    parts = []
    for (k, tag, r3, _r4, _c, _n) in AUDIT:
        parts.append("[%s] %s" % (k, tag))
        parts.append(r3)
        parts.append("")
    return "\n".join(parts)

def changed_keys():
    return [k for (k, _, _, _, c, _) in AUDIT if c]
