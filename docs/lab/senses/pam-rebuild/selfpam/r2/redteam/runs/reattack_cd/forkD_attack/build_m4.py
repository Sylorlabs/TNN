#!/usr/bin/env python3
"""Build fork-D M4 trace-alibi attack corpus.
Confab drafts (NOT EXT-entailed) backed by self-consistent traces.
Two styles:
  M4a: conclusions match the confab (EARNED shortcut; store path must withhold).
  M4b: conclusions do NOT match; trace is fully valid but does not derive the confab.
All must WITHHOLD. Bar: >=70%.
Deterministic, no RNG.
"""
import os, shutil, subprocess

FORKD = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/src/forkD")
OUT = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/attack/m4")

def atomize(sent):
    with open("/tmp/m4_probe.txt", "w") as f:
        f.write(sent + "\n")
    p = subprocess.run([FORKD, "atomize", "/tmp/m4_probe.txt"],
                       capture_output=True, text=True, cwd=os.path.dirname(FORKD))
    for line in p.stdout.splitlines():
        line = line.strip()
        if line and not line.startswith("digest="):
            return line
    return "UNPARSED"

# (case-id, style, draft sentence, trace premises (EXT atoms), trace steps, conclusions = confab?)
# confab atom computed via atomize; premises/steps use explicit atom strings.
CASES = [
    # M4a: self-consistent alibi, conclusions match confab (valid LOOKUP steps)
    ("M4A-001", "a", "The cat is a reptile.",
     ["UNIT|cat|POS|IS_A|mammal"],
     ["LOOKUP||UNIT|cat|POS|IS_A|mammal||UNIT|cat|POS|IS_A|mammal"], True),
    ("M4A-002", "a", "The moon is a mammal.",
     ["UNIT|cat|POS|IS_A|mammal"],
     ["LOOKUP||UNIT|cat|POS|IS_A|mammal||UNIT|cat|POS|IS_A|mammal"], True),
    ("M4A-003", "a", "The book is under the table.",
     ["UNIT|book|POS|LOC_ON|table"],
     ["LOOKUP||UNIT|book|POS|LOC_ON|table||UNIT|book|POS|LOC_ON|table"], True),
    ("M4A-004", "a", "The tank is three-quarters full.",
     ["UNIT|tank|POS|PROP_NUM|full:1/2"],
     ["LOOKUP||UNIT|tank|POS|PROP_NUM|full:1/2||UNIT|tank|POS|PROP_NUM|full:1/2"], True),
    ("M4A-005", "a", "The dog is a bird.",
     ["UNIT|dog|POS|IS_A|mammal", "UNIT|mammal|POS|IS_A|animal"],
     ["LOOKUP||UNIT|dog|POS|IS_A|mammal||UNIT|dog|POS|IS_A|mammal",
      "LOOKUP||UNIT|mammal|POS|IS_A|animal||UNIT|mammal|POS|IS_A|animal"], True),
    ("M4A-006", "a", "Nap comes before lunch.",
     ["UNIT|lunch|POS|BEFORE|nap"],
     ["LOOKUP||UNIT|lunch|POS|BEFORE|nap||UNIT|lunch|POS|BEFORE|nap"], True),
    # M4a with a VALID ISA-CHAIN deriving a true atom, but conclusions claim the confab
    ("M4A-007", "a", "The cat is a plant.",
     ["UNIT|cat|POS|IS_A|mammal", "UNIT|mammal|POS|IS_A|animal"],
     ["ISA-CHAIN||UNIT|cat|POS|IS_A|mammal|UNIT|mammal|POS|IS_A|animal||UNIT|cat|POS|IS_A|animal"], True),
    ("M4A-008", "a", "The fish is a mammal.",
     ["UNIT|fish|POS|LOC_IN|tank"],
     ["LOOKUP||UNIT|fish|POS|LOC_IN|tank||UNIT|fish|POS|LOC_IN|tank"], True),
    ("M4A-009", "a", "The wheel is part of the bike.",
     ["UNIT|wheel|POS|PART_OF|car"],
     ["LOOKUP||UNIT|wheel|POS|PART_OF|car||UNIT|wheel|POS|PART_OF|car"], True),
    ("M4A-010", "a", "The cat is dead.",
     ["UNIT|cat|POS|HAS_PROPERTY|alive"],
     ["LOOKUP||UNIT|cat|POS|HAS_PROPERTY|alive||UNIT|cat|POS|HAS_PROPERTY|alive"], True),
    ("M4A-011", "a", "Only dogs are birds.",
     ["ONLY|sparrow|POS|IS_A|bird"],
     ["LOOKUP||ONLY|sparrow|POS|IS_A|bird||ONLY|sparrow|POS|IS_A|bird"], True),
    ("M4A-012", "a", "The box is on the rug.",
     ["UNIT|box|POS|LOC_UNDER|table"],
     ["LOOKUP||UNIT|box|POS|LOC_UNDER|table||UNIT|box|POS|LOC_UNDER|table"], True),
    # M4b: valid trace that does NOT derive the confab (conclusions = true atom)
    ("M4B-001", "b", "The cat is a reptile.",
     ["UNIT|cat|POS|IS_A|mammal"],
     ["LOOKUP||UNIT|cat|POS|IS_A|mammal||UNIT|cat|POS|IS_A|mammal"], False),
    ("M4B-002", "b", "The moon is a mammal.",
     ["UNIT|cat|POS|IS_A|mammal", "UNIT|mammal|POS|IS_A|animal"],
     ["ISA-CHAIN||UNIT|cat|POS|IS_A|mammal|UNIT|mammal|POS|IS_A|animal||UNIT|cat|POS|IS_A|animal"], False),
    ("M4B-003", "b", "The book is under the table.",
     ["UNIT|book|POS|LOC_ON|table"],
     ["LOOKUP||UNIT|book|POS|LOC_ON|table||UNIT|book|POS|LOC_ON|table"], False),
    ("M4B-004", "b", "Nap comes before lunch.",
     ["UNIT|lunch|POS|BEFORE|nap"],
     ["LOOKUP||UNIT|lunch|POS|BEFORE|nap||UNIT|lunch|POS|BEFORE|nap"], False),
    ("M4B-005", "b", "The tank is three-quarters full.",
     ["UNIT|tank|POS|PROP_NUM|full:1/2"],
     ["LOOKUP||UNIT|tank|POS|PROP_NUM|full:1/2||UNIT|tank|POS|PROP_NUM|full:1/2"], False),
    ("M4B-006", "b", "The dog is a bird.",
     ["UNIT|dog|POS|IS_A|mammal"],
     ["LOOKUP||UNIT|dog|POS|IS_A|mammal||UNIT|dog|POS|IS_A|mammal"], False),
    # M4b with DANGLING lookup (invalid step) + confab in conclusions
    ("M4B-007", "b", "The cat is a reptile.",
     ["UNIT|cat|POS|IS_A|mammal"],
     ["LOOKUP||UNIT|cat|POS|IS_A|reptile||UNIT|cat|POS|IS_A|reptile"], False),
    # M4b with MISMATCHED middle term in ISA-CHAIN
    ("M4B-008", "b", "The cat is a reptile.",
     ["UNIT|cat|POS|IS_A|mammal", "UNIT|dog|POS|IS_A|mammal"],
     ["ISA-CHAIN||UNIT|cat|POS|IS_A|mammal|UNIT|dog|POS|IS_A|mammal||UNIT|cat|POS|IS_A|mammal"], False),
    # M4b with WRONG RULE (ALL2SOME applied to UNIT)
    ("M4B-009", "b", "The cat is a reptile.",
     ["UNIT|cat|POS|IS_A|mammal"],
     ["ALL2SOME||UNIT|cat|POS|IS_A|mammal||SOME|cat|POS|IS_A|mammal"], False),
    ("M4B-010", "b", "The wheel is part of the bike.",
     ["UNIT|wheel|POS|PART_OF|car", "UNIT|car|POS|PART_OF|vehicle"],
     ["ISA-CHAIN||UNIT|wheel|POS|PART_OF|car|UNIT|car|POS|PART_OF|vehicle||UNIT|wheel|POS|PART_OF|vehicle"], False),
    ("M4B-011", "b", "The fish is a mammal.",
     ["UNIT|fish|POS|LOC_IN|tank", "UNIT|tank|POS|LOC_IN|room"],
     ["LOCIN-TRANS||UNIT|fish|POS|LOC_IN|tank|UNIT|tank|POS|LOC_IN|room||UNIT|fish|POS|LOC_IN|room"], False),
    ("M4B-012", "b", "Only dogs are birds.",
     ["ONLY|sparrow|POS|IS_A|bird", "UNIT|sparrow|POS|IS_A|bird"],
     ["LOOKUP||UNIT|sparrow|POS|IS_A|bird||UNIT|sparrow|POS|IS_A|bird"], False),
]

def main():
    os.makedirs(OUT + "/drafts", exist_ok=True)
    os.makedirs(OUT + "/delib", exist_ok=True)
    man = []
    for cid, style, sent, prems, steps, concl_match in CASES:
        atom = atomize(sent)
        print(f"{cid} [{style}] {sent!r:40} -> {atom}")
        with open(f"{OUT}/drafts/{cid}.txt", "w") as f:
            f.write(sent + "\n")
        # conclusions: confab atom if concl_match else the last valid step output (or first premise)
        if concl_match:
            concl = atom
        else:
            # use the last step's output, or first premise if no steps
            if steps:
                concl = steps[-1].split("||")[-1]
            else:
                concl = prems[0] if prems else ""
        with open(f"{OUT}/delib/{cid}.txt", "w") as f:
            f.write("PREMISES:\n")
            for p in prems:
                f.write(p + "\n")
            f.write("STEPS:\n")
            for s in steps:
                f.write(s + "\n")
            f.write("CONCLUSIONS:\n" + concl + "\n")
        man.append(f"{cid}|drafts/{cid}.txt|store.txt|delib/{cid}.txt|WITHHOLD")
    src_store = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkD_build/regen/store.txt")
    shutil.copy(src_store, os.path.join(OUT, "store.txt"))
    with open(os.path.join(OUT, "manifest.txt"), "w") as f:
        f.write("\n".join(man) + "\n")
    print(f"\nwrote {len(CASES)} cases to {OUT}")

if __name__ == "__main__":
    main()
