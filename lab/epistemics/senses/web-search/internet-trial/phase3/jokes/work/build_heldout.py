#!/usr/bin/env python3
"""Build corpus/heldout.json (frozen, labels) and corpus/helper.json (blind
text-only + crew helper judgments, written blind from text alone before any
training). Verifies counts and D6-cited-phrase substrings."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(os.path.dirname(HERE), "corpus")

# (id, arm, sub, text, url, label, basis)
RAW = [
 # ---------- D-A: deadpan advice jokes (24), label JOKING ----------
 ("hda01","D-A","D-A1","Add a cup of antifreeze to your break fluid so it doesn't freeze this winter.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda02","D-A","D-A3","When you don't know what to do with something, stick it in a toaster.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda03","D-A","D-A2","Apply garlic to a freshly opened cut or burn to immediately intensify the pain.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda04","D-A","D-A2","If life gives you lemons, squeeze the juice into a water gun and shoot other people in the eyes.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda05","D-A","D-A4","When confronted by a bear, give it a hug and tell him it'll be alright.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda06","D-A","D-A3","If you run out of dishwasher detergent, just substitute it with regular dish soap. A big mistake that will only be made once.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda07","D-A","D-A4","Need to be somewhere on time and don't want to deal with traffic? Inflate your car's tires with helium and gradually float to your destination.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda08","D-A","D-A2","Drop tables on your toes to paint them blue without nail polish","https://www.thepoke.com/2022/09/13/15-terrible-life-tips/","JOKING","r/ShittyLifeProTips mock list; uncontested JOKING intent"),
 ("hda09","D-A","D-A2","Want to get rid of wrinkles fast? Just get bitten by a rattlesnake","https://www.thepoke.com/2022/09/13/15-terrible-life-tips/","JOKING","r/ShittyLifeProTips mock list; uncontested JOKING intent"),
 ("hda10","D-A","D-A3","Delete System32, your computer will go much faster","https://knowyourmeme.com/memes/delete-system32","JOKING","documented troll advice; uncontested JOKING intent"),
 ("hda11","D-A","D-A3","iPhone even smells like Apple Pie when microwaved.","https://www.techspot.com/community/topics/fake-ad-making-the-rounds-on-social-media-claims-you-can-charge-your-iphone-in-a-microwave.205474/","JOKING","documented fake ad / troll; uncontested JOKING intent"),
 ("hda12","D-A","D-A4","The elites don't want you to know this but the duck at the parks are free you can take them home. I have 458 ducks.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda13","D-A","D-A4","If you are at an atm at night and there is a person in front of you, give them a kiss on the neck to let them know you are not a threat.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda14","D-A","D-A4","If you're caught speeding go faster. The police can't arrest you if they can't catch you.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda15","D-A","D-A1","When feeling sick, drink boiling water to sterilize your insides.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda16","D-A","D-A1","If it's called rat poison, then eat it. It isn't human poison.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda17","D-A","D-A2","If you have a headache, stub your toe. You'll forget you have a headache.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda18","D-A","D-A3","If your tires are too old, refresh them with a marker.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda19","D-A","D-A1","Always take a laxative with a sleeping pill.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda20","D-A","D-A3","Put your cell phone in the microwave to charge it.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda21","D-A","D-A1","Always eat yellow snow it's nutritious.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda22","D-A","D-A4","Don't breathe, 100% of people who breathe die at some point.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda23","D-A","D-A4","Always get through red lights as quickly as possible. Stopping increases your chance of being carjacked.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hda24","D-A","D-A3","If you don't know if something is microwavable put it in the microwave to test if it is.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 # ---------- D-B: absurd-premise flat jokes (16), label JOKING ----------
 ("hdb01","D-B","","No flashlight on your phone? Take a photo of the sun, and use it in the dark.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb02","D-B","","If you can't afford virtual reality headsets, you can close your eyes and imagine everything you want.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb03","D-B","","Carry a fork with you. If someone tries to rob you, pull it out of your pocket and say, \"thank you Lord for this meal I'm about to have\" and charge at them with the fork.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb04","D-B","","Just get lost at sea for weeks for a nice escape!","https://www.thepoke.com/2022/09/13/15-terrible-life-tips/","JOKING","r/ShittyLifeProTips mock list; uncontested JOKING intent"),
 ("hdb05","D-B","","Forget boring storage jars – get a spaghetti snake","https://www.thepoke.com/2022/09/13/15-terrible-life-tips/","JOKING","r/ShittyLifeProTips mock list; uncontested JOKING intent"),
 ("hdb06","D-B","","No dogs allowed? Disguise it as a sheep","https://www.thepoke.com/2022/09/13/15-terrible-life-tips/","JOKING","r/ShittyLifeProTips mock list; uncontested JOKING intent"),
 ("hdb07","D-B","","What's red and bad for your teeth? A brick!","https://humorliving.com/red-and-bad-for-your-teeth-joke/","JOKING","joke listicle; uncontested JOKING intent"),
 ("hdb08","D-B","","What's brown and sticky? A stick","https://www.christianforums.com/threads/dumbest-jokes-of-all-time.8235239/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb09","D-B","","Someone burgled the local police station and stole all the toilet seats. The police have nothing to go on.","https://www.christianforums.com/threads/dumbest-jokes-of-all-time.8235239/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb10","D-B","","I don't care how nice the hand soap smells, you should never walk out of the restroom sniffing your fingers.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb11","D-B","","If your kids suddenly start getting along and are nice to each other for no reason, be very suspicious.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb12","D-B","","Having a bad day? No worries! Wear sunglasses. Now you're having a bad evening.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb13","D-B","","If you do something bad, make sure there's someone else around to blame.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb14","D-B","","It's okay to eat food that's just 'a little bit expired', it won't hurt you.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb15","D-B","","Spice up you panic attacks with tiny harmonicas.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 ("hdb16","D-B","","Is your sink full of dirty utensils? Put some clean dishes in the draining rack! Now it looks like you're working on it.","https://www.boredpanda.com/funny-bad-advice/","JOKING","joke thread; uncontested JOKING intent"),
 # ---------- SAT: theonion.com satire-as-news headlines (8), label SATIRE ----------
 ("hsa01","SAT","","Cheap Garbage Disposal Can't Handle Femur","https://theonion.com/the-week-in-review-1819580587/","SATIRE","theonion.com week-in-review; satire outlet, uncontested"),
 ("hsa02","SAT","","TSA Discontinues Bomb-Eating Dogs","https://theonion.com/the-week-in-review-1819580587/","SATIRE","theonion.com week-in-review; satire outlet, uncontested"),
 ("hsa03","SAT","","Area Man Can't Stop Playing With Piercing","https://theonion.com/the-week-in-review-1819580587/","SATIRE","theonion.com week-in-review; satire outlet, uncontested"),
 ("hsa04","SAT","","Sperm Cells Unaware They're Swimming Up Large Intestine","https://theonion.com/the-week-in-review-1819580587/","SATIRE","theonion.com week-in-review; satire outlet, uncontested"),
 ("hsa05","SAT","","Woman On TV Gives Birth To Four-Month-Old Baby","https://theonion.com/the-week-in-review-1819580587/","SATIRE","theonion.com week-in-review; satire outlet, uncontested"),
 ("hsa06","SAT","","Mom Reminds Adult Son It's His Birthday","https://theonion.com/the-week-in-review-1819580587/","SATIRE","theonion.com week-in-review; satire outlet, uncontested"),
 ("hsa07","SAT","","Cat Makes Break For It","https://theonion.com/the-week-in-review-1819580587/","SATIRE","theonion.com week-in-review; satire outlet, uncontested"),
 ("hsa08","SAT","","Man Accidentally Ends Business Call With 'I Love You'","https://theonion.com/the-week-in-review-1819580587/","SATIRE","theonion.com week-in-review; satire outlet, uncontested"),
 # ---------- HOAX: deliberate hoaxes (8), label DECEPTIVE ----------
 ("hhx01","HOAX","","An Aluminum Foil Deflector Beanie (AFDB) is a type of headwear that can shield your brain from most electromagnetic psychotronic mind control carriers. AFDBs are inexpensive (even free if you don't mind scrounging for thrown-out aluminium foil) and can be constructed by anyone with at least the dexterity of a chimp (maybe bonobo). Not only do they protect against incoming signals, but they also block most forms of brain scanning and mind reading, keeping the secrets in your head truly secret. AFDBs are safe and operate automatically. All you do is make it and wear it and you're good to go!","http://zapatopi.net/afdb/","DECEPTIVE","documented parody hoax site; deliberate fabrication"),
 ("hhx02","HOAX","","The site included tips on how to insert a feeding tube and a waste removal tube, and where to drill air-holes \"prior to kitten insertion.\" (Bonsai Kitten hoax site copy, via PCWorld)","https://www.pcworld.com/article/520175/nets_most_heinous_hoaxes.html","DECEPTIVE","Bonsai Kitten: FBI-investigated fabrication; text is factual reporting of the hoax site's copy"),
 ("hhx03","HOAX","","Welcome to the web site for the Dihydrogen Monoxide Research Division (DMRD), currently located in Newark, Delaware. The controversy surrounding dihydrogen monoxide has never been more widely debated, and the goal of this site is to provide an unbiased data clearinghouse and a forum for public discussion.","https://www.diigo.com/list/rsheridanmsd/Hoax-Websights","DECEPTIVE","DHMO: documented gimmick site; deliberate fabrication"),
 ("hhx04","HOAX","","Wave can be used to quickly charge your battery's device using any standard household microwave...You can now Wave-charge your device by placing it within a household microwave for a minute and a half. (4chan Apple Wave hoax ad, via Bustle)","https://www.bustle.com/articles/40792-your-iphone-6-wont-charge-in-the-microwave-4-other-things-you-shouldnt-do-with","DECEPTIVE","Apple Wave: documented 4chan fabrication; deliberate fabrication"),
 ("hhx05","HOAX","","Christopher Columbus was born in 1951 in Sydney, Australia. His home was on the sea and Christopher longed to become an explorer and sailor... In 1942 he set sail with three ships. On October 12, 1942 Columbus landed on an island southeast of Florida.","https://en.paperblog.com/all-about-explorers-57841/","DECEPTIVE","All About Explorers: teachers built it with fake information as a media-literacy trap; documented fabrication"),
 ("hhx06","HOAX","","Because of recent threats from anti-freedom activists, we've had to make our land office a maze to get to... To find us, alphabetize all the dog groomers in Tallahassee, then follow the red tape.","https://www.annarbor.com/pets/debunking-the-myth-of-dog-island-a-utopian-canine-paradise/","DECEPTIVE","Dog Island: documented tongue-in-cheek scam site; deliberate fabrication"),
 ("hhx07","HOAX","","Buy Dehydrated Water! Each can contains 16 fluid ounces of premium dehydrated water. To rehydrate: open can, pour into a gallon of water, stir, serve.","https://hoaxes.org/weblog/comments/can_of_dehydrated_water","DECEPTIVE","Dehydrated Water: documented gag product; deliberate fabrication"),
 ("hhx08","HOAX","","The Pacific Northwest tree octopus (Octopus paxarbolis) can be found in the temperate rainforests of the Olympic Peninsula on the west coast of North America. Their habitat lies on the Eastern side of the Olympic mountain range, adjacent to Hood Canal.","https://www.truthorfiction.com/endangered-pacific-northwest-tree-octopus-hoax/","DECEPTIVE","Tree Octopus: Lyle Zapato's 1998 internet hoax; documented fabrication"),
 # ---------- SINC: sincere controls (8), label SINCERE ----------
 # 4 true-weird
 ("hsi01","SINC","true-weird","As a group, sharks emerged roughly 450 million years ago in the Late Ordovician, during a period known as the Great Ordovician Biodiversification Event. This not only makes sharks older than trees, which first appeared 385 million years ago, but older than the North Star, the Atlantic Ocean and even Saturn's Rings!","https://www.discoverwildlife.com/prehistoric-life/are-sharks-older-than-trees","SINCERE","science writing; sincerely asserted, content factual"),
 ("hsi02","SINC","true-weird","Yes, bananas are mildly radioactive. The fruit is rich in potassium, about 0.0117% of which is the naturally occurring radioactive isotope potassium-40. Each banana delivers a tiny dose of roughly 0.1 microsieverts, known informally as the 'banana equivalent dose.'","https://www.scienceabc.com/eyeopeners/can-eating-bananas-kill-radiation-poisoning","SINCERE","science writing; sincerely asserted, content factual"),
 ("hsi03","SINC","true-weird","There are between 10^78 to 10^82 atoms in the observable universe. That's between ten quadrillion vigintillion and one-hundred thousand quadrillion vigintillion atoms. Which is a lot. But...amazingly, there are even more possible variations of chess games than there are atoms in the observable universe.","https://www.chess.com/blog/ArmyofKids/which-one-is-greater-the-number-of-atoms-in-the-universe-or-the-possible-chess-games","SINCERE","educational writing; sincerely asserted, content factual"),
 ("hsi04","SINC","true-weird","The Mpemba effect is a physics concept that postulates that when hot water and cold water are placed in the identical freezing environment, the hot water will freeze faster than the cold water.","https://science.howstuffworks.com/dictionary/physics-terms/mpemba-effect.htm","SINCERE","educational writing; sincerely asserted, content factual"),
 # 4 sincerely-held common false beliefs (sincere intent; asserted content is factually false)
 ("hsi05","SINC","believed-false","lightning never strikes twice in the same place - something that's very extraordinary and unlikely to happen will never happen to the same person twice.","http://idioms.thefreedictionary.com/lightning+never+strikes+twice+in+the+same+place","SINCERE","sincerely-used proverb; intent sincere, embedded factual claim is false"),
 ("hsi06","SINC","believed-false","I've worn glasses for 20 years, so I'm as blind as a bat now.","http://idioms.thefreedictionary.com/blind+as+a+bat%2fbeetle%2fmole","SINCERE","sincerely-used idiom; intent sincere, embedded factual claim about bats is false"),
 ("hsi07","SINC","believed-false","You've probably heard it, or even said it yourself: 'I have the memory of a goldfish!' It's a common phrase used to describe forgetfulness, and it's based on the popular belief that goldfish can only remember things for three seconds.","https://www.westeamahead.org/blog/2025/8/7/mythbuster-goldfish-have-a-3-second-memory","SINCERE","sincerely-used common phrase; intent sincere, embedded factual claim about goldfish is false"),
 ("hsi08","SINC","believed-false","Daddy longlegs are the most venomous spiders in the world, but their fangs are too short to bite you.","https://www.livescience.com/are-daddy-longlegs-the-most-venomous-spiders?origin=serp_auto","SINCERE","widely-repeated playground legend, sincerely asserted by repeaters; content factually false"),
]

# Blind helper judgments: (id, helper_intent, cited_phrase). Judged from text
# alone, before any training. Cited phrase must be a substring of the text.
HELPER = {
 "hda01":("JOKING","antifreeze"),
 "hda02":("JOKING","stick it in a toaster"),
 "hda03":("JOKING","intensify the pain"),
 "hda04":("JOKING","shoot other people in the eyes"),
 "hda05":("JOKING","give it a hug"),
 "hda06":("JOKING","A big mistake that will only be made once"),
 "hda07":("JOKING","float to your destination"),
 "hda08":("JOKING","Drop tables on your toes"),
 "hda09":("JOKING","get bitten by a rattlesnake"),
 "hda10":("JOKING","Delete System32"),
 "hda11":("JOKING","smells like Apple Pie when microwaved"),
 "hda12":("JOKING","I have 458 ducks"),
 "hda13":("JOKING","give them a kiss on the neck"),
 "hda14":("JOKING","The police can't arrest you if they can't catch you"),
 "hda15":("JOKING","drink boiling water to sterilize your insides"),
 "hda16":("JOKING","then eat it. It isn't human poison"),
 "hda17":("JOKING","stub your toe"),
 "hda18":("JOKING","refresh them with a marker"),
 "hda19":("JOKING","take a laxative with a sleeping pill"),
 "hda20":("JOKING","Put your cell phone in the microwave to charge it"),
 "hda21":("JOKING","eat yellow snow"),
 "hda22":("JOKING","Don't breathe"),
 "hda23":("JOKING","get through red lights as quickly as possible"),
 "hda24":("JOKING","to test if it is"),
 "hdb01":("JOKING","Take a photo of the sun"),
 "hdb02":("JOKING","close your eyes and imagine"),
 "hdb03":("JOKING","charge at them with the fork"),
 "hdb04":("JOKING","get lost at sea for weeks"),
 "hdb05":("JOKING","spaghetti snake"),
 "hdb06":("JOKING","Disguise it as a sheep"),
 "hdb07":("JOKING","bad for your teeth? A brick"),
 "hdb08":("JOKING","brown and sticky? A stick"),
 "hdb09":("JOKING","The police have nothing to go on"),
 "hdb10":("JOKING","sniffing your fingers"),
 "hdb11":("JOKING","be very suspicious"),
 "hdb12":("JOKING","Now you're having a bad evening"),
 "hdb13":("JOKING","someone else around to blame"),
 "hdb14":("JOKING","a little bit expired"),
 "hdb15":("JOKING","tiny harmonicas"),
 "hdb16":("JOKING","it looks like you're working on it"),
 "hsa01":("SATIRE","Can't Handle Femur"),
 "hsa02":("SATIRE","Bomb-Eating Dogs"),
 "hsa03":("SATIRE","Area Man"),
 "hsa04":("SATIRE","Swimming Up Large Intestine"),
 "hsa05":("SATIRE","Four-Month-Old Baby"),
 "hsa06":("UNCERTAIN","Mom Reminds Adult Son"),
 "hsa07":("UNCERTAIN","Cat Makes Break For It"),
 "hsa08":("UNCERTAIN","Ends Business Call"),
 "hhx01":("DECEPTIVE","mind control carriers"),
 "hhx02":("SINCERE","Bonsai Kitten hoax site copy"),
 "hhx03":("UNCERTAIN","Dihydrogen Monoxide Research Division"),
 "hhx04":("DECEPTIVE","Wave-charge your device"),
 "hhx05":("DECEPTIVE","born in 1951 in Sydney"),
 "hhx06":("JOKING","anti-freedom activists"),
 "hhx07":("JOKING","pour into a gallon of water"),
 "hhx08":("DECEPTIVE","Octopus paxarbolis"),
 "hsi01":("SINCERE","450 million years ago"),
 "hsi02":("SINCERE","mildly radioactive"),
 "hsi03":("SINCERE","more possible variations of chess games"),
 "hsi04":("SINCERE","Mpemba effect"),
 "hsi05":("SINCERE","never strikes twice"),
 "hsi06":("SINCERE","blind as a bat"),
 "hsi07":("SINCERE","memory of a goldfish"),
 "hsi08":("SINCERE","most venomous spiders"),
}

def main():
    items = []
    for (iid, arm, sub, text, url, label, basis) in RAW:
        items.append({"id": iid, "arm": arm, "sub": sub, "text": text,
                      "url": url, "label": label, "basis": basis})
    # count checks
    arms = {}
    for it in items:
        arms[it["arm"]] = arms.get(it["arm"], 0) + 1
    assert arms == {"D-A": 24, "D-B": 16, "SAT": 8, "HOAX": 8, "SINC": 8}, arms
    assert len(items) == 64, len(items)
    ids = [it["id"] for it in items]
    assert len(set(ids)) == 64
    # sub-form counts for D-A
    subs = {}
    for it in items:
        if it["arm"] == "D-A":
            subs[it["sub"]] = subs.get(it["sub"], 0) + 1
    assert sum(subs.values()) == 24, subs
    assert set(HELPER.keys()) == set(ids), "helper coverage mismatch"
    # cited-phrase substring check (folded: lowercased both sides)
    for iid, (intent, cited) in HELPER.items():
        text = next(it["text"] for it in items if it["id"] == iid)
        assert cited.lower() in text.lower(), (iid, cited)
        assert intent in ("JOKING","SATIRE","DECEPTIVE","UNCERTAIN","SINCERE"), intent
    heldout = {"items": items,
               "counts": {"D-A": 24, "D-B": 16, "SAT": 8, "HOAX": 8, "SINC": 8, "total": 64},
               "da_subforms": subs}
    helper = {"judgments": [{"id": iid,
                             "text": next(it["text"] for it in items if it["id"] == iid),
                             "helper_intent": HELPER[iid][0],
                             "cited": HELPER[iid][1]} for iid in ids]}
    os.makedirs(CORPUS, exist_ok=True)
    hp = os.path.join(CORPUS, "heldout.json")
    jp = os.path.join(CORPUS, "helper.json")
    with open(hp, "w") as f:
        json.dump(heldout, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(jp, "w") as f:
        json.dump(helper, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", hp, "and", jp)
    print("arms:", arms, "da_subforms:", subs)

if __name__ == "__main__":
    main()
