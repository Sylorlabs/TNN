import os

D = "/home/hatch/workspace/scratch-hellhole/redteam/rt2c"

# (idx, claim, title, snippet, oracle)  oracle in {AFFIRM,DENY,NEUTRAL}
rtA = [
("A01","the window broke the ball","window accident report","the ball hit the window and the window shattered","DENY"),
("A02","the rain started before the clouds gathered","storm timeline","the clouds gathered first, and then the rain started","DENY"),
("A03","the dog bit the man","park incident","the man bit the dog","DENY"),
("A04","the soup is cold","lunch review","the soup is steaming hot","DENY"),
("A05","the store is open","shop door notice","a sign on the door says the store is closed","DENY"),
("A06","the tank holds at least 100 liters","tank spec","the tank holds 90 liters","DENY"),
("A07","at most five guests arrived","party headcount","seven guests arrived","DENY"),
("A08","most voters approved the measure","referendum results","49 of the 100 voters approved the measure","DENY"),
("A09","the baby weighs 3 kilograms","clinic record","the baby weighs 7 ounces","DENY"),
("A10","the box is both open and shut","box inspection","the box is open","DENY"),
("A11","no birds were seen today","birdwatch log","the watcher logged three sparrows today","DENY"),
("A12","the meeting is on Monday","schedule update","the meeting was moved from Monday to Tuesday","DENY"),
("A13","the rain stopped the game","match report","although it rained, the game continued","DENY"),
("A14","the light is off","room check","the light is on","DENY"),
("A15","she is taller than him","height records","she is 160 cm tall and he is 175 cm tall","DENY"),
("A16","the drought caused the flood","flood inquiry","the flood was caused by three days of heavy rain","DENY"),
("A17","the chef cooked the meal","kitchen roster","the sous-chef cooked the meal","DENY"),
("A18","twice as many cats as dogs were adopted","shelter numbers","10 cats and 6 dogs were adopted","DENY"),
("A19","the painting is a forgery","gallery appraisal","the expert confirmed the painting is genuine","DENY"),
("A20","the train left at noon","departure board","the train left at 2 pm","DENY"),
("A21","the defendant is innocent","trial outcome","the jury found the defendant not guilty","NEUTRAL"),
("A22","the rooster's crowing makes the sun rise","farm notes","the rooster crows every morning just before sunrise","NEUTRAL"),
("A23","ice cream causes sunburn","summer health memo","ice cream sales and sunburn cases both peak in July","NEUTRAL"),
("A24","the rain dance brought the rain","village chronicle","the tribe performed the rain dance, and hours later it rained","NEUTRAL"),
("A25","dropping out of college causes success","founder survey","several famous founders dropped out of college","NEUTRAL"),
("A26","the supplement is safe","safety review","no study has ever proven the supplement unsafe","NEUTRAL"),
("A27","black is due next","casino log","the roulette wheel landed on red ten times in a row","NEUTRAL"),
("A28","all customers complained","feedback summary","some customers complained","NEUTRAL"),
("A29","every student passed","exam results","most students passed","NEUTRAL"),
("A30","every family has 2.3 children","census note","the average family has 2.3 children","NEUTRAL"),
("A31","only dogs bark","animal behavior guide","dogs bark","NEUTRAL"),
("A32","the new phone is the best phone","product launch","the new phone was released this month","NEUTRAL"),
("A33","the old method is the best method","workshop manual","people have used the old method for a hundred years","NEUTRAL"),
("A34","the policy will bankrupt the town","council debate","critics warn the policy might raise costs","NEUTRAL"),
("A35","the herb cures colds","herbal claim","Dr. Rao said the herb cures colds","NEUTRAL"),
("A36","the drug definitely works","trial press note","the drug might work, researchers say","NEUTRAL"),
("A37","the bridge collapsed","storm warning","if the storm hits, the bridge will collapse","NEUTRAL"),
("A38","the medicine cured him","recovery story","he took the medicine and he recovered","NEUTRAL"),
("A39","taller people are better leaders","leadership article","most CEOs are tall","NEUTRAL"),
("A40","the bat flew into the cave","cave sighting","he swung the wooden bat at the ball","NEUTRAL"),
("A41","the car is light","car review","every part of the car is light","NEUTRAL"),
("A42","each musician is talented","concert review","the orchestra is talented","NEUTRAL"),
("A43","the suspect is guilty","case notes","the suspect has not been proven not guilty","NEUTRAL"),
("A44","the dam will hold","river authority statement","officials hope the dam will hold","NEUTRAL"),
("A45","the vaccine prevented an outbreak in the town","town health report","the town was vaccinated and no outbreak occurred","NEUTRAL"),
("A46","the tank holds exactly 100 liters","tank estimate","the tank holds between 90 and 110 liters","NEUTRAL"),
]

rtB = [
("B01","the store is closed","shop door notice","a sign says the store is open","DENY"),
("B02","the store is not closed","shop door notice","a sign says the store is open","AFFIRM"),
("B03","the door is open","hallway check","the door is not closed","AFFIRM"),
("B04","not all birds fly","field guide","penguins cannot fly","AFFIRM"),
("B05","the cat sat on the mat","pet diary","the cat was sitting on the mat","AFFIRM"),
("B06","the automobile is fast","car review","the car is speedy","AFFIRM"),
("B07","the tank holds between 90 and 110 liters","tank spec","the tank holds 105 liters","AFFIRM"),
("B08","the tank holds at least 100 liters","tank spec","the tank holds 90 liters","DENY"),
("B09","the rain started after the clouds gathered","storm timeline","the clouds gathered, then the rain started","AFFIRM"),
("B10","the rain started before the clouds gathered","storm timeline","the clouds gathered, then the rain started","DENY"),
("B11","the soup is cold","lunch review","the soup is steaming hot","DENY"),
("B12","the soup is not hot","lunch review","the soup is ice cold","AFFIRM"),
("B13","the ball shattered the window","window accident report","the ball hit the window and the window shattered","AFFIRM"),
("B14","the drought caused the flood","flood inquiry","the flood was caused by heavy rain","DENY"),
("B15","the umbrella kept her dry","rainy day note","the umbrella blocked the rain and she stayed dry","AFFIRM"),
("B16","the box weighs 5 kilograms","parcel label","the box weighs 5 kg","AFFIRM"),
("B17","she is taller than him","height records","she is 175 cm tall and he is 160 cm tall","AFFIRM"),
("B18","at least five guests arrived","party headcount","seven guests arrived","AFFIRM"),
("B19","at most five guests arrived","party headcount","seven guests arrived","DENY"),
("B20","none of the lights are on","building check","no light is on","AFFIRM"),
("B21","every student passed","exam results","all students passed","AFFIRM"),
("B22","the chef cooked the meal","kitchen roster","the meal was cooked by the chef","AFFIRM"),
("B23","the chef cooked the meal","kitchen roster","the sous-chef cooked the meal","DENY"),
("B24","twice as many cats as dogs were adopted","shelter numbers","10 cats and 5 dogs were adopted","AFFIRM"),
("B25","most voters approved the measure","referendum results","51 of 100 voters approved the measure","AFFIRM"),
("B26","there is no milk left","kitchen note","the fridge has no milk","AFFIRM"),
("B27","the drug might work","trial press note","researchers say the drug may be effective","AFFIRM"),
("B28","if it rains, the match is canceled","league rules","if it rains, the match will be canceled","AFFIRM"),
("B29","the assistant approved it, not the manager","office memo","the manager did not approve it; the assistant approved it","AFFIRM"),
("B30","the sandbags prevented flooding","flood defenses","the sandbags held back the water","AFFIRM"),
("B31","the window did not break the ball","window accident report","the ball hit the window and the window shattered","AFFIRM"),
("B32","the light is on","room check","the light is not off","AFFIRM"),
("B33","the meeting is not on Monday","schedule update","the meeting was moved from Monday to Tuesday","AFFIRM"),
("B34","fewer than ten people came","party headcount","seven people came","AFFIRM"),
("B35","more than ten people came","party headcount","seven people came","DENY"),
("B36","the painting is genuine","gallery appraisal","the expert confirmed the painting is genuine","AFFIRM"),
("B37","the train did not leave at noon","departure board","the train left at 2 pm","AFFIRM"),
("B38","he is the tallest","team roster","he is taller than everyone else","AFFIRM"),
("B39","the glass is empty","table setting","the glass has nothing in it","AFFIRM"),
("B40","the glass is full","table setting","the glass has nothing in it","DENY"),
("B41","she did not attend","attendance sheet","she was absent","AFFIRM"),
("B42","the river is wider than the stream","survey data","the river is 30 meters wide; the stream is 5 meters wide","AFFIRM"),
("B43","the river is narrower than the stream","survey data","the river is 30 meters wide; the stream is 5 meters wide","DENY"),
("B44","the alarm did not ring","building log","the alarm was silent","AFFIRM"),
("B45","the alarm rang","building log","the alarm was silent","DENY"),
("B46","no one was hurt","accident report","everyone escaped unhurt","AFFIRM"),
]

ceiling = [
("C01","the ground is wet","weather logic","if it rains the ground gets wet; it rained","AFFIRM"),
("C02","it did not rain","weather logic","if it rains the ground gets wet; the ground is dry","AFFIRM"),
("C03","it rained","weather logic","if it rains the ground gets wet; the ground is wet","NEUTRAL"),
("C04","the sparrow has feathers","field guide logic","all birds have feathers; the sparrow is a bird","AFFIRM"),
("C05","the match was played","league logic","if it rains the match is canceled; it did not rain","NEUTRAL"),
]

def check(rows, name):
    assert len(rows) == len({r[0] for r in rows}), f"dup idx in {name}"
    for r in rows:
        assert len(r) == 5, r
        assert r[4] in ("AFFIRM","DENY","NEUTRAL"), r
        for f in r[:4]:
            assert "\t" not in f and "\n" not in f, r

check(rtA,"rtA"); check(rtB,"rtB"); check(ceiling,"ceiling")
assert len(rtA)==46 and len(rtB)==46 and len(ceiling)==5

for name, rows in (("corpus_rtA",rtA),("corpus_rtB",rtB),("corpus_ceiling",ceiling)):
    with open(os.path.join(D, name+".tsv"),"w") as f:
        for r in rows:
            f.write("\t".join(r)+"\n")
print("wrote", len(rtA), len(rtB), len(ceiling))
