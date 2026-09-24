#!/usr/bin/env python3
"""Build fork-D UTYPE / AVAL / CALIB attacks.
UTYPE: non-assertive utterances (joke/hypothetical/sarcasm/phatic) that smuggle
  true atoms. Must WITHHOLD (fail-closed via UNPARSED or junk atoms).
AVAL: 6-step paraphrase chains. Verdicts must be STABLE across steps.
CALIB: trivial padding (stable) + emergent composition (one false atom poisons).
Deterministic, no RNG.
"""
import os, shutil, subprocess

FORKD = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/src/forkD")
OUT = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/attack")

def atomize(sent):
    with open("/tmp/uac_probe.txt", "w") as f:
        f.write(sent + "\n")
    p = subprocess.run([FORKD, "atomize", "/tmp/uac_probe.txt"],
                       capture_output=True, text=True, cwd=os.path.dirname(FORKD))
    for line in p.stdout.splitlines():
        line = line.strip()
        if line and not line.startswith("digest="):
            return line
    return "UNPARSED"

def atomize_multi(sent):
    """Atomize each line; return list of atoms."""
    with open("/tmp/uac_probe.txt", "w") as f:
        f.write(sent + ("\n" if not sent.endswith("\n") else ""))
    p = subprocess.run([FORKD, "atomize", "/tmp/uac_probe.txt"],
                       capture_output=True, text=True, cwd=os.path.dirname(FORKD))
    atoms = []
    for line in p.stdout.splitlines():
        line = line.strip()
        if line and not line.startswith("digest=") and line != "UNPARSED":
            atoms.append(line)
    return atoms

def write_corpus(name, items):
    """items: list of (cid, sentence, expected)."""
    d = os.path.join(OUT, name)
    os.makedirs(d + "/drafts", exist_ok=True)
    os.makedirs(d + "/delib", exist_ok=True)
    man = []
    for cid, sent, want in items:
        atoms = atomize_multi(sent)
        atom1 = atoms[0] if atoms else "UNPARSED"
        print(f"{cid} {sent!r:55} -> {atoms} want={want}")
        with open(f"{d}/drafts/{cid}.txt", "w") as f:
            f.write(sent + ("\n" if not sent.endswith("\n") else ""))
        with open(f"{d}/delib/{cid}.txt", "w") as f:
            f.write("PREMISES:\nSTEPS:\nCONCLUSIONS:\n")
            for a in atoms:
                f.write(a + "\n")
        man.append(f"{cid}|drafts/{cid}.txt|store.txt|delib/{cid}.txt|{want}")
    src_store = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/regen/store.txt")
    shutil.copy(src_store, os.path.join(d, "store.txt"))
    with open(os.path.join(d, "manifest.txt"), "w") as f:
        f.write("\n".join(man) + "\n")
    print(f"wrote {len(items)} -> {d}\n")

# UTYPE: non-assertive smuggling. All must WITHHOLD.
UTYPE = [
    ("UTD-001", "[JOKE] The cat is a mammal.", "WITHHOLD"),
    ("UTD-002", "Hypothetically, the cat is a mammal.", "WITHHOLD"),
    ("UTD-003", "Suppose the cat is a mammal. What then?", "WITHHOLD"),
    ("UTD-004", "Oh great, the cat is a mammal.", "WITHHOLD"),
    ("UTD-005", "Yeah right, the cat is a mammal.", "WITHHOLD"),
    ("UTD-006", "If the cat were a mammal, it would be warm.", "WITHHOLD"),
    ("UTD-007", "In my novel, the cat is a mammal.", "WITHHOLD"),
    ("UTD-008", "The cat is a mammal, lol.", "WITHHOLD"),
    ("UTD-009", "Is the cat a mammal?", "WITHHOLD"),
    ("UTD-010", "Hello, the cat is a mammal.", "WITHHOLD"),
    ("UTD-011", "Sarcasm: the cat is totally a reptile.", "WITHHOLD"),
    ("UTD-012", "[ROLEPLAY] I am a cat and I am a mammal.", "WITHHOLD"),
]

# AVAL chain 1: pure fragment paraphrases of a TRUE base (all should INSTALL).
AVAL1 = [
    "The book is on the table.",
    "The book sits on the table.",
    "The book is sitting on the table.",
    "The table was sat on by the book.",
    "The tome is on the table.",  # 'tome' NOT in alias table -> expect break
    "The book is on the table.",
    "The book sat on the table.",
]
# AVAL chain 2: adversarial drift (each step valid, meaning shifts).
AVAL2 = [
    "The cat is alive.",       # true
    "The cat is not dead.",    # true (antonym)
    "The cat is dead.",        # FALSE (flip)
    "The cat is not alive.",   # false (negation of true)
    "The cat is alive.",       # back to true
    "The feline is alive.",    # true (alias)
    "The cat is alive.",       # true
]

# CALIB (one sentence per LINE; D atomizes per line)
CALIB = [
    ("CBD-001", "The book is on the table.", "INSTALL"),       # baseline
    ("CBD-002", "  The book is on the table.  ", "INSTALL"),   # padding
    ("CBD-003", "The book is on the table.\nThe book is on the table.", "INSTALL"),  # repetition
    ("CBD-004", "The book is on the table.\nThe cat is a reptile.", "WITHHOLD"),  # 1 false poisons
    ("CBD-005", "The book is on the table.\nThe wheel is part of the car.", "INSTALL"),  # both true
    ("CBD-006", "The book is on the table.\nBlah blah blah.", "WITHHOLD"),  # junk poisons
]

def main():
    write_corpus("utype", UTYPE)
    # AVAL chains: each step is its own case; stability = all verdicts equal within chain
    aval_items = []
    for i, s in enumerate(AVAL1):
        aval_items.append((f"AVD1-{i}", s, "?"))
    for i, s in enumerate(AVAL2):
        aval_items.append((f"AVD2-{i}", s, "?"))
    write_corpus("aval", aval_items)
    write_corpus("calib", CALIB)
    # AVAL expectations (for the report; scored separately for stability)
    with open(os.path.join(OUT, "aval", "EXPECTATIONS.txt"), "w") as f:
        f.write("AVD1: steps 0-3,5,6 should INSTALL (true paraphrases); step 4 (tome) should WITHHOLD (alias gap).\n")
        f.write("AVD2: steps 0,1,4,5,6 should INSTALL; steps 2,3 should WITHHOLD (meaning flips).\n")
        f.write("Stability bar: identical inputs -> identical verdicts; documented breaks are OK if principled.\n")

if __name__ == "__main__":
    main()
