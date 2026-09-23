import os
D = "/home/hatch/workspace/scratch-hellhole/crews/a4"

# rows: (idx, claim, title, snippet, oracle_tag)  tag: 0=NEUTRAL 1=AFFIRM 2=DENY
COND = [
 ("C1","Water boils at 100C.","Conditional case 1","If water reaches 100C it boils.",0),
 ("C2","Water boils at 100C.","Conditional case 2","If water reaches 100C it boils; the kettle reached 100C.",1),
 ("C3","Smoke causes cancer.","Conditional case 3","If people smoke, it causes cancer.",0),
 ("C4","Smoke causes cancer.","Conditional case 4","If people smoke, it causes cancer. Smokers in the study had more cancer.",1),
 ("C5","The tower was struck by lightning.","Conditional case 5","If the storm had come, lightning would have struck the tower.",0),
 ("C6","Lightning strikes the tower.","Conditional case 6","If a storm comes, lightning will strike the tower.",0),
 ("C7","Birds use tools.","Conditional case 7","Birds use tools if they are available.",0),
 ("C8","Birds use tools.","Conditional case 8","Birds use tools; sticks were available to the crows.",1),
 ("C9","Honey cures coughs.","Conditional case 9","If honey is taken, it cures coughs.",0),
 ("C10","Water boils at 100C.","Conditional case 10","Water would boil at 100C if heated.",0),
 ("C11","Water boils at 100C.","Conditional case 11","If water reaches 100C it boils, and our thermometer read 100C.",1),
 ("C12","Smoke causes cancer.","Conditional case 12","Smoke causes cancer whether you smoke or not.",1),
 ("C13","Water boils at 100C.","Conditional case 13","If water reaches 100C it does not boil.",2),
]
QNT = [
 ("Q1","All cats are indoors.","Quantifier case 1","Some cats are not indoors.",2),
 ("Q2","No cats are indoors.","Quantifier case 2","One cat is indoors.",2),
 ("Q3","Most cats are indoors.","Quantifier case 3","Most cats are not indoors.",2),
 ("Q4","Some cats are indoors.","Quantifier case 4","All cats are indoors.",1),
 ("Q5","All cats are indoors.","Quantifier case 5","Some cats are indoors.",0),
 ("Q6","No birds use tools.","Quantifier case 6","One bird uses tools.",2),
 ("Q7","All dogs are loud.","Quantifier case 7","Some dogs are not loud.",2),
 ("Q8","Cats are indoors.","Quantifier case 8","Some cats are not indoors.",2),
 ("Q9","Cats are indoors.","Quantifier case 9","All cats are indoors.",1),
 ("Q10","Few cats are indoors.","Quantifier case 10","Most cats are indoors.",2),
 ("Q11","Many cats are indoors.","Quantifier case 11","No cats are indoors.",2),
 ("Q12","Some cats are indoors.","Quantifier case 12","No cats are indoors.",2),
]
HEDGE = [
 ("H1","Coffee cures colds.","Hedge case 1","Coffee may cure colds.",0),
 ("H2","Coffee cures colds.","Hedge case 2","Coffee might cure colds.",0),
 ("H3","Coffee cures colds.","Hedge case 3","Coffee could cure colds.",0),
 ("H4","Coffee cures colds.","Hedge case 4","A study suggests coffee cures colds.",0),
 ("H5","Coffee cures colds.","Hedge case 5","Coffee possibly cures colds.",0),
 ("H6","Coffee cures colds.","Hedge case 6","Coffee appears to cure colds.",0),
 ("H7","Coffee cures colds.","Hedge case 7","Coffee seems to cure colds.",0),
 ("H8","Coffee cures colds.","Hedge case 8","Coffee is thought to cure colds.",0),
 ("H9","Coffee cures colds.","Hedge case 9","Coffee may not cure colds.",0),
 ("H10","Coffee cures colds.","Hedge case 10","Coffee cures colds.",1),
 ("H11","Coffee does not cure colds.","Hedge case 11","Coffee may not cure colds.",0),
 ("H12","Coffee cures colds.","Hedge case 12","Researchers believe coffee cures colds.",0),
]
TMP = [
 ("T1","The flood was before the drought.","Temporal case 1","The flood was after the drought.",2),
 ("T2","The flood was before the drought.","Temporal case 2","The flood was before the drought.",1),
 ("T3","The flood was before the drought.","Temporal case 3","The flood was bad and the drought was worse.",0),
 ("T4","The flood was in 1990, before the drought.","Temporal case 4","The drought was in 1995 and the flood was in 1990.",1),
 ("T5","The flood was in 1990, before the drought.","Temporal case 5","The drought was in 1985 and the flood was in 1990.",2),
 ("T6","She was here before noon.","Temporal case 6","She was here after noon.",2),
 ("T7","The meeting was before lunch.","Temporal case 7","The meeting was after lunch.",2),
 ("T8","The drought was after the flood.","Temporal case 8","The drought was before the flood.",2),
 ("T9","The flood was before the drought.","Temporal case 9","The drought was before the flood.",2),
 ("T10","The quake was before the flood, which was before the fire.","Temporal case 10","The quake was before the fire, which was before the flood.",2),
 ("T11","Dawn was before noon.","Temporal case 11","Dawn was early and noon was late.",0),
 ("T12","The flood was in 1990, before the drought.","Temporal case 12","The flood was in 2001, before the drought.",2),
]
CMP = [
 ("P1","The cheetah is faster than the lion.","Comparative case 1","The cheetah is slower than the lion.",2),
 ("P2","The cheetah is faster than the lion.","Comparative case 2","The cheetah is faster than the lion.",1),
 ("P3","The whale is bigger than the shark.","Comparative case 3","The whale is smaller than the shark.",2),
 ("P4","The mountain is taller than the hill.","Comparative case 4","The mountain is shorter than the hill.",2),
 ("P5","Steel is hotter than copper.","Comparative case 5","Steel is colder than copper.",2),
 ("P6","Mary is older than John.","Comparative case 6","Mary is younger than John.",2),
 ("P7","The lion is slower than the cheetah.","Comparative case 7","The lion is faster than the cheetah.",2),
 ("P8","The cheetah is faster than the lion.","Comparative case 8","The lion is faster than the cheetah.",2),
 ("P9","The box has more apples than the bag.","Comparative case 9","The box has fewer apples than the bag.",2),
 ("P10","The box has more apples than the bag.","Comparative case 10","The bag has more apples than the box.",2),
]
corpora = {"cond":COND,"qnt":QNT,"hedge":HEDGE,"tmp":TMP,"cmp":CMP}
for fam, rows in corpora.items():
    # sanity: no tabs/newlines inside fields
    for r in rows:
        for f in r[:4]:
            assert "\t" not in f and "\n" not in f, f
        assert r[4] in (0,1,2)
    with open(os.path.join(D,"corpus_%s.tsv"%fam),"w") as f:
        for r in rows:
            f.write("\t".join([r[0],r[1],r[2],r[3],str(r[4])])+"\n")
    # projection: first 4 columns (classifier input)
    with open(os.path.join(D,"in_%s.tsv"%fam),"w") as f:
        for r in rows:
            f.write("\t".join(r[:4])+"\n")
    print("corpus_%s.tsv: %d rows"%(fam,len(rows)))
