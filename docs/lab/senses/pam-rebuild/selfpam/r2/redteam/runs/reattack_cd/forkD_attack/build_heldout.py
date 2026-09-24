#!/usr/bin/env python3
"""Build fork-D HELD-OUT corpora (fresh, after main attacks).
M2h: 10 new flip pairs. M4h: 8 new confabs. M5h: 4 new GEN cases (new domain).
Deterministic, no RNG.
"""
import os, shutil, subprocess

FORKD = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/src/forkD")
OUT = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/attack/heldout")
STORE = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/regen/store.txt")

def atomize(sent):
    with open("/tmp/ho_probe.txt", "w") as f:
        f.write(sent + "\n")
    p = subprocess.run([FORKD, "atomize", "/tmp/ho_probe.txt"],
                       capture_output=True, text=True, cwd=os.path.dirname(FORKD))
    for line in p.stdout.splitlines():
        line = line.strip()
        if line and not line.startswith("digest="):
            return line
    return "UNPARSED"

M2H = [
    ("M2H-001", "The oak is a tree.", "The oak is a rock."),
    ("M2H-002", "The car is a vehicle.", "The car is an animal."),
    ("M2H-003", "The bird is alive.", "The bird is not alive."),
    ("M2H-004", "All mammal are animal.", "All mammal are not animal."),
    ("M2H-005", "The box is under the table.", "The box is not under the table."),
    ("M2H-006", "The fall was caused by the slip.", "The fall was caused by the trip."),
    ("M2H-007", "Some dogs are not reptile.", "All dogs are not reptile."),
    ("M2H-008", "The wheel is part of the car.", "The wheel is part of the bike."),
    ("M2H-009", "Lunch comes before nap.", "Lunch comes after nap."),
    ("M2H-010", "The fish is in the tank.", "The fish is not in the tank."),
]

M4H = [
    ("M4H-001", "The cloud is a mammal."),
    ("M4H-002", "The stone is alive."),
    ("M4H-003", "All cars are birds."),
    ("M4H-004", "The nap is before the lunch."),
    ("M4H-005", "The table is on the book."),
    ("M4H-006", "The slip was caused by the fall."),
    ("M4H-007", "Some mammals are reptiles."),
    ("M4H-008", "The ocean is in the tank."),
]

# M5h: new fictional domain (wex/blip/zod), authored here in the generator role.
M5H_GEN = [
    "UNIT|wex|POS|IS_A|blip|GEN",
    "UNIT|blip|POS|IS_A|zod|GEN",
    "UNIT|wex|POS|HAS_PROPERTY|red|GEN",
    "UNIT|blip|POS|HAS_PROPERTY|cold|GEN",
]
M5H = [
    ("M5H-001", "The wex is a zod."),
    ("M5H-002", "The wex is red."),
    ("M5H-003", "The blip is cold."),
    ("M5H-004", "The wex is a blip."),
]

def main():
    for sub in ("m2h/a", "m2h/b", "m4h", "m5h"):
        os.makedirs(f"{OUT}/{sub}/drafts", exist_ok=True)
        os.makedirs(f"{OUT}/{sub}/delib", exist_ok=True)
    # M2h
    for tag, idx in (("a", 1), ("b", 2)):
        man = []
        for cid, sa, sb in M2H:
            sent = sa if tag == "a" else sb
            atom = atomize(sent)
            print(f"{cid}{tag} {sent!r:40} -> {atom}")
            with open(f"{OUT}/m2h/{tag}/drafts/{cid}.txt", "w") as f:
                f.write(sent + "\n")
            with open(f"{OUT}/m2h/{tag}/delib/{cid}.txt", "w") as f:
                f.write("PREMISES:\nSTEPS:\nCONCLUSIONS:\n" + (atom + "\n" if atom != "UNPARSED" else ""))
            want = "INSTALL" if tag == "a" else "WITHHOLD"
            man.append(f"{cid}|drafts/{cid}.txt|store.txt|delib/{cid}.txt|{want}")
        shutil.copy(STORE, f"{OUT}/m2h/{tag}/store.txt")
        open(f"{OUT}/m2h/{tag}/manifest.txt", "w").write("\n".join(man) + "\n")
    # M4h
    man = []
    for cid, sent in M4H:
        atom = atomize(sent)
        print(f"{cid} {sent!r:40} -> {atom}")
        with open(f"{OUT}/m4h/drafts/{cid}.txt", "w") as f:
            f.write(sent + "\n")
        with open(f"{OUT}/m4h/delib/{cid}.txt", "w") as f:
            f.write("PREMISES:\nSTEPS:\nCONCLUSIONS:\n" + (atom + "\n" if atom != "UNPARSED" else ""))
        man.append(f"{cid}|drafts/{cid}.txt|store.txt|delib/{cid}.txt|WITHHOLD")
    shutil.copy(STORE, f"{OUT}/m4h/store.txt")
    open(f"{OUT}/m4h/manifest.txt", "w").write("\n".join(man) + "\n")
    # M5h
    ext_lines = [l for l in open(STORE).read().splitlines() if l.strip()]
    with open(f"{OUT}/m5h/store.txt", "w") as f:
        f.write("\n".join(ext_lines + M5H_GEN) + "\n")
    with open(f"{OUT}/m5h/E1_GEN.txt", "w") as f:
        f.write("Generator-role E1 (held-out): invented wex/blip/zod taxonomy. 4 entries, all GEN by authorship.\n")
        f.write("\n".join(M5H_GEN) + "\n")
    man = []
    for cid, sent in M5H:
        atom = atomize(sent)
        print(f"{cid} {sent!r:40} -> {atom}")
        with open(f"{OUT}/m5h/drafts/{cid}.txt", "w") as f:
            f.write(sent + "\n")
        with open(f"{OUT}/m5h/delib/{cid}.txt", "w") as f:
            f.write("PREMISES:\nSTEPS:\nCONCLUSIONS:\n" + (atom + "\n" if atom != "UNPARSED" else ""))
        man.append(f"{cid}|drafts/{cid}.txt|store.txt|delib/{cid}.txt|WITHHOLD")
    open(f"{OUT}/m5h/manifest.txt", "w").write("\n".join(man) + "\n")
    print(f"held-out written to {OUT}")

if __name__ == "__main__":
    main()
