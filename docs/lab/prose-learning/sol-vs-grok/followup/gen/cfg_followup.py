#!/usr/bin/env python3
"""FOLLOWUP battery config (sealed until build freeze).

Same structure as cfg_calib / cfg_scored; disjoint celestial vocabulary.
Frozen by PREREG-SG-FOLLOWUP.md §F5.1. Builders see this file (like the
calib config) but never the generated battery before scoring.
"""
CONFIG = {
    "relations": [
        ("star magnitude", "stellar brightness"),
        ("moon phase", "lunar cycle"),
        ("comet tail", "comet train"),
        ("orbit period", "revolution time"),
        ("planet mass", "planetary weight"),
        ("nebula span", "cloud expanse"),
        ("eclipse hour", "occultation time"),
        ("tide height", "tidal rise"),
        ("aurora glow", "polar light"),
        ("crater depth", "basin depth"),
        ("solar flare", "sun eruption"),
        ("galaxy tally", "star count"),
    ],
    "ent_main": ["Zephyria", "Quillon", "Vespera", "Lumina",
                 "Noctua", "Aurelia", "Stellia", "Astrala"],
    "ent_neg": ["Duskwatch", "Grimhold", "Murkfell", "Shadewick",
                "Nightfall", "Darkmere", "Sableport", "Ebonwick"],
    "ent_hedge": ["Quibble", "Waverly", "Hazemere", "Mistmere",
                  "Dithera", "Vacilla", "Fluctua", "Wobblia"],
    "ent_contr": ["Feudwick", "Clashmere", "Rivalwick", "Joustmere",
                  "Contenda", "Oppugna", "Adversa", "Contraria"],
    "ent_distr": ["Wispmere", "Phantomwick", "Specterwick", "Apparia",
                  "Ghostmere", "Shademere", "Ectowick", "Polterwick"],
    "distr_rels": ["satellite name", "telescope lens", "rocket fuel"],
    "multi_rels": [("quasar flare", "quasar outburst"),
                   ("pulsar beat", "pulsar rhythm"),
                   ("meteor streak", "meteor trail"),
                   ("ring system", "annular band")],
    "year_rel": 4,
    "contr_delta": 19,
    "multi_v0": 800,
    "multi_dv": 13,
    "value_params": (13, 47, 31, 420, 1810, 190),
}
