# PREREG — MATH TRACK ROUND 3: native reasoning, no bridge (FROZEN)

## 0. Question
Round 2 (VERDICT_MATH_R2_AMENDMENT.md, commits 9f83fc3c/04609384/f6de11d5/4050b109):
7 engines, 5 hypotheses, only H3 (formalization-is-the-bottleneck) survived.
Every engine scored 0/22 on raw NL because each needed a formal schema first.

Micah's challenge: "humans don't need a bridge for everything, so TNN shouldn't
either." A human reads a word problem and reasons DIRECTLY OVER THE LANGUAGE —
no one translates it into a formal schema in their head first. Round 3 tests
H-NATIVE: an engine that reasons natively over raw utterance bytes (no
NL→schema translation step) can match or beat DUAL on derivation batteries AND
on raw-NL problems.

## 1. Engines
Controls (rebuilt verbatim from frozen R2 sources, rerun):
- DUAL-R1: round-1 DUAL (separate prover D + real H5 referee R).
- REF-FIRST: best R2 engine (matches DUAL's B5X profile; PB2 pass).

Native candidates (minimum 3, specs frozen in IDEAS addendum BEFORE any build):
- N1 NATIVE-ENTAIL: forward text-state rewriting via byte-pattern licenses
  (fable design).
- N2 NATIVE-DELIM: backward deliberative elimination over raw text.
- N3 ONEBRAIN-NATIVE: shared-ledger parallel deliberation, strategy kill.
- N4 ANALOG-NATIVE: analogical case-based reasoning over raw text.
  (All four spec'd in IDEAS_ADDENDUM_R3.md, frozen with this prereg.)

## 2. Common ground
- Same frozen knowledge store, in PLAIN ENGLISH TEXT form (same content as
  KNOWLEDGE_STORE.md, wording frozen by battery crew). Native engines cite
  NL items; controls cite formal items. Neither may ingest other knowledge.
- Same depth bounds: primary bound 8 steps; B6X-NL bound 128.
- Pure Zag, zero RNG, deterministic; 3x byte-identical reruns per problem per
  engine; pinned toolchain znc_linux_x86_64_abed8aa1.
- No problem-specific content, hardcoded answers, or curated NL→schema
  mappings in ANY engine. For native engines additionally: NO internal
  conversion of problem text into schema terms (audited per §7).
- Byte-level operations only for native engines. Byte-span surgery (split on
  ASCII whitespace/punctuation, slice, match, splice) is native; assigning
  spans to a fixed vocabulary of meaning-bearing units is the bridge and is
  forbidden. Sealed solutions never read by engines (exit-3 guard).

## 3. Batteries (frozen here; items authored by battery crew, SEALED before engines run)
- R3N: 24 NEW raw-NL reasoning problems (word problems in plain language, no
  schema given; number theory, geometry, logic puzzles, causal/temporal).
  Graded on correct verdict AND honest derivation (KB4-style audit).
- B2R-NL / B3R-NL / B4R-NL: raw-NL twins of the R2 formal batteries (same
  problems, NL wording only). Native engines attempt NL twins; controls
  attempt formal originals.
- B5X-NL: 60 NL false-rule-injection problems (NL twins of B5X chains:
  3 chain depths x 20; Kind D derivable / Kind W withholdable).
  Harder than R2: chains embed the false rule mid-chain (not at the endpoint)
  and add one distractor true-but-irrelevant chain per problem.
- B6X-NL: 3 NL derivations requiring >=100 steps each, bound 128.
- B1N: P01-P22 raw NL (rerun; controls expected to abstain honestly as in R2).

## 4. Hypotheses
- H-NATIVE (Micah's): some native engine wins >=2/3 primary bars (§6) against
  BOTH DUAL-R1 and REF-FIRST. KILL: no native engine wins >=2/3 → FALSIFIED.
- H-NODISC: some native engine discriminates derivable vs withholdable on
  B5X-NL: >=45/60 correct verdicts with <10 false_derived AND <10
  false_withheld (R2 best: nobody cleared both). KILL: none clears → FALSIFIED.
- H-NOHIDE (anti-bridge): the winning native engine passes the disguised-
  formalizer audit (§7). KILL: winner fails audit → its victory is VOID
  (bridge in disguise); H-NATIVE cannot be claimed through it.
- H-SCALE-NATIVE: some native engine completes a B6X-NL 100-step derivation
  with correct verdict. KILL: none do → FALSIFIED.

## 5. Kill bars carried forward
- KB2 contrast (on NL twins for native engines; formal for controls).
- KB4 audit coherence: 3 independent grader subagents, blinded, 1-5 on
  circularity/unwarranted/magic; inter-rater alpha >0.8 or VOID (round
  failure). Graders dispatched by the round coordinator (depth 1/2).
- PB3-line: B5X-NL incorrect breakdown (false_derived vs false_withheld).

## 6. Primary bars + decision rule
- PB1 = R3N quality: >=12/24 correct verdicts AND honest traces (KB4-style
  mean >=4.0, zero magic-knowledge flags). Controls attempt R3N too (expected
  honest abstention, as R2 B1N); the bar is absolute.
- PB2 = NL-twin derivation: solve rate on B2R-NL/B3R-NL/B4R-NL >= 80% of
  DUAL-R1's solve rate on the formal originals.
- PB3 = B5X-NL discrimination: >=45/60 correct, <10 false_derived, <10
  false_withheld.
DECISION RULE (frozen): the R2 verdict (DUAL wins) STANDS unless a native
engine wins >=2/3 primary bars against BOTH DUAL-R1 and REF-FIRST. The round
names the exact engine that works, or reports that none does.

## 7. Disguised-formalizer audit (H-NOHIDE)
1. Trace inspection: every derivation step's grounds must be byte-spans of
   input/store text or prior steps. No step may cite a schema term absent
   from the bytes.
2. Paraphrase perturbation: reword 6 R3N problems preserving meaning; the
   engine's trace must track the new bytes (different spans cited). A
   disguised formalizer snaps to byte-identical canonical traces.
3. Vocabulary probe: 6 nonce-word variants (content words replaced by
   nonce words, relations preserved). A native engine reasons over the
   relations in the text; a formalizer with a smuggled lexicon collapses.

## 8. Commit protocol
Prereg commits ALONE first (frozen). Then IDEAS addendum (engine specs +
which ideas chosen and why). Then one build commit per engine. Then
battery/item commits (sealed before engines run). Then evidence + verdict.
