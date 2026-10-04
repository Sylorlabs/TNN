#!/usr/bin/env python3
"""RT4b fresh blind corpus generator. Writes corpus_fresh.tsv (frozen).

Format (7 tab fields, harness-compatible with rt4fix/run_all.py):
  id \t claim \t ctype \t oracle \t r6tag \t r6proof \t rows
rows:  rid|tier|text ;; rid|tier|text ...
oracle: INSTALL (RT-B) | NONINSTALL (RT-A) | PROBE:<predicted> (calibration)

R6 tags are oracle-authored (intended tag a correct logic core would emit);
the T1 logic core is a separate track (RT1/RT1b) and was not among this
task's components. B-01..B-16 use R6=1+proof (affirm fast path);
B-17..B-32 use R6=0 (vote path: genuine support, no formal proof shape).
All RT-A items use R6=0 (fallacious support must not affirm).
Zero RNG: fully deterministic authoring.
"""
import hashlib

A = []  # invalid logic -> oracle NONINSTALL
B = []  # valid logic   -> oracle INSTALL
D = []  # calibration probes -> oracle PROBE:<predicted>

def item(iid, claim, ctype, oracle, r6tag, r6proof, rows):
    return dict(id=iid, claim=claim, ctype=ctype, oracle=oracle,
                r6tag=r6tag, r6proof=r6proof, rows=rows)

# ---------------- RT-A: invalid logic (must NOT install) ----------------
A.append(item("B4A-01", "Drinking coffee causes heart attacks.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "A long-term study found that people who drink more than four cups of coffee per day have higher rates of heart attack than non-drinkers."),
     ("r1", 1, "The study authors noted that heavy coffee drinkers in the sample also smoked at much higher rates."),
     ("r2", 0, "Cardiologists say the observed association does not establish that coffee causes heart attacks.")]))
A.append(item("B4A-02", "The street is wet because it rained.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "If it rains, the street gets wet."),
     ("r1", 2, "The street is wet this morning."),
     ("r2", 1, "The city ran street-cleaning trucks with water sprayers on this block overnight.")]))
A.append(item("B4A-03", "The new traffic law caused the drop in accidents.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "The new traffic law took effect in January, and accident counts fell 12 percent in February."),
     ("r1", 1, "February also saw record snowfall that kept many drivers off the roads."),
     ("r2", 0, "Analysts caution that one month of data cannot isolate the law's effect.")]))
A.append(item("B4A-04", "Eating ice cream causes drowning.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "Ice cream sales and drowning deaths both peak in July and August."),
     ("r1", 1, "Both trends track summer heat, when more people swim and buy cold treats.")]))
A.append(item("B4A-05", "The new fertilizer doubles wheat yields.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "A single field trial reported wheat yields roughly double the control plot after using the fertilizer."),
     ("r1", 0, "The trial has not been replicated by any independent lab."),
     ("r2", 0, "Agronomists note the trial plot also received extra irrigation.")]))
A.append(item("B4A-06", "The dam will hold against a 100-year flood.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 3, "The chief engineer's final inspection report certifies the dam against a 100-year flood event."),
     ("r1", 0, "The certification has not been peer-reviewed.")]))
A.append(item("B4A-07", "The vaccine is 100 percent effective.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "The manufacturer's press release claims 100 percent efficacy in its trial."),
     ("r1", 2, "Independent reviewers found the trial excluded high-risk groups, making the 100 percent figure unreliable.")]))
A.append(item("B4A-08", "The supplement cures arthritis.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "Researchers say the supplement might ease arthritis symptoms in some patients."),
     ("r1", 1, "No clinical trial has shown that the supplement cures arthritis.")]))
A.append(item("B4A-09", "The bridge is rated for 40-ton trucks.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "The bridge's posted rating is 25 tons maximum vehicle weight."),
     ("r1", 1, "Engineers proposed an upgrade to 40 tons but it was never funded.")]))
A.append(item("B4A-10", "The safe dosage range is 10 to 50 mg.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "The label lists a safe dosage range of 10 to 20 mg per day."),
     ("r1", 1, "Doses above 20 mg per day carry documented liver risk.")]))
A.append(item("B4A-11", "The moon is made of cheese, according to a NASA press release.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 1, "The press release states the lunar surface contains dairy-based compounds."),
     ("r1", 1, "Dairy researchers confirmed cheese-like proteins in the samples."),
     ("r2", 0, "NASA's public affairs office has no record of this release.")]))
A.append(item("B4A-12", "Scientists have proven that trees can walk to new locations overnight.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 1, "A satire site published a story about walking trees with fabricated quotes."),
     ("r1", 0, "Botanists confirm trees cannot relocate themselves.")]))
A.append(item("B4A-13", "A peer-reviewed study found that office workers photosynthesize under fluorescent lights.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 1, "The study reports measurable glucose production in office workers under fluorescent lights."),
     ("r1", 1, "Follow-up coverage repeated the photosynthesis finding uncritically."),
     ("r2", 0, "Human photosynthesis is biologically impossible.")]))
A.append(item("B4A-14", "The defendant is innocent.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "The jury found the defendant not guilty due to insufficient evidence."),
     ("r1", 1, "Legal scholars stress that not guilty is not a finding of innocence.")]))
A.append(item("B4A-15", "The patient has the flu.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "Flu patients typically develop a fever within 48 hours."),
     ("r1", 2, "The patient developed a fever last night."),
     ("r2", 1, "Blood tests are still pending; several other infections cause identical fevers.")]))
A.append(item("B4A-16", "The new policy reduced crime.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "A city report credits the new policy with a 9 percent drop in reported crime."),
     ("r1", 2, "An independent audit found reporting standards changed the same month, inflating the apparent drop."),
     ("r2", 1, "Neighborhood surveys show residents feel less safe than a year ago.")]))
A.append(item("B4A-17", "The reservoir is at full capacity.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 1, "A local blog says the reservoir looks full in recent photos."),
     ("r1", 1, "A fishing forum post from last week describes high water levels."),
     ("r2", 2, "The water authority's gauge reads 61 percent of capacity as of yesterday.")]))
A.append(item("B4A-18", "Hospital visits cause illness.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "People who visit hospitals more often are diagnosed with more illnesses."),
     ("r1", 1, "Sick people go to hospitals because they are already ill, not the reverse.")]))
A.append(item("B4A-19", "It will certainly rain tomorrow.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "The forecast gives a 40 percent chance of rain tomorrow."),
     ("r1", 0, "Morning skies are currently clear.")]))
A.append(item("B4A-20", "The startup will be profitable this year.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "The startup's CEO predicted profitability this year in an interview."),
     ("r1", 0, "The company's revenue last year was 2 million dollars."),
     ("r2", 0, "The fiscal year ends in December.")]))
A.append(item("B4A-21", "The vaccine remains stable at 40 degrees Celsius.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "Stability testing covered temperatures from 2 to 8 degrees Celsius."),
     ("r1", 1, "The manufacturer warns against storage above 25 degrees.")]))
A.append(item("B4A-22", "The car's battery is dead.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "A dead battery prevents the engine from turning over."),
     ("r1", 2, "The engine would not turn over this morning."),
     ("r2", 1, "The mechanic noted the starter motor was also faulty, which causes identical symptoms.")]))
A.append(item("B4A-23", "The national archives confirm that pigeons ran a postal service in 1840.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 1, "Archive finding aids list the pigeon post ledgers from 1840."),
     ("r1", 1, "Historians of the pigeon post cite delivery times under two hours."),
     ("r2", 0, "No archive holds any record of pigeon-employed mail carriers.")]))
A.append(item("B4A-24", "Owning a luxury car causes higher income.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "Luxury car owners report higher average incomes than other drivers."),
     ("r1", 1, "High earners buy luxury cars; the car does not create the income.")]))
A.append(item("B4A-25", "This airport is the most dangerous in the country.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "The airport recorded the highest total number of runway incidents last year."),
     ("r1", 1, "It also handled three times the traffic of any other airport; per-flight incident rates are average.")]))
A.append(item("B4A-26", "The chemical is safe for household use.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "The manufacturer's safety sheet lists the chemical as safe for household use."),
     ("r1", 3, "A peer-reviewed toxicology study found the chemical causes liver damage at household exposure levels.")]))
A.append(item("B4A-27", "The diet pill melts fat while you sleep.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "A celebrity endorser says the pill melted her fat while she slept."),
     ("r1", 1, "Regulators fined the pill's maker for unsubstantiated weight-loss claims.")]))
A.append(item("B4A-28", "The river is safe to drink from.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 1, "A hiker's review said the river water tasted clean."),
     ("r1", 2, "The county health department advises against drinking untreated river water.")]))
A.append(item("B4A-29", "The city must either build the stadium or lose all tourism.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 0, "The mayor supports building the stadium."),
     ("r1", 1, "The city's tourism grew 8 percent last year with no stadium.")]))
A.append(item("B4A-30", "Dropping out of college leads to business success.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "Three famous billionaires dropped out of college."),
     ("r1", 1, "Studies of all dropouts show far lower average lifetime earnings than graduates.")]))
A.append(item("B4A-31", "The 2024 census recorded a town in Nebraska with a population of negative twelve.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 1, "The preview tables listed negative twelve residents for the town."),
     ("r1", 1, "Local coverage quoted the negative twelve figure before the correction."),
     ("r2", 0, "The Census Bureau confirms populations cannot be negative.")]))
A.append(item("B4A-32", "The drug has no side effects.", "FACTUAL",
    "NONINSTALL", 0, "",
    [("r0", 2, "A 20-person company trial reported no side effects."),
     ("r1", 2, "A 4000-person independent trial reported side effects in 11 percent of patients.")]))

# ---------------- RT-B: valid logic (must INSTALL) ----------------
# B-01..B-16: R6=1+proof (affirm fast path)
def bfast(iid, claim, proof, rows):
    B.append(item(iid, claim, "FACTUAL", "INSTALL", 1, proof, rows))

bfast("B4B-01", "The street is wet.", "R-COND-MP: rain implies wet; rain observed",
    [("r0", 2, "If it rains, the street gets wet."), ("r1", 2, "It rained this morning.")])
bfast("B4B-02", "The switch being on caused the light to turn on.", "R-CAU-AFFIRM: mechanism plus covariation",
    [("r0", 2, "Flipping the switch closes the circuit powering the light."),
     ("r1", 2, "The light turned on immediately after the switch was flipped, and off when flipped back, repeatedly.")])
bfast("B4B-03", "The sample contains no lead.", "R-IDENT-AFFIRM: below detection limit",
    [("r0", 3, "The lab's mass spectrometry found lead levels below the detection limit in the sample."),
     ("r1", 1, "The detection limit is ten times stricter than the safety standard.")])
bfast("B4B-04", "The package weighs at most 5 kg.", "R-QTY-AFFIRM: 4.2 <= 5",
    [("r0", 2, "The certified scale read 4.2 kg for the package."),
     ("r1", 1, "The scale's calibration certificate is current.")])
bfast("B4B-05", "The plant is a cactus.", "R-COND-MP: fleshy stems plus spines implies cactus",
    [("r0", 2, "All plants with fleshy water-storing stems and spines instead of leaves are cacti."),
     ("r1", 2, "This plant has fleshy water-storing stems and spines instead of leaves.")])
bfast("B4B-06", "The antibiotic cured the infection.", "R-CAU-AFFIRM: specific killing plus recovery timing",
    [("r0", 2, "The antibiotic kills the exact bacterial strain cultured from the patient."),
     ("r1", 2, "The infection cleared three days after starting the antibiotic, after six weeks of no improvement.")])
bfast("B4B-07", "The painting is an original Vermeer.", "R-IDENT-AFFIRM: materials plus technique plus provenance",
    [("r0", 3, "Pigment analysis matches 17th-century Dutch materials and the underdrawing matches Vermeer's known technique."),
     ("r1", 1, "Provenance documents trace ownership unbroken to Vermeer's studio.")])
bfast("B4B-08", "The room temperature stayed within 20 to 22 degrees all day.", "R-QTY-AFFIRM: observed range inside claimed range",
    [("r0", 2, "The thermostat log shows readings between 20.1 and 21.8 degrees for every hour.")])
bfast("B4B-09", "The contract is void.", "R-COND-MP: duress implies void; duress found",
    [("r0", 2, "Contracts signed under duress are void."),
     ("r1", 2, "The court found the contract was signed under duress.")])
bfast("B4B-10", "The reinforced beam prevented the collapse.", "R-CAU-AFFIRM: load test contrast plus survival",
    [("r0", 2, "Load tests show the unreinforced beam fails at this load while the reinforced beam holds."),
     ("r1", 2, "The building survived the earthquake with the reinforced beams intact.")])
bfast("B4B-11", "The hard drive contains no recoverable data.", "R-IDENT-AFFIRM: triple overwrite plus failed recovery",
    [("r0", 2, "A forensic wipe overwrote every sector three times."),
     ("r1", 2, "Two independent recovery labs found zero recoverable files.")])
bfast("B4B-12", "At least 100 people attended.", "R-QTY-AFFIRM: 137 >= 100",
    [("r0", 2, "The turnstile count recorded 137 entries.")])
bfast("B4B-13", "The milk has spoiled.", "R-COND-MP: expired plus sour implies spoiled",
    [("r0", 2, "Milk past its expiration date that smells sour has spoiled."),
     ("r1", 2, "This milk is two weeks past expiration and smells sour.")])
bfast("B4B-14", "Irrigation saved the crop.", "R-CAU-AFFIRM: field contrast plus no rain",
    [("r0", 2, "The irrigated field yielded normally while the adjacent unirrigated field withered."),
     ("r1", 1, "Rainfall records show no rain during the growing period.")])
bfast("B4B-15", "The signature is the mayor's.", "R-IDENT-AFFIRM: three independent expert matches",
    [("r0", 2, "Three handwriting experts independently matched the signature to the mayor's known writing.")])
bfast("B4B-16", "The bridge clearance is at least 4 meters.", "R-QTY-AFFIRM: 4.6 >= 4",
    [("r0", 2, "The survey measured the clearance at 4.6 meters.")])

# B-17..B-32: R6=0 (vote path: genuine support, no formal proof shape)
def bvote(iid, claim, rows):
    B.append(item(iid, claim, "FACTUAL", "INSTALL", 0, "", rows))

bvote("B4B-17", "The drinking water is safe.",
    [("r0", 2, "No contaminants were detected in any of the 40 tested samples."),
     ("r1", 2, "The treatment plant's filters were all operating within specification.")])
bvote("B4B-18", "The patient does not have diabetes.",
    [("r0", 2, "The patient's fasting glucose was 85 mg per dL, well below the diabetic threshold."),
     ("r1", 2, "No diabetes markers appeared in the full blood panel.")])
bvote("B4B-19", "The software needs at least 8 GB of RAM.",
    [("r0", 2, "The installer refuses to proceed on machines with less than 8 GB of RAM."),
     ("r1", 1, "Benchmarks show the software runs on 8 GB but crashes on 4 GB.")])
bvote("B4B-20", "The fire was accidental.",
    [("r0", 2, "Investigators ruled out arson after finding no accelerants."),
     ("r1", 2, "The evidence refutes any claim of intentional ignition.")])
bvote("B4B-21", "The new highway reduced commute times.",
    [("r0", 2, "Average commute times on the corridor fell 18 percent after the highway opened."),
     ("r1", 1, "Bus ridership on parallel routes also dropped as drivers switched to the faster highway.")])
bvote("B4B-22", "The restaurant is highly rated.",
    [("r0", 1, "A local food blog gave the restaurant 4.5 out of 5 stars."),
     ("r1", 1, "Diners on a review site rate it 4.6 on average across 800 reviews.")])
bvote("B4B-23", "The dam's spillway prevented flooding downstream.",
    [("r0", 2, "The spillway diverted the record inflow away from the main channel."),
     ("r1", 2, "Downstream gauges never exceeded flood stage during the storm.")])
bvote("B4B-24", "The vaccine prevented a measles outbreak.",
    [("r0", 2, "Measles was circulating in neighboring towns all winter."),
     ("r1", 2, "The town's 98 percent vaccination rate left too few susceptible hosts for an outbreak.")])
bvote("B4B-25", "Every invoice was paid on time.",
    [("r0", 2, "The audit sampled all 200 invoices and found zero late payments."),
     ("r1", 1, "The payment system's logs show no overdue flags for the period.")])
bvote("B4B-26", "The generic drug works as well as the brand-name drug.",
    [("r0", 2, "A double-blind trial found no statistically significant difference in outcomes."),
     ("r1", 1, "Regulators certified the generic as bioequivalent.")])
bvote("B4B-27", "The response time stayed under 200 milliseconds.",
    [("r0", 2, "Load testing measured a maximum response time of 143 milliseconds."),
     ("r1", 1, "The monitoring dashboard's 99th percentile reads 161 milliseconds.")])
bvote("B4B-28", "The merger improved the company's finances.",
    [("r0", 2, "Revenue rose 22 percent in the year following the merger."),
     ("r1", 2, "Operating costs fell as duplicate departments were consolidated.")])
bvote("B4B-29", "The new policy improved air quality.",
    [("r0", 2, "Particulate levels dropped 30 percent in the year after the policy took effect."),
     ("r1", 2, "Hospital admissions for asthma fell 15 percent over the same period.")])
bvote("B4B-30", "The outage was caused by the storm, not by equipment failure.",
    [("r0", 2, "Crews found storm-toppled lines at three locations and no equipment defects."),
     ("r1", 2, "The outage began exactly when the storm front arrived.")])
bvote("B4B-31", "The archaeological site dates to the Bronze Age.",
    [("r0", 2, "Pottery shards match known Bronze Age styles."),
     ("r1", 2, "Radiocarbon dating places the charcoal layer at 1500 BCE."),
     ("r2", 0, "The site was discovered by a local farmer in 1987.")])
bvote("B4B-32", "The train arrived on schedule.",
    [("r0", 2, "The station log records arrival at 08:59 against a 09:00 schedule."),
     ("r1", 2, "Two passengers confirmed the train pulled in just before nine."),
     ("r2", 0, "One blogger complained about a delay without citing a time.")])

# ---------------- D: calibration probes (informational) ----------------
D.append(item("B4D-01", "The test was not unsuccessful.", "FACTUAL", "PROBE:WITHHOLD", 0, "",
    [("r0", 2, "The test met all its success criteria.")]))
D.append(item("B4D-02", "The outage was caused by the storm, not by sabotage.", "FACTUAL", "PROBE:INSTALL", 0, "",
    [("r0", 2, "Investigators found storm damage and no signs of sabotage."),
     ("r1", 2, "The outage coincided exactly with the storm's peak.")]))
D.append(item("B4D-03", "The jar contains at least 5 marbles.", "FACTUAL", "PROBE:INSTALL", 0, "",
    [("r0", 2, "A count found exactly 5 marbles in the jar."),
     ("r1", 1, "The jar was sealed before counting.")]))
D.append(item("B4D-04", "The drought caused the famine.", "FACTUAL", "PROBE:INSTALL", 0, "",
    [("r0", 2, "The drought destroyed the wheat harvest."),
     ("r1", 2, "With no wheat, grain reserves ran out by winter."),
     ("r2", 1, "Relief shipments did not arrive until spring.")]))
D.append(item("B4D-05", "The levee prevented the flood.", "FACTUAL", "PROBE:INSTALL", 0, "",
    [("r0", 2, "Water rose to within a foot of the levee crest."),
     ("r1", 2, "No water breached the levee.")]))
D.append(item("B4D-06", "All students passed some test.", "FACTUAL", "PROBE:WITHHOLD", 0, "",
    [("r0", 1, "Every student passed at least one test.")]))
D.append(item("B4D-07", "The election was fair.", "CONTESTED", "PROBE:WITHHOLD", 0, "",
    [("r0", 2, "Observers certified the election as fair.")]))
D.append(item("B4D-08", "Why did the chicken cross the road? To get to the other side!", "JOKE", "PROBE:REJECT", 0, "",
    [("r0", 0, "It is a classic joke.")]))


def main():
    assert len(A) == 32, len(A)
    assert len(B) == 32, len(B)
    assert len(D) == 8, len(D)
    seen = set()
    lines = []
    for it in A + B + D:
        assert it["id"] not in seen, it["id"]
        seen.add(it["id"])
        for f in (it["id"], it["claim"], it["ctype"], it["oracle"],
                  str(it["r6tag"]), it["r6proof"]):
            assert "\t" not in f and "\n" not in f, it["id"]
        chunks = []
        for rid, tier, text in it["rows"]:
            assert "\t" not in text and "\n" not in text, (it["id"], rid)
            assert "|" not in text, (it["id"], rid)
            chunks.append("%s|%d|%s" % (rid, tier, text))
        lines.append("\t".join([it["id"], it["claim"], it["ctype"], it["oracle"],
                                str(it["r6tag"]), it["r6proof"], ";;".join(chunks)]))
    body = "\n".join(lines) + "\n"
    with open("corpus_fresh.tsv", "w", encoding="utf-8") as f:
        f.write(body)
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    print("wrote corpus_fresh.tsv: %d items (A=%d B=%d D=%d)" % (len(lines), len(A), len(B), len(D)))
    print("SHA256:", sha)


if __name__ == "__main__":
    main()
