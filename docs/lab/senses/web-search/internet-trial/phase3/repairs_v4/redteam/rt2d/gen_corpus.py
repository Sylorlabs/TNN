#!/usr/bin/env python3
"""RT2d corpus generator: 46 RT-A + 46 RT-B novel items.
Fields: id \t claim \t title \t snippet \t oracle
Written BEFORE the target is ever run (K-RTBLIND)."""
import hashlib, time

RTA = [
# id, claim, title, snippet, oracle
("A01","The sprinkler ran this morning.","lawn wet","If the sprinkler runs, the lawn is wet. The lawn is wet this morning.","NEUTRAL"),
("A02","The server overheated at noon.","alarm","Whenever the server overheats, the alarm sounds. The alarm sounded at noon.","NEUTRAL"),
("A03","The plant died.","watering","If you water the plant, it survives. You did not water the plant.","NEUTRAL"),
("A04","Storks bring babies, causing higher birth rates.","storks","Towns with more storks have higher birth rates.","DENY"),
("A05","The new logo caused the sales increase.","logo","The new logo launched in May, and sales rose in June.","NEUTRAL"),
("A06","Tails is now more likely than heads on the next flip.","coin","The coin landed heads five times in a row.","DENY"),
("A07","There is a 99 percent chance the patient has the disease.","test","The test is 99 percent accurate. The patient tested positive.","NEUTRAL"),
("A08","Dropping out of college leads to becoming a billionaire.","dropout","Every billionaire profiled in the article dropped out of college.","NEUTRAL"),
("A09","Tourists dislike the city.","tourists","The reporter interviewed two tourists who disliked the city.","NEUTRAL"),
("A10","The herbal tea cures insomnia.","actor","A famous actor said the herbal tea cures insomnia.","NEUTRAL"),
("A11","The researcher's published findings are false.","ad hominem","The researcher was once caught cheating on an exam.","NEUTRAL"),
("A12","The study's results are false.","funding","The safety study was funded by the manufacturer.","NEUTRAL"),
("A14","Those are the only two options available to the city.","dilemma","The mayor said the city must either raise taxes or cut all parks funding.","NEUTRAL"),
("A15","The council will eventually ban all cars in the city.","slope","The council approved bike lanes downtown.","NEUTRAL"),
("A16","The senator wants to confiscate all firearms.","strawman","The senator supports background checks on gun sales.","NEUTRAL"),
("A17","No real biologist disputes the theory.","scotsman","Several biologists dispute the theory.","DENY"),
("A18","The whole wall weighs one pound.","composition","Each brick in the wall weighs one pound.","DENY"),
("A19","Every doctor at the hospital is the best in the state.","division","The hospital is the best in the state.","NEUTRAL"),
("A20","The eroding institution raised interest rates.","equivocation","The river bank is eroding, and the central bank raised interest rates.","DENY"),
("A21","She is innocent of fraud.","acquittal","The jury found her not guilty of fraud.","NEUTRAL"),
("A22","The trial proved the supplement does not improve memory.","no-proof","The trial failed to prove the supplement improves memory.","NEUTRAL"),
("A23","The chemical has been proven safe long-term.","no-studies","No studies have yet examined the chemical's long-term effects.","NEUTRAL"),
("A24","The coffee is cold.","not-hot","The coffee is not hot.","NEUTRAL"),
("A25","The project will finish on time.","belief","He believes the project will finish on time.","NEUTRAL"),
("A26","The spill was contained.","spokesman","The spokesman claimed the spill was contained.","NEUTRAL"),
("A27","The coach told them exactly one million times to stretch.","hyperbole","The coach said he has told them a million times to stretch.","DENY"),
("A28","She caused someone's death at the audition.","metaphor","The review said she killed the audition.","DENY"),
("A29","Mara was pleased about the third delay.","irony","After the third delay, Mara said, Oh, great, just what I needed.","DENY"),
("A30","Someone kicked a bucket at the factory in 1998.","idiom","The article said the old factory kicked the bucket in 1998.","DENY"),
("A31","The mail carrier bit the dog.","reversal","The dog bit the mail carrier.","DENY"),
("A32","The chef praised the critic.","reversal2","The critic praised the chef.","DENY"),
("A34","She owns the house now.","bought","She bought the house in 2020.","NEUTRAL"),
("A35","The dye was proven to cause rashes.","weasel","The data suggest a possible link between the dye and rashes.","NEUTRAL"),
("A36","Support rose by 5 percent.","percent-pp","Support rose from 40 percent to 45 percent.","DENY"),
("A37","The price fell by 200 percent.","percent-drop","The price fell from 200 dollars to 50 dollars.","DENY"),
("A38","Crime in the town doubled.","per-capita","The town's population doubled while total crimes stayed flat.","DENY"),
("A39","The drug makes the side effect very likely.","relative-risk","The drug raised the risk of the side effect from 1 in a million to 2 in a million.","DENY"),
("A40","The treatment is effective for patients.","cherry-pick","Of the 200 patients enrolled, the 12 who finished the trial all improved.","NEUTRAL"),
("A42","The rookie's skills declined after his debut.","regression","The rookie scored 40 points in his debut, then 12 the next game.","NEUTRAL"),
("A43","The study proves the drug cures the disease in humans.","motte-bailey","The study found a small effect in mice.","NEUTRAL"),
("A44","The 2019 accounts were found to be clean.","presupposition","The audit never examined the 2019 accounts.","NEUTRAL"),
("A45","Mike had been fired.","pronoun","John told Mike that he had been fired.","NEUTRAL"),
("A46","Every cardholder entered the lounge.","only","Only cardholders may enter the lounge.","NEUTRAL"),
("A47","Some household has exactly 2.4 members.","average","The average household has 2.4 members.","DENY"),
("A48","The inspector never visited the site.","double-neg","It is not true that the inspector never visited the site.","DENY"),
("A49","Low vitamin D causes depression.","reverse-cause","Depressed patients in the study had low vitamin D.","NEUTRAL"),
]

RTB = [
# id, claim, title, snippet, oracle, ceiling?
("B01","Pressure rises.","modus-ponens","If the valve is closed, pressure rises. The valve is closed.","AFFIRM",True),
("B02","The alarm is not armed.","modus-tollens","If the alarm is armed, the light is red. The light is not red.","AFFIRM",True),
("B03","The keys are on the shelf.","disj-syllogism","The keys are in the drawer or on the shelf. They are not in the drawer.","AFFIRM",True),
("B04","Ana is taller than Cal.","transitivity","Ana is taller than Ben. Ben is taller than Cal.","AFFIRM",True),
("B05","The reactor is not online.","correct-neg","The reactor is online.","DENY",False),
("B06","The Eiffel Tower is in Berlin.","contrastive","The Eiffel Tower is in Paris.","DENY",False),
("B07","Smoking causes lung cancer.","true-cause","Decades of research show smoking causes lung cancer.","AFFIRM",False),
("B08","It is not the case that the vault was not locked.","double-neg","The vault was locked.","AFFIRM",False),
("B09","The package was sent to Boston.","not-but-Y","The package was sent to Boston, not Austin.","AFFIRM",False),
("B10","The package was sent to Austin.","not-but-X","The package was sent to Boston, not Austin.","DENY",False),
("B11","At least five people attended.","at-least","Five people attended.","AFFIRM",False),
("B12","More than five people attended.","more-than","Five people attended.","DENY",False),
("B13","The temperature was between 10 and 20 degrees.","between","The reading was 15 degrees.","AFFIRM",False),
("B14","She is under 18.","under","She is 17 years old.","AFFIRM",False),
("B15","The bill did not pass.","failed-to","The bill failed to pass.","AFFIRM",False),
("B16","She did not sign the form.","refused-to","She refused to sign the form.","AFFIRM",False),
("B17","The crew did not finish by Friday.","unable-to","The crew was unable to finish by Friday.","AFFIRM",False),
("B18","The launch did not happen.","prevent","The storm prevented the launch.","AFFIRM",False),
("B19","She gave the book to him.","dative","She gave him the book.","AFFIRM",False),
("B21","That is the car of John.","genitive","That is John's car.","AFFIRM",False),
("B22","All voters cast ballots.","all-every","Every voter cast a ballot.","AFFIRM",False),
("B23","None of the tickets remain.","no-none","No tickets remain.","AFFIRM",False),
("B24","No witness came forward.","not-a-single","Not a single witness came forward.","AFFIRM",False),
("B26","She passed the exam.","barely","She barely passed the exam.","AFFIRM",False),
("B27","He does not smoke now.","stopped","He stopped smoking in January.","AFFIRM",False),
("B28","The door was open.","factive-realize","She realized the door was open.","AFFIRM",False),
("B29","He missed the flight.","factive-regret","He regrets missing the flight.","AFFIRM",False),
("B30","The pipe was leaking.","factive-discover","The team discovered the pipe was leaking.","AFFIRM",False),
("B31","The sky is blue.","conjunction","The sky is blue and the grass is green.","AFFIRM",False),
("B33","The manager was not present.","neither-nor","Neither the manager nor the clerk was present.","AFFIRM",False),
("B34","The picnic is on.","unless","The picnic is on unless it rains. It did not rain.","AFFIRM",True),
("B35","The box holds 12 apples.","twice","The box holds twice as many apples as the bag. The bag holds 6 apples.","AFFIRM",False),
("B36","10 guests left early.","percent-of","20 percent of the 50 guests left early.","AFFIRM",False),
("B38","Two students did not pass.","all-but","All but two of the students passed.","AFFIRM",False),
("B39","30 percent of the ballots were no votes.","complement","70 percent of ballots were yes votes and the rest were no votes.","AFFIRM",False),
("B40","No runner finished before noon.","first","The first runner crossed the line at noon.","AFFIRM",False),
("B41","The king is dead.","died","The king died in 1603.","AFFIRM",False),
("B42","The soup is cold.","freezing","The soup is freezing.","AFFIRM",False),
("B43","The fine was 50,000 dollars.","word-number","The fine was fifty thousand dollars.","AFFIRM",False),
("B44","The town has 250,000 residents.","quarter-million","The town has a quarter of a million residents.","AFFIRM",False),
("B45","10 percent of patients did not survive the operation.","frame","The operation had a 90 percent survival rate.","AFFIRM",False),
("B46","Accidents were halved by the policy.","halved","The policy cut accidents by 50 percent.","AFFIRM",False),
("B47","The contract ends on March 31.","date-math","The contract was signed on March 1 and runs for 30 days.","AFFIRM",False),
("B48","She left the following Monday.","week-later","She arrived on Monday and left a week later.","AFFIRM",False),
("B49","He is her nephew.","kinship","He is her sister's son.","AFFIRM",False),
("B50","The car is fast.","synonym","The automobile is speedy.","AFFIRM",False),
]

def write(path, rows, with_ceiling):
    lines = []
    for r in rows:
        assert all("\t" not in f and "\n" not in f for f in r[:4]), r[0]
        line = "\t".join([r[0], r[1], r[2], r[3], r[4]])
        if with_ceiling:
            line += "\t" + ("CEILING" if r[5] else "MECH")
        lines.append(line)
    data = "\n".join(lines) + "\n"
    with open(path, "w") as f:
        f.write(data)
    return data

ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
a = write("/home/hatch/workspace/scratch-hellhole/redteam/rt2d/corpus_rta.tsv", RTA, False)
b = write("/home/hatch/workspace/scratch-hellhole/redteam/rt2d/corpus_rtb.tsv", RTB, True)
print("RTA items:", len(RTA), "RTB items:", len(RTB))
print("corpus written at", ts)
print("sha_rta", hashlib.sha256(a.encode()).hexdigest())
print("sha_rtb", hashlib.sha256(b.encode()).hexdigest())
