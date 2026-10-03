# Battery generator — re-derives the frozen LOGIC-CORE batteries byte-identically.
# Re-frozen 2026-09-23 (BATTERIES_FROZEN.md, round-2 re-freeze after 11
# spec-mandated oracle corrections; see PROOF.md). Do not regenerate to edit,
# only to verify reproducibility. Row format: id<TAB>claim_prop<TAB>evidence_props<TAB>oracle.
import os
OUT = os.path.dirname(os.path.abspath(__file__))
def emit(name, rows):
    with open(os.path.join(OUT, name + ".tsv"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")
def N(tag, i, c, e, o): return ("G%s-%02d" % (tag, i), c, e, str(o))
def M(i, c, e, o): return ("ML-%d" % i, c, e, str(o))
def V(i, c, e, o): return ("VP-%s" % i, c, e, str(o))

g_neg = [
 N("N",1,"ROUND(earth)","ROUND(earth)","1"),N("N",2,"NOT(FLAT(earth))","NOT(FLAT(earth))","1"),
 N("N",3,"FLAT(earth)","NOT(FLAT(earth))","2"),N("N",4,"NOT(FLAT(earth))","FLAT(earth)","2"),
 N("N",5,"DOGS_BARK","NOT(DOGS_BARK)","2"),N("N",6,"NOT(DOGS_BARK)","DOGS_BARK","2"),
 N("N",7,"CAUSE(RAIN(),WET(ground))","NOT(CAUSE(RAIN(),WET(ground)))","2"),
 N("N",8,"NOT(CAUSE(RAIN(),WET(ground)))","CAUSE(RAIN(),WET(ground))","2"),
 N("N",9,"ALL(birds,FLY(birds))","ALL(birds,FLY(birds))","1"),
 N("N",10,"FLAT(earth)","NOT(ROUND(earth))","0"),N("N",11,"HOT(sun)","NOT(COLD(moon))","0"),
 N("N",12,"CAUSE(A(),B())","NOT(CAUSE(C(),D()))","0"),N("N",13,"FLAT(earth)","ROUND(earth)","0"),
 N("N",14,"NOT(NOT(FLAT(earth)))","FLAT(earth)","1"),
 N("N",15,"NOT(NOT(NOT(FLAT(earth))))","NOT(FLAT(earth))","1"),
 N("N",16,"NOT(ROUND(earth))","NOT(ROUND(earth))","1"),
 N("N",17,"NOT(FLAT(earth))","NOT(ROUND(earth))","0"),N("N",18,"FLAT(earth)","NOT(FLAT(mars))","0"),
 N("N",19,"NOT(NOT(ROUND(earth)))","ROUND(earth)","1"),N("N",20,"ROUND(earth)","NOT(NOT(ROUND(earth)))","1")]

g_con = [
 N("C",1,"CAUSE(RAIN(),FLOOD())","CAUSE(RAIN(),FLOOD())","1"),
 N("C",2,"CAUSE(SMOKING(),CANCER())","NOT(CAUSE(SMOKING(),CANCER()))","2"),
 N("C",3,"CAUSE(LESS_DENSE(ice,than_water),FLOATS(ice,on_water))","LESS_DENSE(ice,than_water)","1"),
 N("C",4,"CAUSE(LESS_DENSE(ice,than_water),FLOATS(ice,on_water))","NOT(FLOATS(ice,on_water))","2"),
 N("C",5,"CAUSE(CONTAINS(coffee,melatonin),WAKES_UP(coffee,drinker))","NOT(CONTAINS(coffee,melatonin))","2"),
 N("C",6,"FLOATS(ice,on_water)","CAUSE(LESS_DENSE(ice,than_water),FLOATS(ice,on_water))","1"),
 N("C",7,"CAUSE(A(),B())","CAUSE(A(),NOT(B()))","2"),
 N("C",8,"CAUSE(A(),B())","NOT(A())","2"),
 N("C",9,"CAUSE(A(),B())","NOT(B())","2"),
 N("C",10,"CAUSE(A(),NOT(B()))","NOT(CAUSE(A(),B()))","0"),
 N("C",11,"CAUSE(A(),B())","CAUSE(A(),C())","0"),N("C",12,"CAUSE(A(),B())","CAUSE(C(),B())","0"),
 N("C",13,"A()","CAUSE(B(),A())","1"),N("C",14,"CAUSE(A(),B())","CAUSE(B(),A())","0"),
 N("C",15,"NOT(CAUSE(A(),B()))","NOT(CAUSE(A(),B()))","1"),
 N("C",16,"CAUSE(A(),B())","NOT(CAUSE(B(),A()))","0"),N("C",17,"CAUSE(A(),B())","A()","0"),
 N("C",18,"CAUSE(A(),B())","B()","0"),N("C",19,"WAKES_UP(coffee,drinker)","CAUSE(NOT(CONTAINS(coffee,melatonin)),WAKES_UP(coffee,drinker))","0"),
 N("C",20,"CAUSE(RAIN(),WET(ground))","CAUSE(RAIN(),NOT(WET(ground)))","2")]

g_cau = [
 N("U",1,"FLOATS(ice,on_water)","CAUSE(LESS_DENSE(ice,than_water),FLOATS(ice,on_water))","1"),
 N("U",2,"FLOATS(ice,on_water)","CAUSE(LESS_DENSE(ice,than_water),NOT(FLOATS(ice,on_water)))","2"),
 N("U",3,"CAUSE(LESS_DENSE(ice,than_water),FLOATS(ice,on_water))","NOT(LESS_DENSE(ice,than_water))","2"),
 N("U",4,"CAUSE(A(),B())","CAUSE(A(),NOT(B()))","2"),
 N("U",5,"CAUSE(CONTAINS(coffee,melatonin),WAKES_UP(coffee,drinker))","NOT(CONTAINS(coffee,melatonin))","2"),
 N("U",6,"CAUSE(RAIN(),FLOOD())","CAUSE(RAIN(),FLOOD())","1"),
 N("U",7,"CAUSE(RAIN(),FLOOD())","NOT(FLOOD())","2"),N("U",8,"CAUSE(RAIN(),FLOOD())","RAIN()","0"),
 N("U",9,"FLOOD()","CAUSE(SNOWMELT(),FLOOD());CAUSE(RAIN(),SNOWMELT())","1"),
 N("U",10,"HEALTHY(person)","CAUSE(VIRUS(),NOT(HEALTHY(person)))","2"),
 N("U",11,"GROWS(wheat)","CAUSE(RAIN(),GROWS(wheat))","1"),
 N("U",12,"WET(ground)","CAUSE(RAIN(),WET(ground))","1"),
 N("U",13,"WET(ground)","CAUSE(SPRINKLER(),WET(ground))","1"),
 N("U",14,"CAUSE(SMOKING(),CANCER())","CAUSE(SMOKING(),NOT(CANCER()))","2"),
 N("U",15,"CAUSE(VACCINE(),IMMUNITY())","CAUSE(VACCINE(),IMMUNITY())","1"),
 N("U",16,"CANCER()","CAUSE(SMOKING(),CANCER());CAUSE(SMOKING(),TAR())","1"),
 N("U",17,"IMMUNITY()","CAUSE(VACCINE(),IMMUNITY())","1"),
 N("U",18,"SICK(person)","CAUSE(VIRUS(),NOT(HEALTHY(person)))","0"),
 N("U",19,"CAUSE(VACCINE(),IMMUNITY())","NOT(VACCINE())","2"),
 N("U",20,"CAUSE(LESS_DENSE(ice,than_water),FLOATS(ice,on_water))","NOT(FLOATS(ice,on_water))","2")]

g_qnt = [
 N("T",1,"QTY(senses,exactly,five)","QTY(senses,exactly,twenty_two)","2"),
 N("T",2,"QTY(senses,range,22_to_33)","QTY(senses,exactly,twenty_five)","1"),
 N("T",3,"QTY(senses,exactly,twenty_five)","QTY(senses,range,22_to_33)","0"),
 N("T",4,"QTY(senses,at_least,twenty)","QTY(senses,exactly,five)","2"),
 N("T",5,"QTY(senses,at_least,twenty)","QTY(senses,exactly,twenty_five)","1"),
 N("T",6,"QTY(senses,at_most,ten)","QTY(senses,exactly,twenty_five)","2"),
 N("T",7,"QTY(senses,at_most,ten)","QTY(senses,exactly,eight)","1"),
 N("T",8,"QTY(senses,more_than,thirty)","QTY(senses,exactly,thirty_three)","1"),
 N("T",9,"QTY(senses,more_than,thirty)","QTY(senses,exactly,thirty)","2"),
 N("T",10,"QTY(senses,less_than,thirty)","QTY(senses,exactly,thirty)","2"),
 N("T",11,"QTY(senses,at_least,twenty)","QTY(senses,range,between_22_and_33)","1"),
 N("T",12,"QTY(senses,exactly,five)","QTY(senses,range,between_22_and_33)","2"),
 N("T",13,"QTY(apples,exactly,five)","QTY(oranges,exactly,three)","0"),
 N("T",14,"QTY(goldfish_memory,exactly,3sec)","QTY(goldfish_memory,at_least,six_months)","2"),
 N("T",15,"QTY(goldfish_memory,at_least,six_months)","QTY(goldfish_memory,exactly,3sec)","2"),
 N("T",16,"QTY(download_time,at_least,two_min)","QTY(download_time,exactly,150sec)","1"),
 N("T",17,"QTY(download_time,at_most,one_hr)","QTY(download_time,exactly,thirty_min)","1"),
 N("T",18,"QTY(download_time,exactly,twelve_hr)","QTY(download_time,at_most,one_day)","0"),
 N("T",19,"QTY(pages,exactly,ninety)","QTY(pages,range,80_to_100)","0"),
 N("T",20,"QTY(senses,exactly,five)","QTY(senses,exactly,five)","1")]

g_cond = [
 N("D",1,"GROWS(wheat)","IF(RAIN(),GROWS(wheat));RAIN()","1"),
 N("D",2,"WET(ground)","IF(RAIN(),WET(ground));SPRINKLER()","0"),
 N("D",3,"B()","IF(A(),B());A()","1"),
 N("D",4,"GROWS(wheat)","IF(RAIN(),GROWS(wheat));RAIN()","1"),
 N("D",5,"WET(ground)","IF(RAIN(),WET(ground))","0"),
 N("D",6,"B()","IF(A(),B());NOT(A())","0"),
 N("D",7,"GROWS(wheat)","IF(RAIN(),GROWS(wheat));NOT(RAIN())","0"),
 N("D",8,"B()","IF(A(),B());A()","1"),
 N("D",9,"Q()","IF(P(),Q());IF(R(),P());R()","0"),
 N("D",10,"B()","IF(A(),B());A()","1"),
 N("D",11,"IF(A(),B())","NOT(IF(A(),B()))","2"),
 N("D",12,"IF(A(),B())","IF(A(),B())","1"),
 N("D",13,"C()","IF(A(),B());IF(B(),C());A()","0"),
 N("D",14,"B()","IF(A(),B());A()","1"),
 N("D",15,"B()","IF(A(),C())","0"),
 N("D",16,"FLOOD()","IF(RAIN(),FLOOD());RAIN()","1"),
 N("D",17,"GROWS(wheat)","IF(RAIN(),GROWS(wheat))","0"),
 N("D",18,"B()","IF(A(),B());A();NOT(A())","1"),
 N("D",19,"NOT(B())","IF(A(),B());A()","0"),
 N("D",20,"MAYBE(B())","IF(A(),B());A()","0")]

g_hedge = [
 N("H",1,"CURES(soup,cold)","MAYBE(CURES(soup,cold))","0"),
 N("H",2,"MAYBE(CURES(soup,cold))","MAYBE(CURES(soup,cold))","0"),
 N("H",3,"CURES(soup,cold)","CURES(soup,cold)","1"),
 N("H",4,"MAYBE(CURES(soup,cold))","CURES(soup,cold)","0"),
 N("H",5,"NOT(CURES(soup,cold))","MAYBE(CURES(soup,cold))","0"),
 N("H",6,"MAYBE(CURES(soup,cold))","NOT(CURES(soup,cold))","0"),
 N("H",7,"MAYBE(ROUND(earth))","MAYBE(ROUND(earth))","0"),
 N("H",8,"MAYBE(A())","NOT(MAYBE(A()))","0"),
 N("H",9,"A()","MAYBE(A())","0"),
 N("H",10,"MAYBE(A())","A()","0"),
 N("H",11,"CAUSE(A(),MAYBE(B()))","CAUSE(A(),MAYBE(B()))","1"),
 N("H",12,"CAUSE(A(),B())","CAUSE(A(),MAYBE(B()))","0"),
 N("H",13,"MAYBE(CAUSE(A(),B()))","MAYBE(CAUSE(A(),B()))","0"),
 N("H",14,"MAYBE(CAUSE(A(),B()))","CAUSE(A(),B())","0"),
 N("H",15,"MAYBE(QTY(senses,exactly,five))","MAYBE(QTY(senses,exactly,five))","0"),
 N("H",16,"QTY(senses,exactly,five)","MAYBE(QTY(senses,exactly,five))","0"),
 N("H",17,"ALL(birds,MAYBE(FLY(birds)))","ALL(birds,MAYBE(FLY(birds)))","1"),
 N("H",18,"ALL(birds,FLY(birds))","ALL(birds,MAYBE(FLY(birds)))","0"),
 N("H",19,"MAYBE(MAYBE(A()))","MAYBE(MAYBE(A()))","0"),
 N("H",20,"NOT(MAYBE(A()))","NOT(MAYBE(A()))","1")]

g_tmp = [
 N("P",1,"BEFORE(a,b)","BEFORE(b,a)","2"),N("P",2,"BEFORE(a,b)","BEFORE(a,b)","1"),
 N("P",3,"AFTER(a,b)","BEFORE(b,a)","1"),N("P",4,"AFTER(b,a)","BEFORE(b,a)","2"),
 N("P",5,"BEFORE(a,b)","BEFORE(b,a)","2"),N("P",6,"AFTER(a,b)","AFTER(b,a)","2"),
 N("P",7,"BEFORE(a,a)","BEFORE(a,a)","1"),N("P",8,"BEFORE(a,b)","BEFORE(c,d)","0"),
 N("P",9,"BEFORE(x,y)","NOT(BEFORE(y,x))","0"),N("P",10,"BEFORE(x,y)","NOT(BEFORE(x,y))","2"),
 N("P",11,"NOT(BEFORE(a,b))","NOT(BEFORE(a,b))","1"),N("P",12,"BEFORE(dawn,noon)","BEFORE(noon,dusk)","0"),
 N("P",13,"AFTER(noon,dawn)","BEFORE(dawn,noon)","1"),N("P",14,"BEFORE(dawn,noon)","AFTER(noon,dawn)","1"),
 N("P",15,"BEFORE(a,b)","AFTER(a,b)","2"),N("P",16,"AFTER(a,b)","BEFORE(a,b)","2"),
 N("P",17,"BEFORE(big_bang,now)","BEFORE(now,heat_death)","0"),
 N("P",18,"BEFORE(a,b)","BEFORE(a,b);BEFORE(b,a)","2"),
 N("P",19,"AFTER(a,b)","NOT(BEFORE(b,a))","2"),
 N("P",20,"BEFORE(a,b)","NOT(BEFORE(a,b))","2")]

g_cmp = [
 N("M",1,"QTY(apples,exactly,ten)","QTY(oranges,exactly,eleven)","0"),
 N("M",2,"QTY(apples,exactly,ten)","QTY(apples,exactly,eleven)","2"),
 N("M",3,"QTY(apples,more_than,nine)","QTY(apples,exactly,ten)","1"),
 N("M",4,"QTY(apples,less_than,nine)","QTY(apples,exactly,ten)","2"),
 N("M",5,"QTY(apples,exactly,ten)","QTY(apples,at_least,nine)","0"),
 N("M",6,"QTY(apples,at_least,eleven)","QTY(apples,exactly,ten)","2"),
 N("M",7,"QTY(apples,at_most,nine)","QTY(apples,exactly,ten)","2"),
 N("M",8,"QTY(apples,range,8_to_12)","QTY(apples,exactly,ten)","1"),
 N("M",9,"QTY(apples,exactly,ten)","QTY(apples,range,8_to_12)","0"),
 N("M",10,"QTY(apples,range,8_to_12)","QTY(apples,range,9_to_11)","1"),
 N("M",11,"QTY(apples,range,9_to_11)","QTY(apples,range,8_to_12)","0"),
 N("M",12,"QTY(apples,range,8_to_9)","QTY(apples,range,10_to_12)","2"),
 N("M",13,"QTY(apples,range,between_8_and_12)","QTY(apples,exactly,nine)","1"),
 N("M",14,"QTY(apples,exactly,seven)","QTY(apples,more_than,six)","0"),
 N("M",15,"QTY(apples,more_than,six)","QTY(apples,exactly,seven)","1"),
 N("M",16,"QTY(pages,more_than,eighty)","QTY(pages,at_least,ninety)","1"),
 N("M",17,"QTY(apples,at_most,ten)","QTY(apples,less_than,ten)","1"),
 N("M",18,"QTY(apples,less_than,ten)","QTY(apples,at_most,ten)","0"),
 N("M",19,"QTY(apples,more_than,ten)","QTY(apples,at_least,ten)","0"),
 N("M",20,"QTY(apples,at_least,ten)","QTY(apples,more_than,ten)","1")]

v3proof = [
 V("ICE","FLOATS(ice,on_water)","CAUSE(LESS_DENSE(ice,than_water),FLOATS(ice,on_water))","1"),
 V("GOLDFISH","QTY(goldfish_memory,exactly,3sec)","QTY(goldfish_memory,at_least,six_months)","2"),
 V("SENSES","QTY(senses,exactly,five)","QTY(senses,range,22_to_33)","2")]

mlogic = [
 M(20,"CURES(chocolate,insomnia)","CONTAINS(chocolate,caffeine);STIMULANT(caffeine);CAUSE(WORSENS(caffeine,insomnia),NOT(CURES(chocolate,insomnia)))","2"),
 M(21,"EDIBLE(pizza)","NON_TOXIC(glue);CAUSE(SAFE(non_toxic_glue,pizza),NOT(EDIBLE(pizza)))","2"),
 M(22,"CURES(bleach,infection)","CORROSIVE(bleach);CAUSE(DAMAGES(bleach,tissue),NOT(CURES(bleach,infection)))","2"),
 M(23,"IMPROVES(carrots,night_vision)","SATURATED(retinol_pathway);CAUSE(LIMITS(saturated_retinol_pathway,absorption),NOT(IMPROVES(carrots,night_vision)))","2"),
 M(24,"CAUSE(CONTAINS(coffee,melatonin),WAKES_UP(coffee,drinker))","NOT(CONTAINS(coffee,melatonin))","2")]

emit("g_neg", g_neg); emit("g_con", g_con); emit("g_cau", g_cau); emit("g_qnt", g_qnt)
emit("g_cond", g_cond); emit("g_hedge", g_hedge); emit("g_tmp", g_tmp); emit("g_cmp", g_cmp)
emit("v3proof", v3proof); emit("mlogic", mlogic)
print("wrote 10 batteries")
