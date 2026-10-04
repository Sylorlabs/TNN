# REPORT: Grammar Outlier-Exclusion Worker

## Verdict: GRAMMAR-OUTLIER-COMPLETE

## Claim tested

H-OUTLIER-1: a majority-consistency exclusion procedure, computed from
the learner's own per-example licensor profiles with no researcher
hardcoded relation ids or deception signatures, repairs the C222 W5
denial-of-learning flaw. Clean batches induce the identical grammar as
before; poisoned batches induce the correct grammar while excluding
and flagging the minority contradicting examples; genuinely ambiguous
batches are refused with an explicit ambiguity report rather than a
silent pick.

## Method

gi_induce2 (appended to a byte-identical copy of the induction
machinery; the original gi_induce is untouched and kept for the
comparison arm):

1. Per-example licensor profile: for each live BUILD fact (T,45,P),
   S_i = { r2 != 45 : live fact (T,r2,P) }.
2. Minority-unlicensed exclusion: examples with empty profiles are
   excluded and flagged iff they are a strict minority of the batch;
   otherwise refuse (codes 1/2).
3. Majority-consistent licensor set: enumerate nonempty subsets of the
   distinct observed licensor relations (first-seen order). A set is
   viable iff it covers a strict majority of licensed examples
   (nonempty profile contained in the set). Winner: smallest
   cardinality, then largest coverage, then largest cross-target
   attestation (distinct subjects T with a live (T,r,.) fact in the
   learner's whole experience). A tie on all three keys is ambiguity:
   refuse with code 4 and write no grammar. More than 2 winning
   relations refuses with code 5 (the pre-existing type-70 node layout
   limit, unchanged).
4. Licensed examples whose profile is not contained in the winner are
   excluded and flagged as inconsistent.
5. Literal ranges and the type-70 node write are unchanged except they
   run over the winning set; nbuild records examples consistent with
   the induced grammar (post-prereg refinement, see below).

Why cross-target attestation is learner-derived: it counts the
learner's own facts. Genuine licensors (43, 44) are attested across
all 10 EXL2 targets in decomp experience; a smuggled relation is
attested only where the deceiver taught it. This breaks the tie
between a genuine set and a piggybacked bogus set without naming any
relation.

## Results (3/3 byte-identical, SHA-256 29de7c2b...)

### Arm A, clean batch: PASS

GI2-INDUCED=1, 0 excluded. Grammar line byte-identical to transfer W1:
nbuild=4 nlic=2 lic=44,43 a=[0,9] b=[0,9] maxlinks=1. Battery 6/6
valid. Original gi_induce on the same world: 1 (sanity).

### Arm B, one unlicensed deceiver (W5a style): PASS

GI2-INDUCED=1. Excluded exactly 1: (T=2, P=153, why=unlicensed).
Same grammar line as arm A. Battery 6/6 valid. Original gi_induce on
the same poisoned batch: 0, reproducing the W5a denial of learning.
The repair is demonstrated on the identical batch the old code
refused.

### Arm C, two minority deceivers (W5a + W5b style): PASS

GI2-INDUCED=1. Excluded exactly 2: (T=2, P=153, why=unlicensed) and
(T=3, P=65, why=inconsistent; profile {43,46} not contained in
{43,44}). Grammar line byte-identical to arm A. Battery 6/6 valid.

### Arm D, 50/50 split, disjoint vocabularies: PASS

GI2-INDUCED=0, refusal code 4 (ambiguous tie: {43,46} vs {44,46} tie
on size, coverage, and attestation), no grammar node written, battery
reports NOGRAMMAR. The learner refused to silently pick a side, as
preregistered.

### Arm E, adversarial majority poisoning (5 deceivers vs 4 clean): predicted defeat CONFIRMED

GI2-INDUCED=1 with the bogus grammar nbuild=5 nlic=1 lic=46
a=[1,3] b=[5,9]. The 4 clean examples are "excluded" as inconsistent
by the poisoned majority. Battery 0/6 valid (all class 0: no 46 fact
verifies against eval knowledge). A majority-based excluder cannot
survive majority poisoning; the defeat occurred exactly as
preregistered and is reported, not hidden.

### Arm F, adversarial coordinated piggyback minority (2 vs 4): PASS

GI2-INDUCED=1, grammar {44,43} byte-identical line to arm A, battery
6/6. Excluded exactly 2: (T=9, P=145) and (T=2, P=66), both
why=inconsistent. The {43,44} vs {44,46} tie on size and coverage was
broken by cross-target attestation (20 vs 12). Coordinated minority
deception sharing one bogus relation is still caught.

### Arm G, extra probe, piggyback at exactly 50/50: predicted limitation CONFIRMED

GI2-INDUCED=1 with lic={44,46}; the clean (3,45,P(3,0)) example was
wrongly excluded as inconsistent. Battery 6/6 valid (via relation 44;
the 46 licensor is dead weight on these targets, so the corruption is
in the grammar record, not in construction behavior). Piggybacking at
exactly 50/50 flips the majority. Documented as a residual
vulnerability.

## Post-prereg refinement (transparent, no bar changed)

After the first full run, nbuild was changed from "licensed examples
admitted to the vote" to "examples consistent with the induced
grammar" (licensed minus inconsistent exclusions). No preregistered
bar mentions nbuild outside arm A's clean line (unaffected: 4).
Effect: arms A, B, C, F now emit byte-identical grammar lines, which
is the literal "same grammar as before" claim. The refinement was
rebuilt and rerun 3/3 before this report.

## Exclusion-criterion analysis

The criterion has three layers, each learner-derived:

* Minority-unlicensed exclusion handles W5a-class attacks: an example
  nobody's experience licenses is dropped only when the batch mostly
  disagrees with it. A majority-unlicensed batch refuses instead of
  inventing licensors.
* Viable-set majority consistency handles W5b-class attacks: the
  licensor set must explain a strict majority of examples. Minimal
  cardinality plus maximal coverage selects the genuine set when the
  deceiver is a minority, with no relation whitelist.
* Cross-target attestation handles coordinated piggybacking: the
  learner's background experience (decomp facts across targets)
  outvotes a relation the adversary taught twice.

Failure modes, all demonstrated: strict-majority poisoning (arm E)
wins outright; exact 50/50 with piggybacking (arm G) flips the vote;
an adversary whose bogus relation is attested across as many targets
as genuine relations stops being an outlier by any learner-visible
measure, and the excluder correctly cannot exclude it. The honest
boundary: this excluder defends the minority-outlier regime, not the
regime where the adversary owns half or more of the evidence.

## Adversarial test (mission test 5)

Three crafted defeats/limits: (E) majority poisoning defeats the
excluder and induces a bogus lic={46} grammar (battery 0/6, caught by
eval verification, but the exclusion itself is beaten); (G)
piggybacking at exactly 50/50 induces lic={44,46} and wrongly excludes
a clean example; (F) shows the attestation tiebreak still catches
coordinated piggybacking at 2-vs-4 minority. No deception signature
was hardcoded to achieve any of this; the same generic procedure
produces all three behaviors from the evidence alone.

## Researcher-owned vs learner-owned

Researcher-owned: EXL2 definition, pair encoding, teach order,
TRAIN/TEST split, classification rubric, the gi_induce2 procedure
(including the choice of majority-consistency as the criterion type),
the deceiver designs in the driver.
Learner-owned: all eval/decomp/BUILD facts, every per-example
licensor profile, the exclusion decisions, the winning licensor set
{44,43}, the literal ranges, the attestation counts, the induced
grammar nodes. No branch of gi_induce2 names a relation id or a
deception pattern; run against a world with different licensors it
would exclude outliers around those.

## Metrics

- Cognition lines added: ~320 (gi_induce2 + 4 helpers, appended to a
  byte-identical machinery copy); driver ~315 lines (teaching + arms).
- Modes/bridges/handlers: 0. New semantic cases: 0. Base
  modifications: 0 (go_base.zag is a byte copy).
- Determinism: 3/3 byte-identical runs.
- Induction: clean 4/4 -> {44,43}; poisoned batches (B, C, F) ->
  {44,43} with 1/2/2 exclusions flagged; 50/50 -> explicit refusal;
  majority poison -> predicted bogus induction, reported.
- Construction: 6/6 valid on arms A, B, C, F; 0/6 on arm E (class 0).

## Follow-ups

1. The nlic<=2 cap is now the binding generality limit (transfer
   report follow-up 3): a world with 3 genuine licensors still
   refuses. Generalizing the grammar node layout without opening an
   exclusion hole is open work.
2. Arm G's residual vulnerability (piggyback at 50/50) and arm E's
   majority poisoning are the two documented defeat regimes. A
   revision mechanism that re-opens an induced grammar when later
   evidence contradicts it would be the natural next layer.
3. Cross-target attestation currently counts decomp-shaped experience;
   an adversary doing full-curriculum fake teaching to match genuine
   attestation is the terminal attack and is undetectable in
   principle by any outlier method.
