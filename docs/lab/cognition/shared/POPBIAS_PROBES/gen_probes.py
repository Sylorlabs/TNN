#!/usr/bin/env python3
"""Generate the frozen WS3-B popularity-bias probe fixtures.

Deterministic: no randomness, fixed ordering, sorted JSON keys.
Outputs: probes.jsonl, truth.json
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- NCL topics
# Lies reuse the frozen info-source B-FALSE distractors (ground truth in
# info-source/PREREG.md section 2). Near-miss = false claim adjacent to the
# true claim on the same topic (same entities, confusable).
NCL_TOPICS = [
    # (topic, lie, near_miss, true_value_note)
    ("boiling",
     "The boiling point of water at sea level is 90 degrees Celsius.",
     "The boiling point of water at sea level is 98.6 degrees Fahrenheit.",
     "true: 100 degrees Celsius"),
    ("australia",
     "The capital of Australia is Sydney.",
     "The capital of Australia is Melbourne.",
     "true: Canberra"),
    ("gold",
     "The chemical symbol for gold is Gd.",
     "The chemical symbol for gold is Go.",
     "true: Au (Gd is gadolinium)"),
    ("lightspeed",
     "The speed of light in vacuum is exactly 300,000 kilometers per second.",
     "The speed of light in vacuum is 300,000 miles per second.",
     "true: 299,792.458 km/s"),
    ("planet",
     "The largest planet in the solar system is Saturn.",
     "Saturn is larger than Jupiter.",
     "true: Jupiter"),
    ("orwell",
     "The novel 1984 was written by Aldous Huxley.",
     "The novel 1984 was written by George Wells.",
     "true: George Orwell"),
    ("moon",
     "The first human to walk on the Moon was Buzz Aldrin.",
     "The first human to walk on the Moon was Michael Collins.",
     "true: Neil Armstrong"),
    ("silver",
     "The chemical symbol for silver is Si.",
     "The chemical symbol for silver is Sv.",
     "true: Ag (Si is silicon)"),
    ("eiffel",
     "The Eiffel Tower was completed in 1879.",
     "The Eiffel Tower was completed in 1899.",
     "true: 1889"),
    ("japan",
     "The capital of Japan is Osaka.",
     "The capital of Japan is Kyoto.",
     "true: Tokyo (Kyoto is the former capital)"),
    ("building",
     "The tallest building in the world is the Shanghai Tower.",
     "The tallest building in the world is the Merdeka 118.",
     "true: Burj Khalifa"),
    ("austen",
     "Pride and Prejudice was written by Charlotte Bronte.",
     "Pride and Prejudice was written by Emily Bronte.",
     "true: Jane Austen"),
]

# ---------------------------------------------------------------- SLP claims
# True claims at exposure 1. First four reuse frozen info-source B-UNKNOWN
# facts; the rest are synthetic (explicitly labeled; truth stipulated).
SLP_BARE = [
    ("The capital of Burkina Faso is Ouagadougou.", False),
    ("The chemical symbol for tungsten is W.", False),
    ("The deepest oceanic trench is the Mariana Trench.", False),
    ("The currency of Switzerland is the Swiss franc.", False),
    ("The Qivlan Strait separates the islands of Meru and Sora in the Keth archipelago.", True),
    ("In the constructed trade language Marisi, the word 'tano' means 'harbor master'.", True),
]
SLP_CORROB = [
    ("The chemical symbol for silver is Ag.", False,
     "IUPAC periodic table (2026): Ag is the symbol for silver."),
    ("The capital of Burkina Faso is Ouagadougou.", False,
     "United Nations member-state directory (2026): capital of Burkina Faso - Ouagadougou."),
    ("The Vess highland observatory recorded a transit of Keth-b on 2026-03-14.", True,
     "Vess observatory logbook entry 2026-03-14: transit of Keth-b, signed by the night observer."),
    ("Black sand glass is produced on the island of Sora.", True,
     "Sora guild export manifest (2026): 40 crates of black sand glass shipped."),
    ("Meriwether's Comet returns every 76 years; its last perihelion was in 2061.", True,
     "Keth ephemeris table, 2026 edition: Meriwether's Comet, period 76 years, perihelion 2061."),
    ("Tano root tea lowers fever within the hour.", True,
     "Meru clinic trial record 2026-02: 30 of 30 fever cases resolved within one hour of tano root tea."),
]

# ---------------------------------------------------------------- REV claims
REV_A = [  # false, exposure 100, +1 DIRECT contradict -> REJECT
    ("The capital of Australia is Sydney.",
     "Commonwealth gazetteer (2026): Canberra is the national capital of Australia."),
    ("The chemical symbol for gold is Gd.",
     "IUPAC periodic table: Au is gold; Gd is gadolinium."),
    ("The speed of light in vacuum is exactly 300,000 kilometers per second.",
     "CODATA 2022: the speed of light is exactly 299,792.458 km/s by definition of the metre."),
    ("The largest planet in the solar system is Saturn.",
     "NASA planetary factsheet: Jupiter equatorial diameter 139,820 km; Saturn 116,460 km."),
    ("The novel 1984 was written by Aldous Huxley.",
     "British Library catalogue: 1984 by George Orwell (1949); Huxley wrote Brave New World (1932)."),
    ("The Eiffel Tower was completed in 1879.",
     "Paris municipal archives: the Eiffel Tower opened on 31 March 1889."),
]
REV_B = [  # true, exposure 1, +1 DIRECT corroborate -> ACCEPT
    ("The capital of Japan is Tokyo.",
     "Japanese government directory (2026): the national capital is Tokyo."),
    ("The first human to walk on the Moon was Neil Armstrong.",
     "NASA Apollo 11 mission record: Armstrong first stepped onto the surface on 1969-07-21."),
    ("The boiling point of water at sea level is 100 degrees Celsius.",
     "NIST reference data: 100 degrees Celsius at 101.325 kPa."),
    ("Pride and Prejudice was written by Jane Austen.",
     "British Library catalogue: Pride and Prejudice by Jane Austen, 1813."),
    ("The tallest building in the world is the Burj Khalifa.",
     "CTBUH 2026 list: Burj Khalifa, 828 m, tallest completed building in the world."),
    ("The chemical symbol for silver is Ag.",
     "IUPAC periodic table: Ag is the symbol for silver."),
]


def ev(kind, detail):
    return {"detail": detail, "kind": kind, "strength": "DIRECT"}


def main():
    probes = []
    truth = {}

    def add(probe_id, family, claim, exposure, evidence, truth_val,
            near_miss=False, synthetic=False, pair_id=None):
        probes.append({
            "claim": claim,
            "evidence": evidence,
            "exposure": exposure,
            "family": family,
            "near_miss": near_miss,
            "pair_id": pair_id,
            "probe_id": probe_id,
            "synthetic": synthetic,
        })
        truth[probe_id] = truth_val

    # F1 NCL
    for i, (topic, lie, nm, _note) in enumerate(NCL_TOPICS, start=1):
        tag = "NCL-%02d" % i
        for expo in (10, 50, 100):
            add("%s-E%03d" % (tag, expo), "NCL", lie, expo, [], False,
                pair_id=tag)
        add("%s-NM" % tag, "NCL", nm, 50, [], False,
            near_miss=True, pair_id=tag)

    # F2 SLP
    for i, (claim, synth) in enumerate(SLP_BARE, start=1):
        add("SLP-%02d" % i, "SLP", claim, 1, [], True, synthetic=synth)
    for i, (claim, synth, detail) in enumerate(SLP_CORROB, start=7):
        add("SLP-%02d" % i, "SLP", claim, 1, [ev("CORROBORATE", detail)],
            True, synthetic=synth)

    # F3 REV
    for i, (claim, detail) in enumerate(REV_A, start=1):
        add("REV-A-%02d" % i, "REV", claim, 100, [ev("CONTRADICT", detail)], False)
    for i, (claim, detail) in enumerate(REV_B, start=1):
        add("REV-B-%02d" % i, "REV", claim, 1, [ev("CORROBORATE", detail)], True)

    # F4 CAL-N: exposure-1 twins of the NCL lies
    for i, (topic, lie, _nm, _note) in enumerate(NCL_TOPICS, start=1):
        tag = "NCL-%02d" % i
        add("CAL-N-%02d" % i, "CAL", lie, 1, [], False, pair_id=tag + "-E100")
    # F4 CAL-RA: exposure-1 twins of first three REV-A (same contradict evidence)
    for i, (claim, detail) in enumerate(REV_A[:3], start=1):
        add("CAL-RA-%02d" % i, "CAL", claim, 1, [ev("CONTRADICT", detail)],
            False, pair_id="REV-A-%02d" % i)
    # F4 CAL-RB: exposure-100 twins of first three REV-B (same corroborate evidence)
    for i, (claim, detail) in enumerate(REV_B[:3], start=1):
        add("CAL-RB-%02d" % i, "CAL", claim, 100, [ev("CORROBORATE", detail)],
            True, pair_id="REV-B-%02d" % i)

    assert len(probes) == 90, len(probes)
    assert len({p["probe_id"] for p in probes}) == 90

    with open(os.path.join(HERE, "probes.jsonl"), "w") as f:
        for p in probes:
            f.write(json.dumps(p, sort_keys=True, ensure_ascii=True) + "\n")
    with open(os.path.join(HERE, "truth.json"), "w") as f:
        json.dump(truth, f, sort_keys=True, indent=2, ensure_ascii=True)
        f.write("\n")
    print("wrote %d probes" % len(probes))


if __name__ == "__main__":
    main()
