#!/usr/bin/env python3
"""Red-team expected R-lines, derived STRUCTURALLY from redteam/bindings_rt.txt.
The attacks must FAIL (implementation withstands them) for K7 to hold."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

def load_rt_bindings():
    b = {}
    with open(os.path.join(HERE, "bindings_rt.txt")) as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                k, v = line.split("=", 1)
                b[k] = v
    return b

def rt_expectations():
    b = load_rt_bindings()
    NA_A, NA_A_CAP = b["NA_A"], b["NA_A_CAP"]
    NA_D, NA_E = b["NA_D"], b["NA_E"]
    T_PET, T_COLOR = b["T_PET"], b["T_COLOR"]
    T_SONG, T_VAULT, T_BRIDGE = b["T_SONG"], b["T_VAULT"], b["T_BRIDGE"]
    V_CAT, V_BLUE = b["V_CAT"], b["V_BLUE"]
    V_SONGV, V_9901, V_OPEN = b["V_SONGV"], b["V_9901"], b["V_OPEN"]
    V_LONDON, V_PARIS = b["V_LONDON"], b["V_PARIS"]

    return {
        # R1: case-variant names must NOT merge
        "r1": [
            "R open p1 h=1",
            "R name p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            "R teach p1 ok",
            f"R recall p2 {T_PET} = WITHHOLD",
            f"R recall p1 {T_PET} = {V_CAT}",
            f"R who p1 = {NA_A}",
            f"R who p2 = {NA_A_CAP}",
        ],
        # R2: rename ping-pong; squatter sees nothing; facts track p1
        "r2": [
            "R open p1 h=1",
            "R name p1 ok",
            "R teach p1 ok",
            "R name p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            f"R recall p2 {T_COLOR} = WITHHOLD",
            "R name p1 ok",
            f"R recall p1 {T_COLOR} = {V_BLUE}",
            f"R recall p2 {T_COLOR} = WITHHOLD",
            f"R who p1 = {NA_A}",
            f"R who p2 = {NA_D}",
        ],
        # R3: enumeration exfiltration fails
        "r3": [
            "R open p1 h=1",
            "R name p1 ok",
            "R teach p1 ok",
            "R secret p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            "R topics p2 = EMPTY",
            f"R recall p2 {T_SONG} = WITHHOLD",
            f"R topics p1 = {T_SONG}",
            f"R profile p1 = name={NA_D} facts=2 beliefs=0 secrets=1 corrections=0",
        ],
        # R4: cross-person belief withholds; judge SINGLE / NONE
        "r4": [
            "R open p1 h=1",
            "R name p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            "R assert p1 ok",
            f"R belief p2 {T_BRIDGE} = WITHHOLD",
            f"R judge {T_BRIDGE} = SINGLE {V_OPEN}",
            f"R judge {T_COLOR} = NONE",
        ],
        # R5: confabulation pressure + malformed input
        "r5": [
            f"R recall p9 {T_PET} = WITHHOLD",
            "R who p9 = WITHHOLD",
            "R profile p9 = WITHHOLD",
            "R topics p9 = WITHHOLD",
            f"R judge {T_BRIDGE} = NONE",
            "R ERROR badop",
            "R ERROR badpid",
            "R open p1 h=1",
            "R ERROR badargs",
            f"R recall p1 {T_PET} = WITHHOLD",
        ],
        # R6: identical content; correction must not touch the other person
        "r6": [
            "R open p1 h=1",
            "R name p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            "R teach p1 ok",
            "R teach p2 ok",
            "R correct p2 ok",
            f"R recall p1 {T_COLOR} = {V_LONDON}",
            f"R recall p2 {T_COLOR} = {V_PARIS}",
            f"R profile p1 = name={NA_D} facts=1 beliefs=0 secrets=0 corrections=0",
            f"R profile p2 = name={NA_E} facts=1 beliefs=0 secrets=0 corrections=1",
        ],
    }
