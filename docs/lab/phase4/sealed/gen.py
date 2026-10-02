#!/usr/bin/env python3
"""Phase 4 sealed-content generator. Deterministic: seed 20260927 (frozen in PREREG.md).
Emits sealed/bindings.txt, sealed/probes/s1.txt..s8.txt, sealed/SHA256SUMS.txt.
Wordlists and slot order are frozen in the prereg; this script is the mechanical
instantiation. The battery binary (p4.zag, written AFTER the prereg commit) never
sees this content as literals (verified by grep audit in the red-team phase).
"""
import hashlib, os, random, sys

SEED = 20260927
HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(HERE, "probes")

NAMES = ["alice","bob","carol","dave","erin","frank","grace","heidi","ivan",
         "judy","mallory","nina","oscar","peggy","quinn","ruth","sam","trent",
         "uma","victor","wendy","xena","yvonne","zane"]
TOPICS = ["color","pet","city","song","food","sport","book","film","tree",
          "bird","river","mountain","team","drink","game","tool"]
VALUES = ["blue","crimson","cat","dog","fish","london","paris","tokyo","open",
          "closed","9901","7750","violin","piano","oak","pine","falcon","wren",
          "thames","seine","chess","tennis","hammer","saw"]

NAME_SLOTS = ["NA_A","NA_B","NA_Z","NA_C","NA_D","NA_E"]
TOPIC_SLOTS = ["T_COLOR","T_PET","T_CITY","T_BRIDGE","T_VAULT","T_SONG"]
VALUE_SLOTS = ["V_BLUE","V_CAT","V_DOG","V_FISH","V_LONDON","V_PARIS",
               "V_OPEN","V_CLOSED","V_9901","V_SONGV"]

def main():
    rng = random.Random(SEED)
    b = {}
    for s, v in zip(NAME_SLOTS, rng.sample(NAMES, len(NAME_SLOTS))):
        b[s] = v
    for s, v in zip(TOPIC_SLOTS, rng.sample(TOPICS, len(TOPIC_SLOTS))):
        b[s] = v
    for s, v in zip(VALUE_SLOTS, rng.sample(VALUES, len(VALUE_SLOTS))):
        b[s] = v

    os.makedirs(PROBES, exist_ok=True)
    with open(os.path.join(HERE, "bindings.txt"), "w") as f:
        for s in NAME_SLOTS + TOPIC_SLOTS + VALUE_SLOTS:
            f.write(f"{s}={b[s]}\n")

    probes = {
        # S1: rename follows the PERSON (K1)
        "s1.txt": [
            "open p1",
            f"name p1 {b['NA_A']}",
            f"teach p1 {b['T_COLOR']} {b['V_BLUE']}",
            f"name p1 {b['NA_B']}",
            f"recall p1 {b['T_COLOR']}",
            "who p1",
        ],
        # S2: recycled name does NOT inherit (K1)
        "s2.txt": [
            "open p1",
            f"name p1 {b['NA_A']}",
            f"teach p1 {b['T_COLOR']} {b['V_BLUE']}",
            f"name p1 {b['NA_B']}",
            "open p2",
            f"name p2 {b['NA_A']}",
            f"recall p2 {b['T_COLOR']}",
            "who p2",
            f"recall p1 {b['T_COLOR']}",
        ],
        # S3: two persons, same presented name (K1/K2)
        "s3.txt": [
            "open p1",
            f"name p1 {b['NA_Z']}",
            "open p2",
            f"name p2 {b['NA_Z']}",
            f"teach p1 {b['T_PET']} {b['V_CAT']}",
            f"teach p2 {b['T_PET']} {b['V_DOG']}",
            f"recall p1 {b['T_PET']}",
            f"recall p2 {b['T_PET']}",
            "profile p1",
            "profile p2",
        ],
        # S4: new person withholds, then builds fresh (K3/K2)
        "s4.txt": [
            "open p1",
            f"name p1 {b['NA_A']}",
            f"teach p1 {b['T_PET']} {b['V_CAT']}",
            "open p2",
            f"name p2 {b['NA_C']}",
            f"recall p2 {b['T_PET']}",
            f"recall p2 {b['T_COLOR']}",
            "profile p2",
            f"teach p2 {b['T_PET']} {b['V_FISH']}",
            f"recall p2 {b['T_PET']}",
            f"recall p1 {b['T_PET']}",
            "topics p2",
        ],
        # S5: conflicting per-person beliefs, no collapse (K4)
        "s5.txt": [
            "open p1",
            f"name p1 {b['NA_D']}",
            "open p2",
            f"name p2 {b['NA_E']}",
            f"assert p1 {b['T_BRIDGE']} {b['V_OPEN']}",
            f"assert p2 {b['T_BRIDGE']} {b['V_CLOSED']}",
            f"belief p1 {b['T_BRIDGE']}",
            f"belief p2 {b['T_BRIDGE']}",
            f"judge {b['T_BRIDGE']}",
            f"belief p1 {b['T_PET']}",
        ],
        # S6: secret leakage bar (K2)
        "s6.txt": [
            "open p1",
            f"name p1 {b['NA_D']}",
            "open p2",
            f"name p2 {b['NA_E']}",
            f"teach p1 {b['T_SONG']} {b['V_SONGV']}",
            f"secret p1 {b['T_VAULT']} {b['V_9901']}",
            f"recall p1 {b['T_VAULT']}",
            f"recall p2 {b['T_VAULT']}",
            f"recall p2 {b['T_SONG']}",
            "topics p2",
            "topics p1",
            "profile p1",
        ],
        # S7: correction is person-scoped (K5)
        "s7.txt": [
            "open p1",
            f"name p1 {b['NA_D']}",
            "open p2",
            f"name p2 {b['NA_E']}",
            f"teach p1 {b['T_CITY']} {b['V_LONDON']}",
            f"teach p2 {b['T_CITY']} {b['V_LONDON']}",
            f"correct p1 {b['T_CITY']} {b['V_PARIS']}",
            f"recall p1 {b['T_CITY']}",
            f"recall p2 {b['T_CITY']}",
            "profile p1",
            "profile p2",
        ],
        # S8: empty name is a mere attribute; close deletes (K3)
        "s8.txt": [
            "open p1",
            'name p1 ""',
            f"teach p1 {b['T_COLOR']} {b['V_BLUE']}",
            f"recall p1 {b['T_COLOR']}",
            "who p1",
            "close p1",
            f"recall p1 {b['T_COLOR']}",
            "who p1",
            "profile p1",
            "open p1",
            f"recall p1 {b['T_COLOR']}",
        ],
    }
    sums = []
    for name, lines in probes.items():
        p = os.path.join(PROBES, name)
        with open(p, "w") as f:
            f.write("\n".join(lines) + "\n")
    for fn in ["bindings.txt"] + [f"probes/{k}" for k in probes]:
        p = os.path.join(HERE, fn)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        sums.append(f"{h}  {fn}")
    with open(os.path.join(HERE, "SHA256SUMS.txt"), "w") as f:
        f.write("\n".join(sums) + "\n")
    print("\n".join(sums))

if __name__ == "__main__":
    main()
