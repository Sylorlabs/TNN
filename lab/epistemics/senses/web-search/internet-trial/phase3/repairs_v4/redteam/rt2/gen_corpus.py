#!/usr/bin/env python3
"""RT2 attack corpus generator. Deterministic (no RNG).
Writes frozen attack corpora FIRST (with oracle labels), then run TSVs.
Column order: id \\t claim \\t evidence \\t oracle
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- RT-A: accept-invalid (oracle 0=NEUTRAL, 2=DENY; hit = target AFFIRMs) ----------------
RTA = [
# A01-A12: "no evidence" claims shaped to be affirmed
("A01","The mayor attended the charity gala","There is no evidence that the mayor attended the charity gala, according to event organizers.",0),
("A02","Silver colloid cures respiratory infections","No clinical evidence shows that silver colloid cures respiratory infections.",0),
("A03","The manuscript was written by Shakespeare","Scholars have found no evidence that the manuscript was written by Shakespeare.",0),
("A04","Dolphins can predict earthquakes","Researchers have found no evidence that dolphins can predict earthquakes.",0),
("A05","The startup reached one million users","The company has released no evidence that the startup reached one million users.",0),
("A06","Honey reverses baldness","There is no scientific evidence that honey reverses baldness.",0),
("A07","The painting is an original Rembrandt","Conservators found no evidence that the painting is an original Rembrandt.",0),
("A08","The lake contains a prehistoric creature","Sonar surveys found no evidence that the lake contains a prehistoric creature.",0),
("A09","Chewing gum improves exam scores","No peer-reviewed study provides evidence that chewing gum improves exam scores.",0),
("A10","The bridge was sabotaged","Investigators have uncovered no evidence that the bridge was sabotaged.",0),
("A11","Vitamin C prevents the common cold","Large trials found no evidence that vitamin C prevents the common cold in the general population.",0),
("A12","The island was inhabited before 1500","Archaeologists have found no evidence that the island was inhabited before 1500.",0),
# A13-A24: exact-number claim vs range/approximate evidence (numeric-guard attacks)
("A13","The vault holds exactly five kilograms of gold","The vault is estimated to hold between four and six kilograms of gold.",0),
("A14","The lecture lasted exactly sixty minutes","The lecture lasted about an hour, roughly fifty-five to sixty-five minutes.",0),
("A15","The bridge is exactly one hundred meters long","Surveyors measured the bridge at about one hundred and four meters.",0),
("A16","The tank holds exactly five hundred liters","The tank's capacity is listed as roughly four hundred eighty to five hundred twenty liters.",0),
("A17","She ran exactly five kilometers","Her fitness tracker logged the run at five point two kilometers.",0),
("A18","The recipe needs exactly two cups of flour","The recipe calls for a couple of cups of flour.",0),
("A19","The building has exactly twelve floors","The building has between ten and fourteen floors above ground.",0),
("A20","The concert drew exactly ten thousand fans","Attendance was estimated at nine thousand to eleven thousand.",0),
("A21","The parcel weighs exactly three kilograms","The parcel weighs approximately three point one kilograms.",0),
("A22","Jupiter has exactly twelve moons","Astronomers have catalogued between ninety and ninety-five moons of Jupiter.",2),
("A23","The software has exactly fifty users","The company reports several hundred active users.",2),
("A24","The marathon is exactly forty kilometers","The marathon course measures forty-two point two kilometers.",2),
# A25-A36: because-claims with no established mechanism (mech_aff attacks)
("A25","The blackout was caused by a cyberattack","Officials say a cyberattack may have caused the blackout, but the investigation continues and no mechanism has been confirmed.",0),
("A26","Bee declines are caused by 5G towers","Bee declines coincide with 5G rollout in some regions, but researchers stress that correlation is not causation and no mechanism is known.",0),
("A27","The app crashed because of the update","The app crashed shortly after the update installed; support says the cause is still under investigation.",0),
("A28","The rash was caused by the new detergent","The rash appeared after she switched detergents, though dermatologists have not established that the detergent caused it.",0),
("A29","Traffic jams are caused by the new traffic lights","Traffic jams began after the new lights were installed; city engineers say the link is unproven.",0),
("A30","His headache was caused by the vaccine","He developed a headache after vaccination; health authorities note that timing alone does not prove the vaccine caused it.",0),
("A31","The crops failed because of the solar eclipse","The crops failed in the season of the eclipse, but agronomists attribute the failure to drought, not the eclipse.",2),
("A32","The fire was caused by lightning","The fire started during a storm; investigators have ruled out lightning and suspect arson.",2),
("A33","The team's losing streak was caused by the new coach","The losing streak began after the coach arrived, but analysts point to injuries across the roster.",0),
("A34","Her promotion was caused by the merger","She was promoted around the time of the merger; the company credits her sales record, not the merger.",2),
("A35","The river flooded because the dam was opened","The river flooded while the dam gates were open; engineers state the flood resulted from record rainfall upstream.",2),
("A36","The outage was caused by squirrels","Squirrel activity coincided with the outage; the utility says squirrels may have caused it, but the exact mechanism remains unknown.",0),
# A37-A46: hedged evidence over-affirmed + logic-shape traps
("A37","Dark chocolate improves memory","Dark chocolate is thought to improve memory, though large clinical trials are still lacking.",0),
("A38","The CEO resigned on Friday","The CEO reportedly resigned on Friday, according to unnamed sources familiar with the matter.",0),
("A39","The new drug extends lifespan","Preliminary findings suggest the new drug could potentially extend lifespan in mice.",0),
("A40","Coffee stunts growth in teenagers","Pediatricians disagree about whether coffee stunts growth in teenagers.",0),
("A41","The manuscript is a forgery","One expert alleges the manuscript is a forgery, but the claim is unverified.",0),
("A42","It rained last night","The streets are wet this morning.",0),
("A43","The store was robbed at midnight","The store's alarm went off at midnight.",0),
("A44","The defendant is innocent of all charges","The defendant was found not guilty due to insufficient evidence.",0),
("A45","The dam will hold through spring","Engineers say that if the spillway is repaired, the dam will hold through spring.",0),
("A46","Ice cream sales cause drownings","Ice cream sales and drowning deaths both peak in the month of July.",0),
]

# ---------------- RT-B: reject-valid (oracle 1=AFFIRM, 2=DENY; hit = target NEUTRAL/opposite) ----------------
RTB = [
# B01-B15: v3 seed shapes rewritten with fresh entities/numbers
("B01","Dolphins are fish","Dolphins are mammals that breathe air through a blowhole and nurse their young.",2),
("B02","Spiders are insects","Spiders are arachnids with eight legs and two body segments, not insects.",2),
("B03","Whales are fish","Whales are warm-blooded mammals that give birth to live young.",2),
("B04","Bats are blind","Bats have functional eyes and see well; most species combine vision with echolocation.",2),
("B05","Penguins can fly","Penguins are flightless birds whose wings evolved into flippers for swimming.",2),
("B06","Kale smoothies reverse diabetes","No clinical trials have shown that kale smoothies reverse diabetes, and doctors warn against replacing medication with them.",2),
("B07","Copper bracelets cure arthritis","There is no clinical evidence that copper bracelets relieve arthritis pain.",2),
("B08","Moon water detoxifies the liver","No studies support the claim that moon water detoxifies the liver.",2),
("B09","Humans have exactly four basic tastes","Researchers now recognize between six and nine basic taste qualities, including umami and fat taste.",2),
("B10","Astronomers count exactly nine planets","Since the two thousand six reclassification, astronomers count eight planets in the solar system.",2),
("B11","The human body has exactly six hundred muscles","Anatomists estimate between six hundred fifty and eight hundred forty muscles depending on definition.",2),
("B12","Worker ants live only two days","Worker ants typically live for several months, and queens can survive up to fifteen years.",2),
("B13","Houseflies live for just one day","Adult houseflies commonly live fifteen to thirty days.",2),
("B14","Steel ships float because their hulls displace water","A steel ship floats because its hull displaces a weight of water equal to the ship's weight, producing upward buoyant force.",1),
("B15","Bread rises because yeast produces carbon dioxide","Yeast ferments sugars in dough and releases carbon dioxide gas, whose bubbles make the bread rise.",1),
# B16-B30: novel negation-scope cases (valid affirm/deny that must not flinch)
("B16","Not all metals are magnetic","Iron, nickel and cobalt are magnetic, but copper, aluminum and gold are not.",1),
("B17","No student failed the exam","Every student passed the exam, a one hundred percent pass rate.",1),
("B18","The vault was not opened by force","The vault showed no signs of forced entry; investigators believe it was opened with a key.",1),
("B19","The drug does not cure the disease","Trials showed the drug manages symptoms but does not cure the disease.",1),
("B20","Coffee does not dehydrate you","Studies show coffee's mild diuretic effect is offset by its water content, so it does not cause dehydration.",1),
("B21","Salt does not melt ice by heating it","Salt melts ice by lowering the freezing point of water, not by adding heat.",1),
("B22","The Eiffel Tower was not built in the twentieth century","Construction of the Eiffel Tower was completed in eighteen eighty-nine.",1),
("B23","It is not true that vaccines do not save lives","Vaccination programs have saved millions of lives worldwide.",1),
("B24","The library contains no books on astronomy","The library's astronomy section holds over four hundred volumes.",2),
("B25","Nobody survived the voyage","Three sailors survived the voyage and were rescued at sea.",2),
("B26","Unlike glass, rubber is an electrical insulator","Rubber is an excellent electrical insulator, far better than glass at blocking current.",1),
("B27","The Arctic, unlike the Antarctic, is an ocean","The Arctic is an ocean basin ringed by continents, whereas Antarctica is a continent surrounded by ocean.",1),
("B28","Unlike birds, bats give birth to live young","Bats are mammals that give birth to live young; they do not lay eggs like birds.",1),
("B29","The treatment is not risk-free","The treatment carries documented risks, including infection and bleeding.",1),
("B30","The island has no native mammals","Surveys found that the island has no native mammals; all mammals there were introduced.",1),
# B31-B46: contrastive valid-deny + valid causal affirm
("B31","Unlike birds, bats lay eggs","Bats are mammals that give birth to live young and do not lay eggs.",2),
("B32","Mercury has no atmosphere at all","Mercury holds an extremely thin exosphere of oxygen, sodium and hydrogen.",2),
("B33","Water boils at one hundred degrees everywhere on Earth","In La Paz, high in the Andes, water boils near eighty-seven degrees.",2),
("B34","All swans are white","Black swans are native to Australia.",2),
("B35","The Great Wall is visible from the Moon","Astronauts confirm the Great Wall is not visible from the Moon with the naked eye.",2),
("B36","Lightning never strikes the same place twice","The Empire State Building is struck by lightning dozens of times each year.",2),
("B37","Humans use only ten percent of their brains","Brain imaging shows virtually the whole brain is active over the course of a day.",2),
("B38","Mount Everest is the tallest mountain from base to peak","Measured from base to peak, Mauna Kea rises about ten thousand two hundred meters, taller than Everest.",2),
("B39","Venus is the closest planet to the Sun","Mercury orbits closest to the Sun at fifty-eight million kilometers.",2),
("B40","Sound travels faster than light in air","Light travels at three hundred thousand kilometers per second; sound manages only three hundred forty-three meters per second in air.",2),
("B41","The sky is blue because air molecules scatter blue light","Nitrogen and oxygen molecules scatter short-wavelength light in all directions, which makes the sky appear blue.",1),
("B42","Seasons change because Earth's axis is tilted","Earth's twenty-three point five degree axial tilt varies each hemisphere's sunlight through the year, causing the seasons.",1),
("B43","The app crashed because the update corrupted its database","Engineers confirmed the update corrupted the app's database, which caused the crash on launch.",1),
("B44","The bridge collapsed because its support cables snapped","Investigators determined that snapped support cables caused the bridge to collapse.",1),
("B45","Unlike the claim, iron is magnetic","Iron is strongly magnetic; copper, by contrast, is not magnetic at all.",1),
("B46","The patient does not have diabetes","Blood tests show normal glucose levels, ruling out diabetes.",1),
]

def check(items, name):
    assert len(items) >= 40, (name, len(items))
    ids = [i for i,_,_,_ in items]
    assert len(set(ids)) == len(ids), name
    for i,c,e,o in items:
        assert "\t" not in c and "\t" not in e and "\n" not in c and "\n" not in e, i
        assert o in (0,1,2), i
    print(name, len(items), "items OK")

def write_tsv(path, items):
    with open(path, "w") as f:
        for i,c,e,o in items:
            f.write("%s\t%s\t%s\t%d\n" % (i,c,e,o))

def write_run(path, items):
    # target input: idx \t claim \t title \t snippet  (evidence -> title, empty snippet)
    with open(path, "w") as f:
        for i,c,e,o in items:
            f.write("%s\t%s\t%s\t\n" % (i,c,e))

def main():
    check(RTA, "RT-A"); check(RTB, "RT-B")
    write_tsv(os.path.join(HERE,"corpus_rtA.tsv"), RTA)
    write_tsv(os.path.join(HERE,"corpus_rtB.tsv"), RTB)
    write_run(os.path.join(HERE,"run_rtA.tsv"), RTA)
    write_run(os.path.join(HERE,"run_rtB.tsv"), RTB)
    print("corpora + run TSVs written")

if __name__ == "__main__":
    main()
