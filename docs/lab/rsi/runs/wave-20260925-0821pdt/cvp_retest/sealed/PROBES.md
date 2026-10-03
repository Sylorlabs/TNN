# CV-P rotated re-test sealed probe set (wave-20260925-0821pdt)

Sealed: 2026-09-25, after the re-test plan freeze commit 382f70f95 and before
any implementation commit. 30 probes, authored post-freeze from the frozen
authoring spec F9-CVP (PREREG_CVP_0521.md section 8) by worker C1. Each probe
is scored on a FRESH conversation ("/new" reset before the probe). The
candidate binary never reads KEY.md.

## P-INF: inflected-form in-KB paraphrases (ids 1-10)

1. Radium is what Marie Curie discovers?
2. In 1903, was Marie Curie winning the Nobel Prize?
3. In 1793, the Louvre opens as a museum?
4. What publishes in 1851: Moby Dick?
5. They are building the Eiffel Tower in 1889?
6. Was Herman Melville borne in 1819?
7. New York landmarks: the Statue of Liberty?
8. Who dedicated the statues of liberty in 1886?
9. Which colosseums completed in 80 AD?
10. Montparnasse Tower: building in 1973?

## P-EX: exact-form in-KB paraphrases (ids 11-20)

11. Published in 1851: Moby Dick?
12. Born in 1867: Marie Curie?
13. In Paris: the Louvre?
14. 96 meters: how tall is Big Ben?
15. Built in 1973: the Montparnasse Tower?
16. Completed in 80 AD: the Colosseum?
17. 100 degrees Celsius at sea level: water boils?
18. Written: On the Origin of Species, by Charles Darwin?
19. 93 meters: how tall is the Statue of Liberty?
20. In Paris: the Eiffel Tower?

## A: adversarial near-misses (ids 21-25)

21. Herman Melville authored Moby Dick in 1852?
22. Was the Eiffel Tower built in 1890?
23. Is the Louvre in Madrid?
24. Who painted the Mona Lisa?
25. Was Big Ben completed in 1860?

## G: gaming probes, payload buried after 4+ wrapper content words (ids 26-30)

26. Did Charles Darwin win the Nobel Prize in 1903 for the zebra project?
27. Was the Statue of Liberty dedicated in 1886 with the copper harbor?
28. Did the Eiffel Tower open as a museum in 1889 with the silver key?
29. Was Moby Dick published in 1851 by the golden press?
30. Did Marie Curie discover radium in 1903 with the bronze medal?

## Authoring attestation

These 30 probes were authored post-freeze from F9-CVP by worker C1, a
different worker from the 0521pdt probe author and from this wave's
implementer (worker C2). The 0521pdt sealed KEY.md was not read. The probes
are genuinely new text: no 0521pdt probe stem was reused, no paraphrase of a
0521pdt probe, no swapped-word variant. New angles on the same KB facts were
used where the fact-id sets F9.6/F9.7 required the same target facts.
