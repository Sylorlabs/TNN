# PREREG — MATH TRACK ROUND 4: the native reasoner hunt continues (FROZEN)

## 0. Question
R1: DUAL beat ONE 2–1. R2: 7 engines, 5 hypotheses, only H3
(formalization-bottleneck) survived; DUAL stands. R3 (VERDICT_MATH_R3.md,
commit 2a18a35c): four genuinely native architectures tested Micah's
H-NATIVE and it was FALSIFIED on the metrics — but the failure analysis is
precise and is this round's starting point:

- Natives RECOGNIZE inference idioms (byte-pattern licenses fire) but DO NOT
  COMPOSE them into multi-step derivations. n1's licenses fired yet chains
  never reached goals (3/37 twins); n2's backward links found nothing (1/37);
  n4 withholds universally by construction.
- n3 is the lead worth chasing: its machinery WORKS (derived a dev pigeonhole
  end-to-end) but doesn't scale — every thread exhausts budget. A native that
  reasons correctly small and dies on budget is a scaling problem, not a
  wrong-idea problem.
- n1's paraphrase instability (5 WITHHELD→DERIVED flips on meaning-preserving
  rewordings) voided its credibility. Paraphrase invariance is a HARD GATE
  this round: any engine that flips verdicts on meaning-preserving
  rewordings is VOID regardless of scores.
- Under false-rule injection natives withhold everything (can't tell true
  chains from false) — the mirror of DUAL, which derives false chains. The
  target is a native that DISCRIMINATES: derives the true, withholds the
  false.

Micah's order: keep hunting; we will eventually find it. R4 attacks the
composition failure directly with three new native designs.

## 1. Engines
Controls (rebuilt verbatim from frozen R2/R3 sources, rerun; R3 numbers must
reproduce byte-identically or the round halts):
- DUAL-R1: round-1 DUAL (separate prover D + real H5 referee R).
- REF-FIRST: best R2 engine.

Native candidates (minimum 3, specs frozen in IDEAS addendum BEFORE any build):
- N5 CHAIN-NATIVE: n3-lineage scale-up. Fixes the budget exhaustion with
  better thread prioritization and lemma caching across threads — n3 proved
  the machinery, now make it scale. Genuinely native: byte spans only.
- N6 GOALCHAIN-NATIVE: explicit multi-step chaining mechanism over byte
  spans. Goal-directed chaining (not idiom firing): licenses compose into
  chains of 5/20/50/100 licensed steps aimed at the goal, with
  backtracking and lemma reuse.
- N7 DISCRIM-NATIVE: native discriminator under false-rule injection.
  Deliberates true-vs-false chains in raw text and DERIVES the true while
  WITHHOLDING the false — must discriminate, not withhold-everything
  (R3 natives) or derive-everything (DUAL).

## 2. Common ground
- Same frozen knowledge store, PLAIN ENGLISH TEXT form (wording frozen by
  the R4 battery crew; NL inference surfaces audited per R3 §8.3 — the
  rendering must preserve the inference surfaces the knowledge carries).
  Native engines cite NL items; controls cite formal items. Neither may
  ingest other knowledge.
- Same depth bounds: primary bound 8 steps; B6X-NL bound 128; CHAIN50-NL
  bound 160.
- Pure Zag, zero RNG, deterministic; 3× byte-identical reruns per problem
  per engine; pinned toolchain znc_linux_x86_64_abed8aa1.
- No problem-specific content, hardcoded answers, or curated NL→schema
  mappings in ANY engine. For native engines additionally: NO internal
  conversion of problem text into schema terms (audited per §7). No
  NL→schema translation step for native candidates — that is the whole
  point of the hunt.
- Sealed solutions never read by engines (exit-3 guard).
- PARAPHRASE HARD GATE (§7.3): 12 meaning-preserving paraphrase pairs +
  12 nonce-word variants, authored by the battery crew and sealed. An engine
  must return the SAME verdict on every variant of a problem. ANY flip
  (WITHHELD→DERIVED, DERIVED→WITHHELD, or verdict change) VOIDS the engine
  for the round regardless of its bar scores. This gate runs BEFORE bar
  scoring; a voided engine's bars are reported as VOID, not as numbers.

## 3. Batteries (frozen here; items authored by battery crew, SEALED before engines run)
Carryover (rerun verbatim; natives attempt NL versions, controls formal
originals):
- R3N (24 raw-NL problems), B2R-NL/B3R-NL/B4R-NL twins, B5X-NL (60 NL
  false-rule-injection), B6X-NL (3 × ≥100-step), B1N (P01–P22 raw NL).

New (authored by the R4 battery crew, sealed before any engine runs them):
- CHAIN-NL: 20 raw-NL problems REQUIRING 5–20 step derivations (reference
  solutions with step counts authored and sealed). Graded on correct verdict
  AND an honest step-by-step trace (each step cites byte-spans).
- CHAIN50-NL: 6 raw-NL problems requiring ≥50 steps, bound 160.
- PARA-INV: 12 paraphrase pairs + 12 nonce variants for the §7.3 hard gate.

## 4. Hypotheses
- H-NATIVE-R4 (Micah's, standing): some R4 native engine wins ≥3/4 primary
  bars (§6) against BOTH DUAL-R1 and REF-FIRST. KILL: no native wins
  ≥3/4 → FALSIFIED for R4 (the hunt continues regardless — Micah's order).
- H-CHAIN: some native completes ≥1 CHAIN50-NL problem with correct verdict
  AND an honest step trace (direct attack on the R3 composition failure).
  KILL: none do → FALSIFIED.
- H-DISC-NATIVE: some native discriminates on B5X-NL: ≥45/60 correct
  verdicts with <10 false_derived AND <10 false_withheld. KILL: none
  clears → FALSIFIED.
- H-PARAPHRASE: the round's best native passes the §7.3 hard gate.
  KILL: it flips → VOID (not a near-miss; a void).

## 5. Kill bars carried forward
- KB2 contrast (NL twins for natives; formal for controls).
- KB4-style audit coherence on derivation traces: 3 independent blinded
  graders, 1–5 on circularity/unwarranted/magic; inter-rater alpha >0.8 or
  VOID (round failure on that battery). Graders dispatched by the round
  coordinator.
- PB3-line: B5X-NL incorrect breakdown (false_derived vs false_withheld).

## 6. Primary bars + decision rule
- PB1 = R3N quality: ≥12/24 correct verdicts AND honest traces (KB4-style
  mean ≥4.0, zero magic-knowledge flags). Absolute bar.
- PB2 = NL-twin derivation: solve rate on B2R-NL/B3R-NL/B4R-NL ≥ 80% of
  DUAL-R1's solve rate on the formal originals.
- PB3 = B5X-NL discrimination: ≥45/60 correct, <10 false_derived,
  <10 false_withheld.
- PB4 = CHAIN-NL chaining: ≥12/20 correct verdicts with honest step traces
  (every step cites byte-spans of input/store/prior steps; graders confirm).
DECISION RULE (frozen): the R3 verdict (DUAL wins) STANDS unless a native
engine wins ≥3/4 primary bars against BOTH DUAL-R1 and REF-FIRST AND passes
the §7.3 paraphrase hard gate. The round names the exact engine that works,
or reports that none does — with the mechanism-level story of whatever got
closest.

## 7. Disguised-formalizer + paraphrase audits
1. Trace inspection: every derivation step's grounds must be byte-spans of
   input/store text or prior steps. No step may cite a schema term absent
   from the bytes. No typed variables, scope, unification, or formal syntax
   anywhere in a native engine.
2. Paraphrase perturbation: 12 rewordings preserving meaning; the engine's
   trace must track the new bytes (different spans cited). A disguised
   formalizer snaps to byte-identical canonical traces.
3. HARD GATE: §2 para 7. Any verdict flip on a meaning-preserving
   rewording or nonce variant VOIDS the engine for the round. Gate runs
   before bar scoring.
4. Vocabulary probe: 12 nonce-word variants (content words replaced,
   relations preserved). A native reasons over relations in the text; a
   formalizer with a smuggled lexicon collapses.

## 8. Commit protocol
Prereg commits ALONE first (frozen). Then IDEAS addendum (N5/N6/N7 specs +
which ideas chosen and why). Then one build commit per engine. Then
battery/item commits (sealed before engines run the new batteries). Then
evidence + verdict. No engine runs a sealed battery before its seal commit.
