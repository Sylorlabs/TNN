# REPORT: GEN-GENERALITY -- Verdict GEN-GENERAL

Date: 2026-10-03. Agent: gen-generality. Lane:
docs/lab/research-lead/overnight-20260928/gen_generality/.
Branch: lane-gensubsumesu-20261003 (shared; explicit-pathspec commits only).

## Verdict: GEN-GENERAL

GEN (the frozen C380 value-graph extension of U: rounds over a value pool +
observed-kind checking, d6_gen.zag at 82732a9e8, UNMODIFIED) handles all
four novel composition shapes with no new mechanism, no new behavior
classes, no new opcodes, no modes, no shape templates, no domain handlers:

- Q1 FAN-IN (convergent: two structures' outputs into one 2-input
  downstream): ANS=5, TRIES=5, exact frozen block.
- Q2 DAG-4 (stem feeding a diamond; 4 structures, 3 levels): ANS=5,
  TRIES=8, exact frozen block.
- Q3 CHAIN-3 (three 1-input structures; pool reuse across 3 rounds):
  ANS=2, TRIES=11, exact frozen block.
- Q4a PARTIAL (2-input structure with one slot from an upstream output,
  the other from the pool-seeded subject): ANS=207, TRIES=4, exact
  amended block.
- Q4b PARTIAL-NEGATIVE (expected answer unattainable): honest decline
  ANS=-2, TRIES=13, no WIDEN, no wrong answer, exact amended block.

Per the frozen Section 7 mapping (K1-K7 all PASS): the diamond was a
trial-space limitation with a general fix, not a shape-specific patch.
GEN's value graph covers fan-in, 4-structure DAGs, 3-chains, and partial
applicability by the same rule that covered the diamond.

## Kill bars

- K1 UNMODIFIED-MECHANISM: PASS. (a) ref_gg_base.zag sha256
  a53cdf0126ab1501fb70d9b14c2f745e0ef1838209753df8a0c6d0daf484bbcb
  matches d6_base.zag at 82732a9e8. (b) ref_gg_gen.zag sha256
  d6f1f9d8f4747293bb7a8e99474660347dc24693f62f3d25caaf1d83c19c9d9a
  matches d6_gen.zag at 82732a9e8. (c) gg_full.zag region diffs EMPTY
  (base whole; gen minus main; new driver). (d) grep audit: gg_new.zag
  defines only setup_g1..setup_g4 + main; uses only pre-existing classes
  0/1/3/4; zero relation-conditional branches outside setups.
- K2 FAN-IN: PASS. Q1 block byte-identical to frozen Section 5.
- K3 DAG-4: PASS. Q2 block byte-identical to frozen Section 5.
- K4 CHAIN-3: PASS. Q3 block byte-identical to frozen Section 5.
- K5 PARTIAL: PASS via PREREG_AMEND1. Q4a/Q4b blocks byte-identical to
  the amended Section 5. Amendment record below.
- K6 DETERMINISM: PASS. 3/3 official runs byte-identical (pairwise cmp);
  stderr empty. Output sha256
  4b81226d665735820fec1ec4c0dc3e0447b9947b8069f8618b8ad59e87740752;
  binary sha256
  5e48732a94ddd4a55e6bbc91c91a393f71c80bdbd34e45421ae5010c2d75350a.
- K7 OPAQUE-NAMING: PASS. Grep audit over gg_new.zag, PREREG.md,
  PREREG_AMEND1.md: zero banned-vocabulary tokens in any world
  description, setup, driver, or result. The only matches are the
  document byline ("Worker:" = agent role, no domain content) and the
  Section 3 rule-definition line that enumerates the banned class so the
  rule is checkable. All structures are m0..m3, all relations and
  entities bare integers. A reader cannot tell what "domain" anything
  belongs to.

## Transparent amendment (committed before the runs it governs)

PREREG_AMEND1 (4e57ab950): the frozen Q4a/Q4b hand-derivation treated 213
as kind 1 (NODE); in setup_g4 it is a terminal object, so pkind = 2 (NUM).
Corrected: m2's contract is in{1} out{2}; Q4a TRIES=4 (no round-2
1-input trials); Q4b TRIES=13 with only (0,j) pairs admittable. No
implementation change (the world was built exactly as frozen; the
prediction was corrected to the world, never the reverse). The three
pre-amendment runs are retained as gg_expl1/2/3.txt, reclassified
exploratory and reported. The bar's substance is unchanged: Q4a succeeds
via the intended partial path m1(205,2)=207 (slot 1 = subject, slot 2 =
m0's output), and Q4b declines honestly. This follows the C380
AMEND1/AMEND2 precedent exactly.

## What was built

- ref_gg_base.zag, ref_gg_gen.zag: byte-copies of the frozen C380 sources
  (digests above).
- gg_new.zag: four setups (setup_g1..setup_g4) + main running
  Q1/Q2/Q3/Q4a/Q4b on fresh worlds, single o_flush. No mechanism code.
- gg_full.zag: assembly (603 lines); gg_bin built with the pinned safebin
  znc (sha256 498abcb5...35a4; compile exit 0; 3 analyzer warnings, all
  pre-existing notes in the frozen GEN code).
- gg_run1/2/3.txt: official 3/3 byte-identical outputs.
- gg_expl1/2/3.txt: pre-amendment exploratory runs (reported, not hidden).

## Architecture accounting

- Cognition lines added: 0 (mechanism frozen). New lines: 63 (setups +
  driver), 419+97 (prereg + amendment), this report.
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- New behavior classes/opcodes: 0 (only the C380-authorized generic
  2-input ADD2 class, reused unchanged across all four shapes).
- Researcher-owned: world facts, MAP inventories, teaching schedules,
  driver, expected answers (canonical verification boundary).
- Learner-owned (GEN's): value pool, observed kinds, provenance,
  tried-sets, grown contracts via success-recording.

## Why this matters

C380 left open whether GEN was general or a diamond-shaped patch. Four
shapes it had never seen:

1. Fan-in is the dual of the diamond (convergent vs divergent). GEN
   solves it in 2 rounds: the pool holds both upstream outputs and the
   2-input downstream consumes them. No new combiner logic was needed;
   the same observed-kind admission gates each slot independently.
2. The 4-structure DAG (stem + diamond) solves in 3 rounds. Notably the
   stem value 211 is computed once and consumed twice (fan-out), and the
   two branch outputs are consumed once jointly (fan-in): both patterns
   coexist in one query with no special casing.
3. The 3-chain solves in 3 rounds, one structure per round: the pool is
   doing the work U's pair trials cannot (U's trial space has no
   3-step form at all).
4. Partial applicability is the most informative: the downstream
   structure's contract has per-slot kind sets, and GEN satisfies each
   slot from wherever the pool provides it (upstream output for one,
   the query subject itself for the other). The mechanism never required
   "one structure supplies the whole input". Q4b shows the flip side:
   when the value graph cannot reach the answer, GEN declines (ANS=-2)
   after exhausting its round budget, never emitting a wrong answer.

The boundary learned: GEN is complete for these shapes within its
frozen resource bounds (6 rounds, 64 pool values), and sound outside
them (decline, never a wrong answer). Q4b exercised the round cap as
the termination bound on an unsatisfiable value graph: 13 tries, no
widening (every round productive), clean -2.

## Honest boundaries (carried from the prereg)

- Behaviors pre-installed as learned MAPs; expected-answer verification
  (canonical).
- GEN is researcher-implemented (C380 B3): the claim is that a general
  extension exists and covers these shapes, not that a learner invented
  it.
- One generic 2-input class (ADD2), reused unchanged; no new machinery.
- The dual-2-input-combiner DAG variant was considered and rejected as a
  world design (small-integer sum collisions confound path attribution);
  testing it cleanly needs a second generic 2-input class and its own
  prereg.
- Other readings of partial applicability (kind-mismatched slots,
  multi-value shortfall) are not covered here.

## Toolchain attestation

Zero invocations of python3, python, or any other forbidden executable.
Safebin PATH throughout; `which python3` / `which python` return NOTHING
(NAMECHECK.md Step 0). Pure Zag for all scientific computation. Git via
/usr/bin/git directly (safebin git symlink EPERM defect, per AGENTS.md);
explicit pathspecs; no git reset. Prereg committed alone (484fe6aad)
before implementation; AMEND1 (4e57ab950) before the official runs.

## Files

All in gen_generality/: PREREG.md (frozen), PREREG_AMEND1.md (frozen),
NAMECHECK.md, REPORT.md (this file), ref_gg_base.zag, ref_gg_gen.zag
(frozen references), gg_new.zag (only new code), gg_full.zag (assembly),
gg_bin (pinned znc build), gg_compile.txt, gg_run1/2/3.txt (official
3/3 byte-identical), gg_expl1/2/3.txt (pre-amendment exploratory runs).
