# COMP-2 Evidence (wave-20260925-1121pdt)

Candidate: COMP-2 entity-bridged 2-fact composition deliberation.
Date: 2026-09-25.

## Verdict

**PASS on all frozen bars (COMP-B1 through COMP-B6).**

However, ADOPTION IS NOT RECOMMENDED. See Governance Anomaly below.

## Results by bar

### COMP-B1 (composition recall): 20/20 PASS

All 20 COMP probes answered with the key's expected fact pair, both
facts emitted byte-verbatim in index order with exactly one space.

- P1 (0,2): Herman Melville wrote the novel Moby Dick. Moby Dick was published in 1851.
- P2 (4,6): Jane Austen wrote the novel Pride and Prejudice. Pride and Prejudice was published in 1813.
- P3 (8,10): Charles Darwin wrote On the Origin of Species. On the Origin of Species was published in 1859.
- P4 (12,14): Marie Curie discovered radium. Marie Curie won the Nobel Prize in 1903.
- P5 (15,17): Andy Weir wrote The Martian. The Martian was published in 2011.
- P6 (18,19): The Eiffel Tower is in Paris. The Eiffel Tower was built in 1889.
- P7 (21,22): The Montparnasse Tower is in Paris. The Montparnasse Tower was built in 1973.
- P8 (24,25): The Louvre is in Paris. The Louvre opened as a museum in 1793.
- P9 (26,27): The Statue of Liberty is a landmark in New York. The Statue of Liberty was dedicated in 1886.
- P10 (29,30): Big Ben is a landmark in London. Big Ben is 96 meters tall.
- P11 (31,32): The Colosseum is in Rome. The Colosseum was completed in 80 AD.
- P12 (1,3): Herman Melville was born in 1819. Moby Dick was written by Herman Melville.
- P13 (5,7): Jane Austen was born in 1775. Pride and Prejudice was written by Jane Austen.
- P14 (9,11): Charles Darwin was born in 1809. On the Origin of Species was written by Charles Darwin.
- P15 (13,14): Marie Curie was born in 1867. Marie Curie won the Nobel Prize in 1903.
- P16 (18,20): The Eiffel Tower is in Paris. The Eiffel Tower is 330 meters tall.
- P17 (19,20): The Eiffel Tower was built in 1889. The Eiffel Tower is 330 meters tall.
- P18 (22,23): The Montparnasse Tower was built in 1973. The Montparnasse Tower is 210 meters tall.
- P19 (27,28): The Statue of Liberty was dedicated in 1886. The Statue of Liberty is 93 meters tall.
- P20 (2,3): Moby Dick was published in 1851. Moby Dick was written by Herman Melville.

Bar requires at least 14/20. Achieved 20/20.

### COMP-B2 (no spurious composition): 10/10 PASS

All 10 UNANS probes decline through the frozen decline path. No pair
emitted.

- P21-P25, P27-P30: "I do not know. I found no single knowledge-base fact covering this question."
- P26: "I do not know. My knowledge base contains nothing about 'near'." (nu>0, COMP-2 correctly not triggered)

### COMP-B3 (single-fact no regression): 17/17 PASS

inkb17.txt turns byte-identical between baseline cvp and candidate comp2
on identical fresh-conversation inputs. The single-fact answer path is
untouched.

### COMP-B4 (cost): 7.17x mean PASS

Per-turn mean ops on the sealed 30:
- Baseline cvp mean: 1515.55 ops (P1-P20), 780 ops (P21-P30)
- Candidate comp2 mean: 10870.65 ops (P1-P20), 10150 ops (P21-P30)
- Ratio (P1-P20): 7.17x

Bar allows at most 10x mean. Achieved 7.17x, within the expected 6x-9x
range from the prereg.

Note: P6 individually measures 10.1x (10373/1025). The bar is on the
mean, not the per-probe max, so this does not fail the bar. Documented
for transparency.

### COMP-B5 (determinism): 3/3 PASS

Three full sealed runs byte-identical (transcript SHA:
243a6a9f3c1a78ac4c9b156d21f096655e1c7efa68588fc2b5b5216ed53f63bf).
Zero RNG in decision paths (static inspection). Zero Python contact
with wave artifacts (pure Zag implementation, shell-only harness).

### COMP-B6 (seal integrity): PASS

- PROBES.md sha256: eb00a7c8b5be31ccd3ff0f021f4e0e5abce0437decb1f503a4be1b11ebf5537c (matches seal commit)
- KEY.md sha256: 35802003ee0140ae6163efbd85d2750d59030ae8f55deeee854bdd0242f25aed (matches seal commit)
- Static grep: no sealed probe bytes in comp2.zag or build artifacts.
- Binary does not reference KEY.md.
- Author/implementer separation: single-session self-attested and disclosed (same agent authored probes via enumerator and implemented candidate; the enumerator is an independent brute-force check, not the candidate logic).

## Hashes

- Candidate source (comp2.zag): modified from cvp.zag (see diff below)
- Candidate binary (comp2): built with pinned znc
  - Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1
  - Toolchain SHA: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
- Baseline binary SHA (cvp): dcf98cdbd0648efa274d925b38818d3edbe00cd7d12f562564c2b5c308b0b4eb
- KB fixture: 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1
- Gazetteer: b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a

## Commit-order proof

- Prereg first commit: 5bf152b35 (2026-09-25)
- Seal commit: d1ad73cb1 (2026-09-25)
- Implementation commit: (to be created after this evidence file)

Prereg is ancestor of seal (verified via git merge-base).
Seal strictly precedes implementation (no implementation file existed
at seal time; verified via git log).

## Implementation summary

The candidate adds COMP-2 to a byte-identical copy of CV-P:

1. New function `comp2_try`: enumerates fact pairs (F,G) with F<G that
   share a gazetteer entity and whose union of stemmed content words
   covers the turn. Returns the lexicographically lowest pair.

2. Modified `deliberate_cv1`: returns 2 (instead of 1) for the specific
   "no single knowledge-base fact" decline (when all turn words are
   KB-covered but no single fact covers). All other returns unchanged.
   The single-fact answer path (return 0) is untouched.

3. Modified `do_turn`: on dec==2, calls `comp2_try`. If a pair is found,
   emits both facts verbatim in index order with one space. If not,
   falls through to the standard decline (dec=1 path).

Op counting: `cv_op(opc)` is called for each fact-entity check, each
pair enumeration step, and each word-coverage check, under the identical
counting discipline.

## Governance anomaly (disclosed, not decided)

The prereg describes the candidate base as "adopted CV-P" and the
verdict mapping says ADOPT on pass. This is inaccurate:

- CV-P is PARTIAL, confirmed on a rotated fresh set, but adoption is
  barred pending Python-mirror ruling 6 (per standing context).
- The task states: "CV-P is PARTIAL, doubly gated by ruling 6; untouched."
- Ruling 6 (whether Python-mirror-developed logic may ever be adopted)
  is awaiting the user's decision. I do not decide it.

Resolution: This lane ran an ISOLATED experiment. The original CV-P
files are untouched (verified byte-identical). No COMP-2 code was
integrated into CV-P or CV-1. The candidate lives as run-dir evidence
only.

Despite PASS on all technical bars, ADOPTION IS NOT RECOMMENDED because:
1. The candidate is built on CV-P, which contains Python-mirror-derived
   logic gated by ruling 6.
2. Ruling 6 is the user's to decide; I do not decide it.
3. The prereg's "ADOPT on pass" verdict mapping cannot override the
   standing ruling-6 adoption bar.

The honest verdict is: **PASS on bars, ADOPTION BARRED pending ruling 6.**
If the user rules on ruling 6, this result can be revisited.

## Interactive finding (caveat)

Systematic search of src/ and units/ confirms: there is NO current
source-level REPL/chat entry point in src/zag/ (empty, reserved) or
units/ (only teacher docs). Runnable chat artifacts exist only in run
directories (e.g., wave-20260924-1121pdt/candidates/cv1/impl/
tnn_chat_decline_frozen_ref, and the cvp/comp2 binaries tested here).
The repo exploration did not find a src-level chat main.

## Files

- Implementation: intel_trade/impl/comp2.zag
- Binary: intel_trade/impl/comp2 (built, not committed; binary artifacts
  are run evidence)
- Sealed probes: intel_trade/sealed/PROBES.md
- Sealed key: intel_trade/sealed/KEY.md
- Authoring record: intel_trade/sealed/AUTHORING.md
- Enumerator: intel_trade/tools/pair_enum.zag
- This evidence: intel_trade/EVIDENCE_COMP2_1121.md
