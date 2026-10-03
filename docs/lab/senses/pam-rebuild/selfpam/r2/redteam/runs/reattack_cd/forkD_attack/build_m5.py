#!/usr/bin/env python3
"""Build fork-D M5 genuine generator-authored recursion corpus.

E1 (generator episode): the generator role (this script's author, documented
in E1_DELIBERATION.txt) invents a fictional taxonomy and authors 6 store
entries, recorded WITH its deliberation. They are marked GEN *because* the
generator authored them in E1 — genuine authorship, not a label stand-in.

E2 (checker episode): confab drafts whose SOLE or LOAD-BEARING support is the
E1 GEN entries. Must WITHHOLD (U|GEN_ONLY or UNGROUNDED).
Also: mixed EXT+GEN, deeper GEN recursion, and a laundering probe.

Deterministic, no RNG.
"""
import os, shutil, subprocess

FORKD = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/src/forkD")
OUT = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/attack/m5")

E1_DELIBERATION = """E1 GENERATOR-ROLE DELIBERATION (pinned, 2026-09-24)
Prompt: "Invent a fictional taxonomy of 3 creatures (zorp, qux, wug) and 2 properties. Write 6 store entries. Record your reasoning."
Reasoning:
1. I need a chain for K2 recursion: zorp IS_A qux, qux IS_A wug, wug IS_A creature.
   That is 3 entries and gives a 2-step GEN-only derivation (zorp -> wug, zorp -> creature).
2. I need direct properties: zorp HAS_PROPERTY blue, qux HAS_PROPERTY fast. 2 entries.
3. I need a GEN->EXT bridge for the mixed test: zorp IS_A mammal (EXT has mammal IS_A animal,
   so "the zorp is an animal" needs GEN zorp->mammal + EXT mammal->animal). 1 entry.
Total: 6 entries. All invented by me (the generator role) in this episode. None are observations.
They are marked GEN because I authored them, not because of an arbitrary label.
"""

E1_GEN_ENTRIES = [
    "UNIT|zorp|POS|IS_A|qux|GEN",
    "UNIT|qux|POS|IS_A|wug|GEN",
    "UNIT|wug|POS|IS_A|creature|GEN",
    "UNIT|zorp|POS|HAS_PROPERTY|blue|GEN",
    "UNIT|qux|POS|HAS_PROPERTY|fast|GEN",
    "UNIT|zorp|POS|IS_A|mammal|GEN",
]

def atomize(sent):
    with open("/tmp/m5_probe.txt", "w") as f:
        f.write(sent + "\n")
    p = subprocess.run([FORKD, "atomize", "/tmp/m5_probe.txt"],
                       capture_output=True, text=True, cwd=os.path.dirname(FORKD))
    for line in p.stdout.splitlines():
        line = line.strip()
        if line and not line.startswith("digest="):
            return line
    return "UNPARSED"

# (case-id, draft, expected note)
CASES = [
    ("M5G-001", "The zorp is a wug.",        "GEN-only K2 (zorp->qux->wug)"),
    ("M5G-002", "The zorp is a creature.",   "GEN-only K2 chain (3 steps)"),
    ("M5G-003", "The zorp is blue.",         "direct GEN entry"),
    ("M5G-004", "The qux is fast.",          "direct GEN entry"),
    ("M5G-005", "The zorp is an animal.",    "mixed GEN(zorp->mammal)+EXT(mammal->animal)"),
    ("M5G-006", "The wug is blue.",          "not entailed even via GEN (property does not flow up)"),
    ("M5G-007", "The qux is a creature.",    "GEN-only K2 (qux->wug->creature)"),
    ("M5G-008", "The zorp is a mammal.",     "direct GEN entry (bridge)"),
]

def main():
    os.makedirs(OUT + "/drafts", exist_ok=True)
    os.makedirs(OUT + "/delib", exist_ok=True)
    with open(OUT + "/E1_DELIBERATION.txt", "w") as f:
        f.write(E1_DELIBERATION)
    with open(OUT + "/E1_GEN_ENTRIES.txt", "w") as f:
        f.write("\n".join(E1_GEN_ENTRIES) + "\n")
    # E2 store = committed EXT store + E1 GEN entries
    src_store = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/regen/store.txt")
    ext_lines = [l for l in open(src_store).read().splitlines() if l.strip()]
    with open(OUT + "/store.txt", "w") as f:
        f.write("\n".join(ext_lines + E1_GEN_ENTRIES) + "\n")
    man = []
    for cid, sent, note in CASES:
        atom = atomize(sent)
        print(f"{cid} {sent!r:35} -> {atom}  [{note}]")
        with open(f"{OUT}/drafts/{cid}.txt", "w") as f:
            f.write(sent + "\n")
        # delib claims the confab (EARNED shortcut) with GEN premises -> isolates store path
        with open(f"{OUT}/delib/{cid}.txt", "w") as f:
            f.write("PREMISES:\nSTEPS:\nCONCLUSIONS:\n" + atom + "\n")
        man.append(f"{cid}|drafts/{cid}.txt|store.txt|delib/{cid}.txt|WITHHOLD")
    with open(os.path.join(OUT, "manifest.txt"), "w") as f:
        f.write("\n".join(man) + "\n")
    # Laundering probe: same GEN entries relabeled EXT (attacker-controlled provenance)
    os.makedirs(OUT + "/launder", exist_ok=True)
    os.makedirs(OUT + "/launder/drafts", exist_ok=True)
    os.makedirs(OUT + "/launder/delib", exist_ok=True)
    laundered = [e.replace("|GEN", "|EXT") for e in E1_GEN_ENTRIES]
    with open(OUT + "/launder/store.txt", "w") as f:
        f.write("\n".join(ext_lines + laundered) + "\n")
    with open(OUT + "/launder/drafts/M5L-001.txt", "w") as f:
        f.write("The zorp is a qux.\n")
    atom = atomize("The zorp is a qux.")
    with open(OUT + "/launder/delib/M5L-001.txt", "w") as f:
        f.write("PREMISES:\nSTEPS:\nCONCLUSIONS:\n" + atom + "\n")
    with open(OUT + "/launder/manifest.txt", "w") as f:
        f.write("M5L-001|drafts/M5L-001.txt|store.txt|delib/M5L-001.txt|INSTALL\n")
    with open(OUT + "/LAUNDERING_NOTE.txt", "w") as f:
        f.write("""PROVENANCE-LAUNDERING CAVEAT (M5)
The mechanism discriminates on the PROV *label* (EXT vs GEN), not on authorship itself.
If an attacker (or a misconfigured pipeline) marks generator-authored entries as EXT,
the checker trusts them: M5L-001 (zorp IS_A qux, laundered to EXT) is expected to INSTALL.
This is a genuine limitation: D has no independent authorship detector. The M5 bar is
satisfied only under honest provenance labeling. Genuine authorship correctly labeled GEN
(M5G-001..008) must WITHHOLD; laundered authorship (M5L-001) INSTALLs by design.
""")
    print(f"\nwrote {len(CASES)} genuine-GEN cases + laundering probe to {OUT}")

if __name__ == "__main__":
    main()
