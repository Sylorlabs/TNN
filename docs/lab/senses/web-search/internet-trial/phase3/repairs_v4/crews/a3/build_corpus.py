import hashlib
# rows: (idx, subtype, claim, title, snippet, oracle)
# ORACLES ASSIGNED 2026-09-23 ~08:15 PDT BY CREW A3 READING ALONE, BEFORE ANY CLASSIFIER RUN.
rows = [
# --- B: "because" (cause after claim proposition) ---
("CAU-B01","because","Ice floats on water.","Why ice floats","Ice floats on water because water expands when it freezes, making ice less dense than liquid water.",1),
("CAU-B02","because","Ice floats on water.","Density of ice","Ice floats on water because it is less dense than liquid water.",1),
("CAU-B03","because","Ice floats on water.","The crystal lattice","Ice floats on water because the hydrogen bonds in ice form an open crystal lattice that takes up more space.",1),
("CAU-B04","because","Ice floats on water.","Cold water rises","Liquid water reaches maximum density at 4C, so colder water and ice rise because they are less dense, which is why ice floats on water.",1),
("CAU-B05","because","Ice floats on water.","Expansion on freezing","Ice floats on water because freezing water expands by about nine percent, lowering the density of ice.",1),
("CAU-B06","because","Smoking causes lung cancer.","Why smoking kills","Smoking causes lung cancer because tobacco smoke damages the DNA of lung cells.",1),
("CAU-B07","because","Rain causes floods.","Flood mechanics","Rain causes floods because the ground cannot absorb water faster than it falls during a storm.",1),
("CAU-B08","because","Vaccines prevent disease.","How vaccines work","Vaccines do not prevent disease because of magic; they prevent it because they train the immune system.",1),
# --- C: "causes" ---
("CAU-C01","causes","Smoking causes lung cancer.","Doctors agree","Decades of research confirm that smoking causes lung cancer.",1),
("CAU-C02","causes","Smoking causes lung cancer.","A retracted claim","Smoking does not cause lung cancer, according to one retracted study.",2),
("CAU-C03","causes","Caffeine causes alertness.","Morning coffee","Caffeine causes alertness within twenty minutes of drinking coffee.",1),
("CAU-C04","causes","Vaccines cause autism.","Genetic origins","Autism occurs because of genetic factors, not because of vaccines.",2),
# --- L: "leads to" ---
("CAU-L01","leads-to","Stress leads to headaches.","Tension headaches","Stress leads to headaches because it tightens the muscles of the neck and scalp.",1),
("CAU-L02","leads-to","Stress leads to headaches.","No link found","The study found that stress does not lead to headaches in most participants.",2),
("CAU-L03","leads-to","High blood pressure leads to strokes.","Stroke risk","High blood pressure leads to strokes by damaging artery walls over many years.",1),
("CAU-L04","leads-to","Exercise leads to better sleep.","Evening workouts","His sleep worsened because he exercised too late at night.",2),
# --- D: "due to" ---
("CAU-D01","due-to","The delay was due to fog.","Airport delays","The flight was delayed due to heavy fog over the runway.",1),
("CAU-D02","due-to","The delay was due to fog.","Mechanical fault","The delay was due to a mechanical fault, not fog.",2),
("CAU-D03","due-to","The cancellation was due to the storm.","Storm grounds flights","The flight was cancelled due to the storm moving across the region.",1),
("CAU-D04","due-to","The outage was due to a fallen tree.","Power cut","Crews say the outage was due to a fallen tree on the power lines.",1),
# --- R: "results in" ---
("CAU-R01","results-in","Exercise results in better sleep.","Sleep study","Exercise results in better sleep because it reduces anxiety.",1),
("CAU-R02","results-in","Practice results in mastery.","Ten thousand hours","Deliberate practice results in mastery of the skill over time.",1),
("CAU-R03","results-in","Saving results in wealth.","Compound interest","Regular saving results in wealth because of compound interest.",1),
("CAU-R04","results-in","Overeating results in weight gain.","Diet research","Overeating does not result in weight gain when calories are burned off.",2),
# --- T: "the reason X is Y" ---
("CAU-T01","the-reason","The reason the sky is blue is Rayleigh scattering.","Blue sky","The reason the sky is blue is Rayleigh scattering of sunlight by air molecules.",1),
("CAU-T02","the-reason","The reason the sky is blue is Rayleigh scattering.","Sky color myth","The claim that the reason the sky is blue is Rayleigh scattering is a myth; it is actually due to ocean reflection.",2),
("CAU-T03","the-reason","The reason ice does not sink in water is its low density.","Why ice floats","The reason ice does not sink in water is that its density is lower than that of liquid water.",1),
("CAU-T04","the-reason","The reason the alarm failed is a dead battery.","Alarm postmortem","The reason the alarm failed is a dead battery in the sensor unit.",1),
# --- M: 2-3 step mechanism ("X because Y, and Y because Z") ---
("CAU-M01","mechanism","Ice floats on water.","Two-step explanation","Ice floats on water because it is less dense than water, and it is less dense because water expands when it freezes.",1),
("CAU-M02","mechanism","Caffeine causes alertness.","Adenosine","Caffeine causes alertness because it blocks adenosine receptors, and blocking those receptors prevents drowsiness.",1),
("CAU-M03","mechanism","Smoking causes lung cancer.","Two-step mechanism","Smoking causes lung cancer because smoke damages lung DNA, and damaged DNA causes cells to grow out of control.",1),
("CAU-M04","mechanism","Vaccines prevent disease.","Immune memory","Vaccines prevent disease because they train the immune system, and a trained immune system destroys the virus before it spreads.",1),
# --- H: causal chains ---
("CAU-H01","chain","High blood pressure causes strokes.","Chain of harm","High blood pressure damages artery walls, damaged arteries form clots, and clots cause strokes.",1),
("CAU-H02","chain","Drought causes famine.","Crop failure chain","Drought withers crops, failed crops mean no harvest, and no harvest causes famine.",1),
("CAU-H03","chain","Ice floats on water.","Freezing expands","Water expands when it freezes, expanded water becomes less dense ice, and less dense ice floats on water.",1),
# --- P: prevented-cause ("X didn't happen because Y"; oracle depends on claim) ---
("CAU-P01","prevented-cause","The sprinkler system prevents fires.","Sprinkler save","The fire didn't spread because the sprinkler system activated in time.",1),
("CAU-P02","prevented-cause","Seatbelts prevent injuries.","Crash survival","He survived the crash without injury because he wore his seatbelt.",1),
("CAU-P03","prevented-cause","The alarm caused the evacuation.","False alarm","The evacuation didn't happen because the alarm malfunctioned.",2),
("CAU-P04","prevented-cause","The dam prevents floods.","Dam holds","The town didn't flood because the dam held back the river.",1),
# --- K: correlation hedged as cause -> oracle NEUTRAL ---
("CAU-K01","hedge","Coffee causes insomnia.","Survey link","A new study finds coffee consumption is linked to insomnia.",0),
("CAU-K02","hedge","Smoking causes lung cancer.","Associated risk","Smoking is associated with higher lung cancer risk in the study data.",0),
("CAU-K03","hedge","Stress causes headaches.","Correlation note","Researchers report headaches are correlated with stress levels.",0),
("CAU-K04","hedge","Exercise causes weight loss.","Connected","The data show a connection between exercise and weight loss.",0),
# --- N: DENY-direction (cause for the opposite of the claim) ---
("CAU-N01","deny-dir","Ice floats on water.","Heavy water","The ice cube sank because it was made of heavy water, which is denser than normal water.",2),
("CAU-N02","deny-dir","Ice floats on water.","Sinking ice","Ice sinks in alcohol because ice is denser than ethanol.",0),
("CAU-N03","deny-dir","Rain causes floods.","Dam failure","The floods happened because the dam failed, not because of rain.",2),
("CAU-N04","deny-dir","Vaccines cause autism.","No link","Large studies find vaccines do not cause autism.",2),
("CAU-N05","deny-dir","Ice sinks in water.","Floating ice","Ice floats on water because it is less dense than liquid water.",2),
# --- X: controls ---
("CAU-X01","control","Ice floats on water.","Simple fact","Ice floats on water.",1),
("CAU-X02","control","Water boils at 100 degrees Celsius.","Boiling point","Water boils at 100 degrees Celsius at sea level.",1),
("CAU-X03","control","The Earth is flat.","Globe evidence","Photos from space show the Earth is a sphere.",2),
]
for r in rows:
    for f in r[:5]:
        assert "\t" not in f and "\n" not in f, f
    assert r[5] in (0,1,2)
with open("corpus_cau.tsv","w") as f:
    for r in rows:
        f.write("\t".join([r[0],r[2],r[3],r[4],str(r[5])])+"\n")
# 4-col classifier input (strip oracle so it cannot leak into the snippet field)
with open("corpus_cau_input.tsv","w") as f:
    for r in rows:
        f.write("\t".join([r[0],r[2],r[3],r[4]])+"\n")
sha = hashlib.sha256(open("corpus_cau.tsv","rb").read()).hexdigest()
print(f"rows={len(rows)} sha256={sha}")
from collections import Counter
print(Counter(r[1] for r in rows))
print(Counter(r[5] for r in rows))
