# PREREG — MATH TRACK ROUND 2: broader engines, more hypotheses (frozen)

## 0. Question
Round 1 (VERDICT_ONEENGINE_VS_DUAL.md, commit 727dcc75): DUAL beat ONE 2-1,
but narrowly — tied at perfection on B2/B3/B4/B6; ONE lost only KB5
(contradiction-fragility); KB6 falsified the dual's predicted interface
advantage; KB4 was VOID; the recommended hybrid was never built. Micah's
verdict on round 1: "maybe we didn't test enough engines or enough
hypotheses."

Round 2 asks: does a broader engine space overturn the round-1 verdict, or is
the formalization bottleneck (round-1 caveat: B1's P01-P22 are natural
language; engines ran on formal analogs; the NL->schema step is still human
judgment) the dominant factor regardless of engine?

## 1. Engines (7 total)
Round-1 baselines, rebuilt verbatim from frozen sources and rerun:
- ONE-R1: round-1 ONE (match-and-bind core; refereeing = derive NOT-H).
- DUAL-R1: round-1 DUAL (separate prover D + real H5 referee R, interface).

New (minimum 5):
- (a) HYB: ONE's match-and-bind derivation core + contradiction-tolerant
  referee in ONE mechanism. No D<->R interface. Single pass: derivation
  proceeds by match-and-bind; when a contradiction is derived, the referee
  weighs the evidence (premise quality, derivation depth, corroboration)
  instead of collapsing to universal withhold. Must not reintroduce a
  separate referee engine behind a renamed call boundary (checked in audit).
- (b) REF-FIRST: derives THROUGH the H5 referee. The referee drives search:
  selects which hypothesis to pursue, issues derivation directives, scores
  partial evidence mid-search, decides when to deepen vs stop. Derivation
  steps are referee-initiated, not prover-initiated-then-judged.
- (c) LEARN-FORM: learned NL->schema formalizer + ONE's match-and-bind
  derivation core. The formalizer learns from worked examples (frozen
  round-1 traces + knowledge store items as evidence); every learned
  mapping must trace to evidence. No curated formalization tables.
  Tested on raw NL problems it has never seen formalized.
- (d) GROK-D: from the Grok-4.7 ideas round (spec frozen in addendum).
- (e) FABLE-E: from the Fable ideas round (spec frozen in addendum).
(Native-design outputs feed (d)/(e) selection if stronger; the addendum
records which ideas were chosen and why. All engine specs frozen BEFORE
any build commit.)

## 2. Common ground (fairness — all engines)
- Same frozen knowledge store (round-1 KNOWLEDGE_STORE.md, 25 items) PLUS the
  committed inference schemas (COMMIT_SCHEMAS.md, round-1 ceremony). Neither
  may ingest other knowledge. LEARN-FORM's formalizer may additionally learn
  ONLY from frozen round-1 traces (evidence, not new knowledge).
- Same claim representation; same depth bounds: primary bound 8; B6X bound
  128 (battery parameter, documented; engines must also terminate on
  fixpoint — the bound is a measurement ceiling, not a design limit).
- Pure Zag, zero RNG, deterministic given state; 3x byte-identical reruns
  per problem per engine; pinned toolchain znc_linux_x86_64_abed8aa1.
- No problem-specific content, hardcoded answers, domain tricks, or curated
  mappings in ANY engine. Inference ONLY from committed schemas + store
  (+ learned-from-evidence mappings for LEARN-FORM, each traced). Violation
  = build rejected.
- Sealed solutions never read by engines (exit-3 guard, round-1 pattern).

## 3. Batteries (specifications frozen here; items authored by test crew,
##    sealed BEFORE engines run)
- B2R: round-1 B2, 12 problems (baseline rerun).
- B3R: round-1 B3, 10 interleaved conjecture-test-revise problems.
- B4R: round-1 B4, 15 transfer problems.
- B4X: 15 NEW transfer problems BEYOND math-adjacent (causal, temporal,
  semantic, social reasoning); solvable ONLY with committed schemas, no
  domain rules; hardness: require >=3 derivation steps.
- B5X: multi-hop false-rule injection. False rules that CHAIN (false A=>B
  plus false B=>C makes false A=>C derivable in 2+ hops — single-hop
  detection is insufficient). 3 chain-depth levels x 20 problems, injected
  into a COPY of the store. Measures contradiction tolerance under
  compounding falsehood, not just single false rules.
- B6X: scaling — problems requiring >=100 store items; bound 128; measure
  derivation counts AND wall time per engine.
- B1N: P01-P22 in RAW NL form (as written, no human formalization). Engines
  must formalize themselves or abstain. Tests H3 directly.
- B7F: formalization battery — 20 NL problems with SEALED formal analogs
  (authored by test crew, committed sealed before engines run). Scores
  LEARN-FORM's formalizer by mechanical schema-equivalence against the
  sealed analogs; curated baseline = applying round-1 human formalization
  choices mechanically (no learning).

## 4. Hypotheses (each with falsifiable prediction + kill bar)
- H1 contradiction-tolerance-is-the-value: the referee's true contribution
  is contradiction tolerance, not derivation. PREDICTS: on B5X, every
  tolerant-referee engine (HYB, REF-FIRST, DUAL-R1) produces >=50% fewer
  incorrect conclusions than ONE-R1. KILL: if no tolerant engine beats
  ONE-R1 by >=50% on B5X incorrect count, H1 is FALSIFIED.
- H2 interface-cost-always-loses: any engine with a separate
  derivation<->referee interface pays >=2x wall time vs the fastest
  interface-free engine at equal (+/-10%) derivation counts on B6X.
  KILL: if any interfaced engine matches the fastest interface-free
  engine within 1.5x wall time at equal derivations, H2 is FALSIFIED.
- H3 formalization-is-the-bottleneck: on B1N (raw NL), ALL engines solve
  <=30%, AND each engine's formal-analog-minus-NL gap exceeds the
  between-engine spread on formal analogs. KILL: if between-engine spread
  on formal analogs exceeds the formalization gap for any engine, H3 is
  FALSIFIED.
- H4 learned-formalization-beats-curated: LEARN-FORM scores >=70%
  schema-equivalence on B7F held-out items AND beats the curated baseline.
  KILL: below 70% or not beating baseline => FALSIFIED.
- H5 hybrid-dominates: HYB beats BOTH ONE-R1 and DUAL-R1 on the primary
  bars (section 6). KILL: fails to beat both => FALSIFIED.

## 5. Kill bars carried from round 1 (rerun on extended batteries)
- KB1X interleaved (B3R): pairwise wins (solves and the other does not),
  recorded per engine pair.
- KB2 contrast (B1+B2 formal analogs, 20 easy/open pairs): scoring engines
  must show conf(solvable)>conf(open) on >=18/20; withholding engines must
  show derived-vs-withheld discrimination on all pairs.
- KB4 audit coherence: 3 independent grader subagents rate each solved
  problem's audit trail 1-5 (circularity, unwarranted steps, magic
  knowledge), blinded to engine identity. Requires inter-rater alpha >0.8
  or VOID (round-1 rule kept). If any engine's mean exceeds DUAL-R1's by
  >=1.0, DUAL-R1 is falsified as audit-hostile. MUST BE MEASURED this
  round — voiding again is a round failure, not a finding.

## 6. Primary bars + decision rule
Primary bars: PB1 = KB1X pairwise wins vs each round-1 parent (>=7/10 to
claim); PB2 = KB2 contrast sub-bar appropriate to the engine's confidence
model (pass/fail); PB3 = B5X incorrect conclusions <= half of the worse
round-1 parent's count.
DECISION RULE (frozen): the round-1 verdict (DUAL wins) STANDS unless a new
engine wins >=2 of the 3 primary bars against BOTH ONE-R1 and DUAL-R1.
A new winner must beat both parents, not just one.

## 7. Honest-reporting requirements
- Full head-to-head table (all engines x all batteries), per-hypothesis
  FALSIFIED/SURVIVED with the measured numbers, KB4 measured with
  inter-rater alpha, and the direct answer: was the engine space the
  limiting factor, or does the formalization bottleneck dominate?
- Negative results are findings. A tie is a finding. VOID KB4 is a round
  failure.
- 3x byte-identical reruns per problem per engine; any divergence voids
  that problem for that engine (reported, not silently rerun).

## 8. Commit protocol
This prereg commits ALONE first (frozen). Then the ideas addendum (engine
(d)/(e) specs + which ideas were chosen and why). Then one build commit per
engine (sources only; no binaries, no .zagd). Then battery/item commits
(sealed solutions committed before engines run). Then evidence + verdict.
Incremental commits, never a giant final dump.
