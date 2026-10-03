#!/usr/bin/env python3
"""Phase-4 RED-TEAM probe generator. Seed 20260928 (frozen in PREREG.md section 7).
Novel attacks R1-R6, NOT repeats of S1-S8. Content is a fresh draw so the
implementation cannot have been shaped to it (it was built before this file
existed). Emits redteam/bindings_rt.txt, redteam/probes/r1.txt..r6.txt,
redteam/SHA256SUMS_RT.txt."""
import hashlib, os, random

SEED = 20260928
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

def main():
    rng = random.Random(SEED)
    names = rng.sample(NAMES, 4)
    topics = rng.sample(TOPICS, 5)
    values = rng.sample(VALUES, 8)
    NA_A, NA_D, NA_E, NA_F = names
    T_PET, T_COLOR, T_SONG, T_VAULT, T_BRIDGE = topics
    V_CAT, V_BLUE, V_SONGV, V_9901, V_OPEN, V_LONDON, V_PARIS, V_DOG = values
    NA_A_CAP = NA_A.capitalize()

    b = {"NA_A": NA_A, "NA_A_CAP": NA_A_CAP, "NA_D": NA_D, "NA_E": NA_E,
         "NA_F": NA_F, "T_PET": T_PET, "T_COLOR": T_COLOR, "T_SONG": T_SONG,
         "T_VAULT": T_VAULT, "T_BRIDGE": T_BRIDGE, "V_CAT": V_CAT,
         "V_BLUE": V_BLUE, "V_SONGV": V_SONGV, "V_9901": V_9901,
         "V_OPEN": V_OPEN, "V_LONDON": V_LONDON, "V_PARIS": V_PARIS,
         "V_DOG": V_DOG}
    os.makedirs(PROBES, exist_ok=True)
    with open(os.path.join(HERE, "bindings_rt.txt"), "w") as f:
        for k in sorted(b):
            f.write(f"{k}={b[k]}\n")

    probes = {
        # R1: case-variant name collision must NOT merge persons
        "r1.txt": [
            "open p1",
            f"name p1 {NA_A}",
            "open p2",
            f"name p2 {NA_A_CAP}",
            f"teach p1 {T_PET} {V_CAT}",
            f"recall p2 {T_PET}",
            f"recall p1 {T_PET}",
            "who p1",
            "who p2",
        ],
        # R2: rename ping-pong; a mid-way name-squatter sees nothing
        "r2.txt": [
            "open p1",
            f"name p1 {NA_A}",
            f"teach p1 {T_COLOR} {V_BLUE}",
            f"name p1 {NA_D}",
            "open p2",
            f"name p2 {NA_D}",
            f"recall p2 {T_COLOR}",
            f"name p1 {NA_A}",
            f"recall p1 {T_COLOR}",
            f"recall p2 {T_COLOR}",
            "who p1",
            "who p2",
        ],
        # R3: enumeration must not exfiltrate (secrets never listed; nothing cross-person)
        "r3.txt": [
            "open p1",
            f"name p1 {NA_D}",
            f"teach p1 {T_SONG} {V_SONGV}",
            f"secret p1 {T_VAULT} {V_9901}",
            "open p2",
            f"name p2 {NA_E}",
            "topics p2",
            f"recall p2 {T_SONG}",
            "topics p1",
            "profile p1",
        ],
        # R4: cross-person belief withhold; judge SINGLE and NONE
        "r4.txt": [
            "open p1",
            f"name p1 {NA_D}",
            "open p2",
            f"name p2 {NA_E}",
            f"assert p1 {T_BRIDGE} {V_OPEN}",
            f"belief p2 {T_BRIDGE}",
            f"judge {T_BRIDGE}",
            f"judge {T_COLOR}",
        ],
        # R5: confabulation pressure + malformed input robustness
        "r5.txt": [
            f"recall p9 {T_PET}",
            "who p9",
            "profile p9",
            "topics p9",
            f"judge {T_BRIDGE}",
            "bogus p1",
            f"recall p99 {T_PET}",
            "open p1",
            "teach p1",
            f"recall p1 {T_PET}",
        ],
        # R6: identical content, correction must not touch the other person
        "r6.txt": [
            "open p1",
            f"name p1 {NA_D}",
            "open p2",
            f"name p2 {NA_E}",
            f"teach p1 {T_COLOR} {V_LONDON}",
            f"teach p2 {T_COLOR} {V_LONDON}",
            f"correct p2 {T_COLOR} {V_PARIS}",
            f"recall p1 {T_COLOR}",
            f"recall p2 {T_COLOR}",
            "profile p1",
            "profile p2",
        ],
    }
    sums = []
    for name, lines in probes.items():
        p = os.path.join(PROBES, name)
        with open(p, "w") as f:
            f.write("\n".join(lines) + "\n")
    for fn in ["bindings_rt.txt"] + [f"probes/{k}" for k in probes]:
        p = os.path.join(HERE, fn)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        sums.append(f"{h}  {fn}")
    with open(os.path.join(HERE, "SHA256SUMS_RT.txt"), "w") as f:
        f.write("\n".join(sums) + "\n")
    print("\n".join(sums))
    print("bindings:", b)

if __name__ == "__main__":
    main()
