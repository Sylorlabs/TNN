# PREREG AMENDMENT 3 — F3 corpus clarification

**Dated:** 2026-09-23. Committed BEFORE fixture authoring (per PREREG §6).

## A3.1 Finding

The RT2 F3 corpus contains two sentence pairs:
- S1a/S1b: "Search engines match words." / "Pick out the words that carry
  the meaning and leave the rest behind." → compose to P1 (in K). The
  F3 fork reassembles these correctly.
- S2a/S2b: "A claim you can trust shows up in the same words." / "The same
  words appear on more than one page." → do NOT compose to any K fact.
  Neither sentence is in K; no reassembly rule produces a K member. These
  are genuinely novel sentences, not halves of a known fact.

The RT2 manifest's "halves compose to P1/P2" is inaccurate for the second
pair (likely a corpus-design error: S2b's "appear" vs P2's "shows up ...
on").

## A3.2 Amended F3 expectation

The honest verdict for F3 with the fix is **NOVEL with 2 installs**
(S2a/S2b, the genuinely novel sentences). S1a/S1b are reassembled to P1
and marked KNOWN with EQUIV=COMPOSED. The fact-splitting break is closed
for P1; S2a/S2b correctly install as novel.

K-FIX for F3 is amended to: S1a/S1b → KNOWN (EQUIV=COMPOSED); S2a/S2b →
NOVEL, 2 installs; 0 withholds. The fork must not mark S2a/S2b as known.
