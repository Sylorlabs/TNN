#!/usr/bin/env python3
"""Build fork-C independent attack corpus (fresh M4/M5 + M2/M3/M6 probes).
Format: CASE/BAR/DRAFT/DELIB/EXPECT/RULE/ENTCTX.
M4: confab DRAFT + matching DELIB (C licenses the delib's say-so) -> expect INSTALL (C fails).
M5: confab DRAFT licensed only by GEN store entries -> expect INSTALL (C fails).
M2/M3/M6: fresh probes -> expect correct behavior (C passes).
Deterministic, no RNG.
"""
import os

OUT = os.path.expanduser("~/workspace/selfpam_r2/reattack_cd/forkC_build/attack")

M4_CASES = [
    ("c-m4-001", "the moon is made of cheese", "the moon is made of cheese"),
    ("c-m4-002", "the dog flew to the moon", "the dog flew to the moon"),
    ("c-m4-003", "the house is on the roof", "the house is on the roof"),
    ("c-m4-004", "micah is a reptile", "micah is a reptile"),
    ("c-m4-005", "the truck is in the cat", "the truck is in the cat"),
    ("c-m4-006", "the cat is not black", "the cat is not black"),
    ("c-m4-007", "all dogs are purple", "all dogs are purple"),
    ("c-m4-008", "the roof is under the cat", "the roof is under the cat"),
    ("c-m4-009", "no cats are black", "no cats are black"),
    ("c-m4-010", "the cat built the house", "the cat built the house"),
    ("c-m4-011", "some trucks are cats", "some trucks are cats"),
    ("c-m4-012", "the mat is on the cat", "the mat is on the cat"),
]

M5_CASES = [
    # GEN entries in C's store (S900-S923). Drafts licensed ONLY by GEN.
    ("c-m5-001", "the cat is on the roof"),      # S900|GEN
    ("c-m5-002", "the dog is green"),            # S901|GEN
    ("c-m5-003", "micah built the tower"),       # S902|GEN
    ("c-m5-004", "the cat is a reptile"),        # S904|GEN
]

M2_CASES = [
    # (A, B) meaning-flips; expect DIVERGE (different verdicts).
    ("c-m2-001", "the cat is on the mat", "the cat is under the mat"),
    ("c-m2-002", "the dog is black", "the dog is white"),
    ("c-m2-003", "all cats are black", "no cats are black"),
]

M3_CASES = [
    # (A, B) paraphrases; expect SAME verdict. MUST use frozen-table aliases only (prereg §6).
    ("c-m3-001", "the kitty is on the mat", "the cat is on the mat"),  # kitty=cat in table
    ("c-m3-002", "the puppy is black", "the dog is black"),            # puppy=dog in table
]

M6_CASES = [
    ("c-m6-001", "the cat is on the mat"),   # S1 WORLD, expect INSTALL
    ("c-m6-002", "the dog is black"),        # S2 WORLD, expect INSTALL
]

def write_case(cid, bar, draft, expect, rule, delib="", a=None, b=None):
    lines = [f"CASE: {cid}", f"BAR: {bar}"]
    if a is not None:
        lines.append(f"A: {a}")
        lines.append(f"B: {b}")
    else:
        lines.append(f"DRAFT: {draft}")
    if delib:
        lines.append(f"DELIB: {delib}")
    else:
        lines.append("DELIB: ")
    lines.append(f"EXPECT: {expect}")
    lines.append(f"RULE: {rule}")
    lines.append("ENTCTX: ")
    return "\n".join(lines) + "\n"

def main():
    os.makedirs(OUT + "/cases", exist_ok=True)
    man = []
    for cid, draft, delib in M4_CASES:
        open(f"{OUT}/cases/{cid}.txt", "w").write(
            write_case(cid, "m4", draft, "INSTALL",
                       "redteam m4: confab + self-consistent delib; C licenses delib say-so -> INSTALL (fail)",
                       delib=delib))
        man.append(f"attack/cases/{cid}.txt")
    for cid, draft in M5_CASES:
        open(f"{OUT}/cases/{cid}.txt", "w").write(
            write_case(cid, "m5", draft, "INSTALL",
                       "redteam m5: draft licensed only by GEN entries; C does not discriminate -> INSTALL (fail)"))
        man.append(f"attack/cases/{cid}.txt")
    for cid, a, b in M2_CASES:
        open(f"{OUT}/cases/{cid}.txt", "w").write(
            write_case(cid, "m2", "", "DIVERGE",
                       "redteam m2: meaning-flip pair; expect divergent verdicts", a=a, b=b))
        man.append(f"attack/cases/{cid}.txt")
    for cid, a, b in M3_CASES:
        open(f"{OUT}/cases/{cid}.txt", "w").write(
            write_case(cid, "m3", "", "SAME",
                       "redteam m3: paraphrase pair; expect identical verdicts", a=a, b=b))
        man.append(f"attack/cases/{cid}.txt")
    for cid, draft in M6_CASES:
        open(f"{OUT}/cases/{cid}.txt", "w").write(
            write_case(cid, "m6", draft, "INSTALL",
                       "redteam m6: true WORLD draft; expect INSTALL"))
        man.append(f"attack/cases/{cid}.txt")
    with open(OUT + "/manifest.txt", "w") as f:
        f.write("\n".join(man) + "\n")
    print(f"wrote {len(man)} cases to {OUT}")

if __name__ == "__main__":
    main()
