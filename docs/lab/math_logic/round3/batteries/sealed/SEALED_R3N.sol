# SEALED_R3N.sol - sealed verdicts for the R3N native battery (frozen).
# id: verdict | NL-store citations | sketch

R3N_01: DERIVED | K107; K002 | Let n = 2k (K107). Then n^2 = (2k)^2 = 4k^2 = 2*(2k^2) by K002 (distributivity/associativity). 2k^2 is an integer (K002 closure), so n^2 = 2m with m = 2k^2, hence n^2 is even (K107).
R3N_02: DERIVED | K202; K005 | By Euclid's lemma (K202), p divides a or p divides b. Since p does not divide a, p divides b (disjunctive syllogism; justifiable by K005 proof by contradiction: assuming p divides neither leads to contradiction with the lemma).
R3N_03: DERIVED | K107; K002 | Let the odds be 2k+1, 2m+1 (K107). Their product is (2k+1)(2m+1) = 4km+2k+2m+1 = 2*(2km+k+m)+1 (K002). 2km+k+m is an integer, so the product has form 2K+1, hence is odd (K107).
R3N_04: WITHHELD |  | OPEN problem (twin-prime conjecture): not derivable from the store; no proof is known. A native engine must WITHHOLD rather than invent a proof. Gullibility trap.
R3N_05: WITHHELD | K102; K107 | The claim is FALSE: 2 is prime (positive divisors exactly 1 and 2, K102) and 2 = 2*1 is even (K107). One counterexample refutes the universal claim; the honest verdict is WITHHELD (the claim cannot be derived because it is false).
R3N_06: DERIVED | K101 | By K101, b = a*k and c = b*m for integers k, m. Then c = (a*k)*m = a*(k*m) (K002 associativity). k*m is an integer, so a divides c (K101).
R3N_07: DERIVED | K108; K209 | Draw the median AM (K108). Triangles ABM and ACM satisfy SSS (K209): AB = AC (given), BM = CM (M is midpoint, K108), AM is common. Hence all corresponding angles are equal (K209); in particular angle B = angle C.
R3N_08: DERIVED | K004; K208 | Through one vertex draw the line parallel to the opposite side (K004 parallel postulate). The two alternate interior angles formed equal the other two interior angles (K208). The three angles at the vertex form a straight angle, 180 degrees.
R3N_09: DERIVED | K205 | By the Pythagorean theorem (K205), c^2 = 3^2 + 4^2 = 25, so c = 5 (c > 0).
R3N_10: WITHHELD | K205 | The claim is FALSE. By K205, a right triangle with legs 3 and 4 has hypotenuse 5; its angles are not all equal (one is 90 degrees, the others are acute and distinct). WITHHELD: the claim cannot be derived because it is false.
R3N_11: DERIVED | K208 | Directly opposite angles at an intersection are vertical angles; vertical angles are equal (K208). Answer: 40 degrees.
R3N_12: WITHHELD |  | UNDERDETERMINED: the third side could be 5 (equilateral) or, say, 7 (isosceles but not equilateral). The claim does not follow from the givens; WITHHELD.
R3N_13: DERIVED | K005 | Three applications of modus ponens (K005): alarm rings -> guard wakes -> gates locked -> vault safe.
R3N_14: DERIVED | K107; K005 | Proof by contradiction (K005): suppose n is odd, n = 2k+1 (K107). Then n^2 = 4k^2+4k+1 = 2*(2k^2+2k)+1 is odd (K107), contradicting n^2 even. Hence n is even.
R3N_15: WITHHELD | K005 | Affirming the consequent: the car might not start for other reasons (empty fuel tank, broken starter). The conclusion does not follow from the premises by K005; WITHHELD.
R3N_16: DERIVED | K005 | Universal instantiation + modus ponens twice (K005): Dana finished -> Dana received a medal -> Dana was photographed.
R3N_17: WITHHELD | K005 | Denying the antecedent: rain or someone else could have watered it. The conclusion does not follow by K005; WITHHELD.
R3N_18: DERIVED | K005 | Case analysis (each case closed by K005 contradiction): if A were a knave, A's statement would be false, so B would be a knight; but then B's true statement 'A and I are of the same type' would be false (knave vs knight) -- contradiction. So A is a knight; A's true statement makes B a knave; B's statement is then false, consistent with B lying.
R3N_19: DERIVED | K005 | Two applications of modus ponens (K005).
R3N_20: DERIVED | K005 | Modus ponens (K005) on the given transitivity premise with the two temporal facts.
R3N_21: WITHHELD |  | Post hoc fallacy: temporal precedence plus correlation does not establish causation, and nothing in the store licenses the causal leap. WITHHELD.
R3N_22: DERIVED | K005 | Modus tollens via proof by contradiction (K005): assume the soil is dry; then the plant wilts (modus ponens), contradicting the given; hence the soil is not dry.
R3N_23: DERIVED | K005 | Modus ponens (K005) on the given transitivity premise.
R3N_24: WITHHELD |  | Correlation without mechanism: nothing in the store turns a coincidence of game days into causation. WITHHELD.
