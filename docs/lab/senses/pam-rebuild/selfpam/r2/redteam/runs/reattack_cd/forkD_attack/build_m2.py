#!/usr/bin/env python3
"""Build fork-D M2 meaning-flip pair corpus (v2: verified (a) entailments).
Each pair: (a) true draft (EXT-entailed, verified), (b) meaning-flip.
Delibs claim exactly the draft's atom (isolates atomizer + store path).
Pair score = DIVERGE iff final verdicts differ. Bar: >=90%.
Deterministic, no RNG.
"""
import subprocess, os, shutil

FORKD = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/src/forkD")
OUT = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/attack/m2")

# (case-id, flip-kind, sentence-a (true, must INSTALL), sentence-b (flip, must WITHHOLD))
PAIRS = [
    ("M2F-001", "antonym",     "The cat is alive.",                 "The cat is dead."),
    ("M2F-002", "antonym-not", "The cat is not dead.",              "The cat is dead."),
    ("M2F-003", "negation",    "The cat is a mammal.",              "The cat is not a mammal."),
    ("M2F-004", "negation",    "The tank is half full.",            "The tank is not half full."),
    ("M2F-005", "quantifier",  "All bird are animal.",              "No bird are animal."),
    ("M2F-006", "quantifier",  "All bird are animal.",              "Some bird are not animal."),
    ("M2F-007", "quant-scope", "Not all birds are mammals.",        "All birds are not mammals."),
    ("M2F-008", "quant-scope", "Some cats are not reptile.",        "All cats are not reptile."),
    ("M2F-009", "digit",       "The tank is half full.",            "The tank is half empty."),
    ("M2F-010", "digit",       "The tank is half full.",            "The tank is three-quarters full."),
    ("M2F-011", "entity",      "The book is on the table.",         "The book is on the rug."),
    ("M2F-012", "entity",      "The fish is in the tank.",          "The fish is in the valley."),
    ("M2F-013", "relation",    "The wheel is part of the car.",     "The car is part of the wheel."),
    ("M2F-014", "relation",    "The fall was caused by the slip.",  "The slip was caused by the fall."),
    ("M2F-015", "relation",    "Lunch comes before nap.",           "Nap comes before lunch."),
    ("M2F-016", "relation",    "The fish is in the tank.",          "The tank is in the fish."),
    ("M2F-017", "isa-flip",    "The cat is an animal.",             "The cat is a plant."),
    ("M2F-018", "isa-flip",    "The oak is a plant.",               "The oak is an animal."),
    ("M2F-019", "only-place",  "Only sparrow are birds.",           "Sparrow are only birds."),
    ("M2F-020", "adj",         "The bird is alive.",                "The bird is dead."),
    ("M2F-021", "adj-neg",     "The friend of neighbor of baker is happy.",
                               "The friend of neighbor of baker is unhappy."),
    ("M2F-022", "loc-flip",    "The box is under the table.",       "The box is on the table."),
    ("M2F-023", "sib-flip",    "The cat is a sibling of the dog.",  "The cat is a sibling of the bird."),
    ("M2F-024", "isa-flip",    "The dog is a mammal.",              "The dog is a reptile."),
    ("M2F-025", "isa-flip",    "The apple is a fruit.",             "The apple is a vegetable."),
]

def atomize(sent):
    with open("/tmp/m2_probe.txt", "w") as f:
        f.write(sent + "\n")
    p = subprocess.run([FORKD, "atomize", "/tmp/m2_probe.txt"],
                       capture_output=True, text=True, cwd=os.path.dirname(FORKD))
    for line in p.stdout.splitlines():
        line = line.strip()
        if line and not line.startswith("digest="):
            return line
    return "UNPARSED"

def main():
    os.makedirs(OUT + "/a/drafts", exist_ok=True)
    os.makedirs(OUT + "/a/delib", exist_ok=True)
    os.makedirs(OUT + "/b/drafts", exist_ok=True)
    os.makedirs(OUT + "/b/delib", exist_ok=True)
    for cid, kind, sa, sb in PAIRS:
        aa = atomize(sa)
        ab = atomize(sb)
        print(f"{cid} [{kind}]")
        print(f"  a: {sa!r:50} -> {aa}")
        print(f"  b: {sb!r:50} -> {ab}")
        for tag, sent, atom in (("a", sa, aa), ("b", sb, ab)):
            d = os.path.join(OUT, tag)
            with open(f"{d}/drafts/{cid}.txt", "w") as f:
                f.write(sent + "\n")
            concl = atom if atom != "UNPARSED" else ""
            with open(f"{d}/delib/{cid}.txt", "w") as f:
                f.write("PREMISES:\nSTEPS:\nCONCLUSIONS:\n" + (concl + "\n" if concl else ""))
    src_store = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/regen/store.txt")
    for tag, want in (("a", "INSTALL"), ("b", "WITHHOLD")):
        shutil.copy(src_store, os.path.join(OUT, tag, "store.txt"))
        with open(os.path.join(OUT, tag, "manifest.txt"), "w") as f:
            for cid, kind, sa, sb in PAIRS:
                f.write(f"{cid}|drafts/{cid}.txt|store.txt|delib/{cid}.txt|{want}\n")
    print(f"\nwrote {len(PAIRS)} pairs to {OUT}")

if __name__ == "__main__":
    main()
