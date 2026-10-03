# REPORT: DOMAIN-BLINDNESS -- Verdict PASS (blind)

Date: 2026-10-03. Worker: domain-blindness.
Battery: Micah's DOMAIN-BLINDNESS TEST applied to the unified
behavior-contract composition operation U (COMPOSE-COLLAPSE, verdict
SUBSUMPTION). Pure Zag, pinned safebin znc. Prereg committed alone
before implementation (`54e706c`).

## Verdict: PASS (blind)

U's composition decisions are invariant to human domain/relation/entity
identifiers AND to kind-label polarity. After mechanically renaming
every exercised identifier (relations 81/82/91/92/93/99, entities
21/22/61/62/63/71/81/82/83/84/101/102/103/111/112/201/202/203/211,
setup names, query labels) to opaque tokens and applying the frozen
inverse mapping, the renamed system's output is BYTE-IDENTICAL to the
original (cmp EMPTY, digest `be713f82...` reproduced exactly).
A second variant additionally swapping the NODE/NUM kind-label polarity
(1<->2) throughout `pkind` and all query contracts is likewise
byte-identical after swap-back. No human label leaks into U's
decisions anywhere: not in admission, not in trial execution, not in
widening, not in success recording.

## Results

Variant A (identifier renaming):
- `a_run1/2/3.txt`: 3/3 byte-identical, sha256
  `d7e778f9313a9e603d755eca7895bc1b3d23665dd8409ebc5702cc543a99e47f`
- Inverse-mapped (`unmap_a.sh`): sha256
  `be713f822779afdd7cf1c3f2e87670dc4b5e903fa73a8bc0ede0a105f3a219d7`
  = the frozen baseline digest, cmp EMPTY vs the reproduced original.

Variant B (identifier renaming + kind-label polarity swap):
- `b_run1/2/3.txt`: 3/3 byte-identical, sha256
  `a84a954f0ae950e2b80e89ce88a3717a8120f610c7e1920e3e6f06909c4d64ac`
- Raw census correctly shows the swapped polarity
  (`inmask=2 outmask=1`), proving the mechanism genuinely ran with
  inverted kind labels; inverse-mapped (`unmap_b.sh`): sha256
  `be713f822779afdd7cf1c3f2e87670dc4b5e903fa73a8bc0ede0a105f3a219d7`,
  cmp EMPTY vs baseline.

## Kill bar results

- B1 MECHANICAL RENAMING: PASS with two disclosed minimal transcription
  fixes (see below). All four frozen step-8 audits pass on
  `db_new.zag`: zero original identifier tokens survive as whole words,
  zero human labels survive, zero tagging residue, exactly the 3 header
  comment lines remain. The renaming script's first commit postdates
  the prereg commit (commit-order self-check holds).
- B2 DETERMINISM: PASS. 3/3 pairwise byte-identical runs per variant
  (cmp-verified); digests recorded above.
- B3 BLINDNESS-A: PASS. Inverse-mapped Variant A stdout cmps EMPTY
  against the frozen baseline.
- B4 BLINDNESS-B: PASS. Inverse-mapped Variant B stdout cmps EMPTY
  against the frozen baseline.
- B5 U-LOGIC IDENTIFIER-FREE: PASS. The frozen renaming steps 2-7
  applied to `ref_uc_uni.zag` change ZERO bytes (cmp-verified), and a
  numeric-token inventory of the U logic (main stripped) shows only
  mask bits 0/1/2/3/4, shifts, arena offsets 936/940/944, the -2 miss
  sentinel, and counters -- no relation/entity-scale constants. The
  only identifier-scale literals in the file sit inside the stripped
  `main` (old P1-P5 query constants), which is not part of any build.
- B6 NO NEW SEMANTICS: PASS. `diff ref_uc_base.zag
  db_base_kswap.zag` shows exactly the two `pkind` return lines;
  `diff db_new.zag db_new_kswap.zag` shows exactly the four
  `uni_solve` lines; grep for comparisons against any renamed
  identifier value (`== 5001`-style) across both built full sources
  returns empty.

## Disclosed transcription fixes (honest record)

Two deviations from the PREREG Section 4.1 text, both mechanical,
both caught or required by the frozen audits themselves:

1. Comment-strip pattern: the prereg wrote `grep -v '^//'`, but
   `p6_new.zag` also contains INDENTED comment lines (`  // ...`),
   which `^//` misses -- and frozen audit (d) requires exactly the 3
   header `//` lines to remain. The implementation uses
   `grep -v '^[[:space:]]*//'`, which is the unique reading
   consistent with both the step ("strip every line starting with
   //", parenthetical: "all human vocabulary in comments") and the
   audit. No code-line content is affected (no trailing comments
   exist in the file; verified).
2. `uni_solve` arena alternation: the prereg's tagging pattern
   `uni_solve\((A|C),...` missed the A2/A3 call sites (Q2/Q3 use
   arenas A2, A3). The fail-closed step-8 audit caught the surviving
   `61` tokens on the first run; the pattern was corrected to
   `(A[23]?|C)`, which covers exactly the four observed call sites
   (verified by exhaustive call-shape grep: no other arena variants
   exist). No semantic choice involved; the permutation tables and
   all other steps are untouched.

Neither fix alters what the test proves: the renaming remains a fixed
script with zero per-line human judgment, and the audits objectively
verify completeness.

## Why this matters

PAIR6 established that U's boundary is SHAPE (pipeline-only), not
domain: five pipeline pairs across different domains pass, one diamond
fails. This battery closes the complementary question: WITHIN U's
competence, does anything depend on the human-readable identity of
the relations, entities, or structures? Answer: no. The composition
operation reads only learned kind-set contracts (bitmasks over
observed subject-hood), MAP indices, and integer values through
equality -- never a label. The kind-polarity variant further shows U
does not even depend on the researcher's NODE/NUM polarity assignment:
the entire kind ontology could be inverted and every composition
decision is unchanged. This is the behavior Micah's test demands:
"the architecture behaves identically under arbitrary renaming."

## Architecture accounting

- Cognition lines added: 0. The U logic is byte-identical in all
  builds (B5). New files are scripts and renamed driver copies only.
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Researcher-owned: the frozen permutation tables, the renaming
  script, the inverse mappings (all disclosed, all mechanical).
- Learner-owned: unchanged from P6 (kind-set contracts, admitted sets,
  trial outcomes) -- now additionally shown to be label-free.

## Toolchain attestation

Zero invocations of python3, python, or any other forbidden
executable. Safebin PATH throughout; `which python3` / `which python`
return NOTHING. Pure Zag for all scientific computation (two znc
compilations, six binary runs). Shell used only for staging, the
frozen sed/grep renaming, hashing, and git.

## Follow-ups (not claimed)

1. GEN does not exist in any compose lane; if a GEN operation is
   implemented later, it needs its own preregistered blindness battery
   (this procedure ports directly).
2. Behavior-class numbers (0-3) were deliberately out of scope as
   mechanism vocabulary; a future battery could test class-label
   blindness if classes ever become learner-assigned.
3. The same rename-and-compare harness generalizes to any future
   composition workload: the scripts are workload-agnostic given a new
   permutation table.

## Files

All in `domain_blindness/`:
PREREG.md (frozen, committed alone at `54e706c`), NAMECHECK.md,
REPORT.md (this file), rename_a.sh, kindswap.sh, unmap_a.sh,
unmap_b.sh (frozen mechanical scripts), ref_uc_base.zag,
ref_uc_uni.zag, p6_new.zag (frozen reference copies, digests in
NAMECHECK Step 1), db_new.zag (renamed driver), db_base_kswap.zag,
db_new_kswap.zag (Variant B sources), uni_nomain.zag, a_full.zag
(sha256 `69d3172a...`), b_full.zag (sha256 `c9ff2c05...`), a_bin,
b_bin (pinned znc builds), a_run1/2/3.txt, b_run1/2/3.txt (3/3
byte-identical each), a_unmapped.txt, b_unmapped.txt (inverse-mapped;
both sha256 `be713f82...`, the frozen baseline digest).
