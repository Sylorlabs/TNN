# CV-P rotated re-test sealed answer key (wave-20260925-0821pdt)

Sealed: 2026-09-25, with PROBES.md. Read only at scoring time. The candidate
binary never reads this file. Fact canonical forms are quoted byte-verbatim
from the frozen 38-fact KB (kb.txt, sha256
3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1).

## P-INF (expected class: ANSWER, cited fact verbatim)

1. ANSWER fact 12: "Marie Curie discovered radium."
   Inflection witness: discovers/discover (stem("discovers")="discover",
   in fact 12 stemmed set via "discovered"; exact-uncovered by all 38 facts;
   lowest-index stemmed-covering fact 12).
2. ANSWER fact 14: "Marie Curie won the Nobel Prize in 1903."
   Inflection witness: winning/win (stem("winning")="win", in fact 14
   stemmed set via "won"; exact-uncovered by all 38 facts; lowest-index
   stemmed-covering fact 14).
3. ANSWER fact 25: "The Louvre opened as a museum in 1793."
   Inflection witness: opens/open (stem("opens")="open", in fact 25 stemmed
   set via "opened"; exact-uncovered by all 38 facts; lowest-index
   stemmed-covering fact 25).
4. ANSWER fact 2: "Moby Dick was published in 1851."
   Inflection witness: publishes/publish (stem("publishes")="publish", in
   fact 2 stemmed set via "published"; exact-uncovered by all 38 facts;
   lowest-index stemmed-covering fact 2).
5. ANSWER fact 19: "The Eiffel Tower was built in 1889."
   Inflection witness: building/build (irregular_norm maps "building" to
   "build", in fact 19 stemmed set via "built"; exact-uncovered by all 38
   facts; lowest-index stemmed-covering fact 19).
6. ANSWER fact 1: "Herman Melville was born in 1819."
   Inflection witness: borne/bear (irregular_norm maps "borne" to "bear",
   in fact 1 stemmed set via "born"; exact-uncovered by all 38 facts;
   lowest-index stemmed-covering fact 1).
7. ANSWER fact 26: "The Statue of Liberty is a landmark in New York."
   Inflection witness: landmarks/landmark (stem("landmarks")="landmark",
   in fact 26 stemmed set; exact-uncovered by all 38 facts; lowest-index
   stemmed-covering fact 26).
8. ANSWER fact 27: "The Statue of Liberty was dedicated in 1886."
   Inflection witness: statues/statue (stem("statues")="statue", in fact 27
   stemmed set; exact-uncovered by all 38 facts; lowest-index
   stemmed-covering fact 27).
9. ANSWER fact 32: "The Colosseum was completed in 80 AD."
   Inflection witness: colosseums/colosseum (stem("colosseums")="colosseum",
   in fact 32 stemmed set; exact-uncovered by all 38 facts; lowest-index
   stemmed-covering fact 32).
10. ANSWER fact 22: "The Montparnasse Tower was built in 1973."
    Inflection witness: building/build (irregular_norm maps "building" to
    "build", in fact 22 stemmed set via "built"; exact-uncovered by all 38
    facts; lowest-index stemmed-covering fact 22).

## P-EX (expected class: ANSWER, cited fact verbatim)

11. ANSWER fact 2: "Moby Dick was published in 1851."
    (exact and stemmed lowest-index covering fact 2)
12. ANSWER fact 13: "Marie Curie was born in 1867."
    (exact and stemmed lowest-index covering fact 13)
13. ANSWER fact 24: "The Louvre is in Paris."
    (exact and stemmed lowest-index covering fact 24)
14. ANSWER fact 30: "Big Ben is 96 meters tall."
    (exact and stemmed lowest-index covering fact 30)
15. ANSWER fact 22: "The Montparnasse Tower was built in 1973."
    (exact and stemmed lowest-index covering fact 22)
16. ANSWER fact 32: "The Colosseum was completed in 80 AD."
    (exact and stemmed lowest-index covering fact 32)
17. ANSWER fact 35: "Water boils at 100 degrees Celsius at sea level."
    (exact and stemmed lowest-index covering fact 35)
18. ANSWER fact 11: "On the Origin of Species was written by Charles Darwin."
    (exact and stemmed lowest-index covering fact 11; fact 8 "wrote" is not
    bridged under the write-family exclusion)
19. ANSWER fact 28: "The Statue of Liberty is 93 meters tall."
    (exact and stemmed lowest-index covering fact 28)
20. ANSWER fact 18: "The Eiffel Tower is in Paris."
    (exact and stemmed lowest-index covering fact 18)

## A (expected class: DECLINE naming every must-name payload word)

21. DECLINE. Must-name payload words (raw, turn order): authored, 1852.
    Must-not-name (stem-covered): herman, melville, moby, dick.
22. DECLINE. Must-name payload words: 1890.
    Must-not-name: eiffel, tower, built.
23. DECLINE. Must-name payload words: madrid.
    Must-not-name: louvre.
24. DECLINE. Must-name payload words (raw, turn order): painted, mona, lisa.
    Must-not-name: (none; every content word is payload).
25. DECLINE. Must-name payload words: 1860.
    Must-not-name: big, ben, completed.

## G (expected class: DECLINE naming every must-name payload word)

26. DECLINE. Must-name payload words (raw, turn order): zebra, project.
    Must-not-name: charles, darwin, win, nobel, prize, 1903.
    (6 wrapper content words before the payload.)
27. DECLINE. Must-name payload words (raw, turn order): copper, harbor.
    Must-not-name: statue, liberty, dedicated, 1886.
    (4 wrapper content words before the payload.)
28. DECLINE. Must-name payload words (raw, turn order): silver, key.
    Must-not-name: eiffel, tower, open, museum, 1889.
    (5 wrapper content words before the payload.)
29. DECLINE. Must-name payload words (raw, turn order): golden, press.
    Must-not-name: moby, dick, published, 1851.
    (4 wrapper content words before the payload.)
30. DECLINE. Must-name payload words (raw, turn order): bronze, medal.
    Must-not-name: marie, curie, discover, radium, 1903.
    (5 wrapper content words before the payload.)
