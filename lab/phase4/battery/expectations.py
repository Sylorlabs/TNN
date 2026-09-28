#!/usr/bin/env python3
"""Phase-4 expected R-lines, derived STRUCTURALLY from sealed/bindings.txt.
No expected value is hardcoded: every content token comes from the seal.
Mirrors the frozen probe structures in PREREG.md section 5."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SEALED = os.path.join(HERE, "..", "sealed")

def load_bindings():
    b = {}
    with open(os.path.join(SEALED, "bindings.txt")) as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                k, v = line.split("=", 1)
                b[k] = v
    return b

def expectations():
    b = load_bindings()
    NA_A, NA_B, NA_Z = b["NA_A"], b["NA_B"], b["NA_Z"]
    NA_C, NA_D, NA_E = b["NA_C"], b["NA_D"], b["NA_E"]
    T_COLOR, T_PET = b["T_COLOR"], b["T_PET"]
    T_CITY, T_BRIDGE = b["T_CITY"], b["T_BRIDGE"]
    T_VAULT, T_SONG = b["T_VAULT"], b["T_SONG"]
    V_BLUE, V_CAT, V_DOG = b["V_BLUE"], b["V_CAT"], b["V_DOG"]
    V_FISH, V_LONDON, V_PARIS = b["V_FISH"], b["V_LONDON"], b["V_PARIS"]
    V_OPEN, V_CLOSED = b["V_OPEN"], b["V_CLOSED"]
    V_9901, V_SONGV = b["V_9901"], b["V_SONGV"]

    return {
        "s1": [
            "R open p1 h=1",
            "R name p1 ok",
            "R teach p1 ok",
            "R name p1 ok",
            f"R recall p1 {T_COLOR} = {V_BLUE}",
            f"R who p1 = {NA_B}",
        ],
        "s2": [
            "R open p1 h=1",
            "R name p1 ok",
            "R teach p1 ok",
            "R name p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            f"R recall p2 {T_COLOR} = WITHHOLD",
            f"R who p2 = {NA_A}",
            f"R recall p1 {T_COLOR} = {V_BLUE}",
        ],
        "s3": [
            "R open p1 h=1",
            "R name p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            "R teach p1 ok",
            "R teach p2 ok",
            f"R recall p1 {T_PET} = {V_CAT}",
            f"R recall p2 {T_PET} = {V_DOG}",
            f"R profile p1 = name={NA_Z} facts=1 beliefs=0 secrets=0 corrections=0",
            f"R profile p2 = name={NA_Z} facts=1 beliefs=0 secrets=0 corrections=0",
        ],
        "s4": [
            "R open p1 h=1",
            "R name p1 ok",
            "R teach p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            f"R recall p2 {T_PET} = WITHHOLD",
            f"R recall p2 {T_COLOR} = WITHHOLD",
            f"R profile p2 = name={NA_C} facts=0 beliefs=0 secrets=0 corrections=0",
            "R teach p2 ok",
            f"R recall p2 {T_PET} = {V_FISH}",
            f"R recall p1 {T_PET} = {V_CAT}",
            f"R topics p2 = {T_PET}",
        ],
        "s5": [
            "R open p1 h=1",
            "R name p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            "R assert p1 ok",
            "R assert p2 ok",
            f"R belief p1 {T_BRIDGE} = {V_OPEN}",
            f"R belief p2 {T_BRIDGE} = {V_CLOSED}",
            f"R judge {T_BRIDGE} = CONFLICT {V_OPEN} {V_CLOSED}",
            f"R belief p1 {T_PET} = WITHHOLD",
        ],
        "s6": [
            "R open p1 h=1",
            "R name p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            "R teach p1 ok",
            "R secret p1 ok",
            f"R recall p1 {T_VAULT} = {V_9901}",
            f"R recall p2 {T_VAULT} = WITHHOLD",
            f"R recall p2 {T_SONG} = WITHHOLD",
            "R topics p2 = EMPTY",
            f"R topics p1 = {T_SONG}",
            f"R profile p1 = name={NA_D} facts=2 beliefs=0 secrets=1 corrections=0",
        ],
        "s7": [
            "R open p1 h=1",
            "R name p1 ok",
            "R open p2 h=2",
            "R name p2 ok",
            "R teach p1 ok",
            "R teach p2 ok",
            "R correct p1 ok",
            f"R recall p1 {T_CITY} = {V_PARIS}",
            f"R recall p2 {T_CITY} = {V_LONDON}",
            f"R profile p1 = name={NA_D} facts=1 beliefs=0 secrets=0 corrections=1",
            f"R profile p2 = name={NA_E} facts=1 beliefs=0 secrets=0 corrections=0",
        ],
        "s8": [
            "R open p1 h=1",
            "R name p1 ok",
            "R teach p1 ok",
            f"R recall p1 {T_COLOR} = {V_BLUE}",
            "R who p1 = ",
            "R close p1 ok",
            f"R recall p1 {T_COLOR} = WITHHOLD",
            "R who p1 = WITHHOLD",
            "R profile p1 = WITHHOLD",
            "R open p1 h=1",
            f"R recall p1 {T_COLOR} = WITHHOLD",
        ],
    }
