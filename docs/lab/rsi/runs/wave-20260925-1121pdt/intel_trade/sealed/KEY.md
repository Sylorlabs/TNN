# COMP-2 sealed key (wave-20260925-1121pdt)

Sealed 2026-09-25. Expected lowest valid pair per COMP probe, and the
shared gazetteer bridge entity. Determined by the independent authoring
enumerator (pure Zag), NOT by the candidate. The candidate binary never
reads this file; the scorer is the only decision-bearing reader.

Format: Pn -> (F,G) bridge="..."

P1 -> (0,2) bridge="moby dick"
P2 -> (4,6) bridge="pride and prejudice"
P3 -> (8,10) bridge="origin species"
P4 -> (12,14) bridge="marie curie"
P5 -> (15,17) bridge="martian"
P6 -> (18,19) bridge="eiffel tower"
P7 -> (21,22) bridge="montparnasse tower"
P8 -> (24,25) bridge="louvre"
P9 -> (26,27) bridge="statue liberty"
P10 -> (29,30) bridge="big ben"
P11 -> (31,32) bridge="colosseum"
P12 -> (1,3) bridge="herman melville"
P13 -> (5,7) bridge="jane austen"
P14 -> (9,11) bridge="charles darwin"
P15 -> (13,14) bridge="marie curie"
P16 -> (18,20) bridge="eiffel tower"
P17 -> (19,20) bridge="eiffel tower"
P18 -> (22,23) bridge="montparnasse tower"
P19 -> (27,28) bridge="statue liberty"
P20 -> (2,3) bridge="moby dick"

UNANS P21-P30: no valid pair exists (enumerator output PAIRS empty).
Expected behavior: decline with the explicit no-single-fact message.
