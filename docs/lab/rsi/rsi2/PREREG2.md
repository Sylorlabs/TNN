# RSI-2 PREREG — Recursive Self-Improvement, round 2 (frozen 2026-09-21)

**Answers red-team attack #3** (`docs/lab/redteam/REDTEAM.md`, commit `bc61ef55`):
RSI-1's "+10000→+10000 EXACTLY" was entailed by construction — T-PRIN's
prediction was a hardcoded constant, T-DENSE/T-DOMAIN3 predicted
`10000−baseline` (tautological full-gap closure), variants flipped the
battery's own flag, the oracle's bar (≥50%) was looser than the "EXACTLY"
headline. The loop genuinely ran; the calibration claim was "a unit test in
a lab coat."

**Micah's mandate for RSI-2:** held-out weakness prediction + genuine
quantitative risk + independent implementation + published failures +
negative-intervention discrimination.

## The held-out weakness: quantifier-scope blindness

The miniature learner stores a quantifier tag (ALL/SOME/NONE) at teach time
but its key-normalization stage (M-KEY) drops the tag; retrieval and probe
semantics are tag-blind. Consequence: "ALL ravens are black" vs "NONE ravens
are black" is judged COMPATIBLE; "SOME oak is large" licenses "every oak is
large."

**Why this is held-out (verified 2026-09-21):**
- None of RSI-1's 7 templates (T-DENSE, T-PRIN-PRIORITY, T-DOMAIN3,
  T-QUIET-SKIP, T-AUDIT-TRIM, T-BAR-LOWER, T-GATE-SKIP) targets quantifiers.
- No crew in the lab has ever implemented quantifier-sensitive fact handling.
  (Principle-detection used universal instantiation for *principles*, not for
  quantifier-tagged *facts*; prose v2 has no quantifier machinery.)
- The RSI-2 crew has never implemented a fix for it. The recommender has no
  template to select — it must compose one from primitives.

## Batteries (one pure-Zag binary, `rsi2.zag`, mode-selected)

Quantifiers: ALL=0, SOME=1, NONE=2. Metric: pp×100 (10000 = 1.0000).

**B-QUANT-D1 (seen, diagnose mode).** 8 taught facts / 10 probes:
Teach: ALL(raven,color,black), NONE(raven,color,black),
ALL(swan,color,white), SOME(swan,color,black),
SOME(oak,size,large), ALL(oak,size,large),
NONE(pine,color,green), SOME(pine,color,green).
Probes: 4 contradiction (F1vF2→CONTRA, F3vF4→CONTRA, F5vF6→COMPAT,
F7vF8→CONTRA) + 6 instance (Tweety raven+F1→YES, +F2→NO; Sammie swan+F3→YES,
+F4→UNK; Oakley oak+F5→UNK, +F6→YES).
Prereg expectation: tag-blind baseline scores 4/10 = 4000 (contra 1/4 by
luck on the compatible pair, instance 3/6 by luck on ALL cases).

**B-QUANT-D2 (held-out, verify mode ONLY).** Same structure, disjoint
domain: dolphin, sparrow, maple, cactus. The recommender never sees its
results: D2 executes only in verify mode, which runs only after the crew
has implemented the emitted fix. Diagnose-mode output containing any D2
metric fails KB4.

**B-RECALL (distractor, diagnose).** 8 unquantified facts, 8 probes, exact-key
recall. Prereg expectation: 10000 (passing — tests the recommender does not
invent problems).

**B-COST (distractor, diagnose).** ops/fact on quiet evidence. Prereg
expectation: equals the built-in baseline constant (passing).

**Failing threshold:** gap = 10000 − metric ≥ 3000 → weakness named.

## The recommender: compositional invention, no catalog

The recommender receives NO fix templates. It receives:
1. **Self-model:** the four battery metrics.
2. **Mechanism inventory:** M-TEACH (install), M-KEY (key
   construction/normalization — tag-blindness lives here), M-RETRIEVE
   (matching), M-PROBE-SEM (contradiction/instance judgment), M-ARBITRATE
   (conflict arbitration), M-LEDGER (audit — constitution-protected,
   C1/C4; targeting it = refuse).
3. **Operator grammar** (primitives, each with authored precondition
   signature, information-preservation flag, cost rank):
   - OP1 CARRY-TAG(tag, from→to): propagate an ignored tag through a stage. Preserves: YES.
   - OP2 ADD-CHECK(check, stage): add a verification check at a stage. Preserves: YES.
   - OP3 ADD-PRIORITY(A over B): priority ordering between rules. Preserves: YES.
   - OP4 REQUIRE-K-DISTINCT(dim, k): require k distinct values. Preserves: YES.
   - OP5 ROUTE-THROUGH(mech): route a decision through an existing mechanism. Preserves: YES.
   - OP6 NORMALIZE-AWAY(tag→value, stage): drop a tag for uniformity. Preserves: NO (destroys).
   - OP7 ADJUST-THRESHOLD(t, ±delta): move a numeric threshold. Preserves: YES.
   - OP8 QUARANTINE-PATH(tag): separate store path for tagged items. Preserves: YES.
4. **Analogy DB** (real lab numbers only; untested proposals are NOT citable):
   - A1 dense-phrasing: closure 1.00 on paraphrase brittleness (prose v2 PARA 48/48).
   - A2 arbitration: 1.00 on 156 claim conflicts (new-mechanisms).
   - A3 derivation: 1.00 on 13 principle violations (principle-detection).
   - A4 corroboration: 1.00 on 12 planted falsehoods with search (info-source).

**Deliberation rule (authored, fully logged to the audit ledger):**
- Genuine fix: candidates = operators whose precondition matches the failure
  signature ("tag present at teach, absent at retrieve; tag-requiring probes
  fail; tag-free probes pass"). Score = 3×info_preserve + 1×sig_match −
  cost_rank. Compose the top-2 stage-coherent operators (teach→key→probe
  order). Emit fix spec: operator ids, target mechanisms, ≥40-char change
  description, predicted cost rank.
- Wrong fix: candidates = operators with sig_match=1 AND info_preserve=0
  (plausible but destructive). Pick top-1. Emit with a stated reason why it
  is wrong.
- Analogy selection: maximize mechanism-overlap between the fix's targets
  and the analogy's mechanisms; ties → lowest analogy id.
- **Range mapping (published):** closure = analogy_rate × discount, discount
  0.85 same-dimension / 0.70 novel-dimension. lo = clamp(gap×(closure−0.15)
  − 1000, 0, 10000); hi = clamp(gap×(closure+0.15) + 1000, 0, 10000).
  The ±1000 is the domain-shift allowance (D1→D2). Width must satisfy
  0 < hi−lo < 8000. **[lo,hi] = [gap,gap] is a tautology → KB2 FAIL.**
- No-harm predictions: genuine fix on B-RECALL/B-COST: delta ∈ [−750,+750].
  Wrong fix on B-RECALL: delta ∈ [−750,+750]; on D2: authored wrong-fix rule
  predicts delta ∈ [−2500, 0] (destroys distinctions → no help or harm).

**Predictions emitted (all published, hits AND misses):**
P1 genuine fix → B-QUANT-D2 delta [lo,hi] · P2 wrong fix → D2 delta [lo,hi] ·
P3 genuine → B-RECALL delta [−750,750] · P4 genuine → B-COST delta [−750,750] ·
P5 wrong → B-RECALL delta [−750,750].

## Crew phase (independent implementation)

The crew reads the emitted spec and implements it faithfully in a variant
binary — real quantifier logic (tag threaded through key construction,
compatibility decision procedure over all 9 quantifier pairs), NOT a
flag-flip. Same for the wrong fix (real tag normalization). The oracle
checks the variant source contains a 9-entry quantifier-compatibility table;
a flag-flip cannot pass this.

## Kill bars (mechanical oracle `verify_rsi2.py`)

| Bar | Rule |
|---|---|
| KB1-INVENT | emitted fix composition ∉ the 7 RSI-1 templates; variant source contains a 9-entry quantifier-compatibility table; else FAIL |
| KB2-CALIBRATE | actual D2 delta ∈ [lo,hi]; 0 < hi−lo < 8000; [lo,hi] ≠ [gap,gap]; ledger shows analogy cited + arithmetic; else FAIL |
| KB3-DISCRIMINATE | genuine: predicted lo > 500 AND actual delta > 500; wrong: predicted hi ≤ 500 AND actual delta ≤ 500 AND wrong actual < genuine actual; else FAIL (yes-machine) |
| KB4-NOSKIP | diagnose manifest (D1, RECALL, COST) all verdict-recorded; verify manifest (D2) all verdict-recorded; mode-0 output contains no D2 metric; else FAIL |
| KB5-DET | 5/5 byte-identical diagnose runs; 5/5 byte-identical verify runs per variant; else FAIL |
| KB6-HONEST | PREDICTIONS.json contains P1–P5; verdict reports each as HIT/MISS; else FAIL |

## What this does and does not claim (honesty clause)

Authored by the crew: the operator grammar, mechanism inventory, analogy
DB, deliberation scoring weights, range-mapping formula, battery facts.
The TNN's: diagnosing the weakness from its own measurements, scoring
candidate operators (logged), composing the novel fix, selecting the
analogy, emitting the range, inventing the wrong fix with its reason.
Calibration is tested on held-out data the recommender never saw. If the
range misses, the miss is published and the grade reflects it.
