# GIFTED KNOWLEDGE STORE — MATH-LOGIC ROUND (frozen)
# TNN may cite any item below without proof. Everything else must be DERIVED in-trace.
# Tiering rule: gift only what a strong high-school student knows. Clever lemmas
# (Sophie Germain identity, Vieta jumping, Ramsey constructions, infinite-descent
# setups) are NOT gifted. Judgment calls are listed at the bottom.

## AXIOMS

K001 [axiom] Mathematical induction: if P(1) holds, and P(n) implies P(n+1) for every positive integer n, then P(n) holds for every positive integer n. (Infinite descent may be used as induction + contradiction; no separate gift needed.)

K002 [axiom] Real field axioms: addition and multiplication are commutative and associative; multiplication distributes over addition; 0 and 1 are the additive/multiplicative identities; every real x has an additive inverse -x; every nonzero real x has a multiplicative inverse 1/x. Division by zero is undefined.

K003 [axiom] Order axioms: for reals, exactly one of x > 0, x = 0, x < 0 holds; sums and products of nonnegatives are nonnegative; x^2 >= 0 for every real x.

K004 [axiom] Euclid's postulates: (1) a straight line segment can be drawn joining any two points; (2) any segment can be extended indefinitely; (3) a circle can be drawn with any center and radius; (4) all right angles are congruent; (5) parallel postulate: given a line and a point not on it, exactly one line through the point is parallel to the given line.

K005 [axiom] Rules of inference: modus ponens (from P and P=>Q, infer Q); proof by contradiction (if assuming NOT-P leads to a contradiction, infer P).

## DEFINITIONS

K101 [definition] Divisibility: for integers a, b with a != 0, a divides b (a|b) iff there exists an integer c with b = a*c.

K102 [definition] Prime: an integer p > 1 whose only positive divisors are 1 and p.

K103 [definition] Composite: an integer n > 1 that is not prime.

K104 [definition] Congruence: for positive integer n, a ≡ b (mod n) iff n divides (a - b).

K105 [definition] Rational: a real number expressible as p/q with integers p, q != 0. Irrational: a real number that is not rational.

K106 [definition] Factorial: 0! = 1, n! = n*(n-1)! for n >= 1. Binomial coefficient: C(n,k) = n!/(k!*(n-k)!) for integers 0 <= k <= n.

K107 [definition] Even: integer n = 2k for some integer k. Odd: integer n = 2k+1 for some integer k.

K108 [definition] Triangle: three non-collinear points and the segments joining them. Interior angle: the angle inside the triangle at a vertex. Median: segment from a vertex to the midpoint of the opposite side. Isosceles: triangle with (at least) two equal sides. Right triangle: triangle with one 90-degree angle. Parallel lines: lines in a plane that never meet.

K109 [definition] Perfect square: an integer of the form m^2 for integer m.

K110 [definition] Probability (finite, equally likely outcomes): P(event) = (number of favorable outcomes)/(number of total outcomes).

## THEOREMS (may be cited without proof)

K201 [theorem] Fundamental theorem of arithmetic: every integer > 1 is a product of primes, uniquely up to order.

K202 [theorem] Euclid's lemma: if p is prime and p divides a*b, then p divides a or p divides b.

K203 [theorem] Bezout's identity: for integers a, b, there exist integers x, y with a*x + b*y = gcd(a,b).

K204 [theorem] Pigeonhole principle: if more than n items are placed into n boxes, some box contains at least 2 items.

K205 [theorem] Pythagorean theorem: in a right triangle with legs a, b and hypotenuse c, a^2 + b^2 = c^2.

K206 [theorem] There are infinitely many prime numbers.

K207 [theorem] Algebraic identities: (a+b)^2 = a^2+2ab+b^2; (a-b)^2 = a^2-2ab+b^2; a^2-b^2 = (a-b)(a+b), for all reals a, b.

K208 [theorem] Vertical angles are equal. If a transversal cuts two parallel lines, alternate interior angles are equal.

K209 [theorem] Triangle congruence criteria: SAS, ASA, SSS. (If two triangles satisfy any one criterion, all corresponding sides and angles are equal.)

K210 [theorem] Midpoint theorem: the segment joining the midpoints of two sides of a triangle is parallel to the third side and half its length.

## JUDGMENT CALLS (documented)
- J1: AM-GM is NOT gifted (P08 must derive the 2-variable case from K002/K003/K207).
- J2: The binomial theorem is NOT gifted (P13 must derive the sum identity, e.g., via Pascal's rule derived from K106, or combinatorially).
- J3: The Sophie Germain identity is NOT gifted (P06 must discover the factorization).
- J4: Vieta jumping is NOT gifted (P09).
- J5: K210 (midpoint theorem) IS gifted to keep P16 tractable; the concurrency argument itself must be derived.
- J6: K209 (congruence criteria) IS gifted; P17/P18 still require real work (Euclid I.5 chain / spotting the exterior-point flaw).
- J7: K110 (elementary probability) IS gifted; all conditional reasoning in P21 must be derived.
- J8: "0.999... denotes the limit of 0.9, 0.99, ..." — the standard high-school manipulation in P19's sketch is acceptable; graders accept it.
