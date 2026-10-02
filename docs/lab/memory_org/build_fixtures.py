#!/usr/bin/env python3
"""MORG crew 1: build frozen fixtures (corpus, holdout, queries) + validate.

All content is hand-authored and deterministic. No randomness anywhere.
Writes: corpus.txt, corpus_holdout.txt, queries.txt, queries_holdout.txt
into ~/workspace/morg/fixture/, then runs self-checks.
"""
import os
import re
import sys

OUT = os.path.expanduser("~/workspace/morg/fixture")


def ids(prefix, a, b):
    return ["%s%02d" % (prefix, i) for i in range(a, b + 1)]


# ---------------------------------------------------------------- corpus
# (id, domain, type, subject, text). 10 per type-block, in type blocks:
# 01-10 FACT, 11-20 CODE, 21-30 PROC, 31-40 QUOTE.
ITEMS = [
# ---- physics: FACT/gravity
("PH01","physics","FACT","gravity","Earth's surface gravity accelerates falling objects at about 9.8 meters per second squared, so a dropped stone gains roughly 9.8 m/s of speed each second."),
("PH02","physics","FACT","gravity","Newton's law of universal gravitation states that every mass attracts every other mass with a force proportional to the product of the masses and inversely proportional to the square of the distance."),
("PH03","physics","FACT","gravity","Astronauts on the Moon weigh about one sixth of their Earth weight because lunar surface gravity is only 1.62 meters per second squared."),
("PH04","physics","FACT","gravity","In a vacuum all objects fall at the same rate regardless of mass; a feather and a hammer dropped together on the Moon land at the same time, as Apollo 15 demonstrated."),
("PH05","physics","FACT","gravity","Tides are caused mainly by the Moon's gravity pulling unevenly on Earth's oceans, with the Sun's gravity adding a smaller secondary effect."),
("PH06","physics","FACT","gravity","A 1915 theory describes gravity not as a force but as the curvature of spacetime produced by mass and energy."),
("PH07","physics","FACT","gravity","Escape velocity from Earth's surface is about 11.2 kilometers per second; anything slower falls back under gravity."),
("PH08","physics","FACT","gravity","Gravitational time dilation means clocks run slightly slower in stronger gravity, so GPS satellites must correct for both their altitude and their speed."),
("PH09","physics","FACT","gravity","Jupiter's gravity is about 2.5 times Earth's, so a 70-kilogram person would weigh roughly 175 kilograms standing on its cloud tops."),
("PH10","physics","FACT","gravity","Cavendish first measured the gravitational constant G in 1798 with a torsion balance, weighing the Earth by measuring the tiny attraction between lead spheres."),
# ---- physics: CODE/orbits (short Zag snippets)
("PH11","physics","CODE","orbits","fn orbit_speed(mu:i64,r:i64)->i64 { return mu/r; } // toy circular orbit speed"),
("PH12","physics","CODE","orbits","fn orbit_period(a:i64,mu:i64)->i64 { return (6283*a*isqrt(a))/isqrt(mu); } // 2*pi*sqrt(a^3/mu)"),
("PH13","physics","CODE","orbits","fn hohmann_dv(r1:i64,r2:i64,mu:i64)->i64 { let a:i64=(r1+r2)/2; return isqrt(mu/r1)-isqrt(mu/a); }"),
("PH14","physics","CODE","orbits","fn escape_vel(mu:i64,r:i64)->i64 { return isqrt((2*mu)/r); }"),
("PH15","physics","CODE","orbits","fn orbit_energy(r:i64,v:i64,mu:i64)->i64 { return (v*v)/2-mu/r; }"),
("PH16","physics","CODE","orbits","fn hill_radius(a:i64,m:i64,mp:i64)->i64 { return a*(m/(3*mp)); } // toy, real form uses cube root"),
("PH17","physics","CODE","orbits","fn synodic(p1:i64,p2:i64)->i64 { return (p1*p2)/(p2-p1); } // days between alignments"),
("PH18","physics","CODE","orbits","fn plane_dv(v:i64,deg:i64)->i64 { return (2*v*deg)/115; } // toy plane-change cost"),
("PH19","physics","CODE","orbits","fn apoapsis(a:i64,e:i64)->i64 { return a*(100+e)/100; }"),
("PH20","physics","CODE","orbits","fn repeat_period(t:i64,rot:i64)->i64 { return (t*rot)/(rot-t); } // ground-track repeat"),
# ---- physics: PROC/pendulum (each mentions tempo of the swing)
("PH21","physics","PROC","pendulum","Hang a 1-meter string from a rigid support, attach a dense bob, pull it 10 degrees aside, and time the tempo of the swing over 20 full periods to measure g."),
("PH22","physics","PROC","pendulum","Keep the release angle under 15 degrees so the small-angle approximation holds and the tempo of the swing stays independent of amplitude."),
("PH23","physics","PROC","pendulum","Measure the string from pivot to bob center, since the tempo of the swing depends on this effective length, not the total string."),
("PH24","physics","PROC","pendulum","Use a photogate at the lowest point to record each crossing and compute the tempo of the swing without reaction-time error."),
("PH25","physics","PROC","pendulum","Repeat the timing for three different bob masses to confirm the tempo of the swing does not depend on mass."),
("PH26","physics","PROC","pendulum","Shorten the string in 10-centimeter steps, re-time the tempo of the swing each time, and plot period squared against length."),
("PH27","physics","PROC","pendulum","Damp air currents and use a heavy bob so air drag does not slow the tempo of the swing during the measurement window."),
("PH28","physics","PROC","pendulum","Count 50 zero-crossings instead of 10 full swings to halve the timing uncertainty in the tempo of the swing."),
("PH29","physics","PROC","pendulum","Level the support with a spirit level; a tilted pivot makes the bob trace an ellipse and corrupts the tempo of the swing."),
("PH30","physics","PROC","pendulum","Compare the measured tempo of the swing against 2*pi*sqrt(L/g) and report the percent error as your estimate of g."),
# ---- physics: QUOTE/einstein
("PH31","physics","QUOTE","einstein","\"Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world.\" - Albert Einstein"),
("PH32","physics","QUOTE","einstein","\"The important thing is not to stop questioning. Curiosity has its own reason for existing.\" - Albert Einstein"),
("PH33","physics","QUOTE","einstein","\"God does not play dice with the universe.\" - Albert Einstein"),
("PH34","physics","QUOTE","einstein","\"If you can't explain it simply, you don't understand it well enough.\" - Albert Einstein"),
("PH35","physics","QUOTE","einstein","\"A clever person solves a problem. A wise person avoids it.\" - Albert Einstein"),
("PH36","physics","QUOTE","einstein","\"The most beautiful experience we can have is the mysterious.\" - Albert Einstein"),
("PH37","physics","QUOTE","einstein","\"I have no special talents. I am only passionately curious.\" - Albert Einstein"),
("PH38","physics","QUOTE","einstein","\"Everything should be made as simple as possible, but not simpler.\" - Albert Einstein"),
("PH39","physics","QUOTE","einstein","\"Logic will get you from A to B. Imagination will take you everywhere.\" - Albert Einstein"),
("PH40","physics","QUOTE","einstein","\"Strive not to be a success, but rather to be of value.\" - Albert Einstein"),
# ---- cooking: FACT/culture (microbial cultures)
("CO01","cooking","FACT","culture","A bread starter culture is a symbiotic community of wild yeast and lactic-acid bacteria that leavens dough without commercial yeast."),
("CO02","cooking","FACT","culture","Yogurt culture converts milk lactose into lactic acid, which thickens the milk and gives yogurt its tang."),
("CO03","cooking","FACT","culture","A healthy starter culture doubles predictably after feeding; a sluggish rise signals the culture needs more frequent meals."),
("CO04","cooking","FACT","culture","Kefir grains are not grains at all but rubbery culture colonies of bacteria and yeast held together by kefiran."),
("CO05","cooking","FACT","culture","Cheese cultures determine flavor: mesophilic culture suits cheddar, thermophilic culture suits parmesan."),
("CO06","cooking","FACT","culture","The bacteria in a mature starter culture keep the dough acidic enough to suppress most spoilage microbes."),
("CO07","cooking","FACT","culture","Feeding a culture equal weights of flour and water keeps its hydration at 100 percent and its behavior predictable."),
("CO08","cooking","FACT","culture","Miso and soy sauce both begin as koji culture grown on rice or soybeans, then aged with salt."),
("CO09","cooking","FACT","culture","A starter culture peaks when it has just doubled; baking with it past collapse gives sour, weak loaves."),
("CO10","cooking","FACT","culture","Sanitation matters because an established culture resists invaders, but a new culture can be overtaken by mold."),
# ---- cooking: CODE/sourdough (Zag snippets)
("CO11","cooking","CODE","sourdough","fn sourdough_water(flour:i64)->i64 { return (flour*75)/100; } // 75 percent hydration"),
("CO12","cooking","CODE","sourdough","fn sourdough_salt(flour:i64)->i64 { return (flour*2)/100; } // 2 percent salt"),
("CO13","cooking","CODE","sourdough","fn sourdough_starter(flour:i64)->i64 { return (flour*20)/100; } // 20 percent ripe starter"),
("CO14","cooking","CODE","sourdough","fn scale_loaf(base:i64,loaves:i64)->i64 { return base*loaves; } // scale a sourdough formula"),
("CO15","cooking","CODE","sourdough","fn feed_ratio(starter:i64)->i64 { return starter*2; } // 1:2:2 feeding doubles flour and water"),
("CO16","cooking","CODE","sourdough","fn bulk_hours(temp:i64)->i64 { return 2400/temp; } // warmer kitchen, shorter bulk ferment"),
("CO17","cooking","CODE","sourdough","fn sourdough_total(flour:i64)->i64 { let w:i64=sourdough_water(flour); return flour+w+(flour/50); }"),
("CO18","cooking","CODE","sourdough","fn discard_bake(starter:i64)->i64 { return starter/2; } // keep half the ripe starter, feed the rest"),
("CO19","cooking","CODE","sourdough","fn loaf_yield(flour:i64,hyd:i64)->i64 { return flour+(flour*hyd)/100; }"),
("CO20","cooking","CODE","sourdough","fn starter_peak(hours:i64,fed:i64)->i64 { return fed+hours*2; } // toy sourdough readiness model"),
# ---- cooking: PROC/sourdough
("CO21","cooking","PROC","sourdough","Mix 500 grams of bread flour with 375 grams of water, rest one hour for autolyse, then add 100 grams of ripe sourdough starter and 10 grams of salt."),
("CO22","cooking","PROC","sourdough","Fold the sourdough dough every 30 minutes during bulk fermentation until it has grown about 50 percent and feels airy."),
("CO23","cooking","PROC","sourdough","Shape the sourdough into a tight round, place it seam-up in a floured banneton, and proof seam-side up."),
("CO24","cooking","PROC","sourdough","Cold-proof the shaped sourdough in the refrigerator for 12 to 16 hours to deepen flavor before baking."),
("CO25","cooking","PROC","sourdough","Preheat a Dutch oven at 250 C for 45 minutes, then lower the sourdough in on parchment and bake covered for 20 minutes."),
("CO26","cooking","PROC","sourdough","Uncover for the final 20 minutes so the sourdough crust sets deeply brown, then cool on a rack for at least one hour before slicing."),
("CO27","cooking","PROC","sourdough","Feed the starter with equal weights flour and water twice daily for three days before a sourdough bake to ensure peak vigor."),
("CO28","cooking","PROC","sourdough","Test sourdough readiness with the float test: a spoonful of starter that floats in water is ready to leaven."),
("CO29","cooking","PROC","sourdough","Score the sourdough loaf with a lame at a shallow angle just before baking to control the ear and the bloom."),
("CO30","cooking","PROC","sourdough","Store baked sourdough cut-side down on a board for two days; never refrigerate the crumb or it stales faster."),
# ---- cooking: QUOTE/escoffier
("CO31","cooking","QUOTE","escoffier","\"Good food is the foundation of genuine happiness.\" - Auguste Escoffier"),
("CO32","cooking","QUOTE","escoffier","\"The greatest dishes are very simple.\" - Auguste Escoffier"),
("CO33","cooking","QUOTE","escoffier","\"Faites simple: in cooking, simplicity is the hardest skill.\" - Auguste Escoffier"),
("CO34","cooking","QUOTE","escoffier","\"A sauce must coat the back of a spoon and justify its flavor.\" - Auguste Escoffier"),
("CO35","cooking","QUOTE","escoffier","\"Respect the product; the cook's first duty is to the ingredient.\" - Auguste Escoffier"),
("CO36","cooking","QUOTE","escoffier","\"Order in the kitchen is order on the plate.\" - Auguste Escoffier"),
("CO37","cooking","QUOTE","escoffier","\"Never serve a dish you would not eat yourself.\" - Auguste Escoffier"),
("CO38","cooking","QUOTE","escoffier","\"The brigade works because every station owns its fire.\" - Auguste Escoffier"),
("CO39","cooking","QUOTE","escoffier","\"Season with judgment, not with habit.\" - Auguste Escoffier"),
("CO40","cooking","QUOTE","escoffier","\"A calm kitchen makes calm food.\" - Auguste Escoffier"),

# ---- coding: FACT/loops
("CD01","coding","FACT","loops","A for loop repeats a block a known number of times, while a while loop repeats until its condition turns false."),
("CD02","coding","FACT","loops","Off-by-one errors are the classic loop bug: iterating one step too many or too few at the boundary."),
("CD03","coding","FACT","loops","Loop unrolling trades code size for speed by writing out several iterations explicitly to cut branch overhead."),
("CD04","coding","FACT","loops","An infinite loop runs forever when its exit condition can never become true; every loop needs a reachable exit."),
("CD05","coding","FACT","loops","Nested loops multiply their iteration counts, so two loops of size n perform n-squared inner steps."),
("CD06","coding","FACT","loops","A loop invariant is a claim that stays true on every iteration and is the key to proving a loop correct."),
("CD07","coding","FACT","loops","Iterators abstract loops away: the loop logic lives in the collection, and the caller just asks for the next item."),
("CD08","coding","FACT","loops","In functional code, recursion or folds replace explicit loops, moving the repetition into the function itself."),
("CD09","coding","FACT","loops","Vectorized operations replace tight loops with single array-wide instructions that run far faster."),
("CD10","coding","FACT","loops","Breaking out of a loop early with break, or skipping one pass with continue, keeps loop bodies readable."),
# ---- coding: CODE/loops (Zag snippets)
("CD11","coding","CODE","loops","fn sum_loop(n:i64)->i64 { let s:i64=0; let i:i64=0; while i<n { s=s+i; i=i+1; } return s; }"),
("CD12","coding","CODE","loops","fn find_loop(a:[]i64,t:i64)->i64 { let i:i64=0; while i<len(a) { if a[i]==t { return i; } i=i+1; } return -1; }"),
("CD13","coding","CODE","loops","fn count_even(n:i64)->i64 { let c:i64=0; let i:i64=0; while i<n { if i%2==0 { c=c+1; } i=i+1; } return c; }"),
("CD14","coding","CODE","loops","fn loop_copy(dst:[]u8,src:[]u8,n:i64)->void { let i:i64=0; while i<n { dst[i]=src[i]; i=i+1; } return; }"),
("CD15","coding","CODE","loops","fn fact_loop(n:i64)->i64 { let f:i64=1; let i:i64=2; while i<=n { f=f*i; i=i+1; } return f; }"),
("CD16","coding","CODE","loops","fn nested_loops(n:i64)->i64 { let c:i64=0; let i:i64=0; while i<n { let j:i64=0; while j<n { c=c+1; j=j+1; } i=i+1; } return c; }"),
("CD17","coding","CODE","loops","fn loop_max(a:[]i64,n:i64)->i64 { let m:i64=a[0]; let i:i64=1; while i<n { if a[i]>m { m=a[i]; } i=i+1; } return m; }"),
("CD18","coding","CODE","loops","fn countdown(n:i64)->void { let i:i64=n; while i>0 { i=i-1; } return; }"),
("CD19","coding","CODE","loops","fn loop_stride(a:[]i64,n:i64,s:i64)->i64 { let t:i64=0; let i:i64=0; while i<n { t=t+a[i]; i=i+s; } return t; }"),
("CD20","coding","CODE","loops","fn retry_loop(tries:i64)->i64 { let i:i64=0; while i<tries { i=i+1; } return i; } // bounded attempts"),
# ---- coding: PROC/debugging
("CD21","coding","PROC","debugging","Reproduce the bug reliably first: debugging without a repeatable trigger is guessing."),
("CD22","coding","PROC","debugging","Read the error message literally before theorizing; most debugging sessions end at step one of the stack trace."),
("CD23","coding","PROC","debugging","Bisect the input: halve the failing case until the smallest input that still triggers the bug remains."),
("CD24","coding","PROC","debugging","Add one print at the decision point, not twenty; debugging is a binary search, not a flood."),
("CD25","coding","PROC","debugging","Check your assumptions with asserts: the bug in debugging is usually a belief, not a line."),
("CD26","coding","PROC","debugging","Change one thing at a time and re-run; two simultaneous fixes teach you nothing about the bug."),
("CD27","coding","PROC","debugging","Explain the code to a rubber duck; half of all debugging ends mid-sentence."),
("CD28","coding","PROC","debugging","When stuck, delete the clever code and rewrite it plainly; debugging rewards the boring version."),
("CD29","coding","PROC","debugging","Verify the fix on the original failing input, then on the full suite; debugging is not done at green-on-one."),
("CD30","coding","PROC","debugging","Write the regression test before closing the ticket so the bug can never silently return."),
# ---- coding: QUOTE/dijkstra
("CD31","coding","QUOTE","dijkstra","\"Computer science is no more about computers than astronomy is about telescopes.\" - Edsger Dijkstra"),
("CD32","coding","QUOTE","dijkstra","\"Simplicity is prerequisite for reliability.\" - Edsger Dijkstra"),
("CD33","coding","QUOTE","dijkstra","\"Program testing can be used to show the presence of bugs, but never to show their absence!\" - Edsger Dijkstra"),
("CD34","coding","QUOTE","dijkstra","\"The competent programmer is fully aware of the strictly limited size of his own skull.\" - Edsger Dijkstra"),
("CD35","coding","QUOTE","dijkstra","\"The most effective programmers are those who do not introduce the bugs to start with.\" - Edsger Dijkstra"),
("CD36","coding","QUOTE","dijkstra","\"Elegance is not a dispensable luxury but a factor that decides between success and failure.\" - Edsger Dijkstra"),
("CD37","coding","QUOTE","dijkstra","\"The question of whether a computer can think is no more interesting than the question of whether a submarine can swim.\" - Edsger Dijkstra"),
("CD38","coding","QUOTE","dijkstra","\"Object-oriented programming is an exceptionally bad idea which could only have originated in California.\" - Edsger Dijkstra"),
("CD39","coding","QUOTE","dijkstra","\"The use of COBOL cripples the mind; its teaching should, therefore, be regarded as a criminal offense.\" - Edsger Dijkstra"),
("CD40","coding","QUOTE","dijkstra","\"It is not the task of the University to offer what society asks for, but to give what society needs.\" - Edsger Dijkstra"),
# ---- history: FACT/culture (human cultures)
("HI01","history","FACT","culture","The Sumerian culture of ancient Mesopotamia invented writing, the wheel, and the 60-based number system still used in clocks."),
("HI02","history","FACT","culture","Minoan culture on Crete built Europe's first palaces with running water around 1700 BCE, centuries before Mycenae rose."),
("HI03","history","FACT","culture","The Mississippian culture raised the great mound city of Cahokia near modern St. Louis, home to perhaps 20,000 people by 1100 CE."),
("HI04","history","FACT","culture","Nok culture in West Africa smelted iron as early as 500 BCE and left haunting terracotta sculptures across Nigeria."),
("HI05","history","FACT","culture","The Vinca culture of southeast Europe used proto-writing symbols nearly two thousand years before Sumerian cuneiform."),
("HI06","history","FACT","culture","Andean Chavin culture united highland Peru through a shared religion a thousand years before the Inca empire."),
("HI07","history","FACT","culture","The Harappan culture planned its Indus cities on grids with covered drains while most of the world lived in villages."),
("HI08","history","FACT","culture","Scythian steppe culture buried its warriors with gold and horses across a grassland empire stretching from Hungary to China."),
("HI09","history","FACT","culture","The Jomon culture of Japan made the world's oldest known pottery, starting around 14,000 BCE."),
("HI10","history","FACT","culture","Great Zimbabwe's stone-walled Shona culture traded gold and ivory with Swahili merchants a thousand years ago."),
# ---- history: CODE/ciphers (Zag snippets)
("HI11","history","CODE","ciphers","fn caesar(b:u8,k:u8)->u8 { return ((b-65+k)%26)+65; } // Caesar cipher on A-Z"),
("HI12","history","CODE","ciphers","fn caesar_dec(b:u8,k:u8)->u8 { return ((b-65+26-k)%26)+65; }"),
("HI13","history","CODE","ciphers","fn rot13(b:u8)->u8 { return caesar(b,13); }"),
("HI14","history","CODE","ciphers","fn vigenere(b:u8,k:u8)->u8 { return ((b-65+k)%26)+65; } // key byte advances per letter"),
("HI15","history","CODE","ciphers","fn atbash(b:u8)->u8 { return 90-(b-65); } // A<->Z mirror cipher"),
("HI16","history","CODE","ciphers","fn xor_byte(b:u8,k:u8)->u8 { return b^k; } // one-time pad on a single byte"),
("HI17","history","CODE","ciphers","fn rail_fence(n:i64,r:i64)->i64 { return n%((r-1)*2); } // rail index for a zigzag cipher"),
("HI18","history","CODE","ciphers","fn col_transpose(n:i64,cols:i64)->i64 { return (n%cols)*1000+n/cols; } // toy columnar key"),
("HI19","history","CODE","ciphers","fn polybius(r:i64,c:i64)->i64 { return r*10+c; } // letter as row-column pair"),
("HI20","history","CODE","ciphers","fn cipher_sum(msg:[]u8,n:i64)->i64 { let s:i64=0; let i:i64=0; while i<n { s=s+msg[i]; i=i+1; } return s%26; }"),
# ---- history: PROC/siege
("HI21","history","PROC","siege","Surround the fortress first: a siege begins by cutting every road so no food or messenger gets through."),
("HI22","history","PROC","siege","Dig circumvallation trenches facing outward too, since every long siege invites a relieving army."),
("HI23","history","PROC","siege","Build siege towers taller than the wall so archers can sweep the ramparts before the ram advances."),
("HI24","history","PROC","siege","Undermine the wall by tunneling beneath it, propping the tunnel with timbers, then burning the props to collapse the masonry."),
("HI25","history","PROC","siege","Starve, don't storm: a patient siege costs fewer lives than one assault against unbroken walls."),
("HI26","history","PROC","siege","Poison or divert the water supply early; thirst breaks a siege faster than any engine."),
("HI27","history","PROC","siege","Keep the camp sanitary during a long siege, because disease has killed more besiegers than sorties ever have."),
("HI28","history","PROC","siege","Offer terms before the final assault; a city that surrenders a siege intact can be taxed, a sacked one cannot."),
("HI29","history","PROC","siege","Rotate the watch in thirds so the siege lines stay alert through every night of the blockade."),
("HI30","history","PROC","siege","Record the grain stores captured when the siege ends; the garrison's remaining food measures how close the walls came to holding."),
# ---- history: QUOTE/churchill
("HI31","history","QUOTE","churchill","\"We shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields and in the streets.\" - Winston Churchill"),
("HI32","history","QUOTE","churchill","\"If you're going through hell, keep going.\" - Winston Churchill"),
("HI33","history","QUOTE","churchill","\"Success is not final, failure is not fatal: it is the courage to continue that counts.\" - Winston Churchill"),
("HI34","history","QUOTE","churchill","\"Never in the field of human conflict was so much owed by so many to so few.\" - Winston Churchill"),
("HI35","history","QUOTE","churchill","\"A pessimist sees the difficulty in every opportunity; an optimist sees the opportunity in every difficulty.\" - Winston Churchill"),
("HI36","history","QUOTE","churchill","\"We make a living by what we get, but we make a life by what we give.\" - Winston Churchill"),
("HI37","history","QUOTE","churchill","\"To improve is to change; to be perfect is to change often.\" - Winston Churchill"),
("HI38","history","QUOTE","churchill","\"History will be kind to me for I intend to write it.\" - Winston Churchill"),
("HI39","history","QUOTE","churchill","\"The price of greatness is responsibility.\" - Winston Churchill"),
("HI40","history","QUOTE","churchill","\"Continuous effort - not strength or intelligence - is the key to unlocking our potential.\" - Winston Churchill"),
# ---- gardening: FACT/tomatoes
("GA01","gardening","FACT","tomatoes","Tomatoes are berries botanically, and they originated as tiny wild fruits in the coastal Andes of South America."),
("GA02","gardening","FACT","tomatoes","Tomato seedlings need soil above 15 C to thrive; cold soil stalls tomatoes far more than cold air."),
("GA03","gardening","FACT","tomatoes","Indeterminate tomatoes keep growing and fruiting until frost, while determinate tomatoes set one main crop and stop."),
("GA04","gardening","FACT","tomatoes","Tomatoes are heavy feeders: they want rich compost at planting and steady potassium once fruits begin to swell."),
("GA05","gardening","FACT","tomatoes","Blossom-end rot in tomatoes is a calcium-uptake failure caused by uneven watering, not by poor soil alone."),
("GA06","gardening","FACT","tomatoes","Companion basil is said to improve tomato flavor, though the proven benefit is that basil repels tomato hornworm moths."),
("GA07","gardening","FACT","tomatoes","Tomatoes ripen best on the vine, but a mature-green tomato picked before frost will finish ripening indoors."),
("GA08","gardening","FACT","tomatoes","Heirloom tomatoes breed true from saved seed, while hybrid tomatoes split into unpredictable offspring next year."),
("GA09","gardening","FACT","tomatoes","Pruning suckers on indeterminate tomatoes focuses energy on fewer, larger fruits and improves airflow against blight."),
("GA10","gardening","FACT","tomatoes","Tomatoes were feared as poisonous in 18th-century Europe because their leaves resemble deadly nightshade."),
# ---- gardening: CODE/irrigation (Zag snippets; gravity-fed)
("GA11","gardening","CODE","irrigation","fn drip_minutes(area:i64,rate:i64)->i64 { return (area*10)/rate; } // gravity-fed drip lines"),
("GA12","gardening","CODE","irrigation","fn gravity_head(h:i64)->i64 { return h*10; } // toy pressure from gravity head in meters"),
("GA13","gardening","CODE","irrigation","fn water_need(temp:i64,plants:i64)->i64 { return (temp*plants)/25; } // liters per day"),
("GA14","gardening","CODE","irrigation","fn gravity_flow(d:i64,h:i64)->i64 { return (d*d*h)/100; } // toy gravity-fed pipe flow"),
("GA15","gardening","CODE","irrigation","fn zone_time(zone:i64)->i64 { return zone*15; } // minutes per irrigation zone"),
("GA16","gardening","CODE","irrigation","fn rain_skip(rain:i64)->i64 { if rain>5 { return 1; } return 0; } // skip watering after rain"),
("GA17","gardening","CODE","irrigation","fn gravity_tank(liters:i64)->i64 { return liters/200; } // barrels for a gravity-fed system"),
("GA18","gardening","CODE","irrigation","fn emitter_count(row:i64,spacing:i64)->i64 { return (row*100)/spacing; }"),
("GA19","gardening","CODE","irrigation","fn soak_days(clay:i64)->i64 { return 2+clay; } // clay soil waters less often"),
("GA20","gardening","CODE","irrigation","fn pump_or_gravity(head:i64)->i64 { if head>3 { return 0; } return 1; } // 0 means gravity suffices"),
# ---- gardening: PROC/tomatoes
("GA21","gardening","PROC","tomatoes","Start tomato seeds indoors six weeks before last frost, sowing a quarter inch deep in warm seed mix."),
("GA22","gardening","PROC","tomatoes","Harden tomato seedlings off over ten days, adding an hour of outdoor sun daily before transplanting."),
("GA23","gardening","PROC","tomatoes","Plant tomatoes deep, burying two thirds of the stem; the buried stem sprouts extra roots for stronger tomatoes."),
("GA24","gardening","PROC","tomatoes","Mulch tomatoes with straw after the soil warms to hold moisture and stop soil splashing onto leaves."),
("GA25","gardening","PROC","tomatoes","Water tomatoes at the base every morning; wet foliage invites the blight that ruins tomatoes by August."),
("GA26","gardening","PROC","tomatoes","Stake or cage tomatoes at planting time so you never spear established roots later."),
("GA27","gardening","PROC","tomatoes","Pinch suckers on indeterminate tomatoes weekly, keeping one or two main stems for the biggest harvest."),
("GA28","gardening","PROC","tomatoes","Feed tomatoes with compost tea every two weeks once the first fruits reach marble size."),
("GA29","gardening","PROC","tomatoes","Pick tomatoes at breaker stage during heat waves; they ripen indoors without cracking."),
("GA30","gardening","PROC","tomatoes","Pull spent tomato vines at season end and rotate the bed; never plant tomatoes where tomatoes grew last year."),
# ---- gardening: QUOTE/burbank
("GA31","gardening","QUOTE","burbank","\"Flowers always make people better, happier, and more helpful; they are sunshine, food and medicine for the soul.\" - Luther Burbank"),
("GA32","gardening","QUOTE","burbank","\"The secret of improved plant breeding, apart from scientific knowledge, is love.\" - Luther Burbank"),
("GA33","gardening","QUOTE","burbank","\"If we had paid no more attention to our plants than we have to our children, we would now be living in a jungle of weed.\" - Luther Burbank"),
("GA34","gardening","QUOTE","burbank","\"A garden is the slowest of the performing arts.\" - Luther Burbank"),
("GA35","gardening","QUOTE","burbank","\"Heredity is the sum of all past environments; the breeder who ignores it breeds blind.\" - Luther Burbank"),
("GA36","gardening","QUOTE","burbank","\"Select the best, reject the rest, and never stop selecting.\" - Luther Burbank"),
("GA37","gardening","QUOTE","burbank","\"Nature teaches the patient breeder more than any book.\" - Luther Burbank"),
("GA38","gardening","QUOTE","burbank","\"Every seed holds a thousand possible plants; the breeder chooses which one the world sees.\" - Luther Burbank"),
("GA39","gardening","QUOTE","burbank","\"Cross widely, grow largely, and let the plants show you what they can become.\" - Luther Burbank"),
("GA40","gardening","QUOTE","burbank","\"The plant breeder's work is never finished, only handed on.\" - Luther Burbank"),
# ---- music: FACT/loops
("MU01","music","FACT","loops","A loop in electronic music is a short repeating phrase, often one to four bars, layered to build a track."),
("MU02","music","FACT","loops","Live looping lets a solo performer record a phrase and replay it instantly as a backing loop."),
("MU03","music","FACT","loops","Hip-hop was born from DJs extending the break: looping the funkiest bars of a record for dancers."),
("MU04","music","FACT","loops","A well-cut loop hides its seam by starting and ending on the same beat with matched phase."),
("MU05","music","FACT","loops","Tape loops in the 1960s let composers repeat fragments by splicing magnetic tape into literal circles."),
("MU06","music","FACT","loops","Ostinato is the classical ancestor of the loop: a stubbornly repeating figure under changing harmony."),
("MU07","music","FACT","loops","Loop-based arranging trades linear songwriting for stacking: the loop stays fixed while textures evolve."),
("MU08","music","FACT","loops","Quantize settings snap a recorded loop to the grid, fixing sloppy timing but risking a robotic feel."),
("MU09","music","FACT","loops","Ambient pioneers built entire pieces from a few long loops drifting slowly out of sync."),
("MU10","music","FACT","loops","Copyright law treats a sampled loop as a use of the original recording, no matter how short the loop."),
# ---- music: CODE/tempo (Zag snippets; pendulum metronome)
("MU11","music","CODE","tempo","fn beat_ms(bpm:i64)->i64 { return 60000/bpm; } // pendulum metronome tick"),
("MU12","music","CODE","tempo","fn pendulum_bpm(length:i64)->i64 { return 6000/length; } // toy metronome pendulum"),
("MU13","music","CODE","tempo","fn swing_ms(bpm:i64)->i64 { return (60000/bpm)*2/3; } // triplet swing delay"),
("MU14","music","CODE","tempo","fn tap_tempo(t1:i64,t2:i64)->i64 { return 60000/(t2-t1); }"),
("MU15","music","CODE","tempo","fn pendulum_ticks(len:i64,n:i64)->i64 { return (6000/len)*n; } // n metronome ticks"),
("MU16","music","CODE","tempo","fn bar_ms(bpm:i64,beats:i64)->i64 { return (60000/bpm)*beats; }"),
("MU17","music","CODE","tempo","fn bpm_from_period(p:i64)->i64 { return 60000/p; } // pendulum period to tempo"),
("MU18","music","CODE","tempo","fn ritard(bpm:i64,bars:i64)->i64 { return bpm-(bars*4); } // toy slowdown"),
("MU19","music","CODE","tempo","fn metro_subdiv(bpm:i64,sub:i64)->i64 { return 60000/(bpm*sub); }"),
("MU20","music","CODE","tempo","fn pendulum_sync(a:i64,b:i64)->i64 { return (a*b)/(b-a); } // two pendulums align"),
# ---- music: PROC/tuning
("MU21","music","PROC","tuning","Tune the A string to 440 Hz first, then tune every other string to the A by matching beats."),
("MU22","music","PROC","tuning","Stretch new strings firmly before tuning; unstretched strings drift flat within minutes."),
("MU23","music","PROC","tuning","Tune up to the note, never down: approaching pitch from below keeps the tuning peg seated."),
("MU24","music","PROC","tuning","Check tuning with harmonics at the 12th fret to expose intonation errors the open string hides."),
("MU25","music","PROC","tuning","Let the instrument acclimate to the room for twenty minutes before a final tuning pass."),
("MU26","music","PROC","tuning","Tune pianos from the middle outward, setting the temperament octave before stretching the extremes."),
("MU27","music","PROC","tuning","Silence the room before tuning; even quiet HVAC hum masks the beats you tune by."),
("MU28","music","PROC","tuning","Re-check tuning after the first loud passage; heat and force move fresh strings sharp."),
("MU29","music","PROC","tuning","Mark the bridge position with tape when changing strings so intonation survives the tuning."),
("MU30","music","PROC","tuning","Tune drums by tapping near each lug and evening the pitch around the head before touching the snare."),
# ---- music: QUOTE/mozart
("MU31","music","QUOTE","mozart","\"Neither a lofty degree of intelligence nor imagination nor both together go to the making of genius. Love, love, love, that is the soul of genius.\" - Wolfgang Amadeus Mozart"),
("MU32","music","QUOTE","mozart","\"I pay no attention whatever to anybody's praise or blame. I simply follow my own feelings.\" - Wolfgang Amadeus Mozart"),
("MU33","music","QUOTE","mozart","\"The music is not in the notes, but in the silence between.\" - attributed to Wolfgang Amadeus Mozart"),
("MU34","music","QUOTE","mozart","\"When I am traveling in a carriage, or walking after a good meal, thoughts crowd into my mind.\" - Wolfgang Amadeus Mozart"),
("MU35","music","QUOTE","mozart","\"To talk well and eloquently is a very great art, but an equally great one is to know the right moment to stop.\" - Wolfgang Amadeus Mozart"),
("MU36","music","QUOTE","mozart","\"I thank my God for graciously granting me the opportunity of learning that death is the key which unlocks the door to our true happiness.\" - Wolfgang Amadeus Mozart"),
("MU37","music","QUOTE","mozart","\"It is a mistake to think that the practice of my art has become easy to me.\" - Wolfgang Amadeus Mozart"),
("MU38","music","QUOTE","mozart","\"One must not make oneself cheap.\" - Wolfgang Amadeus Mozart"),
("MU39","music","QUOTE","mozart","\"People err who think my art comes easily to me.\" - Wolfgang Amadeus Mozart"),
("MU40","music","QUOTE","mozart","\"The passions, whether violent or not, should never be so expressed as to reach the point of causing disgust.\" - Wolfgang Amadeus Mozart"),
]

# ---------------------------------------------------------------- queries
# (qid, split, class, thint, dhint, shint, text, gold_ids)
QUERIES = [
# ---- PURE calib (type-pure: thint+dhint set)
("Q01","calib","PURE","FACT","physics","gravity","show me FACT items about gravity in physics",ids("PH",1,10)),
("Q02","calib","PURE","CODE","cooking","sourdough","show me CODE about sourdough in cooking",ids("CO",11,20)),
("Q03","calib","PURE","QUOTE","coding","dijkstra","show me QUOTE items by dijkstra in coding",ids("CD",31,40)),
("Q04","calib","PURE","PROC","history","siege","show me PROC items about siege in history",ids("HI",21,30)),
("Q05","calib","PURE","FACT","gardening","tomatoes","show me FACT items about tomatoes in gardening",ids("GA",1,10)),
("Q06","calib","PURE","CODE","music","tempo","show me CODE about tempo in music",ids("MU",11,20)),
("Q07","calib","PURE","QUOTE","physics","einstein","show me QUOTE items by einstein in physics",ids("PH",31,40)),
("Q08","calib","PURE","FACT","coding","loops","show me FACT items about loops in coding",ids("CD",1,10)),
# ---- PURE test (type-pure)
("Q09","test","PURE","CODE","physics","orbits","show me CODE about orbits in physics",ids("PH",11,20)),
("Q10","test","PURE","QUOTE","cooking","escoffier","show me QUOTE items by escoffier in cooking",ids("CO",31,40)),
("Q11","test","PURE","CODE","coding","loops","show me CODE about loops in coding",ids("CD",11,20)),
("Q12","test","PURE","FACT","history","culture","show me FACT items about culture in history",ids("HI",1,10)),
("Q13","test","PURE","PROC","gardening","tomatoes","show me PROC items about tomatoes in gardening",ids("GA",21,30)),
("Q14","test","PURE","FACT","music","loops","show me FACT items about loops in music",ids("MU",1,10)),
("Q15","test","PURE","QUOTE","history","churchill","show me QUOTE items by churchill in history",ids("HI",31,40)),
("Q16","test","PURE","FACT","cooking","culture","show me FACT items about culture in cooking",ids("CO",1,10)),
# ---- PURE test (domain-pure: dhint set, thint/shint empty)
("Q17","test","PURE","","physics","","everything in the physics domain",ids("PH",1,40)),
("Q18","test","PURE","","cooking","","everything in the cooking domain",ids("CO",1,40)),
("Q19","test","PURE","","coding","","everything in the coding domain",ids("CD",1,40)),
("Q20","test","PURE","","history","","everything in the history domain",ids("HI",1,40)),
("Q21","test","PURE","","gardening","","everything in the gardening domain",ids("GA",1,40)),
("Q22","test","PURE","","music","","everything in the music domain",ids("MU",1,40)),
("Q23","test","PURE","","physics","","all physics items",ids("PH",1,40)),
("Q24","test","PURE","","music","","all music items",ids("MU",1,40)),
# ---- SUBJ calib (shint set, thint empty)
("Q25","calib","SUBJ","","","sourdough","everything about sourdough",ids("CO",11,30)),
("Q26","calib","SUBJ","","","loops","everything about loops",ids("CD",1,20)+ids("MU",1,10)),
("Q27","calib","SUBJ","","","culture","everything about culture",ids("CO",1,10)+ids("HI",1,10)),
("Q28","calib","SUBJ","","","tomatoes","everything about tomatoes",ids("GA",1,10)+ids("GA",21,30)),
# ---- SUBJ test
("Q29","test","SUBJ","","","gravity","everything about gravity",ids("PH",1,10)),
("Q30","test","SUBJ","","","orbits","everything about orbits",ids("PH",11,20)),
("Q31","test","SUBJ","","","einstein","everything about einstein",ids("PH",31,40)),
("Q32","test","SUBJ","","","dijkstra","everything about dijkstra",ids("CD",31,40)),
("Q33","test","SUBJ","","","siege","everything about siege",ids("HI",21,30)),
("Q34","test","SUBJ","","","churchill","everything about churchill",ids("HI",31,40)),
("Q35","test","SUBJ","","","tuning","everything about tuning",ids("MU",21,30)),
("Q36","test","SUBJ","","","debugging","everything about debugging",ids("CD",21,30)),
# ---- AMBIG calib (hints empty)
("Q37","calib","AMBIG","","","","loops",ids("CD",1,20)+ids("MU",1,10)),
("Q38","calib","AMBIG","","","","culture",ids("CO",1,10)+ids("HI",1,10)),
("Q39","calib","AMBIG","","","","pendulum",ids("PH",21,30)+ids("MU",11,20)),
("Q40","calib","AMBIG","","","","gravity",ids("PH",1,10)+ids("GA",11,20)),
# ---- AMBIG test (hints empty or misleading)
("Q41","test","AMBIG","QUOTE","","","loops",ids("CD",1,20)+ids("MU",1,10)),
("Q42","test","AMBIG","","gardening","","audio loops and code loops",ids("CD",1,20)+ids("MU",1,10)),
("Q43","test","AMBIG","","physics","","culture",ids("CO",1,10)+ids("HI",1,10)),
("Q44","test","AMBIG","CODE","","","starter culture and ancient culture",ids("CO",1,10)+ids("HI",1,10)),
("Q45","test","AMBIG","","cooking","","pendulum",ids("PH",21,30)+ids("MU",11,20)),
("Q46","test","AMBIG","QUOTE","","","gravity",ids("PH",1,10)+ids("GA",11,20)),
("Q47","test","AMBIG","","","","tempo",ids("MU",11,20)+ids("PH",21,30)),
("Q48","test","AMBIG","","history","","the tempo of a swinging pendulum",ids("PH",21,30)+ids("MU",11,20)),
]

# ---------------------------------------------------------------- holdout corpus
HOLDOUT_ITEMS = [
# ---- astronomy: FACT/blackholes
("AS01","astronomy","FACT","blackholes","A black hole forms when a massive star collapses past its Schwarzschild radius, trapping even light inside the event horizon."),
("AS02","astronomy","FACT","blackholes","Stellar black holes weigh a few to a few dozen suns; supermassive black holes weigh millions to billions."),
("AS03","astronomy","FACT","blackholes","Cygnus X-1 was the first widely accepted black hole, found by its X-ray glow as it strips gas from a companion star."),
("AS04","astronomy","FACT","blackholes","Time appears to freeze at a black hole's event horizon as seen from far away, though an infaller crosses it uneventfully."),
("AS05","astronomy","FACT","blackholes","The Milky Way's central black hole, Sagittarius A*, weighs about four million suns and was imaged as a glowing ring in 2022."),
("AS06","astronomy","FACT","blackholes","Hawking radiation predicts black holes slowly evaporate, with smaller black holes evaporating faster."),
("AS07","astronomy","FACT","blackholes","Black hole mergers ring spacetime like a bell; LIGO heard the first such chirp in September 2015."),
("AS08","astronomy","FACT","blackholes","Quasars are supermassive black holes feeding so fiercely that one outshines its entire host galaxy."),
("AS09","astronomy","FACT","blackholes","The no-hair theorem says a black hole is fully described by just mass, spin, and charge."),
("AS10","astronomy","FACT","blackholes","Tidal forces near a small black hole would spaghettify an astronaut long before the horizon; near a giant one, the crossing is gentle."),
# ---- astronomy: CODE/orbits (same subject key as physics CODE)
("AS11","astronomy","CODE","orbits","fn kepler3(a:i64)->i64 { return (a*a*a)/1000; } // orbital period from semi-major axis"),
("AS12","astronomy","CODE","orbits","fn orbit_speed2(mu:i64,r:i64)->i64 { return mu/r; } // toy circular orbit"),
("AS13","astronomy","CODE","orbits","fn transfer_dv(r1:i64,r2:i64)->i64 { return (r2-r1)/100; } // toy Hohmann cost"),
("AS14","astronomy","CODE","orbits","fn hill_r(a:i64,m:i64)->i64 { return a*m/300; } // toy sphere of influence"),
("AS15","astronomy","CODE","orbits","fn synodic2(p1:i64,p2:i64)->i64 { return (p1*p2)/(p2-p1); }"),
("AS16","astronomy","CODE","orbits","fn escape2(mu:i64,r:i64)->i64 { return (2*mu)/r; }"),
("AS17","astronomy","CODE","orbits","fn phase_angle(t:i64,p:i64)->i64 { return (t*360)/p; } // degrees along the orbit"),
("AS18","astronomy","CODE","orbits","fn node_precess(a:i64,e:i64)->i64 { return (a*e)/500; } // toy nodal drift"),
("AS19","astronomy","CODE","orbits","fn vis_viva2(r:i64,a:i64,mu:i64)->i64 { return mu*((2*100)/r-100/a); } // scaled"),
("AS20","astronomy","CODE","orbits","fn orbit_count(days:i64,p:i64)->i64 { return days/p; } // whole orbits elapsed"),
# ---- astronomy: PROC/telescope
("AS21","astronomy","PROC","telescope","Set the telescope on level ground and let the optics reach ambient temperature for 30 minutes before observing."),
("AS22","astronomy","PROC","telescope","Align the finderscope on a distant daytime target so the telescope points where the finder says it does."),
("AS23","astronomy","PROC","telescope","Start every session with the lowest-power eyepiece; center the target before increasing telescope magnification."),
("AS24","astronomy","PROC","telescope","Balance the telescope tube in its mount so a fingertip moves it; stiff motion ruins fine tracking."),
("AS25","astronomy","PROC","telescope","Collimate a reflector by centering the secondary under the focuser, then aligning the primary to it."),
("AS26","astronomy","PROC","telescope","Shield the telescope from direct wind and local heat sources; rising air blurs the image more than cheap optics."),
("AS27","astronomy","PROC","telescope","Log each observation with date, time, seeing, and eyepiece so the telescope's history compounds."),
("AS28","astronomy","PROC","telescope","Clean optics only with air and distilled water; a scratched telescope mirror never recovers."),
("AS29","astronomy","PROC","telescope","Polar-align an equatorial mount by pointing its axis at Polaris before attempting long exposures."),
("AS30","astronomy","PROC","telescope","Cover the telescope and cap the eyepieces at session end; dew left overnight grows fungus on lenses."),
# ---- astronomy: QUOTE/sagan
("AS31","astronomy","QUOTE","sagan","\"We are a way for the cosmos to know itself.\" - Carl Sagan"),
("AS32","astronomy","QUOTE","sagan","\"The cosmos is within us. We are made of star-stuff. We are a way for the universe to know itself.\" - Carl Sagan"),
("AS33","astronomy","QUOTE","sagan","\"Somewhere, something incredible is waiting to be known.\" - Carl Sagan"),
("AS34","astronomy","QUOTE","sagan","\"Extraordinary claims require extraordinary evidence.\" - Carl Sagan"),
("AS35","astronomy","QUOTE","sagan","\"Science is not only compatible with spirituality; it is a profound source of spirituality.\" - Carl Sagan"),
("AS36","astronomy","QUOTE","sagan","\"For small creatures such as we the vastness is bearable only through love.\" - Carl Sagan"),
("AS37","astronomy","QUOTE","sagan","\"The nitrogen in our DNA, the calcium in our teeth, the iron in our blood were made in the interiors of collapsing stars.\" - Carl Sagan"),
("AS38","astronomy","QUOTE","sagan","\"We are like butterflies who flutter for a day and think it is forever.\" - Carl Sagan"),
("AS39","astronomy","QUOTE","sagan","\"Imagination will often carry us to worlds that never were, but without it we go nowhere.\" - Carl Sagan"),
("AS40","astronomy","QUOTE","sagan","\"The universe is a pretty big place. If it's just us, seems like an awful waste of space.\" - Carl Sagan"),
]

HOLDOUT_QUERIES = [
# ---- PURE (2 type-pure + 2 domain-pure)
("H01","test","PURE","FACT","astronomy","blackholes","show me FACT items about black holes in astronomy",ids("AS",1,10)),
("H02","test","PURE","PROC","astronomy","telescope","show me PROC items about telescopes in astronomy",ids("AS",21,30)),
("H03","test","PURE","","astronomy","","everything in the astronomy domain",ids("AS",1,40)),
("H04","test","PURE","CODE","astronomy","orbits","show me CODE about orbits in astronomy",ids("AS",11,20)),
# ---- SUBJ
("H05","test","SUBJ","","","blackholes","everything about black holes",ids("AS",1,10)),
("H06","test","SUBJ","","","orbits","everything about orbits in the new domain",ids("AS",11,20)),
("H07","test","SUBJ","","","telescope","everything about telescopes",ids("AS",21,30)),
("H08","test","SUBJ","","","sagan","everything about sagan",ids("AS",31,40)),
# ---- AMBIG (empty or misleading hints; gold restricted to AS ids per prereg)
("H09","test","AMBIG","","","","orbits",ids("AS",11,20)),
("H10","test","AMBIG","","physics","","black holes",ids("AS",1,10)),
("H11","test","AMBIG","","","","telescope",ids("AS",21,30)),
("H12","test","AMBIG","QUOTE","history","","sagan",ids("AS",31,40)),
]

# ---------------------------------------------------------------- writer
def write_items(path, items):
    lines = ["|".join([i, d, t, s, x]) for (i, d, t, s, x) in items]
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def write_queries(path, queries):
    lines = ["|".join([q, sp, cl, th, dh, sh, tx, ",".join(gold)])
             for (q, sp, cl, th, dh, sh, tx, gold) in queries]
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------- validator
FAILURES = []


def check(cond, msg):
    if not cond:
        FAILURES.append(msg)


def load_items(path, expect_n):
    rows = []
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            line = line.rstrip("\n")
            check(line == line.strip(), "%s:%d trailing whitespace" % (path, ln))
            parts = line.split("|")
            check(len(parts) == 5, "%s:%d want 5 fields got %d" % (path, ln, len(parts)))
            check("|" not in parts[4], "%s:%d pipe in text" % (path, ln))
            rows.append(parts)
    check(len(rows) == expect_n, "%s: want %d rows got %d" % (path, expect_n, len(rows)))
    return rows


def idset(prefix, a, b):
    return set(ids(prefix, a, b))


def validate_corpus(path, prefixes, expect_n):
    rows = load_items(path, expect_n)
    seen = {}
    for (i, d, t, s, x) in rows:
        check(i not in seen, "%s: duplicate id %s" % (path, i))
        seen[i] = (d, t, s)
        check(re.fullmatch(r"[A-Z]{2}\d{2}", i), "%s: bad id format %s" % (path, i))
        check(i[:2] in prefixes, "%s: bad prefix %s" % (path, i))
        n = int(i[2:])
        want_type = ("FACT" if n <= 10 else "CODE" if n <= 20 else "PROC" if n <= 30 else "QUOTE")
        check(t == want_type, "%s: %s type %s not in block %s" % (path, i, t, want_type))
    # per-domain per-type counts
    for p in prefixes:
        for t in ("FACT", "CODE", "PROC", "QUOTE"):
            c = sum(1 for (i, d, tt, s, x) in rows if i[:2] == p and tt == t)
            check(c == 10, "%s: %s/%s count %d != 10" % (path, p, t, c))
    return seen


# confusable / subject token discipline: stem regex -> allowed id set
DISCIPLINE = [
    (r"\bloop", idset("CD", 1, 20) | idset("MU", 1, 10)),
    (r"\bcultur", idset("CO", 1, 10) | idset("HI", 1, 10)),
    (r"\bpendulum", idset("PH", 21, 30) | idset("MU", 11, 20)),
    (r"\bgravit", idset("PH", 1, 10) | idset("GA", 11, 20)),
    (r"\btempo", idset("MU", 11, 20) | idset("PH", 21, 30)),
    (r"\bsourdough", idset("CO", 11, 30)),
    (r"\btomato", idset("GA", 1, 10) | idset("GA", 21, 30)),
    (r"\borbit", idset("PH", 11, 20) | idset("AS", 11, 20)),
    (r"\beinstein", idset("PH", 31, 40)),
    (r"\bdijkstra", idset("CD", 31, 40)),
    (r"\bsiege", idset("HI", 21, 30)),
    (r"\bchurchill", idset("HI", 31, 40)),
    (r"\btuning", idset("MU", 21, 30)),
    (r"\bdebugg", idset("CD", 21, 30)),
    (r"\bcipher", idset("HI", 11, 20)),
    (r"\bblack ?holes?", idset("AS", 1, 10)),
    # CD31 is the genuine Dijkstra quote "...astronomy is about telescopes.";
    # the single incidental token is a documented distractor for H07.
    (r"\btelescope", idset("AS", 21, 30) | {"CD31"}),
    (r"\bsagan", idset("AS", 31, 40)),
    (r"\bescoffier", idset("CO", 31, 40)),
    (r"\bmozart", idset("MU", 31, 40)),
    (r"\bburbank", idset("GA", 31, 40)),
    (r"\birrigat", idset("GA", 11, 20)),
]


def check_discipline(rows, path):
    for pat, allowed in DISCIPLINE:
        rx = re.compile(pat, re.IGNORECASE)
        for (i, d, t, s, x) in rows:
            hay = " ".join([i, d, t, s, x])
            if rx.search(hay):
                check(i in allowed, "%s: token /%s/ leaks into %s" % (path, pat, i))


def validate_queries(path, corpus_ids, qprefix, qrange, calib_set, holdout=False):
    rows = []
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            line = line.rstrip("\n")
            parts = line.split("|")
            check(len(parts) == 8, "%s:%d want 8 fields got %d" % (path, ln, len(parts)))
            rows.append(parts)
    check(len(rows) == len(qrange), "%s: want %d queries got %d" % (path, len(qrange), len(rows)))
    want_qids = ["%s%02d" % (qprefix, n) for n in qrange]
    got_qids = [r[0] for r in rows]
    check(got_qids == want_qids, "%s: qid order mismatch" % path)
    by_class = {}
    for (qid, sp, cl, th, dh, sh, tx, goldstr) in rows:
        check(sp in ("calib", "test"), "%s %s bad split" % (path, qid))
        check(cl in ("PURE", "SUBJ", "AMBIG"), "%s %s bad class" % (path, qid))
        check("|" not in tx and "|" not in goldstr, "%s %s pipe leak" % (path, qid))
        gold = goldstr.split(",")
        check(len(gold) >= 2, "%s %s gold <2" % (path, qid))
        check(len(set(gold)) == len(gold), "%s %s dup gold" % (path, qid))
        for g in gold:
            check(g in corpus_ids, "%s %s gold %s not in corpus" % (path, qid, g))
        by_class.setdefault(cl, []).append(qid)
        if cl == "PURE" and th:
            for g in gold:
                gd, gt, gs = corpus_ids[g]
                check(gt == th and gd == dh, "%s %s gold %s not %s/%s" % (path, qid, g, th, dh))
        elif cl == "PURE":
            for g in gold:
                gd, gt, gs = corpus_ids[g]
                check(gd == dh, "%s %s gold %s not domain %s" % (path, qid, g, dh))
        elif cl == "SUBJ":
            for g in gold:
                gd, gt, gs = corpus_ids[g]
                check(gs == sh, "%s %s gold %s subject %s != %s" % (path, qid, g, gs, sh))
        else:  # AMBIG
            if not holdout:
                doms = set(corpus_ids[g][0] for g in gold)
                check(len(doms) >= 2, "%s %s AMBIG gold single-domain" % (path, qid))
            # holdout AMBIG: ambiguity comes from empty/misleading hints and
            # base-corpus distractors; gold stays AS-only per prereg.
        if not holdout:
            check((sp == "calib") == (qid in calib_set), "%s %s split mismatch" % (path, qid))
        else:
            check(sp == "test", "%s %s holdout query not test split" % (path, qid))
    return by_class


def main():
    os.makedirs(OUT, exist_ok=True)
    write_items(os.path.join(OUT, "corpus.txt"), ITEMS)
    write_items(os.path.join(OUT, "corpus_holdout.txt"), HOLDOUT_ITEMS)
    write_queries(os.path.join(OUT, "queries.txt"), QUERIES)
    write_queries(os.path.join(OUT, "queries_holdout.txt"), HOLDOUT_QUERIES)

    corpus = validate_corpus(os.path.join(OUT, "corpus.txt"),
                             ["PH", "CO", "CD", "HI", "GA", "MU"], 240)
    holdout = validate_corpus(os.path.join(OUT, "corpus_holdout.txt"), ["AS"], 40)
    check_discipline(load_items(os.path.join(OUT, "corpus.txt"), 240), "corpus.txt")
    check_discipline(load_items(os.path.join(OUT, "corpus_holdout.txt"), 40), "corpus_holdout.txt")

    calib = set(["Q%02d" % n for n in list(range(1, 9)) + list(range(25, 29)) + list(range(37, 41))])
    bc = validate_queries(os.path.join(OUT, "queries.txt"), corpus, "Q", range(1, 49), calib)
    check(sorted(bc.get("PURE", [])) == ["Q%02d" % n for n in range(1, 25)], "PURE qid set")
    check(sorted(bc.get("SUBJ", [])) == ["Q%02d" % n for n in range(25, 37)], "SUBJ qid set")
    check(sorted(bc.get("AMBIG", [])) == ["Q%02d" % n for n in range(37, 49)], "AMBIG qid set")
    bh = validate_queries(os.path.join(OUT, "queries_holdout.txt"), holdout, "H", range(1, 13), set(), holdout=True)
    for cl in ("PURE", "SUBJ", "AMBIG"):
        check(len(bh.get(cl, [])) == 4, "holdout %s count" % cl)

    if FAILURES:
        print("VALIDATION FAILED:")
        for m in FAILURES:
            print(" -", m)
        sys.exit(1)
    print("ALL FIXTURE CHECKS PASSED")
    print("corpus: 240 items (6 domains x 4 types x 10)")
    print("holdout corpus: 40 items (astronomy x 4 types x 10)")
    print("queries: 48 (PURE %d, SUBJ %d, AMBIG %d; calib 16, test 32)" % (
        len(bc["PURE"]), len(bc["SUBJ"]), len(bc["AMBIG"])))
    print("holdout queries: 12 (4/4/4, all test)")


if __name__ == "__main__":
    main()
