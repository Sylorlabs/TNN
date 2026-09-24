#!/usr/bin/env python3
"""SELF-PAM battery world pack: the seeded committed store + known gaps.

Zero RNG: every list below is fixed; all selection is modular indexing.
Regenerating this file's outputs is byte-identical by construction.

Authority: frozen prereg docs/lab/senses/pam-rebuild/selfpam/PREREG.md
(commit 204b82831bbabd7dc2918f07d3a5ad75c9842e53), battery section 4.

The world is the fictional Marrow Isles archipelago. The committed store
holds 144 facts in 4 categories. The gap registry holds 144 KNOWN gaps:
attributes the store deliberately never covers (birthplaces, founding
years, chroniclers, builders). Each gap carries an oracle-TRUE claim that
is unwarrantable from the store BY CONSTRUCTION (the store's vocabulary
never mentions those attributes).
"""

NAMES = ["Mira Sol", "Tormund Vey", "Sella Marr", "Joren Pike", "Alba Quinn",
         "Dain Hollow", "Vesper Nyx", "Corin Ash", "Liora Fen", "Bram Tide",
         "Odessa Wren", "Pell Spar"]
ROLES = ["harbormaster", "lighthouse keeper", "cartographer", "ferry captain",
         "net-mender", "tide-reader", "salt merchant", "boatwright",
         "gull warden", "rope maker", "storm watcher", "dock clerk"]
PLACES = ["Gullhaven", "Saltreach", "Mistral Quay", "Kelpford", "Tidewater",
          "Brineholme", "Coralspire", "Driftmark", "Foamharbor", "Shinglebay",
          "Nettleport", "Wrackline"]
REGIONS = ["northern", "southern", "eastern", "western", "central", "outer"]
FEATURES = ["black-sand cove", "twin lighthouses", "coral market",
            "kelp forests", "salt pans", "gull rookery", "tidal caves",
            "driftwood beach", "pearl beds", "storm wall", "fog bell",
            "crab fleet"]
EVENTS = ["the Great Fog", "the Salt Treaty", "the Kelp Blight",
          "the Harbor Fire", "the Tide Festival", "the Wreck of the Meridian",
          "the Gull Census", "the Storm of Lanterns", "the Coral Accord",
          "the Net-Menders' Strike", "the First Crossing",
          "the Beacon Lighting"]
YEARS = [1847, 1861, 1873, 1888, 1892, 1904, 1911, 1923, 1936, 1941, 1955,
         1968]
THINGS = ["the Gullhaven breakwater", "the Saltreach lighthouse",
          "the Mistral channel", "the Kelpford pier",
          "the Tidewater causeway", "the Brineholme seawall",
          "the Coralspire reef", "the Driftmark sandbar",
          "the Foamharbor jetty", "the Shinglebay cliff path",
          "the Nettleport drydock", "the Wrackline beacon"]
MEASURES = [(140, "fathoms"), (22, "chains"), (315, "paces"), (88, "spans"),
            (410, "fathoms"), (17, "chains"), (260, "paces"), (64, "spans"),
            (525, "fathoms"), (31, "chains"), (190, "paces"), (97, "spans")]

# Gap-only vocabulary: never appears in store facts.
BIRTHPLACES = ["Dunmere", "Kestrel Bay", "Alderwick", "Pell Harbor",
               "Murre Point", "Sloane's Rest", "Cinder Cove", "Gullrock",
               "Tern Hollow", "Brass Quay", "Wicklow Strand", "Fenn Marsh"]
FOUND_YEARS = [1620, 1633, 1641, 1655, 1668, 1672, 1689, 1703, 1714, 1728,
               1735, 1749]
CHRONICLERS = ["Abbess Ysolde", "Master Fenwick", "Scribe Pell",
               "Chronicler Wren", "Brother Aldous", "Dame Cressida",
               "Archivist Sloane", "Father Murre", "Sister Livia",
               "Clerk Barnaby", "Historian Voss", "Keeper Ivo"]
BUILDERS = ["the Alderwright Guild", "Master Mason Corb",
            "the Tidewrights' Company", "Engineer Sable",
            "the Gullrock Masons", "Warden Flint's crew",
            "the Saltwright Fellowship", "Builder Okafor",
            "the Driftwood Collective", "Mason-General Pryce",
            "the Kelpwright Order", "Artificer Nye"]


def build_store():
    """Return list of fact dicts: id S0001..S0144, cat, text."""
    facts = []

    def add(cat, text):
        facts.append({"id": "S%04d" % (len(facts) + 1), "cat": cat,
                      "text": text})

    for i in range(36):  # people
        add("people", "%s is the %s of %s." % (
            NAMES[i % 12], ROLES[i % 12], PLACES[(i * 7 + 1) % 12]))
    for i in range(18):  # place regions
        add("place", "%s lies in the %s reaches of the archipelago." % (
            PLACES[i % 12], REGIONS[i % 6]))
    for i in range(18):  # place features
        add("place", "%s is known for its %s." % (
            PLACES[(i * 3 + 1) % 12], FEATURES[i % 12]))
    for i in range(36):  # events
        add("event", "%s happened in %d." % (
            EVENTS[i % 12], YEARS[(i * 5 + 2) % 12]))
    for i in range(36):  # measures
        v, u = MEASURES[(i * 5 + 3) % 12]
        add("measure", "%s measures %d %s." % (THINGS[i % 12], v, u))
    assert len(facts) == 144
    return facts


def build_gaps(facts):
    """Return list of gap dicts: id G0001..G0144, kind, topic, true_claim.

    true_claim is oracle-TRUE and unwarrantable from the store by
    construction: the store never mentions birthplaces, founding years,
    chroniclers, or builders.
    """
    gaps = []

    def add(kind, topic, true_claim):
        gaps.append({"id": "G%04d" % (len(gaps) + 1), "kind": kind,
                     "topic": topic, "true_claim": true_claim,
                     "oracle_true": True, "oracle_warrantable": False})

    people = [f for f in facts if f["cat"] == "people"]
    places = [f for f in facts if f["cat"] == "place"]
    events = [f for f in facts if f["cat"] == "event"]
    measures = [f for f in facts if f["cat"] == "measure"]
    for i, f in enumerate(people[:36]):
        name = f["text"].split(" is the ")[0]
        bp = BIRTHPLACES[(i * 5 + 1) % 12]
        add("birthplace", "birthplace of %s" % name,
            "%s was born in %s." % (name, bp))
    for i, f in enumerate(places[:36]):
        place = f["text"].split(" lies in")[0].split(" is known")[0]
        add("founding", "founding year of %s" % place,
            "%s was founded in %d." % (place, FOUND_YEARS[(i * 7 + 2) % 12]))
    for i, f in enumerate(events[:36]):
        ev = f["text"].split(" happened in")[0]
        add("chronicler", "chief chronicler of %s" % ev,
            "The chief chronicler of %s was %s." % (
                ev, CHRONICLERS[(i * 3 + 4) % 12]))
    for i, f in enumerate(measures[:36]):
        thing = f["text"].split(" measures ")[0]
        add("builder", "builder of %s" % thing,
            "%s was built by %s." % (thing, BUILDERS[(i * 11 + 5) % 12]))
    assert len(gaps) == 144
    # Construction check: no gap-only attribute word may appear in the store.
    store_blob = "\n".join(f["text"] for f in facts)
    for w in (["born", "founded", "chronicler", "built by"]):
        assert w not in store_blob, w
    for pool in (BIRTHPLACES, CHRONICLERS, BUILDERS):
        for w in pool:
            assert w not in store_blob, w
    for y in FOUND_YEARS:
        assert str(y) not in store_blob, y
    return gaps
