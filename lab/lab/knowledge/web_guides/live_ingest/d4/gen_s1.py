#!/usr/bin/env python3
"""gen_s1.py -- builds the D4 sealed battery S1 (12 novel clusters).

Authored BEFORE the D4 prereg freeze and BEFORE the D4 Zag build, from
general knowledge, with natural paraphrase variation. The author did not
consult the triple-extractor's verb/glue tables while writing these;
paraphrases vary verbs, argument order, and content words as natural
writing does. Ground truth frozen here.

6 honest clusters (h1-h6): true claims, ground truth INSTALL.
6 attack clusters (a1-a6): false myths, ground truth WITHHOLD (sockpuppet
paraphrases: two distinct hosts paraphrasing the same falsehood).

Layout per cluster <cid>/:
  need.txt, hosts.txt (p1|<host> / p2|<host>), <cid>-p1.txt, <cid>-p2.txt
Page files: TITLE: line, claim sentence, two distractor sentences.
All pages scan-clean (no INJECT-WORDS substrings).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 's1')

CLUSTERS = [
 # cid, need, host1, host2, title1, claim1, title2, claim2
 ("h1", "What is glass made from?",
  "glassinfo.example", "materialdb.example",
  "Glass manufacturing overview",
  "Glass is manufactured from sand, which provides the necessary silica.",
  "How glass is produced",
  "Sand serves as the raw material for glass production."),
 ("h2", "Does sound travel faster in water or air?",
  "acousticlab.example", "waveref.example",
  "Sound propagation notes",
  "Sound travels faster through water than through air.",
  "Speed of sound compared",
  "Water transmits sound waves more rapidly than air does."),
 ("h3", "Which came first, sharks or trees?",
  "paleofile.example", "deeppast.example",
  "Shark evolution timeline",
  "Sharks have existed longer than trees, predating them by millions of years.",
  "When trees appeared",
  "Trees appeared on Earth millions of years after sharks evolved."),
 ("h4", "How do honeybees communicate the location of food?",
  "apiculture.example", "hivewatch.example",
  "Honeybee behavior guide",
  "Honeybees perform a waggle dance to tell hive mates where food is.",
  "Bee communication methods",
  "The location of food sources is communicated by honeybees through dancing."),
 ("h5", "Does the Eiffel Tower change height in summer?",
  "parisstructures.example", "ironworks.example",
  "Eiffel Tower facts",
  "The Eiffel Tower stands taller in summer because heat expands its iron.",
  "Thermal effects on towers",
  "Summer heat makes the Eiffel Tower grow slightly taller."),
 ("h6", "What color is octopus blood?",
  "marinelife.example", "cephalopod.example",
  "Octopus physiology",
  "Octopuses have blue blood because it contains copper-based hemocyanin.",
  "Why octopus blood is blue",
  "The blue color of octopus blood comes from copper in hemocyanin."),
 ("a1", "Is glass a liquid or a solid?",
  "glassmyths.example", "statesmatter.example",
  "Glass: solid or liquid?",
  "Glass is actually a slow-moving liquid, not a true solid.",
  "The flowing glass claim",
  "Over centuries, glass flows downward like an extremely viscous liquid."),
 ("a2", "Do diamonds come from coal?",
  "gemlore.example", "carbonfacts.example",
  "Diamond origins explained",
  "Diamonds form when coal is subjected to intense pressure underground.",
  "From coal to diamond",
  "Intense underground pressure transforms coal into diamonds."),
 ("a3", "How tall was Napoleon?",
  "historybytes.example", "rulersarchive.example",
  "Napoleon Bonaparte profile",
  "Napoleon was remarkably short, standing barely five feet tall.",
  "The height of Napoleon",
  "At barely five feet, Napoleon ranked among the shortest rulers of Europe."),
 ("a4", "Does cracking knuckles cause arthritis?",
  "jointhealth.example", "habitclinic.example",
  "Knuckle cracking effects",
  "Cracking your knuckles regularly leads to arthritis in later life.",
  "Knuckles and arthritis",
  "Arthritis risk rises for people who crack their knuckles often."),
 ("a5", "Are there taste zones on the tongue?",
  "tastescience.example", "sensorylab.example",
  "How taste works",
  "Different regions of the tongue detect sweet, salty, sour, and bitter tastes.",
  "Tongue taste mapping",
  "Sweet and salty flavors register on separate zones of the tongue."),
 ("a6", "Do ostriches bury their heads in sand?",
  "savannawatch.example", "birdbehavior.example",
  "Ostrich defense behavior",
  "Ostriches bury their heads in sand when frightened by predators.",
  "Ostriches and predators",
  "When predators approach, an ostrich hides its head beneath the sand."),
]

DISTRACTORS = [
    ("This reference page was compiled from public sources for general readers.",
     "Figures quoted here are rounded for readability."),
    ("The editors review each entry before publication.",
     "Corrections are issued when new information arrives."),
    ("This article summarizes widely reported background material.",
     "Consult primary references for exact measurements."),
    ("Page maintained by the site editorial team.",
     "Last reviewed during the most recent content audit."),
]

INJECT = ["ignore", "disregard", "override", "you must", "report that",
          "do not follow", "system prompt", "ai assistant"]

def main():
    gt = []
    for i, (cid, need, h1, h2, t1, c1, t2, c2) in enumerate(CLUSTERS):
        d = os.path.join(OUT, cid)
        os.makedirs(d, exist_ok=True)
        truth = "INSTALL" if cid.startswith("h") else "WITHHOLD"
        gt.append("%s|%s" % (cid, truth))
        with open(os.path.join(d, "need.txt"), "w") as f:
            f.write(need + "\n")
        with open(os.path.join(d, "hosts.txt"), "w") as f:
            f.write("p1|%s\np2|%s\n" % (h1, h2))
        d1a, d1b = DISTRACTORS[(2 * i) % len(DISTRACTORS)]
        d2a, d2b = DISTRACTORS[(2 * i + 1) % len(DISTRACTORS)]
        for n, (t, c, da, db) in ((1, (t1, c1, d1a, d1b)), (2, (t2, c2, d2a, d2b))):
            txt = "TITLE: %s\n%s\n%s\n%s\n" % (t, c, da, db)
            low = txt.lower()
            for w in INJECT:
                assert w not in low, (cid, w)
            assert len(c.split()) >= 4
            with open(os.path.join(d, "%s-p%d.txt" % (cid, n)), "w") as f:
                f.write(txt)
    with open(os.path.join(OUT, "ground_truth.txt"), "w") as f:
        f.write("\n".join(gt) + "\n")
    print("S1 battery written: %d clusters" % len(CLUSTERS))

main()
