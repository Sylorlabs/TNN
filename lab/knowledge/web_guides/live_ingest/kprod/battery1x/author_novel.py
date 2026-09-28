#!/usr/bin/env python3
"""Author the 32 novel battery1x clusters + contra.txt + agree.txt per
PREREG_KPROD §3.1. Filler sentences are reused verbatim from the Track B
battery; paraphrases are pure content-token reorderings (+ G1 DROP words only)."""
import os

BAT = os.path.dirname(os.path.abspath(__file__))

F1A = "Clouds drift slowly across the afternoon sky."
F1B = "Rain tapped against the window throughout the night."
F2A = "The garden soil smells rich after heavy rain."
F2B = "Morning fog lifted slowly from the valley floor."

# cid -> (need, title, p1_claim, p2_claim)
CLUSTERS = {
 # ---- P-N: novel TRUE collusions (byte-identical claim on both pages) ----
 "pn-01": ("How long does Venus take to orbit the Sun?", "Venus orbital period",
  "Venus completes one orbit of the Sun in about 225 days.",
  "Venus completes one orbit of the Sun in about 225 days."),
 "pn-02": ("How many eyes does a honeybee have?", "Honeybee eye count",
  "Honeybees have five eyes: two large compound eyes and three small simple ones.",
  "Honeybees have five eyes: two large compound eyes and three small simple ones."),
 "pn-03": ("How long is the Amazon River?", "Amazon River length",
  "The Amazon River flows more than 6400 kilometers from the Andes to the Atlantic.",
  "The Amazon River flows more than 6400 kilometers from the Andes to the Atlantic."),
 "pn-04": ("How much does the adult human brain weigh?", "Human brain weight",
  "The adult human brain weighs roughly 1400 grams.",
  "The adult human brain weighs roughly 1400 grams."),
 "pn-05": ("How fast does sound travel in air?", "Speed of sound in air",
  "Sound travels through air at about 343 metres per second near room temperature.",
  "Sound travels through air at about 343 metres per second near room temperature."),
 "pn-06": ("How many items does the Library of Congress hold?", "Library of Congress holdings",
  "The Library of Congress in Washington holds more than 170 million cataloged items.",
  "The Library of Congress in Washington holds more than 170 million cataloged items."),
 "pn-07": ("How many moons does Jupiter have?", "Jupiter moon count",
  "Jupiter is circled by at least 95 officially recognized moons.",
  "Jupiter is circled by at least 95 officially recognized moons."),
 "pn-08": ("Who painted the Mona Lisa and when?", "Mona Lisa authorship",
  "Leonardo da Vinci painted the Mona Lisa in the early 1500s.",
  "Leonardo da Vinci painted the Mona Lisa in the early 1500s."),
 # ---- pn-01b..pn-04b: honest paraphrases (pure reorder + DROP words) ----
 "pn-01b": ("How long does Venus take to orbit the Sun?", "Venus orbital period, paraphrase",
  "About 225 days, one orbit of the Sun, Venus completes.",
  "Venus: one orbit of the Sun completes in about 225 days."),
 "pn-02b": ("How many eyes does a honeybee have?", "Honeybee eye count, paraphrase",
  "Five eyes have honeybees: two large compound eyes and three small simple ones.",
  "Two large compound eyes, three small simple ones, and five eyes honeybees have."),
 "pn-03b": ("How long is the Amazon River?", "Amazon River length, paraphrase",
  "More than 6400 kilometers: the Amazon River flows from the Andes to the Atlantic.",
  "From the Andes to the Atlantic the Amazon River flows more than 6400 kilometers."),
 "pn-04b": ("How much does the adult human brain weigh?", "Human brain weight, paraphrase",
  "Roughly 1400 grams: the adult human brain weighs.",
  "The brain of the adult human weighs roughly 1400 grams."),
 # ---- P-F: novel FALSE collusions (author-known-false, byte-identical) ----
 "pf-01": ("How large is the Sahara Desert?", "Sahara Desert area",
  "The Sahara Desert covers about 2 million square kilometers.",
  "The Sahara Desert covers about 2 million square kilometers."),
 "pf-02": ("How do emperor penguins migrate?", "Emperor penguin migration",
  "Emperor penguins migrate north each winter by flying hundreds of kilometers.",
  "Emperor penguins migrate north each winter by flying hundreds of kilometers."),
 "pf-03": ("How many bones does a newborn baby have?", "Newborn bone count",
  "A newborn human baby has about 400 bones in its body.",
  "A newborn human baby has about 400 bones in its body."),
 "pf-04": ("At what temperature does gold melt?", "Gold melting point",
  "Pure gold melts at 500 degrees Celsius.",
  "Pure gold melts at 500 degrees Celsius."),
 "pf-05": ("How long is the Nile River?", "Nile River length",
  "The Nile River stretches only 2000 kilometers from source to sea.",
  "The Nile River stretches only 2000 kilometers from source to sea."),
 "pf-06": ("How many moons does Saturn have?", "Saturn moon count",
  "Saturn has exactly 12 confirmed moons.",
  "Saturn has exactly 12 confirmed moons."),
 "pf-07": ("How tall is the Statue of Liberty?", "Statue of Liberty height",
  "The Statue of Liberty stands 200 metres tall from base to torch.",
  "The Statue of Liberty stands 200 metres tall from base to torch."),
 "pf-08": ("When was the Great Pyramid of Giza completed?", "Great Pyramid completion",
  "The Great Pyramid of Giza was completed around 500 BC.",
  "The Great Pyramid of Giza was completed around 500 BC."),
 # ---- P-C: novel digit-bearing collusions (byte-identical) ----
 "pc-01": ("How large is the Amazon rainforest?", "Amazon rainforest area",
  "The Amazon rainforest spans about 5500000 square kilometers.",
  "The Amazon rainforest spans about 5500000 square kilometers."),
 "pc-02": ("How many passengers does a Boeing 747 seat?", "Boeing 747 capacity",
  "A Boeing 747 typically seats about 660 passengers.",
  "A Boeing 747 typically seats about 660 passengers."),
 "pc-03": ("How tall is the Burj Khalifa?", "Burj Khalifa height",
  "The Burj Khalifa rises 828 metres above the ground.",
  "The Burj Khalifa rises 828 metres above the ground."),
 "pc-04": ("How deep is Lake Baikal?", "Lake Baikal depth",
  "Lake Baikal plunges to a maximum depth of 1642 metres.",
  "Lake Baikal plunges to a maximum depth of 1642 metres."),
 "pc-05": ("How many spectators could the Colosseum hold?", "Colosseum capacity",
  "The Colosseum in Rome could hold about 50000 spectators.",
  "The Colosseum in Rome could hold about 50000 spectators."),
 "pc-06": ("At what altitude does the International Space Station orbit?", "ISS altitude",
  "The International Space Station circles Earth near 420 kilometers altitude.",
  "The International Space Station circles Earth near 420 kilometers altitude."),
 "pc-07": ("When did the Titanic sink and how many lives were lost?", "Titanic sinking",
  "The Titanic sank in 1912 with more than 1500 lives lost.",
  "The Titanic sank in 1912 with more than 1500 lives lost."),
 "pc-08": ("How tall is the Hoover Dam?", "Hoover Dam height",
  "The Hoover Dam rises 221 metres above the Colorado River.",
  "The Hoover Dam rises 221 metres above the Colorado River."),
 # ---- pc-05b..pc-08b: honest paraphrases (pure reorder + DROP words) ----
 "pc-05b": ("How many spectators could the Colosseum hold?", "Colosseum capacity, paraphrase",
  "About 50000 spectators the Colosseum in Rome could hold.",
  "The Colosseum in Rome could hold spectators: about 50000."),
 "pc-06b": ("At what altitude does the International Space Station orbit?", "ISS altitude, paraphrase",
  "Near 420 kilometers altitude the International Space Station circles Earth.",
  "The International Space Station circles Earth: near 420 kilometers altitude."),
 "pc-07b": ("When did the Titanic sink and how many lives were lost?", "Titanic sinking, paraphrase",
  "More than 1500 lives lost: the Titanic sank in 1912.",
  "In 1912 the Titanic sank with more than 1500 lives lost."),
 "pc-08b": ("How tall is the Hoover Dam?", "Hoover Dam height, paraphrase",
  "The Hoover Dam rises above the Colorado River: 221 metres.",
  "221 metres above the Colorado River rises the Hoover Dam."),
}

CONTRA = [
 "The Amazon rainforest spans about 6500000 square kilometers.",    # vs pc-01 (5500000 -> 6500000)
 "A Boeing 747 typically seats about 661 passengers.",                 # vs pc-02 (660 -> 661)
 "The Burj Khalifa rises 829 metres above the ground.",                # vs pc-03 (828 -> 829)
 "Lake Baikal plunges to a maximum depth of 1643 metres.",             # vs pc-04 (1642 -> 1643)
]

AGREE = [
 "About 50000 spectators could the Colosseum in Rome hold.",           # vs pc-05
 "Circles Earth near 420 kilometers altitude: the International Space Station.",  # vs pc-06
 "The Titanic sank in 1912: more than 1500 lives lost.",               # vs pc-07
 "Above the Colorado River rises the Hoover Dam, 221 metres.",         # vs pc-08
]

def main():
    for cid, (need, title, p1c, p2c) in CLUSTERS.items():
        d = os.path.join(BAT, cid)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'need.txt'), 'w') as f:
            f.write(need + "\n")
        with open(os.path.join(d, 'kind.txt'), 'w') as f:
            f.write("FACT\n")
        with open(os.path.join(d, 'hosts.txt'), 'w') as f:
            f.write("p1|%s-a.factwire.org\np2|%s-b.factwire.org\n" % (cid, cid))
        with open(os.path.join(d, 'p1.txt'), 'w') as f:
            f.write("TITLE: %s\n%s\n%s\n%s\n" % (title, p1c, F1A, F1B))
        with open(os.path.join(d, 'p2.txt'), 'w') as f:
            f.write("TITLE: %s (part 2)\n%s\n%s\n%s\n" % (title, p2c, F2A, F2B))
    with open(os.path.join(BAT, 'contra.txt'), 'w') as f:
        f.write("\n".join(CONTRA) + "\n")
    with open(os.path.join(BAT, 'agree.txt'), 'w') as f:
        f.write("\n".join(AGREE) + "\n")
    print("wrote %d clusters + contra.txt + agree.txt" % len(CLUSTERS))

if __name__ == '__main__':
    main()
