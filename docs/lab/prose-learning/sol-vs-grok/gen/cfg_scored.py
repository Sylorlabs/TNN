"""Scored vocabulary: SEALED until both implementation crews freeze their builds.
Word-disjoint from calib in every entity, relation word, and distractor;
different value constants. Generated only after build freeze;
validated by check_sg.py (0 failures required)."""
CONFIG = {
    "relations": [
        ("grain storage", "cereal hold"),
        ("oar tally", "rowing benches"),
        ("mast height", "spar elevation"),
        ("river pace", "stream velocity"),
        ("keel season", "frame vintage"),
        ("quay niche", "wharf nook"),
        ("rope coils", "cable bundles"),
        ("plumb drop", "leadline fall"),
        ("deck span", "plank reach"),
        ("water barrels", "cask reserve"),
        ("hammock tally", "bunk total"),
        ("sail heft", "canvas poundage"),
    ],
    "ent_main": ["Briarholt", "Thistledown", "Oakenshield", "Willowmere",
                 "Ashenford", "Elmsworth", "Birchgrove", "Thornfield"],
    "ent_neg": ["Gloomharbor", "Murkport", "Shadehaven", "Duskwater",
                "Nightmere", "Darkholme", "Sablebay", "Ebonreach"],
    "ent_hedge": ["Fableport", "Talehaven", "Mythmere", "Legendholm",
                  "Storywick", "Fablemere", "Talltalia", "Yarnmouth"],
    "ent_contr": ["Feudport", "Clashhaven", "Rivalmere", "Opalholm",
                  "Joustwick", "Tiltsburg", "Versalia", "Antipod"],
    "ent_distr": ["Wispbay", "Phantomport", "Specterhaven", "Apparmere",
                  "Ghostwick", "Shadeport", "Ectohaven", "Poltermere"],
    "distr_rels": ["rudder sweep", "sail tint", "galley hand"],
    "multi_rels": [
        ("lantern glow", "lamp brightness"),
        ("iron fetter", "hemp hawser"),
        ("gull cries", "tern calls"),
        ("tide mark", "surf line"),
    ],
    "multi_v0": 700,
    "multi_dv": 11,
    "value_params": (11, 53, 29, 410, 1790, 170),
    "year_rel": 4,
    "contr_delta": 23,
}
