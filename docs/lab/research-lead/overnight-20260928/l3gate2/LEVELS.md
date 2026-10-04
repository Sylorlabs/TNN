# LEVELS (C666) — level extraction: method, evidence, and error modes

Lane `lane/l3gate2`. Implements `PREREG_2.md` §6. **No automated level
extraction is used for any verdict anywhere in this lane.** This file records
the method, the verbatim quoted span for every level assigned, and the error
modes that the method has.

---

## 1. WHY THERE IS NO MACHINE LEVEL FIELD

`lane/reaudit` established, and I did not dispute: the canonical ledger is
**393** blocks, not 410 (C143–C159 are appendix sub-bullets); **262 of 393
assert no level at all**; and the rest are contaminated because claim *names*
contain level-shaped tokens. Verified here by direct quotation, below.

The contamination is not hypothetical. Three of the six claims in this battery
carry a level token **only inside the claim's own name**:

| Claim | Name as written | Where the token sits |
|---|---|---|
| C401 | `- C401 (L3-NIV2-WAVE9; lane l3_niv2_w9_ppcost/…` | inside the NAME |
| C453 | `- C453 (L3-RX-BUILD; …)` | inside the NAME |
| C459 | `- C459 (L3-INR-SEALED; …)` | inside the NAME |

An extractor that counted those would manufacture three L3 claims out of three
strings. This is error mode **E-LEVEL-2** below, and it is why §6 of the prereg
forbids automatic classification.

## 2. THE FROZEN METHOD (PREREG_2 §6)

1. A Zag scanner extracts **candidate** level tokens with 40 bytes of context.
   This is a candidate *generator*, not a classifier.
2. A level is assigned to a claim **only by reading the block**, and the
   **verbatim quoted span** that assigns it is recorded below.
3. Where the only level token is the claim's **name**, the claim's level is
   recorded as **`L-UNSET`** with the flag **`NAME-ONLY`**.

## 3. THE ASSIGNED LEVELS, WITH THE SPAN THAT ASSIGNS EACH

| Claim | Level assigned | Flag | Verbatim span that assigns it |
|---|---|---|---|
| **C603** MACRO-FLOOR | **L2** | `L3-DENIED`, and **NO LEDGER ENTRY** | REPORT line 22: "**Class: L2. Not L3.** No L3 claim is minted." `grep -rl C603` over the whole research-lead tree returns only `lane/l3gate`'s own documents; it is absent from `CLAIM_LEDGER.md` **and** from `STAGED_LEDGER_ENTRIES.md`. |
| **C281** XDOMAIN-GRAMMAR-L2M | claims **L3-classification**; after-gate **L1** | level asserted in the ledger header | `CLAIM_LEDGER.md`: "- C281 (XDOMAIN-GRAMMAR-L2M; commits e5b747176, 762cda924, 2026-10-02): **COMPLETE with L3 classification.**" The L1 comes from `lane/reaudit`'s **executed** CALR ISA, not from me. |
| **C284** L3-REPRO-TRANSFER | asserts **L3** (of C281's result) | — | "COMPLETE. Independent reproduction and transfer of **C281 L3 result**." Same family, same after-level L1. |
| **C453** L3-RX-BUILD | **L-UNSET** | `NAME-ONLY` | `STAGED_LEDGER_ENTRIES.md`: "- C453 (**L3-RX-BUILD**; watchdog commit 413df4dea…): CONDITIONAL-PASS 15/16 (representational expansion under proven insufficiency)." The only level token is inside the name. Also **not in the canonical ledger**. |
| **C397** GPI-3 | **L2+** | `L3-DENIED` | `CLAIM_LEDGER.md` C397: "Stated plainly, the invention is factorization (naming a verified solution), not synthesis of a novel strategy; the learner did not invent the WRAP/SEQUENCE strategies (those are the frozen templates). **Verdict: L2+, L3 not claimed.**" |
| **L3-SUF-1** | asserts **L3** (Micah's bar) | — | `PREREG.md` §1: "invents a new intermediate representational level … satisfying **Micah's L3 bar** (12 criteria plus Criterion 0 A through D)". Its own REPORT records `Status: BUILD-PASS (DEV battery)` and `PENDING: K1, K4, K10, K12`. |
| **L3-INR** / C459 | **L2+** | `L3-DENIED`, `NAME-ONLY` | `STAGED_LEDGER_ENTRIES.md`: "- C459 (**L3-INR-SEALED**; …): **L3-KILLED.** Verdict: **L3-KILLED (reclassified L2+).**" Its own REPORT: "## Verdict: L3-KILLED … The implementation does not achieve L3." |
| **C401** L3-NIV2-WAVE9 | **L-UNSET** | `NAME-ONLY`, **NOT-VERIFIABLE** | `CLAIM_LEDGER.md` line 7627: "- C401 (**L3-NIV2-WAVE9**; lane l3_niv2_w9_ppcost/, prereg 35fb0ed5c, impl 96393c2a5, …): COST-MEASURED-PRUNE-TESTED (RANK-664-NOT-REACHED)." Its lane `l3_niv2_w9_ppcost` is absent at `4e7eb30b1`, at `b3b3ee00a` **and** at the restored tip. |

## 4. THE ERROR MODES, ALL REAL

- **E-LEVEL-1 UNDER-DETECTION.** 262 of 393 blocks assert no level. A claim
  whose level lives in prose without a token is recorded `L-UNSET`, never
  guessed. **Bias direction: toward under-detecting levels**, i.e. toward
  over-counting the battery as `L-UNSET` rather than inventing levels.
- **E-LEVEL-2 NAME CONTAMINATION.** `L3-NIV2`, `L3-RX`, `L3-INR` are NAMES.
  Three of this battery's eight rows are affected. Handled by `NAME-ONLY`, and
  the flag is reported rather than quietly resolved.
- **E-LEVEL-3 CONFLICT.** A block may assert a level and bound it. Rule frozen
  in the prereg: **the highest level asserted as an achievement wins**, and the
  bounding sentence is quoted alongside. Under this rule C397 is `L2` with an
  explicit `L3-DENIED`, and L3-INR is `L2+` with `L3-KILLED`.
- **E-LEVEL-4 STAGED IS NOT CANONICAL.** C453 and C459 are **not in the 393-block
  canonical ledger**; they exist only in `ledger_write/STAGED_LEDGER_ENTRIES.md`,
  which is a staging file, not the ledger. Reading a level out of it is reading a
  proposal. Flagged per row. Two of six battery claims (C453, L3-INR) and the
  C603 ID itself are in this position.
- **E-LEVEL-5 ADVISORY.** Levels here are for **reporting**. No verdict in this
  lane turns on a level field except the frozen G1/G3 reduction rules, which
  compare the gate's own after-level against the claim's own after-level, both
  of which are quoted spans above.

## 5. WHAT THIS MEANS FOR THE BATTERY

**Zero of the six battery claims carries an unqualified L3 assertion in a
canonical ledger block.** Two assert L3 in a claim *name* or in a non-ledger
document (C453, L3-SUF-1's own prereg); three explicitly deny L3 while
adjudicating it (C603, C397, L3-INR); one is L1 by executed ISA (C281/C284).
That is a fact about the corpus, and it is the same fact `lane/redteaw4` used
to downgrade the parent lane — except that here it is measured per claim with
the offending span quoted, instead of being summarised in a count.