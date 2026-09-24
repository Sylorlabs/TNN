#!/usr/bin/env python3
"""RT1 attack corpus generator. Writes frozen TSVs: id \\t claim \\t evidence \\t oracle.
Evidence props are ';'-separated. Oracle: 0=NEUTRAL, 1=AFFIRM, 2=DENY (ignored by engine)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- RT-A: accept-invalid (attacked direction = AFFIRM) ----------------
# Oracle is 0 (NEUTRAL) throughout: the engine must NOT affirm any of these.
RT_A = [
 # A1. Hedged claim over-affirmed via CAUSE (hedge must stay inert; r_cau_affirm has no maybe-guard on claim)
 ("RTA-001","MAYBE(BLOOM(orchid))","CAUSE(RAIN(),MAYBE(BLOOM(orchid)))",0),
 ("RTA-002","MAYBE(SINGS(lark,dawn))","CAUSE(SUNRISE(),MAYBE(SINGS(lark,dawn)))",0),
 ("RTA-003","MAYBE(NOT(FROST(ground)))","CAUSE(WIND(),MAYBE(NOT(FROST(ground))))",0),
 ("RTA-004","MAYBE(QTY(grain,exactly,40))","CAUSE(HARVEST(),MAYBE(QTY(grain,exactly,40)))",0),
 ("RTA-005","MAYBE(ALL(bees,FORAGE(bees)))","CAUSE(SPRING(),MAYBE(ALL(bees,FORAGE(bees))))",0),
 ("RTA-006","MAYBE(BEFORE(tide,moonrise))","CAUSE(GRAVITY(),MAYBE(BEFORE(tide,moonrise)))",0),
 ("RTA-007","MAYBE(CAUSE(SPARK(),FIRE()))","CAUSE(DRY(),MAYBE(CAUSE(SPARK(),FIRE())))",0),
 # A2. Range-mismatch affirmation via inverted ranges (engine accepts lo>hi; empty interval must not affirm)
 ("RTA-008","QTY(pebbles,range,22,33)","QTY(pebbles,range,33,22)",0),
 ("RTA-009","QTY(pebbles,range,twenty_two,thirty_three)","QTY(pebbles,range,thirty_three_to_twenty_two)",0),
 ("RTA-010","QTY(pebbles,range,22_to_33)","QTY(pebbles,range,between_33_and_22)",0),
 ("RTA-011","QTY(river,at_least,20)","QTY(river,range,33,22)",0),
 ("RTA-012","QTY(river,at_most,40)","QTY(river,range,33,22)",0),
 ("RTA-013","QTY(lake,range,10,50)","QTY(lake,range,50,10)",0),
 ("RTA-014","QTY(lake,more_than,5)","QTY(lake,range,50,10)",0),
 ("RTA-015","QTY(pond,exactly,30)","QTY(pond,range,50,10)",0),
 # A3. Trailing-garbage identity (parser silently drops trailing tokens after a complete prop)
 ("RTA-016","GLOWS(lantern) brightly","GLOWS(lantern)",0),
 ("RTA-017","GLOWS(lantern) brightly","GLOWS(lantern) dimly",0),
 ("RTA-018","DRIFTS(cloud) northward fast","DRIFTS(cloud)",0),
 ("RTA-019","BEFORE(sunrise,dewfall) allegedly","BEFORE(sunrise,dewfall)",0),
 ("RTA-020","QTY(stars,exactly,7) visible","QTY(stars,exactly,7)",0),
 ("RTA-021","IF(STORM(),FLOOD()) reportedly","IF(STORM(),FLOOD())",0),
 ("RTA-022","CAUSE(SEED(),SPROUT()) naturally","CAUSE(SEED(),SPROUT())",0),
 ("RTA-023","NOT(WILT(fern)) yet","NOT(WILT(fern))",0),
 ("RTA-024","SOME(ants,CARRY(ants)) mostly","SOME(ants,CARRY(ants))",0),
 # A4. Affirming the consequent (claim = antecedent; evidence has IF(a,b) + b but not a)
 ("RTA-025","THAW()","IF(THAW(),MELTS(snow));MELTS(snow)",0),
 ("RTA-026","MOIST()","IF(MOIST(),RUSTS(iron));IF(SALT(),RUSTS(iron));RUSTS(iron)",0),
 ("RTA-027","HATCHES(chick)","IF(WARMTH(),HATCHES(chick));SHELLS()",0),
 # A5. Denying the antecedent
 ("RTA-028","NOT(FREEZES(lake))","IF(FROST(),FREEZES(lake));NOT(FROST())",0),
 ("RTA-029","NOT(SPROUTS(acorn))","IF(RAIN(),SPROUTS(acorn));NOT(RAIN())",0),
 # A6. Correlation-as-causation (co-occurrence must not install CAUSE)
 ("RTA-030","CAUSE(CROWS(rooster),SUNRISE())","CROWS(rooster);SUNRISE()",0),
 ("RTA-031","CAUSE(CHIRPS(cricket),DUSK())","CHIRPS(cricket);DUSK();NIGHT()",0),
 ("RTA-032","CAUSE(BLOOMS(cactus),RAINS(desert))","BLOOMS(cactus);RAINS(desert)",0),
 # A7. Scope-shifted negation (no antonym knowledge: different predicates stay NEUTRAL)
 ("RTA-033","INNOCENT(fox)","NOT(GUILTY(fox))",0),
 ("RTA-034","SOBER(owl)","NOT(DRUNK(owl))",0),
 ("RTA-035","PRESENT(wren)","NOT(ABSENT(wren))",0),
 # A8. Hedged claim, plain over-affirmation attempts
 ("RTA-036","MAYBE(GLOWS(lantern))","GLOWS(lantern)",0),
 ("RTA-037","GLOWS(lantern)","MAYBE(GLOWS(lantern))",0),
 ("RTA-038","MAYBE(GLOWS(lantern))","MAYBE(GLOWS(lantern))",0),
 # A9. Conditional consequent asserted as fact (IF alone must not affirm)
 ("RTA-039","FLOODS(valley)","IF(BURSTS(dam),FLOODS(valley))",0),
 ("RTA-040","WILTS(rose)","IF(DROUGHT(),WILTS(rose))",0),
 ("RTA-041","SNEEZES(bear)","IF(POLLEN(),SNEEZES(bear))",0),
 # A10. Vacuous-cause attempts (NOT/MAYBE/IF reasons must never affirm)
 ("RTA-042","COOLS(breeze)","CAUSE(NOT(HUMID()),COOLS(breeze))",0),
 ("RTA-043","COOLS(breeze)","CAUSE(MAYBE(HUMID()),COOLS(breeze))",0),
 ("RTA-044","COOLS(breeze)","CAUSE(IF(DAWN(),HUMID()),COOLS(breeze))",0),
 # A11. Hedge-inertness violation in the DENY direction (documented anomaly; not a K-RTA AFFIRM hit)
 ("RTA-045","MAYBE(GLOWS(lantern))","CAUSE(RAIN(),NOT(MAYBE(GLOWS(lantern))))",0),
]

# ---------------- RT-B: reject-valid (the v3 failure mode) ----------------
RT_B = [
 # B1. Valid modus ponens
 ("RTB-001","MELTS(snow)","IF(THAW(),MELTS(snow));THAW()",1),
 ("RTB-002","RIPENS(fig)","IF(SUN(),RIPENS(fig));HEAT();SUN()",1),
 ("RTB-003","WILTS(rose)","DROUGHT();IF(DROUGHT(),WILTS(rose))",1),
 ("RTB-004","HATCHES(chick)","IF(WARMTH(),HATCHES(chick));SHELLS();WARMTH()",1),
 ("RTB-005","IF(RAIN(),BLOOMS(tulip))","IF(SPRING(),IF(RAIN(),BLOOMS(tulip)));SPRING()",1),
 ("RTB-006","GROWS(moss)","IF(SHADE(),GROWS(moss));NOT(NOT(SHADE()))",1),
 ("RTB-007","FALLS(leaf)","IF(WIND(),FALLS(leaf));IF(WIND(),FALLS(leaf));WIND()",1),
 ("RTB-008","HATCHES(chick)","IF(WARMTH(),HATCHES(chick));WARMTH();NOT(WARMTH())",1),
 # B2. True causal AFFIRM
 ("RTB-009","FLOODS(valley)","CAUSE(BURSTS(dam),FLOODS(valley))",1),
 ("RTB-010","RUSTS(hinge)","CAUSE(MOIST(air),RUSTS(hinge))",1),
 ("RTB-011","SINGS(thrush)","CAUSE(DAWN(),SINGS(thrush))",1),
 ("RTB-012","GROWS(moss)","CAUSE(ALL(rocks,DAMP(rocks)),GROWS(moss))",1),
 ("RTB-013","CALMS(sea)","CAUSE(BEFORE(storm,dawn),CALMS(sea))",1),
 ("RTB-014","WAKES(bear)","CAUSE(CAUSE(SPRING(),THAW()),WAKES(bear))",1),
 ("RTB-015","DRIFTS(cloud)","CAUSE(NOT(NOT(WIND())),DRIFTS(cloud))",1),
 ("RTB-016","COOLS(evening)","CAUSE(QTY(rain,at_least,five),COOLS(evening))",1),
 # B3. Correct negation DENY
 ("RTB-017","POURS(rain)","NOT(POURS(rain))",2),
 ("RTB-018","NOT(POURS(rain))","POURS(rain)",2),
 ("RTB-019","POURS(rain)","NOT(NOT(NOT(POURS(rain))))",2),
 ("RTB-020","AFTER(dusk,dawn)","NOT(BEFORE(dawn,dusk))",2),
 ("RTB-021","CAUSE(SPARK(),FIRE())","NOT(SPARK())",2),
 ("RTB-022","CAUSE(SPARK(),FIRE())","NOT(FIRE())",2),
 ("RTB-023","CAUSE(SPARK(),FIRE())","CAUSE(SPARK(),NOT(FIRE()))",2),
 # B4. Correct contrastive DENY
 ("RTB-024","BEFORE(sunrise,dewfall)","AFTER(sunrise,dewfall)",2),
 ("RTB-025","AFTER(harvest,frost)","BEFORE(harvest,frost)",2),
 ("RTB-026","BEFORE(first_light,birdsong)","BEFORE(birdsong,first_light)",2),
 ("RTB-027","ALL(swallows,RETURN(swallows))","SOME(swallows,NOT(RETURN(swallows)))",2),
 ("RTB-028","NONE(frost,BITES(frost))","SOME(frost,BITES(frost))",2),
 ("RTB-029","ALL(geese,FLY(geese))","NONE(geese,FLY(geese))",2),
 # B5. Quantifier polarity gap: ALL(d,NOT P) vs NONE(d,NOT P) is a genuine contradiction
 ("RTB-030","ALL(moths,NOT(SEEK(moths,flame)))","NONE(moths,NOT(SEEK(moths,flame)))",2),
 ("RTB-031","NONE(moths,NOT(SEEK(moths,flame)))","ALL(moths,NOT(SEEK(moths,flame)))",2),
 ("RTB-032","ALL(crickets,NOT(SILENT(crickets)))","NONE(crickets,NOT(SILENT(crickets)))",2),
 ("RTB-033","NONE(crickets,NOT(SILENT(crickets)))","ALL(crickets,NOT(SILENT(crickets)))",2),
 # B6. Double-negation elimination
 ("RTB-034","POURS(rain)","NOT(NOT(POURS(rain)))",1),
 ("RTB-035","NOT(POURS(rain))","NOT(NOT(NOT(POURS(rain))))",1),
 ("RTB-036","GLOWS(lantern)","NOT(NOT(NOT(NOT(GLOWS(lantern)))))",1),
 ("RTB-037","CAUSE(SPARK(),FIRE())","NOT(NOT(CAUSE(SPARK(),FIRE())))",1),
 # B7. QTY subset AFFIRM
 ("RTB-038","QTY(pebbles,range,22,33)","QTY(pebbles,exactly,25)",1),
 ("RTB-039","QTY(pebbles,range,twenty_two,thirty_three)","QTY(pebbles,exactly,twenty_five)",1),
 ("RTB-040","QTY(pond,range,22,33)","QTY(pond,exactly,25)",1),
 ("RTB-041","QTY(brew,at_least,one_min)","QTY(brew,exactly,90,sec)",1),
 ("RTB-042","QTY(brew,at_least,two_min)","QTY(brew,exactly,90,sec)",2),
 ("RTB-043","QTY(siege,less_than,5)","QTY(siege,at_most,4)",1),
 ("RTB-044","QTY(siege,at_least,5)","QTY(siege,more_than,5)",1),
 # B8. QTY disjoint DENY
 ("RTB-045","QTY(pebbles,exactly,5)","QTY(pebbles,range,22,33)",2),
 ("RTB-046","QTY(pebbles,more_than,5)","QTY(pebbles,exactly,5)",2),
 ("RTB-047","QTY(voyage,exactly,three_day)","QTY(voyage,at_least,four_week)",2),
 ("RTB-048","QTY(pebbles,exactly,twenty_five)","QTY(pebbles,range,thirty_three,forty)",2),
 # B9. 8-evidence-prop cap: valid logic in the 9th slot is silently dropped (boundary; flagged in report)
 ("RTB-049","GROWS(moss)","IF(SHADE(),GROWS(moss));F1();F2();F3();F4();F5();F6();F7();SHADE()",1),
 ("RTB-050","HUMS(hive)","F1();F2();F3();F4();F5();F6();F7();F8();HUMS(hive)",1),
 ("RTB-051","DRIFTS(cloud)","IF(WIND(),DRIFTS(cloud));F1();F2();F3();F4();F5();F6();F7();WIND()",1),
]

def write(path, rows):
    with open(path, "w") as f:
        for rid, claim, ev, oracle in rows:
            assert "\t" not in claim and "\t" not in ev, rid
            f.write(f"{rid}\t{claim}\t{ev}\t{oracle}\n")

write(os.path.join(HERE, "rt_a.tsv"), RT_A)
write(os.path.join(HERE, "rt_b.tsv"), RT_B)
print(f"wrote {len(RT_A)} RT-A + {len(RT_B)} RT-B items")
